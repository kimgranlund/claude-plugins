# Headings, display, and sub-headings

Display plus three heading-family voices (heading · sub-heading · kicker) do different jobs — pick by
voice, then size by level. Use the `.md-sys-typescale-{voice}-{level}` utility class; the raw
`--md-sys-typescale-*` vars are there when you need to compose (e.g. a single-line override).

## The heading voices

| Voice | Font | Job | Case |
|---|---|---|---|
| **display** | `--font-display` (Inter Tight, weight 700) | the single hero statement on a landing/marketing view — not a document heading | as-set (mixed) |
| **heading** | `--font-heading` (Inter Tight, weight 620) | real document headings: page title, section headings, card/dialog titles | as-set |
| **sub-heading** | `--font-heading` (Inter Tight, weight 600) | a wide-tracked label sitting ABOVE a heading (e.g. "PRICING") | UPPERCASE (treatment) |
| **kicker** | `--font-mono` (JetBrains Mono, weight 600) | the smallest overline / metadata tag — mono, tracked | UPPERCASE (treatment) |

In this ADIA kit `display` and `heading` share the **Inter Tight** face (a tight, low-contrast
grotesque) — the hierarchy between them is size, weight (700 vs 620), and leading, not a different
family. `quote` also rides `--font-heading`; see prose.md.

## Mapping to an HTML heading ladder

There is no fixed voice-per-`<h1>`; map by size and importance. A common app mapping:

| Element | Class |
|---|---|
| hero / splash headline | `.md-sys-typescale-display-lg` (or `-xl` for the biggest) |
| page title (h1) | `.md-sys-typescale-heading-xl` |
| major section (h2) | `.md-sys-typescale-heading-lg` |
| subsection (h3) | `.md-sys-typescale-heading-md` |
| card / group title (h4) | `.md-sys-typescale-heading-sm` |
| minor label (h5/h6) | `.md-sys-typescale-heading-xs` |
| sub-heading above any of the above | `.md-sys-typescale-sub-heading-sm` (or `-xs`) |
| kicker / metadata overline | `.md-sys-typescale-kicker-xs` — a single-line overline: set `line-height: var(--md-sys-typescale-kicker-{level}-line-single)` (it rides the `mono` role, so it has one; leading 1.0) |

Both display and heading run XS–XL, so sizes overlap (display-xs 36px = heading-lg 36px). That's
expected — they're different voices, not the same size twice; pick by function first, then level. Keep
the ladder monotonic: don't skip so far that h2 and h3 look identical, and don't drop the display voice
into a document where an editorial heading belongs.

## The heading↔body pairing

Headings use `--font-heading` (here Inter Tight); body prose uses `--font-body` (here Inter) — the
treatment pairs them deliberately (the tighter display cut over the neutral text cut). Never swap a
heading onto the body font or vice versa; use the voice and its family follows.

Vertical rhythm between a heading and the paragraph under it comes from the heading level's
`--md-sys-typescale-{voice}-{level}-para` (paragraph spacing) — set it as `margin-block-end`; don't
invent a gap. In this kit the heading roles' `-para` runs ~0.7× the size (e.g. `heading-md` 28px size /
20px para). Headings are hierarchy by **size + weight** (the voice/level), never by color — a heading
is the same ink as body (see material-design-color-tokens); don't dim it unless it's genuinely secondary.

## Don't

- Don't use `display` for long text — it's tuned for one short line, with **negative tracking and
  sub-1.0 leading** (display-xl is 88px on a 70px line). Multi-line big text is `heading`.
- Don't `text-transform: uppercase` a heading — `sub-heading`/`kicker` are already uppercase by
  treatment (the class does it); `heading`/`display` are intentionally not.
- Don't hand-set `letter-spacing`/`line-height` on a heading — `-tracking` and `-line` are tuned per
  level (sub-heading opens the tracking with the size: `sub-heading-xs` 1.8px → `sub-heading-xl` 3.7px).
