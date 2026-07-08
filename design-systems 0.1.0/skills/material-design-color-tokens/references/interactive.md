# Interactive elements — buttons, controls, form fields

`{p}` = the palette slug. Buttons/CTAs usually ride the brand accent (`primary`); fields and
controls ride the chrome palette (`neutral`) until they carry meaning (then an intent palette —
same roles, different `{p}`). Every recipe below is a complete state family — ship all rows. The
`-hover` / `-active` / `-disabled` siblings are nonoun's extension of the M3 baseline (M3 leaves
these to state-layer opacity; here they're real, tuned tokens) — use them verbatim.

## Buttons

**Filled (primary CTA)** — the accent as a fill:

| State | background | text/icon |
|---|---|---|
| rest | `--md-sys-color-{p}` | `--md-sys-color-{p}-on-{p}` |
| hover | `--md-sys-color-{p}-hover` | `--md-sys-color-{p}-on-{p}-hover` |
| active/pressed | `--md-sys-color-{p}-active` | `--md-sys-color-{p}-on-{p}-active` |
| disabled | `--md-sys-color-{p}-disabled` | `--md-sys-color-{p}-on-{p}-disabled` |

**Tonal / soft (secondary emphasis)** — the translucent container tier:

| State | background | text/icon |
|---|---|---|
| rest | `--md-sys-color-{p}-container` | `--md-sys-color-{p}-on-surface` |
| hover | `--md-sys-color-{p}-container-hover` | `--md-sys-color-{p}-on-surface-hover` |
| active | `--md-sys-color-{p}-container-active` | `--md-sys-color-{p}-on-surface-active` |
| disabled | `--md-sys-color-{p}-container-disabled` | `--md-sys-color-{p}-on-surface-disabled` |

Containers are 500-based translucents — they tint whatever surface they sit on, so a tonal button
composes correctly on any elevation tier. (Text on a container is the palette's `-on-surface`, not
an `-on-container` — there is no such role.)

**Outlined** — transparent fill, stroked:

| State | border | text/icon | background |
|---|---|---|---|
| rest | `--md-sys-color-{p}-outline` | `--md-sys-color-{p}` | transparent |
| hover | `--md-sys-color-{p}-outline-hover` | `--md-sys-color-{p}-hover` | `--md-sys-color-{p}-container-low` |
| active | `--md-sys-color-{p}-outline-active` | `--md-sys-color-{p}-active` | `--md-sys-color-{p}-container` |
| disabled | `--md-sys-color-{p}-outline-disabled` | `--md-sys-color-{p}-disabled` | transparent |

**Ghost / text button** — text-only: text `--md-sys-color-{p}` (states `-hover/-active/-disabled` on
the accent), hover background `--md-sys-color-{p}-container-low`, active `--md-sys-color-{p}-container`.

**Destructive** — the same four recipes with `{p} = danger`. Never restyle a chrome button red by
hand; switch the palette.

## Form fields (text inputs, textareas, selects)

Fields live on the chrome palette (`neutral` below):

| Part | Role |
|---|---|
| field background | `--md-sys-color-neutral-surface-low` (recessed) or `--md-sys-color-neutral-surface` (flush) |
| border, rest | `--md-sys-color-neutral-outline-variant` |
| border, hover | `--md-sys-color-neutral-outline-variant-hover` |
| border, focus | `--md-sys-color-neutral-outline-active` — plus the focus ring (navigation.md) |
| value text | `--md-sys-color-neutral-on-surface` |
| **placeholder** | `--md-sys-color-neutral-placeholder` — the dedicated role; never fake it with opacity |
| label | `--md-sys-color-neutral-on-surface-variant`; floated/active label may take `--md-sys-color-primary` |
| helper text | `--md-sys-color-neutral-on-surface-variant` |
| error state | swap the border+helper to the intent palette: `--md-sys-color-danger-outline`, helper `--md-sys-color-danger` |
| disabled | bg `--md-sys-color-neutral-container-disabled` · border `--md-sys-color-neutral-outline-disabled` · text `--md-sys-color-neutral-on-surface-disabled` |

## Toggles — checkboxes, radios, switches

| Part | Role |
|---|---|
| unchecked box/track border | `--md-sys-color-neutral-outline` |
| unchecked track fill (switch) | `--md-sys-color-neutral-container` |
| **checked/selected fill** | `--md-sys-color-{p}` (accent) — mark/thumb `--md-sys-color-{p}-on-{p}` |
| checked hover/active | `--md-sys-color-{p}-hover` / `--md-sys-color-{p}-active` |
| disabled unchecked | border `--md-sys-color-neutral-outline-disabled` |
| disabled checked | fill `--md-sys-color-{p}-disabled` · mark `--md-sys-color-{p}-on-{p}-disabled` |

## Sliders & progress

Track: `--md-sys-color-neutral-container` (unfilled) · filled portion + thumb: `--md-sys-color-{p}` ·
thumb border on light fills: `--md-sys-color-{p}-on-{p}` · disabled: the `-disabled` pair.

## Text selection & focus (all interactive elements)

`::selection` background `--md-sys-color-{p}-container-high`, text `--md-sys-color-{p}-on-surface`. The
focus ring is one recipe app-wide: `outline-color: var(--md-sys-color-{p})` (see navigation.md; width/offset
come from the geometry tokens' `--md-sys-focus-ring-*`).
