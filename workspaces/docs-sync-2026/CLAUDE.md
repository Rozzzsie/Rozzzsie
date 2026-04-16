# CLAUDE.md — Cross-Team Docs Sync 2026

## What this workspace is
*This workspace is where the fam is applied to cross-team documentation ownership. The two-mode shape below is the operational form that work takes.*

Two modes: an Ops pipeline that drafts Confluence updates from detected source
changes, and a Q&A mode that answers product questions with Confluence-backed
sources. Together they keep an internal product Playbook in sync with ongoing
product changes for an influencer marketing platform and serve as a live
knowledge assistant for Product Support questions grounded in that Playbook.

## Orientation
Rosie is a Product Support lead working on cross-team documentation ownership
for an influencer marketing platform. Sign-off rules and output tone are
defined at the repo root (see root `CLAUDE.md`). She owns the
Confluence Playbook directly — no sign-off is required to publish — but
strategic scope and priority calls route through the Product Support &
Engineering lead.

---

## Mandatory startup — every session

1. Read `CONTEXT.md` for last-run date and current source status
2. Count pending drafts in the local drafts store (ground truth for review backlog)
3. Read today's auto-generated Slack signal scan (if present) — filter for
   platform-relevant signals only
4. Present a status briefing **before doing anything else**

> Note: The Slack signal scan runs automatically via SessionStart hook —
> covers the channels configured for this workspace.
> The scanner uses a **User OAuth Token** to read channels via Rosie's own
> membership. A separate **Bot Token** is only used by the FAQ Agent for
> posting. Do not swap these.
> The Google Docs drift check is a separate Ops step — only run when
> triggered in Ops mode.

### Status briefing format
```
Cross-Team Docs Sync — [today's date]
Last check: [N days ago / today] ([date])
Pending drafts: [N] awaiting review
Slack signals: [N platform-relevant / none] (from today's scan)
→ Recommended next action: [one clear suggestion]
```

---

## Two modes

### Ops mode
Triggered by: "run check", "review drafts", "apply", or any pipeline task.

**Workflow:**
1. Check the PS&E lead DM for new insights — surface anything
   platform-relevant before running
2. Run the pipeline check — detects changes, classifies them, drafts updates
3. Review generated drafts in the local drafts store
4. Apply approved drafts one at a time (or `--dry-run` to preview)

> Consolidation rule: multiple section changes on the same Confluence page
> should fold into a single draft per page before applying. This is both a
> cost control and a review-quality control.

### Q&A mode
Triggered by: any product question.

Steps:
1. Search the PS&E lead DM for relevant context
2. Use the local page map to identify the most relevant Confluence pages
3. Fetch live content from those pages via the Confluence client
4. If the question touches recent product changes, also check the platform's
   public product-updates page (login-gated, JS-rendered; ask Rosie to paste
   content if the scrape fails)
5. Answer with page titles + Confluence links as sources
6. If Rosie adds context that wasn't in Confluence, note it as a KB gap to address

---

## Pipeline architecture

```
change signal
    ↓
section classifier  ← keyword match → detected sections → filter the full
    ↓                   page set down to the relevant subset
classification      ← Claude classifies against the filtered page list
    ↓                   (not the full set — keeps token cost down)
drafter             ← Claude drafts the Confluence update
    ↓
review / apply      ← Rosie reviews + publishes
```

Key artifacts:
- Full hierarchical page map — pipeline source of truth for which pages exist
- Section-classified reference map — used by the section classifier to pre-filter
  pages by topic; excludes pages flagged as work-in-progress, to-be-updated,
  or duplicate

## Subagent drafting workflow

When drafting Confluence updates via subagents instead of the pipeline:
1. Run the pipeline check in detect-only mode to enumerate change signals
2. Dispatch a classification agent with the change signals + page map — it
   identifies which pages are affected
3. Dispatch parallel drafting agents grouped by topic — each fetches live
   Confluence content via MCP, drafts updates, saves review files
4. Rosie reviews and applies

**Rules for subagent prompts:**
- Always provide the **raw source document**, not a summary — summaries lose
  details that matter for Product Support workflow impact
- Every draft MUST include a **"PS Workflow Impact" section** — this is the
  value-add over customer-facing changelogs
- Flag items needing engineering-lead confirmation in a **"Needs
  Confirmation" section**

## Dry run / pre-demo checklist

Before any demo or production run:
1. Verify Google OAuth is healthy (the refresh-token flow can fail silently;
   re-auth if it does)
2. Run the Slack signal scan so the day's scan is dated
3. FAQ Agent @mentions must come from the **Slack client** — MCP-sent
   messages do not trigger `app_mention` events
4. Dry-run the apply step before any live publish

---

## Supervise layer — MANDATORY

Before finalizing ANY deliverable in this workspace, execute the quality gate
and state update protocols in `_config/agent-protocols.md`. This is not
optional.

**Deliverables that trigger the quality gate in this workspace:**
- Confluence page updates (drafts or published)
- Slack scan summaries and platform signal reports
- Q&A responses with Confluence sources
- Pipeline check/apply outputs
- Stakeholder comms (to the Product Support & Engineering lead or the team)

**After every deliverable:**
1. Run output checklist (`_config/output-checklist.md`)
2. Update `CONTEXT.md` current state
3. Append to `CHANGELOG.md`
4. Capture learnings AND propagate to rules if applicable

**Do not close a productive session without completing all four steps.**

**After context compaction:** re-read this file + `CONTEXT.md` + the last 5
`CHANGELOG.md` entries before resuming.

> **Response gate — active every turn.** See root CLAUDE.md. Every tool-using
> response must pass the hard checkpoint before shipping. Hooks fire
> automatically after file edits (PostToolUse) and at session close (Stop).
> Checkpoint line is mandatory.

---

## What to always remember
- Drafts are **never auto-published** — every apply requires a manual command
- The page map is what Claude uses for classification — keep it fresh
- The section reference map drives the pre-filter — rebuild it if sections
  change significantly
- Rosie owns and manages this Confluence space directly — no sign-off
  required to publish
- Flag anything requiring the Product Support & Engineering lead's strategic
  input (scope, priorities) — but publishing itself is Rosie's call
- Think step by step before recommending actions
