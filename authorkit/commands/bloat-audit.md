---
name: bloat-audit
kind: command
description: Audit a skill, agent, plugin, or any markdown corpus for busy-work: ceremony disproportionate to task size, and prose that costs tokens without buying instruction-following value.
argument-hint: "[path-to-target]"
author: kim
created: 2026-08-13
last_updated: 2026-08-13
wraps: bloat-audit
requires: [bloat-audit]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/measure.py *)
---

Invoke the bloat-audit skill against `$ARGUMENTS` (default: the current
project). Follow that skill's procedure exactly; this wrapper adds nothing
— it exists because skills are not user-invocable and audits are demanded
on demand.
