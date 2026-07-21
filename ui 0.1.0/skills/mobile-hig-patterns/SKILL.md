---
name: mobile-hig-patterns
description: >-
  Answers Apple Human Interface Guidelines (HIG) questions — its own navigation, modality, and
  component vocabulary — from a cited corpus. Use when asked "tab bar vs navigation stack", "sheet
  vs modal vs popover — which does HIG say to use", "what sheet detent heights does HIG define",
  "alert vs action sheet for this confirmation", "HIG's button style guidance", "grouped vs plain
  list", "swipe action conventions", "what belongs in a nav bar vs a toolbar", or "where should
  search live in this navigation hierarchy". Carries HIG's stated navigation-model guidance,
  modality/sheet-detent behavior, alert/action-sheet/sheet escalation, button-style vocabulary,
  list/swipe conventions, and nav-bar/toolbar/search placement — cited to specific HIG pages.
  ANSWERS HIG's semantics; does not name page-shell regions (ui-patterns), animation timing
  (motion-design), or icon sizing (icon-rules). NOT Android/Material guidance
  (material-design-*-tokens); NOT building the component (component-forge).
user-invocable: false
disable-model-invocation: false
---

# mobile-hig-patterns — the Apple HIG world model

Answers what Apple's Human Interface Guidelines actually say about navigation, modality, and
component choice — from a cited, dated corpus — so a mobile design decision reasons from HIG's own
stated rules instead of a remembered screenshot of some other app.

| Ask | Load |
|---|---|
| Tab bar vs navigation stack vs flat navigation; nav-bar/toolbar/search placement | `references/navigation.md` |
| Sheets, detents, modals, popovers — HIG's modality model | `references/modality-and-sheets.md` |
| Alerts vs action sheets vs sheets; buttons; grouped/plain lists; swipe actions | `references/components.md` |
| Provenance and the unverified edges | `references/sources.md` |

## Consult procedure

1. Classify the ask: navigation model · modality/sheets · component choice. Load only the matching
   reference.
2. Answer on the contract: **claim + cited HIG page + the failure mode HIG's rule prevents**. A
   pattern recommendation without HIG's own stated rationale is a guess wearing HIG's name.
3. State which register the answer comes from: HIG-cited vs. ecosystem convention not directly
   sourced from developer.apple.com — and say so when it's the latter (see `sources.md`'s
   unverified-edges list; HIG does not centrally publish every convention this pack might be asked
   about).
4. Route shell/motion/icon/build work at the boundary (below) — this pack never emits a wireframe,
   a spring value, or component code.

## Boundaries

- **This skill answers HIG's own navigation/modality/component semantics; it does not name page
  regions, animate anything, size an icon, or build anything.**
  - Page-shell region naming (header/view-scroll/bottom-tab-bar/sheets as REGIONS on a screen) →
    `ui-patterns`' `references/archetype-mobile-app.md` (applied by [[layout-decompose]]) — this
    pack explains what a tab bar or sheet IS FOR and when HIG says to reach for it; that file
    names where it sits on the screen.
  - Spring/animation timing values (Apple's spring model, durations) → [[motion-design]] — already
    the house default for motion generally; this pack never restates spring numbers.
  - Icon construction and sizing (SF Symbols weights, grid, sizing) → [[icon-rules]] — already
    covers SF Symbols in its per-system construction table; this pack covers HIG's *button* and
    *navigation* vocabulary, not icon geometry.
- **Android/Material's equivalent guidance** → `material-design-*-tokens` (design-kits plugin,
  where installed) — a different platform's own stated rules; this pack is Apple-specific.
- **Building the actual component** → [[component-forge]] — this pack cites HIG's rule; it never
  emits a wireframe or component code.

## Extending this pack

A missing axis, a stale reference (a HIG revision changes stated guidance), or "add X" is
authoring work — route to [[pack-forge]] (grounded research waves, one axis per wave); never bolt
an uncited claim onto the corpus inline.
