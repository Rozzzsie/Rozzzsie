# Hooks

The enforcement layer. These scripts are what make the protocols mechanical instead of aspirational.

| Hook | Event | What it does | Protocols enforced |
|------|-------|--------------|-------------------|
| `session-start.sh` | `SessionStart` | Writes session-start timestamp + baseline commit hash; computes P8 retro status | P8 |
| `post-edit-reminder.sh` | `PostToolUse:Edit\|Write` | Injects the checkpoint-bar and state-update reminder after every edit | P3 (checkpoint), P4 (state), P5 (learning) |
| `bash-write-reminder.sh` | `PostToolUse:Bash` | Lightweight nudge to check whether a Bash write needs state capture | P4 |
| `stop-gate.sh` | `Stop` | Hard gate. Blocks session-close on protocol failures: missing checkpoint bar, unupdated state files, untracked productive files, stale CHANGELOG | P3, P4, P7 |
| `insights-capture.py` | `Stop` | Parses the session transcript for `★ Insight ─...` cards and appends deduped entries to `.claude/insights-buffer.md` for P8 audit | P5, P8 |
| `lib/workspace-tier.sh` | (sourced) | Single source of truth for workspace list + tier semantics. Sourced by `stop-gate.sh` and the pre-commit hook so both reach the same layer. | — |

## The shape

Three invariants hold across all hooks:

1. **Cwd guard** — every hook runs `git rev-parse --show-toplevel` and exits cleanly if not in the repo, so sessions opened in subdirectories don't trigger partial enforcement.
2. **Fail closed, not silently** — the stop-gate blocks session-close with a named reason. There is no silent success path for a protocol miss.
3. **Hooks only gate on state they don't manage** — the insights-capture hook writes to `.claude/insights-buffer.md`; the stop-gate explicitly excludes that path from its "uncommitted state" check. A hook that gates on its own writes livelocks itself.

## Settings

`.claude/settings.json` wires the scripts into Claude Code's hook matrix. Paths are repo-relative; Claude Code normalizes them against the session's working directory.
