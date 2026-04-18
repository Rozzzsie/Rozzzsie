# Rozzzsie

A living snapshot of the agent fam and the governance OS they run on.

Seven agents. Eleven protocols and a checkpoint bar, mechanically enforced by hooks that fail session-close when any of them slips. Adversarial audits run against the governance doc itself — the fam writes the rules, Breakline tries to break them, the fam decides what to fix.

**Start here:** [`agents/breakline.md`](agents/breakline.md) — the adversarial auditor. The clearest single page on how the fam operates.

## The fam

**Rosie** — architect + decision-maker. The one whose taste the fam is tuned to.

### Strategic Layer

**Root** — minister of agents. Session orchestration, state commits, stop-gate enforcement, cross-workspace ledger.

**Breakline** — the fam's adversarial auditor. No mercy, no softening. He runs every harness, protocol, and output against the strictest success criteria available — and breaks the line when they fail.

**Luma** — translator rail. New in v3.3; invoked before state-changing decisions when the option space is unclear. Her job is axis reframing, not option ranking.

### The Crew

![The Crew](assets/the-crew.png)

**Brindle** — companion. Cosmetic only; reacts to events, doesn't help with tasks.

**Codex** — secondary validator. Invoked for pair programming, rescue after failure loops, and adversarial code review.

**Deputies** — the sub-agent pool. Zero-context by design; each one gets a task brief and nothing more.

## The OS

Rozzzsie runs a governance OS (v3.3.1) with four layers the fam operates under:

- **Protocols** (P1–P8, plus sub-protocols P1B/P2B/P3B for Codex validation) — intent confirmation, loop detection, quality gate, state update, learning capture, cross-pollination, session close, weekly retrospective.
- **Hooks** — `PostToolUse`, `Stop`, `SessionStart`. Reminders fire automatically; the stop-gate blocks session-close on protocol failures.
- **Checkpoint bar** — every tool-using response carries `[checkpoint: P3 — ... | P4 — ... | P5 — ...]`. Verifiable friction.
- **Session lifecycle** — startup briefing, state updates after every meaningful increment, p3-trace at close, CONTEXT + CHANGELOG current before commit.

## What's in this repo

- `_config/` — the protocols pointer and the output-checklist
- `agents/` — fam character briefs
- `hooks/` — the enforcement layer (the hooks the protocols reference)
- `workspaces/` — four sanitized work surfaces, anonymized for public sharing
- `LEARNINGS.md` / `CHANGELOG.md` — curated slices
