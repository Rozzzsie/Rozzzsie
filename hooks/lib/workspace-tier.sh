#!/usr/bin/env bash
# Shared helper: workspace tier resolution (v3.3.1)
# Sourced by: hooks/stop-gate.sh and _config/hooks/pre-commit
# Both callers cd to the repo root before sourcing, so paths are repo-relative.
#
# Schema (.claude/workspaces.conf):
#   Format: name:tier   where tier ∈ { full, lightweight }
#   - full        → require CHANGELOG + CONTEXT when productive files committed
#   - lightweight → require CHANGELOG only (CONTEXT optional — snapshot, not per-change state)
#   Legacy bare-name lines resolve to "full" for backward compat.
#   Comment lines (#) and blank lines ignored.
#
# Fallback: if workspaces.conf is missing, auto-discover workspaces by finding
# directories containing a CONTEXT.md. Auto-discovered workspaces default to "full".

_WORKSPACES_CONF=".claude/workspaces.conf"

_parse_workspaces_conf() {
  if [[ -f "$_WORKSPACES_CONF" ]]; then
    grep -v '^#' "$_WORKSPACES_CONF" | grep -v '^$'
  else
    find . -maxdepth 2 -name 'CONTEXT.md' -not -path './CONTEXT.md' 2>/dev/null \
      | sed 's|^\./||' \
      | sed 's|/CONTEXT\.md$||' \
      | sed 's|$|:full|'
  fi
}

get_all_workspaces() {
  _parse_workspaces_conf | cut -d: -f1 | tr '\n' ' '
}

get_workspace_tier() {
  local ws="$1"
  local line
  line=$(_parse_workspaces_conf | grep -E "^${ws}(:|$)" | head -1)
  if [[ -z "$line" ]]; then
    echo "unknown"
    return 1
  fi
  if [[ "$line" == *:* ]]; then
    local tier="${line#*:}"
    case "$tier" in
      full|lightweight) echo "$tier" ;;
      *) echo "full" ;;
    esac
  else
    echo "full"
  fi
}

requires_context() {
  local ws="$1"
  local tier
  tier=$(get_workspace_tier "$ws") || return 1
  case "$tier" in
    full) return 0 ;;
    lightweight) return 1 ;;
    *) return 0 ;;
  esac
}

requires_changelog() {
  local ws="$1"
  local tier
  tier=$(get_workspace_tier "$ws") || return 1
  case "$tier" in
    full|lightweight) return 0 ;;
    *) return 0 ;;
  esac
}
