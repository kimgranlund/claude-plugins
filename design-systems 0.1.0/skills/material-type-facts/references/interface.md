# Interface text — `label` (static chrome), `ui-control` (controls), `ui-widget` (compact widgets)

Interface chrome you *operate or read* splits across **three** voices now (TKT-0008, 2026-07-16),
where it used to be one:

- **`label`** (`ui` font role) — the STATIC label voice: text you read but don't operate — table
  cells, tooltips, standalone captions, form field labels, tabs. Rides the shared SM/MD/LG ramp and is
  now a **PROSE** voice (changed 2026-07-16 — it used to be BOX and carry `-line-single`; it no longer
  does).
- **`ui-control`** (`ui` font role) — text FOR a control you operate: buttons, inputs, selects, menu
  items. Rides its OWN full six-level ramp (XS/SM/MD/LG/XL/2XL) and is a **BOX** voice — it has
  `-line-single`. It also composes DIRECTLY into geometry's control-box `-font` field at every one of
  geometry's six steps (the boundary section below).
- **`ui-widget`** (`ui` font role) — text FOR a compact widget you operate but don't type into: tags,
  badges, switches, radio/checkbox labels. Also rides its own six-level ramp and is a **BOX** voice.
  Its size table is its own (smaller than `ui-control`'s) and does NOT compose into geometry.

The two mono siblings, **`body-mono`** and **`label-mono`**, are PROSE too (also changed 2026-07-16) —
see "Code in the interface" below. **`kicker`** (mono role) remains the fourth BOX voice, unchanged.

## Static label text (non-control, non-widget chrome)

The `label` voice's own **size** applies to interface text that is neither a control nor a widget.
Pick the level by density (SM/MD/LG):

| Element | Class | Line |
|---|---|---|
| field label | `.md-sys-typescale-label-sm` | `-line` |
| helper / error text under a field | `.md-sys-typescale-label-sm` | `-line` (wraps) |
| table cell | `.md-sys-typescale-label-sm` | `-line` |
| table column header | `.md-sys-typescale-label-sm` (often paired with `sub-heading` for caps labels) | `-line` |
| tooltip | `.md-sys-typescale-label-sm` | `-line` |
| tab label (non-interactive text portion) | `.md-sys-typescale-label-md` | `-line` |

`label` has **no `-line-single`** since 2026-07-16 — even a visually single-line element like a table
cell uses the ordinary `-line` (multi-line leading). Don't reach for a leading-1.0 override by hand;
the class already sets the right `-line`.

## Control text (buttons, inputs, selects, menu items)

A **control**'s text is `ui-control`, not `label` — this is the change TKT-0008 made. Pick the level
by the control's own geometry step (they share names — `xs·sm·md·lg·xl·2xl`):

| Element | Class | Line |
|---|---|---|
| button label | `.md-sys-typescale-ui-control-md` (or the control's own step) | `-line-single` |
| input value / placeholder | `.md-sys-typescale-ui-control-md` | `-line-single` |
| select value | `.md-sys-typescale-ui-control-md` | `-line-single` |
| menu item | `.md-sys-typescale-ui-control-md` | `-line-single` |
| a control at a compact step | `.md-sys-typescale-ui-control-sm` (or `-xs`) | `-line-single` |
| a control at an expressive step | `.md-sys-typescale-ui-control-lg`/`-xl`/`-2xl` | `-line-single` |

`ui-control` has `-line-single` on every level (leading 1.0) — it is a BOX voice; text in a control
never wraps, and the box owns the rhythm.

## Widget text (tags, badges, switches, radio/checkbox labels)

Compact widget chrome is `ui-widget` — a smaller size table than `ui-control`'s (its own six-level
ramp), for elements that don't need a full control's footprint:

| Element | Class | Line |
|---|---|---|
| badge / chip / tag | `.md-sys-typescale-ui-widget-sm` | `-line-single` |
| switch label | `.md-sys-typescale-ui-widget-sm` | `-line-single` |
| radio / checkbox label | `.md-sys-typescale-ui-widget-sm` | `-line-single` |
| a denser widget variant | `.md-sys-typescale-ui-widget-xs` | `-line-single` |

`ui-widget` also has `-line-single` on every level (it's a BOX voice) but, unlike `ui-control`, it does
**not** compose into `material-shape-facts` — a widget's own box (if it has one) sizes
itself independently; only controls get the geometry composition described below.

## Composing with control geometry (the boundary with the geometry skill — CHANGED 2026-07-16)

**A control's own text-size is the `ui-control` voice, composed directly into geometry.** A control
styled with `.md-sys-control-{step}` takes its text size from the geometry CONTROL ramp's
`--md-sys-size-{step}-font` field, which now **composes from `ui-control`'s matching level** at every
one of geometry's six steps (`xs·sm·md·lg·xl·2xl`) — TKT-0008 retired the old partial composition
(only `sm`/`md`/`lg` used to compose from type; `xs`/`xl`/`2xl` fell back to a standalone geometry-only
law). At default values the two numbers are value-neutral (the `ui-control` voice's own Desktop sizes
are the SAME ratified table — 12·13·15·16·18·20 — geometry's fallback law reproduces on its own), but
`ui-control` tuning now flows all the way into every control box, not just three of its six sizes.

Give a control `font-family: var(--font-voice-ui-control)` + the matching `ui-control` level's
`-weight`/`-tracking` for character, and let geometry's own `--md-sys-size-{step}-font` (or the
`.md-sys-control-{step}` class, which already reads it) own the size — the two should always agree
since one composes from the other; a mismatch means a stale export. "What size is this button" is
answered by `ui-control`'s own level table now, not a separate geometry-only number.

## Code in the interface

`body-mono`/`label-mono` (mono role) for keyboard shortcuts, technical values, inline tokens in
settings, and tabular figures in a table — the mono figures keep columns straight. Same SM/MD/LG ramp
as `body`/`label`. **Both are PROSE voices** (changed 2026-07-16, alongside `label`) — neither carries
`-line-single`; use `-line` even for a single-line mono value. Reach for `ui-control`/`ui-widget`
instead when the mono text sits INSIDE an interactive control or widget box (rare — most mono interface
text is read, not operated).

## Don't

- Don't use `body` for buttons/labels — interface chrome reads `label` (static), `ui-control`
  (controls), or `ui-widget` (compact widgets); `body`'s leading and rhythm are tuned for reading
  paragraphs, not fitting a box.
- Don't reach for `label` on a button, input, select, or menu item — that text is `ui-control` now;
  `label` no longer has `-line-single` to give it.
- Don't reach for `label` on a tag, badge, switch, or checkbox label — that's `ui-widget`.
- Don't set control or widget `line-height` by hand — use `-line-single`; that IS the fit.
- Don't assume `label`, `body-mono`, or `label-mono` has `-line-single` — none of the three do since
  2026-07-16; only `kicker`, `ui-control`, and `ui-widget` are BOX voices.
- Don't uppercase a `label` for a caps column header by hand — pair it with `sub-heading` (uppercase by
  treatment) instead.
