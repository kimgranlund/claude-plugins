# Audit — /issue (scribe) · floor depth · fresh context

Skill: scribe 0.1.0/skills/issue/SKILL.md · Standards: skill-authoring-standards · Lint: clean
Verdict: FAIL (fix-first — one blocking record-integrity finding, four majors; every fix is small and enumerated; no restructure needed. Ship after fixes.)

Reviewed: SKILL.md (96 lines, desc 913/1024 chars), intent.md, evals/baseline/session-evidence.md.
Siblings read: ../feature/SKILL.md, ../bug-report/SKILL.md.
Auditor: fresh-context skill-auditor, 2026-07-16. Lint run: `skill_lint.py` → `clean`.

## Criteria table

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | SKILL.md:44 (never-closes-silent), :60–62 (dedup), :72–73 (labels created once) — each maps to a measured variance in evals/baseline/session-evidence.md:5–15; deletion would restore the baseline failure | — |
| R2 | N/A | — | Command species, `disable-model-invocation: true` (SKILL.md:14); description never enters model context; skip recorded at intent.md:39–41, matching the siblings' convention | — |
| R3 | PASS | nit | SKILL.md:2,14–15 — command species, both dials explicit, dials/content/menu-doc description agree. Name `issue` is a noun head where command grammar wants an imperative verb, but it matches the shipped sibling convention (`feature`, `bug-report`) | none (convention holds corpus-wide or changes corpus-wide) |
| R4 | PASS | — | Spec-present standing register throughout (e.g. SKILL.md:44, :79–80); uppercase gate budget within 3 (lint W7 clean); locks lowercase (`never re-mint` :38, `never nothing` :67) | — |
| R5 | FAIL | minor | SKILL.md:66–69 — payload contract (Summary·Acceptance·Links·Scope/Open·Findings) restated a THIRD time (feature:83–86, bug-report:68–71) with no drift-pair annotation, unlike the seam paragraph which names its source (SKILL.md:27, "bug-report's rule, shared verbatim") | Annotate the payload block the same way, or hoist it to doc-authoring-standards' TICKET contract and reference it from all three |
| R6 | PASS | — | Whole file ≈1.6K tokens; phases, failure branches (:82–89), stopping predicate (:91–96) all inside the compaction head | — |
| R7 | PASS | major (gap) | Output contract :79–80 + :47; named failure branches :82–89; checkable done/NOT-done :91–96. Gap: no closed-record resume branch — see finding 3 | Add the closed branch |
| R8 | PASS | — | "ONE clarifying question" :55, "one-line reason" :43, "decided once per run" :27, size classes :72 | — |

## Findings, severity-ordered

**1. BLOCKING — intent.md P5 is a falsified gate record.** intent.md:62–67 records "P5 PASS 2026-07-16" citing a "fresh-context skill-auditor report at evals/audit-report.md (verdict PASS, fix-first findings applied…)" — that file did not exist when this audit ran (the directory held only `evals/baseline/`), the named fixes are NOT applied (findings 2 and 6 below are still live in SKILL.md), and the claim "reciprocal NOT-clauses verified in feature/bug-report (both already carry their side)" is false — a grep of both siblings finds no mention of `/issue` or `task` anywhere (finding 5). A pre-written PASS launders an unrun gate; skill-review's own rule is that an unmeasured check is recorded, never laundered as clean. *Fix:* delete the anticipatory P5 entry; re-record P5 with this audit's actual verdict once the fixes below land.

**2. MAJOR — resume verb grammar is not executable when detail starts with a verb token.** SKILL.md:40 ("A status verb — `done` · `wontfix` · `doing` →") vs :45 ("any other trailing text"). `/issue #19 done deal — see the PR comment` starts with `done`: the branch test as written matches the verb branch, closing the issue and fabricating a Findings entry, when the user meant to fold detail. The dispatch's exact probe; unresolved. *Fix:* define the verb branch as *the entire trailing text is exactly one token* in {`done`,`doing`,`wontfix`}, case-insensitive — with the single exception `wontfix <reason>`, where the remainder is the reason (see finding 6). Anything else is detail.

**3. MAJOR — no closed-record resume branch (sibling drift).** SKILL.md:34–49 branches on what follows the id, never on the record's state. Both siblings refuse to touch closed records: bug-report:43 and :126, feature:37–38 — "report and stop; reopening is the user's call." `/issue #19 doing` or `/issue #19 <detail>` against a closed record is unspecified here and would silently edit or re-label a closed issue. *Fix:* prepend a state check to Phase 1 — record already `done`/`wontfix`/closed → report the closed state and stop; reopen only on an explicit ask (the siblings' shared clause).

