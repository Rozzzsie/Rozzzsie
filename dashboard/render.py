#!/usr/bin/env python3
"""
Rozzzsie Governance Dashboard renderer — sprint-1 v1.

Reads a sanitized retro sidecar YAML from `retros/<date>-pN.yaml` and emits a
pre-rendered `dashboard/index.html` ready for GitHub Pages serving.

Architecture per Synthesis-Surface Pre-Render Pattern (v3.5.0): mechanical
rendering happens hook-side / build-side; the agent fills judgment slots if
any are present. v1 has no judgment slots — single-retro snapshot is purely
mechanical. v2 (multi-retro trends, once 3+ sidecars exist) is the natural
extension surface.

Usage:
    python3 render.py                          # default: render
                                                #   ../retros/2026-05-03-p4.yaml
                                                #   → ./index.html
    python3 render.py <sidecar.yaml>           # render named sidecar to index.html
    python3 render.py <sidecar.yaml> <out.html>

Dependency: only stdlib + PyYAML if available; falls back to a tiny YAML
subset parser sufficient for the v1 schema if PyYAML isn't installed.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-not-found]
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ─── Release ──────────────────────────────────────────────────────────────────
#
# Dashboard release version. Bumped on every change that lands a visible-grain
# difference for readers (copy polish, visual hierarchy, layout fix, schema
# extension). Major bumps reserved for multi-retro trend rendering
# and beyond. Consistent-with-spine semver, mirrors `agent-protocols-X.Y.Z.md`.
DASHBOARD_VERSION = "3.7"


# ─── YAML loader ──────────────────────────────────────────────────────────────

def load_sidecar(path: Path) -> dict[str, Any]:
    """Load a sidecar YAML. Prefers PyYAML; falls back to minimal subset parser."""
    text = path.read_text(encoding="utf-8")
    if HAS_YAML:
        return yaml.safe_load(text)  # type: ignore[no-any-return]
    return _parse_minimal_yaml(text)


def _parse_minimal_yaml(text: str) -> dict[str, Any]:
    """Minimal YAML subset parser for the v1 sidecar schema.

    Handles: top-level scalars, dicts, list of dicts (one per finding),
    nested dicts, strings (quoted/unquoted),
    null, true/false, ints, floats. Comments stripped. No anchors/aliases.
    """
    lines = [_strip_comment(line) for line in text.splitlines()]
    return _parse_block(lines, indent=0, idx=0)[0]


def _strip_comment(line: str) -> str:
    """Strip `# comment` from a line, preserving `#` inside quoted strings."""
    out = []
    in_quote = None
    for ch in line:
        if ch in ('"', "'") and in_quote is None:
            in_quote = ch
        elif ch == in_quote:
            in_quote = None
        elif ch == "#" and in_quote is None:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _parse_block(lines: list[str], indent: int, idx: int) -> tuple[Any, int]:
    """Parse one block (dict / list) at given indent. Returns (value, next_idx)."""
    # Detect list-of-dicts (lines starting with "- ")
    while idx < len(lines) and (not lines[idx].strip()):
        idx += 1
    if idx >= len(lines):
        return {}, idx
    line = lines[idx]
    line_indent = len(line) - len(line.lstrip(" "))
    if line_indent < indent:
        return {}, idx
    stripped = line.strip()
    if stripped.startswith("- "):
        return _parse_list(lines, line_indent, idx)
    return _parse_dict(lines, line_indent, idx)


def _parse_dict(lines: list[str], indent: int, idx: int) -> tuple[dict[str, Any], int]:
    out: dict[str, Any] = {}
    while idx < len(lines):
        raw = lines[idx]
        if not raw.strip():
            idx += 1
            continue
        line_indent = len(raw) - len(raw.lstrip(" "))
        if line_indent < indent:
            break
        if line_indent > indent:
            idx += 1
            continue
        stripped = raw.strip()
        if stripped.startswith("- "):
            break
        if ":" not in stripped:
            idx += 1
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            idx += 1
            sub, idx = _parse_block(lines, indent + 2, idx)
            out[key] = sub
        else:
            out[key] = _parse_scalar(val)
            idx += 1
    return out, idx


def _parse_list(lines: list[str], indent: int, idx: int) -> tuple[list[Any], int]:
    out: list[Any] = []
    while idx < len(lines):
        raw = lines[idx]
        if not raw.strip():
            idx += 1
            continue
        line_indent = len(raw) - len(raw.lstrip(" "))
        if line_indent < indent:
            break
        stripped = raw.strip()
        if not stripped.startswith("- "):
            break
        # Inline first key-value of the dict item
        first = stripped[2:]
        item: dict[str, Any] = {}
        if ":" in first:
            key, _, val = first.partition(":")
            item[key.strip()] = _parse_scalar(val.strip())
        idx += 1
        # Subsequent indented keys belong to this dict item
        while idx < len(lines):
            r = lines[idx]
            if not r.strip():
                idx += 1
                continue
            li = len(r) - len(r.lstrip(" "))
            if li <= indent:
                break
            s = r.strip()
            if s.startswith("- "):
                break
            if ":" in s:
                k, _, v = s.partition(":")
                v = v.strip()
                k = k.strip()
                if v == "":
                    sub, idx = _parse_block(lines, li + 2, idx + 1)
                    item[k] = sub
                else:
                    item[k] = _parse_scalar(v)
                    idx += 1
            else:
                idx += 1
        out.append(item)
    return out, idx


def _parse_scalar(val: str) -> Any:
    """Parse a YAML scalar value (string, int, float, bool, null)."""
    if val == "null" or val == "~" or val == "":
        return None
    if val == "true":
        return True
    if val == "false":
        return False
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(p.strip()) for p in inner.split(",")]
    try:
        if "." in val or "e" in val.lower():
            return float(val)
        return int(val)
    except ValueError:
        return val


# ─── Schema validation ────────────────────────────────────────────────────────
#
# ⛔ WHY THIS EXISTS. Measured 2026-08-02 across 15 sidecars: every TOP-LEVEL key
# in p17 matched p16, and at the sub-key level `discipline_metrics`,
# `fam_dispatch_distribution`, `latency_observations` and `hook_health` shared
# ZERO keys with p16 — `proposal_backlog` shared one of four. Nothing errored,
# because a renamed sub-key makes `.get()` return None, which renders as an
# em-dash: visually identical to "measured, and it was empty". Sixteen cycles
# of sidecars drifted from their renderer one field at a time.
#
# Two arms, deliberately asymmetric:
#   REQUIRED missing -> FAIL. The renderer depends on it; rendering anyway
#     publishes a blank where a number belongs.
#   UNKNOWN present  -> WARN. A new field is how every one of these renames
#     announced itself, and a warn is what turns the NEXT one into a 10-second
#     fix instead of a 16-cycle drift. It does not block, because a sidecar
#     author adding a field before the renderer reads it is legitimate.
#
# The KNOWN set is the load-bearing half. A required-only check cannot see a
# rename — it reports the old key missing and says nothing about the new key
# sitting beside it.
#
# ─────────────────────────────────────────────────────────────────────────────
# THIS IS THE ONLY SCHEMA SURFACE. (merged 2026-08-02)
#
# There used to be a second one: `_config/schemas/retro-sidecar-schema.yaml`, an
# annotated prose template written 2026-06-10, cited in every published sidecar
# header and in this directory's README — and parsed by nothing. It was deleted,
# not deprecated, because a documentation surface that no consumer reads drifts
# in the one direction nobody checks. When it was finally measured against the
# 15 sidecars it claimed to describe, it was not merely stale, it was WRONG:
#
#   category           doc: 6 values     real: 11  (6 never documented)
#   status             doc: 8 values     real: 8   (3 undocumented, 3 unused)
#   recommendation     doc: 5 values     real: 6   ('watch' used 31x, undocumented)
#   source_catchment   doc: 4-value enum real: 70 distinct free-text composites
#
# Being unenforced is the ONLY reason that cost nothing. Had anything parsed it,
# it would have rejected valid sidecars since roughly May.
#
# ─── Field intent (absorbed from the retired 1.0 template) ───────────────────
#
# retro_id      stable id for cross-retro joins, `YYYY-MM-DD-pN`. N is the
#               sequential retro ordinal, NOT the protocol number.
# window_start/_end   inclusive period the metrics cover.
# prior_retro   the id this cycle's trends join against; null for the first.
# findings[]    one entry per retro section-9 row. See `findings_item` below.
# meta_finding  headline + detail_ref ONLY. Design principle, still live: the
#               narrative .md is canonical, and qualitative reasoning stays
#               there. If a meta-finding warrants quantification, split it —
#               the number becomes a field, the prose stays in the .md.
#
# Vocabularies are DESCRIPTIVE, not validated, and that is deliberate. `category`
# gained 6 members in 15 cycles by authors naming what they actually found; a
# hard enum would have converted honest reporting into schema violations, and a
# warn on every new value is noise that teaches you to ignore the warn channel.
# `source_catchment` is free text and was never really an enum — 70 distinct
# composite values, which is a truthful record of how findings arrive.
#
# The ONE vocabulary that is checked is `status`, because it is the only one the
# renderer consumes structurally: `status_pill()` builds a CSS class from it, so
# an unstyled status renders as a bare pill. Measured 2026-08-02: 4 of 8 live
# statuses had no rule, including `rejected` — a rejected finding was visually
# indistinguishable from a styled one on the public page.

SIDECAR_SCHEMA: dict[str, dict[str, Any]] = {
    "1.1": {
        "required": [
            "retro_id", "retro_date", "schema_version", "findings",
            "defect_ledger.open_total",
            "improvement_backlog.total", "improvement_backlog.open",
            "enforcement_coverage.arms_built", "enforcement_coverage.arms_armed",
            "instrument_liveness.silent_failures_observed",
            "instrument_liveness.caught_by_control",
        ],
        # ⛔ NOT required, by operator decision 2026-08-02. Sidecars redact the
        # whole `discipline_metrics` block to null when the underlying counts are
        # traceable to a person, and that redaction is SANCTIONED — so requiring
        # its sub-keys would make a correctly-redacted sidecar fail rc=3 and put
        # the author under pressure to invent numbers to get a render.
        #
        # The two contracts were in genuine conflict and only one could hold:
        # a required-field list says "absent means drift", redaction-to-null says
        # "absent is a legitimate state". Redaction wins on this block. The cost
        # is real and is accepted: drift in these four keys is now invisible to
        # the schema, so the ritual and quality-gate dials degrade to an em-dash
        # rather than raising. They render as UNKNOWN, never as zero.
        "nullable_blocks": {"discipline_metrics"},
        # Scalars the renderer reads directly. Declared so the unknown-block arm
        # can stay strict: anything NOT declared here or in `known` warns.
        "known_scalars": {
            "retro_id", "retro_date", "schema_version", "findings", "prior_retro",
            "window_start", "window_end", "trigger_source", "interactive_mode",
            "meta_finding",
        },
        # Deliberately NOT rendered — carried as a record only. Declared so they
        # do not warn, and so the fact that nothing reads them is explicit
        # rather than discovered by someone wondering where the widget went.
        "record_only": {"hook_health", "latency_observations"},
        # Per-finding contract. `required` is not aspirational — every one of
        # these is present in 154/154 findings across all 15 sidecars, so a
        # missing one is drift rather than a legitimate variation.
        "findings_item": {
            "required": {
                "id", "title", "category", "evidence_count", "source_catchment",
                "recommendation", "status", "execution_target_week",
                "target_surface",
            },
            "optional": {
                "enforcement_log_ref", "blocked_by", "alternative_framings",
                "detail_ref",
            },
        },
        # Statuses `assets/dashboard.css` has a `.pill-<status>` rule for.
        # ANTICIPATORY, not corrective: all four missing rules were added in the
        # same edit, so this arm has nothing to fire on today. It exists because
        # the status vocabulary grew 3 members in 15 cycles and the next one
        # would otherwise ship as an unstyled pill nobody notices.
        "findings_status_styled": {
            "executed", "deferred", "approved", "approved-queued", "pre-ship",
            "partial-executed", "rejected", "carried-open",
        },
        "known": {
            "defect_ledger": {
                "open_total", "live", "parked", "age_under_7d", "age_7_to_29d",
                "age_30d_plus", "age_undated", "median_age_days", "max_age_days",
                "measured_at", "measured_from", "notes",
            },
            "improvement_backlog": {
                "total", "open", "done", "parked", "open_ready",
                "open_decision_gated", "open_upstream_blocked", "notes",
            },
            "enforcement_coverage": {
                "arms_built", "arms_armed", "arms_with_written_exit_criteria",
                "arms_with_falsifiable_exit", "arms_declared_permanent",
                "checks_enumerated", "checks_with_written_exit_criteria",
                "checks_unit", "checks_unit_note", "measured_at", "measured_from",
                "notes",
            },
            "instrument_liveness": {
                "silent_failures_observed", "caught_by_control", "caught_by_review",
                "notes",
            },
            "detection_provenance": {
                "caught_by_control", "caught_by_operator", "caught_by_accident",
                "instrumented_from", "status", "notes",
            },
            "discipline_metrics": {
                "ritual_steps_defined", "ritual_steps_completed",
                "monthly_subritual_due", "monthly_subritual_completed",
                "quality_gate_traces_sampled", "quality_gate_traces_passing",
                "response_marker_missed_turns", "response_marker_blocking_fires",
                "response_marker_note", "notes",
                # Added p18 (2026-08-09) in the same edit as the sidecar that
                # introduced them, per the step 9(a) contract.
                #
                # `response_marker_graded_turns` is the DENOMINATOR that the
                # existing pair never carried: `missed_turns` has always been the
                # deduplicated numerator and `blocking_fires` the raw one, but
                # the population they are drawn from was only ever described in
                # prose. Without it a reader cannot compute a rate, which is how
                # the metrics tally shipped a fire-count ratio labelled "turns"
                # for sixteen cycles. `response_marker_miss_rate` stores that
                # rate explicitly so the tally's raw ratio can never be mistaken
                # for it again.
                #
                # ⚠️ NOT A RE-KEY. Both pre-existing field names continue in p18
                # with unchanged meaning, so no series closes here — the
                # agreement-in-overlap test is satisfied for both.
                "response_marker_graded_turns", "response_marker_miss_rate",
                # Skip rate for the intent-confirmation protocol. New series,
                # starts at p18; previously audited but never published.
                "intent_confirmation_skip_rate",
            },
            "proposal_backlog": {"authored_this_cycle", "deferred_this_cycle", "notes"},
            "fam_dispatch_distribution": {
                "learning_agent", "adversarial_reviewer", "consultant",
                "external_validator", "notes",
            },
        },
    },
}


class SidecarSchemaError(Exception):
    """A required field the renderer depends on is absent."""


def validate_sidecar(sc: dict[str, Any]) -> list[str]:
    """Fail on missing required fields; return a list of warnings for unknowns.

    Raises SidecarSchemaError naming EVERY missing key, not just the first —
    a validator that stops at the first failure turns one render into N.
    """
    version = str(sc.get("schema_version", ""))
    spec = SIDECAR_SCHEMA.get(version)
    if spec is None:
        return [f"schema_version {version!r} has no manifest — nothing validated"]

    def _resolve(path: str) -> Any:
        cur: Any = sc
        for part in path.split("."):
            if not isinstance(cur, dict):
                return None
            cur = cur.get(part)
        return cur

    warnings: list[str] = []
    # Top-level blocks absent from the manifest entirely. Without this arm a
    # whole renamed BLOCK passes silently — the sub-key loop only inspects
    # blocks it already knows about, so it is blind to the coarsest rename.
    declared = (
        set(spec["known"])
        | set(spec.get("known_scalars", ()))
        | set(spec.get("record_only", ()))
    )
    for block in sorted(set(sc) - declared):
        warnings.append(
            f"{block} is a top-level block with no manifest entry — it is "
            "either record-only (no renderer reads it) or newly renamed"
        )
    # ⛔ THE COALESCE LICENSE BELONGS ON THE PATH THAT RUNS. The overlap test
    # that licenses merging these two fields into one trend series lives in the
    # suite — which the bare `python3 render.py` of a retro close never invokes.
    # A future sidecar carrying both keys with different values would make the
    # suite red for anyone who ran it, while the render published quietly.
    dm_t = (sc.get("discipline_metrics") or {}).get("teacher_invocations")
    flat_t = (sc.get("fam_dispatch_distribution") or {}).get("learning_agent")
    if dm_t is not None and flat_t is not None and dm_t != flat_t:
        warnings.append(
            f"teacher_invocations ({dm_t}) and learning_agent ({flat_t}) disagree — "
            "the trend card coalesces them as ONE series on the strength of a "
            "13/13 agreement measurement; that license no longer holds"
        )

    for block, known in spec["known"].items():
        val = sc.get(block)
        if not isinstance(val, dict):
            continue
        for unknown in sorted(set(val) - known):
            warnings.append(
                f"{block}.{unknown} is not in the schema {version} manifest — "
                "if this replaces an existing field, the renderer needs re-keying"
            )

    # Per-finding arm. The top-level check only asserts that `findings` exists;
    # without this, every field inside it could be renamed at once and the
    # render would still succeed with 15 blank rows.
    item_spec = spec.get("findings_item") or {}
    styled = spec.get("findings_status_styled") or set()
    finding_missing: list[str] = []
    findings = sc.get("findings")
    # ⛔ A TYPE GUARD THAT SKIPS IS A GUARD THAT PASSES. `findings` present but
    # not a list satisfied the required check (non-None) and then silently
    # skipped this whole arm — zero warnings, followed by a raw AttributeError
    # from the renderer instead of the rc=3 contract this function promises.
    # The failure mode of an `isinstance` guard is to say nothing.
    if findings is not None and not isinstance(findings, list):
        finding_missing.append(
            f"findings (is {type(findings).__name__}, must be a list)"
        )
    if item_spec and isinstance(findings, list):
        declared_item = item_spec["required"] | item_spec["optional"]
        for i, item in enumerate(findings):
            if not isinstance(item, dict):
                warnings.append(f"findings[{i}] is not a mapping — skipped")
                continue
            fid = str(item.get("id", i))
            for absent in sorted(item_spec["required"] - set(item)):
                finding_missing.append(f"findings[{fid}].{absent}")
            for unknown in sorted(set(item) - declared_item):
                warnings.append(
                    f"findings[{fid}].{unknown} is not in the schema {version} "
                    "manifest — if this replaces an existing field, re-key the renderer"
                )
            status = item.get("status")
            if status and styled and status not in styled:
                warnings.append(
                    f"findings[{fid}].status {status!r} has no .pill-{status} rule "
                    "in assets/dashboard.css — it will render as an unstyled pill"
                )

    # Missing-required is computed LAST and carries the warnings with it. A
    # rename is one event with two halves — the old key gone, the new key
    # present — and raising before the unknown scan reports only the half that
    # says "broken", withholding the half that says "and here is what replaced
    # it". The docstring above claims this check can see a rename; this is what
    # makes that true.
    missing = [k for k in spec["required"] if _resolve(k) is None] + finding_missing
    if missing:
        msg = (
            "sidecar is missing required field(s) the renderer depends on: "
            + ", ".join(missing)
            + " — this is the sub-key drift guard; either restore the field or "
              "update SIDECAR_SCHEMA and the renderer together."
        )
        if warnings:
            msg += " Undeclared field(s) present, likely the rename: " + "; ".join(warnings)
        raise SidecarSchemaError(msg)
    return warnings


# ─── Renderers ────────────────────────────────────────────────────────────────

def _present(value: Any, dash: str = "—") -> str:
    """Render a value, or a dash when it was never recorded.

    ⛔ NEVER default a missing measurement to 0. `dict.get(key, 0)` turns "this
    cycle did not record it" into "this cycle measured zero" — indistinguishable
    on the page, and a fabricated measurement on a public artifact. Shipped in
    v3.0: three cohort stages rendered 0 for fields the p17 sidecar has never
    carried, sitting among honest em-dashes and reading as measured.
    """
    return dash if value is None else html.escape(str(value))


def render_tile(value: Any, label: str, detail: str | None = None) -> str:
    detail_html = (
        f'<div class="tile-detail">{html.escape(detail)}</div>' if detail else ""
    )
    return f"""
    <div class="tile">
      <div class="tile-value">{html.escape(str(value))}</div>
      <div class="tile-label">{html.escape(label)}</div>
      {detail_html}
    </div>
    """


def status_pill(status: str | None) -> str:
    if not status:
        return '<span class="pill pill-deferred">—</span>'
    css_class = f"pill-{status.replace('_', '-')}"
    return f'<span class="pill {css_class}">{html.escape(status)}</span>'


def render_finding_row(f: dict[str, Any]) -> str:
    return f"""
    <div class="findings-row">
      <div class="finding-id">{html.escape(str(f.get("id", "")))}</div>
      <div class="finding-title">{html.escape(str(f.get("title", "")))}</div>
      <div>{status_pill(f.get("status"))}</div>
      <div class="finding-cat">{html.escape(str(f.get("category", "")))}</div>
    </div>
    """


# ─── Decision-velocity buckets ────────────────────────────────────────────────
#
# ⛔ THE HEADLINE COUNTS EVERY FINDING; THE BUCKETS COUNTED A HARDCODED FOUR
# STATUSES. The status vocabulary grew from four to eight over 15 cycles and this
# list did not, so `approved-queued`, `partial-executed` and `carried-open`
# matched nothing and left the page: 6 findings across p4, p14, p15 and p17,
# measured 2026-08-02 — on a page whose findings-detail header reads "every one
# statused".
#
# ⭐ NOTHING WAS MIS-SHAPED, WHICH IS WHY IT RAN FOR THREE MONTHS. Each tile was
# individually correct, the headline was correct, and only the SUM disagreed —
# and no per-tile check ever looks at a sum. Absence of a bucket is invisible;
# there is no gap-shaped mark where a status should have been.
#
# The `unbucketed` return is the half that survives the NEXT status. Extending
# this map closes today's three; only reporting what fell through closes the
# ninth, which will be added by someone who has never read this file.
VELOCITY_BUCKETS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Accepted / shipped",
     ("executed", "approved", "approved-queued", "pre-ship", "partial-executed")),
    ("Deferred", ("deferred",)),
    ("Carried open", ("carried-open",)),
    ("Rejected", ("rejected",)),
)


def velocity_buckets(
    findings: list[dict[str, Any]],
) -> tuple[list[tuple[str, int, str]], dict[str, int]]:
    """Bucket findings by terminal status.

    Returns `(rows, unbucketed)` where rows is `[(label, count, detail)]` and
    `unbucketed` maps any status matching no bucket to its count. The second
    value is the contract: a status this map has never seen is RETURNED, never
    dropped, so the caller can publish it and the sum can be asserted.
    """
    by_status: dict[str, int] = {}
    for f in findings:
        s = f.get("status") or "unknown"
        by_status[s] = by_status.get(s, 0) + 1

    rows: list[tuple[str, int, str]] = []
    claimed: set[str] = set()
    for label, members in VELOCITY_BUCKETS:
        claimed.update(members)
        present = [(m, by_status[m]) for m in members if by_status.get(m)]
        # A multi-member bucket names its composition rather than absorbing it:
        # a cycle that is all `executed` and one that is all `pre-ship` are not
        # the same cycle, and the tile value alone cannot say which you have.
        detail = " · ".join(f"{n} {m}" for m, n in present) if len(members) > 1 else ""
        rows.append((label, sum(n for _, n in present), detail))

    return rows, {s: n for s, n in by_status.items() if s not in claimed}


def render_fam_dispatch_widget(fam: dict[str, Any]) -> str:
    """Render the fam-wide dispatch + reactions widget with sub-band split.

    The two sub-axes carry different units (dispatches vs reactions) and are
    rendered as labeled sub-bands so the unit-asymmetry is structurally legible.
    Rows with count=0 render with a muted CSS class (`kv-row-muted`) so absence
    reads as measurement signal — not "we forgot the row."
    """
    if not fam:
        return (
            "<p class='kv-row'><span class='kv-key'>"
            "(no fam activity recorded this cycle)</span></p>"
        )

    sub_bands = []

    def _render_sub_band(label: str, axis: dict[str, Any]) -> str:
        subagents = axis.get("subagents") or []
        total = axis.get("total")
        # Sort descending by count so highest-volume rails surface first
        rows_sorted = sorted(subagents, key=lambda r: -(r.get("count") or 0))
        rows_html = []
        for r in rows_sorted:
            name = html.escape(str(r.get("name", "—")))
            count = r.get("count") or 0
            role = html.escape(str(r.get("role", "")))
            detail = r.get("detail")
            muted = " kv-row-muted" if count == 0 else ""
            detail_html = (
                f'<span class="fam-row-detail">{html.escape(str(detail))}</span>'
                if detail else ""
            )
            rows_html.append(
                f'<div class="kv-row fam-row{muted}">'
                f'<span class="kv-key">{name}</span>'
                f'<span class="kv-val">{count}</span>'
                f'<span class="fam-row-role">{role}</span>'
                f'{detail_html}'
                f'</div>'
            )
        total_html = (
            f'<div class="kv-row fam-row-total">'
            f'<span class="kv-key">total</span>'
            f'<span class="kv-val">{total}</span>'
            f'</div>'
            if isinstance(total, int) else ""
        )
        return (
            f'<div class="fam-sub-band">'
            f'<h4 class="fam-sub-band-label">{html.escape(label)}</h4>'
            f'{"".join(rows_html)}'
            f'{total_html}'
            f'</div>'
        )

    if "dispatch_axis" in fam:
        sub_bands.append(_render_sub_band("Dispatch axis", fam["dispatch_axis"]))
    if "reactions_axis" in fam:
        sub_bands.append(_render_sub_band("Reactions axis", fam["reactions_axis"]))

    # p17 onward carries FLAT counts (`learning_agent: 1`) instead of the p16
    # axis-of-subagent-dicts shape. Neither vocabulary is wrong; the renderer
    # simply has to speak both, or a sidecar that HAS the data renders blank —
    # which is what shipped, and reads identically to "no dispatches happened".
    if not sub_bands:
        rows = [
            (k, v) for k, v in fam.items()
            if isinstance(v, int) and k not in ("cycle_window",)
        ]
        if rows:
            rows.sort(key=lambda kv: -kv[1])
            rows_html = "".join(
                f'<div class="kv-row fam-row{" kv-row-muted" if n == 0 else ""}">'
                f'<span class="kv-key">{html.escape(k.replace("_", " "))}</span>'
                f'<span class="kv-val">{n}</span></div>'
                for k, n in rows
            )
            total = sum(n for _, n in rows)
            # The cross-cycle comparability disclaimer that used to sit here is
            # REMOVED — operator decision 2026-08-02: "we only show the latest
            # metrics externally, no need to show the notes for prior reporting
            # periods." Its hazard is closed at the source instead: p17's four
            # buckets are lifted from `sidecar-metrics-tally.py`'s `role_buckets`
            # block, so the total is a measured figure rather than four zeros
            # needing a paragraph to explain them. Deleting it also deleted the
            # widget's only reason to hold a PRIOR sidecar — which it selected
            # positionally as `all_sidecars[-2]`, correct only while p17 was
            # last (§68: a deletion beats an index check that has to stay right).
            sub_bands.append(
                f'<div class="fam-sub-band">'
                f'<h4 class="fam-sub-band-label">Dispatch axis</h4>{rows_html}'
                f'<div class="kv-row fam-row-total"><span class="kv-key">total</span>'
                f'<span class="kv-val">{total}</span></div></div>'
            )

    if not sub_bands:
        return (
            "<p class='kv-row'><span class='kv-key'>"
            "(no fam activity recorded this cycle)</span></p>"
        )
    return "".join(sub_bands)


def load_all_sidecars(retros_dir: Path) -> list[dict[str, Any]]:
    """Load every `*.yaml` in the retros directory, sorted by retro_date.

    Used by the trend chart to render cross-cycle metrics. The
    single-retro snapshot (sprint-1) consumes one sidecar; this aggregator
    reads all of them so trend lines have an apples-to-apples axis when the
    measurement shape is stable.
    """
    sidecars: list[dict[str, Any]] = []
    for path in sorted(retros_dir.glob("*.yaml")):
        try:
            sidecars.append(load_sidecar(path))
        except (OSError, ValueError):
            continue
    sidecars.sort(key=lambda s: s.get("retro_date") or "")
    return sidecars


def _trend_sparkline_svg(
    values: list[float | int | None], height: int = 80, width: int = 960
) -> str:
    """Emit an inline SVG sparkline for a list of numeric trend points.

    None values render as gaps (no dot, line broken). Y-axis auto-scales
    against the min/max of present values. Always renders the full
    (width × height) viewBox so cards align even when a series has gaps.
    """
    pad_x, pad_y = 16, 10
    inner_w = width - 2 * pad_x
    inner_h = height - 2 * pad_y
    points = [v for v in values if isinstance(v, (int, float))]
    if not points or len(values) < 2:
        return f'<svg viewBox="0 0 {width} {height}" class="trend-svg" aria-hidden="true"><line x1="{pad_x}" y1="{height/2}" x2="{width-pad_x}" y2="{height/2}" stroke="var(--border)" stroke-width="1" stroke-dasharray="2,3"/></svg>'

    vmin, vmax = min(points), max(points)
    span = vmax - vmin if vmax > vmin else 1.0

    coords: list[tuple[float, float] | None] = []
    n = len(values)
    for i, v in enumerate(values):
        x = pad_x + (i * inner_w / (n - 1)) if n > 1 else width / 2
        if isinstance(v, (int, float)):
            y = pad_y + inner_h - ((v - vmin) / span * inner_h)
            coords.append((x, y))
        else:
            coords.append(None)

    # Build polyline segments (broken across None gaps)
    segments: list[str] = []
    current: list[str] = []
    for c in coords:
        if c is None:
            if len(current) >= 2:
                segments.append(" ".join(current))
            current = []
        else:
            current.append(f"{c[0]:.1f},{c[1]:.1f}")
    if len(current) >= 2:
        segments.append(" ".join(current))

    line_html = "".join(
        f'<polyline points="{seg}" fill="none" stroke="var(--accent)" stroke-width="2"/>'
        for seg in segments
    )
    dot_html = "".join(
        f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="3.5" fill="var(--accent)" />'
        for c in coords if c is not None
    )
    return f'<svg viewBox="0 0 {width} {height}" class="trend-svg" aria-hidden="true">{line_html}{dot_html}</svg>'


def _format_trend_value(v: float | int | None, suffix: str = "") -> str:
    """Format a single trend value (or em-dash for None)."""
    if v is None:
        return "—"
    if isinstance(v, float):
        if suffix == "%":
            return f"{v * 100:.0f}%"
        return f"{v:.1f}"
    return f"{v}{suffix}"


def _trend_scope_label(sidecars: list[dict[str, Any]]) -> str:
    """Say what the trend actually spans.

    The label used to read "n=15 P10 cycles", which was wrong twice. It leaked a
    protocol identifier into the published layer, and it implied the trend covers
    every cycle — it covers every cycle that emitted a sidecar, which starts at
    the third. A count is only a scope if you also say what it counts out of.
    """
    # Deduped: two sidecars sharing an ordinal made the contiguity check fire
    # with an EMPTY gap set, so the label ended in a dangling "· missing ".
    ordinals = sorted({
        int(m.group(1))
        for sc in sidecars
        if (m := re.search(r"p(\d+)$", str(sc.get("retro_id", ""))))
    })
    if not ordinals:
        return f"n={len(sidecars)}"
    lo, hi = ordinals[0], ordinals[-1]
    label = f"n={len(ordinals)} · retrospectives #{lo}–#{hi}"
    if lo > 1:
        earlier = f"#{lo - 1}" if lo == 2 else f"#1–#{lo - 1}"
        label += f" · {earlier} predate the sidecar"
    gaps = sorted(set(range(lo, hi + 1)) - set(ordinals))
    if gaps:
        label += f" · missing {', '.join(f'#{g}' for g in gaps)}"
    return label


def _coalesce(*values: Any) -> Any:
    """First non-None value. Used only where an overlap test has established
    that the fields are the same measurement under different names — never as a
    convenience for "whichever key happens to be there"."""
    for v in values:
        if v is not None:
            return v
    return None


def _trend_annotation(values: list[float | int | None], lower_is_better: bool = False) -> str:
    """Compare last two non-null values; emit directional + label."""
    present = [(i, v) for i, v in enumerate(values) if isinstance(v, (int, float))]
    if len(present) < 2:
        return ""
    _, prev = present[-2]
    _, last = present[-1]
    if last == prev:
        return '<span class="trend-flat">→ flat</span>'
    rising = last > prev
    if rising:
        return (
            '<span class="trend-down">↑ regression</span>' if lower_is_better
            else '<span class="trend-up">↑ accelerating</span>'
        )
    return (
        '<span class="trend-up">↓ improving</span>' if lower_is_better
        else '<span class="trend-down">↓ slowing</span>'
    )


def render_trend_chart(sidecars: list[dict[str, Any]]) -> str:
    """Sprint-2 multi-retro trend rendering. Honest at n=3.

    Each card carries a sparkline + the underlying values + a directional
    annotation comparing the last two cycles.

    ⛔ A CARD WHOSE FIELD STOPPED BEING REPORTED IS DECLARED CLOSED, NEVER
    SILENTLY GAPPED. Absence is not zero, and on a time series it is not a dip.

    ⛔ BUT THE CLOSE/RE-KEY TEST RUNS AGAINST THE SEMANTIC PREDECESSOR, NOT
    AGAINST THE NEW KEY'S OWN COVERAGE. Corrected 2026-08-02 after getting it
    wrong in the other direction. The first pass measured
    `fam_dispatch_distribution.learning_agent` at 1/15 and closed the
    learning-layer series — but 1/15 is what EVERY rename scores on the cycle it
    is introduced, so that test cannot distinguish a rename from a new metric. It
    always says "new".

    The test that discriminates is agreement in the overlap: for every cycle
    where both fields exist, do they carry the same number? Measured across p4-p16,
    `discipline_metrics.teacher_invocations` and the nested dispatch block's
    teacher count agree 13 times out of 13. Same measurement, renamed by the
    public-vocabulary scrub. So the series CONTINUES and is coalesced below.

    `checkpoint_bar_miss_rate` fails that same test and is genuinely closed —
    but not for drift. The metric was RETRACTED this cycle as miscomputed: it
    counted hook fires rather than turns. A retraction and a rename look
    identical from the field's absence alone, and they warrant opposite
    treatments, which is why each card states which one it is.
    """
    if len(sidecars) < 2:
        return (
            '<p class="trend-empty">'
            'Trend rendering activates at n≥2 sidecars; '
            f"{len(sidecars)} accumulated."
            "</p>"
        )

    labels = [str(sc.get("retro_id", "—")).split("-")[-1] for sc in sidecars]

    # `checkpoint_bar_miss_rate` is deliberately NOT read. The 16-cycle rate
    # series was retired from the page on 2026-08-02 by operator decision: the
    # rate was retracted as miscomputed, and a retracted series redrawn beside
    # its replacement invites the eye to read one slope across two units. The
    # values remain in the sidecars — this is a rendering decision, not a
    # deletion of record — and the REASON still renders, because points removed
    # without their reason are just a gap, which is the reading the closed-series
    # machinery exists to prevent.
    # Re-keyed 2026-08-02: `executed_this_cycle` covers 14/15 and dies at p17;
    # `authored_this_cycle` covers 15/15. This is a genuine re-key — the whole
    # series exists under the new field — so the label changes with it, because
    # authored and executed are different predicates.
    velocity_values: list[float | int | None] = [
        (sc.get("proposal_backlog") or {}).get("authored_this_cycle")
        for sc in sidecars
    ]
    # Coalesced, not grafted. See the docstring: these two keys agree in 13 of
    # 13 overlapping cycles, which is what licenses treating them as one series.
    teacher_values: list[float | int | None] = [
        _coalesce(
            (sc.get("discipline_metrics") or {}).get("teacher_invocations"),
            (sc.get("fam_dispatch_distribution") or {}).get("learning_agent"),
        )
        for sc in sidecars
    ]
    # The honest successor to the retracted rate: a COUNT of missed turns. New
    # series, n=1, and labelled as such rather than continuing the rate's line.
    missed_turn_values: list[float | int | None] = [
        (sc.get("discipline_metrics") or {}).get("response_marker_missed_turns")
        for sc in sidecars
    ]

    def _new_axis_card(
        title: str, unit_label: str, values: list[float | int | None],
        retired: str, note: str = "",
    ) -> str:
        """A card for a series that REPLACED a retired one, drawn alone.

        The predecessor's points are not redrawn beneath it. Two consequences
        are deliberate: a single point renders as a VALUE, not a trend — one
        observation has no slope and a sparkline drawn through it invents one —
        and the retraction sentence survives the removal of the data, because
        points deleted without their reason read as a gap rather than a
        decision. At n≥2 this upgrades to a line automatically, so the next
        cycle owes no code edit to get its trend back.
        """
        live = [(lab, v) for lab, v in zip(labels, values) if v is not None]
        n = len(live)
        if n == 1:
            lab, v = live[0]
            body = (
                '<div class="trend-stat">'
                f'<span class="trend-stat-value">{html.escape(_format_trend_value(v))}</span>'
                f'<span class="trend-stat-label">{html.escape(unit_label)} · {html.escape(lab)}</span>'
                '</div>'
            )
        elif n > 1:
            live_values = [v for _, v in live]
            body = (
                '<div class="trend-values">'
                + '<span class="trend-arrow">→</span>'.join(
                    f'<span class="trend-value">{html.escape(_format_trend_value(v))}</span>'
                    for v in live_values
                )
                + '</div>'
                + _trend_sparkline_svg(live_values)
                + '<div class="trend-axis-labels">'
                + "".join(
                    f'<span class="trend-axis-label">{html.escape(lab)}</span>'
                    for lab, _ in live
                )
                + '</div>'
            )
        else:
            body = '<p class="trend-empty">not yet measured on this axis</p>'
        return (
            '<div class="trend-card">'
            f'<h3>{html.escape(title)} '
            f'<span class="trend-card-suffix">{html.escape(unit_label)} · '
            f'new series · n={n}</span></h3>'
            f'{body}'
            f'<p class="trend-closed">{html.escape(retired)}</p>'
            + (f'<p class="trend-note">{html.escape(note)}</p>' if note else "")
            + '</div>'
        )

    def _card(
        title: str, suffix: str, values: list[float | int | None],
        value_format: str = "", lower_is_better: bool = False, note: str = "",
        closed_reason: str = "",
    ) -> str:
        value_strs = [_format_trend_value(v, value_format) for v in values]
        values_inline = (
            '<span class="trend-arrow">→</span>'.join(
                f'<span class="trend-value">{html.escape(s)}</span>' for s in value_strs
            )
        )
        axis_labels = "".join(
            f'<span class="trend-axis-label">{html.escape(l)}</span>' for l in labels
        )
        annotation = _trend_annotation(values, lower_is_better=lower_is_better)
        # Declare a closed series rather than letting the reader assume the
        # final gap is a bad cycle. Absence is not zero, and on a time series
        # it is not a dip either.
        last_live = max((i for i, v in enumerate(values) if v is not None), default=-1)
        if 0 <= last_live < len(values) - 1:
            suffix = f"series closed at {labels[last_live]}"
            # A closed series says WHY. "No longer reported" is the default
            # because drift is the common case, but a retraction is a different
            # event with a different remedy, and the reader cannot tell them
            # apart from the gap.
            annotation = (
                f'<span class="trend-closed">'
                f'{html.escape(closed_reason) if closed_reason else "no longer reported"} '
                f'after {html.escape(labels[last_live])}</span>'
            )
        note_html = (
            f'<p class="trend-note">{html.escape(note)}</p>' if note else ""
        )
        # The sub-line that drew a restarted series UNDER its closed predecessor
        # was removed 2026-08-02 with its only caller. The successor now gets its
        # own card (`_new_axis_card`) with no predecessor drawn at all — the
        # operator's call, and the stronger one: sharing a card kept two units
        # inside one frame, and a frame is exactly what a reader compares within.
        return (
            '<div class="trend-card">'
            f'<h3>{html.escape(title)} <span class="trend-card-suffix">{html.escape(suffix)}</span></h3>'
            f'<div class="trend-values">{values_inline}</div>'
            f'{_trend_sparkline_svg(values)}'
            f'<div class="trend-axis-labels">{axis_labels}</div>'
            f'<div class="trend-annotation">{annotation}</div>'
            f'{note_html}'
            '</div>'
        )

    cards = [
        _new_axis_card(
            "Checkpoint discipline", "missed turns", missed_turn_values,
            retired="The 16-cycle rate that preceded this axis was RETRACTED — "
                    "it counted hook fires, not turns, and no turn denominator "
                    "is derivable from the record. Its points are retired from "
                    "this page rather than redrawn beside a different unit; the "
                    "values remain in the sidecars.",
            note="A count of turns that shipped without the response marker — "
                 "what was actually measurable, in place of a ratio that was "
                 "not. One observation is a value, not a trend.",
        ),
        _card(
            "Proposal authoring", "proposals authored / cycle",
            velocity_values, value_format="",
        ),
        _card(
            "Learning-layer invocations", "learning-layer adoption",
            teacher_values, value_format="",
        ),
    ]

    return "".join(cards)


# ─── Health score (schema 1.1) ────────────────────────────────────────────────
#
# ⛔ DERIVED AT RENDER TIME, NEVER STORED. A composite written into a sidecar is
# stale the instant any input moves and nothing can tell you it did. If a sidecar
# ever grows a `health_score:` key, that is the bug, not this function.
#
# WHAT IS SCORED, AND WHY IT IS NOT THE DEFECT COUNT. A governance OS's job is to
# make failure visible and bounded, not to avoid it. Scoring the open-defect count
# would mean the number improves whenever detection stops working and falls every
# time an audit succeeds. So defects render as unscored INVENTORY, and what gets
# scored is the integrity of the loop that catches them.
#
# Four leading indicators (each guards one known failure mode, each actionable)
# plus one lagging outcome indicator. The leading four are individually gameable
# — a gate can be armed over nothing, a ritual can complete while checking
# nothing. The outcome dial is not gameable that way but is slow and, alone,
# would reward building many trivial controls. Either half without the other lies.

INTENDED_DIAL_COUNT = 5


def _dial(key: str, label: str, value: float | None, detail: str, note: str = "") -> dict[str, Any]:
    return {"key": key, "label": label, "value": value, "detail": detail, "note": note}


def compute_health(sc: dict[str, Any]) -> dict[str, Any]:
    """Derive the health dials + composite from a schema-1.1 sidecar.

    Returns dials (some with value None = no data), the composite over the
    dials that DO have data, and an explicit coverage statement. A composite
    computed over 4 of 5 dials is not the same claim as one computed over 5,
    and the difference is stated rather than left for the reader to assume.
    """
    dials: list[dict[str, Any]] = []

    # 1 — Enforcement coverage. Two components, deliberately: a gate that is
    # armed but carries no written condition for coming back OFF is half
    # governed. That is exactly how gates sat teeth-off for a month with
    # nobody able to say whether that was correct.
    ec = sc.get("enforcement_coverage") or {}
    built = ec.get("arms_built")
    armed = ec.get("arms_armed")
    exits = ec.get("arms_with_written_exit_criteria")
    if isinstance(built, int) and built > 0 and isinstance(armed, int):
        components = [armed / built]
        detail = f"{armed}/{built} arms armed"

        # The predicate is "states the condition under which its teeth come
        # OFF" — satisfied EITHER by a falsifiable exit criterion OR by a
        # documented declaration of permanence. Those are two different
        # properties and the published string names both, because "6/6 with a
        # written exit criterion" asserts of the permanent arm something that
        # is not true of it. Scoring them together is deliberate: marking a
        # documented permanence as a MISS would make inventing a fictional
        # exit criterion the score-maximising move, which is the exact defect
        # the arms file was written to prevent. The defect being repaired is
        # SILENCE, not the absence of an exit.
        if isinstance(exits, int):
            components.append(exits / built)
            falsifiable = ec.get("arms_with_falsifiable_exit")
            permanent = ec.get("arms_declared_permanent")
            detail += f" · {exits}/{built} state an exit condition"
            if isinstance(falsifiable, int) and isinstance(permanent, int):
                detail += f" ({falsifiable} falsifiable · {permanent} documented permanence)"

        # Third component, added the same day the first two hit ceiling. An arm
        # is a hook; a CHECK is one invariant inside it. Arm-level coverage
        # reaching 6/6 while 22 individual checks state nothing is not "fully
        # governed" — it is a dial that stopped discriminating at the resolution
        # it happened to be defined at. Granularity is a property of the metric,
        # not of the system.
        checks = ec.get("checks_enumerated")
        checks_exits = ec.get("checks_with_written_exit_criteria")
        if isinstance(checks, int) and checks > 0 and isinstance(checks_exits, int):
            components.append(checks_exits / checks)
            unit = ec.get("checks_unit", "blocking exit paths")
            detail += f" · {checks_exits}/{checks} individual checks with one"

        note = (
            "Coverage is measured per ARM and again per CHECK. Arm-level "
            "coverage is complete; check-level coverage is zero — the "
            "commit-time arm holds many individually-retirable checks and not "
            "one states its own exit condition. That is the honest reading of "
            "this dial."
        )
        if isinstance(checks, int):
            note += f" Check unit: {unit}."
        basis = ec.get("measured_from")
        if basis:
            note += f" Basis: {basis}."
        dials.append(_dial(
            "enforcement", "Enforcement coverage",
            sum(components) / len(components), detail, note,
        ))
    else:
        dials.append(_dial("enforcement", "Enforcement coverage", None, "no data"))

    # 2 — Ritual integrity. Absorbs close discipline: P9 close is a ritual step,
    # so scoring it separately would double-count it.
    dm = sc.get("discipline_metrics") or {}
    defined = dm.get("ritual_steps_defined")
    completed = dm.get("ritual_steps_completed")
    if isinstance(defined, int) and defined > 0 and isinstance(completed, int):
        val = completed / defined
        sub_due = dm.get("monthly_subritual_due")
        sub_done = dm.get("monthly_subritual_completed")
        detail = f"{completed}/{defined} steps"
        if sub_due:
            detail += f" · monthly sub-ritual {'completed' if sub_done else 'DUE, not run'}"
            if not sub_done:
                val = min(val, 0.5)
        dials.append(_dial("ritual", "Ritual integrity", val, detail,
                           "Self-attested by the session that ran the ritual. "
                           "Includes session-close discipline, which is one of "
                           "the ritual steps rather than a separate score."))
    else:
        dials.append(_dial("ritual", "Ritual integrity", None, "no data"))

    # 3 — Instrument liveness. Scores the LOOP, not the absence of failure:
    # "when an instrument lied, did something catch it". The absolute failure
    # count rides alongside unnormalised — no denominator has been invented.
    il = sc.get("instrument_liveness") or {}
    observed = il.get("silent_failures_observed")
    caught = il.get("caught_by_control")
    if isinstance(observed, int) and isinstance(caught, int):
        val = 1.0 if observed == 0 else caught / observed
        dials.append(_dial(
            "instrument", "Instrument liveness", val,
            f"{caught}/{observed} silent failures caught by a control · "
            f"{il.get('caught_by_review', 0)} by review",
            "Self-attested. Full dial with a high failure count is the correct "
            "reading: the loop held. The count is shown unnormalised. The "
            "dial's failing arm is a failure caught by REVIEW rather than by "
            "an instrument, which scores zero. Its blind spot is stated "
            "rather than scored: a silent failure that nothing caught at all "
            "is never observed, so it enters neither term.",
        ))
    else:
        dials.append(_dial("instrument", "Instrument liveness", None, "no data"))

    # 4 — Quality gate.
    sampled = dm.get("quality_gate_traces_sampled")
    passing = dm.get("quality_gate_traces_passing")
    if isinstance(sampled, int) and sampled > 0 and isinstance(passing, int):
        dials.append(_dial("quality", "Quality gate", passing / sampled,
                           f"{passing}/{sampled} traces passing",
                           f"Small n ({sampled}); a sampled rate, not a census."))
    else:
        dials.append(_dial("quality", "Quality gate", None, "no data"))

    # 5 — Detection provenance (lagging outcome). Ships empty on purpose;
    # it cannot be backfilled, because reconstructing who would have caught a
    # past defect is fabrication rather than measurement.
    dp = sc.get("detection_provenance") or {}
    by_control = dp.get("caught_by_control")
    by_operator = dp.get("caught_by_operator")
    if isinstance(by_control, int) and isinstance(by_operator, int) and (by_control + by_operator) > 0:
        by_accident = dp.get("caught_by_accident")
        total = by_control + by_operator + (by_accident if isinstance(by_accident, int) else 0)
        dials.append(_dial("provenance", "Detection provenance", by_control / total,
                           f"{by_control} caught by a control · {by_operator} by the operator"))
    else:
        dials.append(_dial(
            "provenance", "Detection provenance", None,
            f"awaiting data — instrumented from {dp.get('instrumented_from', 'a future cycle')}",
            "The outcome metric: did a control catch it, or did the operator? "
            "Cannot be backfilled without fabricating attributions.",
        ))

    scored = [d for d in dials if isinstance(d["value"], (int, float))]
    composite = round(100 * sum(d["value"] for d in scored) / len(scored)) if scored else None
    return {
        "dials": dials,
        "composite": composite,
        "scored_count": len(scored),
        "intended_count": INTENDED_DIAL_COUNT,
    }


def _bar(value: float | None, width: int = 10) -> str:
    """Render a fixed-width proportion bar. None renders as an empty track."""
    if not isinstance(value, (int, float)):
        return f'<span class="hs-bar hs-bar-empty">{"·" * width}</span>'
    filled = int(round(value * width))
    return (
        f'<span class="hs-bar">'
        f'<span class="hs-bar-fill">{"█" * filled}</span>'
        f'<span class="hs-bar-track">{"░" * (width - filled)}</span></span>'
    )


def render_health_widget(health: dict[str, Any]) -> str:
    composite = health["composite"]
    rows = []
    for d in health["dials"]:
        val = d["value"]
        pct = f"{round(val * 100)}" if isinstance(val, (int, float)) else "—"
        note = f'<div class="hs-note">{html.escape(d["note"])}</div>' if d.get("note") else ""
        rows.append(f"""
        <div class="hs-row{'' if isinstance(val, (int, float)) else ' hs-row-pending'}">
          <div class="hs-label">{html.escape(d["label"])}</div>
          <div class="hs-meter">{_bar(val)}</div>
          <div class="hs-pct">{pct}</div>
          <div class="hs-detail">{html.escape(d["detail"])}{note}</div>
        </div>""")
    coverage = (
        f'Composite derived from {health["scored_count"]} of {health["intended_count"]} '
        f'intended dials — an unweighted mean over ratios with different '
        f'denominators and different evidentiary grades. It is an average of '
        f'what could be measured, not of what matters.'
    )
    # This paragraph used to live in a Python comment, where it was the
    # strongest sentence in the design and reached no reader. A caveat in the
    # stripped layer is a caveat the author and the approver both read and the
    # audience never does.
    gameable = (
        "All four scored dials are LEADING indicators and each is individually "
        "gameable — a gate can be armed over nothing, a ritual can complete "
        "while checking nothing. The one OUTCOME dial, which is not gameable "
        "that way, is the one with no data. A high score here means four "
        "leading indicators are saturated; it is not a claim that the system "
        "is working."
    )
    return f"""
      <div class="hs-headline">
        <div class="hs-score">{composite if composite is not None else "—"}<span class="hs-score-max">/100</span></div>
        <div class="hs-score-caption">
          <strong>Derived at render, never stored.</strong>
          {html.escape(coverage)}
        </div>
      </div>
      <p class="hs-caveat">{html.escape(gameable)}</p>
      <div class="hs-rows">{"".join(rows)}</div>
      <p class="hs-foot">
        The open-defect count is deliberately absent from this score. A governance system
        scored on defect count improves whenever detection stops working, and falls every
        time an audit succeeds. Defects appear below as inventory.
      </p>"""


def render_defect_inventory(dl: dict[str, Any]) -> str:
    if not dl:
        return '<p class="empty-note">No defect ledger in this sidecar.</p>'
    total = dl.get("open_total")
    # NEVER `or 0` here. A bucket the sidecar did not record is UNKNOWN, and
    # rendering it as 0 publishes a measurement nobody made. A recorded zero
    # still renders "0" — absence and zero are different claims.
    buckets = [
        ("< 7 days", dl.get("age_under_7d")),
        ("7–29 days", dl.get("age_7_to_29d")),
        ("30+ days", dl.get("age_30d_plus")),
        ("undated", dl.get("age_undated")),
    ]
    known = [n for _, n in buckets if isinstance(n, int)]
    peak = max(known + [1])
    bar_rows = "".join(
        f'<div class="inv-row"><span class="inv-key">{html.escape(label)}</span>'
        f'<span class="inv-bar">'
        f'{"█" * max(0, round(n / peak * 18)) if isinstance(n, int) else ""}</span>'
        f'<span class="inv-n">{_present(n)}</span></div>'
        for label, n in buckets
    )
    return f"""
      <div class="inv-head">
        <span class="inv-total">{_present(total)}</span>
        <span class="inv-total-label">open as measured · <strong>not scored</strong></span>
        <span class="inv-split">{_present(dl.get("live"))} live · {_present(dl.get("parked"))} parked</span>
      </div>
      <div class="inv-bars">{bar_rows}</div>
      <div class="inv-foot">
        median age <strong>{_present(dl.get("median_age_days"))}d</strong> ·
        oldest <strong>{_present(dl.get("max_age_days"))}d</strong> —
        the age distribution is the diagnostic here, not the total.
        Measured {html.escape(str(dl.get("measured_at", "—")))} — a stamped
        record of that state, not a current count. The board moved during the
        session that measured it.
        {f'Basis: {html.escape(str(dl.get("measured_from")))}.' if dl.get("measured_from") else ""}
      </div>"""


def render_backlog_widget(bl: dict[str, Any], pb: dict[str, Any] | None = None) -> str:
    """Improvement backlog, plus this cycle's proposal flow.

    The 5-stage cohort funnel was retired 2026-08-02: three of its stages
    (`pending_before_retro`, `approved_not_executed`, `executed_this_cycle`)
    stopped being reported at p17, leaving a funnel that rendered two figures
    and three dashes. The two surviving figures are folded in here rather than
    dropped — retiring a WIDGET must not silently retire its DATA.
    """
    if not bl:
        return '<p class="empty-note">No improvement backlog in this sidecar.</p>'
    axes = [
        ("ready", bl.get("open_ready")),
        ("decision-gated", bl.get("open_decision_gated")),
        ("upstream-blocked", bl.get("open_upstream_blocked")),
    ]
    open_n = bl.get("open")
    # A missing axis must NEVER be summed as zero. A sum over an incomplete
    # set can coincidentally equal the open total and publish a reconciliation
    # that passed only because a value was absent — the reconciliation would
    # then be evidence for exactly the thing it failed to check.
    if any(not isinstance(n, int) for _, n in axes):
        reconcile = "axes incomplete — one or more scheduling values were not recorded"
    else:
        axis_sum = sum(n for _, n in axes)
        reconcile = (
            f"axes sum to {axis_sum}, open total {_present(open_n)}"
            + ("" if axis_sum == open_n else " — MISMATCH: an item carries an unrecognised status")
        )
    chips = "".join(
        f'<span class="bk-chip"><span class="bk-chip-n">{_present(n)}</span>{html.escape(label)}</span>'
        for label, n in axes
    )
    pb = pb or {}
    flow = [("authored", pb.get("authored_this_cycle")), ("deferred", pb.get("deferred_this_cycle"))]
    flow_html = (
        '<div class="bk-flow"><span class="bk-flow-label">this cycle</span>'
        + "".join(
            f'<span class="bk-chip"><span class="bk-chip-n">{_present(n)}</span>{html.escape(lbl)}</span>'
            for lbl, n in flow
        )
        + "</div>"
    ) if any(v is not None for _, v in flow) else ""
    return f"""
      <div class="bk-head">
        <span class="bk-total">{bl.get("total", "—")}</span>
        <span class="bk-total-label">proposed improvements — lifetime</span>
      </div>
      <div class="bk-split">
        <span>{bl.get("done", "—")} done</span><span>{open_n if open_n is not None else "—"} open</span><span>{bl.get("parked", "—")} parked</span>
      </div>
      <div class="bk-axes">{chips}</div>
      {flow_html}
      <div class="bk-foot">
        Scheduling axis is a <strong>derived</strong> view — an item whose status carries an
        unrecognised value is dropped from it silently, so these are a claim about what
        classified, never about what exists. Reconciled: {html.escape(reconcile)}.
      </div>"""


def render_dashboard(sc: dict[str, Any], all_sidecars: list[dict[str, Any]] | None = None) -> str:
    findings = sc.get("findings", []) or []
    backlog = sc.get("proposal_backlog", {}) or {}
    discipline = sc.get("discipline_metrics", {}) or {}
    latency = sc.get("latency_observations", {}) or {}
    # `meta_finding` changed shape between sidecar generations: a dict carrying a
    # `headline` key in p3–p16, a bare block-scalar string from p17 on. The
    # renderer assumed dict and raised AttributeError on p17, which is why that
    # sidecar had never rendered and index.html was still the p16 build. Accept
    # both rather than migrating 15 historical files — a reader of an old sidecar
    # should still get the old page.
    meta_raw = sc.get("meta_finding") or {}
    if isinstance(meta_raw, str):
        meta_text = meta_raw.strip()
    elif isinstance(meta_raw, dict):
        meta_text = str(meta_raw.get("headline", "") or "").strip()
    else:
        meta_text = ""

    # Counts. Bucketing lives in `velocity_buckets` so the residual — statuses
    # matching no bucket — is a returned value the page can publish, rather than
    # the silent subtraction that ran here for three months.
    total_findings = len(findings)
    velocity_rows, velocity_unbucketed = velocity_buckets(findings)
    velocity_tiles = "".join(
        render_tile(n, label, detail or None) for label, n, detail in velocity_rows
    )
    if velocity_unbucketed:
        velocity_tiles += render_tile(
            sum(velocity_unbucketed.values()),
            "Unbucketed status",
            " · ".join(f"{n} {s}" for s, n in sorted(velocity_unbucketed.items())),
        )
    # Printed so a reader can check the arithmetic without opening the yaml.
    # The two figures agree by construction now; publishing them is what makes
    # the next disagreement visible on the surface where it would occur.
    velocity_sum = (
        sum(n for _, n, _ in velocity_rows) + sum(velocity_unbucketed.values())
    )

    # `checkpoint_bar_miss_rate` and its prior-session sibling were read into
    # four locals here and interpolated nowhere — dead since the discipline
    # widget was retired. Deleted 2026-08-02 rather than left for a reader to
    # mistake for a live metric.

    # Latency — pre-format with graceful "—" suppression for null/redacted values
    # (sidecars redact discipline_metrics + latency_observations to null when traceable
    # to specific session windows; the renderer must not crash on `:.0f` against None).
    latency_median = latency.get("median_first_tool_latency_sec")
    latency_p95 = latency.get("p95_first_tool_latency_sec")
    latency_max = latency.get("max_first_tool_latency_sec")
    latency_violations = latency.get("threshold_violations")
    latency_median_str = f"{latency_median:.0f}s" if isinstance(latency_median, (int, float)) else "—"
    latency_p95_str = f"{latency_p95:.0f}s" if isinstance(latency_p95, (int, float)) else "—"
    latency_max_str = f"{latency_max:.0f}s" if isinstance(latency_max, (int, float)) else "—"
    latency_violations_str = str(latency_violations) if latency_violations is not None else "—"
    # Publish the band only when the sidecar actually carries latency keys.
    # Six em-dashes under a "Violations (>120s)" heading reads as a measured
    # clean sheet; it is an absent instrument.
    latency_has_data = any(
        latency.get(k) is not None
        for k in ("source", "sessions_in_window", "median_first_tool_latency_sec",
                  "p95_first_tool_latency_sec", "max_first_tool_latency_sec",
                  "threshold_violations")
    )
    latency_window_str = str(latency.get("window_session_count")) if latency.get("window_session_count") is not None else "—"

    health = compute_health(sc)
    health_html = render_health_widget(health)
    inventory_html = render_defect_inventory(sc.get("defect_ledger") or {})
    backlog_html = render_backlog_widget(sc.get("improvement_backlog") or {}, sc.get("proposal_backlog") or {})

    findings_rows_html = "".join(render_finding_row(f) for f in findings)
    fam_dispatch = sc.get("fam_dispatch_distribution") or {}
    fam_dispatch_html = render_fam_dispatch_widget(fam_dispatch)
    trend_html = render_trend_chart(all_sidecars or [sc])
    trend_section_html = (
        f"""
    <section>
      <h2 class="section-title">Governance trend <span class="section-title-suffix">{_trend_scope_label(all_sidecars or [sc])}</span></h2>
      <div class="trend-grid">
        {trend_html}
      </div>
    </section>
    """
        if all_sidecars and len(all_sidecars) >= 2 else ""
    )

    body = f"""
    <header class="hero">
      <div class="hero-eyebrow">Rozzzsie Governance Dashboard</div>
      <h1>Retrospective #{sc.get("retro_id", "—")}</h1>
      <p class="hero-tagline">Evaluation as continuous governing function, not terminal checkpoint.</p>
      <div class="hero-meta">
        <div><strong>Window</strong> {html.escape(str(sc.get("window_start", "—")))} → {html.escape(str(sc.get("window_end", "—")))}</div>
        <div><strong>Mode</strong> {"interactive" if sc.get("interactive_mode") else "non-interactive"}</div>
        <div><strong>Trigger</strong> {html.escape(str(sc.get("trigger_source", "—")))}</div>
        <div><strong>Schema</strong> v{html.escape(str(sc.get("schema_version", "—")))}</div>
      </div>
      <p class="hero-context">
        Governance health metrics from the most recent weekly retrospective in the Rozzzsie OS.
        Same shape as LangSmith / Langfuse / DashChat dashboards (quantitative metrics on a temporal axis);
        different semantics — governance evolution, not service telemetry.
        Measurement surface — what fired and how often, not what each rail is for.
      </p>
    </header>

    <section class="hs-section">
      <h2 class="section-title">Governance health <span class="section-title-suffix">integrity of the loop that catches failure — not the absence of failure</span></h2>
      <div class="hs-widget">
        {health_html}
      </div>
    </section>

    <section>
      <h2 class="section-title">Known defects <span class="section-title-suffix">inventory · deliberately unscored</span></h2>
      <div class="bands">
        <div class="band">
          <h3>Defect ledger</h3>
          {inventory_html}
        </div>
        <div class="band">
          <h3>Improvement backlog</h3>
          {backlog_html}
        </div>
      </div>
    </section>

    <section>
      <h2 class="section-title">Decision velocity <span class="section-title-suffix">findings triaged + terminal status assigned</span></h2>
      <div class="tiles">
        {render_tile(total_findings, "Findings triaged")}
        {velocity_tiles}
      </div>
      <p class="velocity-reconcile">buckets sum to {velocity_sum} · {total_findings} findings triaged</p>
    </section>
    {trend_section_html}

    <section>
      <h2 class="section-title">Specialist agent dispatches <span class="section-title-suffix">across specialist agents, this cycle</span></h2>
      <div class="fam-widget">
        {fam_dispatch_html}
      </div>
    </section>


    <section>
      <h2 class="section-title">Findings detail <span class="section-title-suffix">{len(findings)} items, every one statused</span></h2>
      <div class="findings">
        <div class="findings-row header">
          <div>id</div>
          <div>title</div>
          <div>status</div>
          <div>category</div>
        </div>
        {findings_rows_html}
      </div>

      {f'''
      <div class="callout">
        <div class="callout-icon" aria-hidden="true">◆</div>
        <div class="callout-body">
          <div class="callout-eyebrow">Meta-finding</div>
          <div class="callout-text">{html.escape(meta_text)}</div>
        </div>
      </div>
      ''' if meta_text else ""}
    </section>

    <footer class="scope-honest">
      <p>
        Dashboard v{DASHBOARD_VERSION}
        <span class="sep">·</span> Schema v{html.escape(str(sc.get("schema_version", "—")))}
        <span class="sep">·</span> <a href="https://arxiv.org/abs/2411.13768">EDD 2024</a>
        <span class="sep">·</span> <a href="https://github.com/Rozzzsie/Rozzzsie/tree/main/dashboard">Source</a>
        <span class="sep">·</span> <a href="https://github.com/Rozzzsie/Rozzzsie/tree/main/dashboard#readme">About</a>
      </p>
    </footer>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rozzzsie Governance Dashboard — Retrospective {html.escape(str(sc.get("retro_id", "")))}</title>
  <link rel="stylesheet" href="assets/dashboard.css">
