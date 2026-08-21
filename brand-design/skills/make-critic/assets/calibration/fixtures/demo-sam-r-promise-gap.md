# Calibration fixture — critic-sam-r (demo, unpromoted)

Companion to `demo-accessibility-gap.md`'s pattern, for the S6 campaign-proof walkthrough
(#829): a brief planting exactly ONE defect `critic-sam-r`'s lens exists to catch — the promise
made in the strategy layer silently contradicted by the described product experience. Markdown
only, unpromoted, scored by inspection.

## The planted artifact — "Meridian" positioning brief + product description

**Positioning (from the Foundation Canon draft):** "Meridian exists so a small business owner
never has to feel alone doing their own books. Onboarding is effortless — we meet you exactly
where you are, human-first, no jargon, no forms that feel like an audit."

**The actual onboarding flow, as shipped (from the product spec, same document):**
1. An 11-field signup form (legal business name, EIN, NAICS code, three bank-routing fields, a
   CAPTCHA) with no inline guidance — every field is required before any part of the product is
   visible.
2. A session-timeout error reads: "Your session has expired. Please retry." No explanation, no
   saved progress.
3. The first-run support macro, verified against the actual support-script doc: "Thank you for
   contacting Meridian support. Please reference KB-1042 for account setup assistance." — a
   ticket-number citation, not a human reply.

## Expected catch (characteristic vocabulary, not exact-string)

`critic-sam-r` should name the 11-field form / EIN-and-CAPTCHA-first flow as the concrete
first-five-minutes moment that contradicts "effortless... human-first... no forms that feel like
an audit" — quoting both the promise and the form. It should separately flag the generic
"session expired, please retry" error state and the KB-number support macro as evidence the
brand's stated warmth reverts to generic-vendor behavior the moment nobody's performing for a
brand review. A critic that only restates the positioning language, or only critiques the
FORM'S usability without tying it back to the specific promise it contradicts, has not run this
lens — that's a generic UX critique, not the promise-delivery gap this seat exists for.

## Scoring approach

Pattern-match the returned findings for: (a) an explicit quote of the "effortless / human-first /
no audit-feeling forms" promise, (b) a cited contradiction from the onboarding flow, error state,
or support macro, and (c) language distinguishing "performed for the review" vs. "the ordinary,
unglamorous texture of actually using the thing" — a fixture that only plants the form without
the error-state and support-macro details would not distinguish this critic's lens from a plain
UX-friction critique, which is not what this council seat is for.

## What promotion would look like (not done here)

Stays unpromoted, per `calibration-discipline.md`'s promoted-script contract — this fixture has
run exactly once, in this walkthrough; promoting an unproven scorer after a single run would ship
the exact hazard `script-writing-rules`' selftest floor exists to catch.
