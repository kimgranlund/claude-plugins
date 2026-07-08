# Color Math System — Architecture

This document fixes the architectural rules for the math-reference corpus (split
2026-07-06 across the four `color-science-*` packs' `references/techniques/`) and
`src/` (kept here, in `color-science-project-files`). The math roadmap, every
existing math reference, and every future addition must satisfy these rules. When in
doubt, **the canonical example is `src/spaces/oklab.ts` paired with
`../color-science-spaces/references/techniques/oklab-xyz-math.md`**.

---

## Goals

1. **Bidirectional** — every transform A → B has an inverse B → A.
2. **Composable** — any space converts to any other via the source-of-truth hub.
3. **Computational** — math goes in TypeScript; description goes in markdown.
4. **Type-safe** — branded types prevent mixing color spaces at the type level.
5. **Self-verifying** — every module exports test vectors for round-trip checks.

---

## Decision 1: Source of truth is CIE XYZ at D65

**The hub.** Every color space converts to and from `XYZ_D65`. Period.

```
                    ┌───────────────┐
                    │   XYZ_D65     │
                    │  (source of   │
                    │    truth)     │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
  ┌─────▼─────┐       ┌─────▼─────┐       ┌─────▼─────┐
  │  sRGB     │       │  OKLab    │       │  CIELAB   │
  │ (linear)  │       │           │       │           │
  └─────┬─────┘       └─────┬─────┘       └───────────┘
        │                   │
  ┌─────▼─────┐       ┌─────▼─────┐
  │  sRGB     │       │  OKLCH    │
  │ (encoded) │       │  (polar)  │
  └───────────┘       └───────────┘
```

**Why XYZ-D65, not OKLab or linear sRGB:**

| Candidate | Rejected because |
|---|---|
| Linear sRGB | Gamut-limited; baking the sRGB primaries into the hub means every wide-gamut conversion goes through an sRGB-clamped path. Loses information. |
| OKLab | Defined as a transform *from* XYZ. Making OKLab the hub means every non-OKLab conversion costs an extra transform leg. |
| Linear Display P3 | Wider gamut than sRGB, but still gamut-bound. Same problem as sRGB. |
| Spectral SPD | Most physically correct, but heavyweight (36+ floats) and overkill for 99% of work. Reserve as an optional richer representation. |
| **XYZ-D65** | **Chosen.** CIE-defined absolute reference. D65 matches modern display white (sRGB, P3, Rec.709/2020). Every space derives from/converts to it cleanly. Chromatic adaptation lives at this layer (Bradford acts on XYZ). |

**White point: D65.** All internal math operates at D65. When working with CIELAB or
ICC profile connection spaces that traditionally use D50, the chromatic adaptation
happens explicitly via `src/adaptation/bradford.ts` — never implicitly.

---

## Decision 2: Optional richer source-of-truth is Spectral SPD

For pigment mixing, metamer construction, and illuminant-correct work, XYZ collapses
too much information. The richer source-of-truth is a Spectral Power Distribution:

```ts
// 36 samples, 380nm to 730nm at 10nm intervals.
export type SPD = ReadonlyArray<number> & { readonly [__brand]: 'SPD_380_730_10nm' };
```

**Bridge from spectral to the hub:** `src/spectral/spd.ts` exports `spdToXYZ_D65(spd: SPD, illuminant: SPD): XYZ_D65` — convolves the SPD against an illuminant and the CIE 1931 (2°) or 1964 (10°) color matching functions.

**Don't bridge XYZ → SPD silently** — that's the spectral upsampling problem (Meng et al., Smits), which is lossy and non-unique. Build a separate explicit function in `src/spectral/upsampling.ts`.

---

## Decision 3: Language is TypeScript

**Why TS:**
- Branded types catch space-mixing at compile time (e.g., passing OKLab to a function expecting CIELAB fails to compile).
- Compiles to JS for browser/Node consumption without changes.
- Matches the broader color-library ecosystem (Culori, Color.js, @texel/color are all JS/TS).
- Type system pays for itself the first time a `[L, a, b]` for OKLab gets passed to a function expecting `[L*, a*, b*]` for CIELAB.

**Project structure:**

```
src/
├── types.ts                  # Branded types + Matrix3x3 + TestVector + helpers
├── spaces/                   # One file per color space — must export toXYZ + fromXYZ
│   ├── srgb.ts               # Linear sRGB ↔ XYZ_D65
│   ├── p3.ts                 # Linear Display P3 ↔ XYZ_D65
│   ├── rec2020.ts            # Linear Rec.2020 ↔ XYZ_D65
│   ├── oklab.ts              # OKLab ↔ XYZ_D65
│   ├── oklch.ts              # OKLCH ↔ OKLab (polar coordinates)
│   ├── cielab.ts             # CIELAB_D65 ↔ XYZ_D65
│   ├── cielch.ts             # CIELCH_D65 ↔ CIELAB_D65 (polar)
│   ├── hsl.ts                # HSL ↔ Linear sRGB
│   ├── hsv.ts                # HSV ↔ Linear sRGB
│   ├── ciecam16.ts           # CIECAM16 JMh ↔ XYZ_D65
│   ├── hct.ts                # Material HCT ↔ XYZ_D65
│   ├── jzazbz.ts             # Jzazbz ↔ XYZ_D65 (HDR)
│   └── ictcp.ts              # ICtCp ↔ XYZ_D65 (HDR)
├── transfer/                 # 1D gamma functions — must export encode + decode
│   ├── srgb.ts               # sRGB segmented transfer (= P3 transfer)
│   ├── rec709.ts             # Rec.709 OETF
│   ├── rec2020.ts            # Rec.2020 OETF
│   ├── pq.ts                 # BT.2100 PQ
│   └── hlg.ts                # BT.2100 HLG
├── adaptation/               # Chromatic adaptation matrices
│   ├── bradford.ts           # Bradford CAT
│   ├── cat02.ts              # CIECAM02 default
│   ├── cat16.ts              # CIECAM16 default
│   └── vonkries.ts
├── gamut/                    # Gamut tests, mapping, peak chroma/lightness
│   ├── oklch-peak.ts         # Peak L(C,h) and C(L,h) — see ../color-science-spaces/references/techniques/oklch-gamut-peak-math.md
│   ├── cusp.ts               # Ottosson cusp algorithm
│   └── mapping.ts            # CSS Color 4 gamut mapping
├── metrics/                  # Distance and contrast
│   ├── deltaE.ts             # ΔE76, ΔE94, ΔE2000, ΔE_ok, HyAB
│   ├── wcag.ts               # WCAG 2.x contrast ratio
│   └── apca.ts               # APCA L^c
├── interpolation/            # Gradients and palette ramps
│   ├── linear.ts             # Linear interp in any space
│   ├── hue-paths.ts          # CSS Color 4 hue path logic
│   ├── spline.ts             # Catmull-Rom, Bezier in OKLab
│   └── cubehelix.ts          # D. A. Green
├── cvd/                      # Color vision deficiency simulation
│   ├── brettel-1997.ts       # LMS confusion lines
│   ├── vienot-1999.ts        # Matrix-based
│   └── machado-2009.ts       # Severity-parameterized
├── pigment/                  # Spectral pigment mixing
│   ├── kubelka-munk.ts       # K-M single and two-constant
│   └── saunderson.ts         # Surface reflection correction
└── spectral/                 # Optional richer SoT
    ├── cmf.ts                # CIE 1931 (2°), 1964 (10°) color matching functions
    ├── illuminants.ts        # D65, D50, A, F2, ... spectra
    ├── spd.ts                # SPD ↔ XYZ_D65 bridge
    └── upsampling.ts         # Meng et al., Smits — XYZ → SPD (explicit, lossy)
```

---

## Decision 4: Branded types prevent space-mixing at compile time

Every color is a `[number, number, number]` tuple at runtime, but the compiler sees
distinct types:

```ts
declare const __brand: unique symbol;

export type XYZ_D65 = readonly [number, number, number] & { readonly [__brand]: 'XYZ_D65' };
export type OKLab   = readonly [number, number, number] & { readonly [__brand]: 'OKLab' };
export type OKLCH   = readonly [number, number, number] & { readonly [__brand]: 'OKLCH' };
// ... one per space
```

**Result.** A function `fromXYZ(xyz: XYZ_D65): OKLab` rejects accidentally passing
OKLab to it. Zero runtime cost — the brand is erased.

**Hue units:** OKLCH and CIELCH store hue in **degrees** (matches CSS convention).
Internally, modules convert to radians where convenient — at the polar-cartesian
boundary.

---

## Decision 5: Bidirectionality contract

Every `src/spaces/X.ts` module **must** export:

```ts
export function toXYZ(value: X): XYZ_D65;
export function fromXYZ(xyz: XYZ_D65): X;
```

Spaces with both linear and encoded forms (sRGB, P3, Rec.2020) **also** export
transfer functions via `src/transfer/X.ts`:

```ts
export function encode(linear: Linear_X): Encoded_X;
export function decode(encoded: Encoded_X): Linear_X;
```

**Round-trip identity** must hold within tolerance:

```ts
const c = oklab(0.5, 0.1, -0.05);
const c2 = oklab_module.fromXYZ(oklab_module.toXYZ(c));
// |c - c2| ≤ 1e-6 for linear transforms, 1e-4 for nonlinear (cubic) transforms
```

**This is mechanically checkable** via the test vectors below.

---

## Decision 6: Composition is always `B.fromXYZ(A.toXYZ(value))`

Conversion between any two spaces goes through XYZ. No direct A → B shortcuts unless
they preserve exact equality with the through-XYZ path (and even then, prefer the
explicit two-step form for auditability).

A small registry helper enables generic conversion:

```ts
// src/convert.ts
import * as srgb from './spaces/srgb.js';
import * as oklab from './spaces/oklab.js';
// ... import all space modules

type SpaceModule<T> = {
  toXYZ: (value: T) => XYZ_D65;
  fromXYZ: (xyz: XYZ_D65) => T;
};

export function convert<A, B>(
  value: A,
  from: SpaceModule<A>,
  to: SpaceModule<B>
): B {
  return to.fromXYZ(from.toXYZ(value));
}

// Usage:
const c_oklab = convert(c_srgb, srgb, oklab);
```

---

## Decision 7: Test vectors are required

Every module exports a `testVectors` array of known input/output pairs from primary
sources:

```ts
export const testVectors: ReadonlyArray<TestVector<XYZ_D65, OKLab>> = [
  {
    input: xyz(0.950, 1.000, 1.089),  // D65 white
    output: oklab_(1.000, 0.000, 0.000),
    tolerance: 1e-4,
    note: 'D65 white → OKLab (1, 0, 0)',
  },
  {
    input: xyz(1.000, 0.000, 0.000),  // pure X
    output: oklab_(0.4499, 1.2354, -0.0190),
    tolerance: 1e-4,
    note: 'Ottosson 2020 Table 1',
  },
  // ... more
];
```

**Provenance.** Every test vector cites a primary source — Ottosson's paper, the W3C
CSS Color 4 conformance suite, Bruce Lindbloom's calculator, etc.

A separate test runner (`src/test/roundtrip.ts`) iterates every space module and
verifies:
1. `fromXYZ(toXYZ(c)) ≈ c` for each test vector.
2. The output matches the published expected value within tolerance.

---

## Decision 8: Where prose and code meet

Each markdown reference file — now distributed across the four `color-science-*`
packs' `references/techniques/` (accessibility owns the apca/luminance/cvd rows; the
rest sit in spaces, perception, or materials per the pack's charter) — follows this
shape:

```markdown
# [Space or algorithm name] — Math

## TL;DR

[1-paragraph result, with the key formula or misconception correction.]

## Natural language description

[What the space is, what problem it solves, when to use it, edge cases.]

## Formulas

[LaTeX math. Display math in `$$...$$`, inline in `$...$`. All matrices written out.]

## Implementation

Canonical TypeScript: `../../../color-science-project-files/src/spaces/X.ts` (or
`.../src/gamut/X.ts`, `.../src/transfer/X.ts`, etc.) — the path back from a pack's
`references/techniques/` file to this repo's `src/`.

[Inline the critical functions as fenced TS code blocks for in-context reading.
For full implementation, link to the src file.]

## Test vectors

[A few example input/output pairs with citations.]

## Edge cases

[Numerical precision, hue wrapping, sign-preserving cube roots, out-of-gamut
handling, etc.]

## Production-library map

[Which mainstream library (Culori, @texel/color, Color.js) provides this. So users
who don't want to copy this implementation know where to grab a battle-tested one.]

## Primary sources

[The paper, the spec, the standards body.]
```

**The markdown is the explanation; the TypeScript is the implementation.** They are
co-versioned: when the TS changes, the markdown (now living in a sibling pack) is
updated in the same commit; when the math description is refined, the TS code blocks
are re-quoted from the canonical source. Same git repo, two folders — co-versioning
stays enforceable.

---

## Decision 9: No automatic gamut clipping inside conversions

Space conversion is pure math. A `fromXYZ(xyz)` that produces out-of-gamut output
(e.g., OKLab → linear sRGB with linear-RGB components > 1) returns those numbers
**as-is**. The caller decides what to do.

Gamut handling is explicit — `src/gamut/mapping.ts` and `src/gamut/oklch-peak.ts`
are separate concerns from space conversion.

**This is non-negotiable.** A converter that silently clips destroys information and
makes round-trip identity fail.

---

## Decision 10: Hue at the boundary

OKLCH and CIELCH store hue in **degrees** in their public API to match CSS
convention (`oklch(50% 0.2 145)`). Internally, modules use radians where convenient
(typically for `Math.cos` / `Math.sin` / `Math.atan2`).

The polar-to-cartesian boundary is the only place degree↔radian conversion happens:

```ts
// src/spaces/oklch.ts
export function toOKLab(oklch: OKLCH): OKLab {
  const [L, C, hDeg] = oklch;
  const hRad = hDeg * Math.PI / 180;
  return [L, C * Math.cos(hRad), C * Math.sin(hRad)] as unknown as OKLab;
}

export function fromOKLab(oklab: OKLab): OKLCH {
  const [L, a, b] = oklab;
  const C = Math.sqrt(a * a + b * b);
  let hDeg = Math.atan2(b, a) * 180 / Math.PI;
  if (hDeg < 0) hDeg += 360;
  return [L, C, hDeg] as unknown as OKLCH;
}
```

Hue wrapping (negative degrees, > 360 degrees) is normalized to `[0, 360)` at the
boundary.

---

## Summary: the contract for every math reference

A new math reference file is **complete** when all of the following exist:

- [ ] `<owning-pack>/references/techniques/<name>.md` — natural-language description
  with LaTeX formulas (accessibility owns apca/luminance/cvd; otherwise spaces,
  perception, or materials per the pack's charter)
- [ ] `src/<category>/<name>.ts` — TypeScript implementation (this repo)
- [ ] Forward and inverse functions exported with branded types
- [ ] `testVectors` array exported with primary-source citations
- [ ] Round-trip identity verified within stated tolerance
- [ ] Markdown file's "Implementation" section links to the TS file
  (`../../../color-science-project-files/src/...`)
- [ ] Markdown file inlines critical functions as fenced TS blocks
- [ ] Owning pack's `references/INDEX.md` table includes the new technique
- [ ] `CHANGELOG.md` entry: this repo's for the library (TS) change, the owning
  pack's `CHANGELOG.md` for the reference (markdown) change
- [ ] `MATH-ROADMAP.md` (this repo, root) status flag updated (🔲 → ✅)

---

## What this enables

Once the foundation is in place, any agent can:

1. Convert any color from space A to space B in one line: `convert(c, A, B)`.
2. Verify that a third-party color library matches our implementation by running
   our test vectors against it.
3. Reason about a chain of transforms knowing every step has an inverse.
4. Build new color algorithms (palette generation, gradient interpolation, gamut
   mapping) on top of the typed primitives without re-implementing conversion math.

The skill stops being a collection of disparate references and becomes a coherent,
testable, composable color math system.
