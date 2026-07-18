# Audit — bug-report after the ADR-0003 three-way backend edit

Auditor: skill-auditor seat (FLOOR depth + the four dispatch-specific checks) · 2026-07-18
Target: `scribe 0.1.0/skills/bug-report/SKILL.md` (worktree issue-34-linear-adapter)
References judged against: `scribe 0.1.0/skills/doc-authoring-standards/references/backend-resolver.md`,
`scribe 0.1.0/skills/doc-authoring-standards/references/linear-adapter.md`

## Resolution (2026-07-18, same session)

All findings applied. MAJOR-1 (undefined "read" operation): fixed at the root — `spec-linear-adapter`
amended to v0.2.0 with REQ-010/AC-010 (a sixth `read` operation), realized in both
backend-resolver.md (now a six-op table) and linear-adapter.md (Linear's `issue(id:...)` query,
marked `[inferred]`, introspect-first). Phase 6's phrasing needed no further edit — it already
named "the resolved adapter's own read operation," now backed by a real contract. MAJOR-2 (Phase 1
binary id grammar): Phase 1 now recognizes an Option-C native id, resolved via the new `read` op;
mirrored in `feature` and `issue` from the same root fix. MINOR-1/2 naming asymmetry and
double-stated fallback: bullet labels unified to Option A/B/C across all three siblings. MINOR-3
stale description: rewritten same-change. MINOR-4 Findings-first parity marker: added to Phase 6.
Resolver-side fallback under-specification: backend-resolver.md's line widened to cover both
Option B (`gh` unavailable) and Option C. `skill_lint.py` and the plugin's `release_gate.py`
re-run clean after all fixes.

## Verdict

**PASS WITH FINDINGS** — no blocker. `skill_lint.py` clean. The Option-C additions are accurate on
every fact they state (status mapping, `create` operation name, fallback discipline all match the
reference files exactly), REQ-006's Findings-first ordering is structurally preserved, and both
cited reference files exist at the cited paths. Two MAJOR findings: Phase 6 names an adapter
"read operation" the five-operation interface does not define, and Phase 1's resume path was left
binary — an adapter-native id the skill itself promises to report cannot be resumed. Four MINOR
findings on register symmetry and stale description. Every finding except MINOR-4 is expected to
apply to the siblings (`issue` confirmed for MAJOR-2; `issue`/`feature` share the Option-C bullet
phrasing for MINOR-1/2).

## MAJOR findings

### MAJOR-1 — Phase 6 references an undefined adapter operation ("read")

SKILL.md:132–133: "Read the record back on return (`gh issue view --comments` on the git-native
backend; **the resolved adapter's own read operation** under Option C)."

backend-resolver.md's interface (its §"The five-operation adapter interface", REQ-001) defines
exactly five operations: `create`, `dedup-search`, `update`, `close`, `discover`. There is no
`read`/`get`. `dedup-search` matches one candidate by nouns, not by id; `discover` lists since a
checkpoint. linear-adapter.md likewise documents no read-one-record-with-comments operation.

This matters beyond wording: Phase 6's read-back is a real step on every backend. Options A/B are
realized inline in the skill (file read; `gh issue view --comments`), but Option C is realized
*only* through the documented interface — so the operation Phase 6 depends on is genuinely
undefined, not merely misnamed. The sibling `issue` needs the same primitive (its resume-with-
nothing-after-the-id branch "report[s] the record's state, labels, and last Findings entry").

