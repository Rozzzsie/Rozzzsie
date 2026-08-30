# Hooks

The enforcement layer. These scripts are what make the protocols mechanical instead of aspirational.

| Hook | Event | What it does | Protocols enforced |
|------|-------|--------------|-------------------|
| `session-start.sh` | `SessionStart` | Writes session-start timestamp + baseline commit hash; computes P8 retro status | P8 |
| `post-edit-reminder.sh` | `PostToolUse:Edit\|Write` | Injects the checkpoint-bar and state-update reminder after every edit | P3 (checkpoint), P4 (state), P5 (learning) |
| `bash-write-reminder.sh` | `PostToolUse:Bash` | Lightweight nudge to check whether a Bash write needs state capture | P4 |
| `stop-gate.sh` | `Stop` | Hard gate. Blocks session-close on protocol failures: missing checkpoint bar, unupdated state files, untracked productive files, stale CHANGELOG | P3, P4, P7 |
| `insights-capture.py` | `Stop` | Parses the session transcript for `★ Insight ─...` cards and appends deduped entries to `.claude/insights-buffer.md` for P8 audit | P5, P8 |
| `lib/workspace-tier.sh` | (sourced) | Single source of truth for workspace list + tier semantics. `stop-gate.sh` is its only consumer here. The git `pre-commit` hook deliberately does *not* source it — that hook is plain bash + git with no dependency on this layer, which is what lets it survive a change of CLI. | — |

## The shape

Three invariants hold across all hooks:

1. **Cwd guard** — every hook runs `git rev-parse --show-toplevel` and exits cleanly if not in the repo, so sessions opened in subdirectories don't trigger partial enforcement.
2. **Fail closed, not silently** — the stop-gate blocks session-close with a named reason. There is no silent success path for a protocol miss.
3. **Hooks only gate on state they don't manage** — the insights-capture hook writes to `.claude/insights-buffer.md`; the stop-gate explicitly excludes that path from its "uncommitted state" check. A hook that gates on its own writes livelocks itself.

## Settings

`.claude/settings.json` wires the scripts into Claude Code's hook matrix. Paths are repo-relative; Claude Code normalizes them against the session's working directory.

## Git hooks — a separate mechanism

`check-no-private-paths.sh` is **not** a Claude Code hook. It is a git `pre-commit` hook,
wired by a symlink rather than by `.claude/settings.json`, and it runs on plain bash + git
with no agent or harness dependency — deliberately, so the guard survives a change of CLI
while the enforcement layer above it does not.

| Hook | Event | What it does | On a hit | If the list won't resolve |
|------|-------|--------------|----------|---------------------------|
| `check-no-private-paths.sh` | git `pre-commit` | Reads the staged set — paths and file content. | **blocks** | **blocks** (fails closed) |
| `check-msg-no-private-paths.sh` | git `commit-msg` | Reads the commit message. | **warns** | **warns** |
| `lib/private-names.sh` | (sourced) | Resolves the watch list. Knows how to *find* it, never what is on it. | — | sets a zero count |

**Neither hook contains the names it guards.** This repo is public, so a guard holding
the names it forbids publishes them — the denylist becomes the disclosure it exists to
prevent. The list lives outside this tree entirely; `lib/private-names.sh` resolves it
at runtime, in this order:

1. `git config rozzzsie.privateNamesFile` — machine-local, in `.git/config`, unpublished
2. `../Rozzzsie/_config/private-workspace-names.txt` — the sibling private repo

The tell that this shape is right: `check-no-private-paths.sh`'s `ALLOWLIST` is now
**empty**. It used to exempt `.gitignore` and itself, because both named the private
workspaces. A guard forced to exempt itself from its own rule is telling you it is part
of the problem.

**Why one blocks and one warns.** `git commit --no-verify` skips *both* hooks — one
switch, both guards. A blocking message check would mean the override you reach for
also disarms the staged-content check, and the commits most likely to trip the message
check are the commits *doing* confidentiality work. That is exactly when you least want
the other guard off. The message hook therefore warns and exits `0`, always.

**A clone installs none of this** — not the symlinks, not the local ignore rules, not
the list. `.git/` is not part of the repository. One-time setup, from the repo root:

```sh
ln -sfn ../../hooks/check-no-private-paths.sh     .git/hooks/pre-commit
ln -sfn ../../hooks/check-msg-no-private-paths.sh .git/hooks/commit-msg

# if the private tree is not the sibling default
git config rozzzsie.privateNamesFile /abs/path/to/private-workspace-names.txt

# local ignore rules for the private directories, which .gitignore no longer names
printf '%s/\n' <name> <name> ... >> .git/info/exclude
```

**What a pass does and does not mean.** Both match name and path strings, not meaning —
content pasted without a path is invisible to them. The `pre-commit` hook reads only the
*staged* set, so anything already committed is never re-scanned. A pass means "nothing
watched appeared", never "this is sanitized".

**Resolution failure is loud on purpose, in both directions.** Moving the list out of the
repo removed a disclosure and introduced a new way to be silently unarmed: a missing
private tree yields an empty list, and an empty list matches nothing. Both hooks therefore
refuse to proceed quietly below three names — the blocking one refuses the commit, the
warning one says on stderr that it is not covering you. Neither exits `0` in silence.

*(An empty list would in fact make the alternation degenerate to `()` and match
everything, so the guards would over-trigger rather than under-trigger. That is an
accident of regex, not a design, and it is not what the floor check is relying on.)*
