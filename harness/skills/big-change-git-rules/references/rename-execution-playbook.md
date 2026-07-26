# Rename-execution playbook — how this estate renames plugins and members safely

Ask this file: "I have a rename to execute — what order, what lands together, how do I prove
routing survived, what gates?" Distilled 2026-07-25 from ADR-0006 (ratified 2026-07-21, executed
PRs #62–#73), ADR-0007 Decision 2, naming-rules' symmetry-hardline record, and the teamwork
README ledger v1.0.0–v1.0.5 (the per-PR execution record). ADR-0007 binds every future rename to
this discipline [ratified, ADR-0007 Decision 2: "the same sweep discipline ADR-0006 used —
guarded replacements, ledger history untouched, insertion audit"].

## Campaign order — standards flip first, then leaf-first

- **Phase 0, before any rename PR:** flip the standards so the new grammar is canon before any
  artifact moves — ADR-0006 made `naming-rules` the estate canon, stamped dated supersession
  notes on the old §Naming sections, and hardened `skill_lint` (W5 noun set) with selftest
  fixtures, all pre-PR-1 [verified, ADR-0006 Decision 2].
- **Then leaf-first, consumers before dependencies:** ADR-0006's order ran
  color → typography → llm → agentic-ui → design-systems → ui → orchestration → scribe → forge —
  "the toolchain renames itself only after every consumer of its old handles is gone"
  [verified, ADR-0006 Decision 3, quoted]. A dependency renamed before its consumers strands
  live references mid-campaign.

## The per-rename same-change contract — eight things land together

Every rename PR carries ALL of these in the one change [verified, ADR-0006 Decision 4; item 8
added 2026-07-26, issue #97]:

1. **Frontmatter + path alignment** — skill `name:` = directory name, agent `name:` = file
   stem, moved together; F9/A6 lint FAILs the copy that lags [verified, naming-rules
   symmetry-hardline].
2. **Live reference rewrite, grep-proven** — descriptions, fences, `skills:` preloads, sibling
   suites' `skill:` fields, READMEs/MANUAL/root routing table, cross-plugin soft mentions.
   Ledger history and `.claude/ops` records are EXCLUDED — old names stay greppable in
   CHANGELOGs, ADRs, `.refactor-attic/` [verified, ADR-0006 Decisions 4+6].
3. **Reciprocal fence re-closure** — every sibling suite whose fenced vocabulary moved gets its
   return case updated in the same change.
4. **Blind eval-run, before AND after** — baseline as control pre-rename, full re-measure of
   every touched suite post-rename (see measurement below).
5. **MAJOR version bump + ledger entry** for the renamed plugin, naming the ADR.
6. **Version bump + ledger line for every sibling touched** — the ledger is the execution
   record; the bump marks that copy forward-aware [verified, teamwork v1.0.1/v1.0.2 pattern].
7. **`release_gate.py` CLEAN** (0 fail / 0 warn) on the renamed plugin and every touched
   sibling, plus CI green on the PR — CI is the merge gate, not a courtesy [verified, ADR-0002].
8. **Rename manifest regenerated** — `python3 harness/scripts/fix_old_names.py derive .`, and the
   resulting `harness/renames.json` committed in the same PR. Items 1–7 all stop at this repo's
   boundary; item 8 is the only one that reaches a repo that merely INSTALLS these plugins.
   Regenerate, never hand-edit: the manifest is derived from git rename detection, so a rename
   git recorded cannot be forgotten, and a hand-typed entry can be wrong in a way nothing
   catches.

## Downstream is not covered by items 1–7

The campaign order above sequences consumers *inside this repo*. A repo that installs these
plugins is invisible to every one of those steps, and its stale handles fail SILENTLY — a
retired agent name errors only at dispatch, a description citing a retired skill mis-routes with
no diagnostic. `fix-old-names` is the consumer-side half; this file is the producer-side half.

Two findings from the first real consumer sweep [verified, agent-ui, 2026-07-26, issue #97]:

- **A plugin-prefix-only rename is invisible to a name-to-name map.** `color:token-builder` →
  `design:token-builder` changed no name at all — only which plugin owns it. It survived an
  automated pass for exactly this reason. The manifest carries `old_plugin`/`new_plugin` per
  entry so the class is representable; a rename wave that merges plugins (ADR-0008) generates
  this class in bulk.
- **Prose is not a durable source for the map.** The per-plugin transition tables were retired
  as stale in the 2026-07-25 v1.0.5 sweep, and `naming-rules`' `estate-rename-map.md` records
  the *planned* 2026-07-20 mapping — execution later drifted from it in three plugin rows. Only
  git's rename records match what shipped, which is why item 8 says derive.

## Routing safety is measured, not asserted

The parity gate: blind `/check-routing` run BEFORE the rename (the control), the same blind run
AFTER across every suite whose fences changed; acceptance is **parity or better** [verified,
ADR-0006 Acceptance]. The judge is blind to the rename, so any delta is a real routing change.
Worked instance: teamwork v1.0.0 baselined 107/108, re-measured 108/108 — one pre-existing miss
healed by the rename itself, two single-judge flips healed same-change by carrying the stolen
verbatims into existing fences [verified, teamwork README v1.0.0 ledger].

## Incident catalog — what actually broke, and the rule each grounds

- **Unreachable-command class** [incident, 2026-07-21, six instances: file-feature, file-task,
  sort-issues, sweep-chores, plan-chores, build-feature] — directory and references renamed,
  frontmatter `name:` never moved; each `/new-command` dead, found "late, by a routing
  re-measure or in passing, never by a gate." Grounds: F9/A6 name/dir/frontmatter drift lint
  (harness 2.0.10) — the class is now extinct by construction [verified, teamwork v1.0.5].
- **Stale reciprocal fences** [incident, 2026-07-21, two instances] — sibling suites' return
  fences lagged a description change; leaked routing signals surfaced only in the re-measure.
  Grounds: contract item 3 + the post-rename re-measure as the blade [verified, teamwork
  v1.0.4].
- **Description-diet collateral** [incident, 2026-07-22, two fences] — a later description trim
  shortened verbatim fence markers, so fences stopped matching and leaked on re-eval. Grounds:
  after ANY description edit, verify suite fences still match verbatim; a modified fence
  re-judges its reciprocal suites [verified, teamwork v1.0.4 repair record].

All three were caught by the eval-run re-measure — none by inspection. The measure, not the
care, is the safety mechanism.

## Scope of this file

Executes ADR-0007-bound renames of plugins and their members in THIS estate. The naming grammar
itself (what the new name should be) is `naming-rules`; the generic campaign mechanics
(worktrees, PR close sequence, who pushes) are this pack's other files — this file owns only
what a RENAME adds on top.
