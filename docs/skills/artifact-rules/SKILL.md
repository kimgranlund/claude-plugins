---
name: artifact-rules
description: >-
  Standards for artifact/report-page authoring: consuming a design system (DESIGN.md +
  tokens.json) into `light-dark()` custom properties with mandatory font fallbacks; the house
  shell doctrine (narrative single-scroll for reports, tabbed chapters for handbooks); mermaid
  house style (single-line labels, token-driven SVG re-theme, width-preserving tab hiding); and
  the refresh procedure. Use when a question about any of these arrives without a build ask.
  Consulted by make-artifact. NOT the build itself (make-artifact); NOT authoring/grading the
  design-system source (make-design-system); NOT generic markdown rendering
  (markdown-to-markup).
disable-model-invocation: false
user-invocable: false
---

# artifact-rules — standards for artifact/report-page authoring

The four rulings that used to live only in session memory before the 2026-08-18 Estate Handbook
gap finding (#619) — six hand-rolled Python rebuilds because nothing owned this capability. Four
distinct question types, under the pack-writing-rules 3–7 axis threshold: flat consult table
below, no `references/INDEX.md` (the table IS the retrieval map).

## Consult table

| Ask | Load |
|---|---|
| "How do a DESIGN.md/tokens.json become the CSS an artifact page uses?" | `references/design-system-consumption.md` |
| "Which page shell does this content class get — narrative, tabbed, or something else?" | `references/shell-doctrine.md` |
| "Why did my mermaid diagram break / render wrong-themed / corrupt in a hidden tab?" | `references/mermaid-style.md` |
| "When and how does a shipped artifact page get refreshed?" | `references/refresh-procedure.md` |

## How to use it

1. **Classify the ask** against the table above; read only the matching file.
2. **`make-artifact` invokes this pack at each build phase** — token consumption at Phase 2,
   shell choice at Phase 3, mermaid assembly at Phase 4, the provenance footer at Phase 5. This
   pack carries the standards; `make-artifact` carries the procedure that applies them (the
   `make-doc` → `doc-writing-rules` contract, adopted verbatim).
3. **The mechanized authority for token consumption is `css_build.py`** (bundled with
   `make-artifact`), not this prose — `design-system-consumption.md` describes the mapping, the
   script IS the check (script-writing-rules' mechanization test).

## Composition

- **`make-artifact`** — the procedural sibling this pack serves; consumed the same way
  `doc-writing-rules` serves `make-doc`.
- **`design`'s `make-design-system`** — the token SOURCE this capability consumes. This pack
  owns consumption doctrine only; authoring or grading the design-system file itself is that
  plugin's job (soft cross-plugin mention, degrades gracefully where `design` isn't installed).
- **`markdown-to-markup`** — the plain markdown→DOM renderer. This pack's shell/CSS doctrine
  governs a fuller, design-system-styled page; it does not replace or extend the markdown
  grammar renderer.

## Human/browser exception, stated

Whether a rendered page's shell actually looks right, and whether a rendered mermaid SVG
actually re-themes visually, are render-shaped criteria this pack's doctrine cannot itself
verify — human render review is the stated exception (assert-layer-choice's own rule: every
human-routed criterion is written down, never a silent absence). `make-artifact`'s Done block
names this exception at build time.

Extension: governed by [[make-pack]].
