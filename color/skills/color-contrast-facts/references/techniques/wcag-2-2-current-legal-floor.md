# WCAG 2.2 — Current Legal Floor

**Last verified:** 2026-04-26

WCAG 2.2 has been the W3C Recommendation since **October 2023**. As of April 2026 it is the version most accessibility regulations point to (EAA, Section 508, AODA, etc.). Treat it as the **legal floor** — the minimum your product must clear — not the design standard.

For design quality, prefer **APCA** ([`apca-myndex-contrast.md`](./apca-myndex-contrast.md)). APCA is more restrictive than WCAG 2.x at comparable thresholds (only ~0.08% of all hex pairs pass APCA Lc 90 vs ~12% passing WCAG 4.5:1) and produces measurably more readable surfaces. WCAG 2.2 is what compliance lawyers ask about; APCA is what users actually read.

## What's new in 2.2 vs 2.1

Nine new SCs, three contrast-relevant:

### SC 2.4.11 — Focus Not Obscured (Minimum) — Level AA
The focus indicator must not be entirely hidden by author-created content (e.g. a sticky footer covering the focused control). Partial occlusion is allowed.

### SC 2.4.12 — Focus Not Obscured (Enhanced) — Level AAA
The focus indicator must not be obscured **at all**.

### SC 2.4.13 — Focus Appearance — Level AAA
Focus indicators must be:
- **At least 2 CSS px thick** along the perimeter, AND
- **3:1 contrast** between focused-state and unfocused-state pixels, AND
- Either a solid outline ≥ 2px around the entire control OR an indicator covering ≥ the area of a 1px-thick perimeter.

This is the SC that kills 1px focus rings against the wrong neighbor.

### SC 2.5.8 — Target Size (Minimum) — Level AA
**24×24 CSS px minimum** target size for pointer inputs, with documented exceptions (inline targets, user-agent control sizes, essential-to-information targets, equivalent UI elsewhere). See [`check-focus`](../../../check-focus/SKILL.md) for the design recipe.

## What carries over from 2.1 (unchanged)

| SC | Threshold | Notes |
|---|---|---|
| 1.4.3 Contrast (Minimum) AA | 4.5:1 normal text, 3:1 large text | The famous numbers; APCA equivalent is roughly Lc 60 / Lc 45 |
| 1.4.6 Contrast (Enhanced) AAA | 7:1 normal text, 4.5:1 large text | APCA equivalent is roughly Lc 90 / Lc 75 |
| 1.4.11 Non-text Contrast AA | 3:1 against adjacent colors | UI components, graphical indicators, focus rings |

For the WCAG ↔ APCA mapping, see [`apca-myndex-contrast.md`](./apca-myndex-contrast.md) (Bridge-PCA section).

## What WCAG 2.2 does NOT address

- **Polarity-sensitive contrast.** Light text on dark backgrounds needs more contrast than dark text on light at the same size; WCAG 2.x scores them identically. APCA fixes this.
- **Spatial frequency.** Small/thin text needs more contrast than large/bold; WCAG 2.x has only a binary "normal vs large" threshold. APCA's per-size lookup tables fix this.
- **Modern color spaces.** WCAG 2.x luminance math predates `oklch()`. APCA uses simplified gamma-2.4 linearization, more aligned with current display tech.

## What WCAG 3 currently is

Per the W3C WAI March 3, 2026 update, WCAG 3 is at **Working Draft** stage with 174 requirements (renamed from "outcomes"). It does **not** include a contrast algorithm — APCA was removed from the WCAG 3 draft in 2023 along with other exploratory items. Realistic Recommendation timeline: **2027–2028 at the earliest**.

This means: you cannot wait for WCAG 3 before shipping accessible contrast. Use **WCAG 2.2 for legal compliance** + **APCA for actual readability**. See [`apca-myndex-contrast.md`](./apca-myndex-contrast.md) for the recommended approach.

Sources:
- [W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)
- [W3C WAI: Understanding SC 2.4.13 Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [W3C WAI: Understanding SC 2.5.8 Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [W3C WAI WCAG 3 Working Draft news (March 2026)](https://www.w3.org/WAI/news/2026-03-03/wcag3/)
- [Adrian Roselli: WCAG 3 Contrast as of April 2026](https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)
- [Eric Eggert: WCAG 3 is not ready yet](https://yatil.net/blog/wcag-3-is-not-ready-yet)

## The recommended stance

1. **Pass WCAG 2.2 AA** (legal). Use a WCAG 2.x checker (Chrome DevTools, axe, Lighthouse).
2. **Design with APCA** (quality). Use the [APCA Calculator](https://apcacontrast.com/) and [`apcach`](https://github.com/antiflasher/apcach) for token derivation. Aim Lc 75+ for body text, Lc 60+ for medium UI text, Lc 45+ for large headings.
3. **Use `contrast-color()` only as a safety net** — it returns black or white, which is sometimes what you want, often not.
4. **Treat WCAG 3 as future** — don't anchor design decisions on a draft that's 2+ years from Recommendation.
