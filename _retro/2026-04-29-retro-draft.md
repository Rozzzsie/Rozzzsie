# Weekly Retrospective — 2026-04-29
**Status:** DRAFT — awaiting Rosie's interactive review
**Period:** 2026-04-23 through 2026-04-29
**Automated by:** P8 Supervise layer retrospective (SessionStart hook)
**Prior retro baseline:** 2026-04-24 interactive review (15/15 items triaged, CONTEXT.md)

---

## Period

April 23–29, 2026. This is the second full P8 cycle. The 2026-04-22 draft was reviewed interactively on 2026-04-24 per CONTEXT.md ("first full interactive in 15 days, 15/15 items triaged with terminal status"). That triage outcome is the prior baseline.

---

## What shipped well

### Governance OS (root-level)

**2026-04-23 morning — Protocols v3.4.3 — Luma translator → consultant promotion:**
- Luma formally promoted from translator rail to consultant: delivers weighted recommendation with evidence, ends in "But you decide."
- Four-role doctrine split finalized: Root (completeness + correctness), Luma (distillation + decision-shape + weighted recommendation), Teacher (proposal authoring), controller (decider). Rails explicitly non-overlapping.
- Three named axis-reframe sub-categories from the 2026-04-16 fam-debut cluster — *demonstrate-vs-guard*, *completeness-vs-shape*, *methodology-vs-character* — now carry session-log machine tags.
- Luma toolset extended `[] → [Read, Grep, Glob]` on root governance surfaces so she can verify artifacts directly rather than relying on handoff stuffing.
- Luma pre-dispatch discipline rule added: Root writes a 2-line handoff (Category + Options A/B/C each on a distinct decision axis) before dispatching; if either line can't be written, no dispatch.

