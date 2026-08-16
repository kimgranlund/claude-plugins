---
name: lead-planning
kind: command
description: Makes this host session a dedicated design/decomposition seat, relaying its own docs to doc-checker for review.
argument-hint: "[charter — the plan/decomposition work needing this seat]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: leading-planning
requires: [leading-planning]
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

Invoke the `leading-planning` skill against `$ARGUMENTS` (the charter). This command is the
human-typed entry point only; `leading-planning` carries the full procedure. NOT for implementing
an approved LLD (`/lead-build`); NOT a generic coordination charter (`/lead-team`).
