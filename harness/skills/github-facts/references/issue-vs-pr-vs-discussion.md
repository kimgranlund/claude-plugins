# Issue vs. Pull Request vs. Discussion — what each primitive fundamentally is

## The core distinction

[verified, docs.github.com, 2026-07-17] An **Issue** is GitHub's general-purpose work-tracking
primitive: "quick to create, flexible, and can be used in many ways... track bug reports, new
features and ideas, and anything else you need to write down or discuss." It carries no built-in
assumption of code attached.

[verified, docs.github.com, 2026-07-17] A **Pull Request** is "a proposal to merge code changes
into a project... you can propose, discuss, and iterate on changes before you merge." It always
carries a code diff.

[verified, docs.github.com, 2026-07-17] A **Discussion** is "an open-ended format" for community
conversation — brainstorming, Q&A, and announcements — explicitly separate from work tracking.

## The data-model relationship: a PR IS an Issue, not a sibling of one

[verified, docs.github.com REST reference, 2026-07-17] "GitHub's REST API considers every pull
request an issue, but not every issue is a pull request." A PR is distinguished in the API only by
the presence of a `pull_request` property on the issue object — everything an Issue can carry
(labels, milestones, assignees, comments, sub-issues) a PR also carries, plus PR-only fields layered
on top (branch/commit metadata, review state, merge status, diff metrics).

A Discussion is a genuinely separate object (its own GraphQL type carrying category assignment and
answer-tracking fields) — it does not sit in the Issue/PR hierarchy at all.

## GitHub's own recommended workflow: Discussion → Issue → PR

[verified, docs.github.com best-practices guide, 2026-07-17] GitHub states the intended funnel
explicitly: "start with discussions for big-picture thinking, then graduate to issues when you are
ready to scope out the work... keeps bug fixes, feature requests, and general conversations
separate." Concretely:

- **Discussion** — the idea isn't scoped yet; open-ended, before committing to actionable work.
- **Issue** — the work is now specific and actionable, with clear ownership: a bug report, a
  planned feature, a task.
- **Pull Request** — code exists (or is proposed) to resolve an Issue; review happens here, not on
  the Issue itself.

[verified, docs.github.com, 2026-07-17] An Issue can be converted directly to a Discussion (a
`converted_to_discussion` event) when it turns out to be a conversation, not scoped work — the
funnel runs in reverse too, not just forward.

## Workspace mapping

Where this funnel meets this workspace's own `issue` skill routing gate → `bug-task-feature-
mapping-nuances.md`, opening section.

## Stability note

[drift-prone, 2026-07-17] The Issue/PR core model predates 2020 and hasn't changed structurally
since; UI and metadata layers keep evolving on top of it (Issue Fields reached GA 2026-07-02,
fifteen days before this research — see `issue-types-and-labels.md`). Discussions are newer (beta
2020-12, GA 2021-08-17) and still receive active feature work (a `gh discussion` CLI command group
landed in 2026). Re-verify any claim here that touches a 2025-2026-dated feature before citing it
as still current.
