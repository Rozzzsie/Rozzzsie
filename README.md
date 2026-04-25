# Rozzzsie

A living snapshot of the agent fam and the governance OS they run on.

Eight agents. Twelve protocols and a checkpoint bar, mechanically enforced by hooks that fail session-close when any of them slips. Adversarial audits run against the governance doc itself — the fam writes the rules, Breakline tries to break them, the fam decides what to fix.

**Start here:** [`agents/breakline/breakline.md`](agents/breakline/breakline.md) — the adversarial auditor. The clearest single page on how the fam operates.

**Live dashboard:** [**rozzzsie.github.io/Rozzzsie/dashboard/**](https://rozzzsie.github.io/Rozzzsie/dashboard/) — the OS observing itself. Decision velocity, discipline metrics, Luma tally by category, proposal backlog cohort flow, latency observations, full findings detail with status pills, meta-finding callout. Renders mechanically from the most recent P8 retro sidecar at [`retros/`](retros/) on every push to `main`. Sprint-1 v1: single-retro snapshot; sprint-2 unlocks multi-retro trend rendering once 3+ sidecars accumulate. The arxiv anchor is [EDD 2024](https://arxiv.org/abs/2411.13768) — *evaluation as continuous governing function, not terminal checkpoint.*

## The fam

**Rosie** — architect + decision-maker. The one whose taste the fam is tuned to.

### Strategic Layer

**Root** — minister of agents. Session orchestration, state commits, stop-gate enforcement, cross-workspace ledger.

**Breakline** — the fam's adversarial auditor. No mercy, no softening. He runs every harness, protocol, and output against the strictest success criteria available — and breaks the line when they fail.

**Luma** — consultant rail. New in v3.3 as translator; promoted to consultant in v3.4.3 after her first organic post-promotion invocation produced a load-bearing axis-reframe that the controller would not have surfaced alone. She now delivers a weighted recommendation with evidence at the end of her frames, not just option enumeration. Toolset includes read access to the governance surface so she can verify artifacts she frames against. Her job is axis reframing first; recommendation second; option ranking never.

### The Crew

![The Crew](assets/the-crew.png)

**Brindle** — companion. Cosmetic only; reacts to events, doesn't help with tasks.

**Codex** — secondary validator. Invoked for pair programming, rescue after failure loops, and adversarial code review.

**Deputies** — the sub-agent pool. Zero-context by design; each one gets a task brief and nothing more.

**Teacher** — learning layer. New in v3.4; reads the governance catchment (insights-buffer + retro-candidates + LEARNINGS deltas) and authors structured proposals for Rosie to review at the weekly P8 retro. Never writes rules directly — silent-override is the failure mode.

## About Brindle

Brindle is the only fam member who ships as her own standalone product. The other seven live here as Claude Code subagents — each one's `.md` file IS the implementation, loaded by the Task tool at invocation time. Brindle's runtime is separate Python code, MIT-licensed, clonable: [`brindle-terminal-bunny`](https://github.com/Rozzzsie/brindle-terminal-bunny).

Her persona card still lives at [`agents/brindle/brindle.md`](agents/brindle/brindle.md) — that hasn't moved. The asymmetry is architectural, not accidental. Seven agents whose contracts live in this repo. One agent who graduated into a standalone product. The two-repo shape is intentional.

## The OS

Rozzzsie runs a governance OS (v3.5.2) with four layers the fam operates under:

- **Protocols** (P1–P9, plus sub-protocols P1B/P2B/P3B for Codex validation) — intent confirmation, loop detection, quality gate, state update, learning capture, cross-pollination, session close, weekly retrospective, autonomous iteration loop.
- **Hooks** — `PostToolUse`, `Stop`, `SessionStart`. Reminders fire automatically; the stop-gate blocks session-close on protocol failures.
- **Checkpoint bar** — every tool-using response carries `[checkpoint: P3 — ... | P4 — ... | P5 — ...]`. Verifiable friction.
- **Session lifecycle** — startup briefing, state updates after every meaningful increment, p3-trace at close, CONTEXT + CHANGELOG current before commit.

## What's new in v3.5 (cumulative through v3.5.2)

- **Synthesis-Surface Pre-Render Pattern (v3.5.0)** — a new architectural primitive: hook-side render scripts pre-compute mechanical content for synthesis-heavy surfaces, agent fills `<JUDGMENT: ___>` slots inline. Reference implementation: SessionStart briefing — ~60–90s of synthesis collapses to ~10–15s of slot-fill on clean state. Surfaces queued for the pattern: P8 weekly retro, P7 session-close summary, CONTEXT updates, compaction recovery. Inv 9 (silent-fallback observability) added: every synthesis surface gets a P8 retro audit step counting `FALLBACK (legacy)` markers, threshold default 2/week.

- **Bidirectional contract (v3.5.1)** — synthesis surfaces are bidirectional: read-render on open is useless if the write side (what populates the state files the render reads) is unbounded. v3.5.0 shipped only the read face; v3.5.1 names both. SessionStart briefing's write surface (the carry-forward block in `.remember/remember.md`) is now capped at ≤500 chars / ≤8 lines (links-not-prose for rich content). Read-side budget enforcement landed as belt-and-suspenders. New PostToolUse hook instruments first-tool-call latency for mechanical regression detection — the controller no longer relies on noticing slowness; the distribution is read at P8.

- **Luma promoted translator → consultant (v3.4.3)** — Luma's first organic post-promotion invocation immediately produced a load-bearing axis-reframe (outside-lens-vs-inside-lens on a retention pressure-test). Promotion formalized: she now delivers a weighted recommendation with evidence at the end of her frames, not just option enumeration. Toolset extended with read access on the root governance surface so she can verify artifacts she frames against. Doctrine: **Root never simplifies for the controller — that's Luma's territory.** The four-role split (Root = doer; Luma = consultant; Teacher = proposal author; controller = decider) holds.

- **v3.5.2 sprint consolidation (2026-04-25)** — Protocol 8 gains step 6.7 (Hook fire-rate audit): a script consumes `.claude/hook-fires.jsonl` v1.0 schema, flags `🔴 SILENT-CANDIDATE` on <80% fire-rate + `🔴 ABSENT-FROM-FIRELOG` for hooks missing from registered inventory. Structural fix for the silent-governance-hook-regressions family caught at instance #3 in 8 days. Plus a checkpoint-bar Tier 2 corrective+formative PostToolUse hook (Frame 3 / Option B) — agent-discipline plateaus around 50% miss rate under multi-edit cadence; hook-side correction takes over. Plus Luma pre-dispatch discipline (2-line handoff: Category + Options before Root-suggests dispatches), axis-reframe sub-categories named for session-log machine-tagging (3 axes: demonstrate-vs-guard, completeness-vs-shape, methodology-vs-character), and a Codex P3B mandate on hook-lifecycle code. Codex P3B caught 7 real defects across the 24h hook-lifecycle ship cluster — strongest evidence yet for the rule's signal quality.

## What's new in v3.4 (cumulative through v3.4.2)

- **Teacher (v3.4.0)** — 8th fam member, the learning-layer agent. Reads the governance catchment (insights-buffer + retro-candidates + LEARNINGS deltas), detects recurring patterns across the week, authors structured proposals into `.claude/teacher-proposals.md`. P8-primary invocation (step 6.5 in the weekly retro); Rosie-secondary manual between P8s. Propose-only on governance surfaces — silent-override is the failure mode. Full contract: [`agents/teacher/teacher.md`](agents/teacher/teacher.md).
- **P9 — autonomous iteration loop (v3.4.0)** added to the protocol quick reference. Partially formalized as Teacher; auto-promotion conditions still open (when Teacher-authored proposals can bypass the Rosie gate).
- **Behind the scenes, also v3.4.0** — a session-archive retrieval primitive (ripgrep-only, one-shot with follow-up refinement), a ratified RoundN round-based nudge hook spec (v1 implementation queued), and a landing-zone design for a pattern-trigger hook (v1 gated on Teacher + RoundN + 2–3 weeks of observation). The harness keeps moving.
- **Governance files come in three flavors (v3.4.1)** — activity (CHANGELOG — everything meaningful that happened), meta (LEARNINGS + retro-candidates + insights-buffer — reflection on activity), and **reference layer** (curated-evidence files with stable look-up answers to specific queries). The reference layer was the gap: Rozzzsie had activity and meta from day one, no dedicated reference layer. Named this patch; operationalized in v3.4.2. Landed alongside an **absorb-not-import doctrine** — learn from neighboring architectures, adopt in the OS's own way, don't import the scaffold wholesale.
- **Reference layer operationalized (v3.4.2)** — first canonical reference-layer file shipped after Rosie flagged she'd been re-asking the same question across sessions getting inconsistent answers each time. New diagnostic rule: *a question re-asked across 2+ sessions is signal that the answer belongs in a reference-layer file, not re-derived each session — author the file, don't answer it more carefully this session.* Cross-pollination convention established (reference files get pointer rows in workspace CLAUDE.md startup loadouts so nobody has to discover them). Teacher gets a new catchment stream at next P8 — re-asked-question audit alongside LEARNINGS deltas + retro-candidates + insights-buffer.

## What's in this repo

- [`dashboard/`](dashboard/) — **the OS observability layer**, sprint-1 v1 shipped. Renders the most recent P8 retro from its YAML sidecar into a static HTML dashboard ([live at `rozzzsie.github.io/Rozzzsie/dashboard/`](https://rozzzsie.github.io/Rozzzsie/dashboard/)). Frame 1 + Frame 3 stacked per Luma's 2026-04-25 evening consult: subtree-in-Rozzzsie-public for consistency-with-spine, scope-honest single-retro v1 over multi-retro-faked-from-n=1 v1.
- [`retros/`](retros/) — **sanitized retro sidecars** the dashboard renders from. One file per P8 (filename pattern: `YYYY-MM-DD-pN.yaml`), 11 fields × N findings. Stakeholder names dropped, workspace paths genericized, narrative `.md` retros stay private; sidecar is the public-grain summary. Schema v1.0 (canonical-symlink pattern), stability review at 2026-05-15 once 3+ retros accumulate.
- [`agents/`](agents/) — **fam character briefs.** One subfolder per agent (Root / Luma / Teacher / Breakline / Codex / Brindle / Deputies). Each agent's `.md` is its system prompt.
- [`hooks/`](hooks/) — **the enforcement layer** (the hooks the protocols reference). Stop-gate, post-edit reminder, session-start digest, insights-capture, plus the v3.5.x synthesis-surface render hooks.
- [`workspaces/`](workspaces/) — **four sanitized work surfaces**, anonymized for public sharing.
- [`_config/`](_config/) — the protocols pointer + output-checklist (the quality gate every deliverable runs through).
- [`CONTEXT.md`](CONTEXT.md) — sanitized public snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private; this is the shape, not the live content.
- [`LEARNINGS.md`](LEARNINGS.md) / [`CHANGELOG.md`](CHANGELOG.md) — curated slices: most-valuable-five cross-workspace insights + most-valuable-five architectural shifts. Earlier entries archived in private; what survives here is what generalizes broadest.
