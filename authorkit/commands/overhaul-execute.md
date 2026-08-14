---
name: overhaul-execute
kind: command
description: Drive an approved estate overhaul end to end — scope confirm, measure, plan, then gated wave execution through rename-planning/rename-execute, reshape-skill, and build-lead dispatches. The execution counterpart of /overhaul-planning; three confirm gates, needs a live user, never unattended.
argument-hint: "[target: estate-root, plugin-set, or member list — blank scans the current project]"
author: kim
created: 2026-08-14
last_updated: 2026-08-14
wraps: overhaul-execute
requires: [overhaul-execute]
mutates: true
confirm: required
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Agent
  - AskUserQuestion
  - Write
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
  - Bash(gh issue *)
---

Invoke the overhaul-execute skill against `$ARGUMENTS` (default: the current project). Follow
that skill's procedure exactly; this wrapper adds nothing except the on-demand, user-typed entry
point — the skill itself is not user-invocable.

`mutates: true` / `confirm: required` is this command's own contract: real mutation happens
across three gates, and the skill's own body is what enforces each one (including the
no-live-user SKIPPED branch) — this wrapper does not restate that logic, it only carries the
tool grants and the slash-command surface.
