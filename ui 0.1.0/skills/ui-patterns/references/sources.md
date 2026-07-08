# Sources — provenance for the pattern claims

The catalogs distill the shared canon of interaction-design pattern literature. When a
claim needs an authority or the canon disagrees, these are the references, in trust order:

## Pattern canon
- **Jenifer Tidwell, Charles Brewer, Aynne Valencia — *Designing Interfaces*, 3rd ed. (O'Reilly, 2020)** —
  the broadest catalog; source for template/module naming conventions (master-detail, wizard,
  center-stage) and many failure modes.
- **Nielsen Norman Group (nngroup.com/articles)** — empirical grounding: form validation timing,
  breadcrumbs, tabs, empty states, notification fatigue, progressive disclosure. Prefer NN/g when a
  pattern claim needs user-research backing.
- **ARIA Authoring Practices Guide (w3.org/WAI/ARIA/apg/patterns)** — the normative interaction
  contracts (keyboard, roles, focus) for tabs, dialog, combobox, listbox, menu, grid. When this file
  and APG disagree on interaction, APG wins.

## Platform systems (convention gravity — deviate knowingly)
- **Apple Human Interface Guidelines** — sheets, navigation stacks, mobile modality.
- **Material Design 3** — component anatomy vocabulary, density, state layers.
- **Microsoft Fluent 2** — data-heavy desktop patterns (grids, command bars).

## Foundational
- **Ben Shneiderman — the mantra**: "overview first, zoom and filter, then details-on-demand"
  (dashboards, master-detail, search results all instantiate it).
- **Alan Cooper et al. — *About Face* 4th ed.** — posture (sovereign vs transient) underlying the
  shell-archetype distinctions.
- **Edward Tufte (*The Visual Display of Quantitative Information*) / Stephen Few (*Information
  Dashboard Design*)** — data-graphics honesty (zero-baseline bars, direct labeling, data-ink)
  behind the data-viz module entry.

In-corpus: the shell archetypes live in THIS pack's `references/archetype-*.md` (applied by
`layout-decompose`); interaction invariants in the verifier family; component realization in
`component-author`. Claims here that drift from those owners should be fixed HERE — they own
their layers.
