# With-skill behavior check — 2026-08-20, run live on the incident host (KG-MacBook-Air-M4)

Executed the skill's own procedure (probe → judge vs remedies.md → report). Assertions:
1 ✓ real measured numbers (probe JSON archived in the forge session) — AND the check caught a
probe defect (the 'Chrome Helper' pattern miscounted the user's real browser as 31 test shards;
fixed to headless/test engines, re-verified 0). 2 ✓ six-column rows below. 3 ✓ zero mutations.
4 n/a (darwin host). 5 ✓ mostly-clear host got a short report, not a padded checklist.

## The report the skill produced (post-remediation host — the incident's fixes verified held):

host-audit · KG-MacBook-Air-M4 · 2026-08-20 · load 2.63/14.32/50.08 on 10 cores (0.26×)
Probe: (JSON, archived)
| # | Finding (measured) | Why it hurts | Fix | Severity | Warning tier |
|---|---|---|---|---|---|
| 1 | swap 14.1 GB used of 15.4 GB, free RAM 994 MB of 32 GB | paging residue from the load-108 day multiplies every stall until processes release | quit + relaunch the heaviest long-lived apps (or reboot); keep ≤3 gate-running lanes | med | safe |
Verdict: 1 action recommended. F1 Spotlight CLEAR (indexers 0% CPU, all worktree homes carry
.metadata_never_index), F2 Time Machine CLEAR (~/Projects [Excluded]), F3 load CLEAR (0.26×;
m15=50 is the incident's decaying tail), F4 orphans CLEAR (0 test browsers), F8 disk CLEAR (96%
free), F9 fd CLEAR (1,048,576).
Deferred to you: the one command above — this audit changed nothing.
