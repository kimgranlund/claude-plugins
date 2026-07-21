# Color token semantics — what each `--md-sys-color-*` role MEANS

One line per token, or per group where tokens are graduated variants of one concept. `{p}` = the
palette (`primary · secondary · tertiary · quartery · accent-1…6 · neutral · info · success · warning
· danger`) — every palette carries the SAME 59 roles; only `neutral` is chrome (structure), the rest
carry MEANING (brand or intent). For the full binding grammar, pairing law, and worked recipes, see
`material-color-facts` — this file only answers "what does this token mean."

## The accent core

| Token | Meaning | Reach for it when… |
|---|---|---|
| `{p}` (bare) | The palette's own identity color — its one true accent. | You need the thing that says "this is `{p}`" — a brand mark, a CTA fill, an active indicator, a bare accent text/icon. |
| `{p}-hover` / `-active` / `-disabled` | The accent's own interaction states — real, tuned tokens, not opacity tricks. | Any interactive element built on the bare accent (a filled button, a toggle's checked fill, a slider thumb) needs its hover/press/disabled look. |

## The accent tonal variants — two DIFFERENT axes, don't conflate them

| Group | Meaning | Reach for it when… |
|---|---|---|
| `{p}-dim` → `{p}-bright` | *Mode-consistent* literal lightness — dim is literally darker, bright literally lighter, in BOTH light and dark scheme. | You mean actual light/shading, not stacking order: a gradient's two ends, a pressed large-surface tint, a decorative duotone. |
| `{p}-low` → `{p}-high` | *Mode-mirrored* emphasis — low always reads as LESS emphasis, high as MORE, in both schemes (they flip stops to hold that relationship). | You mean a *feeling* (muted vs. highlighted), not a direction: a data-viz series' muted vs. spotlighted state, a secondary vs. primary accent line, an active tick vs. inactive ticks. |

Rule of thumb: reaching for a *feeling* → low/high; reaching for a *direction* → dim/bright.

## Text on a filled accent vs. text on a surface

| Token | Meaning | Reach for it when… |
|---|---|---|
| `{p}-on-{p}` (+ `-hover`/`-active`/`-disabled`) | The one legal ink for text/icons sitting ON a `{p}`-filled background (a filled button's label, a checked toggle's mark). | Anything painted directly on the bare `{p}` fill — never pair `{p}` bg with a generic `on-surface` ink. |
| `{p}-on-{p}-variant` | The quieter, secondary ink for text on a `{p}`-filled background — one step down from `-on-{p}`, and (unlike it) carries NO hover/active/disabled state family of its own. | A filled element's secondary line — a filled button's helper text or sub-label, a filled banner's supporting line under its `-on-{p}` title. |
| `{p}-on-surface` | `{p}`-tinted text/icon for use on a NEUTRAL surface (not on the accent fill itself) — e.g. a tonal button's label, a selected-nav-item's label. | Text needs to READ as "`{p}`" while sitting on a card/pane/list, not on the accent fill. |

## The shared text hierarchy (chrome — `neutral`, but every palette has the pair)

| Group | Meaning | Reach for it when… |
|---|---|---|
| `on-surface` | The default, full-emphasis ink — body copy, headings, values. | Anything that's the primary thing being read; the default choice. |
| `on-surface-variant` (+ `-hover`/`-active`/`-disabled`, ADIA extension) | Secondary ink — one step quieter. | Captions, metadata, timestamps, helper text, inactive labels — never invent an intermediate gray instead. |
| `on-surface-hover` / `-active` / `-disabled` | Ink states for interactive text/labels (a text row, a link-like label). | A text element itself is the interactive target (not just its background). |
| `placeholder` | The ONE dedicated placeholder ink. | Form-field placeholder text only — never fake it with opacity on `on-surface-variant`. |

## Outline & border

