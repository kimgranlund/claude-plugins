# Placement heuristics — new skill vs. extend vs. reject

Phase 2 proposes exactly one of four outcomes for a candidate. This file names the test for each,
in the order to check them — cheapest and most conservative first, so "new skill" is never the
default reach.

## 1. Reject as duplicate

Grep the target project's existing `skills/*/SKILL.md` descriptions and `references/*.md` bodies
for the candidate's claim. An exact or near-exact match already on record → reject. Report the
existing file:line so the user can see it was already captured, rather than silently dropping the
candidate with no explanation.

## 2. Extend an existing reference file

The claim sharpens, corrects, or adds a case to something already documented — same topic, same
file, would read as one continuous section rather than two competing ones. This is the majority
outcome for a mature corpus: most new facts are refinements of an existing axis, not new axes.
Versioning: append a dated note or supersede the prior claim with a stated reason (per `SKILL.md`
Phase 2); never edit a prior citation's claim in place without saying what changed and why.

## 3. New reference file within an existing skill

The claim is genuinely a new axis — a distinct "class of ask" this workspace's knowledge-pack
convention names — but the *skill* it belongs to already exists (the skill's own description
already covers this general territory, just not this specific sub-question yet). Add
`references/<new-topic>.md`, wire it into the skill's own consult table, and close the reciprocal
NOT-clause on any sibling skill this new axis might now be confused with (same discipline as
`skill-authoring-standards`' fence-closure step).

## 4. New skill

Reserve this for a claim that is broad and durable enough to be its own routable axis — something
a user would plausibly ask about on its own, not just as a sub-point of an existing skill's
territory. A new skill earns the full authoring loop (description, routing-corpus, evals,
structural gate, independent review) — it is the most expensive outcome and should be the least
common one. If in doubt between 3 and 4, default to 3 (extend the existing skill's axis) and let
scope pressure (the skill's own body budget, a genuinely separate question shape) force the split
later, rather than fragmenting the corpus preemptively.

## Cross-cutting rule

Never let "I'm not sure where this goes" default to "new skill" — that is exactly the corpus-sprawl
failure mode this system exists to prevent. When genuinely undecided between two outcomes, name
both as options in the Phase 3 AskUserQuestion rather than silently picking one.

## What this file does NOT cover

Which repo/project a candidate belongs to is Phase 2's routing step in `SKILL.md`, not this file.
The managed-docs source and its document-type allowlist is `managed-docs-scan.md`.
