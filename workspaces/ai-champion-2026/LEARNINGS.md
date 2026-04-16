# LEARNINGS — AI Chatbot Enablement 2026

Non-obvious insights about the chatbot, the Product Support ticketing
interface, and this workspace.

---

## Workspace architecture — design around real work, not idealized process

Stage-based pipeline architecture (Path A / Path B with 5–6 stages each)
created more friction than value in this workspace. The real work is either
**recurring** (weekly snapshots), **ongoing** (procedure monitoring), or
**reactive** (flagged tickets) — none of which fits a linear stage pipeline.

Task-type folders (`snapshots/`, `procedures/`, `investigations/`,
`brainstorming/`) match how Rosie actually thinks about the work. The
pipeline was replaced in April 2026.

**Lesson:** design workspace structure around the types of work you actually
do, not around an idealized process model. If the workspace demands that you
invent stages for work that doesn't have stages, the workspace is wrong.

---

## Procedure-expansion pattern — monitoring first, procedures second

New topic-of-work areas enter via stakeholder directive — always on-demand
(no baseline data exists yet to trigger a performance-driven rollout). When
this happens, the discipline is:

- **First intervention is monitoring infrastructure, not procedures.** You
  need to see real conversations before you know what procedures to build.
- **Discovery window is 2–4 weeks.** Metric thresholds are directional
  during this period, not scientifically meaningful. Don't over-index on
  early numbers.
- **Procedure backlog is built from observed unresolved-question clusters**
  (3+ hits in one week), not from topics you assumed would be problems.

The temptation is to ship procedures on day one because the stakeholder is
waiting. Resist it. Procedures shipped blind are worse than no procedures —
they get written against imagined conversations, not real ones, and they
have to be rewritten within a month.

---

## Architecture constraints on chatbot optimization — KB ownership is the prerequisite

The pipeline approach Rosie has built in other workspaces — automated
doc-currency checks plus structured feeds for the AI to draw from — **cannot
extend to this chatbot**. The prerequisite is ownership of the underlying
knowledge base the AI reads from.

- **Where the pipeline works:** Rosie owns the foundational documentation in
  those workspaces, so she can build and run the pipeline end-to-end.
- **Where it doesn't:** this chatbot draws from the full Company product
  family KB. Rosie does not own that KB, so there is no reliable pipeline
  she can build on her own to optimize the chatbot's performance.

**Implication:** chatbot optimization is blocked at the architecture layer
for any pipeline-style intervention that depends on structured KB
maintenance. Improvements have to come through other paths — procedure
monitoring, unresolved-question clusters, routing adjustments, asset changes
approved through the product-leader gate — not through a Rosie-owned KB feed.

**Framing to use with stakeholders:** when explaining why this chatbot
isn't the experimental subject for the pipeline work, phrase it as an
architecture constraint, not a bandwidth choice. "I don't own the KB the
chatbot reads from" is factual, non-defensive, and surfaces a real
structural blocker worth leadership awareness.

---

## Build-inactive-by-default — review-before-live as a default posture

All new ticketing-interface assets (monitors, escalations, procedures) are
built INACTIVE. The product leader reviews them, then toggles live. Nothing
goes live unilaterally.

When requesting sign-off, send **one message with direct links to all assets
needing review**, not separate asks one at a time. The reviewer's time
budget for this is limited; batching is respect.

This is narrower than "get approval before shipping" — it's a specific
operational posture. The asset is built, configured, tested in draft state,
and then queued behind a single review message. That posture transfers to
any workspace where a reviewer gates a live system Rosie doesn't own the
runtime of.

---

## What good looks like — chatbot-work outputs

Final plans in this workspace are **Confluence-ready**:

- Plain English, numbered steps, no jargon
- Action steps specific enough to execute without further research — exact
  navigation paths, asset names, configurations
- Sign-off requirements explicitly named, not implied ("needs the product
  leader to toggle live" appears as a numbered step, not a footnote)
- Every plan defines a feedback loop: how do we know if this is working?
- Every plan names an owner per step

This standard exists because the default failure mode for chatbot-work
outputs is "thoughtful but not executable" — a doc that reads well in
review but leaves the next person guessing at three configuration details
they then have to chase down. Exec-ready discipline removes that chase.
