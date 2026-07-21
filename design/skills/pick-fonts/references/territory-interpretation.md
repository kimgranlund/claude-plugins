# Territory interpretation — turning a brief into a point, not a region

This is SKILL.md step 1's worked ground truth. The underlying doctrine belongs to
`make-design-system/references/context-potency.md` (its presupposition technique and
generic-output clinic table) — this file does not re-derive that doctrine, it applies it to the
specific artifact class this skill produces: a typographic decision, not a generation-prompt
carrier. Read `context-potency.md`'s "Why potency governs this artifact class" section for the
underlying mechanism; what follows are worked transformations for this skill's own input.

## Why a region fails before a single font is chosen

A generating model asked to design type for "modern and premium" has no fixed point to aim at — it
fills the region with whatever "modern and premium" means in its prior, and a different session (or
a different voice within the same session) fills it differently. The result is five individually
plausible font picks that were never aimed at the same target — the grab-bag failure named in
SKILL.md step 3. A named reference removes the guessing: "1977 Swiss ski-poster energy" already
implies a hue of grotesque sans, tight tracking, bold color blocking, and a specific decade's
production constraints — a generating model can act on it without inventing a mental image first.

## Worked transformations

| Region (rejected — push back) | Point (accepted — proceed) | Why the point is actionable |
|---|---|---|
| "modern and clean" | "restrained Kinfolk-editorial quiet luxury" | Names a specific publication's visual register: warm neutrals, generous whitespace, a serif with editorial weight — not just "not cluttered" |
| "bold and impactful" | "1977 Swiss ski-poster energy" | Names a decade, a country's design tradition, and a genre (poster) — implies grotesque sans, saturated color blocking, tight kerning, without further elaboration |
| "trustworthy and professional" | "the same register as a Bloomberg Terminal, not a Silicon Valley SaaS landing page" | Names two contrasting REAL products in the same rough category — disambiguates "professional" (dense, data-first) from the more common SaaS-generic reading |
| "friendly but technical" | "Stripe's docs circa 2019 — a humanist sans doing double duty as both brand and code-adjacent chrome" | Names a specific product AND a specific era of it (Stripe's type system has changed) — closes the ambiguity a bare "Stripe-like" would leave open |
| "warm and human" | "an indie bookshop's hand-lettered shopfront sign, translated to screen" | Names a physical referent with load-bearing visual facts (hand-lettering, warmth, imperfection) rather than an adjective pair that also describes a hundred other things |

## Running the elicitation when the brief is thin

If the input never clears "modern," "premium," "bold," "clean," "friendly," or a synonym without a
named referent attached, don't proceed — ask for one of:

- **An existing brand or product** to sit near (not copy) — "closer to X than Y" is often faster
  to state than a description from scratch.
- **A decade or design movement** — "1970s," "Bauhaus," "Y2K web" each carry enough shared visual
  vocabulary to act as a point.
- **A physical or cultural referent** — a genre of print material, a place, an artifact — anything
  concrete enough that two different people would picture roughly the same thing.
- **Existing type commitments** — if the brand already has a locked display face or an existing
  type spec, that IS the point; don't ask for a fresh territory when one already exists.

A brief that names any of the above is a point; a brief that stops at adjectives is a region — push
back once, concretely, before spending the rest of the procedure on an unaimed decision.

## Worked full decision (one territory, carried through to handoff)

A cold-start template — the shape of the decision doc SKILL.md step 5 hands to
`font-token-rules`, with real `typeface-check.py` output (not invented numbers):

> **Territory**: "Stripe's docs circa 2019 — a humanist sans doing double duty as both brand and
> code-adjacent chrome." (a named product + era, not "friendly but technical" — see the worked
> transformations table above)
>
> | Slot | Font | Weight | Rationale (traces to the territory) |
> |---|---|---|---|
> | `display` | Inter | 800 | The territory is restrained tech-brand confidence, not a loud statement — the same humanist sans pushed to its heaviest cut carries scale without importing a second voice |
> | `heading` | Inter | 800 | "Double duty" means brand and chrome share one face; headings commit to the same heavy cut as display for a consistent, confident register |
> | `body` | Inter | 400 | The regular cut is the territory's "chrome" half — legible prose that doesn't compete with the brand voice it shares a family with |
> | `ui` | Inter | 400 | Chrome legibility is explicitly named in the territory ("code-adjacent chrome") — no separate UI face needed |
> | `mono` | JetBrains Mono | 500 | The other explicit half of the territory ("code-adjacent") — a real, separate face, not Inter's fallback monospace, because code is a first-class citizen of this brand's voice |
>
> **Coherence pass**: all five slots trace to the same two-clause territory (brand ↔ chrome); no
> slot introduces an unstated third register.
>
> **Checker verdicts** (same-baseline pairings only — sub-heading/title inherit headline's call,
> tiny inherits label's, kicker/code/sub-title inherit mono's, so no separate pairing check is
> needed for those slots):
> ```
> $ typeface-check.py pair Inter 800 Inter 400          # heading over body
> Inter (800) vs Inter (400)
>   x-height ratio  1.000  OK
>   cap-height ratio  1.000  OK
>   axis apart  True  (weight gap 400 >= 300)
>
> $ typeface-check.py pair "JetBrains Mono" 500 Inter 400   # kicker/code over body
> JetBrains Mono (500) vs Inter (400)
>   x-height ratio  0.982  OK
>   cap-height ratio  1.000  OK
>   axis apart  True  (classification (mono vs sans), register (code vs neutral))
> ```
> Both pairings clear S5/S6 clean — no `font-size-adjust` compensation needed, both axis-apart on
> a real signal (weight, then classification+register). **Accessibility floor**: `body`/`ui` stay
> at Inter's neutral, legibility-optimized cut — no override to justify. Ready to hand to
> `font-token-rules`.

## Boundary

This file is worked application, not the doctrine itself — `make-design-system/references/
context-potency.md` owns the presupposition technique and the generic-output clinic in general;
this file exists so that discipline doesn't have to be re-derived on every typography brief.
