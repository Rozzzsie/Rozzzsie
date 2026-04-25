# Dashboard / Observability Layer

The dashboard is the OS observability surface — a render of the governance state into a shape leadership and external readers can browse without diving into the protocol doc, the retro narratives, or the proposals file. Sprint-1 scope: render the most recent P8 retro from its sidecar YAML, governance-architect framing copy, explicit "v2 will add multi-retro trend graphs" placeholder. Sprint-2: multi-retro aggregation, audience-extension paths, eventual co-emission of sidecar at retro session close (per Protocol 7).

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