**2026-04-23 evening — Protocols v3.5.0 + v3.5.1 — Synthesis-Surface Pre-Render Pattern:**
- New architectural primitive shipped: hook-side renders pre-compute mechanical content; agent fills `<JUDGMENT: ___>` slots inline.
- Reference implementation: SessionStart briefing reduced from 105s → 37s on clean state (65% reduction).
- v3.5.1 codified the bidirectional contract: Read face (hook renders card) + Write face (prior session writes to `.remember/remember.md`, capped ≤500 chars / ≤8 lines). The clean-state regression to 3m 9s was traced to an unbounded `.remember` block — write-side enforcement closes it.
- New LEARNINGS family: ship-validation gaps (clean-state baselines don't hold under real session load). Distribution-reading (median + p95 + max) replaces single-number-baselines.
- New PostToolUse hook instruments `session-start → first-tool-call` latency for P8 distribution reads.
- Fallback observability invariant: every synthesis surface must add a P8 audit step counting fallback markers. Default threshold: 2/week.

**2026-04-25 — Protocols v3.5.2 — sprint consolidation (three structural additions):**
- **P8 step 6.7 — Hook fire-rate audit:** Script consumes `.claude/hook-fires.jsonl` v1.0 schema; flags `🔴 SILENT-CANDIDATE` on <80% fire-rate and `🔴 ABSENT-FROM-FIRELOG` for hooks registered but missing from the firelog. Directly closes the months-long silent cwd-guard regression failure mode.
- **Checkpoint-bar Tier 2 corrective+formative hook:** PostToolUse hook reads transcript JSONL, classifies whether the prior turn was substantive, writes firelog record, emits corrective `additionalContext` on misses. Codex adversarial review caught two real defects pre-ship: mid-body bypass via unanchored regex (closed) and silent-exit on transcript I/O failures (closed).
- **Codex P3B mandatory for hook-lifecycle code:** Codex review now required before any commit touching SessionStart / Stop / PostToolUse / PreCompact. Precedent: 7 real defects across the 24h hook-lifecycle ship cluster.

**2026-04-25 — Dashboard v1.2 — governance observability layer:**
- First public-grain artifact that surfaces governance evolution without requiring the reader to navigate protocol docs, retro narratives, or proposals file.
- Frame 1 + Frame 3 stacked per Luma's layer-mismatch reframe: the v1.1 about-section weirdness was a category error (positioning prose ≠ dashboard element), not a styling problem.
- Hero gains 30-word "what this is" beat for cold landings; footer becomes a thin attribution band (industry-standard); README reordered to lead with positioning prose and collapse developer content into a `<details>` block.
- Render contract: `dashboard/render.py` reads most-recent sidecar from `retros/` → emits `dashboard/index.html` on push. Sprint-2 unlocks multi-retro trend rendering gated on sidecar schema stability review at 2026-05-15.

**2026-04-27 — personal-learnings workspace bootstrapped (partial):**
- `personal-learnings/` workspace and `_input/` folder created.
- Weekly digest agent run blocked: `aiagentstore.ai` fetch blocked by network allowlist. Failure documented at `personal-learnings/_input/2026-04-27_digest-fetch-failed.md` with both blockers (no workspace, blocked fetch) and fix path.
- No digest or analysis produced this cycle; failure documented rather than silently dropped.

---

## Recurring quality gaps

**1. Missing workspace-level CHANGELOG.md files — still unresolved (now 14+ days)**
This gap was flagged in the 2026-04-22 retro draft and may have been addressed in the 2026-04-24 interactive review — but the files still do not exist as of this automated scan. All four workspace CLAUDE.md files mandate "append to CHANGELOG.md" after deliverables; zero CHANGELOG.md files exist in any workspace. Either: (a) the 2026-04-24 review deferred this, or (b) the files were never created. The gap is now 14+ days old from first flag (2026-04-22). If workspace sessions have produced deliverables in this window, those CHANGELOG entries do not exist anywhere.

**Action for Rosie:** confirm triage outcome from 2026-04-24 review. If deferred: set a concrete session for creation. If missed: create now.

**2. Prior retro's unpropagated learnings — propagation status unconfirmed**
The 2026-04-24 interactive review triaged 15/15 items. This automated scan re-checks current file state for propagation (not triage outcome). Several items from the 2026-04-22 retro appear still absent from CLAUDE.md or output-checklist.md based on current file read (see Unpropagated Learnings section). These may have been triaged as "deferred" in the 2026-04-24 review — which is a valid terminal status — but the retro cannot distinguish "deferred" from "accepted but not yet executed" without Rosie's confirmation.

**3. personal-learnings fetch failure — structural gap in personal learning loop**
The network allowlist blocked `aiagentstore.ai`. If this is the primary source for the personal-learning digest, the loop is broken until the allowlist is updated. One failure documented is one signal; if it recurs next cycle with no fix, it becomes a pattern.

---

## Unpropagated learnings

The table below lists learnings with a Rule or Implication section that do not have a clearly corresponding rule in the relevant CLAUDE.md or `_config/output-checklist.md` based on current file state. Items from the prior retro that may have been deferred in the 2026-04-24 review are marked *(carryover — may be deferred)*.

| # | Source | Learning | Implied rule | Suggested location | Status |
|---|--------|----------|-------------|--------------------|--------|
| 1 | Root LEARNINGS, 2026-04-25 | Verify to the artifact, not to a surrogate — six sub-families | Broader than current checklist §4 (which covers external-system-state only). Rule should cover: for any done/not-done claim or "has this shipped" question that shapes a next action, read the artifact itself — not the CHANGELOG line, CONTEXT entry, or retro table that describes it. | output-checklist.md §4 (extend scope) or new §13 | **NEW this cycle** |
| 2 | Root LEARNINGS, 2026-04-23 | Outside-lens diagnostics — when inside lens converges on wrong axis, dispatch outside | "When the inside lens has converged on a small candidate set and they all share an axis the controller didn't explicitly choose, that's a Luma category #4 signal. Dispatch a fresh perspective. Outside-lens diagnostics are cheap (one scoped sub-agent) and produce findings the inside lens cannot." | Root CLAUDE.md §Luma invocation guidance (alongside or after the pre-dispatch discipline rule) | **NEW this cycle** |
| 3 | Root LEARNINGS, 2026-04-16 | Demonstrate-vs-guard framing | "Scan outward-facing paragraphs for defensive language patterns ('without spoiling', 'keeps X private', 'limited version of', 'doesn't include') — rewrite to affirmative demonstration." | output-checklist.md §1 Team Lead framing | *(carryover — may be deferred)* |
| 4 | Root LEARNINGS, 2026-04-16 | P4 workspace-assignment before first state write | "New initiatives: explicit workspace-assignment decision before the first P4 write. Ask 'which workspace owns this work?' before writing CONTEXT.md or CHANGELOG.md. Default (current session context) is the drift vector." | Root CLAUDE.md §State update protocol (new step before step 1) | *(carryover — may be deferred)* |
| 5 | docs-sync LEARNINGS (undated) | Two-stage change detection invariant | "Do not collapse revision-counter pre-filter and content-hash signal-filter into one step. This invariant must survive future pipeline refactors." | docs-sync CLAUDE.md §Pipeline architecture | *(carryover — may be deferred)* |
| 6 | docs-sync LEARNINGS (undated) | Retrieval ≠ search for agent builds | "For any search-grounded agent: search (find pages) and retrieval (read pages) are separate steps. Agent must fetch full page content before answering." | docs-sync CLAUDE.md §Q&A mode or root output-checklist.md §6 | *(carryover — may be deferred)* |
| 7 | kb-architecture LEARNINGS, 2026-04-01 | GDoc formatting: build from reference, not scratch | "Read the target doc's named styles before writing. The correct sequence: (1) read reference doc structure via API; (2) read target doc named styles; (3) build formatter to explicitly set every differing property; (4) test on ONE snippet, read back via API, diff against reference; (5) lock format before batch-write. Do NOT iterate visually." | kb-architecture CLAUDE.md §Content drafting rules — new subsection | *(carryover — may be deferred)* |

**Items not re-flagged (appear to have been propagated or adequately covered):**
- Ship-validation gaps (2026-04-23) → Protocols v3.5.1 CHANGELOG explicitly names the propagation; protocol doc is the enforcement layer. Consider adequate.
- External resource name availability (prior retro #4) → not visible in output-checklist.md §4. May still be missing. Rosie to confirm.

---

## Stale blockers

The root CONTEXT.md is a sanitized public snapshot — private BLOCKER dashboard is not present in this repo. Same limitation as the prior retro.

**Workspace CONTEXT.md scan:** all four workspace CONTEXT.md files carry no BLOCKER flags. They describe workspace structure and approval gates only.

**Known structural blockers (derived from LEARNINGS, not CONTEXT.md):**
- **ai-champion-2026:** chatbot optimization blocked at the architecture layer — Rosie does not own the KB the chatbot reads from. No direct pipeline optimization possible. First flagged in ai-champion LEARNINGS (undated). CLAUDE.md acknowledges the constraint ("Do not make assumptions about the chatbot's internal AI infrastructure") but no evidence it has been communicated to relevant leadership per the LEARNINGS framing note.

**Action for Rosie:**
1. Confirm whether any BLOCKERs exist in the private CONTEXT.md. If yes, surface them here with days-since-flagged.
2. Confirm whether the ai-champion architecture constraint has been communicated to the relevant stakeholder.

---

## Proposed checklist changes

These are suggestions only — Rosie decides. None take effect until accepted in interactive review. Items 3–7 from this list were also proposed in the 2026-04-22 retro; their triage outcome (accepted/deferred/rejected) from the 2026-04-24 review is unknown to this automated process. Rosie to confirm which are still open.

**New this cycle — proposed additions:**

1. **output-checklist.md §4 Ready-to-use criteria — extend existing "verified directly" item:**
   Current: "Any claims about external system state (API keys, credentials, live services, file contents, test results) were verified directly — not inferred from conversation history."
   Proposed extension: "…and for any done/not-done status claim or 'has this shipped' question that shapes a next action, read the artifact itself (the file, the commit, the sent message) — not the CHANGELOG line, CONTEXT entry, or retro table describing it. Descriptors are surrogates."
   *(from Root LEARNINGS 2026-04-25: "Verify to the artifact, not to a surrogate")*

2. **Root CLAUDE.md — Luma invocation guidance — new item:**
   > Outside-lens diagnostic trigger: when inside-lens candidates all share an axis the controller didn't explicitly choose (Root has been ranking on the wrong axis), that's a Luma category #4 signal. Dispatch with a scoped outside-lens brief: what does an outside perspective see that the inside lens is structurally forced to ignore? One sub-agent invocation, narrowly scoped. Do not rank harder inside the wrong axis.
   *(from Root LEARNINGS 2026-04-23: "Outside-lens diagnostics")*

**Carryover proposals (from 2026-04-22 retro — confirm triage outcome):**

3. **output-checklist.md §1 Team Lead framing — new item:**
   > Defensive language scan: for any pull-not-push artifact or outward-facing deliverable, scan for patterns like "without spoiling," "keeps X private," "limited version of," "doesn't include" — rewrite to affirmative demonstration.
   *(from Root LEARNINGS 2026-04-16: "Demonstrate-vs-guard")*

4. **Root CLAUDE.md §State update protocol — new item (before step 1):**
   > Workspace-assignment gate: before the first P4 write of any session, confirm which workspace owns the work. The default (whatever's in context) is the drift vector. Ask: "which workspace owns this work?" before writing.
   *(from Root LEARNINGS 2026-04-16: "P4 workspace-assignment")*

5. **docs-sync CLAUDE.md §Pipeline architecture — new invariant note:**
   > Two-stage detection invariant: revision counter = cheap pre-filter; content hash = authoritative signal filter. Do not collapse into one. Tighten the hash before relaxing the two-stage design.
   *(from docs-sync LEARNINGS)*

6. **docs-sync CLAUDE.md §Q&A mode — new rule:**
   > For any search-grounded agent: search (find pages) and retrieval (read pages) are separate steps. Fetch full page content before answering. Search excerpts are for ranking, not answering.
   *(from docs-sync LEARNINGS)*

7. **kb-architecture CLAUDE.md §Content drafting rules — new subsection:**
   > GDoc formatting workflow: (1) read reference doc structure via API; (2) read target doc named styles; (3) build formatter to explicitly set every differing property; (4) test on ONE snippet, read back via API, diff against reference; (5) lock format before batch-write. Do NOT iterate visually.
   *(from kb-architecture LEARNINGS 2026-04-01)*

**Open structural question (carryover):**
Should workspace-level CHANGELOG.md files be created now (header + no entries) or waited until the next productive session in each workspace? This was raised in the 2026-04-22 retro; triage outcome unknown.

---

## Suggested interactive review agenda

1. Confirm or correct the "what shipped well" summary
2. Confirm triage outcomes from 2026-04-24 review for carryover items (which were accepted, deferred, rejected?)
3. Review the 2 new unpropagated learnings (#1 and #2) — accept, modify, or defer each
4. Confirm status of carryover unpropagated learnings (#3–#7) — still open or previously deferred?
5. Review the 2 new proposed checklist/CLAUDE.md changes — accept, modify, or defer each
6. Confirm carryover proposals (#3–#7) — still open or previously deferred?
7. Surface any BLOCKERs from the private CONTEXT.md
8. Decide on workspace CHANGELOG.md creation
9. Invoke Teacher (step 6.5) for structured proposals if desired
10. Check hook fire-rate log (new in v3.5.2): first P8 cross-cycle observation since it shipped

---

## Status

DRAFT — awaiting Rosie's interactive review.

No changes to CLAUDE.md, output-checklist.md, or agent-protocols.md have been made.
All proposed changes above are recommendations only — Rosie decides.
