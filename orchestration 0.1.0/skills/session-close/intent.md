# intent — session-close
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability uplift

## trigger
should:      [
  "Wrap up this session before we're done.",
  "Close this out — check for anything left to capture.",
  "Before you exit, make sure nothing's left uncaptured.",
  "I'm about to end this session, prepare to close it out.",
  "Make sure nothing's left hanging before I go."
]
should_not:  [
  "Is my worktree colliding with a peer session's uncommitted changes?",
  "Before we wrap up, is there anything still open between us — any question you never got an answer to?",
  "Sweep the whole repo for stale worktrees and dangling branches.",
  "Open a PR for this fix."
]

## delta
Without this skill: a session told to close (via the raw prompt "write any new issues or PR
otherwise prepare to close this session") writes *something* to comply, with no verification loop,
no per-finding routing (a bug, a follow-up, and a durable lesson each want a different record, not
one combined write), and no way to distinguish "I checked and there's genuinely nothing" from "I
didn't check." This skill's delta: a checked sequence — mechanical state check, judged
capture through the existing capture skills, a knowledge-harvest trigger for durable lessons, a
read-back verification before anything counts as captured, and a mandatory verdict that is exactly
one of two shapes, never silence.

Source: this session's own `/forge:intent-extract` pass (self-close scope, hook+skill split later
corrected to skill-primary + a non-blocking SessionEnd log, orchestration placement cross-
referencing concurrency-design — all three confirmed via AskUserQuestion), amended by the user to
add the knowledge-harvest trigger step and its own AskUserQuestion-gated confirm, which already
existed in `knowledge-harvest` and is invoked here rather than re-implemented.

## fences
- NOT for a PEER session's worktree — checking on or closing someone else's (concurrency-design)
- NOT for unresolved conversational questions or assumptions (open-questions-sweep — a different
  axis: conversation loose ends vs. this skill's git/repo state and findings)
- NOT for the worktree removal mechanics themselves (ExitWorktree)
- NOT for a repo-wide hygiene sweep across many worktrees/branches (forge's ops-repo, an agent)
- NOT for authoring knowledge content once a plan is confirmed (knowledge-harvest owns authoring;
  this skill only triggers its detection pass)

## assertions
1. The skill never exits without stating a verdict in one of exactly two shapes: a captured-items
   list, or a single "nothing to capture" line.
2. A finding routes through the matching existing capture skill (bug-report/feature/issue) rather
   than a raw `gh issue create` — no re-derived dedup or payload logic.
3. Nothing is counted as captured without a read-back (git log / gh issue view / gh pr view)
   confirming it actually landed.
4. On a session with zero real findings and zero uncommitted state, the skill declines to
   manufacture a write and states the clean verdict instead.
5. The knowledge-harvest trigger (step 3) only fires the scan — it does not itself author content
   or bypass knowledge-harvest's own AskUserQuestion confirm gate.

## gates
P0 route:      PASS — primitive=skill. The mechanical PART is checkable (git state), but deciding
                what's WORTH capturing, whether work is PR-ready, and whether a knowledge signal
                crosses the bar are judgment calls a hook cannot make (hook-authoring-standards'
                own routing law: "judgment in a hook is wrong often and unoverridable always").
                Verified against Claude Code's own hook docs (code.claude.com/docs/en/hooks,
                2026-07-19) that `Stop` fires on every turn (not session end) and `SessionEnd`
                cannot block anything — ruling out a blocking hook gate entirely; a passive,
                non-blocking `SessionEnd` log hook is a SEPARATE, secondary artifact (see below),
                not this skill's own primitive.
P1 intent:     PASS — slots filled from this session's own `/forge:intent-extract` pass (scope,
                mechanism, and placement forks resolved via AskUserQuestion), amended per the
                user's own follow-up instruction to add the knowledge-harvest trigger step.
P2 evals:      PASS — evals/evals.json (10 should-trigger, 12 no-trigger: fenced to
                concurrency-design ×2, ExitWorktree, ops-repo, knowledge-harvest,
                open-questions-sweep, bug-report, issue, and 3 (n09/n10/n11) deliberately unfenced
                ordinary model behavior with no sweep owner) + 5 assertions (above) +
                evals/baseline/ (2 scenarios: a busy session with a real bug/follow-up/repeated
                correction, and a clean session as negative control). Baselines confirm the actual
                gap: the old raw prompt gets something written but combines distinct findings into
                one write, never verifies the PR it opens, never surfaces a repeated correction as
                a knowledge candidate, and (clean-session baseline) manufactures a low-value Issue
                rather than representing "nothing to capture" as a valid outcome.
P3 draft:      PASS — SKILL.md written from the procedural skeleton (identity line, numbered
                procedure, output contract, failure branches, stopping predicate, labeled
                good/bad example, a references table pointing at the skills it invokes rather than
                restates); 92 lines, well under the 500-line cap; both invocation dials explicit;
                description 928/1024 chars after one trim pass (see P4).
