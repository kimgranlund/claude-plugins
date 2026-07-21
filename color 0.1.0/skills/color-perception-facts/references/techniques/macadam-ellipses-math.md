# MacAdam Ellipses — Math

The empirical **Just Noticeable Difference (JND) regions** in the CIE 1931
chromaticity diagram. MacAdam (1942) measured how much chromaticity an
observer could change before noticing the difference, producing a family
of ellipses across the diagram. These ellipses are the **non-uniformity
that motivated CIELAB, CIELUV, OKLab, and CAM16-UCS** — their existence
proves that CIE 1931 chromaticity is not perceptually uniform.

---

## TL;DR

- MacAdam plotted 25 ellipses across the CIE 1931 (x, y) plane.
- Each ellipse marks the set of chromaticities that look indistinguishable
  from its center to a standard observer.
- Ellipse **sizes vary by 10×** across the diagram — proof of CIE 1931's
  non-uniformity.
- Modern uniform spaces (OKLab, CAM16-UCS) are designed so MacAdam ellipses
  become approximately **equal-sized circles** in the new space.

---

## Natural-language description

### What MacAdam measured

MacAdam's observers stared at a half-disc display where one half had a
fixed chromaticity (the "test" color) and the other half had an adjustable
chromaticity. The adjustable side was perturbed in random directions
through the (x, y) plane; observers reported when they could detect a
difference.

For each of 25 test chromaticities across the visible gamut, MacAdam fit
an ellipse to the JND boundary. The result: ellipses with vastly different
sizes and orientations.

- In the **green region**: ellipses are large (perceptual sensitivity
  low), so a small (x, y) step is invisible.
- In the **blue region**: ellipses are small (sensitivity high), so the
  same (x, y) step is dramatically visible.

This is **the non-uniformity problem**. CIE 1931 chromaticity is a
mathematical projection of cone responses, not a perceptual space.

### The consequences for modern colorimetry

CIELAB (1976), CIELUV (1976), OKLab (2020), and CAM16-UCS (2017) are all
attempts to find a color space where MacAdam ellipses transform to
approximately equal-sized circles. The cube-root nonlinearity of CIELAB,
OKLab's matrix-tuned M2, and CAM16-UCS's hyperbolic remapping all serve
this goal.

In a perfectly uniform space, every MacAdam JND threshold would be the
same scalar distance. No real space achieves this exactly, but OKLab gets
within ~20% — and that's why it's the modern default.

---

## Mathematical structure

Each MacAdam ellipse is parameterized by:
- **Center** $(x_0, y_0)$ in CIE 1931 chromaticity.
- **Semi-axes** $a, b$.
- **Tilt angle** $\theta$ (counterclockwise from $x$-axis).

A point $(x, y)$ is inside the ellipse if:

$$
\frac{((x - x_0) \cos\theta + (y - y_0) \sin\theta)^2}{a^2}
+ \frac{((y - y_0) \cos\theta - (x - x_0) \sin\theta)^2}{b^2}
\leq 1
$$

MacAdam's 25 published centers and ellipse parameters are tabulated in
his original 1942 paper and in countless later texts. The ellipse sizes
range from ~0.001 (in blue regions) to ~0.020 (in green) — a 20× spread.

### The "10-step" convention

MacAdam reported ellipse parameters at **10× JND** for clarity. Dividing
by 10 gives single-JND thresholds. A typical 10-step semi-axis is 0.01 in
(x, y) units; 1-step is 0.001.

---

## Implementation

This skill does **not** include a MacAdam ellipse data module. Use cases
are research-survey / educational; production color difference work uses
ΔE2000 or ΔE_ok which calibrate against the same empirical data.

If you need MacAdam-aware computation:

1. The 25 ellipse parameters are widely tabulated. See **Wyszecki &
   Stiles, "Color Science"** Table I(3.5.2) for the canonical values.
2. To check whether two chromaticities are within $n$ JNDs, compute the
   Mahalanobis-like distance using the local ellipse's parameters.
3. For practical work, use $\Delta E_{2000}$ or $\Delta E_{ok}$ —
   they're calibrated against MacAdam-style threshold data and easier to
   compute than per-region ellipse lookups.

---

## Why this matters for design tokens

MacAdam ellipses prove that **equal-step chromaticity ramps do NOT look
equal-stepped**. If you generate a ramp by linear interpolation in CIE
1931 (x, y), some steps will look 5× more different than others —
because you're crossing varying numbers of MacAdam ellipses per step.

The fix: interpolate in OKLab. Equal Euclidean steps in OKLab approximate
equal perceptual steps because OKLab's coordinate system was designed to
make MacAdam ellipses uniform.

This is the foundation of why this skill defaults to OKLab for palette
generation, gradient interpolation, and color difference. The architecture
choice traces directly back to MacAdam's 1942 experiment.

---

## Modern equivalents

| Space | MacAdam-ellipse uniformity |
|---|---|
| **CIE 1931 (x, y)** | Highly non-uniform (the problem MacAdam exposed) |
| **CIELAB** | ~3× variation in equivalent ellipse size |
| **CIELUV** | Similar to CIELAB |
| **OKLab** | ~1.5× variation — excellent uniformity |
| **CAM16-UCS** | ~1.2× variation — best uniformity in widespread use |

For research-grade perceptual difference work, CAM16-UCS or empirical
ΔE2000 win. For UI / design tokens, OKLab is the practical default.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | No direct MacAdam ellipse data; use ΔE_ok / ΔE2000 instead. |
| **Wyszecki & Stiles** | Canonical reference text with full tables. |
| **Colour** (Python) | `colour.MACADAM_1942_CHROMATICITY_DIAGRAM_DATA` — full ellipse parameters. |
| **MacAdam visualizations** | <https://en.wikipedia.org/wiki/MacAdam_ellipse> has the canonical diagram. |

---

## Primary sources

- **MacAdam, D. L. (1942)** — "Visual Sensitivities to Color Differences
  in Daylight," *Journal of the Optical Society of America* 32(5),
  247-274. The foundational paper.
- **Wyszecki, G. & Stiles, W. S. (1982)** — *Color Science: Concepts and
  Methods, Quantitative Data and Formulae*, 2nd ed. Canonical reference
  with full tables.
- **Brown, W. R. J. (1957)** — extended MacAdam's measurements with
  modern instrumentation.
- **Companion** (in `color-space-facts`): [`oklab-xyz-math.md`](../../../color-space-facts/references/techniques/oklab-xyz-math.md) —
  OKLab's uniformity is calibrated against MacAdam-style data.
- **Companion** (in `color-space-facts`): [`delta-e-formulas.md`](../../../color-space-facts/references/techniques/delta-e-formulas.md) —
  ΔE metrics are the modern practical alternative.
