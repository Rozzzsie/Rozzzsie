# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

## Governance OS state (snapshot 2026-06-21)

| Field | Value |
|-------|-------|
| Protocols version | v3.16.0 (cumulative through the insights A/B promotion-gate — a DRY-RUN-dark layer that derives promotion-eligibility [evidence-mass, post-promotion recurrence] as a pure function of the live signal buffer, split across two clocks [promotion-due at retro-close, recurrence-death at session-close], with a dated enforce-flip review — plus the prior memory-tier enforcement primitive / checkpoint-bar / Sumi-grader / Path-A / Protocol-10-dashboard layers) |
| Last weekly retrospective (P10) | 2026-06-28 (full 10-step ritual from a fresh interactive session; 7 findings; window 2026-06-21 → 2026-06-28. Cycle's center of gravity = **a CALIBRATION-GATE catch**: two dated enforcement-teeth-on reviews came due the same day and **both HELD on data integrity** — one gate had accrued ZERO real deny events in its dry-run shadow [no false-positive rate to calibrate; flipping would calibrate off an empty series], the other had ample clean data but its clean-observation window was a day short AND its deny volume mirrored a live discipline-miss rate [flipping = heavy friction]. Named the lesson: a dated teeth-on review is itself gated on the calibration data being real + sufficient — a finality date raises the verification bar, it does not satisfy it. The retro also caught its OWN insights-archival step gone stale against last month's promotion-gate substrate change [the buffer is now the evidence corpus] → refused the archival + queued a protocols reconciliation. 2 doctrine promotions [fixture-shape fidelity for renderer/parser/serializer tests + delimiter-collision; shape-ambiguity default-deny for machine-parsed fields], both learning-layer-authored + executed. Checkpoint-bar miss 0.26 cycle-wide [↓ slight improvement from 0.28]. Promotion-gate shadow surfaced 0 governance-scope candidates; drift-scan small-sample flag [n=8, watch]. Learning-layer authored 2 [executed] + 1 deferred; a standing commit-boundary-tripwire proposal APPROVED → build-queued; 2 prior proposals re-scanned still-holding. Prior P10: 2026-06-21 (p11 sidecar). | a substrate change shipped last cycle [the promotion-gate above] made the signal buffer the live evidence corpus, which quietly turned an OLD maintenance mechanism [date-based buffer rotation, plus the SessionStart banner that still suggests it] into a silent corruptor of the new gate's inputs — rotating would archive real evidence and blind the gate. The orchestrator, following the stale banner, proposed a date-bounded archive; the **operator caught it** and rotation was SUSPENDED. Named the stale-mechanism class [a substrate change that flips an artifact disposable→load-bearing turns every old maintenance mechanism over it into a corruptor until re-derived against the new contract]. Second finding: the gate's promotion-due predicate over-flags domain-scoped families [no scope filter] → governance-only-teeth scope filter queued for enforce-flip. 3 doctrine promotions [event-log-outranks-rollup = 14th verify-to-artifact sub-family; post-runtime-bump venv-first; question-ending-turn checkpoint-bar-mandatory], all learning-layer-authored + executed. Checkpoint-bar miss 0.28 cycle-wide [↑ regressing from 0.22]; the PreToolUse ack-gate enforce-flip was RE-DATED on a corrupt-pre-fix-calibration basis. Grader flagged a FALSE silent-candidate [audit numerator blind to grader vocabulary] + a real timeout cluster at its raised budget [fail-open]. Learning-layer Write-authority gap verified to source as NOT real [phantom gap closed]. Cross-model reviewer at monthly usage cap → adversarial auditor backed up review. Prior P10: 2026-06-14 (p10 sidecar). |
| Next P10 due | 2026-07-05 |
| Dashboard release | v2.6 (re-rendered against `retros/2026-06-28-p12.yaml`; trend grid extends to n=10 sidecars; `meta_finding` hero callout populated for the 3rd straight cycle [the calibration-gate catch — two enforce-flip reviews both HELD]; version/default-sidecar/state-files all advanced in the same pass — no wiring-lag). |
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
