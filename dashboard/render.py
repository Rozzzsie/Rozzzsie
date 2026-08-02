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
# extension). Major bumps reserved for multi-retro trend rendering
# and beyond. Consistent-with-spine semver, mirrors `agent-protocols-X.Y.Z.md`.
DASHBOARD_VERSION = "3.1"


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
    # reality legible (per the operator's pick 2026-05-04 from the four-candidate set).
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
                 "Windows differ by metric; treat cross-cycle deltas as indicative, not strict.",
        ),
        _card(
            "Decision velocity", "proposals executed / cycle",
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


def render_discipline_rows(dm: dict[str, Any]) -> str:
    """Render whichever discipline vocabulary this sidecar speaks.

    p3-p16 record a checkpoint miss RATE; p17 onward record ritual-step and
    quality-gate counts plus a response-marker figure split into turns and
    fires. The renderer knew only the first vocabulary, so a sidecar full of
    discipline data rendered a single em-dash. Rows are emitted only for keys
    that are PRESENT — an absent metric produces no row at all rather than a
    row reading zero.
    """
    rows: list[str] = []

    def add(key: str, val: str, note: str = "") -> None:
        note_html = f'<span class="kv-note">{html.escape(note)}</span>' if note else ""
        rows.append(
            f'<div class="kv-row"><span class="kv-key">{html.escape(key)}</span>'
            f'<span class="kv-val">{val}</span>{note_html}</div>'
        )

    rate = dm.get("checkpoint_bar_miss_rate")
    if isinstance(rate, (int, float)):
        add("Checkpoint miss rate", f"{rate * 100:.0f}%")
    prior = dm.get("checkpoint_bar_prior_session_rate")
    if isinstance(prior, (int, float)):
        add("Prior session", f"{prior * 100:.0f}%")

    defined, completed = dm.get("ritual_steps_defined"), dm.get("ritual_steps_completed")
    if defined is not None and completed is not None:
        add("Ritual steps completed", f"{completed}/{defined}")
    if dm.get("monthly_subritual_due") is not None:
        add("Monthly sub-ritual",
            "completed" if dm.get("monthly_subritual_completed") else "DUE, not run")

    sampled, passing = dm.get("quality_gate_traces_sampled"), dm.get("quality_gate_traces_passing")
    if sampled is not None and passing is not None:
        add("Quality-gate traces passing", f"{passing}/{sampled}")

    missed = dm.get("response_marker_missed_turns")
    fires = dm.get("response_marker_blocking_fires")
    if missed is not None:
        # Both figures are shown because they are DIFFERENT UNITS and the larger
        # one is the wrong one — reporting fires alone overstates the miss count
        # by an order of magnitude, which this OS has done to itself twice.
        detail = f" · {fires} blocking fires" if fires is not None else ""
        add("Response-marker missed turns", f"{missed}{detail}",
            "turns and fires are different units; the fire count is not a turn count")

    if not rows:
        return '<div class="kv-row"><span class="kv-key">(no discipline metrics recorded this cycle)</span></div>'
    return "".join(rows)


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


def render_backlog_widget(bl: dict[str, Any]) -> str:
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
    return f"""
      <div class="bk-head">
        <span class="bk-total">{bl.get("total", "—")}</span>
        <span class="bk-total-label">proposed improvements — lifetime</span>
      </div>
      <div class="bk-split">
        <span>{bl.get("done", "—")} done</span><span>{open_n if open_n is not None else "—"} open</span><span>{bl.get("parked", "—")} parked</span>
      </div>
      <div class="bk-axes">{chips}</div>
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

    discipline_rows_html = render_discipline_rows(discipline)
    health = compute_health(sc)
    health_html = render_health_widget(health)
    inventory_html = render_defect_inventory(sc.get("defect_ledger") or {})
    backlog_html = render_backlog_widget(sc.get("improvement_backlog") or {})

    findings_rows_html = "".join(render_finding_row(f) for f in findings)
    tally_html = render_tally(discipline.get("luma_tally_by_category") or {})
    fam_dispatch = sc.get("fam_dispatch_distribution") or {}
    fam_dispatch_html = render_fam_dispatch_widget(fam_dispatch)
    trend_html = render_trend_chart(all_sidecars or [sc])
    trend_section_html = (
        f"""
    <section>
      <h2 class="section-title">Governance trend <span class="section-title-suffix">n={len(all_sidecars or [sc])} P10 cycles</span></h2>
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
        Governance health metrics from the most recent P10 weekly retrospective in the Rozzzsie OS.
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
        {render_tile(accepted, "Accepted / shipped", f"{by_status.get('executed', 0)} executed · {by_status.get('approved', 0)} approved · {by_status.get('pre-ship', 0)} pre-ship")}
        {render_tile(deferred, "Deferred", "Each with explicit watch entry or carry-forward")}
        {render_tile(by_status.get("rejected", 0), "Rejected")}
      </div>
    </section>
    {trend_section_html}

    <section>
      <h2 class="section-title">Specialist agent dispatches <span class="section-title-suffix">across specialist agents, this cycle</span></h2>
      <div class="fam-widget">
        {fam_dispatch_html}
      </div>
    </section>

    <section>
      <h2 class="section-title">Discipline <span class="section-title-suffix">governance health under load</span></h2>
      <div class="bands">
        <div class="band">
          <h3>Discipline metrics</h3>
          {discipline_rows_html}
        </div>
        <div class="band band-muted">
          <h3>Reframe-axis facet <span class="band-title-suffix">deep-dive · narrative-review-pending</span></h3>
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
            <div class="cohort-stage"><span class="cohort-label">Pending before retro</span><span class="cohort-count">{_present(backlog.get("pending_before_retro"))}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Approved (not yet executed)</span><span class="cohort-count">{_present(backlog.get("approved_not_executed"))}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Executed this cycle</span><span class="cohort-count">{_present(backlog.get("executed_this_cycle"))}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Authored this cycle</span><span class="cohort-count">{_present(backlog.get("authored_this_cycle"))}</span></div>
            <div class="cohort-arrow">↓</div>
            <div class="cohort-stage"><span class="cohort-label">Deferred this cycle</span><span class="cohort-count">{_present(backlog.get("deferred_this_cycle"))}</span></div>
          </div>
        </div>
        <div class="band">
          <h3>Latency observations</h3>
          {'' if latency_has_data else '<p class="empty-note">Not recorded this cycle — the band is suppressed rather than published as a row of dashes, which reads as measured-and-empty.</p>'}
          {f'''<div class="kv-row">
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
          </div>''' if latency_has_data else ''}
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
    default_sidecar = here.parent / "retros" / "2026-07-26-p16.yaml"
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
