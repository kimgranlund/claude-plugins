---
doc-type: plan
id: plan-2026-08-brand-design-bloat-overhaul
status: active
date: 2026-08-21
owner: Kim Granlund
audience: human, builder
review-cadence: per-wave (re-reviewed whenever a wave's tickets land or the campaign resumes)
---
# Overhaul plan — brand-design (bloat + spec-staleness pass) — 2026-08-21

**Verdict up front: Phase 1 killed every move, rename, and merge — this is a no-restructure
campaign. The six approved seeds are three bloat-hygiene items (Wave 2) and three estate-wide
spec rulings (Wave 3).** Second campaign over this plugin, one day after the council-platform
overhaul closed (`plan-2026-08-brand-design-overhaul.md`, status: complete, seeds #824–#829).
Gate A given 2026-08-21 ("Approve all 6 seeds"). Charter: `/overhaul-planning brand-design
plugin`, measured on the live tree with #838 (roster-as-data) building in-flight — caveats
below.

## Steps

### Phase 0 — Measurements (2026-08-21)

| Instrument | Available? | Finding summary |
|---|---|---|
| naming-audit | yes (workspace-root manifest) | Plugin name + all member shapes conform. The dispatched sweep's 2 agent violations (`council-marshal`, `muse-agent`) DISSOLVE against the workspace-root `naming.manifest.json` (`marshal` ∈ role_lex; `muse` ∈ object_vocab, registered by S4 #827) — the sweep ran plugin-scoped where no manifest lives by design. Residual: the instrument itself refuses "ungoverned" at plugin scope without checking the estate root (seed S6). |
| bloat-audit | yes (live thresholds 6000/700 content/0.5) | 7 flagged: long-body ×5 — check-brand-council 14 834, make-critic 10 732, make-council 10 157, brand-judge 6 749, muse-agent 6 704; dense-description (content chars) ×3 — make-critic 813, brand-methodology-rules 857, check-brand-rubric 776. 20 near-duplicate pairs (Jaccard 0.51–1.0), ~14 000 recoverable chars, concentrated in the 4 `*-facts` packs (3 shared scaffolding blocks + a live "three vs four lenses" copy-drift) and the corpus/guidelines/rubrics provenance sentence (×3 verbatim). |
| check-routing (harness) | yes (reused, not re-run) | 0 dead / 0 stolen / 0 leaked across 20 suites / 182 cases — S6 #829's full blind proof, dated 2026-08-21 (same day). |
| plan-plugin-split surface_map (harness) | yes | 39 nodes (20 skills, 4 agents, 15 scripts), 126 edges (113 mention, 13 script); 0 cross-plugin hard edges; 0 dangling references. `gaps`: file-*/make-* families lack standards/command/script — no job evidence any is a gap (anti-matrix), not carried forward. |
| doctrine-audit | no | No `doctrine.manifest.json` on target — doctrine-drift evidence unavailable for this run; not invented. |
| pattern-audit | not fired | Charter names no pattern. |

**Measurement caveats.**
1. **#838 in-flight contamination:** roster-as-data was building on `live/roster-as-data` in
   this working tree during measurement — bloat rows for `check-brand-council`,
   `council-rules`, `make-critic`, `make-council` reflect a mixed state and SHRINK when #838
   lands (it moves the roster table out of check-brand-council's body). Seed S3 re-measures
   after #838 before any trim verdict.
2. **Estate-wide spec staleness, not brand-design defects:** `evals/` top-level in 20/20
   skills and `intent.md` in 4/20 sit outside spec-naming-convention §6.1's closed folder set;
   0/4 agents carry the §8 frontmatter schema — and sampled agents in harness/teamwork/docs
   carry none either. Both route to Wave 3 spec rulings, never per-member remediation.

### Phase 1 — Per-member kill-switch

| Member | Where it lives | Species | Blast radius (summary) | Merge/Split candidate? | Knowledge tier | Verdict |
|---|---|---|---|---|---|---|
| make-brand, make-brand-guidelines, make-brand-muse, make-brand-stack, check-brand-orientation, file-brand, file-brand-corpus | no move — job evidence per member in README table; routing clean (S6) | dual (skill+command) | n/a — no move proposed | NO — no duplicate pair, no steal/leak | PROCEDURE — keep-inline (always) | NO MOVE |
| check-brand-council | no move | dual | #838 touches it now (roster → references/roster.md) | NO | PROCEDURE — keep-inline; long-body 14 834 measured MID-#838 → re-measure (S3) | NO MOVE |
| make-critic, make-council | no move | dual | #838 touches make-critic's seating step | NO | PROCEDURE — keep-inline; long-body 10 732/10 157 → re-measure (S3); make-critic dense-description 813 → diet (S1) | NO MOVE |
| check-brand-rubric | no move | dual | none | NO | PROCEDURE — keep-inline; dense-description 776 → diet (S1) | NO MOVE |
| brand-methodology-rules | no move | skill (knowledge, model-only) | mention edges only | NO | KNOWLEDGE · keep-inline (body 5 877 ≤ 6 000); dense-description 857 → diet (S1) | NO MOVE |
| brand-corpus, brand-guidelines, brand-rubrics | no move | skill (knowledge, model-only) | mention edges only | NO — duplicate hit is ONE identical provenance sentence ×3 (pairs 9–11, sim 1.0): centralization, not merger | KNOWLEDGE · keep-inline (bodies 5 972/5 741/4 813 ≤ 6 000); dedup rides S2 | NO MOVE |
| brand-advertising-facts, brand-identity-facts, brand-strategy-facts, brand-voice-facts | no move | skill (knowledge, model-only) | mention edges only | NO MERGE — S5 #828's clustering is deliberate and recorded; duplicate pairs 1–8, 12–20 are shared SCAFFOLDING blocks (sim 0.51–1.0) incl. a three-vs-four-lens copy-drift, not corpus overlap; routing 0 steals between them (S6) | KNOWLEDGE · keep-inline (bodies 3 112–4 124); scaffolding dedup rides S2 | NO MOVE |
| council-rules | no move | skill (knowledge, model-only) | #838 adds roster-file-contract reference | NO | KNOWLEDGE · keep-inline (4 606) | NO MOVE |
| brand-judge, muse-agent | no move — names conform per workspace manifest | agent | brand-judge inlined-dispatch shell for 14+ personas; muse-agent dispatched by make-brand-muse | NO | agent bodies 6 749/6 704, marginally over 6 000 — contract text load-bearing by default; trim only what S3's re-measure pass still flags as non-load-bearing | NO MOVE |
| council-marshal, brand-writer | no move — `marshal` ∈ role_lex (workspace manifest) | agent | council-marshal is #826's Chair seat | NO | clean (3 844/4 043, no flags) | NO MOVE |

Killed at this phase, with cause: every rename (0 naming violations survive the workspace-
manifest re-read); every merge/split (0 nominations — duplicate evidence is scaffolding/
provenance boilerplate, and routing shows 0 steals); per-plugin `naming.manifest.json`
seeding (the workspace-root manifest governs — a plugin-local manifest would fork the
lexicon, the exact defect authorkit's manifest discipline exists to prevent).

### Phase 2 — Waved ticket seeds (not yet minted)

#### Wave 0 — merge/split nominations
- none — no nomination survived Phase 1 (evidence cited in the kill-switch table)

#### Wave 1 — mechanically-clean moves
- none — no move survived Phase 1

#### Wave 2 — species changes (semantic — critic pass + eval rewrite required)
- [ ] S1 — description diets ×3: make-critic (813 content chars), brand-methodology-rules
  (857), check-brand-rubric (776) → ≤700 each, evals updated in-change + scoped blind
  re-judge per suite (the v1.0.4/t05 dead-trigger class guards the trims — recorded in
  design/README.md's ledger v1.0.4 entry and make-variants' evals.json dated note, 2026-08-21)
  (Blocked-by: #838 —
  it edits make-critic's routing surface) — status: todo — done-when: all three ≤700 content
  chars, skill_lint W8 clean, scoped re-judge shows no dead/stolen trigger, checker pass clean
- [ ] S2 — dedup the shared scaffolding (~14 000 recoverable chars, all 20 duplicate pairs
  cited): the 4 `*-facts` packs' three repeated blocks → one shared home (cite council-rules
  or one shared reference), fixing the three-vs-four-lens drift as part of the move; the
  corpus/guidelines/rubrics provenance sentence → stated once (`.provenance/` or one pack),
  cited from the other two (Blocked-by: none, but NOTE — #838 touches council-rules in-flight;
  land after it or pick the `.provenance/` home that avoids the file) — status: todo —
  done-when: measure.py
  duplicate_pairs = 0 for the cited pairs, no content lost (each block's single home carries
  the union), checker pass clean, gate green
- [ ] S3 — post-#838 long-body re-measure: check-brand-council, make-critic, make-council,
  brand-judge, muse-agent re-measured on the merged tree; trim ONLY what still flags, per
  bloat-audit's CALIBRATION.md load-bearing test (Blocked-by: #838, S2) — status: todo —
  done-when: re-measured numbers recorded here with a dated note; every member either under
  6 000 or its overage justified line-by-line as load-bearing
#### Wave 3 — contested
- [ ] S4 — spec-naming-convention §6.1 closed folder set is stale: `evals/` (20/20 here,
  mandated estate-wide by plugin-authoring.md) and `intent.md` (4/20) are outside the closed
  set — open question: amend via the ADR-0011 amendment path (add `evals/`; rule intent.md in
  or route it into references/) (Blocked-by: none) — status: todo — done-when: a human
  rules and the spec's closed set and the estate's real convention agree — via an amendment
  ADR or a ruled remediation path; either outcome satisfies this seed
- [ ] S5 — agent frontmatter schema (§8) unpopulated estate-wide (0/4 here; sampled
  harness/teamwork/docs agents carry none) — open question: populate every agent, or amend
  the spec to match the estate's real name+description(+model/tools) convention (Blocked-by:
  none) — status: todo — done-when: a human rules one way and the follow-up work item (if
  any) is minted
- [ ] S6 — authorkit instrument gap: `validate.py --target <plugin>` reports "ungoverned"
  without checking for a governing manifest at an ancestor estate root — today's
  false-violation source (Blocked-by: none) — status: todo — done-when: filed to authorkit
  as a bug with this run's repro; validate.py resolves the nearest governing manifest or
  names the scoping rule explicitly

#### Grandfathered (can't move cleanly — ADR-0011 D8 ratchet)
- none

### Phase 3 — Execution contract (per ticket, once approved)

claim → worktree → `git mv` (history preserved) → supersession note or `renames.json` entry
→ gates + critics → PR → human merge → verified close. Serial through shared ledgers
(`naming.manifest.json`, `renames.json`) — two tickets never touch the same ledger entry in
parallel.

## Validation

How the whole plan proves itself, per wave, once its tickets land:

- [ ] `/check-routing` clean for every touched plugin (S1's trims re-judged scoped; a full
  brand-design run at campaign close)
- [ ] `fix-old-names` sweep run against consumer repos
- [ ] Records amended with dated supersession notes (never rewritten)
- [ ] S3's re-measured bloat numbers recorded in this doc with a dated note

## Rollback

The undo per irreversible step, decided now, not during the incident:

- **A landed `git mv` (Wave 1/2)** — n/a this campaign (no moves survived Phase 1); the
  template's revert path stands if a wave ever adds one.
- **A ledger entry retired (`naming.manifest.json`, `renames.json`)** — re-add the entry
  verbatim from the pre-change git history; the exemptions array is shrink-only by ratchet,
  but a rollback restoring a wrongly-retired entry is a correction, not a forced re-grant.
- **A supersession note** — supersession notes are themselves append-only (docs-mutability);
  rollback of a wrongly-superseded record is a NEW dated note reversing the prior one, never
  an edit or deletion of the note itself.
- **A merge/split executed via `/reshape-skill`** — n/a this campaign (Wave 0 empty).
- **A ticket seed approved and minted, then abandoned mid-build** — the dispatch's own claim
  release (ADR-0005) already covers this: `--remove-assignee`/`--remove-label in-flight` plus
  a release comment; no plan-doc rollback owed beyond flipping that seed's status back to
  `todo`.
- **S2's dedup (content centralized out of 7 SKILL.md bodies)** — each removed block's single
  new home is stated in the S2 PR; revert the PR's merge commit to restore every restated
  copy; no `.refactor-attic/` owed because git preserves the full prior text.
- **S1's description trims** — revert the seed's PR merge commit (description + eval edits are
  one change by plugin-authoring.md, so the revert is atomic); re-run the scoped re-judge
  after the revert so the suite never tests a description that no longer exists.

## The five respect invariants

1. Evidence can veto the plan.
2. History preserved, never replaced.
3. Consumers degrade gracefully.
4. The old design's intent is read before it is judged.
5. Nothing semantic rides hidden in a move.

## Next step

This plan and its ticket seeds are generated only — nothing above has been executed. Gate A
was given 2026-08-21 ("Approve all 6 seeds"). Each approved row is minted through its owning
intake skill (`file-feature`/`file-task`), never auto-created here; S4/S5 are rulings to put
in front of a human before any work item exists. On completion (every wave's tickets closed
or grandfathered), flip `status: complete` — the workspace has no PLAN archive convention yet
(see the prior brand-design plan's Completion note); flip in place until one is ratified.
