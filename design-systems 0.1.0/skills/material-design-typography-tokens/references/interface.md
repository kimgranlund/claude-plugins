# Interface text — the `ui` voice (and `code`)

Everything you *operate* rather than *read* is the **ui** voice on `--font-ui` (Inter): menus, tabs,
table cells, standalone labels, badges, tooltips. It carries the widest ramp (**3XS–2XL**, eight
levels) because interface density varies far more than prose does, and — like the other box voices
(`code` and `kicker`, the mono-role voices) — it has a **single-line height** (`-line-single`, leading
1.0) for text that sits locked in a box. In this kit `ui` is weight 480 and `code` is weight 460.
**Controls** (buttons, inputs, selects) are the one exception: their text *size* is the geometry
skill's (the boundary section below), and the ui voice gives them only family/weight/tracking.

## Interface text levels (non-control chrome)

The `ui` voice's own **size** applies to interface text NOT locked in a control box. Pick the level by density:

| Element | Class | Line |
|---|---|---|
| menu item | `.md-sys-typescale-ui-md` | `-line-single` |
| field label | `.md-sys-typescale-ui-sm` (or `-xs`) | `-line-single` |
| helper / error text under a field | `.md-sys-typescale-ui-xs` | `-line` (may wrap) |
| table cell | `.md-sys-typescale-ui-sm` | `-line-single` |
| table column header | `.md-sys-typescale-ui-xs` (often paired with `sub-heading` for caps labels) | `-line-single` |
| metadata / timestamp chip | `.md-sys-typescale-ui-xs` | `-line` |
| badge / chip / tag | `.md-sys-typescale-ui-2xs` or `-xs` | `-line-single` |
| tooltip | `.md-sys-typescale-ui-xs` | `-line` |
| the tiniest dense affordance | `.md-sys-typescale-ui-3xs` | `-line` |

**A control is NOT in this table.** A button / input value / select takes its text *size* from the
geometry step's `--md-sys-size-{step}-font` (via `.md-sys-control-{step}`) — which **equals** the `ui`
size at that step, so box and text share one number. Give the control `font-family: var(--font-ui)` + the
ui level's `-weight` / `-tracking` for character; **never** the whole `.md-sys-typescale-ui-*` class (it
re-sets `font-size` and a multi-line `-line` against the box). "What size is this button" →
material-design-geometry-tokens.

**Single-line vs multi-line:** non-control chrome that never wraps (a menu item, a cell, a badge) uses
`--md-sys-typescale-ui-{level}-line-single` so the box height is exact; text that may wrap (helper text, a
multi-line tooltip) uses `--md-sys-typescale-ui-{level}-line`. The `.md-sys-typescale-ui-*` class ships the
multi-line `-line` — switch to `-line-single` explicitly, or the box grows on wrap.

## Composing with control geometry (the boundary with the geometry skill)

**A control's own text-size is NOT the `ui` typescale voice — it belongs to the geometry skill.** A
control styled with `.md-sys-control-{step}` takes its text size from the geometry CONTROL ramp's
`--md-sys-size-{step}-font` field (the box height, padding, and radius come from the same
material-design-geometry-tokens step). "What font size for this button" lands THERE, not here — the
two skills must agree, so don't restyle a control's text with a `ui` level.

The `ui` typescale voice is for interface text NOT bound to a control box: menu items, table cells,
standalone labels, badges, helper/tooltip text. Where you *do* map a `ui` level to a control size for
those, note the ramps differ: the geometry control ramp is **xs–2xl** (6 steps), so the `ui`
typescale's `3xs`/`2xs` are the two finer steps BELOW the smallest control, for dense chrome. Match
the level for the middle of the range (MD ↔ MD, 2XL ↔ 2XL) and the text sits right.

## Code in the interface

`code` voice (JetBrains Mono) for keyboard shortcuts (`.md-sys-typescale-code-xs`), technical values,
inline tokens in settings, and tabular figures in a table (`.md-sys-typescale-code-sm` for alignment —
the mono figures keep columns straight). Same 3XS–2XL ramp as `ui`, and it also carries
`-line-single` for single-line cells.

## Don't

- Don't use `body` for buttons/labels — interface chrome is `ui` (body's leading and rhythm are tuned
  for reading paragraphs, not fitting a control).
- Don't set control `line-height` by hand — use `-line-single`; that IS the fit.
- Don't invent sizes between levels — the eight-level `ui` ramp is deliberately fine-grained; there's a
  level for it.
- Don't uppercase a `ui` label by hand for a caps column header — pair it with `sub-heading` (uppercase
  by treatment) instead.
