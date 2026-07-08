# Responsive type, single-line vs multi-line, fonts

## Breakpoint modes (not `clamp()`, not `vw`)

If a kit was exported with breakpoint modes, the `--type-*` variables are **re-declared inside
`@media (min-width: …)` blocks** — one block per breakpoint (a common web set steps at
768/992/1280/1540 above a mobile Base). Because a `.type-{voice}-{step}` class reads the
*variables*, the same class restyles automatically at each breakpoint: you write `.type-body-md`
once and it grows with the viewport.

- **Do not** author fluid `clamp()` type or `vw`-based font sizes — if modes exist they are the
  responsive mechanism and land on the kit's exact quantized sizes at each breakpoint (no
  fractional px); if they don't, the kit is deliberately fixed.
- **Do not** hand-write `@media` font-size overrides — you'd either fight the exported blocks or
  override a deliberately-fixed scale.
- A **Base-only export** (a single `:root`, no `@media` blocks) means the type is fixed across
  viewports — a valid choice; don't "fix" it with fluid type.

## Single-line vs multi-line height

The box voices — **ui, code, and kicker** (the ui/mono-role voices) — carry TWO leadings per step:

- `--type-{voice}-{step}-line` — multi-line leading (text that wraps: helper text, tooltips).
- `--type-{voice}-{step}-line-single` — single-line leading = the size (leading 1.0), for text
  locked in a box (buttons, inputs, cells, a kicker overline) so the box height is exact and
  doesn't grow.

The reading voices — **display, heading, sub-heading, lead, body, quote, caption, legal** — have
only `-line` (they're read as multi-line runs). Reach for `-line-single` on a ui/code/kicker
element whose text must not wrap; note `caption` and `legal` are prose (ui font, but no
`-line-single`).

## Paragraph spacing

`--type-{voice}-{step}-para` is the derived paragraph rhythm, by ROLE (not by the
display-vs-heading grouping). A typical export tunes it:

- **~0.7× size** for the display + heading roles (display · heading · sub-heading · quote).
- **~0.75× size** for the body/prose voices (body · lead · caption · legal).
- **1.0× size** for the ui/mono voices (ui · code · kicker) — `para == size`.

Use it as `margin-block-end` between blocks of that voice; it scales with the size, so vertical
rhythm stays proportional. Don't set paragraph margins by hand.

## Fonts & fallbacks

`--font-{display,heading,body,ui,mono}` name the families — which real typeface fills each role is
a font-selection decision (see [`references/font-selection.md`](font-selection.md)), not a
responsive one. When a family name contains a digit or space (`'Inter Tight'`, `'Source Serif 4'`,
`'JetBrains Mono'`) the export **quotes** it — keep the quotes if you ever write a family literally
(an unquoted digit- or space-bearing family is dropped by strict parsers, notably WebKit/Safari).
If the project self-hosts the kit's fonts, the `@font-face` set ships alongside; otherwise a
licensed or system family renders where installed and a generic fallback covers the rest — either
way you reference the `--font-*` var, never the literal name.
