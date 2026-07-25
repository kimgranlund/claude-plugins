---
name: font-token-rules
description: >-
  Use when setting the TYPE of any UI on the default `--type-*` token grammar (not Material's
  `--md-sys-typescale-*`) — font/size/weight/leading/tracking for a heading, body, label, button,
  caption, code, or kicker ("what type token for this", "which voice/step for this text", "size
  this heading"). Eleven-voice scale: bind `--type-*`/`--font-*`, pick VOICE by job and STEP by
  rank, apply the baked leading/rhythm, pick a concrete font per family slot. Never hardcode a
  px size, line-height, tracking, or font family. NOT for Material's typescale
  (material-type-facts); NOT for a no-token typography question (lettering-facts); NOT for
  building/placing a component (make-component).
disable-model-invocation: false
user-invocable: false
---

# Typography tokens (default `--type-*` grammar)

An Ultimate-Tokens-style export gives eleven named **voices**, each a fixed **SM · MD · LG** ramp
of **steps**, as CSS custom properties. Your job is never to pick a px size or a font stack — it is
to pick the right **voice** (the text's role) and **step** (its size within that role), then — only
where a concrete font must be named — the right typeface for that voice's job.

This is the generic twin of `material-type-facts`: same `{voice}-{step}-{prop}`
grammar, no Material-specific namespace or bound font choices — the prefix after `--` is whatever
the project's export declares. (The Material sibling documents its kit's shipped export, which
predates the 2026-07 taxonomy rewrite — its voice list matches that file, not this table, until
the kit regenerates.)

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file defining `--font-*` families and the type-scale variables
   (often `type.css` / `tokens.css`; a DTCG `*.tokens.json` and utility classes may sit beside
   it). **The scale prefix is configurable:** the default is `--type-*` (class `.type-*`), but a
   Material scheme exports `--md-sys-typescale-*` (that binding lives in
   `material-type-facts`, not here) and a branded kit may export
   `--{brand}-type-*` — **read the actual prefix from the file**; the grammar after it
   (`-{voice}-{step}-{prop}`) is identical either way, and font families stay `--font-*`
   regardless. If no export exists, stop and ask — do not hardcode sizes.
2. **Read the fonts.** Five family roles: `--font-display`, `--font-heading`, `--font-body`,
   `--font-ui`, `--font-mono`. Every voice resolves to one of these — you never name a family
   directly, you use the voice's `--font-*` var (the utility classes already do this). A voice the
   designer escaped from its shared role font also gets its own dedicated `--font-*` var, one per
   voice. Choosing *which* real typeface fills each role is a separate judgment call — see
   [`references/font-selection.md`](references/font-selection.md).
3. **Know the grammar.** `--type-{voice}-{step}-{prop}` where prop ∈
   `size · line · tracking · weight · para` (+ `line-single` on the box voices — label, code,
   kicker). Prefer the ready-made utility class `.type-{voice}-{step}` (it wires
   family+size+line+tracking+weight in one) over composing the vars by hand.

## Two axes — voice (function) × step (hierarchy depth)

A **voice is a ROLE** — the text's *function*, carrying its character (weight, tracking, leading,
case, font) across every size. A **step is a LEVEL** — the element's rank in the hierarchy, from
which the size is *derived*. They're independent: the same voice appears at many steps, and the
same step hosts different voices. **Pick the voice by function and the step by hierarchy depth —
never a voice to hit a size, never a step to hit a px.** Choosing `display` because you want big
text, or a larger step because you want line-height 26, is the mistake this split exists to
prevent.

## The eleven voices — pick by the text's FUNCTION

Every voice is a uniform 3-step **SM–LG** ramp — sizes are a fixed, hand-authored table, not a
modular scale, and identical across every treatment (only font/weight/tracking/leading/case vary
by treatment).

