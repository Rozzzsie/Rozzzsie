#!/usr/bin/env bash
# P7 Hard Gate — Protocols 3.2
# Checks real git/file state before allowing session close.
# Outputs valid Stop hook JSON: decision "block" or "approve" with reason.
#
# Changes from 3.0:
# - P3 trace artifact check (V-03)
# - CHANGELOG minimum entry length (V-02)
# - CONTEXT.md diff validation (V-02)
# - Workspace-scoped state file checks (V-12)
# - Session-scoped time window (V-09)
# - Untracked productive file warning (V-19)

set -euo pipefail

toplevel=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [[ -z "$toplevel" ]]; then
  printf '{"decision":"approve","reason":"Not in a git repo — P7 N/A"}\n'
  exit 0
fi
cd "$toplevel"

source hooks/lib/workspace-tier.sh

block() {
  local reason="$1"
  printf '{"decision":"block","reason":"%s"}\n' "$reason"
  exit 0
}

approve() {
  local reason="${1:-P7 complete — all checks passed}"
  printf '{"decision":"approve","reason":"%s"}\n' "$reason"
  exit 0
}

STATE_PATTERN='(CHANGELOG\.md|CONTEXT\.md|LEARNINGS\.md|CLAUDE\.md|^\.claude/|^_config/)'
WORKSPACES=$(get_all_workspaces)

if [[ -f .claude/session-start ]]; then
  session_start=$(cat .claude/session-start)
  now=$(date +%s)
  age=$(( now - session_start ))
  if [[ "$age" -gt 86400 ]]; then
    session_fresh=false
    since_flag="--since=midnight"
    session_start="$now"
  else
    session_fresh=true
    since_flag="--since=@${session_start}"
  fi
else
  session_fresh=false
  session_start=$(date +%s)
  since_flag="--since=midnight"
fi

# Check 1: Uncommitted changes
uncommitted=$(git status --porcelain 2>/dev/null | grep -v '^??' | grep -v ' \.claude/insights-buffer\.md$' || true)
if [[ -n "$uncommitted" ]]; then
  file_list=$(echo "$uncommitted" | head -5 | awk '{print $2}' | tr '\n' ', ' | sed 's/,$//')
  total=$(echo "$uncommitted" | wc -l | tr -d ' ')
  if [[ "$total" -gt 5 ]]; then
    file_list="${file_list} (+$((total - 5)) more)"
  fi
  block "P7 BLOCK: Uncommitted changes — ${file_list}. Stage, commit, and push before closing."
fi

# Check 2: Unpushed commits
unpushed=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
if [[ "$unpushed" -gt 0 ]]; then
  block "P7 BLOCK: ${unpushed} unpushed commit(s). Run git push before closing."
fi

# Check 3: Was this a productive session?
if [[ "$session_fresh" == "true" ]] && [[ -f .claude/session-start-commit ]]; then
  candidate_baseline=$(cat .claude/session-start-commit)
  if git cat-file -t "$candidate_baseline" &>/dev/null; then
    session_files=$(git log "${candidate_baseline}..HEAD" --name-only --pretty=format:"" 2>/dev/null | sort -u | grep -v '^$' || true)
  else
    session_files=$(git log ${since_flag} --name-only --pretty=format:"" 2>/dev/null | sort -u | grep -v '^$' || true)
  fi
else
  session_files=$(git log ${since_flag} --name-only --pretty=format:"" 2>/dev/null | sort -u | grep -v '^$' || true)
fi

if [[ -z "$session_files" ]]; then
  approve "Read-only session — no commits this session. P7 not applicable."
fi

productive_files=$(echo "$session_files" | grep -v -E "${STATE_PATTERN}" || true)

