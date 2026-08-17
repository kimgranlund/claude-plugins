---
name: sweep-chores
description: >-
  Run one ops-family sweep on demand against this repo — fans out decision-watcher +
  issue-sorter + repo-cleaner in parallel and returns chore-planner's single prioritized queue
  (.claude/ops/plan.md). Reachable as /sweep-chores and via the Skill tool by name. Use for
  "run the ops sweep", "sweep the ops queue", "fan out the standing seats", or a scoped ask
  like "repo hygiene sweep only". NOT for one seat's own single-item job — triage one item
  (issue-sorter), clean one thing (repo-cleaner), check one ADR (decision-watcher): dispatch it
  directly; NOT for driving the queue's buildable tickets to an actual build (teamwork's
  mobilize-chores, which wraps this skill) — this skill only ever reports.
disable-model-invocation: false
user-invocable: true
argument-hint: "[blank for a full sweep | a scope instruction, e.g. 'repo hygiene only']"
allowed-tools: ["Read", "Glob", "Write", "Agent", "Workflow", "Bash(node harness/scripts/chore_sweep_apply.mjs *)", "Bash(node harness/scripts/sweep_guard.mjs *)"]
---

# sweep-chores

Runs the ops-* family sweep directly. Issue #266 retired `chore-lead` — the standing coordinator
agent whose entire job was a deterministic dispatch graph (fan out three seats, collect handoffs,
hand to chore-planner): nothing non-mechanical survived scrutiny (see the Retirement note below),
so the choreography moved here instead of staying a model-in-the-loop hop. This skill is now
reachable two ways for the same reason `dispatch-ticket` is: `/sweep-chores` for a human typing
the command, and `Skill(skill: "harness:sweep-chores", args: "<scope>")` for a programmatic
caller in another plugin (`teamwork:mobilize-chores`) that needs the identical procedure without
duplicating it — a `disable-model-invocation: true` command skill blocks BOTH paths at once
(issue #134's class), so this skill takes the same "both" species `check-state`/`what-shipped`
already use rather than staying command-only.

## Retirement note — chore-lead

`chore-lead`'s five-step procedure (scope → fan out → apply payloads → hand to chore-planner →
apply its payload → relay) was checked against genuine judgment content, step by step: scope
resolution is a fixed three-item menu lookup; fan-out is direct dispatch with no discretion;
payload application is fenced-block extraction plus a verb+path heuristic — now `scripts/
chore_sweep_apply.mjs`, selftested; the planner hand-off is another fixed dispatch. Nothing
survived that a script or this skill's own prose can't do exactly as well, deterministically,
every time — the entire point issue #266 exists to prove. Verdict: **retired outright**, not
shrunk. `harness/agents/chore-lead.md` is deleted; every reference to it across this estate that
named it as a live routing target has been repointed to this skill in the same change.

## Procedure

1. **Concurrency guard, before anything else.** Two firings racing this repo's own
   `.claude/ops/` state have caused a full pre-emption of one firing's seats (the
   2026-08-17T18:45Z-vs-18:55Z duplicate firing — decision-watcher fully pre-empted — and a
   `sync_main` quarantine near-miss the same day). Run:
   ```
   node harness/scripts/sweep_guard.mjs check --root .
   ```
   Exit 1 (a fresh marker, printed as JSON) → **decline this firing outright, do not fan out.**
   Report the in-flight marker's own `startedAt`/`session` verbatim and stop — never queue,
   retry, or silently wait; the other firing's own step 6 relays the real queue when it finishes.
   Exit 0 (clear — no marker, or a stale one just overridden; the script names which) → continue.
   A stale marker (default: older than 30 minutes) means a prior sweep crashed or was abandoned —
   it is removed by `check` itself so this firing's own `start` never collides with it; name the
   override in this firing's eventual report, never swallow it silently.

   Once clear, claim it immediately:
   ```
   node harness/scripts/sweep_guard.mjs start --root . --session <this session's own id>
   ```
   And release it unconditionally at the very end of this procedure (step 8, success or failure
   alike — a sweep that errors out and never releases its own marker becomes the next firing's
   false positive):
   ```
   node harness/scripts/sweep_guard.mjs end --root .
   ```
