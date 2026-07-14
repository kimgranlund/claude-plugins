# Headings, display, sub-headings, titles, sub-titles

Display plus four heading-family voices (headline · sub-heading · title · sub-title) do different jobs
— pick by voice, then size by level (SM/MD/LG — every voice rides the same three levels now). Use the
`.md-sys-typescale-{voice}-{level}` utility class; the raw `--md-sys-typescale-*` vars are there when
you need to compose (e.g. a single-line override).

## The heading-family voices

| Voice | Font role | Job | Case |
|---|---|---|---|
| **display** | display | the single hero statement on a landing/marketing view — not a document heading | title/sentence (UPPERCASE only in an earned "loud" treatment) |
| **headline** | heading | real document headings: page title, section headings, card/dialog titles | sentence |
| **sub-heading** | heading | a wide-tracked label sitting ABOVE a headline (e.g. "PRICING") | UPPERCASE (treatment) |
| **title** | heading | a smaller headline — a card/dialog title one rung below `headline` | sentence |
| **sub-title** | mono, as PROSE | a small heading in an alternate face — a section marker, not a control label | sentence |

`display` and `headline`/`title` typically share the same family (the treatment's `heading` role) — the
hierarchy between them is size, weight, and leading, not a different family. `sub-title` deliberately
rides the MONO role as its face while staying a prose voice (no `-line-single`) — it's a small
alternate-face heading, not mono metadata (that's `kicker`/`label-mono`; see interface.md).

## Mapping to an HTML heading ladder

There is no fixed voice-per-`<h1>`; map by size and importance, using the level (SM/MD/LG) for rank
within a voice:

| Element | Class |
|---|---|
| hero / splash headline | `.md-sys-typescale-display-lg` |
| page title (h1) | `.md-sys-typescale-headline-lg` |
| major section (h2) | `.md-sys-typescale-headline-md` |
| subsection (h3) | `.md-sys-typescale-title-md` (or `.md-sys-typescale-headline-sm` if the kit is flatter) |
| card / group title (h4) | `.md-sys-typescale-title-sm` |
| minor label / small heading (h5/h6) | `.md-sys-typescale-sub-title-md` |
| sub-heading above any of the above | `.md-sys-typescale-sub-heading-sm` (or `-md`) |
| kicker / metadata overline | `.md-sys-typescale-kicker-sm` — a single-line overline: use `-line-single` (it's a BOX voice, leading 1.0) |

Since every voice now shares the same SM/MD/LG level set, sizes across voices at the SAME level differ
by DESIGN — `display-md` and `headline-md` are different literal px values (each voice has its own
fixed size table), not the same number reused. Pick by function first, then by level for rank within
that voice; don't hunt across voices for a specific pixel value.

## The heading↔body pairing

Headings use the `heading` font role; body prose uses `body` — the treatment pairs them deliberately.
Never swap a heading onto the body font or vice versa; use the voice and its family follows (or, for a
one-off exception, the per-voice font override — `--font-voice-{voice}` — rather than hardcoding a
literal family).

Vertical rhythm between a heading and the paragraph under it comes from the heading level's
`--md-sys-typescale-{voice}-{level}-para` (paragraph spacing) — set it as `margin-block-end`; don't
invent a gap. Headline/sub-heading/title/display's `-para` runs at the display/heading reading factor
(lighter than body's own); headings are hierarchy by **size + weight** (the voice/level), never by
color — a heading is the same ink as body (see material-design-color-tokens); don't dim it unless it's
genuinely secondary.

## Don't

- Don't use `display` for long text — it's tuned for one short line, with **negative tracking and
  sub-1.0 leading**. Multi-line big text is `headline`.
- Don't `text-transform: uppercase` a heading — `sub-heading`/`kicker` are already uppercase by
  treatment (the class does it); `headline`/`title`/`display` are intentionally not (except the one
  treatment that earns an ALL-CAPS display).
- Don't hand-set `letter-spacing`/`line-height` on a heading — `-tracking` and `-line` are tuned per
  level (sub-heading's tracking opens with the size).
- Don't invent a fourth heading-family voice for "one size smaller than title" — reach for `sub-title`
  (a genuinely different, mono-faced register) or drop to a `label`/`sub-heading` treatment instead of
  stretching `title` past what it's for.
