# CONTEXT.md — Rozzzsie (sanitized public snapshot)

A sanitized snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private — it carries BLOCKER flags, key-decisions tied to specific stakeholders, queued-initiatives with deadlines, and per-workspace state with private detail. What's here is the shape, not the live content: workspace map at the public grain, governance health one-liner, retro cadence anchor.

For why CONTEXT lives in two surfaces (private narrative + public sanitized): see `LEARNINGS.md` "Verify to the artifact, not to a surrogate" — sprint scoreboards and retro tables describe the artifact; the artifact itself is the file. CONTEXT here is the public *description*; the live state is on the controller's machine.

---

## Governance OS state (snapshot 2026-07-12)

| Field | Value |
|-------|-------|
| Protocols version | v3.16.0 (cumulative through the insights A/B promotion-gate — a DRY-RUN-dark layer that derives promotion-eligibility [evidence-mass, post-promotion recurrence] as a pure function of the live signal buffer, split across two clocks [promotion-due at retro-close, recurrence-death at session-close], with a dated enforce-flip review — plus the prior memory-tier enforcement primitive / checkpoint-bar / Sumi-grader / Path-A / Protocol-10-dashboard layers) |
| Last weekly retrospective (P10) | 2026-07-12 (full 10-step ritual from a fresh interactive session; 7 findings; window 2026-07-05 → 2026-07-12. A **DECISION** cycle — a regular weekly, not month-first (the monthly-housecleaning sub-ritual fired last cycle). Center of gravity [`meta_finding` hero callout] = a **HELD→BUILD flip**: after 6+ cycles on the build-queue, the checkpoint **acknowledgement-gate enforce-flip** [a PreToolUse gate withholding the next mutation until the agent emits its discipline bar] moved to **BUILD, narrow-armed**. The consultant rail reframed the blocking prerequisite — **narrow-arming and friction-relief are the same decision seen from two sides**: arm the gate only on the three turn-clusters doctrine already declares self-discipline-dead [post-compaction continuation, long wrap-arcs, async/deputy-completion] and a legitimate long work-arc, being a *non-cluster* arc, structurally cannot trip it → the scoping choice IS the relief, collapsing the prerequisite into it. Build = dedicated session + adversarial deny-envelope pass, bundled with the fan-out-cost rule into one version bump; basis-honesty rider = calibrate the arming threshold against the tally-derived (hook-truth) miss rate, never self-report. The forcing evidence: checkpoint-bar miss **improved 0.34 → 0.22 cycle-wide [506/2312]** YET the worst single-session barless run **HELD at 78 consecutive** [one build-heavy session: 127 corrective fires] and the miss recurred live inside the promoting session under maximal rule-awareness — the average improved while the peak clusters did not [structural, not knowledge-triggered → arm narrow, not uniform]. 2 verify-to-artifact promotions executed [filtered-grep-false-clean; search-index/content-snippet freshness] → cluster at 18 sub-families; a genuinely-uncovered orchestration gap [fan-out ballooned across a compaction boundary → cost over-run + operator halt] approved + queued. Two hook-health flags surfaced, deliberately NOT blind-fixed [a drift-scanner with no in-window verdict = possible fail-open; a promotion gate inventory-listed but absent from live wiring = inventory drift]. `sidecar-metrics-tally.py` run BEFORE authoring the metrics blocks [it CORRECTED an in-session memory-surrogate carrying last cycle's 0.34 forward — the artifact won]. Pre-publish self-discipline grader on the public sidecar. Prior P10: 2026-07-05 (p13 sidecar). | 2026-07-05 (9 findings; window 2026-06-28 → 2026-07-05. **Promotion-heavy** cycle — all 7 learning-layer P10-slate proposals cleared the operator-gate + executed [decision velocity 2 → 7, heaviest pass of the visible window]. Architect-gold catch [`meta_finding`, 4th straight cycle] = **GRANTS OUTLIVE DIRECTIVES**: reconciling the stale insights-archival step killed the *instruction*, but a separate still-live autonomous *grant* authorized the same buffer-flush — retiring a mechanism means grepping for every standing GRANT of the operation, not just its imperative; grant retired on all 3 surfaces. 7 rule-tier landings → verify-to-artifact cluster at 16 sub-families. Checkpoint-bar miss **0.34 [644/1915; ↑ REGRESSION, highest of the visible window]** — two of the cycle's own promoted rules recurred live inside the promoting session [→ the ack-gate enforce-flip is the fix, not more rules]. Both build-queue items HELD. Prior P10: 2026-06-28 (p12 sidecar). |
| Next P10 due | 2026-07-19 |
| Dashboard release | v2.8 (re-rendered against `retros/2026-07-12-p14.yaml`; trend grid extends to n=12 sidecars; `meta_finding` hero callout = the HELD→BUILD enforce-gate flip [narrow-arming and friction-relief are the same decision]; checkpoint miss improved 0.34 → 0.22 but the worst barless run held at 78 [average improved, peak clusters didn't → arm the gate narrow]; decision velocity = 2 executed + 2 approved-queued; version/default-sidecar/README-note/state-files all advanced in the same pass — no wiring-lag. Pre-publish self-discipline grader on the sanitized sidecar = `warn`, both folds applied [dropped a commentary-axis trigger word + a budget-fraction disclosure]). |
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
