# Prose — body copy, lead, tiny fine-print, lists, links, code-in-text

Running text you *read* (as opposed to interface chrome you *operate*) is the **body** voice on the
`body` font role. Interface text is `label` — see interface.md; the split matters. Prose also has two
dedicated smaller-register voices — reach for the specific voice over a body level when one fits.

## The prose voices

| Text | Class | Why not a body level |
|---|---|---|
| standfirst / intro paragraph | `.md-sys-typescale-lead-md` | **lead** — a larger, lighter opening paragraph, its own semantic token — a former "quote" register folds in here (both are large, single-emphasis body-adjacent text) |
| default body copy, paragraphs | `.md-sys-typescale-body-md` | — the kit's `bodyBase` anchor |
| dense or secondary prose | `.md-sys-typescale-body-sm` | — one level down |
| a small heading in an alternate face | `.md-sys-typescale-sub-title-md` | **sub-title** — see headings.md; it's a heading-family voice, not prose in this table's sense, but rides the mono FONT |
| fine print, footnotes, disclaimers | `.md-sys-typescale-tiny-md` | **tiny** — the smallest READING voice; a former "caption"/"legal" register folds in here |
| fine print in the mono face | `.md-sys-typescale-tiny-mono-md` | **tiny-mono** — same size register as `tiny`, dressed in the mono font |

Every voice now rides the SAME **SM · MD · LG** ramp (`.md-sys-typescale-{voice}-sm|md|lg`); default to
`-md`.

## Paragraph rhythm

Space between paragraphs = the level's `--md-sys-typescale-body-{level}-para` (paragraph spacing,
derived at the body/reading factor) applied as `margin-block-end`. Line-height is
`--md-sys-typescale-body-{level}-line` (multi-line leading) and is already on the
`.md-sys-typescale-body-*` class; don't override it. Never set your own `line-height` or paragraph
`margin` — the rhythm is derived so it stays proportional.

**Measure:** keep body line length ~60–75 characters for readability (a `max-inline-size` on the prose
container, e.g. `65ch`) — a layout concern the type tokens don't set, but the reason the body sizes are
tuned the way they are.

## Tiny/tiny-mono are PROSE, not chrome

`tiny` and `tiny-mono` render in the `ui`/`mono` font roles respectively, but they are **prose voices**:
they wrap, read as multi-line runs, and use `-line` + `-para`. They deliberately have **no
`-line-single`** (unlike the box voices — label, body-mono, label-mono, kicker). Use `tiny` for fine
print/footnotes and `tiny-mono` when that fine print needs the mono face (a legal ID, a tabular
disclaimer figure) — not `label`/`kicker`, which are chrome tuned to sit in a box.

## Lists, blockquotes, fine print

- List items: the same `.md-sys-typescale-body-{level}` as the surrounding prose; the marker inherits it.
- Blockquote / pull-quote / standfirst: `.md-sys-typescale-lead-{level}` — the dedicated **lead** voice
  (its own weight/tracking, own leading); the color/border come from material-design-color-tokens. (For
  a quiet inline aside a body level is fine, but a set-apart intro/pull passage is `lead`.)
- Fine print / footnotes / disclaimers: `.md-sys-typescale-tiny-{level}` (or `tiny-mono` for a mono
  register).

## Links in prose

Links keep the surrounding body voice/level — only the COLOR changes (material-design-color-tokens:
bare accent + underline). Don't bump the weight or size for a link; that's the color layer's job.

## Inline code & code blocks

- Inline code: `.md-sys-typescale-body-mono-sm` (or match the surrounding level) — the mono-role sibling
  of body, tabular figures, a BOX voice (has `-line-single`, though inline code sits inside prose flow so
  `-line` is usually the right choice there — see interface.md for the box-voice mechanics).
- Code block: `.md-sys-typescale-body-mono-md` with `-line` for comfortable multi-line leading. The
  surface/color come from material-design-color-tokens; the type here is only the mono-role voice +
  level.

## Don't

- Don't use `label` for paragraphs or `body` for buttons — prose is `body`/`lead`/`tiny`, chrome is
  `label`/`kicker`.
- Don't set prose `line-height`/`margin` by hand — `-line` and `-para` are derived.
- Don't use `-line-single` on `tiny`/`tiny-mono`/`sub-title` — it doesn't exist; they wrap.
- Don't scale prose with `vw`/`clamp()` — see responsive.md.
