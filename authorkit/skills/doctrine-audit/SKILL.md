---
name: doctrine-audit
kind: skill
description: >
  Sweep an estate for doctrine drift: a canon rule a dependent violates,
  omits, or paraphrases away from. Reads typed edges (verbatim-line |
  ledger-sync | vocab-term | judgment) from doctrine.manifest.json. Use
  when the user asks to audit doctrine drift, check a forge template
  against the standard it invokes, verify a ledger row matches
  its file, or find bodies (agent/skill) using a stale tool name/term instead of
  canon (the vocab-term edge). Read-only. NOT naming (naming-audit), NOT busy-work
  (bloat-audit), NOT an unmanifested pattern (pattern-audit), NOT
  menu rent (attention-audit), NOT an overhaul plan (overhaul-planning),
  NOT the batch form (estate-audit-agent), NOT a one-off script
  (make-script), NOT a retired handle from a rename wave (fix-old-names).
author: kim
created: 2026-08-16
last_updated: 2026-08-19
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/sweep.py *)
---

# doctrine-audit

Deterministic sweep lives in `scripts/sweep.py` — run it; never re-derive matches in
prose or hand-grep what the script measures. This skill's job is locating the manifest,
running the sweep, and rendering the judgment layer on top — same shape as naming-audit's
own split between `validate.py` (mechanics) and the skill (judgment).

## Procedure

1. Locate the target's `doctrine.manifest.json` (estate root, or a path the caller names).
   If absent, stop and offer to seed one — do not audit an estate with no doctrine edges
   declared. This is a SEPARATE manifest from `naming.manifest.json` (ADR-0011 D1: that one
   stays single-purpose for naming grammar) — never conflate the two files or their schemas.
2. Sanity-check the manifest's shape first: `python3 <this skill>/scripts/sweep.py validate
   --manifest <path>`. A shape failure (unknown edge type, missing required field per type)
   stops here — report it plainly, never sweep a malformed manifest.
3. Run the sweep: `python3 <this skill>/scripts/sweep.py --root <estate> [--manifest <path>]
   --json`. The dataset of record is this call's JSON output — per-finding `edge/type/file/
   reason/severity`, a `judgment_queue` (edge + owning checker + status, never mechanically
   checked), and `unrecovered_findings` (if the manifest records a known gap — pass it
   through verbatim, never silently drop it).
4. Interpret:
   - **Mechanizable findings** (`verbatim-line`, `ledger-sync`, `vocab-term`): cite the exact
     edge id, file, and reason from the JSON. A `verbatim-line` finding means the dependent's
     exact text diverges from canon, even a close paraphrase counts — the edge type exists
     precisely to catch drift a looser human read would wave through.
   - **Judgment edges**: report the edge and its `owning_checker` verbatim as "queued, not
     built" — this instrument is read-only like its four siblings; dispatching the named
     checker is always the caller's own decision, never this skill's.
   - **`unrecovered_findings`**: if present, state the gap honestly in the same report
     section as the findings — never omit it, never fabricate entries to fill it.
5. Render a report: verdict line first (the sweep's own `pattern-audit`-style summary
   string), then findings grouped by edge, then the judgment queue, then any unrecovered-gap
   note. Never assert a violation the JSON output does not contain.
6. Hand fixes to whatever the caller names next (the edge's own dependent file, or
   `overhaul-planning` if this ran as its composed Phase-0 doctrine sweep). This skill never
   mutates target files.

## Edge types

| Type | What it checks | Mechanizable |
|---|---|---|
| `verbatim-line` | A dependent must (`mode: require`) or must not (`mode: forbid`) contain an exact pattern from canon | Yes |
| `ledger-sync` | A ledger row's named path still matches what actually exists on disk | Yes |
| `vocab-term` | Dependents use the canonical term for one concept, never a banned alias | Yes |
| `judgment` | No lexical anchor — needs a human/checker call | No — routed, reported "queued, not built" |

## Failure branches

- No `doctrine.manifest.json` found → say so plainly; offer to seed one (own schema, not a
  naming.manifest.json section — Kim's 2026-08-16 ruling). Never invent edges from memory.
- `sweep.py validate` reports shape errors → stop; report them verbatim; never sweep a
  malformed manifest partially.
- `sweep.py --root` exits 2 (root missing, manifest missing/malformed) → report the usage
  error verbatim; never read a usage error as a false CLEAN.
- A `judgment` edge with no `owning_checker` named → that's a manifest shape defect
  (`sweep.py validate` catches it); fix the manifest, don't guess a checker.

Done when the report (findings + judgment queue + any unrecovered-gap note) is delivered
with its verdict line quoted, and the target tree is unchanged.
