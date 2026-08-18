---
name: spend-audit
kind: skill
description: >
  Instrument idr-0010's estate economy claim — a per-firing, per-archetype token-spend
  ledger at `.claude/ops/spend-ledger.csv` (attention-trend.csv-shaped, append-only).
  Appends one validated row per firing and emits a measured per-archetype cost-multiplier
  table vs the solo baseline. Use for "price a sweep/build firing", "append a spend-ledger
  row", "is this sweep worth firing / worth its tokens", "validate the spend ledger",
  "backfill missing firing rows", "per-archetype cost gradient". NOT menu rent /
  description collisions (attention-audit); NOT incident recurrence (recurrence-audit);
  NOT prose bloat (bloat-audit); NOT loop budget design (teamwork loop-rules).
author: kim
created: 2026-08-18
last_updated: 2026-08-18
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/trend.py *)
  - Bash(python3 */scripts/archetype_gradient.py *)
  - Bash(gh pr *)
  - Bash(gh issue *)
  - Bash(git log *)
---

# spend-audit

Reports and appends, never rewrites doctrine or gates — `idr-0010-estate-economy.md`
(LOCKED) is the doctrine this skill instruments; this skill never edits it, only cites
it. The instrument is `.claude/ops/spend-ledger.csv`: one row per firing (a sweep or a
dispatched build), attention-trend.csv-shaped (dated CSV, append-only, the literal
`absent` for anything unmeasured), realizing gh#624's acceptance criterion 2 per
`lld-0018-estate-economy-ledger.md`.

## Schema

`validate.py` is the schema canon (`HEADER` + the closed enums + `validate_row`) —
this table cites it, never restates it as a second source of truth:

| Column | Values | Why it is here |
|---|---|---|
| `date` | `YYYY-MM-DD` (validated) | same grain as `attention-trend.csv` |
| `event_kind` | `sweep` \| `build` | idr-0010's lean — sweeps + dispatched builds first, not every fork/subagent |
| `seat` | non-empty slug — the seat or command that fired (`issue-sorter`, `mobilize-chores`, `build-leader`, `dispatch-ticket`, …) | CSV/CLI hygiene (`--seat`) |
| `ref` | `#NNN` (issue or PR), a repo-relative report path (e.g. `.claude/ops/reports/2026-08-18T02-28-59Z.md`), or the literal `none` | the firing's durable artifact — the ledger's identity/dedupe key `(date, event_kind, seat, ref)`; without it the backfill path cannot tell "already recorded" from "missing" |
| `tokens` | non-negative integer, or the literal `absent` | the metric idr-0010 names first |
| `tokens_source` | `measured` \| `estimated` \| `absent` | provenance of `tokens`, never a derived figure. Cross-field rule (validator-enforced): `tokens == absent` ⇔ `tokens_source == absent` |
| `outcome` | `pr-merged` \| `pr-opened` \| `acted` \| `no-op` \| `blocked` \| `failed` | a closed vocabulary so rows are comparable ("five sweeps, all `no-op`" is a real finding). `acted` = produced its artifact (queued items, a report, a filed issue) short of a PR; `no-op` = fired, changed nothing |
| `verdict` | `worth-firing` \| `not-worth-firing` \| `undetermined` | the closing seat's per-firing judgment, INGESTED never computed — no script derives worth from tokens |
| `archetype` | `A1`..`A8` \| `UNMEASURED` | gh#673 — one of the estate's eight orchestration archetypes (`fleet-rules`/#666's taxonomy: A1 solo · A2 unnamed sync fan-out · A3 named background/teammate seats · A4 fleet terminal seats · A5 forked intake · A6 scheduled routines + `/goal` loops · A7 Workflow scripts · A8 `/batch`). REQUIRED on every new row — never empty. `UNMEASURED` is reserved for a best-effort RETROACTIVE backfill row whose shape is genuinely ambiguous; a live firing's own closing seat always knows its own archetype and states it |

