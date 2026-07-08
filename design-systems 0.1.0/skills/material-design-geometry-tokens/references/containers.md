# Containers — insets, gaps, the space scale, borders

Container geometry is the space BETWEEN and AROUND components — a different tier from control-internal
geometry (controls.md). It's treatment-derived (scales with the kit's density), mode-independent, and
built from the M3 4dp grid. Reach for a SEMANTIC token (`--md-sys-inset-*`, `--md-sys-gap-*`) before a
raw `--md-sys-space-N`.

## Insets — padding INSIDE a container

`--md-sys-inset-{name}` — each is a named rung of the space ladder, sized to the container's scale.
ADIA's values:

| Token | Value | Use for |
|---|---|---|
| `--md-sys-inset-control-group` | 8px  | padding inside a toolbar / button group / segmented control |
| `--md-sys-inset-card`          | 16px | a card's inner padding |
| `--md-sys-inset-panel`         | 24px | a sidebar / panel / section body |
| `--md-sys-inset-dialog`        | 32px | a modal / dialog / sheet body |
| `--md-sys-inset-page`          | 48px | the page gutter / outermost content padding |

Pick by the container, not by eyeballing a number — a card is `--md-sys-inset-card` whether it's small
or large; the token already carries the right rhythm.

## Gaps — space BETWEEN siblings

`--md-sys-gap-{name}` — for `gap` on a flex/grid, or margins between stacked elements. ADIA's values:

| Token | Value | Use for |
|---|---|---|
| `--md-sys-gap-cluster`      | 8px  | inline siblings (a row of buttons, chips, inline meta) |
| `--md-sys-gap-stack-tight`  | 12px | tightly stacked items (a label + its field, list rows) |
| `--md-sys-gap-stack`        | 16px | the default vertical stack gap (form fields, list of cards) |
| `--md-sys-gap-stack-loose`  | 24px | loosely stacked groups (form sections) |
| `--md-sys-gap-grid`         | 16px | the gutter of a card / tile grid |
| `--md-sys-gap-section`      | 48px | rhythm between major page sections |

## The raw space ladder (escape hatch)

`--md-sys-space-{0…9}` is the underlying 4px-founded ladder. ADIA's rungs:
`0·4·8·12·16·24·32·48·64·96px`. The `--md-sys-inset-*` / `--md-sys-gap-*` tier is named rungs OF this
ladder (e.g. `inset-card` = `space-4` = 16px) — use the semantic name first; drop to a raw
`--md-sys-space-N` only for a one-off the tier doesn't cover (an unusual offset, a bespoke grid).

## Recipes

- **Card:** `padding: var(--md-sys-inset-card)`; radius `--md-sys-radius-md` (or `-lg`); border
  `--md-sys-border-thin` (color from the color skill); a grid of cards uses `gap: var(--md-sys-gap-grid)`.
- **Form:** field-to-field `gap: var(--md-sys-gap-stack)`; label-to-field `--md-sys-gap-stack-tight`;
  section-to-section `--md-sys-gap-stack-loose`.
- **Dialog:** body `padding: var(--md-sys-inset-dialog)`; actions row `gap: var(--md-sys-gap-cluster)`.
- **Page:** outer `padding-inline: var(--md-sys-inset-page)`; sections separated by `--md-sys-gap-section`.
- **Toolbar:** `padding: var(--md-sys-inset-control-group)`; items `gap: var(--md-sys-gap-cluster)`.

## Radius & borders

- Container corners use the **Material 3 shape scale** — `--md-sys-radius-none·xs·sm·md·lg·xl·full` =
  `0·4·8·12·16·28·9999px`: `--md-sys-radius-xs`/`-sm` (subtle), `--md-sys-radius-md` (default card, and
  what `--md-sys-radius-default` aliases here), `--md-sys-radius-lg`/`-xl` (prominent surface).
  `--md-sys-radius-none` = square; `--md-sys-radius-full` = pill / circle for round NON-controls.
- Borders / dividers: WIDTH is `--md-sys-border-thin` (1px, hairlines, default) or `--md-sys-border-thick`
  (2px, emphasis); the COLOR is the color skill's outline roles. Never a hardcoded `1px solid`.

## Don't

- Don't reach for `--md-sys-space-N` when a `--md-sys-inset-*` / `--md-sys-gap-*` names the job — the
  semantic tier is why you don't guess rungs.
- Don't pad a card with a control's `--md-sys-size-{step}-pad` — that's control-internal; a container uses
  `--md-sys-inset-*`.
- Don't hardcode `border-radius` / `padding` / `gap` in px.
