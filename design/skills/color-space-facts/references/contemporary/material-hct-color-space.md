# Material HCT — Hue, Chroma, Tone

**Last verified:** 2026-04-26

HCT is Google's color space for Material 3 dynamic color. It powers every Android app's themed surfaces since 2022 — making it one of the most-deployed perceptual color spaces in production today.

## What HCT is

HCT = **CAM16 hue + CAM16 chroma + CIE L\* tone**. Three coordinates, each measuring a perceptually meaningful quantity:

- **H (hue)** — CAM16 hue angle, perceptually uniform unlike sRGB-derived hue.
- **C (chroma)** — CAM16 chroma, measuring colorfulness independently of lightness.
- **T (tone)** — CIE L* (perceived lightness), 0 = black, 100 = white.

The split design — hue + chroma from CAM16, tone from L* — gives HCT a contrast guarantee that pure CAM16 doesn't: **a +40 tone delta produces ~3:1 WCAG contrast; a +50 delta produces ~4.5:1**. This is the property Material 3's tonal palettes lean on.

## How it differs from OKLCH

OKLCH and HCT have the same goals (perceptually uniform, CSS-friendly cylindrical coordinates) but different math.

| | **OKLCH** | **HCT** |
|---|---|---|
| Author | Björn Ottosson, 2020 | Google Material team, 2022 |
| Lightness math | OKLAB-derived (LMS cone simulation + cube-root) | CIE L\* (1976) |
| Hue/chroma source | OKLAB transform | CAM16 |
| Contrast guarantee | None inherent (need APCA / WCAG check) | +40 tone ≈ 3:1, +50 ≈ 4.5:1 |
| Native CSS support | `oklch()` Baseline 2023 | None — library only |
| Adoption | Web (Tailwind v4, Radix Themes 3) | Android Material 3 (every Android app since 2022) |

For web work, **OKLCH is the default** because of native CSS support. For Android (or cross-platform that targets Android natively), **HCT** matches the platform's contrast guarantees and tonal-palette generation.

## Tonal palettes

Material 3 generates 13 tones per color (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100) at constant H + C. The +40 / +50 contrast guarantee lets the system pick contrasting pairs deterministically:

- Surface (Tone 90) + On-surface (Tone 10) → 4.5:1+ guaranteed
- Primary (Tone 40) + On-primary (Tone 100) → 4.5:1+ guaranteed

This is what makes Material 3's "dynamic color" work: extract a seed color from the user's wallpaper, derive HCT tonal palettes, render with guaranteed contrast pairs without needing per-color contrast checks.

## Library

`material-color-utilities` ([github.com/material-foundation/material-color-utilities](https://github.com/material-foundation/material-color-utilities)) — official Google library; available in Dart, Java, TypeScript, Swift, C++, Objective-C. Implements HCT, tonal palettes, dynamic color schemes, scheme variants (Tonal Spot, Vibrant, Expressive, Content, Neutral, Monochrome, Fidelity, Rainbow, Fruit Salad).

## When to reach for HCT vs alternatives

- **Cross-platform with Android target** → HCT, because Android's design system already uses it natively.
- **Web only, modern browsers** → OKLCH, because native CSS support eliminates the runtime library.
- **Iconography / single-tone derivation** → either; both produce coherent ramps.
- **APCA-checked contrast** → Use OKLCH for derivation + APCA for verification ([`apca-myndex-contrast.md`](../../../color-contrast-facts/references/techniques/apca-myndex-contrast.md), color-contrast-facts) — HCT's WCAG-tuned tone deltas don't translate directly to APCA Lc thresholds.

Sources:
- [material-foundation/material-color-utilities](https://github.com/material-foundation/material-color-utilities)
- [Material 3 dynamic color overview](https://m3.material.io/styles/color/dynamic-color/overview)
- [The Science of Color & Design (Google blog)](https://material.io/blog/science-of-color-design)
