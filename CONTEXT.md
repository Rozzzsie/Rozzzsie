# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

## Governance OS state (snapshot 2026-06-14)

| Field | Value |
|-------|-------|
| Protocols version | v3.15.0 (cumulative through the memory-tier enforcement primitive — source-class partition, fail-closed-on-error, dry-run-dark with a dated enforce-flip review — plus the prior checkpoint-bar / Sumi-grader / Path-A / Protocol-10-dashboard layers) |
| Last weekly retrospective (P10) | 2026-06-14 (full 10-step ritual; 8 findings; window 2026-06-07 → 2026-06-14. Cycle's center of gravity = **the audit catching its own auditor trusting a surrogate, twice**: the weekly hook fire-rate audit hard-broke because a liveness marker added last cycle to expose a silent hook was schema-malformed and blinded the auditor to the whole corpus [fixed live + backfilled]; then verify-to-artifact fired on the orchestrator's own claim — a "mechanism-absent" finding asserted from a producer-log's silence, caught by the learning layer reading the source. 4 rule-tier landings [firelog-producer schema-conformance; verify-to-artifact "mechanism-exists" sub-axis; clean-path liveness-marker-at-authoring doctrine; subprocess-env-inheritance + nested-repo absolute-path-append propagations]. Checkpoint-bar miss 0.22 cycle-wide [↓ first improvement in three cycles, from 0.26] — but a 13-of-19 barless cluster in a fresh session reaffirmed the tool-cascade diagnosis; the PreToolUse acknowledgement-gate [dry-run; enforce-flip next cycle] is the structural antidote. Grader recovered from last cycle's fail-open, now watch-tier at ~66.7%. Learning-layer authored 2 proposals [both accepted + executed]. Prior P10: 2026-06-07 (p9 sidecar). |
| Next P10 due | 2026-06-21 |
| Dashboard release | v2.4 (re-rendered against `retros/2026-06-14-p10.yaml`; trend grid extends to n=8 sidecars; debuts the `meta_finding` hero callout; closes the p9 wiring-lag — version/default-sidecar/state-files were behind by one cycle, now current). |
| Active fam roles | 8 (Root / Luma / Teacher / Breakline / Codex / Brindle / Deputies + the controller as architect-decider) — plus Sumi as 5th P3 enforcement layer (NEW v3.10, governance-grader for subagent output / paste-text / design specs) |
| Hook layer | Project-scope governance hooks + user-scope companion hooks; Hook fire-rate audit (Protocol 10 step 6.7) shipped v3.5.2; checkpoint-bar Tier 2 enforcement extended through v3.10.4 with PostToolUse format-validator + substantive_v2 mutation-tool-aware classification; Sumi drift-scan PostToolUse hook on output-checklist + sumi-rubrics edits (v3.10.4) |
| Synthesis-Surface Pre-Render Pattern | v1 reference implementation shipped on SessionStart briefing (2026-04-23); bidirectional contract codified v3.5.1; output-side mirror (MD-canonical + HTML-render hybrid) shipped as deliverable format convention 2026-05-10 |
| Teacher proposal lifecycle | 1 `pending` (Aggressive MUTATION_TOOLS extension — execution gated on SDK MCP tool surface stabilization); current-cycle proposals at terminal status (`executed` / `deferred` with explicit watch entries) |
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
