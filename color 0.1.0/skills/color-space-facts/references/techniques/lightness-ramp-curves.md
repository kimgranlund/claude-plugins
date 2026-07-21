# Lightness Ramp Curves — Math

The progression of lightness values across a design-token palette: 50 → 100
→ 200 → ... → 900 (Tailwind), or 1 → 2 → ... → 12 (Radix). The **curve**
of this progression determines whether the palette feels "natural" — evenly
stepped to the eye — or "lumpy."

This document covers the four curve shapes commonly used and the published
stops from Tailwind v4 and Radix Themes 3.

---

## TL;DR

- **Linear in OKLab L** is the perceptually-even default. Equal $t$ steps =
  equal perceived steps.
- **Tailwind v4** uses 11 published OKLab L stops: 50, 100, ..., 950. They're
  not uniformly spaced — they're tuned for design-system usefulness.
- **Radix Themes 3** uses 12 semantic stops (App background, Subtle BG, UI,
  Hover, Active, Border, ..., High-contrast text). Even less uniform.
- **Gamma curves** (`t^γ`) emphasize one end. Use when you want more
  granularity in either dark or light tones.
- **Smoothstep** ($3t^2 - 2t^3$) emphasizes the middle. Useful when most
  palette use happens at mid-tones.

---

## Natural-language description

### The general curve choice

A lightness ramp is a function $f : [0, 1] \to [L_{min}, L_{max}]$ that maps
a parameter $t$ (your step number normalized) to an OKLab $L$ value.

Four choices cover most practical cases:

1. **Linear** ($f(t) = L_{min} + t(L_{max} - L_{min})$): equal-perceptual-step.
   The default unless you have a specific reason.
2. **Gamma** ($f(t) = L_{min} + t^\gamma (L_{max} - L_{min})$):
   - $\gamma > 1$ "slow start" — more steps near $L_{min}$ (dark end).
   - $\gamma < 1$ "fast start" — more steps near $L_{max}$ (light end).
3. **Smoothstep** ($f(t) = L_{min} + (3t^2 - 2t^3)(L_{max} - L_{min})$):
   compresses the endpoints, expands the middle.
4. **Published stops** (Tailwind, Radix): non-parametric, hand-tuned to
   specific design goals.

Choose by **what each step is used for**. If steps 50-200 are background-
only and 700-950 are text, you may want more granularity at the extremes (a
small $\gamma$ might help). If you use the mid-tones (300-700) most heavily
for UI surfaces, smoothstep gives them more resolution.

### Why Tailwind v4 picked these specific stops

Tailwind v4 chose its L values to satisfy several constraints simultaneously:

- **Sufficient contrast at adjacent steps** for borders/dividers (e.g., 100
  on 50, 200 on 100).
- **WCAG AA contrast at standard pairings** (e.g., 700 text on 50 BG).
- **Perceptually-recognizable identity at each step** ("this is 500-class").
- **Vivid mid-tones** (the 400-600 range gets the most chroma).

The result is non-uniform spacing tuned for design-system ergonomics rather
than mathematical evenness.

### Why Radix 3 picked these specific stops

Radix 3's 12 steps have **explicit semantic roles**:

| Step | Role |
|---|---|
| 1 | App background |
| 2 | Subtle background (e.g., card BG) |
| 3 | UI element BG |
| 4 | UI element hover |
| 5 | UI element active/pressed |
| 6 | Subtle borders, separators |
| 7 | UI borders |
| 8 | Hover borders, focus rings |
| 9 | Solid colors (brand accent) |
| 10 | Solid color hovers |
| 11 | Low-contrast text |
| 12 | High-contrast text |

The L progression is tuned so each step has the right perceptual contrast
against its neighbors for the intended role.

---

## Formulas

### Linear ramp

$$
f(t) = L_{min} + t \cdot (L_{max} - L_{min})
$$

### Gamma ramp

$$
f(t) = L_{min} + t^\gamma \cdot (L_{max} - L_{min})
$$

For $\gamma = 1$, equivalent to linear. Common values:
- $\gamma = 2$ — slow start (more dark detail)
- $\gamma = 0.5$ — fast start (more light detail)

### Smoothstep

The smoothstep function $S(t) = 3t^2 - 2t^3$ has derivative zero at $t = 0$
and $t = 1$:

$$
f(t) = L_{min} + (3t^2 - 2t^3) \cdot (L_{max} - L_{min})
$$

Symmetric: $S(0.5) = 0.5$. Soft endpoints.

### Tailwind v4 OKLab L stops

| Step | L value | Notes |
|---|---|---|
| 50 | 0.985 | App background, very light |
| 100 | 0.967 | Background tier 2 |
| 200 | 0.922 | Subtle background |
| 300 | 0.870 | Light UI |
| 400 | 0.708 | Mid-light (jump to mid) |
| 500 | 0.554 | True mid-tone (brand axis) |
| 600 | 0.446 | Mid-dark |
| 700 | 0.371 | Body text on light |
| 800 | 0.269 | Headings on light |
| 900 | 0.205 | High emphasis text |
| 950 | 0.130 | Maximum contrast |

