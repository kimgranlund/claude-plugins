# Doctrine-vs-practice divergence — a per-layer measurement, not one estate verdict

**The judgment call:** "how much has practice drifted from doctrine" is not a single yes/no
answer for a codebase — it's a per-LAYER measurement, and the layers closest to the primitive
substrate are typically the most coherent while the layers closest to individual product
features are typically the least. Reporting one aggregate verdict ("the mix is real") without the
layered breakdown hides where the actual leverage is; reporting the layered map is what turns a
vague operator complaint into a prioritized fix list.

## The worked case [verified]

gen-ui-kit's review produced exactly this map, ranked by severity, for a single codebase:

| Layer | Model in practice | Coherence |
|---|---|---|
| primitives (web-components) | signal-backed props, one render effect per element, attributes-as-api | HIGH — one substrate, edge drift only |
| composites (web-modules) | reflected attributes + events + method calls; no stores | MEDIUM — coherent style, duplicated machinery |
| shells | behavior-only orchestrators, state in children | HIGH (deliberate, doctrine rule 26) |
| apps | per-app ad-hoc: closures, DOM-as-state, hand-rolled pub/sub, some signals | LOW — every app invents its own |
| a2ui runtime (in-repo) | plain object dataModel, re-apply-all on write | internally consistent, primitive |
| genui runtime (vendored) | Cell/Derived, RFC-6901, memoized per-pointer reads | the best data model in the repo; used by ONE consumer |

Verdict, quoted: "The foundation is in better shape than the symptom suggests: there is exactly
one signal kernel, one element base, and a written doctrine that covers most of the territory.
The mix is real but concentrated in three places, in increasing order of severity" — cosmetic
tiering inside components, one live bug hazard plus duplications in web-modules, and full
STRUCTURAL divergence at the app layer and in the two runtimes, "where doctrine (rule 3: 'one
reactive path'; pattern menu row 1: 'reactive state → signals') and practice have fully
diverged." The operator's own suspicion ("a mix of implementations") was correct, and the layered
map is what gives it a shape instead of a vibe.

Source: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
("Verdict" + "The layered map" table).

## Doctrine documents disagreeing with each other is its own measurable class [incident]

The same corpus's fourth axis inventories the ratified rules themselves and finds internal
contradictions distinct from code-vs-doctrine drift — doctrine-vs-doctrine drift: a live claim
mismatch (`traits.md` says registration throws on missing `attributes`/`events`/`config`; the
ADR it should match verifies only four unrelated fields throw, and the correction "never
landed"), an internal count drift (41 vs. 56 traits, two numbers in the same file), a
frontmatter-vs-body status inversion (an ADR's frontmatter says `accepted` while its own Status
note says it's still conditionally `proposed`, pending a sequencing dependency on a second ADR),
and an undrawn boundary (`querySelector` parent→child coordination vs. "data down, events up"
child→parent — both ratified, aimed at different directions, but no doc states which direction
each governs). None of these are code drifting from doctrine; they are doctrine drifting from
itself.

Worth disclosing about the frontmatter-vs-body item specifically: the SAME corpus's own
`INDEX.md` (a sibling document dated the identical day) states this exact contradiction was
already resolved by the time of authoring — the dependency ADR had since ratified, and "an
appended status note landed" closing the gap. This is itself a worked instance of
`audit-technique.md`'s doctrine-vs-practice-diffing technique catching something the raw
contradiction inventory alone would miss: two documents in the same corpus disagreeing about
whether an earlier finding is still live. Report a doctrine-internal contradiction with its own
resolution status checked against every other document in the same corpus, not just the one
document that first surfaced it.

Source: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/04-doctrine-vs-practice.md`
Part 3 ("Contradictions and tensions between doctrine documents") — eight items total; the
resolution note is `INDEX.md`'s own F9.

## The diagnostic

1. **Build the layer table before writing the verdict.** Rows: layer name, the model actually
   observed in practice, a coherence rating (HIGH/MEDIUM/LOW) with a one-clause reason. This is
   the mechanical form of the judgment — see `audit-technique.md`'s coherence-map technique for how
   to run the survey that fills it in.
2. **Order findings by where coherence is LOWEST, not by where the symptom was first noticed.**
   The operator's complaint here started at one app's page; the highest-severity structural
   divergence was one layer up, at the app tier and the runtime layer generally — the layer table
   is what reveals that the symptom's location and the root cause's location differ.
3. **Separate "practice diverged from doctrine" from "doctrine contradicts itself."** A
   ratified-rules inventory (Part 1 of `04-doctrine-vs-practice.md`'s method) is a distinct pass
   from the code survey — run both, and don't let a doctrine-internal contradiction get
   miscategorized as a code team failing to follow the rules when the rules themselves disagree.
4. **A HIGH-coherence layer is worth stating explicitly, not just the LOW ones.** "Don't touch
   these" is as load-bearing a finding as the drift list — it tells a team which patterns are
   already the reference implementation to hold new work up against (see `adoption-verdict.md`
   for the sibling judgment on load-bearing-vs-not layers specifically).
