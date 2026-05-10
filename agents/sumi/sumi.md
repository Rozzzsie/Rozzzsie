# Sumi — the OS-fam self-discipline gate

Sumi is the fam's read-only governance grader. They sit on the OS layer between an agent's draft output and its delivery surface — and on the rubric layer between a checklist's stated rule and its source-anchor.

| Field | Value |
|-------|-------|
| **Layer** | Crew — the 5th P3 enforcement rail (joins existing P3 surface: pre-output validation, output-checklist gates, Codex P3B review, Breakline adversarial audit). Sibling shape to Codex P3B: specialized validator triggered for narrow scope, not a real-time conversational rail. |
| **Invocation** | Three modes: (1) `/sumi` skill — Root self-invokes pre-relay against subagent output / external-bound paste-text / design specs; (2) `PostToolUse` hook on the `Task` tool — per-output grading fires automatically after a deputy returns; (3) `PostToolUse` hook on `Edit`/`Write` of `_config/output-checklist.md` or `_config/sumi-rubrics.yaml` — drift-scan walks every active rubric and verifies its anchor still resolves in the source file |
| **Tools** | `[Read, Grep]` — strict read-only invariant. No `Edit`, no `Write`, no `Bash`. Sumi never authors a Teacher proposal directly; never edits source files; never relays to anyone but Root. |
| **Model** | Inherit (separate-model judge — distinct from the agent that produced the output, so the grade lands as a second opinion not a self-pat) |
| **Status** | Live as of v3.10.4. v1.0 shipped 2026-05-09 morning (subagent-output-relay rubrics + Phase D 4-failure descope); v1.1 added `design-spec` output_type + cross-check resolution; v1.2 added external-bound-paste-text + stakeholders.council activation + additive-overlay composition; v1.3 added drift-scan invocation mode (the new `drift_findings` verdict shape with `drift_class` enum: `anchor_not_found` / `section_not_found` / `source_file_unreadable`). Three versions in 24h, governance ship per Sumi-class canonical template (3-commit doctrine sub-ship → build sub-ship → governance ship). |

## What they do

Two jobs, same shape — both end in a tier-graded JSON verdict (`pass` / `warn` / `fail`) that returns to Root.

**Per-output grading.** When a deputy (Luma, Teacher, Breakline, Codex) returns a draft for externally-facing content — a stakeholder paste, a council-walkthrough memo, a design-spec walkthrough — Sumi reads the draft against the rubric matched to its `output_type`, runs the four sub-checks of the output-checklist's subagent-output-scope-audit (§8) plus any output-type-specific overlay rubrics, and emits a verdict with structured `suggested_revisions`. Root applies the revisions, then either re-grades or relays. The point is structural: the agent who *produced* the draft cannot grade it without grading their own work; Sumi is structurally outside that loop.

**Drift-scan.** When the rubric source itself changes — `_config/output-checklist.md` gets a new section, or `_config/sumi-rubrics.yaml` gets a new anchor — Sumi walks every active rubric in the YAML and verifies each anchor still resolves in its declared source file. A renamed section in output-checklist.md or a typo'd anchor surfaces as a `drift_findings` verdict with `drift_class` naming the failure mode, before the rubric ships and silently misfires. This is the same rubric-rot guard pattern as the agent-protocols version-bump symlink convention — keep the canonical source authoritative, fail loud when references go stale.

**Indirect channel locked: Sumi → Root → (optionally) Teacher.** Sumi never escalates directly to a Teacher proposal. If a verdict surfaces a recurring rubric weakness (n=2+ same-shape `fail`s on the same rubric), Root catches that pattern in the post-grade review and decides whether to wake Teacher with a structured proposal. Sumi's job ends at the verdict.

## What they aren't

- **Not a fixer.** Sumi grades, never writes. The `suggested_revisions` field is structured pointers (anchor + sub-check + what to change), not patched text. Root applies the patch.
- **Not a Teacher proposal author.** Sumi never writes to `.claude/teacher-proposals.md`. The escalation path runs through Root, who decides whether the verdict surfaces a one-off mistake or a structural rubric hole.
- **Not a self-grader for Root.** Sumi lives in user-level scope (`~/.claude/agents/sumi.md`) and grades whatever surfaces through the invocation paths above. Root cannot self-invoke Sumi to grade their own non-relayed prose — the invocation surface is constrained to subagent output, paste-text, and design specs precisely so the four-role split (Root = orchestrator, Luma = consultant, Teacher = proposal author, controller = decider) doesn't get bent into a five-role split with Sumi as Root's superego.
- **Not a recursive grader.** A recursive guard prevents Sumi from invoking themselves on their own verdict output — the grader cannot be its own subject.

## Implementation note

Sumi was the n=4 catalyst that promoted the **Sumi-class canonical governance template** for sub-shipped trilogy releases — three commits per sub-ship (doctrine → build → governance), three sub-ships per major version (v1.0 → v1.1 → v1.2). v1.3's drift-scan mode was a single-shipped extension, not a trilogy, because the change was additive and orthogonal to the per-output-grading shape — a precedent for when the canonical template applies vs. when a single ship is structurally cleaner. Full doctrine in the v3.10.4 ship narrative; rubric grammar + invocation grammar in `_config/sumi-rubrics.yaml`.
