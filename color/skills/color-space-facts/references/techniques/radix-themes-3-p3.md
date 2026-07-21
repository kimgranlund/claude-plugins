# Radix Themes 3.0 + Radix Colors P3

**Last verified:** 2026-04-26

Radix Themes 3.0 (March 2024) introduced **Display P3 wide-gamut versions of every color scale**, plus a custom palette generator. Radix Colors is the most semantically-organized open color system available today; the P3 expansion makes it the cleanest option for wide-gamut design tokens.

## What's distinctive

### 12-step semantic scales

Every Radix color (e.g. `blue`, `slate`, `tomato`, `mauve`) has 12 steps — but unlike Tailwind's 50–950 numeric scale, Radix steps are **semantically named** for UI states:

| Step | Use |
|---|---|
| 1 | App background |
| 2 | Subtle background |
| 3 | UI element background |
| 4 | Hovered UI element background |
| 5 | Active / Selected UI element background |
| 6 | Subtle borders and separators |
| 7 | UI element border and focus rings |
| 8 | Hovered UI element border |
| 9 | Solid backgrounds |
| 10 | Hovered solid backgrounds |
| 11 | Low-contrast text |
| 12 | High-contrast text |

This is the strongest argument for Radix as a token system: the 12 steps map to UI roles, so component code reads `var(--blue-9)` for "the solid blue surface" rather than "blue-500".

### P3 wide-gamut alpha colors

Radix 3.0 added P3 versions of every scale, including alpha-channel variants. The P3 alpha colors render with accurate appearance on Apple devices (iOS, iPadOS, macOS, recent iPhones) while gracefully falling back to sRGB on legacy displays.

```css
/* Radix automatically picks the right scale per gamut */
@supports (color: color(display-p3 1 0 0)) {
  :root {
    --blue-9: color(display-p3 0.235 0.471 0.957);
  }
}
:root {
  --blue-9: #3b82f6;
}
```

### Themes 3.0 layout engine

Beyond colors, Themes 3.0 added a layout engine (Container, Flex, Grid, Section) and a **custom palette generator** at radix-ui.com/colors/custom. The generator takes a brand color and derives all 12 semantic steps automatically — lighting up the "I want my custom palette to map to UI roles" use case that other token systems require manual setup for.

## Comparison vs. peers

- **vs. Tailwind v4** ([`tailwind-v4-oklch-palette.md`](./tailwind-v4-oklch-palette.md)) — Tailwind: 11 lightness steps, no semantic role mapping. Radix: 12 semantic steps mapped to UI states. Tailwind for utility-first; Radix for token-driven component libraries.
- **vs. Material HCT** ([`../contemporary/material-hct-color-space.md`](../contemporary/material-hct-color-space.md)) — HCT uses tone deltas to guarantee contrast pairs. Radix uses semantic steps with hand-tuned contrast (steps 11/12 are designed for body text against steps 1/2 surfaces).
- **vs. raw OKLCH** — OKLCH is the math; Radix is the curated artifact. Use OKLCH to *generate* a Radix-compatible scale via the custom palette generator.

## Browser support

Radix Themes 3.0 targets modern browsers (Safari 17+, Chrome 111+, Firefox 113+). The P3 alpha-color story specifically requires `@supports (color: color(display-p3 ...))` (Chrome 111+, Safari 15+, Firefox 113+).

## When to reach for Radix vs alternatives

- **Component-library author** → Radix, because the semantic 12-step scale maps cleanly to component states.
- **Utility-first user** → Tailwind v4, because the numeric 11-step scale fits utility classes.
- **Custom brand palette with role mapping** → Radix custom palette generator (radix-ui.com/colors/custom).
- **Wide-gamut design tokens** → Radix P3 colors are the most polished open implementation.

Sources:
- [Radix Themes 3.0 announcement](https://www.radix-ui.com/blog/themes-3)
- [Radix Colors documentation](https://www.radix-ui.com/colors)
- [Radix custom palette generator](https://www.radix-ui.com/colors/custom)

## Related in this skill

- [`tailwind-v4-oklch-palette.md`](./tailwind-v4-oklch-palette.md) — peer modern utility-first system.
- [`../contemporary/material-hct-color-space.md`](../contemporary/material-hct-color-space.md) — Android equivalent.
- [`css-color-2026-snapshot.md`](./css-color-2026-snapshot.md) — wide-gamut CSS context.
