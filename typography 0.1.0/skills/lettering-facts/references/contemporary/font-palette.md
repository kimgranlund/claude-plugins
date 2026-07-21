---
date: 2026-04-18
coverage: light
peers:
  - ./color-fonts.md
  - ./variable-fonts.md
  - ./opentype-features.md
primary_sources:
  - https://www.w3.org/TR/css-fonts-4/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-palette
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-palette-values
  - https://caniuse.com/css-font-palette
  - https://caniuse.com/css-font-palette-values
  - https://chromestatus.com/feature/5691020776210432
  - https://webkit.org/blog/12420/new-webkit-features-in-safari-15-4/
  - https://developer.apple.com/documentation/safari-release-notes/safari-15_4-release-notes
---

# `font-palette` and `@font-palette-values` — contemporary reference

**Coverage tier**: light
**Last verified**: 2026-04-18
**Sources**: MDN (`font-palette`, `@font-palette-values`), W3C CSS Fonts Module Level 4 §9, caniuse (`css-font-palette`, `css-font-palette-values`), Chrome Status feature 5691020776210432, Safari 15.4 release notes, WebKit blog, Firefox 107 release notes.
**Peer files**: [./color-fonts.md, ./variable-fonts.md, ./opentype-features.md]

<orientation>
This file covers the CSS surface for selecting and customizing palettes declared by a color font: the `font-palette` property and the `@font-palette-values` at-rule. Focus is narrow — palette selection, overrides, dark-mode switching, interaction with `light-dark()`, and practical limitations.

What this file does **not** cover:
- The COLR / CPAL / sbix / CBDT / SVG-in-OT formats themselves — see `./color-fonts.md`.
- Variable-font axis animation of color-font glyphs — see `./variable-fonts.md` §Color Fonts + Variable Axes.
- OpenType feature tags — see `./opentype-features.md`.

All dated claims are scoped to stable releases as of **April 2026**. "Baseline" uses the Web Platform DX Community Group definition.
</orientation>

---

## Definition

`font-palette` is a CSS property that selects among the palettes declared inside a color font's `CPAL` table, or activates an author-authored custom palette declared via `@font-palette-values`.

`@font-palette-values` is an at-rule that declares a named custom palette — either from scratch, from a base-palette in the font, or as a sparse override of specific palette indices.

A color font in this context is one with a `COLR` (v0 or v1) table backed by `CPAL`. sbix and CBDT fonts do not respond to `font-palette` — the bitmap strikes are pre-baked and cannot be recolored. On such fonts, `font-palette` is effectively a no-op.

---

## Browser support (2026-04)

| Engine | First stable version | Release date |
|---|---|---|
| Chromium (Blink) | 101 | 2022-04-26 |
| Edge (Chromium) | 101 | 2022-04-29 |
| Firefox (Gecko) | 107 | 2022-11-15 |
| Safari (WebKit) | 15.4 | 2022-03-14 |
| iOS Safari | 15.4 | 2022-03-14 |
| Android Chrome | 101 | 2022-04-26 |
| Samsung Internet | 19 | 2022-07 |

**Global availability (caniuse 2026-04)**: ~93%. Baseline since 2022; widely supported for over three years.

Safari shipped `font-palette` first (March 2022), even before Chromium. Note that Safari has still not shipped COLRv1 rendering as of Safari 26.5 (2026-04) per caniuse — so Safari's `font-palette` support applies meaningfully only to COLRv0 fonts on that engine.

---

## Syntax

### `font-palette` property

```
font-palette: normal | light | dark | <dashed-ident>
```

- **`normal`** — use the font's default palette (palette index 0 in `CPAL`). Initial value.
- **`light`** — use the palette marked `USABLE_WITH_LIGHT_BACKGROUND` in the font's `CPAL` palette-type bits. Falls back to `normal` if the font has no such palette.
- **`dark`** — use the palette marked `USABLE_WITH_DARK_BACKGROUND`. Falls back to `normal` if absent.
- **`<dashed-ident>`** — reference a custom palette declared via `@font-palette-values --name`. Falls back to `normal` if the named rule doesn't apply to the current font-family.

