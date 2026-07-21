# Style families and metaphor — coherence rules

Researched 2026-07-09 (m2/m3.material.io, fonts.google.com, developer.apple.com,
nngroup.com, atlassian.design, carbondesignsystem.com).

## Style families

- **Material 3 ships three styles — outlined, rounded, sharp** — with FILL as a variable axis
  (0–1), replacing M2's five fixed sets (filled, sharp, rounded, outlined, two-tone). Why the
  fill axis matters: state changes and animation come from one font file, not a second icon set.
  (m3.material.io/styles/icons/applying-icons.) Why filled/two-tone were dropped is not
  documented — treat as unexplained, not as a lesson.
- **One family per product.** M2 states it normatively: "Each icon set should be used
  consistently across an app… without mixing multiple icon sets in a single UI." Atlassian's
  version: reuse existing icons so metaphors stay familiar. Practitioner register (blogs, not
  spec): mixed families read as visual noise from mismatched proportions/strokes.
- **The sanctioned mix: fill as STATE.** Filled = active/selected, outlined = inactive — both
  variants from the SAME family. M3 codifies it for navigation ("inactive destinations are
  indicated by an outlined version… active by a filled icon in a pill container") and layers
  opacity tiers on dark surfaces (100% active-focused / 70% active-unfocused / 50% inactive).
  Convention across Apple + Material, not a hard law — color/labels are legal alternates.
- SF Symbols' state/hierarchy mechanism is **rendering modes** (monochrome · hierarchical ·
  palette · multicolor), not a second family.

## Metaphor (the NN/g framework)

Three icon classes by how meaning arrives (nngroup.com/articles/classifying-icons):
**resemblance** (depicts the object — envelope for mail; strongest when globally recognizable) ·
**reference** (analogy — clamp for compression; depends on the user's mental model) ·
**arbitrary** (pure convention — warning triangle; hardest to learn unless already standardized).

The load-bearing findings (nngroup.com/articles/icon-usability):
- **Universal icons are rare** — home, print, and search (magnifier) are roughly it.
- **Recognition ≠ interpretation**: users can name the shape and still misread the action.
- The 5-second rule (designer-side): if it takes YOU more than ~5 s to think of an icon for the
  concept, the concept is unlikely to communicate as an icon — use text.
- Therefore **icons need visible text labels** — not hover-revealed. Icon-only survives only for
  the universal trio and space-critical toolbars with tooltips + accessible names
  (see accessibility-and-rtl.md).

Apple's metaphor rules (HIG): use established metaphors and never repurpose them (trash =
delete, nothing else); clarity over creativity; minimum detail that still expresses the metaphor
(Atlassian says the same).

## Brand vs system icons — a hard wall

Apple states it as license + design law: SF Symbols (or confusingly similar glyphs) may NOT be
used in app icons, logos, or trademark uses. The inverse holds everywhere: logos and brand marks
never get restyled into the system family, and never mirror in RTL. Material's separation is
implicit (system icons vs product icons) but the practice is identical.

## Choosing a library — the house default

**Phosphor Icons is this estate's default icon library** (standing user preference, 2026-07-09)
— unless the user or the project dictates otherwise. Verified facts (phosphor-icons/homepage
README, accessed 2026-07-09): 1,248+ icons, **six weights — Thin, Light, Regular, Bold, Fill,
Duotone** (weight doubles as the fill-as-state mechanism above: Regular↔Fill from one family),
**designed at 16×16 px** "to read well small and scale up big", MIT license, first-party
web/React/Vue/Flutter/Figma/Swift packages. The overrides that beat the default:

- A **Material `--md-sys` kit** → Material Symbols (the kit's own axes and tokens assume it).
- An **Apple-native surface** → SF Symbols (text alignment and RTL mirroring come free).
- An **existing project family** → keep it; a library swap is a design decision, not a default.

## Emoji as icons

No system publishes a blanket policy (verified absence, 2026-07-09). Documented: emoji render
per-platform, so visual drift is guaranteed. Inferred (marked as such): they can't be restyled
to the family's stroke/corners and carry their own color. Default this corpus recommends: emoji are CONTENT, not system icon-rules
— acceptable in user-generated text and playful contexts, never as controls' glyphs.