if [[ -z "$productive_files" ]]; then
  root_state_touched=$(echo "$session_files" | grep -E '^(LEARNINGS\.md|CLAUDE\.md|_config/)' || true)
  if [[ -n "$root_state_touched" ]]; then
    root_changelog_in_commits=$(echo "$session_files" | grep -c '^CHANGELOG\.md$' || true)
    if [[ "$root_changelog_in_commits" -eq 0 ]]; then
      block "P7 BLOCK: Root state files committed but root CHANGELOG.md not updated this session."
    fi
  fi

  untracked_productive=$(git status --porcelain 2>/dev/null | grep '^??' | awk '{print $2}' | grep -v -E "${STATE_PATTERN}" | grep -v -E '(^\.claude/|^_config/|^_input/)' || true)
  if [[ -n "$untracked_productive" ]]; then
    untracked_count=$(echo "$untracked_productive" | wc -l | tr -d ' ')
    untracked_list=$(echo "$untracked_productive" | head -3 | tr '\n' ', ' | sed 's/,$//')
    approve "State-only session — but ${untracked_count} untracked productive file(s) detected: ${untracked_list}. Verify these are intentional WIP."
  fi
  approve "State-only session — no productive file commits this session. P7 not applicable."
fi

# Check 4: State files updated (workspace-scoped)
workspace_hits=""
root_productive=""

for f in $productive_files; do
  matched=false
  for ws in $WORKSPACES; do
    if echo "$f" | grep -q "^${ws}/" ; then
      if ! echo "$workspace_hits" | grep -q "$ws"; then
        workspace_hits="${workspace_hits} ${ws}"
      fi
      matched=true
      break
    fi
  done
  if [[ "$matched" == "false" ]]; then
    root_productive="yes"
  fi
done

if [[ "$root_productive" == "yes" ]]; then
  has_root_changelog=$(echo "$session_files" | grep -c '^CHANGELOG\.md$' || true)
  has_root_context=$(echo "$session_files" | grep -c '^CONTEXT\.md$' || true)
  if [[ "$has_root_changelog" -eq 0 ]]; then
    block "P7 BLOCK: Root-level productive files committed but root CHANGELOG.md not updated."
  fi
  if [[ "$has_root_context" -eq 0 ]]; then
    block "P7 BLOCK: Root-level productive files committed but root CONTEXT.md not updated."
  fi
fi

for ws in $workspace_hits; do
  if requires_changelog "$ws"; then
    ws_changelog=$(echo "$session_files" | grep -c "^${ws}/CHANGELOG\.md$" || true)
    if [[ "$ws_changelog" -eq 0 ]]; then
      block "P7 BLOCK: Productive files in ${ws}/ but ${ws}/CHANGELOG.md not updated."
    fi
  fi
  if requires_context "$ws"; then
    ws_context=$(echo "$session_files" | grep -c "^${ws}/CONTEXT\.md$" || true)
    if [[ "$ws_context" -eq 0 ]]; then
      block "P7 BLOCK: Productive files in ${ws}/ but ${ws}/CONTEXT.md not updated."
    fi
  fi
done

# Check 5: CHANGELOG entry quality
# Assumes bottom-append CHANGELOG format (newest entry = last non-header line).
# Reverse-chronological (newest-at-top) layouts would need head -1 instead of tail -1.
changelogs_to_check="CHANGELOG.md"
for ws in $workspace_hits; do
  changelogs_to_check="${changelogs_to_check} ${ws}/CHANGELOG.md"
done

