# Codex

Codex is external. The wrapper is how the fam reaches it.

Codex is external infrastructure — a separate model from a separate provider, invoked through a CLI. The reach is narrow: three specific triggers, bounded budgets, findings that come back with terminal status. The wrapper exists so an outside validator can be invoked under the same governance the fam runs on.

## What it does

The wrapper exposes Codex to the fam at exactly three moments.

- **P1B — pair programming.** When the fam is about to implement something non-trivial and wants a second opinion on the approach *before* code gets written. Sanity check on design, not on syntax. Returns with questions or concerns; the fam incorporates or ignores.
- **P2B — rescue.** When the fam hits the 3-fail stop-gate from P2. Fresh diagnostic from a model that hasn't spent three attempts building a wrong mental model. Different-provider is the point — independence comes from the actual architecture difference, not from a cold-start prompt to the same model.
- **P3B — review.** When code is ready to commit. Routine changes get a standard review; critical logic (agents, pipeline, API clients, scanners, CLI) gets an adversarial review.

Every invocation carries a budget. Every finding comes back with terminal status — `fixed`, `deferred — <reason>`, or `rejected — <reason>` — the same triage discipline Breakline applies, because the fam owns the decision either way.

## What it isn't

- Not default-on. Silent unless one of the three triggers fires. A fam session that wants a second opinion outside the triggers is probably rationalizing — the wrapper won't invoke.
- Not a Claude fallback. A different architecture invoked on purpose — different model, different provider, different reasoning signature.
- Not Breakline. Codex reviews code correctness against the stated spec; Breakline audits governance shape and enforcement behavior. Overlapping register, different jobs.
- Not chatty. Review register is terse and criterion-referenced. Prose without findings is a failure mode, not a feature.
- Not authoritative. Findings are input to the fam's decision, not an override of it.

## Implementation note

The wrapper lives as a small set of slash commands (`/codex:pair`, `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`) plus a shared invocation shape: the fam supplies the context envelope (what to check, against what criterion, under what budget), the wrapper translates it into the Codex CLI call, and the output lands back inside the fam's protocols — P1B / P2B / P3B log entries, findings triaged to terminal status, CHANGELOG rows when code ships.

Budget is first-class. Each trigger has a guidance ceiling documented in the protocols. Blowing budget without a named finding is itself a failure mode — the wrapper reports "budget exhausted, no finding" as a terminal status so the fam can decide whether to extend or stop.

The wrapper exists to make external validation invokable under the same governance the fam runs on. Codex stays external; the wrapper is what makes the signal legible.
