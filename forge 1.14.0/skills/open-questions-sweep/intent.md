# intent — open-questions-sweep
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: encoded-preference

## trigger
should:      [
  "before we wrap up, is there anything still open?",
  "did we ever resolve that — let's clear whatever's still pending",
  "any decisions still open before we close this out?",
  "wrap up any loose ends from this session"
]
should_not:  [
  "what's still open in the issue tracker?",
  "what should I do about the failing test right now?"
]

## delta
Without this skill: Claude asks a clarifying question mid-task, gets no answer (or the
conversation moves on before one arrives), and silently proceeds on an assumption — the item
never resurfaces unless the user happens to remember it themselves. Across a long session,
several of these accumulate and quietly rot. This skill's delta is a narrow trigger, distinct
from asking-in-the-moment (which Claude already does), that notices the accumulated backlog at
a closing point and clears it in one batched round instead of leaving it dropped.

Source: prior /forge:intent-extract pass in this session — resolved intent for "for forge, write
a kind of simple knowledge skill occasionally that instructs claude to ask me all the unanswered
questions using AskUserQuestions so we can wrap them up or provide insights or decisions."
Corrected there from "knowledge" to procedural species (it changes behavior; it isn't reference
content).

## fences
- NOT for resolving ambiguity before starting a task (intent-extract)
- NOT for a scheduled/interval reminder (orchestration's loop-design / `/loop`)
- NOT for tracking or filing work items in an external tracker (ops-issues)
- NOT for producing a persisted decision record/ticket after answers land (a separate, heavier ask)

## assertions
1. The single AskUserQuestion call carries 1-4 questions, each with 2-4 options, and marks a
   recommended option whenever one exists.
2. Every question traces to a specific item Claude raised or noticed earlier in the session and
   never got a resolved answer for — none are manufactured or already-settled.
3. The reply after the user answers resolves each item explicitly (states the decision, insight,
   or next step) rather than just acknowledging receipt of answers.
4. On a session with zero genuinely open items, the skill declines to fire rather than
   manufacturing filler questions.

## gates
P0 route:      PASS — primitive=skill. Not mechanically checkable (judgment call on what counts
                as "genuinely still open"); not an always-true fact; no tool-wall/parallelism/
                multi-skill preload need that would earn an agent. Procedure needed on demand.
P1 intent:     PASS — slots filled from the upstream /forge:intent-extract resolved intent plus
                author judgment on trigger phrasing/freedom/type (background session, user
                already greenlit the full resolved spec with "yes"); no slot stalled.
P2 evals:      PASS — evals/evals.json (12 should-trigger, 10 no-trigger: 7 fenced to a named
                owner — ops-issues, intent-extract, loop-design, scribe doc-authoring — and 3
                (n02/n07/n10) deliberately unfenced, ordinary model behavior with no sweep owner
                to route to) +
                4 assertions (recorded above) + evals/baseline/ (2 scenarios: 4 unresolved items,
                and a clean session as negative control). Baseline confirms the actual gap: Claude
                already recalls dropped items correctly but dumps them as prose + one open-ended
                follow-up instead of a resolving batched round — the skill's delta is the closure
                mechanism, not the noticing.
P3 draft:      PASS — SKILL.md written from the procedural skeleton (identity line, numbered
                procedure, output contract, failure branches, stopping predicate, labeled
                good/bad example); 66 lines, well under the 500-line cap; both invocation dials
                explicit; description 827/1024 chars.
P4 language:   PASS — potency_lint.py: hedges 0/0, prohibitions 1/5 (the template's sanctioned
                "do not imitate" bad-side label), NEVER 0/3, vague 1/3 (false-positive "fall
                short" matching the "short" pattern), hard-emphasis 0/3 — within budget.
                Rewrote the first draft's "never"-heavy procedure/failure-branches into
                affirmative framing (unanswered/unconfirmed/stale vocabulary instead of
                never-X'd), and dropped the HEDGE-triggering "might want to X" phrasing from both
                the description and step 1. L1/L3/L6 self-scored 5/5/5 (all load-bearing lines
                commit or demonstrate; procedure reads as instantiated action, not description).
P5 validate:   PASS
                1. Lint: skill_lint.py clean.
                2. Fresh-context audit (skill-auditor, FLOOR): PASS, no blocking findings.
                   Fixed: broadened ops-issues fence from "tracking or filing" to "querying,
                   tracking, or filing" (n01-style backlog-query near-miss); added a failure
                   branch for the user skipping/declining the AskUserQuestion round. Report at
                   evals/audit-report.md.
                3. Behavior check (fresh-session, with skill instructions active vs. the P2
                   baseline): scenario with 4 unresolved items -> one AskUserQuestion call, 4
                   questions, 3-4 options each, recommended option first, every question traced
                   to a real session item (assertions 1-2 demonstrated). Simulated answers ->
                   reply resolved all 4 by name with concrete next steps, not a bare
                   acknowledgment (assertion 3). Clean-session scenario -> single "nothing open"
                   line, no manufactured question (assertion 4). All 4 assertions demonstrated
                   present (with skill) vs. absent (P2 baseline: prose dump + one open-ended
                   follow-up instead of a resolving batch).
                4. Fence closure: added a reciprocal no-trigger case (this skill's flagship
                   phrasing, "Before we wrap up, is there anything still open?") to
                   intent-extract/evals/evals.json (n05) and orchestration's
                   loop-design/evals/evals.json (n13) — both named in this skill's own
                   NOT-clauses. Also added a defensive case to handoff-compose/evals/evals.json
                   (n13) per the auditor's flagged "nearest grab risk" (its Open-questions
                   handback field), though handoff-compose isn't one of this skill's own fences.
                   ops-issues is an AGENT, not a skill — it carries no evals/evals.json to
                   reciprocate against; the fence stands unreciprocated by mechanism, not by
                   oversight. `/eval-run` still needs a human/CI run at the next wave boundary
                   for forge and orchestration (this skill cannot trigger it itself).

## rulings
- Species corrected from the literal ask's "knowledge skill" to procedural — recorded as an
  explicit assumption in the upstream intent-extract pass and accepted when the user approved
  proceeding to skill-forge.
- Type recorded as encoded-preference, not capability uplift: Claude can already do each
  piece (notice a gap, call AskUserQuestion) — the delta is making the noticing-and-batching
  actually happen at the right moment instead of never. Per standards, encoded-preference skills
  earn brevity: state the sequence and stop.
- Post-ship workflow-backed code review (xhigh, on the open PR) found and this record's own
  maker fixed 5 real defects the P5 audit's FLOOR depth missed: (1) step 3 forced a fabricated
  "recommended" marking on stray-idea items with no stated assumption — now conditional on one
  actually existing; (2) the on-its-own trigger had no unattended/scheduled-firing fence, risking
  an unanswerable AskUserQuestion hang — added, mirroring ops-issues' own established convention;
  (3) the stopping predicate didn't recognize a user decline as a valid terminal state despite the
  failure branch requiring one — reconciled; (4) this skill's own fence-closure step (P5.4) closed
  reciprocal no-trigger cases for intent-extract/loop-design/handoff-compose but missed scribe's
  issue/feature/bug-report — added n12/n09/n10 there too; (5) this file's own P2 gate line
  overclaimed "10 no-trigger fenced to owners" when 3 (n02/n07/n10) were deliberately unfenced —
  corrected in place. A sixth finding (ops-issues.md overclaiming bug-report/feature share
  `issue`'s missing-label-creation fallback, when only `issue` documents it) was fixed in the
  sibling agent file, not this record. Generator-fixes-own-findings is an accepted deviation from
  strict generator≠critic here: the review ran in an independent workflow context this maker did
  not author or see mid-run, satisfying the independence the principle actually protects.
