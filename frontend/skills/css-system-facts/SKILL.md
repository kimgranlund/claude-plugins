---
name: css-system-facts
description: >-
  Answers CSS ARCHITECTURE facts — @layer vs. load-order precedence, three-tier tokens +
  generated theme packs, light-dark() as the theming primitive, the FRAME-vs-RHYTHM geometry
  split, @scope vs CSS Modules scoping, CSS as decision logs + tested contracts. Use for "@layer
  or import order", "theme pack needs no fallback", "light-dark() vs [data-theme]", "FRAME or
  RHYTHM token", "@scope vs CSS Modules", "unit-test a CSS file". NOT token DESIGN — palettes,
  type, exports (design plugin: make-palette, make-design-system, token-builder); NOT
  spacing/density THEORY (size-and-shape-rules); NOT motion (motion-rules); NOT component anatomy
  (make-component); NOT platform facts (web-component-facts).
user-invocable: false
disable-model-invocation: false
---

# css-system-facts — the CSS architecture world model

Answers how a production CSS system is actually structured and kept safe to change — cascade
precedence, token tiering and theming, geometry-family naming, scoping strategy, and how CSS
itself carries and proves its own decisions — from two live source trees read directly (agent-ui,
gen-ui-kit), not general CSS folklore. This pack owns CSS ARCHITECTURE MECHANICS; it does not
design token VALUES (that's the `design` plugin's job — see Boundaries below).

| Ask | Load |
|---|---|
| `@layer` or import-order precedence; why a codebase picked one over the other | `references/cascade-and-load-order.md` |
| The primitive→semantic→component token tiers; why a generated theme pack needs no fallback mechanism | `references/token-taxonomy-and-themes.md` |
| `light-dark()` mechanics; how it composes with a theme-pack attribute selector | `references/light-dark-theming.md` |
| Is this value a FRAME (scale-riding) or RHYTHM (density-riding) token; the rejected multiplier-ladder history | `references/frame-vs-rhythm-geometry.md` |
| `@scope` vs. CSS Modules; why a compiler-enforced boundary beats build-time class hashing for a distributed library | `references/scoping-strategies.md` |
| Why CSS comments cite ADRs/tickets inline; how to unit-test a CSS file's structure (sectioning, token hygiene, negative controls) | `references/css-as-decision-log-and-contract.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask: precedence mechanism · token tiering/theming · `light-dark()` · geometry
   family (FRAME vs. RHYTHM) · scoping strategy · CSS-as-log/CSS-as-tested-contract. Grep the
   matching reference for the specific term first, then Read the hit's section — don't load the
   whole file when the ask names one mechanism.
2. Answer on the contract: **claim + cited source (file path or ADR) + the failure mode the
   default prevents** — every grounded claim in this pack's six axis files carries a `[verified]`
   or `[incident]` marker (see `references/sources.md`); a framing/comparison paragraph that
   synthesizes already-marked claims doesn't re-mark each sentence.
3. When an ask spans two axes (e.g. "should a themed subtree's tokens ride `light-dark()`
   too?"), load both references — the axes compose (see `light-dark-theming.md`'s own citation of
   the theme-pack mechanism) rather than nesting one as a subset of the other.

## Boundaries — the critical fence, both directions

**This pack answers CSS ARCHITECTURE; it never designs token VALUES.** The `design` plugin owns
token DESIGN — palettes, type systems, and design-system exports: `make-palette` (OKLCH ramps),
`pick-fonts`/`font-token-rules` (typography systems and their `--type-*` grammar),
`make-design-system` (cross-platform export strategy), and the `token-builder` agent (a project's
token layer). A question like "what OKLCH pair should this semantic role use" or "pick a font
pairing" routes there, even when it mentions `light-dark()` or a token tier in passing — this pack
answers HOW the CSS mechanism resolves or is organized, never WHICH values fill it. Checked
directly against this pack's own trigger surface (`@layer`, cascade, `@scope`, `light-dark()`, CSS
Modules, decision-log/tested-contract): none of the five design-plugin descriptions above carries
any of that vocabulary, so no reciprocal fence was needed on their side (see
`references/sources.md`'s "Fence provenance" section).

**Frontend-side fences**, both directions:

- `size-and-shape-rules` owns the general THEORY of why a spacing/sizing scale looks the way it
  does (base unit, progression shape, density composition) — a question like "why 4px/8px steps"
  or "linear or geometric progression" stays there. This pack's FRAME-vs-RHYTHM axis is the
  narrower, CSS-specific fact of which token FAMILY a value belongs to and which multiplier it
  rides — a question like "is this a FRAME or RHYTHM token" or "why does `[density]` skip the
  frame" is this pack's.
- `web-component-facts` owns per-control platform facts (lifecycle, stamping, traits,
  ElementInternals, the per-control test-file quintet). This pack's CSS-as-tested-contract axis
  is about testing a CSS FILE's structure specifically (sectioning, token-hygiene regex audits,
  negative controls) — a question about which test FILES a new control needs, or jsdom-vs-browser
  test tiers generally, stays with `web-component-facts`.
- `motion-rules` owns transition/animation timing; `make-component` owns build procedure and
  derived component geometry (padding, icon sizing) — neither collides with this pack's
  architecture-mechanics scope.

## Sources & provenance

`references/sources.md` — grounding file table, `[verified]`/`[incident]` marker definitions, the
same-number-different-repo ADR-0003/ADR-0038 trap this pack surfaces rather than silently
resolves, and fence-negotiation provenance.

Extension: governed by [[make-pack]]
