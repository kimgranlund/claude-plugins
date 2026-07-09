---
name: typography-tokens
description: >
  Use when setting the TYPE of any UI on the default `--type-*` token grammar (not Material's
  `--md-sys-typescale-*`) — font/size/weight/leading/tracking for a heading, body, label, button,
  caption, code, or kicker ("what type token for this", "which voice/step for this text", "size
  this heading", "what font should this use"). Eleven-voice scale (voice=function x step=rank,
  size derived): bind `--type-*`/`--font-*` (prefix configurable), pick VOICE by job (READ prose
  vs. OPERATE chrome) and STEP by rank, apply the baked leading/paragraph rhythm, pick a concrete
  font per family slot — distinctive vs. neutral, by voice. Never hardcode a px size, line-height,
  tracking, or font family. TYPE only. NOT for Material's `--md-sys-typescale-*`
  (material-design-typography-tokens); NOT for a no-token typography question
  (typography-lettering); NOT for building/placing a component (component-forge); NOT for locale
  number/date/currency formatting (i18n-verify).
disable-model-invocation: false
user-invocable: false
---

# Typography tokens (default `--type-*` grammar)

An Ultimate-Tokens-style export gives eleven named **voices**, each a ramp of **steps**, as CSS
custom properties. Your job is never to pick a px size or a font stack — it is to pick the right
**voice** (the text's role) and **step** (its size within that role), then — only where a concrete
font must be named — the right typeface for that voice's job.

This is the generic twin of `material-design-typography-tokens`: same eleven-voice ladder, same
`{voice}-{step}-{prop}` grammar, no Material-specific namespace or bound font choices — the prefix
after `--` is whatever the project's export declares.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file defining `--font-*` families and the type-scale variables
   (often `type.css` / `tokens.css`; a DTCG `*.tokens.json` and utility classes may sit beside
   it). **The scale prefix is configurable:** the default is `--type-*` (class `.type-*`), but a
   Material scheme exports `--md-sys-typescale-*` (that binding lives in
   `material-design-typography-tokens`, not here) and a branded kit may export
   `--{brand}-type-*` — **read the actual prefix from the file**; the grammar after it
   (`-{voice}-{step}-{prop}`) is identical either way. If no export exists, stop and ask — do not
   hardcode sizes.
2. **Read the fonts.** Five family roles: `--font-display`, `--font-heading`, `--font-body`,
   `--font-ui`, `--font-mono`. Every voice resolves to one of these — you never name a family
   directly, you use the voice's `--font-*` var (the utility classes already do this). Choosing
   *which* real typeface fills each role is a separate judgment call — see
   [`references/font-selection.md`](references/font-selection.md).
3. **Know the grammar.** `--type-{voice}-{step}-{prop}` where prop ∈
   `size · line · tracking · weight · para` (+ `line-single` on the box voices — ui, code,
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

| Voice | Font role | Use for | Steps |
|---|---|---|---|
| **display** | display | hero/marketing headlines, the one big statement on a view | XS–XL |
| **heading** | heading | section & content headings (h1–h4), card titles, dialog titles | XS–XL |
| **sub-heading** | heading | a wide-tracked label above a heading — uppercase by treatment | XS–XL |
| **kicker** | mono | the smallest overline / metadata label — mono, tracked, uppercase | XS–XL |
| **lead** | body | the standfirst / intro paragraph opening an article or section | SM–LG |
| **body** | body | running prose, paragraphs, descriptions, long-form reading | XS–XL |
| **quote** | heading | block & pull quotes — takes the heading face for presence | SM–LG |
| **caption** | ui (as prose) | figure/image/table captions, chart annotations — wraps | SM–LG |
| **ui** | ui | interface text: buttons, labels, inputs, menus, cells, badges | 3XS–2XL |
| **code** | mono | code, tabular figures, keyboard shortcuts, technical values | 3XS–2XL |
| **legal** | ui (as prose) | fine-print, disclaimers, footnotes — smallest reading text | SM–LG |

Note the split: **body** is *prose you read*; **ui** is *interface chrome you operate*. A button
label is `ui`, a paragraph is `body`. The editorial voices are prose too — **lead · quote ·
caption · legal** — even though caption/legal render in the *ui font*, they wrap (`-line`, never
`-line-single`). Reach for `caption` on a figure caption, not `ui`.

## Choosing a concrete font per family slot

Steps 1–3 name the five font-family *roles* (`--font-display/heading/body/ui/mono`); they don't
say which real typeface fills each one. That choice is a judgment call, not a token lookup — a
brand-forward marketing display voice and a dense enterprise data-table body voice want opposite
answers, both correct. Designing that choice from a brand concept or creative brief is
`typography-system-design`'s job (territory interpretation, per-voice rationale, pairing drama,
verified metric compatibility) — route there for the full treatment, then bind its decision here.
Read [`references/font-selection.md`](references/font-selection.md) only for the no-brief fallback
heuristic (distinctiveness vs. neutrality by slot, absent any other signal).

## The laws (violating any is a defect)

1. **Voice+step, not px, not a font stack.** If a size or family isn't a `--type-*` var (or a
   `.type-*` class), it doesn't belong in UI code. No `font-size: 14px`, no
   `font-family: Inter`, no `line-height: 1.5`.
2. **Voice = function, step = rank; size is derived.** Choose the voice from what the text *is*
   (prose → `body`, chrome → `ui`, a heading → a heading voice), then the step from its rank —
   the size falls out. Never reach for `display` just to get big text, a larger step to hit a
   target line-height, or `ui` to get small headings. If a size feels wrong, it's the wrong
   *step*, not a reason to switch voices.
3. **`line` and `para` come with the size.** Line-height (`-line`) and paragraph spacing (`-para`)
   are derived per step — use them; don't set your own. For single-line control text (a button, an
   input value, a kicker overline) use `-line-single` (leading 1.0), which exists ONLY on the box
   voices — **ui · code · kicker**; every other voice has only `-line`.
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

## Surface map — where to look things up

| Setting type on… | Reference |
|---|---|
| Headings h1–h4, sub-headings, kickers, display, the heading↔body pairing | [`references/headings.md`](references/headings.md) |
| Body prose, lead/standfirst, quotes & pull-quotes, captions, legal fine-print, lists, links, inline code | [`references/prose.md`](references/prose.md) |
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
- The voice matches the text's job (prose → `body`, chrome → `ui`, headings → a heading voice) —
  one thing the linter can't see.
- Single-line controls use `-line-single`; prose and any wrapping text uses `-line`.
- No hand-set line-height, letter-spacing, weight, or `clamp()`/`vw` sizing.
- A distinctive font choice states its reason (brand-forward voice, editorial register); a neutral
  choice on body/ui/legal is a deliberate legibility/i18n/enterprise call, not a fallback — see
  `references/font-selection.md`.
