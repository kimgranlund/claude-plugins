---
name: plugin-forge
description: >-
  Forge a whole plugin from a domain intent: "create a plugin with all the skills related to UI
  design", "build me a plugin for our API review workflow", "turn this domain into a skill family".
  Charter interview, family design via the four decomposition tests run forward (question types,
  projected ask co-occurrence, vocabulary separability, per-member cost) with a rejected-members
  ledger, plugin scaffold, a /skill-forge pass per member, fence-graph closure, /eval-run routing
  proof, /plugin-release ship. Run /plugin-forge [domain or one-line charter]. Human-timed; writes
  a new plugin directory. NOT for one artifact (skill-forge / agent-forge / hook-forge); NOT for
  splitting an existing corpus into a family (skill-decompose — this is greenfield); NOT for
  partitioning an existing surface into plugins (plugin-decompose runs on inventories, this on
  projections); NOT for releasing an already-built plugin (plugin-release).
disable-model-invocation: true
user-invocable: true
argument-hint: "[domain or one-line charter]"
---

# plugin-forge

plugin-forge composes what the single-artifact forges make: a domain goes in, a released plugin
comes out, and every member skill earns its place through the same tests that would judge it after
the fact. Seed: `$ARGUMENTS`. Invoke `plugin-authoring-standards` now — structure, naming,
versioning, and release rules are its; not restated here.

## Phase 0 — Route

One artifact wanted → the matching single forge. An *existing* corpus to break up →
`skill-decompose` (its tests need real files; this command's tests run on projections). A built
plugin needing a ship → `/plugin-release`. Greenfield domain → proceed.

## Phase 1 — Charter

Run the `intent-extract` discipline on the domain: audience, the asks the plugin must answer,
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
   exactly as in `skill-decompose`.
3. **Vocabulary separability.** Lay the members' candidate descriptions side by side; siblings
   competing for one token field will steal from each other at routing time (`/eval-run`'s *stolen*
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

Plugin skeleton per `plugin-authoring-standards`: manifest at `0.1.0`, README with the member map,
empty member dirs. Nothing else — content comes from the forges.

## Phase 4 — Forge loop

One `/skill-forge` pass per member, with the family manifest as pre-answered interview context (the
charter answers the audience/scope slots once; per-member slots still run). Families above ~5
members: forge the first member alone, confirm it clears Phase 5 clean, then run the rest — the
family manifest is a projection until one member proves it real. Each member's Phase-2
suite seeds from this command's Phase-2 projected prompts — the family's routing design and the
members' evals are the same corpus by construction. Knowledge-species members inherit the honest
gap: this loop authors entry surfaces, and any `references/` corpus a member needs is routed to `/pack-forge`
(one wave per axis), scheduled after the member's surface exists — never silently skipped.

## Phase 5 — Fence closure and routing proof

Cross-derive the no-triggers: every pair of siblings sharing any vocabulary gets reciprocal
no-trigger cases; every NOT-clause gets its return edge (skill-forge P5.4 does this per member —
this phase verifies the *graph* is closed, not just each node). Then `/eval-run` on the new plugin:
the routing matrix is the proof the Phase-2 projections held. Stolen/leaked pairs are fixed here,
before the first release, while every description is still cheap to change.

## Phase 6 — Ship

`/plugin-release`. The report inherits both gates' output and adds the family ledger: members
built, members rejected (with killing test), routing matrix summary, and any flagged corpus gaps
routed onward.

Done when the released artifact exists, the routing matrix is clean or its failures are triaged,
and the rejected-members ledger is in the README. NOT done if any member shipped without its suite,
any fence lacks its return edge, or the family was never ratified as a manifest — composing forges
does not suspend their gates; it multiplies them.
