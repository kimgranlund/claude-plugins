---
name: material-design-typography-tokens
description: >
  Use when setting the TYPE of any UI in a project whose type tokens use the Material
  `--md-sys-typescale-*` naming (a nonoun / ADIA "Material-Design-founded" export) — the
  font/size/weight/leading/tracking for a heading, body copy, a menu item, a table cell, a standalone
  label, a badge, a caption, code, a quote, or a kicker ("what type token for this heading/label/caption",
  "which voice/step should this text use", "which typescale class for a menu item or table cell", "why is
  this text the wrong size/weight"). The consumption guide for the eleven-voice type scale that EXTENDS
  Material 3: how to find and bind the project's `--md-sys-typescale-*` variables and `--font-*` families,
  choose the right VOICE (prose you READ vs. chrome you OPERATE) and LEVEL (rank), and apply the baked
  leading/tracking/paragraph rhythm. Never hardcode a px size, line-height, letter-spacing, or font family
  — this names the Material `--md-sys-typescale-*` role for every job.
  NOT for a control's own text-SIZE — a button/input/select with a `.md-sys-control-{step}` box takes its
  size from material-design-geometry-tokens' `--md-sys-size-{step}-font` (this voice supplies only its
  family/weight/tracking); NOT for color (material-design-color-tokens); NOT for radius/spacing/density
  (material-design-geometry-tokens); NOT for kits on the default `--type-*` grammar (the ultimate-tokens
  `typography-tokens` skill); NOT for DESIGNING a type scale or specimen (typography-lettering).
disable-model-invocation: false
user-invocable: false
---

# Material Design typography tokens (M3-founded, extended)

This kit's type layer is **Material Design's type scale as the conceptual foundation, extended with
more semantic voices.** It exports under M3's `--md-sys-typescale-*` namespace, but the scale carries
**eleven named voices** — the M3 baseline reorganized and grown. Your job is never to pick a px size
or a font stack: pick the right **voice** (the text's role) and the right **level** (its rank), and
size, leading, tracking, weight, and paragraph spacing fall out of the token.

## Foundation vs. extension (what's M3, what's ours)

| Material 3 baseline (recognizable M3) | The nonoun extensions (why eleven voices) |
|---|---|
| `display`, `headline` (→ heading), `title`, `label` (→ ui), `body` | **Editorial voices M3 lacks**: `sub-heading`, `kicker`, `lead`, `quote`, `caption`, `legal` — plus the **body/ui split** (prose you READ vs. chrome you OPERATE) |
| Large / Medium / Small (3 sizes per role) | **Finer per-voice ramps**: `3XS–2XL` (8 levels) on ui/code, `XS–XL` (5) on display/heading/sub-heading/kicker/body, `SM–LG` (3) on the editorial prose voices (lead/quote/caption/legal) |
| one font/size/line/tracking/weight per style | **Per-step baked props**: `size · line · tracking · weight · para` (paragraph spacing) — plus a **single-line leading** (`-line-single`) on the box voices ui/code/kicker |
| 5 named type roles | **11 named voices** riding **5 font-family roles** (display · heading · body · ui · mono) |

Recognize the M3 names, but reach for the eleven voices — they exist so you never hand-roll a caption,
a kicker, a pull-quote, or a single-line control leading with `font-size` and `line-height`.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file whose `:root` defines `--font-*` families and `--md-sys-typescale-*`
   variables (in ADIA's case `typography/type.css`; a DTCG `type.tokens.json` sits beside it). If none
   exists, **stop and ask — do not hardcode sizes.**
2. **Read the five font-family roles.** `--font-display` · `--font-heading` · `--font-body` ·
   `--font-ui` · `--font-mono`. In this kit they are **Inter Tight · Inter Tight · Inter · Inter ·
   JetBrains Mono**. Every voice resolves to one of these — you never name a family directly.
3. **Enumerate the voices & levels.** Each `--md-sys-typescale-{voice}-{level}-size` line marks a
   voice×level. **Read what's actually in the file** — this kit ships the eleven voices at the exact
   levels in the table below; another kit's ramps may differ.
4. **Know the grammar.** Semantic = `--md-sys-typescale-{voice}-{level}-{prop}`, prop ∈
   `size · line · tracking · weight · para` (+ `line-single` on ui/code/kicker). Prefer the ready-made
   utility class **`.md-sys-typescale-{voice}-{level}`** (53 of them; each wires family+size+line+
   tracking+weight in one) over composing the vars by hand:
   ```css
   .section-title { /* the class already sets family+size+line+tracking+weight */ }
   /* a non-control interface label — menu item, table cell, badge: the FULL ui voice, size included.
      -line-single (leading 1.0) because it's single-line and doesn't wrap. */
   .menu-item { font-family: var(--font-ui);
                font-size: var(--md-sys-typescale-ui-md-size);
                line-height: var(--md-sys-typescale-ui-md-line-single);
                letter-spacing: var(--md-sys-typescale-ui-md-tracking);
                font-weight: var(--md-sys-typescale-ui-md-weight); }
   ```
   A **control** (a button/input/select with a `.md-sys-control-{step}` box) is different: its font-**size**
   comes from geometry's `--md-sys-size-{step}-font` (locked to the box — the same number as this voice's
   size at that step) — reach for it there (**material-design-geometry-tokens**), not this voice's `-size`.
   The ui voice still supplies a control's **family/weight/tracking** (`--font-ui` + `-ui-{level}-weight`/
   `-tracking`); only its size and line belong to the box.

