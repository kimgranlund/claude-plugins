---
doc-type: lld
id: lld-0003-adr-0012-allow-rule-verification
status: draft
version: 0.2.0
date: 2026-08-15
owner: kim.granlund
ticket: nonoun-plugins#256
adr: adr-0012 (verifies its named deployment prerequisite; both outcome addenda pre-drafted in D2)
---
# LLD — Verify the ADR-0012 `autoMode.allow` rule live: one real quick-build test dispatch (#256)

*Amended 2026-08-15 (v0.2.0) per docs:doc-checker's fix-then-ship review, before any dispatch:
C3's test issue re-kinded `task` → `feature` (MAJOR — the task path's one sealed child dispatch
can never carry the grant under stage 2b's non-inheritance rule, so QB0 was structurally
unreachable; feature+small builds inline in build-lead's own granted context); I2's silent
branch gains that wrong-kind cause as its likeliest tell; the estate README claim corrected
(authorkit already carries `## Version ledger` — six of eight lack it, not all); D2's addendum
dates made slots.*

**Verdict, head-first: the test vector is a real stale-context fix, not ceremony** — the
parenthetical in `dispatch-ticket` Phase 5 stage 2b itself still says the classifier blocks
`gh pr merge` "until Kim arms a scoped allow-rule", and Kim armed it in commit 40dd5c3
(2026-08-14). Repairing that line is a genuine defect fix (stale context = defect), sits squarely
in QB4 class (a) (SKILL.md body-only), and is useful whichever way the experiment lands.

**Two findings this research surfaced that the test cannot proceed without:**

1. **QB3 is indeterminate in six of the eight plugins today — teamwork included.** QB3's
   ride-along check reads "every changed hunk in `README.md` starts at or below the version-ledger
   heading … no ledger heading found → indeterminate → out" — and only `authorkit/README.md`
   carries one (`## Version ledger`, line 79; grepped all eight, 2026-08-15, corrected per
   doc-checker review — the first pass missed authorkit and claimed zero). Teamwork's ledger
   entries sit headingless after the `## Evals` prose. Without prep (C1), the dispatch fails QB3
   before `gh pr merge` is ever attempted and the run answers nothing about the classifier.
2. **The grant literal is `auto-merge: authorized` — WITH the space.** Issue #256's own body (and
   this ticket's dispatch prose) spell it `auto-merge:authorized`; the normative spelling in
   ADR-0012 D4, stage 2b, mobilize-chores step 5, and the settings rule has the space. A sealed
   prompt carrying the space-less spelling makes QB0 silently absent — stage 2b "does not exist",
   the PR waits for a human, and the observer could misread a no-op as a classifier verdict. I2's
   taxonomy encodes the tell.

The four research answers, verdict-first:

1. **Candidate:** the stage-2b stale-parenthetical fix in
   `teamwork/skills/dispatch-ticket/SKILL.md` (C2) — one substantive body-only SKILL.md edit,
   one plugin, ride-alongs only, genuinely needed either way.
2. **Observation:** run the REAL production path unattended (`/goal` wrapping
   `/mobilize-chores auto` scoped to the test issue) so the auto-mode classifier is actually
   engaged; distinguish outcomes by the typed handoff's fields plus independent re-query, never
   by the seat's prose alone (I2, D1).
3. **Rollback:** an unwanted auto-merge is an ordinary PR revert with a bounded, designed blast
   radius — one QB4-class file in one plugin — plus two independent revocation levers (R1).
4. **Recording:** both terminal addenda are pre-drafted verbatim in D2; predicate-miss and
   unverified outcomes are explicitly NON-terminal (re-run or investigate, no addendum).

## Components

### C1 — Prep change (BEFORE dispatch, human-landed): give teamwork's README a ledger heading

Insert a `## Version ledger` heading (plus one blank line) in `teamwork/README.md` immediately
above the first ledger entry (`v2.12.1 · 2026-08-14 · …`, line 86 at time of writing). The
heading text follows the in-estate precedent — `authorkit/README.md:79` uses exactly `## Version
ledger`, which is also how QB3's evaluator will recognize it. Without the heading QB3 is
indeterminate → the whole test invalid (finding 1 above).

