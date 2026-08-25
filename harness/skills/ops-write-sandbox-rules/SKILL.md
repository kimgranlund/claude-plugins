---
name: ops-write-sandbox-rules
description: >-
  The .claude/ops/ write-sandbox contract (issue #125): why decision-watcher, issue-sorter,
  repo-cleaner, and chore-planner carry no Write tool, what a fenced target-pathed payload block
  is, how chore-lead applies their computed state instead, and the push-verification convention
  (issue #936) for a skill that commits directly to main. Use when asked why an ops-family seat
  can't write its own state file, what "narrated-but-absent" means, or how a direct-to-main
  commit should confirm the push landed. NOT for one seat's own per-firing procedure (watch-adrs,
  watch-tickets, clean-git); NOT bare-name dispatch (agent-writing-rules); NOT the PR-branch push
  path (`campaign_close.py`).
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

**The payload-fence rule binds regardless of hedge language.** Narrating a path conditionally —
"report written to X, if applicable/if written" — without ever emitting X's fenced block is the
same narrated-but-absent violation in softer words, not an exemption from it: a seat with nothing
to report for a path omits that path entirely rather than naming it conditionally. The rule also
binds a LATER payload that cites an EARLIER one: a state file (e.g. `held-items.md`) may reference
another path (e.g. a per-firing report) as existing only once that path's own fenced block has
actually been emitted in this firing or a prior one — never on the strength of having been merely
mentioned. A live sweep on a repo consuming this plugin found exactly this gap (issue-sorter hedged a report path
as "if written," never emitted it, and `held-items.md` went on to cite it as if it did) — the fix
is this rule, stated once here for every ops-family seat rather than patched per-instance.

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

## Push-verification for a direct-to-main commit (issue #936)

A third case sits outside both roles above: a **live invoking session** (never a dispatched
compute-only seat — those never touch a real path at all, per the scratch/fenced-payload contract
above) that writes AND commits a small, source-free `.claude/ops/...` state file directly to
`main` in a shared primary checkout, rather than through a PR. `teamwork:chores-run` step 2 is the
one skill body in this estate that does this today — cited here rather than re-derived.

The failure mode this closes: a `git push` can fail, or never run at all, while the local commit
still landed — the seat's own completion report then claims "committed to main" as if that meant
landed, when it only landed locally. A subsequent `git pull --ff-only` reporting "Already up to
date" does not disprove this — that message is about origin having nothing NEW to offer, not about
local being in sync WITH origin. Nothing forces a re-check on this path the way
`campaign_close.py` already re-queries `git ls-remote --heads origin <branch>` after a PR merges
and verifies the branch is gone (`harness/scripts/campaign_close.py`, cited as the existing
pattern this convention ports to the direct-to-main path — read, never re-derived).

**The convention:** after `git push`, before reporting the commit as landed, re-read origin's
truth and compare it against the local commit that was just pushed:

```
git push origin main
git ls-remote origin refs/heads/main   # or: git fetch origin main && git rev-parse origin/main
```

(fully qualify as `refs/heads/main`, not a bare `main` — an unqualified ref name matches any
branch whose path ends in `main`, e.g. `release/main`, and can return more than one line.)

Compare the SHA `ls-remote`/`fetch` returns against `git rev-parse HEAD` (the commit just made).
Match → report the commit as landed, citing the confirmed SHA. Mismatch, or the push exits
non-zero → the commit is NOT landed; report it as a pushed-but-unconfirmed (or failed) state
exactly the way `dispatch-ticket`'s own stage 2a names a hold rather than guessing — never narrate
"committed to main" past this point. This is a cheap, mechanical re-read (one `ls-remote` call),
not a new gate or script — every skill that commits directly to `main` cites this section by name
instead of re-deriving the check inline.

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