## Two axes — voice (function) × level (hierarchy depth)

A **voice is a ROLE** — the text's *function*, carrying its character (family, weight, tracking,
leading, case) across every size. A **level is a RANK** — the element's place in the hierarchy, from
which the size is *derived*. They're independent: the same voice appears at many levels, and the same
level hosts different voices. **Pick the voice by function and the level by hierarchy depth — never a
voice to hit a size, never a level to hit a px.** Choosing `display` because you want big text, or a
larger level because you want line-height 26, is the mistake this split exists to prevent.

## The eleven voices — pick by the text's FUNCTION

| Voice | Font (role) | Use for | Levels |
|---|---|---|---|
| **display** | Inter Tight (display) | hero / marketing headline — the one big statement on a view | XS–XL |
| **heading** | Inter Tight (heading) | section & content headings (h1–h4), card & dialog titles | XS–XL |
| **sub-heading** | Inter Tight (heading) | wide-tracked label above a heading — UPPERCASE by treatment | XS–XL |
| **kicker** | JetBrains Mono (mono) | smallest overline / metadata — UPPERCASE, tracked; has `-line-single` | XS–XL |
| **lead** | Inter (body) | standfirst / intro paragraph — larger, lighter than body; wraps | SM–LG |
| **body** | Inter (body) | running prose, paragraphs, long-form reading | XS–XL |
| **quote** | Inter Tight (heading) | block & pull quotes — take the heading face | SM–LG |
| **caption** | Inter (ui, as PROSE) | figure / media / table captions — wraps, uses `-line` | SM–LG |
| **ui** | Inter (ui) | menus, table cells, standalone labels, badges, tooltips — interface text NOT in a control box; has `-line-single` | 3XS–2XL |
| **code** | JetBrains Mono (mono) | code, tabular figures, shortcuts; has `-line-single` | 3XS–2XL |
| **legal** | Inter (ui, as PROSE) | fine-print, disclaimers, footnotes — smallest reading text | SM–LG |

Note the split: **body** is *prose you read*; **ui** is *interface chrome you operate*. A paragraph is
`body`; a menu item or table cell is `ui`. **One boundary inside chrome:** a **control** (button, input,
select — anything with a `.md-sys-control-{step}` box) takes its font-**size** from geometry's
`--md-sys-size-{step}-font` (the box and text share one number), so "what size is this button" is a
**geometry** question; the ui voice supplies the control's family/weight/tracking, never its size. The ui
voice's *own* size is for chrome NOT in a control box — menu items, cells, standalone labels, badges (its
finer 3XS/2XS steps exist for exactly that dense text). The **editorial** voices are prose too — **lead ·
quote · caption · legal** — even though caption/legal render in the *ui font* (`--font-ui`), they wrap: use
`-line` and `-para`, **never** `-line-single`. Reach for `caption` on a figure caption, not `ui`.

