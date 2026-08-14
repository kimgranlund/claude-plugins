# Overhaul plan — <target name> — <YYYY-MM-DD>

## Phase 0 — Measurements

| Instrument | Available? | Finding summary |
|---|---|---|
| naming-audit | yes/no | error count, exemption burn-down |
| bloat-audit | yes/no | files flagged, chars recoverable |
| check-routing (harness) | yes/no | stolen/leaked/dead counts, or "unavailable — harness not installed" |
| plan-plugin-split surface_map (harness) | yes/no | dependency-closure edges, or "unavailable — harness not installed" |

## Phase 1 — Per-member kill-switch

| Member | Where it lives | Species | Blast radius (summary) | Merge/Split candidate? | Knowledge tier | Verdict |
|---|---|---|---|---|---|---|
| <name> | <job-evidence citation, or "no move — absence is correctly absent"> | command/skill/agent/dual | <invocation strings, relations, hooks touched> | <MERGE with {set} → plan-skill-merge / SPLIT into {set} → plan-skill-split / NO — reason, evidence cited> | <PROCEDURE — keep-inline (always) / KNOWLEDGE · keep-inline\|move-to-references\|extract-to-pack\|retire — bloat-audit number cited> | MOVE / NO MOVE (reason) |

State every "no move", every "NO" merge/split verdict, and every knowledge-tier verdict with
its reason cited against Phase 0 evidence — a falsifiable plan never asserts a kill, a
nomination, or a tier without a cause.

## Phase 2 — Waved ticket seeds (not yet minted)

### Wave 0 — merge/split nominations (route to plan-skill-merge / plan-skill-split, executed via /reshape-skill)
- [ ] MERGE: <candidate set> → seed for `harness:plan-skill-merge` (Blocked-by: none)
- [ ] SPLIT: <member> → seed for `harness:plan-skill-split` (Blocked-by: none)

### Wave 1 — mechanically-clean moves
- [ ] <member> → <target name> (Blocked-by: <wave-0 seed id, if this member was also nominated>)

### Wave 2 — species changes (semantic — critic pass + eval rewrite required)
- [ ] <member> → <target name> (Blocked-by: <wave-0 seed id if nominated, plus any wave-1 seed ids this depends on>) — knowledge tier: <move-to-references/extract-to-pack/retire, if that's this seed's reason>

### Wave 3 — contested
- [ ] <member> — open question: <what's unresolved> (Blocked-by: <any wave-0/1/2 seed ids this depends on, or none>)

### Grandfathered (can't move cleanly — ADR-0011 D8 ratchet)
- <member> — exemption retained; reason: <why no wave moves it cleanly>

## Phase 3 — Execution contract (per ticket, once approved)

claim → worktree → `git mv` (history preserved) → supersession note or `renames.json` entry
→ gates + critics → PR → human merge → verified close. Serial through shared ledgers
(`naming.manifest.json`, `renames.json`) — two tickets never touch the same ledger entry in
parallel.

## Phase 4 — Closeout (per wave, once tickets land)

- [ ] `/check-routing` clean for every touched plugin
- [ ] `fix-old-names` sweep run against consumer repos
- [ ] Records amended with dated supersession notes (never rewritten)

## The five respect invariants

1. Evidence can veto the plan.
2. History preserved, never replaced.
3. Consumers degrade gracefully.
4. The old design's intent is read before it is judged.
5. Nothing semantic rides hidden in a move.

## Next step

This plan and its ticket seeds are generated only — nothing above has been executed. A human
reviews the seed list and approves each row; approved rows are minted through their owning
intake skill (`file-feature`/`file-task`), never auto-created here.
