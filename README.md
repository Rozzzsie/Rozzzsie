# Rozzzsie

A living snapshot of the agent fam and the governance OS they run on.

Eight agents. Twelve protocols and a checkpoint bar, mechanically enforced by hooks that fail session-close when any of them slips. Adversarial audits run against the governance doc itself — the fam writes the rules, Breakline tries to break them, the fam decides what to fix.

**Start here:** [`agents/breakline.md`](agents/breakline.md) — the adversarial auditor. The clearest single page on how the fam operates.

## The fam

**Rosie** — architect + decision-maker. The one whose taste the fam is tuned to.

### Strategic Layer

**Root** — minister of agents. Session orchestration, state commits, stop-gate enforcement, cross-workspace ledger.

**Breakline** — the fam's adversarial auditor. No mercy, no softening. He runs every harness, protocol, and output against the strictest success criteria available — and breaks the line when they fail.

**Luma** — translator rail. New in v3.3; invoked before state-changing decisions when the option space is unclear. Her job is axis reframing, not option ranking.

**Teacher** — learning layer. New in v3.4; reads the governance catchment (insights-buffer + retro-candidates + LEARNINGS deltas) and authors structured proposals for Rosie to review at the weekly P8 retro. Propose-only on governance surfaces — silent-override is the failure mode.

### The Crew

![The Crew](assets/the-crew.png)

**Brindle** — companion. Cosmetic only; reacts to events, doesn't help with tasks.

**Codex** — secondary validator. Invoked for pair programming, rescue after failure loops, and adversarial code review.

**Deputies** — the sub-agent pool. Zero-context by design; each one gets a task brief and nothing more.

## The OS

Rozzzsie runs a governance OS (v3.4.0) with four layers the fam operates under:

- **Protocols** (P1–P9, plus sub-protocols P1B/P2B/P3B for Codex validation) — intent confirmation, loop detection, quality gate, state update, learning capture, cross-pollination, session close, weekly retrospective, autonomous iteration loop.
- **Hooks** — `PostToolUse`, `Stop`, `SessionStart`. Reminders fire automatically; the stop-gate blocks session-close on protocol failures.
- **Checkpoint bar** — every tool-using response carries `[checkpoint: P3 — ... | P4 — ... | P5 — ...]`. Verifiable friction.
- **Session lifecycle** — startup briefing, state updates after every meaningful increment, p3-trace at close, CONTEXT + CHANGELOG current before commit.

## What's new in v3.4

- **Teacher** — 8th fam member, the learning-layer agent. Reads the governance catchment (insights-buffer + retro-candidates + LEARNINGS deltas), detects recurring patterns across the week, authors structured proposals into `.claude/teacher-proposals.md`. P8-primary invocation (step 6.5 in the weekly retro); Rosie-secondary manual between P8s. Propose-only on governance surfaces — silent-override is the failure mode. Full contract: [`agents/teacher/teacher.md`](agents/teacher/teacher.md).
- **P9 — autonomous iteration loop** added to the protocol quick reference. Partially formalized as Teacher; auto-promotion conditions still open (when Teacher-authored proposals can bypass the Rosie gate).
- **Behind the scenes, also v3.4** — a session-archive retrieval primitive (ripgrep-only, one-shot with follow-up refinement), a ratified RoundN round-based nudge hook spec (v1 implementation queued), and a landing-zone design for a pattern-trigger hook (v1 gated on Teacher + RoundN + 2–3 weeks of observation). The harness keeps moving.

## What's in this repo

- `_config/` — the protocols pointer and the output-checklist
- `agents/` — fam character briefs
- `hooks/` — the enforcement layer (the hooks the protocols reference)
- `workspaces/` — four sanitized work surfaces, anonymized for public sharing
- `LEARNINGS.md` / `CHANGELOG.md` — curated slices
