---
name: material-design-geometry-tokens
description: >
  Use when SIZING or SPACING any UI whose dimension tokens use the Material `--md-sys-size-*` /
  `--md-sys-radius-*` / `--md-sys-space-*` naming — the
  height/padding/radius of a control, a card's inset, gaps, icon sizes, focus rings, borders
  ("what size/spacing token for this", "how tall should this control be", "what padding/gap/
  radius", "make the layout denser"). The consumption guide for the dimensional layer extending
  Material 3: the control ramp, corner scale, and space/inset/gap
  ladders; the centering law; the two paddings by anatomy. A CONTROL's own text-SIZE is this skill's
  `--md-sys-size-{step}-font` field — "what font size for this button" lands HERE. Never hardcode
  a px height/padding/radius. NOT for color (material-design-color-tokens); NOT for the type
  scale/voices of NON-control text (material-design-typography-tokens); NOT for motion
  easing/duration (material-design-motion-tokens); NOT for kits on the
  default `--size-*`/`--space-*` grammar; NOT for DESIGNING the dimensional system.
disable-model-invocation: false
user-invocable: false
---

# Material Design geometry tokens (M3-founded, extended)

This kit's dimensional layer is **Material Design as the conceptual foundation, extended into a full
control-geometry system.** It exports under M3's `--md-sys-*` namespace, but a size is never a number you
type — it's a **role** you pick from the right **tier**. The system is **two tiers**: **control geometry**
(everything inside one control, derived from its height) and **container geometry** (the spacing between
and around components). Raw px values live only inside the tokens as substrate.

## Foundation vs. extension (what's M3, what's ours)

| Material 3 baseline (recognizable M3) | The nonoun extensions (why two tiers, not one grid) |
|---|---|
| The **shape-corner scale** `--md-sys-radius-{none·xs·sm·md·lg·xl·full}` = `0·4·8·12·16·28·9999px` — M3's own corner tokens | **A per-step control ramp**: `--md-sys-size-{xs…2xl}-{9 fields}` — every control's height, icon, caret, font, gap, paddings, min and radius, which M3 leaves to per-component specs |
| The 4dp spacing grid (`--md-sys-space-{0…9}`, a 4px-founded ladder) | **A centering law**: everything in a control derives from its height — edge padding = (height − glyph)/2 — so a glyph sits optically centered in a height² cell, not hand-tuned per component |
| `--md-sys-density` = 1 (the density concept) | **Two paddings by anatomy**: `-pad` (the SLOT edge, a control WITH a leading icon) vs `-pad-edge` (the SLOTLESS edge, a bare text button/label) — M3 folds this into component variants |
| M3's fully-rounded / pill shape | **Control radius = height/2** (already a full pill — a "rounded" control needs nothing extra); plus **semantic insets & gaps** (`--md-sys-inset-*` / `--md-sys-gap-*`, named rungs of the space ladder) and `--md-sys-border-*` / `--md-sys-focus-ring-*` primitives |

So: recognize the M3 radius scale and 4dp grid, but reach for the extensions — they exist precisely so you
never hand-roll a control height, a centered padding, or a container inset with a raw px value.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file whose `:root` defines dimensions under the **`--md-sys-size-*` /
   `--md-sys-radius-*` / `--md-sys-space-*`** prefix (in ADIA's case, `geometry/geometry.css`; a DTCG
   `geometry.tokens.json` sits beside it, and `.md-sys-control-{step}` utility classes live in the same
   CSS). If none exists, **stop and ask — do not hardcode dimensions.**
2. **Know the two tiers.** *Control* geometry is per-size (`--md-sys-size-{step}-*`, steps `xs…2xl`) and
   scales with the control's height. *Container* geometry (`--md-sys-radius-*`, `--md-sys-space-*`,
   `--md-sys-inset-*`, `--md-sys-gap-*`, borders, focus ring) is treatment-derived and mode-independent.
   **Don't cross them** — a control's inner padding is `--md-sys-size-{step}-pad`; a card's is
   `--md-sys-inset-card`.
3. **Classify the control ramp.** Six steps `xs…2xl`; `md`=28px is this kit's **baseHeight** — start
   there. Each step carries **9 fields**: `height · icon · caret · font · gap · pad · pad-edge · min ·
   radius`. The full per-step value table lives in [`references/controls.md`](references/controls.md)
   (the single source of truth for the numbers); the bind check echoes the heights it actually reads. This
   kit's geometry treatment is **"comfortable"**.
