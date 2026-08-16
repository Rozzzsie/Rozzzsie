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
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETROS = HERE.parent / "retros"

# ─── Known-nonconformant published sidecars (Rosie's ruling, 2026-08-16) ──────
#
# `required_groups` (render.py) landed at p19 and enforces block-level
# completeness. Two ALREADY-PUBLISHED sidecars fail it. They are NOT repaired:
# the readings they are missing were never recorded, and back-filling plausible
# values to turn a suite green is precisely the failure the guard exists to
# catch. Conformance is asserted from p19 FORWARD; these two are named here with
# the measured gap, so the exemption is a declaration rather than a silence.
#
# ⛔ The test asserts these still RAISE. An entry that starts passing is a
#    signal — either it was quietly edited, or the schema was loosened — and
#    either way the right response is to look, not to delete the line.
KNOWN_NONCONFORMANT = {
    # `latency_observations` lost ALL SIX core keys at once, after 14 unbroken
    # cycles (p3→p16). The block is absent entirely, not null.
    "2026-08-02-p17": "latency_observations absent — 6 keys, never recorded",
    # `defect_ledger` lost ALL SIX age keys — present in p17, absent here, i.e.
    # 1 of the 2 cycles in which this block has existed.
    "2026-08-09-p18": "defect_ledger age group absent — 6 keys, never recorded",
}


