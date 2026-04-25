# Dashboard / Observability Layer

**Current release: v1.2** (2026-04-25 night) · Tag: `dashboard-v1.2` · [Source](https://github.com/Rozzzsie/Rozzzsie/tree/main/dashboard)

**Live: [rozzzsie.github.io/Rozzzsie/dashboard/](https://rozzzsie.github.io/Rozzzsie/dashboard/)** — GitHub Pages serves the rendered `index.html` on every push to `main`. HTTPS enforced. Open `dashboard/index.html` directly in a browser to read locally — the render is fully self-contained (CSS in `assets/`, no JS).

## What this is

The dashboard is the OS observability surface — a render of the governance state into a shape leadership and external readers can browse without diving into the protocol doc, the retro narratives, or the proposals file.

Industry harness dashboards (LangSmith, Langfuse, DashChat) surface telemetry — tokens, latency, error rates, eval scores. Same *shape* (quantitative metrics on a temporal axis), different *semantics*. Rozzzsie's dashboard surfaces **governance evolution**: proposal lifecycle from authoring to executed, hook fire-rate health, checkpoint-bar discipline trends, Luma tally by category, decision velocity per retro, family-pattern detection across weeks. The arxiv anchor is *evaluation as continuous governing function, not terminal checkpoint* ([EDD 2024](https://arxiv.org/abs/2411.13768)) — that principle is what distinguishes this layer from a Langfuse/LangSmith clone.

**Why scope-honest matters.** A polished-looking dashboard with one data point is the kind of thing a sharp reviewer (CTO, interviewer, peer architect) catches and discounts. Sprint-1 is honest: this is what one retro looks like, here's the rendering contract, the next retro's sidecar will auto-render here when it lands. That's the L5-evidence move — *the OS observes itself* — without faking trends from n=1. Sprint-2 unlocks multi-retro trend rendering once 3+ sidecars accumulate (gated on schema v1.0 stability review at 2026-05-15).

## Release notes

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

- **Source data**: each P8 retro emits a YAML sidecar parallel to the narrative `.md`. Filename pattern: `_retro/YYYY-MM-DD-pN.yaml` (private; sanitized excerpts surface here for the public render).
- **Schema**: `_config/schemas/retro-sidecar-schema-1.0.yaml` (canonical, private) + stable symlink. Symlink-canonical pattern, mirrors `agent-protocols-3.5.2.md` precedent.
- **Render**: HTML single-page rendered from the sidecar(s) and dropped into this `dashboard/` subtree on push. GitHub Pages serves the same subtree at `rozzzsie.github.io/Rozzzsie/dashboard/`.
- **Update cadence**: sprint-1 ships static-rendered v1.x from a single retro. Sprint-2 unlocks multi-retro aggregation once 3+ retros' sidecars exist.

## What's here

- `README.md` (this file) — positioning prose + release notes + developer reference (this collapsible)
- `index.html` — pre-rendered single-retro snapshot from `../retros/2026-04-24-p3.yaml` (most recent sidecar)
- `assets/dashboard.css` — director-audience styling: typographic hierarchy, status-pill semantics, no-JS, print-friendly
- `render.py` — Python renderer (stdlib + optional PyYAML); reads a sidecar YAML and emits `index.html`. `DASHBOARD_VERSION` constant carries the canonical version surface.
- *(coming, sprint-2)* `trend.html` — multi-retro trend page once schema has survived 3 cycles

## Re-rendering after a new sidecar

When a new P8 retro lands and a sidecar is added to `../retros/`, regenerate the dashboard:

```bash
cd dashboard/
python3 render.py ../retros/2026-05-01-p4.yaml index.html  # example
```

The renderer defaults to `../retros/2026-04-24-p3.yaml` → `./index.html` if no args given. For v1.x: uses the most recent retro as the single source. v2 (multi-retro trend) is the natural extension surface once 3+ sidecars exist.

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