**Fix at the interface, not per-skill:** add a sixth `read` operation (fetch one record + its
Findings trail by id) to backend-resolver.md's table with Local/Git-native columns
(read the TICKET file / `gh issue view --comments`) and a Linear realization in linear-adapter.md
(the `issue(id:)` query + its comments connection — mark `[inferred]`, introspect-first, per that
file's own grounding discipline). Then this skill's Phase 6 phrase becomes accurate as written.

### MAJOR-2 — Phase 1 resume was not generalized: an Option-C native id is a dead end

Phase 1 (SKILL.md:39–42) resolves exactly two id shapes: `tkt-####` (file) and `#NN`/bare number
via `gh issue view` (git-native). But Phase 6 and the Done-when line both promise the close-out
reports the "adapter-native id" (SKILL.md:138, 170), and the argument-hint still reads
"[raw bug report, or a TKT-/#issue id to resume]". A user who captured to Linear gets an id
(e.g. `ENG-123`) that Phase 1 cannot resolve — and Phase 1's explicit rule for an unresolvable id
is "treat it as a fresh report", so handing back the very id the skill reported mints a
**duplicate record**. bug-report has no dedup phase (unlike `issue`), so nothing downstream
catches it.

**Fix:** extend Phase 1's id grammar with the Option-C case (under a ruled Option C, an id in the
adapter's native shape — Linear: `TEAM-###` — resolves via the adapter's read operation, which is
MAJOR-1's missing primitive), and extend the argument-hint. Confirmed the same gap in
`issue`'s Phase 1 (`issue/SKILL.md:42–43`); expect it in `feature` too — fix all three the same
way.

## MINOR findings

### MINOR-1 — Phase 4 bullet naming asymmetry (bolted-on register)

The three Record bullets are labeled "**File backend:**", "**Git-native backend:**",
"**Option C (external, e.g. Linear):**" — two named by backend noun, one by option letter. Phase 0
introduces all three as Options A/B/C; the graft shows at Phase 4. Rename the first two to
"**Option A (file):**" / "**Option B (git-native):**" (or the third to match the noun style).
`issue` and `feature` carry the identical third-bullet phrasing — same cosmetic fix there.

### MINOR-2 — Option-C fallback stated twice; A/B pattern states it once

The Option-C bullet (SKILL.md:96–101) inlines the partway-failure fallback ("A create call that
fails partway falls back to the file backend … never leave the report uncaptured"), and the
Failure branches restate it (SKILL.md:165–167). The established Option-B pattern keeps the
fallback *only* in Failure branches (the git-native bullet at 92–95 carries none). Trim the
Phase 4 sentence to keep parity — the Failure branch and backend-resolver.md's REQ-008 already own
the rule.

### MINOR-3 — Frontmatter description still describes the pre-ADR binary

Description (SKILL.md:10–11): "doc-forge's TICKET path by default, or the workspace's ruled
git-native backend (`gh issue`)" — Option C is absent. Routing is unaffected (bug asks route on
bug language, not backend vocabulary), so this is stale context rather than a routing defect —
but the workspace treats stale context as a defect. If edited, the workspace invariant requires
touching `evals/evals.json` in the same change (a dated note suffices; no case changes look
needed — backend words appear in no prompt). Check the siblings' descriptions for the same
staleness.

### MINOR-4 — Option-C close doesn't name Findings-first where the sibling does

`issue`'s equivalent close clause says "…`references/linear-adapter.md`, **Findings-first, same
ordering**" (issue/SKILL.md:53–56); bug-report's Phase 6 Option-C clause omits the marker. Not a
contract violation (see REQ-006 check below) — add the two words for register parity and to make
the guarantee explicit at the point of close.

## The four dispatch-specific checks

1. **Natural extension of the A/B pattern?** Largely yes — Phase 0 enumerates A/B/C in order and
   at matching detail; Phase 4 adds a third bullet in the established bullet shape; Phase 6 and
   Failure branches extend in place. The graft shows only at MINOR-1 (bullet naming) and MINOR-2
   (fallback stated inline where B keeps it in Failure branches).
2. **Accuracy against the reference files?** Every checkable fact matches: `create` is a real
   interface operation; the fallback discipline mirrors REQ-008 verbatim in spirit; Phase 6's
   status mapping `doing`/`done`/`wontfix` → `started`/`completed`/`canceled` matches
   linear-adapter.md REQ-007 exactly (and correctly binds to state *types*, not names). One drift:
   the "read operation" (MAJOR-1) — an operation-name claim the interface doesn't back. One
   resolver-side note, not a skill defect: Phase 0 says "the ruled option's adapter is
   unreachable → Option A" (correctly preserving the pre-edit "no `gh` → file" behavior for
   Option B), while backend-resolver.md's fallback sentence names only the Option-C-unreachable
   case — backend-resolver.md under-specifies B-unreachable; a one-line addition there closes it.
3. **REQ-006 Findings-first preserved?** Yes, structurally: Phase 6 advances status *only* inside
   the "Findings gained an entry →" branch; both no-entry branches leave status unchanged (append
   the loss entry / re-dispatch). A close can never land on an empty Findings trail under any of
   the three options. Explicit naming would still help (MINOR-4).
4. **Dangling refs / redundancy?** Both cited files exist:
   `doc-authoring-standards/references/backend-resolver.md` and `…/linear-adapter.md`. No phantom
   pointers. One redundant restatement (MINOR-2). Phase 6's bare `references/linear-adapter.md`
   citation is resolvable via Phase 0's possessive ("doc-authoring-standards' backend resolver") —
   acceptable, though Phase 4's fully-qualified form is the better pattern.

## Mechanical + FLOOR checks

- `skill_lint.py`: **clean**.
- Structure: frontmatter complete (`disable-model-invocation: false`, `user-invocable: true`,
  argument-hint present — but see MAJOR-2 for its content); phases ordered 0–6 with Phase 0 as a
  seam paragraph; Failure branches enumerated; single Done-when close. Sound.
- Language register: additions instantiate rather than describe (imperative, "never leave the
  report uncaptured", the em-dash house cadence). Consistent with the surrounding body.
- Routing surface: description unchanged by this edit → no eval obligation triggered;
  `evals/evals.json` (8 positives, 9 adversarial negatives) remains valid — no prompt turns on
  backend vocabulary. MINOR-3 governs any follow-up description edit.
- Cross-plugin boundaries: all new pointers are scribe-internal (doc-authoring-standards is a
  same-plugin sibling) — no hard-boundary violation.

## Sibling applicability (for the parallel audits)

| Finding | issue | feature |
|---|---|---|
| MAJOR-1 (undefined read op) | Needed — its resume-report branch reads records back; phrase "read operation" itself not present, but the missing primitive is shared. Fix belongs in backend-resolver.md + linear-adapter.md once, for all three. | Same — verify its close/read-back phrasing |
| MAJOR-2 (Option-C resume dead end) | **Confirmed** (issue/SKILL.md:42–43, `#NN`/`tkt-####` only) | Expected — verify |
| MINOR-1/2 (bullet naming, inline fallback) | Identical Option-C bullet phrasing confirmed (issue/SKILL.md:112) | Identical (feature/SKILL.md:105) |
| MINOR-3 (stale description) | Verify each | Verify each |
| MINOR-4 | N/A — issue already carries "Findings-first, same ordering" | Verify |