P4 language:   PASS — skill_lint.py's potency rules (hedges/prohibitions/NEVER/vague-quantifiers/
                hard-emphasis, W-series) clean within budget after a rewrite pass (first draft: 13
                prohibitions / 10 NEVER, over budget on both — the whole Procedure/Failure-branches
                section was reframed from negative "never X" phrasing to affirmative statements of
                what each step DOES, keeping exactly one hard gate: a verdict is only as true as
                what the read-back step actually verified). Correction 2026-07-19: this gate had
                cited a standalone `potency_lint.py` that does not exist in this tree — the checks
                are folded into `skill_lint.py`'s own rules; corrected here, no re-run needed since
                the underlying lint pass was already run against the real script.
P5 validate:   PASS (2026-07-19)
                1. Lint: skill_lint.py clean — re-run after every fix below, still clean.
                2. Fresh-context audit (skill-auditor, FLOOR, real dispatch): FAIL on first pass —
                   evals/audit-report.md records one blocking finding (B1: the step-1 "clean tree
                   → skip to step 5" branch incorrectly skipped step 3's knowledge-harvest trigger
                   too, reproducing this skill's own baseline gap) and two majors (M1: SKILL.md's
                   description and evals.json t06 used a phrase near-verbatim identical to
                   open-questions-sweep's own t05, an unanchored routing collision; M2: this file
                   overclaimed status/gates before the real audit and behavior check had run).
                   Fixes applied: step 1 now reads "skip step 2; steps 3-5 still run" (SKILL.md);
                   t06 and the description's trigger phrase anchored to "...in the worktree before
                   I go" (SKILL.md + evals.json); this file corrected (see P4 note and this entry).
                   skill_lint.py and eval_check.py both re-run clean after the fixes. The auditor's
                   answers to the four commissioned questions (Skill-tool nesting sound; no failure
                   branch exits verdict-less; the read-back gate is instantiated, not just asserted;
                   the SessionEnd hook pair is correctly scoped and separate) stand as accepted
                   findings, not re-litigated.
                3. Behavior check (real, 2 fresh-context dry-run dispatches, no shared context,
                   general-purpose/sonnet, tools withheld — narrate-don't-execute so no fabricated
                   GitHub side effects land in the real repo): busy-session dispatch walked all 5
                   steps against the P2 scenario and confirmed, with evidence, all 4 checked
                   assertions — two separate records (bug-report → Issue, issue → a second Issue,
                   never merged), the PR only counted captured after narrating a `gh pr view`
                   read-back, and the 3rd-occurrence correction handed to knowledge-harvest rather
                   than dropped. Clean-session dispatch confirmed no write was manufactured to
                   satisfy the literal old phrasing, and the sole output was the exact single line
                   "nothing to capture — clean, safe to close." All 5 P2 assertions now have a real
                   demonstrated instance, not an assumed one.
                4. Fence closure: reciprocal no-trigger case added to open-questions-sweep's own
                   evals/evals.json (this skill's flagship phrasing, git/repo-state axis) and a
                   return NOT-clause added to its description. concurrency-design's own
                   description gains a forward pointer to this skill for the self-close case
                   (distinct from its own peer-collision scope). ops-repo is an agent, not a
                   skill — no evals/evals.json to reciprocate against; the fence stands
                   unreciprocated by mechanism, matching open-questions-sweep's own precedent.
                   Verified via the skill-auditor dispatch above that both reciprocal fences
                   actually landed in the sibling files (concurrency-design SKILL.md:19,
                   open-questions-sweep SKILL.md:15-16 + suite case n11).

## Separate artifact — the SessionEnd log hook
A non-blocking safety net, NOT part of this skill's own gates: `orchestration 0.1.0/hooks/`
registers a `SessionEnd` hook (`scripts/session_end_worktree_check.py`) that, on real session
termination, checks the same mechanical state (uncommitted changes, unpushed commits) in a git
worktree and — since `SessionEnd` cannot block anything (verified, P0 above) — writes a durable,
discoverable note if state was left behind, rather than trying to prevent the session from
ending. It exists so nothing is silently lost even when this skill was never invoked at all; it
is documented and gated separately (own selftest, own hook-authoring-standards lint) because it is
a different primitive, not a restatement of this skill.

## rulings
- Placement: orchestration, not forge — cross-references concurrency-design (same
  actor-classification domain, same plugin) rather than forge's git-campaign-workflows (a
  knowledge pack, answers-only; this skill is procedural and drives action).
- Type recorded as capability uplift, not encoded-preference: the verify-before-counting and
  two-shape-verdict discipline is new judgment Claude does not reliably apply unprompted (the
  baseline demonstrates this concretely), not merely a sequencing preference for something Claude
  already does correctly.
- The knowledge-harvest trigger step was added mid-design at the user's explicit instruction,
  after the initial `/forge:intent-extract` pass — folded in as step 3 rather than a parallel
  skill, since knowledge-harvest already owns detection + confirm + authoring end-to-end and this
  skill's only job is calling it at the right moment.
