# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

## Governance OS state (snapshot 2026-09-27)

| Field | Value |
|-------|-------|
| Protocols version | v3.27.0 — the thirteen rituals are now factored into independently versioned units and the index file is an INDEX, read paginate-to-completion, with four Tier-1 units full-loaded eagerly and nine read at point-of-use. Two units are covered by NEITHER the session-start digest NOR the eager set — a named gap, not a closed one, and a non-interactive run has no path to either. Prior: v3.16.0 (cumulative through the insights A/B promotion-gate — a DRY-RUN-dark layer that derives promotion-eligibility [evidence-mass, post-promotion recurrence] as a pure function of the live signal buffer, split across two clocks [promotion-due at retro-close, recurrence-death at session-close], with a dated enforce-flip review — plus the prior memory-tier enforcement primitive / checkpoint-bar / Sumi-grader / Path-A / Protocol-10-dashboard layers) |
| Last weekly retrospective (P10) | **2026-09-27** (retro #25; 16-step ritual, 16 steps complete, counted after the canonical artifact existed and the private close had committed; 10 findings; window 2026-09-21 → 2026-09-26, six days because the retro ran a day early; the monthly-housecleaning sub-ritual did not fire. `meta_finding` = most failures were recurrences of rules already written, and the one new failure was a leak canary that classed a live gate's records as test fixtures, so a purge on the same predicate deleted the evidence the hook audit then read as absence) |
| Next P10 due | 2026-10-04 (the first P10 of October, so the monthly-housecleaning sub-ritual fires) |
| Dashboard release | **v3.14** (re-rendered against `retros/2026-09-27-p25.yaml` with no arguments, so the default-sidecar path is the one exercised; schema check clean and validated by two positive controls; the ritual dial is written after the private close, forecasting only the public push, and reverts to null if that push fails) |
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
- Verify-to-artifact §14 family — 11 sub-families codified, propagation across all workspace LEARNINGS (extended through 2026-08-28 operator-recollection entry)
- Sumi 5th P3 enforcement layer (v1.0/v1.1/v1.2/v1.3 trilogy 2026-05-09/10) — read-only governance grader for subagent output / paste-text / design specs + drift-scan invocation walking active rubrics

**Evolving** (active development surface):
- Instrument-independence family (NEW 2026-08-28, n=3 same-session) — diagnostics that route through the subsystem under repair: recovery channel / test target / symptom string. Landed in root `LEARNINGS.md` only; **not yet propagated** to `_config/output-checklist.md` or workspace LEARNINGS files, so it is an observation at rule-tier but not yet enforced — P5 step (b) outstanding
- Published P7 stop-gate — two independent defects (found 2026-09-27) — the public copy of the session-close gate assumes a bottom-append `CHANGELOG.md` in two checks. The entry-length check passes by luck; the retrospective-recency check misreads the cadence as ~151 days stale against a 14-day grace and blocks a session whose real retro is 7 days old. A comment on the check directly above it documents the assumption, so the defect ships with its own description. **Not fixed here** — hook logic is governance code and the fix is the operator's call; flagged rather than patched, and no ledger line was reworded to clear the block. A second, prior defect surfaced once the state-file checks were cleared: the trace-staleness check calls `stat` in the BSD spelling first, whose GNU failure mode writes a filesystem block to the same stdout the fallback feeds, so the numeric comparison aborts under `set -u` with no verdict emitted. The gate is macOS-only and has never completed past its CONTEXT check on this platform, which means the ordering defect above is reachable only where `stat -f` succeeds. A third property, not a defect but load-bearing: the gate scopes a session by a baseline commit file rewritten at every session start, so on a re-provisioned container the baseline is the default branch's tip and every commit arriving by merge reads as authored in-session — which is why a merge that carries a productive file trips the root-CHANGELOG check while four earlier state-only merges did not
- Synthesis-Surface Pre-Render Pattern (reference implementation on SessionStart shipped v3.5.0; output-side mirror via MD-canonical+HTML-render hybrid shipped 2026-05-10 as deliverable format convention)
- Teacher proposal cadence + auto-promotion gating (P8 firmware ON as of v3.9.1 — Teacher agent + grammars + ledger + auto-promote-enabled gate; gate still controller-supervised in observation window)
- MUTATION_TOOLS doctrine (v3.10.3 introduced + v3.10.4 Conservative extended; Aggressive direction pre-staged as Teacher proposal pending SDK MCP tool surface stabilization)
- Dashboard / observability layer (sprint-2 v2.0 live — multi-retro trend rendering unlocked 2026-05-10 after 3+ retro sidecars accumulated; schema v1.0 stability review window: 2026-05-15)
- Sidecar schema v1.0 stability review window: 2026-05-15 (3+ retro cycles needed before mid-week emission unlocks)

---

## Cross-workspace ledger

The root `CHANGELOG.md` is the cross-workspace ledger — every governance-state change lands there even when the productive work happens inside a workspace. The five most-valuable architectural shifts are surfaced in the public CHANGELOG; older shifts archived in private and accessible through the session-archive retrieval primitive.
