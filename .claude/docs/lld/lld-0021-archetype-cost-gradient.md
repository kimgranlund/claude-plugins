---
doc-type: lld
id: lld-0021-archetype-cost-gradient
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#673
idr: idr-0010 (LOCKED — .claude/docs/idr/idr-0010-estate-economy.md; cited, never edited)
spec: none — gh#673's own Acceptance section (plus the 2026-08-18 resume-answers fold-in
  comment) carries the checkable criteria, and idr-0010 (LOCKED) already carries the ruled
  economy claim this extends; a standalone SPEC would restate what the ticket already states
  (lld-0018/lld-0020's own routing test).
scope: component
audience: builder, reviewer
---
# LLD — `spend-audit` gains per-archetype cost attribution + a measured multiplier table (gh#673)

**Verdict, head-first.** `spend-audit`'s ledger row schema (`validate.py`'s `HEADER`, the schema
canon lld-0018 established) gains a ninth column, `archetype` — REQUIRED on every new firing,
one of the estate's eight orchestration archetypes (#666's taxonomy) or the literal `UNMEASURED`
reserved for best-effort retroactive backfill of a genuinely ambiguous historical row, never a
live firing's own default. A new bundled script, `scripts/archetype_gradient.py`, reads the
ledger and emits a MEASURED per-archetype token-cost multiplier table against the A1 solo
baseline, normalized per a newly-DEFINED "per equivalent outcome" concept (two closed classes,
`pr-shipped` / `record-minted`, stated against the ledger's existing `outcome` enum — no new
column). Wall-clock stays uninstrumented by this ledger (a deliberate non-goal); every computed
wall-clock cell reads `UNMEASURED (not instrumented)`, and gh#265's own anchor (1.92× tokens /
3.6× wall-clock, the coordinator-hop measurement) is cited as an external reference, never
computed from ledger rows and never blended into the computed table. Output lands in two forms
per the ticket's own Acceptance: the script's own machine-parseable render (`--json`), and a
committed snapshot doc at a stable path, `authorkit/skills/spend-audit/references/
archetype-cost-snapshot.md`, refreshed at every authorkit release boundary.

## Resolution 1 — Schema: `archetype` as a ninth, REQUIRED column, appended at the end

**Placement:** appended at the end of `HEADER` (`..., "verdict", "archetype"`), not inserted
mid-schema — minimizes positional churn on the existing seven columns and matches how the
schema already grew once before (`ref`/`tokens_source`, lld-0018 Resolution 2, added rather than
inserted). **Values:** `A1`..`A8` (#666's taxonomy, cited not restated — `fleet-rules`' Part B
Seat-access-doors + the taxonomy amendment comment on gh#666) or `UNMEASURED`. **REQUIRED, not
optional, on every new row** — the ticket's own ruled resize trigger ("archetype attribution
becomes a REQUIRED ledger field on new firings"); `trend.py`'s `--archetype` joins the existing
required-flag list (`--event-kind`/`--seat`/`--ref`/`--outcome`/`--verdict`) at the same usage-
error tier (a missing flag is exit 2), while an out-of-enum VALUE still routes through
`validate_row` for the exit-1 write-refusal path — the identical two-tier treatment every other
enum column already gets, and for the identical reason (`trend.py`'s own comment: an invalid
enum must reach the semantic-validation path, `choices=` would intercept it as a usage error
first, which is the wrong tier for a well-formed-but-wrong value).

**`UNMEASURED` is a closed-set member, not a shape exception** — `validate.py`'s `ARCHETYPES`
set is `{A1..A8} | {UNMEASURED}`; the validator enforces only that the value is IN this set, not
which firing class may use it. The never-for-a-live-firing rule is policy stated in `SKILL.md`'s
close-out convention and this LLD, not a shape check this validator can mechanically distinguish
(a validator cannot see whether a firing was live or backfilled from the row alone) — the same
posture idr-0010 already takes toward `tokens: absent` (a row can honestly carry it; the
instrument doesn't grade WHY).

## Resolution 2 — "Per equivalent outcome" normalization: defined here, against the existing enum

The ticket's own acceptance names this as undefined territory ("it exists nowhere yet"). Kept
simple and stated, per the ticket's own instruction, against `OUTCOMES` (already closed, no new
column):

| Outcome class | `outcome` values covered | Denominator meaning |
|---|---|---|
| `pr-shipped` | `pr-merged` | cost per PR that actually shipped |
| `record-minted` | `acted` | cost per non-PR artifact produced (queued items, a report, a filed ticket) |

`pr-opened`/`no-op`/`blocked`/`failed` firings are out of scope for this table (neither class
claims them) — they still feed the existing Audit render's worth-firing judgment, just not this
per-outcome cost comparison. Every multiplier the script emits states which class it normalizes
against (the `archetypes` JSON key is nested `{archetype: {outcome_class: {...}}}`, and the text
render prints the class inline on every line) — never a bare unlabeled number.

**Rejected: a `pr-opened`-inclusive `pr-shipped` class.** Considered folding `pr-opened` into
`pr-shipped` (a PR opened is a PR-shaped artifact too) — rejected: `pr-merged` is the outcome
that actually confirms the artifact landed (idr-0010's own worth-firing test already treats
`pr-opened` as a weaker signal than `pr-merged`), and blending the two would make the class
boundary a judgment call rather than a closed-set membership test.

## Resolution 3 — Extend `spend-audit`, not a sibling script (the ticket's own open call)

The ticket's Scope/Open section left this as the implementer's call. **Decision: extend
`spend-audit`** — the multiplier table reads the SAME ledger, imports the SAME schema canon
(`validate.py`), and belongs beside the existing Audit render (`SKILL.md` step 4) as step 5, not
a second skill duplicating the read path. A sibling `archetype-audit`-shaped skill was
considered and rejected: it would re-import `validate.py` across a plugin boundary with no
benefit, and `authorkit`'s own `*-audit` family already reads as "one instrument per skill" —
this is one MORE instrument on the SAME ledger, not a new domain.

## Resolution 4 — Computation: measured-only, per-cell, never blended across source classes

`archetype_gradient.py`'s `measured_tokens()` filters to `tokens_source == "measured"` before
computing a mean — reusing lld-0018 Resolution 3's comparability rule (`measured` compared with
`measured` only) at the multiplier-table layer, not just the Audit render's. A cell computes
`mean(archetype's measured tokens) / mean(A1's measured tokens)` for the SAME outcome class only
when both sides carry ≥ 1 qualifying row; short of that, `UNMEASURED` — literal, never a guess,
never an average pulled from `estimated`/`absent` rows to fill the gap. The A1 baseline itself is
never listed as its own subject row (comparing A1 to A1 is not a finding).

