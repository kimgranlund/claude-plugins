---
name: rename-execute
kind: skill
description: >
  Atomically apply one rename plan produced by rename-planning — folder,
  frontmatter, every enumerated invocation string, relation edges, exemption
  retirement — then verify via the validator, reverting the whole rename on
  any new error. Use when a rename plan already exists and needs applying,
  or when asked to execute, apply, or land a rename/move. The estate's
  single mutation point. NOT for producing the plan itself (rename-planning,
  always this skill's own precondition); NOT for a phased campaign spanning
  many members (overhaul-execute, which invokes this skill once per rename
  row); NOT for auditing conformance in the first place (naming-audit).
author: kim
created: 2026-08-13
last_updated: 2026-08-17
requires: [rename-planning, naming-audit]
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash(git mv *)
  - Bash(git restore *)
  - Bash(python3 */scripts/validate.py *)
---

# rename-execute

Grammar licence: `.claude/docs/spec/spec-naming-convention.md` §14.9 (issue #525) — a
verb-terminal skill name off `user-invocable: true` alone, no sibling command required.

Target: `$ARGUMENTS` (a rename-planning plan, or an old artifact name to plan from first). The
estate's single mutation point. Rules, in order:

1. A plan from rename-planning is the precondition. Given only an old name, invoke
   `rename-planning` (Skill tool) first and present the plan.
2. Present the plan's full touched-file list and wait for explicit confirmation. No confirmation,
   no mutation — this gate is not a suggestion. Before applying, check the plan's touched paths
   are clean (`git status -- <touched paths>`); dirt on any of them → stop and report rather than
   mutating on top of unrelated in-progress work.
3. Apply atomically: `git mv` the folder/file, then every enumerated reference, then relation
   edges (`performs`/`wraps` renamed in the same pass — the same-plan rule), then retire the
   exemption entry if one exists. Touch NOTHING outside the plan.
4. Verify: run the validator (`naming-audit`'s `scripts/validate.py`) against the estate. Errors →
   revert, scoped to exactly the plan's touched paths: `git restore --staged --worktree --
   <touched paths>` for the edited/renamed references, `git mv <new> <old>` to undo the folder/file
   move; never a blanket `git checkout -- .` or `git restore .`, which would also clobber
   unrelated dirt step 2 didn't already rule out. A half-landed rename is worse than the
   violation it fixed.
5. Done when either the validator ran clean on the mutated estate and the report below is
   emitted, or the gate reported SKIPPED/blocked per steps 2–4 above with nothing left mutated.
   Report: old → new, files touched, exemption count before → after (or the SKIPPED/blocked
   reason and confirmation nothing was left mutated).
