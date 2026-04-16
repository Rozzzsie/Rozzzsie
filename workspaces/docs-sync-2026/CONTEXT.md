# CONTEXT.md — Cross-Team Docs Sync 2026

## What this workspace is

This is where the fam is applied to cross-team documentation ownership —
keeping a product Playbook in sync with live product changes for an
influencer marketing platform, and standing up a Confluence-grounded FAQ
agent on top of it. The pipeline and the agent are the workspace's
operational shape.

## How the work is shaped

Two modes, one shared substrate (the Playbook page map):

| Mode | Trigger | Output |
|------|---------|--------|
| **Ops** | A detected change in an upstream product source (Google Doc, Slides deck, Slack signal) | A reviewed-and-applied Confluence page update |
| **Q&A** | A product question from the Product Support team | An answer grounded in named Playbook pages, with links |

Drafts are never auto-applied — every publish is a manual step behind a
human review gate.

## Approval gates

| What | Who approves |
|------|--------------|
| Confluence page updates | Rosie (owns the Playbook space directly) |
| Scope and priority of what the pipeline covers | The Product Support & Engineering lead |
| New product-source integrations (Slides, Sheets, external watchers) | Rosie, in consultation with the lead |

The Product Support & Engineering lead gates scope and priority calls; the
publishing itself sits with Rosie. This split shows up elsewhere in the fam
(owner-of-the-surface publishes; owner-of-the-function decides what goes on it).

## Why the architecture looks like this

The Playbook lives in Confluence, but its upstream truth lives in scattered
product-team surfaces — Docs, Slides, Slack, the platform's public updates
page. Before the pipeline, staleness was the default and detection was
manual. The fam runs the same governance protocols here (P1–P8, checkpoint
bar, state updates) as in every other workspace; the shape of the work —
two-mode pipeline + agent, with human review as the only publish gate — is
what's workspace-specific.
