# private-names.sh — resolves the watch list for this repo's confidentiality guards.
# Sourced, never executed.
#
# WHY THE LIST IS NOT IN THIS FILE, OR ANYWHERE IN THIS REPO
#   This repo is PUBLIC. A guard that hard-codes the names it forbids publishes them:
#   the denylist becomes the disclosure it exists to prevent. So this file knows how to
#   FIND the list, which discloses nothing, and the list itself lives outside the
#   published tree.
#
#   The tell that this is the right shape: neither guard needs an entry in the other's
#   ALLOWLIST any more. A guard forced to exempt itself from its own rule is telling you
#   it is part of the problem.
#
# RESOLUTION ORDER
#   1. `git config rozzzsie.privateNamesFile` — machine-local, lives in .git/config,
#      never published. Set this if your layout differs from the default.
#   2. ../Rozzzsie/_config/private-workspace-names.txt — the sibling private repo.
#
# WHAT IT SETS
#   PRIVATE_NAMES_LIST    newline-delimited names, or empty
#   PRIVATE_NAMES_COUNT   integer, 0 when unresolved
#   PRIVATE_NAMES_SOURCE  the path it read, or empty
#
# THE CALLER'S OBLIGATION, AND IT IS NOT OPTIONAL
#   An unresolved list makes any caller match nothing and therefore pass everything —
#   the failure mode that is indistinguishable from success. Every caller MUST test
#   PRIVATE_NAMES_COUNT and choose its own direction explicitly:
#     pre-commit  -> fail CLOSED (block), because silence there is a published leak
#     commit-msg  -> warn, because it is warn-only by design
#   No caller may proceed quietly on a short list.

PRIVATE_NAMES_LIST=""
PRIVATE_NAMES_SOURCE=""
PRIVATE_NAMES_COUNT=0

_pn_path=$(git config --get rozzzsie.privateNamesFile 2>/dev/null || true)
[ -n "$_pn_path" ] || _pn_path="../Rozzzsie/_config/private-workspace-names.txt"

if [ -f "$_pn_path" ]; then
  # strip comments, blank lines and stray whitespace
  PRIVATE_NAMES_LIST=$(/usr/bin/grep -vE '^[[:space:]]*(#|$)' "$_pn_path" 2>/dev/null | tr -d ' \t' || true)
  PRIVATE_NAMES_SOURCE="$_pn_path"
  PRIVATE_NAMES_COUNT=$(printf '%s\n' "$PRIVATE_NAMES_LIST" | /usr/bin/grep -c . || true)
fi
PRIVATE_NAMES_COUNT=${PRIVATE_NAMES_COUNT:-0}

# Alternation for grep -E. Empty when unresolved; callers must not reach this.
# -E is mandatory downstream: BSD grep does not honour BRE \| and silently under-counts.
PRIVATE_NAMES_ALT=$(printf '%s' "$PRIVATE_NAMES_LIST" | tr '\n' '|')
PRIVATE_NAMES_ALT="${PRIVATE_NAMES_ALT%|}"

_pn_unresolved_msg() {
  echo ""
  echo "    watch list: ${PRIVATE_NAMES_COUNT} name(s) resolved from '${PRIVATE_NAMES_SOURCE:-<nothing>}'."
  echo "    Expected at least 3. The list lives OUTSIDE this repo by design, so a"
  echo "    missing private tree or a moved path disarms these guards entirely."
  echo ""
  echo "    Fix by pointing at it explicitly, once per clone:"
  echo "        git config rozzzsie.privateNamesFile /abs/path/to/private-workspace-names.txt"
  echo ""
}
