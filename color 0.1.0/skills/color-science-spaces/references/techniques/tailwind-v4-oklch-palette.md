# Tailwind v4 — Default OKLCH Palette

**Last verified:** 2026-04-26

Tailwind v4 (January 2025) shipped with a **default palette built in OKLCH targeting the Display P3 gamut**. This is the first major mainstream design system to default to a perceptual-uniform color space — and the migration is the largest single design-system shift of 2025.

## What changed

Pre-v4 (v3 and earlier) palette was HSL-derived sRGB hex values. v4's palette is generated in OKLCH and serialized as `oklch()` declarations in the default CSS:

```css
/* Tailwind v3 */
--color-blue-500: #3b82f6;

/* Tailwind v4 */
--color-blue-500: oklch(62.3% 0.214 259.815);
```

Output gamut: P3 where supported, sRGB-fallback otherwise (the OKLCH values are gamut-mapped at compile time per the chosen target).

## Implications

- **Wider gamut on Apple devices.** OKLCH-authored colors produce more vivid output on P3 displays without changing the source declarations. iOS/iPadOS, modern Macs, and recent iPhones see the gamut benefit; sRGB displays render the gamut-mapped fallback.
- **Perceptual uniformity across the 11-step scale.** Every `*-50` through `*-950` step is uniform in lightness, so cross-color comparisons (e.g. "blue-500 next to green-500") look balanced rather than blue-heavy.
- **Browser floor: Safari 16.4+, Chrome 111+, Firefox 128+.** v4 dropped support for older engines as part of the Oxide engine launch.

## v4.2 additions (Mauve, Olive, Mist, Taupe)

v4.2 added four "earth tone" palettes alongside the existing 22-color set, also OKLCH-derived. These fill in the under-represented muted/earthy region of color space and are commonly used for content surfaces, ghost buttons, and editorial themes.

Source: [superhighway.dev: Tailwind v4.2 new palettes](https://superhighway.dev/tailwind-v4-2-new-palettes).

## Migration notes

- **Existing v3 hex values still work.** v4 doesn't force a re-author; the palette change applies to *new* uses of the default colors.
- **Custom palettes can be authored in OKLCH** via the `@theme` block — recommend authoring all new palettes this way.
- **Browser-support gate.** If your support matrix predates Safari 16.4, you cannot use the v4 default palette as-is; ship v3 fallback values via `@supports` or downgrade.

## Why this matters for the broader landscape

Tailwind v4 normalizes OKLCH for non-design-system audiences. Before v4, OKLCH was a niche choice for design-system authors familiar with perceptual color. After v4 (used by ~25% of frontend stacks per State of CSS surveys), OKLCH is the default the typical web developer encounters when they `npm i tailwindcss`. This is the single largest move toward perceptual color in mainstream web tooling.

Sources:
- [Tailwind v4 release post (Jan 2025)](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind v4.2 new palettes](https://superhighway.dev/tailwind-v4-2-new-palettes)
- [Tailwind colors reference](https://tailwindcss.com/docs/colors)

## Related in this skill

- [`bjorn-ottosson-oklab-articles.md`](../contemporary/bjorn-ottosson-oklab-articles.md) — OKLCH foundations.
- [`css-color-2026-snapshot.md`](./css-color-2026-snapshot.md) — broader CSS Color baseline.
- [`radix-themes-3-p3.md`](./radix-themes-3-p3.md) — peer modern token system.
