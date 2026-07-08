# Interface text — the `ui` voice (and `code`)

Everything you *operate* rather than *read* is the **ui** voice on `--font-ui`: buttons, inputs,
labels, menus, tabs, table cells, badges, tooltips. It carries the widest ramp (**3XS–2XL**, eight
steps) because interface density varies far more than prose does, and — like the other box-text
voices (`code` and `kicker`, the `mono`-role voices) — it has a **single-line height**
(`-line-single`, leading 1.0) for text that sits locked in a box.

## Control & component text

| Element | Class | Line |
|---|---|---|
| default button / input value / menu item | `.type-ui-md` | `-line-single` (single-line control) |
| large / prominent button | `.type-ui-lg` | `-line-single` |
| small / dense button, compact control | `.type-ui-sm` | `-line-single` |
| field label | `.type-ui-sm` (or `-xs`) | `-line-single` |
| helper / error text under a field | `.type-ui-xs` | `-line` (may wrap) |
| table cell | `.type-ui-sm` | `-line-single` |
| table column header | `.type-ui-xs` (often paired with `sub-heading` for caps labels) | `-line-single` |
| metadata / timestamp chip | `.type-ui-xs` | `-line` |
| badge / chip / tag | `.type-ui-2xs` or `-xs` | `-line-single` |
| tooltip | `.type-ui-xs` | `-line` |
| the tiniest dense affordance | `.type-ui-3xs` | `-line` |

**Single-line vs multi-line:** a control whose text never wraps (a button, an input value, a cell)
uses `--type-ui-{step}-line-single` so the box height is exact; text that may wrap (helper text, a
multi-line tooltip) uses `--type-ui-{step}-line`. The `.type-ui-*` class ships the multi-line
`-line` — switch to `-line-single` explicitly on single-line controls, or the box grows on wrap.

## Composing with control geometry

**A control's own text-size is the `ui` typescale voice; the control's BOX is not.** A control's
height, padding, and radius belong to the project's dimension/geometry token layer, not this
skill — that layer typically derives each control size's font-size from the `ui` voice at the
matching step, so a small control ↔ UI small, medium ↔ medium, and so on. Match the step across
the two systems and the box fits the text; "what font-size for this button" still resolves to a
`ui` step even when the box geometry is a different skill's concern.

The `ui` typescale voice is for interface text NOT bound to a control box too: menu items, table
cells, standalone labels, badges, helper/tooltip text — anywhere interface chrome needs sizing
without a paired control box.

## Code in the interface

`code` voice (mono) for keyboard shortcuts (`.type-code-xs`), technical values, inline tokens in
settings, and tabular figures in a table (`.type-code-sm` for alignment — the mono figures keep
columns straight). Same 3XS–2XL ramp as `ui`, and it also carries `-line-single` for single-line
cells. Which real monospace typeface backs `--font-mono` is a font-selection call — see
[`references/font-selection.md`](font-selection.md).

## Don't

- Don't use `body` for buttons/labels — interface chrome is `ui` (body's leading and rhythm are
  tuned for reading paragraphs, not fitting a control).
- Don't set control `line-height` by hand — use `-line-single`; that IS the fit.
- Don't invent sizes between steps — the eight-step `ui` ramp is deliberately fine-grained; there's
  a step for it.
- Don't uppercase a `ui` label by hand for a caps column header — pair it with `sub-heading`
  (uppercase by treatment) instead.