def _load_render():
    spec = importlib.util.spec_from_file_location("render_mod", HERE / "render.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


R = _load_render()


def _sidecar() -> dict:
    """A schema-CONFORMANT p17, for tests that need "a valid 1.1 sidecar".

    p17 as published is not conformant: it dropped all six `latency_observations`
    core keys (after 14 unbroken cycles) and the p19 `required_groups` arm now
    says so. Eight tests here use this helper as their baseline, so without a
    fix they fail for a reason that has nothing to do with what they assert.

    ⛔ THE BLOCK IS REMOVED, NOT REPOPULATED. Those six readings were never
    recorded — there is nothing to restore, and inventing plausible latencies to
    turn a suite green is the failure this whole guard exists to catch. Removing
    the block uses the guard's own semantics instead: an ABSENT block is not
    owed its group, so the fixture is conformant without asserting a single
    number nobody measured. `latency_observations` is `record_only` and reaches
    no rendering path, so its absence changes no other assertion in this file.

    p17's `defect_ledger` age group is already complete (measured: present in
    p17, dropped in p18), so it needs no treatment.
    """
    sc = R.load_sidecar(RETROS / "2026-08-02-p17.yaml")
    sc.pop("latency_observations", None)
    return sc


def _all_sidecars() -> list[dict]:
    return R.load_all_sidecars(RETROS)


def _first_present(*vals):
    return next((v for v in vals if v is not None), None)


def _safe_read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


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

    def test_an_unrecorded_flow_value_renders_a_dash_not_a_zero(self):
        """Repointed 2026-08-02: the 5-stage cohort funnel was retired after
        three of its stages stopped being reported. The invariant it protected
        — an unrecorded field must never render 0 — now lives on the surviving
        flow chips folded into the backlog widget."""
        sc = _sidecar()
        pb = dict(sc["proposal_backlog"])
        pb.pop("deferred_this_cycle", None)
        out = R.render_backlog_widget(sc["improvement_backlog"], pb)
        seg = out[out.index("bk-flow"):]
        self.assertIn("—", seg)
        self.assertNotIn(">0<", seg)

    def test_a_recorded_flow_value_still_renders_its_number(self):
        """Retiring a WIDGET must not silently retire its DATA."""
        sc = _sidecar()
        out = R.render_backlog_widget(sc["improvement_backlog"], sc["proposal_backlog"])
        self.assertIn("authored", out)
        self.assertIn(">3<", out)


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

    # ── Repointed 2026-08-02 when the Discipline widget was retired ──────────
    # These guarded real invariants, so they follow the data to whichever
    # surface now carries it rather than being deleted with the widget.

    def test_the_p17_vocabulary_still_reaches_the_page_via_the_health_dials(self):
        """Ritual-step and quality-gate counts moved from the retired widget
        into the health score. Retiring a WIDGET must not retire its DATA."""
        out = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("10/10 steps", out)
        self.assertIn("3/3 traces passing", out)

    def test_the_p16_rate_is_retired_from_the_PAGE_but_not_from_the_RECORD(self):
        """Rewritten 2026-08-02. This asserted `19%` was "still plotted", which
        the operator decision reverses — the retracted rate is no longer drawn.

        The invariant it was written for survives and is what is asserted now:
        retiring a RENDERING must not retire the DATA. So the card is still
        present, the percentage is gone from the page, and the value is still
        in the sidecar where anyone auditing the retraction can find it."""
        out = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("Checkpoint discipline", out)
        self.assertNotIn("19%", out, "the retracted rate is no longer plotted")
        p16 = R.load_sidecar(RETROS / "2026-07-26-p16.yaml")
        self.assertIsNotNone(
            p16["discipline_metrics"].get("checkpoint_bar_miss_rate"),
            "the rate must survive in the record even though the page drops it",
        )

    def test_fires_never_appear_without_turns(self):
        """Reporting fires as a turn count overstates it ~33x. The widget that
        paired them is gone; the INVARIANT is not. Stated as an implication so
        it survives the surface change: if the page shows the fire count, it
        must show the turn count too."""
        out = R.render_dashboard(_sidecar(), _all_sidecars())
        dm = _sidecar()["discipline_metrics"]
        fires, turns = dm["response_marker_blocking_fires"], dm["response_marker_missed_turns"]
        self.assertEqual((fires, turns), (33, 1), "positive control: the fixture is the real one")
        if f">{fires}<" in out:
            self.assertIn(f">{turns}<", out, "fires shown without turns")

    def test_no_legacy_widget_is_silently_empty_on_p17(self):
        """The ship defect: sections rendered with titles and no content."""
        out = R.render_dashboard(_sidecar(), _all_sidecars())
        for marker in ("Dispatch axis", "10/10 steps", "authored"):
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
        field is the shape; it must not reappear in either widget.

        Two defects this test had to survive, both found 2026-08-02:
        (1) its end anchor named a function defined EARLIER in the file, so the
            slice was start > end — Python returns "" rather than raising, and
            `assertNotIn` on an empty string passes. It had checked zero bytes
            since it was written. Hence the non-empty assertion below.
        (2) the function's own comment says "NEVER `or 0` here", so a raw scan
            false-positives on the explanation of the rule. Code only.
        """
        src = (HERE / "render.py").read_text()
        start, end = src.index("def render_defect_inventory"), src.index("def render_backlog_widget")
        self.assertLess(start, end, "slice anchors inverted — the body would be empty")
        body = src[start:end]
        self.assertGreater(len(body), 500, "positive control: a real body was sliced")
        code = "\n".join(
            ln for ln in body.splitlines() if not ln.lstrip().startswith("#")
        )
        self.assertNotIn("or 0", code)


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

    def test_no_protocol_identifier_reaches_the_page(self):
        """The list above was fitted to the instances found, not to the
        vocabulary. It bans the phrase "P10 Retro" — so "n=15 P10 cycles"
        walked straight through it and shipped. A phrase list only ever
        catches the phrasings you already saw; the thing that is actually
        confidential is the TOKEN.
        """
        import re as _re
        page = R.render_dashboard(_sidecar(), [_sidecar()])
        leaked = sorted(set(_re.findall(r"\bP\d+\b", page)))
        self.assertEqual(leaked, [], f"protocol identifiers on the page: {leaked}")

    # ⛔ RETIRED 2026-08-02 by operator decision: rail names are PUBLIC
    # vocabulary. `test_agent_names_do_not_reach_the_page_in_ANY_case` used to
    # live here and banned six of them, case-folded.
    #
    # It is deleted rather than narrowed, and the reason is worth keeping: the
    # 15 sidecars published in this same repo carry those names 298 times in
    # plaintext. The test was enforcing on ONE surface a policy the data beside
    # it had never followed — so it read as confidentiality coverage while
    # providing none, which is worse than no test at all. The list was also
    # incomplete (`deputies`, `silent-failure-hunter`), and completing it would
    # have deepened exactly that false signal.
    #
    # Protocol identifiers are a SEPARATE question and are still banned above:
    # a decision that rail names are public says nothing about P-numbers.

    def test_the_rendered_page_is_clean(self):
        """Audit the OUTPUT, not the source. A comment in render.py explaining
        the sanitization is not published; a string literal is. Grepping the
        source would both miss the distinction and false-positive on this very
        test's own explanation of it."""
        page = R.render_dashboard(_sidecar(), [_sidecar()])
        for term in self.FORBIDDEN:
            with self.subTest(term=term):
                self.assertNotIn(term, page)



class TestSidecarSchemaGuard(unittest.TestCase):
    """The guard against the drift that actually happened: 16 cycles in which
    every top-level key matched and the sub-keys silently diverged."""

    def test_a_missing_required_field_fails_the_render(self):
        sc = _sidecar()
        del sc["defect_ledger"]["open_total"]
        with self.assertRaises(R.SidecarSchemaError) as ctx:
            R.validate_sidecar(sc)
        self.assertIn("defect_ledger.open_total", str(ctx.exception))

    def test_a_rename_reports_BOTH_halves(self):
        """A rename is one event with two halves. Reporting only the missing
        key withholds the half that says what replaced it."""
        sc = _sidecar()
        sc["defect_ledger"]["open_count"] = sc["defect_ledger"].pop("open_total")
        with self.assertRaises(R.SidecarSchemaError) as ctx:
            R.validate_sidecar(sc)
        msg = str(ctx.exception)
        self.assertIn("open_total", msg, "the missing half")
        self.assertIn("open_count", msg, "the replacement half")

    def test_every_missing_field_is_named_not_just_the_first(self):
        sc = _sidecar()
        del sc["defect_ledger"]["open_total"]
        del sc["enforcement_coverage"]["arms_built"]
        with self.assertRaises(R.SidecarSchemaError) as ctx:
            R.validate_sidecar(sc)
        self.assertIn("open_total", str(ctx.exception))
        self.assertIn("arms_built", str(ctx.exception))

    def test_an_undeclared_sub_key_warns(self):
        sc = _sidecar()
        sc["discipline_metrics"]["brand_new_metric"] = 7
        self.assertTrue(any("brand_new_metric" in w for w in R.validate_sidecar(sc)))

    def test_an_undeclared_top_level_block_warns(self):
        """Without this arm a renamed BLOCK passes silently — the sub-key loop
        only inspects blocks it already knows about."""
        sc = _sidecar()
        sc["some_new_block"] = {"a": 1}
        self.assertTrue(any("some_new_block" in w for w in R.validate_sidecar(sc)))

    def test_record_only_blocks_do_not_warn(self):
        """hook_health and latency_observations are carried as records with no
        renderer. Declared, so their silence is deliberate, not an oversight."""
        warns = R.validate_sidecar(_sidecar())
        self.assertFalse([w for w in warns if "hook_health" in w or "latency_observations" in w])

    def test_the_real_sidecar_validates_silently(self):
        """Positive control. A guard that fires on correct input is noise."""
        self.assertEqual(R.validate_sidecar(_sidecar()), [])

    def test_an_unknown_schema_version_says_so_rather_than_passing(self):
        sc = _sidecar()
        sc["schema_version"] = "9.9"
        self.assertTrue(any("no manifest" in w for w in R.validate_sidecar(sc)))


class TestClosedSeriesIsDeclaredNotGapped(unittest.TestCase):
    """Absence is not zero, and on a time series it is not a dip either."""

    def _series(self, values):
        return [{"retro_id": f"2026-01-01-p{i}", "discipline_metrics": {"checkpoint_bar_miss_rate": v},
                 "proposal_backlog": {}, "fam_dispatch_distribution": {}}
                for i, v in enumerate(values, start=1)]

    def test_a_field_that_stops_being_reported_is_declared_closed(self):
        """Exercises the DEFAULT closure text. The checkpoint card now carries an
        explicit retraction reason, so testing this through that card would pass
        on the override and never touch the default branch."""
        series = self._series([0.3, 0.2, 0.25, None])
        for i, v in enumerate([1, 2, None, None]):
            series[i]["discipline_metrics"]["teacher_invocations"] = v
        out = R.render_trend_chart(series)
        card = out[out.index("Learning-layer invocations"):]
        self.assertIn("no longer reported after", card)

    def test_a_live_series_is_not_declared_closed(self):
        out = R.render_trend_chart(self._series([0.3, 0.2, 0.25, 0.1]))
        self.assertNotIn("no longer reported after", out)


class TestRetiredWidgetsAreGone(unittest.TestCase):
    """Retired 2026-08-02 after measuring their sidecar coverage."""

    RETIRED = ["Reframe-axis facet", "Latency observations",
               "Proposal backlog cohort", "Pending before retro"]

    def test_retired_widgets_do_not_render(self):
        page = R.render_dashboard(_sidecar(), [_sidecar()])
        for widget in self.RETIRED:
            with self.subTest(widget=widget):
                self.assertNotIn(widget, page)

    def test_retiring_the_cohort_did_not_drop_its_surviving_data(self):
        """A retired WIDGET must not silently retire its DATA."""
        sc = _sidecar()
        out = R.render_backlog_widget(sc["improvement_backlog"], sc["proposal_backlog"])
        self.assertIn("authored", out)
        self.assertIn("deferred", out)


class TestFindingsItemsAreUnderContract(unittest.TestCase):
    """Absorbed from the retired `retro-sidecar-schema.yaml` at the merge.

    The top-level manifest only asserts that `findings` exists. Without a
    per-item arm every field inside it could be renamed at once and the render
    would succeed with N blank rows — the same em-dash failure one level down.
    """

    def test_a_missing_per_finding_required_key_fails_and_names_the_finding(self):
        sc = _sidecar()
        del sc["findings"][0]["target_surface"]
        with self.assertRaises(R.SidecarSchemaError) as ctx:
            R.validate_sidecar(sc)
        msg = str(ctx.exception)
        self.assertIn("target_surface", msg)
        self.assertIn(str(sc["findings"][0]["id"]), msg, "names WHICH finding")

    def test_an_undeclared_per_finding_key_warns(self):
        sc = _sidecar()
        sc["findings"][0]["severity_tier"] = "high"
        self.assertTrue(any("severity_tier" in w for w in R.validate_sidecar(sc)))

    def test_a_status_with_no_stylesheet_rule_warns(self):
        sc = _sidecar()
        sc["findings"][0]["status"] = "quantum-superposed"
        warns = R.validate_sidecar(sc)
        self.assertTrue(any("quantum-superposed" in w and "unstyled" in w for w in warns))

    def test_every_declared_styled_status_really_has_a_css_rule(self):
        """The arm above claims the stylesheet covers the declared set. This is
        what keeps that claim honest — the manifest and the CSS are separate
        artifacts and either can move. Iterates the whole set, not one member.
        """
        css = (HERE / "assets" / "dashboard.css").read_text()
        declared = R.SIDECAR_SCHEMA["1.1"]["findings_status_styled"]
        self.assertTrue(declared, "positive control: the set is non-empty")
        missing = sorted(s for s in declared if f".pill-{s}" not in css)
        self.assertEqual(missing, [], f"declared styled but absent from CSS: {missing}")

    def test_every_status_used_by_any_real_sidecar_is_declared_styled(self):
        """The other direction. The first test proves the manifest does not
        over-claim; this proves it does not under-cover the live corpus."""
        declared = R.SIDECAR_SCHEMA["1.1"]["findings_status_styled"]
        used = {
            f.get("status")
            for p in sorted(RETROS.glob("*.yaml"))
            for f in (R.load_sidecar(p).get("findings") or [])
            if isinstance(f, dict) and f.get("status")
        }
        self.assertGreaterEqual(len(used), 5, "positive control: the corpus was read")
        self.assertEqual(sorted(used - declared), [])

    def test_every_published_finding_carries_the_required_keys(self):
        """Corpus-wide positive control over all 154 findings.

        The first version of this ran `validate_sidecar` in a loop and skipped
        any sidecar whose `schema_version` has no manifest — which is 14 of 15.
        It was named for the corpus and exercised ONE file, and its positive
        control counted files FOUND rather than findings CHECKED, so the count
        could not reveal the gap. The required set was derived by measuring all
        154; the assertion has to be made where the derivation was.
        """
        required = R.SIDECAR_SCHEMA["1.1"]["findings_item"]["required"]
        checked = 0
        for p in sorted(RETROS.glob("*.yaml")):
            for f in R.load_sidecar(p).get("findings") or []:
                if not isinstance(f, dict):
                    continue
                checked += 1
                with self.subTest(sidecar=p.stem, finding=f.get("id")):
                    self.assertEqual(sorted(required - set(f)), [])
        self.assertGreaterEqual(checked, 154, f"only {checked} findings checked")

    def test_the_version_gated_validator_runs_on_every_sidecar_it_can(self):
        """The arm above is version-blind on purpose. This one records how much
        of the corpus the full validator actually covers, so 'the validator
        passes' is never mistaken for 'the corpus was validated'."""
        paths = sorted(RETROS.glob("*.yaml"))
        covered = [p for p in paths
                   if str(R.load_sidecar(p).get("schema_version")) in R.SIDECAR_SCHEMA]
        for p in covered:
            with self.subTest(sidecar=p.stem):
                if p.stem in KNOWN_NONCONFORMANT:
                    with self.assertRaises(
                        R.SidecarSchemaError,
                        msg=f"{p.stem} is on the known-nonconformant list but now "
                            "validates — if it was repaired, take it off the list",
                    ):
                        R.validate_sidecar(R.load_sidecar(p))
                    continue
                R.validate_sidecar(R.load_sidecar(p))
        self.assertGreaterEqual(len(paths), 15, "positive control: sidecars found")
        self.assertGreaterEqual(len(covered), 1, "at least the current cycle")
        # Positive control on the list itself: an allowlist that names files
        # which do not exist is an allowlist that has quietly stopped applying.
        stems = {p.stem for p in paths}
        for stem in KNOWN_NONCONFORMANT:
            self.assertIn(stem, stems, f"{stem} is allowlisted but not in the corpus")


class TestReKeyIsTestedAgainstTheSemanticPredecessor(unittest.TestCase):
    """The learning-layer series was CLOSED on 2026-08-02 and should not have
    been. The close/re-key test was run against the new key's own coverage
    (1/15) — which is what every rename scores on the cycle it appears, so that
    test can only ever answer "new series". The discriminating test is agreement
    in the overlap.
    """

    def test_the_two_learning_layer_fields_agree_wherever_both_exist(self):
        """This is the measurement that licenses the coalesce. If it ever goes
        red, the two fields are NOT the same series and the card is lying."""
        agree = disagree = 0
        for p in sorted(RETROS.glob("*.yaml")):
            sc = R.load_sidecar(p)
            old = (sc.get("discipline_metrics") or {}).get("teacher_invocations")
            fam = sc.get("fam_dispatch_distribution") or {}
            nested = {
                r.get("name"): r.get("count")
                for r in (fam.get("dispatch_axis") or {}).get("subagents") or []
                if isinstance(r, dict)
            }
            new = _first_present(fam.get("learning_agent"), nested.get("teacher"))
            if old is None or new is None:
                continue
            (agree := agree + 1) if old == new else (disagree := disagree + 1)
        self.assertGreaterEqual(agree, 13, "positive control: overlap was found")
        self.assertEqual(disagree, 0)

    def test_the_learning_layer_series_is_not_closed(self):
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        card = page[page.index("Learning-layer invocations"):]
        card = card[: card.index("</div></div>") if "</div></div>" in card else 2000]
        self.assertNotIn("series closed", card)

    def test_a_closed_series_states_WHY_not_merely_that_it_stopped(self):
        """A retraction and a rename are indistinguishable from the gap alone,
        and they warrant opposite remedies."""
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("RETRACTED", page)

    def test_the_restarted_series_is_labelled_new_and_not_grafted(self):
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("new series", page)
        self.assertIn("missed turns", page)


# RETIRED 2026-08-02 — `TestDispatchTotalIsNotPresentedAsComparable`.
# It asserted the "no longer reported / not comparable" disclaimer, which the
# operator removed from the published page ("we only show the latest metrics
# externally"). Its replacement is `TestDroppedRailsNoteIsGone` below, which
# asserts the inverse. Recorded rather than silently deleted: the underlying
# hazard it was written for — a role-bucket total read as a per-agent total —
# is now closed at the source instead, because p17's buckets are re-authored
# from measurement rather than shipped as four zeros needing a disclaimer.


class TestTrendScopeLabelSaysWhatItCountsOutOf(unittest.TestCase):
    def test_the_label_names_the_range_and_the_cycles_it_excludes(self):
        """The label must name its own count and range — DERIVED, never pinned.

        ⛔ THIS TEST USED TO HARD-CODE `n=15`, AND WAS RED FOR A FULL CYCLE BECAUSE OF IT
        (2026-08-09 → 2026-08-16, found during p19's ritual and verified on a clean tree).
        The corpus grows by exactly one every retro cycle, so a pinned count tests the
        CALENDAR, not behaviour: it goes red on every publish, and re-pinning buys one week.

        ⭐ The repair is to assert the SHAPE — that the label reports the count it actually
        counted, and names its own excluded range — which is stable across growth. Compare
        `required_groups`, shipped the same cycle: also a shape assertion, also growth-stable.

        📌 It went red the moment p18 published and nothing reported it for seven days, which
        is direct evidence for the run-the-suites ceremony step added 2026-08-15 — measured on
        the cycle immediately before that step existed.
        """
        sidecars = _all_sidecars()
        label = R._trend_scope_label(sidecars)

        # The count is derived from the corpus, not from a literal.
        self.assertIn(f"n={len(sidecars)}", label,
                      "the label must report the number it actually counted")

        # The range must name a first and last cycle, whatever they currently are.
        cycles = sorted(
            int(mo.group(1))
            for sc in sidecars
            if (mo := re.search(r"-p(\d+)$", str(sc.get("retro_id", ""))))
        )
        self.assertTrue(cycles, "positive control: retro_ids must parse to cycle numbers")
        self.assertIn(f"#{cycles[0]}", label, "names the first cycle in scope")
        self.assertIn(f"#{cycles[-1]}", label, "names the last cycle in scope")
        self.assertIn("predate", label, "says what the count is out of")


class TestRetiredDisciplineWidgetIsGone(unittest.TestCase):
    def test_the_discipline_section_and_its_renderer_are_removed(self):
        self.assertFalse(hasattr(R, "render_discipline_rows"))
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertNotIn("Discipline metrics", page)

    def test_the_dead_tally_renderer_is_removed(self):
        """Computed into a variable that was never interpolated. Deleted rather
        than wired up — nothing had rendered it since the widget retirement."""
        self.assertFalse(hasattr(R, "render_tally"))


class TestTheRetiredSchemaFileIsNotCitedAnywhere(unittest.TestCase):
    """The merge is only complete if no pointer survives it. A citation to a
    deleted file is worse than one to a stale file: it resolves to nothing, and
    every one of these lived in the PUBLIC repo pointing at a PRIVATE path, so
    they never resolved for the audience that reads them.
    """

    def test_the_only_surviving_mention_is_the_tombstone_in_render_py(self):
        """Exactly one mention is sanctioned: the comment in render.py that
        explains what was deleted and why. That one is a RECORD, and it is what
        a reader who greps an old citation needs to land on.

        Asserted as a set EQUALITY, not an exemption list — an allowlist rots
        by accretion, whereas this fails the moment the sanctioned set widens
        OR the tombstone itself disappears.
        """
        root = HERE.parent
        hits = {
            str(p.relative_to(root))
            for p in root.rglob("*")
            if p.is_file()
            and ".git/" not in str(p)
            and p.suffix in {".md", ".yaml", ".yml", ".py", ".html", ".css"}
            and p.name != Path(__file__).name
            and "retro-sidecar-schema" in _safe_read(p)
        }
        self.assertEqual(hits, {"dashboard/render.py"})


class TestDecisionVelocityLosesNoFinding(unittest.TestCase):
    """The headline counts EVERY finding; the buckets counted a hardcoded four
    statuses. The vocabulary grew to eight over 15 cycles and the bucket list
    never did, so `approved-queued`, `partial-executed` and `carried-open`
    matched nothing and left the page — 6 findings across 4 cycles, on a section
    whose sibling header says "every one statused".

    Measured 2026-08-02 before the fix: p4 12→10, p14 7→5, p15 8→7, p17 8→7.
    """

    def test_every_status_in_every_sidecar_lands_in_a_bucket(self):
        """Name says every — so the body iterates every sidecar and every
        status, not the one that prompted the question (§67)."""
        for sc in _all_sidecars():
            for f in sc.get("findings") or []:
                status = f.get("status")
                with self.subTest(retro=sc.get("retro_id"), status=status):
                    _, unbucketed = R.velocity_buckets(sc.get("findings") or [])
                    self.assertNotIn(
                        status, unbucketed,
                        f"{status} renders in no bucket and leaves the page",
                    )

    def test_the_buckets_sum_to_the_headline_for_every_cycle(self):
        for sc in _all_sidecars():
            findings = sc.get("findings") or []
            rows, unbucketed = R.velocity_buckets(findings)
            with self.subTest(retro=sc.get("retro_id")):
                self.assertEqual(
                    sum(n for _, n, _ in rows) + sum(unbucketed.values()),
                    len(findings),
                )

    def test_a_status_nobody_has_invented_yet_is_REPORTED_not_dropped(self):
        """The guard, not the fix. Extending the bucket list closes today's
        three; only a residual arm closes the ninth status, and that one will
        be added by someone who has never read this file."""
        findings = [{"status": "executed"}, {"status": "invented-status-2027"}]
        rows, unbucketed = R.velocity_buckets(findings)
        self.assertEqual(unbucketed, {"invented-status-2027": 1})
        self.assertEqual(sum(n for _, n, _ in rows) + sum(unbucketed.values()), 2)

    def test_the_published_page_states_the_reconciliation(self):
        """§87 — the defect was on the rendered layer, so the assertion is too.
        A reader must be able to check the arithmetic without opening the yaml."""
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("Carried open", page)
        self.assertIn("buckets sum to 8", page)

    def test_an_unbucketed_status_reaches_the_VELOCITY_SECTION_not_just_the_helper(self):
        """Scoped to the section, deliberately. The first version of this test
        asserted the name appeared anywhere on the page and PASSED against the
        broken renderer — the findings-detail table prints every status pill,
        so the assertion was satisfied by a table that was never the subject.
        A test whose input can reach the assertion by a second path is not a
        control on the first one."""
        sc = _sidecar()
        sc["findings"] = list(sc["findings"]) + [
            {"id": "X", "title": "t", "category": "c", "evidence_count": 1,
             "source_catchment": "s", "recommendation": "r",
             "status": "invented-status-2027", "execution_target_week": "w",
             "target_surface": "s"}
        ]
        page = R.render_dashboard(sc, _all_sidecars())
        velocity = page[page.index("Decision velocity"):page.index("Governance trend")]
        self.assertIn("invented-status-2027", velocity)


class TestTheNonListFindingsArmActuallyFires(unittest.TestCase):
    """The last standing residual from the 2026-08-01 adversarial pass.

    The guard itself was already correct — `findings` present but not a list
    satisfies the required-field check (it is non-None) and would then skip the
    per-item arm silently, so the branch exists to convert that into rc=3. What
    was missing is any input that reaches it: an unexercised guard and a broken
    one are indistinguishable from the suite, and this one protects a path whose
    failure mode is a raw AttributeError from the renderer.
    """

    def _sc_with_findings(self, value):
        sc = _sidecar()
        sc["findings"] = value
        return sc

    def test_a_non_list_findings_block_RAISES_and_names_the_type(self):
        for bad in ({"id": "x"}, "a string", 7):
            with self.subTest(type=type(bad).__name__):
                with self.assertRaises(R.SidecarSchemaError) as cm:
                    R.validate_sidecar(self._sc_with_findings(bad))
                msg = str(cm.exception)
                self.assertIn("findings", msg)
                self.assertIn(type(bad).__name__, msg, "names what it got")

    def test_a_LIST_of_findings_does_not_trip_the_type_guard(self):
        """The negative control. Without it the test above passes against a
        guard that rejects everything, which is not the contract."""
        warnings = R.validate_sidecar(_sidecar())
        self.assertIsInstance(warnings, list)


class TestTheRetractedRateIsGoneNotRedrawn(unittest.TestCase):
    """Operator decision 2026-08-02: retire the 16 rate points entirely and show
    only the new axis. A retracted series redrawn alongside its replacement
    invites the eye to read one slope across two units."""

    def test_no_rate_value_from_the_retracted_series_renders(self):
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        # Sliced to the next card by NAME. A slice on a closing-tag pattern
        # would move with any markup change and start asserting about a
        # different region while still passing.
        checkpoint = page[
            page.index("Checkpoint discipline"):page.index("Proposal authoring")
        ]
        self.assertNotIn("%", checkpoint, "a percentage from the retracted rate survived")

    def test_the_reason_the_series_is_absent_survives_its_deletion(self):
        """Deleting the points without the reason turns a retraction into a
        silent gap — the exact reading the closed-series machinery was built to
        prevent. The data goes; the sentence stays."""
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("RETRACTED", page)

    def test_a_single_point_is_labelled_a_value_not_a_trend(self):
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertIn("n=1", page)
        self.assertIn("missed turns", page)


class TestDroppedRailsNoteIsGone(unittest.TestCase):
    """Operator decision 2026-08-02 (Rosie, verbatim): "we only show the latest
    metrics externally, no need to show the notes for prior reporting periods."

    Recorded as a decision rather than a silent deletion — the note it removes
    was itself built to prevent a misreading, so the reason it is now
    unnecessary matters: p17's four buckets are re-authored from measurement,
    so the total is no longer a coverage artefact needing a disclaimer.
    """

    def test_the_note_and_its_helper_are_removed(self):
        page = R.render_dashboard(_sidecar(), _all_sidecars())
        self.assertNotIn("no longer reported:", page)
        self.assertNotIn("not comparable", page)
        self.assertFalse(hasattr(R, "_dropped_rails"))

    def test_the_widget_no_longer_reaches_for_a_POSITIONAL_prior_sidecar(self):
        """`all_sidecars[-2]` meant "the previous cycle" only while p17 was
        last. Deleting the consumer closes it outright, which is the fix a
        compensating index check could not be (§68)."""
        import inspect
        self.assertNotIn("all_sidecars[-2]", inspect.getsource(R.render_dashboard))


if __name__ == "__main__":
    unittest.main(verbosity=2)