- **Not quick-build-eligible itself** (README.md is a QB3 ride-along; a README-only change has
  zero substantive files) — land it as an ordinary solo single-file fix committed to main
  (ADR-0002's standing precedent) or a tiny human-merged PR, BEFORE the test dispatch. Never
  fold it into the test PR: the heading must pre-exist on `origin/main` so the test diff's
  README hunks sit unambiguously below it.
- Five other plugin READMEs share the gap (authorkit already has the heading). Out of scope
  here; file a follow-up issue ("six of eight plugin READMEs lacked the version-ledger heading
  QB3 anchors on; teamwork fixed by #256 prep, five remain") after the test.

### C2 — The candidate test change (the substantive file)

`teamwork/skills/dispatch-ticket/SKILL.md`, body-only, one contiguous edit (current lines
294–295). Old text:

> `campaign_close`'s summary line. A denial at step 2 (the unattended permission classifier still
> blocks `gh pr merge` until Kim arms a scoped allow-rule) or any later failure → the named

New text:

> `campaign_close`'s summary line. A denial at step 2 (possible if the scoped `autoMode.allow`
> rule — armed 2026-08-14, commit 40dd5c3, matched to exactly this predicate — does not cover the
> command, or has been revoked) or any later failure → the named

Outcome-neutral by design: accurate whether the rule clears the block or not. Ride-alongs:
`teamwork/.claude-plugin/plugin.json` 2.12.1 → 2.12.2 (version line only) and one ledger entry
under C1's new heading. QB conjunct fit: QB1 via C3's label; QB2 all three paths under
`teamwork/`; QB3 exactly one substantive file, ride-alongs in R and diff-clean; QB4 class (a) —
the hunk sits ~280 lines below the closing frontmatter `---`; QB5 the dispatch's own
fresh-context critic (skill-checker — this is a semantic SKILL.md edit); QB6 gate + CI; QB7
pre-checked by the coordinator (I1 step 3).

**Self-reference, examined not waved off:** the edit touches stage 2b's own prose while a seat
executes stage 2b. Safe because the executing seat's instructions load from the INSTALLED plugin
at dispatch time, not from the PR branch — unlike QB4 class (c)'s excluded gate scripts, which
would RUN during their own evaluation, prose never executes. The edit changes a factual
parenthetical, not a conjunct, and QB5+QB6 still grade it. (R2.)

### C3 — The test issue (minted BEFORE dispatch — QB1 reads its labels)

