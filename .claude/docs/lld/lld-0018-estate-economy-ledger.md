---
doc-type: lld
id: lld-0018-estate-economy-ledger  # gh#624's claim comment named lld-0015; lld-0015 landed
  # first via PR #638 (#626), then a fresh planner pass took 0016, but by PR-open time origin/main
  # also carried lld-0016-doctrine-revalidation-mode.md (PR #640) and lld-0017-feedback-intake-door.md
  # (PR #641) — same collision class lld-0013/lld-0015's own frontmatter notes document, caught by
  # code-checker's independent review before merge, renumbered to the next free slot at PR-open
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#624
idr: idr-0010 (LOCKED — .claude/docs/idr/idr-0010-estate-economy.md; cited, never edited)
spec: none — gh#624's own Acceptance section plus Kim's 2026-08-18 follow-up-seed comment carry
  the checkable criteria, and idr-0010 (LOCKED) already carries the ruled claim and every named
  lean; a standalone SPEC would restate both (same routing test lld-0011/lld-0015 applied).
---
# LLD — Estate economy: the spend ledger instrument (`spend-audit`) — gh#624, realizing idr-0010

**Verdict, head-first.** One new authorkit skill, `spend-audit`, owning a per-firing token-spend
ledger at `.claude/ops/spend-ledger.csv` (attention-trend.csv-shaped: dated CSV, append-only,
the literal `absent` for anything unmeasured) and two bundled scripts — `validate.py` (the
schema owner: standalone re-validation of an existing ledger, selftest-bearing) and `trend.py`
(append exactly one row from CLI-supplied fields, validated on write, imports `validate.py`'s
schema so there is one canon). The row schema is Kim's six base columns plus two this design
adds and justifies: `tokens_source` (`measured` | `estimated` | `absent` — a provenance flag,
never a derived number; the honesty column idr-0010's own falsification clause demands) and
`ref` (the firing's durable artifact — issue/PR number or report path — the dedupe key the
backfill path needs). The write path is hook-free by construction (#466): a **close-out
convention** — the seat that OWNS a firing's close-out on a real checkout appends the row as its
last step; a sealed dispatched seat reports its fields and its DISPATCHER appends (the only
place the measured token figure is visible, and the only place the `.claude/ops/` write lands
per `harness:ops-write-sandbox-rules`) — with a **backfill procedure** (the skill's own, armed
via session-scoped `CronCreate` on decision-watcher's pattern) as the fallback for firings whose
owner never appended. **Sequencing decision (stated, not a corner cut):** Wave 1 ships
authorkit-only now; the teamwork `fleet-rules`/`loop-rules` pricing bullets are Wave 2,
DEFERRED — see "Scope and sequencing" immediately below.

## Scope and sequencing — Wave 1 (authorkit, now) / Wave 2 (teamwork, deferred)

gh#624's acceptance has four criteria. This LLD maps them:

| # | Acceptance criterion (gh#624) | Wave | Status after Wave 1 |
|---|---|---|---|
| 1 | Economy concept RULED (IDR/ADR draft awaiting ratification) | already done | idr-0010 LOCKED 2026-08-18 (PR #628) — cited here, untouched |
| 2 | Minimal ledger instrument: per-firing rows carrying tokens + outcome, attention-trend-shaped | **Wave 1** | closed by `spend-audit` + `.claude/ops/spend-ledger.csv` |
| 3 | `fleet-rules` and `loop-rules` each carry a pricing bullet citing the ruled doctrine | **Wave 2 — DEFERRED** | open; tracked on gh#624 as an explicit follow-up step |
| 4 | Row schema checkable by a selftest-bearing script; doctrine draft passes doc_lint | **Wave 1** | closed by `validate.py`/`trend.py` selftests + this LLD's doc_lint pass (idr-0010 already passes) |

**Why Wave 2 is deferred, exactly:** `python3 harness/scripts/version_claim_check.py teamwork
--repo kimgranlund/claude-plugins` (run 2026-08-18 by the dispatching session, not re-derived
here) shows PR #639 OPEN and claiming teamwork's next version slot (2.24.4). `fleet-rules`
Section 4 (version-slot + merge-order) rules one version-bumping build in flight per plugin at
a time; both Wave 2 bullets are body edits to teamwork prompt-carrying skills and therefore owe
a teamwork version bump + a fresh-context skill-checker pass (`.claude/rules/plugin-authoring.md`,
semantic-edit invariant). Bundling them into this PR would open a second concurrent teamwork
version claim. So: **Wave 1 = authorkit only (this build's PR); Wave 2 = the two bullets (+ the
optional close-out wiring below), a separate PR, `blocked-by: PR #639 merged and teamwork's
version slot clear`.** gh#624 stays OPEN after Wave 1 lands with criterion 3 named as the
remaining item; the Wave 1 Findings write-back states this verbatim.

**Non-goals (both waves):** numeric pricing bands or ceilings (idr-0010: qualitative first,
bands only after the ledger has data); rows for every fork/subagent (sweeps + dispatched builds
first, per idr-0010's lean); any hook (all retired, #466); a new collector AGENT (a procedure
armed by `CronCreate` is enough until the ledger proves it is read — idr-0010's own
falsification test applies to its instrument too); a roadmap row (ruled below); any change to
`harness:sweep-chores`, `teamwork:mobilize-chores`, or `teamwork:dispatch-ticket` bodies (the
close-out wiring into those flows is Wave 2's optional second half, each riding its own plugin's
version slot when clear — Wave 1 only STATES the convention wording those flows will paste).

## Resolution 1 — Home and name: `authorkit`, skill `spend-audit`

**Home: authorkit**, no fork — it already owns the trend-instrument + audit family
(`attention-audit`, `recurrence-audit`, `bloat-audit`, `naming-audit`, `pattern-audit`,
`doctrine-audit`, `estate-audit`, `repo-audit`) and the exact `trend.py`-appends-a-CSV shape
this reuses; lld-0011's Ruling 1 (recurrence-audit) already made this call for the same family
and it holds unchanged here.

**Name: `spend-audit`** — `{object: spend}-{process: audit}` under ADR-0011's grammar; `audit`
is already in both manifests' `process_lex`; `spend` is registered in `object_vocab` of BOTH
`naming.manifest.json` (repo root) and `authorkit/naming.manifest.json` by this build (checked
2026-08-18: present in neither). Why not the nearer words: `cost` and `economy` both already
appear in `attention-audit`'s own description ("attention economy", "audit our menu cost") — a
skill named `cost-audit`/`economy-audit` would be a routing twin by construction; `token` is
in `object_vocab` already but means DESIGN tokens estate-wide (design plugin), a worse
collision. `spend` is idr-0010's own noun ("recurring spend is priced") and, as a noun, appears in no
routable description today (grep 2026-08-18 over every SKILL.md/agent description: one verb hit
only — `bloat-audit`'s "prose that spends words", which `spend-audit`'s own NOT-prose-bloat
clause already fences; the remaining ~10 hits are body prose, not routing surface).

**Fence with `attention-audit` — one-sided by measured necessity.** `attention-audit`'s
description is 692 chars (measured 2026-08-18) against skill_lint's W8 700-char ceiling: 8 chars
headroom, `fence_tight` by `collide.py`'s own rule (under 23) — a NOT-clause on that side does
not fit without a diet, and a diet-to-afford-a-fence is the treadmill attention-audit's own step
3 names. `collide.py`'s `fenced` test is satisfied when EITHER side names the other, so the
fence lives on `spend-audit`'s side ("NOT menu rent / description collisions
(`attention-audit`)") plus the sibling-suite half of `.claude/rules/plugin-authoring.md`'s
reciprocal-fence rule: `attention-audit/evals/evals.json` gains one no-trigger case (a
per-firing token-spend prompt, `comment: owner: spend-audit`). `attention-audit`'s description
is NOT edited. `check-routing authorkit` proves the boundary.

## Resolution 2 — Row schema: Kim's six columns + `tokens_source` + `ref`

`HEADER = ["date", "event_kind", "seat", "ref", "tokens", "tokens_source", "outcome",
"verdict"]` — eight columns, one row per firing.

| Column | Values | Why it is here |
|---|---|---|
| `date` | `YYYY-MM-DD` (validated) | Kim's seed; same grain as attention-trend.csv |
| `event_kind` | `sweep` \| `build` | Kim's seed; idr-0010's lean (sweeps + dispatched builds first, not every fork) |
| `seat` | non-empty slug — the seat or command that fired (`issue-sorter`, `mobilize-chores`, `build-leader`, `dispatch-ticket`, …) | Kim's "seat/command"; column named `seat` for CSV/CLI hygiene (`--seat`) |
| `ref` | `#NNN` (issue or PR), a repo-relative report path (e.g. `.claude/ops/reports/2026-08-18T02-28-59Z.md`), or the literal `none` | ADDED. The firing's durable artifact = the ledger's identity/dedupe key `(date, event_kind, seat, ref)`; without it the backfill path cannot tell "already recorded" from "missing", and an `outcome` of `pr-merged` is unverifiable. Kim/doc-checker may veto — it is flagged as an addition beyond the seed, not smuggled in |
| `tokens` | non-negative integer, or the literal `absent` | Kim's seed; the metric idr-0010 names first |
| `tokens_source` | `measured` \| `estimated` \| `absent` | ADDED. Provenance of `tokens`. Cross-field rule (validator-enforced): `tokens == absent` ⇔ `tokens_source == absent`. This is a categorical provenance flag, not a derived or blended figure — see the precedent check below |
| `outcome` | `pr-merged` \| `pr-opened` \| `acted` \| `no-op` \| `blocked` \| `failed` | Kim's seed, made a closed vocabulary so rows are comparable ("five sweeps, all `no-op`" is the finding idr-0010 wants to be able to make). `acted` = the sweep/build produced its artifact (queued items, a report, a filed issue) short of a PR; `no-op` = fired, changed nothing |
| `verdict` | `worth-firing` \| `not-worth-firing` \| `undetermined` | Kim's seed; the per-firing qualitative judgment, INGESTED never computed (Resolution 5) |

**No-blended-column precedent — verified, not assumed.** `attention-audit/scripts/trend.py`'s
selftest asserts its header carries no `ratio`/`quotient`/`per_token` column and its docstring
states why: a single blended quotient rewards deleting the fences that protect
rare-but-expensive misroutes (Goodhart, 2026-08-15). `recurrence-audit/scripts/trend.py`
extends it to "no cross-series column" — while itself carrying `routing_pass_rate`, a WITHIN-
series ratio, so the law is about blending series into one score, not about every derived
column. `tokens_source` is neither: it is a categorical tag describing where `tokens` came
from, and `verdict` is a recorded judgment, not a computation. Both scripts' selftests carry the
identical no-ratio/quotient/per_token header assertion so the law is enforced here too — and,
per idr-0010's "numeric bands only after the ledger has data", the schema deliberately has no
`tokens_per_outcome`-shaped column; if bands are ever ruled, they are a REPORT computation over
rows, never a stored column.

## Resolution 3 — Token-count source: the trichotomy, honestly

The hard part gh#624 and idr-0010 both flag: no reliable programmatic per-agent token count is
reachable from inside a firing, and no hook may own it. The design does not solve measurement;
it makes non-measurement visible and never fabricates:

- **`measured`** — an instrument reported the figure for the whole firing. Two instruments
  exist in this estate today, both matching idr-0010's own first two options: (a) the
  DISPATCHING session's Agent-tool completion summary for a sealed dispatch (the channel
  gh#265's hop-tax measurement itself read — 61,515 / 117,950 output tokens, subtree-inclusive
  for the chain); (b) a transcript-jsonl usage sum over the firing's own `agent-*.jsonl` under
  the project's `~/.claude/projects/<project>/` dir (the recovery path already in this estate's
  memory notes). Either is `measured`; the row does not distinguish them (a `note` column was
  considered and rejected — Rejected alternatives).
- **`estimated`** — a declared or derived approximation: a seat's own "~200k", one leg of a
  chain standing in for the whole, a figure read off a rounded status line. idr-0010's own
  order-of-magnitude numbers are exactly this class.
- **`absent`** — nothing was measured or declared. `tokens` reads `absent` too. A row with
  `absent` tokens is STILL a row: it records that the firing happened, its outcome, and its
  verdict — the cadence-vs-yield judgment idr-0010 wants is possible on outcomes alone; the
  token column sharpens it when present.

Comparability rule (skill body, not script): the audit compares `measured` rows with
`measured`, `estimated` with `estimated`; it never averages across source classes. idr-0010's
falsification clause ("a ledger of estimates nobody trusts is worse than no ledger") is
answered by making the estimate share of the ledger a first-class audit finding: a ledger that
is 100% `estimated`/`absent` after several cycles is reported as "the instrument has not been
found", not silently tolerated.

## Resolution 4 — Write path: close-out convention (primary) + backfill (fallback), no hooks

**Root-cause constraint that shapes this (not just #466):** `harness:ops-write-sandbox-rules`
(issue #125) — a dispatched seat's direct `.claude/ops/...` write lands in the dispatching
session's isolated worktree, stranded; and the `measured` figure for a sealed dispatch is
visible only to its dispatcher (Resolution 3a). Both point the same way: **the row is written
by whoever owns the firing's close-out on a real checkout.**

**The convention — exact wording (paste-ready; Wave 2 wires it into the dispatching flows,
Wave 1 records it here and in the skill body):**

> **Spend-ledger close-out (idr-0010, `authorkit:spend-audit`).**
> **If you are the host, or you own this firing's close-out on a real checkout** (a
> `/mobilize-chores` or `/sweep-chores` run in your own session; a build you dispatched and
> whose handback you just read; a sweep seat's payload you just applied): as your LAST step,
> append exactly one row —
> `python3 authorkit/skills/spend-audit/scripts/trend.py --out .claude/ops/spend-ledger.csv --event-kind <sweep|build> --seat <seat-or-command> --ref <#NNN | report path | none> --tokens <N | absent> --tokens-source <measured|estimated|absent> --outcome <pr-merged|pr-opened|acted|no-op|blocked|failed> --verdict <worth-firing|not-worth-firing|undetermined>`
> — one row per firing; for a build you dispatched, `--tokens` is the Agent-tool completion
> summary's token figure with `--tokens-source measured`. Never invent a count: no instrument
> and no declared estimate → `--tokens absent --tokens-source absent`. Commit the row with the
> same vehicle as your other state for this firing (an `ops:` commit for a sweep firing; your
> session's next commit otherwise). Name the appended row in your handback's Evidence.
> **If you are a sealed dispatched seat** (an `Agent`-tool dispatch with no real-checkout write —
> `harness:ops-write-sandbox-rules`): do NOT run `trend.py`. State `outcome` and `ref` in your
> handback (write-handoff's Status/Evidence already carry them) and, only if you have one, your
> own token estimate as `estimated`; your dispatcher appends the row.

**Backfill (fallback path, the skill's "Collector" procedure — no new agent):** run by a host
session on the real checkout, optionally armed session-scoped via `CronCreate` exactly as
`harness:decision-watcher` is ("re-armed per work session, not a durable crontab"). Steps: (1)
`validate.py .claude/ops/spend-ledger.csv --json` → last recorded date + the set of
`(date, event_kind, seat, ref)` keys; (2) enumerate firings since then from sources that
already exist — builds: `gh pr list --state merged --search "merged:>=<date>"` and
`gh issue list --label in-flight` (dispatch-ticket's claim comments name the seat); sweeps:
`.claude/ops/reports/*.md` filenames (issue-sorter's hourly firings already land there,
verified live in lld-0015) and `git log --format=%s -- .claude/ops/` `ops: sweep firing …`
subjects; (3) append one row per unrecorded key with `--tokens absent --tokens-source absent`
(or `estimated` when the report itself states a figure) and `--verdict undetermined`; (4)
report how many rows were backfilled — a persistently high backfill share is itself the
finding that the close-out convention is not being followed (surface it, don't absorb it).
`ref` is what makes step 3 idempotent; a firing with `ref none` cannot be backfilled and the
skill says so.

**Append-collision class, named:** two branches each appending a row to the same CSV conflict
on a 3-way merge (both add at EOF). Mitigations, in order: rows for a sealed build are appended
by its dispatcher (one writer per session, not one per PR); `.gitattributes` gains
`.claude/ops/spend-ledger.csv merge=union` (git's built-in driver keeps both sides' lines —
honored by local merges/rebases and `sync_main.py`; GitHub's web merge does NOT honor custom
drivers, so a PR conflict on this file is still possible and resolves by keeping both rows);
the backfill's dedupe key re-adds any row a conflict resolution dropped.

## Resolution 5 — What `verdict` means on a row (self-grading, bounded)

The row's `verdict` is the closing seat's judgment for THAT firing — a sweep that spent a
`measured` 200k and produced `no-op` is `not-worth-firing`; a build that reached `pr-merged` is
`worth-firing`; unclear is `undetermined` (the honest default, expected to dominate early). It
is ingested by `trend.py`, never computed — no script derives worth from tokens (that would be
`script-writing-rules`' "judgment wearing a costume"). idr-0010's REAL test — is this firing
CLASS worth its cadence — is the skill's audit render over the row history (Components, skill
step 4): per `(event_kind, seat)` class, rows, outcome mix, token range per source class, and a
recommendation drawn from a closed set — keep / re-cadence / re-scope / retire — with the rows
cited, feeding the calendar's cadence column and the DRI review, exactly the gh#265-shaped
"second measurement-driven decision" idr-0010's Proof clause asks for. Generator≠critic
weakness of self-graded rows is bounded by (a) the dispatcher, not the firing seat, writing
build rows, and (b) the class-level judgment being re-made over history by a different session.

## Resolution 6 — Ledger location and seeding

`.claude/ops/spend-ledger.csv` — Kim's explicit 2026-08-18 direction ("under `.claude/ops/`"),
followed over the repo-root precedent of `attention-trend.csv`/`recurrence-trend.csv`. Named
`ledger`, not `trend`: it is per-firing rows, not a per-release series. Seeded by the build
itself: the FIRST real row is this build's own firing (`build`, `dispatch-ticket`, `#624`,
tokens as the builder honestly has them, `pr-opened`, `undetermined`) — written by a real
`trend.py` run, never by hand, so the header is script-emitted. `.claude/ops/calendar.md` gains
one standing-loop row ("Spend-ledger review — monthly, alongside the brief review; human-assert
cadence, tunable") — idr-0011 rules every standing loop carries a cadence, and calendar.md's own
header already points cost pricing at "idr-0010's ledger".

## Resolution 7 — Roadmap-row discrepancy: no roadmap row is owed (recorded)

idr-0010's Open questions and Kim's seed comment both record that gh#624's intake note claimed a
roadmap row that does not exist on origin/main and that gh#624 carries no `roadmap` label.
Checked against the roadmap file's own contract (`.claude/docs/roadmap/roadmap-nonoun-plugins.md`
header) and `docs:doc-writing-rules`' RDD section (ruled gh#611, realized by lld-0010): a roadmap
row is for a `roadmap`-LABELED issue — a parked, sweep-immune, release-grain item bound to an
RDD via `Tracked at <owner>/<repo>#NNN`. gh#624 is `feature` + `size:big` + `in-flight`, claimed
and building — the opposite of parked; labeling it `roadmap` would make it sweep-immune mid-
build. **Decision: gh#624 is a build ticket; the intake claim was a mis-statement, not a missing
row. No roadmap row, no `roadmap` label.** The Wave 1 Findings write-back states this on the
ticket so the discrepancy stops being carried.

## Components

All Wave 1 paths under `authorkit/` unless stated.

### `skills/spend-audit/SKILL.md`

Frontmatter mirrors the audit-family siblings (recurrence-audit precedent): `kind: skill`,
`author: kim`, `created`/`last_updated: 2026-08-18`, `disable-model-invocation: false`,
`user-invocable: true`, `allowed-tools: Read, Glob, Grep, Bash(python3 */scripts/validate.py *),
Bash(python3 */scripts/trend.py *), Bash(gh pr *), Bash(gh issue *), Bash(git log *)`. Description
(≤ 700 chars, W8): use for "price a sweep/build firing", "append a spend-ledger row",
"is this sweep worth firing / worth its tokens", "validate the spend ledger", "backfill missing
firing rows", "which recurring automation costs more than it yields"; NOT menu rent / description
collisions (`attention-audit`); NOT incident recurrence (`recurrence-audit`); NOT prose bloat
(`bloat-audit`); NOT loop budget design (teamwork `loop-rules`).

Body, in order: (1) the idr-0010 citation and the "reports and appends, never rewrites doctrine
or gates" posture; (2) the schema (one table, the Data section below, cited from `validate.py`
as canon); (3) **the close-out convention block verbatim** (Resolution 4) — this is the text a
dispatch prompt pastes; (4) Procedure — **Append** (one firing: `trend.py`), **Validate**
(`validate.py <ledger>`), **Collector/backfill** (Resolution 4's steps), **Audit** (per-class
worth-firing render, Resolution 5, verdict-first, keep/re-cadence/re-scope/retire from a closed
set, rows cited, `estimated`/`absent` share reported as a finding, comparisons within source
class only); (5) Degraded modes — no ledger yet (first run seeds header via `trend.py`; validate
reports "no ledger, nothing to validate", exit 0 with that verdict line, never a false failure);
100% `absent` tokens (rows still judged on outcomes; the instrument gap is the finding); `gh`
unavailable (backfill degrades to report-path + git-log sources only, stated); (6) Composition —
`estate-audit-agent` is NOT extended (its `requires:` enumerates instruments; adding `spend` is
a Wave-2-or-later agent edit, not needed to ship — the skill's scripts already ride the agent's
existing `validate.py`/`trend.py` grants if a future dispatch names them); the ledger's reader is
the monthly brief review + `calendar.md`'s new row. Procedure text uses `<this skill>/scripts/…`
(lld-0004/lld-0011's family ruling, reused).

Rides a fresh-context `harness:skill-checker` pass before merge (semantic edit to a
prompt-carrying artifact).

### `skills/spend-audit/scripts/validate.py` — schema owner + re-validator

Deterministic, stdlib-only, offline. Owns `HEADER`, `EVENT_KINDS`, `TOKENS_SOURCES`, `OUTCOMES`,
`VERDICTS`, `DATE_RE`, `validate_row(row: dict) -> list[str]` (findings, empty = clean) and
`validate_file(path) -> dict` (per-line findings + summary). `trend.py` imports it as a sibling
module (`import validate` — `sys.path[0]` is the script's own dir when run by path, which is how
G4 and every caller run it), so the schema exists in exactly one file.

```
validate.py <ledger.csv> [--json]
validate.py selftest
```

Checks: header equals `HEADER` exactly (a foreign/reordered header is a FAIL, never coerced);
per row: column count; `date` matches `YYYY-MM-DD` and parses; `event_kind`/`tokens_source`/
`outcome`/`verdict` in their enums; `seat` non-empty; `ref` is `#\d+`, a repo-relative path
(no leading `/`), or `none`; `tokens` is a non-negative integer or `absent`; cross-field:
`tokens == absent` ⇔ `tokens_source == absent`; duplicate key `(date, event_kind, seat, ref)`
with `ref != none` → WARN (a legitimate re-fire is possible; the backfill must not double-add).
Verdict line NORMATIVE (`spend-ledger validate · <clean|N fail / M warn> · <rows> rows`), then
`file:line: message` findings. Exit: 0 clean / 1 findings / 2 usage (missing path; unreadable
file). A missing ledger file at the ruled path is exit 0 with the verdict `no ledger yet` — the
expected first-run state, never a false failure (mirrors recurrence-audit's zero-seeded honesty).

Selftest fixtures (negative controls that bite, reverse controls that stay quiet): a clean
3-row fixture → 0 findings (reverse); a foreign header → FAIL; a bad date, an unknown
`event_kind`, an unknown `outcome`, an unknown `verdict` → each one FAIL by line; `tokens
absent` with `tokens_source measured` → FAIL (cross-field, both directions: `tokens 1200` with
`tokens_source absent` also FAILs); a negative or non-integer `tokens` → FAIL; a `ref` of `/abs`
→ FAIL, `#12` and `none` and `.claude/ops/reports/x.md` → clean; an exact duplicate key → WARN
(and the same key with `ref none` → NOT a warn — the reverse control for dedupe); the header
carries no `ratio`/`quotient`/`per_token` column (the family's Goodhart assertion); the verdict
line string is pinned exactly; the missing-file path → exit 0 + `no ledger yet`.

### `skills/spend-audit/scripts/trend.py` — append exactly one validated row

```
trend.py --out <ledger.csv> --event-kind <sweep|build> --seat <slug> --ref <#NNN|path|none>
         --tokens <N|absent> --tokens-source <measured|estimated|absent>
         --outcome <enum> --verdict <enum> [--date YYYY-MM-DD] [--dry-run]
trend.py selftest
```

Same append anatomy as its two siblings (`new = not os.path.isfile(out)` → header first, then
one row). Behaviour that differs from the siblings and is the point: it **validates before it
writes** — builds the row dict from argv, calls `validate.validate_row`; any finding → print
findings, exit 1, **nothing written** (not even the header on a fresh file); an existing file
whose header is not `HEADER` → exit 2 (never append under a foreign schema; run `validate.py`
to see why). No `--tokens` and no `--tokens-source` → both default to `absent` together (the
convenient honest default); exactly one of them supplied → usage error 2 (never silently pair
a number with `absent` or vice versa). `--dry-run` prints the row it WOULD append and exits 0
without touching the file (what a sealed seat can use to hand its dispatcher a pre-validated
line). Prints `appended row to <out>: {…}` on success. Exit: 0 appended / 1 row invalid /
2 usage or schema mismatch.

Selftest fixtures: fresh file → header + one row (positive), second append does not rewrite
the first (append semantics); a malformed row (bad `outcome`) → exit-1 path AND the file is
byte-identical before/after (negative control — the write is refused, not partially applied);
a fresh path + malformed row → no file created; a foreign-header file → the schema-mismatch
path and no append; both `tokens` flags omitted → row carries `absent`,`absent`; only one
supplied → usage error; `--dry-run` leaves the file untouched and prints the row; header carries
no `ratio`/`quotient`/`per_token` column; `verdict` is passed through verbatim (assert the script
never rewrites it from tokens — feed `tokens 999999`, `verdict worth-firing` and read it back
unchanged).

**Script names are `validate.py`/`trend.py` deliberately** — `estate-audit-agent`'s existing
tool grants (`Bash(python3 */scripts/validate.py *)`, `Bash(python3 */scripts/trend.py *)`, path-
glob-scoped, not skill-scoped) already cover both basenames; reusing them means no agent
allowlist edit (lld-0011's own ruling on `scan.py`/`trend.py` reuse, extended). This is a design
constraint honored, not a coincidence.

### `skills/spend-audit/evals/evals.json`

≥ 6 trigger cases ("Append a spend-ledger row for the sweep that just ran", "Is the hourly
issue-sorter worth its tokens?", "Which of our recurring sweeps cost more than they yield?",
"Validate .claude/ops/spend-ledger.csv", "Backfill ledger rows for yesterday's builds", "Price
this build firing per idr-0010"); no-trigger fences with owners in `comment`: menu rent /
description collision → `attention-audit`; incident recurrence → `recurrence-audit`; prose bloat →
`bloat-audit`; "design the token budget for a /goal loop" → teamwork `loop-rules`; "how much
does this description cost per turn" → `attention-audit` (the nearest twin phrase, deliberately
included).

### `skills/attention-audit/evals/evals.json` (edit — sibling-suite half of the fence)

One new no-trigger case: a per-firing token-spend / worth-firing prompt, `comment: owner:
spend-audit — per-firing token spend and worth-firing verdicts, not menu rent`. **Description
untouched** (692/700 chars — Resolution 1).

### `.claude/ops/spend-ledger.csv` (new, script-seeded) · `.claude/ops/calendar.md` (edit) · `.gitattributes` (new)

Ledger seeded with this build's own row via a real `trend.py` run (Resolution 6). Calendar gains
one row in "Standing loops": Spend-ledger review · Monthly (tunable) · Human review of
`.claude/ops/spend-ledger.csv` via `spend-audit`'s Audit procedure · Kim · human-assert cadence,
alongside the brief review. `.gitattributes` created at repo root with the single line
`.claude/ops/spend-ledger.csv merge=union` and a comment naming this LLD (Resolution 4).

### Ledger/manifest edits

`authorkit/README.md` Map rows (skill + two scripts) + Version ledger line (`v0.22.0` — re-read
`authorkit/.claude-plugin/plugin.json` off `origin/main` immediately before bumping, G14/#445's
value-race discipline; 0.21.0 was current at authoring); `authorkit/.claude-plugin/plugin.json`
version; `naming.manifest.json` (root) AND `authorkit/naming.manifest.json` `object_vocab` +=
`{"canonical": "spend", "plural": null, "banned_aliases": []}` (shape per the existing entries —
copy a neighbor's exact key set).

### Rulings that earned no ADR (recorded here, ADR-default-no)

Every ruling above follows an established estate pattern (family home, script-name reuse, no
blended column, sandbox-aware write path, one-sided fence under a measured W8 constraint) or is a
sequencing choice forced by a live version-slot fact; none is a hard-to-reverse fork between
genuine alternatives that changes an owning doc's substance. idr-0010 stays the doctrine; this
LLD is its instrument's how. Should the `ref`/`tokens_source` columns be vetoed at doc-check, that
is a schema edit here, not a supersession anywhere.

## Interfaces

- **`validate.py` ↔ `trend.py`:** sibling import; `validate.py` is the schema canon
  (`HEADER` + enums + `validate_row`); `trend.py` never redefines any of them. A schema change
  is one edit in `validate.py` and both selftests move together.
- **Close-out convention → dispatching flows:** the block in Resolution 4 is the interface; Wave 1
  publishes it (LLD + skill body), Wave 2's optional second half pastes it into
  `dispatch-ticket`'s Findings write-back step, `mobilize-chores`'/`sweep-chores`' last step —
  each in its own plugin's version slot when clear. Until then a host session applies it by
  reading the skill.
- **Sealed seat → dispatcher:** the seat's write-handoff block (Status/Evidence) already carries
  `outcome` and `ref`; a seat MAY add a `--dry-run` line; the dispatcher appends and cites the
  row in ITS handback/Findings.
- **`spend-ledger.csv` → readers:** the skill's Audit render, the monthly brief review
  (`brief-nonoun-plugins.md`), `calendar.md`'s cadence column (a re-cadence recommendation edits
  that file directly, per lld-0015's Resolution 1), and idr-0010's Proof clause (a sweep retired /
  re-scoped / re-cadenced citing its rows = the confirming datum).
- **`spend-audit` ↔ `attention-audit`:** one-sided NOT-clause + sibling-suite case; `collide.py
  --against spend-audit` and `check-routing authorkit` are the proofs.
- **`estate-audit-agent`:** no interface change in Wave 1; the scripts are grant-compatible by
  name (Components).

## Data

Ledger row shape (`.claude/ops/spend-ledger.csv`), header script-emitted:

```
date,event_kind,seat,ref,tokens,tokens_source,outcome,verdict
2026-08-18,build,dispatch-ticket,#624,absent,absent,pr-opened,undetermined
2026-08-18,sweep,issue-sorter,.claude/ops/reports/2026-08-18T02-28-59Z.md,absent,absent,acted,undetermined
2026-08-18,build,build-leader,#626,117950,measured,pr-merged,worth-firing
```

`validate.py --json` output:

```json
{
  "path": ".claude/ops/spend-ledger.csv",
  "rows": 3,
  "header_ok": true,
  "findings": [{"line": 4, "level": "FAIL", "message": "tokens_source `measured` requires an integer tokens value, got `absent`"}],
  "duplicate_keys": [],
  "summary": {"fail": 1, "warn": 0},
  "last_date": "2026-08-18",
  "keys": [["2026-08-18", "build", "dispatch-ticket", "#624"]]
}
```

(`last_date` and `keys` exist for the backfill procedure — Resolution 4.)

## Build sequence (Wave 1 — the order a builder implements)

| # | Step | Path | Done when |
|---|---|---|---|
| 1 | Register `spend` in `object_vocab` (root + authorkit manifests) | `naming.manifest.json`, `authorkit/naming.manifest.json` | `validate.py --scope grammar` (naming-audit's) accepts `spend-audit` |
| 2 | Write `validate.py` (schema owner) + selftest | `authorkit/skills/spend-audit/scripts/validate.py` | `python3 … validate.py selftest` → exit 0, every fixture above present |
| 3 | Write `trend.py` importing `validate` + selftest | `authorkit/skills/spend-audit/scripts/trend.py` | `python3 … trend.py selftest` → exit 0; malformed-row fixture proves nothing written |
| 4 | Write `SKILL.md` (convention block verbatim, four procedures, degraded modes) | `authorkit/skills/spend-audit/SKILL.md` | `skill_lint.py` clean; description ≤ 700 chars; names both scripts (no orphan script) |
| 5 | Write `evals/evals.json`; add attention-audit's no-trigger case | `…/spend-audit/evals/evals.json`, `…/attention-audit/evals/evals.json` | `release_gate.py authorkit` G7 green; `check-routing authorkit` green; `collide.py --target authorkit --against spend-audit` reports the pair fenced |
| 6 | Seed the ledger with this build's own row (real `trend.py` run) + `.gitattributes` + calendar row | `.claude/ops/spend-ledger.csv`, `.gitattributes`, `.claude/ops/calendar.md` | `validate.py .claude/ops/spend-ledger.csv` → exit 0, `rows: 1`; `git check-attr merge .claude/ops/spend-ledger.csv` → `union` |
| 7 | README Map rows + ledger line; version bump (re-read origin/main first) | `authorkit/README.md`, `authorkit/.claude-plugin/plugin.json` | `release_gate.py authorkit --package` fully green (G1–G14) |
| 8 | Fresh-context `harness:skill-checker` on the new SKILL.md; record verdict in the handback | — | verdict recorded; any semantic finding fixed before PR |
| 9 | Findings write-back on gh#624: Wave 1 shipped, criterion 3 = Wave 2 deferred (blocked-by PR #639 / teamwork slot), roadmap-row decision recorded, `ref`/`tokens_source` additions flagged for veto | gh#624 | comment posted; issue stays OPEN |

**Wave 2 (deferred, separate PR, `blocked-by: PR #639 merged + teamwork version slot clear`):**
(a) `teamwork/skills/fleet-rules/SKILL.md` Part B §9 Design rule 1 (solo-first / coordination
tax) gains one bullet: every recurring seat, sweep, and dispatched build is PRICED — a
per-firing row in `.claude/ops/spend-ledger.csv` via `authorkit:spend-audit`'s close-out
convention, the worth-firing test any cadence must pass (idr-0010, cited); (b)
`teamwork/skills/loop-rules/SKILL.md` Operating-model bullet on hierarchical budgets gains the
same one-line pricing citation; (c) optional: paste the convention block into `dispatch-ticket`'s
Findings write-back step and `mobilize-chores`' last step (teamwork), and `sweep-chores`' last
step (harness, its own slot). Each is a body edit → plugin version bump + fresh-context
skill-checker. Wave 2's own acceptance: `grep -c idr-0010` ≥ 1 in each of the two skills;
`release_gate.py teamwork` green; gh#624 closes.

## Acceptance (Wave 1 build gate — checkable predicates)

1. `python3 authorkit/skills/spend-audit/scripts/validate.py selftest` → exit 0.
2. `python3 authorkit/skills/spend-audit/scripts/trend.py selftest` → exit 0.
3. `python3 authorkit/skills/spend-audit/scripts/validate.py .claude/ops/spend-ledger.csv` → exit
   0, verdict line reports ≥ 1 row.
4. `python3 authorkit/skills/spend-audit/scripts/trend.py --out /tmp/x.csv --event-kind build
   --seat t --ref none --outcome bogus --verdict undetermined` → exit 1 and `/tmp/x.csv` does
   not exist (the write-refusal contract, checked live, not only in selftest).
5. `python3 harness/scripts/release_gate.py authorkit --package` → green (G4 selftests, G7
   evals, G10 README/version, G12/G12b naming grammar + manifest parity, G14 monotonicity).
6. `/check-routing authorkit` (harness; its Phase 1 runs `python3
   harness/scripts/eval_check.py` over every authorkit `evals.json`, which G7 also runs) → passes
   with the new suite and attention-audit's added case; the printed routing matrix shows no
   stolen/leaked case between `spend-audit` and `attention-audit`.
7. `python3 authorkit/skills/attention-audit/scripts/collide.py --target authorkit --against
   spend-audit --json` → the spend-audit/attention-audit pair is absent from unfenced output
   (fenced by construction).
8. Fresh-context skill-checker verdict on `spend-audit/SKILL.md` recorded in the handback.
9. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0018-estate-economy-ledger.md` → exit 0.
10. `git check-attr merge .claude/ops/spend-ledger.csv` → `union`.

## Risks

- **R-1 — the token instrument is the weak link (idr-0010's own doubt).** Early rows will be
  mostly `absent`/`estimated`. Detection: the Audit render reports the source-class share every
  cycle. Fallback: rows still carry outcome + verdict, so the cadence-vs-yield judgment survives;
  a ledger still 100% unmeasured after several cycles is reported as "instrument not found" and
  routes to idr-0010's supersession path, never silently tolerated. Locus: spec.
- **R-2 — the convention is not followed (rows never appended).** Detection: backfill share; a
  ledger with fewer rows than `.claude/ops/reports/` firings in the same window. Fallback:
  Wave 2(c) wires the block into the dispatching flows so it stops depending on habit. Locus:
  plan.
- **R-3 — self-graded `verdict`.** Bounded per Resolution 5 (dispatcher writes build rows; the
  class-level judgment is re-made over history). Detection: a class whose rows are all
  `worth-firing` while outcomes are all `no-op` — the audit flags the contradiction. Locus: spec.
- **R-4 — append conflicts on the shared CSV.** Named in Resolution 4; `merge=union` +
  one-writer-per-session + dedupe backfill. Residual: a GitHub-side conflict resolves by keeping
  both rows. Locus: execution.
- **R-5 — `ref`/`tokens_source` exceed Kim's six-column seed.** Both flagged explicitly for veto
  at doc-check; removing either is a `validate.py` edit + selftest update, no doctrine touched.
  Locus: spec.
- **R-6 — Wave 2 never lands.** gh#624 stays open with criterion 3 unmet. Detection: the
  ticket's own Findings entry names the blocker and the re-check command
  (`version_claim_check.py teamwork`); `/mobilize-chores`' next drain sees an in-flight ticket
  with a stated remaining step. Locus: plan.

## Rejected alternatives

- **Bundling the fleet-rules/loop-rules bullets into this PR.** Rejected: PR #639 holds
  teamwork's version slot (Scope and sequencing); a second concurrent claim violates fleet-rules
  §4. Deferred, not dropped.
- **A hook to append rows.** Rejected outright — all hooks retired (#466); nothing to argue.
- **Each dispatched seat appending its own row from inside the sandbox.** Rejected: the write
  strands per `ops-write-sandbox-rules` (#125) and the seat cannot see its own measured tokens;
  the dispatcher can do both. Kept as the host/close-out-owner form only.
- **A new collector agent.** Rejected for now: a procedure armed by session-scoped `CronCreate`
  covers the backfill; a standing seat must buy its coordination tax (idr-0007) and this ledger
  is the thing that would price it — build the seat only if backfill proves recurrent.
- **A `note`/`tokens_kind` ninth column** to distinguish output-only vs total figures or the
  instrument used. Rejected: `measured`/`estimated` already carries the honesty; a free-text
  column invites narrative rows the validator can't check. Revisit if two measured instruments
  prove non-comparable.
- **A per-firing row file (`.claude/ops/spend/<id>.csv`) instead of one CSV** to dodge append
  conflicts. Rejected: breaks Kim's attention-trend-shaped single-file direction; `merge=union` +
  dedupe backfill covers the conflict class at far lower cost.
- **A `tokens_per_outcome` (or any band) column.** Rejected: idr-0010 rules bands only after
  data exists, and the family's no-blended-column law makes it a report computation, never a
  stored column.
- **Naming the skill `cost-audit`/`economy-audit`/`token-audit`.** Rejected: routing twins with
  `attention-audit` (its description already owns "cost"/"economy") or with design tokens.
- **Editing `attention-audit`'s description for a two-sided fence.** Rejected: 8 chars of W8
  headroom (measured); `collide.py`'s fenced test accepts one side; the sibling-suite case
  closes the reciprocal half without a diet.
- **A roadmap row / `roadmap` label for gh#624.** Rejected — Resolution 7.
- **A SPEC or ADR for this change.** Rejected: acceptance is already checkable from the ticket +
  the locked IDR; no hard-to-reverse fork was resolved (Rulings that earned no ADR).

## Agent verification

Per `docs:agent-harness-rules` and gh#624's own criterion 4, the assert layer is the payload:
**new harnesses this build creates** — `validate.py selftest` and `trend.py selftest` (both
scripts' counters, negative + reverse controls, per `.claude/rules/scripts.md`), plus the live
write-refusal check (Acceptance 4). **Existing instruments that cover the rest** —
`release_gate.py authorkit` (G4 runs both selftests; G7 the evals suite; G12/G12b the `spend`
registration; G10/G14 README/version), `check-routing authorkit` (the routing boundary),
`collide.py --against` (the fence), `doc_lint.py` on this LLD, `git check-attr` for the merge
driver. **Fresh-context checker:** `harness:skill-checker` on the new SKILL.md (semantic edit).
**Human/judgment layer, stated as such:** whether a given firing class is worth its cadence is
the skill's Audit render read by the monthly review — a judgment over rows, never a script
verdict; and idr-0010's Proof clause (a second measurement-driven decision) is confirmed only by
a human decision citing rows, which no instrument here can assert. Wave 2's own verification is
`release_gate.py teamwork` + a skill-checker on each edited skill.
