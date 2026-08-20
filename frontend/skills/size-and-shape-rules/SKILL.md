---
name: size-and-shape-rules
description: >-
  Answers sizing and spacing SCALE questions — the theory beneath any dimensional token
  system, from a cited corpus. Use for "why 4px/8px steps", "how do I build a spacing scale",
  "linear or geometric progression", "why the scale gets sparser at larger sizes", "how nested
  containers compose their padding", "what's the right base unit". Carries base-unit
  rationale, dense-then-sparse progression, composable-spacing theory, cross-system
  comparison. ANSWERS the theory — does not derive one component's law (make-component) or
  bind a platform scale (material-shape-facts); NOT CSS token-family naming
  (css-system-facts); NOT a codebase's control-sizing/density token implementation
  (css-system-facts).
user-invocable: false
disable-model-invocation: false
---

# size-and-shape-rules — the spacing/sizing scale world model

Answers why a dimensional scale looks the way it does — base unit, step shape, how nested spacing
composes, how density multiplies — from a cited, dated corpus, so a new scale is designed from
principle instead of copied by eye from whichever system is open in another tab.

| Ask | Load |
|---|---|
| "Why 4px/8px? Linear or geometric? Why does it get sparser at the top?" | `references/scale-theory.md` |
| "How does nested padding compose? What does density actually scale? What radius on a nested surface?" | `references/composable-spacing.md` (its §House lock carries the ratified nested-radius formula + escape hatch) |
| "How do Material/Tailwind/Carbon/Apple structure their scales?" | `references/scale-theory.md` §Cross-system comparison |
| Provenance and the unverified edges | `references/sources.md` |

## Consult procedure

1. Classify the ask: base-unit choice · progression shape · composition/nesting · density · cross-
   system comparison. Load only the matching reference.
2. Answer on the contract: **claim + cited source + the failure mode the default prevents** —
   naming the register: corpus-backed · house-ruled (composable-spacing.md §House lock — a ruled
   point, overridable by a project ruling) · general convention. A
   scale question answered without naming what breaks if you ignore it is an opinion, not this
   pack's answer.
3. State which register the answer comes from: corpus-backed vs general convention — and say so
   when it's the latter.
4. Route derivation/binding work at the boundary (below) — this pack never emits a token file.

## Boundaries

- **This skill answers theory; it does not derive or bind a scale.** Two worked instances already
  exist in this estate and this pack cites them rather than restating their content:
  - `make-component`'s `references/geometry-system.md` — the button-family law (`(height − glyph)
    / 2`), the six-step comfortable ramp, and the separate compact/dense two-band system. That
    file's "Composed padding" section is the worked EXAMPLE of the nesting principle
    `composable-spacing.md` states generally — read the principle here, see it applied there.
  - `material-shape-facts` (design plugin, where installed) — the *consumption*
    guide for a project already bound to Material's own specified scale (control ramp, radius
    scale, space ladder). This pack explains why a scale like that has the shape it does; that
    skill verifies a specific export carries it.
- **Realizing a scale as project tokens** is the design plugin's `token-builder` seat (where
  installed) or `make-component`'s own build step — this pack supplies the rationale they realize.
- **Page-region layout** (where a sidebar or header sits) → [[break-down-layout]]; **raw CSS
  box-model/flow mechanics** (why a margin collapsed, what a BFC does) → [[dom-layout-facts]];
  **one component's full anatomy** → [[make-component]]. A scale question about "how much space"
  belongs here; a question about "where" or "why did the box behave that way" belongs to those.

## Extending this pack

Extension: governed by [[make-pack]]
