---
name: rename-execute
kind: command
description: Atomically apply one rename plan produced by rename-planning — folder, frontmatter, every enumerated invocation string, relation edges, exemption retirement — then verify via the validator.
argument-hint: "[plan or old-name]"
author: kim
created: 2026-08-13
last_updated: 2026-08-13
requires: [rename-planning, naming-audit]
mutates: true
confirm: required
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash(git mv *)
  - Bash(python3 */scripts/validate.py *)
---

The estate's single mutation point. Rules, in order:

1. A plan from rename-planning is the precondition. Given only an old name,
   invoke rename-planning first and present the plan.
2. Present the plan's full touched-file list and wait for explicit
   confirmation. No confirmation, no mutation — `confirm: required` is the
   contract, not a suggestion.
3. Apply atomically: `git mv` the folder/file, then every enumerated
   reference, then relation edges (`performs`/`wraps` renamed in the same
   pass — the same-plan rule), then retire the exemption entry if one exists.
   Touch NOTHING outside the plan.
4. Verify: run the validator against the estate. Errors → revert the whole
   rename (git makes this cheap); a half-landed rename is worse than the
   violation it fixed.
5. Report: old → new, files touched, exemption count before → after.
