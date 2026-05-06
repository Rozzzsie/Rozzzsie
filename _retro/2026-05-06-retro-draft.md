# Weekly Retrospective — 2026-05-06
**Status:** DRAFT — awaiting Rosie's interactive review
**Period:** 2026-04-29 through 2026-05-06
**Automated by:** P10 Supervise layer retrospective (SessionStart hook)
**Prior retro baseline:** 2026-05-03 interactive P10 (P4 sidecar, window 2026-04-26 → 2026-05-03, private narrative); and 2026-04-29 automated draft (narrative-only, awaiting interactive review as of that date)

> **Hook tracking discrepancy noted:**
> The SessionStart hook fires on "7 days since last retro" and measures from the last public `_retro/` draft (2026-04-29). The last *actual* P10 was the 2026-05-03 interactive session (3 days ago; narrative private). CONTEXT.md states next P10 due 2026-05-10. This automated draft is therefore 4 days early per CONTEXT.md's tracking surface, but on-schedule per the hook's tracking surface. The two surfaces diverge because interactive retros produce private narratives outside the hook's scan path. Suggested action: Rosie to confirm whether this is the intended behavior or whether the hook's tracking path should also scan the retros/ sidecar dates. This is an instance of the "verify to artifact, not surrogate" family — the hook is reading a surrogate (last public draft date) rather than the artifact (last actual P10 completion date).

---

## Period

2026-04-29 through 2026-05-06 (7 days). The prior public automated draft was 2026-04-29. The prior interactive P10 was 2026-05-03 (3 days ago; window 2026-04-26 → 2026-05-03, covers the v3.9.x ship cycle). This draft covers the gap since 2026-04-29; items already covered in the 2026-05-03 interactive session are noted as such.

---

## What shipped well

### Governance OS / Root-level (since 2026-04-29)

**2026-05-04 — Dashboard v1.4 — Frame 2 fam-dispatch widget + measurement-surface anchor:**
- New top-band widget surfaces fam-wide agent activity with explicit sub-band split: dispatch axis (Agent-tool subagents: Deputies 31 / Luma 26 / Codex 13 / silent-failure-hunter 4 / Breakline 3 / Teacher 2; total 79) and reactions axis (Brindle: 299 reactions across 54 starts + 210 mid-session + 35 closes). Sub-band split was Luma's verdict: conflating the two axes would let the high-cardinality reactions axis visually overpower dispatch rails (different units).
- The "Discipline + dispatch" band simplified to "Discipline" (checkpoint-bar only); Codex/Teacher/Luma scalars removed (now redundant with fam widget).
- Luma reframe-axis tally relocated from band-tier prominence to a "Luma reframe-axis facet (deep-dive)" panel with explicit empty-state copy naming the categorization constraint (human-distilled review, not auto-extracted).
- Hero gains explicit measurement-surface anchor: "Measurement surface — what fired and how often, not what each rail is for." Locks dashboard scope vs. Roles map scope (dashboard = observed behavior; Roles map = intended function).
- 0-count rows rendered with `kv-row-muted` CSS class (opacity 0.55 + italic): absence reads as measurement signal, not missing row.
- 7-test smoke suite at `dashboard/test_render_fam_dispatch.py`.
- `DASHBOARD_VERSION = "1.4"`. Shipped via PR #4 + PR #5 (co-line follow-up).

**2026-05-04 — retros/2026-05-03-p4.yaml phase-3 metrics backfill:**
- `discipline_metrics` + `latency_observations` computed from `.claude/hook-fires.jsonl` (47 sessions / 2,573 substantive turns / 592 missed bars, ~23% miss rate) and `.claude/session-start-latency.log` (66 datapoints; median 89.5s / p95 546s / max 1,420s / 22 violations >120s).
- `fam_dispatch_distribution` section added with `dispatch_axis` + `reactions_axis` sub-keys.
- Dashboard re-rendered against backfilled sidecar. Codex/Teacher/Luma invocation counts + Luma category breakdown remain `null` — require human-distilled retro narrative review (structural: auto-extraction not available for this field).
- Shipped via PR #3.

**2026-05-04 — v3.9.3 reframe Phase 1 — public-tree register shift:**
- Public-tree register shifted to AI governance reference architecture framing.
- CONTEXT.md and CHANGELOG.md updated with v3.9.3 cascade detail.

