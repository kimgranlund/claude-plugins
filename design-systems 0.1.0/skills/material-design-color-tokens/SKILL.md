---
name: material-design-color-tokens
description: >
  Use when choosing the COLOR of any UI whose color tokens use the Material `--md-sys-color-*` naming —
  the color/role for a button, control, text, card, modal, nav, toast, border, or state ("which
  color should this use", "what token for this background/text", "add hover/disabled colors", "wire the
  theme", "make it work in dark mode", "why is this the wrong color"). Consumption guide for the
  59-role semantic layer extending Material 3: binding palettes, M3 baseline vs. extensions
  (state families, tonal variants, surface/scrim ladders, intents as palettes), pairing laws keeping fg on
  a legal bg, per-surface role maps. Never guess a hex or raw stop. NOT for type/font/weight
  (material-design-typography-tokens); NOT for radius/spacing/density (material-design-geometry-tokens);
  NOT for the default `--c-*` grammar (`color-tokens`); NOT for designing or verifying a palette
  (make-palette / check-colors); NOT for color-space math (color-space-facts); NOT for motion
  easing/duration (material-design-motion-tokens).
disable-model-invocation: false
user-invocable: false
---

# Material Design color tokens (M3-founded, extended)

This kit's color layer is **Material Design as the conceptual foundation, extended with more semantic
roles.** It exports under M3's `--md-sys-color-*` namespace, but every palette carries **59 semantic
roles** — the M3 baseline plus nonoun's extensions. Your job is never to invent a color: pick the right
**role** from the right **palette**. Raw stops exist only as the substrate the roles reference.

## Foundation vs. extension (what's M3, what's ours)

| Material 3 baseline (recognizable M3) | The nonoun extensions (why 59, not ~26) |
|---|---|
| `-primary` / `-on-primary`, secondary, tertiary; `error` | **Intents are FULL palettes**: `info`, `success`, `warning`, `danger` — each with all 59 roles, not just one `error` |
| `-surface`, `-on-surface`, `-on-surface-variant`, `-background` | **Tonal accent variants**: `-dim` / `-bright` / `-low` / `-high` on the accent |
| `-outline`, `-outline-variant` | **Baked state families**: `-hover` / `-active` / `-disabled` on the accent, on-accent, on-surface, on-surface-variant, container, and outline (M3 leaves these to state-layer opacity — here they're real, tuned tokens) |
| `-inverse-surface`, `-inverse-on-surface` | **A 12-tier surface elevation ladder** (below) vs. M3's ~5 container tiers |
| `-surface-dim` / `-surface-bright`; opaque `surface-container-*` tiers; `-scrim` | **A 7-step scrim ladder** (`-scrim-weakest … -scrim-strongest`) vs. M3's single `scrim`; plus `-placeholder`, `-on-{p}-variant`, and `-container-low/-high` (a **translucent** tint family, distinct from M3's opaque `surface-container-*`) |

So: recognize the M3 names, but reach for the extensions — they exist precisely so you never hand-roll a
hover, a disabled, a divider, or an elevation with `opacity` / `color-mix()`.

## Bind to the project first (always step 1)

1. **Find the export.** A CSS file whose `:root` sets `color-scheme: light dark` and defines colors via
   `light-dark(...)` under the **`--md-sys-color-*`** prefix (in ADIA's case, `css-oklch/adia.css`; a
   DTCG `*.tokens.json` may sit beside it). If none exists, **stop and ask — do not fabricate tokens.**
2. **Enumerate the palettes.** Every `--md-sys-color-<slug>-050` line marks a palette. ADIA ships eight:
   `neutral` · `primary` · `secondary` · `tertiary` · `info` · `success` · `warning` · `danger` —
   but **read what's actually in the file**; slugs and counts vary per kit.
3. **Classify them.** The **chrome palette** is the lowest-chroma one — here **`neutral`** (M3's own
   tonal-palette name) — and drives backgrounds, surfaces, text, and outlines app-wide. The **brand
   accent** is **`primary`** (CTAs, links, focus, selection); `secondary` / `tertiary` are supporting
   accents. The **intent palettes** carry MEANING only, never decoration: `info`, `success`, `warning`,
   `danger` (each the full 59-role palette, not a lone `error`).
4. **Know the grammar.** Semantic = `--md-sys-color-{p}{suffix}`. The accent itself is the bare
   `--md-sys-color-{p}` (e.g. `--md-sys-color-primary`); the on-accent uses the palette's OWN slug
   (`--md-sys-color-primary-on-primary`, `--md-sys-color-neutral-on-neutral`). Raw =
   `--md-sys-color-{p}-050…950` solids and `--md-sys-color-{p}-500-{step}` translucents — **never in UI code.**
   In CSS the consumption form is always `var(--md-sys-color-…)`:
   ```css
   .btn-danger        { background: var(--md-sys-color-danger); color: var(--md-sys-color-danger-on-danger); }
   .btn-danger:hover  { background: var(--md-sys-color-danger-hover); color: var(--md-sys-color-danger-on-danger-hover); }
   .btn-danger:disabled { background: var(--md-sys-color-danger-disabled); color: var(--md-sys-color-danger-on-danger-disabled); }
   ```

## The laws (violating any is a defect)

1. **Roles, not raws, not hexes.** If a color isn't a `--md-sys-color-*` semantic role, it doesn't go in
   UI code. No `#hex`, no `oklch(...)`, no `--md-sys-color-*-500` raw stop.
2. **The pairing law.** A foreground sits only on its own palette's base family: `-on-primary` only on a
   `--md-sys-color-primary` fill (and its hover/active); the `-on-surface` family only on that same
   palette's surface / container / background tiers. **Never cross palettes mid-pair** — `neutral-on-surface`
   text on a `danger-container` fill is a violation; use `danger-on-surface`.
3. **States ship as families.** Where a role has a `-hover` / `-active` / `-disabled` sibling, use it
   verbatim — never synthesize a state with `opacity`, `color-mix()`, or a raw stop. Not every role has
   states; the references are the exact map — don't assume a sibling that isn't there.
4. **The scheme is baked in.** Every role flips via `light-dark()` — write each color ONCE, no
   `@media (prefers-color-scheme)` per-color overrides, no `.dark` class swaps. To force a subtree into one
   scheme (a preview pane, an always-dark hero), set `color-scheme: light` / `dark` on it; the roles follow.
5. **Elevation is a surface ladder, not a shadow.** Raise/recess with the tiered surfaces — dimmer↔brighter
   (`-surface-dimmest/-dimmer/-dim` … `-surface-bright/-brighter/-brightest`) and lower↔higher
   (`-surface-lowest/-lower/-low` … `-surface-high/-higher/-highest`); shadows are optional garnish. See
   containers.md for the mirror/non-mirror distinction — it's exact and easy to get wrong.
6. **On-colors are fixed light BY DESIGN (do not "fix" this).** `-on-{p}` / `-on-{p}-variant` resolve to
   the palette's light end in BOTH modes, for all palettes — a deliberate brand decision that intentionally
   overrides per-pair contrast math (e.g. white on a `warning` fill). Do not swap in black text, auto-contrast
   logic, or your own dark variant. If a client insists on a WCAG-floor on-color, raise it as a kit-level
   decision — never patch it locally.

## Surface map — where to look things up

| Building… | Reference |
|---|---|
| Buttons (all variants + states), inputs, selects, checkboxes/radios/switches, sliders, placeholder/focus/selection | [`references/interactive.md`](references/interactive.md) |
| Text hierarchy, headings, links-in-prose, code, disabled text, the accent `-dim/-bright/-low/-high` variants | [`references/text.md`](references/text.md) |
| Cards, panes, sheets, modals, canvas, page background, the 12-tier elevation ladder, dividers/borders | [`references/containers.md`](references/containers.md) |
| Status/intent UI (info·success·warning·danger), toasts/banners, overlays & the 7-step scrim ladder, skeletons, badges | [`references/feedback.md`](references/feedback.md) |
| Navs, tabs, menus, selection/highlight, links-as-chrome, icons, focus rings, data-viz series | [`references/navigation.md`](references/navigation.md) |

## Verify before you ship

- **Run the checker** — it binds the export (confirms every palette carries all 59 roles, so your
  `var(--md-sys-color-…)` will resolve) and lints your UI sources for the four forbidden defects (hex,
  color functions, raw stops, unwrapped custom props):
  ```
  node <skill>/scripts/token-check.mjs <path/to/export.css> <src-dir-or-files…>
  ```
  A missing-roles report means the bound export drifted from the 59-role assumption — re-bind before
  trusting the recipes. (The role set is a *regenerated* export, so this is also the drift gate.)
- Every fg/bg pair obeys the pairing law (same palette, matching family) — the one thing the linter can't see.
- Interactive elements use the full state family (hover, active, disabled — not just base).
- Intent palettes carry meaning only; chrome (`neutral`) and the brand accent (`primary`) carry everything else.

_Provenance: 53 of the 59 roles are the nonoun engine's own canon — `role-table.json`
(`docs/reference/data/role-table.json`, moved from `.claude/docs/spec/` in 2026-07); the remaining 6
(`-on-surface-variant-{hover,active,disabled}`, `-outline-variant-{hover,active,disabled}`) are this
kit's own ADIA-side extension, giving state families to the two "variant" roles nonoun itself doesn't.
This skill was authored against the ADIA reference export (`css-oklch/adia.css`, 2026-07-05). When the
engine regenerates the export, re-run the bind check and re-sync any changed role names here — owner:
the kit maintainer. Every role's MEANING (not its binding grammar) is mirrored in
`material-design-token-semantics` — re-sync that pack's `references/color.md` on any role rename,
addition, or removed state family too, the same trigger as this file._
