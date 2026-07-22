---
name: check-doc
description: >-
  Review an existing functional document (ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK): a
  mechanical doc_lint pass, then judgment — unfalsifiable requirements, missing non-goals,
  restated substrate, broken ID spine, class violations, verdict-first. Use it to review,
  audit, critique, or score a document, or when a doc "feels off". NOT for drafting one
  (make-doc); NOT the rules themselves (doc-writing-rules).
disable-model-invocation: false
user-invocable: true
argument-hint: "[path-to-document]"
---

# check-doc

Mechanical first, judgment second, verdict first in the report. Target: `$ARGUMENTS`. Invoke
`doc-writing-rules`; its practices are the criteria.

1. **Mechanical:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doc_lint.py" <file>` — its findings
   head the report verbatim; never re-derive by eye what the script already checked.
2. **Judgment criteria (cite line numbers, never impressions):**
   - J1 Falsifiability — every requirement/outcome/done-when phrased so it could fail.
   - J2 Non-goals — present, concrete, actually fencing the known scope-creep directions.
   - J3 ID spine — IDs minted and referenced across the doc's links; restatement flagged as a
     drift pair with its source.
   - J4 Head-first — the opening carries the verdict/decision/summary; a buried lede is a finding.
   - J5 Class discipline — content matching the declared mutability class (no todo lists in an
     ADR, no requirements in a PLAN).
   - J6 Consumer fit — could a fresh context execute or consume this without the author present?
3. **Report:** verdict (ship / fix-then-ship / rethink) first, then findings as
   `severity · location · criterion · repair`, then at most three prioritized repairs. A review
   with findings but no repairs is half done.
