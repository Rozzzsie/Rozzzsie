# LEARNINGS.md — Rozzzsie

Cross-workspace insights. Things that apply everywhere, not just one project.

The most valuable five, curated. Earlier entries archived in private — what survives here is what generalizes broadest.

---

## Verify to the artifact, not to a surrogate

**2026-04-25 (extended through 6 sub-families)**

For any done/not-done claim, state-file reference, or "has this shipped" question that shapes a next action, verification must drill one more layer than feels sufficient — open the artifact itself, not the description of the artifact. Memory entries, CHANGELOG lines, CONTEXT claims, retro-candidate inheritance tables, sprint scoreboards — all of these *describe* artifacts, they are not the artifact. The pattern has produced six sub-families across nine days: status-check (memory says yes, the file says no), decision-making (memory says estimate, the live state says different), authoring-grounding (the source the draft cited isn't what the source says now), link-target (the URL points at the parent space, not the page), routing-authority (the role-in-team is a surrogate; artifact ownership is the real routing key), and proposals-file lifecycle (the retro § 9 triage table inherits from a prior retro's candidate list and silently misses proposals living in the proposals file outside the inheritance lineage).

**Rule.** Identify the deepest available source. If the claim is about an artifact (file, commit, draft, shipped doc, sent message, spec), that artifact is the deepest source; descriptors are surrogates. Read the artifact before confirming status. Memory claims under controller challenge get artifact-depth verification — re-reading the descriptor is not sufficient when the controller has pushed back on a memory-based claim. Status hedges in past-session-authored sources are treated as stale until confirmed against the artifact at current read time. Two-file artifacts get both layers checked separately. The retro § 9 triage table is itself a surrogate; the proposals file is the artifact for "what's open."

---

## Ship-validation gaps: clean-state baselines don't hold under real session load

**2026-04-23 (evening, after a primitive's first post-ship real session regressed 5×)**

A new architectural primitive shipped with an advertised baseline metric (a 65% reduction; 37s vs the 105s prior). The first post-ship real session on the same surface measured 3m 9s — five times the baseline, eight times the advertised target. Investigation: the hook itself ran in 73ms; the regression lived entirely in the synthesis the hook couldn't displace, amplified by adjacent state files the prior session had stuffed unbounded into the read source. The pattern itself didn't fail; what failed was ship-validation. The baseline was measured in a clean-state scenario and got stress-tested for the first time tonight under max-content load. Three simultaneous edge-case dimensions, never measured pre-ship.

**Rule.** *For new architectural primitives (patterns, protocols, hooks, libs) whose advertised value is a measurable metric (latency, token count, accuracy, fire rate): baseline numbers must be measured across at least three named edge-case scenarios before they enter protocol-doc language as load-bearing claims. Clean-state scenarios are a single data point, not a baseline. The enumeration of edge cases is itself a pre-ship artifact, reviewable at the controller's gate, and becomes part of the primitive's acceptance criteria.*

The single-number-baseline pattern was ergonomic but produced unearned doctrine claims. Distribution-reading (median + p95 + max) replaces it.

---

## Outside-lens diagnostics: when the inside lens converges, dispatch the outside

**2026-04-23 (morning, F2 pressure-test)**

After a startup-latency drift signal, the inside-lens diagnostic candidates were "measure first" and "reshape first" — both calibrated on the assumption that the bottleneck lived in compression of the loaded text. Luma reframed: that's a *timing* axis, not the load-bearing axis. The real axis was *inside-out vs outside-in* — what does an outside lens see that the inside lens has structurally been forced to ignore? Outside-lens here meant a deliberate caveman-compress pass on the three governance files: prose-tightness baseline against a known compression benchmark. Result: 2.3% avg compression versus the benchmark's 46%. The prose was already tight. **Retention, not compression, was the attack vector** — and that finding was inaccessible from inside the lens that had been counting bytes per paragraph all morning.

**Rule.** When the inside lens has converged on a small set of candidates and they all share an axis the controller didn't explicitly choose, that's a Luma category #4 signal — architectural design with 3+ forks, often manifested as *the option set sits on the wrong axis*. The intervention is not to rank inside the axis better; it's to dispatch a fresh perspective whose tooling forces it to look at a different axis. Outside-lens diagnostics are cheap (one fresh sub-agent invocation, scoped narrowly) and produce findings the inside lens cannot — by construction.

---

## Demonstration vs guarding: mutually exclusive framings for pull-not-push artifacts

**2026-04-16**

Luma caught a single phrase in a public-facing design spec that contradicted its own thesis: *"without spoiling what makes it valuable."* The spec's thesis was pull-not-push — the artifact demonstrates the system by running it; what's not in the artifact isn't hidden, it's simply not the artifact. But "without spoiling" is defensive framing — it tells the reader the artifact is *less than* what the author has. Defensive framing and pull-creating framing can't both be true.

**Rule.** When an artifact's thesis is "pull, not push," the language must demonstrate, not guard. Scan every outward-facing paragraph for defensive patterns — "without revealing," "keeps X private," "limited version of," "doesn't include" — and rewrite to affirmative demonstration. Defensive phrasings signal you think the artifact is a fallback; affirmative phrasings signal you think the artifact *is* the artifact. This was the first of three load-bearing axis-reframes Luma produced in the same authoring cluster — *demonstrate-vs-guard*, *completeness-vs-shape*, and *methodology-vs-character* now carry session-log machine tags as named axes.

---

## P4 state writes default to session-start workspace context

**2026-04-16**

An entire initiative — 22 CHANGELOG entries, 20+ commits touching CONTEXT.md — was logged in the wrong workspace for ~10 hours of productive work. The session opened in one workspace for brainstorming; when the initiative pivoted to architecture work, state writes continued landing in the same workspace by inertia. The workspace mismatch went undetected until the next session.

**Rule.** New initiatives need an explicit workspace-assignment decision before the first state write — not after. The protocol says "update CONTEXT.md + CHANGELOG.md" but doesn't specify *which* — the implicit default (whatever's already in context) is the drift vector. When brainstorming pivots from one domain to another mid-session, pause and ask: "which workspace owns this work?"

The system caught its own mistake — but the fix was a 7-file migration that could have been a 0-file prevention.
