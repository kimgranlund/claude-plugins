# `reviewer` spawn mechanics — a genuine `claude -p` subprocess (issue #853)

F6 split from `fleet-bootstrap/SKILL.md` Phase 5 (issue #932) — cited there, not restated. The
old in-process shape (an `Agent`-tool dispatch that wrote its own wall mid-session) is what issue
#852 found never actually enforces — permission/hook config loads once per OS process and does
not hot-reload, and an `Agent`-tool dispatch inherits the parent's permission mode rather than
re-deriving one from its own cwd, so it was never a genuinely new process either. Issue #853's own
investigation (Findings, this issue) live-tested the fix: a `claude -p` child spawned with cwd
already inside an ALREADY-walled worktree IS correctly denied, from inside a dispatched seat's own
`Bash` tool, even under this machine's global `bypassPermissions` default. This dispatch realizes
that tested shape:

1. **Worktree precondition, run by the ORCHESTRATOR itself** (this session — never a dispatched
   seat). `team-scaffolding` Phase 1's own check against the reviewer's target worktree:
   `git rev-parse --git-common-dir` vs. `--git-dir` — differ only inside a linked worktree. Same
   (shared checkout) → stop here: no wall write and no spawn attempted, and the ORCHESTRATOR itself
   (never a dispatched seat) immediately appends `live_state.joined` (`role: "reviewer"`, `mode:
   "background-subprocess"`, `agent_name: null` — no process was ever spawned, today's date,
   `action: "joined"`, `wall_applied: "blocked-worktree"`, no `wall_verified_via`) — report per
   Phase 6 and name `EnterWorktree` as the fix, same as the manual path.
2. **Write and verify the wall — by the ORCHESTRATOR, entirely BEFORE any spawn.**
   `team-scaffolding` Phase 3's own C1–C1a write (merge `deny: ["Edit","Write"]` plus the
   `gh`/Read/Grep/Glob allow-list; merge the `PreToolUse` `Bash`-gating hook) then C3's own
   re-read-and-grep verify, run directly with this session's own `Read`/`Write`/`Edit`/`Bash` tools
   — this session is not walled, so it can do this cleanly, and the wall must already be ON DISK
   before the child process starts (issue #853's Q1: a wall written before process start enforces;
   a wall a session writes about itself never does, issue #852). Verification fails → stop, report
   the failure (Failure branches), no spawn attempted.
3. **Spawn exactly ONE `claude -p` child**, `--model <seats.reviewer.tier's model> --effort
   <its effort>` (canonically `--model sonnet --effort high`, read from `fleet.json` rather than
   hardcoded) **passed explicitly on the spawn command line** — a separate OS process has no
   dispatching-session frontmatter to inherit; absent these flags its model is just the CLI's own
   configured default, which may have nothing to do with this repo's tier ladder (issue #919, a
   live gap here). Background `Bash` (`run_in_background: true`), cwd =
   the pre-walled worktree, stdout+stderr redirected to a log file by THIS SESSION'S OWN shell
   redirect — that redirect is this session's operation, not a tool call the child itself makes, so
   the child's wall never touches it (the exact mechanism this issue's own live round-trip test
   verified: the spawning session's redirect landed cleanly while the child's own in-process
   `Write`/denied-`Bash` attempts were both denied). The child's prompt carries: the naming line
   (`Seat: {scope}-reviewer`), the reviewer's charter (`team-scaffolding` Phase 4 points 1, 4, 6 —
   tier, review-instrument roster, locked-spec self-check — quoted verbatim, no Skill-tool
   hand-off, same reasoning as `planner`'s dispatch above), and one MANDATORY first act before any
   review work: run `lld-0006` I2's own three-probe sequence (a denied `Write`, a denied-pattern
   `Bash`, one allowed `gh`-shaped `Bash`) and print each result to stdout in this EXACT
   three-line, colon-delimited format, one line per probe, no other text on those lines (the
   orchestrator's step 4 parses these literal keys):
   ```
   I2-PROBE write: DENIED|SUCCEEDED
   I2-PROBE bash-denied: DENIED|SUCCEEDED
   I2-PROBE bash-allowed: PASSED|FAILED
   ```
   followed by the quoted denial/pass text on subsequent lines, free-form. **This confirm step's
   own report channel is the child's stdout alone — captured by the orchestrator's own log
   redirect above, never a `gh issue comment` and never a Bash-redirect write to
   `fleet.json`/`fleet-roster.md`.** (Once this child moves on to actual REVIEW work, its output
   channel is the normal one: `gh issue`/`pr comment` on whatever target it's reviewing,
   `bind-review`'s own routing table — a concrete target per review task, unlike this one-shot
   confirm which has no natural GitHub target of its own.) A Bash-redirect write to `fleet.json`
   would additionally hit a confirmed platform gap regardless: this issue's own live build found
   the retirement-only C1a escape hatch's charset structurally excludes `{`/`}` (verified against
   the exact hook regex in `lld-0006-fleet-permission-profile.md` C1a), so a JSON-object append —
   exactly what a structured `fleet.json` entry needs — is denied even when it targets one of the
   three permitted paths; lld-0006's own C1a text already flagged this as a residual gap to widen
   deliberately if ever needed, never silently — filed as follow-up issue #855 rather than widened
   here. The child never attempts a `fleet.json`/roster write at all; step 4 below is the
   orchestrator's job instead.
