# check-state — FLOOR audit report

Auditor: skill-checker seat (fresh context) · 2026-07-29
Standards applied: skill-writing-rules, script-writing-rules
Scope: SKILL.md, intent.md, evals/evals.json, scripts/{git_state,ticket_state,doc_state,state_diff}.py
All claims below are from runs, not reading alone; repro commands included where a defect was executed.

## Verdict

🟡 One blocking procedural gap (the skill's own documented degraded mode breaks its Delta
step), five minor findings, and a set of notes. The scripts are well above house floor —
all four selftests green with negative + reverse controls including the two same-day
incident fixtures, stdlib-only, docstring manuals, verdict lines — and the SKILL.md is a
clean procedural skeleton (identity line, numbered steps, output contract, failure
branches, checkable stopping predicate, labeled contrastive pair). The findings are edge
seams, not structural rot.

## Blocking

### B1 — Step 2 is unexecutable when any collector is UNMEASURED

`state_diff.py` requires all three JSON paths (`len(argv) != 6 → exit 2`), but the skill's
own primary degraded mode — no `gh`, or a non-GitHub backend — means `ticket_state.py`
exits 2 and **no ticket.json exists**. Step 2 as written then fails (`state_diff · FAIL ·
unreadable input`), and the body gives no instruction for what to pass in a skipped
collector's slot. The failure branches cover collector exits 1/2 for the *report* sections
but never say what Delta does when an input is missing.

Two-layer consequence:
1. On a non-GitHub repo the Delta section can never be produced as written — yet the
   stopping predicate demands "the checkpoint reflects this run".
2. If the fix is "pass `{}` for the skipped layer" (the snapshot's `.get` defaults handle
   it), the checkpoint stores empty issues/prs; the next run with `gh` working reports
   every open issue and PR as *added* — delta noise across measurability transitions the
   design doesn't acknowledge.

Fix: state_diff accepts a `-` or missing-file sentinel per slot, records
`"unmeasured": [...]` in the checkpoint, and the diff suppresses (or labels) transitions
into/out of unmeasured; SKILL.md step 2 and the failure branches name this path.

## Minor

### M1 — ticket_state.py: `--stale-days N` without a root misparses, then tracebacks

Confirmed by run: `python3 scripts/ticket_state.py --stale-days 45` → the value `45` is
collected as a positional (the filter only drops args starting with `-`), becomes the repo
root, and `subprocess` raises an **uncaught `FileNotFoundError`** — a raw traceback instead
of the contract's FAIL line (exit happens to be 1 only because the interpreter died). The
documented usage line `ticket_state.py [<repo-root>] [--stale-days N]` promises this form
works. Fix: consume the flag's value before the positional filter (or use a real parse),
and add `FileNotFoundError`/`NotADirectoryError` to main's catch. Selftest gap: no fixture
exercises argument parsing.

### M2 — "Blocked on you" contract names data no collector collects

SKILL.md step 4 and the Output contract key blocked-on-you off "`failing_ci` on the
user's own PRs", and treat `awaiting_review` PRs as blocked-on-you — but the PR JSON
fields (`number,title,isDraft,reviewDecision,mergeable,statusCheckRollup,headRefName,
updatedAt`) include **no author**, and step 4 explicitly forbids re-running gh by hand.
Ownership is therefore unmeasurable from the collector JSON: the judgment pass either
violates the no-hand-gh rule or silently reports *all* failing/awaiting PRs as
blocked-on-you (a PR the user authored and is awaiting others' review is blocked on
*them*, not the user). Fix: add `author` to the `--json` list (and classify
`mine_failing_ci` / `awaiting_my_review` in the collector, where `gh` knows `@me`), or
soften the body's wording to match what's measured.

### M3 — doc_state.py: substring doc-name matcher inventories non-docs

Confirmed by run: `DOC_NAME` matches on substring, so `explanation.md`, `airplane.md`,
and `implants.md` all match `plan` (`bool(DOC_NAME.search("explanation")) == True`).
Every hit lands in `items` and in the state_diff `docs` snapshot — phantom docs in Counts
and delta noise when such a file is added/removed. The selftest's reverse control
(`readme` must not hit) doesn't cover the boundary class. Fix: word-boundary the
alternation (`\b(roadmap|plan|...)\b` won't catch `my-plan`; use
`(?<![a-z])(...)(?![a-z])` or match on hyphen/underscore-split stem tokens), plus a
reverse-control fixture for `explanation`.

### M4 — state_diff.py: corrupt checkpoint tracebacks; write-before-print loses the delta

