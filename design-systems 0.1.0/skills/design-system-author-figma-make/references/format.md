# Figma Make — Platform Ground Truth

Everything a generator must know about how Figma Make consumes a design system.
Self-contained: no fact here requires a file outside this skill bundle.

derived-from:
- "Figma Make: Write design system guidelines" — developers.figma.com/docs/code/write-design-system-guidelines/ (fetched 2026-07-05). Re-verify on Make releases; the format is convention, not versioned schema.
- "Design System Files for LLMs" (universal spec, v0.1, 2026-07-05) — §6 encoding, §6.5 Ultimate Tokens naming grammar, §7 reduction, §8 gates; the Figma Make conformance profile minted under its §10.4.

## 1. File layout

Guidelines live in `guidelines/` inside the Make kit. The documented minimal shape:

```
guidelines/
├─ Guidelines.md        # entry point — "the initial set of guidelines Figma Make always looks at first"
├─ setup.md             # technical wiring: CSS imports, providers, build rules (only when a code package exists)
├─ components/
│  ├─ overview.md       # catalog + decision trees routing to per-component files
│  └─ button.md …       # one file per component
└─ foundations/
   ├─ color.md          # token tables, naming patterns, decision trees, rules
   ├─ typography.md
   └─ spacing.md
```

The exact name `Guidelines.md` at the folder root is load-bearing — it is the entry.
Everything else is convention Make tolerates: any folder structure, any section names;
unknown files are simply routed to or ignored.

## 2. Consumption model — a routed prompt reader

Make is the third consumer shape under the universal spec: Stitch is a *strict parser*
of one file, Claude Design is a *prompt reader* of one bundle, Figma Make is a **routed
prompt reader** — it reads `Guidelines.md` first, then follows links and folder
structure to only the files a task needs.

- **`Guidelines.md` is read first**; it must carry the product character, the hard
  rules, and the routing to granular files.
- **Overview files are routers**: catalogs and ASCII decision trees that "help Figma
  Make find only what it needs."
- **Progressive disclosure is the sizing rule**: "multiple short guidelines files are
  better than a few large files" — the docs frame file granularity explicitly around
  the context window. Consequence: structure IS the prompt; a single-file export
  flattened into `Guidelines.md` is legal but fights the platform's documented sizing
  rule.
- **Imperative voice is the documented best practice**: "'Do not use small text for
  anything except captions' is better than 'use small text sparingly'." Prohibitions
  may be marked IMPORTANT.
- **Make can auto-generate initial guidelines** from a design package; hand-authored
  guidelines override and refine that baseline — so an authored folder must be more
  specific than what Make would generate itself, or it adds nothing.
- **No published linter and no schema** — structure is convention, not validation;
  every verification gate falls to the generator (this skill's checker run is the gate
  of record).

## 3. Content shapes the docs endorse

| Shape | Where | Example from the docs |
|---|---|---|
| Token tables with purpose column | foundations/*.md | `--brand-primary` (primary actions, small accents only) |
| Composite type classes | typography.md | `text-title` (24px, 600, 1.4) → page titles |
| ASCII decision trees | overview + token files | "which token should I use?" flowcharts |
| Props/variant tables + closed variant sets | components/*.md | "Valid variants are `primary`, `neutral`, `subtle` — nothing else" |
| Explicit prohibitions | Guidelines.md, per-component rules | "Do NOT use brand-primary as backgrounds for large areas" |
| Correct-vs-incorrect code examples | components/*.md | paired do/don't snippets |

## 4. What the universal spec adds (facts the platform docs don't state)

The platform docs say how Make reads; the universal spec says what the content must be.
Both bind:

- **Values are terminal.** The model emits values verbatim; it is not a derivation
  engine. Every value — dark counterpart, hover state, on-color — ships explicit,
  precomputed, verified. OKLCH is the default payload (`oklch(L C H)`, alpha in the
  value); runtime is OKLCH-native (`oklch()` Baseline 2023, `light-dark()` Baseline
  2024).
- **15–25 roles** is the working band. Full ramps never ship in consumption files.
- **Scheme pairs, not transforms.** Every role states a light AND a dark value;
  identical role inventory across schemes. Runtime idiom: `color-scheme: light dark`
  on `:root` + one `light-dark(light, dark)` custom property per role. **Trap:**
  without `color-scheme: light dark` the second argument never fires — the two lines
  ship together, always.
- **Pairing law.** Text on a fill uses that fill's own on-token; the pair differs by
  scheme; crossing a pair fails contrast in one scheme.
- **States as values (reduction rule R3).** Hover/active/focus/disabled land as
  literal per-scheme values, never adjectives — "hover brightens slightly" yields
  per-generation drift.
- **The reduction is re-verified, not trusted (R4).** Upstream verification does not
  survive projection; every gate runs on the reduced artifact. The classic silent bug:
  all foregrounds collapsed to constant `#FFFFFF`, dark-scheme fills landing 3.1–3.7:1.
- **Prose and tokens reduce together (R2/R5).** Every color the character prose sells
  exists as a token; a cut family loses its prose in the same change.

## 5. Divergence from the sibling platforms

| Concern | Stitch (alpha) | Claude Design | Figma Make |
|---|---|---|---|
| Unit consumed | one DESIGN.md | DESIGN.md + tokens.json + previews | `guidelines/` folder tree |
| Reader type | strict parser | prompt reader | routed prompt reader |
| Entry point | frontmatter + section grammar | the spine is the prompt | `Guidelines.md`, then links |
| Machine tokens | YAML frontmatter | tokens.json | none — tables in prose |
| Sizing pressure | one file, ordered sections | prompt budget | context window via many small files |
| Native gates | lint (9 rules) | none | none |
| Voice | prose doctrine, declarative | prompt spine | explicitly imperative |

Two properties are Figma-Make-specific: **routing as a first-class artifact** (the
router files are content the other platforms don't need) and the **setup contract**
(`setup.md` wires the kit's package — absent when no code package ships).

## 6. Conformance checklist (the profile; receipt records results per build)

- `Guidelines.md` exists; carries character, hard rules, and a routing table naming
  every leaf file that exists (no dangling routes, no unrouted leaves)
- Token tables carry the canonical fixed values; fill/foreground pairs ≥ 4.5:1 in both
  schemes (all-pairs policy)
- Scheme parity: every role row states both light and dark values
- Signature roles present with usage boundaries (prose–token accord)
- Component files list closed variant sets and literal state values per scheme
- Cross-carrier equality with sibling exports when they exist (same build, same values)

Gate mechanics and the receipt template: `gates.md` in this folder.
