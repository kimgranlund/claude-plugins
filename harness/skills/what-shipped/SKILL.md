---
name: what-shipped
description: >-
  Summarizes what shipped in a date window — PRs merged and opened, GitHub issues, and
  ticket-backend records (local ticket files, GitHub Issues, or a connected adapter such
  as Linear) — defaulting to today, with release-bot noise counted but excluded and real
  work grouped by workstream. Use when the user asks "what shipped today", "summarize PRs
  merged today", "what did we ship this week", "what landed in the last 24 hours", "what
  changed yesterday", "give me a standup summary", or names a date or range to report on.
  NOT for the repo's current work-state — branches, blocked-on-you, drift (check-state, a
  point-in-time snapshot; this skill reports a window of activity); NOT for publishing
  the summary as a shareable page (the Artifact tool); NOT for creating PRs or picking
  up tickets (the host repo's own workflow skills).
disable-model-invocation: false
user-invocable: true
argument-hint: "[today | yesterday | this week | 36h | YYYY-MM-DD[..YYYY-MM-DD]]"
---

# what-shipped

Produces one activity report for a date window: which PRs merged, which opened, which
tickets moved, which issues opened or closed — release-bot noise counted but excluded,
real work grouped by workstream.

## Window

Resolve the argument to a `SINCE UNTIL` pair of `YYYY-MM-DD` dates before collecting
anything. Bare invocation and any phrasing naming today or the last 24 hours both
resolve to today's date. `yesterday` resolves to today minus one; `this week` to the
last 7 days ending today; an hour count over 24 (`36h`, `48h`) reaches back as many
calendar days as it spans; an explicit date or `A..B` range passes through.

Windows are UTC at date granularity, so a late-evening merge in a timezone behind UTC
(UTC−) lands on the next UTC day, and an early-morning merge in a timezone ahead of UTC
(UTC+) can fall on the previous one. State the resolved window in the report header — the
reader reconciles their own memory against it.

## Collect

**Step 0 — backends and identity.** Two seams, resolved once per run:

- **Ticket backend:** where doc-writing-rules is installed, call its backend resolver
  (`references/backend-resolver.md`) once — Option A (local `docs/tickets/` files),
  Option B (git-native GitHub Issues), or Option C (a named external adapter, e.g.
  Linear). No resolver, or the ruled adapter unreachable → GitHub-only report, with the
  ticket side declared unmeasured. Adapter-specific query mechanics (paging, windowing,
  output caps) live in that adapter's own reference, not here.
- **Identity:** `gh api user --jq .login` for the GitHub login, plus the resolved
  backend's own notion of "me" (Linear: `get_user("me")`). An item whose author or
  assignee matches either identity is the user's — append `(you)` after the owner name
  wherever it appears in the report.

**Step 1 — GitHub, via the bundled collector.** One call returns every section:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/what-shipped/scripts/collect_github.py <SINCE> <UNTIL>
```

It emits `PR_MERGED`, `PR_OPENED`, `PR_OPEN_NOW`, `ISSUE_OPENED`, `ISSUE_CLOSED`, and a
`BOT_NOISE` tally, each headed by its own count. The repo comes from the working
directory's `gh repo view` (override with `WHAT_SHIPPED_REPO=owner/name`). Hand-rolling
`gh pr list` with a jq date filter instead over-fetches, silently truncates at the
limit, and misses the bot-filter correction below — run the script.

**Check the trailer before reading any count.** A complete run ends with `## OK — all
queries succeeded` on stdout and exits 0; a failed run exits 1, omits that line, and
prints `## ERROR` plus the failing command on stderr. Treat a missing `## OK` as
collection failure, always — never as a quiet day. Zero counts under a present `## OK`
are real.

Two mechanics the script already encodes, load-bearing if it is ever edited:

- Bot authorship reads from `.author.type == "Bot"`, always — never `.author.is_bot`,
  which `gh search prs` reports as `false` for GitHub App authors even where `gh pr list`
  reports `true` for that same PR (verified 2026-07-25). Filtering on `is_bot` under
  search silently passes every release bump through as human work.
- Bot volume is reported, never hidden. A day that is 39 release bumps and 18 real PRs
  is a different day from one with 18 PRs and no release activity.

**Step 2 — tickets, per the resolved backend, windowed and capped.**

- **Option A (local files):** scan `docs/tickets/*.md` frontmatter; a ticket whose
  `date` or a dated `## Findings` heading falls inside the window counts as updated.
- **Option B (GitHub Issues):** already covered by Step 1's issue sections — skip.
- **Option C (adapter):** query by an updated-at window sized to reach `SINCE` from
  **now** (a rolling pre-filter), with the adapter's own paging and output caps; then
  enforce the date boundary as the contract — drop every record whose update falls
  outside `SINCE..UNTIL`, both bounds. Widen by paging, never by raising limits past
  the adapter's documented caps.

What an updated-at window measures is **updates**, not state transitions: it moves on
comments and metadata edits too. Report these as "tickets updated" — never "moved" or
"changed state" — except where a record's own started/completed/canceled timestamp
falls inside the window, which does prove a transition and may be reported as one.

**Step 3 — join tickets to PRs.** PR titles carry ticket ids in a recognizable form —
match `[A-Z][A-Z0-9]*-\d+` (adapter keys), `#\d+` (issues), or `tkt-\d+` (local files)
in parentheses or brackets. The residue after the join is the finding worth surfacing:
**tickets updated with no PR behind them** — a campaign closed as investigated, a
status correction, a record cancelled. Those never appear in a PR-only summary, and
they are the reason this skill reads the ticket backend at all.

## Report contract

Lead with the verdict line, then the sections below in order. Skip any section that is
empty rather than printing an empty heading — except `PR_MERGED`, whose zero is itself
the answer.

```
<N> real PRs merged, <M> release-bot bumps, <K> tickets updated — <window>.

## <Workstream name> — <owner>
<count> PRs, ~<lines> changed. <One sentence on what it accomplishes.>
1. **<Theme>** (#<pr>) — <what it does>
...

## Tickets updated without a PR
- **<id>** <title> — <what changed and why it matters>

## Still open
<count> PRs in flight; <the oldest or most notable, capped at 5>
```

Group into at most 5 workstreams, ordered by volume. A workstream is a coherent unit of
work — one epic, one campaign, one person's thread — not a directory. Name each one's
owner, with `(you)` where Step 0's identity matches. Where a single ticket spans many
PRs, report the ticket as the workstream and the PRs as its steps; a flat list of 18 PR
titles is data, not a summary.

Ground `~<lines>` in `gh pr view <n> --json additions,deletions`, summed over the PRs the
workstream actually cites — the collector returns only number, author, and title, so an
unfetched line count is a guess. Where a workstream collapses a tail, sum the cited PRs
only and say so ("~1.2k lines across the 5 listed").

Cap each workstream at 5 bullets. Beyond that, collapse the tail into a "plus" line
naming the count and the shape of what was collapsed.

## Failure branches

- Collector exits non-zero, or its `## OK` trailer is missing → report the blocker verbatim
  from stderr and stop. A summary built from a partial fetch reads as a complete one, and a
  rate-limited query that returned nothing is indistinguishable from a quiet day once its
  zero is copied into a report.
- Ticket backend unresolved or unreachable → produce the GitHub sections, and say plainly
  that the ticket side is unmeasured. Never infer ticket state from PR titles alone.
- Window resolves to zero PRs and zero tickets → say so, and name the window checked. A
  quiet day and a broken query look identical in an empty report.

Done when the report names the resolved window, every non-empty section is present, and
each workstream carries an owner and a one-sentence purpose.

## Escape hatch

Asked only about one source ("just the PRs", "what tickets closed"), run only that step
and label the report accordingly. Asked to publish or share the summary, render the
finished report as an Artifact rather than re-deriving it.
