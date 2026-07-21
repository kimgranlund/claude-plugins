# Responsive type, single-line vs multi-line, fonts

## Breakpoint modes — hierarchy-aware compression, not `clamp()`/`vw`

If a kit was exported with breakpoint modes, the `--md-sys-typescale-*` variables are **re-declared
inside `@media (min-width: …)` blocks** — one self-contained file per breakpoint mode (each bounded on
both ends except the narrowest, which stays open below). Because a `.md-sys-typescale-{voice}-{level}`
class reads the *variables*, the same class restyles automatically at each breakpoint.

The source engine's compression law (2026-07-10, current) is **hierarchy-aware, not a flat shrink**:
body-class voices (lead/body/body-mono/label/label-mono/tiny/tiny-mono, plus `ui-control`/`ui-widget`
since TKT-0008, 2026-07-16 — all small-size voices) stay frozen or nearly frozen across breakpoints,
while display-class type (display/headline/sub-heading/title) compresses harder the bigger it is — the
canonical factors are **5/6 at Tablet** and **2/3 at Mobile**, applied at the TOP of each voice's own
ramp and interpolated down toward the frozen body anchor. A kit may instead ship **Base-only** (a
single `:root`, no `@media` blocks) — a valid, deliberately fixed choice; don't "fix" either shape with
fluid type.

- **Do not** author fluid `clamp()` type or `vw`-based font sizes — if modes exist they are the
  responsive mechanism and land on the kit's exact quantized sizes at each breakpoint; if they don't,
  the kit is deliberately fixed.
- **Do not** hand-write `@media` font-size overrides — you'd either fight the exported blocks or
  override a deliberately-fixed scale.
- **Do not** expect display-class and body-class voices to compress by the same amount — that
  asymmetry (body barely moves, display compresses hard) is the intended hierarchy-aware behavior, not
  a bug.

## Single-line vs multi-line height

The BOX voices — **kicker, ui-control, and ui-widget** (changed 2026-07-16 — `label`, `body-mono`, and
`label-mono` used to be BOX and lost `-line-single` the same window) — carry TWO leadings per level:

- `--md-sys-typescale-{voice}-{level}-line` — multi-line leading (text that wraps: helper text,
  tooltips).
- `--md-sys-typescale-{voice}-{level}-line-single` — single-line leading = the size (leading 1.0), for
  text locked in a box (a kicker overline, a control, a widget) so the box height is exact and doesn't
  grow.

Every other voice — **display, headline, sub-heading, title, sub-title, lead, body, body-mono, label,
label-mono, tiny, tiny-mono** — has only `-line` (they're read as multi-line runs, even a
visually-single-line use like a table cell or a mono metadata chip). Reach for `-line-single` on a
kicker/ui-control/ui-widget element whose text must not wrap; note `sub-title`/`tiny`/`tiny-mono` ride
a box-default role (mono/ui) but are prose, so they have NO `-line-single` either.

## Paragraph spacing

`--md-sys-typescale-{voice}-{level}-para` is the derived paragraph rhythm, keyed on FLOW (box vs
prose), not on the display-vs-heading grouping:

- **BOX voices** (kicker · ui-control · ui-widget) use a flat **1.0× size** — `para == size` (their
  "paragraph" is their own box height).
- **PROSE voices** breathe at a reading factor from their role: display/heading-family (display ·
  headline · sub-heading · title) run lighter, body-class (lead · body · body-mono · label · label-mono
  · sub-title · tiny · tiny-mono) run at the body reading factor.

Use it as `margin-block-end` between blocks of that voice; it scales with the size, so vertical rhythm
stays proportional. Don't set paragraph margins by hand.

## Sibling weights — a heavier/lighter variant without hand-picking a number

Every voice auto-populates named weight variants around its own core weight — e.g.
`--md-sys-typescale-body-weight-medium`, `-body-weight-semi-bold` — exposed once per voice (not
per-level). Reach for the named sibling (`var(--md-sys-typescale-{voice}-weight-{slug})`) for a
"bolder" emphasis inside a voice instead of guessing a raw weight number; a voice with no siblings
configured simply has none to reach for. This is a SEPARATE channel from the per-level `-weight` (the
voice's own baseline weight at every size).

## Fonts & fallbacks

`--font-{display,heading,body,ui,mono}` name the five family roles; a voice may additionally carry its
own `--font-voice-{voice}` (a per-voice override off the shared role — byte-identical to the role font
when no override is configured). When a family name contains a digit or space (e.g. `'Inter Tight'`,
`'JetBrains Mono'`) the export **quotes** it — keep the quotes if you ever write a family literally (an
unquoted digit- or space-bearing family is dropped by strict parsers, notably WebKit/Safari). If the
project self-hosts the kit's fonts, the `@font-face` set ships alongside; otherwise a licensed or
system family renders where installed and a generic fallback covers the rest — either way you reference
the `--font-*` (or `--font-voice-*`) var, never the literal name.
