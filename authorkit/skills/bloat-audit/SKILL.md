---
name: bloat-audit
kind: skill
description: >
  Run the busy-work / over-specification audit over a skill, agent, command,
  or any corpus of instruction-carrying markdown — ceremony disproportionate
  to task size, and prose that spends words without buying instruction-
  following value. Use when asked to audit or review a skill/agent/plugin
  for verbosity, bloat, heavy-handedness, "does this need to be this long",
  or busy-work root causes. Read-only: reports, never rewrites. NOT for a skill's content
  correctness, routing fidelity, or standards compliance (harness's check-skill).
author: kim
created: 2026-08-13
last_updated: 2026-08-17
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/measure.py *)
---

# bloat-audit

Deterministic measurement lives in `scripts/measure.py` — run it; never
re-derive line counts or cross-file duplication in prose. This skill's job
is the judgment layer on top of its output: deciding what's load-bearing
and what's hand-holding a capable model doesn't need.

## Procedure

1. Resolve the target: `$ARGUMENTS` (default: the current project) — a
   skill/agent/command directory, a whole plugin root, or any directory of
   markdown files (frontmatter optional — files with no `kind` are measured
   as plain instruction documents).
2. Run: `python3 <this skill>/scripts/measure.py --target <path> --json`
3. Judge each flagged file against references/CALIBRATION.md's test: does
   cutting this content lose a real instruction (a dated gotcha, a safety
   prohibition, a non-obvious convention), or only its retelling? Only the
   second is a finding.
4. Classify each finding: ceremony (a judgment call expanded into phases
   a capable model wouldn't need), restatement (the same content stated
   more than once, in this file or across siblings — the script's
   duplicate-pair output), or template-tax (a boilerplate section —
   Failure branches, Done/NOT-done — present out of habit rather than need).
5. Render the report per references/REPORT-TEMPLATE.md. Lead with the two
   numbers: files flagged and estimated chars/tokens recoverable. Cite the
   evidence (file:line, the actual duplicate text or phase list) per
   finding; never assert bloat the script's output doesn't support.
6. This skill never rewrites. Hand the fix to whoever owns the target file
   — bloat-audit only finds, it doesn't fix.

## References

| File | Read when |
|---|---|
| REPORT-TEMPLATE.md | rendering the busy-work report |
| CALIBRATION.md | judging whether a finding is real bloat or load-bearing content — calibrated against this plugin's first cross-estate audit |
