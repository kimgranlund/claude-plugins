# Geometry token semantics — what each `--md-sys-size/-radius/-space/-inset/-gap/-border/-focus-ring-*` field MEANS

One line per token, or per group where tokens are graduated variants of one concept. Two tiers: CONTROL
geometry (one size step, everything inside derives from its height) and CONTAINER geometry (space
between/around components, mode-independent). This file only answers "what does this token mean" — for
the binding grammar and recipes, see `material-shape-facts`.

## The control ramp — `--md-sys-size-{xs…2xl}-*`

Six steps (`xs · sm · md · lg · xl · 2xl`); pick the STEP first (the whole control's scale), then every
field below follows from it — never set one field independently of its step.

| Field | Meaning | Reach for it when… |
|---|---|---|
| `-height` | The control's own block-size — the one number everything else derives from. | Sizing the box itself: `block-size`/`height` on a button, input, select. |
| `-icon` | The leading content-icon / slot glyph size, centered by the height. | An icon living INSIDE this control's step. |
| `-caret` | The affordance mark (a dropdown ▾, a disclosure chevron). | A select/dropdown/expandable control at this step. |
| `-font` | The control's text size — composed from the `ui-control` typescale voice at EVERY step (`xs`..`2xl`; the voice rides the full 6-level ramp — the old partial `label`-voice composition at `sm`/`md`/`lg` only is retired). | Setting a control's `font-size` — never the typescale's own `-size` var for a control. |
| `-gap` | The icon↔label gap INSIDE the control — a hand-CALIBRATED unit per step (not a font fraction), scaled by baseHeight and the density knob. | Spacing a leading/trailing icon from its label, same step. |
| `-padding-narrow` | Inline edge padding for a control WITH a leading slot/icon (the SLOT edge) — (height − icon)/2. | The control has an icon, avatar, or other leading element. |
| `-padding-wide` | Inline edge padding for a SLOTLESS (bare text) control (the bare/caret edge) — (height − caret)/2. | A plain text button/label/input with no leading slot. |
| `-padding-narrow-compact` | The slot edge with the control's own gap absorbed — (height − gap − icon)/2. | A dense layout that also wants the tighter compact rhythm. |
| `-padding-wide-compact` | The bare/caret edge with the control's own gap absorbed — (height − gap − caret)/2. | A dense layout's bare-text control. |
| `-min` | The 1:1 hit-target floor — an icon-only control is at least square (height×height). | Sizing an icon-only control's minimum footprint; also the base to extend from for the ~44px touch-target floor on compact steps. |
| `-radius` | The control's own corner = height/2 — already a full pill. | A control's `border-radius` — never a fixed radius level here; it must track the step. |

## Radius scale — `--md-sys-radius-{none·xs·sm·md·lg·xl·full}` (containers only)

| Group | Meaning | Reach for it when… |
|---|---|---|
| `-none` | Square corners. | A container that should read hard-edged (a table, a full-bleed media block). |
| `-xs` / `-sm` | Subtle rounding. | A small chip, a dense list row, a subtle card. |
| `-md` (the usual default) | The kit's favored "default card" corner — what `-default` aliases. | The everyday card/panel/dialog corner when nothing more specific applies. |
| `-lg` / `-xl` | More prominent rounding. | A hero card, a prominent surface that wants a softer, louder corner. |
| `-full` | A full pill/circle (9999px). | Round NON-controls only — avatars, dots, standalone pill shapes. A CONTROL never needs this explicitly; its own `-radius` is already height/2. |

Containers pick a LEVEL off this scale; a control's own corner is its per-step `-radius` instead — never
put a fixed `--md-sys-radius-*` on something that should scale with a control's height.

## The raw space ladder — `--md-sys-space-{0…9}` (the escape hatch)

The underlying 4dp-founded ladder everything else is named rungs of. Reach for a SEMANTIC inset/gap
token first (below); drop to a raw `--md-sys-space-N` only for a one-off neither tier names (an unusual
offset, a bespoke grid gutter).

## Insets — padding INSIDE a container

| Group | Meaning | Reach for it when… |
|---|---|---|
| `-control-group` | Padding inside a toolbar / button group / segmented control. | Wrapping a cluster of controls as one unit. |
| `-card` | A card's inner padding. | Any card-shaped container's own padding. |
| `-panel` | A sidebar / panel / section body's padding. | A larger structural region, one tier up from a card. |
| `-dialog` | A modal / dialog / sheet body's padding. | The content area of an overlay surface. |
| `-page` | The outermost page gutter / content padding. | The page's own outer inline padding. |

Pick by WHAT CONTAINS the content, not by eyeballing a number — the token already carries the right rhythm.

## Gaps — space BETWEEN siblings

| Group | Meaning | Reach for it when… |
|---|---|---|
| `-cluster` | The tightest sibling gap. | Inline siblings — a row of buttons, chips, inline metadata. |
| `-stack-tight` | A tight vertical gap. | Closely related stacked items — a label and its own field, list rows. |
| `-stack` | The default vertical stack gap. | The everyday vertical rhythm — form fields, a list of cards. |
| `-stack-loose` | A looser vertical gap. | Loosely related stacked groups — form sections. |
| `-grid` | The gutter of a grid. | A card/tile grid's own gutter. |
| `-section` | The widest gap. | Rhythm between major page sections. |

## Borders & focus ring — constants, not rhythm

| Token | Meaning | Reach for it when… |
|---|---|---|
| `-border-thin` | The default hairline width. | Dividers, subtle card borders, field borders — the default choice. |
| `-border-thick` | An emphasized border width. | A rule or border that needs to read heavier than the default hairline. |
| `-focus-ring-width` / `-focus-ring-offset` | The one focus-ring recipe's geometry (color comes from the color skill's accent). | EVERY focusable element — never omit or hand-roll a focus indicator. |

Borders and the focus ring don't scale with density or a control's step — a hairline is a hairline at
every size; the ring is an accessibility contract, not a design lever.
