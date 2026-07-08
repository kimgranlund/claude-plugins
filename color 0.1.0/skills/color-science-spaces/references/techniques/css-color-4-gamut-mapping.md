# CSS Color 4 Gamut Mapping — Math

The normative algorithm for fitting an out-of-gamut color into a target RGB
gamut **without shifting hue**. Required for any modern color pipeline that
generates colors outside sRGB (P3, Rec.2020, OKLCh) and needs to render them
on narrower-gamut displays.

---

## TL;DR

- **Naive clipping shifts hue.** A vivid red at `oklch(0.6 0.5 29deg)` clipped
  to sRGB lands at sRGB red but with visibly shifted hue compared to its
  perceptual neighbors.
- **CSS Color 4 algorithm**: binary-search OKLCh chroma reduction with hue +
  lightness preserved. Accept the result when ΔE_ok between the chroma-reduced
  color and its naive clip falls below the JND threshold (0.02).
- **Result**: hue-preserving in-gamut color. Chroma reduced as little as the
  gamut allows.

---

## Natural-language description

### Why naive clipping is wrong

Suppose your generated color is `linearRGB(1.1, 0.2, 0.1)`. Clipping channel-by-
channel produces `linearRGB(1, 0.2, 0.1)`. The visual result:

- **Lightness** changed slightly (you lost some red intensity).
- **Hue shifted**: the original color had a specific R:G:B ratio; the clip
  altered that ratio non-uniformly.
- **Chroma reduced**: somewhat, but unpredictably.

For a single color it's barely noticeable. For a gradient or a generated
palette, naive clipping produces **visible hue waver** across colors — the
hue of one swatch differs from its perceptual neighbor by an unintended angle.

### Why hue-preserving chroma reduction works

In OKLCh, hue is an angular coordinate independent of $L$ and $C$. Reducing
$C$ while keeping $h$ and $L$ fixed walks the color **directly toward the
achromatic axis** without rotating around it.

Once $C$ is small enough that the color fits in the target gamut, we stop.
The result has:
- Identical hue.
- Identical lightness (within tolerance).
- Reduced chroma (the minimum reduction that fits the gamut).

### The JND optimization

A pure binary search on $C$ converges in $\log_2(C_0 / \epsilon)$ iterations
(~14 for typical tolerances). But often the **naive clip itself** is
perceptually indistinguishable from the target color — within JND of $0.02$
in $\Delta E_{ok}$.

When this is true, we can return the naive clip immediately. The algorithm
includes this check both at entry (fast path for near-edge colors) and
during the search (early termination).

---

## Formulas

### Inputs

- `origin` — OKLCh color, possibly out-of-gamut.
- `inGamut(c)` — predicate that returns whether OKLCh $c$ is in the target gamut.
- `naiveClip(c)` — naive per-channel clip in the target's linear-RGB space,
  converted back to OKLCh.

### Constants

$$
JND = 0.02, \quad \epsilon = 10^{-4}
$$

### Algorithm

```
function mapToGamut(origin):
  if inGamut(origin): return origin
  if origin.L >= 1: return oklch(1, 0, origin.h)        // white
  if origin.L <= 0: return oklch(0, 0, origin.h)        // black

  // Fast path: naive clip is perceptually identical?
  clipped = naiveClip(origin)
  if ΔE_ok(origin, clipped) < JND: return clipped

  // Binary search on chroma
  min ← 0
  max ← origin.C
  minInGamut ← true
  while max − min > ε:
    chroma ← (min + max) / 2
    current ← oklch(origin.L, chroma, origin.h)
    if minInGamut and inGamut(current):
      min ← chroma
    else:
      clipped ← naiveClip(current)
      E ← ΔE_ok(current, clipped)
      if E < JND:
        if JND − E < ε: return clipped       // converged within JND band
        minInGamut ← false
        min ← chroma
      else:
        max ← chroma

  return oklch(origin.L, min, origin.h)
```

The two "phases" of the search:

1. **Phase 1 (`minInGamut: true`)** — find the largest $C$ for which the
   color is strictly in gamut. This is monotonic and binary search converges
   directly.

2. **Phase 2 (`minInGamut: false`)** — even after exiting strict in-gamut,
   tolerate up to JND difference against the naive clip. This trades a tiny
   perceptual error for a more chromatic result.

