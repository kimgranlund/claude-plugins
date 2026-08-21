# Token grammar & color laws

## The naming grammar

Every color token is **constructed, never invented**: `--{prefix}-{family}-{slot}`.

- **Prefix** — one per project (`md-sys-color`, `color`, …). The grammar is **prefix-adaptive**: under a different host prefix, swap the prefix and keep `{family}-{slot}` intact. A DESIGN.md states its prefix once.
- **Families** — the reference set: `neutral`, `primary`, `secondary`, `tertiary`, `danger`, `success`, `warning`, `info`. A brand may add signature families; every family it declares carries the full slot inventory. Family names are role positions, not mandated literals — a generator may derive them from its own palette naming (the ultimate-tokens exporter's neutral family is kit-derived), as long as the file states the mapping.
- **Compat aliases** — a consumer dialect may require a literal family name (Stitch expects
  `primary`): emit an alias token pointing at the brand family's values, and only when the brand
  family isn't already literally so named — never a duplicate key (added 2026-08-20, documenting
  the ultimate-tokens exporter's Stitch-compat alias).
- **Slots** — the constructable vocabulary:
  - family name alone = the fill: `--md-sys-color-primary`
  - text/icons ON a fill: `{family}-on-{family}` (e.g. `primary-on-primary`)
  - states suffix the fill: `-hover`, `-active`, `-disabled`. Disabled is an inert wash — either
    a resolved role-table token (the ultimate-tokens exporter's way, preferred: it stays a real
    token; its light and `-dark` values are identical) or a 60%-alpha wash of the base,
    mode-independent either way (amended 2026-08-20, exporter-alignment review). `-active` is
    required wherever a family is actually used as an interactive fill (typically the
    neutral/chrome controls + the brand family) and omitted on families never used as
    interactive fills; status families rarely serve as interactive fills, but when one does — a
    danger-filled destructive-action button is legal status semantics — it too carries the
    interactive states. (Dated correction 2026-08-20: this file's prior text enumerated `active`
    for every family; that blanket requirement is retired.)
  - app surfaces live in **neutral**: `neutral-background`, `neutral-surface`, `neutral-surface-high`; text on them: `neutral-on-surface`, `neutral-on-surface-variant`; hairlines: `neutral-outline-variant` (translucent, often identical in both schemes)
  - extended layer (optional but standardized): `-container(-low/-high)` tints, `-scrim-{weakest…strongest}` ladders, `-surface-{dimmest…brightest}` ladders, `-outline(-hover/-active/-disabled)`, `-placeholder`, `-inverse-surface`/`-inverse-on-surface`

## The five laws

1. **Pairing law.** Text on a family fill uses that family's own `on-{family}` token — which differs by scheme. Text on background/surface uses `on-surface` / `on-surface-variant`. A crossed pair (e.g. `primary` fill + `neutral-on-surface` text) fails contrast in one scheme, always.
2. **Scheme parity.** Every role ships a light value AND a `-dark` sibling — identical key inventories. Never hand-roll a dark variant; pick the pair. State values invert direction by scheme: hover **darkens** on light, **brightens** on dark.
3. **Role, never raw.** Consumers bind to roles so a re-theme flows everywhere. A raw hex in generated UI is a defect regardless of how correct the color looks.
4. **One primary per view.** A single `primary` action; signature families (secondary/tertiary) carry quiet emphasis — small reads, never fields of color.
5. **Status means status.** `danger`/`success`/`warning`/`info` speak only for state — never decoration.

## The runtime idiom

The reference consumption pattern is native scheme switching — one declaration, both schemes:

```css
:root {
  color-scheme: light dark;   /* REQUIRED — without it the dark end never fires */
  --md-sys-color-primary: light-dark(oklch(0.6498 0.1222 224.12), oklch(0.6498 0.1222 224.12));
  --md-sys-color-primary-hover: light-dark(oklch(0.496 0.0966 227.89), oklch(0.7657 0.1409 221.45));
  /* …every role, from its light + -dark pair… */
}
```

No media-query fork; no duplicate token blocks. Force a scheme locally with `color-scheme: light` on a scope.

## Disclosure over correction

A DESIGN.md ships the brand's values **verbatim** and discloses what measurement finds — it never silently "fixes" the brand:

- Contrast is measured per fill/on-pair per scheme. Pairs below 4.5:1 are **listed as disclosures** (e.g. "warning-on-warning / warning = 1.97:1 < 4.5:1 — accepted brand override"), with the escape hatch named (a contrast-first mode, or the family's `on-surface-variant` roles for text-critical UI).
- Authorial divergences from the grammar's expectations are called out inline ("DIVERGENCE: … rationale …"), never smoothed over.
- This is a hard fence for authors and consumers alike: **accessibility standards are disclosed, not enforced**. The file gives the brand's decision and the measured consequence; the consuming team owns the tradeoff.

## Scales and geometry

- **Spacing** — one closed ladder (reference: 0/4/8/12/16/24/32/48/64/96). The law travels with it: *an off-scale gap does not exist.*
- **Radii** — one closed scale with an element map (chips xs · inputs sm · buttons md · cards lg · modals xl · pills full) and the mixing prohibition: one radius language per view.
- **Typography** — leading is a **unitless factor**, tracking is **em**; px in either slot is a defect. Weight is voice: never interchange weights across levels. The section always carries the **text-rendering baseline** block (the macOS smoothing pair · `text-rendering: optimizeLegibility` · `font-optical-sizing: auto` · `font-synthesis: none` · `font-kerning: normal` + `font-variant-ligatures: common-ligatures` · the `code, pre, kbd { font-variant-ligatures: none }` exception) — a DESIGN.md whose Typography section omits it is incomplete.
- **Geometry (optional extended layer)** — a control-size ramp (height/icon/font/padding per size step), insets, gaps, border widths, and a numeric focus ring (e.g. 2px ring at 2px offset). Include when the brand ships dense product UI.
