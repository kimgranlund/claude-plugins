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

---

# Audit report — `feature` SKILL.md after the ADR-0004 Issue-Type dual-write edit

- **Target:** `scribe 0.1.0/skills/feature/SKILL.md` (uncommitted edit on `issue-44-adr-0004-dual-write` worktree)
- **Audited against:** `.claude/docs/adr/0004-issue-types-for-bug-feature-task.md` (ratified),
  `forge:skill-authoring-standards`, siblings `bug-report`/`issue`/`ops-issues` (same edit class),
  `.github/ISSUE_TEMPLATE/feature.yml`, live `gh` 2.96.0
- **Depth:** FLOOR + the four dispatch-specific checks
- **Date:** 2026-07-18

```
Skill: scribe 0.1.0/skills/feature/SKILL.md · Standards: skill-authoring-standards · Lint: clean
Verdict: PASS — no blocking finding; 1 major (class-wide), 1 minor, 4 notes
```

## FLOOR criteria

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | PASS | — | SKILL.md:106–110 (delete → no `--type`, no retry discipline); :27–35 (resolver); :128–141 (opt-in gate) — all three fail the deletion test in the right direction | — |
| R2 trigger fidelity | PASS | — | Description untouched by this edit; "can we add a dark mode" / "what if we supported CSV export" / `/feature` all match :7–8; fences :13–15 repel bug/issue//build/doc-forge | — |
| R3 species/dials | PASS | nit | Procedural, both dials explicit (:16–17); noun-head name `feature` predates this edit, shipped through prior gates — precedent, not a new finding | — |
| R4 register | PASS | — | New clause instantiates, spec-present ("fallback: retry without `--type` … note the skipped type", :108–110); uppercase-gate count unchanged, lint clean | — |
| R5 no restatement | PASS | note | The fallback line now exists verbatim in 4 files (three skills + ops-issues) with doc-authoring-standards' new §Issue Type dual-write as canon — ADR-0004's own ratified consequence ("four files, one line each"), so sanctioned; it is a 4-way drift-watch from here on | — |
| R6 position | PASS | — | 176-line body, entirely inside the 5,000-token survival window; contract (Phase 5) ahead of Failure branches ahead of Done-when | — |
| R7 contracts | PASS | see F1 | Payload contract :96–99, failure branches :143–165, checkable Done-when :167–176 all present; the NEW failure mode is named inline only (F1) | one clause |
| R8 quantities | PASS | — | "one round max" :54, "ONE AskUserQuestion" :131, "one hop only" :152; the retry clause is singular and unambiguous | — |

## Dispatch-specific checks

### 1. Natural extension, not bolted on — YES

