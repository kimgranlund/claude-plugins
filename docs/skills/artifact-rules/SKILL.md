---
name: artifact-rules
description: >-
  Procedure-side standards for artifact/report-page authoring: classifying a content source
  (report/retro vs handbook vs both), composing content from a project's own records tree
  (Intent/User-Story/Concept/System layers to chapters), the `css_build.py` script interface, and
  the provenance-footer/refresh procedure. Use for a standards question with no build ask.
  Visual/styling doctrine (tokens, type, mermaid, shells) lives in design's artifact-styling-rules
  — cited, not restated. Consulted by make-artifact. NOT the build itself (make-artifact); NOT
  visual styling doctrine (artifact-styling-rules); NOT generic markdown rendering
  (markdown-to-markup).
disable-model-invocation: false
user-invocable: false
---

# artifact-rules — procedure-side standards for artifact/report-page authoring

Slimmed 2026-08-18 (#650): the visual doctrine this pack used to carry (token consumption's WHY,
shell/genre taste, mermaid house style) moved wholesale to `design:artifact-styling-rules` — a
hard fence, never duplicated on either side. What stays here is procedure only: 4 declared axes
(content classification, composition, the script interface, refresh) since 2026-08-19's
`composition-model.md` addition (#649), flat consult table below, no `references/INDEX.md`
(pack-writing-rules' enumerability rule).

## Consult table

| Ask | Load |
|---|---|
| "Is this content a report, a handbook, or both?" | `references/content-structure.md` |
| "How does a project's own records tree become chapters/sections?" | `references/composition-model.md` |
| "What does `css_build.py` actually take and emit?" | `references/script-interface.md` |
| "When/how does a shipped artifact get refreshed?" | `references/refresh-procedure.md` |

**Anything about how it should LOOK — theme, tokens, type, mermaid, shell taste — routes to
`design:artifact-styling-rules` instead** (soft cross-plugin mention, degrades gracefully where
`design` isn't installed). This pack never re-answers a visual question; it points.

## How to use it

1. **Classify the ask** against the table above; if it's visual rather than procedural, hand off
   to `design:artifact-styling-rules` instead of answering from here. Grep the routed file for the
   specific term first, then Read the section it lands in — this is a catalog, not a linear read.
2. **Answer with the claim, the cited file, and any stated exception** — never a bare assertion.
3. **`make-artifact` invokes this pack at each build phase** — the records-tree composition phase
   at Phase 1b (records-tree content sources only), content classification at Phase 3, the script
   contract at Phase 2, the provenance footer at Phase 5. This pack carries the procedure;
   `make-artifact` carries the build that runs it (the `make-doc` → `doc-writing-rules` contract,
   adopted verbatim).

## Composition

- **`make-artifact`** — the procedural sibling this pack serves.
- **`design:artifact-styling-rules`** — the visual-doctrine sibling (Resolution 3 of lld-0020):
  token architecture, type/layout, mermaid, shells/genres. Cited for every "why it looks this way"
  question; never restated here.
- **`design`'s `make-design-system`** — the token SOURCE `script-interface.md`'s contract
  consumes; authoring/grading it is that plugin's job.
- **`markdown-to-markup`** — the plain markdown→DOM renderer; this pack's fuller,
  design-system-styled page is a different, heavier render path.

## Human/browser exception, stated

Whether a rendered page's shell actually looks right, and whether a rendered mermaid SVG actually
re-themes visually, are render-shaped criteria neither pack can verify — human render review is the
stated exception. `make-artifact`'s Done block names this exception at build time.

Extension: governed by [[make-pack]].
