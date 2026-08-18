---
doc-type: lld
id: lld-0011-recurrence-audit
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
spec: none — issue #618 (original body) is the upstream contract, descending from IDR-0006 (locked)
ticket: nonoun-plugins#618
---
# LLD — recurrence-audit: instrumenting IDR-0006's primary (incident-recurrence) + secondary (routing-eval trend) success measures

**The four open questions, ruled head-first:**

1. **Home: `authorkit`.** It already owns the trend-instrument + audit family
   (`attention-audit`, `bloat-audit`, `naming-audit`, `doctrine-audit`, `pattern-audit`,
   `estate-audit`, `repo-audit`) and the `trend.py`-appends-a-CSV-per-release pattern this
   feature reuses verbatim. `harness` was the seed's other candidate ("acceptable if the
   ledger-walk couples to release_gate") — it doesn't: the ledger walk is a plain text sweep
   over citations, no coupling to `release_gate.py`'s own internals. Ruling: authorkit, no fork.
2. **Ledger-inventory computed-or-seeded verdict: SEEDED, not fully computed today.** Grepping
   the estate for bare issue-number citations (`grep -rlE '#[0-9]{2,4}\b'`) hits 406 files — real
   citation coverage exists in volume, but it is unstructured prose (`"...before a human caught
   it (#551)"`) with no machine-extractable **class** label a script can group on. A structured
   evidence-tag convention exists in 14 files (`grep -rl '\[incident\]'`) but it is a citation-
   *confidence* tag borrowed from a different repo's harvest format (`gen-ui-kit fleet-ops
   harvest`), not a class-identifying key this estate's own ledger uses — most of its 14 hits
   are unrelated (LLM knowledge-pack provenance citations, not this repo's own incidents). **So:
   citation coverage is real but not class-taggable as-is** — this build ships Part 1, the
   ledger-seeding convention (`LEDGER-CLASS:` tag, below), plus a script that (a) inventories
   today's bare-citation baseline honestly and (b) computes real per-class recurrence for any
   citation that HAS adopted the seeded tag, starting at zero and growing as doctrine bullets/
   gate checks/fixtures adopt it going forward.
3. **Recurrence definition: BOTH conjuncts, as the seed specifies** — a new matching issue
   post-mechanization AND a gate firing red on the same class. Neither conjunct is safely
   computable *offline* by a selftest-provable script: conjunct A needs a live `gh issue`
   lookup: conjunct B needs CI history no static repo scan carries. Both stay a **live,
   judgment-layer check the SKILL body runs** (`gh issue list`/`gh issue view`), never inside
   the deterministic script — same skill/script split `pattern-audit` already established
   (script deterministic and offline-testable; interpretation/network calls live in the skill).
   Conjunct B's proxy, stated explicitly as a proxy: a class re-cited with a SECOND, later-dated
   id under the same `LEDGER-CLASS:` slug is direct evidence the class recurred badly enough
   that someone recorded it again — this is literally how the estate already narrates
   recidivism today (`fleet-rules`' own "#530, #546, #549 ... before a human caught it (#551)").
4. **Routing-eval persistence: not persisted today — this feature starts it.**
   `harness:check-routing`'s Phase 5 report (`SKILL.md` line 66-73) is a printed matrix, never
   written to disk — grep for any script writing a routing-report JSON or a routing trend CSV
   estate-wide returns nothing. This build's `trend.py` accepts an optional `--routing-report
   <path>` exactly like `attention-audit/scripts/trend.py` already does (degraded-mode parity:
   present → real numbers, absent → the literal string `absent`, never invented) — the
   producer side (turning check-routing's printed line into that JSON) is a one-line manual/
   scripted transcription documented in the SKILL procedure, not a change to check-routing
   itself (Rejected alternatives, below).

## Components

New members, all under `authorkit/`:

### `skills/recurrence-audit/SKILL.md`

Frontmatter mirrors the audit-family siblings (`bloat-audit`/`pattern-audit` precedent):
`kind: skill`, `author: kim`, `created/last_updated: 2026-08-18`,
`disable-model-invocation: false`, `user-invocable: true`,
`allowed-tools: Read, Glob, Grep, Bash(python3 */scripts/scan.py *), Bash(python3
*/scripts/trend.py *), Bash(gh issue *)`.

Description carries the fences: use for measuring IDR-0006's two success signals — per-class
incident-recurrence rate and the routing-eval pass-rate trend. NOT for the menu-rent/collision
series (`attention-audit`), NOT for naming conformance (`naming-audit`), NOT for prose bloat
(`bloat-audit`), NOT for running the routing simulation itself (`harness:check-routing` — this
skill only persists its output).

Procedure (skill = judgment + live layer over the deterministic script):

1. `python3 <this skill>/scripts/scan.py --target <repo-root> --json` — inventories every
   `LEDGER-CLASS:` tag (grouped by class: ids, mechanized date, citing files) plus the bare
   `#NNN`-citation baseline count in markdown docs. Never hand-count what the script measures.
