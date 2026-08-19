---
name: plugin-install-facts
description: >-
  Verified per-channel install instructions for Claude Code plugins — /plugin marketplace add +
  /plugin install (github shorthand, git https/SSH URLs, local paths), npm-sourced plugins, dev
  checkouts, CI forms, trust/scope/update facts. Use for "how do I install this plugin",
  "install instructions", "plugin install command", "install via npx or npm", "install from a
  local path", "which install method", "my installed plugin never got the update", or writing a
  README's install section. NOT for declaring
  a plugin/marketplace in a repo's settings.json (adopt-plugin); NOT authoring/shipping
  a plugin (plugin-writing-rules); NOT settings.json edits with no plugin object
  (update-config); NOT whether a fix already landed in ANOTHER repo (check-state --fleet).
disable-model-invocation: false
user-invocable: false
---

# plugin-install-facts

A verified facts pack: the exact, dated install-command forms for every channel a Claude Code
plugin installs through, and the decision table for which channel fits which situation. The
corpus is the authority — never emit an install command absent from `references/`; report it
as unverified instead.

## Answers only — build asks route out

This pack answers; wiring and shipping route out. "Make this plugin installable for
contributors" / any settings.json edit → `adopt-plugin`. "Ship / release the plugin" →
`/ship-plugin`. "Build the plugin's content" → `/make-plugin`. A new manifest →
`plugin-writing-rules`. An install ask with none of these shapes is answered here, from the
corpus.

## Consult table

Enter by Grep: search the matching file for the channel or command term first, then Read that
section — Grep-first, not a start-to-finish read of the folder.

| Ask pattern | File |
|---|---|
| exact install command for a channel — github repo, git URL (https/SSH), local path, marketplace add→install sequence, npm-sourced, CI/non-interactive | `references/install-commands.md` |
| which channel should I use — private repo, team distribution, solo dev checkout, public release | `references/channel-choice.md` |
| what happens around the install — trust prompt, user vs project scope, update/autoUpdate, why an update didn't arrive, uninstall/disable | `references/install-lifecycle.md` |

## Answer contract

Every answer carries: the exact command form(s) verbatim from the corpus · the cited file ·
the precondition or failure mode that bites next (trust prompt, marketplace-add-first, version
cache key). README install sections extend this: one fenced runnable block per supported
channel, most-common-first, preconditions in order.

Worked example (normative shape, illustrative values) — "how do I install your plugin from
GitHub?":

> Two commands, in order (`references/install-commands.md`):
> ```
> /plugin marketplace add kimgranlund/claude-plugins
> /plugin install harness@nonoun-plugins
> ```
> First use prompts for trust — installing is running code; expect and confirm it.

## Deviation doctrine

Corpus defaults carry their rationale — e.g. SSH `git@` over `https://` because of the recorded
2026-07-22/25 host-flakiness incidents — so a consumer can deviate exactly when the rationale
doesn't hold (a host where HTTPS auth is the working path takes HTTPS, no violation).

## Corpus of record

The trigger-phrasing test set lives at `evals/evals.json` (this workspace's suite schema);
`[drift-prone]` markers in `references/` are the refresh checklist at every release boundary —
platform install syntax is drift-prone by nature, so answers cite their verification dates.
Markers follow `pack-writing-rules`, plus one declared local sub-class: `[verified absence]` —
a documented ABSENCE checked against the primary source (e.g. "no npx form exists"), carrying
`[verified]` weight; it is what licenses correcting an invented command instead of hedging.
