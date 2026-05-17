# Dashboard / Observability Layer

**Current release: v2.1** (2026-05-17) · Tag: `dashboard-v2.1` · [Source](https://github.com/Rozzzsie/Rozzzsie/tree/main/dashboard)

**Live: [rozzzsie.github.io/Rozzzsie/dashboard/](https://rozzzsie.github.io/Rozzzsie/dashboard/)** — GitHub Pages serves the rendered `index.html` on every push to `main`. HTTPS enforced. Open `dashboard/index.html` directly in a browser to read locally — the render is fully self-contained (CSS in `assets/`, no JS).

## What this is

The dashboard is the OS observability surface — a render of the governance state into a shape leadership and external readers can browse without diving into the protocol doc, the retro narratives, or the proposals file.

Industry harness dashboards (LangSmith, Langfuse, DashChat) surface telemetry — tokens, latency, error rates, eval scores. Same *shape* (quantitative metrics on a temporal axis), different *semantics*. Rozzzsie's dashboard surfaces **governance evolution**: proposal lifecycle from authoring to executed, hook fire-rate health, checkpoint-bar discipline trends, Luma tally by category, decision velocity per retro, family-pattern detection across weeks. The arxiv anchor is *evaluation as continuous governing function, not terminal checkpoint* ([EDD 2024](https://arxiv.org/abs/2411.13768)) — that principle is what distinguishes this layer from a Langfuse/LangSmith clone.

**Why scope-honest matters.** A polished-looking dashboard with one data point is the kind of thing a sharp reviewer (CTO, interviewer, peer architect) catches and discounts. Sprint-1 is honest: this is what one retro looks like, here's the rendering contract, the next retro's sidecar will auto-render here when it lands. That's the L5-evidence move — *the OS observes itself* — without faking trends from n=1. Sprint-2 unlocks multi-retro trend rendering once 3+ sidecars accumulate (gated on schema v1.0 stability review at 2026-05-15).

## Release notes

### v2.1 — 2026-05-17 (re-render against `2026-05-17-p6.yaml` + n=4 sidecar trend extension + P10-ritual final-step codification)

- **Re-render against the new sidecar.** Source data updated from `retros/2026-05-10-p5.yaml` → `retros/2026-05-17-p6.yaml` (window 2026-05-10 → 2026-05-17, 13 findings × 11 fields, 7d-on-the-nose cadence per SessionStart OVERDUE banner). Default sidecar arg in `render.py` retargeted to match.
- **Trend lines auto-extend to n=4 sidecars.** Sprint-2's `load_all_sidecars()` aggregator picks up `2026-05-17-p6.yaml` automatically — no renderer change. Each of the 3 metric cards (checkpoint miss / decision velocity / Teacher invocations) now carries a 4-point inline SVG sparkline + the v2.0 directional annotations re-computed on the new tail. Direction calls: (a) **Checkpoint miss rate** — 29% → 23% → 32% → 35% (↑ regression continues; late-session-fatigue plateau in the retro session itself is a representative within-session instance per the public sidecar's `discipline_metrics` comment); (b) **Decision velocity** — 4 → 9 → 12 → 8 executed findings (↓ deceleration from prior cycle, but the cycle's lighter-ship-trilogy character explains the dip cleanly; carries no plateau signal at n=4); (c) **Teacher invocations** — 1 → 2 → 4 → 1 (↓ from peak; the v3.10.x cycle's 4-Teacher-touch trilogy was the local maximum, this cycle's single P10-dispatch is the steady-state baseline).
- **Findings detail table reshape.** Sprint-1's 15-line findings cluster from the v3.10.x cycle was structured around the Sumi-trilogy ship trio (1.1-1.4) + Phase 1 doctrine ship (1.7-1.9); the v6 cycle's 13 findings are **family-grouped** (Items A-H from the underlying narrative), which surfaces as 11 promote-tier items (1.1-1.10 + 2.1 methodology) + 2 process-level rows (3.1 helper-axis-completeness post-retro fix + 4.1 hybrid-format doctrine watch). This is the first sidecar to carry an item with `recommendation: watch` AND `status: deferred` AND `execution_target_week: null` (row 4.1) — the schema accommodates the three-way "watch + defer + null-target" combination without renderer changes, but worth surfacing as a schema-shape observation for the schema-stability review (v1.0 → v1.1 gated on n≥3 such observations).
- **Final-step codification in P10 ritual.** Today's update is the first ship under the new Protocol 10 § "How to execute" Step 9 ("update the public dashboard") — codified in `_config/agent-protocols.md` v3.10.5 (this cycle's patch ship). The doctrine extension was the second half of today's controller directive; the first half was this re-render. Forward state: every P10 retro from this cycle on emits a sidecar + companion narrative + dashboard re-render as part of the canonical close.
- **Renderer + README OS version bump in footer.** Thin attribution band now reads `Dashboard v2.1 · Schema v1.0 · Rozzzsie OS v3.10.5 · EDD 2024 · Source · About`. No renderer architecture changes this release — v2.0's aggregator + trend chart machinery handle n=4 mechanically.
- **Sidecar count: 4.** The dashboard now treats `retros/` as a 4-cycle collection. Sprint-2's trend grid is meaningful at n=4 (direction calls hold up over 3 tail comparisons); distribution-shape metrics (median + p95 + percentile bands) still require n≥5 per the original Sprint-2 gating note.

### v2.0 — 2026-05-10 (sprint-2 unlocked: multi-retro trend rendering — 3 metric cards × n=3 sidecars)

- **Sprint-2 trend rendering shipped.** New "Governance trend" section below the Findings detail panel renders 3 metric cards across all accumulated sidecars (`2026-04-24-p3.yaml` + `2026-05-03-p4.yaml` + `2026-05-10-p5.yaml`). Each card carries a 3-point inline SVG sparkline + the underlying values inline + a directional annotation (↑ regression / ↑ accelerating / ↑ improving / etc.) comparing the last two cycles + an optional measurement-shape caveat note when cross-cycle apples-to-apples is partial.
- **3 metrics in v2.0 first-pass:** (a) **Checkpoint miss rate** — 29% → 23% → 32% (↑ regression annotation; the v3.10.x cycle's wrap-arc miss plateau showed up); (b) **Decision velocity** — 4 → 9 → 12 executed findings per cycle (↑ accelerating); (c) **Teacher invocations** — 1 → 2 → 4 (↑ accelerating; learning-layer adoption doubling each cycle). The miss-rate card carries an apples-to-apples caveat note inline (p3 measured this-retro-session; p4/p5 measure cycle-window — strict cross-cycle comparison lands at p6 once the window-shape has been stable for 3 cycles).
- **Honest at n=3, scope-honest about it.** This is the "first taste" of trend rendering — 3 datapoints per metric is enough to surface direction (rising / falling / flat) but not enough to call inflection points. The `trend_grid` activates at n≥2 sidecars and degrades gracefully below threshold (placeholder copy if only 1 accumulated). The metric set will expand at n≥5 when distribution-shape (median + p95 + percentile bands) becomes meaningful.
- **No JS, inline SVG, no external dependencies.** Sparklines rendered server-side as inline SVG with auto-scaled Y-axis based on min/max of present values; None values render as gaps (line breaks, no dot). Same no-JS / mobile-responsive / print-friendly contract as v1.x.
- **Renderer architecture extension.** New `load_all_sidecars()` aggregator + `render_trend_chart()` + `_trend_sparkline_svg()` + `_format_trend_value()` + `_trend_annotation()` helpers in `render.py`. `render_dashboard(sc, all_sidecars=...)` signature gained a second arg; defaults to single-sidecar shape if not provided (back-compat for direct invocation patterns).
- **Footer OS version bump.** Stale `Rozzzsie OS v3.9.3` ref in the footer corrected to `v3.10.4` (caught as parity-fix during v2.0 ship — should have landed in v1.5; the missed update is itself an instance of the layer-classification family from earlier today, where reference axes get scoped to the wrong update batch).
- **Sidecar count: 3.** This is the first dashboard release that treats the `retros/` folder as a *collection* rather than a single-input source. Future sidecar drops auto-extend the trend lines without a renderer change.

### v1.5 — 2026-05-10 (re-render against `2026-05-10-p5.yaml` + v3.10.x ship cycle + 9th fam member surface)

- **Re-render against the new sidecar.** Source data updated from `retros/2026-05-03-p4.yaml` → `retros/2026-05-10-p5.yaml` (the P5 sidecar shipped with the v3.10.x ship cycle, window 2026-05-03 → 2026-05-10, 15 findings × 11 fields). Default sidecar arg in `render.py` retargeted to match.
- **First sidecar with parallel public narrative companion.** `_retro/2026-05-10-p10-retro.md` lands alongside `retros/2026-05-10-p5.yaml` — prior public-side cycles (P3 / P4) shipped sidecar-only, with public `_retro/` containing only automated SessionStart-hook drafts. The parallel narrative pattern is the explicit publication shape for interactive P10 retros going forward.
- **9th fam member surfaces in the OS.** Sumi joined The Crew this cycle as the 5th P3 enforcement rail (Frame E placement; specialist agent triggered for narrow scope, sibling-shape to Codex P3B). Sumi v1.0/v1.1/v1.2 trilogy in 24 hours + v1.3 drift-scan extension the next day. The dashboard's findings detail table now reflects this as 4 line items (Sumi v1.0 / v1.1 / v1.2 / v1.3 — `1.1` through `1.4`).
- **Sidecar count crosses sprint-2 threshold.** With `2026-04-24-p3.yaml` + `2026-05-03-p4.yaml` + `2026-05-10-p5.yaml` now accumulated, the 3+ sidecar threshold for multi-retro trend rendering is met. Sprint-2 unlocks at the next sidecar ship; this v1.5 stays single-retro snapshot grain to preserve the v1.x release lineage.
- **Null-field forward-compatibility verified end-to-end.** v1.5's sidecar leaves `discipline_metrics` + `latency_observations` + `fam_dispatch_distribution` null in this first ship (per-cycle tally script not yet shipped); the dashboard renders graceful "—" placeholders for null fields per v1.3's null-handling fix. Backfill from `.claude/hook-fires.jsonl` + `~/.claude/projects/*.jsonl` will land in a follow-up sidecar revision; the cross-cycle apples-to-apples shape is gated on this becoming script-driven (not manual) before sprint-2 ships.
- **OS version bump in footer attribution.** Thin attribution band now reads `Dashboard v1.5 · Schema v1.0 · Rozzzsie OS v3.10.4 · EDD 2024 · Source · About`.

### v1.4 — 2026-05-04 (Frame 2 fam-dispatch widget + measurement-surface anchor + Luma reframe-axis tally relocation)

- **New top-band fam-dispatch widget.** Surfaces fam-wide agent activity with explicit sub-band split: dispatch axis (Agent-tool subagents: Deputies / Luma / Codex / silent-failure-hunter / Breakline / Teacher) and reactions axis (Brindle: hook-driven session_starts + reactions + session_ends). Sub-band split was Luma's verdict — conflating the two axes would let the high-cardinality reactions axis visually overpower the dispatch rails (different units).
- **Discipline band simplified.** "Discipline + dispatch" band collapsed to "Discipline" (checkpoint-bar only); Codex/Teacher/Luma scalars removed from this band (now redundant with the fam widget).
- **Luma reframe-axis tally relocated.** Moved from band-tier prominence to a "Luma reframe-axis facet (deep-dive)" panel with explicit empty-state copy naming the categorization constraint (human-distilled review, not auto-extracted from transcript metadata).
- **Measurement-surface anchor.** Each rendered metric now footnotes its source path (`.claude/hook-fires.jsonl`, `~/.claude/projects/*.jsonl`, `.claude/session-start-latency.log`) so the reader can trace the artifact behind every number.

### v1.3 — 2026-05-04 (re-render against `2026-05-03-p4.yaml` + v3.9.3 cascade + null-handling fix)

- **Re-render against the new sidecar.** Source data updated from `retros/2026-04-24-p3.yaml` → `retros/2026-05-03-p4.yaml` (the P4 sidecar shipped with the v3.9.3 reframe, covering the v3.9.x ship cycle, window 2026-04-26 → 2026-05-03, 12 findings × 11 fields). Default sidecar arg in `render.py` retargeted to match.
- **v3.9.3 Pn-token cascade lands in the renderer.** Hero header `P8 Retro #...` → `P10 Retro #...`; hero subtitle "...most recent P8 weekly retrospective..." → "...most recent P10 weekly retrospective..."; HTML `<title>` tag likewise. Sidecar finding titles that name the *new* P8 (autonomous iteration loop, was P9 in v3.4-v3.9.0) propagate verbatim — those are correct content under v3.9.3 numbering, not residual cascade.
- **OS version bump in footer attribution.** Thin attribution band now reads `Dashboard v1.3 · Schema v1.0 · Rozzzsie OS v3.9.3 · EDD 2024 · Source · About`.
- **Null-handling bug fix (real graceful suppression).** v1.0–v1.2's design intent was "absent metrics gracefully suppress their callouts" but only `miss_pct` + `meta_finding.headline` were actually implemented that way. The `2026-05-03-p4.yaml` sidecar surfaced the gap by redacting `discipline_metrics` + `latency_observations` to null (operator-traceable to specific session windows); `:.0f` against `None` crashed the renderer at first run. Fixed: `latency_median`, `latency_p95`, `latency_max`, `latency_violations`, `window_session_count` now pre-format with `"—"` fallback when null; `codex_invocations` + `teacher_invocations` get `or 0` coercion (since `dict.get(K, 0)` only fires on missing keys, not on `null` values). Behavior now matches design intent across all dashboard bands.

### v1.2 — 2026-04-25 night (Frame 1 + 2 enhancements composite per Luma reframe)

- **Layer-mismatch fix.** Luma's reframe on the v1.1 about-section question: the issue wasn't footer-styling, it was the category error of treating positioning prose as a dashboard element. Frame 1 + 2 enhancements stacked: prose moves to README (here), dashboard footer becomes a thin attribution band, hero gains a single inline "what this is" beat so cold-landings answer the category question without a click.
- **Footer thin attribution band.** Replaced the 3-paragraph "About this dashboard" prose footer with a single-line band: `Dashboard v1.2 · Schema v1.0 · Rozzzsie OS v3.5.2 · EDD 2024 · Source · About`. Width rhythm now holds — 1080px container all the way down, no narrow-column snap. Industry-legible: dashboards rarely have prose footers; readers stop noticing the footer because there's nothing to notice.
- **Hero "what this is" beat.** New 30-word inline subtitle right under the hero meta row: *"Governance health metrics from the most recent P8 weekly retrospective in the Rozzzsie OS. Same shape as LangSmith / Langfuse / DashChat dashboards (quantitative metrics on a temporal axis); different semantics — governance evolution, not service telemetry."* Cold-landing CTO gets the category answer in two seconds without scrolling.
- **README reorder for audience-grain.** This file now leads with positioning prose ("What this is"), surfaces release notes second, collapses developer-facing content (architecture, build provenance, re-render workflow) into a `<details>` block at the bottom. CTO cold-landing on README hits L5 thesis above the dev fold.
- **§14 sub-family #8 captured (sanitization-rule-vs-audience-grain).** Earlier in the v1.x evening, public sidecar `retros/2026-04-24-p3.yaml` leaked a meta-finding text describing controller-decision-cadence governance-internal observation. The sanitization passed all 4 §15 sub-checks (a/b/c/d — names/paths/commits/workspace-lists) but missed the commentary axis. Fixed in commit `99d4eb6`; rule extension queued for next P8.

### v1.1 — 2026-04-25 evening (polish release, post-v1 review)

- **Copy polish.** Verbose label tightening across the discipline + latency bands. "Checkpoint-bar miss rate (this retro)" → "Current checkpoint miss rate" · "Prior-session miss rate" → "Prior session" · "Luma invocations (total)" → "Luma invocations" · "Window session count" → "Sessions in window" · "P95 first-tool latency" → "P95" · "Threshold violations (>120s)" → "Violations (>120s)". Director-skim grain.
- **Meta-finding callout louder.** Was a thin 3px green strip; now a full-bordered card with 6px accent rail, an architectural ◆ icon at 1.75rem, bolder eyebrow, larger callout-text, subtle shadow. The "architect gold" insight at the bottom of the page now reads as the eye-magnet it should always have been.
- **Scope-honest footer layout fix.** Was sitting bottom-left only because `.scope-honest p { max-width: 64ch }` constrained paragraph width without anything balancing the right side. Moved max-width to the parent section + added `margin: 4rem auto 0` so the footer reads as a deliberate centered narrow block. (Subsequently superseded by v1.2's thin-band rewrite — Luma's layer-mismatch reframe surfaced that the underlying issue was prose-as-dashboard-element, not footer-styling.)
- **README dashboard pointer.** The repo README now surfaces the live dashboard URL above the agent fold; `dashboard/` and `retros/` finally listed in "What's in this repo".
- **URL fix carried forward (`d66b8e8`).** The earlier-tonight URL claim was corrected from a memory-not-artifact assertion (org-page form) to the verified project-page form (`rozzzsie.github.io/Rozzzsie/dashboard/`). All four URL mentions now consistent.

### v1.0 — 2026-04-25 (initial ship, commit `a7e0305`)

- Sprint-1 single-retro render shipped per Luma's 2026-04-25 evening consult (Frame 1 + Frame 3 stacked: subtree-in-Rozzzsie-public, scope-honest single-retro v1).
- 6 sections: hero with EDD-arxiv anchor / decision velocity tiles / discipline + dispatch bands / proposal backlog cohort + latency observations / 15-finding detail table / scope-honest footer.
- Renderer: `render.py` (stdlib + optional PyYAML; minimal YAML subset parser fallback so the renderer runs anywhere `python3` runs).
- Director-audience styling: typographic hierarchy, status-pill semantics, no-JS, print-friendly, mobile-responsive.

### v2 (queued, gated on schema-stability review at 2026-05-15)

- Multi-retro trend rendering once 3+ sidecars accumulate
- Sparkline-style miss-rate trends + Teacher-invocations-over-time visualization
- Audience-extension paths (interviewer mode, internal-vs-external surface variants)
- Possible Frame-3 follow-up if README's dev-vs-positioning balance becomes a friction point: spin up `dashboard/about.html` as a third surface (positioning narrative gets its own page; README stays dev-flavored)

---

<details>
<summary><strong>For developers</strong> — architecture, build provenance, re-render workflow</summary>

## Architecture (sprint-1)

- **Source data**: each P10 retro emits a YAML sidecar parallel to the narrative `.md` (P10 was P8 in v3.5.x; the v3.9.3 cascade renumbered the weekly retro slot). Filename pattern: `_retro/YYYY-MM-DD-pN.yaml` (private; sanitized excerpts surface here for the public render).
- **Schema**: `_config/schemas/retro-sidecar-schema-1.0.yaml` (canonical, private) + stable symlink. Symlink-canonical pattern, mirrors `agent-protocols-3.9.3.md` precedent.
- **Render**: HTML single-page rendered from the sidecar(s) and dropped into this `dashboard/` subtree on push. GitHub Pages serves the same subtree at `rozzzsie.github.io/Rozzzsie/dashboard/`.
- **Update cadence**: sprint-1 ships static-rendered v1.x from a single retro. Sprint-2 unlocks multi-retro aggregation once 3+ retros' sidecars exist.

## What's here

- `README.md` (this file) — positioning prose + release notes + developer reference (this collapsible)
- `index.html` — pre-rendered single-retro snapshot. Currently rendered against `../retros/2026-05-03-p4.yaml` (the most recent sidecar, shipped with the v3.9.3 reframe).
- `assets/dashboard.css` — director-audience styling: typographic hierarchy, status-pill semantics, no-JS, print-friendly
- `render.py` — Python renderer (stdlib + optional PyYAML); reads a sidecar YAML and emits `index.html`. `DASHBOARD_VERSION` constant carries the canonical version surface.
- *(coming, sprint-2)* `trend.html` — multi-retro trend page once schema has survived 3 cycles

## Re-rendering after a new sidecar

When a new P10 retro lands and a sidecar is added to `../retros/`, regenerate the dashboard:

```bash
cd dashboard/
python3 render.py ../retros/2026-05-03-p4.yaml index.html  # example
```

The renderer defaults to `../retros/2026-05-03-p4.yaml` → `./index.html` if no args given (v1.3+; v1.0–v1.2 defaulted to `2026-04-24-p3.yaml`). For v1.x: uses the most recent retro as the single source. v2 (multi-retro trend) is the natural extension surface once 3+ sidecars exist; the default-arg pattern retires once the renderer auto-selects the most recent sidecar by glob.

## Build provenance

Sprint Item 7 of the 2026-04-25 weekend architecture sprint shipped the sidecar schema + first hand-built sidecar (`_retro/2026-04-24-p3.yaml` — 15 findings × 11 fields). The render layer (this folder) is the next deliverable. Frame 1 + Frame 3 stacked per Luma's 2026-04-25 evening consult: subtree-in-Rozzzsie-public over a separate-repo build (consistency-with-spine), single-retro v1 over multi-retro-faked v1 (scope-honest, no overclaiming from n=1 data). v1.2 layered Luma's second consult (layer-mismatch reframe, Frame 1 + 2 enhancements composite) on top.

## Sanitization rules for public-facing sidecars

(Family: §15 confidentiality scope audit, extended via §14 sub-family #8 captured 2026-04-25 night.)

- (a) Direct workspace references — drop or genericize
- (b) Bespoke private-scope construct names — drop from enumerations, genericize
- (c) Evidence citations to private files / commit hashes — strip
- (d) Enumerated workspace lists — generalize
- (e) **Commentary axis** (added v1.2 / 2026-04-25): free-text fields (headlines, descriptions, summaries, meta-findings, comments) get audience-grain audit separate from rule-match audit. Imagine the artifact in front of a director / CTO / external reviewer. Does any sentence read as workplace-style commentary about a person's working pattern, decision cadence, capacity, or performance — even when phrased generically? If yes, redact or rephrase.

The `meta_finding.headline` field in the public sidecar is currently absent because the 2026-04-24 retro's meta-finding carried governance-internal commentary (controller decision cadence). The dashboard's meta-finding callout suppresses gracefully when the field is empty.

</details>