`gh issue create` on kimgranlund/claude-plugins, labels `feature` + `size:small` — **feature,
NOT task, and this is load-bearing** (doc-checker MAJOR, verified against the SKILL): the task
kind builds via ONE sealed child dispatch (`dispatch-ticket` Phase 2, "A task is ONE sealed
dispatch" via the Agent tool), and stage 2b's non-inheritance rule ("a seat that received the
grant does not pass it to a child it spawns") means that child — the seat that opens the PR and
evaluates stage 2b — structurally cannot carry the grant: QB0 absent, test dead on arrival. The
feature path at `size:small` reads "the host builds it inline" (Phase 4), so `build-lead` itself —
whose sealed prompt from mobilize-chores step 5 carries the grant — is the seat stage 2b runs in:

- **Title:** dispatch-ticket stage 2b: stale "until Kim arms a scoped allow-rule" parenthetical —
  the rule was armed in 40dd5c3
- **Body:** the C2 old→new edit spec verbatim; acceptance = edit applied body-only + teamwork
  2.12.2 bump + ledger entry + recorded critic verdict + gate green; **plus one test-specific
  line: "If stage 2b evaluates and `gh pr merge` is denied, QUOTE THE VERBATIM DENIAL TEXT in the
  Findings comment"** — the raw material D1's classification needs, requested where the seat will
  actually see it. Reference #256 as the observing ticket; do NOT put `Closes #256` anywhere —
  the test PR closes only the test issue, #256 stays open until the addendum lands (Phase 6 of
  #256 is the coordinator's, not the seat's).

### C4 — The dispatch vector: the real production path, unattended

`/goal` wrapping `/mobilize-chores auto <scope: only issue #<test-id>>` — the leading `auto`
token is Kim's explicit unattended grant (2026-08-11 doctrine) and the scope instruction pins the
sweep to the one test issue.

Why this vector and not a direct attended dispatch: the recorded block
(`auto-mode-gh-permissions`, 2026-07-30) bit during **unattended /goal runs** — the same denial
did NOT apply when Kim typed the merge himself. `autoMode.allow` is by name an auto-mode rule. An
attended dispatch would either prompt Kim or bypass the classifier entirely, proving nothing.
The unattended mobilize-chores path also exercises the production grant placement: its step 5
writes the literal `auto-merge: authorized` line into the sealed build-lead prompt on the
UNATTENDED branch only — the exact chain a real overnight quick-build will run. No hand-built
sealed prompt, no bespoke test scaffolding.

### C5 — Recording (coordinator, after observation)

Append the matching D2 addendum to ADR-0012's Consequences section (append-only — doc_lint T4
permits appending to an accepted ADR; the Decision text is never touched), then close #256 with a
dated Findings comment linking the test issue, the PR, and the addendum commit. Also repair the
sibling stale line found during research — `teamwork/skills/mobilize-chores/intent.md:304` ("still
blocks `gh pr merge` until Kim arms a scoped allow-rule") — in the recording pass or a follow-up
(intent.md is QB4-unlisted, so it could never ride the test PR anyway).

## Interfaces

### I1 — Run procedure (coordinator timeline)

1. Land C1 (ledger heading) on main; verify with
   `grep -n "^## Version ledger" teamwork/README.md`.
2. Mint C3; verify `gh issue view <id> --json labels` shows `size:small`.
3. Pre-clear QB7: `gh pr list --state open --json number,files` — no open PR touches
   `teamwork/`; hold any new teamwork PRs until the test closes (R4).
4. Start the unattended run: `/goal` → `/mobilize-chores auto` scoped to the test issue (C4).
5. Observe per I2. Budget: **max 2 dispatch attempts** — the first, plus one re-run only after a
   predicate-miss or inconclusive outcome whose setup cause was fixed; a real classifier denial
   is terminal on the first attempt (never retried into eligibility — stage 2b's own rule).
6. Record per C5.

### I2 — Observation procedure: what each outcome looks like from the coordinator's seat

The primary signal is `build-lead`'s typed retirement handoff (relayed verbatim per its return
contract) plus the durable artifacts — Findings comments on the test issue and the PR itself —
which survive even a lost seat transcript (if only idle notifications arrive, read the
`agent-*.jsonl` files per the `subagent-output-recovery` memory; the issue/PR record is the
fallback of record either way).

**Success** — the handoff carries three extra fields: `merge-sha: <sha>` ·
`campaign-close: <summary>` · `qb-snapshot: <eight observed conjunct values>`. Verify
independently, never trusting the seat's print (the ADR's own step-3 doctrine, applied one level
up):

