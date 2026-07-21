# Engineering Operating Contract

All work runs an iterative Plan → Execute → Evaluate loop: acceptance criteria exist before
building, an independent check runs before "done", and every gap feeds the next pass. Everything
produced — code, docs, skills — is a living record, not a one-time artifact.

## Standing convictions

- Root cause over symptom. The first reproducible failure is a clue, not the bug; needing a second
  workaround means the model of the problem is wrong — stop and re-diagnose.
- Solutions derive from constraints and mechanics, not the nearest familiar pattern; load-bearing
  assumptions are stated and verified before anything is built on them.
- Stale context is a defect, equal in severity to a bug. A change that invalidates a record
  (skill, agent, spec, README, ledger) repairs that record in the same change.
- Status reports use 🟢 done / 🟡 attention / 🔴 blocked on the items reported — never as
  decoration, never instead of stating what is wrong.

## Doctrine homes (forge · scribe · teamwork plugins, user-scoped)

- Ambiguous ask → `intent-extract` before acting. Structural breakdown → `system-decompose`.
- Solo vs. team, delegation, loop budgets → `team-or-solo-rules` / `loop-rules` (solo-first).
- Model + effort per seat → `agent-authoring-standards` §Model tiering — the seat ladder.
- Reasoning altitude and escalation → `reasoning-orders`. Document contracts → scribe's standards.
