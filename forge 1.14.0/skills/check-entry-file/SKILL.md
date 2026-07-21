---
name: check-entry-file
description: >-
  Audit and slim CLAUDE.md (and .claude/rules/) by classifying every line against the residency
  test and migrating evictions to their proper tier — checks to hooks, procedures to skills,
  subtree truths to rules — with a landing artifact for every behavior removed. Run
  /check-entry-file [path, default ./CLAUDE.md]. Human-timed; edits files on approval only.
disable-model-invocation: true
user-invocable: true
argument-hint: "[path to CLAUDE.md]"
---

# check-entry-file

check-entry-file slims an entry file without losing a single behavior: every evicted line gets a landing artifact before the prose is cut. Target: `$ARGUMENTS` (default `./CLAUDE.md`, plus `.claude/rules/` if present).

Invoke `entry-file-rules` now — its routing table is the classifier; it is not restated here.

## Phase 1 — Inventory and classify

1. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/skill_lint.py" <path>` — the C-rules give the mechanical smells (length, checks-in-prose density) as the report's header.
2. Read the file; classify **every line or coherent block** into exactly one class from the standards' routing table: `KEEP` (passes the residency test) · `→HOOK` · `→SKILL` · `→RULE` · `CUT-stale` · `CUT-known` (restates model knowledge). Staleness is checked first and against the repo, not memory — a line referencing a path, tool, or decision is verified with Grep/Glob before it may KEEP.
3. Emit the migration table, verdict first:

```
check-entry-file · <path> · N lines → keep K · hooks H · skills S · rules R · cut C
| Lines | Content (≤10 words) | Class | Destination + disposition |
```

Every `→HOOK` row names the pass/fail function; every `→SKILL` row names an existing skill to extend or a new one to forge; every `CUT-stale` row cites the evidence (the missing path, the retired tool).

**Gate E1:** every line classified; no row's destination reads "somewhere".

## Phase 2 — Approval

Present the table and the projected file (KEEP lines + pointers). This phase ends with the user's explicit approval of the table, row edits applied; classification disagreements resolve in the user's favor and are recorded. No file is touched before approval.

## Phase 3 — Migrate, then cut — in that order

Per approved row, landing artifact first:

- `→HOOK` — draft via `/make-hook` (or extend an existing script); the prose is cut only after the hook's selftest passes and it is registered.
- `→SKILL` — route to `/make-skill` for a new skill, or land the lines in the owning skill's body; cut after the skill lints clean. A one-line pointer may replace the block when discoverability warrants it.
- `→RULE` — move to `.claude/rules/<scope>.md` with its path filter; cut the global copy.
- `CUT-*` — remove; `CUT-stale` rows are listed in the report (they were false presuppositions the whole time — worth knowing).

If a landing artifact cannot be completed this session → its prose **stays** and the row is marked DEFERRED with the blocker; a behavior is never dropped into the gap between "removed from CLAUDE.md" and "not yet enforced anywhere".

**Gate E3:** every executed row has its landing artifact verified (hook selftest / skill lint / rule file present) before its cut.

## Phase 4 — Verify and report

1. Re-run the lint: C1 under threshold or the remaining length justified line-by-line in the report.
2. The residency read: each surviving line passes "true every turn, needed before task content" — read it as a fresh session would.
3. Final report: before/after line counts, the migration table with dispositions, DEFERRED rows with blockers, and the reminder that this audit recurs — the growing dotfile grows back.

Done when the approved table is fully executed or explicitly deferred, the slimmed file is on disk, every migrated behavior has a verified landing artifact, and the report is delivered. NOT done while any cut row lacks its landing artifact — that is behavior loss wearing a cleanup's name.
