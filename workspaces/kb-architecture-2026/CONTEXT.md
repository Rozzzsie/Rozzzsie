# CONTEXT.md — KB Architecture 2026

## What this workspace is

*This is where the fam is applied to KB programme management for two AI
products — an AI-driven media analysis platform and a generative-AI brand
monitoring tool. The four-stage pipeline + human-review gate is the
workspace's operational shape.*

The KB is a two-layer structure: foundational Core Articles per product, plus
modular Snippets that are reusable support responses. The KB is designed to
function as a support manual, not a reference document. Scope decisions are
driven by what a support agent needs to resolve a ticket.

## How the work is shaped

The pipeline has four stages, each with a distinct trigger and output:

| Stage | Trigger | Output |
|-------|---------|--------|
| **Check** | Session startup or on-demand run | A list of upstream sources whose revision counters have moved since the last baseline |
| **Draft** | A real change detected in Check | A set of KB article drafts, classified by affected section, written into the drafts store |
| **Review** | Pending drafts exist | A reviewed draft, marked approved or rejected |
| **Apply** | An approved draft | A Confluence page update, published on explicit confirmation |

A separate signal scan covers product Slack channels — treated as a signal
layer (flagging gaps and release activity), not a structured source.

## Approval gates

| What | Who approves |
|------|--------------|
| KB drafts and Confluence publishes | Rosie (owns authoring directly) |
| Scope and priority of what the pipeline covers | A co-owner on the KB work |
| Cross-functional alignment on what belongs in KB vs. engineering | A co-owner on the KB work + a cross-functional stakeholder |

The publishing gate sits entirely with Rosie; scope and priority calls route
through the co-owner. Same split shows up elsewhere in the fam: owner-of-the-
surface publishes, owner-of-the-function decides what goes on it.

## Why the architecture looks like this

KB content is authoritative for frontline support — incorrect or premature
content has real downstream consequences for how a support agent handles a
ticket. That makes two design choices non-negotiable: human review before
every publish, and explicit authority hierarchy across upstream sources
(an official product FAQ is the floor; internal GTM material never leaks into
support language).

The pipeline itself is the delivery mechanism. The load-bearing artifacts are
the source map (which upstream sources map to which KB articles) and the scope
rules (the UI-vs.-AI-behavior distinction that classifies every incoming
ticket). Those artifacts are the brain — the pipeline is the arms and legs.