**2026-05-04 — README.md update.**

### Workspace-level activity (all four workspaces)

No workspace CHANGELOG entries exist — none of the four workspaces (`ai-champion-2026`, `docs-sync-2026`, `kb-architecture-2026`, `team-leadership-2026`) have a `CHANGELOG.md` file. It is not possible to determine from this automated scan whether productive workspace sessions occurred in this window and were not logged, or whether no productive sessions ran. This is the same structural ambiguity flagged in the 2026-04-22 and 2026-04-29 retro drafts — now on its third consecutive flag.

---

## Recurring quality gaps

**1. Missing workspace CHANGELOG.md files — third consecutive flag (21+ days)**
Three consecutive automated retro drafts (2026-04-22, 2026-04-29, 2026-05-06) have flagged this gap. All four workspace `CLAUDE.md` files mandate "append to `CHANGELOG.md` after every deliverable" and "do not close a productive session without completing all four steps" (the four steps being: output checklist, CONTEXT.md update, CHANGELOG.md append, learnings capture). Zero `CHANGELOG.md` files exist in any workspace.

This gap has reached the P2 threshold: same-axis failure on three iterations. The question is no longer "should we create these files?" (protocol mandates it) — it's "what is the structural reason they haven't been created despite three retro flags?" Possible diagnoses: (a) workspace sessions have not run since the mandate was added, (b) sessions ran but the CHANGELOG mandate was not executed, (c) the 2026-04-24 interactive review explicitly deferred this and the defer condition has not been met. None of these can be confirmed without Rosie's input.

**Action required:** Rosie to provide triage outcome from 2026-04-24 and 2026-05-03 interactive reviews on this item. If still open: create the four `CHANGELOG.md` files with a header + no entries in this session or name a concrete session. If deferred: name the defer condition and add it to the relevant workspace CONTEXT.md.

---

**2. personal-learnings weekly digest — second consecutive blocked fetch**
`aiagentstore.ai` returns 403 on WebFetch and is blocked by curl allowlist. Both the 2026-04-27 and 2026-05-04 digest cycles failed. The 2026-05-04 failure note includes "recurring-failure escalation flag added." Two consecutive failures = structural loop break, not a transient incident.

**Action required:** decide whether to (a) add `aiagentstore.ai` to the allowlist, (b) replace with an alternative source, or (c) suspend the personal-learnings digest loop until the allowlist is updated. Current state: the loop is running but producing nothing.

---

**3. Checkpoint-bar discipline — plateau at ~23% miss rate**
The P4 sidecar (2026-05-03 metrics backfill) surfaces 592 missed bars across 2,573 substantive turns (~23%). The Tier 2 per-turn enforcement hook shipped in v3.5.2. At 47 sessions (from the firelog), the miss rate has not yet closed to the target. Whether this is improving session-over-session cannot be determined from the aggregate; per-session trend would require the full firelog read (not available in this automated scan).

**Action for Rosie:** at interactive review, check whether the per-session miss rate is trending down since v3.5.2 shipped, or holding flat. If flat, the hook is firing but not changing behavior — a different intervention may be needed.

---

**4. Carryover unpropagated learnings — no new propagation since 2026-04-29**
Six items from the 2026-04-29 retro remain unpropagated (see Unpropagated Learnings section). No new LEARNINGS.md entries have been added since 2026-04-29 (verified: all root LEARNINGS entries pre-date 2026-04-29; all workspace LEARNINGS appear unchanged). The learnings layer is not growing this cycle, which may mean: sessions didn't surface surprises, or sessions didn't run, or surprises weren't captured. Cannot determine which.

---

## Unpropagated learnings

No new learnings this cycle. All six items below are carryover from the 2026-04-29 retro. Items flagged in multiple consecutive retros are noted.

