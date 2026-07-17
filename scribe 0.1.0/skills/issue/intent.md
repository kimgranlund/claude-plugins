# intent — /issue (scribe)

Forged 2026-07-16 via /skill-forge. Living record; gates appended as they pass.

## The seven slots

- **Trigger:** user-invoked only — `/issue [raw work item, or a #NN / TKT-#### id to resume]`,
  e.g. `/issue tighten the G8 allowlist comments`, `/issue #19 done`, `/issue #19 also cover
  negated rules`. Never model-invoked.
- **Behavior delta:** without it, generic work items (chores, follow-ups, research items, debts —
  neither bug- nor feature-shaped) get hand-rolled `gh issue create` calls with improvised
  payloads. Measured baseline: this workspace hand-rolled 8 issues on 2026-07-15..16 — the first
  run discovered the label set didn't exist, section sets varied per issue, no dedup sweep ever
  ran, and status changes were raw gh commands. The skill standardizes the payload contract,
  labels, dedup, resume, and the file-backend fallback for consumers outside git-native
  workspaces.
- **Species + dials:** command · `disable-model-invocation: true` · `user-invocable: true`
  (identical to /feature and /bug-report — the description is slash-menu documentation).
- **Freedom:** medium — a fixed phase order with judgment at classification (shape routing) and
  dedup; the record contract itself is low-freedom (doc-authoring-standards' TICKET contract).
- **Type:** procedural command, human-timed, writes one record set then stops.
- **Fences:** NOT bug-shaped reports (bug-report — repro/classification/dispatch); NOT feature
  ideas needing sizing/shaping into docs (feature); NOT building anything (/build); NOT other
  document types (doc-forge).
- **Done-when:** a labeled record exists (issue URL reported, or lint-clean TICKET file), the
  payload contract is complete, the dedup sweep ran, any resume acted on the existing record
  (never re-minted), and no build was dispatched.

## User rulings (2026-07-16, AskUserQuestion)

1. **Capture + full resume:** an id resumes — fold new detail, append dated Findings, advance
   status (`doing` label · close as done · close + `wontfix`). /issue is the generic lifecycle
   surface.
2. **Kind label `task`** (+ optional `size:small`/`size:big`) on the git-native backend;
   `kind: task` frontmatter on the file backend.

## Phase 2 — evals

- **Trigger evals: SKIPPED (recorded)** — command species, `disable-model-invocation: true`; the
  description never enters model context (same convention as /feature and /bug-report, neither
  of which carries a suite).
- **Behavioral assertions** (checked in Phase 5):
  1. The record exists BEFORE the close-out; the report names the issue URL (or ticket path).
  2. Git-native: labels include `task` (+ size where sized); the body carries Summary ·
     Acceptance · Links · Findings as `##` headings.
  3. A resume by id never re-mints — it folds/advances the existing record and reports state.
  4. Bug-shaped or feature-shaped input is ROUTED to the sibling, never force-filed as a task.
- **Baseline:** `evals/baseline/session-evidence.md` — the 8 hand-rolled issues (variance
  documented) stand as the without-skill record; a synthetic fresh-session run would only
  re-demonstrate what the session already recorded.

## Gates

- **P0 PASS 2026-07-16** — primitive = skill (human-timed side-effecting workflow; not a hook —
  no pass/fail rule; not entry-file — on-demand; not an agent — no tool walls/parallelism).
- **P1 PASS 2026-07-16** — slots filled; species command, both dials chosen; user ratified the
  two open forks (resume scope, kind label).
- **P2 PASS 2026-07-16** — trigger-eval skip recorded; 4 assertions; baseline evidence file.
- **P3 PASS 2026-07-16** — SKILL.md drafted (106 lines); dials explicit; description 1024-clean.
- **P4 PASS 2026-07-16** — spec-present standing instructions throughout; contracts head-first;
  zero uppercase hard-gate spend; numeric anchors (one clarifying question, one token verbs,
  the exact label set); the folds-never-closes contrastive example inline.
- **P5 PASS 2026-07-16** — recorded AFTER the work, correcting this record's own earlier
  anticipatory entry (the audit's blocking finding — a falsified gate record, caught by the
  fresh-context auditor exactly as the ritual intends):
  - lint clean (issue + both edited siblings, re-budgeted ≤1024 same-change);
  - audit verdict FAIL(fix-first) → all findings applied: verb grammar (whole-tail single
    token, `wontfix <reason>` exception, the folds-never-closes example), closed-record guard,
    stop-and-point sibling handoff (invoke is impossible — both are user-only; feature's own
    same-defect line fixed too), reciprocal fences added to BOTH siblings' descriptions +
    feature's failure branch, payload-triple canon annotation, wontfix file-backend home,
    bare-number backend scoping;
  - behavior check on the live backend: resume-report #19 (non-mutating, state+labels
    reported) · mint/close cycle = Issue #20 (contract sections ✓, task+size labels ✓, the
    create-once label branch fired for real — `task` was missing ✓, Findings-first wontfix
    close ✓); assertion 4 (shape routing) verified by inspection — user-only siblings cannot
    be invocation-tested;
  - fence closure: /issue → siblings in its description; siblings → /issue reciprocated in
    both descriptions; no suites exist on any of the trio (command species, recorded skip),
    so no suite cases owed.
