---
name: material-design-typography-tokens
description: >
  Use when setting the TYPE of any UI whose type tokens use the Material `--md-sys-typescale-*`
  naming — font/size/weight/leading/tracking for a heading, body, label, button, input,
  menu item, table cell, badge, kicker ("what type token for this", "which voice/level",
  "why is this text the wrong size/weight"). Consumption guide for the
  fifteen-voice scale extending Material 3: bind `--md-sys-typescale-*` + `--font-*`, pick VOICE (prose you READ vs chrome you
  OPERATE — control text vs. static label vs. widget text) and LEVEL, apply the baked
  leading/tracking rhythm. Never hardcode a
  px size, line-height, tracking, or family. NOT for a control's own text-SIZE
  (material-design-geometry-tokens' `--md-sys-size-{step}-font`, which composes FROM this skill's
  `ui-control` voice — read here for what drives it); NOT for color (material-design-color-tokens);
  NOT for radius/spacing (material-design-geometry-tokens); NOT for kits on the default `--type-*`
  grammar (typography plugin's font-token-rules); NOT for DESIGNING a type scale
  (lettering-facts); NOT for motion easing/duration (material-design-motion-tokens).
disable-model-invocation: false
user-invocable: false
---

# Material Design typography tokens (M3-founded, extended)

This kit's type layer is **Material Design's type scale as the conceptual foundation, extended with
more semantic voices.** It exports under M3's `--md-sys-typescale-*` namespace, but the scale carries
**fifteen named voices**. Thirteen ride a **uniform 3-level ramp** (SM/MD/LG) — the M3 baseline
reorganized, grown, and (since the source engine's 2026-07-13 rewrite) simplified onto one shared
level set — and **two** (`ui-control`, `ui-widget`) ride their own **full 6-level ramp** (XS/SM/MD/
LG/XL/2XL, TKT-0008, 2026-07-16), the only voices that do. Your job is never to pick a px size or a
font stack: pick the right **voice** (the text's role) and the right **level** (its rank), and size,
leading, tracking, weight, and paragraph spacing fall out of the token.

## Foundation vs. extension (what's M3, what's ours)

| Material 3 baseline (recognizable M3) | The nonoun extensions (why fifteen voices) |
|---|---|
| `display`, `headline`, `title`, `label`, `body` | **Finer voices M3 lacks**: `sub-heading`, `sub-title`, `lead`, `kicker`, plus **mono siblings** of body/label (`body-mono`, `label-mono`), a prose micro-voice (`tiny`, `tiny-mono`), and two dedicated **interactive-text** voices (`ui-control`, `ui-widget`) — 15 total riding 5 font-family roles |
| Large / Medium / Small (3 sizes per role) | **A shared 3-level ramp — SM · MD · LG — on 13 of the 15 voices** (2026-07-13: previously the ramps varied 3/5/8 steps by voice; now one uniform level set for most voices, and SIZE itself is a hand-authored FIXED px table shared by every treatment, not a derived modular scale). **`ui-control` and `ui-widget` are the exception** — they ride the FULL 6-level XS…2XL ramp (TKT-0008), because control geometry needs a size at every one of its six steps |
| one font/size/line/tracking/weight per style | **Per-step baked props**: `size · line · tracking · weight · para` (paragraph spacing) — plus a **single-line leading** (`-line-single`) on the BOX voices (control/widget text) |
| 5 named type roles | **15 named voices** riding **5 font-family roles** (display · heading · body · ui · mono) |
| one weight per role | **Sibling weights** — named heavier/lighter variants around a voice's core weight, ready-made CSS custom props (`-weight-{slug}`) for a "bolder" emphasis without hand-picking a number |

Recognize the M3 names, but reach for the fifteen voices — they exist so you never hand-roll a
kicker, a pull-quote-style lead, a button's own text size, or a single-line control leading with
`font-size` and `line-height`.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file whose `:root` defines `--font-*` families and `--md-sys-typescale-*`
   variables. If none exists, **stop and ask — do not hardcode sizes.**
2. **Read the five font-family roles.** `--font-display` · `--font-heading` · `--font-body` ·
   `--font-ui` · `--font-mono`. Every voice resolves to one of these — you never name a family
   directly. A current-engine export ALSO carries a `--font-voice-{voice}` prop for EVERY voice (a
   per-voice override off the shared role, TKT-0006) — prefer it over the bare role prop; it's
   byte-identical to the role font when no override is configured, so it's always safe to reach for.
   An older export may only carry the five role props — fall back to those if `--font-voice-*` is
   absent.
3. **Enumerate the voices & levels.** Each `--md-sys-typescale-{voice}-{level}-size` line marks a
   voice×level. **Read what's actually in the file** — the source engine's current shape ships
   thirteen voices at the uniform SM/MD/LG levels PLUS `ui-control`/`ui-widget` at the full XS/SM/MD/
   LG/XL/2XL levels (the table below); an older or hand-edited export may still carry the old
   per-voice ramps or lack the two interactive voices entirely — bind against what's THERE, not this
   doc.
4. **Know the grammar.** Semantic = `--md-sys-typescale-{voice}-{level}-{prop}`, prop ∈
   `size · line · tracking · weight · para` (+ `line-single` on the BOX voices) + an optional
   `-weight-{slug}` per sibling weight. Prefer the ready-made utility class
   **`.md-sys-typescale-{voice}-{level}`** (one per voice×level — 51 total: 13 voices × 3 levels +
   `ui-control`/`ui-widget` × 6 levels) over composing the vars by hand:
   ```css
   .section-title { /* the class already sets family+size+line+tracking+weight */ }
   /* a non-control interface label — table cell, tooltip, standalone caption: the FULL label voice,
      size included. -line-single (leading 1.0) does NOT apply here — label is a PROSE voice
      (2026-07-16); reach for -line even on single-line text. */
   .table-cell { font-family: var(--font-voice-label);
                 font-size: var(--md-sys-typescale-label-sm-size);
                 line-height: var(--md-sys-typescale-label-sm-line);
                 letter-spacing: var(--md-sys-typescale-label-sm-tracking);
                 font-weight: var(--md-sys-typescale-label-sm-weight); }
   /* a menu item is a CONTROL now — ui-control, not label (TKT-0008) — and IS single-line boxed. */
   .menu-item { font-family: var(--font-voice-ui-control);
                font-size: var(--md-sys-typescale-ui-control-md-size);
                line-height: var(--md-sys-typescale-ui-control-md-line-single);
                letter-spacing: var(--md-sys-typescale-ui-control-md-tracking);
                font-weight: var(--md-sys-typescale-ui-control-md-weight); }
   ```
   A **control** (a button/input/select with a `.md-sys-control-{step}` box) composes its font-**size**
   from the SAME `ui-control` level that names it — geometry's `--md-sys-size-{step}-font` field IS that
   composed size (or its fallback table when no type scale feeds geometry) — see the boundary section
   below; every one of geometry's six steps is typed this way now (TKT-0008 closed the old 3-of-6 gap).

## Two axes — voice (function) × level (hierarchy depth)

A **voice is a ROLE** — the text's *function*, carrying its character (family, weight, tracking,
leading, case) across every size. A **level is a RANK** — SM/MD/LG, the element's place in that
voice's own hierarchy, from which the size is *derived*. They're independent: the same voice appears
at all three levels, and the same level hosts every voice. **Pick the voice by function and the level
by hierarchy depth — never a voice to hit a size, never a level to hit a px.** Choosing `display`
because you want big text, or `lg` because you want more line-height, is the mistake this split exists
to prevent.

## The fifteen voices — pick by the text's FUNCTION

| Voice | Font role | Levels | Flow | Use for |
|---|---|---|---|---|
| **display** | display | SM/MD/LG | prose | hero / marketing headline — the one big statement on a view |
| **headline** | heading | SM/MD/LG | prose | real document headings: page title, section headings, card/dialog titles |
| **sub-heading** | heading | SM/MD/LG | prose | wide-tracked UPPERCASE label sitting ABOVE a heading (e.g. "PRICING") |
| **title** | heading | SM/MD/LG | prose | a smaller headline — a card/dialog title one rung below `headline` |
| **sub-title** | mono (as PROSE) | SM/MD/LG | prose | a small heading in an alternate face — the mono role dressed as a headline, not a control label |
| **lead** | body | SM/MD/LG | prose | standfirst / intro paragraph — larger, lighter than body; wraps |
| **body** | body | SM/MD/LG | prose | running prose, paragraphs, long-form reading |
| **body-mono** | mono (as PROSE) | SM/MD/LG | prose | body-sized text in the mono face (metadata rows, tabular prose-adjacent copy) — reads as a wrapping run, NOT boxed (changed 2026-07-16) |
| **label** | ui (as PROSE) | SM/MD/LG | prose | the STATIC label voice — table cells, tooltips, standalone captions, form field labels — interface text you READ, not a control (changed 2026-07-16; was BOX) |
| **label-mono** | mono (as PROSE) | SM/MD/LG | prose | label-sized text in the mono face (a mono metadata chip) — reads, doesn't box (changed 2026-07-16) |
| **kicker** | mono | SM/MD/LG | **BOX** | the smallest overline / metadata tag — UPPERCASE, tracked; has `-line-single` |
| **tiny** | ui (as PROSE) | SM/MD/LG | prose | the smallest READING text — fine print, footnotes, disclaimers (wraps, no `-line-single`) |
| **tiny-mono** | mono (as PROSE) | SM/MD/LG | prose | `tiny`-sized text in the mono face, still prose |
| **ui-control** | ui | **XS/SM/MD/LG/XL/2XL** | **BOX** | interactive CONTROL text — buttons, inputs, selects, menu items; composes into geometry's control-box `-font` field at EVERY step (TKT-0008, 2026-07-16) |
| **ui-widget** | ui | **XS/SM/MD/LG/XL/2XL** | **BOX** | compact WIDGET text — tags, badges, switches, radio/checkbox labels; its own smaller size table, NOT composed into geometry |

Note the split: **body** is *prose you read*; **label** is now the *static* interface voice — text you
read but don't operate (table cells, tooltips, form field labels, standalone captions). The two
voices for chrome you *operate* are **`ui-control`** (buttons, inputs, selects, menu items) and
**`ui-widget`** (tags, badges, switches, radio/checkbox labels) — both riding the full six-level ramp,
because control geometry needs a size at every one of its six steps. **The boundary inside chrome:** a
**control** (button, input, select — anything with a `.md-sys-control-{step}` box) takes its
font-**size** from geometry's `--md-sys-size-{step}-font`, which now composes DIRECTLY from the
`ui-control` voice's matching level at every one of geometry's six steps (TKT-0008 closed the old
3-of-6 gap — SM/MD/LG used to compose, XS/XL/2XL used to fall back to a standalone law; now all six
do) — so `ui-control`'s own level table IS the answer to "what size is this button", not a separate
geometry-only number.

**The BOX voices are exactly `kicker`, `ui-control`, `ui-widget`** — they emit `-line-single` (leading
1.0, for text locked in a box) and a flat 1.0×size paragraph rhythm. Every other voice is PROSE —
including `label`, `body-mono`, and `label-mono` (moved from BOX to PROSE 2026-07-16, the same window
`ui-control`/`ui-widget` took over the box job for interactive/widget chrome), plus `sub-title` and
`tiny`/`tiny-mono`, which ride a box-default role (mono/ui) but are deliberately flagged prose:
`sub-title` is a small heading, `tiny`/`tiny-mono` are reading text, not controls. Prose voices never
emit `-line-single`.

## The laws (violating any is a defect)

1. **Voice+level, not px, not a font stack.** If a size or family isn't a `--md-sys-typescale-*` var
   (or a `.md-sys-typescale-*` class), it doesn't belong in UI code. No `font-size: 14px`, no
   `font-family: Inter`, no `line-height: 1.5`.
2. **Voice = function, level = rank; size is derived.** Choose the voice from what the text *is* (prose
   → `body`, chrome → `label`, a heading → `headline`/`title`), then the level from its rank — the size
   falls out. Never reach for `display` just to get big text, or `lg` to hit a target line-height. If a
   size feels wrong, it's the wrong *level*, not a reason to switch voices.
3. **`line` and `para` come with the size.** Line-height (`-line`) and paragraph spacing (`-para`) are
   derived per step — use them; don't set your own. For single-line boxed chrome (a kicker overline, a
   control, a widget) use `-line-single` (leading 1.0), which exists ONLY on the BOX voices —
   **kicker · ui-control · ui-widget**; every other voice — including `label`, `body-mono`, and
   `label-mono` — has only `-line`, even for single-line uses like a table cell. (A control's line is
   its box height, set by the `.md-sys-control-{step}` geometry — not a leading token.)
4. **Tracking is baked and optical.** `-tracking` is tuned per step (tight/negative on display, open on
   kicker and sub-heading) — apply it; never add your own `letter-spacing`.
5. **Weight is the voice's, case is the treatment's.** Use `-weight` (or the class); don't bold a voice
   by hand. `sub-heading` and `kicker` are UPPERCASE by treatment (the class sets
   `text-transform: uppercase`) — don't `text-transform` them yourself, and don't uppercase a voice that
   isn't. For a heavier emphasis WITHIN a voice, reach for its sibling weight
   (`--md-sys-typescale-{voice}-weight-{slug}` — "bold", "semi-bold", …) instead of guessing a number.
6. **Responsive is per-breakpoint modes, not `clamp()`/`vw`.** If a kit exports breakpoint modes, the
   vars are re-declared inside `@media` blocks and the same class restyles automatically. Body-class
   voices — including `ui-control`/`ui-widget`, whose sizes top out at 20px — stay frozen (or nearly
   so) across breakpoints while display-class type compresses — see
   [`references/responsive.md`](references/responsive.md); don't add fluid `clamp()`/`vw` type to
   compensate for a kit that already ships modes (or one that doesn't).

## Surface map — where to look things up

| Setting type on… | Reference |
|---|---|
| Headlines, sub-headings, titles, sub-titles, display, the heading↔body pairing | [`references/headings.md`](references/headings.md) |
| Body prose, lead/standfirst, tiny fine-print, lists, links, inline code | [`references/prose.md`](references/prose.md) |
| Buttons, inputs, selects, menu items (`ui-control`); tags, badges, switches, checkboxes (`ui-widget`); static labels, table cells, tabs, tooltips (`label`); the mono siblings; single- vs multi-line | [`references/interface.md`](references/interface.md) |
| Breakpoint modes + compression, single- vs multi-line height, the fluid-type anti-pattern, fonts & fallbacks | [`references/responsive.md`](references/responsive.md) |

## Verify before you ship

- **Run the checker** — it binds the export (confirms every voice carries its levels × the five props
  so your `var(--md-sys-typescale-…)` will resolve, and that all five `--font-*` roles are defined) and
  lints your UI sources for hardcoded type (`font-size` / `font-family` / `line-height` /
  `letter-spacing` / `font-weight` that isn't var-backed):
  ```
  node <skill>/scripts/type-check.mjs <path/to/type.css> <src-dir-or-files…>
  ```
  The checker is fully dynamic — it reads whatever voices/levels/props are ACTUALLY in the bound file,
  so it works unmodified whether the export is on the old or the current voice taxonomy. A missing-props
  report means the bound export is internally inconsistent (a voice missing a prop on some level) — not
  a taxonomy question. The linter catches both CSS (`font-size:`) and JS style objects (`fontSize:`),
  but a green run is necessary, not sufficient — styles built dynamically (a template string, a value
  behind a variable) are invisible to a static scan; eyeball those.
- The voice matches the text's job (prose → `body`, static chrome → `label`, a control → `ui-control`,
  a compact widget → `ui-widget`, headings → `headline`/`title`) — the one thing the linter can't see.
- Single-line boxed chrome (`kicker`/`ui-control`/`ui-widget`) uses `-line-single`; every other voice —
  prose AND `label`/`body-mono`/`label-mono` — uses `-line`, even single-line uses like a table cell.
- No hand-set line-height, letter-spacing, weight, or `clamp()`/`vw` sizing.

_Provenance: the fifteen-voice scale is the nonoun type engine's (`src/engine/type.mjs`). The base
thirteen voices + the uniform SM/MD/LG ramp date to the engine's 2026-07-13 rewrite (PR #279 — pure
RENAMES: `heading`→`headline`, `ui`→`label`; FOLDS: the old `quote` voice folds into `lead`, `caption`
and `legal` both fold into `tiny`; `title` and `sub-title` are genuinely NEW voices, not renames of
anything. SIZE became a fixed hand-authored table shared across all treatments, replacing the old
per-voice modular scale; sibling weights + a per-voice font-family override were added the same
window). `ui-control` and `ui-widget` were added 2026-07-16 (TKT-0008) as the two INTERACTIVE-text
voices — the only voices on the full 6-level XS…2XL ramp — and took over the BOX job (`-line-single`,
1.0×size paragraph rhythm) for control and widget chrome; `label`, `body-mono`, and `label-mono`
became PROSE the same window (they used to be BOX). `ui-control` also composes into
`material-design-geometry-tokens`' control-box `-font` field at every one of geometry's six steps,
retiring the old partial (SM/MD/LG-only) composition. This skill now targets that current engine, not
any one bound export — **before this doc is trustworthy against a specific project, confirm that
project's own export has been regenerated to match** (an export built before 2026-07-16 lacks
`ui-control`/`ui-widget` entirely and still treats `label`/`body-mono`/`label-mono` as BOX; bind-check
it and re-sync per-project notes if it hasn't). Owner: the kit maintainer. Every voice's MEANING (not
its binding grammar) is mirrored in `material-design-token-semantics` — re-sync that pack's
`references/typography.md` on any voice rename, fold, or role change too, the same trigger as this
file._