| # | Source | Learning summary | Implied rule target | Flag count | Status |
|---|--------|-----------------|---------------------|------------|--------|
| 1 | Root LEARNINGS, 2026-04-25 | "Verify to artifact, not surrogate" — six sub-families. For any done/not-done claim that shapes next action: read the artifact (file, commit, message), not the CHANGELOG line, CONTEXT entry, or retro table describing it. | `output-checklist.md` §4 — extend existing "verified directly" item to cover done/not-done status claims (currently scoped to external system state only) | 2nd flag | Not propagated |
| 2 | Root LEARNINGS, 2026-04-23 | "Outside-lens diagnostics" — when inside lens has converged on candidates sharing an axis the controller didn't choose, dispatch a fresh perspective. One scoped sub-agent. Do not rank harder inside the wrong axis. | Root `CLAUDE.md` — Luma invocation guidance (new item after pre-dispatch discipline rule) | 2nd flag | Unverifiable (may be in private CLAUDE.md) |
| 3 | Root LEARNINGS, 2026-04-16 | "Demonstrate-vs-guard" — for pull-not-push artifacts, scan for defensive language patterns ("without spoiling," "keeps X private," "limited version of") and rewrite to affirmative demonstration. | `output-checklist.md` §1 Team Lead framing — new "defensive language scan" item | 3rd+ flag | Not propagated |
| 4 | Root LEARNINGS, 2026-04-16 | "P4 workspace-assignment gate" — before the first P4 write of any session, explicitly confirm which workspace owns the work. Default (current session context) is the drift vector. | Root `CLAUDE.md` §State update protocol — new step before step 1 | 3rd+ flag | Not propagated |
| 5 | docs-sync LEARNINGS | "Two-stage detection invariant" — revision counter = cheap pre-filter; content hash = authoritative signal filter. Do not collapse. Tighten hash before relaxing design. | `docs-sync/CLAUDE.md` §Pipeline architecture — explicit invariant note | 2nd flag | Not propagated |
| 6 | kb-architecture LEARNINGS, 2026-04-01 | "GDoc formatting: build from reference, not scratch." 5-step workflow: read reference doc structure → read target doc named styles → build formatter to set every differing property explicitly → test on ONE snippet and read back via API → lock format before batch-write. Do NOT iterate visually. | `kb-architecture/CLAUDE.md` §Content drafting rules — new subsection | 2nd flag | Not propagated |

