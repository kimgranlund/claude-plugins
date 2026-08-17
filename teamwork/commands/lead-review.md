---
name: lead-review
kind: command
description: Makes this host session a standing review desk, routing each target to its owning fresh-context checker.
argument-hint: "[optional target — a diff, branch, doc, skill, or agent to route]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: leading-review
requires: [leading-review]
mutates: false
confirm: none
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Skill
  - Agent
---

Invoke the `leading-review` skill against `$ARGUMENTS` (optional target). This command is the
human-typed entry point only; `leading-review` carries the full routing procedure — it never
grades anything itself, only dispatches to the owning checker.