Notice the **non-uniform spacing**: 50 → 100 → 200 → 300 are tightly packed
(L deltas of 0.018, 0.045, 0.052), then 300 → 400 jumps by 0.162.
This is intentional — backgrounds need more granular variation than text.

### Radix Themes 3 light-mode L stops

| Step | L value | Role |
|---|---|---|
| 1 | 0.995 | App BG |
| 2 | 0.988 | Subtle BG |
| 3 | 0.965 | UI BG |
| 4 | 0.930 | Hover |
| 5 | 0.879 | Active |
| 6 | 0.821 | Subtle border |
| 7 | 0.756 | Border |
| 8 | 0.673 | Hover border |
| 9 | 0.564 | Solid (brand) |
| 10 | 0.481 | Solid hover |
| 11 | 0.396 | Low-contrast text |
| 12 | 0.180 | High-contrast text |

Step 12 (the darkest) jumps significantly from step 11 — high-contrast text
needs to be clearly darker than low-contrast text.

---

## Implementation

Canonical TypeScript: [`src/interpolation/lightness-curves.ts`](../../../../color-science-project-files/src/interpolation/lightness-curves.ts).

Exports:
- `linearRamp(t, lMin?, lMax?)` — linear curve
- `gammaRamp(t, gamma, lMin?, lMax?)` — gamma curve
- `perceptualRamp(t, lMin?, lMax?)` — alias for linear (OKLab L is already perceptual)
- `smoothstepRamp(t, lMin?, lMax?)` — soft-endpoint S-curve
- `TAILWIND_V4_L_STOPS`, `tailwindV4LAtStep(step)` — published Tailwind values
- `RADIX_THEMES_3_L_STOPS_LIGHT`, `radixLightLAtStep(step)` — published Radix values

```ts
export function gammaRamp(t: number, gamma: number, lMin = 0, lMax = 1): number {
  return lMin + Math.pow(t, gamma) * (lMax - lMin);
}

export const TAILWIND_V4_L_STOPS: readonly number[] = [
  0.985, 0.967, 0.922, 0.870, 0.708, 0.554,
  0.446, 0.371, 0.269, 0.205, 0.130,
];

export function tailwindV4LAtStep(step: number): number {
  const stepMap: Record<number, number> = {
    50: 0, 100: 1, 200: 2, 300: 3, 400: 4, 500: 5,
    600: 6, 700: 7, 800: 8, 900: 9, 950: 10,
  };
  const idx = stepMap[step];
  if (idx === undefined) throw new Error(`Tailwind step must be 50/100/200/.../950 (got ${step})`);
  return TAILWIND_V4_L_STOPS[idx];
}
```

Test vectors verify endpoint anchoring, mid-point values for parametric
curves, and exact lookup for published stops.

---

## Worked example: building an 11-step palette in OKLCh

Pick a hue (e.g., 264° for blue) and a chroma profile (e.g., max chroma at
step 500, tapering at the ends). For each Tailwind step:

1. $L = \text{tailwindV4LAtStep}(\text{step})$
2. $C$ = chroma curve (e.g., bell-shaped peaking at step 500)
3. $h = 264°$ (constant per ramp)
4. Convert OKLCh → linear sRGB → encoded sRGB → hex.

The chroma curve typically follows the gamut cusp: a single hue's gamut is
widest near the cusp $L$, narrower at the dark and light ends. See
[`ottosson-cusp-algorithm.md`](./ottosson-cusp-algorithm.md) for finding
the cusp.

---

## Edge cases

- **`t < 0` or `t > 1`**: defined mathematically (extrapolation) but produces
  out-of-range $L$. Caller should clamp `t`.
- **`gamma = 0`**: undefined behavior (division-by-zero analogue). Use `gamma > 0`.
- **`gamma → ∞`**: ramp degenerates to a step function at the endpoints.
- **Out-of-range step number**: `tailwindV4LAtStep` and `radixLightLAtStep` throw.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/interpolation/lightness-curves.ts` — all four curve types + published stops. |
| **Tailwind v4** | Color generation script at <https://github.com/tailwindlabs/tailwindcss/tree/main/packages/tailwindcss>. |
| **Radix Themes 3** | Palette generator at <https://www.radix-ui.com/colors/custom>. |
| **Culori** | `interpolateScaleStops(...)` for arbitrary-stop palettes. |
| **chroma.js** | `chroma.scale(...).domain(stops)` supports irregular stops. |

---

## Primary sources

- **Tailwind v4 release** (Jan 2025) — first major design system to ship a
  default OKLab-tuned palette. Tailwind v4.2 (mid-2025) added Mauve, Olive,
  Mist, Taupe families using the same L stop convention.
- **Radix Themes 3** (Mar 2024) — published the 12-step P3-capable semantic
  palette with the role mapping above.
- **Material Design 3 tonal palettes** — uses HCT (Hue + CAM16 Chroma + L*)
  with a 13-step tone scale (0, 10, 20, ..., 100). Different convention but
  similar goal.
- **Companion**: [`oklab-xyz-math.md`](./oklab-xyz-math.md) — what OKLab L
  represents.
- **Companion**: [`ottosson-cusp-algorithm.md`](./ottosson-cusp-algorithm.md) —
  finding the cusp for chroma-profile design.
