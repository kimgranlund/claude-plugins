# Issue Types vs. labels vs. Issue Fields — three distinct classification layers

## Issue Types is a real, GA platform feature — not a proposal

[verified, github.blog changelog, 2026-07-17] GitHub's native **Issue Types** shipped public beta
2024-10-01, public preview 2025-01-12, and reached **general availability 2025-04-09**. It is
current, stable, and available by default — not a beta feature to hedge against.

[verified, docs.github.com, 2026-07-17] Every organization gets three default types out of the
box: **Task, Bug, Feature** — the exact three shapes this workspace's own `bug-report`/`feature`/
`issue` skill family already routes work into by name. Organizations can rename/recolor these and
add up to 25 total types.

## The mechanical difference from labels

| | Issue Types | Labels |
|---|---|---|
| Scope | **Organization-level**, shared across every repo | Repository-level, independently defined per repo |
| Cardinality | One type per issue | Multiple labels per issue |
| Structure | A managed, validated taxonomy (admin-controlled) | Free-form tags, no validation, no cross-repo consistency |
| Query syntax | `type:"Bug"` (boolean-combinable, nests up to 5 levels) | `label:bug` |
| Projects integration | A first-class Type field, enable via "Hidden fields" | Also filterable/groupable in Projects |
| REST API | Full CRUD since 2025-03-18 (`type` on create/PATCH) | Long-standing full CRUD |

[verified, docs.github.com, 2026-07-17] Both mechanisms are queryable and both integrate with
GitHub Projects — GitHub's own docs do not publish a single decision rule for "type here, label
there" beyond stating they're complementary. [inferred] The practical split that follows from the
mechanics above: **Issue Type for the one-per-issue, org-wide-consistent shape question** (is this
a Bug, a Feature, or a Task — exactly the three this workspace already asks); **labels for
everything that can be multi-valued or repo-specific** (priority tags, area tags, `wontfix`,
`good-first-issue`).

## A third, newer layer: Issue Fields — do not confuse with Issue Types

[verified, github.blog changelog, 2026-07-17] **Issue Fields** is a separate, newer feature:
public preview 2026-03-12, GA **2026-07-02** — fifteen days before this research. It adds
typed, org-wide structured metadata (four defaults: Priority, Effort, Start date, Target date)
that GitHub explicitly positions as *replacing label-based workarounds* for structured data ("no
types, no validation, no consistency across repositories" is GitHub's own stated critique of using
labels for this). Fields can be pinned per Issue Type, so selecting a type auto-surfaces its
relevant fields in the sidebar. Over 40,000 organizations adopted it during preview.

[drift-prone, 2026-07-17] Issue Fields is fifteen days old at GA as of this research's access
date — the most likely fact in this whole pack to have shifted by the time it's read. Re-verify
before treating any specific field-count or adoption-number claim as current.

## Workspace mapping

This workspace's `kind: bug`/`kind: feature` label convention against Issue Types →
`bug-task-feature-mapping-nuances.md` Finding 1.
