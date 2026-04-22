# Weekly Retrospective — 2026-04-22
**Status:** DRAFT — awaiting Rosie's interactive review
**Period:** 2026-04-16 through 2026-04-22
**Automated by:** P8 Supervise layer retrospective (SessionStart hook)

---

## Period

April 16–22, 2026. Today is the first retro; no prior retro baseline exists to compare against.

---

## What shipped well

### Governance OS (root-level)

**2026-04-20 — Protocols v3.4 + v3.4.2 (two-increment release):**
- Teacher (8th fam member) shipped: pattern detector + proposal author on the governance catchment. Invoked at P8 as step 6.5; propose-only on governance surfaces; strict-validated direct-write on a narrow pre-approved list.
- P9 (autonomous iteration loop) named in the protocol quick reference. Partially formalized as Teacher; auto-promotion conditions remain open.
- Brindle's two-repo architecture received its naming — "graduated" — closing a framing gap in the public surface.
- Reference layer named and operationalized: three-flavor taxonomy (activity / meta / reference) established for all future governance files. First canonical reference-layer file created.
- Cross-pollination convention added: reference files get pointer rows in workspace CLAUDE.md startup loadouts.
- Teacher gets a new catchment stream at P8: re-asked-question audit, alongside LEARNINGS deltas + retro-candidates + insights-buffer.

**2026-04-17 — types-of-work.md:**
- First OS capabilities reference artifact. 7 live types across 4 layers (Infrastructure / Workflow / Intelligence / Content) + 3 horizon items.
- Swept from all 4 active workspaces. Delivered to Dhruv Gupta as Ask 1 of council onboarding.

**2026-04-17 — Landing surface demonstrate-vs-guard pass:**
- Root README, root CLAUDE.md, and agent-protocols.md reframed per the 2026-04-16 LEARNINGS rule.
- CLAUDE.md: imperative startup voice → descriptive session startup; private files marked as private (not silently broken).
- agent-protocols.md: "why it's not here" defensive phrasing removed.
- README: narrative hook, start-here signpost to breakline.md, protocol count reconciled.
- hooks/README.md: 20-line orientation (hook-to-protocol map + three invariants) added.
- Rule applied within 24 hours of being written — fast propagation.

**2026-04-16 — Scope-drift cleanup:**
- System detected its own workspace-assignment mistake. 7-file migration executed; 22 CHANGELOG entries and ~20 CONTEXT.md commits moved to correct workspace.
- Learning written and captured in root LEARNINGS.md same session.

### Workspace delivery

No workspace-level CHANGELOG.md files exist in any of the four workspaces
(`ai-champion-2026`, `docs-sync-2026`, `kb-architecture-2026`, `team-leadership-2026`).
All four workspace CLAUDE.md files instruct "After every deliverable: ... append to CHANGELOG.md"
but no CHANGELOG.md has been created in any workspace.

Two interpretations: (a) no deliverables have been produced in any workspace yet, or
(b) deliverables were produced but CHANGELOG entries were not written (protocol compliance gap).

The root CHANGELOG.md is scoped to "Architectural shifts, not individual fixes" — workspace
deliverable entries belong in workspace-level files, not the root.

**Flagged for interactive review.** See Stale Blockers section.

---

## Recurring quality gaps

**1. Missing workspace-level CHANGELOG.md files (structural)**
Every workspace CLAUDE.md mandates "append to CHANGELOG.md" after deliverables, but none of
the four workspaces has a CHANGELOG.md file. If any productive workspace sessions have occurred,
those entries have been lost. If no workspace sessions have occurred yet, the gap is latent.
Either way, the files should exist (even if empty with a header) before the next workspace session.

**2. Unpropagated learnings volume (five from a single day)**
Five of the eight flagged unpropagated learnings in this retro were dated 2026-04-16 — the day
of the scope-drift event. That's a high volume in a short window. The learnings are high quality,
but propagation into rules was partial. Four of the five have no corresponding checklist item
or CLAUDE.md rule yet. This isn't a content problem — the insights are sharp. It's a mechanical
one: the learning-capture layer is working; the rule-propagation layer lagged.

**3. Root CONTEXT.md is private / not in repo**
The cross-workspace BLOCKER dashboard is private and not present in this workspace. This retro
cannot check for stale blockers against the standard. If BLOCKER flags exist in the private
CONTEXT.md, they are invisible to this automated process. Interactive review step with Rosie
should surface any known blockers manually.

---

## Unpropagated learnings

Eight learnings were flagged as having no corresponding rule in a CLAUDE.md or output-checklist.md.
Listed below with the implied rule and a suggested landing location for Rosie's review.

