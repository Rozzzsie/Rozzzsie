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



class TestEnforcementThirdComponent(unittest.TestCase):
    """Added 2026-08-02 after the first two components both hit ceiling.

    Arm-level coverage at 6/6 while 22 individual checks state nothing is not
    "fully governed" — it is a dial that stopped discriminating at the
    resolution it happened to be defined at.
    """

    def test_check_level_gap_pulls_the_dial_off_ceiling(self):
        sc = _sidecar()
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertLess(dial["value"], 1.0, "dial is at ceiling despite 0/22 checks")
        self.assertAlmostEqual(dial["value"], 2 / 3, places=3)

    def test_the_component_is_zero_for_every_plausible_denominator(self):
        """The unit is instrument-dependent; the READING must not be."""
        sc = _sidecar()
        for denom in (17, 22, 28):
            with self.subTest(denominator=denom):
                sc["enforcement_coverage"]["checks_enumerated"] = denom
                dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
                self.assertAlmostEqual(dial["value"], 2 / 3, places=3)

    def test_absent_check_fields_fall_back_to_two_components(self):
        """A sidecar predating this component must still score, not crash."""
        sc = _sidecar()
        del sc["enforcement_coverage"]["checks_enumerated"]
        del sc["enforcement_coverage"]["checks_with_written_exit_criteria"]
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertAlmostEqual(dial["value"], 1.0)

    def test_closing_the_check_gap_would_restore_full_credit(self):
        """The dial must be able to reach 100 — a dial that cannot is a scold."""
        sc = _sidecar()
        # Derive the closing value from the sidecar's OWN denominator. A
        # hardcoded 22 here broke the moment the check unit was pinned at 28 —
        # a literal transcribed from a measurement it does not own.
        ec = sc["enforcement_coverage"]
        ec["checks_with_written_exit_criteria"] = ec["checks_enumerated"]
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertAlmostEqual(dial["value"], 1.0)



class TestInstrumentLivenessCanActuallyFail(unittest.TestCase):
    """The §68 control: a guard's PASS is uninterpretable until its FAIL arm
    has been observed firing on a known-bad input.

    A pre-publish grade read `caught / observed` and concluded the dial could
    only ever return 1.0 — that numerator and denominator named the same set.
    They do not: `observed` is control-catches PLUS review-catches, so a
    failure caught by a human reading rather than by an instrument scores
    zero. But the objection was still worth its weight, because being able to
    NAME the failing input is not the same as having FED it one. These tests
    feed it.
    """

    def test_a_review_catch_drives_the_dial_below_full(self):
        sc = _sidecar()
        sc["instrument_liveness"] = {
            "silent_failures_observed": 10,
            "caught_by_control": 9,
            "caught_by_review": 1,
        }
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "instrument")
        self.assertAlmostEqual(dial["value"], 0.9)
        self.assertLess(dial["value"], 1.0, "the fail arm must actually fire")

    def test_an_all_review_cycle_bottoms_the_dial_out(self):
        sc = _sidecar()
        sc["instrument_liveness"] = {
            "silent_failures_observed": 4,
            "caught_by_control": 0,
            "caught_by_review": 4,
        }
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "instrument")
        self.assertEqual(dial["value"], 0.0)

    def test_the_blind_spot_is_stated_on_the_page_not_scored(self):
        """A silent failure nothing caught enters neither term. That is not
        fixable by arithmetic, so it must be published as a limit."""
        sc = _sidecar()
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "instrument")
        self.assertIn("never observed", dial["note"])


