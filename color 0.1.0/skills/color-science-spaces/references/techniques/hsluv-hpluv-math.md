# HSLuv & HPLuv — Math

Alexei Boronine's **CIELUV-normalized HSL** (2012, refined 2015). The
"missing perceptual HSL" — a cylindrical reparameterization of CIELUV
where saturation goes from 0 to 100 regardless of hue or lightness.

For typical UI work, **OKLCh and OKHSL have superseded HSLuv**. This
document is included for compatibility / legacy use; no TypeScript module
is provided in this skill.

---

## TL;DR

| Space | Hue | Saturation | Lightness | Property |
|---|---|---|---|---|
| **HSLuv** | CIELUV polar hue (degrees) | 0–100 normalized to gamut | CIELUV L* (0–100) | Full hue+lightness covered |
| **HPLuv** | Same | 0–100 (pastel-only) | Same | All in-gamut, but desaturated |

HSLuv answers: "Give me a saturation that's 100 at the maximum-chroma point
of the sRGB gamut at this (hue, lightness)." HPLuv answers: "...at the
maximum-chroma point of the **achievable for ALL hues at this lightness**."

---

## Natural-language description

### Why HSL fails

CSS `hsl()` and HSV are non-perceptual cylindrical reparameterizations of
encoded sRGB. Saturation = 100% means "fully saturated for this hue at
this lightness", but the gamut envelope is irregular — saturated yellow
is much brighter than saturated blue at the same nominal lightness.

### What CIELUV-based HSL gives you

CIELUV is a perceptually uniform color space (the U/V counterpart to
CIELAB). Its polar form CIELChuv gives uniform hue and chroma. But CIELChuv
chroma has no fixed maximum — at lightness 50 with hue 25°, max chroma is
~70 in CIELUV units; at hue 200°, it might be ~150. UI designers want
"saturation 100" to always mean "max for this color."

HSLuv normalizes: $S = 100 \cdot C / C_{\text{max}}(h, L)$ where
$C_{\text{max}}(h, L)$ is the maximum CIELUV chroma achievable in sRGB
at hue $h$ and lightness $L$. So saturation is always in [0, 100] and
always reaches 100 at the gamut edge.

### HPLuv variant

HPLuv uses the **minimum across all hues** for normalization:
$C_{\text{max,pastel}}(L) = \min_h C_{\text{max}}(h, L)$. The result is
that HPLuv at full saturation is achievable for ALL hues — producing
pastels rather than vibrant colors.

---

## Formulas

### Forward HSLuv → CIELChuv → CIELUV → XYZ

Forward pipeline:

```
1. (H, S, L) → (Cmax, h_rad)
   - h_rad = H · π / 180
   - Cmax = computeMaxChromaAtHueAndLightness(h_rad, L)  // sRGB gamut envelope
2. C = (S / 100) · Cmax
3. (L, C, h) → CIELUV (L, U, V) via polar-to-cartesian
4. CIELUV → XYZ via CIE 1976 inverse formulas
```

### Computing $C_{\text{max}}(h, L)$

The gamut envelope at fixed $(h, L)$ is the maximum $C$ such that the
resulting XYZ converts to in-gamut linear sRGB. Boronine derives this
analytically by solving for $C$ at each sRGB face boundary:

For each of 6 face conditions (R=0, R=1, G=0, G=1, B=0, B=1), solve for
$C$ at the given $(h, L)$. Take the smallest positive solution.

Each face condition is linear in $C$:

$$
C \cdot (a_i \cos h + b_i \sin h) = c_i - d_i \cdot L
$$

where $a_i, b_i, c_i, d_i$ depend on the chosen face. Solving gives one
candidate; take minimum across faces.

### CIELUV → XYZ

CIELUV is defined relative to a reference white $(u'_n, v'_n)$:

$$
u' = \frac{U}{13 L} + u'_n, \quad v' = \frac{V}{13 L} + v'_n
$$

Then convert $(u', v', L)$ back to XYZ via:

$$
Y = f^{-1}(L^* / 116), \quad X = -9 Y u' / (u'(v' - 4) - 4 v')
$$

(Similar formulas for $Z$.)

Where $f^{-1}$ is the inverse CIELAB-style nonlinearity.

---

## Implementation

**Not implemented in this skill's TypeScript.** Reasons:

1. For modern UI design tokens, OKLCh and OKHSL (already implemented)
   serve the same purpose with better perceptual uniformity.
2. The gamut-envelope computation is involved (~6 face-conditions × per-hue
   evaluation).
3. Boronine's reference implementation is excellent and well-tested —
   reach for it directly when needed.

If a use case emerges, the structure would be:
- `src/spaces/cieluv.ts` (CIELUV ↔ XYZ — not yet implemented)
- `src/spaces/hsluv.ts` (HSLuv ↔ CIELChuv with gamut normalization)

---

## When to use which

| Need | Use |
|---|---|
| Perceptual color picker for UI | OKHSL (`src/spaces/okhsl.ts`) |
| CSS-compatible cylindrical | OKLCh (`src/spaces/oklch.ts`) |
| Cross-tool compatibility with hsluv.org | HSLuv (external) |
| Legacy systems already using HSLuv | HSLuv (external) |

OKHSL has very similar properties (normalized saturation, cusp-aware shape)
with the advantage of being built on OKLab (a more uniform space than
CIELUV). For new code, prefer OKHSL.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | Not implemented; use OKHSL instead. |
| **hsluv-javascript** | Reference implementation from <hsluv.org>. |
| **hsluv-python**, **hsluv-rust**, **hsluv-go** | Same reference, multiple languages. |
| **Culori** | `mode_hsluv` and `mode_hpluv`. |

---

## Primary sources

- **Boronine, A. (2012, refined 2015)** — HSLuv reference site:
  <https://www.hsluv.org/>
- **HSLuv specification** — <https://www.hsluv.org/comparison/> — paper
  and explanatory comparisons with HSL and CIELChuv.
- **CIE 015:2018** — CIELUV definition.
- **Companion**: [`oklab-xyz-math.md`](./oklab-xyz-math.md) — OKLab is the
  modern alternative to CIELUV for this purpose.
- **Companion**: OKHSL implementation at `src/spaces/okhsl.ts`.
