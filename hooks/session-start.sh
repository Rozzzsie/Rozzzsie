#!/usr/bin/env bash
# Session Start Hook — Protocols 3.2
# 1. Writes session-start timestamp (for session-scoped time window)
# 2. Writes session-start commit hash (for CONTEXT.md diff baseline — V-22 fix)
# 3. Computes P8 retrospective status (definitive verdict, no agent date math)

set -euo pipefail

# --- Cwd guard (portable — requires git repo) ---
toplevel=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [[ -z "$toplevel" ]]; then
  exit 0
fi
cd "$toplevel"

# --- Write session-start timestamp + commit hash ---
mkdir -p .claude
echo "$(date +%s)" > .claude/session-start
git rev-parse HEAD > .claude/session-start-commit 2>/dev/null || echo "none" > .claude/session-start-commit

# --- Compute P8 retrospective status ---
last_retro_line=$(grep -i 'retrospective' CHANGELOG.md 2>/dev/null | head -1 || true)

if [[ -z "$last_retro_line" ]]; then
  echo "SUPERVISE LAYER — session start check:"
  echo "P8 RETRO STATUS: OVERDUE (no retrospective entry found in CHANGELOG.md). Run weekly retrospective before starting any work."
  exit 0
fi

last_retro_date=$(echo "$last_retro_line" | grep -oE '\[([0-9]{4}-[0-9]{2}-[0-9]{2})\]' | tr -d '[]' | head -1)

if [[ -z "$last_retro_date" ]]; then
  echo "SUPERVISE LAYER — session start check:"
  echo "P8 RETRO STATUS: OVERDUE (could not parse last retrospective date). Run weekly retrospective before starting any work."
  exit 0
fi

if [[ "$(uname)" == "Darwin" ]]; then
  last_retro_epoch=$(date -j -f "%Y-%m-%d" "$last_retro_date" +%s 2>/dev/null || echo "0")
else
  last_retro_epoch=$(date -d "$last_retro_date" +%s 2>/dev/null || echo "0")
fi

now_epoch=$(date +%s)
days_elapsed=$(( (now_epoch - last_retro_epoch) / 86400 ))

if [[ "$(uname)" == "Darwin" ]]; then
  next_retro_date=$(date -j -v+7d -f "%Y-%m-%d" "$last_retro_date" "+%Y-%m-%d" 2>/dev/null || echo "unknown")
else
  next_retro_date=$(date -d "$last_retro_date + 7 days" "+%Y-%m-%d" 2>/dev/null || echo "unknown")
fi

echo "SUPERVISE LAYER — session start check:"

if [[ "$days_elapsed" -ge 7 ]]; then
  echo "P8 RETRO STATUS: OVERDUE (last retro: ${last_retro_date}, ${days_elapsed} days ago). Run weekly retrospective before starting any work."
else
  echo "P8 RETRO STATUS: NOT DUE (last retro: ${last_retro_date}, ${days_elapsed} days ago). Next retro due ${next_retro_date}."
fi

cat << 'DIGEST'

PROTOCOL DIGEST — Tier 1 critical rules (backstop; full doc: _config/agent-protocols.md):
READ THE FULL PROTOCOLS DOC as startup step 6. Confirm with one specific detail in your briefing.

P1  (Tier 2): Confirm intent (what/why/scope/approach) before non-trivial work. Log [P1] to .claude/session-log.md.
P2  (Tier 3): Stop at 3 failed attempts. Check for rhyming failures at 2 — same axis = reframe, don't retry. Log [P2] or [P2-rhyme].
P3  (Tier 1): Write .claude/p3-trace.md with section verdicts + evidence (>=40 chars each). Stop hook blocks on missing/stale/thin traces.
P4  (Tier 1): Update CONTEXT.md + CHANGELOG.md immediately after every meaningful edit.
              VERIFICATION RULE: before writing any claim about external state (API keys, credentials,
              file contents, test results) into a state file, verify it directly — read the file, run
              the command. Do NOT infer external state from conversation history.
P5  (Tier 2): Two steps — (1) capture surprises in LEARNINGS.md, (2) propagate to CLAUDE.md/checklist rules.
              A learning only in LEARNINGS.md is an observation, not an iteration. Log [P5] to session-log.md.
P6  (Tier 3): After logging to a personal or lightweight workspace LEARNINGS file, seed relevant workspace LEARNINGS files immediately.
P7  (Tier 1): Commit + push before closing. Stop hook blocks on: uncommitted changes, unpushed commits,
              stale state files, short CHANGELOG entries, no-diff CONTEXT.md, missing p3-trace, missing session-log entries.
DIGEST
