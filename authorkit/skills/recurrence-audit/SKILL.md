---
name: recurrence-audit
kind: skill
description: >
  Instrument IDR-0006's estate success measures — the incident-recurrence rate (primary) and
  the /check-routing routing-eval pass-rate trend (secondary). Walks the estate's incident
  ledger (gate checks, doctrine bullets, fixtures citing an incident id) for the seeded
  `LEDGER-CLASS:` convention, computes per-class recurrence live, and appends a dated trend row.
  Use for "is our incident-recurrence rate actually being measured", "walk the ledger and tell
  me which incident classes came back", "what's IDR-0006's primary measure reading this
  release", "check whether a mechanized gate or doctrine fix has recurred", "track the
  routing-eval pass-rate trend release over release". Read-only, report-only, appends the trend
  file — never rewrites doctrine or gates. NOT for the menu-rent/collision series
  (attention-audit); NOT for naming conformance (naming-audit); NOT for prose bloat
  (bloat-audit); NOT for running the routing simulation itself (harness check-routing — this
  skill only persists its output); NOT for an arbitrary caller-supplied pattern with no
  incident-class shape (pattern-audit).
author: kim
created: 2026-08-18
last_updated: 2026-08-18
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/scan.py *)
  - Bash(python3 */scripts/trend.py *)
  - Bash(gh issue *)
---

# recurrence-audit

Deterministic measurement lives in `scripts/` — the seeded-class inventory and the trend file's
append both come from a script run; a count derived in prose is a defect. This skill's job is
the live judgment layer on top: the conjunct-A `gh issue` lookup no offline script can safely
run, the per-class recurrence verdict, and honest rendering of what is (and isn't) computed yet.

The two series — incident-recurrence and routing-eval pass-rate — stay separate columns, never
collapsed into one score (the estate's own Goodhart rule, `attention-audit`'s precedent: a
blended quotient rewards deleting the fence that protects a rare-but-expensive misroute).

## The `LEDGER-CLASS:` convention (lld-0011)

A per-incident-class citation tag, additive and optional, that a doctrine bullet, gate-check
comment, or fixture gains the next time it's touched:

```
LEDGER-CLASS: <slug> | ids: #NNN[, #NNN...] | mechanized: YYYY-MM-DD
```

Plain grep-able text — no bracket syntax (this estate's `[[skill-name]]` double-bracket form is
already a cross-reference convention). Works unmodified in markdown prose, a trailing `#`/`//`
code comment, or a fixture's string value. Adoption is a process ratchet, not a retrofit sweep
this skill ever performs on its own — a citation with no tag still counts in the honest
bare-citation baseline below, it just isn't class-computable yet.

## Procedure

1. **Inventory**: `python3 <this skill>/scripts/scan.py --target <repo-root> --json` — every
   `LEDGER-CLASS:` tag, grouped by class (ids, mechanized date, citing files/lines), plus the
   bare `#NNN`-citation baseline count across `.md` files. Never hand-count what the script
   measures; never conflate the two counters (a seeded class and a bare citation are genuinely
   independent signals).
2. **Live conjunct-A check** (per seeded class from step 1 — today, honestly, this is often
   zero classes): for each id under the class, `gh issue view <id> --json createdAt,number` and
   compare `createdAt` against the class's `mechanized` date. Any id created strictly AFTER
   mechanization → conjunct A holds for that class (a new matching issue post-mechanization,
   per IDR-0006's own recurrence wording).
3. **Conjunct-B proxy**: a class carrying ≥2 distinct ids is the estate's own existing way of
   narrating recidivism (e.g. a doctrine bullet citing "#530, #546, #549 ... before a human
   caught it (#551)") — treat ≥2 ids as conjunct B's evidence. State this explicitly as a
   **proxy**, never as a literal CI-history read (no durable per-class CI record exists to query
   directly) — a disagreement a DRI review later finds routes to IDR-0006's own falsification
   path (a superseding IDR), never a silent patch here.
4. Recurrence for a class = conjunct A AND conjunct B (proxy). Write the per-class verdicts to
   a small JSON: `{"<slug>": true|false, ...}`.
5. **Routing-eval input** (secondary series): run or locate a fresh `harness:check-routing`
   pass; transcribe its printed `<passed>/<total> cases` line into `{"passed": N, "total": M}`.
   Omit entirely when no fresh run exists this cycle — never invent a number.
6. **Persist**: `python3 <this skill>/scripts/trend.py --scan <scan.json> [--recurrence
   <recurrence.json>] [--routing-report <path>] --out <repo-root>/recurrence-trend.csv` —
   appends one dated row. Zero seeded classes → `recurred_classes` reads `0` (nothing to
   check); seeded classes present but step 2–4 wasn't run this pass → `absent` (a real gap,
   not a false zero); missing routing input → its three columns read `absent`.
7. **Render**, verdict-first: seeded-class count and the bare-citation baseline (stated
   explicitly as a baseline, never mistaken for computed recurrence when it's zero), each
   seeded class's recurrence verdict with its evidence (ids + dates), and the routing pass-rate
   (or "not measured this cycle"). A flat zero seeded classes across several releases, alongside
   a growing bare-citation count, is itself a finding — the convention isn't being adopted —
   surface it rather than accept it silently.

Done when: the trend row is appended (or its columns honestly read `absent`/`0` per step 6's
rules), every seeded class's recurrence verdict is stated with its evidence, and the
bare-citation baseline is reported as exactly that — never conflated with per-class recurrence.

## Degraded modes

- Zero `LEDGER-CLASS:` tags exist anywhere yet (the expected state immediately after this skill
  ships): steps 2–4 have nothing to check; step 6 records `seeded_classes: 0`,
  `recurred_classes: 0`; the render states the convention just shipped and adoption is
  additive going forward — never reads as "the tool is broken."
- No fresh `check-routing` run this cycle: step 5 is skipped; step 6's three routing columns
  read `absent`; the report names the missing signal plainly.
- `gh` unavailable or rate-limited: step 2's live check degrades to "not verified this cycle" for
  every seeded class — recorded in the recurrence JSON as an explicit gap (a class with no
  computed verdict is never defaulted to `false`), never silently skipped.

## Composition

Reads `.claude/docs/idr/idr-0006-incident-recurrence-as-success-measure.md` for the two
measures' own definitions and falsification test; the trend file's reader is the same DRI review
IDR-0006 names (`brief-nonoun-plugins.md`'s monthly review cadence) — a human diffing rows
release over release, exactly as `attention-trend.csv` is read today.

## References

None yet — the LEDGER-CLASS convention and the recurrence definition are stated in full above
and in lld-0011; a references/ corpus would be manufactured process for a skill this size.
