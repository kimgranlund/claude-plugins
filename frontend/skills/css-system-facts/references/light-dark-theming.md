# light-dark() as the theming primitive

**This axis is CSS mechanics — how a scheme-aware value gets resolved at the semantic tier. The
VALUES themselves (which OKLCH pair, which contrast ratio) are the `design` plugin's
`make-palette`/`check-colors` job; this pack only answers how the CSS runtime resolves a
scheme-aware declaration once those values exist.**

## The mechanism

**[verified]** `light-dark(<light-value>, <dark-value>)` is a CSS value function that resolves to
its first argument when the page is in light mode and its second when in dark mode, per the
nearest ancestor's `color-scheme` property. agent-ui's `tokens.css` sets the precondition once,
at `:root`:

```css
:root {
  color-scheme: light dark;
  ...
}
```

...then every scheme-aware semantic role is declared as a single `light-dark()` expression over
two already-defined primitive steps, never as two separate light/dark custom properties needing a
separate override mechanism:

```css
--md-sys-color-neutral: light-dark(var(--md-sys-color-neutral-550), var(--md-sys-color-neutral-450));
--md-sys-color-neutral-on-surface: light-dark(var(--md-sys-color-neutral-950), var(--md-sys-color-neutral-050));
--md-sys-color-neutral-background: light-dark(var(--md-sys-color-neutral-100), var(--md-sys-color-neutral-900));
```

This pattern repeats for every semantic role in the file — dozens of `light-dark()` calls, each
picking a light-mode primitive step and a dark-mode primitive step from the SAME flat,
mode-independent primitive ramp declared above them. The primitive ramp itself (e.g.
`--md-sys-color-neutral-100` through `-950`) carries no scheme awareness at all — scheme-awareness
lives entirely at the semantic tier, exactly where ADR-0002's three-tier model says it should
(`token-taxonomy-and-themes.md`): "Wrapped in `light-dark()` where applicable... Semantics answer
'what's the role?'"

## Why this is the THEMING primitive, not just a light/dark switch

**The runtime resolution is the load-bearing property.** Because `light-dark()` resolves against
`color-scheme` — a property that itself responds to the user's OS preference, an explicit
`color-scheme: light` / `dark` override, or a `[data-scheme]`/class-based override further up the
tree — a single semantic declaration serves every scheme-selection MECHANISM a consumer might
choose, without the token layer needing to know which one. Contrast this with the alternative
generation strategies this same problem has historically used:

- **A `.dark` class toggling two full stylesheets** — doubles the CSS surface, and a value
  forgotten in one stylesheet silently falls back to light-mode's value with no error.
- **A `[data-theme="dark"]` attribute re-declaring every custom property** — this is exactly the
  THEME-PACK mechanism `token-taxonomy-and-themes.md` documents (agent-ui's `themes/*.css`), which
  operates ORTHOGONALLY to light/dark: a theme pack re-declares the same `light-dark()` pairs
  under its own attribute selector, so a themed subtree is STILL scheme-aware via `light-dark()`
  — theme and scheme are two independent axes, not two rungs of the same ladder.
- **JS-computed inline styles per scheme** — requires a script to run before paint or a
  flash-of-wrong-theme is visible; `light-dark()` is resolved by the CSS engine itself, so there is
  no JS-timing race.

`light-dark()` is a theming PRIMITIVE, not a "dark mode feature," precisely because it composes
with the theme-pack mechanism rather than substituting for it: a themed, dark-mode subtree resolves
BOTH selectors (the theme's attribute selector picks the primitive-ramp values, `light-dark()`
picks which half of each pair applies) without either mechanism needing to model the other.

## The design-system-hub's own citation of this mechanism

Notably, the `design` plugin's `make-design-system` hub cites the identical runtime primitive in
its own shared-doctrines reference — "Dark counterparts, hover states, on-colors ship precomputed
and verified — pairs as data in carriers, `color-scheme` + `light-dark()` at runtime" — but from
the opposite altitude: that citation is about which VALUES ship precomputed in a design-system
export carrier (a design-token authoring concern), never about the CSS mechanics of how
`light-dark()` itself resolves, cascades, or composes with a theme-pack attribute selector (this
pack's concern). Neither citation duplicates the other's job; a design-system export's carrier
still needs THIS pack's facts to reason about why shipping precomputed pairs as `light-dark()`
arguments is safe under a themed subtree.

## Sources

- agent-ui `packages/agent-ui/shared/src/tokens/tokens.css` — `color-scheme: light dark;` at
  `:root`, and the full `light-dark()` semantic-role block, read directly 2026-08-20.
- gen-ui-kit `docs/ops/adr/adr-0002-three-tier-token-layering.md` — "Wrapped in `light-dark()`
  where applicable... Semantics answer 'what's the role?'"
- `token-taxonomy-and-themes.md` (this pack) — the theme-pack mechanism `light-dark()` composes
  with, not substitutes for.
