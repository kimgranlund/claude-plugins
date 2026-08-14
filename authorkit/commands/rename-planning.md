---
name: rename-planning
kind: command
description: Plan a single artifact rename — propose the conforming target name and enumerate the full blast radius. Produces a typed plan; never executes.
argument-hint: "[artifact-name-or-path]"
author: kim
created: 2026-08-14
last_updated: 2026-08-14
wraps: rename-planning
requires: [rename-planning]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git log *)
  - Bash(git grep *)
---

Invoke the rename-planning skill against `$ARGUMENTS`. Follow that skill's
procedure exactly; this wrapper adds nothing — it exists because skills are
not user-invocable and a rename plan is demanded on demand. Plan-only: this
command never mutates anything — it carries no `Write`/`Edit` tool, matching
the wrapped skill's own read-only allowed-tools — so it needs no confirmation
gate. `/rename-execute` is the only estate mutation point; hand this plan to
it next.
