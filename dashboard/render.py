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
# extension). Major bumps reserved for sprint-2 (multi-retro trend rendering)
# and beyond. Consistent-with-spine semver, mirrors `agent-protocols-X.Y.Z.md`.
DASHBOARD_VERSION = "2.0"


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
    nested dicts (luma_tally_by_category etc.), strings (quoted/unquoted),
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


# ─── Renderers ────────────────────────────────────────────────────────────────

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


def render_tally(tally: dict[str, Any]) -> str:
    if not tally:
        return "<p class='kv-row'><span class='kv-key'>(no data)</span></p>"
    # Null-vs-measured-zero contract: distinguish "unmeasured this cycle" (total
    # null AND no concrete int categories — categorization requires human-distilled
    # Luma-output narrative review) from "measured zero" (concrete int values
    # totaling 0). Same shape as the discipline-counter null suppression.
    total_raw = tally.get("total")
    int_values = [v for k, v in tally.items() if isinstance(v, int) and k != "total"]
    if total_raw is None and not int_values:
        return "<p class='kv-row'><span class='kv-key'>(unmeasured this cycle)</span></p>"
    total = total_raw if isinstance(total_raw, int) else sum(int_values)
    if total == 0:
        return "<p class='kv-row'><span class='kv-key'>(no invocations this window)</span></p>"
    rows = []
    for key, count in tally.items():
        if key == "total" or not isinstance(count, int) or count == 0:
            continue
        pct = (count / total) * 100 if total else 0
        rows.append(
            f"""
        <div class="tally-row">
          <div class="tally-label">{html.escape(key.replace("_", "-"))}</div>
          <div class="tally-bar"><div class="tally-fill" style="width: {pct:.1f}%"></div></div>
          <div class="tally-count">{count}</div>
        </div>
        """
        )
    # total > 0 but no measured categories — scalar known, breakdown is human-distilled
    # review work, not auto-extracted telemetry. Empty-state copy makes the structural
    # reality legible (per Rosie's pick 2026-05-04 from the four-candidate set).
    if not rows:
        return (
            f"<p class='kv-row'><span class='kv-key'>{total} invocations this cycle</span></p>"
            f"<p class='kv-row kv-row-detail'><span class='kv-key'>"
            f"Per-axis bars populate when narrative review runs — categorization isn't "
            f"auto-extracted from transcripts</span></p>"
        )
    return "".join(rows)


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

    return "".join(sub_bands)


def load_all_sidecars(retros_dir: Path) -> list[dict[str, Any]]:
    """Load every `*.yaml` in the retros directory, sorted by retro_date.

    Used by the trend chart (sprint-2) to render cross-cycle metrics. The
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


def _trend_sparkline_svg(values: list[float | int | None], height: int = 60, width: int = 240) -> str:
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

    Three metric cards: checkpoint miss rate, decision velocity (executed
    findings per cycle), Teacher invocations. Each card carries a 3-point
    sparkline + the underlying values + a directional annotation comparing
    the last two cycles. Apples-to-apples caveat for miss rate documented
    inline (p3 measured this-retro-session, p4/p5 measure cycle-window).
    """
    if len(sidecars) < 2:
        return (
            '<p class="trend-empty">'
            'Trend rendering activates at n≥2 sidecars; '
            f"{len(sidecars)} accumulated."
            "</p>"
        )

    labels = [str(sc.get("retro_id", "—")).split("-")[-1] for sc in sidecars]

    miss_values: list[float | int | None] = [
        (sc.get("discipline_metrics") or {}).get("checkpoint_bar_miss_rate")
        for sc in sidecars
    ]
    velocity_values: list[float | int | None] = [
        (sc.get("proposal_backlog") or {}).get("executed_this_cycle")
        for sc in sidecars
    ]
    teacher_values: list[float | int | None] = [
        (sc.get("discipline_metrics") or {}).get("teacher_invocations")
        for sc in sidecars
    ]

    def _card(
        title: str, suffix: str, values: list[float | int | None],
        value_format: str = "", lower_is_better: bool = False, note: str = "",
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
        note_html = (
            f'<p class="trend-note">{html.escape(note)}</p>' if note else ""
        )
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
        _card(
            "Checkpoint miss rate", "lower is better",
            miss_values, value_format="%", lower_is_better=True,
            note="p3 measured this-retro-session; p4/p5 measure cycle-window. "
                 "Strict cross-cycle apples-to-apples lands at p6 (window-shape stable since p4).",
        ),
        _card(
            "Decision velocity", "executed findings / cycle",
            velocity_values, value_format="",
        ),
        _card(
            "Teacher invocations", "learning-layer adoption",
            teacher_values, value_format="",
        ),
    ]

    return "".join(cards)


