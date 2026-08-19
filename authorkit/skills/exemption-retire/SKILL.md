---
name: exemption-retire
kind: skill
description: >
  Retire one exemption opportunistically — verify it via naming-audit, chain
  rename-planning for the plan, then rename-execute (whose own confirmation
  gate and atomic apply include the manifest exemption shrink) — for an
  artifact that is already being touched anyway. Use when asked to retire,
  burn down, or clear one named exemption, or "since we're touching this
  anyway, fix its name too." NOT for a bulk/estate-wide exemption burn-down
  across many members in one pass (overhaul-execute's waved campaign); NOT
  for producing the rename plan alone with no intent to apply it
  (rename-planning); NOT for the mutation itself, which this skill only
  hands off to (rename-execute); NOT a manifest-only removal once the
  rename already landed elsewhere (manifest-authoring).
author: kim
created: 2026-08-13
last_updated: 2026-08-19
requires: [rename-planning, naming-audit, rename-execute]
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
---

# exemption-retire

Moved in from the command-only `commands/exemption-retire.md` wrapper (issue #525: skill-as-command
is the estate's dual-access successor to the command-wrapper pattern — this skill now carries the
whole procedure, no separate command file).

Thin orchestration; owns no writes of its own. Target: `$ARGUMENTS` (the exempt artifact's name).

1. Verify the target is in the estate's `exemptions` array (`naming-audit`, Skill tool) — else
   stop, nothing to retire.
2. Invoke `rename-planning` (Skill tool) for it.
3. Hand the plan to `rename-execute` (Skill tool), whose own confirm gate governs the mutation.
   The manifest shrink (removing the exemption entry) happens inside `rename-execute`'s own
   atomic apply — this skill never edits `naming.manifest.json` directly.

Done when `rename-execute` reports the applied rename and the exemption entry is gone from
`naming.manifest.json` (or step 1/2 stopped first, with nothing mutated) — report the retired
name and which step the chain reached.