**4. MAJOR — "hand to bug-report / feature" cannot execute as written.** SKILL.md:53–54 and :86–87. Both targets are `disable-model-invocation: true` (bug-report:15, feature:15), so the Skill tool cannot invoke them mid-run; the model will either fail the handoff or improvise the capture inline without the sibling's contract. *Fix:* name the real mechanism — stop, report the detected shape, and tell the user to run `/bug-report <seed>` (or `/feature <seed>`); nothing is minted here. Note: feature:122 carries the same defect ("hand to `bug-report`") — a sibling fix outside this skill's diff, flag it to the maker.

**5. MAJOR — the siblings' fences do not reciprocate.** SKILL.md:11–13 fences bug-shaped → bug-report and feature-shaped → feature; neither sibling fences the generic remainder back. feature:13–14 and bug-report:12–14 name each other, /build, doc-forge — never `issue`/`task`; feature's Phase 4 shape gate (:71–79) has Work/Knowledge but no "this is a chore, not a feature → /issue" branch. A follow-up typed into /feature gets force-shaped into `kind: feature`. *Fix (sibling-side; one finding, one home):* add `NOT for generic chores/follow-ups/tasks (issue)` to both sibling descriptions plus a routing line in feature Phase 4 and bug-report Phase 2/3 — a description/boundary-tier edit on each (re-budget before adding; feature's description is the tighter one).

**6. MINOR — wontfix reason: source and file-backend home unstated.** SKILL.md:42–43 presupposes "the one-line reason" exists but never says where it comes from — `/issue #19 wontfix` bare has no reason to post. File backend: "a comment" has no file equivalent. *Fix:* reason = the trailing text after `wontfix`; absent → ask once (ONE question, the Phase-2 budget pattern); file backend: the reason lands as the dated `## Findings` close-out entry. The never-closes-silent rule (:44) then covers both verbs completely.

**7. MINOR — payload-contract drift triple.** See R5 row. SKILL.md:66–69 / feature:83–86 / bug-report:68–71.

**8. NIT — bare-number ambiguity.** SKILL.md:36–37: `/issue 3 flaky tests to quarantine` — id `3` + detail, or a fresh item starting with a digit? Shared with siblings verbatim. *Fix (optional):* bare number counts as an id only when it is the entire argument; with trailing text, require `#NN`.

**9. NIT — id case rule dropped.** Siblings state `tkt-####`/`TKT-####` case-insensitive (bug-report:35, feature:35); SKILL.md:37 writes only `tkt-####` while the description's example (:11) is uppercase `TKT-0044`. Add the two words.

## Dispatch answers, condensed

1. **Sibling consistency:** seam matches verbatim in substance (the explicit "No ruling, or no `gh` → file backend" tail sentence is elided but implied — no contradiction); payload contract matches (drift-triple annotation missing, finding 7); resume semantics genuinely diverge — issue dispatches on trailing text where siblings dispatch on record state, a deliberate design (intent.md ruling 1) except the missing closed-record guard (finding 3).
2. **Phase-2 gate:** criteria crisp ("X is broken"/repro vs new-capability/needs-sizing vs remainder, ambiguity → capture as task — good persistence-beats-taxonomy default); the handoff *verb* is not executable (finding 4); reciprocity absent in siblings (finding 5).
3. **Resume grammar:** not executable at the `done`-prefix boundary (finding 2).
4. **Findings-first close:** complete for `done` (the :44 never-closes-silent rule is the strongest line in the file); `wontfix` reason under-specified (finding 6).
5. **Species conformance:** preconditions (seam + id resolution) gated with named branches; report format present (:47, :79–80); escape hatches present (:47, :55–56); stopping predicate checkable with NOT-done clauses (:91–96) — conformant. No `allowed-tools` grant (siblings likewise; shared convention, not scored).
6. **Budgets:** description 913/1024; body 96 lines / ≈1.6K tokens. Clean.

## Top 3

1. Rewrite intent.md's P5 entry to record reality; re-gate after fixes (finding 1 — blocking).
2. Make the resume grammar executable: verb = whole trailing text, single token, `wontfix <reason>` exception (findings 2+6 — one edit).
3. Add the closed-record guard and the real handoff mechanism; open a sibling-side change for the reciprocal fences (findings 3, 4, 5).
