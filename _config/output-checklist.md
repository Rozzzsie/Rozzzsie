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
Fires when the output is a findings list (adversarial audit, P8 retro, attacker test, gap analysis). Narrative completion ("the summary sounds good") is a weaker signal than triage completion ("every item has a status"). Reference: `agent-protocols.md` "Triage completeness rule" + adversarial audit v2 meta-finding (2026-04-13).

- [ ] **Every finding has a terminal status** — `fixed`, `deferred — <reason>`, or `rejected — <reason>`. No finding is left in limbo.
- [ ] **Status assignments are explicit, not implied** — a finding that appears in a "fixed" section but was never explicitly marked is not triaged. Say it.
- [ ] **Deferred items have a concrete destination** — "deferred" without naming *when* or *what session* is not a real deferral. Name the session, the retro, or the design doc.
- [ ] **Narrative-completion drift check** — before presenting a summary, count: total findings vs. statused findings. If they don't match, you're stopping early. Log `[drift-risk]` to session-log.md.

## How to use this checklist
- **Self-review**: Before finalizing, run through the checklist mentally or explicitly. Flag any item that fails.
- **Self-correction**: If an item fails, fix it before marking done. Do not ship with known failures.
- **If unsure**: Surface the uncertainty to the controller rather than guessing.

## This checklist evolves
When a new pattern, trap, or quality standard is identified, add it here. This is a living document — the Supervise layer only works if it stays current.
