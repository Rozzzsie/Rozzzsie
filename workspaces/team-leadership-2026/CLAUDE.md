# CLAUDE.md — Team Leadership 2026

## What this workspace is
*This workspace is where the fam is applied to team leadership for a Product
Support (Frontline) team in the AI-powered support era. The four-stage
framework and rules below are the **operational** form that work takes.*

A structured workspace for Rosie's informal L4 leadership practice on a small,
remote team: supporting the team's manager on hiring, coaching peers and
mentees, drafting team communications, and driving visibility on team
performance. Every session produces a concrete artifact — a candidate
evaluation, a coaching plan, a team update, or a performance read — ready to
act on or hand to the manager.

## Orientation
Rosie is a Product Support lead doing informal team-leadership work alongside
her IC responsibilities. Sign-off rules and output tone are defined at the
repo root (see root `CLAUDE.md`). Rosie's manager is the final decision-maker
on hiring and cross-team positioning; Rosie's role is to produce structured,
specific, ready-to-use artifacts that make those decisions easier.

---

## First thing every session

1. Read `CONTEXT.md` — current state, stage directory, approval gates
2. Read `LEARNINGS.md` — validated patterns for reading candidates, coaching,
   and team-comms work
3. Scan `stages/` — are there pending outputs or stale initiatives?
4. Present a summary to Rosie before starting

---

## Stage directory

| Stage | Folder | When to use |
|-------|--------|-------------|
| **01 — Hiring** | `stages/01_hiring/` | Interview prep, candidate evaluation, hire recommendations |
| **02 — Coaching** | `stages/02_coaching/` | 1:1 prep, mentee development, skill-gap work, feedback drafting |
| **03 — Team comms** | `stages/03_team_comms/` | Team updates, async messages, knowledge sharing, announcements |
| **04 — Team performance** | `stages/04_team_performance/` | Team health reviews, performance insights, recommendations for the manager |

Sessions operate in one stage at a time. Navigate to the right stage and read
its local notes before producing output.

---

## The performance philosophy — the "main character" standard

Performance in the AI-powered support era is not just ticket volume,
resolution time, or CSAT. Those are table stakes. What the team is held to —
and what hiring, coaching, and performance reads are all oriented around — is:

- **Insight-sharing** — proactively surfacing patterns and observations;
  turning individual ticket experience into collective knowledge.
- **Continuous learning** — treating product and industry changes as
  opportunities, not obligations; building personal knowledge systems.
- **Creative problem-solving** — looking for better ways to do things;
  comfortable with ambiguity; finds a path forward anyway.
- **AI-era readiness** — treating AI tools as collaborators, not threats;
  understands how automation changes the support landscape.
- **Team contribution** — elevates the people around them; shares knowledge
  generously; shows up as a leader before the title arrives.

This standard applies across all four stages. In hiring it's the screen
(curiosity, composure, "main character" signals — not just correct answers).
In coaching it's the development target (the whole person, not just the
ticket handler). In team comms it's the cadence (create space for
insight-sharing, not just updates). In performance reads it's the story
(growth and contribution, not just metrics).

---

## Operational rules (enforced — from LEARNINGS)

### Hiring output format
- Always produce BOTH a per-competency scorecard with evidence AND a narrative
  summary. A scorecard alone is too cold; a narrative alone is too vague. The
  decision-maker needs both to make the call.
- Rosie's role is to produce structured, specific evaluations that make the
  manager's decision easier — not to advocate strongly for one outcome.

### Candidate evaluation signals
- "Main character" signals show up in HOW candidates talk about past
  challenges — ownership, learning, bringing others along — not just whether
  the answer is correct.
- Candidates who ask clarifying questions before answering behavioral prompts
  tend to perform better in practice. It signals thinking before acting.
- Composure under scenario-based questions is often more revealing than the
  answer itself.

### Cross-team work — visibility tactic, not admin routing
- Cross-post unanswerable cross-team work to a high-visibility team channel
  with the manager CC'd. Never drop the CC. Never solve cross-team questions
  silently in DMs.

### Cross-team work you can answer — draft a guidance note
- For cross-team questions Rosie can answer directly: draft a reusable
  guidance note, park it somewhere retrievable, then reply with the note as a
  pointer. Run the note through the output checklist.

---

## Supervise layer — MANDATORY

Before finalizing ANY deliverable in this workspace, execute the quality gate
and state update protocols in `_config/agent-protocols.md`. This is not
optional.

**Deliverables that trigger the quality gate in this workspace:**
- Candidate evaluations (scorecards + narrative summaries)
- Coaching plans, mentee feedback, 1:1 prep notes
- Team communications (async updates, announcements, knowledge-sharing posts)
- Performance reads and insight artifacts
- Guidance notes for cross-team questions

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

## What to always remember
- Rosie supports the team's manager — she does not act unilaterally as
  manager.
- Every output should be concrete and ready to use: a draft, a plan, a
  recommendation, or a structured set of notes.
- Flag anything that needs Rosie's manager or a cross-functional leader to
  sign off on explicitly.
- Think step by step before recommending actions.
- "Better performance" is not just ticket metrics — it's insight-sharing,
  continuous learning, and creative problem-solving in the AI-powered
  support era.

---

## What NOT to do

- Do not make hiring decisions or recommendations without the manager's
  sign-off
- Do not post cross-team communications under team identity without review
- Do not drop the visibility CC when cross-posting cross-team work
- Do not skip reading `CONTEXT.md` at session start