4. **Monitor and collect, by the ORCHESTRATOR.** Poll the spawned process (bounded budget — ~180s
   default, overridable; this issue's own live round trip completed in 40–48s) until it exits or
   the budget is exhausted, then read the captured log for the I2 verdict in the fixed format the
   prompt required.
   - Process exited AND both denied-probe lines confirm DENIED, with the allowed-probe line
     confirming PASSED → `wall_applied: true`, `wall_verified_via: "subprocess-spawn"`
     (`references/fleet-manifest-schema.md`). Quote both denial texts (from the child's own report)
     in this dispatch's Findings.
   - Process exited but the log doesn't show the expected denial (a probe unexpectedly succeeded,
     or the fixed format is missing/malformed) → `wall_applied: "same-session-unenforced"` — same
     honest label issue #852 named, since the observable outcome (an unwalled write went through)
     is identical regardless of which process shape produced it.
   - Budget exhausted with no exit → `wall_applied: "spawn-unconfirmed"` (issue #853) — the process
     may still be running or may have died silently; name it plainly rather than guessing, and
     leave the background process running (never kill it blind) unless a repeat check later
     confirms it has since exited.
   - **Append `live_state.joined`** in `fleet.json` (`role: "reviewer"`, `mode:
     "background-subprocess"`, `agent_name`: a name identifying the spawned process — there is no
     fleet messaging identity for a subprocess, so its log-file path or PID-at-spawn-time is the
     durable pointer — today's date, `action: "joined"`, `wall_applied` and, when `true`,
     `wall_verified_via`, per the above). **This append is now done by the ORCHESTRATOR, never by
     the spawned child** — a genuinely walled subprocess structurally cannot write it (step 3's own
     finding), so the prior design's "the dispatched seat is its own fleet.json writer" assumption
     no longer holds for `reviewer`.
5. **Ongoing review work — the durable artifact is the wall on disk, not one long-lived process.**
   `claude -p` is one-shot per invocation (this issue's Findings) and cannot itself "hold a seat
   open" the way an interactive terminal does. The wall (step 2) persists in the worktree for the
   fleet's duration regardless of whether any one `claude -p` process is currently running — every
   FUTURE `claude -p` invocation spawned with cwd in that same worktree inherits the same
   structural enforcement for free, with no re-write needed, and does NOT need periodic
   re-verification against that same wall (Kim's ruling, issue #856, 2026-08-21 — a file-on-disk
   artifact does not degrade, so no re-probe after a `/team-scaffolding retire` cycle or on a fixed
   interval). So "holding the reviewer contract" now means: further review tasks are driven by
   fresh, per-task `claude -p` spawns into this same pre-walled worktree, via
   `teamwork/scripts/reviewer_scheduler.py` (issue #856) — one scheduling pass per invocation over
   an explicit `--tasks-file`, handling the spawn/crash-recovery/log-rotation/index mechanics; drive
   its recurring cadence with `/loop` (a live session) or `/schedule` (unattended), never a
   bespoke daemon this plugin reimplements. Full mechanics, the per-task prompt contract, and the
   local index shape: `references/reviewer-scheduler.md`. What #853 itself shipped was the one-shot
   bind-plus-I2-confirm round trip (steps 1–4) that the scheduler's own `verify_wall_present`
   precondition now composes on top of — it refuses to spawn anything against a worktree whose wall
   was never confirmed written.
