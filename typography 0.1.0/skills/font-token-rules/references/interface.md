# Interface text — the `label` voice (and `code`, `kicker`)

Everything you *operate* rather than *read* is the **label** voice on `--font-ui`: buttons,
inputs, labels, menus, tabs, table cells, badges, tooltips. Like the other box-text voices
(`code` and `kicker`, the `mono`-role voices — pegged to the same sizes as `body` and `label`
respectively), it's a 3-step **sm/md/lg** ramp and carries a **single-line height**
(`-line-single`, leading 1.0) for text that sits locked in a box.

## Control & component text

| Element | Class | Line |
|---|---|---|
| default button / input value / menu item | `.type-label-md` | `-line-single` (single-line control) |
| large / prominent button | `.type-label-lg` | `-line-single` |
| small / dense button, compact control, field label | `.type-label-sm` | `-line-single` |
| helper / error text under a field | `.type-label-sm` | `-line` (may wrap) |
| table cell | `.type-label-sm` | `-line-single` |
| table column header | `.type-label-sm` (often paired with `sub-heading` for caps labels) | `-line-single` |
| caption / metadata / timestamp | `.type-tiny-md` | `-line` (prose — `tiny` rides `ui`'s font but wraps) |
| badge / chip / tag | `.type-label-sm` | `-line-single` |
| tooltip | `.type-label-sm` | `-line` |

**Single-line vs multi-line:** a control whose text never wraps (a button, an input value, a cell)
uses `--type-label-{step}-line-single` so the box height is exact; text that may wrap (helper
text, a multi-line tooltip) uses `--type-label-{step}-line`. The `.type-label-*` class ships the
multi-line `-line` — switch to `-line-single` explicitly on single-line controls, or the box grows
on wrap.

## Composing with control geometry

**A control's own text-size is the `label` voice; the control's BOX is not.** A control's height,
padding, and radius belong to the project's dimension/geometry token layer, not this skill — that
layer typically derives each control size's font from the `label` voice at the matching step
(SM ↔ SM, MD ↔ MD, LG ↔ LG). A geometry ladder with steps beyond the label ramp (an XS or an
expressive XL/2XL band) has no label counterpart there and falls back to its own size law — match
the step across the two systems where both exist and the box fits the text.

The `label` voice covers interface text NOT bound to a control box too: menu items, table cells,
standalone labels, badges, helper/tooltip text — anywhere chrome needs sizing without a paired box.

## Code in the interface

`code` voice (mono, pegged to `body`'s own sizes) for keyboard shortcuts (`.type-code-sm`),
technical values, inline tokens in settings, and tabular figures in a table (`.type-code-md` for
alignment — the mono figures keep columns straight). It also carries `-line-single` for
single-line cells. Which real monospace typeface backs `--font-mono` is a font-selection call —
see [`references/font-selection.md`](font-selection.md).

## Don't

- Don't use `body` for buttons/labels — interface chrome is `label` (body's leading and rhythm are
  tuned for reading paragraphs, not fitting a control).
- Don't set control `line-height` by hand — use `-line-single`; that IS the fit.
- Don't invent sizes between steps — every voice is a fixed sm/md/lg ramp; there's a step for it.
- Don't uppercase a `label` by hand for a caps column header — pair it with `sub-heading`
  (uppercase by treatment) instead.