</head>
<body>
  <main class="container">
{body}
  </main>
</body>
</html>
"""


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent
    # Retargeted every cycle at P10 step 9(c). Verify by running this file
    # with NO arguments and reading the header: found stale at p17, where
    # the documented bare command rendered the PREVIOUS cycle silently.
    default_sidecar = here.parent / "retros" / "2026-08-09-p18.yaml"
    default_out = here / "index.html"

    sidecar = Path(argv[1]) if len(argv) > 1 else default_sidecar
    out = Path(argv[2]) if len(argv) > 2 else default_out

    if not sidecar.exists():
        print(f"sidecar not found: {sidecar}", file=sys.stderr)
        return 2

    sc = load_sidecar(sidecar)

    # Validate BEFORE rendering. A blank widget is the failure mode this
    # guards, so producing the page and then complaining defeats the point.
    try:
        for warning in validate_sidecar(sc):
            print(f"schema: WARN  {warning}", file=sys.stderr)
    except SidecarSchemaError as exc:
        print(f"schema: FAIL  {exc}", file=sys.stderr)
        return 3

    retros_dir = sidecar.parent
    all_sidecars = load_all_sidecars(retros_dir)
    html_out = render_dashboard(sc, all_sidecars=all_sidecars)
    out.write_text(html_out, encoding="utf-8")
    # Display path robustly: a relative `out` arg (e.g. the README's documented
    # `render.py <sidecar> index.html`) isn't a subpath of `here.parent`, so
    # `relative_to` would raise AFTER the write already succeeded — a false
    # exit-1 on a good render. Resolve first; fall back to the raw path.
    try:
        out_display: Any = out.resolve().relative_to(here.parent)
    except ValueError:
        out_display = out
    print(
        f"rendered {sidecar.name} → {out_display} "
        f"(trend: n={len(all_sidecars)} sidecars)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
