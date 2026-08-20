# Responsive type, single-line vs multi-line, fonts

## Breakpoint modes (not `clamp()`, not `vw`)

If a kit was exported with breakpoint modes, the `--type-*` variables are **re-declared inside
`@media (min-width: …)` blocks** — one block per breakpoint; read the actual widths from the blocks
(Ultimate Tokens kits since 2026-07 always carry **Mobile ≤476 → Tablet 992 → Desktop 1280**,
synthesized automatically when the designer configured none; other producers choose their own
ladder). Because a `.type-{voice}-{step}` class reads the *variables*, the same class restyles
automatically at each breakpoint: you write `.type-body-md` once and it grows with the viewport.

The stepping is **hierarchy-aware**, not uniform: body-class text (body · body-mono · label ·
label-mono · tiny · tiny-mono) is **frozen** across breakpoints, `ui-control`/`ui-widget` are
effectively frozen too (their whole ramp already sits near `bodyBase`), headings compress
partially on smaller screens, and display-class type compresses fully (a 90px Desktop display
lands near 75 on Tablet, 60 on Mobile). So don't "fix" a heading that shrinks on mobile while body
text doesn't — that asymmetry IS the system.

- **Do not** author fluid `clamp()` type or `vw`-based font sizes — if modes exist they are the
  responsive mechanism and land on the kit's exact quantized sizes at each breakpoint (no
  fractional px); if they don't, the kit is deliberately fixed.
- **Do not** hand-write `@media` font-size overrides — you'd either fight the exported blocks or
  override a deliberately-fixed scale.
- In a moded export the `:root` block (no media query) is the mobile scale; each `@media` block
  steps up. A **Base-only export** (a single `:root`, no `@media` blocks) means the type is fixed
  across viewports — a valid producer choice (in a current Ultimate Tokens kit it means the export
  predates 2026-07; regenerating it adds the standard set) — don't "fix" it with fluid type.

## Single-line vs multi-line height

The genuinely interactive/box voices — **`ui-control`, `ui-widget`, and `kicker`** (re-split
2026-08-20, TKT-0008) — carry TWO leadings per step:

- `--type-{voice}-{step}-line` — multi-line leading (text that wraps: helper text, tooltips, prose).
- `--type-{voice}-{step}-line-single` — single-line leading = the size (leading 1.0), for text
  locked in a box (buttons, inputs, selects — `ui-control`; tags, badges, switches — `ui-widget`;
  a kicker overline) so the box height is exact and doesn't grow.

Every other voice — **display, headline, sub-heading, title, sub-title, lead, body, body-mono,
label, label-mono, tiny, tiny-mono** — has only `-line` (read as multi-line runs). This includes
`sub-title` and the mono-sibling voices, which ride the `mono` FONT role like the box voices do,
but are prose flow, not control text — and it includes `label` itself, which is explicitly
**static**: it names or describes interface elements but is never the operable control, so it
never gets `-line-single`. Reach for `-line-single` only on a `ui-control`/`ui-widget`/`kicker`
element whose text must not wrap.

## Paragraph spacing

`--type-{voice}-{step}-para` is the derived paragraph rhythm, by FLOW (not just by role). A
typical export tunes it:

- **~0.7× size** for the display + heading-family voices (display · headline · sub-heading · title).
- **~0.75× size** for the prose voices on the body/ui/mono roles (body · body-mono · label ·
  label-mono · lead · sub-title · tiny · tiny-mono).
- **1.0× size** for the three genuinely interactive box voices (`ui-control` · `ui-widget` ·
  `kicker`) — `para == size`.

Use it as `margin-block-end` between blocks of that voice; it scales with the size across
breakpoints, so vertical rhythm stays proportional. Don't set paragraph margins by hand.

## Fonts & fallbacks

`--font-{display,heading,body,ui,mono}` name the five shared families every voice resolves to —
which real typeface fills each role is a font-selection decision (see
[`references/font-selection.md`](font-selection.md)), not a responsive one. A voice the designer
escaped from its shared role font also gets its own dedicated custom property, one per voice. When
a family name contains a digit or space (`'Inter Tight'`, `'Source Serif 4'`, `'JetBrains Mono'`)
the export **quotes** it — keep the quotes if you ever write a family literally (an unquoted
digit- or space-bearing family is dropped by strict parsers, notably WebKit/Safari). If the
project self-hosts the kit's fonts, the `@font-face` set ships alongside; otherwise a licensed or
system family renders where installed and a generic fallback covers the rest — either way you
reference the `--font-*` var, never the literal name.
