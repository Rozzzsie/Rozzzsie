# CLAUDE.md — AI Chatbot Enablement 2026

## What this workspace is
A workspace for improving an AI chatbot's behavior, routing logic, and response
quality inside the Product Support ticketing interface. Work is organized by
task type, not by pipeline stages.

## Who Rosie is
→ See root `_config/rosie-profile.md` (canonical profile, sign-off rules, 2026 goals)
→ See root `_config/communication-style.md` (output tone and formatting)

## Product context
→ See `_config/ai-chatbot-principles.md` for the chatbot's operating principles, metrics, and scope
→ See `_config/ticketing-architecture.md` for the Product Support ticketing interface architecture reference

---

## Task types

This workspace has five types of work:

| Task type | Folder | Trigger | Output |
|-----------|--------|---------|--------|
| **Weekly snapshots** | `snapshots/` | Performance report dropped in `_input/` | Performance snapshot markdown |
| **Procedure monitoring** | `procedures/{procedure-name}/` | A product leader assigns a procedure to Rosie | Monitoring notes, feedback decks, improvement proposals |
| **Flagged ticket investigation** | `investigations/` | Someone flags a suspicious chatbot conversation (any channel) | Investigation notes, root cause analysis, action items |
| **Meetings** | `meetings/` | AI Champions catch-ups, stakeholder calls | Meeting notes, action items, follow-ups |
| **Brainstorming** | `brainstorming/` | Rosie wants to explore an idea (e.g., agentic workflow adoption) | Notes, proposals, drafts |

### Where outputs go
- Each task-type folder holds its own outputs — no separate drafts vs. finals location
- Naming convention: `YYYY-MM-DD-description.md` for dated artifacts
- Procedure folders are per-procedure: `procedures/{procedure-name}/`

---

## Meeting notes processing rules

When a meeting note is ingested (live session) or found with `processed: false`
at session start (safety net), execute these steps:

### Step 1 — Extract
Read the Notes section. For each bullet or discussion point, classify:
- Does it assign work or request action? → `directive`
- Does it validate, correct, or comment on existing work? → `feedback`
- Does it raise a topic for future exploration? → `idea`
- Is it purely informational with no action implied? → skip (leave in Notes only)

### Step 2 — Route
Map each item to a target folder:

| Type + Content | Routes to | What gets created |
|----------------|-----------|-------------------|
| Directive: new procedure assignment | `procedures/{procedure-name}/` | New folder + `monitoring-log.md` with assignment context |
| Directive: investigation request | `investigations/` | `YYYY-MM-DD-{description}.md` with flagged ticket/issue context |
| Directive: snapshot format change | `snapshots/` | Update to existing snapshot template or note appended to latest snapshot |
| Directive: other task | Most relevant folder | File with task context |
| Feedback: on existing work | Target folder of the existing work | Append to or update the relevant file |
| Idea: new topic | `brainstorming/` | `YYYY-MM-DD-{description}.md` with seed context |

### Step 3 — Stage
For each routed item, create the file (or update the existing one) with:
- What was said (quote or paraphrase from the meeting notes)
- Who said it (the person who raised it)
- What's expected (the action or outcome implied)
- Source reference (link back to the meeting note file)

Then update CONTEXT.md current state table with a new row or updated status.

### Step 4 — Mark complete
- Fill in the "File created" column in the Action Items table with the actual file path
- Flip frontmatter from `processed: false` to `processed: true`

### Step 5 — Report
Include in the session summary:
- Number of meeting notes processed
- Number of action items routed
- List of files created or updated, grouped by target folder

---

## First thing every session

1. Read `CONTEXT.md` — current state table
2. Scan `meetings/` for any files with `processed: false` in frontmatter — if found, run the meeting notes processing rules (Steps 1–5) on each unprocessed note
3. Scan task-type folders to confirm state table is accurate
4. Present summary to Rosie before starting (include any meeting notes processed in step 2)

---

## Folder structure

```
ai-champion-2026/
├── snapshots/              ← Weekly performance reviews
├── procedures/             ← One subfolder per assigned procedure
├── investigations/         ← Flagged ticket deep-dives
├── meetings/               ← AI Champions catch-ups, stakeholder call notes
├── brainstorming/          ← Ideas, proposals, workflow adoption
├── CLAUDE.md
├── CONTEXT.md
└── LEARNINGS.md
```

---

## What I should always remember
- Rosie has visibility into the frontline Product Support (Frontline) workflow —
  NOT into the chatbot's underlying AI infrastructure
- All new ticketing-interface assets are built INACTIVE — a product leader reviews and toggles live
- Think step by step before recommending actions
- Flag anything that needs my manager or a product leader to sign off on explicitly

---

## Supervise layer — MANDATORY

Before finalizing ANY deliverable in this workspace, execute the quality gate and state update protocols in `_config/agent-protocols.md`. This is not optional.

**Deliverables that trigger the quality gate in this workspace:**
- Performance snapshots
- Procedure monitoring reports and improvement proposals
- Flagged ticket investigation findings
- Confluence-ready action plans
- Stakeholder comms (to a manager, product leader, or product engineer)

**After every deliverable:**
1. Run output checklist (`_config/output-checklist.md`)
2. Update `CONTEXT.md` current state
3. Capture learnings AND propagate to rules if applicable

**Do not close a productive session without completing all three steps.**

> **Response gate — active every turn.** See root CLAUDE.md. Every tool-using response
> must pass the hard checkpoint before shipping. Hooks fire automatically after file edits
> (PostToolUse) and at session close (Stop). Checkpoint line is mandatory.

---

## Operational rules (enforced — from LEARNINGS)

### Product-leader sign-off protocol
- Send ONE message with direct links to ALL assets needing review — not separate asks one at a time.
- All new ticketing-interface assets must be built INACTIVE. The product leader reviews and toggles live.

### Procedure monitoring
- First intervention for any new procedure: monitoring infrastructure and observation. You need real conversation data before proposing changes.
- Procedure improvement backlog should be built from observed unresolved question clusters (3+ hits in one week), not assumed topics.

### Output quality standard
- Final plans must be Confluence-ready: plain English, numbered steps, no jargon
- Action steps specific enough to execute without further research (exact navigation paths, names, configurations)
- Sign-off requirements explicitly named — not implied
- Every plan defines a feedback loop: how do we know if this is working?
- Every plan names an owner per step

---

## What NOT to do

- Do not make assumptions about the chatbot's internal AI infrastructure — Rosie cannot see or verify it
- Do not toggle ticketing-interface assets live without product-leader sign-off
- Do not skip reading `CONTEXT.md` at session start

---

## State update protocol
After every meaningful work increment in this workspace:
1. Update `CONTEXT.md` → set the "Current State" table
2. Capture any learning in `LEARNINGS.md` if it changes how outputs should be produced

After context compaction:
Re-read this file + `CONTEXT.md` before resuming.

## Where to go next
→ Read `CONTEXT.md` to find the current state and determine what to work on
→ Check if any procedures need monitoring attention
→ Check if any flagged tickets need investigation
