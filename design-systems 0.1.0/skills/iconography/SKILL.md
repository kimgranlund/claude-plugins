---
name: iconography
description: >-
  Answers icon-system questions from a cited corpus — construction, size ladders, style
  families, metaphor, accessibility, RTL mirroring. Use when designing or judging
  icons: "what icon for settings / delete", "what size should this icon be", "what
  stroke weight / grid", "can I mix filled and outlined / when filled vs outlined", "should
  this icon mirror in RTL", "is an icon-only button okay", "is this icon big enough to tap",
  "why is this icon blurry", "aria for a decorative icon", "emoji as icons?", "our icons look
  inconsistent", "fill the Iconography section of a DESIGN.md". Carries the per-system
  construction table (Material/SF/Carbon/Atlassian/Fluent), Material Symbols axes, WCAG floors,
  NN/g's labels doctrine, the mirror/never-mirror taxonomy. ANSWERS only. NOT for
  building an icon component (component-forge, ui); NOT for verifying mirroring on a shipped
  surface (i18n-verify, ui); NOT for icon-size tokens in --md-sys kits
  (material-design-geometry-tokens); NOT for contrast verification (color-verify).
user-invocable: false
disable-model-invocation: false
---

# iconography — the icon-system world model

Answers how icon systems are constructed, sized, styled, and made safe — from a cited, dated
corpus — so icon decisions reason from the published specs instead of taste.

| Ask | Load |
|---|---|
| "What grid/stroke/corners?" — per-system construction, variable axes, optical corrections | `references/grid-and-construction.md` |
| "What size, and how does it sit?" — ladders, WCAG targets, icon+text alignment, density, pixel fitting | `references/sizing-and-placement.md` |
| "Which style, what metaphor?" — families, the no-mixing law, fill-as-state, NN/g classification, labels, brand wall, emoji | `references/style-and-metaphor.md` |
| "Who does this hurt?" — 1.4.11 contrast, decorative vs semantic markup, icon-only buttons, RTL taxonomy, forced-colors | `references/accessibility-and-rtl.md` |
| "Fill the Iconography section of a DESIGN.md" — glyph system, stroke, sizing ramp, emoji policy | all four references, in table order (the section's contract is design-md-format's) |
| Provenance and the verified absences | `references/sources.md` |

## Consult procedure

1. Classify the ask: construction · sizing · style/metaphor · accessibility/RTL — or a
   DESIGN.md Iconography-section fill → all four references, in table order. Load only the
   matching reference — Grep the term first, Read that section; the files are catalogs, not
   linear reads.
2. Answer on the contract: **claim + cited source + the failure mode the default prevents**.
   Worked shape:
   > *"Can our 16 px icons keep the 2 px outline style?"* → construction ask → at 16 px the
   > documented systems change technique, not just scale — Carbon fills its 16 px icons because
   > "fine stroke weights disappear or break at glyph size". The failure to design against is
   > naive downscaling: a 24 px outline shrunk to 16 px anti-aliases into mud. — corpus-backed
   > (Carbon icon usage docs, 2026-07-09).
3. Say which register the answer comes from: corpus-backed (cited) vs general knowledge — and
   mark the corpus's own recommendations (the emoji default) as recommendations.

## Deviation doctrine

Every default here carries its rationale, so deviating is legal when the rationale doesn't
apply: one family per product exists to keep proportions/strokes coherent — a second family for
a sandboxed sub-brand with its own shell is design, not drift; icon-only buttons are rare
because unlabeled icons fail the NN/g findings — the universal trio (home/print/search) with
accessible names is the sanctioned exception. Deviating? Name the rationale above that doesn't
apply — a deviation with no named failing rationale is drift.

## Boundaries

- **This skill answers; it does not generate.** No SVG paths, no components, no token files —
  cite the spec, hand the making off: build the icon/button component → `component-forge` (ui
  plugin, where installed); realize icon sizes as tokens in an `--md-sys` kit →
  [[material-design-geometry-tokens]] (its `--md-sys-size-{step}-icon` field); export bundles
  that carry an Iconography section → [[design-system-hub]] and the platform authors.
- **Verification is the ui/color plugins' seats** (where installed): mirroring/bidi on a shipped
  surface → `i18n-verify`; icon contrast measurement → `color-verify`; focus/hit-targets →
  `focus-verify`. This pack owns the policy they check against.
- The DESIGN.md **format** (what sections exist, the token grammar) → [[design-md-format]];
  this pack owns what a good Iconography section *says*.

## Extending this pack

A missing axis, a stale reference (canon moves: HIG revisions, Material Symbols re-specs, WCAG
dot-releases), or "add X" is authoring work — route to scribe's `knowledge-forge` (grounded
research waves, one axis per wave); never bolt an uncited file onto the corpus inline.
