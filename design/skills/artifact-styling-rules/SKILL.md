---
name: artifact-styling-rules
description: >-
  Standards for styling/authoring Claude Artifacts: runtime constraints (CSP inlining, 16MB
  cap, theme tri-state, body-ground, native mermaid); the token role-alias method
  (light-dark() build-time CSS, never a re-ramp); type/layout doctrine (system-ui body, mono
  interactive, width/spacing/radius scales); the mermaid authoring + re-theming contract;
  shell/genre doctrine (narrative vs tabbed, hero-as-thesis). Use for "why do the colors look
  off", "why sharp corners", "diagrams look off-theme", "what font/type for buttons, tabs,
  interactive elements in an Artifact", or any Artifact styling question with
  no build ask. NOT the build (make-artifact); NOT the token source (make-design-system); NOT
  chart color (dataviz).
disable-model-invocation: false
user-invocable: false
---

# artifact-styling-rules — styling and authoring doctrine for Claude Artifacts

5 declared axes (pack-writing-rules' 3-7 threshold), flat consult table below, no
`references/INDEX.md` — the table IS the retrieval map. `docs:artifact-rules` is this pack's
procedural sibling (the `make-doc` → `doc-writing-rules` contract, same shape): it owns WHEN in a
build to apply this doctrine and how staleness is detected; this pack owns WHAT the doctrine
actually is.

## Consult table

| Ask | Load |
|---|---|
| "What can/can't an Artifact page actually do at runtime — CSP, size, theme signal, storage?" | `references/platform-facts.md` |
| "How do a project's design tokens become the CSS custom properties this page uses?" | `references/token-architecture.md` |
| "What fonts/widths/spacing/radius does an Artifact use by default?" | `references/type-and-layout.md` |
| "Why did my mermaid diagram break, render wrong-themed, or corrupt in a hidden tab?" | `references/mermaid-reference.md` |
| "Which page shell/shape does this content get, and what should it look like?" | `references/shells-and-genres.md` |
| "Score or grade a rendered Artifact page against this pack's doctrine" | `references/rubric.md` |

## How to use it

1. **Classify the ask** against the table above; Grep the matching file for the specific term
   first, then Read the section it lands in — this is a catalog, not a linear read.
2. **Answer with the claim, the cited file, and any grounding marker** (`[verified]`/`[inferred]`/
   `[incident]`/`[drift-prone]`) — e.g. "mermaid's own inline styles carry `!important` scoped to
   the SVG id, so an external override must too, per `mermaid-reference.md` [verified,
   2026-08-18]." Never a bare assertion with no citation.
3. **`docs:make-artifact` invokes this pack at each visual decision point** — token consumption,
   shell choice, mermaid assembly — the same way it invokes `docs:artifact-rules` for procedure;
   the two packs are consulted together, never one standing in for the other.
4. **`scripts/artifact_check.py` is the mechanized authority** for the six named-bug checks
   (theme-block-only colors, external URLs, literal colors outside `:root`, `<br/>` in mermaid
   labels, missing ground/color-scheme, off-doctrine font stacks) — its `selftest` proves the
   rule; `references/rubric.md`'s R1-R8 covers the judgment layer these checks can't reach
   (shell fit, readability, hero-as-thesis).

## Composition

- **`docs:make-artifact`** — the procedural build this pack serves; consumed the same way
  `doc-writing-rules` serves `make-doc` (soft cross-plugin mention, degrades gracefully where
  `docs` isn't installed).
- **`docs:artifact-rules`** — the procedural sibling: content-structure classification,
  provenance-footer stamping/refresh triggers, and the `css_build.py` script interface contract.
  This pack cites it back for "when/how," never restates it.
- **`make-design-system`** — the token SOURCE this pack's `token-architecture.md` consumes.
  Authoring or grading the design-system file itself is that skill's job; this pack owns
  consumption-into-an-artifact doctrine only.
- **`dataviz`** — chart/graph color and mark-spec doctrine lives there; this pack's mermaid axis
  is diagram STRUCTURE and re-theming, never data-encoding choices.
- **`screens:break-down-layout`** — general (non-artifact) screen layout critique lives there.

## Human/browser exception, stated

Whether a rendered shell actually looks right and whether a themed mermaid SVG actually re-themes
in a real browser are render-shaped criteria this doctrine cannot itself verify — `make-artifact`'s
Done block names this exception at build time (assert-layer-choice's own rule: every human-routed
criterion is written down, never a silent absence).

Extension: governed by [[make-pack]].
