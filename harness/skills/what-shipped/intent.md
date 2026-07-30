# intent — what-shipped

Forged 2026-07-25 via `/harness:make-skill`. Seed: _"a user invocable skill for summarizing
Tickets, Issues, PR's created and merged by date today/last 24hrs by default."_

## Gate P0 — Route: **skill**

Ladder walked against the intent:

1. Mechanically checkable rule? No — grouping work into workstreams and judging what is
   worth surfacing is not a pass/fail a program returns.
2. Always-true fact needed every turn? No — needed on demand, at a reporting moment.
3. Needs tool walls, parallelism, or multi-skill preload? No — a script call, one MCP
   query, and a synthesis pass fit one context.
4. Procedure needed on demand → **skill**. PASS.

## Gate P1 — Intent record

| Slot               | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trigger**        | Verbatim from the authoring session: _"summarize PR's merged today"_, _"summarizing Tickets, Issues, PR's created and merged by date today/last 24hrs"_. Extended with lifecycle phrasings: "what shipped today", "standup summary", "what landed in the last 24 hours".                                                                                                                                                                                      |
| **Behavior delta** | Demonstrated in-session, un-skilled, immediately before forging: the ask _"summarize PR's merged today"_ produced an ad-hoc `gh pr list` + jq date filter that (a) covered **only PRs** — no Linear tickets, no GitHub issues; (b) required hand-separating 40 release-bot bumps from 18 real PRs by eyeballing titles; (c) invented the grouping on the fly. The skill fixes all three, and adds the ticket↔PR join that surfaces work with no PR behind it. |
| **Species**        | Procedural — a workflow with an output contract.                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Dials**          | `disable-model-invocation: false`, `user-invocable: true` — user's explicit call: fires on natural phrasing _and_ on `/what-shipped`.                                                                                                                                                                                                                                                                                                                         |
| **Freedom**        | Low for collection (bundled script, exact commands — the two gotchas below are unguessable), medium for synthesis (grouping into workstreams is judgment; the report skeleton constrains its shape).                                                                                                                                                                                                                                                          |
| **Type**           | Mixed. Capability uplift on the two verified gotchas; encoded preference on the report shape.                                                                                                                                                                                                                                                                                                                                                                 |
| **Fences**         | NOT finish-work (creating a PR) · NOT start-work (picking up a ticket) · NOT publishing a shareable page (render as an Artifact — explicit hand-off in the escape hatch; originally named a `session-review-artifact` skill that exists nowhere, corrected 2026-07-27 per re-audit) · NOT adiav2-ci-playbook (diagnosing a failing check).                                                                                                                    |
| **Done-when**      | The report names its resolved window, carries every non-empty section, and gives each workstream an owner plus a one-sentence purpose.                                                                                                                                                                                                                                                                                                                        |

**User confirmed** the four load-bearing choices via a single question round: whole-team
coverage with the user's own items called out · project-local scope · both invocation paths ·
name `what-shipped`. PASS.

## Gate P2 — Evals + assertions + baseline

- `evals/evals.json` — 16 trigger cases (incl. the explicit `/what-shipped` path), 8
  no-trigger near misses. Four negatives are owned by a named sibling (n01→finish-work,
  n02→start-work, n03→adiav2-ci-playbook, n06→requesting-code-review); n04 belongs to
  the Artifact flow (its original owner `session-review-artifact` exists nowhere — same
  correction as the fence); n05/n07/n08 are deliberately unowned over-reach probes —
  see the P5 audit-findings table, fix 3. Conforms to the house `{skill, note, cases[]}`
  schema.
- 5 behavioral assertions recorded in `evals/baseline/assertions.md`.
- Baseline: `evals/baseline/2026-07-25-unskilled.md` — the actual un-skilled output from this
  session, captured verbatim rather than re-simulated.

**Deviation from forge order:** the draft (P3) was written before the eval file (P2) was
committed to disk, because the baseline evidence already existed in-session from the
un-skilled run. Evals were authored against the _recorded_ baseline, not back-fitted to the
draft. Recorded rather than hidden. PASS.

## Gate P3 — Draft

`SKILL.md` (~110 lines, well under the 500 cap) + `scripts/collect-github.sh`. Both dials
explicit. Description 663 chars (re-measured 2026-07-27 after the review pass), under the
1,024 cap. No `references/` — the body carries no corpus, and every mechanic in it is
verified rather than cited.

## Gate P4 — Language pass

Applied inline against `prompt-wording-rules`' instantiation core:

