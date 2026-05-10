# Output Checklist — Quality Gate
*Apply before marking any deliverable as "done." This is the Supervise layer.*

## When to apply
- Before any output file is finalized (reports, comms, analyses, docs)
- Before any message is sent to a stakeholder (Slack, email, Confluence)
- Before any pipeline output is published (snippets, articles, sync runs)
- Before any knowledge asset is finalized (Claude Chat skills, reference docs, FAQ content)

## Which sections apply?

Not every output type needs every section. Use this guide:

| Output type | Sections to apply |
|---|---|
| **Stakeholder comms** (Slack, email, Confluence) | 1, 2, 3, 4, 5, 6, 7, 8 (all) |
| **Pipeline outputs** (snippets, drafts, sync runs) | 1, 4, 5, 6, 7, 8 |
| **Knowledge assets** (skills, reference docs, FAQ content) | 1, 4, 7, 8, 9 |
| **Internal docs** (plans, specs, analyses for the controller only) | 1, 4, 7, 8 (+ 5 if doc contains terminal-rendered templates) |
| **File renames, moves, or deletes** | 10 |
| **Architectural fixes that kill a pattern** (stale directive, deprecated flag, removed file, changed API/render path) | 11 |
| **Audits, retros, attacker tests** (any task that produces a findings list) | 1, 4, 7, 8, 12 |
| **Cross-script patches claiming symmetry** ("X is now symmetric with Y", sibling hook/script fixes) | 13 |
| **Status-check claims based on memory or state-file descriptions** ("is X done?", "is Y pending?") | 1, 4, 14 |
| **Public-facing repo writes** (commits to any public-facing repo or distributed artifact) | 1, 4, 15 |
| **Multi-image review tasks** (slide decks, design boards, screenshot batches for critique) | 1, 4, 7, 8, 16 |
| **Council-memo / shared-stakeholder paste content** (action-plan recaps for cross-stakeholder forums) | 1, 2, 4, 17 |
| **Matcher / parser / validator code** (substring vs structural assertions) | 18 |
| **Reading bundles** (HTML deliverables compiled from MD source — retro reviews, walkthrough decks, multi-doc compilations) | 1, 4, 19 |
| **Long-lived sprint branch merges** (state files modified across multiple phase-close commits over multiple sessions) | 1, 4, 20 |

## The checklist

### 1. Team Lead framing
- [ ] **Insight first** — leads with the pattern and the "why," not just the observation
- [ ] **Proactive** — anticipates what the recipient will need next
- [ ] **Ownership** — the controller owns the recommendation; decision-maker owns the decision
- [ ] **Elevating** — makes the recipient's job easier, not harder
- [ ] **Neutral tone** — no emotional qualifiers ("entirely from scratch," "first-ever"), no narrative arcs ("emerged as," "took on increasing"), no superlatives. State what was done and what it achieved — let the facts carry the weight.

### 2. Stakeholder match
- [ ] Communication style matches the target (manager / product leader / Product Support & Engineering lead / team async) per `communication-style.md`
- [ ] Tone and length are calibrated — no over-explaining, no under-specifying

### 3. Sign-off flags
- [ ] Any item requiring a manager, product leader, Product Support & Engineering lead, or senior stakeholder sign-off is explicitly flagged — not implied
- [ ] Sign-off scope is specific (what exactly needs approval, not "please review")

### 4. Ready-to-use criteria
- [ ] Can be shared or acted on without further editing
- [ ] Decision is made or clearly framed for the reader
- [ ] Action items are numbered, specific, and owned
- [ ] No gaps that require the controller to fill in before sending
- [ ] Any claims about external system state (API keys, credentials, live services, file contents, test results) were verified directly — not inferred from conversation history