---

## Implementation

Canonical TypeScript: [`src/gamut/mapping.ts`](../../../../color-science-project-files/src/gamut/mapping.ts).

Exports:
- `mapToSRGB(oklch): LinearSRGB` — convenience for the sRGB case
- `mapToP3(oklch): LinearP3` — Display P3 variant
- `mapToRec2020(oklch): LinearRec2020` — Rec.2020 variant
- `mapToGamutOklch(origin, toRGBMatrix, inGamutFn): OKLCH` — generic form
- `inGamutSRGB(oklch): boolean`, `inGamutP3(oklch)`, `inGamutRec2020(oklch)` — predicates
- `clipNaive(rgb): [number, number, number]` — for comparison / fallback

```ts
export function mapToGamutOklch(
  origin: OKLCH,
  toRGB: Matrix3x3,
  inGamutFn: (c: OKLCH) => boolean
): OKLCH {
  const [L, C, hDeg] = origin;
  if (inGamutFn(origin)) return origin;
  if (L >= 1) return makeOklch(1, 0, hDeg);
  if (L <= 0) return makeOklch(0, 0, hDeg);

  const naiveClipColor = clipFromOklch(origin, toRGB);
  if (deltaEOK(toOKLab(origin), toOKLab(naiveClipColor)) < JND_OK) {
    return naiveClipColor;
  }

  // ... binary search ...
}
```

---

## Comparison: clipping vs. mapping

| | Naive clip | CSS Color 4 mapping |
|---|---|---|
| **Hue preservation** | No (shifts) | Yes (preserved) |
| **Lightness preservation** | Partial | Yes |
| **Chroma reduction** | Unpredictable | Minimum needed |
| **Cost** | O(1) | ~14 iterations |
| **Use when** | Already in gamut, just trim float drift | Source is out-of-gamut |

**Rule of thumb**: use `clipNaive` only for the **last-mile defensive trim**
after a full conversion pipeline. Use `mapToSRGB` (or P3/Rec.2020) whenever
the input might be genuinely out-of-gamut.

---

## Edge cases

- **L outside [0, 1]**: short-circuits to white or black. No mapping search.
- **Already in gamut**: returns the origin unchanged. No allocation.
- **Tiny chroma**: any color with $C < \epsilon$ is essentially achromatic;
  the algorithm exits quickly.
- **Floating-point drift at the boundary**: the final `clipNaive` call in each
  `mapTo*` wrapper trims residual float noise. Without it, the result might
  be `(0.99998, 0.5, 1.00001)` — close but not actually in gamut.
- **Different JND in different gamuts**: the JND threshold is fixed at 0.02
  per W3C spec. For Rec.2020 (much wider gamut) you may want a tighter
  threshold; W3C doesn't specify, so we keep 0.02 across all gamuts.

---

## Production-library map

| Library | Notes |
|---|---|
| **This skill** | `src/gamut/mapping.ts` — branded-typed, gamut-specific wrappers, JND-based early termination. |
| **Culori** | `toGamut(color, mode)` — implements CSS Color 4 with the same algorithm. |
| **Color.js** | `Color.toGamut(method)` with selectable algorithm. Reference implementation by the spec editors. |
| **CSS** (browsers) | `oklch(0.6 0.5 29deg)` in CSS triggers this algorithm in the rendering pipeline. |

---

## Primary sources

- **W3C CSS Color Module Level 4** — <https://www.w3.org/TR/css-color-4/#binsearch> —
  normative algorithm. Spec editors are Lea Verou and Chris Lilley.
- **Björn Ottosson, "Gamut clipping" (2021)** —
  <https://bottosson.github.io/posts/gamutclipping/> — analytic alternatives
  (cusp-based) and discussion of why hue preservation matters.
- **Companion math**: [`oklch-gamut-peak-math.md`](./oklch-gamut-peak-math.md)
  for peak $L(C, h)$ and peak $C(L, h)$ derivations.
- **Companion algorithm**: [`ottosson-cusp-algorithm.md`](./ottosson-cusp-algorithm.md)
  for the closed-form cusp solver that enables analytic chroma-reduction
  alternatives to binary search.
