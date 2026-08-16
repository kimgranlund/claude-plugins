# Charter: complete mobilize Batches C, D, E — coordination record
# STATUS: CLOSED 2026-08-16 — decision: DONE. All 11 tickets complete (see Batch state).
# Close-out seeds minted via intake-lead (F4/F5 experiments, stall-rule, version-slot rule).

Bound 2026-08-16 via /lead-team (host-as-coordinator, teamwork 2.12.2 contract). Kim's batched
confirm for all 11 tickets was given in the original mobilize round (2026-08-15); the earlier
interrupted attempt left zero residue (repo-cleaner 00:36Z report). Merges are driven by the
coordinator after gates pass, per Kim's explicit "do it" precedent on the previous 7-PR chain.

## Sequencing constraints (standing)
- agent-writing-rules chain, strictly serial: #267 (C) → #272 (D) → #274 (E). #260 already landed.
- harness version slots: one harness-bumping build in flight at a time (#267 ∥ #271 forbidden;
  #271 dispatches after #267 merges). Same rule per plugin for D/E.
- #266 dispatches after #265's measurement lands (soft dependency, ticket's own note).
- #273 needs Kim's answers to its 5 named gaps — batched AskUserQuestion at Batch E dispatch.
- #256 dispatches through teamwork:build-lead WITH the literal `auto-merge: authorized` grant —
  that is the ticket's own acceptance test (ADR-0012 verification), authorized by Kim's confirm.

## Batch state
- Batch C: CLOSED (decision: done). #267 (PR #298, harness 3.7.1) · #268 (PR #299, teamwork
  2.12.3) · #271 (PR #301, harness 3.7.2) all merged+closed · #281 verdict-closed · #300 minted.
- Batch D: CLOSED (decision: done). #272 (PR #302, harness 3.7.3) · #262 (PR #303,
  CLAUDE.md -930 chars + .claude/rules/ x5) both merged+closed ·
  #256 DONE — grant-carrying dispatch blocked by auto-mode classifier at dispatch-creation;
  Kim ruled the block IS the outcome; recorded as ADR-0013 (narrow supersede of ADR-0012's
  deployment-prerequisite bullet — T4 blocks in-place appends to accepted ADRs, seat-verified),
  commit 827a032, issue closed. Wave 2: #265 solo after wave 1 (ops-state race avoidance).
- Batch E: CLOSED (decision: done). #274 (PR #305, harness 3.7.4) ·
  #273 DONE (PR #304 merged — IDR PRD on main; Kim ruled cardinality = bible's shape, plural
  IDRs + one index, recorded on the issue) · #265 DONE (closed, reusable finding) ·
  harvest-edit DONE (PR #306 merged, harness 3.7.5, ADR queue cleared) · #266 DONE
  (PR #307 merged, harness 3.8.0 + teamwork 2.13.0 — chore-lead RETIRED, choreography in
  harness/workflows/chore-sweep.js + verified fallback; sweep-chores now model-invocable,
  new eval suite blind-judged 13/13 post-vote with t04 flip annotated).
- #273 rulings (Kim 2026-08-16): docs-plugin type contract; one founding doc; append-only+
  supersede; spine+indexing+auto-mint. SUPERSEDING INPUT forwarded mid-build: Kim's
  .claude/docs/spec/product-lifecycle-bible.md defines IDR (Intent Decision Record) as the
  existing doctrine concept — seat instructed to realize IDR (bible = concept authority),
  reconcile rulings (one-doc ≈ the living index/product brief; IDRs plural locked records),
  surface any genuine conflict as an open question.
- ADR-queue confirm (Kim 2026-08-16): BOTH candidates, ONE combined edit to who-ships-what.md
  (harvest ADR-0013 finding + repair stale ADR-0012 citation). Harness slot queue:
  #274 (3.7.4) → harvest edit (3.7.5) → #266 (last).
- #265 experiment: scorer fixed pre-run. Condition (a) solo: 61,515 tok · 103.9s · 9 tool calls,
  queue caught adr-0013 delta + who-ships-what stale-citation + charter-dirt + #258 label drift.
  Condition (b) chain: RUNNING (chore-lead full fan-out, same repo state, (a) was read-only).

## Decisions ratified this charter
- #281 cycle: DONE. Verdict CONFIRMED-NEEDED (keep + trim + fence). Follow-up ticket seed to
  mint at C close: "screens:check-whole-ui — trim + fence (keep-confirmed, #281 follow-up)" —
  fence the layout-checker AGENT by name (live 53.9 collision); re-verify ui-pattern-facts
  pairing first (looks already resolved). Findings: issue #281 comment, 2026-08-16.

## Known defect classes to guard (from the 2026-08-15 round)
- build-lead "dispatch nested agent then wait" stall — seals forbid delegate-and-wait.
- Cross-PR same-plugin version collisions — serialized per plugin, chain-stacked ledgers.
- Critic model: fable (sonnet retry on AUP false-positive).
