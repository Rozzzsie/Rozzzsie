#!/usr/bin/env bash
# check-no-private-paths.sh — commit-time guard for the public repo.
#
# WHY THIS EXISTS
#   This repo is the public track. Private workspaces live one directory up, in a
#   separate repo. The ignore rules block whole private directories from syncing in;
#   they do NOT catch private PATHS quoted inside an otherwise-legitimate file
#   (a retro, a sidecar, a README, a CHANGELOG line). That is the gap this closes.
#
# WHY IT LIVES HERE AND NOT IN THE PRIVATE REPO'S pre-commit
#   Three separate git roots. The private repo's hook fires on private-repo commits,
#   where private content is legitimate — the check would be inert there. The commit
#   into THIS repo is the publication event, so this is the only place it can bind.
#
# PORTABILITY
#   Plain bash + git. No Claude Code dependency, no agent, no harness. Survives a
#   change of CLI, which is the point — the enforcement layer above it does not.
#
# THE WATCH LIST IS NOT IN THIS FILE, DELIBERATELY
#   It used to be, and that was the defect: this repo is PUBLIC, so a guard holding
#   the names it forbids publishes them. The list now resolves at runtime from outside
#   the published tree (see hooks/lib/private-names.sh). The tell that this is right is
#   the ALLOWLIST below — it is EMPTY, because nothing here needs exempting any more.
#
# SCOPE — what this does NOT do
#   It matches PATH STRINGS, not meaning. Private content pasted without a path is
#   invisible to it. This is a tripwire for the mechanical misroute (the failure with
#   real history here), not a content classifier. Do not read a pass as "sanitized".
#   It also reads only the STAGED set — anything already committed is never re-scanned,
#   and it never reads the commit MESSAGE. check-msg-no-private-paths.sh covers that.

set -uo pipefail

# git runs hooks with cwd = repo root, so the bare path resolves.
# shellcheck source=lib/private-names.sh
. hooks/lib/private-names.sh

# FAIL CLOSED. An unresolved list is a guard that cannot do its job, and on the
# publication path the safe answer is refusal, not silence.
#
# Note honestly what this check does and does not buy: with an empty list the
# alternation degenerates to "()", which matches everything, so the guard happens to
# over-trigger rather than under-trigger. That accident is not a design. This check
# makes the refusal explicit and gives a remedy instead of a wall of false hits.
if [ "${PRIVATE_NAMES_COUNT:-0}" -lt 3 ]; then
  {
    echo "⛔ BLOCKED — the private-workspace watch list did not resolve."
    _pn_unresolved_msg
    echo "    Or bypass this one commit if you are certain:  git commit --no-verify"
    echo "    (note that also skips the commit-msg guard)"
  } >&2
  exit 1
fi

# Files that legitimately name a private workspace and must be exempt.
# EMPTY, and that is the point — see the header. Newline-delimited, not an array:
# bash 3.2 errors on ${arr[@]} for an empty array under `set -u`, which would block
# every commit for a reason that has nothing to do with confidentiality.
# Add an entry only with a stated reason; every entry is coverage removed.
ALLOWLIST=""

staged=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$staged" ] && exit 0

violations=""

for f in $staged; do
  if [ -n "$ALLOWLIST" ] && printf '%s\n' "$ALLOWLIST" | /usr/bin/grep -qxF "$f"; then
    continue
  fi

  # (1) the staged PATH itself sits under a private name.
  # Unanchored on the left, preserving the original glob semantics: over-triggering
  # here fails CLOSED, which is the direction this guard should err in.
  if printf '%s' "$f" | /usr/bin/grep -qE "(${PRIVATE_NAMES_ALT})/"; then
    violations="${violations}  PATH     ${f}"$'\n'
  fi

  # (2) staged CONTENT quotes a private workspace as a path segment.
  # -E is mandatory: BSD grep does not honour BRE \| alternation and silently under-counts.
  if hits=$(git show ":${f}" 2>/dev/null | /usr/bin/grep -nE "(workspaces/)?(${PRIVATE_NAMES_ALT})/" 2>/dev/null); then
    while IFS= read -r line; do
      [ -n "$line" ] && violations="${violations}  CONTENT  ${f}:${line}"$'\n'
    done <<< "$hits"
  fi
done

if [ -n "$violations" ]; then
  echo "⛔ BLOCKED — private-workspace reference staged for the PUBLIC repo." >&2
  echo "" >&2
  echo "$violations" >&2
  echo "This repo is published. A private path committed here is public permanently," >&2
  echo "and history rewriting is not a remedy once it has been pushed." >&2
  echo "" >&2
  echo "If a hit is legitimate, sanitize the reference — do NOT add to the allowlist" >&2
  echo "without a stated reason; every allowlist entry is coverage removed." >&2
  echo "Override for a genuine false positive:  git commit --no-verify" >&2
  exit 1
fi

exit 0
