# Containers — surfaces, elevation, cards, modals, dividers

All structural fills come from the chrome palette (`neutral` here). The system has THREE fill
families with distinct jobs — page tiers, elevation ladders, and translucent containers.

## The base tiers

| Surface | Role |
|---|---|
| page/app background (the deepest layer) | `--md-sys-color-neutral-background` |
| the default working surface on it (main pane, list body) | `--md-sys-color-neutral-surface` |

## Elevation — two ladders, different physics (exact; easy to get wrong)

Where M3 gives ~5 container tiers, nonoun extends the chrome palette into a **12-tier surface
ladder** — two independent axes of six:

**`-surface-low…high` (mirrored)** — *relational* elevation: `lowest · lower · low · high ·
higher · highest`. These flip stops across modes so **low always reads recessed and high always
reads raised**, in light AND dark. This is the ladder for UI structure:

| Element | Role |
|---|---|
| recessed wells: input fields, code blocks, empty states, track/gutter | `--md-sys-color-neutral-surface-low` (deeper: `-lower`, `-lowest`) |
| raised: cards, panes, popovers | `--md-sys-color-neutral-surface-high` |
| higher still: sticky headers, dropdown menus | `--md-sys-color-neutral-surface-higher` |
| topmost: modals, dialogs, command palettes | `--md-sys-color-neutral-surface-highest` |

**`-surface-dim…bright` (mode-consistent)** — *literal* lightness: `dimmest…brightest` is darker→
lighter in BOTH modes (no flip). Use when you mean actual light, not stacking order: a dimmed
inactive pane, a spotlight/hero band, a photography-adjacent backdrop. Do not mix the two ladders
for the same job — elevation is Low/High; lighting is Dim/Bright.

Shadows are optional garnish on top of the ladder (fills carry the elevation); keep them scheme-aware
and subtle.

## Containers — the translucent tint family

`--md-sys-color-neutral-container` (+ `-low`, `-high`, and the hover/active/disabled states) are
**500-stop translucents**: they tint whatever they sit on, so they compose on ANY tier. Use them for
*grouped-content fills inside a surface* — chips, table row hover, selected list items, tonal
buttons, well-within-a-card — rather than for structural elevation. Accent/intent palettes have the
same family (`--md-sys-color-primary-container`, `--md-sys-color-success-container`) for
meaning-tinted fills.

## Recipes

| Element | background | border | text |
|---|---|---|---|
| card | `--md-sys-color-neutral-surface-high` | `--md-sys-color-neutral-outline-variant` (or none) | `-on-surface` / `-on-surface-variant` |
| pane / sidebar | `--md-sys-color-neutral-surface` or `-surface-low` | `--md-sys-color-neutral-outline-variant` divider | as above |
| sheet / drawer | `--md-sys-color-neutral-surface-higher` | top/side divider `-outline-variant` | as above |
| modal / dialog | `--md-sys-color-neutral-surface-highest` over a scrim (feedback.md) | none or `-outline-variant` | as above |
| canvas (editor/document area) | `--md-sys-color-neutral-background` or `-surface-lowest` | — | — |
| table header | `--md-sys-color-neutral-surface-low` | row dividers `-outline-variant` | `-on-surface-variant` |
| selected/hover row | `--md-sys-color-neutral-container-low` hover · `-container` selected | — | `-on-surface` |

Text on any container is the palette's `-on-surface` / `-on-surface-variant` — there is no
`-on-container` role.

## Dividers & borders

| Job | Role |
|---|---|
| hairline dividers, subtle card borders (the default) | `--md-sys-color-neutral-outline-variant` |
| stronger separation, field borders, emphasized rules | `--md-sys-color-neutral-outline` |
| interactive-border states | the `-outline*-hover/-active/-disabled` families |

Border WIDTH comes from the geometry tokens (`--md-sys-border-thin/-thick`); this palette only colors it.

## Inverse surfaces

`--md-sys-color-neutral-inverse-surface` + `--md-sys-color-neutral-inverse-on-surface` — the
deliberately opposite-scheme pair for small floating chrome that must contrast with everything:
tooltips and toasts (feedback.md). Not for large regions — to make a whole section opposite-scheme,
set `color-scheme` on it instead (SKILL.md law 4).