**Wall-clock, named as a non-goal, not silently dropped.** The ledger schema carries no
wall-clock column — adding one was considered and rejected here: gh#673's own ruled resize
trigger is the `archetype` field alone; a wall-clock column is a SECOND schema/contract change
this ticket never authorized, and no instrument for it exists today (idr-0010's own token-count
doubt applies doubly to wall-clock — no seat currently reports its own elapsed time). Every
computed wall-clock cell instead reads the fixed string `UNMEASURED (not instrumented)`,
honestly naming the gap rather than omitting the axis the ticket's Acceptance explicitly asks
for ("tokens AND wall-clock ... where measurable"). The one wall-clock number ever printed is
gh#265's own anchor, under a separate `anchor` JSON key, textually cited, proven by selftest to
stay constant regardless of ledger content (a reverse control: the anchor is never derived from
rows).

## Resolution 5 — Snapshot doc: home, path, refresh cadence

**Home:** `authorkit/skills/spend-audit/references/archetype-cost-snapshot.md` — a `references/`
folder already exists as a precedented pattern in this plugin (`attention-audit`, `bloat-audit`,
`naming-audit`, `naming-conventions`, `overhaul-planning`, `rename-planning` all carry one); this
is the skill's own generated data snapshot, not a knowledge-pack essay, but the home convention
— citable by stable path, versioned alongside the skill that generates it — transfers directly.
**Stable path, satisfying the ticket's own citability requirement:** `#672`'s ADR and `#666`'s
rubric pack cite this exact path, never a version-suffixed or dated filename (the CONTENT is
refreshed in place; the PATH never moves — `CLAUDE.md`'s "sources flow outward" invariant,
applied: this file is a snapshot that refreshes FROM the ledger + script, never the reverse).
**Refresh cadence:** every authorkit release boundary (a version bump), per the Archetype-
gradient procedure step in `SKILL.md` — paste the script's fresh render in, replacing the prior
block; the diff between snapshots is itself the signal of whether the instrument has been found
(mirrors lld-0018 Risk R-1's "instrument not found" test, applied one layer up).

## Resolution 6 — Migrating the existing one-row ledger

`.claude/ops/spend-ledger.csv` carries exactly one row (`#624`'s own seed, `archetype`-less
under the prior 8-column schema). A header/column-count schema change on an append-ONLY ledger
still needs every EXISTING row to carry a value under the new column, or `validate.py`'s own
column-count check FAILs every one of them permanently. **This is a one-time, disclosed schema
migration** (analogous to a locked ledger's own initial-authoring exemption, not an ordinary
content edit) — not itself mechanized as a bundled script (a single hand-edit of a two-line file,
disclosed in this build's Findings/PR body, is proportionate; a migration script would be
write-once code with no second caller, `script-writing-rules`' own "is this mechanizable"
question answered no). The row's own archetype is set to `UNMEASURED`: PR #642's "Build chain"
note (planner → builder → independent code-checker, `dispatch-ticket` Phase 4) does not by
itself disambiguate which of A2 (unnamed sync fan-out) / A3 (named seats) / A5 (forked intake via
`/build-feature`) the outer dispatch shape was — genuinely ambiguous, so `UNMEASURED` per the
ticket's own honesty bar, never guessed.

## Components

### `authorkit/skills/spend-audit/scripts/validate.py` (edit — schema owner)
`HEADER` gains `archetype`; new module constants `ARCHETYPE_NAMES` (the eight archetypes + short
descriptions, #666's taxonomy) and `ARCHETYPES` (`ARCHETYPE_NAMES` keys ∪ `{UNMEASURED}`); new
`OUTCOME_CLASSES` constant (Resolution 2's table, machine-readable). `validate_row` gains one
more membership check. Selftest fixtures updated (every existing row fixture gains a trailing
`archetype` value) plus new fixtures: an unknown archetype value FAILs; every one of the nine
closed values (`A1`..`A8`, `UNMEASURED`) individually stays clean (positive + reverse control,
every member exercised, not just one representative).

### `authorkit/skills/spend-audit/scripts/trend.py` (edit — the writer)
`--archetype` joins the required-flag set; `build_row` passes it through. Selftest: an invalid
archetype value takes the exit-1 write-refusal path (not a usage error); `UNMEASURED` round-trips
end-to-end (not just validate.py's enum check in isolation); a live CLI call omitting
`--archetype` entirely exits 2 naming the missing flag.

### `authorkit/skills/spend-audit/scripts/archetype_gradient.py` (new — the multiplier table)
Sibling-imports `validate.py` (same discipline as `trend.py` — the schema/taxonomy/outcome-class
constants live in exactly one file). `compute_gradient(rows)` is pure; `run(path, as_json)`
mirrors `validate.py`'s own no-ledger-yet honesty (exit 0, never a false failure) and adds a
foreign-header exit-2 path. Selftest: no-ledger-yet; an all-`UNMEASURED`/no-`measured` ledger (the
real current state) renders every cell `UNMEASURED` with correct n-counts and an unchanged
`anchor`; a positive-control ledger with real `measured` rows on both sides of one cell computes
the exact expected ratio; a different outcome class with zero rows on either side stays
`UNMEASURED` in the SAME payload (per-class isolation, not table-wide contamination); `estimated`/
`absent` rows never feed a ratio even when plentiful (the reverse control); wall-clock is NEVER
computed even in a cell whose tokens DO compute (the "not instrumented" fixed string, proven
independent of the tokens path); a foreign/reordered header exits 2.

### `authorkit/skills/spend-audit/references/archetype-cost-snapshot.md` (new — the citable snapshot)
Generated content: what it measures, the outcome-class definitions (Resolution 2's table
restated for a human reader), the gh#265 anchor block, and the script's real current render
against `.claude/ops/spend-ledger.csv` (1 row, all-`UNMEASURED` — the honest first-emit state,
named as expected per the ticket's own Scope/Open note). Regeneration command stated at the top.

### `authorkit/skills/spend-audit/SKILL.md` (edit)
Schema table gains the `archetype` row; the close-out convention block (paste-ready, both the
real-checkout and sealed-dispatched-seat halves) gains `--archetype`/the archetype-in-handback
instruction; Procedure gains step 5 (Archetype gradient); the backfill step (3) gains inference
heuristics for retroactive `--archetype` (stated as heuristics, not gospel); Degraded modes gains
the all-`UNMEASURED` case; Composition notes the new script's grant and the new reference file.
`allowed-tools` gains `Bash(python3 */scripts/archetype_gradient.py *)`. Description extended
(archetype + cost-gradient trigger phrases) — rides a fresh-context `harness:skill-checker` pass
before merge (semantic edit to a prompt-carrying artifact, `.claude/rules/plugin-authoring.md`).

### `authorkit/skills/spend-audit/evals/evals.json` (edit)
Two new trigger cases (the gradient/multiplier phrasing) and one new no-trigger case fencing
against `teamwork:wiring-checker` (an agent, not a skill — no reciprocal evals suite exists to
edit on that side; the fence is this suite's own disambiguation only).

### `.claude/ops/spend-ledger.csv` (migrated, Resolution 6)

## Interfaces

- **`validate.py` ↔ `trend.py` ↔ `archetype_gradient.py`:** the same sibling-import shape
  lld-0018 established, now with two importers of one schema-owner instead of one — no new
  interface pattern, an application of the existing one.
- **`archetype_gradient.py` → `references/archetype-cost-snapshot.md`:** one-way, generate-then-
  paste, human-triggered at release boundaries (no auto-regeneration hook — all hooks retired,
  #466; consistent with lld-0018's own "no hook" ruling for the ledger writer itself).
- **`spend-ledger.csv` → `archetype_gradient.py` → the snapshot → `#672`'s ADR / `#666`'s rubric
  pack:** the citation chain the ticket's Acceptance names explicitly; the snapshot's stable path
  is the contract those two documents depend on.
- **Close-out convention → every dispatching flow:** unchanged shape from lld-0018 Resolution 4,
  now carrying one more required field in the same paste-ready block.

## Data

Ledger row shape (`.claude/ops/spend-ledger.csv`), header script-emitted/migrated:

```
date,event_kind,seat,ref,tokens,tokens_source,outcome,verdict,archetype
2026-08-18,build,dispatch-ticket,#624,absent,absent,pr-opened,undetermined,UNMEASURED
```

`archetype_gradient.py --json` output shape (abbreviated — one archetype/class cell):

```json
{
  "baseline": "A1",
  "outcome_classes": {"pr-shipped": ["pr-merged"], "record-minted": ["acted"]},
  "anchor": {"source": "#265", "tokens_multiplier": 1.92, "wall_clock_multiplier": 3.6, "...": "..."},
  "rows_considered": 1,
  "archetypes": {
    "A2": {
      "pr-shipped": {"tokens_multiplier": "UNMEASURED", "n_baseline_measured": 0,
                     "n_archetype_measured": 0, "wall_clock_multiplier": "UNMEASURED (not instrumented)"}
    }
  }
}
```

## Build sequence

| # | Step | Path | Done when |
|---|---|---|---|
| 1 | `validate.py`: `archetype` column + `ARCHETYPES`/`ARCHETYPE_NAMES`/`OUTCOME_CLASSES` + selftest | `scripts/validate.py` | `validate.py selftest` exit 0, every closed value exercised |
| 2 | `trend.py`: `--archetype` required flag + selftest | `scripts/trend.py` | `trend.py selftest` exit 0; live missing-flag call exits 2 |
| 3 | `archetype_gradient.py`: new script + selftest | `scripts/archetype_gradient.py` | `archetype_gradient.py selftest` exit 0 |
| 4 | Migrate the 1-row ledger to the new schema | `.claude/ops/spend-ledger.csv` | `validate.py .claude/ops/spend-ledger.csv` exit 0, `rows: 1` |
| 5 | Generate the real snapshot against the migrated ledger | `references/archetype-cost-snapshot.md` | matches a live `archetype_gradient.py` run byte-for-byte on the render block |
| 6 | `SKILL.md` + `evals/evals.json` updates | `SKILL.md`, `evals/evals.json` | `skill_lint.py` clean (description ≤ 700 chars); evals JSON-valid |
| 7 | README ledger + version bump (re-read origin/main first) | `authorkit/README.md`, `authorkit/.claude-plugin/plugin.json` | `release_gate.py authorkit --package` fully green |
| 8 | Fresh-context `harness:skill-checker` on the edited `SKILL.md`; record verdict | — | verdict recorded; any finding fixed before PR |
| 9 | Dated Findings write-back on gh#673 | gh#673 | comment posted |

## Acceptance (checkable predicates)

1. `python3 authorkit/skills/spend-audit/scripts/validate.py selftest` → exit 0.
2. `python3 authorkit/skills/spend-audit/scripts/trend.py selftest` → exit 0.
3. `python3 authorkit/skills/spend-audit/scripts/archetype_gradient.py selftest` → exit 0.
4. `python3 authorkit/skills/spend-audit/scripts/validate.py .claude/ops/spend-ledger.csv` →
   exit 0, `rows: 1`, `header_ok: true`.
5. `python3 authorkit/skills/spend-audit/scripts/trend.py --out /tmp/x.csv --event-kind build
   --seat t --ref none --outcome acted --verdict undetermined` (no `--archetype`) → exit 2, names
   the missing flag, `/tmp/x.csv` not created.
6. `python3 authorkit/skills/spend-audit/scripts/archetype_gradient.py
   .claude/ops/spend-ledger.csv --json` → valid JSON, `anchor.source == "#265"`, every
   `archetypes.*.*.tokens_multiplier` is either a number or the literal `"UNMEASURED"`, every
   `wall_clock_multiplier` is `"UNMEASURED (not instrumented)"`.
7. `references/archetype-cost-snapshot.md` exists at the stated stable path and its render block
   matches a live re-run of step 6 (plain-text form).
8. `python3 harness/scripts/release_gate.py authorkit --package` → green.
9. Fresh-context skill-checker verdict on the edited `SKILL.md` recorded in the handback.
10. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0021-archetype-cost-gradient.md` →
    exit 0.

## Risks

- **R-1 — every computed cell is `UNMEASURED` at first emit.** Expected (ticket's own Scope/Open
  note); the snapshot doc states this plainly rather than reading as a broken instrument.
  Detection: the snapshot's own diff release-over-release. Fallback: the close-out convention now
  requires `--archetype` on every new row, so the gap closes as real `measured` rows accumulate.
  Locus: spec.
- **R-2 — retroactive `UNMEASURED` inference heuristics are soft, not a strict algorithm.** A
  future backfill run may infer differently than another. Detection: the backfill step's own
  "report how many rows were backfilled" line already surfaces volume; a disagreement is visible
  in the row history, not hidden. Fallback: `UNMEASURED` is always the safe default when the
  heuristic doesn't clearly resolve — never a forced guess. Locus: plan.
- **R-3 — wall-clock stays permanently uninstrumented unless a future ticket adds it.** Named as
  a non-goal here, not silently deferred: `#672`'s ADR / `#666`'s rubrics get an honest
  "not instrumented" rather than a guessed figure. A future ticket adding a wall-clock column is
  its own schema change, not owed to this one. Locus: spec.
- **R-4 — the snapshot doc goes stale between release boundaries.** Detection: `#672`/`#666`
  citing a snapshot whose `rows_considered` count is far below the live ledger's. Fallback: the
  refresh step is named explicitly in the Archetype-gradient procedure; a monthly cadence (the
  same review that reads the Audit render) is the natural trigger, not a new standing loop.
  Locus: plan.

## Rejected alternatives

- **A new sibling skill instead of extending `spend-audit`.** Rejected — Resolution 3.
- **A wall-clock ledger column.** Rejected — Resolution 4; a second schema/contract change this
  ticket never authorized, and no instrument exists for it today.
- **Folding `pr-opened` into the `pr-shipped` outcome class.** Rejected — Resolution 2.
- **A migration SCRIPT for the one-row ledger.** Rejected — Resolution 6; write-once code with
  no second caller, disproportionate to a two-line hand-edit disclosed in the build's own
  Findings/PR body.
- **Inserting `archetype` mid-schema (after `seat`, say) instead of appending at the end.**
  Rejected — appending minimizes positional churn on the seven existing columns and matches how
  the schema grew once before (lld-0018's `ref`/`tokens_source` additions).
- **A `note`-shaped free-text field for archetype instead of a closed enum.** Rejected — the
  family's own no-blended/no-free-text-narrative-column law (lld-0018 Resolution 2's rejected
  alternatives, same reasoning): a closed set stays comparable across rows; free text would
  invite narrative the validator can't check.
- **A SPEC or ADR for this change.** Rejected — acceptance is already checkable from the ticket +
  the locked IDR; no hard-to-reverse fork was resolved (same routing test lld-0018/lld-0020 both
  already applied).

## Agent verification

Per `docs:agent-harness-rules` and gh#673's own acceptance criterion, the assert layer is the
payload: **new harnesses this build creates** — `validate.py`/`trend.py`/`archetype_gradient.py`
selftests (negative + reverse controls, per `.claude/rules/scripts.md`), plus the live
missing-flag and write-refusal checks (Acceptance 4-6). **Existing instruments covering the
rest** — `release_gate.py authorkit` (G4 runs all three selftests; G7 the evals suite; G10
README/version), `doc_lint.py` on this LLD. **Fresh-context checker:** `harness:skill-checker` on
the edited `SKILL.md` (semantic edit). **Human/judgment layer, stated as such:** whether a given
archetype/outcome-class multiplier, once real `measured` data exists, is itself worth acting on
(a re-cadence/retire decision) is the monthly review's own judgment over the snapshot, never a
script verdict — the same posture lld-0018 Resolution 5 already took for `verdict`, extended one
layer up to the multiplier table.
