# Type and layout — the artifact's own defaults, independent of the source system

The question this file answers: **what fonts, widths, spacing, and radii does an Artifact use by
default, regardless of what the consuming project's own design system specifies?** Per
`token-architecture.md`'s colors-from-system/geometry-from-doctrine split, THIS is the geometry/
type half — the artifact's own fixed doctrine, applied unless the source system explicitly
overrides it.

## Type doctrine: system-ui body, mono interactive

**[verified, Kim's ruling per ticket #649, carried forward as shipped doctrine here]** Artifacts
default to `system-ui, -apple-system, 'Segoe UI', sans-serif` for body/reading type, and a
monospace stack (`ui-monospace, 'SF Mono', Menlo, monospace`) for **interactive elements** —
buttons, links, tabs, badges, kickers. **[verified, reference impl `typography` block, 2026-08-18]**
the reference implementation's own `interactive` role carries the identical note: *"buttons,
links, tabs, badges, kickers — per the artifact type doctrine."* This is a deliberate inversion of
the usual web convention (mono for CODE, sans for UI chrome) — here mono marks anything the reader
CLICKS, distinguishing interactive chrome from reading prose at a glance without color alone.

**Anthropic's own steering-lever findings** [verified, "Improving frontend design through Skills"
blog, accessed 2026-08-18] reinforce why this doctrine exists rather than leaving font choice to
whatever the model defaults to: Claude's untuned defaults regress to "generic, on-distribution"
choices (Inter/Roboto) because those dominate training data; explicitly forbidding the default and
naming the alternative is what actually changes the output. A fixed, named doctrine — not a
per-build judgment call — is this project's own application of that same lever.

## Width system: three tiers

- **74rem** — extra-wide content default (the handbook precedent). **[verified, reference token
  file `layout.content-max-width`, 2026-08-18]**.
- **54rem** — narrative prose width, for the narrative single-scroll shell
  (`shells-and-genres.md`). **[verified, reference token file `layout.prose-max-width`,
  2026-08-18]**.
- **62rem** — the tabbed-handbook chapter reading width, a middle tier between the two above.
  **[inferred, from ticket #650's own stated acceptance text, 2026-08-18]** — this third number is
  NOT independently verified against the reference token file (which only carries the two above);
  it is carried forward as this record's own differentiator fact. A future touch of this pack that
  finds a primary source for 62rem should amend this marker in place with a dated note, per
  pack-writing-rules' correction discipline — never silently upgrade the marker without a cite.

**Community steering findings on width/density** [verified, dev.to "Ultimate Claude Artifacts
Guide", accessed 2026-08-18]: "use asymmetry, overlap, diagonal flow for visual interest... choose
between generous negative space OR controlled density" — a general principle this project narrows
to its own three named tiers rather than leaving width an ad-hoc per-build choice.

## Spacing scale

The general grammar names each stop `--space-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`2xl`/
`3xl`/`4xl`/`5xl` (values in px, per `docs:artifact-rules`' `script-interface.md`'s emitted
contract). **[verified, reference impl `_integration.spacing`, 2026-08-18]** the reference
implementation itself subsets this to `4/8/12/16/24/32/48` for static pages (no interactive
density/size attribute API needed outside a live component library) — a static Artifact page may
legitimately use only this subset; a component-carrying artifact uses the full named scale.

## Two-tier radius

**[verified, reference impl `_integration.radius`, 2026-08-18]** radius follows a **two-tier cap**,
not one flat value: **controls cap at 12px**, **surfaces cap at 16px** — a button or input never
exceeds the controls cap even if the surface it sits on uses the surfaces cap. The reference
implementation's own resolved defaults (`rounded`: xs=6px/sm=8px/md=12px/lg=16px/full=9999px) are
one frozen resolution (`k=1`) of AdiaUI's parametric radius clamp — an artifact consuming a
DIFFERENT source system still applies the two-tier CAP RULE, even if the absolute px values differ
per system.

## Specificity pitfalls

An injected third-party inline style (a syntax highlighter's own `style="color: ..."` on a code
span, a markdown-render library's inline attributes) can out-specificity a page-level custom-
property rule the same way mermaid's own inline SVG styles do (`mermaid-reference.md`). The fix is
identical: an `!important` override scoped to that library's own emitted class, bound to the
page's `--c-*` tokens — never a blanket page-wide `!important`, and never hand-patching the
third-party output directly (that drifts the moment the library's own markup changes).

## Width-preserving tab hiding — general, not mermaid-specific

**[incident, 2026-08-18, generalized from the mermaid-specific finding]** ANY content that
measures its own layout at render time (mermaid is the worked case, but a chart library or a
canvas-based widget behaves identically) corrupts permanently if it renders inside a
`display: none` container — the measured zero-width sticks even after the container becomes
visible again. The fix, general to any such content sitting inside an initially-hidden tab panel:

```css
[data-tab-panel][hidden] {
  visibility: hidden;
  position: absolute;
  inset: 0;
  pointer-events: none;
}
```

`visibility: hidden` keeps the layout box present (so anything inside always measures a real
width) while `position: absolute` + `inset: 0` keeps the hidden panel from pushing other content
around. Never substitute `display: none` for this as a "cleaner" hide.

Extension: governed by [[make-pack]].
