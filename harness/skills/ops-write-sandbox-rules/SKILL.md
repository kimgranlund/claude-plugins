---
name: ops-write-sandbox-rules
description: >-
  The .claude/ops/ write-sandbox contract (issue #125): why decision-watcher, issue-sorter,
  repo-cleaner, and chore-planner carry no Write tool, what a fenced target-pathed payload block
  is, and how chore-lead applies their computed state instead. Use when asked why an ops-family
  seat can't write its own state file, how a new ops seat should hand its output back, what
  "narrated-but-absent" means, or why a scheduled ops firing commits only its state files. NOT
  for one seat's own per-firing procedure (watch-adrs, watch-tickets, clean-git); NOT for
  bare-name dispatch or named-teammate misaddress (agent-writing-rules).
disable-model-invocation: false
user-invocable: false
---

# ops-write-sandbox-rules

The `.claude/ops/` write-sandbox split (issue #125): a dispatch sandbox redirects a subagent's
direct `.claude/ops/...` write into the *coordinating session's own isolated worktree* instead of
the real shared checkout — the write lands, but on a branch nothing merges, so the state is
silently stranded. Every ops-family seat that computes durable `.claude/ops/` state works around
this the same way, and this is the one canonical statement of that mechanism — a seat's own body
cites this skill by name instead of re-deriving the rationale.

## The two roles

**Compute-only seat** (`decision-watcher`, `issue-sorter`, `repo-cleaner`, `chore-planner`) —
`tools` carries no `Write` at all. Every mutating operation targets a **scratch copy** of the real
state file (`cp .claude/ops/<file> /tmp/<seat>-<file>`, or the equivalent scratch-path argument a
bundled script accepts) — never the real path. The seat's final report carries the mutated scratch
content as a **fenced code block, headed by the file's real target path** (e.g. a ````
```.claude/ops/adr-queue.json ```` fence) — this fenced block IS the write, deferred to whichever
session dispatched the seat. A seat with nothing changed this firing needs no block for that file.
A seat that also keeps unrestricted `Bash` (every one of the four does, for `git`/`gh` or to run
its own bundled scripts) could technically reach the real `.claude/ops/...` path directly — the
scratch-only rule is contract, not a tool wall, and binds regardless of what `Bash` alone would
allow.

**Dispatching session** (`/sweep-chores`'s own procedure, when a seat runs inside its sweep — issue
#266 retired the `chore-lead` coordinator agent that used to hold this role, porting its
choreography into that skill directly, via `scripts/chore_sweep_apply.mjs`; a direct host
dispatch, otherwise) — reads every fenced, target-pathed block in a returned report and writes
each one to its named path verbatim, never edited or re-derived. `/sweep-chores`'s own
`allowed-tools` grants `Write` (plus the scoped `Bash` call to that script) for exactly this
purpose — applying an already-computed payload, never authoring content of its own.
A report that claims IN PROSE to have written, emitted, or produced a `.claude/ops/...`-shaped
path, with no matching fenced block backing the claim, is a **narrated-but-absent** write — a
contract violation, not "nothing changed" (issue #140: a live sweep found a seat narrating a write
with no fenced block behind it; nothing landed until the dispatching session caught it by hand).
Name every narrated-but-absent claim explicitly rather than silently absorbing it.

## Why state persists through the repo at all

A cloud-routine checkout (a scheduled `CronCreate` firing) is isolated per firing, and now also
isolated per dispatch — exactly what this payload contract works around. On a scheduled firing,
the dispatching session commits and pushes ONLY the seat's own state files (never source, never
any other path) once their payload blocks are applied — state must persist through the repo
itself, or the next firing starts blind.

## What stays local to each seat

The specific state file names, their schema, and the scratch-copy script invocations are
seat-specific and live in that seat's own preloaded procedure skill (`watch-adrs`,
`watch-tickets`, `clean-git`) — this skill states only the shared mechanism, never a particular
file's shape. A seat minting a real record via a platform API (e.g. `issue-sorter`'s `gh issue
create`) is not a local filesystem write and is outside this sandbox's scope entirely — the
sandbox problem is `.claude/ops/...` file writes, not API calls.

## The shared description template — owned here, not restated

Each per-firing-procedure sibling's own description carries these two shared fence clauses
(seat-specific clauses, like clean-git's own `/clean-repo` fence, may follow): a short
"NOT for the write-sandbox boundary (ops-write-sandbox-rules)" pointing here for WHY its seat
can't write its own state directly, and a second "NOT for running a sweep (dispatch <agent>)"
pointing at its own agent for actually firing it. The WHY lives entirely in this skill's own
description above ("Use when asked why an ops-family seat can't write its own state file...") —
a sibling never re-derives or restates that explanation inline; it names this skill and stops. This is the
one canonical statement of that template, the same way the mechanism itself is canonical above —
`watch-adrs`, `watch-tickets`, and `clean-git` reference it by name only.
