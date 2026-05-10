# Rozzzsie

A living snapshot of the agent fam and the governance OS they run on.

Nine agents. Thirteen protocols (P1–P10 + sub-protocols P1B/P2B/P3B for Codex validation) and a checkpoint bar, mechanically enforced by hooks that fail session-close when any of them slips. Adversarial audits run against the governance doc itself — the fam writes the rules, Breakline tries to break them, the fam decides what to fix.

**Start here:** [`agents/breakline/breakline.md`](agents/breakline/breakline.md) — the adversarial auditor. The clearest single page on how the fam operates.

**Live dashboard (v1.4):** [**rozzzsie.github.io/Rozzzsie/dashboard/**](https://rozzzsie.github.io/Rozzzsie/dashboard/) — the OS observing itself. Decision velocity, discipline metrics, Luma tally by category, proposal backlog cohort flow, latency observations, full findings detail with status pills. Renders mechanically from the most recent P10 retro sidecar at [`retros/`](retros/) on every push to `main`. Sprint-1 v1.4: single-retro snapshot rendered against `retros/2026-05-03-p4.yaml` (the v3.9.x ship-cycle retro) with Frame 2 fam-dispatch widget (sub-band split for dispatch + reactions axes) + measurement-surface anchor + Luma reframe-axis tally relocated to deep-dive panel. Sprint-2 unlocks multi-retro trend rendering once 3+ sidecars accumulate. Release notes in [`dashboard/README.md`](dashboard/README.md); tagged in git as `dashboard-v1.4`. The arxiv anchor is [EDD 2024](https://arxiv.org/abs/2411.13768) — *evaluation as continuous governing function, not terminal checkpoint.*

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

**Sumi** — read-only governance grader. New in v3.10 as the 5th P3 enforcement rail (joins pre-output validation, output-checklist gates, Codex P3B review, and Breakline adversarial audit). Two job modes: per-output grading (Sumi reads a deputy's draft against the rubric matched to its output_type and emits a tier-graded verdict with structured suggested revisions) and drift-scan (Sumi walks every active rubric in `_config/sumi-rubrics.yaml` and verifies each anchor still resolves in its declared source file). Tools strictly `[Read, Grep]`. Indirect channel locked: Sumi → Root → (optionally) Teacher — never authors proposals directly, never edits source files. Separate-model judge so the grade lands as a second opinion, not a self-pat.

**Deputies** — the sub-agent pool. Zero-context by design; each one gets a task brief and nothing more.

**Teacher** — learning layer. New in v3.4; reads the governance catchment (insights-buffer + retro-candidates + LEARNINGS deltas) and authors structured proposals for the controller to review at the weekly P10 retro. Never writes rules directly — silent-override is the failure mode.

## About Brindle

Brindle is the only fam member who ships as her own standalone product. The other seven live here as Claude Code subagents — each one's `.md` file IS the implementation, loaded by the Task tool at invocation time. Brindle's runtime is separate Python code, MIT-licensed, clonable: [`brindle-terminal-bunny`](https://github.com/Rozzzsie/brindle-terminal-bunny).

Her persona card still lives at [`agents/brindle/brindle.md`](agents/brindle/brindle.md) — that hasn't moved. The asymmetry is architectural, not accidental. Seven agents whose contracts live in this repo. One agent who graduated into a standalone product. The two-repo shape is intentional.

## The OS

Rozzzsie runs a governance OS (v3.10.4) with four layers the fam operates under:

- **Protocols** (P1–P10, plus sub-protocols P1B/P2B/P3B for Codex validation) — intent confirmation, loop detection, quality gate, state update, focus-chain discipline, learning capture, cross-pollination, autonomous iteration loop, session close, weekly retrospective.
- **Hooks** — `PostToolUse`, `Stop`, `SessionStart`. Reminders fire automatically; the stop-gate blocks session-close on protocol failures.
- **Checkpoint bar** — every tool-using response carries `[checkpoint: P3 — ... | P4 — ... | P6 — ...]`. Verifiable friction.
- **Session lifecycle** — startup briefing, state updates after every meaningful increment, p3-trace at close, CONTEXT + CHANGELOG current before commit.

## Patterns and where to read them

The 10 governance-architecture patterns this OS implements at company-scale design intent + single-operator run-time. Each row maps a named pattern to its load-bearing artifact in this repo. Drafting-as-test was applied during compilation: any pattern whose name didn't read as field vocabulary, or whose code-pointer didn't resolve to a real file, demoted out of this Tier A table.

| # | Pattern | One-line definition | Where to read it |
|---|---------|---------------------|------------------|
| 1 | **Tier 1 / 2 / 3 enforcement classification** | Three-tier scale separating mechanically-enforced rules (T1, fail loud), corrective+formative hooks (T2), and pure conventions (T3); rule severity is declared, not implicit. | `_config/agent-protocols.md` (header) + [`hooks/`](hooks/) (stop-gate, checkpoint-bar Tier 2) |
| 2 | **Versioned governance protocols + symlink-canonical** | Canonical filename carries the version (`agent-protocols-3.10.4.md`); a stable symlink (`agent-protocols.md`) retargets on bumps so references never break. | [`_config/`](_config/) (canonical + symlink) |
| 3 | **Multi-agent role separation (4-role split)** | Doer / consultant / proposal-author / decider — each rail load-bearing against exactly one failure mode; Root never simplifies for the controller (that's Luma's territory). | [`agents/`](agents/) (Root, Luma, Teacher, Breakline, Codex, Sumi, Brindle, Deputies) |
| 4 | **Three-flavor governance file taxonomy** | Activity (CHANGELOG — what happened) / meta (LEARNINGS + retros — reflection on activity) / reference (curated stable look-ups). Re-asked questions across 2+ sessions promote into reference. | [`CHANGELOG.md`](CHANGELOG.md) + [`LEARNINGS.md`](LEARNINGS.md) + [`retros/`](retros/) |
| 5 | **Hooks-as-enforcement** | Mechanical enforcement at runtime via `PostToolUse` / `Stop` / `SessionStart`; rules don't rely on agent self-discipline. Stop-gate blocks session-close on protocol failures. | [`hooks/`](hooks/) |
| 6 | **Synthesis-Surface Pre-Render Pattern** | Hook-side render scripts pre-compute mechanical content for synthesis-heavy surfaces; agent fills `<JUDGMENT: ___>` slots inline. Bidirectional contract: read-render + write-budget. | [`hooks/`](hooks/) (render scripts) + `.remember/remember.md` (write-cap) |
| 7 | **Closed-loop learning (P6 → P7 → P10 + Teacher)** | Insights captured during work (P6) → cross-pollinated to LEARNINGS (P7) → triaged at the weekly retro (P10), with Teacher authoring structured rule-change proposals from the catchment. | [`agents/teacher/`](agents/teacher/) + [`retros/`](retros/) + [`LEARNINGS.md`](LEARNINGS.md) |
| 8 | **Adversarial audit as routine governance** | Breakline runs audits against the governance doc itself on a cadence — not a one-time review. Findings flow into the retro as `adversarial-audit` source-catchment. | [`agents/breakline/`](agents/breakline/) |
| 9 | **Sanitization pipeline (private narrative → public sidecar)** | Narrative `.md` stays canonical with full operator context; public `.yaml` sidecar drops stakeholder names, genericizes workspace paths, redacts session-traceable metrics. Narrative wins on disagreement. | [`retros/README.md`](retros/README.md) (sanitization rules) |
| 10 | **Evidence-required rule-change proposal mechanism** | Teacher writes proposals into `.claude/teacher-proposals.md` with evidence_count + source_catchment fields; controller-gated for accept/defer. Proposals never silent-override. | [`agents/teacher/`](agents/teacher/) |

## What's new in v3.10 (cumulative through v3.10.4)

- **Sumi v1.0/v1.1/v1.2/v1.3 trilogy (5th P3 enforcement layer; v3.10–v3.10.4)** — Sumi joins the fam as the 5th rail in the four-role split's P3 layer: a read-only governance grader for subagent output, paste-text, and design specs. Tools stay `[Read, Grep]`; indirect channel locked Sumi → Root → (optionally) Teacher; never authors Teacher proposals or edits source files. v1.0 morning shipped subagent-output-relay rubrics + Phase D 4-failure descope; v1.1 night added design-spec output_type + cross-check resolution; v1.2 night added external-bound-paste-text + stakeholders.council activation + additive-overlay composition; v1.3 mid-day next added drift-scan invocation mode that walks every active rubric in `_config/sumi-rubrics.yaml` and verifies each anchor still resolves in its source file (new `drift_findings` verdict shape with `drift_class` enum — anchor_not_found / section_not_found / source_file_unreadable). Three versions in 24h, governance ship per Sumi-class canonical template (3-commit doctrine sub-ship → build sub-ship → governance ship — eligible canonical-spec template at n=4).

- **Checkpoint-bar PostToolUse format-validator + substantive_v2 (v3.10.3)** — checkpoint-bar enforcement extended along two axes. NEW `LOOSE_BAR_PATTERN` (footer-anchored permissive regex) detects bar-attempted-but-malformed turns (typo'd em-dash, comma-instead-of-pipe, Pn-mismatch, missing field); NEW `block-corrective-format` action emits format-specific corrective naming the actual mistake instead of the misleading generic "missing bar." NEW `substantive_v2` mutation-tool-aware classification when `tool_names` provided: `(mutation_tool_count ≥ 1) OR (tool_use_count ≥ 3) OR (prose > 300)`. Closes Teacher proposal "checkpoint-bar Tier 2 PostToolUse extension" (Frame 3 corrective+formative + Option B PostToolUse pre-block per Luma framing).

- **MUTATION_TOOLS Conservative extension + Path A unified gate (v3.10.4)** — MUTATION_TOOLS frozenset extended `{Edit, Write, Bash}` → `{Edit, Write, MultiEdit, NotebookEdit, Bash}` (filesystem-identical mutation surface). mcp__*-write tools deliberately deferred (SDK MCP tool surface still evolving — Aggressive direction pre-staged as separate Teacher proposal). Path A unified gate combined the MUTATION_TOOLS Conservative ship with Sumi v1.3 drift-scan in one v3.10.4 patch. Codex P3B adversarial review caught 3 ship-blockers all fixed pre-ship including hookSpecificOutput envelope cross-find: drift-scan hook used wrong envelope shape; same bug pre-existed in sibling sumi-post-task.sh since v3.10 ship and was fixed as parity cross-find — adversarial review of NEW hooks should sweep sibling hooks for the same pattern when implementation was modeled on a sibling.

- **MD-vs-HTML deliverable format convention (Phase 1 doctrine ship)** — Luma F3 edit-locus reframe: artifacts split by binary "does this get re-edited after creation" predicate. Reading bundles (zero post-create edits, often shared) → HTML in `_artifacts/`; source-of-truth artifacts (continuous edits, VC, grep-targeted, agent-read) → MD; hybrid artifacts → MD canonical edited + HTML render regenerated on meaningful change. Architecture is the output-side mirror of v3.5 synthesis-surface pre-render pattern (input-side handles agent perception; HTML render handles output-side controller perception). Tooling cadence: ad-hoc Python+pandoc for n=1 instances; promote to scripted `_config/scripts/md-bundle-to-html.py` at n=2.

- **Long-lived branch merge discipline (output-checklist §20)** — for sprint branches > 1 day touching state files (CHANGELOG / CONTEXT / LEARNINGS) across multiple phase-close commits: rebase against main pre-merge to surface conflicts incrementally, not all at once at merge time. State-files-FIRST close-out doctrine remains load-bearing — don't defer state-file writes to AFTER merge. Watch n=2 recurrence on next worktree-based sprint for structural-fix consideration (PreToolUse hook detecting long-lived state-file divergence).

- **Novel doctrine-tag: "axis-coherent, evidence-weight-rejected"** — new precedent for bundled-framing gates where the controller accepts Luma's axis but declines a surface; distinct from axis-rejected + locus-disputed. Surfaced during Phase 1 doctrine ship gate dispositions; resolves apparent contradictions when Luma's frame is structurally sound but the evidence weight on a specific surface is below the controller's bar.

## What's new in v3.9 (cumulative through v3.9.3)

- **P8 firmware formalization (v3.9.0 → v3.9.1)** — autonomous iteration loop graduates from doctrine-only to formal firmware: YAML-grammar DSL for proposal records, Teacher-awareness layer for catchment routing, ledger schema for proposal lifecycle (`pending` → `approved` → `executed` / `deferred`). Auto-promote gate ships OFF in v3.9.0 (controller-supervised observation window); promoted to ON in v3.9.1 after 7 days clean.
- **Pn-token cascade renumber (v3.9.3)** — clean permutation across 6 protocols: old P5/P6/P7 (state update / focus chain / learning capture) cascade up to absorb Focus-chain discipline as the new P5; P8 (autonomous loop) renumbers to P8; P9 (session close) → P9; P10 (weekly retro) → P10. The cascade closes a Reading A doctrine gap where Pn-tokens were being read as positional indices instead of stable identifiers — symlink-canonical pattern doctrine extended to protocol numbering.
- **AUTO_PROMOTE_ENABLED env-var decouple (v3.9.3)** — promotion-gate env var renamed from `P9_AUTO_PROMOTE_ENABLED` to `AUTO_PROMOTE_ENABLED` so the Teacher proposal-promotion mechanism is protocol-numbering-independent. Future Pn-cascades won't drag env-var renames behind them.
- **26-finding Silent-Failure-Hunter audit closure (v3.9.1)** — Breakline + SFH adversarial pass against the v3.9.0 surface produced 26 findings (7 CRITICAL + 8 HIGH triaged in Phase 1; 11 deferred to Phases 2-4). Critical fixes: stop-gate firing bug (rate-limit + unpushed-commit false-positive interaction), pipefail bug in `subagent-nudge.sh` (silent suppression of subprocess failures). TDD-fixed; audit-test substring-tightening pattern codified for the symmetric assertIn / assertNotIn family.

## What's new in v3.8 (cumulative through v3.8.2)

- **Bar-mandatory turns + Tier 2 corrective hook (v3.8.0)** — checkpoint-bar policy formalized into a turn-shape rule: every substantive tool-using turn must end with the canonical bar. PostToolUse Tier 2 hook lands corrective+formative messages when the bar is missed; agent-side discipline plateaued around 50% miss-rate under multi-edit cadence, hook-side correction takes over. Real-traffic firelog at `.claude/hook-fires.jsonl` populates per-turn audit records consumed at P10 step 6.7.
- **SFH integration as systematic-risk-surface mapping (v3.8.0–v3.8.2)** — Silent-Failure-Hunter adversarial review + TDD integration codified as the systematic risk-surface mapping pattern for release cycles. Identity-candidate observation carried forward to next P10 promotion review.

## What's new in v3.7 (cumulative through v3.7.2)

- **P5 Focus-chain discipline (v3.7.0)** — new protocol slot added to the spine: focus-chain state must persist on disk across compaction events so post-compact recovery doesn't lose the active task plan. Reference implementation: `.claude/focus-chain.md` + pre-compact snapshot. Closed a real failure mode where compaction silently dropped the in-flight task list.
- **API context-bloat retry-loop fix (v3.7.0)** — AUTOCOMPACT window raised to 500K to prevent a critical retry-loop bug where context-overflow on tool result triggered immediate retry against the same overflow.

## What's new in v3.6

- **Read-tool size-class thresholds (v3.6.1)** — PDF and large-text reads classified by token-cost band (500 / 2k / 12k thresholds); Read calls above the band require explicit pages parameter or grep-first triage. Landed from a Breakline audit finding; documented in the read-tool reference card.

## What's new in v3.5 (cumulative through v3.5.2)

> **Note on Pn references in v3.5 and v3.4 sections:** these reflect version-time numbering. v3.9.3's cascade renumbered the weekly retro to **P10** and the autonomous iteration loop to **P8** — see "What's new in v3.9" above. Reading A doctrine treats Pn-tokens as stable identifiers across the live OS; historical sections preserve their original numbering for accuracy of the changelog.

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

- [`dashboard/`](dashboard/) — **the OS observability layer**, currently at **v1.4** ([live at `rozzzsie.github.io/Rozzzsie/dashboard/`](https://rozzzsie.github.io/Rozzzsie/dashboard/), tagged `dashboard-v1.4`). Renders the most recent P10 retro from its YAML sidecar into a static HTML dashboard. Frame 1 + Frame 3 stacked per Luma's 2026-04-25 evening consult (subtree-in-Rozzzsie-public for consistency-with-spine, scope-honest single-retro v1); v1.2 layered Luma's second consult (layer-mismatch reframe); v1.3 re-renders against the v3.9.x ship-cycle sidecar with v3.9.3 Pn-token cascade + graceful-suppression for redacted (null) discipline + latency fields; v1.4 adds Frame 2 fam-dispatch widget (sub-band split for dispatch + reactions axes) + measurement-surface anchor + Luma reframe-axis tally relocated to deep-dive panel. Full release notes in [`dashboard/README.md`](dashboard/README.md).
- [`retros/`](retros/) — **sanitized retro sidecars** the dashboard renders from. One file per P10 (filename pattern: `YYYY-MM-DD-pN.yaml`), 11 fields × N findings. Stakeholder names dropped, workspace paths genericized, narrative `.md` retros stay private; sidecar is the public-grain summary. Schema v1.0 (canonical-symlink pattern), stability review at 2026-05-15 once 3+ retros accumulate.
- [`agents/`](agents/) — **fam character briefs.** One subfolder per agent (Root / Luma / Teacher / Breakline / Codex / Brindle / Deputies). Each agent's `.md` is its system prompt.
- [`hooks/`](hooks/) — **the enforcement layer** (the hooks the protocols reference). Stop-gate, post-edit reminder, session-start digest, insights-capture, plus the v3.5.x synthesis-surface render hooks.
- [`workspaces/`](workspaces/) — **four sanitized work surfaces**, anonymized for public sharing.
- [`_config/`](_config/) — the protocols pointer + output-checklist (the quality gate every deliverable runs through).
- [`CONTEXT.md`](CONTEXT.md) — sanitized public snapshot of the cross-workspace governance state. The full live `CONTEXT.md` is private; this is the shape, not the live content.
- [`LEARNINGS.md`](LEARNINGS.md) / [`CHANGELOG.md`](CHANGELOG.md) — curated slices: most-valuable-five cross-workspace insights + most-valuable-five architectural shifts. Earlier entries archived in private; what survives here is what generalizes broadest.
