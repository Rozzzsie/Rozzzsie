# CLAUDE.md — KB Architecture 2026

## What this workspace is
*This workspace is where the fam is applied to KB programme management for AI
tooling. The four-stage pipeline and snippet authoring rules below are the
operational form that work takes.*

A Product Support knowledge bank for two AI products — an AI-powered media
analysis interface and a generative-AI brand monitoring tool. The KB is a
two-layer structure (Core Articles + modular Snippets), and this workspace
automates the detection of upstream product changes, the classification of
which KB articles they affect, and the drafting of updates — always behind a
human review gate.

## Orientation
Rosie is a Product Support lead building a KB programme for AI tooling.
Sign-off rules and output tone are defined at the repo root (see root
`CLAUDE.md`). She owns KB authoring directly — no sign-off is required to
publish — but scope and priority calls route through a co-owner on the KB work.

---

## First thing every session

1. Read `CONTEXT.md` — current project state, gap analysis, open questions
2. Read `LEARNINGS.md` — cross-session insights, traps to avoid, validated approaches
3. Check the local drafts store — are there pending drafts that need attention?
4. Run the Slack signal scan — signal channels for the two products, plus the
   project-comms channel for any stakeholder replies
5. Present a scan summary before proceeding

---

## The scope rule (apply this to everything)

> **In scope for KB:** UI behavior that intersects with AI output behavior
> **Out of scope:** Pure front-end bugs unrelated to AI behavior

When in doubt, ask: "Can a support agent use this to resolve a ticket?" If yes,
it belongs in the KB.

---

## Critical facts — never get these wrong

- **Agents read configuration, not instructions** — a confirmed, documented
  gap in the current KB: retrieval agents can be scoped by filter/config
  surfaces rather than by project-level instructions. Do not write anything
  that contradicts what config surfaces can actually scope.
- **The media analysis interface's outputs are non-deterministic by design** —
  variability is expected behavior, not a defect. Never frame it as a bug.
- **Sales framing must not appear in support language** — internal GTM and
  sales enablement references are reference-only. Translate positioning; do
  not reproduce it.
- **The media analysis interface does not use the open internet** — it is
  grounded in account data only.
- **Prompts in the brand monitoring tool cannot be edited after creation** —
  deletion permanently removes data. Always warn before delete.

---

## Upstream source authority hierarchy

| Priority | Document type | Rule |
|----------|---------------|------|
| 1 — Must not contradict | Official product FAQ | Official definitions |
| 2 — Current truth | Release notes (current year) | Defines current vs. legacy |
| 3 — Variability framing | Data quality changelog | Governs all variability explanations |
| 4 — Hard boundary | Source coverage doc | What data is / isn't used |
| 5 — Translate only | Sales enablement reference | Positioning, not support language |
| 6 — Do not expose | Internal GTM deck | Internal framing only |

---

## Pipeline shape

The workspace runs a four-stage pipeline:

| Stage | What it does |
|-------|--------------|
| **Check** | Detect upstream source changes (safe — no model calls) |
| **Draft** | Classify which KB articles are affected, then draft updates |
| **Review** | Open a review interface for pending drafts |
| **Apply** | Publish approved drafts to Confluence (requires explicit confirmation) |

A separate signal scan covers the product Slack channels — treated as a signal
layer, not a structured document source.

**Rosie always reviews before anything is published. Never auto-publish.**

---

## Output targets

| Stage | Destination |
|-------|-------------|
| Working drafts | Google Docs (Snippet Library format) |
| Approved / published | Confluence (Product Support KB space) |

---

## Snippet Library (current state)

First build complete: 37 snippets across 8 buckets in a dual-audience format.

**Dual-audience format:** each snippet has Technical Notes (human agents) plus
a "For an AI chatbot" section (Customer-Facing Response + Bot Action).

| Bucket | Snippets |
|--------|----------|
| 1 — Access, Entitlement & Data Scope | 5 |
| 2 — AI Output & Answer Behavior | 6 |
| 3 — Agents | 5 |
| 4 — Projects & Saved Searches | 5 |
| 5 — Prompting Tools | 4 |
| 6 — Canvas & Response Transparency | 4 |
| 7 — Sharing, Exporting & Prompt Library | 5 |
| 8 — Escalation & Operational Boundaries | 3 |

A later stage handles incremental updates when upstream sources change.

---

## Content drafting rules (enforced — from LEARNINGS)

### Snippet format
- Every snippet MUST include the AI chatbot section with Customer-Facing
  Response + Bot Action from the start. Never draft without it — retrofitting
  means re-reading every snippet, doubling the work.
- Technical Notes must be **flat**: one "Refer to" line, one numbered list,
  one escalation rule. No bold sub-headings, no multi-section categories, no
  markdown tables. If categorical distinction is needed, embed it in the list
  items (e.g., "DO NOT ESCALATE: Non-deterministic output differences...").
- Customer-Facing Responses must be plain language — no internal doc
  references, no operational jargon. These are delivered by the AI chatbot
  directly to customers.

### Core Article references
- If a snippet has a matching sub-heading in the Core Article, use it. If not,
  default to the parent section. Do not invent sub-sections that don't exist.
- When the Core Article is updated with new sub-sections, revisit the
  reference map and promote any parent-level references.

### Subagent prompts for content drafting
- Include exact snippet-level specs in every prompt: title, Bot Action value,
  key facts, scope boundaries. Do not leave agents to infer from general
  context.
- Front-load the specifics — underspecified prompts produce mismatches that
  require review fixes.
- Explicitly state: "Do NOT update CONTEXT.md or CHANGELOG.md" in every
  implementer prompt.
- All content sections must be flat (no markdown tables, no bold sub-headings)
  — the GDoc formatter cannot handle them.

### Gap validation
- Cross-referencing upstream sources against existing articles is necessary
  but not sufficient. Periodically pressure-test the KB against real support
  tickets to surface gaps invisible in source documents.

---

## Supervise layer — MANDATORY

Before finalizing ANY deliverable in this workspace, execute the quality gate
and state update protocols in `_config/agent-protocols.md`. This is not
optional.

**Deliverables that trigger the quality gate in this workspace:**
- Snippets (drafts or published)
- Confluence KB articles
- Pipeline outputs (check / draft / apply results)
- Slack scan summaries
- Subagent prompts for content drafting

**After every deliverable:** run the output checklist, update `CONTEXT.md`,
append to `CHANGELOG.md`, capture learnings and propagate to rules if
applicable. Do not close a productive session without completing all four.

**After context compaction:** re-read this file + `CONTEXT.md` + the last 5
`CHANGELOG.md` entries before resuming.

> **Response gate — active every turn.** See root CLAUDE.md. Every tool-using
> response must pass the hard checkpoint before shipping. Hooks fire
> automatically after file edits (PostToolUse) and at session close (Stop).
> Checkpoint line is mandatory.

---

## What NOT to do

- Do not publish to Confluence without explicit confirmation from Rosie in
  this session
- Do not treat sales enablement or GTM references as authoritative for
  support language
- Do not frame AI output variability as a bug or defect
- Do not skip reading `CONTEXT.md` at session start
