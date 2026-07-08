# Text — hierarchy, emphasis, and the accent variants

Prose and labels live on the chrome palette (`neutral` here). The whole hierarchy is TWO ink roles
plus their states — resist inventing intermediate grays.

## The hierarchy

| Text | Role |
|---|---|
| default body, headings, values — **the default is full ink** | `--md-sys-color-neutral-on-surface` |
| secondary: captions, meta, timestamps, helper text, inactive labels | `--md-sys-color-neutral-on-surface-variant` |
| placeholder (form fields only) | `--md-sys-color-neutral-placeholder` |
| disabled text anywhere | `--md-sys-color-neutral-on-surface-disabled` (secondary: `-on-surface-variant-disabled`) |
| interactive text hover/pressed (a text row, a link-like label) | `-on-surface-hover` / `-on-surface-active` (variant: `-on-surface-variant-hover` / `-active`) |
| text on the inverse surface (tooltips, toasts) | `--md-sys-color-neutral-inverse-on-surface` |

M3 ships `on-surface` and `on-surface-variant`; the `-hover/-active/-disabled` ink states are
nonoun's extension — use them instead of dimming with opacity.

Headings are hierarchy-by-typography (size/weight from the typography tokens), not by color — a
heading is `-on-surface` like body. Don't dim headings to `-variant` unless they're genuinely
secondary.

## Accent-colored text

Links, emphasized numbers, active labels: `--md-sys-color-{p}` (the bare accent) — it doubles as a
text color on surface tiers. States: `-hover`/`-active`. In prose, underline links; color alone is
not an affordance.

## The `-dim / -bright / -low / -high` accent variants

Four **tonal variants of the accent itself** (not text-hierarchy roles — that's `-on-surface*`), a
nonoun extension M3 has no equivalent for:

- **`--md-sys-color-{p}-dim` / `--md-sys-color-{p}-bright`** — *mode-consistent*: dim is literally
  darker, bright literally lighter, in both schemes. Use for literal shading: a gradient's two ends,
  a pressed large-surface tint, a decorative duotone.
- **`--md-sys-color-{p}-low` / `--md-sys-color-{p}-high`** — *mode-mirrored*: low reads as LESS
  emphasis and high as MORE emphasis in both schemes (they flip stops across modes so the
  relationship holds). Use for emphasis ladders: a data-viz series' muted vs highlighted state, a
  secondary vs primary accent line, an active tick vs inactive ticks.

Rule of thumb: reaching for a *feeling* (more/less emphasis) → `-low/-high`; reaching for a
*direction* (darker/lighter) → `-dim/-bright`.

## Code & pre

Inline code and code blocks sit on a recessed tier: bg `--md-sys-color-neutral-surface-low` (block)
or `--md-sys-color-neutral-container-low` (inline chip), text `--md-sys-color-neutral-on-surface`;
syntax accents may borrow supporting palettes' bare accents (`--md-sys-color-secondary`,
`--md-sys-color-tertiary`) — never intent palettes.

## Never

- No `opacity` on text for hierarchy (breaks on tinted surfaces; the variant/disabled roles exist).
- No raw stops (`--md-sys-color-neutral-700`) as "custom gray" — if `-on-surface-variant` feels
  wrong, the kit needs tuning, not a bypass.
- No hand-flipped dark-mode text colors — `light-dark()` already did it.