class TestEnforcementPredicateIsNamedExactly(unittest.TestCase):
    """The published string must not assert of six arms a property one of
    them does not have. Merging 'has a falsifiable exit' with 'documents its
    permanence' into one denominator is fine; calling the merged thing 'a
    written exit criterion' is not."""

    def test_both_predicates_are_named_in_the_detail(self):
        sc = _sidecar()
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertIn("state an exit condition", dial["detail"])
        self.assertIn("falsifiable", dial["detail"])
        self.assertIn("documented permanence", dial["detail"])
        self.assertNotIn("with a written exit criterion", dial["detail"])

    def test_a_missing_exit_count_is_not_scored_as_zero(self):
        """Absence is not a measured zero — here it must drop the component
        entirely rather than score the arms as having no exits."""
        sc = _sidecar()
        ec = dict(sc["enforcement_coverage"])
        ec.pop("arms_with_written_exit_criteria", None)
        ec.pop("checks_enumerated", None)
        sc["enforcement_coverage"] = ec
        dial = next(d for d in R.compute_health(sc)["dials"] if d["key"] == "enforcement")
        self.assertAlmostEqual(dial["value"], 1.0)
        self.assertNotIn("/6 state an exit condition", dial["detail"])


class TestBacklogRefusesToSumAnIncompleteAxisSet(unittest.TestCase):
    def test_a_missing_axis_blocks_the_reconciliation_entirely(self):
        """A sum over an incomplete set can coincidentally match the total and
        publish a reconciliation that passed only because a value was absent."""
        bl = {"total": 79, "open": 28, "open_ready": 14, "open_decision_gated": 12}
        out = R.render_backlog_widget(bl)
        self.assertIn("axes incomplete", out)
        self.assertNotIn("axes sum to", out)

    def test_a_complete_axis_set_still_reconciles(self):
        bl = {"total": 79, "open": 28, "open_ready": 14,
              "open_decision_gated": 12, "open_upstream_blocked": 2}
        out = R.render_backlog_widget(bl)
        self.assertIn("axes sum to 28", out)
        self.assertNotIn("MISMATCH", out)


class TestNoFabricatedZerosSurvive(unittest.TestCase):
    def test_absent_age_buckets_render_as_dashes_not_zeros(self):
        out = R.render_defect_inventory({"open_total": 38, "live": 34})
        self.assertNotIn(">0<", out)
        self.assertIn("—", out)

    def test_a_recorded_zero_still_renders_zero(self):
        out = R.render_defect_inventory({"open_total": 38, "age_30d_plus": 0})
        self.assertIn(">0<", out)

    def test_the_shape_is_swept_not_patched(self):
        """§67: grep the shape, never patch the instance. `or 0` on a measured
        field is the shape; it must not reappear in either widget."""
        src = (HERE / "render.py").read_text()
        body = src[src.index("def render_defect_inventory"):src.index("def render_discipline_rows")]
        self.assertNotIn("or 0", body)


class TestPublishedLayerCarriesItsCaveats(unittest.TestCase):
    """§45: a caveat in the stripped layer is one the audience never reads."""

    def test_the_gameability_caveat_reaches_the_page(self):
        html_out = R.render_health_widget(R.compute_health(_sidecar()))
        self.assertIn("individually", html_out)
        self.assertIn("gameable", html_out)
        self.assertIn("not a claim that the system", html_out)

    def test_the_inventory_states_its_basis_and_its_stamped_nature(self):
        out = R.render_defect_inventory({
            "open_total": 38, "measured_at": "2026-08-02 15:3x",
            "measured_from": "governance status file",
        })
        self.assertIn("stamped", out)
        self.assertIn("Basis:", out)
        self.assertIn("open as measured", out)


class TestNoInsiderVocabularyInThePublishedLayer(unittest.TestCase):
    """The sanitization sweep ran against the SIDECAR; every leak found by the
    pre-publish grade was injected by this renderer's own hardcoded literals.
    The published layer is the one that has to be audited."""

    FORBIDDEN = ["Teacher invocation", "Luma", "fam-wide", "sprint-2",
                 "P9 is a ritual", "P10 Retro"]

    def test_the_rendered_page_is_clean(self):
        """Audit the OUTPUT, not the source. A comment in render.py explaining
        the sanitization is not published; a string literal is. Grepping the
        source would both miss the distinction and false-positive on this very
        test's own explanation of it."""
        page = R.render_dashboard(_sidecar(), [_sidecar()])
        for term in self.FORBIDDEN:
            with self.subTest(term=term):
                self.assertNotIn(term, page)


if __name__ == "__main__":
    unittest.main(verbosity=2)
