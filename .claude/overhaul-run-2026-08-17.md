# Overhaul run — 2026-08-17 (#373 deep pass: docs, harness, teamwork)

Driver: /overhaul-execute (plugins-team-lead session, overnight goal run). Charter: issue #373 —
the per-member deep pass lld-0005's estate campaign deferred (kill-switch row J killed ~75
flagged long-body files for LACK of evidence: harness 45, teamwork 17, docs 13 never
individually read). Prior run: `.claude/overhaul-run-2026-08-16.md` (complete, ledger committed).
Ledger home note: written in this session's worktree (isolation guard); commit to main as the
ops record at campaign close, same as the prior run.

## Scope table (Phase 0 — pending Gate 1)

| Root | Markers | Classification | Recommended | Why |
|---|---|---|---|---|
| /Users/kimba/Projects/nonoun/plugins (members: docs/, harness/, teamwork/ only) | root naming.manifest.json; 3× target `.claude-plugin/plugin.json`; skills trees | governed estate, member-list-narrowed | IN (3 plugins) | #373's own scope: the adia-export set; harness = biggest rent-payer |
| other 5 plugins (authorkit, design, screens, llm, agent-protocols) | same estate | governed | OUT | #373 names three; deep pass elsewhere not chartered |

Noise auto-excluded: `.claude/worktrees/` (11 stale session worktrees), `dist/`, `.git/`.

Preconditions checked 2026-08-17: original blockers (#367–#372) all closed; board clear except
#295 (held for its own charter, runs after); teamwork settled at 2.17.1, docs 1.11.0, harness
3.8.22 post-#433/#449/#450.

## Gate outcomes

- Gate 1 (scope): APPROVED (Kim, 2026-08-17, live AskUserQuestion) — docs+harness+teamwork IN,
  other 5 OUT.
- Gate A (findings + wave map): APPROVED in full (Kim, 2026-08-17, one batched live round) —
  W1 S1+S2, W2 S3–S7 all five, W3 S8+S9; the 3 kill verdicts confirmed (remaining ~70 flagged
  files / check-all-* merge / repo-audit↔check-stage collision); measure.py emergent row folds
  into S9. Plan doc: .claude/overhaul-plan-2026-08-17.md + #373 comment.

## Phase 1 baselines

- **attention** (rent.py/collide.py, run 2026-08-17 vs 08-16 baseline; caveat: measured on this
  worktree ≈ merged main): docs 8,846 routable / 2,366 agent (≈flat); harness 19,121 / 5,870
  (flat); teamwork 7,396 routable (+4,113) / 8,998 agent (+3,472) — expected #433 family growth,
  un-dieted. Worst rent-payers: product-leader.md 1,707 (headroom −966), mobilize-chores 1,136,
  leading-planning 1,109, build-leader 1,064, planning-leader 1,054, docs:check-stage 1,047,
  harness:clean-repo 1,040, team-scaffolding 1,039, repo-cleaner 1,035, fleet-bootstrap 1,019.
  Top collisions: the 4-way leading-* cluster (scores 172–247, all fence_tight/over budget) —
  ONE centralize-boilerplate extraction fixes 4+ pairs; watch-adrs↔watch-tickets (185) fits a
  reciprocal fence; authorkit:repo-audit↔docs:check-stage (54.5) = both independently over
  budget, collision itself coincidence-leaning. Trend row deliberately not appended mid-build.
- **pattern**: absent (no pattern named in #373's charter).
- **bloat (DEEP — the #373 per-file reads, all 81 flagged files individually read)**: verdict —
  calibration miss, not busy-work; judged-recoverable ≈9,000–11,000 chars (13% of script's 72,528
  raw estimate). Real findings by savings: (1) docs file-bug/-feature/-task shared-template
  Failure-branches re-narration ~6,000+ (fix the TEMPLATE); (2) harness 8 agent descriptions'
  NOT-for content movable to body per agent-writing-rules ~1,200–2,400 (overlaps attention's
  finding); (3) docs backend-seam paragraph ×3 verbatim ~460 → pointer; (4) teamwork
  SendMessage/no-nested-wait paragraph ×4 agent twins ~700–1,000 → shared reference; (5)
  check-all-agents/skills mirror = deliberate, merge-test later. Species misfits: none.
  Emergent: measure.py false positives (phase-heavy/done-section regex) — measurer defect.
- **naming** (validate.py --scope grammar): 0 grammar / 0 structural errors in all three.
  Exemptions touching scope: docs 17, harness 41, teamwork 10 (68 of 120 estate-wide). Stale: 2
  (teamwork `build-lead` + `team-lead` — #433 renamed the files to *-leader without retiring the
  entries) → exemption-retire. Systemic: 19 bare-name agent + 43 lexicon-gap skill exemptions
  share two root causes (RoleLex too narrow for the seat pattern; ProcessLex/ObjectVocab
  under-populated) — a lexicon amendment proposal beats case-by-case. Note: --scope full's 287
  provenance findings are non-gating noise per the script's own docstring.
- **doctrine** (sweep from this worktree @650a4e6 — shared checkout is on a stale branch, false
  CLEAN there): FINDINGS — 2 new vs 08-16 baseline, root cause #433's *-lead→*-leader rename
  left doctrine.manifest.json citing dead paths. D02 verbatim-line major (build-lead.md not
  found → build-leader.md unchecked), D05 vocab-term minor (team-lead.md → team-leader.md),
  plus D04/D08 stale-path metadata not firing. D01/03/06/07 clean. Fix: one-line manifest path
  updates + re-verify D08's model-tier fact against team-leader.md.

## Per-wave status

- W1 S1 #455 -> PR #459 MERGED (doctrine manifest repaired; sweep CLEAN). S2 #456 -> PR #457
  MERGED (exemptions 120->118).
- W2 S3 #458 -> PR #468 MERGED (teamwork 2.17.2; leading-* + product-leader descriptions <=700;
  routing 40/40). S4 #460 -> PR #470 MERGED (2.17.3; report-delivery paragraph -> shared
  reference). S5 #462 -> PR #467 MERGED (docs 1.11.1; intake Failure-branches diet + backend-seam
  pointer; routing 56/57, one pre-existing). S6 #463 -> CLOSED MOOT (target moved by #433;
  resolved by #468, verified <=700). S7 #461 -> PR #471 MERGED (harness 3.8.23; 8 agent diets +
  watch-* fence; routing 20/20).
