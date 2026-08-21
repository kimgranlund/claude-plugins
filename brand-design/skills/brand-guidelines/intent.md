# intent — brand-guidelines
status: shipped
species: knowledge
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability-uplift

## trigger
should:      ["build brand guidelines", "brand design system", "guide me through the brand system",
              "2x2 options for the brand", "elicit the color/type/voice system",
              "help me decide the brand expression", "assemble a brand guidelines section"]
should_not:  ["decide the brand's position or strategy" (routes to brand-methodology-rules),
              "write the actual voice/copy" (routes to the brand-writer agent),
              "grade or score these guidelines" (routes to brand-rubrics, or
              design-skills:brand-decomposer — nonoun-skills marketplace — when installed)]

## delta
Retrospective record — no live forge interview exists; this skill was ported, not freshly minted.
Most brand-guidelines documents are written by one person guessing, then policed after the fact.
Without this skill, there is no structured way to build one collaboratively with evidence. With
it, each of six domains (mark/voice/color/type/expression/governance) is walked as a 2x2 of
concrete, exemplar-grounded design-move cards; the human picks a quadrant + comments; the pick is
captured as a typed, append-only choice in a ledger; the ledger assembles into corpus docs the
`brand-rubrics` skill can then score.

## fences
- NOT strategy/positioning — that's decided upstream, in `brand-methodology-rules`
- NOT the actual words — voice *behavior* lives here, the copy itself is the `brand-writer` agent
- NOT grading — `brand-rubrics` (in-plugin) and `design-skills:brand-decomposer` (the
  `nonoun-skills` marketplace, when installed) score what this skill makes

## assertions
1. States the six domains and that the loop generates a 2x2 (not a single suggestion) per domain.
2. States the ledger is append-only with `supersedes` for revisions, never a silent rewrite.
3. States assembly is dry-run by default, matches the corpus's flat/folder convention, and never
   clobbers a hand-authored layer doc.
4. States the split with brand-decomposer by verb (MAKES vs. GRADES), not by capability overlap.

## gates
Forge event: the brand-forge → brand-design migration campaign, Phase 3 Track D (2026-08-19) —
ported from brand-forge's shipped `brand-guidelines` skill (source
`/Users/kimba/Projects/nonoun/nonoun-plugins/brand-forge`, frozen SHA
`1e0d2d9e554b547f59260f63e31b4af2575196b0`, 2026-06-20), not authored fresh through make-skill's
P0-P5 ladder. Track D re-verified against pack-writing-rules (axes declared — 2, below the 3-7
floor and flagged rather than padded — consult table added, stale `bin/guidelines-ledger`/command
names repaired); Track D's own handoff disclosed it had no Agent-tool access to run the checker
itself, so the real fresh-context `harness:skill-checker` pass ran post-merge, once Track D and
Track E's work landed together on `phase2-integration` (agent `a50a000314dc45397`, 2026-08-19) —
verdict PASS-with-notes, 4 majors, all resolved in that same reconciliation round.

## rulings
- No live P0-P5 forge history exists for this skill; this record is written retrospectively from
  the shipped artifact, per this migration's convention for ported (not freshly forged) packs.
- The 2-axis reference corpus is below pack-writing-rules' 3-axis floor; Track D declared it
  honestly rather than inventing a third reference file to pad the count (see SKILL.md's axis note).
