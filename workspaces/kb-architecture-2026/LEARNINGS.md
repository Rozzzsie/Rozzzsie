# LEARNINGS — KB Architecture 2026

Non-obvious insights about KB content drafting, GDoc formatting, and the
way subagent-driven batches behave in this workspace.

---

## On subagent-driven content drafting

**2026-03-31**

First use of subagent-driven development for a content drafting session
(a Snippet Library build of 37 snippets across 8 buckets). Each bucket was
dispatched to a fresh implementer agent with isolated context, followed by
two-stage review (spec compliance + content quality).

**What worked well:**
- Fresh context per bucket prevented drift — Bucket 8 was as clean as Bucket
  3, despite being drafted hours later.
- Two-stage review caught issues at different levels: spec review caught
  format/rule violations (sales language in a Customer-Facing Response),
  content review caught realism issues (unrealistic Q&A phrasings, Bot Action
  mismatches).
- Early buckets (1 and 2) absorbed most review findings — 8 fixes total.
  Buckets 3–8 all shipped clean on first review. The implementer agents
  learned from progressively better-crafted prompts.
- Parallel review dispatch (spec + content simultaneously) saved time
  without sacrificing quality.

**What to watch for next time:**
- Some implementer agents updated CONTEXT.md and CHANGELOG.md mid-session
  without being asked — this created partial state entries that had to be
  cleaned up. Add explicit "Do NOT update CONTEXT.md or CHANGELOG.md" to
  every implementer prompt (fixed partway through this session).
- The first two implementer prompts were underspecified on Bot Action values
  — later prompts included exact values per snippet, which eliminated
  mismatches. Front-load the specifics.
- Content quality review is more valuable than spec compliance for content
  drafting — spec compliance catches format issues, but content quality
  catches the things that matter for real ticket resolution.

**Implication:** subagent mode is well-suited for large-batch content
drafting where each unit is independent. Key: craft implementer prompts that
include exact snippet-level specs (title, Bot Action, key facts, scope
boundaries) rather than leaving the agent to infer from general context.

---

## On dual-audience snippet design (human + AI chatbot)

**2026-03-31**

Adding a dedicated AI-chatbot section to every snippet — with a Customer-
Facing Response and a Bot Action — was a design-time decision that added
~5 lines per snippet but will save significant rework when the AI chatbot
integration begins. The key insight: Technical Notes are written for human
agents (detailed, references internal docs, operational language) while
Customer-Facing Responses must be plain language a bot can deliver verbatim.
These two audiences need materially different content, not just different
formatting.

The Bot Action field (`Answer directly` / `Acknowledge + collect info` /
`Acknowledge + escalate`) prevents the bot from confidently answering a
snippet that should trigger escalation, and prevents unnecessary escalation
of things the bot could handle alone. One snippet (the escalation snippet)
carries a conditional Bot Action — two categories, two actions.

**Implication:** when drafting any future KB content, always include the
AI-chatbot section from the start. Retrofitting it later means re-reading
every snippet to determine the right Bot Action and write a plain-language
response — essentially double the work.

---

## On Google Docs API formatting — build from a reference, not from scratch

**2026-04-01**

Writing formatted content to Google Docs via the API consumed the majority
of a single session. What should have been a straightforward "parse markdown
→ write to GDoc" task turned into 10+ iterative cycles of write →
screenshot → fix → rewrite. The core problem: we built the formatter
speculatively and iterated visually, instead of reading an existing
reference document programmatically first.

**Specific traps:**

1. **Document-level named styles differ between GDocs.** Two different
   product docs had different NORMAL_TEXT defaults (different spaceAbove,
   spaceBelow, and lineSpacing). Paragraph styles that look right in one
   doc look wrong in another. Always read the target doc's named styles
   before writing.

2. **`updateParagraphStyle` with a fields mask can reset unrelated fields.**
   Setting `fields: "indentStart,indentFirstLine"` caused `spaceAbove` and
   `spaceBelow` to reset to 0. The fix: always explicitly include fields
   you want to preserve.

3. **`weightedFontFamily.weight=400` undoes `bold=True`.** The Docs API
   treats font weight and bold as related — setting weight=400 (Normal)
   clears bold. Fix: always apply bold AFTER setting font family, not
   before.

4. **Tables inject a ghost paragraph.** `insertTable` creates an empty
   paragraph before the table that cannot be deleted. It inherits
   surrounding styles, which can cascade unexpected font sizes. Fix:
   explicitly style both the ghost paragraph and the table cell text.

5. **Empty spacer paragraphs inherit doc defaults.** A `"\n"` paragraph
   inserted as NORMAL_TEXT uses the doc's NORMAL_TEXT style, not the
   surrounding content style. If the doc default has 12pt spaceAbove, every
   spacer adds 24pt of whitespace. Fix: apply explicit paragraph spacing
   to ALL NORMAL_TEXT, including empty lines.

**Implication — the correct workflow for GDoc formatting:**
1. Read the reference document's full structure via API (named styles,
   paragraph styles, text styles, table cell styles).
2. Read the target document's named styles to identify divergences.
3. Build the formatter to explicitly set every property that differs from
   the target doc's defaults.
4. Test on ONE snippet, read it back via API, diff against reference — do
   NOT rely on visual inspection alone.
5. Lock the format in a spec doc before batch-writing.

This workflow would have reduced the 10+ visual iteration cycles to 2–3
programmatic ones. Applies to any future GDoc formatting work.

---

## On loop detection — the GDoc formatting saga was a missing harness block

**2026-04-10**

Pressure-testing the Supervise layer against the "Harness Engineering"
framework (7 blocks for reliable agent execution) surfaced a gap: **loop
detection**. The system had no structural mechanism to detect when the
agent was retrying the same failing approach without progress.

In hindsight, the GDoc formatting saga (10+ visual iteration cycles of
write → screenshot → fix → rewrite) was exactly this failure mode — the
agent kept tweaking formatting parameters instead of stepping back to read
the reference document programmatically. A loop detection protocol would
have flagged this at attempt 3 and forced a fundamentally different
approach.

A loop-detection rule was added to the Supervise layer: at 2 failed
attempts, stop and re-read the failure signal. At 3 failed attempts, hard
stop — present a diagnosis + options to Rosie. No 4th attempt without new
direction or a fresh diagnostic from outside the session.

**Implication:** during future batch content drafting, if any formatting
or publishing step fails twice, treat it as a signal to change approach —
not to try harder at the same thing.
