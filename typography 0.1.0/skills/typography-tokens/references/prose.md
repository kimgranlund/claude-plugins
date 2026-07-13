# Prose — body copy, lead, captions, legal, lists, links, code-in-text

Running text you *read* (as opposed to interface chrome you *operate*) is the **body** voice on
`--font-body` (see interface.md for the `label`/`body` split — it matters). Prose also has two
dedicated voices — **lead** and **tiny** — plus **sub-title**, a smaller alternate-typeface
heading that's still prose flow. Reach for the specific voice over a body step when one fits.

## The prose voices

| Text | Class | Why not a body step |
|---|---|---|
| standfirst / intro paragraph / pull-quote | `.type-lead-md` | **lead** — a larger, lighter opening paragraph, its own semantic token (also where a block quote belongs — there is no separate "quote" voice) |
| default body copy, paragraphs | `.type-body-md` | — |
| dense or secondary prose, fine print, legal, footnotes | `.type-body-sm` | body's own smallest step covers legal/fine-print — there is no separate "legal" voice |
| figure / image / table caption, small supporting text | `.type-tiny-md` | **tiny** — the ui font, but set as PROSE (wraps, reading leading) — a figure caption lives here, not on a dedicated "caption" voice |
| a smaller sub-heading in an alternate typeface | `.type-sub-title-md` | **sub-title** — mono-by-default face, but prose flow (a small heading, not a control label) |

Every voice rides the same **SM · MD · LG** ramp (`.type-{voice}-sm|md|lg`); default to `-md`.

## Paragraph rhythm

Space between paragraphs = the step's `--type-body-{step}-para` (paragraph spacing, derived at
~0.75× the size for prose) applied as `margin-block-end`. Line-height is
`--type-body-{step}-line` (multi-line leading, ~1.5×) and is already on the `.type-body-*` class;
don't override it. Never set your own `line-height` or paragraph `margin` — the rhythm is derived
so it stays proportional across breakpoints.

**Measure:** keep body line length ~60–75 characters for readability (a `max-inline-size` on the
prose container, e.g. `65ch`) — a layout concern the type tokens don't set, but the reason the
body sizes are tuned the way they are.

## Sub-title & tiny are PROSE, not chrome

`sub-title` and `tiny` render in the `mono`/`ui` font respectively, but they are **prose voices**:
they wrap, read as multi-line runs, and use `-line` + `-para`. They deliberately have **no
`-line-single`** (unlike the `label` voice itself). Use `tiny` for a figure/table caption and
`body-sm` for fine print — not `label`, which is chrome tuned to sit in a box.

## Lists, quotes, captions

- List items: the same `.type-body-{step}` as the surrounding prose; the marker inherits it.
- Blockquote / pull-quote: `.type-lead-{step}` — a larger, lighter paragraph reads as a set-apart
  quote; color/border are the color layer's. (For a quiet inline aside a body step is fine.)
- Caption / figure label: `.type-tiny-{step}` — the dedicated **tiny** voice (ui font, prose). If
  it's really interface *metadata* rather than a caption, `.type-label-sm` (interface.md).
- Fine print / legal / footnotes: `.type-body-sm`.

## Links in prose

Links keep the surrounding body voice/step — only the color changes (a separate color-token
concern: bare accent + underline). Don't bump the weight or size for a link; sizing stays with the
type layer, color doesn't.

## Inline code & code blocks

- Inline code: `.type-code-sm` (or match the surrounding step) — mono family, tabular figures,
  pegged to `body`'s own sizes.
- Code block: `.type-code-sm` / `-md` with `--type-code-{step}-line` for comfortable multi-line
  leading (the `code` voice carries both `-line` and `-line-single`). The type here is only the
  mono voice + step; surface/background color is a separate concern.

## Don't

- Don't use `label` for paragraphs or `body` for buttons — prose is `body`, chrome is `label`.
- Don't set prose `line-height`/`margin` by hand — `-line` and `-para` are derived.
- Don't use `-line-single` on `sub-title`/`tiny` — it doesn't exist; they wrap.
- Don't scale prose with `vw`/`clamp()` — see [`references/responsive.md`](responsive.md).
