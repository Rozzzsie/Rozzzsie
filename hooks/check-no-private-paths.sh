#!/usr/bin/env bash
# check-no-private-paths.sh — commit-time guard for the public repo.
#
# WHY THIS EXISTS
#   This repo is the public track. Private workspaces live one directory up, in a
#   separate repo. The .gitignore blocks whole private directories from syncing in;
#   it does NOT catch private PATHS quoted inside an otherwise-legitimate file
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
# SCOPE — what this does NOT do
#   It matches PATH STRINGS, not meaning. Private content pasted without a path is
#   invisible to it. This is a tripwire for the mechanical misroute (the failure with
#   real history here), not a content classifier. Do not read a pass as "sanitized".

set -uo pipefail

# Private workspace directory names. These already appear in this repo's .gitignore,
# so listing them here discloses nothing new.
PRIVATE_NAMES=(
  "career-move-2026"
  "personal-learnings"
  "personal-ventures"
  "external-track-ramp"
)

# Files that legitimately NAME the private workspaces in order to exclude them.
# Deliberately tiny: every entry here is coverage removed. Add one only with a reason.
ALLOWLIST=(
  ".gitignore"
  "hooks/check-no-private-paths.sh"
)

staged=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$staged" ] && exit 0

violations=""

for f in $staged; do
  skip=0
  for a in "${ALLOWLIST[@]}"; do
    [ "$f" = "$a" ] && skip=1 && break
  done
  [ "$skip" -eq 1 ] && continue

  # (1) the staged PATH itself sits under a private name
  for n in "${PRIVATE_NAMES[@]}"; do
    case "$f" in
      *"$n"/*|"$n"/*) violations="${violations}  PATH     ${f}  (under '${n}')"$'\n' ;;
    esac
  done

  # (2) staged CONTENT quotes a private workspace as a path segment.
  # -E is mandatory: BSD grep does not honour BRE \| alternation and silently under-counts.
  alt=$(printf "%s|" "${PRIVATE_NAMES[@]}"); alt="${alt%|}"
  if hits=$(git show ":${f}" 2>/dev/null | /usr/bin/grep -nE "(workspaces/)?(${alt})/" 2>/dev/null); then
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
