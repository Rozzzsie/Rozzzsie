# Retros — Rozzzsie

Sanitized snapshots of P8 weekly retrospectives. The dashboard renders from the sidecar YAML files in this folder.

## What's here

- `2026-04-24-p3.yaml` — sanitized sidecar from the 2026-04-24 P8 retro (the most recent full interactive retro, 15-day catchup window 2026-04-17 → 2026-04-24). 15 findings × 11 fields. The dashboard's v1 renders from this file as its single canonical input.
- *(coming, sprint-2 once 3+ retros exist)* `2026-05-01-p4.yaml`, `2026-05-08-p5.yaml`, etc. — the trend-rendering substrate.

The narrative `.md` retros are private — they carry stakeholder names, specific Confluence pages, Slack channel IDs, commit hashes, and per-workspace state with private detail. The sidecars are designed to be the public-grain summary: structured, abstract, citation-removed, suitable for the dashboard render and for external readers.

## Why two surfaces (narrative + sidecar)

The sidecar pattern was named in v3.5.0 as part of the Synthesis-Surface Pre-Render Pattern primitive. **Narrative stays canonical**: when the .md and the .yaml disagree, the .md wins; the .yaml is regenerated from the .md, never the other way. Sidecars live in this folder parallel to the narrative for sprint-1; v1 sidecars are hand-built; sprint-2+ co-emit at retro session close once the schema has survived 3 cycles.

Schema reference: the sidecar schema lives at the canonical-symlink path on the private side; future versions will retarget the symlink without touching live references (see `CLAUDE.md` versioned-file naming convention).

## Sanitization rules applied

For each public-surfaced sidecar:
- Stakeholder names dropped or genericized (Caroline / Julius / Gonzalo / etc. → "manager" / "Ops Lead" / "Product Lead" / etc.)
- Private-workspace paths in `target_surface` fields replaced with generic surface names where they leaked specific workspace names; otherwise governance paths (`_config/`, `.claude/`, `~/.claude/agents/`) stay verbatim — those are public-by-design
- `detail_ref` cross-pointers dropped or replaced with self-references — the narrative they pointed at is private
- `meta_finding.detail_ref` similarly dropped
- All other fields (IDs, categories, evidence counts, recommendations, statuses, target_week) are already abstract enough — kept verbatim

## What this enables

- **Dashboard rendering** — the dashboard at `dashboard/index.html` (sprint-1 not yet shipped; placeholder at `dashboard/README.md`) consumes this folder's `*.yaml` files as its data layer.
- **External reader scan** — a reader can browse this folder and see the *shape* of the retro discipline (15 findings, terminal status on each, decision velocity, family-pattern detection) without needing access to the private narrative.
- **Trend substrate (sprint-2)** — once 3+ sidecars accumulate, multi-retro trend graphs become the natural next surface; the schema is stable enough now to support that without breaking changes.
