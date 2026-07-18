# Audit — /issue (scribe) · ADR-0003 Option-C generalization · floor depth · fresh context

Skill: scribe 0.1.0/skills/issue/SKILL.md · Standards: skill-authoring-standards · Lint: clean
Verdict: FIX-FIRST (1 blocking, 1 major, 2 minor, 2 nit — every fix is a clause-level edit, no
restructure; the Option-C additions are otherwise accurate against both reference files and
consistent with the sibling pattern. Ship after fixes.)

**Resolution (2026-07-18, same session):** all findings applied. (1) Description rewritten
(SKILL.md:9–11) to drop the false "everywhere else" binary; evals.json re-checked, no case
changes needed (backend is not a trigger axis), no boundary moved, no /eval-run owed. (2) Phase 1
gained an Option-C id form (an adapter-native id resolves via the new `read` operation, REQ-010 —
added to `spec-linear-adapter` v0.2.0 and both reference files at the SAME root cause all three
siblings shared, rather than patched per-skill). (3) Phase 3's dedup sweep now names the adapter's
`dedup-search` operation. (4) backend-resolver.md's fallback sentence widened to cover both
Option B (`gh` unavailable) and Option C (adapter unreachable). (5)/(6) nits left as-is — cosmetic,
non-blocking, no reader-facing ambiguity. `skill_lint.py` and the plugin's `release_gate.py`
re-run clean after all fixes.

Reviewed: SKILL.md (145 lines, post-edit), git diff vs HEAD, intent.md, evals/evals.json,
doc-authoring-standards/references/backend-resolver.md, .../references/linear-adapter.md.
Siblings read for the shared-seam check: ../bug-report/SKILL.md (Phase 0 + description),
../feature/SKILL.md (Phase 0 + description).
Auditor: fresh-context skill-auditor, 2026-07-18. Lint run: `skill_lint.py` → `clean` (exit 0).
Frontmatter untouched by this edit (diff starts at body line 25), so no same-change evals.json
obligation was *triggered* — but see finding 1, which creates one.

## Dispatch answers, condensed

1. **Natural extension of the A/B pattern?** Yes in four of five touch points. Phase 0
   (SKILL.md:28–38), the Phase 4 Option-C bullet (:112–117), the Option-C failure branch
   (:128–130), and the Done-when clause (:137–139) all mirror the existing A/B ordering, detail
   level, and register — the Phase 4 bullet even reproduces the sibling bullets' "gate sentence
   last" shape. The one dense spot is the Phase 1 insertion (finding 5, nit): accurate, but
   nested two em-dash asides deep inside an already three-clause parenthetical.
2. **Accurate against the reference files?** Yes — no operation-name or field-name drift.
   `create` (:112) is the interface's own operation name; the fallback triple "auth, API error,
   MCP disconnect" (:128–129) matches REQ-008 verbatim; "size … carried as a label" matches
   REQ-004's Size→labels row; the status mapping `doing`/`done`/`wontfix` →
   `started`/`completed`/`canceled` (:53–54) matches REQ-007 exactly, and "a state of the mapped
   type" correctly preserves linear-adapter's type-not-name binding. No overclaiming: the skill
   never promises the `[inferred]` label-field mechanics linear-adapter itself declines to
   hardcode. One scope mismatch runs the other direction — finding 4.
3. **Phase 1 status-mapping clause in the folded-resume location?** Correctly placed, no
   duplication, no contradiction. Phase 4's Option-C bullet covers the `create` operation only;
   Phase 1's clause covers status representation only; the shared linear-adapter.md pointer is
   needed in both. "Findings-first, same ordering" (:55) correctly carries the close discipline
   into Option C, matching linear-adapter's close op (comment lands before the state
   transition). Residual looseness is register-only (finding 5).
4. **Dangling references / redundancy?** Both cited reference files exist at
   doc-authoring-standards/references/. No dangling pointer. The per-phase Option-C clauses
   mildly restate Phase 0's blanket "every phase below follows whichever option the resolver
   returned", but that matches the pre-existing A/B pattern — not a defect. The real gaps are
   the two places the generalization *didn't* reach: the frontmatter description (finding 1)
   and the Phase 1 id grammar (finding 2).

## Findings, severity-ordered

**1. BLOCKING — the frontmatter description still describes the retired binary, and it is now
model-visible routing surface.** SKILL.md:9–11: "Records land on the workspace's ruled backend —
a GitHub Issue (`kind: task` label + optional size) where the entry file rules git-native, a
`kind: task` TICKET file **everywhere else**." Under an Option-C ruling that last clause is false
— records land in the external tracker, not a TICKET file. Since the 2026-07-17 species
conversion (`disable-model-invocation: false`, evals.json's own note) this description enters
model context on every routing decision. The estate's stale-context rule (a change that
invalidates a record repairs it in the same change) makes this same-PR work: the ADR-0003 edit
invalidated the sentence and did not repair it. *Fix:* one clause — e.g. "…where the entry file
rules git-native, a `kind: task` TICKET file by default, or the workspace's ruled external
adapter (ADR-0003, e.g. Linear)". Description edit → touch evals.json in the same change (the
invariant); no *case* changes needed — backend choice is not a trigger axis, all 19 cases stand
— and no boundary moved, so no /eval-run owed. **Cross-sibling:** bug-report's description
("doc-forge's TICKET path by default, or the workspace's ruled git-native backend") and
feature's ("the TICKET file by default, or the workspace's ruled git-native backend") carry the
identical staleness — same fix, all three.

