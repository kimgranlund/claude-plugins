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
   - J7 Agent-testability — on a SPEC/PRD/LLD: is `## Agent verification` present and real, not a
     placeholder? Every Acceptance criterion (SPEC) or Outcome (PRD) whose assert layer isn't
     obvious needs a stated layer and harness/instrument an agent can run unattended (an
     obvious-layer criterion may omit its line — the template's own allowance, not a J7 gap); a
     criterion that's genuinely human-only is named as an explicit exception rather than silently
     unaddressed. On an LLD, the section names an existing instrument that already verifies the
     design or cites the owning SPEC's own section — never restates it. A section that only
     restates the requirement ("verify it works") fails this the same way a missing one does.
     Assert-layer judgment: docs' `agent-harness-rules`.
3. **Report:** verdict (ship / fix-then-ship / rethink) first, then findings as
   `severity · location · criterion · repair`, then at most three prioritized repairs. A review
   with findings but no repairs is half done.