## The laws (violating any is a defect)

1. **Voice+level, not px, not a font stack.** If a size or family isn't a `--md-sys-typescale-*` var
   (or a `.md-sys-typescale-*` class), it doesn't belong in UI code. No `font-size: 14px`, no
   `font-family: Inter`, no `line-height: 1.5`.
2. **Voice = function, level = rank; size is derived.** Choose the voice from what the text *is* (prose
   → `body`, chrome → `ui`, a heading → a heading voice), then the level from its rank — the size falls
   out. Never reach for `display` just to get big text, a larger level to hit a target line-height, or
   `ui` to get small headings. If a size feels wrong, it's the wrong *level*, not a reason to switch voices.
3. **`line` and `para` come with the size.** Line-height (`-line`) and paragraph spacing (`-para`) are
   derived per step — use them; don't set your own. For single-line NON-control text (a table cell, a
   standalone label, a kicker overline) use `-line-single` (leading 1.0), which exists ONLY on the box
   voices — **ui · code · kicker**; every other voice has only `-line`. (A control's line is its box
   height, set by the `.md-sys-control-{step}` geometry — not a leading token.)
4. **Tracking is baked and optical.** `-tracking` is tuned per step (tight/negative on display, open on
   kicker and sub-heading) — apply it; never add your own `letter-spacing`.
5. **Weight is the voice's, case is the treatment's.** Use `-weight` (or the class); don't bold a voice
   by hand. `sub-heading` and `kicker` are UPPERCASE by treatment (the class sets
   `text-transform: uppercase`) — don't `text-transform` them yourself, and don't uppercase a voice
   that isn't.
6. **Responsive is per-breakpoint modes, not `clamp()`/`vw`.** If a kit exports breakpoint modes, the
   vars are re-declared inside `@media` blocks and the same class restyles automatically. **This ADIA
   kit shipped Base-only** (no `@media` blocks — the type is fixed), a valid choice; don't add fluid
   `clamp()`/`vw` type to "fix" it (see [`references/responsive.md`](references/responsive.md)).

## Surface map — where to look things up

| Setting type on… | Reference |
|---|---|
| Headings h1–h4, sub-headings, kickers, display, the heading↔body pairing | [`references/headings.md`](references/headings.md) |
| Body prose, lead/standfirst, quotes & pull-quotes, captions, legal fine-print, lists, links, inline code | [`references/prose.md`](references/prose.md) |
| Buttons, inputs, labels, menus, tabs, table cells, badges, tooltips, code, single- vs multi-line | [`references/interface.md`](references/interface.md) |
| Breakpoint modes, single- vs multi-line height, the fluid-type anti-pattern, fonts & fallbacks | [`references/responsive.md`](references/responsive.md) |

## Verify before you ship

- **Run the checker** — it binds the export (confirms every voice carries its levels × the five props
  so your `var(--md-sys-typescale-…)` will resolve, and that all five `--font-*` roles are defined) and
  lints your UI sources for hardcoded type (`font-size` / `font-family` / `line-height` /
  `letter-spacing` / `font-weight` that isn't var-backed):
  ```
  node <skill>/scripts/type-check.mjs <path/to/type.css> <src-dir-or-files…>
  ```
  A missing-props report means the bound export drifted from the eleven-voice assumption — re-bind
  before trusting the recipes. The linter catches both CSS (`font-size:`) and JS style objects
  (`fontSize:`), but a green run is necessary, not sufficient — styles built dynamically (a template
  string, a value behind a variable) are invisible to a static scan; eyeball those.
- The voice matches the text's job (prose → `body`, chrome → `ui`, headings → a heading voice) — the
  one thing the linter can't see.
- Single-line controls use `-line-single`; prose and any wrapping text uses `-line`.
- No hand-set line-height, letter-spacing, weight, or `clamp()`/`vw` sizing.

_Provenance: the eleven-voice scale is the nonoun type engine's (`src/engine/type.mjs`); this skill was
authored against the ADIA reference export (`typography/type.css`, 2026-07-05). When the engine regenerates
the export, re-run the bind check and re-sync any changed voices/levels here — owner: the kit maintainer._