**2. MAJOR — Phase 1's resume-id grammar has no Option-C form, so an Option-C record can be
minted and reported but never resumed.** SKILL.md:42–44 and :64–65 define exactly two id shapes:
`#NN`/bare number (git-native) and `tkt-####` (file). The close-out promises "the issue URL,
ticket path, **or adapter-native id**" (:119) and Done-when promises status-advance works
(:139–140) — but `/issue ENG-123 done` parses as *no leading record id* and falls through to
fresh-item capture: Phase 2 classifies it, Phase 3's dedup sweeps only `gh issue list` and
`docs/tickets/` (finding 3), and the skill mints a junk task titled from the id it should have
resolved. The asymmetry is structural: this skill's whole status-advance design lives in Phase
1's resume branch, so under Option C the folded lifecycle (the thing this skill uniquely owns)
is unreachable. *Fix:* extend the id grammar — "on an Option-C backend, the adapter's native id
form (Linear: `TEAM-NN`, e.g. `ENG-123`) resolves via the adapter; on other backends it is not
an id." *Cross-sibling:* bug-report:39–41 and feature's Phase 1 define the same two-shape
grammar — same gap, same fix, all three.

**3. MINOR — Phase 3 dedup is the one backend-specific phase the generalization skipped.**
SKILL.md:93 names `gh issue list --search` and `docs/tickets/` but not the adapter's
`dedup-search` operation — which backend-resolver.md defines precisely so "a capture skill's own
call sequence never branches on which backend is active" (five-op table). The edit chose
explicit Option-C clauses in Phases 0/1/4/Failure/Done-when; Phase 3 is the odd one out, and
under Option C it is load-bearing (it is the only net against finding 2's junk mint). *Fix:*
three words — "…(`gh issue list --search`, `docs/tickets/`, or the resolved adapter's
`dedup-search`)".

**4. MINOR — fallback-scope drift between the skill trio and backend-resolver.md, resolver side
suspect.** All three skills say "No ruling, or **the ruled option's** adapter is unreachable →
Option A" (issue:32–33) — covering Option B's `gh`-unavailable case, which the pre-ADR text
guaranteed explicitly ("AND `gh` is available"). backend-resolver.md:19 states the narrower "No
ruling, or **Option C ruled** but its adapter is unreachable → Option A". The skills preserve
the pre-ADR semantic; the resolver's sentence would lose it if read as canon. *Fix (resolver
side, one file):* widen backend-resolver.md's fallback sentence to "the ruled option's
realization is unreachable (Option B: `gh` unavailable; Option C: the adapter)" — otherwise the
next drift-check will "correct" three skills into a regression.

**5. NIT — Phase 1 Option-C clause density.** SKILL.md:52–55 nests two em-dash asides inside the
pre-existing three-clause parenthetical hanging off the `wontfix` arm; and the tail
"Findings-first, same ordering" formally attaches to all three verbs though the ordering rule
governs closes only (`doing` is a plain state update — linear-adapter's `update`, no Findings
gate). Accurate but the densest sentence in the file; the mid-clause wrap "same ordering).
Closing a" (:55–56) reads as a paste seam. *Fix (optional):* unpack to its own sentence after
the parenthetical.

**6. NIT — citation-form drift within the file.** Phase 0 cites `` `references/backend-resolver.md` ``
and `` `references/linear-adapter.md` `` (backticked, bare-relative — no `references/` dir
exists under issue itself; the "doc-authoring-standards'" attribution disambiguates), while
Phase 4 writes "(`doc-authoring-standards` references/linear-adapter.md" — plugin backticked,
path bare (:113). Pick one form; the Phase 0 shape matches both siblings.

## Cross-sibling expectation (per the dispatch)

Findings 1 and 2 are structural to the shared edit and should reproduce in bug-report and
feature (both descriptions verified stale here; both Phase 1 grammars verified two-shape here —
the sibling auditors should confirm in situ). Finding 4's fix lands once, in
backend-resolver.md. Findings 3/5/6 are issue-local (Phase 3's command list and the folded
status-advance parenthetical are this skill's own shapes).

## Top 3

1. Repair the description's "everywhere else" clause + touch evals.json, all three siblings
   (finding 1 — blocking, same-change rule).
2. Give Phase 1 an Option-C id form so adapter records are resumable — the folded lifecycle is
   this skill's entire value under Option C (finding 2; siblings likewise).
3. Add `dedup-search` to Phase 3 and widen the resolver's fallback sentence (findings 3 + 4 —
   two one-line edits, one per file).

---
---

*The 2026-07-16 forge audit below is preserved verbatim — intent.md's P5 gate record cites it;
it predates the ADR-0003 edit audited above.*

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