2. For each seeded class in the scan (today: likely zero — this is the honest baseline), run
   the live conjunct-A check: `gh issue view <id> --json createdAt,number` for each id under
   the class, compare against the class's `mechanized` date — any id created strictly after
   → conjunct A holds for that class. Conjunct B: the class carries ≥2 distinct ids (the
   re-citation proxy, Ruling 3). Recurrence = A AND B. Write the per-class verdicts to a
   small JSON (`{"<slug>": true|false, ...}`).
3. `python3 <this skill>/scripts/trend.py --scan <scan.json> --recurrence <recurrence.json>
   [--routing-report <path>] --out <repo-root>/recurrence-trend.csv` — appends one dated row.
   Missing `--recurrence` (seeded classes exist but the live step above wasn't run this pass)
   records `absent`, matching zero-seeded classes recording `0` (nothing to check, not a
   missing signal — the same present/absent honesty `attention-audit`'s own `trend.py` applies).
4. Routing-eval input: transcribe `check-routing`'s own printed `<passed>/<total> cases` line
   into `{"passed": N, "total": M}` (by hand, or the caller's own wrapper) and pass it as
   `--routing-report`; omit it entirely when no fresh `check-routing` run exists this cycle.
5. Render: seeded-class count, recurred-class count (or "not yet computed"), bare-citation
   baseline, routing pass-rate — verdict-first, citing the trend row just appended.

Done when: the trend row is appended (or its columns honestly read `absent`), every seeded
class's recurrence verdict is stated with its evidence (ids, dates), and the bare-citation
baseline is reported as exactly that — a baseline, never mistaken for per-class recurrence.

### `skills/recurrence-audit/scripts/scan.py`

Deterministic, offline, selftest-provable — sibling anatomy (module docstring, `analyze()` pure
of argv, `main()`, `selftest`, exit tri-state). Recognizes the seeded tag:

```
LEDGER-CLASS: <slug> | ids: #NNN[, #NNN...] | mechanized: YYYY-MM-DD
```

grep-able plain text (no bracket syntax — this estate's `[[skill-name]]` double-bracket form is
already a cross-reference convention; a second bracket-shaped marker would collide visually).
Works unmodified inside markdown prose, a Python/JS trailing `#`/`//` comment, or a fixture's
string value — it's a text pattern, not bound to any one comment syntax.

```
scan.py --target PATH [--json]
scan.py selftest
```

- Exit tri-state: 0 = scanned, zero seeded `LEDGER-CLASS:` entries (bare-citation baseline
  only); 1 = at least one seeded class found; 2 = usage error (target missing, or nothing
  survived the skip-dir/binary filter).
- Skip-dirs identical to `pattern-audit/scripts/scan.py`: `.git`, `node_modules`, `dist`,
  `.claude-plugin`, `.refactor-attic`, `.claude/worktrees`.
- **Self-exclusion**: the skill's OWN directory (`authorkit/skills/recurrence-audit/**`) is
  always skipped — its bundled scripts' selftest fixtures and its own docs necessarily contain
  example `LEDGER-CLASS:` text (illustrating the tag, or proving the parser), which is not a
  real citation about a production incident. Measured 2026-08-18: without this, the first real
  run against this estate surfaced 7 phantom seeded classes, every one traced to `scan.py`'s own
  selftest string literals.
- Bare-citation counting is scoped to `.md` files only (doctrine bullets/SKILL.md is where the
  overwhelming majority of citations live, per the ruling-2 grep evidence) — counting bare `#N`
  across `.py`/`.js`/config would drown in hex colors, anchors, and code comments unrelated to
  incidents; this narrowing is stated, not silent.
- Selftest fixtures (negative controls included): a planted `LEDGER-CLASS:` tag is found with
  correct slug/ids/mechanized/file/line (positive); a clean tree with only bare `#NNN` citations
  scores zero seeded classes and a nonzero baseline (reverse — proves seeded and bare-citation
  counting are genuinely independent counters, not one masquerading as the other); two ids under
  one slug group correctly (multi-id); two DIFFERENT slugs stay separate totals (no cross-class
  bleed); a malformed tag (missing `ids:` or an unparseable date) is skipped, never crashes and
  never silently counted as seeded (malformed-tag negative control); skip-dir + binary pruning;
  an empty target raises a clean usage error (never a false-clean 0); the verdict-line string is
  pinned exactly; ids/output are stable across two runs of an unchanged tree.

### `skills/recurrence-audit/scripts/trend.py`

Same append-only CSV anatomy as `attention-audit/scripts/trend.py` (`HEADER`, `append_rows`,
`new = not os.path.isfile(out_path)`, one row per date). Never blends the two series into one
quotient (separate-series law, same rationale attention-audit's own header carries).

```
trend.py --scan <scan.json> [--recurrence <recurrence.json>] [--routing-report <path>]
         --out <path> [--date YYYY-MM-DD]
trend.py selftest
```

`HEADER = ["date", "seeded_classes", "recurred_classes", "bare_citations", "files_scanned",
"routing_passed", "routing_total", "routing_pass_rate"]`. `recurred_classes`: `0` when
`seeded_classes == 0` (nothing to check); the recurrence-JSON's count of `true` values when
supplied; the literal `absent` when seeded classes exist but no recurrence JSON was supplied
this pass. `routing_*` columns: real numbers when `--routing-report` is supplied and parses;
`absent` otherwise. Selftest fixtures (negative controls included): a fresh file gets the
header row (positive); a second append does not rewrite the first row (append semantics); zero
seeded classes → `recurred_classes` is `0`, never `absent` (the zero-vs-absent distinction is
the one a naive implementation collapses); seeded classes present with no `--recurrence` →
`absent`; a supplied `--recurrence` with a mix of true/false counts only the `true`s; missing
`--routing-report` → all three routing columns read `absent`; a present, parseable
`--routing-report` → real numbers and a computed `routing_pass_rate` (rendered as a decimal
string, e.g. `"0.92"`); header carries no blended/ratio column across the two series (mirrors
`attention-audit/scripts/trend.py`'s own assertion, extended: no cross-series quotient either).

### `skills/recurrence-audit/evals/evals.json`

Trigger cases (≥6): "Is our incident-recurrence rate actually being measured anywhere", "Walk
the ledger and tell me which incident classes came back", "What's IDR-0006's primary measure
reading this release", "Check whether any mechanized gate/doctrine fix has recurred", "Track the
routing-eval pass-rate trend release over release", "Append this release's recurrence + routing
numbers to the trend file". No-trigger fences (owners in comments): menu-rent/collision series →
`attention-audit`; naming conformance → `naming-audit`; prose bloat → `bloat-audit`; "run the
routing simulation itself" → `harness:check-routing`; an arbitrary caller pattern with no
incident-class shape → `pattern-audit`.

### Ledger/manifest edits

`authorkit/README.md` member table + footer ledger row; `authorkit/.claude-plugin/plugin.json`
version bump; `authorkit/naming.manifest.json` AND the repo-root `naming.manifest.json` both
gain `{"canonical": "recurrence", "plural": null, "banned_aliases": []}` in `object_vocab` — the
skill name `recurrence-audit` parses as `{object: recurrence}-{process: audit}` (§3.2 of the
naming spec; `audit` is already in both manifests' `ProcessLex`/`process_lex`). `recurrence`
exists in neither manifest today (checked directly), so — unlike `pattern-audit`'s single
estate-local registration (the root manifest already had `pattern`) — this build registers it in
BOTH.

### Rulings that earned no ADR (recorded here, per the ADR-default-no discipline)

- **Skill named `recurrence-audit`, not the ticket's own `measure-recurrence` slug.** The ticket
  title is a label, not a naming mandate; every audit-family sibling (`attention-audit`,
  `bloat-audit`, `naming-audit`, `doctrine-audit`, `pattern-audit`, `estate-audit`,
  `repo-audit`) already conforms to `{object}-audit`, and `measure` is in neither lexicon
  (adding it as a new `VerbLex`/`ProcessLex` entry is a closed-lexicon governance PR this ticket
  doesn't need to spend). `recurrence-audit` conforms today with one registration, matches the
  family shape, and reads identically to a human.
- **One combined trend file (`recurrence-trend.csv`), not two.** Mirrors `attention-trend.csv`
  itself, which already blends menu-rent counts and dead/stolen/leaked routing counts in one
  row — precedent for co-locating two distinct series in one file's columns, never one blended
  quotient column.
- **Script names `scan.py`/`trend.py` reused across skills, not renamed to avoid collision.**
  `estate-audit-agent`'s own tool grants already list `Bash(python3 */scripts/scan.py *)` and
  `Bash(python3 */scripts/trend.py *)` scoped by path glob, not by skill — a second skill using
  the same script *names* (in ITS OWN `scripts/` directory) rides the existing grant rather than
  minting a new one, the inverse of `pattern-audit`'s LLD's own `measure.py`-avoidance ruling
  (there, reusing a name would have let a NEW skill ride an EXISTING skill's narrower grant
  unintentionally; here, both names are already estate-wide glob-scoped by convention, so there
  is no narrower grant to leak past).

## Interfaces

### Skill ↔ script boundary

Same split `pattern-audit` established: the scripts are deterministic, instruction/network-blind,
selftest-provable offline. All interpretation — the live `gh issue` conjunct-A check, the
class-recurrence verdict, rendering — lives in the skill body.

### `LEDGER-CLASS:` tag — the seeded convention this ticket ships

```
LEDGER-CLASS: watch-exit-0-advisory | ids: #NNN, #NNN, #NNN, #NNN | mechanized: 2026-08-14
```

(`#NNN` placeholders, deliberately non-matching to `scan.py`'s own `ID_RE` — this is an
illustrative worked example, not a real tag; `scan.py` itself additionally self-excludes its own
skill directory so its selftest fixtures never surface as phantom ledger entries either,
Components below.) Adoption is additive and optional going forward: a doctrine bullet, gate-check comment, or
fixture that already narrates an incident (as hundreds already do, per Ruling 2's grep) gains
this one trailing line the next time it's touched — never a retrofit sweep this build owes (that
would be its own, much larger, ticket). `scan.py`'s selftest proves the parser; adoption is a
process ratchet, not a mechanized requirement.

### Consumers

`recurrence-trend.csv`'s reader is the same DRI review IDR-0006 itself names (`brief-
nonoun-plugins.md`'s monthly review) — a human diffing rows release over release, exactly as
`attention-trend.csv` is read today. No other consumer is assumed.

## Data

`scan.py --json` output:

```json
{
  "target": "/abs/path",
  "files_scanned": 1631,
  "seeded_classes": [
    {
      "class": "watch-exit-0-advisory",
      "ids": ["#530", "#546", "#549", "#551"],
      "mechanized": "2026-08-14",
      "citations": [{"file": "teamwork/skills/fleet-rules/SKILL.md", "line": 214}]
    }
  ],
  "bare_citations": {"count": 406, "files": 406},
  "totals": {"seeded_classes": 1, "seeded_citations": 4, "bare_citations": 406}
}
```

`trend.py`'s appended row (`recurrence-trend.csv`):

```
date,seeded_classes,recurred_classes,bare_citations,files_scanned,routing_passed,routing_total,routing_pass_rate
2026-08-18,1,absent,406,1631,absent,absent,absent
```

## Build manifest

| # | Path | Action |
|---|---|---|
| 1 | `authorkit/skills/recurrence-audit/SKILL.md` | create |
| 2 | `authorkit/skills/recurrence-audit/scripts/scan.py` | create, selftest per Components |
| 3 | `authorkit/skills/recurrence-audit/scripts/trend.py` | create, selftest per Components |
| 4 | `authorkit/skills/recurrence-audit/evals/evals.json` | create |
| 5 | `authorkit/README.md` + `authorkit/.claude-plugin/plugin.json` | edit: member row, ledger row, version bump |
| 6 | `authorkit/naming.manifest.json` + repo-root `naming.manifest.json` | edit: register `recurrence` in `object_vocab` |
| 7 | `recurrence-trend.csv` (repo root) | create, seeded by the first real `trend.py` run |

Explicitly NOT in this build: any change to `harness:check-routing` itself (Rejected
alternatives); any retrofit sweep adding `LEDGER-CLASS:` tags to existing doctrine bullets (a
future, separately-sized ticket once the convention proves useful); any ADR (no fork was
resolved that needed ratifying — every ruling above follows an established estate pattern or is
recorded here per the ADR-default-no discipline).

## Acceptance (build gate — checkable predicates)

1. `python3 authorkit/skills/recurrence-audit/scripts/scan.py selftest` → exit 0.
2. `python3 authorkit/skills/recurrence-audit/scripts/trend.py selftest` → exit 0.
3. `python3 harness/scripts/release_gate.py authorkit` → green (G4 selftest sweep, G7 eval-suite
   schema, G10 README/manifest version match, G12 naming grammar).
4. `python3 authorkit/skills/naming-audit/scripts/validate.py --target authorkit --manifest
   naming.manifest.json --scope grammar --json` (repo root, G12's own invocation) →
   `grammar_errors` names no `recurrence-audit` entry.
5. Fresh-context skill-checker pass on the new `SKILL.md` — verdict recorded in the build
   handback (semantic-edit invariant).
6. This LLD passes `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0011-recurrence-audit.md`.

## Risks

1. **Zero seeded classes at ship time reads as "nothing works."** Detection: a reviewer sees an
   all-`absent`/all-`0` first trend row and assumes the tool is broken. Fallback: the SKILL's
   render step states the baseline explicitly as a baseline ("406 bare citations, 0 seeded
   classes — convention just shipped, adoption is additive going forward"), never silently.
2. **Conjunct-B proxy (re-citation as a stand-in for "a gate fired red again") is imperfect** —
   a class could recur without anyone re-citing it, or get re-cited for a near-miss that wasn't
   a true re-fire. Detection: a DRI review (IDR-0006's own falsification test) finds the proxy
   disagreeing with a known real recurrence. Fallback: the SKILL states the proxy explicitly as
   a proxy in its render step, never as ground truth; a disagreement routes to IDR-0006's own
   escalation path (a superseding IDR), not a silent patch here.
3. **`LEDGER-CLASS:` adoption never happens** (a convention nobody uses is a convention that
   doesn't exist). Detection: `scan.py`'s `seeded_classes` count stays at 0 across several
   releases' trend rows. Fallback: this is itself a finding the trend row surfaces — a flat
   0 alongside a growing bare-citation count is evidence the seeding step needs a push (a
   `chore-planner`-queued retrofit-a-few-classes task), not silently accepted forever.
4. **Routing-eval column stays perpetually `absent`** if no caller ever transcribes a
   `check-routing` run into `--routing-report`. Detection: same as Risk 3, visible in the trend
   file itself. Fallback: named as a real gap in this build's own Findings write-back, not
   hidden — a follow-up could wire `check-routing` to emit the JSON directly (Rejected
   alternatives), closing this gap mechanically instead of by habit.

## Rejected alternatives

- **Modifying `harness:check-routing` to emit a machine-readable JSON report directly** (instead
  of this skill transcribing its printed line). Rejected as separate scope: `check-routing` is a
  `harness` plugin; changing its Phase 5 output shape is a cross-plugin contract change this
  size:big ticket doesn't need to also own, and IDR-0006's own proof-ref already treats
  `check-routing`'s existing report as sufficient. Left as a named future improvement (Risk 4).
- **Fully mechanizing recurrence conjunct B (a gate literally firing red) via CI history** (e.g.
  `gh api` over historical check-runs). Rejected: no durable, queryable record of "which gate
  fired red for which incident class" exists anywhere in this estate today — building one is a
  much larger, separate instrumentation effort than IDR-0006's ticket asks for. The re-citation
  proxy (Ruling 3) is the honest, shippable substitute, named as a proxy, not silently upgraded
  to ground truth.
- **A retrofit sweep tagging existing doctrine bullets with `LEDGER-CLASS:` now.** Rejected as
  out of this build's size: hundreds of citations, most needing a human judgment call on class
  boundaries neither script nor skill can safely automate. Left as future queued work (Risk 3's
  fallback names the owner: `chore-planner`).
- **A single blended recurrence/routing quotient column.** Rejected on the estate's own
  Goodhart precedent (`attention-audit`'s separate-series law) — a blended figure rewards
  deleting the fence that protects a rare-but-expensive misroute exactly as it would for
  attention's own dead/stolen/leaked columns.
