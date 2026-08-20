# Component / module intake schema

Fields lifted verbatim from `frontend:make-component`'s own Compose (whole → part) × Realize
(part → whole) axes (`make-component/SKILL.md`) — never restated as doctrine here, only reframed
as intake QUESTIONS a ticket must answer before build.

## Compose (outside-in) — the abstraction

| Field | Question | Owning step |
|---|---|---|
| Placement | Where does this sit — primitive, component, or module on the tier ladder? Which family (value-bearing control, overlay, display, container)? | `make-component` step 1 |
| Parents / children | What does it nest inside (a select trigger? a menu item? a modal action)? What does it host? | `make-component` step 2 |
| Composition & nesting | Anatomy — named parts and slots. Content model: host-as-grid or a rendered cell? | `make-component` step 2 |
| Consuming surfaces | Where does the finished component get placed — which screens/layouts consume it? What's the seam it wires into upward? | `make-component` step 4 |

## Realize (inside-out) — the embodiment

| Field | Question | Owning step |
|---|---|---|
| States | What custom states does it carry (`ElementInternals`)? What's the value-bearing contract — FACE, never a wrapped native? | `make-component` step 6 |
| API surface | Attributes · properties · events · custom states — closed sets as literal enums, one source of truth per datum. | `make-component` step 3 |
| Geometry (incl. nested-radius-class) | Which size ramp (XS–2XL)? Any nested-surface radius/spacing question this ticket must NOT answer inline (routes to `size-and-shape-rules` instead)? | `make-component` step 5 |
| Token bindings | Which EXISTING design tokens does it consume — color, spacing, radius? Not a `make-component` axis itself (the skill consumes tokens generically, no dedicated step); if the ticket is ALSO introducing a NEW token, that half of the grid routes to `design:token-feature-intake-rules` instead. | cross-cutting (no dedicated step) |
| Feedback | Keyboard/interaction fidelity — APG pattern, focus ring, `forced-colors`, mobile parity. | `make-component` step 7 |

## Scope frontmatter this shape stamps

```
scope: component
build-owner: make-component
dod-checker: component-checker
```

## Both-planes note

Compose-filled/Realize-empty is the "orphan component" quadrant (nowhere named to consume a
fully-specified API); the reverse is "looks clean but nothing does anything" — the same quadrant
names `break-down-layout`'s own defect grid uses (see the pack's own both-planes rule for the
general statement; not restated per file below).
