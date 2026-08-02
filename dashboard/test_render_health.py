#!/usr/bin/env python3
"""Tests for the v3.0 governance-health widget set.

Run: python3 -m pytest test_render_health.py -q   (or python3 test_render_health.py)

The load-bearing test here is `test_defect_count_does_not_move_the_composite`.
It is the negative control for the whole design decision: the score is on the
integrity of the loop that catches failure, never on the count of failures
caught. If that test ever goes red, the dashboard has started rewarding
switching the instruments off.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETROS = HERE.parent / "retros"


def _load_render():
    spec = importlib.util.spec_from_file_location("render_mod", HERE / "render.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


R = _load_render()


def _sidecar() -> dict:
    return R.load_sidecar(RETROS / "2026-08-02-p17.yaml")


class TestCompositeIsDerivedNeverStored(unittest.TestCase):
    def test_no_sidecar_stores_a_health_score(self):
        """A stored composite goes stale the instant an input moves.

        Iterates EVERY sidecar rather than one, because the name of this test
        is plural and a set-shaped claim must exercise the set.
        """
        files = sorted(RETROS.glob("*-p*.yaml"))
        self.assertGreaterEqual(len(files), 15, "expected the full sidecar series")
        for f in files:
            with self.subTest(sidecar=f.name):
                sc = R.load_sidecar(f)
                for banned in ("health_score", "health", "composite_score"):
                    self.assertNotIn(
                        banned, sc,
                        f"{f.name} stores a derived composite under '{banned}'",
                    )


class TestDefectCountIsNotScored(unittest.TestCase):
    def test_defect_count_does_not_move_the_composite(self):
        """THE control for the design decision. Inflate the ledger 10x; score holds."""
        sc = _sidecar()
        before = R.compute_health(sc)["composite"]
        self.assertIsNotNone(before)

        sc["defect_ledger"]["open_total"] *= 10
        sc["defect_ledger"]["live"] *= 10
        sc["defect_ledger"]["age_30d_plus"] = 999
        after = R.compute_health(sc)["composite"]

        self.assertEqual(
            before, after,
            "the defect count changed the health score — the dashboard now "
            "rewards switching detection off",
        )

    def test_backlog_size_does_not_move_the_composite(self):
        sc = _sidecar()
        before = R.compute_health(sc)["composite"]
        sc["improvement_backlog"]["open"] = 9999
        sc["improvement_backlog"]["total"] = 9999
        self.assertEqual(before, R.compute_health(sc)["composite"])


class TestEnforcementDialScoresBothComponents(unittest.TestCase):
    def test_armed_without_exit_criteria_is_half_credit(self):
        sc = _sidecar()
        sc["enforcement_coverage"] = {
            "arms_built": 6, "arms_armed": 6, "arms_with_written_exit_criteria": 0,
        }
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertAlmostEqual(dial["value"], 0.5)

    def test_fully_armed_and_fully_conditioned_is_full_credit(self):
        sc = _sidecar()
        sc["enforcement_coverage"] = {
            "arms_built": 6, "arms_armed": 6, "arms_with_written_exit_criteria": 6,
        }
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertAlmostEqual(dial["value"], 1.0)

    def test_nothing_armed_is_zero_not_none(self):
        """Zero armed is a MEASURED zero, distinct from 'no data'. §85."""
        sc = _sidecar()
        sc["enforcement_coverage"] = {
            "arms_built": 6, "arms_armed": 0, "arms_with_written_exit_criteria": 0,
        }
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertEqual(dial["value"], 0.0)
        self.assertIsNotNone(dial["value"])


class TestPendingDialsAreExcludedAndDeclared(unittest.TestCase):
    def test_detection_provenance_is_pending_and_not_averaged_in(self):
        health = R.compute_health(_sidecar())
        dial = next(d for d in health["dials"] if d["key"] == "provenance")
        self.assertIsNone(dial["value"])
        self.assertEqual(health["scored_count"], 4)
        self.assertEqual(health["intended_count"], 5)

    def test_a_pending_dial_still_renders(self):
        """'Could not measure' must be visible, never silently dropped."""
        html_out = R.render_health_widget(R.compute_health(_sidecar()))
        self.assertIn("Detection provenance", html_out)
        self.assertIn("hs-row-pending", html_out)
        self.assertIn("4 of 5", html_out)

    def test_missing_block_yields_none_not_zero(self):
        """An absent block is 'no data'; scoring it 0 would be a false measurement."""
        sc = _sidecar()
        del sc["instrument_liveness"]
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "instrument")
        self.assertIsNone(dial["value"])


class TestEverySidecarStillRenders(unittest.TestCase):
    def test_all_sidecars_render_without_raising(self):
        """Regression guard for the meta_finding shape change.

        `meta_finding` is a dict in p3-p16 and a bare string from p17 on. The
        renderer assumed dict and raised AttributeError, which is why p17 had
        never rendered and index.html was stale by a full cycle. This iterates
        the whole series so a future shape change cannot pass silently.
        """
        files = sorted(RETROS.glob("*-p*.yaml"))
        for f in files:
            with self.subTest(sidecar=f.name):
                sc = R.load_sidecar(f)
                out = R.render_dashboard(sc)
                self.assertIn("<h1>", out)

    def test_a_string_meta_finding_reaches_the_callout(self):
        sc = _sidecar()
        sc["meta_finding"] = "A UNIQUE SENTINEL PHRASE FOR THIS TEST"
        self.assertIn("A UNIQUE SENTINEL PHRASE FOR THIS TEST", R.render_dashboard(sc))

    def test_a_dict_meta_finding_still_reaches_the_callout(self):
        sc = _sidecar()
        sc["meta_finding"] = {"headline": "LEGACY DICT SHAPE SENTINEL"}
        self.assertIn("LEGACY DICT SHAPE SENTINEL", R.render_dashboard(sc))


class TestBacklogReconciliation(unittest.TestCase):
    def test_matching_axes_report_no_mismatch(self):
        out = R.render_backlog_widget(_sidecar()["improvement_backlog"])
        self.assertIn("axes sum to 28, open total 28", out)
        self.assertNotIn("MISMATCH", out)

    def test_an_unclassified_item_is_flagged_not_hidden(self):
        """§78 — a derived view drops an unrecognised status silently."""
        bl = dict(_sidecar()["improvement_backlog"])
        bl["open"] = 29  # one item carries a status the axis view cannot classify
        out = R.render_backlog_widget(bl)
        self.assertIn("MISMATCH", out)


class TestBarRendering(unittest.TestCase):
    def test_none_renders_an_empty_track_not_a_full_bar(self):
        self.assertIn("hs-bar-empty", R._bar(None))
        self.assertNotIn("█", R._bar(None))

    def test_bar_proportions(self):
        for value, filled in ((0.0, 0), (0.5, 5), (1.0, 10)):
            with self.subTest(value=value):
                self.assertEqual(R._bar(value).count("█"), filled)



class TestAbsenceNeverRendersAsZero(unittest.TestCase):
    """v3.0 shipped three cohort stages reading 0 for fields p17 never carried.

    A fabricated zero is worse than a blank on a public artifact: it sits among
    honest em-dashes and reads as a measurement that was taken.
    """

    def test_present_renders_a_dash_for_none(self):
        self.assertEqual(R._present(None), "—")

    def test_present_preserves_a_real_zero(self):
        """A MEASURED zero must survive. Absence and zero are different facts."""
        self.assertEqual(R._present(0), "0")

    def test_cohort_stages_absent_from_p17_render_as_dashes(self):
        out = R.render_dashboard(_sidecar())
        cohort = out[out.index("Proposal backlog cohort"):]
        cohort = cohort[:cohort.index("Latency observations")]
        for label in ("Pending before retro", "Approved (not yet executed)", "Executed this cycle"):
            with self.subTest(stage=label):
                seg = cohort[cohort.index(label):]
                seg = seg[:seg.index("</div>", seg.index("cohort-count"))]
                self.assertIn("—", seg, f"{label} rendered a value for an unrecorded field")
                self.assertNotIn(">0<", seg)

    def test_a_recorded_cohort_stage_still_renders_its_number(self):
        out = R.render_dashboard(_sidecar())
        self.assertIn("Authored this cycle", out)
        self.assertRegex(out, r"Authored this cycle</span><span class=\"cohort-count\">3<")


class TestBothSidecarVocabularies(unittest.TestCase):
    """p17 renamed nearly every metric field. The renderer must speak both."""

    def test_flat_dispatch_counts_render(self):
        out = R.render_fam_dispatch_widget({"learning_agent": 1, "consultant": 0})
        self.assertIn("learning agent", out)
        self.assertIn("total", out)
        self.assertNotIn("no fam activity", out)

    def test_axis_shaped_dispatch_still_renders(self):
        out = R.render_fam_dispatch_widget(
            {"dispatch_axis": {"total": 4, "subagents": [{"name": "x", "count": 4}]}}
        )
        self.assertIn("Dispatch axis", out)
        self.assertIn("x", out)

    def test_genuinely_empty_dispatch_says_so(self):
        self.assertIn("no fam activity", R.render_fam_dispatch_widget({}))

    def test_discipline_renders_the_p17_vocabulary(self):
        out = R.render_discipline_rows(_sidecar()["discipline_metrics"])
        self.assertIn("Ritual steps completed", out)
        self.assertIn("Quality-gate traces passing", out)
        self.assertIn("Response-marker missed turns", out)
        self.assertNotIn("no discipline metrics", out)

    def test_discipline_renders_the_p16_vocabulary(self):
        out = R.render_discipline_rows({"checkpoint_bar_miss_rate": 0.19})
        self.assertIn("Checkpoint miss rate", out)
        self.assertIn("19%", out)

    def test_response_marker_shows_BOTH_units_never_fires_alone(self):
        """Reporting fires as a turn count overstates it ~13x. Both or neither."""
        out = R.render_discipline_rows(
            {"response_marker_missed_turns": 1, "response_marker_blocking_fires": 33}
        )
        self.assertIn("1", out)
        self.assertIn("33 blocking fires", out)
        self.assertIn("different units", out)

    def test_no_legacy_widget_is_silently_empty_on_p17(self):
        """The ship defect: sections rendered with titles and no content."""
        out = R.render_dashboard(_sidecar())
        for marker in ("Dispatch axis", "Ritual steps completed", "Authored this cycle"):
            with self.subTest(marker=marker):
                self.assertIn(marker, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
