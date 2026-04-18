# Deputies

![Deputies](../../assets/deputies.png)

The fam's delivery pool — one entity, many instances, gone as soon as the work lands.

Deputies are how the fam gets work done. The pool is the character; any specific deputy is an instance — an implementer, a reviewer, an explorer, a scanner, an agent-typed specialist — dispatched for a single task with a fresh context window and nothing else. They return status in one message and are gone.

## What they do

A deputy receives three things and nothing else: a task brief (what to do, against what criterion, with what constraints), a context envelope (the code, files, or prior findings the task needs), and a return format (terminal status, findings shape, commit discipline if applicable). Zero session history, zero inherited assumptions, zero backchannel — every deputy starts cold.

They're dispatched for four kinds of reasons:

- **Parallel work.** Independent tasks that can run at once without sharing state — survey three tracks, run four reviews, gather context from four unrelated files. Deputies are the mechanism that keeps parallel actually parallel.
- **Context protection.** Tasks that would drag heavy output into the main session — long file reads, long search results, long test runs. A deputy absorbs the output and returns only the findings. The controller's context stays clean.
- **Specialized register.** Tasks that need a voice or discipline the controller's register doesn't match — Luma for decision-shaping, Breakline for adversarial audits, the Codex wrapper for external validation. A deputy in that agent shape is the right vehicle.
- **Discrete implementation.** Well-defined specs where the controller wants fresh eyes executing. An implementer deputy takes the task, returns a commit + tests + self-review, and hands back to the controller for acceptance.

For code work, the fam uses a two-stage review pattern: implementer writes and tests; spec-reviewer deputy verifies the implementation matches the spec; code-quality deputy reviews craft. Each review is its own dispatch — fresh eyes, fresh read. Findings return with terminal status — `fixed`, `deferred — <reason>`, or `rejected — <reason>`. The controller decides accept, reject, or fix.

## What they aren't

- **Not persistent characters.** Each deputy exists for one task. When the task returns, the deputy is gone. No deputy has a name, a voice, or a history. The pool has the character; individuals don't.
- **Not autonomous.** Deputies execute the brief the controller writes. A thin brief produces a thin result. Brief construction is the controller's job and the highest-leverage move in the whole pattern — a precisely-scoped deputy with the right context succeeds; a vague one rationalizes.
- **Not a shared-state pool.** Deputies don't know about each other. Task 1's deputy doesn't inherit from Task 0's. Coordination between deputies is a controller orchestration problem, not a deputy problem.
- **Not a replacement for controller judgment.** Deputy output is input to the controller's next move — findings to triage, code to commit, questions to answer. The controller owns the decisions either way.

## Implementation note

Deputies are dispatched via the Agent tool with `subagent_type` + `prompt`. Named types in this repo map to fam roles (Luma, Breakline, the Codex wrapper via its slash commands); unnamed dispatches default to a general-purpose deputy for arbitrary task work. The brief is the entire payload — no shared instructions, no working-directory assumptions, no session memory.

Output lands back as a single message in the controller's next context window. That message carries the deputy's full return: findings, status, commit SHAs, next-step recommendations. The controller reads it, triages, and either incorporates the result or re-dispatches with tightened scope.

The pattern that makes this work is brief craft. A good deputy brief reads like a briefing to a skilled colleague who just walked into the room with no prior context: the goal, the constraints, what's been ruled out, what success looks like. The brief is where the fam's intelligence lives; deputies are the execution surface.