2. **Banner check.** Whenever `.claude/ops/plan.md` does not exist — no ops
   queue has ever been produced here — show the banner (text below) now, before the sweep: the
   sweep itself is what creates that file, so a post-dispatch check destroys its own condition.
   Once a plan file exists, never show it again.
4. **Resolve scope.** A blank instruction (`$ARGUMENTS`, or an empty/absent `args` on a Skill-tool
   call) → all three seats (`decision-watcher`, `issue-sorter`, `repo-cleaner`). An instruction
   naming a known subset → exactly the seats it names. An instruction naming no known seat →
   report the valid menu (decision-watcher · issue-sorter · repo-cleaner); do not sweep.
5. **One seat's own job with no sweep intent** (e.g. "file this bug" — intake, or "delete that
   stale branch" — hygiene) → name the direct door (`/sort-issues`, `repo-cleaner`,
   `decision-watcher`) and stop; a sweep that exists to wrap one seat's single task is fan-out
   overhead with no roll-up value.
6. **Run the sweep — Workflow path preferred.** If the **Workflow tool** is available in this
   session (this invocation is your authorization):
   ```
   Workflow({
     scriptPath: "harness/workflows/chore-sweep.js",
     args: { scope: [<the resolved scope from step 4>] }
   })
   ```
   returns `{ scope, seatReports: {seat: reportText}, unmeasured: [...], plannerReport }`. Skip to
   step 7 with that result. (Workspace-relative path, not `${CLAUDE_PLUGIN_ROOT}`, deliberately —
   this skill is invoked cross-plugin by `mobilize-chores`, and `${CLAUDE_PLUGIN_ROOT}`'s
   resolution across that boundary is unverified; this repo's own convention is already
   workspace-root-relative for every documented script invocation, so this trades
   install-elsewhere portability for behavior verified safe in THIS repo.) The Workflow path is
   live-proven: the 2026-08-17T18:35Z all-three-seats firing ran it end-to-end clean — 4 agents
   returned, zero UNMEASURED, every payload block applied via step 7's script, plan verified on
   disk.

   **Fallback — no Workflow tool.** Fan out the resolved seats in parallel — one `Agent` call
   each, `subagent_type` the literal `harness:`-prefixed name (`harness:decision-watcher` /
   `harness:issue-sorter` / `harness:repo-cleaner`), never the bare seat name, and WITHOUT a
   `name` (`agent-writing-rules`' Failure catalog: a bare `subagent_type` resolves ambiguously,
   and a named dispatch switches into teammate/mailbox mode and strands the report — gh#154 /
   gh#157). Each dispatch's own prompt states three things explicitly, never left implicit: the
   resolved scope this sweep is running under, any seat step 4 excluded from it by name (so a
   seat's own report carries the context of what else did-or-didn't run alongside it), and this
   firing's own UTC timestamp — the sequence key this sweep and everything downstream of it
   (chore-planner's plan header, the eventual report filename) key on, never an incrementing sweep
   count (a count is only ever a program's OWN local tally, drifts the moment two sessions sweep
   concurrently, and this estate has already seen that drift surface as an informal "sweep #N"
   label in unrelated changelog prose — never repeat that pattern here). A seat's dispatch failing
   to return → UNMEASURED for this sweep, others proceed. At least one seat returned → hand the
   bundle to `chore-planner` — one more `Agent` call, `subagent_type: "harness:chore-planner"`,
   also unnamed, the returned reports as context, naming every UNMEASURED seat. No seat returned
   at all → skip the planner dispatch; report the failed sweep, per-seat status and all.

   **Script-not-found escape hatch.** This skill's paths (`harness/workflows/chore-sweep.js`,
   `harness/scripts/chore_sweep_apply.mjs`) are workspace-relative, deliberately scoped to THIS
   repo (see step 6's own path note above) — not proven portable to a differently-laid-out
   install. The Workflow tool being available doesn't guarantee `scriptPath` resolves; if it
   errors not-found, take the fallback branch immediately, same as "no Workflow tool" — never
   retry the same path. If step 7's `chore_sweep_apply.mjs` call itself can't be resolved, apply
   each seat's fenced, target-pathed blocks by hand per the contract stated there (`Write` each
   verbatim to its named path) and name the degradation in the sweep report — never skip payload
   application because the script that mechanizes it went missing.
7. **Apply every returned payload.** For each seat's raw report text (Workflow or fallback path
   alike), write it to a scratch file and run:
   ```
   node harness/scripts/chore_sweep_apply.mjs SCRATCH_FILE --root .
   ```
   This is `chore-lead`'s own former step 3, mechanized: it extracts every fenced, target-pathed
   payload block and writes it to its named `.claude/ops/...` path verbatim — never edited or
   re-derived — and flags any first-person write claim (wrote/emitted/produced/saved paired with
   a `.claude/ops/...`-shaped path) with no matching fenced block as **narrated-but-absent** (exit
   1; still applies whatever blocks DID arrive). A block whose target path falls outside
   `.claude/ops/` is refused, never written (exit 1) — never guessed at. Then apply the planner's
   own report the same way — it also returns its rewritten `.claude/ops/plan.md` as a fenced,
   target-pathed block.