Confirmed by run: a checkpoint containing invalid JSON raises an **uncaught
`JSONDecodeError`** (line 80 is outside the try) — traceback, no FAIL line. Separately,
the checkpoint is written *before* the result prints, and `mkdir`/`write_text` OSErrors
are uncaught: on an unwritable checkpoint the computed delta dies with the traceback.
SKILL.md's failure branch promises "deliver the report with the Delta section marked
'not saved'" — deliverable only if the script prints the delta first and reports the
write failure distinctly. Fix: treat unreadable checkpoint as first-run-with-warning (or
FAIL cleanly), print the result before writing, catch OSError on the write and emit a
`checkpoint_saved: false` field. Selftest gap: only the pure functions are exercised —
first_run, the write path, and these two failure paths have no fixture.

### M5 — intent.md assertion 4 contradicts assertion 1 and the output contract

Assertion 4: "A repeat run **opens with** a Delta section." Assertion 1 and the SKILL.md
output contract: Blocked-on-you leads, Delta is section 4. A validator scoring assertion
4 literally fails every contract-conformant repeat run. Fix the assertion's wording
("contains a Delta section computed from the checkpoint").

## Notes

- **N1 — "skim stops at the first 🟢" is ambiguous.** Sections are fixed-order, not
  severity-ordered: a 🟢 Blocked-on-you above a 🔴 Drift would end the skim before the
  worst news. If the intent is "you may stop reading once everything remaining is 🟢",
  say that; as written it invites a wrong reading.
- **N2 — step 5 says "then stop"; step 6 follows.** The `--artifact` variant is
  sequenced after the stop instruction. Fold it into step 5 as a conditional, or move the
  stop to the end.
- **N3 — no-args behavior deviates from the anatomy contract.** script-writing-rules:
  "no args → print `__doc__`, exit 2." All three collectors default the root to `.` and
  run. Defensible for collectors (the default is meaningful), but it's an undocumented
  house deviation — worth one docstring line or a ruling.
- **N4 — `subprocess.TimeoutExpired` is uncaught in all collectors** (timeouts 60/120s):
  a hung git/gh yields a traceback, not the FAIL line.
- **N5 — unauthenticated `gh` exits 1 (FAIL), not 2 (SKIP).** Tri-state doctrine treats
  environment absence as skip; missing auth is arguably environmental. The SKILL.md
  failure branch lumps "unauthenticated" with UNMEASURED either way, so the report
  survives — but the "reason line" will be raw gh stderr, not a curated SKIP line. A
  `gh auth status` probe before collecting would make this branch clean.
- **N6 — find_docs misses plugin-root-level docs.** Globs are `*.md`, `docs/**/*.md`,
  `*/docs/**/*.md` — a `harness/ROADMAP.md` (plugin root, outside any docs/) is invisible.
  Matches current workspace layout; note it in the docstring so the gap is disclosed.

## What passes cleanly (verified)

- All four selftests green by run (`exit=0` each); every one carries a biting negative
  control AND a reverse control, including the two 2026-07-29 incident fixtures
  (worktree-branch-as-delete-candidate; absent-dist-as-drift). stdlib-only throughout;
  determinism fine (no network in selftests; gh calls are collection, not checking).
- `skill_lint.py` clean on SKILL.md. Both invocation dials explicit; species/dials/name
  coherent (procedural · false/true · verb-head `check-state`); `argument-hint` present.
- Description is a real trigger contract: verbatim phrasings front-loaded, lifecycle
  trigger ("catch me up"), three parseable `NOT for (owner)` fences, within budget.
- Procedural skeleton complete: identity line, output contract with fixed section order,
  named failure branches, checkable stopping predicate, escape hatches (UNMEASURED
  renders anyway), one contrastive pair with the bad side labeled. Hard-gate budget
  respected (lowercase nevers; no uppercase salience spend).
- Deletion test: the body is tight — no line restates model knowledge; the
  cross-reference pair list and the owner-routing lines are the genuine behavior delta.
- evals.json: 10 trigger / 10 no-trigger, every no-trigger names its owner, near-misses
  well-chosen (chore-planner, repo-cleaner, /check-everything, close-session,
  find-open-questions, single-PR lookup).

## Recommended order of repair

1. B1 (unmeasured-collector slot in state_diff + checkpoint semantics) — it's the
   skill's own advertised degraded mode.
2. M2 (author field) — one `--json` word plus two classifier lists, kills a contract lie.
3. M1, M3, M4 — small script fixes, each with its incident-pattern selftest fixture
   (the workspace's incident→fixture rule applies).
4. M5, N1, N2 — wording-only.
