# Material HCT — Math

**Hue + Chroma + Tone** — Material Design 3's color space, blending CIECAM16's
hue/chroma with CIELAB's tone (L*). The motivation: Material wanted a single
color triple that's **simultaneously** perceptually uniform (CIECAM16) and
preserves CIELAB-compatible tonal contrast (L*).

The result is non-orthogonal — H and C come from one model, T from another —
which makes the **inverse direction iterative** rather than closed-form.

---

## TL;DR

$$
\begin{aligned}
H &= h_{\text{CAM16}} && \in [0, 360°) \\
C &= C_{\text{CAM16}} && \approx M_{\text{CAM16}} / F_L^{1/4} \\
T &= L^*_{\text{CIELAB}} && \in [0, 100]
\end{aligned}
$$

**Forward** (XYZ → HCT): compute CAM16, take h and chroma; compute CIELAB,
take L*.

**Inverse** (HCT → XYZ): iteratively find J such that CIELAB L* of the
resulting XYZ equals the target T, holding h and C fixed in CAM16.

The full Material reference uses a gamut-aware solver that finds the closest
in-gamut chroma at the requested (H, T). This skill's implementation uses a
simpler iterative inverse; for production work with adversarial inputs use
`material-color-utilities` directly.

---

## Natural-language description

### Why HCT exists

Material Design 3 needed a color system where:

1. **The tonal contrast between two shades of a color is predictable**. Two
   colors with T=50 and T=90 should always have the same perceived contrast
   regardless of hue. This requires a CIELAB-style L* axis (luminance-based).
2. **Hue and chroma are perceptually uniform**. Equal angular steps in H
   should look like equal hue rotations; equal C should mean equal chroma.
   This requires a CIECAM16-style perceptual model.

CIELAB alone gives perceptually-uniform L* but its a/b plane has the
well-known blue-purple curvature. OKLab fixes the curvature but L is on a
$[0, 1]$ scale (not the $[0, 100]$ L* designers know).

Material chose **CAM16 H + CAM16 C + CIELAB L*** — getting the best of both
at the cost of inverse-iteration complexity.

### The +40/+50 tone-delta contrast guarantee

A core Material 3 design tool: **for any two colors at the same hue with a
tone difference of ≥40, contrast is at least 3:1**; with ≥50, it's ≥4.5:1
(WCAG AA). This guarantee comes from CIELAB L*'s direct relationship to
WCAG-style luminance contrast.

Material's tonal palettes (the "13-tone" system at $T = 0, 10, 20, ..., 100$)
exploit this: any (text=T80, BG=T20) pair clears WCAG AA for normal text.

### Why the inverse is iterative

If HCT were $(h_{\text{CAM16}}, C_{\text{CAM16}}, J_{\text{CAM16}})$ — all
from one model — the inverse would be closed-form. But $T = L^*$ comes from
a different model. So given a target HCT, finding the XYZ that produces it
requires:

- Hold $h, C$ fixed (CAM16).
- Search for the CAM16 $J$ that, when inverted to XYZ and then forward to
  CIELAB, gives the requested $T$.

Material's solver uses bisection + gamut-aware steps to find the best
in-gamut representative. This skill uses a simpler proportional iteration
(8 steps typically converge).

---

## Formulas

### Forward: XYZ-D65 → HCT

```
(J, M, h) ← CIECAM16.fromXYZ(xyz)      // CAM16 JMh form
(L*, a*, b*) ← CIELAB.fromXYZ(xyz)     // CIELAB
return (h, M, L*)                       // (H, C, T)
```

Note: the Material reference uses $C$ (chroma), but in JMh-form CAM16
outputs $M$ (colorfulness). They're related by $C = M / F_L^{1/4}$. This
skill's `src/spaces/hct.ts` uses $M$ directly (matching Material's
implementation), which means the "C" component is technically colorfulness,
not chroma — but the distinction matters only when comparing across
non-default viewing conditions.

### Inverse: HCT → XYZ-D65 (iterative)

```
function toXYZ(H, C, T):
  if C == 0 or T == 0 or T == 100:
    return CIELAB.toXYZ(L*=T, a*=0, b*=0)

  Y_target ← f^{-1}((T + 16) / 116)    // CIELAB inverse for target Y
  J ← T                                  // initial estimate
  for i in 0..7:
    xyz_candidate ← CIECAM16.toXYZ(J, C, H)
    Y_actual ← xyz_candidate.Y
    if |Y_actual - Y_target| < 1e-6: break
    J *= Y_target / Y_actual             // proportional adjustment
    J = clamp(J, 1e-6, 100)
  return xyz_candidate
```

The iteration converges because CAM16 J and CIELAB L* are monotonically
related. For typical inputs 4–8 iterations suffice.

