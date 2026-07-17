# Audit report — concurrency-design (FLOOR depth, fresh context)

Auditor: concurrency-design-auditor · 2026-07-16 · scored against forge:skill-authoring-standards
Artifacts read: SKILL.md, intent.md, evals/evals.json, evals/baseline/*.md (all 3), sibling
SKILL.md for loop-design and orchestration-design. Mechanical pass: skill_lint.py (forge 1.29.0)
**clean**; description measured 961 chars (< 1,024); dials explicit; body 127 lines; contracts in
the head, worked example in the tail.

## Verdict

**PASS with findings — 1 MAJOR, 3 MINOR.** The skill is real: the behavior delta is sharp,
falsifiable, and honestly baselined; the central three-actor claim survives independent
verification against the live harness. The MAJOR is a boundary conflict with
`orchestration-design` that gives two live skills opposite defaults for the same scenario — it
needs a body edit or an explicit recorded ruling before the Phase 5 gate closes.

---

## MAJOR-1 — Fence/body contradiction + live doctrine conflict with orchestration-design

The description fences: *"NOT for a single session's own subagent-vs-solo or fan-out dispatch
decisions (orchestration-design)"*. But the body takes exactly that decision:

- Decide step 1 (SKILL.md:46–48): "subagents you're about to dispatch … you're about to fan out
  builders, the answer defaults to yes."
- Decide step 2 (SKILL.md:50): "Same-session subagents → the `Agent` tool's
  `isolation:\"worktree\"` at dispatch."
- Eval t04 ("should this subagent use isolation: worktree") and t05 ("dispatch two builders
  touching the same files") claim same-session dispatch prompts as triggers.

And the guidance **conflicts** with the sibling it fences to. orchestration-design Design step 5
(its SKILL.md:40): *"dispatch the disjoint same-tree fan-out … file- and import-disjoint slices
concurrently in one tree … worktrees only when slices must mutate overlapping files."*
concurrency-design Decide 1–2 says fanning out builders defaults the answer to yes and to
"default to isolation up front." For the disjoint-slice builder fan-out — the common case — the
two skills issue opposite defaults.

**Fix (either, recorded in intent.md rulings):**
(a) Condition Decide step 2 on overlap: overlapping or unpartitionable target files → isolate;
cleanly file-disjoint slices → orchestration-design's same-tree fan-out is the sanctioned
default (cite it). Then reword the fence to what the body actually holds: orchestration-design
owns dispatch *shape* (solo/team/fan-out/cost); this skill owns the *tree-safety* of whatever
shape was chosen. Or:
(b) Rule that concurrency-design now owns the isolation half outright and amend
orchestration-design step 5 to defer — a cross-skill edit with its own tier obligations.
Option (a) is smaller and matches the evals as written.

## MINOR-2 — intent.md mislabels the species; the artifact itself is coherent (answers dispatch Q1)

The dispatch asked whether the imperative Decide/Respond body is a species mismatch for a
Knowledge skill. Checked against the standards' species table, the premise dissolves: the dial
set `disable-model-invocation: false` + `user-invocable: true` **is the Procedural row**, not
Knowledge (Knowledge is model-only, `user-invocable: false`). The body is procedural-shaped
(numbered steps, output contract, escalation branches, done/NOT-done predicate) and the name head
`-design` is a zero-derivation verb matching both siblings — which carry the same dials and the
same shape. All three signals tell one story: **this is a procedural skill**, and so are its
siblings. The "deliberate deviation from knowledge-species purity" framing in intent.md P3 defends
a deviation that doesn't exist. Fix: intent.md:3 `species: knowledge` → `procedural` (and trim the
P3 justification). No SKILL.md change needed — the "zero imperatives" rule never applied.

## MINOR-3 — intent.md P4 gate note doesn't match the shipped file

P4 records "NEVER hard-gate cap 3/3, all genuinely catastrophic invariants." The shipped body
contains **zero** uppercase NEVER/MUST NOT (grep-verified; the surviving prohibitions are
lowercase/bold locks, which is fine and within budget — 0 ≤ 3 passes). The note was evidently
written against a pre-language-pass draft. Correct the provenance line; the ship decision reads
this record.

## MINOR-4 — Eval t09's trigger claim is unsupported by description vocabulary

t09: "should I commit before starting this risky multi-file move" → expect trigger. Routing is
description-only, and the description carries no commit-cadence vocabulary at all — a blind
router would plausibly send this nowhere (or to generic git help). The body *does* own the
guidance (Decide 2, third bullet: commit early/small per gate-green unit). Either add one
commit-cadence trigger phrase to the description (961 → still under 1,024; re-budget per the
standards' reciprocal-fence clause) or reclassify t09. Adding the phrase is right — the baseline
finding shows commit-cadence-before-risky-move is part of the delta.

---

## Dispatch questions answered

**Q1 (species):** Not a mismatch and not a purity deviation — see MINOR-2. Artifact coherently
procedural on all three axes; only the intent label is wrong.

**Q2 (fences real?):** Three of four boundaries hold cleanly. loop-design: no bleed — the body
never touches continuation. forge trio: explicitly held in-body (SKILL.md:53–55 defers the
CLAUDE.md-rule *mechanics* to entry-file-standards; References table routes hook-enforcement to
hook-authoring-standards). orchestration-design: **broken both ways** — see MAJOR-1.

**Q3 (no-trigger cases strawmen?):** No — they are near-verbatim sibling vocabulary: n01/n02/n03
from orchestration-design's own description ("should this be a subagent or a team", "how do my
skills and agents connect", fan-out), n04/n05 from loop-design's ("write a /goal", loop
re-running), n06/n07/n08 from the three forge fences. This is a genuinely adversarial negative
set. Gap: the hardest boundary (same-session disjoint fan-out, where orchestration-design should
win) has no near-miss negative — but that case is exactly MAJOR-1's contested territory; add the
negative after the fence ruling, not before.

**Q4 (three-actor table / SendMessage claim):** **Accurate, independently verified — the skill
does not overclaim.** This auditor is itself an instance of type (b): dispatched via a
`<teammate-message>`, running under a harness coordination notice that lists active agents
"addressable via SendMessage({to: name})". The EnterWorktree quote was also verified against the
live tool schema — verbatim-accurate, including the explicit-trigger-only clause ("Never use this
tool unless 'worktree' is explicitly mentioned by the user or in CLAUDE.md / memory"), which is
even stronger than the skill's paraphrase. Two precision caveats, neither a defect:
1. Row (b)'s label "Peer session" — the test the row actually uses (teammate-message sender) is a
   *channel* test, and by construction any such sender is a registered teammate of the session
   team; it may be a genuine peer session joined to the team or a sibling agent. The response is
   identical either way, so classifying by channel is correct — the label could read "named
   teammate (peer session or sibling agent)" to preempt a pedantic misread.
2. Addressability is team-scoped and lifetime-bound — an exited teammate stops answering by name.
   "You can ask it directly" holds; a non-reply is itself a signal to fall through to the
   opaque-session branch, which the skill's escalation ladder already accommodates.
The baseline-3 capture flatly denying the channel exists ("not a spawned agent you can reach with
SendMessage") makes this the skill's strongest, most falsifiable uplift claim — and it's true.

## What's good (keep)

- Behavior delta is real and honestly measured: baselines annotate what the model already does
  well (same-session partitioning) instead of inflating the gap — textbook capability-uplift
  scoping.
- The three-actor table passes the deletion test as a coverage-forcing enumeration: delete it and
  responses collapse back to the spawned-vs-not binary all three baselines exhibited.
- Description is a genuine trigger contract: feature nouns + symptom phrases ("git status shows
  changes I didn't make") + parseable NOT-for fences; 961 chars.
- Output contract, done/NOT-done predicate, and the verify-independently discipline (never act on
  either side's self-report) are all standing-instruction register and head-positioned.
- Worked example is clearly marked as the minting incident (illustrative, not normative) and
  extracts the right reusable lesson (the sequence degrades gracefully without prior isolation).

## Gate recommendation

Close Phase 5 after MAJOR-1 is resolved (option (a) is a ~4-line body edit + fence rewording +
an intent.md ruling line) and the three MINORs are applied. Per the standards' tier ladder the
MAJOR-1 edit is a description/boundary change: it owes lint + the eval suite updated in the same
change (t04/t05 survive under option (a); add the disjoint-fan-out negative then) + /eval-run at
the wave boundary.
