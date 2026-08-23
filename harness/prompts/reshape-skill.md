---
description: "Execute an already-decided skill-corpus split, merge, or rename from its validated manifest. Moves files, retires old surfaces to a timestamped attic, rewrites every referrer, and proves the sweep clean. Run /reshape-skill [manifest.json]. Writes on approval only. NOT for deciding whether to split (plan-skill-split) or merge (plan-skill-merge); NOT for authoring the resulting packs' content (make-skill)."
argument-hint: "[manifest.json]"
---

# reshape-skill

reshape-skill is the executor the decision skills hand off to: a validated manifest in, a proven
refactor out, nothing decided in between. If the manifest's verdict is `no-split` or
`keep-separate`, there is nothing to execute — say so and stop. Manifest: `$ARGUMENTS`.

## Phase 1 — Validate twice, cut once

1. **Design validity:** run the owning checker — `plan-skill-split/scripts/manifest_check.py` for a
   split, `plan-skill-merge/scripts/consolidation_check.py` for a merge. A manifest that was never
   design-validated does not proceed; route it back to its decision skill.
2. **Disk validity:**
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/reshape-skill/scripts/refactor_apply.py" <manifest>` —
   plan mode. It re-validates against reality (every source file exists, no target collisions,
   every repair-map `old` string present) and prints the full operation plan: moves, attic
   retirements, referrer edits. A preflight failure means the manifest is stale against the tree —
   back to the decision skill; never hand-patch a manifest to make it apply.

## Phase 2 — Approval

Show the plan and the two irreversibility facts: retired surfaces go to `.refactor-attic/<ts>/`,
not deletion, and a merge cannot be un-merged by git alone — the attic is the undo. **Apply only on
the user's explicit approval of the printed plan** — the plan, not a summary of it.

## Phase 3 — Apply and prove

Re-run with `--apply`. The script moves files, retires the old entry surfaces, applies every
repair-map edit with occurrence counts, then runs the sweep: any live reference to a retired handle
(outside CHANGELOGs and the attic) exits dirty. A dirty sweep is not a partial success — the
missed referrers are listed; add them to the repair map's spirit (fix each by meaning, not blind
substitution), and re-run the sweep until zero.

## Phase 4 — Report and route onward

```
reshape-skill · <manifest> · <split|consolidate|rename>
Moved: <n> files → <packs>   Retired to attic: <dirs>   Referrers edited: <n> (<total occurrences>)
Sweep: clean (0 live references to <retired handles>)
Next: new packs need their SKILL.md surfaces authored/updated (/make-skill), descriptions
      fenced against siblings, and eval suites derived — then /check-routing to prove the routing.
```

Done when the sweep is clean and the report names the downstream authoring steps. NOT done on a
dirty sweep, on any file deleted rather than atticked, or if the plan was executed without the
user having seen it — the approval gates the side effects; that is the entire reason this is a
command and not a model-invocable skill.
