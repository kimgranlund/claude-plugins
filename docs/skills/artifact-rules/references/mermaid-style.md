# Mermaid house style — how diagrams survive this pipeline

The question this file answers: **what breaks a mermaid diagram in an Artifact/report page, and
what's the fix?** All three rules below are [incident]-grounded: learned 2026-08-18 building the
Estate Handbook, the gap finding that motivated this whole capability (#619) — encoded here so
the next build doesn't re-learn them by trial and error.

## `<br/>` is stripped from mermaid node labels

**Node labels are single-line, always.** This pipeline's mermaid renderer strips `<br/>` tags
inside node labels (`A["line one<br/>line two"]` does not render two lines — the tag is
stripped, or renders as literal text, depending on the render path; either failure mode is
avoidance-worthy). Multi-line detail moves onto **edge labels** instead:

- **Wrong:** `A["Coordinator<br/>dispatches build"]`
- **Right:** `A["Coordinator"] -->|dispatches build| B["Builder"]` — the detail rides the edge,
  the node stays one line.

A node needing more than a short label is a signal the diagram wants an extra node or a
sub-graph, not a longer string crammed into one box.

## Re-theming a rendered SVG requires token-driven `!important` overrides

Mermaid renders to an SVG carrying its own **inline** `style="fill:#...; stroke:#...;"`
attributes baked in at render time — a page-level stylesheet rule at normal specificity cannot
touch them; only `!important` wins against an inline style. The re-theme block
`css_build.py` emits (see `design-system-consumption.md`) targets the mermaid SVG's structural
classes (node fills/strokes, edge paths, node/edge labels) with `!important` declarations bound
to the page's own `--c-*` custom properties — so both light and dark schemes re-theme through
**one mechanism**, never a second hand-maintained palette for the diagram.

## Hidden tab panels: `visibility`, never `display: none`

**The corruption is permanent, not cosmetic.** Mermaid measures its container's dimensions at
render time. If that container is `display: none` when the diagram renders (a mermaid block sits
inside a tab panel that starts hidden — see `shell-doctrine.md`'s tabbed-handbook shell), the
measured width is zero and the diagram lays out corrupted — **even after the tab is later shown
and the panel becomes visible again.** The container's dimensions were wrong at the moment that
mattered; showing the panel later does not re-trigger a re-measure.

The fix is a **width-preserving hide**: keep the panel's layout box present (so mermaid always
measures a real width) and hide it visually instead —

```css
[data-tab-panel][hidden] {
  visibility: hidden;
  position: absolute;
  inset: 0;
  pointer-events: none;
}
```

`visibility: hidden` (not `display: none`) keeps the box in the layout; `position: absolute` +
`inset: 0` keeps it from pushing other content around while hidden. Never swap this for
`display: none` as a "cleaner" hide — that is exactly the corruption class this rule exists to
prevent.

## Where the mechanism lives

The doctrine is here; the mechanism is `css_build.py`'s emitted re-theme block and
`make-artifact`'s assembly phase (which wires the tab-panel hiding CSS and never lets a mermaid
block render inside a display:none container). Consult this file for WHY; consult the script/
skill body for WHAT gets emitted.
