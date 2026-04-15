# Agent protocols

This is the governance doc the hooks in this repo enforce. The full version is private to the workspace it governs. The shape of it is legible from the enforcement layer: the `PostToolUse`/`Stop`/`SessionStart` hooks, the checkpoint bar, and `_config/output-checklist.md`. What's in the missing doc is what those hooks check for.

## Why it's not here

A governance doc written into a public artifact becomes a tutorial. The doc we actually run is battle-tested on live work, adversarially audited by Breakline, and calibrated to the specific contexts we operate in. The shape is more useful than the text; the text would be copy-paste-safe but context-poor.

Read the hooks. Read the output-checklist. The protocols are what those enforce.
