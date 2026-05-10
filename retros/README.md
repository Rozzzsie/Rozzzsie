# Retros — Rozzzsie

Sanitized snapshots of P10 weekly retrospectives (P8 in v3.5.x and earlier; renumbered in v3.9.3 cascade — see CLAUDE.md "Protocol quick reference"). The dashboard renders from the sidecar YAML files in this folder.

## What's here

- `2026-04-24-p3.yaml` — sanitized sidecar from the 2026-04-24 retro (15-day catchup window 2026-04-17 → 2026-04-24). 15 findings × 11 fields. Authored under v3.5.x P8 numbering; dashboard v1 rendered from this file as its single canonical input.
- `2026-05-03-p4.yaml` — sanitized sidecar from the 2026-05-03 retro covering the v3.9.x ship cycle (window 2026-04-26 → 2026-05-03). 12 findings × 11 fields. First sidecar published under v3.9.3 protocol numbering (P10 = Weekly retrospective). Identity-candidate observations on adversarial-audit-as-routine-governance and gate-discipline-for-graduated-authority carried forward to next cycle.
- `2026-05-10-p5.yaml` — sanitized sidecar from the 2026-05-10 retro covering the v3.10.x ship cycle (window 2026-05-03 → 2026-05-10). 15 findings × 11 fields. First sidecar published with a parallel public narrative companion (`_retro/2026-05-10-p10-retro.md`) — prior cycles shipped sidecar-only on the public side. Major content: Sumi v1.0/v1.1/v1.2/v1.3 trilogy + drift-scan extension (5th P3 enforcement layer; new agent in The Crew); v3.10.3 checkpoint-bar PostToolUse format-validator + substantive_v2 mutation-tool-aware classification; v3.10.4 MUTATION_TOOLS Conservative extension; Phase 1 doctrine ships (§18 matcher discipline + §19 MD-vs-HTML deliverable rendering + §20 long-lived branch merge); subagent Write-permission Class-S signal resolved at config layer; 1 pending Teacher proposal (Aggressive MUTATION_TOOLS — execution-trigger SDK MCP tool surface stabilization). discipline_metrics + latency_observations + fam_dispatch_distribution null in this first ship — backfill pending the per-cycle tally script.
- *(coming, sprint-2 — 3+ sidecars now accumulated; multi-retro trend rendering unlocks at next sidecar ship)* `2026-05-17-p6.yaml`, etc. — the trend-rendering substrate.

The narrative `.md` retros are private — they carry stakeholder names, specific Confluence pages, Slack channel IDs, commit hashes, and per-workspace state with private detail. The sidecars are designed to be the public-grain summary: structured, abstract, citation-removed, suitable for the dashboard render and for external readers.

## Why two surfaces (narrative + sidecar)

The sidecar pattern was named in v3.5.0 as part of the Synthesis-Surface Pre-Render Pattern primitive. **Narrative stays canonical**: when the .md and the .yaml disagree, the .md wins; the .yaml is regenerated from the .md, never the other way. Sidecars live in this folder parallel to the narrative for sprint-1; v1 sidecars are hand-built; sprint-2+ co-emit at retro session close once the schema has survived 3 cycles.

Schema reference: the sidecar schema lives at the canonical-symlink path on the private side; future versions will retarget the symlink without touching live references (see `CLAUDE.md` versioned-file naming convention).

## Sanitization rules applied

For each public-surfaced sidecar:
- Stakeholder names dropped or genericized to role categories (e.g., "manager" / "Ops Lead" / "Product Lead" / "peer specialist")
- Private-workspace paths in `target_surface` fields replaced with generic surface names where they leaked specific workspace names; otherwise governance paths (`_config/`, `.claude/`, `~/.claude/agents/`) stay verbatim — those are public-by-design
- `detail_ref` cross-pointers dropped or replaced with self-references — the narrative they pointed at is private
- `meta_finding.detail_ref` similarly dropped
- All other fields (IDs, categories, evidence counts, recommendations, statuses, target_week) are already abstract enough — kept verbatim

## What this enables

- **Dashboard rendering** — the dashboard at [`rozzzsie.github.io/Rozzzsie/dashboard/`](https://rozzzsie.github.io/Rozzzsie/dashboard/) (sprint-1 v1 shipped 2026-04-25 evening; source at `dashboard/index.html` + `dashboard/render.py`) consumes this folder's `*.yaml` files as its data layer.
- **External reader scan** — a reader can browse this folder and see the *shape* of the retro discipline (15 findings, terminal status on each, decision velocity, family-pattern detection) without needing access to the private narrative.
- **Trend substrate (sprint-2)** — once 3+ sidecars accumulate, multi-retro trend graphs become the natural next surface; the schema is stable enough now to support that without breaking changes.
