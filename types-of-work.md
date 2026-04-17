# Types of Work — Rozzzsie OS

*Not a task list. A map of the patterns of work this OS compresses, catches, and holds.*

---

| Layer | Type |
|---|---|
| Infrastructure | Knowledge maintenance — monitors sources, detects drift, drafts updates, queues for human review |
| Infrastructure | Slack knowledge agent — answers internal product questions in real-time from docs, in-thread |
| Infrastructure | Codified workflows *(Claude.ai Skill)* — structured runbook: parse → classify → templated outputs, ready to invoke |
| Workflow | Meeting → action routing — classifies items, routes to right folder, creates follow-up files |
| Intelligence | Performance intelligence — raw metrics → signals → calibrated snapshots + auto-slides |
| Intelligence | Structured judgment — complex inputs → concrete recommendation for a decision-maker |
| Content | Dual-audience content — same material in two registers: human notes + bot-ready format |

---

## Infrastructure

**Knowledge maintenance**
Monitors upstream sources (product release docs, slide decks, Slack channels), detects when documentation has drifted from reality, classifies which pages are affected, drafts updates, and queues them for human review before anything publishes.
→ *Live:* Klear docs sync pipeline; MIRA/GAIL KB pipeline
→ *Could extend to:* any team's Confluence, Notion, or internal wiki

**Slack knowledge agent**
A PS rep @mentions the bot, it searches the internal playbook, and replies in-thread with grounded, sourced answers — no human researcher in the loop.
→ *Live:* KlearPlaybookAgent (210-page Klear Playbook + 73 FAQ cases)
→ *Could extend to:* any product's internal support Slack workspace

**Codified workflows** *(Claude.ai Skill)*
Packages expert knowledge into a structured, invocable runbook: parse the input, classify it, produce templated outputs ready to use.
→ *Live:* Klear Ticket Troubleshooter — parse exported ticket → classify (inquiry / problem / admin request) → draft customer reply + PSX handoff summary
→ *Could extend to:* any triage workflow, escalation checklist, or onboarding procedure

---

## Workflow

**Meeting → action routing**
Ingests meeting notes, classifies each item as a directive, feedback, or idea, routes to the right workspace, creates follow-up files, and marks processed. No manual filing.
→ *Live:* AI Champions catchup processing
→ *Could extend to:* any recurring meeting with structured follow-up requirements

---

## Intelligence

**Performance intelligence**
Takes raw metrics data, extracts signals, and produces structured snapshots calibrated to the audience — with auto-generated presentation slides.
→ *Live:* Weekly Mel APAC performance snapshots (deflection rate, CX score, CSAT) + Google Slides auto-deck
→ *Could extend to:* any recurring metrics → stakeholder report cycle

**Structured judgment**
Takes complex, multi-signal inputs — candidate responses, team dynamics, performance patterns — and produces a concrete recommendation ready for a decision-maker to act on.
→ *Live:* Hiring scorecards + narratives; team performance summaries; L4 operating pattern artifacts
→ *Could extend to:* any domain where the bottleneck is synthesizing judgment, not gathering information

---

## Content

**Dual-audience content**
Produces the same material in two registers simultaneously — human agent notes and bot-ready format in a single artifact. One source, two outputs.
→ *Live:* MIRA Snippet Library (37 snippets — each with Technical Notes for human agents + Customer-Facing Response + Bot Action for Mel)
→ *Could extend to:* any documentation that needs to serve both human and AI consumers

---

## Horizon — for the council to build on

- **Proactive risk surfacing** — flags when a rep's ticket pattern diverges from KB coverage before a CSAT cliff
- **Cross-team gap propagation** — a product gap surfaced in one team's KB surfaces automatically for the adjacent team before it creates a second incident
- **New-member onboarding** — an incoming PS rep gets a personalized reading path built from the existing knowledge infrastructure
