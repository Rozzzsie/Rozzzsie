#!/usr/bin/env bash
# Post-edit reminder hook — Protocols 3.2
# Emits PostToolUse hookSpecificOutput JSON with P4/P5/P6 reminders after Edit|Write.
# Registered in .claude/settings.json so it fires in sessions started
# from any cwd. Cwd guard below ensures no-op outside this repo.
#
# Replaces the inline echo command that was previously in .claude/settings.json.
# Moving to a script file fixes the escape bug where \\n in the inline command
# rendered as literal backslash-n instead of real newlines.

set -euo pipefail

# --- Cwd guard (portable — requires git repo) ---
toplevel=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [[ -z "$toplevel" ]]; then
  exit 0
fi
cd "$toplevel"

# --- Scratch-path guard (2026-04-11, split 2026-04-13) ---
hook_input=$(cat)
file_path=$(jq -r '.tool_input.file_path // ""' <<< "$hook_input" 2>/dev/null || echo "")
if [[ "$file_path" == /tmp/* ]]; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": "CHECKPOINT BAR — append this line at the END of your next response:\n[checkpoint: P3 — <status> | P4 — <status> | P5 — <status>]\nThis is Tier 2. Stop-gate blocks without a ## Checkpoint bar section in your P3 trace."
    }
  }'
  exit 0
fi

# --- Emit full reminder ---
jq -n '{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "CHECKPOINT BAR — append this line at the END of your next response:\n[checkpoint: P3 — <status> | P4 — <status> | P5 — <status>]\nThis is Tier 2. Stop-gate blocks without a ## Checkpoint bar section in your P3 trace.\n---\nSUPERVISE LAYER — post-edit gate (HARD GATE):\nP4: Update CONTEXT.md + append CHANGELOG.md if this was a meaningful work increment.\nP5: Did anything surprise you? If yes, capture in LEARNINGS.md AND propagate to rules (update CLAUDE.md / output-checklist.md).\nP6: If the file you just edited is in personal-learnings/, P6 (cross-pollination) is specifically due — seed relevant workspace LEARNINGS.md files now."
  }
}'
