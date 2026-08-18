---
name: orchestration-audit
kind: skill
description: >
  Sweep an estate for orchestration-archetype drift against fleet-rules' eight
  per-archetype rubrics (A1..A8) — the mechanizable slice only: A3's durable-channel
  evidence reader, A7's workflows/*.js syntax lint tier, review-coverage existence,
  grant-literal and resume-path presence; every judgment criterion reports "queued, not
  built". Use when the user asks to audit orchestration archetypes, check workflows/*.js
  lint coverage, verify named-seat conduct evidence, or reproduce a review's verdicts
  mechanically. Read-only. NOT one arrangement's wiring (wiring-checker); NOT the batch
  form (estate-audit-agent); NOT authoring the rubrics (fleet-rules owns that canon).
author: kim
created: 2026-08-18
last_updated: 2026-08-18
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/audit.py *)
---

# orchestration-audit

Deterministic sweep lives in `scripts/audit.py` — run it; never re-derive a syntax check or
a durable-channel read in prose. This skill's job is locating the rubric files, running the
sweep, and rendering the judgment layer on top — same split as `doctrine-audit`'s own
`sweep.py` (mechanics) / skill (judgment) division, with a THREE-way tag in each rubric
table (2026-08-18 code-checker review: a binary mechanizable/judgment split overclaimed what
`audit.py` actually runs) — **mechanizable — built** (this script computes it TODAY: exactly
six criteria, X-R3/A3-R2/A4-R1/A5-R3/A6-R2/A7-R4), **mechanizable — not built** (a real
future check, reported "queued, not built" identically to judgment until it exists), and
**judgment** (no lexical anchor a script can grade, ever). Never read a plausible-sounding
check description in a rubric row as proof the script actually runs it — the tag is the only
thing that says so, and only "built" means built.

## Procedure

1. Locate the rubric files: `teamwork/skills/fleet-rules/references/orchestration-rubric-
   a{1-8}-*.md`, relative to the estate/plugin-workspace root (feature-detect — teamwork
   may not be installed; degrade gracefully by reporting NOT INSTALLED and running the
   mechanical sweep anyway, since `audit.py` needs the rubrics only for citation, not to
   run). Read the target archetype's rubric file in full before interpreting its findings —
   its own header states the architecture and intended use this instance is scored against,
   never a generic bar.
2. Run the sweep: `python3 <this skill>/scripts/audit.py --root <estate-root> --archetype
   {a1..a8|all} --json`. The dataset of record is this call's JSON output — per-archetype
   findings, each carrying `criterion`/`status`/`detail`.
3. Interpret:
   - **Mechanizable findings** (`pass`/`warn`/`fail`): cite the exact criterion id and
     detail from the JSON. A `fail` on A7-R4 (workflow syntax) names the file and the exact
     `node --check` error; a `warn` on A3-R2 (durable-channel reconciliation) names the
     specific roster/live_state mismatch, never a bare "drift detected".
   - **X-R3 (review coverage)**: an archetype with no owning checker named
     (`OWNING_CHECKERS` maps it to `[]` — currently A3 and A8) reports `warn`, "no owning
     checker named yet" — this is a real gap in the estate, not a script defect; never
     silently pass it.
   - **Judgment and mechanizable-not-built criteria**: every criterion tagged either way in
     the rubric table (the majority — six criteria total carry "mechanizable — built" across
     all eight files, everything else is one of these two) is reported "queued, not built"
     to its rubric-named owning checker (`wiring-checker`, `code-checker`, a human read of
     the durable-channel evidence A3-R2 surfaced) — this instrument is read-only like its
     five siblings; dispatching the named checker is always the caller's own decision.
4. Render a report: verdict line per archetype first (`CLEAN`/`ATTENTION`/`FAIL`, the same
   `pattern-audit`-style summary string `audit.py` itself prints), then findings, then the
   judgment queue for that archetype (pulled from the rubric file's table, never invented).
5. Hand fixes to whatever the caller names next — this skill never mutates target files,
   including the rubric files themselves.

## Reproducing a review's verdicts (Acceptance criterion, #666)

A mechanical re-run reproduces the MECHANIZABLE half of a prior narrative review's verdicts
exactly — the G1/G2 priority axes plus the X-R3/A6-R2/A4-R1/A5-R3 checks, all real, all
selftest-proven, all exercised against this estate's own `.claude/ops/fleet.json`,
`fleet-roster.md`, and `harness/workflows/chore-sweep.js`. It does NOT claim to reproduce a
judgment-tier verdict color from pure mechanics alone — a `🟡` on A3, for instance, may
combine a mechanizable A3-R2 finding with a judgment call on A3-R1/A3-R3/A3-R4 no script can
make. Report the mechanizable layer's own verdict plainly, and name every judgment criterion
still queued — never claim a full color-for-color reproduction the mechanics don't earn,
same discipline `doctrine-audit` already holds for its own judgment edge type.

## Failure branches

- `audit.py` exits 2 (root missing, `--archetype` unrecognized) → report the usage error
  verbatim; never read a usage error as a false CLEAN.
- No `workflows/*.js` files found under root (A7) → reported `n/a`, never a silent pass and
  never a fabricated finding.
- `node` unavailable on PATH for the A7-R4 syntax check → `audit.py` exits 2 with a named
  usage error (`node not found on PATH -> A7-R4's syntax check cannot run`), never an
  unbounded traceback and never a silent false pass.
- teamwork not installed (no rubric files to cite) → run the mechanical sweep anyway and
  say so plainly in the report header; the rubric TEXT is a citation aid, not a runtime
  dependency of `audit.py` itself.
- An X-R3 owning-checker path that doesn't exist → `fail`, named with the missing path;
  never silently treated as "no checker needed".

Done when the report (per-archetype verdict + findings + judgment queue) is delivered with
its verdict lines quoted, and the target tree is unchanged.
