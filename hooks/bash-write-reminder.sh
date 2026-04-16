#!/usr/bin/env bash
# Bash file-write heuristic hook — Protocols 3.2 (V-3.2-003 mitigation)
# Fires on PostToolUse:Bash. Checks if the Bash command likely wrote files.
# If it did, emits the same P4/P5/P6 reminder as post-edit-reminder.sh.
#
# This is a heuristic — false negatives exist for novel write patterns.
# The goal is to catch the most common bypass routes (>, >>, tee, sed -i,
# cp, mv) without being noisy on read-only commands (git, ls, npm).

set -euo pipefail

# --- Cwd guard (portable — requires git repo) ---
toplevel=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [[ -z "$toplevel" ]]; then
  exit 0
fi
cd "$toplevel"

# --- Read hook input ---
hook_input=$(cat)
command_str=$(jq -r '.tool_input.command // ""' <<< "$hook_input" 2>/dev/null || echo "")

# Empty command — nothing to check
if [[ -z "$command_str" ]]; then
  exit 0
fi

# --- Heuristic: did this command likely write files? ---
if echo "$command_str" | grep -qE '^git '; then
  exit 0
fi

# Check for file-write indicators
write_detected=false
if echo "$command_str" | grep -qE '[^<]>>?\s'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\btee\b'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\bsed\s+-i'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\bcp\s'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\bmv\s'; then
  write_detected=true
elif echo "$command_str" | grep -qE 'cat\s*<<'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\bpython3?\b.*\bwrite\b'; then
  write_detected=true
elif echo "$command_str" | grep -qE '\bchmod\b|\bchown\b'; then
  write_detected=true
fi

if [[ "$write_detected" == "false" ]]; then
  exit 0
fi

# --- Scratch-path guard ---
if echo "$command_str" | grep -qE '>\s*/tmp/|tee\s+/tmp/|cp\s+.*\s+/tmp/'; then
  exit 0
fi

# --- Emit reminder (same as post-edit-reminder.sh) ---
jq -n '{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "SUPERVISE LAYER — Bash file-write detected (V-3.2-003 heuristic):\nP4: Update CONTEXT.md + append CHANGELOG.md if this was a meaningful work increment.\nP5: Did anything surprise you? If yes, capture in LEARNINGS.md AND propagate to rules.\nP6: If the write target is in a personal or lightweight workspace, P6 (cross-pollination) is due.\nThis is a heuristic — if this was a false positive (no actual file write), ignore."
  }
}'
