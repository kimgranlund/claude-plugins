# The geometry system — one law, a six-step ramp, everything derived

This is the deterministic foundation of the **Realize** axis (level B1). The button is the base unit
of the *comfortable* controls (input, select, menu-item, tab, and container insets all derive from
it); the *compact / dense* controls (kbd, slider, switch, checkbox, tag, badge, …) are a **separate
size system** on their own two-band ramp — see "The compact / dense realm" below. The whole system is
governed by **one law** and a small ramp of **free values** — everything else is computed,
and `scripts/geometry-check.py` is the source of truth (this file documents what the code computes; the
code's `selftest` proves it against the hand-authored table). **Canon ownership:** for general
components the law's canon is THIS file; agent-ui's `geometry.md` is that repo's realization of it,
not a second canon.

> Run it: `python3 scripts/geometry-check.py ramp` · `… layout XL icon,label,caret` · `… validate card.json`

## The law

> **Edge padding for any glyph = (height − glyph) / 2.**
> Every glyph (icon or caret) is centered in a **square cell** of side = the button height.

Two consequences fall straight out of the law — they are the system, not conventions bolted on top:

1. **An icon-only (or caret-only) button is exactly square** — `width == height`. The glyph centers
   in its square cell; there is nothing else in the box.
2. **The asymmetric inline padding is forced, not chosen.** Because the icon and the caret are
   *intentionally different sizes*, the icon side gets `(h − icon)/2` and the caret side gets
   `(h − caret)/2`. The caret is smaller, so the caret side is more padded — the imbalance you see is
   the law, not a fudge factor.

This is why the only **free** per-size design decisions are five numbers: **height, icon, caret,
font, spacer**. Pick those; the paddings, the squareness, the pill radius, and the composed insets
are all computed.

## The canonical ramp (free values)

| size | height | icon | caret | font | spacer |
|------|-------:|-----:|------:|-----:|-------:|
| 2XL  | 64 | 28 | 18 | 20 | 8 |
| XL   | 48 | 24 | 16 | 18 | 8 |
| LG   | 36 | 20 | 14 | 16 | 8 |
| MD   | 28 | 18 | 14 | 14 | 4 |
| SM   | 24 | 16 | 12 | 13 | 4 |
| XS   | 20 | 14 | 12 | 12 | 4 |

Notes on the shape of the ramp (so you can extend or retune it coherently):
- **Icons shrink slower than height** — the icon/height ratio climbs from 0.44 (2XL) to 0.70 (XS):
  small controls keep a legible glyph. The caret is always smaller than the icon at the same size.
- **Spacer is a two-value split**: `8` for the large tiers (height ≥ 36 / font ≥ 16), `4` for the
  tight tiers. It is the gap flanking the label and between adjacent glyphs.

## The derived ramp (computed by the law)

| size | pad-icon `(h−icon)/2` | pad-caret `(h−caret)/2` | radius-pill `h/2` | inset `=pad-caret` | gap `=spacer` |
|------|-----:|-----:|-----:|-----:|-----:|
| 2XL  | 18 | 23 | 32 | 23 | 8 |
| XL   | 12 | 16 | 24 | 16 | 8 |
| LG   | 8  | 11 | 18 | 11 | 8 |
| MD   | 5  | 7  | 14 | 7  | 4 |
| SM   | 4  | 6  | 12 | 6  | 4 |
| XS   | 3  | 4  | 10 | 4  | 4 |

`pad-icon` and `pad-caret` are the icon-side and caret-side inline paddings. `pad-label` (text at an
edge) takes the generous caret-side value. All are integers at every canonical size because the
heights and glyph sizes share parity — a property worth preserving if you add a size.

## The box model & permutations

Layout is `display: flex` with `justify-content: space-between` and the `spacer` as the gap flanking
the label. Reading left → right, the full pattern is:

```
| pad-lead | glyph | spacer | label (fills) | spacer | glyph | pad-trail |
```

The lead/trail paddings come from whichever slot sits at that edge (icon → pad-icon, caret →
pad-caret, label → pad-label). The label takes the remaining space and **text-aligns by what flanks
it**:

| permutation | label text-align | why |
|---|---|---|
| `icon · label · caret` | **center** | flanked on both sides |
| `icon · label` | **end** (right) | neighbour only on the left |
| `label · caret` | **start** (left) | neighbour only on the right |
| `label` | **center** | alone |
| `icon` | center (square) | single glyph, no label |
| `caret` | center (square) | single glyph, no label |
| `caret · label` | **end** | neighbour only on the left |
| `caret · label · icon` | **center** | flanked on both sides |

Rule, stated once: **label flanked both sides → center; only-left → end; only-right → start;
alone/absent → center.** (`label_justify()` in the engine; verified against all eight above.)

Worked example — `2XL · icon · label · caret` (matches the hand-authored spec exactly):
```
| 18 pad | icon 28 | 8 spacer | label(fill) | 8 spacer | caret 18 | 23 pad |
```
Worked example — `MD · icon` (icon-only → square):
```
| 5 pad | icon 18 | 5 pad |   →  width == height == 28
```

## Radius

- **Pill (default for the chip/button family)** = `height / 2` — fully rounded; the geometric
  default the system computes (`radius-pill` column).
- **Soft / sharp** radii are a *brand* choice layered on top, not a geometric law. A defensible soft
  ramp (tunable): 2XL 20 · XL 16 · LG 12 · MD 10 · SM 8 · XS 6. Keep one radius scale per library and
  re-point it with a token; don't set radius per component instance.

## The compact / dense realm — a SEPARATE size system

A tag or badge is **not** just a small button. The **compact / dense realm** — `kbd`, `slider`,
`slider-multi`, `radio`, `switch`, `tag`, `badge`, `chip`, `checkbox` — is its own size system
(geometry-sizing-spec §5.1/§5.2). These controls are *always* compact and dense, and they differ from
the comfortable button ramp on two rules:

1. **They keep the compact pad — NOT `h/2`.** The comfortable controls take `h/2` on a slotless edge;
   `h/2` would *over-pad* a keycap, a count-pill, or a slider thumb. The compact realm keeps
   `2px + box·ratio·density` instead.
2. **They size their box on a dedicated TWO-BAND ramp** — not the comfortable height ramp, not the icon
   ramp. The box is **density-invariant** (density rides the pad/gap, never the box):

| scale | sm | md | lg | band |
|---|---|---|---|---|
| `ui-sm` | 12 | 14 | 16 | **tight** — the `ui-*` band, 2px steps (compact-UI density) |
| `ui-md` (default) | 14 | 16 | 18 | |
| `ui-lg` | 16 | 18 | 20 | |
| `content-sm` | 18 | 22 | 26 | **generous** — the `content-*` band (reading density) |
| `content-md` | 20 | 24 | 28 | |
| `content-lg` | 24 | 28 | 32 | |

The `ui-*` band realizes the tight lane `12·14·16·18·20`; the `content-*` band the generous lane
`18·20·22·24·26·28·32` — mirroring the comfortable ramp's compact-vs-expressive two bands, one tier
down. `scripts/geometry-check.py compact-ramp` prints it; `validate` checks a compact card's `box` against
it and rejects an `h/2` pad on a compact control. (A glyph the compact control *does* carry still
centers in its cell by the same `(box − glyph)/2` law; an icon-only compact control is still square.)

**Global across BOTH realms** — the *rhythm* family: **`caret = font`** (the dropdown mark = text
height) and **`gap = font / 2`**. Density multiplies the *rhythm* only, never the *frame* (box · pad ·
icon) — scaling the frame un-centers the glyph and breaks the square.

> The ramp is not six hand-picked rows: the glyph columns are a **sublinear power law of height**
> (`icon ≈ 2.49·h^0.58`, `font ≈ 2.65·√h`, `caret = font`), so each glyph occupies a *shrinking*
> fraction of a growing box (the optical correction) — *one rule sampled six times*, which is what lets
> any mapped height read off its icon/caret/font. Geometry is arithmetic, not taste.

## Composed padding — containers & lists

> **Containers and lists use the same inside padding for contained sections.** Nesting reuses the
> same `inset`, so boundaries visibly "compose" (stack) — that is the intended look, not a bug.

- A container/section at size *S* uses inner padding = **`inset[S]`** (= the caret-side pad at *S*).
- The gap between gridded/listed items = **`gap[S]`** (= the spacer at *S*).
- A contained control (e.g. an icon-button in a grid) keeps its own square geometry; the container's
  inset sits *around* it. Two nested sections at the same size therefore show `inset + inset` of
  breathing room at their shared edge — the "Composed Padding" effect.

This is what lets a button, the cell it sits in, the section that holds the cells, and the card that
holds the section all share one coherent rhythm with no magic numbers.

## How it lands in the signals/CSS idiom

The reference libraries (`fable-tests/reactive-components`, `adia/gen-ui-kit`) express this ramp as
**CSS custom properties keyed by a `size` / `scale` attribute**, with components reading the tokens —
never hard-coding pixels. The geometry stays declarative and themeable:

```css
/* size ramp as tokens (illustrative — values from the ramp above) */
:where([scale="xl"]) {
  --c-height: 48px; --c-icon: 24px; --c-caret: 16px; --c-font: 18px; --c-spacer: 8px;
}
/* the law, expressed once, reused by every control */
:where(x-button) {
  --c-pad-icon:  calc((var(--c-height) - var(--c-icon))  / 2);
  --c-pad-caret: calc((var(--c-height) - var(--c-caret)) / 2);
  block-size: var(--c-height);
  border-radius: calc(var(--c-height) / 2);            /* pill */
  padding-inline: var(--c-pad-icon) var(--c-pad-caret);
  display: flex; align-items: center; justify-content: space-between; gap: var(--c-spacer);
}
:where(x-button):is([icon-only], :not([label])) {     /* single glyph -> square */
  inline-size: var(--c-height); padding-inline: 0; justify-content: center;
}
```

Properties (`size`, `icon`, `label`, `caret`) are **signals** on the element; the geometry is pure
CSS driven by the reflected `scale`/`size` attribute, so a size change is one attribute write and
zero layout JS. See `platform-baseline.md` for the element/FACE side.

## Verifying geometry

- `python3 scripts/geometry-check.py validate card.json` against a declared spec:
  ```json
  { "component": "x-button", "size": "XL", "slots": ["icon","label","caret"],
    "height": 48, "icon": 24, "caret": 16, "pad_lead": 12, "pad_trail": 16,
    "justify": "center", "radius": "pill", "radius_px": 24 }
  ```
  The checker fails any value that's off the ramp, any edge padding that breaks the law, a wrong
  label justification, or a glyph-only spec that isn't square.
- The most common geometry defects (all caught): a glyph-only button that isn't square; a symmetric
  inline padding (ignoring icon ≠ caret); a hard-coded radius instead of `height/2`; a container
  inset that doesn't match the size's `inset`; a label justification that doesn't follow the flank
  rule.
