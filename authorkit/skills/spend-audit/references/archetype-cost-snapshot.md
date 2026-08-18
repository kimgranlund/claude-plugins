# Archetype cost snapshot — measured per-archetype orchestration cost gradient

**Stable citable path:** `authorkit/skills/spend-audit/references/archetype-cost-snapshot.md`
(gh#673, lld-0021). This is a GENERATED data snapshot, not authored prose — regenerate it at
every authorkit release boundary (`CLAUDE.md`'s "sources flow outward" invariant, applied here:
this file is the snapshot, `.claude/ops/spend-ledger.csv` plus
`scripts/archetype_gradient.py` are the source of record) via:

```
python3 authorkit/skills/spend-audit/scripts/archetype_gradient.py .claude/ops/spend-ledger.csv
```

Cited by: `#672`'s Track A ADR (native teams vs. fleet), `#666`'s per-archetype rubric pack's
cost lines, `teamwork:fleet-rules`' idr-0010 pricing bullets (§4).

## What this measures

`.claude/ops/spend-ledger.csv` attributes every new firing row to one of the estate's eight
orchestration archetypes (`archetype` column, REQUIRED on new rows — #666's taxonomy: A1 solo ·
A2 unnamed sync fan-out · A3 named background/teammate seats · A4 fleet terminal seats · A5
forked intake · A6 scheduled routines + `/goal` loops · A7 Workflow scripts · A8 `/batch`), or
the literal `UNMEASURED` for a best-effort retroactive backfill row whose archetype is genuinely
ambiguous. `archetype_gradient.py` computes, per archetype (excluding the A1 baseline itself)
and per **outcome class**, the ratio of that archetype's mean MEASURED tokens to A1's mean
MEASURED tokens for the same class — **never a guessed multiplier**: a cell computes only when
both sides carry at least one `tokens_source: measured` row for that exact outcome class;
otherwise it reports `UNMEASURED` honestly.

**Per-equivalent-outcome normalization (defined here, gh#673 — it existed nowhere before this
ticket):** kept simple and stated against the ledger's existing closed `outcome` enum, no new
column —

| Outcome class | Ledger `outcome` values it covers | Denominator meaning |
|---|---|---|
| `pr-shipped` | `pr-merged` | cost per PR that actually shipped |
| `record-minted` | `acted` | cost per non-PR artifact produced (a queued item, a report, a filed ticket) |

Every multiplier below states which of these two denominators it normalizes against. A firing
whose `outcome` is `pr-opened`/`no-op`/`blocked`/`failed` is out of scope for this table (neither
class claims it) — it still counts toward `.claude/ops/spend-ledger.csv`'s own worth-firing
audit, just not this per-outcome cost comparison.

**Wall-clock is a separate, currently-uninstrumented axis.** The ledger schema carries no
wall-clock column (a deliberate non-goal of this ticket — see lld-0021's Rejected alternatives);
every archetype/outcome-class wall-clock cell below reads `UNMEASURED (not instrumented)` by
construction. The one wall-clock figure this snapshot ever carries is the anchor immediately
below, cited textually, never computed from ledger rows.

## Anchor — gh#265 (external citation, not computed from this ledger)

> **#265** — solo-in-one-context vs. the real `chore-lead` seat chain (a coordinator-hop
> instance): **1.92× output tokens, 3.6× wall-clock**, for equivalent outcome quality (single
> trial, one repo state, 2026-08-16). Cited here as the estate's sole prior cost measurement and
> a sanity anchor for what a coordinator hop can cost — **never blended into the computed table
> below**, and never treated as a stand-in multiplier for any specific archetype/outcome-class
> cell that is itself `UNMEASURED`.

## Snapshot — generated 2026-08-18 from `.claude/ops/spend-ledger.csv` (1 row)

```
archetype-gradient · 1 rows considered · baseline A1
  anchor: #265 — tokens 1.92x / wall-clock 3.6x (solo-in-one-context vs. the real chore-lead seat chain (a coordinator-hop instance)) — external citation, not computed
  A2 (unnamed sync fan-out — an unnamed Agent-tool/fork dispatch, synchronous return) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A2=0), wall-clock UNMEASURED (not instrumented)
  A2 (unnamed sync fan-out — an unnamed Agent-tool/fork dispatch, synchronous return) / record-minted: tokens UNMEASURED (n_baseline=0, n_A2=0), wall-clock UNMEASURED (not instrumented)
  A3 (named background/teammate seats — SendMessage-routed, mailbox delivery) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A3=0), wall-clock UNMEASURED (not instrumented)
  A3 (named background/teammate seats — SendMessage-routed, mailbox delivery) / record-minted: tokens UNMEASURED (n_baseline=0, n_A3=0), wall-clock UNMEASURED (not instrumented)
  A4 (fleet terminal seats — joined via team-scaffolding/fleet-bootstrap, marshal-coordinated) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A4=0), wall-clock UNMEASURED (not instrumented)
  A4 (fleet terminal seats — joined via team-scaffolding/fleet-bootstrap, marshal-coordinated) / record-minted: tokens UNMEASURED (n_baseline=0, n_A4=0), wall-clock UNMEASURED (not instrumented)
  A5 (forked intake — a `context: fork` command (file-bug/file-feature/build-feature)) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A5=0), wall-clock UNMEASURED (not instrumented)
  A5 (forked intake — a `context: fork` command (file-bug/file-feature/build-feature)) / record-minted: tokens UNMEASURED (n_baseline=0, n_A5=0), wall-clock UNMEASURED (not instrumented)
  A6 (scheduled routines + `/goal` loops — CronCreate-armed or loop-driven) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A6=0), wall-clock UNMEASURED (not instrumented)
  A6 (scheduled routines + `/goal` loops — CronCreate-armed or loop-driven) / record-minted: tokens UNMEASURED (n_baseline=0, n_A6=0), wall-clock UNMEASURED (not instrumented)
  A7 (Workflow scripts — `harness/workflows/*.js`) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A7=0), wall-clock UNMEASURED (not instrumented)
  A7 (Workflow scripts — `harness/workflows/*.js`) / record-minted: tokens UNMEASURED (n_baseline=0, n_A7=0), wall-clock UNMEASURED (not instrumented)
  A8 (`/batch` — decompose + one subagent per unit + PR-per-unit) / pr-shipped: tokens UNMEASURED (n_baseline=0, n_A8=0), wall-clock UNMEASURED (not instrumented)
  A8 (`/batch` — decompose + one subagent per unit + PR-per-unit) / record-minted: tokens UNMEASURED (n_baseline=0, n_A8=0), wall-clock UNMEASURED (not instrumented)
```

**Honest reading of this first snapshot: every computed cell is `UNMEASURED`.** The ledger
carries exactly one row (`#624`'s own build-firing seed, itself migrated to `UNMEASURED`
archetype at this schema change — its own dispatch shape was genuinely ambiguous across the
fork/coordinator/named-seat hops it crossed, never guessed), and it has no `tokens_source:
measured` value at all. This is the EXPECTED first-emit state (gh#673's own Scope/Open note:
"expected that several [archetypes] start UNMEASURED") — not an instrument failure, and not
silently hidden: the close-out convention (`SKILL.md`) now requires every new firing's `--seat`
to also name `--archetype`, so this table sharpens as real `measured` rows accumulate. Re-run the
generator at the next authorkit release boundary and diff this snapshot against the new one —
the diff IS the signal of whether the instrument has been found.
