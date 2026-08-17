---
name: check-stage
description: >-
  Read-only lifecycle-position report: which of the three nested loops (North star/Foundation/
  Releases) a repo is currently emphasizing, the build turn's current stage (of seven), and the
  version triple — derived from a typed-record census (ADR/IDR/RDD counts, status distributions,
  orphan-ADR density, ROADMAP presence) plus narrated judgment calls, each labeled mechanized or
  judgment (never a bare verdict). Use for "what lifecycle stage is this project in", "are we
  pre- or post-Spec-lock", "which loop are we emphasizing right now", "is the POC boundary
  crossed", "what's our version triple", "orient me on where this project stands in its
  lifecycle". NOT work-state — branches, worktrees, stashes, blocked-on-you, ready-to-close
  (harness check-state); NOT which doc type/sections/frontmatter to file (doc-writing-rules);
  NOT what this repo has decided/queued (project-docs); NOT the general portable doctrine
  itself — what an IDR/ADR/RDD is FOR (product-lifecycle-rules); NOT prioritizing next work
  (chore-planner).
disable-model-invocation: false
user-invocable: true
argument-hint: "[repo-root]"
---

# check-stage

One verdict-first lifecycle-position report: which loop is emphasized, which build-turn stage
is current, and the version triple — mutating nothing but its own report. The general doctrine
this report is read against lives in `docs:product-lifecycle-rules`; this skill is the live
reading, not the doctrine itself.

## Procedure

1. **Collect.** Run the bundled census against the repo root (default `.`):
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-stage/scripts/lifecycle_census.py <root>`
   — emits per-type (`adr`/`idr`/`rdd`) counts and status distributions, the orphan-ADR count,
   and ROADMAP.md presence/status. A script failure (non-zero exit) is reported verbatim; the report
   still renders judgment-tier signals from what's readable directly.
2. **Consume check-state's own JSON as an input, never re-derive it.** Where available, run or
   reuse a recent `harness:check-state` collector output (ticket status counts via its
   `ticket_state.py`, PR/release cadence via `git_state.py`) for the Releases-loop turn-cadence
   read — sources-flow-outward applied to a sibling's collector, per the PRD's Fencing section.
   No `check-state` output available → that cadence input reads "unmeasured", not guessed.
3. **Label every signal mechanized or judgment, per OUT-02 — never a bare verdict:**
   - **Mechanized** (from step 1's JSON directly): per-type counts and status ratios
     (locked-vs-draft), orphan-ADR density, ROADMAP presence, a **derived** version-triple
     candidate (outer≈IDR-cycle count, inner≈ADR count, innermost≈RDD/release count — flagged
     derived, since no file states a version triple literally).
   - **Judgment** (narrated with the signals that informed the call — never a bare boolean):
     - *Is the POC boundary crossed?* — narrate from POC presence, locked-IDR count, whether a
       Foundation-grade test/CI backbone exists.
     - *Which of the three loops is currently emphasized?* — narrate as a weighted read across
       all census signals plus check-state's cadence input; loops differ in emphasis, never
       exclusivity (product-lifecycle-rules' `three-loops.md` concurrency doctrine) — never pick exactly one to the
       exclusion of the others without saying why.
     - *Bug vs. requirement gap* (the Verify-stage discipline) — only answerable with a concrete
       instance in view; when asked with no specific mismatch named, state the discipline
       (product-lifecycle-rules' `build-loop-stages.md`) rather than fabricating a verdict.
     - *Did a Retro's lessons land in the knowledge base?* — no typed record type exists yet to
       check this against (a named gap in `product-lifecycle-rules`); report "unanswerable — no
       typed signal exists for this yet," never a guess.
4. **Report** in the Output contract's order below. Findings are a reading, not a directive —
   acting on any of them (writing an IDR, locking an RDD) is a separate, user-initiated step.

## Output contract

1. **Verdict** — one line: the loop emphasis and build-turn stage, each tagged `(judgment)`.
2. **Version triple** — the derived candidate, tagged `(derived, mechanized)`.
3. **Ledger census** — per-type (ADR/IDR/RDD) counts, status distribution, orphan-ADR count,
   ROADMAP presence/status — all `(mechanized)`.
4. **Judgment calls** — the four questions from step 3 above, each narrated with its signals,
   never a bare boolean.
5. **Unmeasured** — any input this run could not read (missing census script output, no
   check-state JSON available), named plainly rather than silently omitted.

## Boundaries

- **NOT work-state.** Branches, worktrees, stashes, blocked-on-you, ready-to-close, ticket/PR
  drift — that's `harness:check-state`'s own axis; this skill never re-implements its
  `git_state.py`/`ticket_state.py` collectors, only consumes their JSON as an input (step 2).
- **NOT the doc-type contract.** Which type/sections/frontmatter to file in this repo is
  `doc-writing-rules`' live, `doc_lint`-enforced table — this skill only reads what already
  exists, never authors or recommends filing a specific record.
- **NOT what this repo has decided or queued.** `project-docs` answers from the live tree and
  GitHub Issues directly; this skill's census is narrower (typed ledger records + ROADMAP only).
- **NOT the general, portable doctrine.** What an IDR/ADR/RDD is *for*, the three-loop model in
  the abstract, admission tests — `product-lifecycle-rules` (this skill's own doctrine source);
  this skill answers "where is THIS project," never "what does the model mean in general."
- **NOT routing-biasing.** Report-only, per the PRD's resolution (d) — this skill never surfaces
  stage-appropriate skills or alters another skill's behavior; that's a named, gated future
  phase, not built here.
- **NOT an ambient/write surface.** This skill never writes a lifecycle line anywhere (a
  grounding doc, a manifest field) — that's the deferred ambient-convention half (PRD Open
  question 3), scoped later from this skill's own read-only usage.

## Failure branches

- Not a git repo, or neither `docs/ops/` nor `.claude/docs/` exists → report the census as all-zero counts
  (a real, non-degenerate reading: "no typed ledger records exist yet — pre-North-star or the
  doctrine isn't adopted here"), never a hard stop.
- Census script exits 1 → quote its FAIL line, mark the ledger-census section UNMEASURED, still
  render the judgment-tier section from directly-readable signals (ROADMAP.md, recent commits).
- No `rdd` records and the `rdd` doc-type isn't registered in this repo's `doc_lint.py` yet →
  the Releases-loop signal falls back to judgment (ROADMAP presence, ticket-status counts,
  release cadence) rather than blocking the whole report — the PRD's resolution (c), soft
  dependency on RDD landing.

Done when the report's five sections are all present (UNMEASURED counts as present) — or the
not-a-repo/no-doctrine reading is delivered as a real answer, never a placeholder.

## Example

Good (a judgment-tier line, narrated):
`Foundation loop emphasized (judgment): 3 accepted ADRs landed in the last two weeks vs. 0 new
IDRs and no RDD activity — architecture work is currently the active thread, not intent capture
or release commitments.`

Counter-example — do not imitate:
`Stage: Foundation.`
(a bare verdict with no signals cited — the reader can't tell fact from guess, violating OUT-02.)
