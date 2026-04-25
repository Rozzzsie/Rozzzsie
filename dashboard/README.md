# Dashboard / Observability Layer

**Current release:** **v1.1** (2026-04-25 evening). [Live at `rozzzsie.github.io/Rozzzsie/dashboard/`](https://rozzzsie.github.io/Rozzzsie/dashboard/) · Tag: `dashboard-v1.1` · Renderer: [`render.py`](render.py) (`DASHBOARD_VERSION = "1.1"`).

The dashboard is the OS observability surface — a render of the governance state into a shape leadership and external readers can browse without diving into the protocol doc, the retro narratives, or the proposals file. Sprint-1 scope: render the most recent P8 retro from its sidecar YAML, governance-architect framing copy, explicit "v2 will add multi-retro trend graphs" placeholder. Sprint-2: multi-retro aggregation, audience-extension paths, eventual co-emission of sidecar at retro session close (per Protocol 7).

## Release notes

### v1.1 — 2026-04-25 evening (polish release, post-v1 review)

- **Copy polish.** Verbose label tightening across the discipline + latency bands. "Checkpoint-bar miss rate (this retro)" → "Current checkpoint miss rate" · "Prior-session miss rate" → "Prior session" · "Luma invocations (total)" → "Luma invocations" · "Window session count" → "Sessions in window" · "P95 first-tool latency" → "P95" · "Threshold violations (>120s)" → "Violations (>120s)". Director-skim grain.
- **Meta-finding callout louder.** Was a thin 3px green strip; now a full-bordered card with 6px accent rail, an architectural ◆ icon at 1.75rem, bolder eyebrow, larger callout-text, subtle shadow. The "architect gold" insight at the bottom of the page now reads as the eye-magnet it should always have been.
- **Scope-honest footer layout fix.** Was sitting bottom-left only because `.scope-honest p { max-width: 64ch }` constrained paragraph width without anything balancing the right side. Moved max-width to the parent section + added `margin: 4rem auto 0` so the footer reads as a deliberate centered narrow block.
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

## Why this exists

Industry harness dashboards (LangSmith, Langfuse, DashChat) surface telemetry — tokens, latency, error rates, eval scores. Same *shape* (quantitative metrics on a temporal axis), different *semantics*. Rozzzsie's dashboard surfaces governance evolution: proposal lifecycle from authoring to executed, hook fire-rate health, checkpoint-bar discipline trends, Luma tally by category, decision velocity per retro, family-pattern detection across weeks. The arxiv anchor is *evaluation as continuous governing function, not terminal checkpoint* (EDD 2024, arxiv 2411.13768v3) — that principle is what distinguishes this layer from a Langfuse/LangSmith clone.

## Architecture (sprint-1)

- **Source data**: each P8 retro emits a YAML sidecar parallel to the narrative `.md`. Filename pattern: `_retro/YYYY-MM-DD-pN.yaml` (private; sanitized excerpts may surface here for the public render).
- **Schema**: `_config/schemas/retro-sidecar-schema-1.0.yaml` (canonical) + stable symlink. Symlink-canonical pattern, mirrors `agent-protocols-3.5.2.md` precedent.
- **Render**: HTML single-page rendered from the sidecar(s) and dropped into this `dashboard/` subtree on push. GitHub Pages serves the same subtree.
- **Update cadence**: sprint-1 ships static-rendered v1 from a single retro. Sprint-2 unlocks multi-retro aggregation once 3+ retros' sidecars exist.

## What's here

- `README.md` (this file) — the architecture and intent
- `index.html` — **v1 shipped 2026-04-25 evening.** Pre-rendered single-retro snapshot from `../retros/2026-04-24-p3.yaml`
- `assets/dashboard.css` — director-audience styling: typographic hierarchy, generous whitespace, status-pill semantics, no-JS, print-friendly
- `render.py` — Python renderer (stdlib + optional PyYAML); reads a sidecar YAML and emits `index.html`. Run via `python3 dashboard/render.py [sidecar.yaml] [out.html]`. Used build-side for v1 (pre-rendered + checked in); sprint-2+ may auto-render via GitHub Action.
- *(coming, sprint-2)* `trend.html` — multi-retro trend page once schema has survived 3 cycles

## Live URL

**[rozzzsie.github.io/Rozzzsie/dashboard/](https://rozzzsie.github.io/Rozzzsie/dashboard/)** — GitHub Pages serves the rendered `index.html` directly. HTTPS enforced; first build runs on every push to `main`. The `/Rozzzsie/` segment is the repo name; this is project-page hosting, not org-page (which would require a separate repo named `rozzzsie.github.io`).

Alternatively, just open `dashboard/index.html` in a browser locally — the render is fully self-contained (CSS in `assets/`, no JS).

## Re-rendering after a new sidecar

When a new P8 retro lands and a sidecar is added to `retros/`, regenerate the dashboard:

```bash
cd dashboard/
python3 render.py ../retros/2026-05-01-p4.yaml index.html  # example
```

For v1: the renderer uses the most recent retro as the single source. v2 (multi-retro trend) is the natural extension surface once 3+ sidecars exist.

## Build provenance

Sprint Item 7 of the 2026-04-25 weekend architecture sprint shipped the sidecar schema + first hand-built sidecar (`_retro/2026-04-24-p3.yaml` — 15 findings × 11 fields). The render layer (this folder) is the next deliverable. Frame 1 + Frame 3 stacked per Luma's 2026-04-25 evening consult: subtree-in-Rozzzsie-public over a separate-repo build (consistency-with-spine), single-retro v1 over multi-retro-faked v1 (scope-honest, no overclaiming from n=1 data).

## Why scope-honest matters

A polished-looking dashboard with one data point is the kind of thing a sharp reviewer (CTO, interviewer, peer architect) catches and discounts. Sprint-1 is honest: this is what one retro looks like, here's the rendering contract, the next retro's sidecar will auto-render here when it lands. That's the L5-evidence move — *the OS observes itself* — without faking trends from n=1.
