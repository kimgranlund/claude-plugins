---
name: pattern-audit
kind: command
description: Sweep a repo or corpus for a pattern or instruction (given as an argument, or gathered interactively) and emit a structured dataset of matches for downstream work.
argument-hint: "[pattern-or-instruction] [path-to-target]"
author: kim
created: 2026-08-15
last_updated: 2026-08-15
wraps: pattern-audit
requires: [pattern-audit]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/scan.py *)
---

Invoke the pattern-audit skill against `$ARGUMENTS` (default: the current
project). Follow that skill's procedure exactly; this wrapper adds nothing
— it exists because skills are not user-invocable and sweeps are demanded
on demand.