| Voice | Font role | Use for |
|---|---|---|
| **display** | display | hero/marketing headlines, the one big statement on a view |
| **headline** | heading | real document headings: page title, top-level sections (h1–h3), card & dialog titles |
| **sub-heading** | heading | a bold, all-caps CONTEXT heading above a list/grid (e.g. "LATEST STORIES") — wide-tracked |
| **title** | heading | a smaller headline — lower-level section headings, card/dialog titles |
| **sub-title** | mono (prose) | a smaller sub-heading in an alternate typeface — still prose flow, not a control label |
| **lead** | body | the standfirst / intro paragraph, or a block quote / pull-quote — larger than body |
| **body** | body | running prose, paragraphs, long-form reading, and fine-print/legal (body's own smallest step) |
| **code** | mono | code, tabular figures, keyboard shortcuts, technical values — pegged to body's own sizes |
| **label** | ui | interface text: buttons, labels, inputs, menus, table cells, badges |
| **kicker** | mono | the smallest overline / metadata label — mono, uppercase, tracked, pegged to label's own sizes |
| **tiny** | ui (prose) | figure/image/media captions, table captions, chart annotations, small supporting text |

Note the split: **body** is *prose you read*; **label** is *interface chrome you operate*. A
button label is `label`, a paragraph is `body`. **Sub-title** and **tiny** are prose too, even
though they render in the *mono*/*ui* font respectively — they wrap (`-line`, never
`-line-single`). Reach for `tiny` on a figure caption, not `label`. There is no separate
"quote" / "caption" / "legal" / "ui" voice — those jobs live on `lead`, `tiny`, `body`, and
`label` respectively.

## Choosing a concrete font per family slot

Steps 1–3 name the five font-family *roles* (`--font-display/heading/body/ui/mono`); they don't
say which real typeface fills each one. That choice is a judgment call, not a token lookup — a
brand-forward marketing display voice and a dense enterprise data-table body voice want opposite
answers, both correct. Designing that choice from a brand concept or creative brief is
`pick-fonts`'s job (territory interpretation, per-voice rationale, pairing drama,
verified metric compatibility) — route there for the full treatment, then bind its decision here.
Read [`references/font-selection.md`](references/font-selection.md) only for the no-brief fallback
heuristic (distinctiveness vs. neutrality by slot, absent any other signal).

## The laws (violating any is a defect)

1. **Voice+step, not px, not a font stack.** If a size or family isn't a `--type-*` var (or a
   `.type-*` class), it doesn't belong in UI code. No `font-size: 14px`, no
   `font-family: Inter`, no `line-height: 1.5`.
2. **Voice = function, step = rank; size is derived.** Choose the voice from what the text *is*
   (prose → `body`, chrome → `label`, a heading → `headline`/`title`/`sub-heading`), then the step
   from its rank — the size falls out. Never reach for `display` just to get big text, a larger
   step to hit a target line-height, or `label` to get small headings. If two elements share a
   voice, the more prominent one takes the higher step; if a size feels wrong, it's the wrong
   *step*, not a reason to switch voices.
3. **`line` and `para` come with the size.** Line-height (`-line`) and paragraph spacing (`-para`)
   are derived per step — use them; don't set your own. For single-line control text (a button, an
   input value, a kicker overline) use `-line-single` (leading 1.0), which exists ONLY on the box
   voices — **label · code · kicker**; every other voice has only `-line`.
4. **Tracking is baked and optical.** `-tracking` is tuned per step (tight/negative on display,
   open on kicker and sub-heading) — apply it; never add your own `letter-spacing`.
5. **Weight is the voice's, case is the treatment's.** Use `-weight` (or the class); don't bold a
   voice by hand. `sub-heading` and `kicker` are uppercase by treatment (the class sets
   `text-transform: uppercase`) — don't `text-transform` them yourself, and don't uppercase a
   voice that isn't.
6. **Responsive is per-breakpoint modes, not `clamp()`/`vw`.** If a kit exports breakpoint modes,
   the vars are re-declared inside `@media` blocks and the same class restyles automatically. A
   Base-only export (no `@media` blocks) is a valid fixed-type choice; don't add fluid
   `clamp()`/`vw` type to "fix" it (see [`references/responsive.md`](references/responsive.md)).
7. **The text-rendering baseline is always on.** Include it once in the project's global CSS —
   part of the token layer's contract, not an option:
   ```css
   html {
     -webkit-font-smoothing: antialiased;  /* macOS pair: consistent weight in light AND dark */
     -moz-osx-font-smoothing: grayscale;
     text-rendering: optimizeLegibility;   /* kerning + ligatures engaged */
     font-optical-sizing: auto;            /* variable fonts use their optical axes */
     font-synthesis: none;                 /* no faux bold/italic — weights resolve from the font */
     font-kerning: normal;
     font-variant-ligatures: common-ligatures;
   }
   code, pre, kbd { font-variant-ligatures: none; } /* code-like units never ligate */
   ```
   `font-synthesis: none` means an unresolvable weight renders at the nearest REAL weight — if
   something looks un-bold, fix the loaded font (or the `-weight` var), never fake it.

## Surface map — where to look things up

| Setting type on… | Reference |
|---|---|
| Headings h1–h6, sub-headings, titles, kickers, display, the heading↔body pairing | [`references/headings.md`](references/headings.md) |
| Body prose, lead/standfirst, pull-quotes, captions, legal fine-print, lists, links, inline code | [`references/prose.md`](references/prose.md) |
| Buttons, inputs, labels, menus, tabs, table cells, badges, tooltips, code, single- vs multi-line | [`references/interface.md`](references/interface.md) |
| Breakpoint modes, single- vs multi-line height, the fluid-type anti-pattern, fonts & fallbacks | [`references/responsive.md`](references/responsive.md) |
| Naming a concrete font per family slot — distinctive vs. neutral, pairing, weight/size extremes | [`references/font-selection.md`](references/font-selection.md) |

## Verify before you ship

- **Run the checker** — it binds the export (confirms every voice carries its steps × the five
  core props so your `var(--type-…)` will resolve, and that all five `--font-*` roles are defined)
  and lints your UI sources for hardcoded type (`font-size` / `font-family` / `line-height` /
  `letter-spacing` / `font-weight` that isn't var-backed):
  ```
  node <skill>/scripts/type-check.mjs <path/to/type.css> <src-dir-or-files…>
  ```
  A missing-props report means the bound export drifted from the eleven-voice assumption — re-bind
  before trusting the recipes. The linter catches both CSS (`font-size:`) and JS style objects
  (`fontSize:`), but a green run is necessary, not sufficient — styles built dynamically (a
  template string, a value behind a variable) are invisible to a static scan; eyeball those.
- The voice matches the text's job (prose → `body`, chrome → `label`, headings →
  `headline`/`title`/`sub-heading`) — one thing the linter can't see.
- Single-line controls use `-line-single`; prose and any wrapping text uses `-line`.
- No hand-set line-height, letter-spacing, weight, or `clamp()`/`vw` sizing.
- A distinctive font choice states its reason (brand-forward voice, editorial register); a neutral
  choice on body/label/tiny is a deliberate legibility/i18n/enterprise call, not a fallback — see
  `references/font-selection.md`.
