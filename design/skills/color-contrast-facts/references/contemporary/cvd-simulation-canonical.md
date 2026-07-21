# CVD Simulation — Brettel / Viénot / Machado

**Last verified:** 2026-04-26

Color-vision deficiency (CVD) affects ~8% of men and ~0.5% of women globally. Simulating CVD to test design choices is well-served by three canonical algorithms: **Brettel-1997** for severe dichromacy, **Viénot-1999** for a simpler matrix variant, and **Machado-2009** for variable-severity anomalous trichromacy.

## The three canonical algorithms

### Brettel-1997 — Dichromatic projection
Brettel, Viénot & Mollon, *JOSA-A* 1997. Projects the color stimulus onto the dichromatic confusion plane defined by anchor stimuli (575 nm yellow, 475 nm blue). Three projections — protanopia, deuteranopia, tritanopia — produce the canonical "what does a dichromat see" simulation. Computationally heavier than Viénot; more accurate at extreme chroma.

### Viénot-1999 — Simplified matrix
Viénot, Brettel & Mollon, *Color Research & Application* 1999. Replaces Brettel's anchor-stimulus projection with a single linear transform per CVD type. **The matrix you actually find inside CSS `<feColorMatrix>` filters** in most CVD-simulation code is the Viénot variant. Faster, slightly less accurate at the extremes, fine for design-tooling use.

### Machado-2009 — Anomalous trichromacy with severity
Machado, Oliveira & Fernandes, *IEEE TVCG* 2009. Adds a **severity parameter (0–1)** to model anomalous trichromacy (protanomaly, deuteranomaly, tritanomaly) as an interpolation along confusion lines between normal vision (severity 0) and full dichromacy (severity 1). This is the canonical reference for "show me what a 50% protanomaly user sees" — most real-world CVD is anomalous, not full dichromacy.

## Implementations

| Library | Algorithm | Notes |
|---|---|---|
| **Chrome DevTools "Emulate vision deficiencies"** | SVG `<feColorMatrix>` (Viénot-derived) | Most accessible — browser DevTools, no install |
| **Culori** (`culori`) | Brettel + Machado | npm; modular |
| **ColorAide** | Brettel + Machado | Python |
| **Color Buddy** | Brettel + Machado | Tooling for design-system authors |
| **Sim Daltonism** (macOS) | Machado | Native macOS app, real-time camera filter |
| **Coblis** (web) | Multiple | Free web tool |

Chrome DevTools' simulation was last updated July 2025 to use canonical matrices; before that, several DevTools versions used inaccurate ad-hoc transforms.

## How to use

For design review:
1. Load the surface in Chrome DevTools.
2. Cmd+Shift+P → "vision deficiencies" → pick protanopia / deuteranopia / tritanopia / achromatopsia / blurred vision.
3. Verify state cues are not color-only — every red/green status pair should also use icon shape, position, or label.

For tokenized testing:
- Pipe palette colors through `culori`'s `filterDeficiencyDeuter()` etc., compare CIEDE2000 distance pre/post simulation. If a critical pair (e.g. error red vs success green) collapses to <2.0 ΔE under deuteranopia, it's CVD-unsafe.

## What CVD simulation does NOT capture

- **Severity in real users.** Real anomalous trichromacy spans the full 0–1 severity range; simulating only "full" exaggerates the impact.
- **Cone-type rarity.** Tritanopia is ~1 in 10,000; simulating it is good practice but should not drive design decisions over protan/deutan (~5% of men).
- **Cognitive disambiguation.** A skilled deuteranope often distinguishes red/green via context, learning, and cone-type bleed-through that simulations don't model.

## Recommended stance

- **Default to deuteranopia simulation** for design QA — it's the most common CVD type by a wide margin.
- **Use Machado severity 0.6** as the realistic moderate-anomalous case, not severity 1.0 (full dichromacy is rare).
- **Pair color with non-color cues** (shape, icon, text) for any state distinction — passes any CVD test.
- **Don't optimize palettes for CVD-safety alone** — equiluminant safe-for-all-CVD palettes are limited and ugly. Optimize for non-color disambiguation instead.

Sources:
- Brettel, Viénot & Mollon. "Computerized simulation of color appearance for dichromats." JOSA-A 14, no. 10 (1997): 2647-2655. DOI: [10.1364/JOSAA.14.002647](https://doi.org/10.1364/JOSAA.14.002647)
- Viénot, Brettel & Mollon. "Digital video colourmaps for checking the legibility of displays by dichromats." *Color Research & Application* 24, no. 4 (1999): 243-252.
- Machado, Oliveira & Fernandes. "A physiologically-based model for simulation of color vision deficiency." *IEEE TVCG* 15, no. 6 (2009): 1291-1298. DOI: [10.1109/TVCG.2009.113](https://doi.org/10.1109/TVCG.2009.113)
- [Chrome DevTools: Emulate vision deficiencies](https://developer.chrome.com/docs/devtools/rendering/emulate-vision-deficiencies)
- [Culori CVD filter functions](https://culorijs.org/api/#filter)