def render_dashboard(sc: dict[str, Any], all_sidecars: list[dict[str, Any]] | None = None) -> str:
    findings = sc.get("findings", []) or []
    backlog = sc.get("proposal_backlog", {}) or {}
    discipline = sc.get("discipline_metrics", {}) or {}
    latency = sc.get("latency_observations", {}) or {}
    meta = sc.get("meta_finding", {}) or {}

    # Counts
    by_status: dict[str, int] = {}
    for f in findings:
        s = f.get("status") or "unknown"
        by_status[s] = by_status.get(s, 0) + 1

    total_findings = len(findings)
    accepted = (
        by_status.get("approved", 0)
        + by_status.get("executed", 0)
        + by_status.get("pre-ship", 0)
    )
    deferred = by_status.get("deferred", 0)

    miss_rate = discipline.get("checkpoint_bar_miss_rate")
    prior_miss = discipline.get("checkpoint_bar_prior_session_rate")
    miss_pct = f"{miss_rate * 100:.0f}%" if isinstance(miss_rate, (int, float)) else "—"
    miss_detail = (
        f"Prior session: {prior_miss * 100:.0f}%"
        if isinstance(prior_miss, (int, float))
        else None
    )

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
    latency_window_str = str(latency.get("window_session_count")) if latency.get("window_session_count") is not None else "—"

    findings_rows_html = "".join(render_finding_row(f) for f in findings)
    tally_html = render_tally(discipline.get("luma_tally_by_category") or {})
    fam_dispatch = sc.get("fam_dispatch_distribution") or {}
    fam_dispatch_html = render_fam_dispatch_widget(fam_dispatch)
    trend_html = render_trend_chart(all_sidecars or [sc])
    trend_section_html = (
        f"""
    <section>
      <h2 class="section-title">Governance trend <span class="section-title-suffix">sprint-2 · n={len(all_sidecars or [sc])} P10 cycles</span></h2>
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
      <h1>P10 Retro #{sc.get("retro_id", "—")}</h1>
      <p class="hero-tagline">Evaluation as continuous governing function, not terminal checkpoint.</p>
      <div class="hero-meta">
        <div><strong>Window</strong> {html.escape(str(sc.get("window_start", "—")))} → {html.escape(str(sc.get("window_end", "—")))}</div>
        <div><strong>Mode</strong> {"interactive" if sc.get("interactive_mode") else "non-interactive"}</div>
        <div><strong>Trigger</strong> {html.escape(str(sc.get("trigger_source", "—")))}</div>
        <div><strong>Schema</strong> v{html.escape(str(sc.get("schema_version", "—")))}</div>
      </div>
      <p class="hero-context">
        Governance health metrics from the most recent P10 weekly retrospective in the Rozzzsie OS.
        Same shape as LangSmith / Langfuse / DashChat dashboards (quantitative metrics on a temporal axis);
        different semantics — governance evolution, not service telemetry.
        Measurement surface — what fired and how often, not what each rail is for.
      </p>
    </header>

    <section>
      <h2 class="section-title">Decision velocity <span class="section-title-suffix">findings triaged + terminal status assigned</span></h2>
      <div class="tiles">
        {render_tile(total_findings, "Findings triaged")}
        {render_tile(accepted, "Accepted / shipped", f"{by_status.get('executed', 0)} executed · {by_status.get('approved', 0)} approved · {by_status.get('pre-ship', 0)} pre-ship")}
        {render_tile(deferred, "Deferred", "Each with explicit watch entry or carry-forward")}
        {render_tile(by_status.get("rejected", 0), "Rejected")}
      </div>
    </section>

    <section>
      <h2 class="section-title">Specialist agent dispatches <span class="section-title-suffix">fam-wide activity, this cycle</span></h2>
      <div class="fam-widget">
        {fam_dispatch_html}
      </div>
    </section>

    <section>
      <h2 class="section-title">Discipline <span class="section-title-suffix">governance health under load</span></h2>
      <div class="bands">
        <div class="band">
          <h3>Discipline metrics</h3>
          <div class="kv-row">
            <span class="kv-key">Current checkpoint miss rate</span>
            <span class="kv-val">{miss_pct}</span>
          </div>
          {f'<div class="kv-row"><span class="kv-key">Prior session</span><span class="kv-val">{prior_miss * 100:.0f}%</span></div>' if isinstance(prior_miss, (int, float)) else ""}
        </div>
        <div class="band band-muted">
          <h3>Luma reframe-axis facet <span class="band-title-suffix">deep-dive · narrative-review-pending</span></h3>
          <div class="tally">
            {tally_html}
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2 class="section-title">Proposal backlog cohort <span class="section-title-suffix">authoring → approval → execution flow</span></h2>
      <div class="bands">
        <div class="band">
          <h3>This cycle</h3>
          <div class="cohort">
            <div class="cohort-stage"><span class="cohort-label">Pending before retro</span><span class="cohort-count">{backlog.get("pending_before_retro", 0)}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Approved (not yet executed)</span><span class="cohort-count">{backlog.get("approved_not_executed", 0)}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Executed this cycle</span><span class="cohort-count">{backlog.get("executed_this_cycle", 0)}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Authored this cycle</span><span class="cohort-count">{backlog.get("authored_this_cycle", 0)}</span></div>
          </div>
        </div>
        <div class="band">
          <h3>Latency observations</h3>
          <div class="kv-row">
            <span class="kv-key">Source</span>
            <span class="kv-val kv-val-mono">{html.escape(str(latency.get("source", "—")))}</span>
          </div>
          <div class="kv-row">
            <span class="kv-key">Sessions in window</span>
            <span class="kv-val">{latency_window_str}</span>
          </div>
          <div class="kv-row">
            <span class="kv-key">Median first-tool latency</span>
            <span class="kv-val">{latency_median_str}</span>
          </div>
          <div class="kv-row">
            <span class="kv-key">P95</span>
            <span class="kv-val">{latency_p95_str}</span>
          </div>
          <div class="kv-row">
            <span class="kv-key">Max</span>
            <span class="kv-val">{latency_max_str}</span>
          </div>
          <div class="kv-row">
            <span class="kv-key">Violations (&gt;120s)</span>
            <span class="kv-val">{latency_violations_str}</span>
          </div>
        </div>
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
          <div class="callout-text">{html.escape(str(meta.get("headline", "")))}</div>
        </div>
      </div>
      ''' if meta.get("headline") else ""}
    </section>
    {trend_section_html}

    <footer class="scope-honest">
      <p>
        Dashboard v{DASHBOARD_VERSION}
        <span class="sep">·</span> Schema v{html.escape(str(sc.get("schema_version", "—")))}
        <span class="sep">·</span> Rozzzsie OS v3.10.4
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
  <title>Rozzzsie Governance Dashboard — P10 {html.escape(str(sc.get("retro_id", "")))}</title>
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
    default_sidecar = here.parent / "retros" / "2026-05-10-p5.yaml"
    default_out = here / "index.html"

    sidecar = Path(argv[1]) if len(argv) > 1 else default_sidecar
    out = Path(argv[2]) if len(argv) > 2 else default_out

    if not sidecar.exists():
        print(f"sidecar not found: {sidecar}", file=sys.stderr)
        return 2

    sc = load_sidecar(sidecar)
    retros_dir = sidecar.parent
    all_sidecars = load_all_sidecars(retros_dir)
    html_out = render_dashboard(sc, all_sidecars=all_sidecars)
    out.write_text(html_out, encoding="utf-8")
    print(
        f"rendered {sidecar.name} → {out.relative_to(here.parent)} "
        f"(trend: n={len(all_sidecars)} sidecars)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