| Group | Meaning | Reach for it when… |
|---|---|---|
| `outline-variant` (+ hover/active/disabled, ADIA extension) | The default, quiet border — hairline dividers, subtle card edges. | The default border choice; most dividers and card outlines. |
| `outline` (+ hover/active/disabled) | The stronger, more visible border. | Field borders, emphasized rules, an outlined button's stroke, a focused/active border state. |

Border WIDTH is a geometry token (`--md-sys-border-thin/-thick`); these roles only color it.

## Container — the translucent "grouped content" tint

| Token | Meaning | Reach for it when… |
|---|---|---|
| `{p}-container` (+ `-low`/`-high`, + hover/active/disabled) | A 500-stop TRANSLUCENT tint of `{p}` — composes correctly on any surface tier because it tints whatever it sits on. | Grouped-content fills INSIDE a surface — chips, a selected list row, a tonal/soft button, a table row's hover wash — never for large structural elevation (that's the surface ladder below). Text on a container is that palette's `on-surface`, never an `on-container` (no such role exists). |

## Surface elevation — TWO ladders, different physics (the classic mix-up)

| Group | Meaning | Reach for it when… |
|---|---|---|
| `neutral-surface-lowest` → `-lower` → `-low` → *(surface)* → `-high` → `-higher` → `-highest` | *Relational* stacking order — these flip stops across light/dark so **low always reads recessed and high always reads raised in BOTH schemes.** This is the ladder for UI STRUCTURE. | Picking a tier by z-order: recessed wells (inputs, code blocks, empty states) at `-low`/`-lower`/`-lowest`; raised chrome (cards, panes, popovers) at `-high`; stickier chrome (sticky headers, dropdowns) at `-higher`; the topmost layer (modals, dialogs, command palettes) at `-highest`. |
| `neutral-surface-dimmest` → `-dimmer` → `-dim` → *(surface)* → `-bright` → `-brighter` → `-brightest` | *Literal* lightness — mode-CONSISTENT (dimmest is darker in both schemes, no flip). | You mean actual light, not stacking order: a dimmed inactive pane, a spotlight/hero band, a photography-adjacent backdrop. Never use this ladder to express z-order — that's the lowest/highest ladder above. |
| `background` | The single deepest layer — the page/app background under everything. | The outermost canvas, before any surface tier. |
| `surface` | The default working surface — the un-elevated, un-recessed baseline every other tier is relative to. | The main pane/list body with no special elevation. |

## Scrim — the seven-strength overlay ladder

| Group | Meaning | Reach for it when… |
|---|---|---|
| `neutral-scrim-weakest` → `-weaker` → `-weak` → `scrim` → `-strong` → `-stronger` → `-strongest` | A translucent alpha ladder (mode-flat) for anything sitting BETWEEN the page and a floating layer. | Pick by job, weakest→strongest: a hover wash/image-darkening-for-legibility at weak/scrim, a drawer backdrop (content stays glanceable) at `scrim`, a modal/dialog backdrop at `-strong`, a full blocking overlay (loading a whole view) at `-stronger`/`-strongest`. Scrims stack WITH the surface ladder: backdrop = scrim, the floating panel on top = `-surface-highest`. An intent/brand palette carries the SAME suffixes for a tinted overlay (a danger-zone scrim). |

## Inverse surface — the deliberately opposite-scheme pair

| Token | Meaning | Reach for it when… |
|---|---|---|
| `neutral-inverse-surface` + `neutral-inverse-on-surface` | The one pair that's deliberately the OPPOSITE scheme from the rest of the page — guaranteed contrast against anything. | Small floating chrome that must read regardless of what's under it: tooltips, toasts/snackbars. Never for a large region — to flip a whole SECTION's scheme, set `color-scheme` on it instead, don't reach for inverse-surface as a section background. |

## Intent palettes — a concept, not a token

`info · success · warning · danger` are not extra roles — they're the SAME 59-role shape as any other
palette, chosen instead of `primary`/`neutral` specifically because the UI needs to communicate a
state, a result, or a risk. Reach for one only when the UI genuinely MEANS it (never as decoration);
`danger` doubles as the destructive-action palette (delete buttons, error text, a full-pane error
accent).
