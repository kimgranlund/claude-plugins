# Perf playbook: <campaign name>

Baseline reports: `<dir>/<slug>.<preset>.json` (perf-audit, <date>). Brief: `perf-brief.md`.
One entry per fix, appended by perf-fix-loop as each iteration lands. Phase 2 workers read this
as a checklist: apply page-local entries where the page has the same pattern, never redo a
shared entry, add a new entry for anything new.

## Entry template

### <audit-id>: <one-line issue as the report names it>

- issue: `<audit-id>`, item `<url | selector | file:line:col>` (report: `<report file>`)
- cause in this codebase: `<source file or config>` (why it produced the finding)
- files touched: `<path>`, `<path>`
- how to verify: `node <path-to>/lh-diff.mjs <before.json> <after.json>` (exit 0), or `<curl / other command>`
- shared: yes | no (yes = every route inherits it; no = this page only)
- iteration: <n>, result: green | reverted (what regressed)

## Entries

(appended below, newest last)
