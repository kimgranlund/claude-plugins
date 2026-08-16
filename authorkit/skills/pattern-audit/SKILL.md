---
name: pattern-audit
kind: skill
description: >
  Sweep a repo/corpus for a caller-supplied pattern or natural-language
  instruction and emit a structured match dataset (id/file/line/col/match/context/kind;
  kinds instruction-labeled) for a downstream step: review, bulk edit,
  migration, or an audit's own Phase 0. Use when asked to sweep,
  scan, or collect matches for a pattern/regex/instruction. NOT for naming
  conformance (naming-audit), NOT for busy-work/verbosity (bloat-audit),
  NOT for RETIRED-name sweeps (fix-old-names owns rename-provenance finds
  end to end), NOT for partition/artifact-graph analysis
  (plan-plugin-split), NOT for a check that should become a permanent
  script (make-script). Read-only: emits a dataset, never rewrites.
author: kim
created: 2026-08-15
last_updated: 2026-08-15
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/scan.py *)
---

# pattern-audit

Deterministic sweep lives in `scripts/scan.py` — run it; never re-derive
matches in prose or hand-grep what the script measures. This skill's job is
compiling a caller's instruction into the script's literal probes, then
optionally judging the resulting matches. It never mutates target files.

## Procedure

1. Resolve the instruction. Given as a param → use it. Omitted → ask: what
   to find, where (subtree/glob), and what counts as a false positive.
2. Compile the instruction into one or more labeled probes (`LABEL=REGEX` +
   optional globs). A literal regex passes through as a single probe. A
   natural-language instruction may fan out to several labeled probes;
   state the compilation in one line before running so the user can veto a
   bad translation.
3. Run `python3 <this skill>/scripts/scan.py --target <path> --pattern
   <LABEL=REGEX> ... [--glob GLOB ...] --json`. Never re-derive matches in
   prose; never grep by hand what the script measures. The dataset of
   record is this call's `--json` output — per-match `id/file/line/col/
   match/context/kind` + `totals` (schema of record: the script's own
   docstring and Data section in lld-0004-pattern-audit.md).
4. Judgment overlay (only when the instruction was natural-language, or the
   user asks): annotate each match record with `verdict: hit |
   false-positive` and a one-line `reason`, citing the `context` field —
   never delete records, never renumber ids.
5. Hand the dataset (raw or judged) to whatever the caller names next —
   review, bulk edit, migration, an overhaul-planning Phase 0 row. This
   skill never mutates target files.
6. Recurrence ratchet: the same instruction asked twice → recommend
   `harness:make-script` — pattern-audit owns the ad-hoc sweep, never a
   shadow home for a standing check.

## Failure branches

- The instruction cannot compile to any literal probe (e.g. "find comments
  that mislead," a semantic judgment with no lexical anchor) → say so
  plainly; either widen to a coarse probe plus a mandatory judgment
  overlay (step 4), or hand back to the caller for a narrower ask. Never
  force a probe that doesn't actually express the instruction.
- `scan.py` exits 2 (target missing, invalid regex, or no files survived
  filtering) → report the usage error verbatim; never read a usage error
  as a false CLEAN.

Done when the dataset (raw or judged) is delivered with its verdict line
quoted, and the target tree is unchanged.