- Locks written lowercase with named forbidden neighbors ("reads from `.author.type == "Bot"`,
  always — never `.author.is_bot`"), keeping the uppercase salience budget at zero hard gates.
- Numeric anchors on every load-bearing dimension: `limit: 25`, at most 5 workstreams, cap 5
  bullets, ~800 tokens per issue, 39-vs-18 as the worked bot-volume example.
- Contracts in the head (window → collect → report contract), escape hatch in the tail.
- Failure branches named with their consequence, not just their trigger ("a summary built
  from a partial fetch reads as a complete one").

## Gate P5 — Validate — PASS

1. **Lint** — `skill_lint.py` clean on SKILL.md; the post-write hook rejected the first
   `evals.json` (ad-hoc schema) and it was rewritten to the house `{skill, note, cases[]}`
   shape. Both clean at ship.
2. **Fresh-context audit** — `harness:skill-checker`, FLOOR depth. **Verdict PASS**, zero
   blocking, 1 major + 2 minor. Report: `evals/audit-report.md`. The critic independently
   re-ran the collector and independently reproduced the `is_bot` discrepancy, confirming both
   "verified mechanics" as genuine uplift rather than restated model knowledge.
3. **Behavior check** — collector run live against the real repo 6× across authoring and
   repair; reproduces the hand-verified 18-human / 39-bot split for 2026-07-25 every run.
   Failure path forced twice (nonexistent repo, invalid token): exits 3, withholds the `## OK`
   trailer, prints the failing command to stderr.
4. **Fence closure** — reciprocal no-trigger cases owed to the named siblings. Project siblings
   (`finish-work`, `start-work`, `adiav2-ci-playbook`, `requesting-code-review`) carry no
   `evals/` directory, so there is no suite to add the reciprocal case to. **Open asymmetry,
   recorded rather than silently skipped.** Revisit if those skills gain suites.

### Audit findings — all three fixed

| #   | Sev        | Finding                                                                                                                                                                                                                                                                               | Resolution                                                                                                                                                                                                                                            |
| --- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Major (R7) | `2>/dev/null \|\| true` made a _failed_ `gh` query print `## PR_MERGED (0)`, which the body then instructed the model to report as a real quiet day — the exact confusion the failure branch warns about. A rate-limited run would have produced a complete-looking all-zero summary. | Every `gh` call routed through `run_gh`, which fails loudly. Script exits 3 and emits `## ERROR` on any failure, plus a positive `## OK` trailer on success. Body now keys the failure branch on the **absence** of `## OK`. Forced-failure verified. |
| 1b  | —          | _Found while fixing 1, by testing rather than reasoning:_ `fail()` wrote to stdout, but nearly every call site sits inside `$(...)`, which swallowed the message and leaked only the exit code — the repair reintroduced a silent failure.                                            | `fail()` routes to stderr; success signalled positively by the stdout `## OK` trailer, which a truncated run cannot print.                                                                                                                            |
| 2   | Minor (R7) | Window contradiction: body declared UTC date granularity while the Linear query's `-P1D` is a rolling 24h clock, so the two sources covered different windows under one header.                                                                                                       | Body now requires post-filtering Linear results on `updatedAt >= SINCE`, naming the duration a coarse pre-filter and the date boundary the contract.                                                                                                  |
| 3   | Minor (R2) | `evals.json` note claimed every negative was sibling-owned; n05/n07/n08 map to no sibling.                                                                                                                                                                                            | Note amended to split owned (n01–n04, n06) from deliberately unowned over-reach probes (n05, n07, n08).                                                                                                                                               |

## Gate P6 — Ship — PASS

```
.claude/skills/what-shipped/
├── SKILL.md                              procedural · ~120 lines · desc 686 chars
├── intent.md                             this record
├── scripts/collect-github.sh             checked gh calls · OK/ERROR sentinels
└── evals/
    ├── evals.json                        15 trigger · 8 no-trigger
    ├── audit-report.md                   skill-checker, FLOOR, PASS
    └── baseline/
        ├── assertions.md                 5 assertions, each vs baseline
        └── 2026-07-25-unskilled.md       verbatim un-skilled run
```

Post-install: run `/doctor` to confirm the new description fits the shared listing budget.

## Verified mechanics behind this skill

Both discovered by running the real queries during authoring, 2026-07-25:

1. **`gh search prs` misreports bot authorship.** `.author.is_bot` returns `false` for GitHub
   App authors (`login: "adiahealth[bot]"`, `id: "BOT_…"`, `type: "Bot"`) — while `gh pr list`
   returns `true` for the same PR. Filtering on `is_bot` under search passed all 39 release
   bumps through as human work. The reliable discriminator is `.author.type == "Bot"`.
2. **Linear's `list_issues` is a token bomb.** It returns each issue's full description; 15
   issues cost ~12k tokens and an unwindowed `limit: 50` call overflowed the tool's own output
   cap entirely, returning a file path instead of results — hit twice in one session before
   the constraint was understood.

## Elevation — 2026-07-30, adiav2 → harness

Promoted from `adiahealth/adiav2/.claude/skills/what-shipped` (project-local) to a
general-purpose harness skill. Three seams generalized, nothing else changed:

1. **Ticket backend** — the hardcoded Linear query (`list_issues(team: "Adia2")`) became
   doc-writing-rules' backend-resolver seam (Option A local tickets / B GitHub Issues /
   C named adapter); adapter mechanics live in the adapter's reference, not this SKILL.
2. **Join key** — `(ADIA2-NNNN)` became the generic `[A-Z][A-Z0-9]*-\d+` | `#\d+` |
   `tkt-\d+` family.
3. **Collector** — `collect-github.sh` ported to `scripts/collect_github.py` per
   script-writing-rules (selftest proving the bot classifiers, the is_bot search/list
   asymmetry, and cap-guard saturation; exit contract 0/1/2 replacing the sh's exit 3).

The baseline transcript and audit report are provenance from the adiav2 forging and are
retained verbatim. The adiav2 repo-local copy is deleted in a paired adiav2 PR once the
installed harness serves this skill — two same-named skills must never coexist.