**Item with flag count ≥ 3 (items #3 and #4) have hit the P2 threshold for same-axis failures.** If these were deferred in prior interactive reviews, the defer condition should be named. If they were accepted but not executed, they need to be executed now.

---

## Stale blockers

**Root CONTEXT.md:** sanitized public snapshot. Private BLOCKER dashboard not visible to this automated scan. CONTEXT.md reports no active BLOCKERs explicitly.

**Workspace CONTEXT.md files:** all four carry structural content only (workspace purpose, approval gates, pipeline shapes). No BLOCKER flags present.

**Derived structural blockers (from LEARNINGS — not confirmed as flagged BLOCKERs):**

| # | Source | Blocker | First noted | Action status |
|---|--------|---------|-------------|---------------|
| 1 | ai-champion LEARNINGS | Chatbot optimization blocked at architecture layer — Rosie does not own the KB the chatbot reads from. Pipeline-style intervention not available. | Undated (workspace LEARNINGS; present in 2026-04-22 retro) | ai-champion `CLAUDE.md` names the constraint ("Do not make assumptions...") but no evidence the architecture constraint has been communicated to leadership as a structural blocker per LEARNINGS framing note |
| 2 | personal-learnings | Weekly digest fetch blocked by network allowlist (2 consecutive weeks) | 2026-04-27 | No fix applied between 2026-04-27 and 2026-05-04 failures |

**Action for Rosie:**
1. Surface any BLOCKERs from the private CONTEXT.md at interactive review — include days-since-flagged.
2. Confirm whether the ai-champion architecture constraint has been communicated to the relevant stakeholders per the LEARNINGS framing note ("phrase it as an architecture constraint, not a bandwidth choice").

---

## Proposed checklist changes

These are proposals only — Rosie decides. No changes have been made to any governance documents. Items carried over from prior retros are noted with flag count; items flagged 3+ times may warrant either acceptance or an explicit "rejected — reason" status to close the loop.

### Carryover proposals (from 2026-04-29 and earlier)

**#1 — output-checklist.md §4 Ready-to-use criteria (2nd flag):**
> Extend the existing "verified directly" item: after "…not inferred from conversation history," add: "For any done/not-done status claim or 'has this shipped' question that shapes a next action, read the artifact itself (the file, the commit, the sent message) — not the CHANGELOG line, CONTEXT entry, or retro table describing it. Descriptors are surrogates."
> *(from Root LEARNINGS 2026-04-25: "Verify to the artifact, not to a surrogate")*

**#2 — Root CLAUDE.md — Luma invocation guidance (2nd flag, unverifiable):**
> New item after pre-dispatch discipline rule: "Outside-lens diagnostic trigger: when inside-lens candidates all share an axis the controller didn't explicitly choose, that's a Luma category #4 signal. Dispatch with a scoped outside-lens brief. One sub-agent, narrowly scoped. Do not rank harder inside the wrong axis."
> *(from Root LEARNINGS 2026-04-23: "Outside-lens diagnostics")*

**#3 — output-checklist.md §1 Team Lead framing (3rd+ flag):**
> New item under §1: "Defensive language scan: for any pull-not-push artifact or outward-facing deliverable, scan for defensive patterns ('without spoiling,' 'keeps X private,' 'limited version of,' 'doesn't include') and rewrite to affirmative demonstration."
> *(from Root LEARNINGS 2026-04-16: "Demonstrate-vs-guard")*

**#4 — Root CLAUDE.md §State update protocol (3rd+ flag):**
> New step before step 1: "Workspace-assignment gate: before the first P4 write of any session, confirm which workspace owns the work. The default (whatever's in context) is the drift vector. Ask: 'which workspace owns this work?' before writing CONTEXT.md or CHANGELOG.md."
> *(from Root LEARNINGS 2026-04-16: "P4 workspace-assignment before first state write")*

**#5 — docs-sync/CLAUDE.md §Pipeline architecture (2nd flag):**
> Add invariant note after pipeline diagram: "Two-stage detection invariant: revision counter = cheap pre-filter (skip full fetch if counter hasn't moved); content hash = authoritative signal filter (determine whether section content actually changed). Do not collapse into one step. Tighten the hash before relaxing the two-stage design."
> *(from docs-sync LEARNINGS: "Two-stage change detection")*

**#6 — kb-architecture/CLAUDE.md §Content drafting rules (2nd flag):**
> New subsection "GDoc formatting workflow":
> "(1) Read the reference document's full structure via API (named styles, paragraph styles, text styles, table cell styles). (2) Read the target document's named styles to identify divergences. (3) Build the formatter to explicitly set every property that differs from the target doc's defaults. (4) Test on ONE snippet, read it back via API, diff against reference — do NOT rely on visual inspection. (5) Lock the format in a spec doc before batch-writing."
> *(from kb-architecture LEARNINGS 2026-04-01: "On Google Docs API formatting")*

### New this cycle

**#7 — Hook tracking path for P10 retro (new):**
> The hook currently measures last-retro date from public `_retro/` draft files. Interactive retros produce private narratives; their dates are visible in `retros/*.yaml` sidecar files (e.g., `retros/2026-05-03-p4.yaml`). The two tracking surfaces diverged this cycle by 4 days. Suggested fix: hook should also check `retros/*.yaml` `retro_date` fields and take the more recent of the two surfaces.
> *(from this retro: hook tracking discrepancy)*

---

## Suggested interactive review agenda

1. Confirm or correct "what shipped well" summary — does it accurately reflect what ran since 2026-04-29? (The 2026-05-03 interactive P10 may have captured some of this already.)
2. **Workspace CHANGELOG.md gap (3rd flag, P2 threshold):** confirm triage from prior reviews. If still open: create now or name concrete session + owner. If deferred: name defer condition.
3. **personal-learnings digest:** decide on fix path (allowlist / alternative source / suspend).
4. **Unpropagated learnings #3 and #4 (3rd+ flag, P2 threshold):** accept, modify, or explicitly reject with reason — these can't stay in limbo.
5. Confirm items #1, #2, #5, #6 (2nd flag): same decision.
6. Surface any BLOCKERs from private CONTEXT.md with days-since-flagged.
7. **Hook tracking discrepancy (new):** confirm whether proposal #7 is worth fixing.
8. Review checkpoint-bar trend (is 23% miss rate improving session-over-session?).
9. Invoke Teacher (P10 step 6.5) for structured proposals if desired.

---

## Status

DRAFT — awaiting Rosie's interactive review.

No changes to `CLAUDE.md`, `output-checklist.md`, `agent-protocols.md`, or any workspace file have been made. All proposed changes above are recommendations only — Rosie decides.