- `gh pr view <pr> --json state,mergeCommit` → `MERGED` + non-empty SHA
- `gh api repos/kimgranlund/claude-plugins/branches/<branch>` → 404 (campaign_close's deletion)
- `gh issue view <test-id> --comments` → the dated qb-snapshot Findings comment

**Predicate miss (non-terminal, test-invalid)** — the handoff names the failed conjunct
(`QBn`), PR open, no merge attempted. The classifier was never tested; fix the setup cause and
spend the second attempt. Most likely culprits: QB3 (C1 not landed), QB7 (a stray teamwork PR).

**Classifier denial (terminal for "still blocked")** — the handoff names `auto-merge-denied`
with all eight conjuncts green in the snapshot; the Findings comment quotes the verbatim denial
text (C3's test-specific acceptance line). Classify per D1 and record addendum B.

**Silent on auto-merge (non-terminal, test-invalid)** — the handoff says nothing about
auto-merge at all → QB0 never fired → the grant line never reached the prompt of the seat that
opened the PR. Three known causes, in likelihood order: (a) the test issue was task-kind, so the
PR-opening seat was a grant-less sealed child (C3's kind rationale — non-inheritance is working
as designed, on the wrong dispatch shape); (b) finding 2's spelling trap (`auto-merge:authorized`
without the space); (c) step 5's unattended branch didn't run because the session wasn't actually
unattended. Check kind, spelling, and run mode in that order; fix; second attempt.

**`auto-merge-unverified` (non-terminal, investigate)** — merge attempted, `MERGED`+SHA never
confirmed by re-query. Resolve the PR's true state by hand before any addendum; do not classify
as either terminal outcome until the re-query question is answered.

**A permission prompt reaches Kim live** — the session was not in auto mode; the classifier was
bypassed, not tested. Inconclusive; re-run under the `/goal` wrapper.

## Data

### D1 — Denial classification rubric (feeds addendum B's `<reading>` slot)

| Reading | Evidence in the verbatim denial text |
|---|---|
| `hard_deny` | Names the action as reserved for the user / never permitted for agents, with no sign any allow rule was consulted — or byte-identical to the 2026-07-30 observed denial. Meaning: `autoMode.allow` cannot arm this path; escalate past settings. |
| `rule-not-matched` | Shows the policy/allow rules were evaluated but this command didn't qualify. Meaning: the rule's WORDING failed, not the mechanism — next step is rewording 40dd5c3's rule text (never widening it), then one more test. |
| `other` | Anything else — quote it in full in the addendum and decide the next step from the text, not from memory. |

### D2 — Pre-drafted ADR-0012 addenda (append to Consequences; fill `<>` slots; pick exactly one)

**Addendum A — the rule works:**

> - **<date> addendum (#256) — deployment prerequisite CLOSED, verified live.** The scoped
>   `autoMode.allow` rule (commit 40dd5c3) cleared the classifier in a real quick-build: issue
>   #<N>, PR #<P>, all eight conjuncts observed green (qb-snapshot in the Findings comment),
>   `gh pr merge --squash` succeeded inside an unattended `/mobilize-chores auto` run, `MERGED`
>   plus merge SHA `<sha>` confirmed by independent re-query, `campaign_close.py` verified the
>   branch deletion. The "until Kim adds a scoped allow-rule" consequence above is now history;
>   the quick-build path is live end to end.

**Addendum B — still blocked:**

> - **<date> addendum (#256) — the allow-rule did NOT clear the block; the prerequisite
>   stays OPEN.** In a real quick-build (issue #<N>, PR #<P>, all eight conjuncts observed green)
>   the unattended classifier still denied `gh pr merge`. Verbatim denial: "<quoted text>".
>   Reading: <hard_deny — the classifier refuses this command class regardless of
>   `autoMode.allow`, so no settings rule can arm this path | rule-not-matched — the rule was
>   consulted but its wording failed to match; next step is rewording commit 40dd5c3's rule text,
>   never widening it | other — see the quoted text>. The path degraded exactly as designed —
>   `auto-merge-denied` named in the handoff, PR left standing, a human merged: the fail-safe
>   claim above is now verified under live fire, not just asserted.

Predicate-miss / silent / unverified outcomes get NO addendum — they are re-run or investigate
states (I2), and writing one would record a test that didn't happen.

## Risks

- **R1 — an unwanted auto-merge on a mis-scoped candidate (the designed answer, not an
  assumption).** Containment is layered by construction: QB0–QB7 is a fail-closed conjunction;
  QB4's allow-list caps the worst case at ONE body-only/reference/skill-script file in ONE
  plugin — nothing in those classes can grant permissions, alter gates, or execute during its own
  merge (the executing-script class is QB4(c)-excluded). If one lands anyway: (1) the qb-snapshot
  Findings comment shows which conjunct mis-evaluated — auditing is a grep; (2) rollback is an
  ordinary human-merged revert PR (`git revert <merge-sha>`) with version re-bump + ledger entry
  riding it; (3) incident → infrastructure same day — the mis-evaluated conjunct becomes a
  fixture/lint before anything else ships. Two independent revocation levers stand regardless:
  delete the settings rule; stop placing the grant line (each alone kills the path).
- **R2 — self-reference of the candidate** (edits stage 2b's prose while a seat runs stage 2b):
  analyzed in C2 — installed-plugin instructions, prose never executes, factual parenthetical
  only, critic + gate still grade it. Residual risk accepted.
- **R3 — the spelling trap** (finding 2): mitigated by using mobilize-chores' own step-5 grant
  placement (C4) rather than a hand-written sealed prompt, and by I2's "silent on auto-merge"
  tell if it happens anyway.
- **R4 — QB7 TOCTOU** (ADR-0012's accepted risk): during the test window, additionally mitigated
  by I1 step 3's hold on new teamwork PRs. Accepted beyond that, as the ADR rules.
- **R5 — mode confusion**: an attended run silently tests nothing (I2's prompt-reaches-Kim
  branch). Mitigated by the `/goal` wrapper being part of the vector, not optional.
- **R6 — scope creep in the sweep**: `/mobilize-chores auto` unscoped would dispatch every
  mobilizable ticket. The scope instruction pinning it to the test issue is load-bearing; verify
  the step-6 report lists exactly one dispatch.
- **R7 — the QB3 estate gap outlives the test**: C1 fixes teamwork only. The follow-up issue
  (C1) is the record that keeps the other six READMEs from silently failing the next quick-build.
