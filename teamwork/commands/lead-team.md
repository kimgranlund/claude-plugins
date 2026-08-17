---
name: lead-team
kind: command
description: Makes this host session run under the team-leader agent's own contract for one stated charter, never a separately dispatched agent.
argument-hint: "[charter — the plan/build-feature/review work needing a team]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: leading-teams
requires: [leading-teams]
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

Invoke the `leading-teams` skill against `$ARGUMENTS` (the charter — the plan/build-feature/review
work needing a team). This command is the human-typed entry point only; `leading-teams` carries the
full procedure (contract adoption, phases, failure branches). NOT for a task one context can hold
(`team-or-solo-rules`); NOT for reviewing one artifact directly (dispatch the owning reviewer); NOT
a solo design/decomposition charter where the host authors the docs itself (`/lead-planning`).