### 5. Format and platform
- [ ] Output format matches the destination (Slack markup, GDoc-safe content, Confluence, markdown)
- [ ] No markdown tables in GDoc-destined content (use numbered lists or prose)
- [ ] Slack messages use correct formatting (`*bold*`, `_italic_`, `<@USER_ID>`, `<url|text>`) — applies to copy-paste drafts for any Slack context
- [ ] **Sending Slack messages via the MCP plugin** (`slack_send_message`)? Use **standard markdown** (`**bold**`, `_italic_`) — the tool converts to Slack mrkdwn at send time. This is the **opposite** of the copy-paste draft rule above. Italic + strikethrough are the same in both dialects; only bold needs conversion (`*single*` → `**double**`). See root `LEARNINGS.md` entry 2026-04-14 "On Slack MCP tool vs Slack-native mrkdwn — opposite markdown conventions".
- [ ] **Slack code-block tables (triple-backtick monospace):** use **4–5 spaces minimum between columns**, not the 2–3 that work in a terminal. Pad short column headers (e.g. `Me`) so the column width is anchored. Slack's proportional layout around the code block makes terminal-tight spacing read cramped. See root `LEARNINGS.md` entry 2026-04-14 "On Slack code-block tables — terminal-tight spacing reads cramped in Slack".
- [ ] No `~` used as "approximately" in Slack messages (Slack interprets `~` as strikethrough — use "approx." instead)
- [ ] Slack section breaks use a zero-width space (U+200B) on its own line — regular blank lines are collapsed
- [ ] Slack `<url|title>` links have titles sanitized — strip `< > | &` characters from dynamic content to prevent broken links
- [ ] Terminal code blocks with emoji/unicode: verify display widths with `unicodedata.east_asian_width()` — never guess column widths for `🤍`, `•`, `·`, box-drawing chars, etc.
- [ ] Fixed-width boxes with dynamic content (LLM-generated text, variable-length strings): padding must be calculated at render time, never hardcoded in a template. Static templates only work when all content has constrained length.
- [ ] ASCII art or text with backslashes (`\`), asterisks, underscores, or brackets: must be inside a code block (backtick-fenced). Claude Code renders non-code-block output as GFM markdown, which interprets `\_` as an escape sequence — `(\_/)` becomes `(_/)` outside code blocks.
- [ ] Skill or agent rendering output via the Bash tool (card, ASCII art, box-drawing, diagram): **do NOT render via the agent's Bash tool at all.** The "render via Bash + paste in a code block" rule (documented here until 2026-04-11) is superseded — it doubles the render in the UI, because the top of the Bash output leaks past the ~3-line auto-collapse threshold and the pasted code block produces a visible second copy. Instead, use the **Write-trigger hook pattern**: agent Writes a spec JSON to `/tmp/<feature>-spec.json` → a `PostToolUse:Write` hook matches that path, runs the renderer, unlinks the spec file (consume-on-read), and injects the rendered output as `additionalContext` with a `<MARKER>` discriminator → agent pastes the injected block per the literal passthrough rule. Zero Bash chrome, single render. Reference implementation + the full lineage that got us here: `LEARNINGS.md` "On render lineage iteration 4 — hook-side render generalizes to agent-context cards via a Write-trigger."

### 6. Subagent drafting quality
- [ ] Subagent prompts include the **raw source document**, not a summary — summaries lose domain-critical details
- [ ] Every Confluence draft includes a **"Workflow Impact" section** — the value-add over customer-facing changelogs
- [ ] Items needing sign-off are in a **"Needs Confirmation" section**, not buried in the draft body

### 7. LEARNINGS cross-check
- [ ] Checked root `LEARNINGS.md` for any applicable lessons
- [ ] Checked workspace `LEARNINGS.md` (if it exists) for domain-specific traps
- [ ] No known pitfalls repeated

### 8. Scope and boundaries
- [ ] Stays within the controller's visibility boundary (only references internal AI infrastructure where the controller has direct visibility, etc.)
- [ ] Does not act unilaterally on decisions that belong to a manager or other decision-makers
- [ ] Public-facing and stakeholder-facing outputs draw only from shareable content; private-workspace material stays in its workspace

### 9. Knowledge asset quality (skills, reference docs, FAQ content)
- [ ] **Grounded** — every claim is traceable to a source (Confluence page, LEARNINGS.md, validated edge case). No hallucinated features or procedures.
- [ ] **Gaps flagged** — anything the source material didn't cover is explicitly noted as a gap, not silently filled with assumptions
- [ ] **Word budget** — file stays within its target word count (if one was set). Distilled, not exhaustive.
- [ ] **Cross-references valid** — all referenced files, sections, or templates actually exist (e.g., routing table references match real filenames)
- [ ] **Templates complete** — any output templates are paste-ready with no placeholder text (except intentional `[fill in]` fields)
- [ ] **Self-contained** — each file can be understood without reading the others. No implicit dependencies or assumed context.
- [ ] **Maintenance path clear** — it's obvious how to update the content when the source material changes

### 10. File rename / move / delete — dependency graph check
- [ ] **Full grep** — searched the entire workspace root for the old filename/path (not scoped to CWD)
- [ ] **Triage every match** — each result explicitly categorized as "active instruction file → update" or "historical record → leave"
- [ ] **All active references updated** — every CLAUDE.md, CONTEXT.md, settings.json, hook script, and other live instruction file points to the new name/path
- [ ] **Re-grep verification** — re-ran the search from workspace root after updates; zero active references to the old name remain
- [ ] **Old file removed** — deleted or git rm'd the old file (no orphaned duplicates)

### 11. Post-architectural-fix scope audit — grep for the killed pattern
Fires when a fix kills a pattern: a stale directive, a deprecated flag, a removed render path, a changed API, a removed file, a superseded heuristic. Cheap insurance against the pattern living in a second layer you didn't edit. Reference: `LEARNINGS.md` "On post-architectural-fix scope audit" + "On false-dichotomy framing when iterations rhyme" (both 2026-04-11).

- [ ] **Identify the syntactic signature** of the killed pattern — the literal string, path, flag name, or command that future readers or agents would grep for if they were looking up the old way
- [ ] **Run `grep -rn '<signature>' .` from the project root** (not scoped to the file you edited)
- [ ] **Triage every match into exactly one of two buckets:**
  - (a) **Historical reference** — log entries, commit messages, LEARNINGS.md narratives, CHANGELOG lines, retro notes, session-log entries. Describe the past → leave alone (preserves debugging record).
  - (b) **Active instruction** — CLAUDE.md files, SKILL.md, output-checklist.md, hook scripts, agent protocols, live config files, live README content, anything currently read as directive or documentation. Update to match the new reality.
- [ ] **Each match landed in exactly one bucket.** "I'll assume it's historical" is how the bug comes back. Read until you can categorize.
- [ ] **Re-grep verification** after updates — zero active-instruction matches for the old signature remain
- [ ] **Consider the framing trap** — if you're on iteration ≥3 of a fix and the failures have been rhyming (collapsed / misaligned / doubled / partially visible), the reframe is "what shared precondition causes all of these?", not "what's the next knob to turn" (see "false-dichotomy framing" LEARNINGS entry)

### 12. Triage completeness — audits, retros, and attacker tests
Fires when the output is a findings list (adversarial audit, P10 retro, attacker test, gap analysis). Narrative completion ("the summary sounds good") is a weaker signal than triage completion ("every item has a status"). Reference: `agent-protocols.md` "Triage completeness rule" + adversarial audit meta-findings.

- [ ] **Every finding has a terminal status** — `fixed`, `deferred — <reason>`, or `rejected — <reason>`. No finding is left in limbo.
- [ ] **Status assignments are explicit, not implied** — a finding that appears in a "fixed" section but was never explicitly marked is not triaged. Say it.
- [ ] **Deferred items have a concrete destination** — "deferred" without naming *when* or *what session* is not a real deferral. Name the session, the retro, or the design doc.
- [ ] **Narrative-completion drift check** — before presenting a summary, count: total findings vs. statused findings. If they don't match, you're stopping early. Log `[drift-risk]` to session-log.md.

### 13. Cross-script symmetry claims — verify ALL changed properties
Fires when a CHANGELOG or commit message claims "X is now symmetric with Y" or "Z already does this; now symmetric." Partial symmetry claims ("one property matches → therefore symmetric") are how the scope-symmetry family produces next-session failures. Reference: `LEARNINGS.md` "Scope-symmetry family — partial symmetry claim."

- [ ] **Enumerate ALL changes** made to the reference script (Y) — not just the one you verified
- [ ] **Check each change individually** in the target script (X) — presence of one does not imply presence of others
- [ ] **Do not write "now symmetric" until the full change set is confirmed** — partial matches produce false assurance

### 14. Verify to the artifact, not a surrogate
Fires when answering status-check questions ("is X done?", "is Y still pending?", "did Z ship?") based on memory or state-file content. Memory entries and state files (CHANGELOG, CONTEXT) describe artifacts — they are not the artifact. For done/not-done claims that shape the next action, verification must drill one more layer. Sub-family count is now 10 across distinct shapes; all 10 share the same root: trust a summary, skip the artifact open.

- [ ] **Identify the deepest available source** — if the claim is about an artifact (file, commit, draft, shipped doc, DM, spec), that artifact is the deepest source; CHANGELOG/CONTEXT/memory are surrogates
- [ ] **Read the artifact before confirming status** — not the CHANGELOG line that describes it, not the memory entry that mentions it
- [ ] **Memory claims under challenge get artifact-depth verification** — re-reading CHANGELOG is not sufficient when the claim has been challenged; open the artifact itself
- [ ] **Status hedges get verified** — "pending [future action]" phrases in any past-session-authored source are treated as stale until confirmed against the artifact at current read time
- [ ] **Two-file artifacts get both layers checked** — public-file shipped ≠ private-spec internals (DM draft, sub-section state) complete; check each layer separately
- [ ] **Placement / ordering / layer decisions on public-facing storytelling surfaces** (README, public CLAUDE.md, agent cards, workspace maps) — before authoring, grep design docs and governance docs for prior-art decisions on the same entities. Prior-art is the artifact; assumption is the surrogate.
- [ ] **Routing-authority surrogate** — before flagging a data / system / report / integration ask to a specific named person, verify ownership of the underlying artifact or system. Role-in-team is a surrogate; artifact ownership is the real routing key. Default to "flag as unclear owner" when uncertain — never fabricate a routing key.
- [ ] **Proposals-file lifecycle drift** — at any retro § triage AND at sprint or multi-session execution-arc close that delivers `approved` Teacher proposals, verify proposals-file `Status:` field against execution reality before declaring the ritual closed. The retro table and sprint scoreboard describe state; the proposals file IS the lifecycle-of-record.
- [ ] **Running-agent-claimed-state surrogate** — when diagnosing OR taking over from another concurrent / prior session, never trust that session's task panel as authoritative. Internal `✔ done` markers reflect intent + tool-call attempts during conversation, but are never re-grounded against the filesystem. Open `git status` + `git diff HEAD` + the actual files the agent claims to have written, before trusting any reported chain step.
- [ ] **Carry-forward-sketch surrogate** — when session-log / CHANGELOG / focus-chain / `.remember/remember.md` references "N options sketched" (or "axes drafted," "frames considered"), the sketches themselves must exist as a tracked artifact (`_designs/<date>-<topic>-sketch.md` or `.claude/sketches/<date>-<topic>.md`) before P9 close. State-file prose describing-sketches is a surrogate; the sketch file IS the artifact.
- [ ] **Post-Luma-verdict surrogate** — Luma verdict files describe the recommendation; implementation is downstream. At any session that closes a Luma-verdict-driven implementation arc, run a verdict-to-code grep — does every named field/condition/gate-clause from the verdict appear in the implementation? "Frame N spec implemented" is satisfied only when each verdict-named element has corresponding code, not when the implementation broadly resembles the frame's name.
- [ ] **Attribution-conflation surrogate** — when authoring externally-bound paste-text that names a stakeholder as raising / proposing / owning / surfacing a topic, the artifact of attribution is the originating message (thread of record, council meeting notes, decision DM, focus-chain entry where the topic was first surfaced), NOT the cadence / forum / standing meeting where the topic later surfaced or got recapped. Cross-check session-log / source-channel / council notes / focus-chain BEFORE shipping the attribution claim.

### 15. Public-facing repo writes
Fires when committing to any public-facing repo on the controller's behalf. Two independent properties gate whether attribution is controller-authentic AND whether GitHub accepts the push. Reference: `LEARNINGS.md` on GitHub email-privacy push rejection (extends scope-symmetry partial-verification territory).

- [ ] **`git config user.email` resolves to one of the controller's addresses** — guards against the default agent email leaking "this was an agent commit, not human-authored" into public history
- [ ] **The address is either (a) verified+public on the controller's GitHub account OR (b) the GitHub noreply** (`NNN+<handle>@users.noreply.github.com`) — guards against GitHub's email-privacy rejection even when the email is authentic. Prior-commit-history consistency is informational only — a repo that accepted a real address on prior commits may reject the next one if GitHub account-level privacy settings tightened
- [ ] **Safest default: noreply** for any new repo or any repo where the controller hasn't explicitly chosen. Real-email attribution is opt-in per-repo
- [ ] **On push rejection** — if GitHub rejects with "email privacy restrictions" or similar, fix via: `git config user.email <noreply>` + `git commit --amend --no-edit --reset-author` + re-push. Amending an unpushed commit is safe (the "prefer new commit over amend" rule protects published history only)
- [ ] **5-point pre-push verification checklist for agent-portrait + asset shipping:** before pushing any commit that introduces or updates a character portrait, group photo, or referenced asset in a public-facing repo, verify all 5 properties explicitly:
  - **(a) Image variant matches selection** — the asset uploaded is the locked selection, not an earlier draft variant. Cross-check selection note in session-log / spec against the file uploaded.
  - **(b) Portrait referenced in agent `.md`** — the agent file has an inline `![<name>](<relative-path>)` embed; path resolves correctly from the `.md`'s location.
  - **(c) README updated if group-photo or new agent introduced** — the repo README's grouping reflects the new agent or composition; no stale lineup text.
  - **(d) Portrait in correct folder** — character portraits live under `assets/`; the agent `.md` references via relative path. Exception: per-agent assets that are NOT the primary portrait may live next to the `.md`.
  - **(e) Group-photo embedded inline in README, not just referenced** — any group composition has `![<name>](assets/<name>.png)` embedded directly in README prose, not merely named as a caption elsewhere.

### 16. Multi-image / multi-screenshot review discipline
Fires when ≥2 images are provided for review (sample slides, screenshot batches, design mocks, layout audits, photo critiques, image grids). Multi-image review is an **input-side trigger** for the retry-loop family — distinct from but adjacent to the state-write-side rescue-pattern family.

- [ ] **One Read call per image** — never parallel-Read multiple images in a single tool block; never batch-Read a deck before per-image grounding lands. Each image gets its own Read.
- [ ] **One observation block per image** — ground each image's verdict in prose before moving on; do not emit a synthesis summary before per-image observations land. The per-image verdict is the artifact; the synthesis is downstream.
- [ ] **Pause for the controller's signal between images on critique-shaped tasks** — slide reviews, design reviews, layout audits, screenshot critiques. Default cadence: wait for "next" / "go" / "continue" / redirect. Continuous-mode requires explicit prior authorization ("read all 5 in sequence").
- [ ] **Exception — single-image text extraction is not "review"** — lifting a screenshot's text content for a downstream task, scanning a diagram for a code reference, or any non-critique image use is one Read + use. The rule fires on critique-shaped tasks where per-image verdicts compound.

### 17. Council-memo discipline
Fires when authoring pasteable action-plan content for shared council/stakeholder memos (council recaps, action-plan memos to manager + cross-stakeholder leads, shared-doc council content). Council memos are read by 8+ council members + manager + cross-stakeholder leads — voice register and accountability surface decisions that don't apply to direct 1st-person sends or experiential peer comms.

- [ ] **3rd-person controller voice for shared council/stakeholder memos** — pasteable action-plan content uses third-person voice ("[Controller] will…", "[Controller] owns…", "[Controller] + manager aligned on…"), NOT first-person ("I'll…", "I own…"). Distinct from the spokesperson rule (which keeps body in 1st-person voice for direct sends-on-controller's-behalf — see communication-style.md). Sub-rules: (a) action items use 3rd-person; (b) accountability claims use 3rd-person; (c) recaps of decisions use 3rd-person.
- [ ] **Owner matches surface domain** — when naming the lead/owner for an action item in a council-memo paste, the owner name must match the EXACT surface the item touches. Don't pad with adjacent org leads or "reasonable-reviewer-pool" co-owners. Surface map (placeholder shape — fill with the controller's actual org map): `[product domain] → [product lead]`, `[knowledge base structural] → [KB co-owner]`, `[AI chatbot / technical pipeline] → [AI Ops lead]`, `[strategic / sign-off] → [manager]`, `[process triage / cost-estimation] → [process collaborator]`, `[internal tooling] → [tooling owner]`. Council-memo paste rosters favor minimum viable accountable owner over reasonable-reviewer-pool.

### 18. Matcher discipline — structural over substring
Fires when authoring code that asserts or matches on text content — production hooks, validators, parsers, audit assertions, test assertions. Substring matchers fire on the matched vocabulary anywhere in the text — including body prose, educational explanatory text, legend tables, fenced code blocks that QUOTE the schema, and self-referential documentation. Structural matchers (column-delimiter context, semantic API against parsed structure, anchored regexes that include surrounding-context guards) only fire on the structural region. Family n=3 strict cross-layer (validator + hook + audit-test) confirmed; cumulative n=5 at adjacent shapes.

- [ ] **Identify the matched vocabulary's surfaces** — does the matched string appear in MORE places than the structural region your matcher is meant to fire on? Check: legend tables, explanatory body prose, README snippets, fenced code blocks that quote the schema, self-referential rule citations, comment headers, educational text in commit messages, test fixtures that mention the format.
- [ ] **Use column-delimiter context for table-column matches** — `assertIn("| 🔴 SILENT-CANDIDATE |", report)` not `assertIn("🔴 SILENT-CANDIDATE", report)`; pipes anchor the column boundary. Symmetric tightening (matched `assertIn` + `assertNotIn` pairs) is the canonical fix shape.
- [ ] **Use semantic API against parsed structure when available** — `by_hook[name].flag != SILENT_CANDIDATE` over substring matching against rendered output. Parse-then-assert beats render-then-substring-match on every axis (correctness, refactor-tolerance, encoding-resilience).
- [ ] **Anchor regexes with surrounding-context guards** — `^- ` for list-item prefix not just `bullet`; column-anchored not body-anchored; structural-region context required not just substring presence.
- [ ] **Test-side coverage requirement** — when authoring tests for any matcher fitting the above, include adversarial inputs that contain the matched vocabulary in body prose / fenced code / quoted schema. The structural-vs-substring failure mode (gate-logic-layer family) is a known anti-pattern; tests must explicitly cover the structural-region boundary.
- [ ] **Sibling family — case-sensitive grep as hidden contract** — `grep -c '^\[Pn\] X'` patterns where capital-vs-lowercase reads identically to humans but silently fails the gate. Use `grep -ic` for case-insensitive matching when the human-readable contract isn't case-sensitive.

### 19. Reading-bundle rendering
Fires when shipping a Reading bundle (HTML deliverable compiled from MD source — retro reviews, council memos, walkthrough decks, multi-doc compilations).

- [ ] **Identify the artifact's edit-locus:** does this get re-edited after creation, or is it a frozen consumption surface? (binary predicate)
- [ ] **Class assignment + format:** Reading bundle (zero post-create edits, often shared) → HTML in `_artifacts/`. Source-of-truth (continuous edits, VC, grep-targeted, agent-read) → MD where appropriate (`_designs/`, `_retro/`, root state files). Hybrid (MD canonical edited + HTML view regenerated) → MD source + HTML render.
- [ ] **For Hybrid artifacts:** edit ONLY the MD canonical; regenerate HTML render on meaningful change. Never edit the HTML directly — canonical is source, HTML is derivative.
- [ ] **Tooling:** ad-hoc Python+pandoc for n=1 instances; promote to scripted `_config/scripts/md-bundle-to-html.py` at n=2.
- [ ] Reference: `CLAUDE.md` "Deliverable format convention" section.

### 20. Long-lived branch merge discipline
Fires when merging a sprint branch >1 day old that touches state files (CHANGELOG / CONTEXT / LEARNINGS) across multiple phase-close commits.

- [ ] **For sprint branches > 1 day touching state files across multiple phase-close commits:** rebase against main pre-merge to surface conflicts incrementally, not all at once at merge time.
- [ ] **State-files-FIRST close-out doctrine remains load-bearing** — don't defer state-file writes to AFTER merge; the close-out-ordering rule still binds.
- [ ] **Watch:** n=2 recurrence on next worktree-based sprint triggers structural-fix consideration (PreToolUse hook detecting long-lived state-file divergence?).
- [ ] Reference: `.claude/teacher-proposals.md` "Long-lived sprint branches state-file conflict pattern" + the controller's accept gate.

## How to use this checklist
- **Self-review**: Before finalizing, run through the checklist mentally or explicitly. Flag any item that fails.
- **Self-correction**: If an item fails, fix it before marking done. Do not ship with known failures.
- **If unsure**: Surface the uncertainty to the controller rather than guessing.

## This checklist evolves
When a new pattern, trap, or quality standard is identified, add it here. This is a living document — the Supervise layer only works if it stays current.
