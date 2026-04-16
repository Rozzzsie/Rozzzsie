# LEARNINGS — Cross-Team Docs Sync 2026

Non-obvious insights about the pipeline, the FAQ agent, and this workspace.

---

## Raw source > summary — always pass full context to subagents

When dispatching parallel drafting agents, feed them the **raw source
document**, not a summary. The first batch of drafts against a packaging
deck missed real workflow distinctions because the agents only had a
pre-digested version of the source. Corrections were accurate once the
complete source file was provided.

The failure mode is predictable: a summary drops the exact details that
matter most for Product Support workflow impact — tier boundaries, plan-ID
transitions, the one-line caveat that changes how a rep handles a ticket.
Customer-facing changelogs describe what changed for the customer; they do
not cover how reps should handle the change day-to-day. That gap is the
value-add of a Playbook update over a changelog, and it's exactly what a
summary destroys.

**Rule:** every draft must include a "PS Workflow Impact" section, and
every subagent prompt must carry the raw source. Save source files where
all agents can read them — don't paste excerpts.

---

## Two-stage change detection — cheap gate, authoritative filter

The pipeline uses a revision counter as a **cheap gate** (skip the full
fetch if the counter hasn't moved) and a content hash as the
**authoritative filter** (decide whether each section actually changed).
Don't collapse these into one. A first verification run over 27 sources
surfaced ~15 revision bumps since the prior baseline, but only 8 had real
section-content changes. The rest bumped for non-text reasons — metadata
edits, comment resolution, permission changes, even "viewed by owner" in
some cases.

If you gate on revision alone, every noise-bump becomes a false positive.
If you gate on hash alone, you pay for a full fetch on every untouched
file on every check. Neither substitutes for the other.

**Rule:** keep the revision counter as the pre-filter and the hash as the
signal filter. If future noise becomes a problem, tighten the hash (e.g.
normalize whitespace before hashing) rather than relaxing the two-stage
design.

---

## Retrieval is the bottleneck, not the model

The first FAQ Agent test produced a weak answer ("I found the page but
can't pull content") despite running on a strong model. The model wasn't
the problem. Search was returning short excerpts, not page content.
Adding a separate fetch step that pulled full page bodies — same model,
same question, same knowledge base — transformed answer quality from
useless to demo-ready.

Search excerpts are for ranking, not answering. For any
search-grounded agent, search (find pages) and retrieval (read pages)
must be separate steps, and the agent must fetch full content before it
answers. This rule carries to every future agent build with a
documentation backend.

---

## Token hygiene for Slack scanner vs. bot — they are different tokens

The scanner and the FAQ agent use different Slack tokens for different
reasons, and conflating them wastes a debugging session:

- **Scanner** → User OAuth Token. Reads channels via Rosie's own
  membership. Covers public channels, private channels, and DMs (with
  `im:history` scope). No bot invite needed — the scanner is just
  reading what Rosie can already read.
- **FAQ Agent** → Bot User OAuth Token. Posts messages as a bot user.
  Needs `chat:write`, `app_mentions:read`. Can't see DMs it isn't a
  participant in.

Before this was untangled, both lived under a single `SLACK_BOT_TOKEN`
and the user token was mislabeled. The DM scan failed, and the obvious
fix (add `im:history` to the bot) was wrong because the scanner was
silently using the user token the whole time.

**Rule:** never swap a Slack token without checking what actually uses
it. Name env vars by who's reading (user token = scanner; bot token =
bot). If you add new Slack functionality, pick the token based on
whether the path reads (user) or writes (bot).