| # | Source | Learning | Implied rule | Suggested location |
|---|--------|----------|-------------|-------------------|
| 1 | Root LEARNINGS, 2026-04-16 | Demonstrate-vs-guard framing | Add checklist item to §1 L4 Framing: "Scan outward-facing paragraphs for defensive language patterns ('without spoiling', 'keeps X private', 'limited version of') — rewrite to affirmative demonstration." | output-checklist.md §1 |
| 2 | Root LEARNINGS, 2026-04-16 | Luma scope — authoring-work axis | "Consider Luma for authoring-axis decisions (design spec framing, character brief structure, narrative axis) not just state-change option-ranking." | Root CLAUDE.md, Luma invocation guidance |
| 3 | Root LEARNINGS, 2026-04-16 | Meta-review as third Luma shape | Add third invocation shape: meta-review (earlier-Luma + controller converged too cleanly → dispatch fresh instance on the *reasoning*, not the artifact). | Root CLAUDE.md, Luma invocation guidance |
| 4 | Root LEARNINGS, 2026-04-16 | External resource name availability | "Any plan step that calls an external create API must be preceded by a name-availability check step; expected output of the check named in the plan." | output-checklist.md §4 Ready-to-use criteria, or a new §13 |
| 5 | Root LEARNINGS, 2026-04-16 | P4 workspace-assignment before first state write | "New initiatives: explicit workspace-assignment decision before the first state write. Default is the current session context — ask 'which workspace owns this?' before writing CONTEXT.md or CHANGELOG.md." | Root CLAUDE.md §State update protocol |
| 6 | docs-sync LEARNINGS (undated) | Two-stage change detection invariant | "Do not collapse revision-counter pre-filter and content-hash signal-filter into one step. This invariant must survive future pipeline refactors." | docs-sync CLAUDE.md §Pipeline architecture |
| 7 | docs-sync LEARNINGS (undated) | Retrieval ≠ search for agent builds | "For any search-grounded agent: search (find pages) and retrieval (read pages) are separate steps. Agent must fetch full page content before answering." | output-checklist.md §6 or root LEARNINGS cross-workspace note |
| 8 | kb-architecture LEARNINGS, 2026-04-01 | GDoc formatting: build from reference | "Read the target doc's named styles before writing. Do not iterate visually — programmatic diff against reference doc is the test." Add the 5-step workflow as an operational rule. | kb-architecture CLAUDE.md §Content drafting rules |

**Items 2 and 3** (Luma invocation shapes) could be consolidated into a single "Luma invocation guide" section in root CLAUDE.md rather than separate entries.

---

## Stale blockers

The root CONTEXT.md (cross-workspace BLOCKER dashboard) is private and was removed from the
public repo (reverted 2026-04-20 in commit `14e9c2f`). No BLOCKER flags are readable by this
automated process.

Workspace CONTEXT.md files were scanned — none contain BLOCKER flags. All four files describe
workspace structure only and carry no active blocker state.

**Action for Rosie:** confirm whether any BLOCKERs exist in the private CONTEXT.md dashboard.
If yes, surface them here and calculate days-since-flagged.

Known structural blockers (derived from LEARNINGS, not explicitly flagged in CONTEXT.md):
- **ai-champion-2026:** chatbot optimization blocked at architecture layer — no KB ownership.
  Flagged in ai-champion LEARNINGS, no date recorded. Not escalated to a stakeholder yet
  (LEARNINGS notes: "framing to use with stakeholders" but no evidence it was sent).
  **Action:** confirm whether this has been communicated to the relevant leader.

---

## Proposed checklist changes

These are suggestions only — Rosie decides. None take effect until accepted in interactive review.

**Proposed additions to output-checklist.md:**

1. **§1 L4 Framing — new item:**
   > Defensive language scan: for any pull-not-push artifact or outward-facing deliverable, scan for patterns like "without spoiling," "keeps X private," "limited version of," "doesn't include" — rewrite to affirmative demonstration.
   *(from LEARNINGS: "demonstrate-vs-guard")*

2. **§4 Ready-to-use criteria — new item:**
   > Plan steps that call external create APIs (repos, buckets, DNS records, etc.) include a name/availability check step before the create call, with the expected output of the check named in the plan.
   *(from LEARNINGS: "external-resource-name-availability is a mandatory plan gate")*

**Proposed additions to root CLAUDE.md:**

3. **§State update protocol — new item (after step 1):**
   > Workspace-assignment gate: before the first P4 write of any session, confirm which workspace owns the work. The default (whatever's in context) is the drift vector. If the session pivoted domains since startup, re-check.
   *(from LEARNINGS: "P4 state writes default to session-start workspace context")*

4. **§[Luma invocation] — new section:**
   > Three valid invocation shapes: (1) axis reframe — draft on wrong axis; (2) tightening pass — axis right, needs line edits; (3) meta-review — earlier Luma + controller converged too cleanly, dispatch fresh instance on the *reasoning*.
   > Luma applies to authoring-axis decisions (design spec structure, narrative framing, character brief shape), not just state-change option-ranking.
   *(from LEARNINGS: "Luma is for authoring-work axis" + "Meta-review is a third invocation shape")*

**Proposed additions to workspace CLAUDE.md files:**

5. **docs-sync CLAUDE.md — §Pipeline architecture — new invariant note:**
   > Two-stage detection invariant: revision counter = cheap pre-filter (skip the full fetch if counter hasn't moved); content hash = authoritative signal filter (decide whether sections actually changed). Do not collapse into one. Tighten the hash (e.g., normalize whitespace) before relaxing the two-stage design.

6. **kb-architecture CLAUDE.md — §Content drafting rules — new subsection:**
   > GDoc formatting workflow: read the target doc's named styles before writing (not after). The correct sequence: (1) read reference doc structure via API; (2) read target doc named styles; (3) build formatter to explicitly set every differing property; (4) test on ONE snippet, read back via API, diff against reference; (5) lock format before batch-write. Do NOT iterate visually.

**Structural question for Rosie:**
Should workspace-level CHANGELOG.md files be created now (one per workspace, with a header and no entries), or should this wait until the next productive session in each workspace? Creating them now closes the compliance gap; waiting avoids creating empty files that could be confused with "nothing happened."

---

## Status

DRAFT — awaiting Rosie's interactive review.

No changes to CLAUDE.md, output-checklist.md, or agent-protocols.md have been made.
All proposed changes above are recommendations only.

**Suggested interactive review agenda:**
1. Confirm or correct the "what shipped well" summary
2. Review the 8 unpropagated learnings — accept, modify, or defer each
3. Review the 6 proposed checklist/CLAUDE.md changes — accept, modify, or defer each
4. Surface any BLOCKERs from the private CONTEXT.md
5. Decide on workspace CHANGELOG.md creation
6. Invoke Teacher (step 6.5) for structured proposals if desired