for cl in $changelogs_to_check; do
  if [[ -f "$cl" ]]; then
    newest_entry=$(grep -v '^$' "$cl" | grep -v '^#' | grep -v '^---' | grep -v '^\*' | grep -v '^<!--' | tail -1 || true)
    entry_len=${#newest_entry}
    if [[ "$entry_len" -lt 30 ]]; then
      block "P7 BLOCK: Newest entry in ${cl} is too short (${entry_len} chars, minimum 30)."
    fi
  fi
done

# Check 6: CONTEXT.md has substantive changes
if [[ -f .claude/session-start-commit ]]; then
  baseline_commit=$(cat .claude/session-start-commit)
  if ! git cat-file -t "$baseline_commit" &>/dev/null; then
    baseline_commit="HEAD~1"
  fi
else
  baseline_commit="HEAD~1"
fi

for ws in $workspace_hits; do
  if ! requires_context "$ws"; then
    continue
  fi
  context_file="${ws}/CONTEXT.md"
  if [[ -f "$context_file" ]]; then
    context_diff=$(git diff "${baseline_commit}" -- "$context_file" 2>/dev/null | grep -E '^\+[^+]|^-[^-]' | grep -v -E '^\+\s*$|^-\s*$' || true)
    if [[ -z "$context_diff" ]]; then
      block "P7 BLOCK: ${context_file} has no substantive changes since session start."
    fi
  fi
done

if [[ "$root_productive" == "yes" ]] && [[ -f "CONTEXT.md" ]]; then
  context_diff=$(git diff "${baseline_commit}" -- CONTEXT.md 2>/dev/null | grep -E '^\+[^+]|^-[^-]' | grep -v -E '^\+\s*$|^-\s*$' || true)
  if [[ -z "$context_diff" ]]; then
    block "P7 BLOCK: Root CONTEXT.md has no substantive changes since session start."
  fi
fi

# Check 7: P3 trace artifact
if [[ -n "$productive_files" ]]; then
  if [[ ! -f .claude/p3-trace.md ]]; then
    block "P7 BLOCK: Productive session but .claude/p3-trace.md not found."
  fi

  if [[ -f .claude/session-start ]]; then
    p3_mtime=$(stat -f %m .claude/p3-trace.md 2>/dev/null || stat -c %Y .claude/p3-trace.md 2>/dev/null || echo "0")
    if [[ "$p3_mtime" -lt "$session_start" ]]; then
      block "P7 BLOCK: .claude/p3-trace.md is stale (older than session start)."
    fi
  fi

  has_sections=$(grep -cE 'Section [0-9]|section [0-9]|\b[Ss]ections?: [0-9]' .claude/p3-trace.md 2>/dev/null || true)
  if [[ "$has_sections" -eq 0 ]]; then
    block "P7 BLOCK: .claude/p3-trace.md contains no section references."
  fi

  has_verdicts=$(grep -ciE '(PASS|FAIL)' .claude/p3-trace.md 2>/dev/null || true)
  if [[ "$has_verdicts" -eq 0 ]]; then
    block "P7 BLOCK: .claude/p3-trace.md has no PASS/FAIL verdicts."
  fi

  short_verdicts=$(grep -iE '(PASS|FAIL)' .claude/p3-trace.md 2>/dev/null | awk 'length < 40' | head -5 || true)
  if [[ -n "$short_verdicts" ]]; then
    block "P7 BLOCK: .claude/p3-trace.md has verdict lines under 40 chars — evidence required."
  fi

  file_ref_found=false
  for pf in $productive_files; do
    basename_pf=$(basename "$pf")
    if grep -qF "$basename_pf" .claude/p3-trace.md 2>/dev/null; then
      file_ref_found=true
      break
    fi
  done
  if [[ "$file_ref_found" == "false" ]]; then
    block "P7 BLOCK: .claude/p3-trace.md does not reference any productive file from this session."
  fi
fi

# Check 7b: Checkpoint bar section
if [[ -n "$productive_files" ]] && [[ -f .claude/p3-trace.md ]]; then
  has_checkpoint_bar=$(grep -c '^## Checkpoint bar' .claude/p3-trace.md 2>/dev/null || true)
  if [[ "$has_checkpoint_bar" -eq 0 ]]; then
    block "P7 BLOCK: .claude/p3-trace.md has no '## Checkpoint bar' section."
  fi
fi

# Check 8: Session log
if [[ -n "$productive_files" ]]; then
  if [[ ! -f .claude/session-log.md ]]; then
    block "P7 BLOCK: Productive session but .claude/session-log.md not found."
  fi

  last_session_start_line=$(grep -n '^# Session Log' .claude/session-log.md 2>/dev/null | tail -1 | cut -d: -f1)
  if [[ -n "$last_session_start_line" ]]; then
    current_session_log=$(tail -n +"$last_session_start_line" .claude/session-log.md)
  else
    current_session_log=$(cat .claude/session-log.md)
  fi

  has_p1=$(echo "$current_session_log" | grep -c '^\[P1\]' || true)
  has_p5=$(echo "$current_session_log" | grep -c '^\[P5\]' || true)

  if [[ "$has_p1" -eq 0 ]]; then
    block "P7 BLOCK: No [P1] entry for current session."
  fi
  if [[ "$has_p5" -eq 0 ]]; then
    block "P7 BLOCK: No [P5] entry for current session."
  fi

  productive_count=$(echo "$productive_files" | wc -l | tr -d ' ')
  if [[ "$productive_count" -ge 3 ]]; then
    has_p1_confirmed=$(echo "$current_session_log" | grep -c '^\[P1\] confirmed' || true)
    if [[ "$has_p1_confirmed" -eq 0 ]]; then
      block "P7 BLOCK: ${productive_count} productive files but no [P1] confirmed entry."
    fi
  fi

  has_p2=$(echo "$current_session_log" | grep -c '^\[P2\]' || true)
  if [[ "$has_p2" -gt 0 ]]; then
    p5_no_surprises=$(echo "$current_session_log" | grep -c '^\[P5\] no surprises' || true)
    p5_captured=$(echo "$current_session_log" | grep -c '^\[P5\] captured' || true)
    if [[ "$p5_no_surprises" -gt 0 ]] && [[ "$p5_captured" -eq 0 ]]; then
      block "P7 BLOCK: [P2] triggered but [P5] says 'no surprises.'"
    fi
  fi

  has_p5_propagated=$(echo "$current_session_log" | grep -c '^\[P5\] propagated' || true)
  if [[ "$has_p5_propagated" -gt 0 ]]; then
    propagation_target_committed=false
    for sf in $session_files; do
      if echo "$sf" | grep -qE '(CLAUDE\.md|output-checklist\.md|LEARNINGS\.md)$'; then
        propagation_target_committed=true
        break
      fi
    done
    if [[ "$propagation_target_committed" == "false" ]]; then
      block "P7 BLOCK: [P5] propagated claimed but no propagation target committed."
    fi
  fi
fi

# Check 9: External validation for public-facing output
if [[ -n "$productive_files" ]] && [[ -f .claude/p3-trace.md ]]; then
  output_type=$(grep -i 'output type' .claude/p3-trace.md 2>/dev/null | head -1 || true)
  if echo "$output_type" | grep -qiE '(public|plugin|github|confluence|client|external)'; then
    has_external_validation=$(grep -ci 'external validation' .claude/p3-trace.md 2>/dev/null || true)
    if [[ "$has_external_validation" -eq 0 ]]; then
      block "P7 BLOCK: Public-facing output declared but no 'External validation' section in p3-trace."
    fi
  fi
fi

# Check 10: P8 retro enforcement
last_retro_line=$(grep -n 'retrospective' CHANGELOG.md 2>/dev/null | tail -1 || true)
if [[ -n "$last_retro_line" ]]; then
  last_retro_date=$(echo "$last_retro_line" | grep -oE '\[20[0-9]{2}-[0-9]{2}-[0-9]{2}\]' | head -1 | tr -d '[]' || true)
  if [[ -n "$last_retro_date" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
      retro_epoch=$(date -j -f "%Y-%m-%d" "$last_retro_date" +%s 2>/dev/null || echo "0")
    else
      retro_epoch=$(date -d "$last_retro_date" +%s 2>/dev/null || echo "0")
    fi
    now_epoch=$(date +%s)
    retro_age_days=$(( (now_epoch - retro_epoch) / 86400 ))
    if [[ "$retro_age_days" -gt 14 ]]; then
      block "P7 BLOCK: Last retrospective was ${retro_age_days} days ago. Grace period is 14 days."
    fi
  fi
else
  changelog_entries=$(grep -cE '^\[20[0-9]{2}' CHANGELOG.md 2>/dev/null || true)
  if [[ "$changelog_entries" -gt 7 ]]; then
    block "P7 BLOCK: No retrospective entry found but ${changelog_entries} entries exist."
  fi
fi

approve
