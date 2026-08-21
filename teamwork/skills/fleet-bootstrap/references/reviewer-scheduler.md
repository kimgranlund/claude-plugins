# The recurring reviewer scheduler (`teamwork/scripts/reviewer_scheduler.py`, issue #856)

#853's one-shot bind-plus-I2-confirm round trip (`fleet-bootstrap` Phase 5's `reviewer` branch)
confirms a worktree's `deny-edit-write` wall enforces, once, via exactly one `claude -p` child.
That wall is a durable file-on-disk artifact (`.claude/settings.local.json`) — it does not degrade
over time, so no periodic re-probe of an already-confirmed wall is ever needed, not after a
`/team-scaffolding retire` cycle, not on a fixed interval (Kim's ruling, 2026-08-21 — do not
re-open this question). What #853 deliberately left unbuilt is the layer that
turns that one-shot confirm into an ONGOING cadence of per-review-task spawns against the same
walled worktree — this script is that layer.

## What it owns, and what it doesn't

`reviewer_scheduler.py` owns exactly the four things issue #856 scoped: the per-task `claude -p`
spawn mechanics, crash recovery, log rotation/retention, and a durable local index of which spawn
covered which task with what outcome. It does **not** own:

- **Writing or verifying the wall.** That stays `team-scaffolding` Phase 3 / `fleet-bootstrap`
  Phase 5 steps 1–2's job, run once against a worktree before this script's first invocation
  there. `verify_wall_present` refuses to spawn anything against an unwalled worktree (exit 2) —
  a defensive floor against ever repeating #852's false-positive class at this layer, not a
  substitute for the real write-and-verify step.
- **Deciding which review tasks are pending.** A recurring cadence needs a task SOURCE (which PRs
  or targets currently need review) as much as it needs a spawn mechanism; this script takes that
  list as an explicit, already-decided input (`--tasks-file`, a JSON array of task strings — e.g.
  `"PR #870"`, `"skill:teamwork/skills/foo"`) rather than inventing its own discovery policy. A
  human, `fleet-marshal`'s routing (`fleet-rules` Section 7), or `mobilize-chores` names the list;
  this script only handles what happens once it's named.
- **Recurring on its own.** One invocation is one scheduling pass over the given task list, not a
  daemon. Drive the cadence with the harness's own interval primitives instead of reimplementing
  one here:
  - Live session: `/loop <interval> "run python3 ${CLAUDE_PLUGIN_ROOT}/scripts/reviewer_scheduler.py run --worktree <wt> --tasks-file <path>"`.
  - Unattended/cloud: `/schedule` a routine that runs the same command on a cron cadence.

## Per-task contract

Each attempt spawns one `claude -p` child, cwd pinned to `--worktree`, stdout+stderr captured to
its own timestamped log file by this script's own file write (never a tool call the child makes —
the same non-tool-call redirect mechanism #853's own live round trip verified is invisible to the
child's wall). The child's sealed prompt (`build_child_prompt`) quotes `bind-review`'s own routing
table inline (never a Skill-tool hand-off — `bind-review` is `disable-model-invocation: true`,
same reasoning `fleet-bootstrap` Phase 5 step 3 already uses for the one-shot reviewer charter):
classify the target, dispatch the owning checker, post the verdict via `gh issue comment` / `gh pr
comment` on the target (#855's ruling: never a `fleet.json` write from inside the wall), then print
`POSTED: <comment-url>` on its own stdout line — the scheduler's own log parser
(`extract_posted_url`) reads this literal key to populate the index row.

## Crash recovery

A task gets `1 + --max-retries` attempts (default: 1 retry, 2 attempts total). An attempt that
exits non-zero, or that the `--timeout` (default 600s) kills, is retried into a fresh log file. If
every attempt fails, the task's final outcome (`"crashed"` or `"timeout"`) is written to the index
and printed to stderr — the failure is surfaced, never silently absorbed into a quiet skip.

## Log rotation

Every attempt's log lands under `--log-dir` (default `<worktree>-reviewer-logs`, a sibling
directory outside the worktree itself). After each pass, `rotate_logs` deletes every `*.log` file
past the newest `--keep-logs` (default 20) by mtime — the retention policy #853's ad-hoc one log
file per spawn never had.

## The local index

`--index` (default `<log-dir>/index.jsonl`), one JSON row appended per completed task:

```json
{"task": "PR #870", "slug": "pr-870", "attempts": 1, "outcome": "succeeded",
 "log_path": "/path/to/20260821T190000Z-pr-870-attempt1.log",
 "comment_url": "https://github.com/.../issues/870#issuecomment-...",
 "started_at": "2026-08-21T19:00:00Z", "finished_at": "2026-08-21T19:04:12Z"}
```

`outcome` is one of `"succeeded"`, `"crashed"`, `"timeout"`. This index is the durable "which spawn
covered which review task, with what outcome" record issue #856 scoped — it is a pointer/outcome
ledger, not a second copy of the review's own content (that content lives in the `comment_url`
already posted to GitHub).

## Exit codes

`0` — every task in the pass succeeded. `1` — at least one task never succeeded after retries (the
pass still ran to completion; check the index/stderr for which). `2` — a usage error, or the
target worktree carries no wall markers on disk (`verify_wall_present` finds no `deny-edit-write`
+ `PreToolUse` `Bash` shape in `.claude/settings.local.json` — content-checked only, not I2-probe
confirmed; refuses to spawn anything at all rather than guess).
