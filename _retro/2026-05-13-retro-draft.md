# Weekly Retrospective — 2026-05-13
**Status:** DRAFT — awaiting Rosie's interactive review
**Period:** 2026-05-06 through 2026-05-13
**Automated by:** P10 Supervise layer retrospective (SessionStart hook)
**Prior retro baseline:** 2026-05-10 interactive P10 (full 8-step ritual; 167 catchment entries / 7d across all workspaces; 3 LEARNINGS shipped + 5 Teacher proposals authored + 1 Class-S subagent Write-permission gap RESOLVED at config layer). Prior automated draft: 2026-05-06.

> **Hook tracking discrepancy — same family as 2026-05-06 retro:**
> This draft was triggered because the SessionStart hook reads the last public `_retro/` draft date (2026-05-06) and fires at 7-day cadence. The last *actual* interactive P10 was 2026-05-10 (3 days ago). CONTEXT.md states next P10 due 2026-05-17. This automated draft is therefore 4 days early per the canonical P10 tracking surface (CONTEXT.md / retros/*.yaml sidecar). Same discrepancy flagged in the 2026-05-06 draft — the hook is reading a surrogate (last public draft date) rather than the artifact (last actual P10 sidecar date). This is the second consecutive automated draft showing this divergence. Proposal #7 from the 2026-05-06 retro (hook should also check `retros/*.yaml` `retro_date` fields) remains open.

---

## Period

2026-05-06 through 2026-05-13 (7 days per hook; effective productive window post-interactive-P10 is 2026-05-10 → 2026-05-13, 3 days). All git commits in this window are dated 2026-05-10 — the day of the interactive P10 session itself.

---

## What shipped well

### Governance OS / Root-level (since 2026-05-06)

**2026-05-09 — Sumi v1.0/v1.1/v1.2 trilogy (+ v1.3 the next day):**
The single largest architectural ship of the cycle. Sumi joined the fam as the 5th P3 enforcement rail in 24 hours across three sub-shipped versions, with the v1.3 drift-scan extension landing the following day.
- v1.0 morning: subagent-output-relay rubrics + Phase D 4-failure descope + minimum-viable Tools=[Read] profile + governance ship v3.9.3 → v3.10.
- v1.1 night: design-spec output_type + cross-check resolution + Tier B Read+Grep tool grant.
- v1.2 night: external-bound-paste-text output_type + stakeholders.council activation + additive-overlay rubric composition. Closes the original n=1 attribution-conflation catalyst that motivated Sumi's existence.
- v1.3 mid-day (2026-05-10): drift-scan invocation mode — walks every active rubric in `_config/sumi-rubrics.yaml`, verifies each anchor resolves in its declared source file, emits `drift_findings` verdict.
- Sub-ship pattern (3 commits per sub-ship: doctrine → build → governance) held across all three v1.x iterations. Eligible for canonical-spec template at n=4 when v2.x stakeholders-class ships.

**2026-05-10 — v3.10.3 ship:**
Checkpoint-bar PostToolUse format-validator + substantive-heuristic v2.
- NEW `LOOSE_BAR_PATTERN` detects bar-attempted-but-malformed turns; format-corrective action emits typo-specific corrective.
- `substantive_v2` mutation-tool-aware classification when `tool_names` provided.
- Closes Teacher proposal "checkpoint-bar Tier 2 PostToolUse extension" (Frame 3 corrective+formative + Option B PostToolUse per Luma framing). 53/53 tests green.

**2026-05-10 — v3.10.4 ship (Path A unified gate):**
Sumi v1.3 drift-scan invocation mode + MUTATION_TOOLS Conservative extension.
- Sumi gains second job: read-only drift-scan PostToolUse hook on output-checklist + sumi-rubrics edits, walks every active rubric, verifies anchor resolution.
- MUTATION_TOOLS frozenset extended `{Edit, Write, Bash}` → `{Edit, Write, MultiEdit, NotebookEdit, Bash}` (mcp__*-write deferred per stable-MCP-naming gate).
- Codex P3B caught 3 ship-blockers all fixed pre-ship, including `hookSpecificOutput` envelope cross-find parity-fix (silent failure since v3.10 ship).
- 94/94 tests green.
- Aggressive direction pre-staged as Teacher proposal (pending SDK MCP tool surface stabilization).

**2026-05-10 — Phase 1 doctrine ship — MD-vs-HTML deliverable format convention:**
- Luma F3 edit-locus reframe: 3 classes (Reading-bundles-HTML / Source-of-truth-MD / Hybrid).
- Output-side mirror of the v3.5 synthesis-surface pre-render pattern.
- Long-lived branch merge discipline (output-checklist §20) added.
- Novel "axis-coherent, evidence-weight-rejected" doctrine-tag for bundled-framing gates.

**2026-05-10 — Full P10 retro (interactive, 8-step ritual):**
- 167 catchment entries / 7d across all workspaces.
- 3 LEARNINGS shipped: §18 "Matcher discipline — structural over substring" + §19 "Reading-bundle rendering" + §20 "Long-lived branch merge discipline" all added to `_config/output-checklist.md`.
- §15(c) classification-check extension (layer-classification scope-conflation catch).
- 5 Teacher proposals authored (1 pending; rest at terminal status — executed or deferred with explicit watch entries).
- Class-S subagent Write-permission gap RESOLVED at config layer: `permissions.allow` block added to root `.claude/settings.json` with path-targeted Write rules per subagent contract (Teacher → proposals + insights-archive + input-archive; Luma → designs/).

**2026-05-10 — Dashboard v1.5 + v2.0 ship:**
- v1.5: re-render against 2026-05-10-p5 sidecar + v1.4 backfill; minor sidecar metric corrections (silent-failure-hunter row removed from v1.5 dispatch_axis).
- v2.0: sprint-2 multi-retro trend rendering **unlocked** — the gating condition (3+ sidecars at schema v1.0 stability review 2026-05-15) was crossed. First dashboard with cross-cycle trend data.

**2026-05-10 — Public repo sync (Phase 3 sub-ships 1+2+3):**
- Sub-ship 1 (governance): protocols rename 3.9.3 → 3.10.4 + symlink retarget + output-checklist §13–§20 sync.
- Sub-ship 2 (narrative): CHANGELOG architectural-grain entries + CONTEXT v3.10.4 refresh + LEARNINGS §14 extension + Sumi catalyst-vs-domain entry + README v3.10 section.
- Sub-ship 3 (security): personal-learnings/ confidentiality leak removed + .gitignore guard + retro-draft redaction.

**2026-05-10 — Sumi public agent card:**
- Placed in The Crew (sibling-shape to Codex P3B), NOT the Strategic Layer — corrected from initial draft anchored on "5th P3 enforcement layer" descriptor. This correction is itself a live instance of the layer-classification scope-conflation pattern (n=1 flagged at P10 §6c).

**2026-05-10 — retros/2026-05-10-p5.yaml sidecar:**
- First P10 with a parallel public narrative (`_retro/2026-05-10-p10-retro.md`). Prior interactive P10s (P3, P4) shipped sidecar-only.

---

### Workspace-level activity

No workspace `CHANGELOG.md` files exist in any of the four workspaces (`ai-champion-2026`, `docs-sync-2026`, `kb-architecture-2026`, `team-leadership-2026`). This scan cannot determine whether productive workspace sessions ran in this window.

**Structural observation (not a simple gap re-flag):** The 2026-05-10 P10 interactive retro references "167 catchment entries across 10 workspace CHANGELOGs" — implying that active CHANGELOGs exist in the private workspace. The public workspace directories (`workspaces/*/CHANGELOG.md`) are absent, but this may reflect public-vs-private surface split, not a P4 compliance gap. This hypothesis cannot be confirmed or denied from this automated scan. Rosie to confirm the architecture at interactive review.

---

## Recurring quality gaps

### 1. Hook tracking surface divergence — 2nd consecutive automated early draft

The SessionStart hook fires on `last public _retro/ draft date` + 7 days. The canonical P10 tracking surface (CONTEXT.md + retros/*.yaml sidecar) has the actual last-P10 date. These surfaces diverged by 4 days in the 2026-05-06 draft and again today (draft is 4 days early vs CONTEXT.md's "Next P10 due: 2026-05-17"). Proposal #7 from the 2026-05-06 retro remains open: hook should also scan `retros/*.yaml` `retro_date` fields and take the most recent surface.

**Action for Rosie:** confirm whether this draft is still useful given the P10 ran 3 days ago, or whether the hook's tracking surface should be recalibrated.

### 2. Root CHANGELOG coverage — dashboard v2.0 not captured

Dashboard v1.4 was logged in the root CHANGELOG. Dashboard v2.0 (sprint-2 multi-retro trend rendering unlocked — the gating milestone named explicitly in CONTEXT.md) shipped 2026-05-10 but is not in the root CHANGELOG. The CHANGELOG's stated grain is "architectural shifts, not individual fixes" and "the most valuable five." Dashboard v2.0 appears to meet that bar given: (a) the v1.4 precedent, and (b) the explicit "sprint-2 unlocks" language in CONTEXT.md.

**Action for Rosie:** confirm whether v2.0 should be in the root CHANGELOG, and whether any other 2026-05-10 commits (Sumi public card, security fix) warrant a root-level entry.

---

## Unpropagated learnings

### Resolved since 2026-05-06 retro (closed at 2026-05-10 P10)

| # | Source | Status |
|---|--------|--------|
| Verify-to-artifact extend §4 (from 2026-05-06 #1) | §14 comprehensive + all 10 sub-families codified in output-checklist | ✅ CLOSED |
| "Matcher discipline — structural over substring" | §18 added to output-checklist at P10 | ✅ CLOSED |
| "Reading-bundle rendering" | §19 added to output-checklist at P10 | ✅ CLOSED |
| "Long-lived branch merge discipline" | §20 added to output-checklist at P10 | ✅ CLOSED |
| Subagent Write-permission gap | Config-layer fix shipped at P10 | ✅ CLOSED |

### Carry-forward from 2026-05-06 retro

| # | Source | Learning summary | Implied rule target | Flag count | Status |
|---|--------|-----------------|---------------------|------------|--------|
| 1 | Root LEARNINGS, 2026-04-23 | "Outside-lens diagnostics" — when inside-lens candidates share an axis the controller didn't choose, dispatch a fresh outside-lens perspective. Do not rank harder inside the wrong axis. | Root `CLAUDE.md` — Luma invocation guidance (new item after pre-dispatch discipline rule) | **3rd flag** | Unverifiable (may be in private CLAUDE.md) |
| 2 | Root LEARNINGS, 2026-04-16 | "Demonstration vs guarding" — for pull-not-push artifacts, scan for defensive language patterns ("without spoiling," "keeps X private," "limited version of") and rewrite to affirmative demonstration. | `_config/output-checklist.md` §1 Team Lead framing — new "defensive language scan" item | **4th flag** (P2 threshold ×2) | Not propagated |
| 3 | Root LEARNINGS, 2026-04-16 | "P4 workspace-assignment gate" — before the first P4 write of any session, explicitly confirm which workspace owns the work. Default (current session context) is the drift vector. | Root `CLAUDE.md` §State update protocol — new step before step 1 | **4th flag** (P2 threshold ×2) | Not propagated |
| 4 | docs-sync LEARNINGS | "Two-stage detection invariant" — revision counter = cheap pre-filter; content hash = authoritative signal filter. Do not collapse. | `workspaces/docs-sync-2026/CLAUDE.md` §Pipeline architecture — explicit invariant note | **3rd flag** | Not propagated |
| 5 | kb-architecture LEARNINGS, 2026-04-01 | "GDoc formatting: build from reference, not scratch." 5-step workflow. Do NOT iterate visually. | `workspaces/kb-architecture-2026/CLAUDE.md` §Content drafting rules — new "GDoc formatting workflow" subsection | **3rd flag** | Not propagated |

**Items #2 and #3 are at 4th flag (P2 threshold crossed twice over).** These have been proposed in four consecutive retro drafts without a recorded accept, modify, or reject decision from interactive review. At interactive review, these need a terminal disposition: accept (execute), modify (specify what), or explicitly reject with reason.

### New this cycle

| # | Source | Learning summary | Implied rule target | Flag count |
|---|--------|-----------------|---------------------|------------|
| 6 | Root LEARNINGS, 2026-05-09 | "Catalyst-vs-domain conflation" — when a fix scopes to the catalyst's domain rather than the generalizable shape, the rule misses cases in other domains. Cross-check catalyst domain vs. shape domain at design-spec level before accepting the design. | `_config/output-checklist.md` new §21 or extension of §11 "Post-architectural-fix scope audit" | **1st flag** |
| 7 | docs-sync LEARNINGS | "Retrieval is the bottleneck, not the model" — search (find pages) and retrieval (read full page content) must be separate steps. The agent must fetch full content before it answers. Search excerpts are for ranking, not answering. | `workspaces/docs-sync-2026/CLAUDE.md` §Q&A mode — explicit "search ≠ retrieval" step separation rule | **1st flag** |

---

## Stale blockers

**Root CONTEXT.md:** sanitized public snapshot. Private BLOCKER dashboard not visible to this automated scan. CONTEXT.md reports no active BLOCKERs explicitly.

**Workspace CONTEXT.md files:** all four carry structural content only (workspace purpose, approval gates, pipeline shapes). No BLOCKER flags present in any public workspace CONTEXT.

**Inherited watch-list items from 2026-05-10 P10 (may become blockers at next retro):**

| # | Watch item | Source | Due at |
|---|-----------|--------|--------|
| 1 | n=4 threshold for Sumi-class governance-ship sub-ship pattern (currently n=3; v2.x stakeholders-class would tip to canonical) | P10 §7 | 2026-05-17 retro |
| 2 | Eyeball-rejection authority pattern (n=1; promote to §4 sub-bullet at n=2) | P10 §3 + §7 | 2026-05-17 retro |
| 3 | Retro-session-as-datapoint-source meta-pattern (n=2; structural fix shipped; confirm chain broken) | P10 §6a + §7 | 2026-05-17 retro |
| 4 | Aggressive MUTATION_TOOLS proposal execution trigger — has SDK MCP tool surface stabilized? | P10 §4b + §7 | 2026-05-17 retro |
| 5 | Teacher autonomy decision — Luma framing requested at next P10 | P10 §6d + §7 | 2026-05-17 retro |
| 6 | Layer-classification scope-conflation pattern — n=2 surfaces? | P10 §6c + §7 | 2026-05-17 retro |
| 7 | Codex P3B sibling-sweep discipline — n=2 catalyst surfaces? | P10 §5 + §7 | 2026-05-17 retro |
| 8 | Long-lived sprint branches conflict — n=2 on next worktree-based ship? | P10 §4c + §7 | 2026-05-17 retro |
| 9 | Public sidecar metric backfill — per-cycle tally script shipped? | P10 §7 | 2026-05-17 retro |

**Action for Rosie:** surface any BLOCKERs from the private CONTEXT.md at interactive review with days-since-flagged.

---

## Proposed checklist changes

These are proposals only — Rosie decides at interactive review. No changes to any governance document have been made by this automated draft.

### Carry-forward proposals (from prior retros, with updated flag counts)

**#2 — output-checklist.md §1 Team Lead framing (4th flag — P2 threshold ×2):**
> New item under §1: "Defensive language scan: for any pull-not-push artifact or outward-facing deliverable, scan for defensive patterns ('without spoiling,' 'keeps X private,' 'limited version of,' 'doesn't include') and rewrite to affirmative demonstration."
> *(Root LEARNINGS 2026-04-16: "Demonstrate-vs-guard")*
> **At 4th flag: requires terminal disposition at interactive review — accept, modify with specification, or reject with reason.**

**#3 — Root CLAUDE.md §State update protocol (4th flag — P2 threshold ×2):**
> New step before step 1: "Workspace-assignment gate: before the first P4 write of any session, confirm which workspace owns the work. The default (whatever's in context) is the drift vector. Ask: 'which workspace owns this work?' before writing CONTEXT.md or CHANGELOG.md."
> *(Root LEARNINGS 2026-04-16: "P4 workspace-assignment before first state write")*
> **At 4th flag: requires terminal disposition at interactive review.**

**#4 — docs-sync/CLAUDE.md §Pipeline architecture (3rd flag):**
> Add invariant note after pipeline diagram: "Two-stage detection invariant: revision counter = cheap pre-filter (skip full fetch if counter hasn't moved); content hash = authoritative signal filter (determine whether section content actually changed). Do not collapse into one step. Tighten the hash before relaxing the two-stage design."
> *(docs-sync LEARNINGS: "Two-stage change detection")*

**#5 — kb-architecture/CLAUDE.md §Content drafting rules (3rd flag):**
> New subsection "GDoc formatting workflow": (1) Read reference document's full structure via API. (2) Read target document's named styles for divergences. (3) Build formatter to set every differing property explicitly. (4) Test on ONE snippet — read back via API, diff against reference. Do NOT rely on visual inspection. (5) Lock format in spec doc before batch-writing.
> *(kb-architecture LEARNINGS 2026-04-01: "On Google Docs API formatting")*

### New this cycle

**#6 — output-checklist.md §11 extension or new §21 (1st flag):**
> When a fix or design is scoped based on a catalyst, cross-check: does the catalyst's domain match the shape's generalizable domain? If the rule/rubric/fix extends to a broader domain than the catalyst, name that domain explicitly and verify the rule fires correctly in it before accepting the design. The relabel is the load-bearing claim — verify it carries intent into the broader scope.
> *(Root LEARNINGS 2026-05-09: "Catalyst-vs-domain conflation")*

**#7 — docs-sync/CLAUDE.md §Q&A mode (1st flag):**
> Add explicit step-separation rule: "Search (find pages) and retrieval (read full page content) are separate steps. Search excerpts are for ranking, not answering. The agent must fetch full page body before it answers. This rule applies to every agent build with a documentation backend."
> *(docs-sync LEARNINGS: "Retrieval is the bottleneck, not the model")*

**#8 — Hook tracking path (carry-forward from 2026-05-06 #7, now 2nd flag):**
> Hook should also check `retros/*.yaml` `retro_date` fields and take the most recent of (last public `_retro/` draft date, last retro sidecar date). Prevents early automated drafts when the interactive P10 date is ahead of the public draft date.

---

## Suggested interactive review agenda

1. Confirm the correct interpretation of this draft's early-trigger — is the 2026-05-10 P10 treated as the anchor, or does this draft cover 2026-05-06 → 2026-05-13 as its own cycle?
2. Workspace CHANGELOG.md question: confirm whether active CHANGELOGs exist in the private workspace (which would explain the P10's "10 workspace CHANGELOGs" reference). If the public/private split is intentional, note it so the automated scan can account for it.
3. **Root CHANGELOG coverage (dashboard v2.0):** add entry, or confirm intentional omission.
4. **Unpropagated learnings #2 and #3 (4th flag, P2 ×2):** terminal disposition required — accept/modify/reject with reason. Cannot carry forward again without explicit rationale.
5. Confirm learnings #4 and #5 (3rd flag): accept, modify, or defer with explicit condition.
6. Review new proposals #6–#8 (1st flag).
7. **Hook tracking path (proposal #8, 2nd flag):** confirm fix direction.
8. Surface any BLOCKERs from private CONTEXT.md with days-since-flagged.
9. Review 2026-05-10 P10 watch-list: which items have reached n=2 in the 3 days since the P10? (Low probability given elapsed time, but worth checking session activity.)
10. Invoke Teacher (P10 step 6.5) if desired.

---

## Status

DRAFT — awaiting Rosie's interactive review.

No changes to `CLAUDE.md`, `_config/output-checklist.md`, `_config/agent-protocols.md`, or any workspace governance file have been made. All proposed changes above are recommendations only — Rosie decides.