The property inherits and is animatable as a **discrete** transition (step-change at 50%, not smooth interpolation). See §Limitations.

### `@font-palette-values` at-rule

```
@font-palette-values <dashed-ident> {
  font-family: <family-name> [, <family-name>]* ;  /* required */
  base-palette: <integer> ;                         /* optional */
  override-colors: <index> <color> [, <index> <color>]* ;  /* optional */
}
```

- **`font-family`** (required) — which font family this palette applies to. If the current `font-family` at use-time doesn't match, the rule has no effect.
- **`base-palette`** (optional) — integer index into the font's `CPAL` table to use as the base. Defaults to 0. `base-palette: light` and `base-palette: dark` resolve like the property keywords.
- **`override-colors`** (optional) — comma-separated `<index> <color>` pairs that remap specific palette indices. Indices not listed retain their values from the base palette.

Example:

```css
@font-palette-values --brand-mono {
  font-family: "My Icon Font";
  base-palette: 0;
  override-colors:
    0 oklch(20% 0 0),    /* background layer → near-black */
    1 oklch(92% 0.04 260);  /* foreground layer → light blue */
}

.icon { font-palette: --brand-mono; }
```

---

## Practical examples (mechanics only — not token-generation)

### Dark-mode palette switch for an icon font

```css
:root { font-palette: normal; }

@media (prefers-color-scheme: dark) {
  :root { font-palette: dark; }
}

/* The icon font must declare a dark palette in its CPAL for this to work.
   If it doesn't, dark falls back to normal silently. */
```

### Brand-colored overrides for a stock emoji/icon font

```css
@font-palette-values --brand-noto {
  font-family: "Noto Color Emoji";
  override-colors:
    0 oklch(58% 0.20 260),
    1 oklch(72% 0.18 260),
    2 oklch(85% 0.12 260);
}

.branded-emoji {
  font-family: "Noto Color Emoji", "Apple Color Emoji", sans-serif;
  font-palette: --brand-noto;
}
```

Caveat: the indices `0`, `1`, `2` are font-specific. Noto Color Emoji's index 3 is not the same semantic color as Twemoji's index 3. Tie custom palettes to one `font-family` at a time.

### Tinting a single-palette font

A color font with only one palette can still be recolored via `override-colors`:

```css
@font-palette-values --monochromatic-tint {
  font-family: "My Single Palette Icon Font";
  override-colors: 0 currentColor;  /* all layers render in the element's CSS color */
}

.tinted-icon {
  color: oklch(58% 0.20 260);
  font-palette: --monochromatic-tint;
}
```

`currentColor` works inside `override-colors` (CSS Fonts L4 §9.4), letting a palette inherit from the element's `color` cascade.

---

## Interaction with `prefers-color-scheme`

The canonical dark-mode recipe:

```css
:root {
  font-palette: normal;
}

@media (prefers-color-scheme: dark) {
  :root { font-palette: dark; }
}
```

The keywords `light` and `dark` resolve against the font's `CPAL` palette-type bits (`USABLE_WITH_LIGHT_BACKGROUND`, `USABLE_WITH_DARK_BACKGROUND`). A font that doesn't mark any palettes with these bits falls through to `normal` for both keywords — the declaration does nothing visible.

**Verifying palette type bits**: use `fontTools` to inspect:

```python
from fontTools.ttLib import TTFont
f = TTFont("MyFont.ttf")
print(f["CPAL"].paletteTypes)
# [0, 1, 2]  ←  normal, light-bg, dark-bg (bitfield: 0x01, 0x02)
```

Authoring tools that emit CPAL but don't set palette-type bits produce fonts where `font-palette: dark` fails silently. Glyphs 3, FontLab 8, and Google Fonts' COLRv1 pipeline all set the bits correctly; older pipelines or hand-assembled fonts may not.

