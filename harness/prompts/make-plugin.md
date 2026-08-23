---
description: "Forge a whole plugin from a domain intent — \"create a plugin with all the skills related to X\". Charter interview, family design via the four decomposition tests, a rejected-members ledger, scaffold, a make-skill pass per member, routing proof, ship. NOT for splitting a corpus (plan-skill-split, greenfield here); NOT for partitioning a surface (plan-plugin-split); NOT releasing a built plugin (ship-plugin)."
argument-hint: "[domain or one-line charter]"
---

# make-plugin

make-plugin composes what the single-artifact forges make: a domain goes in, a released plugin
comes out, and every member skill earns its place through the same tests that would judge it after
the fact. Seed: `$ARGUMENTS`. Invoke `plugin-writing-rules` now — structure, naming,
versioning, and release rules are its; not restated here.

## Phase 0 — Route

One artifact wanted → the matching single make-* workflow. An *existing* corpus to break up →
`plan-skill-split` (its tests need real files; this command's tests run on projections). A built
plugin needing a ship → `/ship-plugin`. Greenfield domain → proceed.

## Phase 1 — Charter

Run the `find-intent` discipline on the domain: audience, the asks the plugin must answer,
explicit non-goals, and the plugin's name — distribution-scoped, disjoint from every member's
domain prefix (the stutter rule), no reserved words. One batched multiple-choice round; the
charter is written before any member is named.

## Phase 2 — Family design (the four tests, run forward)

Greenfield has no files to count, so every test runs on projections — which makes the projections
the deliverable:

1. **Question types, not topics.** Decompose the domain by *kind of question* ("which standard
   applies" vs "how do I mix these" — different types; four lenses on one question are one skill).
   Target 3–7 members; a two-member family is usually one skill, a ten-member family is usually a
   taxonomy wearing a plugin label.
2. **Projected ask co-occurrence — evals first, at family scale.** Write each member's trigger
   prompts *now*, before any member exists (~8 per member, real phrasings from the charter). Map
   each prompt to the members it needs: a majority needing two members is a kill for that boundary,
   exactly as in `plan-skill-split`.
3. **Vocabulary separability.** Lay the members' candidate descriptions side by side; siblings
   competing for one token field will steal from each other at routing time (`/check-routing`'s *stolen*
   shape, pre-paid). Entangled members merge before they are born.
4. **Per-member cost.** Each member costs a fenced description, an eval suite, and its share of the
   1% listing budget in every consuming session. A member with no projected prompt of its own is a
   rejected member — and the **rejected-members ledger is mandatory**, same as the decompose
   precedent: name what you did *not* build and which test killed it.

Coverage closes the design: every charter ask maps to exactly one member or to a rejected-ledger row — an ask mapping to nothing is the hypothetical corpus's gap, found now instead of after release. Deliverable: the family manifest — per member: name (grammar-checked), one-line identity, species,
both dials with rationale, boundary map; plus the shared-vocabulary map and the rejected ledger.
The user ratifies the manifest before anything is scaffolded — this is the cheapest moment to be
wrong.

## Phase 3 — Scaffold

Plugin skeleton per `plugin-writing-rules`: manifest at `0.1.0`, README with the member map,
empty member dirs. **Bootstrap check (OUT-02, `prd-idr-framework.md`):** run `python3
${CLAUDE_SKILL_DIR}/scripts/mint_idr_bootstrap.py <git-root-of-the-repo-being-scaffolded>` right
after the skeleton lands, same commit — the argument is the git root whose (shared,
workspace-level) `.claude/docs/` will hold the IDR ledger, never the new plugin's own
subdirectory, which owns no docs tree of its own. The script is idempotent by construction — a
repo with no `.claude/docs/idr/idr-0001*` yet treats this as its first bootstrap moment under the
pattern and mints the founding `idr-0001` draft plus the product-brief living-index stub; a repo
that already has one (this isn't its first plugin) skips silently, never duplicating or
overwriting. A nonzero exit stops the scaffold right there and reports it — never continue to
Phase 4 with the bootstrap half-minted. Nothing else — content comes from the make-* workflows.

## Phase 4 — Forge loop

One `/make-skill` pass per member, with the family manifest as pre-answered interview context (the
charter answers the audience/scope slots once; per-member slots still run). Families above ~5
members: forge the first member alone, confirm it clears Phase 5 clean, then run the rest — the
family manifest is a projection until one member proves it real. Each member's Phase-2
suite seeds from this command's Phase-2 projected prompts — the family's routing design and the
members' evals are the same corpus by construction. Knowledge-species members inherit the honest
gap: this loop authors entry surfaces, and any `references/` corpus a member needs is routed to `/make-pack`
(one wave per axis), scheduled after the member's surface exists — never silently skipped.

## Phase 5 — Fence closure and routing proof

Cross-derive the no-triggers: every pair of siblings sharing any vocabulary gets reciprocal
no-trigger cases; every NOT-clause gets its return edge (make-skill P5.4 does this per member —
this phase verifies the *graph* is closed, not just each node). Then `/check-routing` on the new plugin:
the routing matrix is the proof the Phase-2 projections held. Stolen/leaked pairs are fixed here,
before the first release, while every description is still cheap to change.

## Phase 6 — Ship

`/ship-plugin`. The report inherits both gates' output and adds the family ledger: members
built, members rejected (with killing test), routing matrix summary, and any flagged corpus gaps
routed onward.

Done when the released artifact exists, the routing matrix is clean or its failures are triaged,
and the rejected-members ledger is in the README. NOT done if any member shipped without its suite,
any fence lacks its return edge, or the family was never ratified as a manifest — composing forges
does not suspend their gates; it multiplies them.
