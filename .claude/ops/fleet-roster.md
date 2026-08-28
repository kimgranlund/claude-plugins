# Fleet roster

Session-identity records for the standing fleet (see `teamwork:team-scaffolding` Phase 2;
naming is convention, not platform-enforced — lld-0006 D1).

| Role | Session name | Date | Repo |
|---|---|---|---|
| reviewer | plugins-reviewer | 2026-08-16 | plugins |
| agent | plugins-marshal | 2026-08-16 | plugins |
| reviewer | plugins-review (takeover) | 2026-08-16 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-16 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-18 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-21 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-21 | plugins |

Repaired 2026-08-17 (issue #586, ADR-0020 convergence): the two `agent` rows above originally
read `plugins-agent` — stale even under the prior `{repo}-team-lead` convention (#434), since the
printed session name for role `agent` was never the bare role token. Corrected in place to
`plugins-marshal`, the current convention's printed name for this role.
| agent | plugins-marshal (takeover) | 2026-08-22 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-23 | plugins |
| agent | plugins-marshal (takeover) | 2026-08-26 | plugins |
| reviewer | plugins-reviewer (released, legacy null-address row) | 2026-08-27 | plugins |
| planner | plugins-planner (released, legacy null-address row) | 2026-08-27 | plugins |
| agent | plugins-marshal (released, session close) | 2026-08-28 | plugins |
| agent | plugins-marshal | 2026-08-28 | plugins |
| planner | plugins-planner | 2026-08-28 | plugins |
| reviewer | plugins-reviewer (background-subprocess, walled worktree) | 2026-08-28 | plugins |
