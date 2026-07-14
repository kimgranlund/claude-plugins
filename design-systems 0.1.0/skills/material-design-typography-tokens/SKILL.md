---
name: material-design-typography-tokens
description: >
  Use when setting the TYPE of any UI whose type tokens use the Material `--md-sys-typescale-*`
  naming — font/size/weight/leading/tracking for a heading, body, label,
  menu item, table cell, badge, kicker ("what type token for this", "which voice/level",
  "why is this text the wrong size/weight"). Consumption guide for the
  thirteen-voice scale extending Material 3: bind `--md-sys-typescale-*` + `--font-*`, pick VOICE (prose you READ vs chrome you
  OPERATE) and LEVEL, apply the baked leading/tracking rhythm. Never hardcode a
  px size, line-height, tracking, or family. NOT for a control's own text-SIZE
  (material-design-geometry-tokens' `--md-sys-size-{step}-font`; this supplies family/weight only); NOT for color (material-design-color-tokens);
  NOT for radius/spacing (material-design-geometry-tokens); NOT for kits on the default `--type-*`
  grammar (typography plugin's typography-tokens); NOT for DESIGNING a type scale
  (typography-lettering); NOT for motion easing/duration (material-design-motion-tokens).
disable-model-invocation: false
user-invocable: false
---

# Material Design typography tokens (M3-founded, extended)

This kit's type layer is **Material Design's type scale as the conceptual foundation, extended with
more semantic voices.** It exports under M3's `--md-sys-typescale-*` namespace, but the scale carries
**thirteen named voices**, every one riding a **uniform 3-level ramp** — the M3 baseline reorganized,
grown, and (since the source engine's 2026-07-13 rewrite) simplified onto one shared level set. Your
job is never to pick a px size or a font stack: pick the right **voice** (the text's role) and the
right **level** (its rank), and size, leading, tracking, weight, and paragraph spacing fall out of the
token.

## Foundation vs. extension (what's M3, what's ours)

| Material 3 baseline (recognizable M3) | The nonoun extensions (why thirteen voices) |
|---|---|
| `display`, `headline`, `title`, `label`, `body` | **Finer voices M3 lacks**: `sub-heading`, `sub-title`, `lead`, `kicker`, plus **mono siblings** of body/label (`body-mono`, `label-mono`) and a prose micro-voice (`tiny`, `tiny-mono`) — 13 total riding 5 font-family roles |
| Large / Medium / Small (3 sizes per role) | **The SAME 3-level ramp — SM · MD · LG — on EVERY voice** (2026-07-13: previously the ramps varied 3/5/8 steps by voice; now one uniform level set, and SIZE itself is a hand-authored FIXED px table shared by every treatment, not a derived modular scale) |
| one font/size/line/tracking/weight per style | **Per-step baked props**: `size · line · tracking · weight · para` (paragraph spacing) — plus a **single-line leading** (`-line-single`) on the BOX voices (control/label text) |
| 5 named type roles | **13 named voices** riding **5 font-family roles** (display · heading · body · ui · mono) |
| one weight per role | **Sibling weights** — named heavier/lighter variants around a voice's core weight, ready-made CSS custom props (`-weight-{slug}`) for a "bolder" emphasis without hand-picking a number |

Recognize the M3 names, but reach for the thirteen voices — they exist so you never hand-roll a
kicker, a pull-quote-style lead, or a single-line control leading with `font-size` and `line-height`.

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
   voice×level. **Read what's actually in the file** — the source engine's current shape ships all
   thirteen voices at the uniform SM/MD/LG levels (the table below); an older or hand-edited export may
   still carry the old per-voice ramps — bind against what's THERE, not this doc.
4. **Know the grammar.** Semantic = `--md-sys-typescale-{voice}-{level}-{prop}`, prop ∈
   `size · line · tracking · weight · para` (+ `line-single` on the BOX voices) + an optional
   `-weight-{slug}` per sibling weight. Prefer the ready-made utility class
   **`.md-sys-typescale-{voice}-{level}`** (one per voice×level — 39 total at 13×3) over composing the
   vars by hand:
   ```css
   .section-title { /* the class already sets family+size+line+tracking+weight */ }
   /* a non-control interface label — menu item, table cell, badge: the FULL label voice, size included.
      -line-single (leading 1.0) because it's single-line and doesn't wrap. */
   .menu-item { font-family: var(--font-voice-label);
                font-size: var(--md-sys-typescale-label-md-size);
                line-height: var(--md-sys-typescale-label-md-line-single);
                letter-spacing: var(--md-sys-typescale-label-md-tracking);
                font-weight: var(--md-sys-typescale-label-md-weight); }
   ```
   A **control** (a button/input/select with a `.md-sys-control-{step}` box) is different: its font-**size**
   comes from geometry's `--md-sys-size-{step}-font` (locked to the box), NOT this voice's own `-size` —
   see the boundary section below; only SM/MD/LG of geometry's six steps are actually typed this way.

## Two axes — voice (function) × level (hierarchy depth)

A **voice is a ROLE** — the text's *function*, carrying its character (family, weight, tracking,
leading, case) across every size. A **level is a RANK** — SM/MD/LG, the element's place in that
voice's own hierarchy, from which the size is *derived*. They're independent: the same voice appears
at all three levels, and the same level hosts every voice. **Pick the voice by function and the level
by hierarchy depth — never a voice to hit a size, never a level to hit a px.** Choosing `display`
because you want big text, or `lg` because you want more line-height, is the mistake this split exists
to prevent.

## The thirteen voices — pick by the text's FUNCTION

| Voice | Font role | Flow | Use for |
|---|---|---|---|
| **display** | display | prose | hero / marketing headline — the one big statement on a view |
| **headline** | heading | prose | real document headings: page title, section headings, card/dialog titles |
| **sub-heading** | heading | prose | wide-tracked UPPERCASE label sitting ABOVE a heading (e.g. "PRICING") |
| **title** | heading | prose | a smaller headline — a card/dialog title one rung below `headline` |
| **sub-title** | mono (as PROSE) | prose | a small heading in an alternate face — the mono role dressed as a headline, not a control label |
| **lead** | body | prose | standfirst / intro paragraph — larger, lighter than body; wraps |
| **body** | body | prose | running prose, paragraphs, long-form reading |
| **body-mono** | mono | **BOX** | body-sized text in the mono face (metadata rows, tabular prose-adjacent copy) — control/label flow, has `-line-single` |
| **label** | ui | **BOX** | menus, table cells, standalone labels, badges, tooltips — interface text NOT in a control box; has `-line-single` |
| **label-mono** | mono | **BOX** | label-sized text in the mono face (a mono metadata chip) |
| **kicker** | mono | **BOX** | the smallest overline / metadata tag — UPPERCASE, tracked; has `-line-single` |
| **tiny** | ui (as PROSE) | prose | the smallest READING text — fine print, footnotes, disclaimers (wraps, no `-line-single`) |
| **tiny-mono** | mono (as PROSE) | prose | `tiny`-sized text in the mono face, still prose |

Note the split: **body** is *prose you read*; **label** is *interface chrome you operate*. A paragraph
is `body`; a menu item or table cell is `label`. **One boundary inside chrome:** a **control** (button,
input, select — anything with a `.md-sys-control-{step}` box) takes its font-**size** from geometry's
`--md-sys-size-{step}-font` (the box and text share one number, and only for geometry's SM/MD/LG steps
— see below), so "what size is this button" is a **geometry** question; the `label` voice supplies the
control's family/weight/tracking, never its size.

**The BOX voices are exactly `body-mono`, `label`, `label-mono`, `kicker`** — they emit `-line-single`
(leading 1.0, for text locked in a box) and a flat 1.0×size paragraph rhythm. Every other voice is
PROSE — including `sub-title` and `tiny`/`tiny-mono`, which ride a box-default role (mono/ui) but are
deliberately flagged prose: `sub-title` is a small heading, `tiny`/`tiny-mono` are reading text, not
controls. Prose voices never emit `-line-single`.

## The laws (violating any is a defect)

1. **Voice+level, not px, not a font stack.** If a size or family isn't a `--md-sys-typescale-*` var
   (or a `.md-sys-typescale-*` class), it doesn't belong in UI code. No `font-size: 14px`, no
   `font-family: Inter`, no `line-height: 1.5`.
2. **Voice = function, level = rank; size is derived.** Choose the voice from what the text *is* (prose
   → `body`, chrome → `label`, a heading → `headline`/`title`), then the level from its rank — the size
   falls out. Never reach for `display` just to get big text, or `lg` to hit a target line-height. If a
   size feels wrong, it's the wrong *level*, not a reason to switch voices.
3. **`line` and `para` come with the size.** Line-height (`-line`) and paragraph spacing (`-para`) are
   derived per step — use them; don't set your own. For single-line NON-control text (a table cell, a
   standalone label, a kicker overline) use `-line-single` (leading 1.0), which exists ONLY on the BOX
   voices — **body-mono · label · label-mono · kicker**; every other voice has only `-line`. (A
   control's line is its box height, set by the `.md-sys-control-{step}` geometry — not a leading token.)
4. **Tracking is baked and optical.** `-tracking` is tuned per step (tight/negative on display, open on
   kicker and sub-heading) — apply it; never add your own `letter-spacing`.
5. **Weight is the voice's, case is the treatment's.** Use `-weight` (or the class); don't bold a voice
   by hand. `sub-heading` and `kicker` are UPPERCASE by treatment (the class sets
   `text-transform: uppercase`) — don't `text-transform` them yourself, and don't uppercase a voice that
   isn't. For a heavier emphasis WITHIN a voice, reach for its sibling weight
   (`--md-sys-typescale-{voice}-weight-{slug}` — "bold", "semi-bold", …) instead of guessing a number.
6. **Responsive is per-breakpoint modes, not `clamp()`/`vw`.** If a kit exports breakpoint modes, the
   vars are re-declared inside `@media` blocks and the same class restyles automatically. Body-class
   voices stay frozen (or nearly so) across breakpoints while display-class type compresses — see
   [`references/responsive.md`](references/responsive.md); don't add fluid `clamp()`/`vw` type to
   compensate for a kit that already ships modes (or one that doesn't).

## Surface map — where to look things up

| Setting type on… | Reference |
|---|---|
| Headlines, sub-headings, titles, sub-titles, display, the heading↔body pairing | [`references/headings.md`](references/headings.md) |
| Body prose, lead/standfirst, tiny fine-print, lists, links, inline code | [`references/prose.md`](references/prose.md) |
| Buttons, inputs, labels, menus, tabs, table cells, badges, tooltips, the mono box voices, single- vs multi-line | [`references/interface.md`](references/interface.md) |
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
- The voice matches the text's job (prose → `body`, chrome → `label`, headings → `headline`/`title`) —
  the one thing the linter can't see.
- Single-line controls/chrome use `-line-single`; prose and any wrapping text uses `-line`.
- No hand-set line-height, letter-spacing, weight, or `clamp()`/`vw` sizing.

_Provenance: the thirteen-voice scale + the uniform SM/MD/LG ramp is the nonoun type engine's
(`src/engine/type.mjs`), current as of its 2026-07-13 rewrite (PR #279 — pure RENAMES: `heading`→
`headline`, `ui`→`label`; FOLDS: the old `quote` voice folds into `lead`, `caption` and `legal` both
fold into `tiny`; `title` and `sub-title` are genuinely NEW voices, not renames of anything. SIZE became a
fixed hand-authored table shared across all treatments, replacing the old per-voice modular scale;
sibling weights + a per-voice font-family override were added the same window). This skill now targets
that current engine, not any one bound export — **before this doc is trustworthy against a specific
project, confirm that project's own export has been regenerated to match** (an export built before
2026-07-13 still carries the OLD voice names and mixed-step ramps; bind-check it and re-sync per-project
notes if it hasn't). Owner: the kit maintainer. Every voice's MEANING (not its binding grammar) is
mirrored in `material-design-token-semantics` — re-sync that pack's `references/typography.md` on any
voice rename, fold, or role change too, the same trigger as this file._