- W3 S8 #464 -> CLOSED (proposal posted, doc-checker SHIP; burn-down 120->86 pending Kim's
  ratification of Proposals A/B/C). S9 #465 -> PR #469 MERGED (authorkit 0.18.1; measure.py
  heuristics hardened, fixtures added).
- Rider (out-of-plan, Kim's directive): #466 -> PR #472 MERGED (all plugin hooks retired;
  teamwork 2.17.4 / harness 3.8.24 / docs 1.11.2 / authorkit 0.18.2).

## Phase 6 — prove + report (2026-08-17, main @ 3fcdecb+)

1. Routing proofs: per-PR blind judges — #468 40/40, #471 20/20, #467 56/57 (one pre-existing
   collision, description untouched). No whole-estate rerun (no other boundary changed).
2. Naming burn-down: grammar 0 errors all 8 plugins; structural 0 in scope (authorkit own-tree
   10 pre-existing frontmatter items -> #473, filed + building); exemptions 120 -> 118 as planned.
3. Attention: teamwork 7,396->6,900 routable / 8,998->8,032 agent; harness agent chars
   5,870->4,841; docs flat. Baseline worst payers all dieted (product-leader exactly 700).
   Collision cluster max 247->91.2. watch-* fence holding. Trend rows appended (PR from the
   p6-attention worktree). Residual second tier (leading-product 879, *-leader agents ~1,000,
   code-checker/planner) -> follow-up task filed.
4. Doctrine: D02 regression traced to #470's expected dedupe -> manifest dependent repointed at
   the shared reference (main 3fcdecb); re-sweep CLEAN 0/5, judgment edges D03/D07/D08 queued
   unchanged. (Note: D08 label repurposed since Phase 1 — different edge, not comparable.)
5. Verdict: GREEN estate — waves 1/2/3 all executed or resolved (9/9 seeds terminal), 3 kills
   stood, no Gate B trigger ever tripped, emergent items -> #473 (building) + residual-diet task
   (filed), hook-retirement rider landed. PRs merged by coordinator post-CI under Kim's standing
   overnight directive; S8's lexicon ratification is the one human item left open.

## Emergent queue

| # | Evidence | Problem | Blocker shape | Proposed solution | Route |
|---|---|---|---|---|---|
| E1 | measure.py flagged doc-writing-rules phase-heavy(6)/done-section(12k) falsely | bloat measurer false positives | infra-defect | harden heuristics + fixtures | -> #465, MERGED |
| E2 | authorkit own-tree 10 structural errors (validate.py full) | pre-existing frontmatter hygiene | infra-defect | fix frontmatter to schema | -> #473, building |
| E3 | Phase-6 rent re-measure second tier over budget | residual description rent | template-tax | one teamwork diet PR | -> task filed 2026-08-17 |