4. **Know the grammar.** Control = `--md-sys-size-{step}-{field}`. Ladders = `--md-sys-radius-{none…full}`
   (the M3 corner scale; `--md-sys-radius-default` aliases the treatment's favoured corner, here `-md`=12px)
   and `--md-sys-space-{0…9}`. Container tier = `--md-sys-inset-{control-group|card|panel|dialog|page}`,
   `--md-sys-gap-{cluster|stack-tight|stack|stack-loose|grid|section}`, `--md-sys-border-{thin|thick}`,
   `--md-sys-focus-ring-{width|offset}`. In UI code the form is always `var(--md-sys-…)`, or the
   `.md-sys-control-{step}` utility class, which wires a control's whole box in one:
   ```html
   <button class="btn md-sys-control-md">Save</button>
   ```
   ```css
   /* the .md-sys-control-md equivalent, by hand — note box-sizing + font-size, which the class also sets */
   .btn {
     box-sizing: border-box;
     block-size: var(--md-sys-size-md-height);
     min-inline-size: var(--md-sys-size-md-min);
     font-size: var(--md-sys-size-md-font);
     padding-inline: var(--md-sys-size-md-pad-edge);   /* slotless — bare text; -pad if it has a leading icon */
     padding-block: 0;
     gap: var(--md-sys-size-md-gap);
     border-radius: var(--md-sys-size-md-radius);       /* = height/2, already a pill */
   }
   ```

## The laws (violating any is a defect)

1. **Tokens, not px.** If a height, padding, margin, gap, radius, border, or outline isn't a
   `--md-sys-{size|radius|space|inset|gap|border|focus-ring}-*` var (or a `.md-sys-control-*` class), it
   doesn't go in UI code. No `height: 40px`, no `border-radius: 8px`, no `gap: 1rem`.
2. **A control is one size step; everything inside derives from it.** Pick the step (`xs…2xl`); its height,
   icon, font, and paddings all come from `--md-sys-size-{step}-*` — the centering law guarantees the glyph
   sits optically centered. Never set a control's padding independently of its height. See
   [`references/controls.md`](references/controls.md).
3. **Two paddings, by anatomy.** `--md-sys-size-{step}-pad` is the SLOT edge (a control WITH a leading
   icon); `--md-sys-size-{step}-pad-edge` is the SLOTLESS edge (a bare text button/label). ADIA `md`:
   `pad`=5px, `pad-edge`=14px. Use the one that matches the anatomy — mixing them mis-centers the content.
4. **Container spacing is the tier, not a raw `--md-sys-space-N`.** Reach for a semantic
   `--md-sys-inset-*` / `--md-sys-gap-*` first — they ARE named rungs of the space ladder, so you get the
   rhythm without guessing a number. Drop to a raw `--md-sys-space-{0…9}` only for a one-off the tier
   doesn't name. See [`references/containers.md`](references/containers.md).
5. **Radius: the M3 corner scale for containers, the height-linked corner for controls.** Containers pick a
   level off `--md-sys-radius-{xs|sm|md|lg|xl}` (or `--md-sys-radius-default`, here `-md`=12px); a control's
   own corner is `--md-sys-size-{step}-radius` = height/2 (already a full pill — needs nothing extra).
   `--md-sys-radius-full` (9999) is for round NON-controls only — avatars, dots, standalone pills. Never
   put a fixed `--md-sys-radius-*` on a control that should scale with its height.
6. **Focus ring & borders are one recipe.** `outline-width: var(--md-sys-focus-ring-width)` (2px) +
   `outline-offset: var(--md-sys-focus-ring-offset)` (2px) on every focusable element (the COLOR is the
   color skill's accent). Borders are `--md-sys-border-thin` (1px) / `--md-sys-border-thick` (2px) — never
   a hardcoded `1px`. `--md-sys-density` = 1 already rides inside the derived sizes; don't re-apply it.
7. **This export is Base-only (fixed geometry).** ADIA ships a single `Base` mode — no `@media` breakpoint
   re-declarations; the ramp is constant, a valid choice. If a kit DOES export modes, `--md-sys-size-*`
   re-declares inside `@media` blocks and `.md-sys-control-*` restyles automatically; container-tier vars
   and radii stay mode-independent. Never author fluid `clamp()`/`vw` sizing. See
   [`references/responsive.md`](references/responsive.md).

## Surface map — where to look things up

| Sizing… | Reference |
|---|---|
| Buttons, inputs, selects, toggles, chips — heights, the icon/caret/padding derivation, control radius | [`references/controls.md`](references/controls.md) |
| Cards, panels, dialogs, page layout — insets, the gap scale, section rhythm, dividers/borders | [`references/containers.md`](references/containers.md) |
| Icon sizes, the hit-target floor, focus rings, the density knob, the radius ladder vs the control pill | [`references/detail.md`](references/detail.md) |
| Breakpoint modes, what scales vs what's fixed, why THIS export is Base-only | [`references/responsive.md`](references/responsive.md) |

## Verify before you ship

- **Run the checker** — it binds the export (confirms the `xs…2xl` ramp × 9 fields, the radius scale, the
  `space-0…9` ladder, and the inset/gap/border/focus primitives all resolve, so your `var(--md-sys-…)` will
  bind) and lints your UI sources for hardcoded `px`/`rem`/`em` on a dimensional property:
  ```
  node <skill>/scripts/dimension-check.mjs <path/to/geometry.css> <src-dir-or-files…>
  ```
  A missing-token report means the bound export drifted from the assumed ramp — re-bind before trusting the
  recipes.
- A control's inner spacing uses the paired `--md-sys-size-{step}-*` (not an independent padding), and one
  step throughout — height, icon, font, and pad all the same `{step}`.
- Container spacing uses `--md-sys-inset-*` / `--md-sys-gap-*` before any raw `--md-sys-space-N`.
- Every focusable element carries the focus-ring recipe; borders are `--md-sys-border-*`, never a hardcoded
  `1px`; a control's corner is `--md-sys-size-{step}-radius`, containers use the `--md-sys-radius-*` scale.

_Provenance: the two-tier dimensional system is the nonoun geometry engine's (`src/engine/geometry.mjs`);
this skill was authored against the ADIA reference export (`geometry/geometry.css`, 2026-07-05). When the
engine regenerates the export, re-run the bind check and re-sync any changed steps/values here (the value
tables live in `references/controls.md` + `containers.md`) — owner: the kit maintainer._