The clause rides the existing sentence spine: command flag up front (`gh issue create --type
Feature`, :106), prose consequence appended after the label list with the same "and sets…"
shape ADR-0004's own Consequences section prescribes ("labels `X` + sets Issue Type `X'`
(fallback: …)"), and the parenthetical fallback mirrors the in-bullet fallback style Option C
already established two bullets down (:116–118). Sibling diffs are token-for-token the same
shape (`bug-report` :94–96, `issue` :113–117), so the family stays uniform. The one echo — the
flag appears in the command AND "sets the native Issue Type `Feature`" in prose — is the ADR's
own phrasing, and the prose half is what carries the ADR citation + fallback, so it earns its
place.

### 2. Fidelity to ADR-0004's ratified decision — YES, points 1 and 4 both honored

- **Point 1 (additive dual-write):** label list untouched, type added alongside — "same payload
  contract, one more field" ✓ (:107–109).
- **Point 4 (label stays system of record, never block a mint):** "label alone still lands, note
  the skipped type in the close-out" ✓ (:109–110). The Done-when line (:167) still says "a
  labeled GitHub Issue (its URL reported)" — correctly UNCHANGED: a type-skipped issue still
  satisfies it, which is exactly point 4's never-block semantics.
- **Size stays a label — confirmed, no accidental drift:** the pre-existing parenthetical "(the
  machine-read size lives in the label)" (:107–108) survives the edit verbatim, and the new
  clause names only the Issue Type `Feature`. Nothing implies `size:` becomes a type or Field
  (ADR-0004's explicit non-goal, Decision point 2); doc-authoring-standards' new section states
  the non-goal canonically, so this skill correctly doesn't restate it.
- **The ADR's two open verification items are answered and recorded** (pack reference
  `bug-task-feature-mapping-nuances.md`, update block in this same change-set): `--type` is a
  real `gh issue create` flag — re-confirmed live in this audit against gh 2.96.0 (`--type name
  · Set the issue type by name`) — and this repo, being personal-account-owned, has NO Issue
  Types, so the fallback path is the always-taken path here. The recorded probe also confirms
  gh validates-and-rejects before creating anything, so the retry can never double-mint. The
  skill's clause is therefore not an overclaim: verified mechanism, verified-safe fallback.

### 3. Fallback discipline vs the skill's own patterns — consistent in shape; one placement gap (F1)

Same grammar as every existing fallback: attempt → degrade without losing the record → note in
the close-out. Vocabulary matches ("note … in the close-out" = Option C's "reports the fallback
in the close-out", :117–118). But the skill's established pattern (this file's prior audit,
check 4) is that **Failure branches is the canonical enumeration and the Phase-5 text is its
echo** — this new failure mode inverts that: inline only, no branch line. See F1.

### 4. Dangling refs / overclaims

- `ADR-0004` named mention (:108) — file exists at `.claude/docs/adr/0004-issue-types-for-bug-feature-task.md`;
  workspace-level mention degrading gracefully outside this repo, same class as the standing
  ADR-0002 mention (:29) ✓.
- `--type Feature` — verified real (check 2) ✓.
- One partial-mirror claim now stale by omission: F2 below.

## Findings

### 🟡 F1 — major (non-blocking, ALL FOUR consumers): the type-resolution retry lives only inline; the pre-existing "`gh` fails partway → file backend" branch can capture it

The new failure mode ("org's type schema doesn't resolve") is documented only inside the Phase-5
bullet (:108–110). The Failure branches section still says "Workspace rules git-native but `gh`
fails partway through a run → fall back to the file backend for THIS record" (:160–162) — and a
`--type` rejection IS `gh` erroring. In THIS workspace the collision is not an edge case: the
repo is personal-account-owned, so `gh issue create --type Feature` fails on **every** mint;
a run that consults the branch list instead of the bullet's inline parenthetical would abandon
git-native for the file backend on every capture. Record never lost either way (both paths
capture), which is why this is major, not blocking — but for `ops-issues`, which runs this
identical clause unattended hourly, a misroute would silently move records to the wrong store.

**Fix (one clause, all four files or just the canonical branch line per file):** extend the
gh-fails branch: "…(a `--type` resolution error is not a `gh` failure — retry without the flag
first, per Phase 5; only a create that still fails falls back here)". Siblings `bug-report`
(no explicit gh-fails branch wording checked here — verify), `issue`, and `ops-issues` (sweep
report analog) carry the same inline-only shape.

### 🟡 F2 — minor (all three templates): the issue-template mirror claim is now partial

SKILL.md:120 — "`.github/ISSUE_TEMPLATE/feature.yml` mirrors this contract for a human filing
directly on GitHub." The contract now includes the Issue Type; the template sets
`labels: ["feature"]` but no top-level `type:` key, so a human-filed issue gets the label and
never the type. GitHub issue forms do support a top-level `type:` key (verify against current
docs before editing — and note a template-declared type is untestable in this personal-account
repo). Either add `type: Feature` (org-portable, matches best-effort semantics since GitHub
ignores/rejects it gracefully where types are absent — verify) or scope the claim ("mirrors the
section/label contract"). Same for `bug.yml`/`task.yml` and the siblings' mirror lines. ADR-0004
did not name the templates in its four-file consequence list, so this is contract-mirror drift
introduced by the change-set, not an ADR violation.

## Notes (no action owed to ship this edit)

- **N1 — "org's type schema" phrasing is org-centric** where the verified failure case here is
  "personal account, no org at all". doc-authoring-standards' new section carries the precise
  fact; the skill's compressed clause is acceptable reference-not-restate. No action.
- **N2 — Edit-tier accounting (semantic body change → full loop):** lint clean ✓; this audit is
  the fresh-context critic ✓; behavior evidence = the recorded live probe (fallback path proven
  in-repo; happy path — `--type` accepted — is structurally untestable in a personal-account
  repo and rests on gh 2.96.0's documented flag + the ADR's own reversibility clause). Evidence
  gap acknowledged, not closable in this workspace.
- **N3 — evals.json correctly untouched:** description unchanged, no eval update owed, no
  /eval-run owed for this file.
- **N4 — Date anomaly in adjacent files (outside this audit's target):** the pack-reference
  update block and doc-authoring-standards' new section are both dated **2026-07-19**; today is
  2026-07-18. Flagging for the change-set owner — likely a typo, fix before commit.

## Cross-sibling applicability

| Finding | feature | bug-report | issue | ops-issues | templates |
|---|---|---|---|---|---|
| F1 (retry vs gh-fails branch ambiguity) | yes | yes (verify branch wording) | yes | yes (unattended — highest stakes) | — |
| F2 (mirror claim omits `type:`) | :120 | likely (verify) | likely (verify) | — | bug.yml, feature.yml, task.yml |
| N1 (org-centric phrasing) | yes | yes | yes | yes | — |
| N4 (2026-07-19 dates) | — | — | — | — | pack reference + doc-authoring-standards |
