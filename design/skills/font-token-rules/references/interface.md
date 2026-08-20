# Interface text — `label` (static chrome) vs. `ui-control`/`ui-widget` (interactive)

**Re-split 2026-08-20 (TKT-0008, closes #792):** `label` is explicitly **static** interface text —
it names or describes something in the UI but is never itself the operable control.
**`ui-control`/`ui-widget` are the genuinely interactive voices**, each its own dedicated
**6-step XS–2XL ramp** (not the 3-step sm/md/lg ramp `label` rides), because control geometry
needs a size at every one of its six steps. `kicker` is the third and last box voice (mono-role,
pegged to `label`'s own sizes) — `label` itself carries no `-line-single`.

## Control & component text

| Element | Voice · class | Line |
|---|---|---|
| button, input value, select, menu item — any control the user OPERATES | `ui-control` · `.type-ui-control-{xs..2xl}` | `-line-single` (single-line, exact box height) |
| interactive badge/chip/tag/switch — clickable or toggled | `ui-widget` · `.type-ui-widget-{xs..2xl}` (one register under `ui-control`) | `-line-single` |
| static badge count, a read-only chip/tag with no interaction | `label` · `.type-label-sm` | `-line` (not operated — see the single-line rule below) |
| field label, static form caption above an input | `label` · `.type-label-sm` | `-line` (may wrap — `label` is static, never `-line-single`) |
| helper / error text under a field | `label` · `.type-label-sm` | `-line` (may wrap) |
| table cell (data display, non-interactive) | `label` · `.type-label-sm` | `-line` |
| table column header | `label` · `.type-label-sm` (often paired with `sub-heading` for caps labels) | `-line` |
| caption / metadata / timestamp | `tiny` · `.type-tiny-md` | `-line` (prose — `tiny` rides `ui`'s font but wraps) |
| tooltip (informational, non-interactive) | `label` · `.type-label-sm` | `-line` |

**Single-line vs multi-line:** the three box voices — `ui-control`, `ui-widget`, and `kicker` —
use `-line-single` so the box height is exact. Two of them (`ui-control`/`ui-widget`) get it
because the text is genuinely operated; `kicker` is the one static exception — an overline is
never clicked, but it still locks to a single line because it sits in a fixed-height chrome slot.
`label` and every prose voice use only `-line`, even where the text visually sits inside a
chrome-like box (a static badge count, a read-only field) — reach for `-line-single` on
`ui-control`/`ui-widget` only when the element is itself the thing being clicked/typed into/
toggled, and on `kicker` whenever it's used as an overline at all.

## Composing with control geometry

**A control's own text-size is the `ui-control`/`ui-widget` voice; the control's BOX is not.** A
control's height, padding, and radius belong to the project's dimension/geometry token layer, not
this skill — that layer typically derives each control size's font from `ui-control`/`ui-widget`
at the matching step. Because these two voices already ride the full 6-step XS–2XL ramp, a
geometry ladder with an XS or an expressive XL/2XL band has a direct counterpart here where
`label`'s 3-step ramp never did — match the step across the two systems.

`label` still covers static interface text not bound to an operable control: table cells,
standalone descriptive labels, helper/tooltip text, column headers — anywhere chrome needs sizing
without the text itself being the thing operated.

## Code in the interface

The mono-role `body-mono` voice (pegged to `body`'s own sizes — see `prose.md`) for keyboard
shortcuts, technical values, inline tokens in settings, and tabular figures in a table (mono
figures keep columns straight). `body-mono` is a PROSE voice like `body` itself — it carries only
`-line`, never `-line-single`, even set inside a table cell. Which real monospace typeface backs
`--font-mono` is a font-selection call — see [`references/font-selection.md`](font-selection.md).

## Don't

- Don't use `body` for buttons/labels — interface chrome is `label`/`ui-control`/`ui-widget`
  (body's leading and rhythm are tuned for reading paragraphs, not fitting a control).
- Don't use `label` for anything the user operates — that's `ui-control`/`ui-widget`; `label` is
  static only.
- Don't set control `line-height` by hand — use `-line-single` on the three box voices
  (`ui-control`/`ui-widget`/`kicker`); that IS the fit.
- Don't invent sizes between steps — `ui-control`/`ui-widget` are a fixed 6-step XS–2XL ramp,
  every other voice a fixed 3-step sm/md/lg ramp; there's a step for it.
- Don't uppercase a `label` by hand for a caps column header — pair it with `sub-heading`
  (uppercase by treatment) instead.
