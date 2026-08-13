---
name: naming-audit
kind: skill
description: >
  Run the naming-convention conformance audit over a harness estate (a
  .claude/ folder or a plugin root). Use when asked to audit, validate, or
  check naming, review an estate or plugin for conformance, report the
  exemption burn-down, or verify after a rename. Read-only: reports, never
  renames.
author: kim
created: 2026-08-13
last_updated: 2026-08-13
requires: [naming-conventions]
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/validate.py *)
---

# naming-audit

Deterministic checks live in `scripts/validate.py` — run it; never re-derive
its checks in prose. This skill's job is the judgment layer on top of its
output.

## Procedure

1. Locate the target's `naming.manifest.json` (estate root or `.claude/`).
   If absent, stop and offer to seed one via manifest-authoring — do not
   audit an ungoverned estate against invented rules.
2. Run: `python3 <this skill>/scripts/validate.py --target <estate> --json`
3. Interpret findings against naming-conventions (load the reference file
   whose read-when matches the finding class — GRAMMAR.md for name
   violations, FRONTMATTER.md for schema/policy, LAYOUT.md for folder/index).
4. Classify each finding: violation (new name, must fix), exempt (burn-down
   candidate), frontmatter-disagreement (rename-drift signal — highest
   priority), orphaned relation (dangling endpoint).
5. Render the report per references/REPORT-TEMPLATE.md. Lead with the two
   numbers: error count and exemption burn-down. Cite evidence per finding;
   never assert a violation the JSON output does not contain.
6. If the user wants fixes: hand renames to rename-planning, manifest edits
   to manifest-authoring. This skill never mutates.

## References

| File | Read when |
|---|---|
| REPORT-TEMPLATE.md | rendering the conformance report |
| CALIBRATION.md | judging severity or wording of findings — calibrated against this plugin's own first audit |
