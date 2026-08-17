---
name: lead-build
kind: command
description: Makes this host session run under the build-leader agent's own contract, driving every ticket through dispatch-ticket with interactive branches alive.
argument-hint: "[optional repo root]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: leading-builds
requires: [leading-builds]
mutates: true
confirm: none
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash
  - Skill
  - Agent
---

Invoke the `leading-builds` skill against `$ARGUMENTS` (optional repo root). This command is the
human-typed entry point only; `leading-builds` carries the full procedure. NOT the dispatched
sibling seat (`build-leader`, Agent tool); NOT batch ticket mobilization (`/mobilize-chores`); NOT
a generic coordination charter (`/lead-team`); NOT a design/decomposition charter
(`/lead-planning`).
