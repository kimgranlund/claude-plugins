# Platform Map — the three consumers and the core+profiles architecture

Derived from: the universal spec *Design System Files for LLMs* v0.1 + *Figma Make Design
System Guidelines* v0.1 (NONOUN Ultimate Tokens repo, 2026-07-05), which are themselves
derived from the Google Stitch DESIGN.md spec (version **alpha**,
github.com/google-labs-code/design.md), the observed Claude Design bundle format, and
developers.figma.com/docs/code/write-design-system-guidelines/ — all fetched 2026-07-05.
Platform detail beyond this comparison layer lives with the owning sibling
(`make-dscard-kit` / `-google-stitch` / `-figma-make`); re-derive this
map when any platform's spec version bumps.

## The three reader shapes

Every platform decision follows from how the platform **reads** — one axis, three points:

| | Google Stitch | Claude Design / Claude Code | Figma Make |
|---|---|---|---|
| **Reader type** | strict parser | prompt reader | routed prompt reader |
| **Unit consumed** | one DESIGN.md (YAML frontmatter + 8 canonical sections) | DESIGN.md + tokens.json + `@dsCard` previews | `guidelines/` folder tree entered at `Guidelines.md` |
| **Machine tokens** | YAML frontmatter, `{path.to.token}` refs | `tokens.json` flat role maps | none — tables in prose |
| **Dark scheme** | none in schema — `-dark` suffix siblings ride tolerance | `colors` / `colorsDark` paired maps | per-scheme columns in token tables |
| **Native gates** | lint, 9 rules (`broken-ref` the only error; contrast on component pairs, light end only) | none published | none |
| **Gate of record** | lint + the generator's run (dark scheme, all pairs, prose) | the generator's run — entirely | the generator's run — entirely |
| **Sizing pressure** | one file, ordered sections | prompt budget | context window via many small files (progressive disclosure) |
| **Voice** | prose doctrine, declarative | the spine is the prompt | explicitly imperative (`Do NOT …`, IMPORTANT) |
| **Tolerance** | unknown sections preserved; unknown tokens accepted if valid | reads anything | any structure; unrouted files ignored |
| **Declared flavor** | the universal dialect, as-is | the universal bundle, as-is | **React + Tailwind + shadcn/ui** (2026-07-05 decision — see below) |
| **Owning sibling** | make-stitch-kit | make-dscard-kit | make-figma-make-kit |

**Figma Make's flavor decision (resolves a real misalignment, not a preference):** a
second-pass fetch of Figma Make's own docs showed its ecosystem convention is a
two-part `--{category}-{role}` vocabulary consumed via Tailwind utility classes —
not the three-part Ultimate Tokens grammar used raw, and not `light-dark()` (Figma's
docs never mention it; the platform's own dark-mode convention is a `.dark`
class-toggle). Rather than force the same encoding onto a platform whose real runtime
is React + Tailwind + shadcn/ui, the sibling now **compiles into shadcn's own CSS-
variable shape** (`styles.css` + `@theme inline`) as a *profile* of the same
canonical model — the naming grammar stays the authoring source, shadcn's vocabulary
is the projection this platform actually reads. Full mechanism + the four doctrine
overrides (dark mode, states, components, extension roles):
`make-figma-make-kit/references/shadcn-tailwind-flavor.md`. This is the
one platform where the core+profile boundary now includes a *third* artifact type
(a real compiled stylesheet, not just markdown prose) — recorded here because it
changes what "the core" must supply for this platform specifically.

The decisive asymmetry: **one strict parser, two prompt readers.** The universal dialect
therefore adopts Stitch's grammar as its skeleton — satisfying the strict consumer costs
the tolerant consumers nothing, while the reverse forfeits the only native linter in the
set.

## Choosing platforms

- **The platform is usually given, not chosen** — it is wherever the team generates UI.
  When the ask genuinely is "which tool", answer from the reader model: Stitch buys a
  linter and a portable single file; Claude Design buys previews (`@dsCard` cards ground
  the model in rendered examples) and a first-class dark scheme; Figma Make buys
  progressive disclosure for large component catalogs. Cost side: Stitch's alpha schema
  has no color-scheme axis (dark rides as documented `orphaned-tokens` warnings); Claude
  Design and Make validate nothing, so every gate falls to your build.
- **Serving two or more platforms → build the canonical core once** and export per
  profile. N independently-authored systems are N sources of truth and N² drift
  surfaces.
- **When the ask names one platform and one artifact → route to the sibling whole.**

## Core + profiles — the architecture

One canonical fileset, plus a receipt per platform:

```
corpus/
├─ DESIGN.md            # universal dialect — Stitch-canonical sections 1–8
│                       #   + Responsive Behavior + Agent Prompt Guide (ride tolerance)
├─ tokens.json          # flat role maps, colors/colorsDark — Claude consumes; Stitch ignores
├─ components/*.html    # @dsCard previews — Claude consumes; Stitch ignores
└─ profiles/            # per-platform receipts (or per-export README.md receipts)
```

- **The core owns every design fact.** Roles, values, scales, states, rationale — stated
  once. A profile records how a platform consumes the core and certifies which checks
  passed; a profile that introduces a design fact is a fork.
- **Profiles are receipts, not forks** — regenerated on every build; a hand-edited
  receipt is a second source of truth.
- **Distribution layout is free; the facts are not.** Materializing per-platform upload
  folders is legal (the reference implementation ships `design-system-for-{claude-code,
  google-stitch,figma-make}/`) provided the invariants hold: core files byte-identical
  wherever they recur, all carriers value-equal from the same build (±1/255 per sRGB
  channel, notation-aware), and a receipt per folder.
- **Figma Make is the documented projection case**: its folder shape cannot be served by
  the single-file core, so it takes a *derived projection* of the same build — recorded
  in its profile; the core's shape stays fixed.

## Minting a new platform's profile

Mint from the platform's **published spec** — memory drifts; the spec is ground truth —
by resolving four questions:

1. **Which core files does it read?** (Everything else is ignored, at zero cost.)
2. **Strict parser or prompt reader?** A strict parser's grammar constrains the core's
   skeleton; a prompt reader constrains only clarity.
3. **Which gates does it enforce natively?** Everything it does not enforce moves to the
   generator's checklist — the gate-of-record principle.
4. **What does it tolerate?** Unknown-content behavior is the room the core's supersets
   ride in. A platform that *rejects* unknown content takes a derived projection —
   recorded in its profile, the only case where per-platform emit re-enters.

A new profile lands as: this map gains a column, the profile checklist lands with the
receipt, and — if the platform will recur — a new `make-{platform}-kit`
sibling is minted via [[forge's skill-forge]] to own execution.
