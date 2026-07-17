# GitHub Projects v2 — a separate object, not a view

## Structural nature: Projects v2 is its own object, layered ON TOP of Issues/PRs, not a 4th backend

[verified, docs.github.com + GitHub gist, 2026-07-17] Projects v2 introduces a first-class
`ProjectV2` GraphQL object. Its items are `ProjectV2Item` wrappers around one of: an Issue, a Pull
Request, a Draft Issue, or Redacted content. **A Project does not store work-item data itself** —
it references Issues/PRs (or plain draft-issue text) and layers custom fields on top. This answers
this pack's own scoping question directly: **Projects v2 is not a 4th backend candidate alongside
local/git-native/external** — there is no work item that can exist ONLY in a Project; it always
wraps an Issue, a PR, or an ungrounded draft-issue stub. Treat it as a *view + metadata layer*
over the Issue/PR primitives this pack already covers, not a peer storage surface.

## GraphQL-only — no REST equivalent, and Projects (classic)'s REST API is gone

[verified, github.blog changelog, 2026-07-17] Projects v2 is reachable **only via GraphQL**
(`api.github.com/graphql`, scopes `read:project` / `project`). The older Projects (classic) REST
API was **sunset 2025-04-01** — there is no REST fallback for Projects v2 at all, unlike Issues/PRs
which have both. Any adapter or automation touching Projects must speak GraphQL; this is a hard
constraint, not a preference.

[verified] Adding and updating an item cannot happen in one call: `addProjectV2ItemById` then a
separate `updateProjectV2ItemFieldValue` — a two-round-trip minimum for "file this and set its
status," relevant to anything scripting Project field updates.

## Custom fields

[verified, docs.github.com, 2026-07-17] Five field types: **text, number, date, single-select,
iteration**. Plus built-ins: Issue priority/effort, parent/sub-issue progress rollup, PR metadata,
Issue Type. Limits: **50 custom fields per project**; item count is a **soft 50k limit**
[drift-prone — sourced to a 2024 private-beta announcement; verify current limit before relying on
it]. Iteration fields support relative filters (`@current`/`@previous`/`@next`) and configurable
length/breaks.

## Multi-repo and multi-org spanning

[verified, github.blog changelog, 2026-07-17] An organization-level Project spans **every repo in
that org** natively. Cross-**org** item-adding is supported via the GraphQL mutation itself.
Automatic add-by-filter **workflows** are per-repository (must be configured on each repo
individually) and [drift-prone, sourced 2024] multi-repo auto-add automation was Enterprise-only as
of that source — re-verify tier gating before depending on it.

## Webhooks

[verified, github.blog changelog, 2026-07-17] `projects_v2_status_update` (status-update
notifications, with before/after field values) and `project_v2_item` (item changes, enhanced to
include custom-field deltas directly — no follow-up GraphQL query needed to see what changed).

## Workspace mapping

Whether Projects v2 competes with or layers over ADR-0003's backend choice → `bug-task-feature-
mapping-nuances.md`, Projects v2 note (structural-nature finding, this file's own opening section).
