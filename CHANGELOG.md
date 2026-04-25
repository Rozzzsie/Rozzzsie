# CHANGELOG — Rozzzsie

Architectural shifts, not individual fixes. The most valuable five.

---

## Dashboard v1.1 — observability layer polish release (2026-04-25)

The OS observing itself — first public-grain artifact that lets a reader see governance evolution without reading the protocol doc, the retro narratives, or the proposals file. Live at [`rozzzsie.github.io/Rozzzsie/dashboard/`](https://rozzzsie.github.io/Rozzzsie/dashboard/), tagged `dashboard-v1.1`. Frame 1 + Frame 3 stacked per Luma's 2026-04-25 evening consult — subtree-in-Rozzzsie-public for consistency-with-spine + scope-honest single-retro v1 over multi-retro-faked-from-n=1.

v1.0 shipped earlier the same evening (commit `a7e0305`): six sections rendered mechanically from the canonical sidecar — hero with EDD-arxiv anchor, decision-velocity tiles, discipline + dispatch bands, proposal-backlog cohort flow + latency observations, 15-finding detail table with color-coded status pills, scope-honest footer. v1.1 is a polish release: copy tightened on six discipline+latency labels for director-skim grain; meta-finding callout upgraded with architectural ◆ icon + 6px accent rail + bolder typography (the "architect gold" insight at the bottom now reads as the eye-magnet it should always have been); scope-honest footer layout fixed (was bottom-left only because of an unbalanced max-width; now centered narrow block); Luma-tally-bar label column widened from 13ch to 28ch so longer category names like *silent-assumption-catch* and *polish-layer-text-diagnosis* render fully instead of bleeding past their column. README dashboard pointer added so the URL is visible above the agent fold.

The arxiv anchor — [EDD 2024](https://arxiv.org/abs/2411.13768), *"evaluation as continuous governing function, not terminal checkpoint"* — is the thesis line the dashboard plants. Industry harness dashboards (LangSmith, Langfuse, DashChat) surface telemetry; this dashboard surfaces governance evolution. Same shape, different semantics. Sprint-2 unlocks multi-retro trend rendering once 3+ sidecars accumulate (gated on the schema v1.0 stability review at 2026-05-15).

Render contract: `dashboard/render.py` reads the most recent sidecar from `retros/` and emits `dashboard/index.html` on push. The renderer is stdlib + optional PyYAML, with a minimal YAML subset parser fallback so it runs anywhere `python3` runs. `DASHBOARD_VERSION = "1.1"` in the renderer is the canonical version surface; bumped on every change that lands a visible-grain difference for readers.

---

## Protocols v3.5.2 — sprint consolidation (2026-04-25)

A weekend architecture sprint consolidated into one minor-patch bump. Three structural additions land together because they're the same shape of governance failure mode — silent regressions and discipline plateaus where agent-side enforcement degrades under load.

**Protocol 8 step 6.7 — Hook fire-rate audit.** The silent-governance-hook-regressions family hit n=3 in 8 days; an audit script now consumes a `.claude/hook-fires.jsonl` v1.0 schema and flags `🔴 SILENT-CANDIDATE` on <80% fire-rate plus `🔴 ABSENT-FROM-FIRELOG` for hooks present in the registered inventory but missing from the firelog. Cross-checks against any cwd-guard, JSON-envelope-format, or settings.json registration changes shipped in the same window. The earlier failure mode was that hooks could regress silently for months without anyone noticing — the cwd-guard mismatch in the SessionStart hook was running quietly broken from one of the controller's two normal cwd shapes for an undetermined window before a debugging session surfaced it.

**Checkpoint-bar Tier 2 corrective+formative hook.** Agent-discipline on the checkpoint bar plateaus at ~50% miss rate under multi-edit cadence — a v3.2-CB1 hard-gate at session close had been the prior pattern, but per-turn enforcement was missing. The new PostToolUse hook reads the transcript JSONL, classifies whether the prior completed turn was substantive, writes a firelog record, and emits corrective `additionalContext` when a substantive turn missed the bar. Frame 3 (corrective + formative) per Luma consult; Option B per the design's per-turn pre-block axis. Codex `/codex:adversarial-review` caught two real defects on first dogfood-from-itself: a mid-body bar bypass via unanchored regex (closed via footer-anchored pattern) and silent-exit on transcript I/O failures (closed via a fifth `error` action state plus a TranscriptReadError exception on three silent-exit paths).

**Luma pre-dispatch discipline + axis-reframe sub-categories + Codex P3B hook-lifecycle.** Three rules from the same retro that target dispatch budgeting. Before Root-suggests Luma dispatches, Root writes a 2-line handoff (Category + Options A/B/C, each a distinct decision axis); if either line cannot be written, no dispatch. Text-polish on already-shape-selected artifacts and single-section spec double-checks are excluded from Luma-territory. Three named axis-reframe sub-categories — *demonstrate-vs-guard*, *completeness-vs-shape*, *methodology-vs-character* — were observed firing across the 2026-04-16 fam-debut authoring cluster and now carry session-log machine tags. Codex P3B is mandatory before any commit touching hook-lifecycle code (SessionStart / Stop / PostToolUse / PreCompact); precedent is the months-long silent cwd-guard regression and the 7 real defects Codex P3B caught across the 24h hook-lifecycle ship cluster.

Bumped on top of the v3.5.1 bidirectional contract; references shipped through the symlink-canonical pattern (no live-reference rewrites).

---

## Protocols v3.5.1 — Synthesis-Surface bidirectional contract (2026-04-23 evening)

v3.5.0 shipped a synthesis-surface pre-render pattern with a clean-state baseline of 37s on the SessionStart briefing — a 65% reduction from the 105s prior. The first post-ship real session regressed to 3m 9s on the same surface. Investigation: the hook itself ran in 73ms; the regression lived in the synthesis the hook couldn't displace, amplified by an unbounded carry-forward block the prior session had stuffed into `.remember/remember.md`. v3.5.0 had specified only the read side of the pattern; the write side was silent.

v3.5.1 names both faces. **Read face** = hook renders state files into a card with `<JUDGMENT:>` slots. **Write face** = whatever the prior session populated the state files with. SessionStart briefing's write surface is the first `##` section of `.remember/remember.md`, capped at ≤500 chars / ≤8 lines (links-not-prose for rich content — the briefing points at authoritative files like `.claude/teacher-proposals.md` or `_retro/YYYY-MM-DD-retro.md`, opened on demand). Read-side enforcement: a library default truncates with an explicit `[...write-surface budget enforced — see source for full]` marker. Write-side enforcement: a new checklist item in Protocol 7 names the budget at session close.

Observability: a new PostToolUse hook instruments `session-start → first-tool-call` latency to a log file. P8 retro now reads the past 7-day distribution (median + p95 + max) instead of relying on the controller noticing slowness. Threshold for retro-candidate flag: any session > 120s. The single-number-baseline pattern that produced the 2026-04-23 regression is replaced by distribution-reading.

A new LEARNINGS family captured: **ship-validation gaps** — clean-state baselines don't hold under real session load. For new architectural primitives whose advertised value is a measurable metric, baseline numbers must be measured across at least three named edge-case scenarios before they enter protocol-doc language as load-bearing claims. The enumeration of edge cases becomes part of the primitive's acceptance criteria.

---

## Protocols v3.5.0 — Synthesis-Surface Pre-Render Pattern v1 (2026-04-23 evening)

A new architectural primitive: hook-side render scripts pre-compute mechanical content for synthesis-heavy surfaces, agent fills `<JUDGMENT: ___>` slots inline. Reference implementation shipped on the SessionStart briefing — startup thinking time 105s → 37s on clean state, a 65% reduction. Pattern fit covers five surfaces: SessionStart briefing (#1, shipped), P8 weekly retro generation (#2, queued), P7 session-close summary (#3, queued), CONTEXT updates (#4, future), compaction recovery briefing (#5, future). Out of scope: Q&A responses, code edits, brainstorming dialogue, sub-agent dispatch.

**Invariant 9 — silent-fallback observability.** Every synthesis surface must add a P8 retro audit step counting `<SURFACE> — FALLBACK (legacy)` markers in `.claude/session-log.md` over the past 7 days. Threshold for retro-candidate flag: configurable per surface, default 2 fallbacks/week. The library exposes a `count_fallback_markers()` primitive callers can compose with.

**Hook output format requirement.** SessionStart hooks (and future event-types using the pattern) MUST emit `hookSpecificOutput` JSON, not plain text. Plain text is silently dropped despite exit 0; the failure mode is invisible because the hook reports success. A neighboring hook in the cosmetic layer happens to use plain text successfully — that's an undocumented legacy fallback path, not a contract.

**Cwd-guard convention.** Governance hooks with cwd guards must accept both the inner workspace cwd and the parent repo cwd as valid toplevels — the pattern is canonical: detect parent, remap to inner, then `cd`. The earlier overly-strict cwd guard caused a months-long silent governance regression discovered while debugging the briefing — the briefing bug was the canary; the cwd-guard mismatch had been silently breaking the protocol-digest backstop in the controller's normal cwd workflow for an undetermined window.

---

## Protocols v3.4.3 — Luma translator → consultant promotion (2026-04-23 morning)

Luma was originally shaped as a translator rail — convert Root's dense output into decision-shaped frames, then exit. Practice over the prior 9 days produced a different pattern: her highest-value invocations were not framings but **reframings** — surfacing that the controller's option set sat on the wrong axis. The fam-debut authoring cluster (2026-04-16) produced three load-bearing axis-reframes — *demonstrate-vs-guard*, *completeness-vs-shape*, *methodology-vs-character* — each of which would have produced "better wrong answers" if Luma had only ranked options inside the controller's original axis.

Promotion formalized: Luma now delivers a weighted recommendation with evidence at the end of her frames, ending in *"But you decide."* Rule 9 (no original-naming except where load-bearing) was relaxed for axis-name coining when the controller's option set genuinely sat on an unnamed axis; the soft norm is to coin sparingly and re-use existing axis names when they fit. Toolset extended `[] → [Read, Grep, Glob]` on root .md governance surfaces so Luma can verify the artifacts she frames against — the prior zero-tools shape was forcing Root to pre-stuff every relevant detail into the handoff, which sometimes flattened evidence the controller would have wanted Luma to see directly.

Doctrine update — the four-role split (was three-role): **Root = doer (completeness + correctness, full-fidelity output); Luma = consultant (distillation + decision-shape + weighted recommendation with evidence, pre-P4); Teacher = proposal author (pattern detection + structured proposal authoring on governance catchment, post-P8); the controller = decider (picks, modifies, or walks away).** Root never simplifies for the controller anymore; that's Luma's territory. Root never authors rule-change proposals from inside a working session; that's Teacher's territory. Teacher never frames decisions; if Teacher's proposal needs framing, it's handed to Luma. Luma never authors proposals; if Luma identifies a pattern worth proposing, normal flow is the controller logs it to retro-candidates and Teacher picks it up at next invocation. The rails don't overlap; each agent's function is load-bearing against exactly one failure mode.

---

## Protocols v3.4 — Teacher learning layer (2026-04-20)

The governance OS grew an 8th role. Teacher is the pattern detector + proposal author on the governance catchment — insights-buffer, retro-candidates, and LEARNINGS deltas, all three streams already curated upstream. Invoked at the weekly P8 retro as step 6.5, and manually between P8s when the controller asks. Authors 1–3 structured proposals into `.claude/teacher-proposals.md` per invocation; the controller decides accept / modify / reject / defer; Root executes approved proposals at P8.

Propose-only on all governance surfaces (CLAUDE.md, LEARNINGS.md, protocols, output-checklist, workspace state files, hooks, agent files, designs, plans); strict-validated direct-write on a narrow pre-approved list (skill creation, monthly insights-archive rotation, `_input/archive/` moves at distillation time) with degrade-to-propose fallback. Silent-override is the explicit failure mode — every Teacher write surfaces in proposals AND session-log AND the next P8 retro. Memory = the proposals file itself; no separate memory layer.

P9 (autonomous iteration loop) joins the protocol quick reference — partially formalized as Teacher; auto-promotion conditions for Teacher-authored proposals bypassing the controller gate remain open. OS version bumps to v3.4.0; README and CLAUDE.md name Teacher in the Strategic Layer and surface the protocol count as twelve.

Subsequent v3.4.1 / v3.4.2 patches named the three-flavor governance file taxonomy (activity / meta / reference) and operationalized the reference layer after the controller flagged she'd been re-asking the same question across sessions getting inconsistent answers each time. The diagnostic rule: *a question re-asked across 2+ sessions is signal that the answer belongs in a reference-layer file, not re-derived each session — author the file, don't answer it more carefully this session.*

---

*Earlier architectural shifts (v3.3 roles map + Luma translator rail; v3.3.1 scope-symmetry family retired; symlink-canonical pattern; stop-gate Check 3 + 8 patches; landing surface applied demonstrate-vs-guard) archived in private. The five above are the most valuable cumulative shifts at the public-snapshot grain.*
