# Prose — body copy, lead, quotes, captions, legal, lists, links, code-in-text

Running text you *read* (as opposed to interface chrome you *operate*) is the **body** voice on
`--font-body` (Inter). Interface text is `ui` — see interface.md; the split matters. Prose also has
four dedicated **editorial** voices — reach for the specific voice over a body level when one fits.

## The prose voices

| Text | Class | Why not a body level |
|---|---|---|
| standfirst / intro paragraph | `.md-sys-typescale-lead-md` | **lead** — a larger, lighter opening paragraph (Inter, weight 400), its own semantic token |
| default body copy, paragraphs | `.md-sys-typescale-body-md` | — (Inter, weight 440; `md` is 16px on a 24px line — the kit's bodyBase 16) |
| dense or secondary prose | `.md-sys-typescale-body-sm` | — (13px / 20px) |
| a block quote / pull-quote | `.md-sys-typescale-quote-md` | **quote** rides the *heading face* (`--font-heading`, Inter Tight, weight 450) |
| figure / image / table caption | `.md-sys-typescale-caption-md` | **caption** — the ui font (`--font-ui`, Inter) but set as PROSE (wraps, reading leading) |
| fine print, legal, footnotes | `.md-sys-typescale-legal-md` | **legal** — the smallest reading voice, ui font + prose |

The four editorial voices ride the lean **SM · MD · LG** ramp (`.md-sys-typescale-{voice}-sm|md|lg`);
default to `-md`.

## Paragraph rhythm

Space between paragraphs = the level's `--md-sys-typescale-body-{level}-para` (paragraph spacing,
derived at ~0.75× the size for prose — `body-md` is 16px size / 12px para) applied as
`margin-block-end`. Line-height is `--md-sys-typescale-body-{level}-line` (multi-line leading, ~1.5× —
`body-md` 24px) and is already on the `.md-sys-typescale-body-*` class; don't override it. Never set
your own `line-height` or paragraph `margin` — the rhythm is derived so it stays proportional.

**Measure:** keep body line length ~60–75 characters for readability (a `max-inline-size` on the prose
container, e.g. `65ch`) — a layout concern the type tokens don't set, but the reason the body sizes are
tuned the way they are.

## Caption & legal are PROSE, not chrome

`caption` and `legal` render in `--font-ui` (Inter), but they are **prose voices**: they wrap, read as
multi-line runs, and use `-line` + `-para`. They deliberately have **no `-line-single`** (unlike the
`ui` voice itself). Use `caption` for a figure/table caption and `legal` for fine print — not `ui-xs`,
which is chrome tuned to sit in a box.

## Lists, blockquotes, captions

- List items: the same `.md-sys-typescale-body-{level}` as the surrounding prose; the marker inherits it.
- Blockquote / pull-quote: `.md-sys-typescale-quote-{level}` — the dedicated **quote** voice (the
  heading face, its own leading); the color/border come from material-design-color-tokens. (For a quiet
  inline aside a body level is fine, but a set-apart quote is `quote`.)
- Caption / figure label: `.md-sys-typescale-caption-{level}` — the dedicated **caption** voice.
- Fine print / legal / footnotes: `.md-sys-typescale-legal-{level}`.

## Links in prose

Links keep the surrounding body voice/level — only the COLOR changes (material-design-color-tokens:
bare accent + underline). Don't bump the weight or size for a link; that's the color layer's job.

## Inline code & code blocks

- Inline code: `.md-sys-typescale-code-sm` (or match the surrounding level) — mono family (JetBrains
  Mono), tabular figures.
- Code block: `.md-sys-typescale-code-sm` / `-md` with `--md-sys-typescale-code-{level}-line` for
  comfortable multi-line leading (the `code` voice carries both `-line` and `-line-single`). The
  surface/color come from material-design-color-tokens; the type here is only the mono voice + level.

## Don't

- Don't use `ui` for paragraphs or `body` for buttons — prose is `body`, chrome is `ui`.
- Don't set prose `line-height`/`margin` by hand — `-line` and `-para` are derived.
- Don't use `-line-single` on `caption`/`legal` — it doesn't exist; they wrap.
- Don't scale prose with `vw`/`clamp()` — see responsive.md.
