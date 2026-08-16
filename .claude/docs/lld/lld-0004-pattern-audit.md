---
doc-type: lld
id: lld-0004-pattern-audit
status: draft
version: 0.3.0
date: 2026-08-15
owner: kim.granlund
spec: none — issue #257 (original body + 2026-08-15 design-refinement comment) is the upstream contract
ticket: nonoun-plugins#257
---
# LLD — pattern-audit: instructions in, structured match dataset out (issue #257)

*Amended 2026-08-16 (v0.3.0), executing the deferred Composition-contract wiring (issue #286) —
PR #288's review deferred a real gap here as its F2 finding: pattern-audit's own procedure step
2 states its compiled probes so a live user can veto a bad translation before the scan runs, but
an `overhaul-planning`-composed call is frequently unattended (a dispatched build, a batched
drain) with no one to veto. Ruling: the composed call never pauses for a veto — it states the
compiled probes and the resulting dataset's verdict line in the plan doc's own Phase 0
measurements instead, so a human reviews the compilation there, after the fact, rather than
vetoing it before the fact. Risk 1's fallback gains this composed-call branch below. The
Interfaces "Composition contract with overhaul-planning" section is marked REALIZED — this build
(issue #286) landed the (a)–(f) edit list this section had deferred.*

**The four rulings, head-first:**

1. **Output schema:** a flat match dataset — per-match `id / file / line / col / match /
   context / kind`, top-level `target / probes / files_scanned / matches / totals` — emitted
   deterministically by the script; the skill's optional judgment layer ANNOTATES each record
   with `verdict` + `reason` (same ids, a superset, never a mutation). Full shape in Data.
2. **Instruction format: BOTH, via the family's measure-then-judge split.** The SCRIPT accepts
   only literal, labeled regex + glob probes (deterministic, selftest-able). The SKILL accepts
   either a literal pattern or a natural-language instruction and COMPILES it into probes —
   asking interactively when the instruction is omitted or ambiguous (the ticket's own
   acceptance wording) — then optionally judges matches against the instruction's intent.
   Natural language never reaches the script; regex never has to be typed by the user.
3. **Command wrapper: YES** — `commands/pattern-audit.md`, identical-name wrapper production,
   read-only (`mutates: false`, `confirm: none`), body verbatim in the siblings' three-line
   "this wrapper adds nothing" shape. Spec in Interfaces, key-for-key on
   `authorkit/commands/bloat-audit.md`.
4. **Composition contract: ADD a conditional fifth instrument to overhaul-planning Phase 0 —
   replaces NONE of the four.** naming-audit, bloat-audit, check-routing, and surface_map each
   measure a fixed domain axis; pattern-audit is the parameterized slot for campaign-specific
   sweeps that today force a bespoke one-off script. Wiring overhaul-planning is a LATER,
   separately filed ticket (its exact edit list is enumerated in Interfaces; filing it is
   acceptance predicate 8); this build never touches overhaul-planning.

Two boundary rulings the ticket's open questions demanded:

- **pattern-audit is a genuinely distinct fourth tool, NOT a generalization of surface_map.**
  surface_map's output is a typed relation graph (mention/preload/script edges) built from
  frontmatter parsing, `skills:` preload-block extraction, and partition reconciliation —
  domain semantics no regex/glob instruction can carry. The only surface_map sub-feature a
  pattern sweep could reproduce is the weak KEBAB_TOKEN dangling-reference scan
  (`surface_map.py:31`); the reconciliation and family-matrix logic is unreachable.
  surface_map stays whole.
- **Not a make-script pattern either, but adjacent:** make-script mints PERMANENT per-task
  scripts with selftests. pattern-audit owns the AD-HOC sweep where minting a script is pure
  overhead. The skill's procedure states the ratchet explicitly: an instruction that recurs
  graduates to `harness:make-script` — pattern-audit must never become a shadow home for
  standing checks.

## Components

New members, all under `authorkit/` (placement per Kim's 2026-08-15 ruling on #257 — third
audit-family sibling, same deterministic-measure/skill-judgment split):

### `skills/pattern-audit/SKILL.md`

Frontmatter mirrors the siblings key-for-key (`authorkit/skills/bloat-audit/SKILL.md` lines
1–21, `authorkit/commands/bloat-audit.md` lines 6–8 are the precedent): `kind: skill`,
`author: kim`, `created/last_updated: <build date>`, `disable-model-invocation: false`,
`user-invocable: false`, `allowed-tools: Read, Glob, Grep, Bash(python3 */scripts/scan.py *)`.
No `requires` — it leans on no doctrine sibling.

Description carries the fences (the routing surface): use for sweeping a repo/corpus for an
arbitrary caller-supplied pattern or instruction and producing a structured match dataset a
downstream step consumes. NOT for naming conformance (naming-audit), NOT for
verbosity/busy-work (bloat-audit), NOT for sweeps over RETIRED estate names — a rename wave's
known old handles, found or fixed (fix-old-names owns that object end to end, including
read-only "find every stale reference" asks), NOT for artifact-graph/partition analysis
(harness:plan-plugin-split), NOT for a check that should become a permanent script
(harness:make-script). The fix-old-names boundary is cut on the OBJECT (rename-provenance
handles vs. an arbitrary pattern with no rename provenance), never on mutation —
fix-old-names' own suite triggers on read-only finds (its t05/t08).

Procedure (the judgment layer, ~6 steps, sibling-shaped):

1. Resolve the instruction. Given as a param → use it. Omitted → ask: what to find, where
   (subtree/glob), and what counts as a false positive.
2. Compile the instruction into one or more labeled probes (`LABEL=REGEX` + optional globs).
   A literal regex passes through as a single probe. A natural-language instruction may fan
   out to several labeled probes; state the compilation in one line before running so the
   user can veto a bad translation.
3. Run `python3 <this skill>/scripts/scan.py --target <path> --pattern <LABEL=REGEX>
   ... --json` — the `<this skill>` path form is the sibling-parity choice, matching both
   audit siblings' own procedure text (`bloat-audit/SKILL.md` step 2, `naming-audit/SKILL.md`
   step 2), chosen over `${CLAUDE_PLUGIN_ROOT}` for consistency within the family. Never
   re-derive matches in prose; never grep by hand what the script measures.
4. Judgment overlay (only when the instruction was natural-language, or the user asks):
   annotate each match record with `verdict: hit | false-positive` and a one-line `reason`,
   citing the `context` field — never delete records, never renumber ids.
5. Hand the dataset (raw or judged) to whatever the caller names next — review, bulk edit,
   migration, an overhaul-planning Phase 0 row. This skill never mutates target files.
6. Recurrence ratchet: the same instruction asked twice → recommend `harness:make-script`.

### `skills/pattern-audit/scripts/scan.py`

Deterministic sweep, sibling anatomy (module docstring with usage + exit codes, `analyze()`
pure of argv concerns, `main()`, `selftest`). Flag-first invocation, matching the family form
(`validate.py` and `measure.py` docstrings — both flag-first; a deliberate, cited deviation
from script-writing-rules' positional-first default):

```
scan.py --target PATH --pattern [LABEL=]REGEX [--pattern ...]
        [--glob GLOB ...] [--context N] [--json]
scan.py selftest
```

- Exit tri-state, family-consistent: 0 = scanned, no matches; 1 = matches found; 2 = usage
  error, target missing, invalid regex, or no files survived filtering.
- Non-`--json` output leads with the normative verdict line (script-writing-rules §Anatomy's
  `name · verdict · counts` shape), pinned exactly:
  `pattern-audit scan · MATCHES · N matches / M files` (verdict token `MATCHES` | `CLEAN`) —
  followed by per-match display lines. No consumer parses the display lines; the verdict line
  and `--json` are the contract surfaces. (The siblings' em-dash headers predate the
  normative shape; the new script follows the norm, a stated deviation from family practice.)
- Default corpus: every file under target, pruning `SKIP_DIRS = {.git, node_modules, dist,
  .claude-plugin, .refactor-attic, .claude/worktrees}` and binary files (null-byte sniff on
  the first 8KB). `--glob` (repeatable) narrows.
- `--pattern` repeatable; `LABEL=` prefix optional (default label `match`) and plumbs through
  to each record's `kind` — one run can carry several named probes.
- Matching is per-line `re.finditer`; `line`/`col` 1-based; `context` is the matched line, or
  a `±N`-line block under `--context N`.
- `id`: `m001…`, assigned in (file-sorted, line-sorted, col-sorted) order — stable across
  reruns of an unchanged tree, so the judged overlay and any downstream diff can key on it.
- Selftest fixtures (the counters must bite): positive — a planted token is found with correct
  file/line/kind; reverse — a clean tree exits 0 with zero matches; label plumbing —
  `LABEL=` lands in `kind`; multi-probe — two probes partition `totals.per_kind`; glob
  narrowing excludes an out-of-glob hit; skip-dir + binary pruning; invalid regex → exit 2,
  never a traceback (validate.py's #252 fail-clean precedent); id stability across two runs;
  verdict-line shape asserted on the non-`--json` path.

### `commands/pattern-audit.md` — spec in Interfaces.

### `skills/pattern-audit/evals/evals.json`

Trigger cases (≥6): "Sweep the repo for every occurrence of X and give me a dataset", "Find
all places matching this regex and list file/line/context", "Build a structured list of every
TODO-style marker under src/", "Where do we still reference <token>? I need the list, don't
change anything" (where <token> carries no rename provenance), "Collect every match for this
pattern so a later step can bulk-edit them", "Scan this corpus per these instructions and
output JSON matches".
No-trigger fences (owners in comments): naming conformance → naming-audit; verbosity →
bloat-audit; "Sweep .claude/ for stale plugin handles but don't change my ADRs" (fix-old-names
t08, quoted verbatim) → fix-old-names; partition/gap map → plan-plugin-split; "make this
check a permanent CI script" → make-script; "rename this variable across the codebase" → not
this plugin (mutation ask).

### Sibling fence edits (same change, per the descriptions-are-the-routing-surface invariant)

One reciprocal n-case each in `naming-audit`, `bloat-audit`, and `fix-old-names` evals,
disjoint from each sibling's own trigger space: naming-audit and bloat-audit get "Sweep the
repo for every match of this caller-supplied regex and give me the dataset" → `no-trigger`,
comment `owner: pattern-audit`; fix-old-names gets "Collect every occurrence of this
arbitrary pattern — it's not a retired name, just a string I care about — as a JSON dataset"
→ `no-trigger`, `owner: pattern-audit` (the rename-provenance cut, so its t05/t08 read-only
finds stay unambiguously its own).

### Ledger/manifest edits

`authorkit/README.md` member table + footer ledger row; `authorkit/.claude-plugin/plugin.json`
version bump (the update cache key); `authorkit/naming.manifest.json` gains
`{"canonical": "pattern", "plural": "patterns", "banned_aliases": []}` in `object_vocab`
(`audit` is already in its `process_lex`), so the new names conform under BOTH manifests —
the estate-local one its validator loads by default, and the repo-root one release_gate's
G12 pins explicitly (`release_gate.py` G12: `--manifest <repo-root>/naming.manifest.json
--scope grammar`). The root manifest already carries `pattern`; the local one did not.

### Rulings that earned no ADR (recorded here, per the ADR-default-no discipline)

- **Script name `scan.py`, never `measure.py`:** overhaul-planning already grants
  `Bash(python3 */scripts/measure.py *)` (its allowed-tools, live today); reusing bloat-audit's
  script name would let pattern-audit's script silently ride existing scoped grants
  estate-wide. A distinct name keeps every grant scoped to intent. Not a fork — no
  alternative was load-bearing once the collision was seen.
- **No `references/` folder in v1**, breaking family symmetry with the two siblings' 
  REPORT-TEMPLATE.md: the JSON dataset IS the deliverable; a report template would be
  manufactured process. Revisit only if a real consumer asks for a rendered report.

## Interfaces

### Skill ↔ script boundary (the family's load-bearing line)

The script is deterministic and instruction-blind: literal probes in, dataset out, selftest
provable. All interpretation — NL→probe compilation, false-positive verdicts, downstream
handoff — lives in the skill body. This is bloat-audit's measure-then-judge split verbatim,
and it is what keeps the instruction-format answer "BOTH" without making the script's
selftest depend on model judgment.

### Command wrapper (key-for-key on `authorkit/commands/bloat-audit.md`)

```yaml
---
name: pattern-audit
kind: command
description: Sweep a repo or corpus for a pattern or instruction (given as an argument, or gathered interactively) and emit a structured dataset of matches for downstream work.
argument-hint: "[pattern-or-instruction] [path-to-target]"
author: kim
created: <build date>
last_updated: <build date>
wraps: pattern-audit
requires: [pattern-audit]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/scan.py *)
---
```

Body (three lines, sibling-verbatim shape): "Invoke the pattern-audit skill against
`$ARGUMENTS` (default: the current project). Follow that skill's procedure exactly; this
wrapper adds nothing — it exists because skills are not user-invocable and sweeps are
demanded on demand."

### Grammar proof (ADR-0011)

`pattern` ∈ ObjectVocab and `audit` ∈ ProcessLex in the repo-root `naming.manifest.json` —
the manifest release_gate's G12 passes explicitly via `--manifest` — so the skill name parses
via the object-process production. The command parses via validate.py's wrapper production
(name == `wraps` target ∈ skills). The estate-local `authorkit/naming.manifest.json` lacked
`pattern` until this build's registration row (Components › Ledger/manifest edits) — without
it, a bare `validate.py --target authorkit` (which resolves the manifest from the target)
would flag the new names by the same mechanism that already flags `overhaul-*` there. No
exemption entry needed; with the registration row, both names conform from day one under
both manifests.

### Composition contract with overhaul-planning (REALIZED 2026-08-16, issue #286 — was deferred)

Phase 0 gained a conditional step 3: *"When the campaign's charter names a pattern none of the
four instruments owns (a superseded constant still cited, a deprecated frontmatter field, a
banned phrase), run `authorkit:pattern-audit` with that instruction — never hand-author a
one-off sweep script."* It replaces nothing: steps 1–2 keep their fixed axes
(`overhaul-planning/SKILL.md` Phase 0 has exactly two numbered steps, four instruments, before
this build's step 3). The wiring ticket's edit list, as landed (a)–(f): (a) the Phase 0 step
text — plus the composition-veto-substitute ruling this amendment's header names; (b)
`pattern-audit` added to overhaul-planning's `requires`; (c) `Bash(python3 */scripts/scan.py *)`
added to its allowed-tools; (d) reciprocal fences — overhaul-planning's suite gained n12 (a raw
sweep ask stays pattern-audit's own), pattern-audit's suite gained n07 (a campaign-plan ask
stays overhaul-planning's own); (e) `/check-routing authorkit` after — neither description
changed, so this reproves no new steal opened, rather than proving a new one closed; (f)
fresh-context `wording-checker` pass on the Phase 0 semantic edit (the invariant's actual
checker for a prompt-carrying body edit, not `skill-checker` as this section's original text
named — `wording-checker` is the language-of-a-prompt-carrying-artifact critic; `skill-checker`
audits a whole SKILL.md's structure, a broader pass than this narrow body addition needed).
Blast radius as landed: 2 SKILL.md bodies (`overhaul-planning`, this LLD itself), 2 eval suites,
0 scripts — matching the estimate below exactly.

### Consumers

The dataset's contract consumer set: a human reading `--json` output, a bulk-edit/migration
step keying on `id`+`file`+`line`, and overhaul-planning Phase 0 (post-wiring). Non-`--json`
output exposes exactly one contract surface — the normative verdict line
(`pattern-audit scan · N matches / M files`); its per-match display lines are display only.

## Data

Script output (`--json`), the ticket's "structured dataset of matches":

```json
{
  "target": "/abs/path",
  "probes": [{"label": "stale-ref", "regex": "naming-rules", "globs": ["**/*.md"]}],
  "files_scanned": 412,
  "matches": [
    {
      "id": "m001",
      "file": "harness/skills/x/SKILL.md",
      "line": 41,
      "col": 7,
      "match": "naming-rules",
      "context": "the canon is harness's naming-rules (ADR-0006)",
      "kind": "stale-ref"
    }
  ],
  "totals": {"matches": 1, "files_with_matches": 1, "per_kind": {"stale-ref": 1}}
}
```

Precedent mapping, honestly drawn: `kind` follows bloat-audit's per-record labeling
(`measure.py`'s per-measurement `kind` field and named `flags`), not validate.py's `category`
(that axis routes severity between grammar/structural, not probe identity); `context` ≙
bloat-audit's `snippet` (`measure.py:136`); `totals` block ≙ bloat-audit's `totals`
(`measure.py:233`); `probes` echoes the compiled instruction so the dataset is
self-describing (reproducible without the chat that produced it). The per-record `id` is a
NEW invention — no family precedent carries one — justified by downstream keying: the judged
overlay and any bulk-edit/diff step need a stable handle that survives reruns. Judged
overlay (skill-added, optional): each record gains `"verdict": "hit" | "false-positive"` and
`"reason": "<one line>"`; ids and record count are invariant under judgment. No numeric
confidence field — verdict + cited reason is the estate's findings idiom; a float nobody
calibrates is decoration.

## Build manifest

| # | Path | Action |
|---|---|---|
| 1 | `authorkit/skills/pattern-audit/SKILL.md` | create (via `/make-skill` where installed) |
| 2 | `authorkit/skills/pattern-audit/scripts/scan.py` | create, selftest per Components |
| 3 | `authorkit/skills/pattern-audit/evals/evals.json` | create |
| 4 | `authorkit/commands/pattern-audit.md` | create (Interfaces spec verbatim) |
| 5 | `authorkit/skills/{naming-audit,bloat-audit,fix-old-names}/evals/evals.json` | edit: one reciprocal n-case each (wording per Components › Sibling fence edits) |
| 6 | `authorkit/README.md` + `authorkit/.claude-plugin/plugin.json` | edit: member row, ledger row, version bump |
| 7 | `authorkit/naming.manifest.json` | edit: register `pattern` in `object_vocab` |

Explicitly NOT in this build: any overhaul-planning edit (the filed follow-up ticket,
predicate 8); any harness edit; any ADR (no fork was resolved — every ruling follows an
established pattern; the two non-decisions are recorded in Components).

## Acceptance (build gate — checkable predicates, all must pass before "done")

1. `python3 authorkit/skills/pattern-audit/scripts/scan.py selftest` → exit 0 (covers
   manifest row 2's mechanics: planted-fixture field round-trip, label plumbing, glob/
   skip-dir/binary pruning, invalid-regex fail-clean, id stability, verdict-line shape —
   asserting the exact pinned string `pattern-audit scan · MATCHES · N matches / M files`).
   Row 1 (SKILL.md) is covered by predicates 2, 6, and 7, not by this selftest.
2. `python3 harness/scripts/release_gate.py authorkit` → green — this includes G12 (naming
   grammar under the repo-root manifest, `--scope grammar`), G7 (eval-suite schema for rows
   3 and 5), G4 (selftest sweep), and G10 (README-ledger/manifest version match, row 6).
3. `python3 authorkit/skills/naming-audit/scripts/validate.py --target authorkit --manifest
   naming.manifest.json --scope grammar --json` (run from repo root — G12's own invocation)
   → `grammar_errors` contains no entry naming `pattern-audit`; total `grammar_errors`
   count 0 (today's measured count under the root manifest: 0; structural baseline: 9,
   informational, non-gating).
4. Row 7 landed (the estate-local manifest registration): `python3
   authorkit/skills/naming-audit/scripts/validate.py --target authorkit --scope grammar
   --json` (bare — resolves the LOCAL manifest from the target) → `grammar_errors` count
   stays at its measured pre-build baseline of 3 (`fix-old-names`, `overhaul-execute`,
   `overhaul-planning` — all pre-existing) and contains no entry naming `pattern-audit`
   (skill or command).
5. Row 5 landed: `grep -l "owner: pattern-audit"` matches all three sibling
   `evals/evals.json` files, and each new case is `"expect": "no-trigger"`.
6. Fresh-context skill-checker pass on the new SKILL.md and the command body (the
   semantic-edit invariant) — verdict recorded in the build's handback.
7. `/check-routing authorkit` after the descriptions land → ZERO steals in either direction
   between pattern-audit and naming-audit/bloat-audit/fix-old-names (absolute, no baseline
   needed — the skill is new, so any steal touching it is new). Where authorkit is not
   installed to run check-routing, `eval_check` proves suite validity only — the steal count
   is then a deferred predicate, recorded as open in the build's handback, never waived.
8. A follow-up GitHub Issue exists for the overhaul-planning wiring, links this LLD, and
   carries the (a)–(f) edit list from Interfaces verbatim.
9. This LLD passes `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0004-pattern-audit.md`.

## Risks

1. **Generic regex over-match noise** (surface_map's own KEBAB_TOKEN over-fire precedent,
   lld-0001 Risk 4). Detection: a judged dataset where false-positives outnumber hits.
   Fallback: the skill states its probe compilation before running so a bad translation is
   vetoed pre-scan; on a noisy result, recompile the probe — never hand-filter downstream.
   **Composed-call branch (added 2026-08-16, issue #286):** when pattern-audit is invoked from
   inside `overhaul-planning`'s Phase 0 step 3, the caller is frequently unattended and the
   pre-scan veto has no one to answer it — the substitute states the compiled probes and the
   resulting verdict line in the plan doc's Phase 0 measurements instead, so the veto becomes a
   post-hoc plan-doc review rather than a pre-scan pause; a noisy result surfaces there as a
   named finding, recompiled on the campaign's next pass rather than hand-filtered.
2. **Routing steals against near neighbors** — fix-old-names ("Find every reference to a
   retired skill name" is its live t05 trigger), naming-audit, bloat-audit,
   plan-plugin-split. Detection: acceptance predicate 6's steal count goes nonzero, or a
   session routes a retired-handle sweep to pattern-audit. Fallback: the object-cut fence
   (rename provenance vs. arbitrary pattern) is already in the description and both suites;
   a live steal means the fence wording failed — repair the description and re-run
   check-routing, per the routing-surface invariant.
3. **Shadow-home drift**: recurring sweeps quietly staying in pattern-audit instead of
   graduating to make-script. Detection: the same instruction appearing in two sessions'
   datasets. Fallback: the procedure's step-6 ratchet + the make-script fence in both the
   description and the eval suite; a recurrence spotted late still hands off to make-script
   with the existing dataset as its fixture seed.
4. **Deferred wiring drifts stale**: overhaul-planning's Phase 0 may change before the
   wiring ticket runs, staling the (a)–(f) snapshot. Detection: the wiring ticket's
   executor diffs this doc's snapshot against Phase 0's live text at claim time and finds a
   mismatch. Fallback: the ticket re-reads Phase 0 at execution (stated in Interfaces); the
   snapshot here is marked as such, never authoritative.
