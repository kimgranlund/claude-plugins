# Cross-cutting UX intake schema (motion / focus / i18n)

Not a two-plane schema like the other three shapes — cross-cutting concerns don't decompose into
a build-time OUTSIDE-IN/INSIDE-OUT split, they're a per-concern BUDGET a ticket must state or
explicitly waive. Each sub-section's fields are lifted verbatim from that concern's own owning
`check-*`/`*-rules` skill — never restated as doctrine here.

## Motion (`screens:motion-rules`)

| Field | Question |
|---|---|
| Timing | Does this feature introduce a new transition/animation? What duration ladder does it fall on? |
| Choreography | If multiple elements move together, what's the stagger/sequencing? |
| Reduced-motion | What's the `prefers-reduced-motion` fallback? |

## Focus (`screens:check-focus`)

| Field | Question |
|---|---|
| Focus order | Does this feature change tab sequence or introduce a new focus trap (modal/dialog)? |
| Keyboard affordances | What keys move/activate — Escape, arrows, Enter/Space? |
| Focus-ring tokens | Does the new surface need a focus-ring recipe that clears 3:1 under every background it can sit on? |
| Hit targets | Do any new interactive elements need a hit-area expansion beyond their visual box? |

## i18n (`screens:check-translations`)

| Field | Question |
|---|---|
| RTL / bidi | Does this feature's layout need to mirror under RTL? |
| Locale formatting | Any new number/date/currency/pluralization surface? |
| Text expansion | Does the layout budget for German-class text expansion on any new label? |
| Hardcoded strings | Are any new UI strings hardcoded instead of routed through the translation layer? |

## Scope frontmatter this shape stamps

```
scope: cross-cutting
build-owner: motion-rules | check-focus | check-translations (per concern touched)
dod-checker: check-focus | check-translations (self-checking; motion-rules is answer-only, no gate)
```

## Both-planes note

Cross-cutting concerns are budget statements, not a two-column grid — the both-planes
capture-completeness rule still applies in spirit: an UNSTATED budget (no motion answer, no focus
answer, no i18n answer) is a named open fork, never silently assumed "not applicable." A ticket
that genuinely doesn't touch a concern states so explicitly ("no new motion introduced") rather
than leaving the row blank.
