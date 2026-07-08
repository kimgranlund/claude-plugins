# Prose — body copy, lead, quotes, captions, legal, lists, links, code-in-text

Running text you *read* (as opposed to interface chrome you *operate*) is the **body** voice on
`--font-body` (see interface.md for the `ui`/`body` split — it matters). Prose also has four
dedicated **editorial** voices — reach for the specific voice over a body step when one fits.

## The prose voices

| Text | Class | Why not a body step |
|---|---|---|
| standfirst / intro paragraph | `.type-lead-md` | **lead** — a larger, lighter opening paragraph, its own semantic token |
| default body copy, paragraphs | `.type-body-md` | — |
| dense or secondary prose | `.type-body-sm` | — |
| a block quote / pull-quote | `.type-quote-md` | **quote** rides the *heading face* (`--font-heading`) for presence |
| figure / image / table caption | `.type-caption-md` | **caption** — the ui font (`--font-ui`), but set as PROSE (wraps, reading leading) |
| fine print, legal, footnotes | `.type-legal-md` | **legal** — the smallest reading voice, ui font + prose |

The four editorial voices ride the lean **SM · MD · LG** ramp (`.type-{voice}-sm|md|lg`); default
to `-md`.

## Paragraph rhythm

Space between paragraphs = the step's `--type-body-{step}-para` (paragraph spacing, derived at
~0.75× the size for prose) applied as `margin-block-end`. Line-height is
`--type-body-{step}-line` (multi-line leading, ~1.5×) and is already on the `.type-body-*` class;
don't override it. Never set your own `line-height` or paragraph `margin` — the rhythm is derived
so it stays proportional across breakpoints.

**Measure:** keep body line length ~60–75 characters for readability (a `max-inline-size` on the
prose container, e.g. `65ch`) — a layout concern the type tokens don't set, but the reason the body
sizes are tuned the way they are.

## Caption & legal are PROSE, not chrome

`caption` and `legal` render in `--font-ui`, but they are **prose voices**: they wrap, read as
multi-line runs, and use `-line` + `-para`. They deliberately have **no `-line-single`** (unlike
the `ui` voice itself). Use `caption` for a figure/table caption and `legal` for fine print — not
`ui-xs`, which is chrome tuned to sit in a box.

## Lists, blockquotes, captions

- List items: the same `.type-body-{step}` as the surrounding prose; the marker inherits it.
- Blockquote / pull-quote: `.type-quote-{step}` — the dedicated **quote** voice (the heading face,
  its own leading). (For a quiet inline aside a body step is fine, but a set-apart quote is
  `quote`.)
- Caption / figure label: `.type-caption-{step}` — the dedicated **caption** voice.
- Fine print / legal / footnotes: `.type-legal-{step}`.

## Links in prose

Links keep the surrounding body voice/step — only the color changes (a separate color-token
concern). Don't bump the weight or size for a link; sizing stays with the type layer, color
doesn't.

## Inline code & code blocks

- Inline code: `.type-code-sm` (or match the surrounding step) — mono family, tabular figures.
- Code block: `.type-code-sm` / `-md` with `--type-code-{step}-line` for comfortable multi-line
  leading (the `code` voice carries both `-line` and `-line-single`). The type here is only the
  mono voice + step; surface/background color is a separate concern.

## Don't

- Don't use `ui` for paragraphs or `body` for buttons — prose is `body`, chrome is `ui`.
- Don't set prose `line-height`/`margin` by hand — `-line` and `-para` are derived.
- Don't use `-line-single` on `caption`/`legal` — it doesn't exist; they wrap.
- Don't scale prose with `vw`/`clamp()` — see [`references/responsive.md`](responsive.md).
