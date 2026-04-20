# CHANGELOG — Rozzzsie

Architectural shifts, not individual fixes.

---

## Protocols v3.4 — Teacher learning layer + Brindle-graduated framing (2026-04-20)

The governance OS grew an 8th role. Teacher is the pattern detector + proposal author on the governance catchment — insights-buffer, retro-candidates, and LEARNINGS deltas, all three streams already curated upstream. Invoked at the weekly P8 retro as step 6.5, and manually between P8s when Rosie asks. Authors 1–3 structured proposals into `.claude/teacher-proposals.md` per invocation; Rosie decides accept / modify / reject / defer; Root executes approved proposals at P8.

Propose-only on all governance surfaces (CLAUDE.md, LEARNINGS.md, protocols, output-checklist, workspace state files, hooks, agent files, designs, plans); strict-validated direct-write on a narrow pre-approved list (skill creation, monthly insights-archive rotation, `_input/archive/` moves at distillation time) with degrade-to-propose fallback. Silent-override is the explicit failure mode — every Teacher write surfaces in proposals AND session-log AND the next P8 retro. Memory = the proposals file itself; no separate memory layer.

P9 (autonomous iteration loop) joins the protocol quick reference — partially formalized as Teacher; auto-promotion conditions for Teacher-authored proposals bypassing the Rosie gate remain open. OS version bumps to v3.4.0; README and CLAUDE.md name Teacher in the Strategic Layer and surface the protocol count as twelve.

Alongside the protocol bump, the repo's storytelling layer now names Brindle as the fam member who graduated into a standalone product. Seven agents live in this repo as Claude Code subagents (their `.md` IS their implementation); Brindle lives here as persona only, with her Python runtime shipping separately at [`brindle-terminal-bunny`](https://github.com/Rozzzsie/brindle-terminal-bunny) under MIT. The asymmetry was there before the framing landed — the two-repo shape predates v3.4. What's new is the word "graduated" for what was previously an unnamed gap. Presentation-symmetry isn't the only kind of symmetry worth protecting; architectural differences deserve their own language.

---

## types-of-work.md added (2026-04-17)

First-cut OS capabilities reference artifact. 7 live types across 4 layers (Infrastructure / Workflow / Intelligence / Content) + 3 horizon items for the council. Swept from all 4 active workspaces. Delivered to Dhruv Gupta as Ask 1 of council onboarding.

---

## Landing surface applied demonstrate-vs-guard (2026-04-17)

The public README, root `CLAUDE.md`, and `_config/agent-protocols.md` were the first-click surface for any reader — but they still carried the private version's imperative voice and defensive framings. `CLAUDE.md` was reframed from "mandatory startup for an agent" (thirteen steps, five referencing files private to the live workspace) to "session startup" (six descriptive steps, private files marked as private, not silently broken). `agent-protocols.md` was stripped of "why it's not here" defensive phrasing per the 2026-04-16 LEARNINGS rule. `README.md` gained a narrative hook, a start-here signpost to `agents/breakline.md`, and reconciled its protocol count with the actual governance doc. `hooks/README.md` was added as a 20-line orientation — hook-to-protocol map plus the three invariants (cwd guard, fail-closed gate, hooks don't gate on state they manage). The rule the fix applied had been written six days earlier in LEARNINGS but hadn't propagated to the surface readers actually land on. The landing is now consistent with the doctrine.

## Protocols v3.3 — roles map + Luma translator rail (2026-04-14)

The governance OS grew a named roles map and its first decision-surface sub-agent. Seven roles (Root, Luma, Deputies, Codex-wrapper, Breakline, Brindle, Rosie) formalized in a single table. Luma — a translator rail that converts Root's dense output into decision-shaped frames — shipped as a user-level sub-agent descriptor with zero tools and inherited model. Doctrine locked: Root never simplifies for Rosie anymore; the model is not the product, the harness is.

## v3.3.1 structural rollup — scope-symmetry family retired (2026-04-15)

An 8-instance bug family that accumulated over 5 days was retired in a single patch. All 8 bugs shared the same shape: enforcement gates whose grep and validation reached different layers (different file scopes, different time windows, different workspace tiers). Fix: a shared helper library became the single source of truth for workspace list + tier semantics; both the stop-gate and the pre-commit hook source it. The pre-commit hook itself moved from untracked `.git/hooks/` to version-controlled `_config/hooks/` with an installer script — closing a meta-gap where governance enforcement code lived outside governance.

## Symlink-canonical pattern for versioned governance docs (2026-04-15)

Governance docs that carry a semver version now use a symlink-canonical pattern: the canonical file carries the full version in its filename (`agent-protocols-3.3.1.md`); a stable symlink (`agent-protocols.md`) sits alongside it and retargets on every version bump. All ~14 live references point at the symlink path — they never need updating. Same engineering shape as the pre-commit hook pattern: one-time setup cost, ongoing one-line `ln -sfn` on every bump, references stable forever. Replaced a 14-file rename sweep that had already fired twice in one week.

## Stop-gate hard gates — Check 3 + Check 8 patches (2026-04-15)

Two structural bugs in the session-close enforcement gate were fixed together: (1) governance-only sessions that touched root state files (LEARNINGS.md, CLAUDE.md, `_config/*`) without updating the root CHANGELOG now fail closed — previously they slipped through because the gate classified governance files as "state" and only demanded CHANGELOG for non-state files. (2) Session-log greps now scope to the current session's entry only — previously, prior sessions' valid propagation claims became perpetual blockers for future sessions. Both are scope-symmetry fixes: the gate's grep and its validation were reaching different layers.

## Scope-drift cleanup — the system catches its own mistakes (2026-04-16)

22 CHANGELOG entries and ~20 CONTEXT.md commits were logged in the wrong workspace for ~10 hours of productive work. The session opened in one workspace for brainstorming; when the initiative pivoted to architecture work, state writes continued landing by inertia. The drift went undetected until the next session, when a Luma-framed decision produced three cleanup options. The fix was a 7-file migration; the learning was that new initiatives need an explicit workspace-assignment decision before the first state write. The protocol said "update CONTEXT.md" but never specified *which* — the implicit default was the drift vector.
