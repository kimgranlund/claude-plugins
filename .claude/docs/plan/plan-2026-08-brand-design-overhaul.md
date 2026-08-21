---
doc-type: plan
id: plan-2026-08-brand-design-overhaul
status: complete
date: 2026-08-20
owner: Kim Granlund
audience: human builder
review-cadence: per-wave (re-reviewed whenever a wave's tickets land or the campaign resumes) — closed 2026-08-21, no further review owed
---
# Overhaul plan — brand-design — 2026-08-20

Charter (ratified via harness:find-intent, 2026-08-20; all four forks answered by Kim): evolve
brand-design into a council-as-platform plugin — generalized council/critic machinery IN this
plugin (no new plugin, no teamwork change); two-phase council (blind verdicts preserved +
chair-moderated deliberation round; chair = in-plugin fleet-marshal-patterned moderator seat);
Claude Code/Cowork + Claude Project portability (corpus-resolution ladder MCP → filesystem →
Project knowledge; every procedure declares a single-context degraded mode); structural
hygiene (zero stray root files/folders; placeholder manifest description replaced). Run mode:
this plan's Gate-A confirm (given 2026-08-20, "Approve all 6"), then autonomous serial
build-leader waves, PR-opened ceiling, merge-on-green.

## Steps

### Phase 0 — Measurements (2026-08-20)

| Instrument | Available? | Finding summary |
|---|---|---|
| naming-audit (grammar, root manifest) | yes | 0 errors / 16 artifacts; exemption in use: `muse-agent` (strip `-agent` → `muse` is no RoleLex production) |
| bloat-audit | yes | 6 long-body flags: brand-corpus 9,953 · check-brand-council 9,470 · brand-methodology-rules 8,751 (+dense-description 729) · brand-rubrics 6,969 · brand-guidelines 6,858 · muse-agent 6,704; 3 duplicate pairs (Jaccard 1.0) — the identical brand-forge provenance paragraph restated in brand-corpus/brand-guidelines/brand-rubrics; est. 4,776 recoverable chars |
| check-routing (harness) | yes (prior audit) | 2026-08-19 row: dead=1 stolen=1 leaked=0; the rubrics/guidelines action-twin seam already fixed and live-re-verified 10/10 · 9/10 (README, Phase 4). No fresh run spent here; S6 runs the full proof post-campaign |
| plan-plugin-split surface_map (harness) | yes (map mode) | 29 nodes / 72 edges; stale cross-plugin handle `design-skills:brand-decomposer` cited in ≥5 files (README, .provenance/source-CHANGELOG, brand-guidelines SKILL/intent/references) — that plugin does not exist in this estate. check-mode (partition reconcile) N/A for a single-plugin scope |
| doctrine-audit | n/a | no `doctrine.manifest.json` on target — doctrine-drift evidence unavailable for this run (stated, not invented) |
| pattern-audit | not fired | charter names no pattern outside the four instruments' axes; the stray-file inventory below came from direct listing |

Stray root inventory (hygiene track evidence): `references/` (critics ×14 persona files;
`corpus-reader/` — a full JS site-viewer lib; `gate-lint-conversion.md`;
`mcp-first-precedent.md`), `calibration/` (council-calibration, guidelines-walkthrough,
stamp-smoke — fixtures + dated run logs whose promoted `calibration_*.py` scripts already live
in `scripts/`), `reviews/` (3 dated red-team records), `templates/` (brand-stack-one-pager.md),
`.provenance/` (deliberate hidden provenance — KEEP, documented), gitignored `.name-map.md`
(deliberate — convention to be documented in make-critic).

### Phase 1 — Per-member kill-switch

| Member | Where it lives | Species | Blast radius (summary) | Merge/Split candidate? | Knowledge tier | Verdict |
|---|---|---|---|---|---|---|
| brand-corpus | stays (charter home ruling) | skill (model-only pack) | its own references/, .mcp.json wiring notes, every corpus-consuming procedure cites it | NO — dup evidence is one restated provenance paragraph, below plan-skill-merge's bar | KNOWLEDGE · move-to-references (long-body 9,953) | MOVE (S2: diet + gains the resolution ladder) |
| brand-guidelines | stays | skill (model-only pack) | make-brand-guidelines, guidelines_ledger.py, design-skills:brand-decomposer stale seam | NO — same single-paragraph dup | KNOWLEDGE · move-to-references (long-body 6,858) | MOVE (S1 handle fix; S2 diet) |
| brand-methodology-rules | stays | skill (model-only pack) | make-brand + council personas cite the Foundation Canon | NO | KNOWLEDGE · move-to-references (long-body 8,751; dense-description 729) | MOVE (S2 diet + description diet) |
| brand-rubrics | stays | skill (model-only pack) | check-brand-rubric, check-brand-council | NO — same single-paragraph dup | KNOWLEDGE · move-to-references (long-body 6,969) | MOVE (S2 diet) |
| check-brand-council | stays | skill (dual) — procedure/orchestrator | 14 persona files (inlined at dispatch), brand-judge, calibration fixtures, sub-council groupings | NO | PROCEDURE — keep-inline (roster table may move to references/ inside S3, not a tier change) | MOVE (S1 re-home of critics under it; S3 two-phase refactor to instance-of-general) |
| make-brand | stays | skill (dual) | brand-methodology-rules, muse-agent, brand-writer | NO | PROCEDURE — keep-inline | MOVE (S2 Project-mode branch) |
| make-brand-muse | stays | skill (dual) | muse-agent | NO | PROCEDURE — keep-inline | MOVE (S2 Project-mode branch) |
| make-brand-guidelines | stays | skill (dual) | guidelines_ledger.py, calibration/guidelines-walkthrough | NO | PROCEDURE — keep-inline | MOVE (S1 fixture re-home; S2 Project-mode branch incl. declared no-filesystem ledger degradation) |
| make-brand-stack | stays | skill (dual) | templates/brand-stack-one-pager.md | NO | PROCEDURE — keep-inline | MOVE (S1 template re-home; S2 Project-mode branch) |
| check-brand-orientation | stays | skill (dual) | brand-corpus layout conventions | NO | PROCEDURE — keep-inline | MOVE (S2 Project-mode branch — absent-from-uploads vs missing-from-brand distinction) |
| check-brand-rubric | stays | skill (dual) | brand-rubrics | NO | PROCEDURE — keep-inline | MOVE (S2 Project-mode branch) |
| file-brand | stays | skill (dual) | brand_stamp.py, brand_lint.py, calibration/stamp-smoke | NO | PROCEDURE — keep-inline | MOVE (S1 fixture re-home; S2 declares filesystem-only where scripts are load-bearing) |
| file-brand-corpus | stays | skill (dual) | build_sitemap.py, references/corpus-reader lib | NO | PROCEDURE — keep-inline | MOVE (S1 corpus-reader re-home to its assets/; S2 declares filesystem-only) |
| agents/brand-judge | stays | agent (dispatched, unnamed) | check-brand-council fan-out; every persona file cites its severity convention | NO | n/a (agent) | MOVE (S3 gains the deliberation-round contract; blind phase contract unchanged) |
| agents/brand-writer | stays | agent (dispatched) | make-brand voice work | NO | n/a | NO MOVE — untouched by this campaign |
| agents/muse-agent | stays | agent (dispatched) | make-brand-muse; naming exemption | NO | n/a (long-body 6,704 noted; no diet forced — agent bodies bill on dispatch only) | MOVE (S4: register `muse` in RoleLex via manifest-authoring; exemption retires; no rename) |
| NEW: council-rules | brand-design (charter job evidence) | skill (model-only pack) | check-brand-council, make-council, make-critic will cite it | n/a | KNOWLEDGE (new) | BUILD (S3) |
| NEW: make-critic | brand-design (charter) | skill (dual) | critic template, .name-map.md discipline, roster + sub-council registration, calibration seed | n/a | PROCEDURE | BUILD (S4) |
| NEW: make-council | brand-design (charter) | skill (dual) | council-rules, roster file conventions | n/a | PROCEDURE | BUILD (S4) |
| NEW: council-marshal | brand-design (charter) | agent (dispatched moderator seat) | check-brand-council phase 2; patterned on teamwork:fleet-marshal's strict-router contract (named mention only — no cross-plugin preload) | n/a | n/a | BUILD (S3) |
| NEW: ~4 role-category packs | brand-design (charter) | skills (model-only packs) | make-critic grounding; clustering of the 14 personas (~strategy / identity-design / voice-writing / advertising-creative), finalized inside S5's build | n/a | KNOWLEDGE (new) | BUILD (S5) |

Wave 0 verdict: **no merge/split nominations** — the only cross-member duplication evidence
(three identical provenance paragraphs) is a centralize-in-place fix, not corpus overlap; no
routing steal/leak survives the 2026-08-19 fix. Stated per the falsifiability rule.

### Phase 2 — Waved ticket seeds (minted 2026-08-20 post-Gate-A as GitHub Issues, per ADR-0002)

#### Wave 0 — merge/split nominations
- none (verdict above)

#### Wave 1 — mechanically-clean moves
- [ ] S1 (#824) structure re-home + stale-handle repair (Blocked-by: none) — status: todo — done-when: zero stray root dirs beyond `.provenance/`; every moved path's referrers repaired; `design-skills:brand-decomposer` handles fixed; provenance paragraph centralized to one home; gate green

#### Wave 2 — species changes (semantic — critic pass + eval rewrite required)
- [ ] S2 (#825) portability (Blocked-by: S1) — knowledge tier: move-to-references ×4 + description diet — status: todo — done-when: resolution ladder canonical in brand-corpus; every procedure declares its Project mode (or filesystem-only, disclosed); all 4 bloat flags cleared; manifest description evals-first-rewritten; checker + scoped re-judge green
- [ ] S3 (#826) council generalization (Blocked-by: S1) — status: todo — done-when: council-rules pack live; check-brand-council is an instance of the general machinery; council-marshal seat exists; two-phase council runs (blind calibration fixtures still green + a deliberation calibration fixture); brand-judge deliberation contract; checker + re-judge green
- [ ] S4 (#827) minting (Blocked-by: S3) — status: todo — done-when: /make-critic and /make-council produce a conforming critic/council end-to-end; `muse` registered in RoleLex, muse-agent exemption retired; checker + re-judge green
- [ ] S5 (#828) role-category packs (Blocked-by: S1) — status: todo — done-when: ~4 packs live, clustered from the personas with the clustering recorded; pack-writing-rules conformant; evals + fences; checker + re-judge green

#### Wave 3 — contested
- none — every design fork was closed at the find-intent round (2026-08-20)

#### Wave 4 — prove
- [x] S6 (#829) campaign proof (Blocked-by: S2, S3, S4, S5) — status: done — done-when: full blind /check-routing brand-design clean (routing-report row updated); fix-old-names sweep zero LIVE; the walkthrough demonstrably runs: mint a critic → seat it in a sub-council → run blind + deliberation phases in Claude Code AND the declared sequential mode

#### Grandfathered
- none (muse-agent's exemption retires via S4's vocab registration rather than riding)

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
- **A merge/split executed via `/reshape-skill`** — n/a this campaign (Wave 0 empty).
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

Gate A was given 2026-08-20 ("Approve all 6"). Seeds are minted as GitHub Issues and the waves
run serially via build-leader dispatches (PR-opened ceiling, merge-on-green). On completion
(every wave's tickets closed), flip `status: complete` and move this file to the docs archive
per PLAN's living-state contract — never leave a finished plan `active`.

## Completion (2026-08-21)

All five waved tickets (S1 #824, S2 #825, S3 #826, S4 #827, S5 #828) merged; this file's own S6
(#829) closes the campaign with the proof wave — full blind `/check-routing brand-design` clean
(0 dead/stolen/leaked across 20 suites/182 cases, two real stolen findings the same wave's own
proof surfaced and fixed same-change: `brand-methodology-rules`'s build-action triggers ceded to
`make-brand` mirroring S2's own `brand-guidelines` fix, and `make-critic`/`check-brand-rubric`
gained NOT-clauses fencing the four role-family packs' own lens-grounding questions), a zero-LIVE
`fix-old-names` sweep, and the mint-and-run walkthrough (a demo critic, `sam-r`, minted end to
end and unseated after proving the pattern — see this PR's own Findings for the full run).
**Archive-location check:** no `.claude/docs/` archive-for-completed-PLANs convention exists yet
in this workspace (no `archive/` subdirectory under any doc type as of this date) — `status:
complete` above is flipped in place per the fallback this file's own "Next step" names, rather
than moved, since there is nowhere established to move it to. A future `PLAN` archive convention,
if one is ever ratified, should sweep this file in retroactively rather than this file inventing
one unilaterally.
