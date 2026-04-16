# LEARNINGS.md — Rozzzsie

Cross-workspace insights. Things that apply everywhere, not just one project.

---

## Demonstration vs guarding: mutually exclusive framings for pull-not-push artifacts

**2026-04-16**

Luma caught a single phrase in the fam debut design spec that contradicted its own thesis: *"without spoiling what makes it valuable."* The spec's thesis was pull-not-push — the artifact demonstrates the system by running it; what's not in the artifact isn't hidden, it's simply not the artifact. But "without spoiling" is defensive framing — it tells the reader the artifact is *less than* what the author has. Defensive framing and pull-creating framing can't both be true.

**Rule.** When an artifact's thesis is "pull, not push," the language must demonstrate, not guard. Scan every outward-facing paragraph for defensive patterns — "without revealing," "keeps X private," "limited version of," "doesn't include" — and rewrite to affirmative demonstration. Defensive phrasings signal you think the artifact is a fallback; affirmative phrasings signal you think the artifact *is* the artifact.

---

## Luma is for authoring-work axis, not just state-changing decisions

**2026-04-16**

Luma was originally shaped as a translator rail for state-changing decisions with 3+ real options. She got invoked three times against authoring work in the same day — the design spec framing, a character brief for one agent, and a character brief for another. Each invocation used the same brief pattern: declare controller's gut, explicitly ask for reframe not validation, enumerate axes the controller hasn't ruled out. Each invocation produced a pattern-level catch the controller would not have surfaced alone:

1. **Design spec §1:** `demonstrate-vs-guard` axis-flip. Draft used defensive framing that contradicted the spec's own pull-not-push thesis.
2. **Agent character brief #1:** `completeness-vs-shape` axis. Draft was mechanics-first; Luma reframed to shape-first. Without the reframe, downstream briefs would have been forced into a mechanics mold.
3. **Agent character brief #2:** `methodology-vs-character` axis. Draft read as "how audits work with his name stapled on." Luma reframed to lead with relationship to the fam.

All three were pattern-level errors — polished at the line level, wrong at the axis level. Option-ranking inside the wrong axis produces better wrong answers, not the right axis.

---

## Meta-review Luma is a third invocation shape

**2026-04-16**

After earlier Luma returned a tightening pass (line-level polish, no reframe) and the controller agreed with the draft, Rosie pattern-sensed the convergence felt too clean: "Please wake up Luma for this question." A **fresh Luma instance** was dispatched for meta-review on the combined earlier-Luma + controller reasoning — not on the artifact alone.

Fresh Luma caught what neither earlier Luma nor controller saw: **tagline-body contradiction.** The opener personified a wrapper as a fam member; the body argued it was a translation mechanism; the closing paragraph literally walked the tagline back. Two axes fighting inside one piece — invisible when each paragraph reads clean in isolation.

**Three valid output shapes:** (1) axis reframe — draft on wrong axis; (2) tightening pass — axis right, needs line edits; (3) meta-review — earlier Luma + controller converged too cleanly, fresh eyes on the *reasoning* catch what each pass alone cannot.

---

## External-resource-name-availability is a mandatory plan gate

**2026-04-16**

The implementation plan said: run `gh repo create Rozzzsie/Rozzzsie --public`. It failed instantly — that name was already taken by the private profile repo this whole working tree pushes to. The plan was self-reviewed, user-approved, and looked complete. But it prescribed an external create-call without first verifying the name was free.

**Rule.** Any plan step that calls an external create API must be preceded by a name-availability check step, and the check's expected output must be named in the plan. If the check surfaces an existing resource, the plan has a decision point — don't paper over it. Checking availability is one API call; the failure mode of colliding is unbounded.

This was a planning failure, not bad luck. We got a clean error; for a namespace with looser guarantees (a DNS A record, a storage bucket in some regions) the same pattern would have been destructive.

---

## P4 state writes default to session-start workspace context

**2026-04-16**

An entire initiative — 22 CHANGELOG entries, 20+ commits touching CONTEXT.md — was logged in the wrong workspace for ~10 hours of productive work. The session opened in one workspace for brainstorming; when the initiative pivoted to architecture work, state writes continued landing in the same workspace by inertia. The workspace mismatch went undetected until the next session.

**Rule.** New initiatives need an explicit workspace-assignment decision before the first state write — not after. The protocol says "update CONTEXT.md + CHANGELOG.md" but doesn't specify *which* — the implicit default (whatever's already in context) is the drift vector. When brainstorming pivots from one domain to another mid-session, pause and ask: "which workspace owns this work?"

The system caught its own mistake — but the fix was a 7-file migration that could have been a 0-file prevention.