No blended column, ever: the header carries no `ratio`/`quotient`/`per_token` column
(both scripts' selftests assert this); `tokens_source` is a categorical tag, `verdict`
is a recorded judgment — neither is a computation over the row. Numeric pricing bands
are a Wave-2-or-later REPORT computation over rows, never a stored column (idr-0010:
bands only after the ledger has data).

## Spend-ledger close-out (idr-0010, `authorkit:spend-audit`) — the paste-ready convention

> **Spend-ledger close-out (idr-0010, `authorkit:spend-audit`).**
> **If you are the host, or you own this firing's close-out on a real checkout** (a
> `/mobilize-chores` or `/sweep-chores` run in your own session; a build you dispatched and
> whose handback you just read; a sweep seat's payload you just applied): as your LAST step,
> append exactly one row (run from the workspace root — both paths below are repo-relative) —
> `python3 authorkit/skills/spend-audit/scripts/trend.py --out .claude/ops/spend-ledger.csv --event-kind <sweep|build> --seat <seat-or-command> --ref <#NNN | report path | none> --tokens <N | absent> --tokens-source <measured|estimated|absent> --outcome <pr-merged|pr-opened|acted|no-op|blocked|failed> --verdict <worth-firing|not-worth-firing|undetermined> --archetype <A1..A8|UNMEASURED>`
> — one row per firing; for a build you dispatched, `--tokens` is the Agent-tool completion
> summary's token figure with `--tokens-source measured`. Never invent a count: no instrument
> and no declared estimate → `--tokens absent --tokens-source absent`. `--archetype` is
> REQUIRED (gh#673): state which of the estate's eight orchestration archetypes fired (the
> Schema table above) — you almost always know this from how you dispatched or were
> dispatched; `UNMEASURED` is for a backfill row only, never a live firing's own default.
> Commit the row with the same vehicle as your other state for this firing (an `ops:` commit
> for a sweep firing; your session's next commit otherwise). Name the appended row in your
> handback's Evidence.
> **If you are a sealed dispatched seat** (an `Agent`-tool dispatch with no real-checkout write —
> `harness:ops-write-sandbox-rules`): do NOT run `trend.py`. State `outcome`, `ref`, and your
> own `archetype` in your handback (write-handoff's Status/Evidence already carry the first two;
> a dispatched seat knows how it was dispatched, so state the archetype too) and, only if you
> have one, your own token estimate as `estimated`; your dispatcher appends the row.

## Procedure

1. **Append** (one firing): `python3 <this skill>/scripts/trend.py --out
   .claude/ops/spend-ledger.csv --event-kind <sweep|build> --seat <slug> --ref <#NNN|path|none>
   [--tokens <N> --tokens-source <measured|estimated>] --outcome <enum> --verdict <enum>
   --archetype <A1..A8|UNMEASURED>` — exactly the close-out convention above. `--archetype` is
   REQUIRED like `--outcome`/`--verdict` (gh#673) — an omitted flag is a usage error, exit 2.
   Validated before it writes: a malformed row
   is refused outright, nothing written, not even the header on a fresh file. An existing
   file whose header is foreign is refused too (schema mismatch, exit 2 — run Validate to
   see why). `--dry-run` prints the row it WOULD append without touching the file — what a
   sealed seat can hand its dispatcher as a pre-validated line.
2. **Validate**: `python3 <this skill>/scripts/validate.py .claude/ops/spend-ledger.csv
   [--json]` — standalone re-validation of the whole ledger: header-exact, per-row shape,
   the `tokens`/`tokens_source` cross-field rule, duplicate `(date, event_kind, seat, ref)`
   keys (`ref != none`) as a WARN (a legitimate re-fire is possible; the backfill must
   never double-add). Never hand-count what the script measures.
3. **Collector/backfill** (fallback for firings whose owner never appended; run by a host
   session on a real checkout, optionally armed session-scoped via `CronCreate` exactly as
   `harness:decision-watcher` is — "re-armed per work session, not a durable crontab"):
   1. `validate.py .claude/ops/spend-ledger.csv --json` → `last_date` + the `keys` set —
      the dedupe key that makes this step idempotent.
   2. Enumerate firings since `last_date` from sources that already exist — builds:
      `gh pr list --state merged --search "merged:>=<date>"` and `gh issue list --label
      in-flight` (`dispatch-ticket`'s claim comments name the seat); sweeps:
      `.claude/ops/reports/*.md` filenames and `git log --format=%s -- .claude/ops/`
      `ops: sweep firing …` subjects.
   3. Append one row per unrecorded key: `--tokens absent --tokens-source absent` (or
      `estimated` when the report itself states a figure) and `--verdict undetermined`.
      A firing with `ref none` cannot be backfilled — say so, don't guess a `ref`. Best-effort
      infer `--archetype` from the firing's own shape (heuristics, not gospel — never guessed
      past what the evidence supports): a sweep fired by `sweep-chores`'s own fan-out (issue-
      sorter/repo-cleaner/decision-watcher in parallel) → `A2`; a `CronCreate`-armed standing
      seat's own periodic firing → `A6`; a build whose PR body names a `context: fork` command
      (`/build-feature`) → `A5`; a build dispatched via a `*-leader` agent with no fleet-roster
      join → `A2`/`A3` depending on whether the dispatch was named (check the PR's own "Build
      chain"/environment-clean prose for a teammate `SendMessage` mention); a seat with a live
      `fleet.json` roster entry at firing time → `A4`; a `harness/workflows/*.js` firing → `A7`;
      a `/batch` decompose-then-per-unit-PR firing → `A8`. Genuinely ambiguous (the evidence
      does not clearly name one archetype) → `--archetype UNMEASURED`, never a guess.
   4. Report how many rows were backfilled — a backfill share above 50% of a window's new
      rows is itself the finding that the close-out convention is not being followed.
      Surface it, never absorb it silently.
4. **Audit** (the worth-firing render, per `(event_kind, seat)` class, verdict-first): rows,
   outcome mix, and token range PER SOURCE CLASS (`measured` compared with `measured`,
   `estimated` with `estimated` — never averaged across source classes) for the class, then
   a recommendation drawn from a closed set — **keep / re-cadence / re-scope / retire** —
   with the cited rows. A class earns a keep/re-cadence/re-scope/retire recommendation only
   once it carries ≥ 3 rows; fewer than that, report `undetermined` rather than judging on
   thin evidence. Report the `estimated`/`absent` share as a first-class finding: a ledger
   that is still 100% `estimated`/`absent` after 3 review cycles (the calendar's monthly
   cadence, so roughly a quarter) reads "the instrument has not been found", never silently
   tolerated. A class whose rows are all `worth-firing` while outcomes are all `no-op` is a
   contradiction — flag it, don't resolve it here (a generator≠critic weakness this skill
   does not adjudicate alone; the class-level judgment is re-made over history by a
   DIFFERENT session, per lld-0018 Resolution 5). A re-cadence/re-scope/retire
   recommendation is applied by the human reviewer editing `.claude/ops/calendar.md`
   directly — this skill reports the render, it does not edit ops state itself.
5. **Archetype gradient** (gh#673): `python3 <this skill>/scripts/archetype_gradient.py
   .claude/ops/spend-ledger.csv [--json]` — the measured per-archetype token-cost multiplier
   table vs the A1 solo baseline, per outcome class (`pr-shipped` := `outcome == pr-merged`;
   `record-minted` := `outcome == acted` — the two classes this ticket defines, stated on
   every multiplier). A cell computes only when both the archetype's own rows and A1's own
   rows carry ≥ 1 `tokens_source: measured` value for that class; otherwise `UNMEASURED`,
   never guessed. Wall-clock is not instrumented by this ledger (a stated non-goal) and
   always reads `UNMEASURED (not instrumented)`; the one wall-clock figure ever printed is
   gh#265's own anchor (1.92× tokens / 3.6× wall-clock, the coordinator-hop measurement),
   emitted under a separate `anchor` key, an external citation never blended into the
   computed table. Refresh `references/archetype-cost-snapshot.md` (the committed, citable
   snapshot #672's ADR and #666's rubrics cite) from this render at every authorkit release
   boundary — paste the new output in, replacing the prior snapshot's own render block.

Done when: the row is appended (or its columns honestly read `absent`/`UNMEASURED` per the
convention), or the requested Validate/Audit/Archetype-gradient render is produced with every
source-class comparison kept separate and every `undetermined`/`absent`/`UNMEASURED` state
reported as exactly that — never conflated with a computed judgment.

## Degraded modes

- **No ledger yet** (the expected first-run state): `trend.py`'s first real append seeds
  the header; `validate.py` on a not-yet-existing path reports `no ledger yet` and exits 0
  — never a false failure.
- **100% `absent` tokens**: rows are still judged on `outcome` + `verdict` alone — the
  cadence-vs-yield judgment survives without a token figure; the instrument gap itself is
  the finding (lld-0018 Risk R-1), reported, never hidden inside a silently-skipped column.
- **`gh` unavailable or rate-limited**: the Collector/backfill procedure degrades to
  `.claude/ops/reports/*.md` filenames + `git log` sources only — state the degraded mode
  plainly, never silently drop the build-firing half of the backfill without saying so.
- **All rows `UNMEASURED`/no `measured` tokens on either baseline or archetype side** (the
  expected early state, gh#673): every Archetype-gradient cell reads `UNMEASURED` — this is
  the honest first-emit shape, not an instrument failure; it sharpens as `measured` rows
  accumulate under the archetype-required close-out convention.

## Composition

`estate-audit-agent` is **NOT extended** in Wave 1 — its `requires:` enumerates
instruments; adding `spend` is a Wave-2-or-later agent edit, not needed to ship. The
scripts already ride the agent's existing `Bash(python3 */scripts/validate.py *)` /
`Bash(python3 */scripts/trend.py *)` grants (path-glob-scoped, not skill-scoped) if a
future dispatch names them — the reason both scripts are named `validate.py`/`trend.py`
in the first place (`lld-0011`'s ruling on `scan.py`/`trend.py` reuse, extended here).
`archetype_gradient.py` is new (gh#673) and this skill's own `allowed-tools` grants it
directly; extending `estate-audit-agent`'s own grant is the same Wave-2-or-later call.

The ledger's reader is the monthly brief review (`brief-nonoun-plugins.md`) and
`.claude/ops/calendar.md`'s "Spend-ledger review" standing-loop row — a human diffing
this skill's Audit render release over release, exactly as `attention-trend.csv` is read
today. A re-cadence recommendation from the Audit step is applied by the human reviewer,
who edits `calendar.md` directly (`lld-0015`'s Resolution 1 licenses the direct edit) —
this skill itself only ever reports the render, never rewrites ops state on its own
initiative (the identity line above). `references/archetype-cost-snapshot.md` (gh#673) is
this skill's own committed, citable render snapshot — `#672`'s ADR and `#666`'s per-
archetype rubric pack cite it by stable path; refreshed at every authorkit release
boundary per the Archetype-gradient procedure step, never hand-edited between refreshes.
