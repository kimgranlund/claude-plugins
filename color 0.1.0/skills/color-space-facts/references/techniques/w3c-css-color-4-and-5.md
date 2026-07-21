# W3C CSS Color 4, 5, and 6

**Specs:**

- CSS Color 4 — [w3.org/TR/css-color-4](https://www.w3.org/TR/css-color-4/) (CR Draft, last republished 2026-02-27)
- CSS Color 5 — [w3.org/TR/css-color-5](https://www.w3.org/TR/css-color-5/) (Working Draft)
- CSS Color 6 — [drafts.csswg.org/css-color-6](https://drafts.csswg.org/css-color-6/) (Editor's Draft)

## What It Is

The canonical standards for **modern color in CSS**. If a task touches browser color syntax, interpolation, wide gamut, or CSS-native color computation, these specs are more authoritative than blog posts or library docs.

For the current Apr 2026 baseline-interop snapshot of all the features below, see [`css-color-2026-snapshot.md`](./css-color-2026-snapshot.md).

## CSS Color 4 — Key Additions

- **`lab()` / `lch()`** and **`oklab()` / `oklch()`** in CSS
- **`color()`** for predefined spaces like `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`, `xyz-d50`, `xyz-d65`
- Defined **interpolation spaces** and **gamut mapping** behavior
- Sample conversion code, including **D65↔D50 Bradford adaptation** and **ΔE2000**

## CSS Color 5 — Key Additions

- **`color-mix()`**
- **relative color syntax** (`oklch(from base ...)`)
- **`light-dark()`**
- **`@color-profile`** for ICC-backed custom spaces
- **`device-cmyk()`** for uncalibrated CMYK, plus calibrated CMYK workflows via ICC profiles

Note: the original L5 draft included `color-contrast()` (with candidate list + algorithm parameter). It was **dropped**. The replacement, `contrast-color()`, shipped via L6.

## CSS Color 6 — Key Additions

- **`contrast-color()`** — returns black or white only; the algorithm is intentionally unspecified. Shipped Chrome 147 (Mar 2026), Firefox 146, Safari 26.
- **`color-layers()`** — under draft.

For richer contrast logic — including APCA-aware color selection — use [`apcach`](https://github.com/antiflasher/apcach) and see [`apca-myndex-contrast.md`](../../../color-contrast-facts/references/techniques/apca-myndex-contrast.md) (color-contrast-facts).

## Why This Matters for the Skill

- This is the correct source for browser-facing advice on **OKLCH**, **wide-gamut CSS**, and **mixing in Oklab/Oklch**.
- Useful for distinguishing what is **standardized**, what is **browser-specific**, and what is just a library convention.
- Bridges design-system tasks with real color science: **D50/D65 adaptation**, **gamut mapping**, and **profiled color spaces** are all first-class topics here.

## Practical Use

- Use for any **web or design-system** question involving color syntax.
- Use when recommending **CSS-native palette generation** or **relative color transformations**.
- Use when a user asks what a feature **means** or how it is **supposed** to behave in CSS.
- If a user asks whether a workflow is **currently shipped**, pair this reference with up-to-date browser compatibility data rather than inferring support from the spec alone.
