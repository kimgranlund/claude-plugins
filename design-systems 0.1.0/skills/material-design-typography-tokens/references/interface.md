# Interface text — the `label` voice (and its mono siblings)

Everything you *operate* rather than *read* is the **label** voice on the `ui` font role: menus, tabs,
table cells, standalone labels, badges, tooltips. Like the other BOX voices — **body-mono, label-mono,
kicker** (the mono-role box voices) — it has a **single-line height** (`-line-single`, leading 1.0) for
text that sits locked in a box. **Controls** (buttons, inputs, selects) are the one exception: their
text *size* is the geometry skill's (the boundary section below), and the `label` voice gives them only
family/weight/tracking.

Since 2026-07-13 every voice — `label` included — rides the SAME uniform **SM/MD/LG** ramp (previously
`label`'s ancestor, `ui`, had a much wider **3XS–2XL**, eight levels, specifically to cover geometry's
denser steps). That wider ramp is gone; **only 3 of geometry's 6 control steps now compose with type at
all** (see the boundary section) — plan interface density accordingly.

## Interface text levels (non-control chrome)

The `label` voice's own **size** applies to interface text NOT locked in a control box. Pick the level
by density (only three exist now — SM/MD/LG):

| Element | Class | Line |
|---|---|---|
| menu item | `.md-sys-typescale-label-md` | `-line-single` |
| field label | `.md-sys-typescale-label-sm` | `-line-single` |
| helper / error text under a field | `.md-sys-typescale-label-sm` | `-line` (may wrap) |
| table cell | `.md-sys-typescale-label-sm` | `-line-single` |
| table column header | `.md-sys-typescale-label-sm` (often paired with `sub-heading` for caps labels) | `-line-single` |
| metadata / timestamp chip | `.md-sys-typescale-label-mono-sm` | `-line` |
| badge / chip / tag | `.md-sys-typescale-label-sm` | `-line-single` |
| tooltip | `.md-sys-typescale-label-sm` | `-line` |

**A control is NOT in this table.** A button / input value / select takes its text *size* from the
geometry step's `--md-sys-size-{step}-font` (via `.md-sys-control-{step}`). Give the control
`font-family: var(--font-voice-label)` (or `var(--font-ui)` on an older export without the per-voice
prop) + the `label` level's `-weight` / `-tracking` for character; **never** the whole
`.md-sys-typescale-label-*` class (it re-sets `font-size` and a multi-line `-line` against the box).
"What size is this button" → material-design-geometry-tokens.

**Single-line vs multi-line:** non-control chrome that never wraps (a menu item, a cell, a badge) uses
`--md-sys-typescale-label-{level}-line-single` so the box height is exact; text that may wrap (helper
text, a multi-line tooltip) uses `--md-sys-typescale-label-{level}-line`. The `.md-sys-typescale-label-*`
class ships the multi-line `-line` — switch to `-line-single` explicitly, or the box grows on wrap.

## Composing with control geometry (the boundary with the geometry skill — CHANGED 2026-07-13)

**A control's own text-size is NOT the `label` typescale voice — it belongs to the geometry skill.** A
control styled with `.md-sys-control-{step}` takes its text size from the geometry CONTROL ramp's
`--md-sys-size-{step}-font` field (the box height, padding, and radius come from the same
material-design-geometry-tokens step). "What font size for this button" lands THERE, not here — the two
skills must agree, so don't restyle a control's text with a `label` level.

**Only geometry's SM/MD/LG steps are actually typed from `label` now.** Geometry keeps its full six
control steps (**xs·sm·md·lg·xl·2xl**), but `label` only has three levels (SM/MD/LG) to compose with —
geometry's `xs`, `xl`, and `2xl` steps have no `label` counterpart anymore and fall back to geometry's
own standalone size law for their `-font` field (still a real, derived value — just not sourced from
type). This is a real narrowing from the old `ui` voice (which had 3XS–2XL, eight levels, wide enough to
cover every geometry step): before composing a NEW control size at `xs`/`xl`/`2xl`, confirm the export's
`--md-sys-size-{step}-font` and the `label` level's `-size` at the matching name — they will legitimately
DIFFER at those three steps, by design, not drift.

## Code in the interface

`body-mono`/`label-mono` (mono role) for keyboard shortcuts, technical values, inline tokens in
settings, and tabular figures in a table — the mono figures keep columns straight. Same SM/MD/LG ramp as
every other voice, and both carry `-line-single` for single-line cells (they're BOX voices).

## Don't

- Don't use `body` for buttons/labels — interface chrome is `label` (body's leading and rhythm are
  tuned for reading paragraphs, not fitting a control).
- Don't set control `line-height` by hand — use `-line-single`; that IS the fit.
- Don't assume a `label`/`label-mono` level exists for every geometry control step — only SM/MD/LG do;
  `xs`/`xl`/`2xl` controls get their font size from geometry's own fallback law, not a typescale level.
- Don't uppercase a `label` for a caps column header by hand — pair it with `sub-heading` (uppercase by
  treatment) instead.
