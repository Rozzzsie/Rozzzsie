# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

## Governance OS state (snapshot 2026-04-27)

| Field | Value |
|-------|-------|
| Protocols version | v3.5.2 |
| Last weekly retrospective (P8) | 2026-04-29 — automated draft generated; awaiting Rosie's interactive review (prior interactive: 2026-04-24, 15/15 triaged) |
| Next P8 due | 2026-05-06 |
| Active fam roles | 8 (Root / Luma / Teacher / Breakline / Codex / Brindle / Deputies + the controller as architect-decider) |
| Hook layer | Project-scope governance hooks + user-scope companion hooks; Hook fire-rate audit (Protocol 8 step 6.7) ships in v3.5.2 |
| Synthesis-Surface Pre-Render Pattern | v1 reference implementation shipped on SessionStart briefing (2026-04-23), bidirectional contract codified v3.5.1 |
| Teacher proposal lifecycle | 0 `pending`, 0 unresolved `approved`, all current-cycle proposals at terminal status (`executed` / `deferred` with explicit watch entries) |
| Checkpoint-bar Tier 2 hook | Live, real-traffic firelog populating per-turn audit records |

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
- Protocol skeleton P1–P9 with sub-protocols P1B / P2B / P3B for Codex validation
- The four-role split (Root / Luma / Teacher / controller) — each rail load-bearing against exactly one failure mode
- Symlink-canonical pattern for versioned governance docs (governance changes don't require N-file rename sweeps)
- Workspace state-update protocol (CONTEXT + CHANGELOG after every meaningful work increment)
- Verify-to-artifact §14 family — six sub-families codified, propagation across all workspace LEARNINGS

**Evolving** (active development surface):
- Synthesis-Surface Pre-Render Pattern (1 of 5 surfaces shipped; #2 P8 retro and #3 P7 close are sprint candidates)
- Teacher proposal cadence + auto-promotion gating (P9 partially formalized; full autonomy still controller-gated)
- Hook fire-rate audit history (just shipped; first cross-cycle observation due at 2026-05-01 P8)
- Dashboard / observability layer (sprint-1 scope: governance metrics rendered from retro sidecar — see `dashboard/`)
- Sidecar schema v1.0 stability review window: 2026-05-15 (3+ retro cycles needed before mid-week emission unlocks)

---

## Cross-workspace ledger

The root `CHANGELOG.md` is the cross-workspace ledger — every governance-state change lands there even when the productive work happens inside a workspace. The five most-valuable architectural shifts are surfaced in the public CHANGELOG; older shifts archived in private and accessible through the session-archive retrieval primitive.
