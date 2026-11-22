# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

> **Retro cadence anchor — updated 2026-11-22 (P10 #33).** Cycle p33 published; window 2026-11-16 → 2026-11-22; dashboard v3.22 renders `retros/2026-11-22-p33.yaml` by default. Seventeen findings. The ritual dial reads 16 of 17, the incomplete step being propagation.

## Governance OS state (snapshot 2026-10-03)

| Field | Value |
|-------|-------|
| Protocols version | v3.29.4 — the thirteen rituals are now factored into independently versioned units and the index file is an INDEX, read paginate-to-completion, with four Tier-1 units full-loaded eagerly and nine read at point-of-use. Two units are covered by NEITHER the session-start digest NOR the eager set — a named gap, not a closed one, and a non-interactive run has no path to either. Prior: v3.16.0 (cumulative through the insights A/B promotion-gate — a DRY-RUN-dark layer that derives promotion-eligibility [evidence-mass, post-promotion recurrence] as a pure function of the live signal buffer, split across two clocks [promotion-due at retro-close, recurrence-death at session-close], with a dated enforce-flip review — plus the prior memory-tier enforcement primitive / checkpoint-bar / Sumi-grader / Path-A / Protocol-10-dashboard layers) |
| Last weekly retrospective (P10) | **2026-11-15** (retro #32; 17-step ritual, **16 steps complete** — the first non-perfect dial in four cycles, and the incomplete step is propagation: eighty-two entries in the window carry no promotion receipt and none was propagated, with the operator's deferral covering three named proposals rather than that backlog. 17 findings; window 2026-11-08 → 2026-11-15; the monthly-housecleaning sub-ritual was NOT due, a retro having already run this calendar month. `meta_finding` = a correct instrument pointed at the wrong subject and believed — a commit-stamp gate was measured as failing open and filed onto four surfaces, then reported itself clean in the commit path minutes later, the session's shell having sat in a parent directory that is its own repository with the governed tree nested and ignored inside it. The verification ritual ran and endorsed the wrong conclusion, because only one of two hypotheses — subject broken, instrument misaimed — was ever named. The same shape recurred twice before close: a mandated census satisfied by a substitute that could not produce the step's own summary line, and an invented schema field refused by the guard, which is a second instance of a class already published as a finding in the same file) |
| Next P10 due | 2026-11-22 |
| Dashboard release | **v3.21** (re-rendered against `retros/2026-11-15-p32.yaml` with no arguments, so the default-sidecar path is the one exercised and a stale target would have shown itself; schema check clean at 0 warnings, with the guard having refused an invented field name on the way there; the ritual dial is written after the private close, forecasts only the public push, and reverts to null if that push fails. ⚠️ The suite runs 112 tests with the same **2 pre-existing failures**, both on an open row since 2026-09-27 and both asserting on older fixtures, not on this cycle's sidecar — this release's only code change is two literals, neither reachable from the validator those tests exercise. ⚠️ The dial's basis note is recorded in a schema field no renderer reads: published in the YAML, absent from the page. ⚠️ No external code review was possible: one validator returned a model-not-found error all window and the other refuses a scope outside the private tree. ⚠️ The prior release shipped with no release note and left the dashboard README header a version behind; named rather than back-filled) |
| Active fam roles | 8 (Root / Luma / Teacher / Breakline / Codex / Brindle / Deputies + the controller as architect-decider) — plus Sumi as 5th P3 enforcement layer (NEW v3.10, governance-grader for subagent output / paste-text / design specs) |
| Hook layer | Project-scope governance hooks + user-scope companion hooks; Hook fire-rate audit (Protocol 10 step 6.7) shipped v3.5.2; checkpoint-bar Tier 2 enforcement extended through v3.10.4 with PostToolUse format-validator + substantive_v2 mutation-tool-aware classification; Sumi drift-scan PostToolUse hook on output-checklist + sumi-rubrics edits (v3.10.4) |
| Synthesis-Surface Pre-Render Pattern | v1 reference implementation shipped on SessionStart briefing (2026-04-23); bidirectional contract codified v3.5.1; output-side mirror (MD-canonical + HTML-render hybrid) shipped as deliverable format convention 2026-05-10 |
| Teacher proposal lifecycle | 4 authored this cycle plus 2 re-proposals of stale approved items, all ruled in-session: all four proposals accepted as recommended, two executed in-session and two filed as ungated backlog rows; the re-proposals split one approved item and moved another off a queue with no reader. Zero approved items now sit on a queued status |
| Checkpoint-bar Tier 2 hook | Live, real-traffic firelog populating per-turn audit records; v3.10.3 LOOSE_BAR_PATTERN format-validator + substantive_v2 mutation-tool-aware classification; v3.10.4 MUTATION_TOOLS frozenset extended `{Edit, Write, Bash}` → `{Edit, Write, MultiEdit, NotebookEdit, Bash}` (mcp__*-write deferred) |

---

## Workspace map (sanitized)

| Workspace | Purpose | Current state grain |
|-----------|---------|---------------------|
| `workspaces/team-leadership-2026/` | Informal senior-IC leadership: hiring, coaching, team comms, performance | Hiring paused (team at steady state); post-promotion daily operational rules codified; HITL-CC visibility tactic active |
| `workspaces/ai-champion-2026/` | AI-bot empowerment in a Product Support ticketing context: behavior, routing, response quality | Bi-weekly snapshots running; per-procedure deep-dives shipped; deck script v2 locked; cross-functional asks routed to artifact-owner not role-in-team |
| `workspaces/docs-sync-2026/` | Product docs sync to the customer-facing knowledge surface, plus FAQ-agent for internal Q&A | Pipeline live; knowledge agent on Sonnet 4.6 since 2026-04-02; pipeline migrated Sonnet 4 → 4.6 in 2026-04-25 retroactive sweep |
| `workspaces/kb-architecture-2026/` | Product Support Knowledge Bank for two AI products | Snippet Library complete (37 snippets across 8 buckets); pipeline built; second-tool rescope pending |

Two private workspaces (lightweight personal-learning log + sandbox for fun builds) are intentionally not surfaced here; they carry the controller's reading-distillations and experimental scaffolds, neither of which generalizes outside the live system.

---

## What's stable vs what's evolving

**Stable** (well past the breakage point):
- Protocol skeleton P1–P10 with sub-protocols P1B / P2B / P3B for Codex validation (v3.9.3 cascade complete; P5 Focus-chain discipline added v3.7.0)
- The four-role split (Root / Luma / Teacher / controller) — each rail load-bearing against exactly one failure mode
- Symlink-canonical pattern for versioned governance docs (governance changes don't require N-file rename sweeps)
- Workspace state-update protocol (CONTEXT + CHANGELOG after every meaningful work increment)
- Verify-to-artifact §14 family — 10 sub-families codified, propagation across all workspace LEARNINGS (extended through 2026-05-09 attribution-conflation entry)
- Sumi 5th P3 enforcement layer (v1.0/v1.1/v1.2/v1.3 trilogy 2026-05-09/10) — read-only governance grader for subagent output / paste-text / design specs + drift-scan invocation walking active rubrics

**Evolving** (active development surface):
- Synthesis-Surface Pre-Render Pattern (reference implementation on SessionStart shipped v3.5.0; output-side mirror via MD-canonical+HTML-render hybrid shipped 2026-05-10 as deliverable format convention)
- Teacher proposal cadence + auto-promotion gating (P8 firmware ON as of v3.9.1 — Teacher agent + grammars + ledger + auto-promote-enabled gate; gate still controller-supervised in observation window)
- MUTATION_TOOLS doctrine (v3.10.3 introduced + v3.10.4 Conservative extended; Aggressive direction pre-staged as Teacher proposal pending SDK MCP tool surface stabilization)
- Dashboard / observability layer (sprint-2 v2.0 live — multi-retro trend rendering unlocked 2026-05-10 after 3+ retro sidecars accumulated; schema v1.0 stability review window: 2026-05-15)
- Sidecar schema v1.0 stability review window: 2026-05-15 (3+ retro cycles needed before mid-week emission unlocks)

---

## Cross-workspace ledger

The root `CHANGELOG.md` is the cross-workspace ledger — every governance-state change lands there even when the productive work happens inside a workspace. The five most-valuable architectural shifts are surfaced in the public CHANGELOG; older shifts archived in private and accessible through the session-archive retrieval primitive.
