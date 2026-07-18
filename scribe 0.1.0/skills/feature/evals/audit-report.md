# Audit report — `feature` SKILL.md after the ADR-0003 three-way backend edit

- **Target:** `scribe 0.1.0/skills/feature/SKILL.md` (uncommitted edit on `issue-34-linear-adapter` worktree)
- **Audited against:** `scribe 0.1.0/skills/doc-authoring-standards/references/backend-resolver.md`,
  `.../references/linear-adapter.md`, and siblings `bug-report`/`issue` (same edit class)
- **Depth:** FLOOR + the four dispatch-specific checks
- **Date:** 2026-07-18

## Verdict: 🟡 PASS with attention findings — no blocker

`skill_lint.py` clean (exit 0). Both referenced files exist (intra-plugin, no boundary
violation). No phantom `[[handle]]`s. No phase-number breakage. The Option-C additions read as a
native extension of the A/B pattern and match what the reference files actually promise. Three
🟡 findings, one of them a genuine regression introduced by this edit; five low notes.

## Resolution (2026-07-18, same session)

F1 (Done-when regression, feature-only): fixed — "(its URL reported)" restored for the
git-native clause. F2 (stale "both backends" phrasing): fixed here and in bug-report/issue —
reworded to "identical regardless of backend". F3 (Option C stops at create — no resume/dedup):
fixed at the root, not per-skill — `spec-linear-adapter` amended to v0.2.0 (REQ-010/AC-010, a
`read` operation), backend-resolver.md and linear-adapter.md updated to a six-op interface; Phase
1's id grammar now recognizes an Option-C native id via `read`, and Phase 3's dedup sweep now
names the adapter's `dedup-search` operation. N1 (stale frontmatter description): fixed same-change
across all three siblings; evals.json re-checked, no case changes needed (backend is not a trigger
axis), no /eval-run owed. N2–N5: left as observed, non-blocking. `skill_lint.py` and the plugin's
`release_gate.py` re-run clean after all fixes.

---

## Findings

### 🟡 F1 — Done-when regression: the git-native URL-reporting requirement was dropped (feature-specific, introduced by THIS edit)

Before: `...a lint-clean file on disk, or a labeled GitHub Issue **whose URL was reported**...`
After (SKILL.md:159–160): `...a lint-clean file on disk, a labeled GitHub Issue, or an Option-C
adapter's record (its native id reported)...`

The rewrite attaches a reporting requirement to Option C only; Option B's URL clause — which the
old line carried and which appears **nowhere else in feature** (unlike bug-report, whose Phase 4
body independently requires "a created issue whose URL is reported") — was silently lost. `issue`'s
done-line kept its URL clause ("an issue URL reported, ..."). Fix: `a labeled GitHub Issue (its
URL reported), or an Option-C adapter's record (its native id reported)`. Feature-only; siblings
do not need this fix.

### 🟡 F2 — Stale "both backends" ×2 now that there are three (applies to ALL THREE siblings)

- SKILL.md:91 — "The payload contract, identical on both backends: Summary · ..."
- SKILL.md:115 — "(both backends; queue docs stay files)"

Same stale word in `bug-report`:83 and `issue`:99. "Both" was correct under the binary seam; the
edit generalized the seam to three options without repairing the counter — exactly the
stale-context class the operating contract names a defect. Fix: "identical on every backend" /
"(all backends; queue docs stay files)". Cross-sibling sweep warranted.

### 🟡 F3 — Option-C generalization stops at the Record phase: resume-by-id and dedup never gained their Option-C reading (applies to ALL THREE siblings)

backend-resolver.md's five-operation interface exists "so a capture skill's own call sequence
never branches on which backend is active" — and defines `dedup-search` and `update` alongside
`create`. But:

- **Phase 1 (Route/resume)** — the id grammar is concretely A/B-only: `tkt-####` (file) or
  `#NN`/bare number (`gh issue view`). A Linear-native id (e.g. `ENG-123`) has no parse rule, so
  resume-by-id structurally cannot fire under Option C — yet the Done-when line promises "its
  native id reported", handing the user an id the skill can't later resume. The argument-hint
  (`[raw feature idea, or a TKT-/#issue id to resume]`) has the same A/B-only shape.
- **Phase 3 (Dedup)** — surface 1 names only `docs/tickets/` and `gh issue list --search`; the
  adapter's `dedup-search` operation (realized in linear-adapter.md) is never invoked.

Phase 0's blanket clause ("Every phase below follows whichever option the resolver returned")
partially covers Phase 3, but a blanket clause cannot rescue an id *grammar*. Same gap in
`bug-report` (Phase 1) and `issue` (Phases 1, 3). Not a blocker — Option C degrades to
create-only capture with graceful A-fallback, nothing is lost — but it undercuts the resolver's
"never branches" promise and should be a follow-up item for all three siblings (plus the shared
argument-hints).

