# CSS Color 2026 — Spec & Baseline Snapshot

**Last verified:** 2026-04-26

The modern CSS color stack is now broadly shipped. By April 2026, OKLCH, `color-mix()`, relative color syntax, `light-dark()`, and `contrast-color()` are all Baseline. The recipes below assume these are available and use them as the default.

## Spec map (April 2026)

| Module | Status | What's new |
|---|---|---|
| **CSS Color 4** | CR Draft, last republished 2026-02-27 | OKLCH, OKLAB, LCH, LAB, Display P3, Rec2020, the `color()` function — all shipped |
| **CSS Color 5** | Working Draft | `color-mix()`, relative color syntax (`oklch(from base ...)`), `light-dark()`, `device-cmyk()`, `@color-profile` |
| **CSS Color 6** | Editor's Draft | `contrast-color()`, `color-layers()` |

Sources: [W3C CSS Color 4 (CR)](https://www.w3.org/TR/css-color-4/), [CSS Color 5 (WD)](https://www.w3.org/TR/css-color-5/), [drafts.csswg.org/css-color-6](https://drafts.csswg.org/css-color-6/).

## Baseline interop snapshot

| Feature | Chrome | Firefox | Safari | Status |
|---|---|---|---|---|
| `oklch()` / `oklab()` / `lch()` / `lab()` | 111 | 113 | 16.4 | **Baseline 2023** |
| `color()` function (`display-p3`, `rec2020`) | 111 | 113 | 15+ | **Baseline 2023** |
| `color-mix()` | 111 | 113 | 16.2 | **Baseline 2023** |
| Relative color syntax `oklch(from …)` | 119 | 128 | 16.4 | **Baseline (full cross-engine)** |
| `light-dark()` | 123 | 120 | 17.5 | **Baseline 2024** |
| `contrast-color()` | 147 (Mar 2026) | 146 | 26 | **Newly Available 2026** |
| `@media (dynamic-range: high)` | shipped | shipped | shipped | Baseline |
| `dynamic-range-limit` | partial | partial | partial | Newer; controls HDR tone mapping |
| `accent-color` | shipped | shipped | partial | Safari still incomplete on some controls |

Source: [MDN color value reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value), [caniuse css-relative-colors](https://caniuse.com/css-relative-colors), [WebKit blog: contrast-color()](https://webkit.org/blog/16929/contrast-color/).

## `color-contrast()` is dead — `contrast-color()` is what shipped

The CSS Color 5 draft once defined `color-contrast()` (with a list of candidate colors and an algorithm parameter). **It was dropped.** The replacement, `contrast-color()`, shipped in CSS Color 6 in 2026 — but with an important constraint: it returns only black or white, and the algorithm is intentionally unspecified until the contrast-algorithm question settles.

Practical implication: `contrast-color()` is great for "give me readable text on this surface, automatically" when black/white satisfies the design. It is *not* a general contrast picker. For richer contrast logic — including APCA-aware color selection — use [`apcach`](https://github.com/antiflasher/apcach) at build time or runtime.

## The modern token recipe

All of these primitives compose into a single dual-mode design-token pattern. Derive everything from one OKLCH anchor:

```css
:root {
  /* Anchor */
  --brand-h: 250;
  --brand-c: 0.18;

  /* Light/dark mode tokens */
  color-scheme: light dark;
  --bg:          light-dark(oklch(99% 0.005 var(--brand-h)), oklch(15% 0.01 var(--brand-h)));
  --fg:          light-dark(oklch(20% 0.02 var(--brand-h)), oklch(95% 0.01 var(--brand-h)));
  --brand:       oklch(60% var(--brand-c) var(--brand-h));
  --brand-hover: oklch(from var(--brand) calc(l - 0.05) c h);
  --muted:       color-mix(in oklab, var(--fg) 50%, var(--bg));
  --on-brand:    contrast-color(var(--brand)); /* black or white per spec */
}

/* Graceful fallback for the small subset of users still on legacy engines */
@supports not (color: oklch(50% 0.1 0)) {
  :root {
    --bg: white;
    --fg: black;
    --brand: hsl(250 70% 50%);
  }
}
```

Compose these primitives once at the token layer, then components consume only semantic tokens. See also [`apca-myndex-contrast.md`](../../../color-science-accessibility/references/techniques/apca-myndex-contrast.md) (color-science-accessibility) for picking text colors against a surface using APCA Lc thresholds rather than `contrast-color()`'s black/white heuristic.

## Known gotchas

- **Safari `accent-color`** does not adjust every form control per spec — fall back to native styling for affected controls.
- **Firefox `light-dark()` images** behind a flag through ~150; image-typed `light-dark()` is the latest landing surface.
- **Wide-gamut overflow.** Authoring in `oklch()` / `color()` does not automatically gamut-map for sRGB-only displays — pair with `@media (color-gamut: p3)` when wide-gamut output meaningfully changes the brand.
- **`light-dark()` requires `color-scheme`.** Without `color-scheme: light dark` set on `:root`, the second argument never fires.
- **Relative color syntax with `from currentColor`** can be a footgun in cascade — `currentColor` resolves at use time, not authorship time.

## Why this matters for the modern stack

Before 2024, "color tokens" meant maintaining two parallel palettes (one for light, one for dark) and shipping a contrast-checked combinatorial matrix. By 2026 that whole approach is obsolete. With `oklch(from …)` for derivation, `color-mix()` for blends, `light-dark()` for dual mode, and `contrast-color()` for binary text-on-surface picks, a complete dual-mode token system fits in ~30 lines of CSS keyed off one or two OKLCH anchors. Use this default; reach for runtime libraries (Culori, ColorAide, `apcach`) only when you need APCA-aware contrast selection or wide-gamut math the browser can't express.
