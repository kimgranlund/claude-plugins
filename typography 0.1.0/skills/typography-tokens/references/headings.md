# Headings, display, and sub-headings

Display plus three heading-family voices (heading · sub-heading · kicker) do different jobs — pick
by voice, then size by step. Use the `.type-{voice}-{step}` utility class; the raw
`--type-{voice}-{step}-{prop}` vars are there when you need to compose (e.g. a single-line
override).

## The heading voices

| Voice | Font role | Job | Case |
|---|---|---|---|
| **display** | display | the single hero statement on a landing/marketing view — not a document heading | as-set (mixed) |
| **heading** | heading | real document headings: page title, section headings, card/dialog titles | as-set |
| **sub-heading** | heading | a wide-tracked label sitting ABOVE a heading (e.g. "PRICING") | uppercase (treatment) |
| **kicker** | mono | the smallest overline / metadata tag — mono, tracked | uppercase (treatment) |

`display` and `heading` carry separate font-family *roles* (`--font-display` for display,
`--font-heading` for heading) which may or may not resolve to the same physical typeface — the
hierarchy between them is size, weight, and leading either way, not a shared role. `quote` also
rides `--font-heading` (see prose.md). Whether `display` and `heading` should
be the *same* typeface or a deliberately contrasting pair is a font-selection decision, not a
scale decision — see [`references/font-selection.md`](font-selection.md).

## Mapping to an HTML heading ladder

There is no fixed voice-per-`<h1>`; map by size and importance. A common app mapping:

| Element | Class |
|---|---|
| hero / splash headline | `.type-display-lg` (or `-xl` for the biggest) |
| page title (h1) | `.type-heading-xl` |
| major section (h2) | `.type-heading-lg` |
| subsection (h3) | `.type-heading-md` |
| card / group title (h4) | `.type-heading-sm` |
| minor label (h5/h6) | `.type-heading-xs` |
| sub-heading above any of the above | `.type-sub-heading-sm` (or `-xs`) |
| kicker / metadata overline | `.type-kicker-xs` — a single-line overline: set `line-height: var(--type-kicker-{step}-line-single)` (it rides the `mono` role, so it has one; leading 1.0) |

Both display and heading typically run XS–XL, so sizes can overlap across the two voices — that's
expected: they're different voices, not the same size twice; pick by function first, then step.
Keep the ladder monotonic: don't skip so far that h2 and h3 look identical, and don't drop the
display voice into a document where an editorial heading belongs.

## The heading↔body pairing

Headings use `--font-heading`; body prose uses `--font-body` — the project's font-selection pass
pairs them deliberately (see `font-selection.md` for the contrast-vs-compatibility mechanics).
Never swap a heading onto the body font or vice versa; use the voice and its family follows.

Vertical rhythm between a heading and the paragraph under it comes from the heading step's
`--type-{voice}-{step}-para` (paragraph spacing) — set it as `margin-block-end`; don't invent a
gap. Headings are hierarchy by **size + weight** (the voice/step), never by color — a heading is
the same ink as body; dimming it for hierarchy is a color-layer concern, not a type one, and
usually the wrong call unless the heading is genuinely secondary.

## Don't

- Don't use `display` for long text — it's tuned for one short line, with tight-to-negative
  tracking and sub-1.0 leading at the largest steps. Multi-line big text is `heading`.
- Don't `text-transform: uppercase` a heading — `sub-heading`/`kicker` are already uppercase by
  treatment (the class does it); `heading`/`display` are intentionally not.
- Don't hand-set `letter-spacing`/`line-height` on a heading — `-tracking` and `-line` are tuned
  per step (sub-heading and kicker open their tracking as steps grow).
