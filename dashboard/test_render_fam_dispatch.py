"""Smoke tests for render_fam_dispatch_widget — covers the four states
the widget must handle:
  1. Both sub-bands populated with real data (current cycle shape)
  2. dispatch_axis only (no reactions_axis present)
  3. reactions_axis only (no dispatch_axis present)
  4. 0-count row inside dispatch_axis (muted-row treatment)
"""
import sys
from pathlib import Path

# Add dashboard/ to path so we can import render
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_fam_dispatch_widget


SAMPLE_DATA = {
    "dispatch_axis": {
        "subagents": [
            {"name": "deputies", "count": 31, "role": "general-purpose / Root parallel-fanout (not consultant)"},
            {"name": "luma",     "count": 26, "role": "consultant"},
            {"name": "teacher",  "count":  2, "role": "learning-layer"},
            {"name": "deputies-zero", "count": 0, "role": "(test-only zero-count row)"},
        ],
        "total": 59,
    },
    "reactions_axis": {
        "subagents": [
            {"name": "brindle", "count": 299, "role": "companion (hook-driven)",
             "detail": "54 session_starts + 210 reactions + 35 session_ends across 54 sessions"},
        ],
        "total": 299,
    },
}


def test_both_sub_bands_render():
    out = render_fam_dispatch_widget(SAMPLE_DATA)
    assert "Dispatch axis" in out, "dispatch sub-band header missing"
    assert "Reactions axis" in out, "reactions sub-band header missing"
    assert "deputies" in out and "31" in out, "deputies row missing"
    assert "luma" in out and "26" in out, "luma row missing"
    assert "brindle" in out and "299" in out, "brindle row missing"


def test_role_labels_render():
    out = render_fam_dispatch_widget(SAMPLE_DATA)
    assert "general-purpose / Root parallel-fanout (not consultant)" in out, \
        "deputies role label missing"
    assert "companion (hook-driven)" in out, "brindle role label missing"


def test_brindle_detail_renders():
    out = render_fam_dispatch_widget(SAMPLE_DATA)
    assert "54 session_starts + 210 reactions + 35 session_ends across 54 sessions" in out, \
        "brindle detail breakdown missing"


def test_zero_count_row_renders_with_muted_class():
    out = render_fam_dispatch_widget(SAMPLE_DATA)
    # The 0-count row must appear (not be suppressed) AND carry a muted/dashed CSS hook
    assert "deputies-zero" in out, "0-count row was suppressed (should render with muted treatment)"
    assert "kv-row-muted" in out or "fam-row-muted" in out, \
        "0-count row missing muted CSS class"


def test_dispatch_only_input_renders_without_reactions_band():
    dispatch_only = {"dispatch_axis": SAMPLE_DATA["dispatch_axis"]}
    out = render_fam_dispatch_widget(dispatch_only)
    assert "Dispatch axis" in out
    assert "Reactions axis" not in out, "reactions band rendered despite missing reactions_axis"


def test_reactions_only_input_renders_without_dispatch_band():
    reactions_only = {"reactions_axis": SAMPLE_DATA["reactions_axis"]}
    out = render_fam_dispatch_widget(reactions_only)
    assert "Reactions axis" in out
    assert "Dispatch axis" not in out, "dispatch band rendered despite missing dispatch_axis"


def test_empty_input_renders_graceful_placeholder():
    out = render_fam_dispatch_widget({})
    assert "no fam activity recorded" in out.lower() or "(no data)" in out, \
        "empty input must render a graceful placeholder, not crash or empty string"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
