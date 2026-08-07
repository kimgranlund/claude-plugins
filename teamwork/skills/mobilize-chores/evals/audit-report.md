# check-skill audit — mobilize-chores (FLOOR)

Skill: /Users/kimba/Projects/nonoun/plugins/teamwork/skills/mobilize-chores/SKILL.md · Standards: skill-writing-rules · Lint: clean
Verdict: FAIL (one blocking finding)

Audited 2026-08-07 against `check-skill` + `skill-writing-rules` + `checking-rules`, with the
intent record (intent.md) read for design context. All runtime claims below were checked against
`gh version 2.97.0 (2026-07-31)` on the live workspace repo.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | FAIL | **blocking** | SKILL.md:30-33 — both step-2 mechanics are invalid against real `gh` 2.97.0. (a) `--json number,title,labels,linkedBranches` errors: `Unknown JSON field: "linkedBranches"` (verified by running it; the field is not in `gh issue list`'s field set). Step 2 dies every run → the skill's entire delta (mobilize) never executes; the "unreachable → UNMEASURED" branch (:57) launders it into a permanent sweep-only degrade. (b) `gh pr list --search "linked:<id>"` — GitHub's `linked:` qualifier accepts only `pr`/`issue`, never an id; the query silently returns wrong/empty results → every ticket reads as not-in-flight → double-dispatch, the exact hazard step 2 exists to prevent, failing *silently* | Rewrite step 2 with verified mechanics: `gh issue list --state open --label feature --json number,title,labels` (same for `bug`); in-flight check = `gh issue view <id> --json closedByPullRequestsReferences` non-empty (field verified present and returning on this repo). Before shipping, verify against one live issue with an open linked PR that the field includes open PRs; if it proves closed-only, fall back to `gh pr list --state open --search "<id> in:body"` |
| R1 (delta) | PASS | — | Sampled 3 load-bearing lines beyond the broken mechanics: :41-43 (one batched confirm, nothing dispatches before it) — deletion → per-item confirms or auto-dispatch; :44-47 (dispatch by kind, bug→file-bug never build-feature) — deletion → default routes bugs to build-feature, which redirects (verified: build-feature/SKILL.md:24 "`kind: bug` → this is file-bug's work, hand it over"); :55-56 (sweep fails → never run 2-6). All three survive | — |
| R2 | N/A | — | SKILL.md:14 `disable-model-invocation: true` — the description never enters model context; per skill-writing-rules it is slash-menu documentation. Nit: it is written in full trigger-contract register (~900 chars of fences and phrasings) where the standard says spend zero trigger keywords; harmless here since the fences double as human menu docs | Optional trim, never blocking |
| R3 | PASS | — | Command species story consistent three ways: side-effectful human-timed workflow (:22-24), dials explicit `true`/`true` (:14-15), imperative-verb name head `mobilize-`. Not preloaded anywhere (command species is un-preloadable and none references it) | — |
| R4 | PASS | — | Standing spec-present register throughout: "Nothing dispatches before this round returns" (:43), "Every dispatch is independent; one failing never blocks the others" (:47), "ambiguity is never a license to dispatch" (:60). Lint clean → W7 gate count within budget; uppercase salience spent only on ONE/BOTH/NOT-done emphasis | — |
| R5 | PASS | nit | Wraps `/sweep-chores` by reference, never reimplements (:22-24, :28-29 — verified sweep-chores owns `.claude/ops/plan.md`, sweep-chores/SKILL.md:24,42). Nit: build-feature's bug-redirect rationale is restated three times (:6-7, :45-46, :67-68) — a drift trio against build-feature/SKILL.md:24; one statement in step 5 suffices | Keep the step-5 parenthetical; cut the description and Done-section repeats |
| R6 | PASS | — | 68-line body; procedure, failure branches, and stopping predicate all in the head, no tail examples needed; zero `references/` (correctly, under the split threshold) | — |
| R7 | PASS | — | Output contract :48-51 (verdict-first, table of every ticket CONSIDERED with per-ticket disposition); 4 named failure branches :53-62; checkable stopping predicate + NOT-done clauses :64-68 matching intent.md's 4 assertions | — |
| R8 | PASS | minor | Anchors present: "ONE AskUserQuestion round — never per-ticket" (:41-42), "0 tickets mobilizable" (:38). Minor: the label→kind mapping is implicit — step 2 filters by *label* (:32), step 5 dispatches by *kind* (:44); a ticket carrying both `feature` and `bug` labels has no named disposition (the ambiguity branch :59-60 plausibly covers it, but doesn't name the label-set case) | Add one line: "kind = the ticket's single `feature`/`bug` label; both or neither → the ambiguity branch (exclude)" |

Secondary finding, no rubric row: **allowed-tools omits the pr-list verb.** SKILL.md:17 grants
`Bash(gh issue list *)` and `Bash(gh issue view *)` but step 2 (:33) runs `gh pr list` —
a mid-run permission prompt in the middle of the discovery step. Severity: minor. Fix travels
with the R1 rewrite: grant exactly the verbs the fixed step 2 uses (per skill-writing-rules'
Command rule, `allowed-tools` pre-approves exactly the workflow's verbs).

## Dismissed findings (checks named, per checking-rules)

- **"The `feature` label doesn't exist in this repo, so the filter can never match"** — drafted,
  then dismissed. Check: `gh label list` shows only GitHub defaults (no `feature`), but
  file-feature/SKILL.md:100 ("labels `feature` + `size:small`/`size:big`") and
  file-bug/SKILL.md:88 ("labels `bug` + the severity") prove `feature`/`bug` IS the estate's
  filing convention — the label appears when the first such ticket is filed. Environment state,
  not a skill defect. (Steelman-pass proof: this is the finding whose author-rebuttal survived,
  so it was dropped before filing.)
- **"file-bug resume path may not dispatch investigation as claimed"** — dismissed. Check:
  file-bug/SKILL.md:4 ("then dispatch the investigation"), :7 ("resumes"), :30-38 (resume routing
  by record state). The claim at SKILL.md:7 and :45-46 is accurate.
- **"`allowed-tools` restricts the skill from running `/sweep-chores`"** — dismissed. Check:
  skill-writing-rules' frontmatter rule — `allowed-tools` grants, never restricts; `Skill` is
  granted at :17 anyway.

Steelman on the blocking finding: could `linkedBranches` work on a newer gh, or `linked:<id>` be
valid search syntax? Ran both against gh 2.97.0 (released 2026-07-31, current): the field is
rejected outright, and GitHub's documented `linked:` qualifier is value-less (`linked:pr`/
`linked:issue` only). The finding survives its rebuttal.

## Top 3

1. **(blocking)** Step 2's discovery/in-flight mechanics are fictional against real `gh` —
   `linkedBranches` is not a `gh issue list` field and `linked:<id>` is not a search qualifier.
   Rewrite with `--json number,title,labels` + `closedByPullRequestsReferences`, and verify the
   open-PR case live before P5.
2. **(minor)** Grant `Bash(gh pr list *)` (or whatever the fixed step 2 actually runs) in
   `allowed-tools` — the current grant list doesn't cover the workflow's own verbs.
3. **(minor)** State the label→kind mapping once and name the both-labels case as an explicit
   exclusion under the ambiguity branch.