For fonts without declared light/dark variants, use custom `@font-palette-values`:

```css
@font-palette-values --custom-dark {
  font-family: "My Color Font";
  override-colors: 0 oklch(85% 0.15 260), 1 oklch(72% 0.12 260);
}

@media (prefers-color-scheme: dark) {
  :root { font-palette: --custom-dark; }
}
```

---

## Fonts shipping declared palettes (2026-04)

| Font | Format | Palettes declared | Notes |
|---|---|---|---|
| Noto Color Emoji | COLRv1 (2023+) | `normal` + `dark` (limited coverage) | Most glyphs resolve both; some only `normal`. |
| Segoe UI Emoji | COLRv1 (Win 11 22H2+) | `normal` + `light` + `dark` | Shipped with Windows 11 dark theme support. |
| Twemoji Mozilla | COLRv0/v1 | `normal` only | No declared variants; use custom overrides. |
| Material Symbols COLRv1 | COLRv1 | `normal` only (Google's baseline build) | Custom brand palettes via `override-colors`. |
| Apple Color Emoji | **sbix** | — | `font-palette` is a no-op on sbix fonts. |
| Nabla (Google Fonts) | COLRv1 variable | `normal` + multiple named | Reference example of multi-palette design. |
| Bungee Spice | COLRv0 | `normal` + alternates | Google Fonts classic. |
| Phosphor Icons Color | COLRv1 | `normal` | Custom overrides for brand tinting. |

The honest state of palette support in 2026-04: **the ecosystem is sparse**. Most COLR fonts ship one palette. Multi-palette fonts are the minority, and fonts with properly-tagged light/dark palette-type bits are a minority within that minority. Custom `@font-palette-values` with `override-colors` is almost always the practical path.

---

## `light-dark()` vs `font-palette`

These are two different layers in the rendering stack:

- **`light-dark(light-value, dark-value)`** — a CSS *color function* (Chrome 123+, Firefox 120+, Safari 17.5+; Baseline 2024). Resolves to one of two CSS color values based on the computed `color-scheme`. Applies to *any* CSS property that accepts a color: `color`, `background-color`, `border-color`, `fill`, `stroke`.
- **`font-palette`** — a CSS *property* that selects among palettes declared inside the font file. Applies only to color-font glyphs rendered via `COLR` + `CPAL`.

They operate on different surfaces:

```css
:root {
  color-scheme: light dark;

  /* Element-level text color — resolves from CSS */
  color: light-dark(oklch(20% 0 0), oklch(90% 0 0));

  /* Font-level color-layer palette — resolves from CPAL */
  font-palette: light;  /* and an @media (prefers-color-scheme: dark) rule for 'dark' */
}
```

The element `color` controls the monochrome text rendering (and COLR layers that reference `currentColor`); `font-palette` controls the palette-indexed COLR layers inside emoji or color glyphs.

In practice, both are used together: `light-dark()` for element color and background; `font-palette: dark` for color-font glyphs that declare dark palettes; a `@media (prefers-color-scheme: dark)` block wrapping custom `@font-palette-values` for fonts without declared dark variants.

As of 2026-04, `font-palette` does **not** accept `light-dark()` as a value — the property takes only keywords and `<dashed-ident>`, not color functions. If you want smooth dark-mode response on a font without declared palettes, use custom `@font-palette-values` + media query, not `font-palette: light-dark(...)`.

---

## Limitations

### Palette values are discrete; no interpolation

Per CSS Fonts Level 4 §9.1, transitions between `font-palette` values are **discrete** — the browser swaps palette at the 50% mark of the transition duration, not blending indices linearly. Confirmed in Chromium implementation notes (2023) and shipping behavior across Firefox, Safari, Chrome as of 2026-04.

```css
/* This does NOT smoothly cross-fade between palettes */
.icon {
  font-palette: --palette-a;
  transition: font-palette 400ms ease;  /* step-change at 200ms */
}
.icon:hover { font-palette: --palette-b; }
```

For animated color-font rendering, use `font-variation-settings` on a COLRv1 variable font instead — see `./variable-fonts.md` §Animation and §Color Fonts + Variable Axes.

### `override-colors` is a sparse override, but must be complete for undeclared palettes

`override-colors` remaps only the indices you list; indices not listed retain their values from the base palette. This is a sparse override.

However, if the base palette doesn't exist (e.g., `base-palette: 5` when the font has 3 palettes), the rule falls back silently to `base-palette: 0` or `normal`. Always confirm palette count before relying on high indices.

### Animating between palettes

Not supported natively. JavaScript can swap `font-palette` values at discrete intervals, which the browser will honor as instantaneous changes — no cross-fade. To animate color-glyph rendering smoothly, use a variable COLRv1 font with axis-driven color-stop positions.

### sbix and CBDT fonts

`font-palette` is a no-op on sbix (Apple Color Emoji) and CBDT (legacy Noto Color Emoji) fonts. These formats pre-bake bitmaps; there's no palette to remap. On Safari rendering Apple Color Emoji, `font-palette: dark` does nothing.

### Performance

Swapping `font-palette` at runtime invalidates the glyph cache for the affected font — the rasterizer re-renders affected glyphs with the new palette colors. On COLR fonts with many layers per glyph, this can be a measurable repaint cost (1–5 ms for ~100 visible glyphs). Animating palette switches on scroll or hover is fine for small UIs; large grids of color-font glyphs may stutter on mid-range devices.

### Forced Colors Mode

In Windows High Contrast / `forced-colors: active`, the OS may override palette colors with system palette. `forced-color-adjust: none` preserves the font-defined palette; `forced-color-adjust: auto` (default) lets the OS remap. The right choice depends on whether the color carries meaning (auto, accept remap) or is decorative brand identity (none, preserve). See `./color-fonts.md` §Accessibility.

### Custom palettes scoped to one `font-family`

`@font-palette-values` must list the applicable `font-family`. A palette declared for "Noto Color Emoji" is ignored when the active font is "Twemoji Mozilla." If you need the same palette semantic across multiple fonts, declare separate `@font-palette-values` rules per font, because palette indices are font-specific — there is no canonical "index 0 = skin tone" across fonts.

### No read-back of current palette colors

There's no CSS or JavaScript API to query "what RGB value is palette index 0 currently resolving to?" The browser resolves the palette internally for rendering and doesn't expose the resolved color values. If a surrounding layout needs a color matching the glyph palette (e.g., a border matching the emoji skin-tone), author both the palette override and the matching CSS color side-by-side, keyed off the same source.

---

## Practical recommendations

1. **Prefer font-declared palettes over custom ones.** If the font ships `light` and `dark` palettes with proper CPAL type-bits, use the keywords. Custom palettes couple CSS to specific font internals and break when the font is swapped.
2. **Override only when brand color is mandatory.** If a product spec requires "logo must be exactly #5B8DEF in all contexts," `@font-palette-values` + `override-colors` is the right answer. For "logo looks nice in the brand palette," the font's default palette is usually fine.
3. **Test Safari rendering explicitly.** Safari has supported `font-palette` since 15.4 (March 2022) but has **not** shipped COLRv1 rendering as of Safari 26.5 (2026-04). `font-palette` on a COLRv1 font in Safari selects a palette the engine can't render — the font falls back to monochrome. `font-palette` works meaningfully in Safari only on COLRv0 fonts.
4. **Keep palette count low (≤3) for maintainability.** A color font shipping `normal`, `light`, `dark` + a handful of branded custom palettes is manageable. A font shipping 12 palettes tends to accumulate inconsistent definitions and becomes a QA liability.
5. **Pair `font-palette` changes with a `@media (prefers-color-scheme: dark)` rule, not JavaScript.** CSS media queries respect OS-level preference changes automatically (including mid-session theme switches in modern OSes); JS palette-swap code tends to drift out of sync.
6. **Use `currentColor` in `override-colors` for tintable monochrome.** A single-palette color font becomes a CSS-tintable glyph set with one line:
   ```css
   @font-palette-values --tint {
     font-family: "MyFont";
     override-colors: 0 currentColor;
   }
   ```
   Then `color: red` applied to elements using `font-palette: --tint` recolors the glyph layers per-element.
7. **Verify CPAL palette-type bits with `fontTools`** before relying on `font-palette: light`/`dark` keywords. A font missing those bits will silently fall through to `normal`, and you'll wonder why dark mode isn't switching.
8. **Don't animate `font-palette` expecting smooth transitions.** Discrete step-change. If you need smooth, use `font-variation-settings` on COLRv1 + variable axes.

---

## Anti-patterns

1. **Relying on `font-palette: dark` without verifying the font has a dark palette.** Silent fallback to `normal`; "dark mode does nothing" bug.
2. **Hardcoding palette indices across fonts.** `override-colors 0 red` means different layers on different fonts. Always scope `@font-palette-values` to one `font-family`.
3. **Using `font-palette` for sbix-based Apple Color Emoji.** No effect. If you need colored emoji with dark-mode palette swap, ship a COLRv1 emoji font (Noto Color Emoji, Twemoji Mozilla).
4. **Attempting smooth palette animation.** Discrete per spec. Use variable-axis animation on COLRv1 if you need interpolation.
5. **Declaring `@font-palette-values` without `font-family`.** Required field; the rule is ignored if missing.
6. **Over-using custom palettes for minor tints.** Each custom palette is a maintenance surface. Prefer CSS `color` + `currentColor` in overrides over declaring separate palettes for each brand variant.
7. **Expecting `font-palette` to change which font is used.** It only selects a palette within the already-selected font. `font-family` is the control for font selection.

---

## Sources

URLs retrieved **2026-04-18** unless noted.

- **W3C CSS Fonts Module Level 4 §9 (Color Font Support)**: https://www.w3.org/TR/css-fonts-4/#font-palette-prop — `font-palette` property, `@font-palette-values` at-rule, discrete transition semantics.
- **MDN — `font-palette`**: https://developer.mozilla.org/en-US/docs/Web/CSS/font-palette — syntax, keyword resolution, browser compat.
- **MDN — `@font-palette-values`**: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-palette-values — at-rule descriptors, `base-palette`, `override-colors`.
- **MDN — `light-dark()`**: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark — Baseline 2024, element-color function.
- **caniuse — `css-font-palette`**: https://caniuse.com/css-font-palette — ~93% global availability 2026-04.
- **caniuse — `css-font-palette-values`**: https://caniuse.com/css-font-palette-values — same timeline.
- **Chrome Status — `font-palette` and `@font-palette-values`**: https://chromestatus.com/feature/5691020776210432 — shipping Chrome 101 (2022-04).
- **Safari 15.4 release notes**: https://developer.apple.com/documentation/safari-release-notes/safari-15_4-release-notes — initial `font-palette` support (2022-03).
- **WebKit blog — "New WebKit Features in Safari 15.4"** (2022): https://webkit.org/blog/12420/new-webkit-features-in-safari-15-4/ — `font-palette` announcement.
- **Firefox 107 release notes**: https://www.mozilla.org/en-US/firefox/107.0/releasenotes/ — `font-palette` + COLRv1 simultaneous ship (2022-11).
- **Microsoft Learn — CPAL table**: https://learn.microsoft.com/en-us/typography/opentype/spec/cpal — palette-type bits (LIGHT/DARK background) that underpin the `light`/`dark` keywords.
- **Related**: `./color-fonts.md` for the COLR/CPAL/sbix/CBDT/SVG-in-OT format landscape; `./variable-fonts.md` §Color Fonts + Variable Axes for smooth animated color via variable axes.
