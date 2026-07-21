# B2 baseline — naming the issue-triage pair

- **Subagent:** `issue-triage`
- **Slash command:** `/issue-triage`

Reasoning: One capability with two entry points (scheduled run vs. on-demand dispatch) should carry
one name — a shared kebab noun-phrase makes the command↔agent pairing self-evident and grep-able.
`issue-triage` names the job, not the actor or the schedule (no `-agent`/`-bot`/`-cron` suffixes),
so the name stays true if the trigger mechanism changes.
