Skill: orchestration 0.1.0/skills/session-close · Standards: skill-authoring-standards · Lint: clean
Verdict: FAIL (one blocking finding — B1; fix is one clause)

Floor review (post-write independent check), 2026-07-19, second pass. This report SUPERSEDES the
prior same-day audit that occupied this path (FIX-FIRST verdict); every prior finding was
re-verified against the current tree and dispositioned below — two were fixed in the interim, one
was dismissed on runtime evidence, the rest stand. Paths are relative to the worktree root
`/Users/kimba/Projects/nonoun/plugins/.claude/worktrees/session-close-skill/`.

Mechanical gates run for real this pass: `skill_lint.py` → clean · `eval_check.py` → clean ·
`session_end_worktree_check.py selftest` → 4/4 fixtures pass, exit 0. (`potency_lint.py`, which
both intent.md P4 and the prior report cite as a gate, exists nowhere in the tree — see M2; the
potency counters live inside `skill_lint.py`, which is clean.)

## Findings

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| B1 | FAIL | **blocking** | SKILL.md:28–29: "Clean on all three → skip to step 5 with 'nothing to capture.'" Git-cleanness is a fact about the TREE, not the SESSION: a read-only session carrying a third-time correction (exactly the signal step 3 exists for, and exactly the gap the busy-session baseline names) reaches step 5 and states a FALSE "nothing to capture" verdict — the skill reproduces its own baseline failure whenever the knowledge signal arrives without git state. Contradicts intent.md:28–30's own delta claim. Steelmanned: "real work behind it" in the description doesn't save it — the clean-session baseline (evals/baseline/scenario-clean-session.md:4–5) is read-only Q&A, and a fully-pushed tree can co-occur with an uncaptured correction | One clause at :28–29: "Clean on all three → skip step 2; steps 3–5 still run." (Carried from prior audit MAJOR-1 — verified still unfixed) |
| M1 | FAIL | major | Live-suite routing collision on the flagship phrase: session-close evals t06 "Make sure nothing's left hanging before I go." → trigger, vs open-questions-sweep evals t05 "Let's make sure nothing's left hanging before I go." → trigger for oqs (both verified present in both suites this pass). Near-verbatim prompts, opposite owners; the phrase is also verbatim in the description (SKILL.md:8) | Anchor t06 and the description phrase with repo state, the same move as oqs n11 ("…left hanging **in the worktree** before I go"), or cede the bare phrase to one owner with a reciprocal no-trigger in the other suite; then `/eval-run` orchestration + forge. (Carried from prior audit MAJOR-2 — still open) |
| M2 | FAIL | major | Record integrity, intent.md. Verified claim-by-claim: (a) :2 `status: shipped` while the skill is unmerged pre-ship work; (b) :96–97 P5.2 cites this audit "for findings and fixes applied" — B1 and M1 fixes were NOT applied (both re-verified open); (c) :98–103 P5.3 behavior-check runs have no artifact anywhere in the tree — UNVERIFIED, not PASS; (d) :88 P4 cites `potency_lint.py` — `find` over the whole tree: the script does not exist (counters live in skill_lint.py); (e) :86 P3 claims "92 lines" — `wc -l`: 89. Now-true parts, verified: the oqs fence + n11 case landed, and concurrency-design's return pointer EXISTS (concurrency-design/SKILL.md:19) — the prior audit flagged it missing; fixed in the interim | Set status to draft/in-review; mark P5.2/P5.3 pending until each is actually done (record the behavior-check runs as artifacts or drop the claim); s/potency_lint.py/skill_lint.py potency tier/; fix the line count. (Narrowed from prior audit MAJOR-3) |
| m1 | FAIL | minor | Third verdict shape + duplicate case ownership: SKILL.md:55–56's "nothing to check" is a shape outside the two-shape contract (:46–48) and outside intent.md assertion 1 (:49–50); and its "repo has no changes of any kind" clause IS step 1's clean case, already mapped to "nothing to capture" at :28–29 — same condition, two outputs | The no-git-repo branch wears the clean-verdict shape with a reason ("nothing to capture — not a git repo"); delete the "no changes" clause from the branch. (Merges prior MINOR-1 and this pass's independent find; B1's fix makes the ownership cleaner still) |
| m2 | FAIL | minor | Fence misattributes authoring ownership: SKILL.md:12–13 "knowledge-harvest owns authoring" — knowledge-harvest's own description fences authoring OFF: "NOT authoring content once confirmed (knowledge-forge)" (forge 1.14.0/skills/knowledge-harvest/SKILL.md:12). Same drift in intent.md:45–46 and :132. Routing still lands (harvest re-routes), but the routing surface states a claim its target denies | Reword: "knowledge-harvest owns the confirm-and-mint pipeline; this only triggers its detection" — don't attribute authoring to a skill that fences it to knowledge-forge |
| m3 | FAIL | minor | Read-back gate coverage hole: step 4 (SKILL.md:40) reads "every write this step just made" — step 4 makes no writes (steps 2–3 do), and the enumerated read-backs (`git log`, `gh issue view`, `gh pr view`) omit the knowledge-pack file write the verdict example counts as a capture item (:43, :73). Steelmanned ("harvest verifies its own writes"): rejected — :66–67 says a verdict "is only as true as what step 4 actually verified", so an item in THIS verdict needs THIS gate's coverage | "Read back every write steps 2–3 made — `git log`, `gh issue view`, `gh pr view`, and a Read of any minted knowledge-pack path" |
| m4 | FAIL | minor | No branch for scribe absent: step 2 (SKILL.md:31–32) forbids the raw-`gh` fallback while depending on cross-plugin skills; workspace invariant requires named mentions to degrade gracefully. Precedent for the fix exists in the target itself: bug-report SKILL.md:59 "Where intent-extract is not installed, apply its discipline inline" | Add a branch: capture skills unavailable → file via raw `gh issue create` applying their discipline inline; verdict names that the dedup sweep was skipped |
| n1 | note | nit | One-directional pair docs: the SessionEnd hook's docstring names this skill (scripts/session_end_worktree_check.py:9); the skill's References table (:82–89) never names the hook. Scoping itself is correct — see Q4 below | One References row: the hook is the passive net when this skill never ran; warnings land in `${CLAUDE_PLUGIN_DATA}/session-close-warnings.log` |
| n2 | note | nit | knowledge-harvest's own suite has no session-close no-trigger case (grep over its evals/evals.json: no match); session-close's n05 covers one direction only | Add a "wrap up this session…" no-trigger there at the next boundary-edit wave — not owed by this change alone |

