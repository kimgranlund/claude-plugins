# Pointer's Gamut — Math

The empirical boundary of **real-world surface colors** — what paint, dye,
ink, fabric, and natural materials can actually produce. About 75% of the
human visual gamut. Useful for **physical-feasibility checks** on a
generated palette: a color outside Pointer's gamut can be displayed on a
wide-gamut HDR screen but probably can't be reproduced as a paint or print.

---

## TL;DR

Pointer (1980) compiled measurements of 4,089 real surface reflectances
and computed the chromaticity envelope. The result, tabulated by hue,
gives the maximum **chroma achievable as a real surface** at each
combination of (hue, lightness Y).

The data is published as a lookup table — 16 hue angles × 16 lightness
values = 256 chroma maxima.

**No TypeScript module in this skill** — use cases are specialized
(palette design for physical media). The math is a simple lookup +
bilinear interpolation if needed.

---

## Natural-language description

### Visible vs reproducible gamut

The human visual system can perceive a much wider range of colors than
any physical pigment or dye can produce. Spectral lasers, saturated LEDs,
and certain phosphors can produce colors outside the surface-color gamut.

Pointer's question: of all the colors the eye can see, **which ones can
actually exist as a physical surface**? A surface that's not self-emissive
just modifies an illuminant via reflectance $R(\lambda) \in [0, 1]$. The
constraint $R \le 1$ everywhere means surface colors can't be brighter
than the illuminant, and the spectral shape constraints (no negative
reflectances, continuous functions) further restrict the gamut.

Pointer measured 4,089 real-world surfaces (paints, dyes, plants, minerals,
human skin, fabrics) and computed the convex hull of their chromaticities
under Illuminant D65. The result: a gamut substantially smaller than
the visible gamut.

### Why this matters

For palette design intended for physical media (printing, paint,
embroidery), checking Pointer's gamut catches unrealizable colors before
they hit production. A color in **sRGB but outside Pointer's gamut** is
displayable but unprintable.

For purely-digital design (UI, web, screen-only art), Pointer's gamut is
mostly a curiosity — the display constraints (sRGB / P3 / Rec.2020) bind
tighter than the surface-color constraints.

### The data structure

Pointer published the gamut as a table of maximum CIELAB $C^*$ values at
selected $(L^*, h^\circ)$ pairs. The table is sparse (16 hues × 16
lightness levels). Bilinear interpolation gives intermediate values.

The original Pointer 1980 data is at the D65 white point with the 2°
observer. Modern reanalyses (Buck, Pointer & van der Veen 2005) refined
the data.

---

## Mathematical structure

For a given chromaticity $(x, y)$ in CIE 1931, **is it in Pointer's
gamut?**

1. Convert $(x, y, Y)$ to CIELAB $(L^*, a^*, b^*)$.
2. Compute hue: $h = \text{atan2}(b^*, a^*) \cdot 180/\pi$.
3. Compute chroma: $C^* = \sqrt{(a^*)^2 + (b^*)^2}$.
4. Look up $C^*_{\max}(L^*, h)$ from Pointer's table (bilinear interp).
5. In-gamut iff $C^* \le C^*_{\max}(L^*, h)$.

The maximum chroma varies dramatically by hue:
- **Yellow** ($h \approx 90°$): high — yellow ochre, lemons, traffic
  signs are achievable as surfaces.
- **Cyan** ($h \approx 200°$): high.
- **Blue** ($h \approx 270°$): low — pure deep blues are rare in surfaces
  (most "blue" pigments are violet-shifted or gray-shifted).
- **Magenta** ($h \approx 320°$): moderate.

---

## Pointer's gamut and modern display gamuts

The visible gamut (CIE 1931 horseshoe) > Pointer's gamut (surfaces) >
modern display gamuts:

```
Visible (CIE 1931)
  > Pointer (1980, real surfaces)
    > Rec.2020 (HDR / UHD displays)
      > Display P3 (Apple ecosystem)
        > sRGB (standard web)
```

A color can be in display gamut but outside Pointer (uncommon — usually
saturated cyans, magentas, or yellows that don't exist as surfaces). Or
in Pointer but outside display gamut (e.g., bright yellow surfaces that
exceed sRGB).

For digital UI work, **Pointer is irrelevant** (display gamut binds
tighter). For print, fabric, or paint design work, **Pointer is the
binding constraint**.

---

## Implementation

**Not implemented in this skill.** Reasoning:

1. Specialized use case (physical-media design only).
2. Data is a 16×16 lookup table; trivial to add but rarely needed.
3. Modern wide-gamut display constraints typically bind tighter than
   Pointer's gamut for UI work.

If a concrete use case arises:
1. Add `src/gamut/pointers-data.ts` with the 16×16 chroma maxima table.
2. Add `src/gamut/pointers-check.ts` exporting `inPointersGamut(xyz)`.
3. Bilinear interpolation in $(L^*, h)$ for non-tabulated points.

Reference for the data table: Pointer 1980 Tables 2-3, or the digital
version at `colour-science.org`.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | Not implemented. |
| **Colour** (Python) | `colour.is_within_pointer_gamut(xyz)` — full lookup. |
| **OpenColorIO** | Used internally for physical-media-aware tone mapping. |

---

## Primary sources

- **Pointer, M. R. (1980)** — "The gamut of real surface colours,"
  *Color Research & Application* 5(3), 145-155. The original paper.
- **Buck, B., Pointer, M. R., van der Veen, R. (2005)** — refined
  reanalysis.
- **CIE 015:2018 — Colorimetry, 4th edition** — references Pointer's
  gamut as the practical surface-color envelope.
- **Companion**: [`cielab-xyz-conversion.md`](../../../color-space-facts/references/techniques/cielab-xyz-conversion.md) —
  CIELAB is the working space for Pointer's gamut lookup.
- **Companion**: [`xyz-rgb-conversion-matrices.md`](../../../color-space-facts/references/techniques/xyz-rgb-conversion-matrices.md) —
  display gamut matrices for the comparison hierarchy above.
