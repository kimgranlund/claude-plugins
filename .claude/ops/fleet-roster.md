# Fleet roster

Session-identity records for the standing fleet (see `teamwork:team-scaffolding` Phase 2;
naming is convention, not platform-enforced — lld-0006 D1).

**Migration note (#434, 2026-08-16):** the `agent` role's printed session name changed from
`{repo}-agent` to `{repo}-team-lead`; the `agent` role KEY in `fleet.json` is unchanged. Existing
`plugins-agent` rows below are historical and left as-is (append-only log, never rewritten in
place) — new `agent`-role joins append as `plugins-team-lead`.

| Role | Session name | Date | Repo |
|---|---|---|---|
| reviewer | plugins-reviewer | 2026-08-16 | plugins |
| agent | plugins-agent | 2026-08-16 | plugins |
| reviewer | plugins-review (takeover) | 2026-08-16 | plugins |
| planner | plugins-planner (ex plugins-reviewer, seat switch) | 2026-08-16 | plugins |
| agent | plugins-agent (takeover) | 2026-08-16 | plugins |
| product | plugins-product | 2026-08-16 | plugins |
