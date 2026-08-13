---
name: rename-planning
kind: skill
description: >
  Plan a single artifact rename: propose the conforming target name and
  enumerate the full blast radius — every invocation string, relation edge,
  wrapper, hook, and workflow config the rename touches. Use when a naming
  violation or exemption needs a fix, before any rename is executed.
  Produces a typed plan; never executes.
author: kim
created: 2026-08-13
last_updated: 2026-08-13
requires: [naming-conventions, naming-audit]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git log *)
  - Bash(git grep *)
---

# rename-planning

## Procedure

1. Confirm the violation via naming-audit output (never plan from an
   unverified claim of non-conformance).
2. Propose the conforming target: parse the intent of the current name, mint
   the target per GRAMMAR.md productions, verify the target parses clean and
   collides with nothing extant.
3. Enumerate blast radius per references/BLAST-RADIUS-CHECKLIST.md — every
   hunting ground, greps cited, zero-hit grounds explicitly recorded as
   checked.
4. Emit the plan: `{old, new, touched: [{file, line, kind-of-reference}],
   relations-affected, exemption-entry-retired?}`. The plan is the contract
   rename-execute consumes; anything not in the plan does not get touched.

## References

| File | Read when |
|---|---|
| BLAST-RADIUS-CHECKLIST.md | enumerating what a rename touches — the hunting grounds per artifact kind |
