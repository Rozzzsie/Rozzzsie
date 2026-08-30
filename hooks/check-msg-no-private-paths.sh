#!/usr/bin/env bash
# check-msg-no-private-paths.sh — commit-MESSAGE guard for the public repo. WARN-ONLY.
#
# WHY THIS EXISTS
#   check-no-private-paths.sh reads the staged set: paths and file content. A commit
#   message is neither, so it passes that guard untouched — and a message is as
#   permanent and as public as the diff. This repo's own history carries the proof:
#   the commit that REMEDIATED an earlier leak itemised, in its message, every private
#   file it had just removed, and closed with a zero-remaining verification claim that
#   was true of tracked content and false of the message asserting it.
#
# WHY IT WARNS AND DOES NOT BLOCK
#   `git commit --no-verify` skips pre-commit AND commit-msg — one switch, both guards.
#   A blocking version here would mean the override you reach for also disarms the
#   staged-content guard, and the commits most likely to trip a message check are the
#   commits DOING confidentiality work. That is precisely when you least want the other
#   guard off. Warning costs one look and couples nothing.
#
# WHY IT NAMES NOTHING
#   The watch list resolves at runtime from outside this repo (hooks/lib/private-names.sh).
#   This repo is PUBLIC, so a hard-coded list would publish the very names the guard
#   exists to keep out of it.
#
# SCOPE — what this does NOT do
#   It matches name strings in the message text, not meaning. It never blocks, and it is
#   not a review. A silent run means "no watched name appeared", never "safe".

set -uo pipefail

MSG_FILE="${1:-}"
[ -n "$MSG_FILE" ] && [ -f "$MSG_FILE" ] || exit 0

# git runs hooks with cwd = repo root, so the bare path resolves.
# shellcheck source=lib/private-names.sh
. hooks/lib/private-names.sh

# An unresolved list cannot be scanned against. Warn-only means this hook may not
# block, so it says plainly that it is not covering you rather than exiting quietly.
if [ "${PRIVATE_NAMES_COUNT:-0}" -lt 3 ]; then
  {
    echo ""
    echo "⚠️  check-msg-no-private-paths: THIS GUARD IS NOT COVERING THIS COMMIT."
    _pn_unresolved_msg
  } >&2
  exit 0
fi

# Scan the message, minus the comment lines git strips.
# -E is mandatory: BSD grep does not honour BRE \| alternation and silently under-counts.
hits=$(/usr/bin/grep -vE '^#' "$MSG_FILE" | /usr/bin/grep -nE "(${PRIVATE_NAMES_ALT})" || true)

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