8. **Verify, then relay.** `Read` confirms `.claude/ops/plan.md` exists before the queue is
   relayed as real. Report: this firing's own UTC timestamp (the sequence key, per step 6 —
   never a sweep count), the banner (if shown), which path ran (Workflow or fallback), the scope
   swept and any seats it excluded by name, per-seat status (returned · UNMEASURED · refused —
   read off each `chore_sweep_apply.mjs` run's own findings), any narrated-but-absent claims named
   explicitly, and the planner's queue unmodified. Then run
   `node harness/scripts/sweep_guard.mjs end --root .` to release step 1's marker — this is the
   very last action of the procedure, run on every exit path (a normal finish, a zero-return
   sweep, or an earlier failure branch below), never skipped.

## The banner

```
sweep-chores — one-pass sweep of this repo's ops-* seats (intake · ADR review · repo hygiene).

What it does: fans out the three standing seats in parallel, then chore-planner turns their reports
into one prioritized action queue (.claude/ops/plan.md).
What it never does: edit source, or mutate anything outside a dispatched seat's own gates —
coordination and payload application are this skill's entire write surface.
```

## Failure branches

- The Workflow dispatch, or a fallback Agent dispatch, fails to return at all (a tool error, not
  an agent-reported failure) → report the failure plainly; never fabricate a sweep report to fill
  the gap — then still run step 8's `sweep_guard.mjs end` before stopping.
- `sweep_guard.mjs check` reports a fresh in-flight marker → decline the firing per step 1 and
  stop immediately; do not run `start`, and do not run `end` (this firing never claimed the
  marker, so it must never release the OTHER firing's own marker).
- `chore_sweep_apply.mjs` exits 2 (usage error — a missing scratch file, a bad flag) → name it in
  the sweep report as a write that could not be applied; continue with whatever DID parse.
- A human asks to see the banner again after a plan file exists → answer inline from the banner
  text above; a disclosure re-read never costs a three-seat sweep.

Done when a declined firing (step 1's in-flight case) named the in-flight marker and stopped
without touching it, OR this firing's own marker was released (step 8's `end` call, success or
failure alike, for every firing that got past step 1), the banner was shown before the sweep whenever step 2's condition held, the resolved
scope actually ran (Workflow path or the named fallback), every returned payload block has been
applied via `chore_sweep_apply.mjs` (or its absence/refusal explicitly named), the planner's queue
(verified on disk by Read, or its named absence) is relayed unmodified, and the conversational
return leads with the verdict line plus per-seat status. NOT done while a seat failure is silently
dropped, a seat's job was done inline, a zero-return sweep still dispatched the planner, this
skill authored its own queue, a returned payload block goes unapplied and unreported, or a
narrated-but-absent write claim goes unflagged.
