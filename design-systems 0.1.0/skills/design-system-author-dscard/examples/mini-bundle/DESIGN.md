---
version: alpha
name: Blueprint · the light table
description: An architect's light table — cool paper white, drafting-ink blue lines, everything measured.
colors:
  neutral-background: "oklch(0.97 0 0)"
  neutral-background-dark: "oklch(0.22 0 0)"
  neutral-surface: "oklch(0.94 0 0)"
  neutral-surface-dark: "oklch(0.25 0 0)"
  neutral-on-surface: "oklch(0.18 0 0)"
  neutral-on-surface-dark: "oklch(0.99 0 0)"
  neutral-on-surface-variant: "oklch(0.45 0 0)"
  neutral-on-surface-variant-dark: "oklch(0.8 0 0)"
  neutral-outline-variant: "oklch(0.6 0 0 / 30%)"
  neutral-outline-variant-dark: "oklch(0.6 0 0 / 30%)"
  primary: "oklch(0.45 0.16 260)"
  primary-dark: "oklch(0.7 0.14 260)"
  primary-hover: "oklch(0.38 0.14 262)"
  primary-hover-dark: "oklch(0.78 0.12 261)"
  primary-on-primary: "oklch(1 0 0)"
  primary-on-primary-dark: "oklch(0.18 0 0)"
typography:
  heading-md:
    fontFamily: Inter Tight
    fontSize: 28px
    fontWeight: 800
    lineHeight: 1.143
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.5
spacing:
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
rounded:
  sm: 8px
  md: 12px
  full: 9999px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  card:
    backgroundColor: "{colors.neutral-surface}"
    textColor: "{colors.neutral-on-surface}"
    rounded: "{rounded.md}"
    padding: 16px
---

# Blueprint · the light table — Design System

_Read this file as your instructions — it is the prompt. Token values are normative;
the prose explains how to apply them. Every color role ships a light value and a
`-dark` sibling: pick the pair, not one end. (Teaching fixture: 8 roles, deliberately
below the 15–25 production band — shape over fidelity.)_

## Overview

An architect's light table: cool paper white, one drafting-ink blue, everything
measured twice. Precision is the personality — no decoration a ruler didn't draw.

## Colors

Reason over **roles**, never raw values. Token naming follows the Ultimate Tokens
grammar `--{prefix}-{family}-{slot}`; this fixture's prefix is `c`, families
`neutral` (the paper) and `primary` (the ink).

- **Background `{colors.neutral-background}` / Surface `{colors.neutral-surface}`** —
  the paper: page, then one raised sheet.
- **Foreground `{colors.neutral-on-surface}`** — primary text;
  **Muted `{colors.neutral-on-surface-variant}`** — captions and secondary text;
  **Border `{colors.neutral-outline-variant}`** — a translucent hairline, same value
  both schemes.
- **Primary `{colors.primary}`** — drafting-ink blue: the one decisive action per
  view. `{colors.primary-on-primary}` carries its label; `{colors.primary-hover}`
  carries hover.

**Pairing law.** Text on `primary` uses `primary-on-primary` (white in light,
near-black in dark — the pair differs by scheme). Text on paper uses `on-surface`
or `on-surface-variant`. A crossed pair fails contrast in one scheme.

## Typography

`Inter Tight` for headings (800), `Inter` for body (500); fallback `system-ui`.
Set size, line-height, and weight together from one level — never free-type.

## Layout

Compose every gap from the spacing scale (`{spacing.sm}` … `{spacing.xl}`); a 13px
gap does not exist. Whitespace separates; borders are a last resort.

## Elevation & Depth

Elevation is a surface step (`background` → `surface`), not a drop shadow.

## Shapes

Inputs `{rounded.sm}`, buttons and cards `{rounded.md}`. One radius language per view.

## Components

- **Buttons.** `button-primary` per the frontmatter; **hover** uses
  `{colors.primary-hover}` (both scheme ends ship); **focus** shows a 2px
  `{colors.primary}` outline at 2px offset; **disabled** drops to ~45% opacity.
- **Cards.** `{colors.neutral-surface}` on `{colors.neutral-background}` with a 1px
  `{colors.neutral-outline-variant}` hairline.
- **Chips/badges.** `{colors.neutral-surface}` fill, `{colors.neutral-on-surface-variant}`
  text, `{rounded.full}` radius. Padding is the one sanctioned exception to the
  spacing scale: a compound value below the 4px floor (e.g. `2px 8px`) — the
  schema's `padding` property holds one Dimension, so a pill's asymmetric padding
  can never BE a frontmatter token. Pick one value, hardcode it in every chip,
  everywhere. The violation is inconsistency, not being off-scale.

## Do's and Don'ts

- ❌ **Never hardcode a color** — bind the role.
- ❌ **Never cross an on-pair** — the fill's own on-token, per scheme.
- ❌ **Never stack competing primaries** — one ink-blue action per view.

## Responsive Behavior

Mobile-first; stack below ~640px; touch targets ≥ 44px; body text stays ≥ 16px.
Both schemes hold at every width.

## Agent Prompt Guide

You are generating UI for **Blueprint · the light table**. Work in this order:
tokens first (never invent a value) → roles, then scheme (both ends provided) →
scale, then states. Define roles once as custom properties — `color-scheme` on
`:root` is required or the dark end never fires:

```css
:root {
  color-scheme: light dark;
  --c-primary: light-dark(oklch(0.45 0.16 260), oklch(0.7 0.14 260));
  --c-primary-on-primary: light-dark(oklch(1 0 0), oklch(0.18 0 0));
  /* …every role, from its light + -dark pair… */
}
```

When rules conflict, the three hard rules win. Mirror the `components/` previews.
