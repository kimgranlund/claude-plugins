---
doc-type: plan
id: plan-<YYYY-MM>-<target-slug>-overhaul
status: active
date: YYYY-MM-DD
owner: <human who approves the seed list>
review-cadence: per-wave (re-reviewed whenever a wave's tickets land or the campaign resumes)
---
# Overhaul plan — <target name> — <YYYY-MM-DD>

## Steps

### Phase 0 — Measurements

| Instrument | Available? | Finding summary |
|---|---|---|
| naming-audit | yes/no | error count, exemption burn-down |
| bloat-audit | yes/no | files flagged, chars recoverable |
| check-routing (harness) | yes/no | stolen/leaked/dead counts, or "unavailable — harness not installed" |
| plan-plugin-split surface_map (harness) | yes/no | dependency-closure edges, or "unavailable — harness not installed" |

### Phase 1 — Per-member kill-switch

| Member | Where it lives | Species | Blast radius (summary) | Merge/Split candidate? | Knowledge tier | Verdict |
|---|---|---|---|---|---|---|
| <name> | <job-evidence citation, or "no move — absence is correctly absent"> | command/skill/agent/dual | <invocation strings, relations, hooks touched> | <MERGE with {set} → plan-skill-merge / SPLIT into {set} → plan-skill-split / NO — reason, evidence cited> | <PROCEDURE — keep-inline (always) / KNOWLEDGE · keep-inline\|move-to-references\|extract-to-pack\|retire — bloat-audit number cited> | MOVE / NO MOVE (reason) |

State every "no move", every "NO" merge/split verdict, and every knowledge-tier verdict with
its reason cited against Phase 0 evidence — a falsifiable plan never asserts a kill, a
nomination, or a tier without a cause.

### Phase 2 — Waved ticket seeds (not yet minted)

Each row below is a plan step: owner is the human who approves it, status starts `todo`, and
its done-when is stated per seed.

#### Wave 0 — merge/split nominations (route to plan-skill-merge / plan-skill-split, executed via /reshape-skill)
- [ ] MERGE: <candidate set> → seed for `harness:plan-skill-merge` (Blocked-by: none) — status: todo — done-when: <the split/merge analysis returns a recorded verdict>
- [ ] SPLIT: <member> → seed for `harness:plan-skill-split` (Blocked-by: none) — status: todo — done-when: <the split/merge analysis returns a recorded verdict>

#### Wave 1 — mechanically-clean moves
- [ ] <member> → <target name> (Blocked-by: <wave-0 seed id, if this member was also nominated>) — status: todo — done-when: <the move lands, gate green>

#### Wave 2 — species changes (semantic — critic pass + eval rewrite required)
- [ ] <member> → <target name> (Blocked-by: <wave-0 seed id if nominated, plus any wave-1 seed ids this depends on>) — knowledge tier: <move-to-references/extract-to-pack/retire, if that's this seed's reason> — status: todo — done-when: <critic pass clean, gate green>

#### Wave 3 — contested
- [ ] <member> — open question: <what's unresolved> (Blocked-by: <any wave-0/1/2 seed ids this depends on, or none>) — status: todo — done-when: <the open question is resolved by a human>

#### Grandfathered (can't move cleanly — ADR-0011 D8 ratchet)
- <member> — exemption retained; reason: <why no wave moves it cleanly>

### Phase 3 — Execution contract (per ticket, once approved)

claim → worktree → `git mv` (history preserved) → supersession note or `renames.json` entry
→ gates + critics → PR → human merge → verified close. Serial through shared ledgers
(`naming.manifest.json`, `renames.json`) — two tickets never touch the same ledger entry in
parallel.

## Validation

How the whole plan proves itself, per wave, once its tickets land:

- [ ] `/check-routing` clean for every touched plugin
- [ ] `fix-old-names` sweep run against consumer repos
- [ ] Records amended with dated supersession notes (never rewritten)

## Rollback

The undo per irreversible step, decided now, not during the incident:

- **A landed `git mv` (Wave 1/2)** — `git mv` back on a fresh branch, or `git revert` the merge
  commit; history is preserved either way (the plan's own invariant 2), so the undo is never
  destructive.
- **A ledger entry retired (`naming.manifest.json`, `renames.json`)** — re-add the entry verbatim
  from the pre-change git history; the exemptions array is shrink-only by ratchet, but a rollback
  restoring a wrongly-retired entry is a correction, not a forced re-grant.
- **A supersession note** — supersession notes are themselves append-only (docs-mutability);
  rollback of a wrongly-superseded record is a NEW dated note reversing the prior one, never an
  edit or deletion of the note itself.
- **A merge/split executed via `/reshape-skill`** — the pre-reshape state is the last commit
  before the reshape PR merged; revert that PR's merge commit to restore the prior member
  boundary, then re-open the Wave-0 seed if the nomination should be retried differently.
  Nomination-only rows (Wave 0 before Waves 1–3 fire) have nothing to roll back — no move has
  executed yet.
- **A ticket seed approved and minted, then abandoned mid-build** — the dispatch's own claim
  release (ADR-0005) already covers this: `--remove-assignee`/`--remove-label in-flight` plus a
  release comment; no plan-doc rollback owed beyond flipping that seed's status back to `todo`.

## The five respect invariants

1. Evidence can veto the plan.
2. History preserved, never replaced.
3. Consumers degrade gracefully.
4. The old design's intent is read before it is judged.
5. Nothing semantic rides hidden in a move.

## Next step

This plan and its ticket seeds are generated only — nothing above has been executed. A human
reviews the seed list and approves each row; approved rows are minted through their owning
intake skill (`file-feature`/`file-task`), never auto-created here. On completion (every wave's
tickets closed or grandfathered), flip `status: complete` and move this file to the docs
archive per PLAN's living-state contract — never leave a finished plan `active`.
