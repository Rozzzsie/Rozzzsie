#!/usr/bin/env bash
# check-msg-no-private-paths.sh — commit-MESSAGE guard for the public repo. WARN-ONLY.
#
# WHY THIS EXISTS
#   check-no-private-paths.sh reads the staged SET: paths and file content. A commit
#   message is neither, so it passes through that guard untouched — and a message is
#   as permanent and as public as the diff. The repo's own history carries the proof:
#   the commit that REMEDIATED an earlier leak itemised, in its message, every private
#   file it had just removed.
#
# WHY IT WARNS AND DOES NOT BLOCK
#   `git commit --no-verify` skips pre-commit AND commit-msg — one switch, both guards.
#   A blocking version here would mean the override you reach for also disarms the
#   staged-content guard, and the commits most likely to trip this one are the commits
#   DOING confidentiality work. That is exactly when you least want the other guard off.
#   Warning costs one look and couples nothing.
#
# WHY IT NAMES NOTHING
#   The watch list is derived from .gitignore at runtime. This repo is PUBLIC, so a
#   hard-coded list would publish the very names the guard exists to keep out of it.
#   .gitignore must name them to function; nothing else here has to.
#
# SCOPE — what this does NOT do
#   It matches name strings in the message text, not meaning. It never blocks, and it
#   is not a review. A silent run means "no watched name appeared", never "safe".

set -uo pipefail

MSG_FILE="${1:-}"
[ -n "$MSG_FILE" ] && [ -f "$MSG_FILE" ] || exit 0

# --- derive the watch list from .gitignore's private block --------------------
# git runs hooks with cwd = repo root, so the bare path resolves. Bounded read: from
# the marker comment to the first blank line. Entries starting with '.' or '#' are
# skipped, so tooling ignores in the same block are not treated as workspace names.
NAMES=$(awk '
  /^# Private workspaces/            { inblock = 1; next }
  inblock && /^[[:space:]]*$/        { exit }
  inblock && /^[^.#].*\/$/           { sub(/\/$/, ""); print }
' .gitignore 2>/dev/null || true)

count=$(printf '%s\n' "$NAMES" | /usr/bin/grep -c . || true)

# An empty or short list would make this hook pass EVERYTHING — the failure mode that
# looks exactly like success. Say so out loud rather than exiting 0 in silence.
if [ "${count:-0}" -lt 3 ]; then
  {
    echo ""
    echo "⚠️  check-msg-no-private-paths: derived only ${count:-0} name(s) from .gitignore."
    echo "    Expected at least 3. The watch list is unreliable, so THIS GUARD IS NOT"
    echo "    COVERING YOU on this commit. Check the '# Private workspaces' block."
    echo ""
  } >&2
  exit 0
fi

# --- scan the message, minus the comment lines git strips ---------------------
# -E is mandatory: BSD grep does not honour BRE \| alternation and silently under-counts.
alt=$(printf '%s' "$NAMES" | tr '\n' '|'); alt="${alt%|}"
hits=$(/usr/bin/grep -vE '^#' "$MSG_FILE" | /usr/bin/grep -nE "(${alt})" || true)

if [ -n "$hits" ]; then
  {
    echo ""
    echo "⚠️  WARNING — this commit message names a private workspace, and this repo is PUBLIC."
    echo ""
    echo "$hits" | sed 's/^/    /'
    echo ""
    echo "    NOT blocked, and nothing is wrong with the commit itself. But a message is"
    echo "    permanent and public, and check-no-private-paths.sh never reads messages."
    echo "    If the name is not load-bearing, describe the CLASS instead of the instance:"
    echo ""
    echo "        git commit --amend"
    echo ""
  } >&2
fi

exit 0
