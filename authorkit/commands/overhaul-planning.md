---
name: overhaul-planning
kind: command
description: Generate a phased estate-overhaul plan for a target — measure-first, a per-member kill-switch design doc, and waved ticket seeds. Never executes a move.
argument-hint: "[target: estate-root, plugin-set, or member list]"
author: kim
created: 2026-08-14
last_updated: 2026-08-14
wraps: overhaul-planning
requires: [overhaul-planning]
mutates: true
confirm: required
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
---

Invoke the overhaul-planning skill against `$ARGUMENTS` (default: the current project).
Follow that skill's procedure exactly; this wrapper adds nothing except the on-demand,
user-typed entry point — the skill itself is not user-invocable.

Before writing the plan doc and ticket-seed list to disk, present the full Phase 0
measurements and the Phase 1 kill-switch table and wait for explicit confirmation —
`confirm: required` is the contract, not a suggestion. This command GENERATES only: it never
executes a move, a rename, or a build, and it never mints ticket Issues on its own — the
seed list it writes is what a human reviews and approves next (that's `/overhaul-execute`).
