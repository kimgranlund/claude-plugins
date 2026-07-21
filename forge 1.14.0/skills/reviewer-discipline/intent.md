# intent — reviewer-discipline
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability-uplift

## trigger
should:      ["review this diff for real bugs, not just the happy path", "before you file this review, steelman what the author would say back", "am I being too easy on this — did I actually check it runs, or just read the diff", "grade this fresh-context review before it ships"]
should_not:  ["review this PR's code style" (existing *-reviewer agents already own artifact-specific rubrics; this skill is conduct, not a rubric)]

## delta
Confirmed absent from every reviewer/auditor agent and skill in this workspace (fresh grep+read
sweep, 2026-07-18, GitHub issue #39): (1) reviewers push adversarial rigor only toward CONFIRMING
positive claims ("a green result is the builder's claim, not your verdict — distrust it," found in
ui:component-reviewer, typography:font-choice-checker) — none apply the same rigor to a
DISMISSAL; a reviewer can currently wave off a real finding with no evidentiary cost. (2) ~8 of 13
reviewer agents have a generic "verify claims with tools, don't trust the summary" step, but none
names the runtime-vs-changelog distinction specifically — a "fixed/shipped" claim can be accepted
from a commit message without checking the actual artifact. (3) zero prior art anywhere for a
steelman-self-review pass before filing. Source: adia-ui-kit v3.7.13's
references/response-authoring.md (legacy, external, not in this repo) via issue #39's Links.

## fences
- NOT for the return-block format a reviewer hands back to its coordinator (forge:handoff-compose)
- NOT for one artifact type's own rubric/dimensions — what to check for a component, a doc, an
  agent (the bound *-reviewer/*-auditor agent's own preloaded standard)
- NOT for portfolio/DEEP-tier campaign scoring across a whole corpus (agents-audit/skills-audit)

## assertions
1. A review report's dismissed findings each cite specific evidence (a command run, a file:line, a
   check performed) — never a bare "looks fine" with no evidentiary trail.
2. A "fixed/shipped/done" claim under review is checked against the actual runtime/build artifact
   (a real command output or file inspection cited), not accepted from a changelog or commit
   message alone.
3. The review process shows a self-check step taken before filing — a stated anticipated rebuttal
   that either survives scrutiny or causes a finding to be revised/dropped pre-filing, not only
   after the maker pushes back.

## gates
P0 route:      PASS — 2026-07-18 — knowledge/procedure needed on demand by existing reviewer
                agents; not mechanically checkable (hook), not an always-true entry-file fact, not
                itself an agent (the 5 target agents already exist and only need a preload)
P1 intent:     PASS — 2026-07-18 — user confirmed the record as drafted (name "reviewer-discipline",
                species/dials, pilot scope) via one consolidated confirmation, per the interview's
                own no-theater rule for slots the seed had already answered
P2 evals:      PASS — 2026-07-18 — evals/evals.json (22 trigger-routing cases); 3 assertions above
                (>=3); baseline captured in evals/baseline/01-03.md. Honest caveat, recorded rather
                than hidden: baselines 1-2's prompts were leading ("verify this claim before you
                rely on it", "do you agree with that assessment?") and the fresh agent already
                showed real rigor under that framing — the clean gap only baseline 3 shows cleanly
                is the steelman/self-rebuttal step (assertion 3), never spontaneously present.
                Phase 5's with-skill rerun should watch specifically whether assertions 1-2 hold
                under a NEUTRAL prompt (an ordinary review request, scrutiny not pre-cued) — that
                is the real bar this skill needs to clear, not just matching what a leading prompt
                already elicits.
P3 draft:      PASS — 2026-07-18 — SKILL.md written (~60 lines, well under the 500-line split
                threshold, no references/ needed); dials explicit; procedural skeleton followed
                (identity, Procedure, Output contract, Failure branches, Example with labeled
                bad/good pair drawn from the actual baseline-2 finding)
P4 language:   PASS — 2026-07-18 — potency_lint.py clean before and after; L1 instantiate-over-
                describe strong throughout (declarative identity, imperative procedure steps,
                arrow-format failure branches, a real labeled bad/good pair drawn from baseline-2's
                actual finding, not invented); L3 rewritten — prohibitions 5/5→2/5, NEVER 3/3→0/3,
                budget headroom restored with identical semantics (3 lines reframed affirmatively);
                L6 clean throughout (0 hedges/vague-quantifiers/hard-emphasis-markers; 9 bold spans
                are sanctioned handle-naming, not shouting)
P5 validate:   PASS pending fence closure only — 2026-07-18 — skill_lint.py clean. Fresh-context FLOOR audit
                (forge:skill-auditor): PASS, 0 blocking/major, 4 minor + 2 nits. Triaged:
                F1 (letter-vs-spirit gap — Procedure demanded a steelman per finding, Output
                contract only required evidence from one) FIXED — contract now distinguishes
                coverage (every finding) from evidence (>=1 cites its rebuttal). F2 (Example only
                demonstrated a good CONFIRMATION, none of a good DISMISSAL — the contract's own
                first bullet) FIXED — added a labeled dismissal example (caught my own drafting
                error mid-fix: the first attempt was itself a confirmation mislabeled as a
                dismissal; corrected to an actual cleared-not-a-bug case). F3 (identity paragraph's
                "confirmed absent... issue #39" clause workspace-couples the body and goes stale
                once preloaded) FIXED — trimmed; that provenance already lives here in intent.md.
                F4 (noun-head name on a procedural/user-invocable skill breaks the "verb head for
                invocables" grammar convention) — record, don't rename, per the auditor's own
                suggestion: "reviewer-discipline" was proposed and explicitly user-ratified
                (2026-07-18 AskUserQuestion) before this classification tension surfaced; a rename
                now costs directory/frontmatter/evals churn for a naming-grammar nuance, not a
                functional defect. Nits (duplication-with-target-agents' generic "verify claims"
                step; UNVERIFIED-vs-handoff-compose's-UNMEASURED marker adjacency) deferred to the
                preload-edit step and judged not worth a fix respectively — UNVERIFIED names a
                genuinely different concept (an unconfirmed external claim, not an unrun gate).
                Behavior check complete: all 4 reruns (baselines 1-3 with-skill + a 4th genuinely
                neutral-framed prompt, evals/baseline/04) show real deltas, not process theater —
                summarized per-assertion:
                - Assertion 1 (evidentiary symmetry): every with-skill rerun cites specific checks
                  for both confirmed AND dismissed findings; baseline 2's rerun ran its truth table
                  instead of only reasoning through it.
                - Assertion 2 (runtime over claim): baseline 3's rerun moved from doc-citation to
                  live commands against this repo's real GitHub remote, empirically proving the bug
                  with this repo's own actual branches; the neutral-framed rerun (04) applied a
                  diff to a scratch copy and ran both pre/post-patch states rather than trusting
                  "verified locally," catching an inaccuracy in the test PR description itself as
                  a side effect.
                - Assertion 3 (steelman before filing): the clean gap baseline 3 originally showed
                  is closed in every with-skill rerun — dismissal-rigor's rerun revised its own
                  verdict from a flat "not fine" to a precise "not a live bug at this call site,
                  but a latent contract violation" after steelmanning; the neutral rerun (04)
                  engaged a real, grep-verified objection rather than a token one.
                Rerun 1 additionally showed the steelman habit generalizing into a task that wasn't
                specifically testing it (an unprompted "Steelman check" section on a runtime-claim
                task) — evidence the discipline isn't narrowly overfit to its own test prompts.

                Fence closure: agents-audit/skills-audit both disable-model-invocation:true with no
                evals/ directory at all — command-only, categorically unreachable via model
                routing, so no routing leak exists to reciprocate against (matches the FLOOR
                audit's own finding: "no overlap risk found"). handoff-compose is the one real
                target (model-invocable) — added n13 (this skill's own t02 phrasing) to its
                evals.json as a no-trigger case, plus a note-field pointer explaining the boundary
                (return-block FIELDS vs. per-finding CONDUCT). No return NOT-clause added to
                handoff-compose's description — the audit already confirmed the boundary isn't
                contested, and the fence-closure step only asks for one "if the boundary is
                contested." All 6 gates now PASS.

## rulings
- Species: procedural (not knowledge) — this is a conduct/discipline layer applied during an
  activity (reviewing), not a reference corpus answering standalone factual questions; matches the
  texture of sibling cross-cutting skills (handoff-compose, linguistic-techniques, reasoning-orders)
  over knowledge-species siblings (the color-science/*-patterns families).
- Dials: disable-model-invocation=false because the pilot scope requires 5 agents to preload it
  (frontmatter `skills:` preload is blocked by disable-model-invocation:true, per
  agent-authoring-standards). Corrected during Phase 3 drafting (2026-07-18): user-invocable was
  first recorded false on the assumption "not a side-effecting action -> not a command a human
  types" — checking the closest sibling (`handoff-compose`, itself user-invocable:true) before
  drafting showed that assumption wrong. This workspace's actual convention for a cross-cutting
  discipline skill is user-invocable:true: a human reviewer can consult/run it directly
  (`/reviewer-discipline`) when writing a manual review, not only have it silently preloaded into
  an agent. Caught by checking precedent before drafting rather than after shipping — exactly the
  runtime-vs-assumption discipline this skill itself encodes.
- Pilot scope (explicit, user-ratified 2026-07-18): preloaded by forge:agent-reviewer,
  forge:plugin-reviewer, forge:hook-reviewer, forge:linguistics-reviewer, forge:skill-auditor only
  — the five that already share forge:handoff-compose as a common preload. ui/design-systems/
  typography reviewer agents and orchestration:code-reviewer/orchestration-reviewer are explicitly
  OUT of scope for this pass, per the user's own choice to pilot small rather than roll out
  estate-wide in one change.
- A fourth candidate prior (an emoji verdict taxonomy: ✅/⚠️/⏳/❌×3/🔍/🔀) was explicitly REJECTED
  by the user (2026-07-18) as conflicting with this workspace's own ratified 🟢/🟡/🔴 status
  convention (global CLAUDE.md). Not included in this skill's scope, and not a gap to revisit
  without a fresh decision.
