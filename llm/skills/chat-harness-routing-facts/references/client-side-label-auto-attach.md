# Client-side auto-attach on exact label match — closing the "tell them to tag it" hole

> Axis: a live UX failure mode where the assistant tells the user to reference something it just
> offered, but the user's plain-text reply doesn't route the same way an explicit tag would.
> Grounded in a worked instance: `@agent-ui/a2ui`'s ADR-0190 amendment.

## Resolve an exact match through the same path as an explicit tag — nothing fuzzy

**Claim — after a live incident (a dealer persona telling the user "tag @texas-holdem in your
next message" one turn after offering the game, and the user's next message not routing because
it wasn't an explicit tag), the fix resolves a user-typed EXACT label (case/punctuation-
normalized) through the SAME path as an explicit tag.** No fuzzy or description matching (the
false-positive risk was explicitly declined); first hit only; never a disabled entry; and the
teaching block is re-taught so the model knows naming loads it. · ADR-0190 amendment cl.A1/A2 (GH
#1030) · 2026-08-17 · [verified][incident]

**Why exact-only, not fuzzy:** a fuzzy or description-based match trades a real but narrow UX gap
(the model told the user to type something specific, and they typed close-but-not-exact) for a
much broader false-positive surface (any plain-text mention loosely resembling a capability's
name auto-attaching it) — the incident this fix closes never asked for that trade.

## What this file does NOT cover

The routing-integrity check for the MODEL's own declared routing facts (the surface being tagged,
here, is user-typed, not model-declared): `model-declared-routing-integrity-check.md`. General
description-based routing accuracy and adversarial evals for SKILL selection (a different
mechanism, at a different layer): `description-routing-and-adversarial-evals.md`.
