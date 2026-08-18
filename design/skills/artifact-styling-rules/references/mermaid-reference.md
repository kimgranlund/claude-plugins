# Mermaid reference — authoring and re-theming, dedicated

The question this file answers: **how do I write a mermaid diagram that survives this pipeline,
and how does it re-theme through the page's own live tokens?** Two halves, both load-bearing:
authoring (what to write) and rendering (why the CSS override works the way it does).

## Authoring half

- **Single-line node labels, always.** [incident, 2026-08-18] This pipeline's renderer strips
  `<br/>` tags inside node labels (`A["line one<br/>line two"]` does not render two lines — the
  tag is stripped or rendered as literal text). Multi-line detail moves to **edge labels**:
  `A["Coordinator"] -->|dispatches build| B["Builder"]`, never crammed into one node. This is
  `artifact_check.py`'s `br-in-mermaid-label` check.
- **Detail on edges, mechanism over inventory.** A node needing more than a short label wants an
  extra node or a sub-graph, not a longer string. Diagrams should show the actual mechanism (boxes
  + arrows for how something works), never stand in for a chip-wall enumeration
  (`shells-and-genres.md`'s mechanism-diagram-over-chip-wall rule).
- **One `:::accent` per diagram** — the single highlighted node, the hop under discussion.
  [verified, reference token file `emphasisNode`, 2026-08-18].
- **Intent classes** — `:::danger`/`:::success`/`:::warning`/`:::info`, the same
  family-soft-fill + family-stroke + on-surface-text recipe as page callouts [verified, reference
  token file `intentNodes`, 2026-08-18] — never a bespoke diagram-only color for status.
- **LR/TB guidance** — a left-right flow for a PIPELINE (steps happen in sequence, reading order
  matters); a top-bottom flow for a HIERARCHY (a tree, a decision cascade). Pick by what the
  diagram is actually representing, not by habit.

## Rendering half

### Why `!important` beats mermaid's own injected in-SVG stylesheet

**[verified, mermaid.js.org theming docs + flowchart syntax docs, accessed 2026-08-18]** Mermaid
renders to an SVG carrying its OWN inline `style="fill:#...; stroke:#...;"` attributes, injected
with `!important` and scoped to the SVG's own element id — a page-level stylesheet rule at NORMAL
specificity cannot touch them, and community reports confirm external CSS targeting mermaid's
`.node`/`.edgePath .path`/`.edgeLabel`/`.cluster`/`.label` classes at ordinary specificity is
silently overridden. **The fix is symmetric**: the page's own re-theme block must ALSO carry
`!important`, bound to the same `--c-*` custom properties as the rest of the page — this is the
one mechanism that re-themes both light and dark schemes together, never a second hand-maintained
palette for the diagram.

### The full CSS override class list

**[verified, reference token file's `mermaid` object, 2026-08-18]** — the roles a re-theme block
targets, each bound to a page token:

| Mermaid element | Bound to | Notes |
|---|---|---|
| `node` fill/stroke/text | `--chip` (or `--card-high` equivalent) / `--accent` / `--ink` | `strokeWidth: 1.2px`, font-family from the body role |
| `edge` stroke/marker | `--muted` | |
| `edgeLabel` background/text | `--paper` / `--muted` | |
| `cluster` fill/stroke/label | `--accent-soft` / `--line` / `--accent` | label styled as an uppercase kicker (interactive/mono face, 12px, 0.08em tracking) |
| `emphasisNode` (`:::accent`) | `--accent-soft` fill / `--accent` stroke | the one highlighted node |
| `intentNodes` (`:::danger`/etc) | intent-family-soft fill + intent stroke + on-surface text | same recipe as page callouts |
| `datastore` (cylinder/db shapes) | node recipe unchanged | `--tertiary` reserved for data-distinction when two node families must read apart |

**[verified, mermaid's own docs, accessed 2026-08-18]** mermaid's alternative in-syntax mechanisms
— `classDef`/`class` statements, or per-node `style` keyword — are mermaid's OWN recommended way
to customize a single diagram's colors, and they DO reliably win against mermaid's base theme.
This pack does not use them as the primary mechanism because neither binds to the PAGE's live
`--c-*` custom properties — a `classDef` bakes a literal hex at diagram-authoring time, so it
cannot re-theme when the viewer's tri-state (`platform-facts.md`) flips. The CSS-override-with-
`!important` approach is the one mechanism that stays theme-reactive; `classDef`/`style` are noted
here as the mermaid-native alternative, not adopted.

### The surface-ladder rule

**[verified, reference token file `_ladder_rule`, 2026-08-18]** — *"nodes sit one surface tier
ABOVE whatever they rest on: surface-high over paper/cluster panels — never card-over-paper (a
0.025L step reads as black boxes on dark)."* A node rendered on the page's paper background uses
the `--chip`/surface-high tier, never a single small lightness step up from paper — in dark mode a
too-small lightness delta between a node and its background reads as a solid black box rather than
a bordered shape.

### `rx=0` needs explicit radius

**[verified, reference token file `mermaid.node.radius`, 2026-08-18]** mermaid's `base` theme ships
node rectangles at `rx=0`/`ry=0` (sharp corners) by default — the re-theme block must explicitly
set `rx`/`ry` (8px, "rounded sm" per the reference implementation) via CSS; a diagram that looks
"sharp-cornered" against an otherwise rounded page is this exact gap, not a mermaid bug.

### Why CSS overrides beat `%%{init}%%` themeVariables

**[verified, mermaid.js.org theming docs, accessed 2026-08-18]** `%%{init: {'theme': 'base',
'themeVariables': {...}}}%%` is mermaid's own per-diagram config syntax, and only the `base` theme
is user-modifiable through it (`default`/`neutral`/`dark`/`forest` are static). The colors it sets
are BAKED at parse/render time — a diagram authored with a `themeVariables` init block renders
ONE static theme and cannot re-theme when the page's viewer flips light/dark afterward. A CSS
override block, by contrast, binds to the page's own `--c-*` custom properties, which already
re-theme via `light-dark()`/`color-scheme` — the diagram re-themes FOR FREE the instant the page
does, with no re-render and no second config surface to keep in sync. `themeVariables`' own
derived-variable hierarchy (`primaryColor` → `primaryBorderColor`/`secondaryColor`, etc. — [verified,
mermaid-js/mermaid's own theming docs, accessed 2026-08-18]) is real and useful for a
STANDALONE mermaid deployment, but it is solving a problem (deriving a coherent palette from one
seed color) this pipeline doesn't have, since the palette already comes fully resolved from
`token-architecture.md`'s role inventory.

## Hidden tab panels

See `type-and-layout.md`'s width-preserving hide technique (generalized from this mermaid-specific
finding: a mermaid diagram rendered inside a `display: none` tab panel measures zero width at
render time and corrupts permanently, even after the tab is shown).

Extension: governed by [[make-pack]].