## R-criteria summary

R1 pass (SKILL.md:33–34, :40–41, :52–54 all survive deletion) · R2 fail → M1, m2 · R3 pass
(procedural, verb-head, dials explicit :14–15) · R4 pass-with-m3 (one hard gate, :64–67) · R5 pass
(references, never restates — :31–32, :86–87; m2 is the one drift pair) · R6 pass (contract :46–48,
gates :63–67, example tail, refs one level, 89 lines) · R7 fail → B1, m1, m4 · R8 pass ("stays
one" :34, "one of two shapes" :42, three checks :26–28). Description 928/1,024 chars (counted).

## Dispatch questions, answered

1. **Skill-tool-invoking-Skill-tool (steps 2–3): sound.** All four targets verified
   `disable-model-invocation: false`; none carries `context: fork` or `agent:` — bodies load
   in-context as standing instructions, no subagent boundary, no authority ambiguity; SKILL.md:31–32
   explicitly cedes contract authority to the invoked skills, and the house pattern is identical on
   scribe's side (bug-report:75, feature:152/157, issue:74/146, per the prior audit — spot-confirmed).
   Residual: a future dial flip on a target silently breaks the call; m4's branch absorbs it.
2. **Failure branches vs contract: no branch exits verdict-less** (branches 1, 3, 4 all fold into
   the verdict), but branch 2 leaks a third shape past the two-shape contract — m1.
3. **The one hard gate: instantiated, not just asserted** — it binds in three places (step :40–41,
   branch 4 :60–61, stopping predicate :64–67), which is the maximum enforcement a skill body has.
   Its coverage has the m3 hole (knowledge-pack writes unenumerated).
4. **Companion hook: present, green, correctly scoped, non-overlapping.** Both artifacts exist;
   selftest run this pass: 4/4, exit 0. Hook is passive (always exit 0 — SessionEnd cannot block,
   per its own cited doc check), logs to `${CLAUDE_PLUGIN_DATA}`, never the repo; the skill owns all
   judgment. intent.md:112–120 scopes the split correctly. Docs reference is one-directional — n1.

## Prior-report dispositions (evidentiary symmetry)

- **MAJOR-1 → carried as B1** (re-verified open, escalated: the false-verdict path makes it blocking).
- **MAJOR-2 → carried as M1** (both suite cases re-read this pass; still colliding).
- **MAJOR-3 → narrowed to M2**: the concurrency-design pointer it flagged missing now EXISTS
  (concurrency-design/SKILL.md:19 — read, not trusted); the oqs closure landed (its SKILL.md:15–16 +
  n11); the rest of the record-integrity finding stands, plus the new potency_lint.py phantom.
- **MINOR-1 → merged into m1.**
- **MINOR-2 → DISMISSED on runtime evidence**: bug-report self-skips its interactive round on
  "a scheduled/unattended firing" (bug-report SKILL.md:59–62, read this pass) and feature does the
  same (feature SKILL.md:132–134); step 2 cannot hang unattended, so branch 1's deferring only
  step 3 is consistent as written.
- **MINOR-3 → folded into M2(e).**
- Prior report's own "potency_lint.py within budget" gate claim: UNVERIFIABLE — no such script
  exists; superseded by this pass's skill_lint clean run.

## Blocking

- **B1** — the step-1 short-circuit skips the knowledge scan; one clause fixes it.

## Nice-to-haves, severity-ordered

M1 (suite collision) · M2 (intent.md record) · m1 (third verdict shape) · m2 (authoring
misattribution) · m3 (read-back hole) · m4 (scribe-absent branch) · n1 (hook References row) ·
n2 (harvest-suite reciprocity, next wave).

Top 3: 1) B1 — "Clean on all three → skip step 2; steps 3–5 still run." 2) M1 — anchor the
"left hanging" phrase with worktree/repo state in t06 + the description, then `/eval-run` both
plugins. 3) M2 — intent.md re-recorded to reality (status, P5.2/P5.3, potency_lint.py phantom,
line count).

Maker applies the fixes; re-run `skill_lint` + `/eval-run` after M1's description edit.
