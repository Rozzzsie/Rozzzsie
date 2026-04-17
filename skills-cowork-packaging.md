# Skills + Co-Work — Packaging Claude for Product Support

*Not a chat guide. A packaging proposal: how Claude.ai's tooling layers map to PS workflows, and what it would take to roll them out org-wide.*

---

## The two-part system

| Layer | What it is | Who invokes it | Fits when |
|-------|-----------|----------------|-----------|
| **Skills** | A reusable procedure — structured prompt + reference docs, invocable anywhere | Any Claude.ai user (chat) or Co-Work agent (desktop) | The workflow requires a human in the loop before the output lands at the end-user |
| **Co-Work** | An autonomous desktop agent — plans, executes, and schedules tasks on cadence | Claude Desktop (scheduled or on-demand) | The workflow is non-HITL: output lands at the end-user without a quality gate stop |

Skills and Co-Work are complementary, not competing. A Skill is the procedure layer — *how* to do something. Co-Work is the execution layer — *who* (or what) runs it and *when*.

**The routing test — which layer fits a workflow?**
> Does the output need a human decision point before it lands at the end-user?
> - **Yes** → Skills (human in the loop, invokes and reviews)
> - **No** → Co-Work (autonomous, scheduled, lands directly)

---

## Where each layer fits in PS

### Skills — real-time, human-invoked

The rep is in the loop. They invoke the skill, review the output, decide what to send.

Skills handle:
- **Frontline ticketing** — parse the ticket, classify it, draft a reply + PSX handoff summary
- **Any triage workflow** — escalation checklists, onboarding procedures, structured classification
- **In-the-moment judgment calls** — wherever the output needs a human decision point before it reaches the customer

### Co-Work — scheduled, autonomous

No human in the loop at each step. The process runs on cadence and the output lands directly.

Co-Work handles:
- **Weekly performance snapshots** — pull metrics, extract signals, generate the report, deliver to the channel
- **Recurring batch work** — scanning, summarizing, filing across multiple sources on a schedule
- **Standardized reporting** — any fixed process that produces the same output shape every time, without nuance or exception handling

---

## The proof-of-concept: Klear Ticket Troubleshooter

A live Claude.ai Skill built for the Klear PSX workflow.

**What it does:**
- Parses an inbound Klear ticket
- Classifies it: inquiry / problem / admin request
- Drafts a customer-facing reply + a PSX handoff summary, ready to paste

**How to invoke:**
1. Open Claude.ai → Customize → Skills
2. Upload `SKILL.md` + all files from the `reference/` folder
3. Start a new conversation and invoke the skill
4. Pull the ticket directly via Intercom MCP — no export or attachment needed

**What it demonstrates:**
- Expert knowledge packaged once, reusable by the whole team
- The same skill works in chat (rep invokes) or Co-Work (agent invokes on schedule)
- The pattern extends: any product's triage workflow can be packaged the same way

---

## What org packaging looks like

**Skills rollout:**
1. Identify the highest-friction triage workflows across PS teams
2. Package each as a Skill (SKILL.md + reference folder)
3. Upload to Claude.ai → distribute the file set to the team
4. One training session, one workflow, one demo — that's the onboarding

**Co-Work extension (non-HITL workflows only):**
1. Identify recurring reports with a fixed output shape and no human review gate
2. Configure as a Co-Work scheduled task (requires Claude Desktop)
3. Define the output destination — Slack channel, shared doc, etc.
4. Set the cadence — it runs without manual triggering

**Who owns what:**
- **Skills:** whoever owns the workflow owns the skill. The PS rep closest to the problem builds and maintains it.
- **Co-Work tasks:** team lead or ops owner configures the scheduled task. Output destination determines who reviews.

---

## Open questions for the council

- Which PS workflows are highest-friction and most standardized? → Skill candidates
- Which recurring reports have a fixed output shape and no HITL gate? → Co-Work candidates
- What's the maintenance model — who updates a skill when the underlying procedure changes?
- How do Skills interact with MCP connectors already in play (Intercom MCP, Confluence MCP)?