**Gamut awareness** (in Material's full solver, not in this skill's port):
if the requested $C$ is out-of-gamut at the target $T$, Material's solver
reduces $C$ to the largest in-gamut value. This skill's `mapToSRGB` (Tier 3
gamut mapping) provides similar functionality.

### CAM16 hue / chroma range

- $H \in [0, 360°)$ — same as CSS hue convention.
- $C$ (CAM16 colorfulness $M$): typically $[0, 120]$ in default viewing
  conditions. Maximum varies by hue.
- $T = L^*$: $[0, 100]$, same as CIELAB.

---

## Implementation

Canonical TypeScript: [`src/spaces/hct.ts`](../../../../color-science-project-files/src/spaces/hct.ts).

```ts
export function fromXYZ(c: XYZ_D65): HCT {
  const cam: CIECAM16_JMh = cam16.fromXYZ(c);
  const lab: CIELAB_D65 = cielab.fromXYZ(c);
  return hct(cam[2], cam[1], lab[0]);  // [h, M, L*]
}

export function toXYZ(c: HCT): XYZ_D65 {
  const [H, C, T] = c;
  if (C === 0 || T === 0 || T === 100) {
    return cielab.toXYZ(cielab_D65(T, 0, 0));
  }
  const Y_target = yFromLstar(T);
  let J = T;
  let xyzCandidate;
  for (let i = 0; i < 8; i++) {
    xyzCandidate = cam16.toXYZ(ciecam16_JMh(J, C, wrapHueDeg(H)));
    if (Math.abs(xyzCandidate[1] - Y_target) < 1e-6) break;
    J *= Y_target / xyzCandidate[1];
    J = Math.max(1e-6, Math.min(100, J));
  }
  return xyzCandidate!;
}
```

Test vectors:
- Black (XYZ=0) → HCT (0, 0, 0)
- D65 white → HCT (h_undef, ~0, 100) — small residual chroma from partial
  CAM16 adaptation, tolerated within ±0.5.

---

## Material's tonal palette convention

Material 3 generates 13 tonal stops per "key color":

| Tone | Use |
|---|---|
| **0** | Pure black |
| **10** | High-emphasis on dark |
| **20** | Body text on dark / dark surface |
| **30** | High-emphasis on dark variant |
| **40** | Medium-emphasis |
| **50** | Equal-tone mid |
| **60** | Medium-emphasis (light) |
| **70** | Mid-light surface |
| **80** | Body text on light |
| **90** | Background on light variant |
| **95** | App background light |
| **99** | Near-white |
| **100** | Pure white |

These are spaced for the +40/+50 tone-delta contrast guarantee. Generating
a palette from a key color: forward the key color to HCT (extract H and C),
then emit `HCT(H, C, T)` for each T in the tonal stops.

---

## Edge cases

- **Achromatic shortcut** (C=0, T=0, or T=100): bypass the iteration and use
  the CIELAB direct conversion. Avoids unnecessary CAM16 work.
- **Out-of-gamut HCT**: the iterative inverse may converge to an XYZ that
  doesn't fit in sRGB. Apply gamut mapping (e.g., `mapToSRGB`) post-hoc.
- **CAM16 viewing condition mismatch**: HCT's forward uses
  `DEFAULT_VC` (Material's). Using non-default VCs without updating both
  the forward and inverse breaks round-trip identity.
- **Material's gamut-aware solver vs. this skill's simple iteration**: the
  simple iteration works for typical inputs. For adversarial inputs (very
  high C requested at T near 0 or 100), Material's solver is more robust.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/spaces/hct.ts` — simple iterative inverse; sufficient for most cases. |
| **Material color-utilities** | <https://github.com/material-foundation/material-color-utilities> — full gamut-aware solver, multi-language (TypeScript, Dart, Java, Kotlin, Python, Swift). |
| **Color.js** | Has Material HCT support via the `cam16` mode plus L* extraction. |
| **Culori** | No native HCT support as of 2026; can compose via `mode_cam16_jmh` + `mode_lab`. |

---

## Primary sources

- **Material Design 3 — Color system** — <https://m3.material.io/styles/color/system> —
  the design framework that defines HCT and its tonal palettes.
- **Material color-utilities source** — <https://github.com/material-foundation/material-color-utilities> —
  reference implementation across 6 languages.
- **CIE 248:2022** — CIECAM16 normative reference (for the H, C components).
- **CIE 015:2018** — CIELAB normative reference (for the T component).
- **Companion**: [`ciecam16-forward-inverse.md`](./ciecam16-forward-inverse.md) —
  the CAM16 part of HCT.
- **Companion**: [`cielab-xyz-conversion.md`](./cielab-xyz-conversion.md) —
  the L* part of HCT.
- **Companion**: [`material-hct-color-space.md`](../contemporary/material-hct-color-space.md) —
  existing overview / positioning doc (vs OKLCh, vs CIELAB).