---

## Dispatch-specific checks

### 1. Natural extension of the A/B pattern — YES

- **Phase 0:** same resolver-call paragraph shape as siblings; keeps feature's pre-existing
  "Canonical statement: bug-report's SKILL.md — this is the same seam, not a second one" closer
  intact and in the same position. Correctly omits bug-report's canonical-only "consumers outside
  a ruled workspace see no change" clause (deferring, not duplicating).
- **Phase 5 bullets:** ordering File → Git-native → Option C matches bug-report's Record phase
  exactly; bullet length and register match the two above it.
- **Failure branches:** the Option-C branch is appended immediately after the git-native
  fallback branch it says "same fallback discipline" about — the antecedent is adjacent, same
  placement as both siblings.
- **Noun adaptation is correct:** "never leave the **idea** uncaptured" (bug-report: "the
  report"; issue: "the item") — the edit adapted, not copy-pasted.

### 2. Accuracy against the reference files — YES, no operation-name or field drift

- "the resolved adapter's `create` operation" — `create` is the interface's first operation ✓.
- "`size` carried as a label" — matches linear-adapter.md's payload mapping (Size → Linear
  labels) ✓, and is correctly feature-specific (see check 3).
- Partway-failure fallback "to the file backend for this operation, reported in the close-out" —
  matches REQ-008's per-operation fallback verbatim in substance ✓.
- "a bring-your-own adapter documents its own" — matches the resolver's Option-C row ✓.
- Low wording note (N3 below): the skills' Phase-0 fallback says "the ruled option's adapter is
  unreachable → Option A" where the resolver says "**Option C** ruled but its adapter is
  unreachable" — a superset (it also covers `gh` down under B), consistent with the failure
  branches' actual behavior, shared verbatim by all three siblings. Benign; if anyone "fixes" it,
  fix the resolver toward the skills, not vice versa.

### 3. Feature's own phrasing respected (not a bug-report paste) — YES

- The Option-C bullet landed in **Phase 5** ("Record, lint, place"), feature's own numbering; no
  added text references any phase number, so nothing to break. Feature's internal "re-run Phase
  4's sizing" (Phase 1) still points at its own Phase 4 (Size and shape) ✓.
- Size labeling is handled per-sibling correctly: feature says "`size` carried as a label"
  (mandatory size — feature always sizes), issue says "`size` (where clear)" (unsized legal for
  tasks), bug-report's bullet says nothing about size (bugs carry severity, not size) ✓.
- No bug-report vocabulary leaked (no "report", "Classification", "Severity" in the added text).

### 4. Dangling refs / redundancy — see F1–F3; plus low notes

- Both `references/*.md` targets exist and say what feature claims they say ✓.
- The mid-operation fallback is stated twice (Phase 5 bullet + Failure branch) — mirrors
  bug-report/issue exactly; the failure-branch list is the canonical enumeration and the bullet
  is its in-place echo. Acceptable pattern-consistency, not flagged.

## Low notes (no action owed to ship this edit)

- **N1 — Frontmatter description still binary:** "the TICKET file by default, or the workspace's
  ruled git-native backend" doesn't mention Option C. Identical situation in both siblings —
  plausibly intentional (Option C doesn't change *routing*, and a description edit owes a
  same-change evals.json update per the workspace invariant). If descriptions are ever updated
  for Option C, do all three + evals in one change and `/eval-run`.
- **N2 — Option-C bullet names the size label but not the `feature` kind label** (the git-native
  bullet names both); linear-adapter.md's mapping table covers kind → label, so nothing is
  actually lost. Cosmetic.
- **N3 —** the "ruled option's adapter unreachable" superset phrasing (detailed in check 2).
- **N4 — Ragged wrap in the Done-when line** (SKILL.md:161–162: "...linked into / whatever queue
  docs exist, with / every extraction gap named" — a near-empty line mid-sentence). Cosmetic;
  worth smoothing if F1 is fixed in the same lines anyway.
- **N5 — evals.json untouched and correctly so** — the description didn't change, so no eval
  update was owed; suite is valid JSON, 15 cases, unchanged.

## Cross-sibling applicability

| Finding | feature | bug-report | issue |
|---|---|---|---|
| F1 (dropped URL clause) | fix here | not affected (Phase 4 body keeps it) | not affected (done-line keeps it) |
| F2 (stale "both backends") | ×2 | ×1 (line 83) | ×1 (line 99) |
| F3 (no Option-C resume/dedup) | yes | yes (Phase 1) | yes (Phases 1, 3) |
| N1 (binary description) | yes | yes | yes |
