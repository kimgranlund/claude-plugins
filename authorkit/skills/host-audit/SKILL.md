---
name: host-audit
kind: skill
description: >
  Run the local dev-HOST performance audit — measure what degrades the machine while agent
  fleets, parallel test suites, and worktree churn run, and emit a warned, discretionary fix
  checklist. Use for "why is my machine slow", "load average is huge", "laptop on fire while
  agents run", "audit my host/machine performance", "everything times out under parallel
  agents", "is Spotlight or Time Machine eating my CPU". Read-only: the user runs every fix.
  NOT whether a red TEST RUN is trustworthy (the host repo's flaky-gates, where present); NOT
  token spend (spend-audit); NOT repo layout (repo-audit).
author: kim
created: 2026-08-20
last_updated: 2026-08-20
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(ps *)
  - Bash(uptime*)
  - Bash(tmutil isexcluded*)
  - Bash(git worktree list*)
---

# host-audit

host-audit turns "my machine is slow" into a measured report: one read-only probe run, each
finding matched against `references/remedies.md`'s thresholds, and a checklist the USER acts
on — the audit itself mutates nothing. Forged from a live incident (2026-08-19/20: load 108–180
on a 10-core host, ten test suites red identically on clean main; root causes were Spotlight
indexing worktree npm-install churn, Time Machine inclusion, 7 lanes × workers-per-core test
runners, orphaned browser shards, and 14 parked worktrees — every remedy below was verified by
applying it).

## Procedure

1. **Probe.** `node "<this skill dir>/scripts/host_probe.mjs"` — one JSON object: load per core,
   memory, indexer/backup CPU, Time Machine exclusion state, worktree-home census (Spotlight
   markers, parked counts, node_modules posture, per-home package-manager mix + aggregate
   node_modules disk MB), dev-process counts with oldest etimes, disk,
   fd limit. The probe is read-only and exit-coded (0 ran / 1 probe-failure / 2 usage); findings
   live in the JSON, never the exit code. Script won't run (no node, denied) → fall back to the
   probe commands quoted per-finding in `references/remedies.md`, and say the fallback happened.
2. **Judge.** Grep `references/remedies.md` for each finding class F1–F10 whose threshold the
   JSON crosses; consult only the matched entries. `platform != darwin` → report the portable
   classes (the catalog's Non-macOS section is the single home of that list) and name the macOS-probe gap verbatim from the catalog's Non-macOS
   section — every claim carries its verified/unverified label from the catalog.
3. **Corroborate before accusing.** A finding that implicates ANOTHER live actor (a peer
   session's processes, a runner mid-flight) is reported as "held by <owner>, verify before
   acting" — the orphan-kill remedy lists specific pids for the user's review — pid lists only (F4's
   warning is a hard rule, not advice).
4. **Report.** Emit the contract below. A host whose numbers cross NO threshold gets the
   all-clear form: the probe block + "no action recommended" — padding a healthy host's report
   with optional tuning is a failure, not thoroughness.

## Report contract

```
host-audit · <hostname> · <date> · load <m1>/<m5>/<m15> on <cores> cores (<perCore1m>×)
Probe: <the JSON block, or "prose fallback — script unavailable">
| # | Finding (measured number) | Why it hurts | Fix (the exact command) | Severity | Warning tier |
Verdict: <N actions recommended | all clear — no action>
Deferred to you: every command above — this audit changed nothing.
```

Every row carries all six columns; the warning tier is one of **safe** / **needs-sudo** /
**changes-system-behavior**, and the last two always state the side effect in the row (what
stops being backed up, what stops being searchable, what a broad kill would take down).

**Good row:** `| 1 | mds_stores+corespotlightd at 214% CPU; 2 worktree homes lack the marker |
Spotlight re-indexes every npm install's ~40k files | touch <home>/.metadata_never_index (both
paths printed) | high | changes-system-behavior — Finder search stops inside excluded dirs |`
**Bad row (do not imitate):** `| 1 | Spotlight seems busy | indexing | consider excluding some
folders | ? | — |` — no measured number, no runnable command, no named side effect.

NEVER execute a remedy command — sudo-tier or not — the report hands every action to the user.

## Failure branches

- Probe exits 1 → report the probe's own stderr as the first finding and continue with the
  prose fallback; a broken probe never silently becomes "all clear".
- Load is high but every threshold points at ANOTHER user's live work → report "measured,
  attributable to <owner>, no unilateral action" and stop.
- The user asks the audit to also FIX things → decline within this skill (the read-only fence is
  its identity); hand the specific commands over and, where the host repo has gated executors
  (a reap script, repo-cleaner), name them instead.

Done when the report is printed with every crossed threshold as a six-column row (or the
all-clear form), and the session performed zero mutations beyond the report itself.
