# Navigation — navs, tabs, menus, selection, icons, focus, data-viz

Chrome rides `neutral`; the CURRENT/selected signal rides the accent. The pattern everywhere:
rest = quiet chrome, hover = a container wash, current = accent-marked.

## Nav items (sidebar, top nav, menus, command palettes)

| State | background | text/icon |
|---|---|---|
| rest | transparent | `--md-sys-color-neutral-on-surface-variant` |
| hover | `--md-sys-color-neutral-container-low` | `--md-sys-color-neutral-on-surface-hover` |
| pressed | `--md-sys-color-neutral-container` | `--md-sys-color-neutral-on-surface-active` |
| **current/selected** | `--md-sys-color-{p}-container` | `--md-sys-color-{p}-on-surface` (+ an optional bare `--md-sys-color-{p}` indicator bar) |
| disabled | transparent | `--md-sys-color-neutral-on-surface-disabled` |

Menus/popovers float on `--md-sys-color-neutral-surface-higher` with an `-outline-variant` border
(containers.md); destructive menu items use `--md-sys-color-danger` text.

## Tabs

Inactive label `--md-sys-color-neutral-on-surface-variant` (hover `-hover`) · active label
`--md-sys-color-neutral-on-surface` · the active indicator (underline/pill) bare
`--md-sys-color-{p}` · a pill-style active tab: bg `--md-sys-color-{p}-container`, label
`--md-sys-color-{p}-on-surface`.

## Links (as chrome: breadcrumbs, footers, "view all")

`--md-sys-color-{p}` with `-hover`/`-active`; visited state is not modeled — don't invent one.
Breadcrumb separators and inactive crumbs: `--md-sys-color-neutral-on-surface-variant`.

## Selection & highlight

- Selected list rows / cells: bg `--md-sys-color-neutral-container` (meaning-laden selection: `--md-sys-color-{p}-container`).
- Multi-select checkmarks: interactive.md's toggle recipe.
- Search-hit highlight: `--md-sys-color-{p}-container-high` behind `-on-surface` text.
- Drag-over / drop target: border `--md-sys-color-{p}-outline-active`, wash `--md-sys-color-{p}-container-low`.

## Icons

Icons inherit their text partner's role — an icon beside `-on-surface-variant` text is
`-on-surface-variant`. Standalone icon buttons follow interactive.md's ghost recipe. Decorative
icons may take supporting accents' bare roles; meaningful icons take intent accents.

## Focus rings (every focusable element, one recipe app-wide)

`outline-color: var(--md-sys-color-{p})` (the brand accent) — width/offset come from the geometry tokens
(`--md-sys-focus-ring-width/-offset`). On accent-filled elements where the ring would vanish, ring with
`--md-sys-color-{p}-on-{p}` instead, or rely on the offset gap. Never remove the ring without
replacing it.

## Data-viz series

Series colors: the bare accents of the non-intent palettes in kit order (`--md-sys-color-primary`,
`--md-sys-color-secondary`, `--md-sys-color-tertiary`, then supporting palettes) — skip `neutral`
and reserve intents for meaning-bearing series (a "failures" line may be `--md-sys-color-danger`).
Emphasis within one series: `-high` (highlighted) vs `-low` (muted context) — the mode-mirrored pair
(text.md). Gridlines `--md-sys-color-neutral-outline-variant`; axis labels `-on-surface-variant`.
