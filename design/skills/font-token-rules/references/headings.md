# Headings, display, and sub-headings

Display plus three heading-family voices (headline · sub-heading · title) do different jobs, plus
kicker for the smallest overline — pick by role, then size by step. Use the `.type-{voice}-{step}`
utility class; the raw `--type-{voice}-{step}-{prop}` vars are there when you need to compose
(e.g. a single-line override). Every voice is a 3-step ramp — `sm`/`md`/`lg` only.

## The heading voices

| Voice | Font role | Job | Case |
|---|---|---|---|
| **display** | display | the single hero statement on a landing/marketing view — not a document heading | as-set (mixed) |
| **headline** | heading | real document headings: page title, top-level section headings | as-set |
| **sub-heading** | heading | a bold, all-caps CONTEXT heading sitting ABOVE a list/grid (e.g. "LATEST STORIES") — not a subordinate h2 | uppercase (treatment) |
| **title** | heading | a smaller headline — card/dialog titles, lower-level section headings | as-set |
| **kicker** | mono | the smallest overline / metadata tag — mono, tracked, pegged to the same sizes as `label` | uppercase (treatment) |

`display` and the heading-family voices carry separate font-family *roles* (`--font-display` for
display, `--font-heading` for headline/sub-heading/title) which may or may not resolve to the same
physical typeface — the hierarchy between them is size, weight, and leading either way, not a
shared role. Whether `display` and `heading` should be the *same* typeface or a deliberately
contrasting pair is a font-selection decision, not a scale decision — see
[`references/font-selection.md`](font-selection.md).

## Mapping to an HTML heading ladder

There is no fixed voice-per-`<h1>`; map by size and importance. A common app mapping:

| Element | Class |
|---|---|
| hero / splash headline | `.type-display-lg` |
| page title (h1) | `.type-headline-lg` |
| major section (h2) | `.type-headline-md` |
| subsection (h3) | `.type-headline-sm` or `.type-title-lg` |
| card / group title (h4) | `.type-title-md` |
| minor label (h5/h6) | `.type-title-sm` |
| context heading above a list/grid | `.type-sub-heading-md` |
| kicker / metadata tag | `.type-kicker-md` — a single-line overline: use `--type-kicker-{step}-line-single` (it rides the `mono` role, so it has one; leading 1.0) |

Keep the ladder monotonic — don't skip so far that h2 and h3 look identical, and don't drop the
display voice into a document where an editorial heading belongs.

## The heading↔body pairing

Headline/sub-heading/title use `--font-heading`; body prose uses `--font-body` — the project's
font-selection pass pairs them deliberately (see `font-selection.md` for the
contrast-vs-compatibility mechanics). Never swap a heading onto the body font or vice versa; use
the voice and its family follows.

Vertical rhythm between a heading and the paragraph under it comes from the heading step's
`--type-{voice}-{step}-para` (paragraph spacing) — set it as `margin-block-end`; don't invent a
gap. Headings are hierarchy by **size + weight** (the voice/step), never by color — a heading is
the same ink as body; dimming it for hierarchy is a color-layer concern, not a type one, and
usually the wrong call unless the heading is genuinely secondary.

## Don't

- Don't use `display` for long text — it's tuned for one short line, with tight-to-negative
  tracking and sub-1.0 leading at the largest steps. Multi-line big text is `headline` or `title`.
- Don't `text-transform: uppercase` a heading — `sub-heading`/`kicker` are already uppercase by
  treatment (the class does it); `headline`/`title`/`display` are intentionally not.
- Don't hand-set `letter-spacing`/`line-height` on a heading — `-tracking` and `-line` are tuned
  per step (sub-heading and kicker run wide-tracked by design).
