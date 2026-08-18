---
doc-type: lld
id: lld-0020-artifact-styling-rules
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#650
spec: none — #650's own Acceptance section carries the checkable criteria (the 5-axis reference
  list, R1-R8 rubric dimensions, artifact_check.py fixtures, evals+fences) and its Scope/Open
  section names the two open questions this LLD resolves (the exact docs/design section split,
  agent-verifiability layering); a standalone SPEC would restate what the ticket already states
  (doc-writing-rules' own routing test, same as lld-0013/lld-0008/lld-0009).
---
# LLD — `design:artifact-styling-rules` + `docs:artifact-rules` slim-down (#650)

**Verdict, head-first:** one new knowledge pack, `design/skills/artifact-styling-rules/` (5
declared axes, flat consult table, no INDEX.md — pack-writing-rules' enumerability rule), carrying
every VISUAL/styling doctrine for Claude Artifacts: platform runtime facts, the token
role-alias architecture, type/layout doctrine, the full mermaid authoring+rendering contract, and
shell/genre doctrine. `docs/skills/artifact-rules/` slims to PROCEDURE-side standards only — the
content-structure classification task (feeding #649's future composition phase), the provenance
footer stamping + refresh-trigger procedure, and the `css_build.py` mechanical interface contract
— citing the new pack for every visual "why". Mechanized by a new bundled script,
`design/skills/artifact-styling-rules/scripts/artifact_check.py` (grep-gate selftest, fixtures
from this record's own named bugs). Both plugins ship together as one PR (design 1.0.9→1.1.0,
docs 1.19.3→1.19.4 — re-verified against `origin/main` immediately before PR-open per Phase 5's
VALUE-race check).

## Resolution 1 — Home of the visual doctrine: `design`, per Kim's 2026-08-18 ruling

Already ratified in the ticket body ("homed in the DESIGN plugin, Kim's ruling 2026-08-18") — not
re-litigated here. Job evidence for the record: `design`'s manifest already claims "color science
and palettes, typography systems, and design-system exports" — Artifact *styling* doctrine
(tokens→CSS role-alias method, type/layout, mermaid theming, shell/genre visual taste) is
downstream of exactly those three domains, while `docs` keeps the *procedural* orchestration
(`make-artifact`'s phase sequence, content-structure classification, provenance/refresh) the way
`lld-0013` already drew the authoring-vs-consuming line for the design-system source itself.

## Resolution 2 — Shape: 5-axis knowledge pack, no INDEX (pack-writing-rules' own threshold)

Per `harness/skills/pack-writing-rules/SKILL.md` (read in this clone): 3-7 axes, flat consult
table when the corpus is ≤~7 files (`the table IS the retrieval map`). The ticket's own Acceptance
section already enumerates exactly 5 distinct question types:

| # | File | Question it answers |
|---|---|---|
| 1 | `platform-facts.md` | What does the Artifact *runtime itself* allow/forbid — CSP, size, theme signal, ground color, downloads, native mermaid? |
| 2 | `token-architecture.md` | How does a project's design-system tokens become an artifact's `--c-*`/etc custom properties — the role-alias method, not a re-ramp? |
| 3 | `type-and-layout.md` | What are the artifact's own type/width/spacing/radius defaults, independent of the source design system? |
| 4 | `mermaid-reference.md` | How does a diagram survive this pipeline — authoring AND re-theming? |
| 5 | `shells-and-genres.md` | Which page shape (visually) does a content class get? |

5 axes clears the 3-7 threshold; a flat 1:1 consult table in the SKILL.md body, no `INDEX.md` —
same precedent `lld-0013`/`docs/skills/agent-harness-rules` already ship at 4 files.

**Rejected:** an `INDEX.md` anyway "for future growth" — pack-writing-rules is explicit that an
INDEX earns its keep only once files outgrow 1:1 enumeration; shipping one now would be a second
copy of the same 5-line table with nothing to route yet.

## Resolution 3 — The docs/design section split (ticket's own named open question, resolved)

**Hard fence, stated once:** `design:artifact-styling-rules` owns *what it should look like and
why*; `docs:artifact-rules` owns *when in the build sequence to apply it and how to detect
staleness*. Concretely, per current file:

- **`design-system-consumption.md` (docs, existing)** → renamed **`script-interface.md`**,
  trimmed to ONLY the `css_build.py` mechanical contract: the two accepted input JSON shapes, the
  invocation, and the emitted custom-property NAMES (`--c-*`/`--text-*`/`--space-*`/`--r-*`) as an
  interface list — no doctrine on *why* role-alias, *why* `light-dark()`, or the token inventory.
  Every "why" line now cites `design:artifact-styling-rules`' `token-architecture.md` instead of
  restating it (the exact duplication the ticket forbids: "never duplicate the visual doctrine").
- **`shell-doctrine.md` (docs, existing)** → renamed **`content-structure.md`**, trimmed to the
  CLASSIFICATION task only — is a content source a report/retro, a handbook, or spanning both
  (the same three-way test `make-artifact`'s Phase 3 already runs) — because this is where #649's
  future composition phase (Intent/User-Story/Concept/System → chapter mapping) plugs in structural
  routing, a docs-owned procedure concern. The VISUAL doctrine for each shell (narrative
  single-scroll taste ruling, mechanism-diagram-over-chip-wall, hero-as-thesis, mechanism-first
  cards with collapsed rosters) moves to design's `shells-and-genres.md` wholesale; docs' file
  cites it for "what it should look like."
- **`mermaid-style.md` (docs, existing)** → **retired outright.** Its full content (br-stripping,
  `!important`-over-inline-style, width-preserving tab hide) migrates verbatim into design's
  `mermaid-reference.md`'s rendering half, expanded with this wave's new research (full SVG class
  list, surface-ladder rule, `rx=0`, `!important`-vs-`%%{init}%%`). `make-artifact`'s Phase 4 now
  cites `design:artifact-styling-rules`' file directly — soft cross-plugin mention, degrades
  gracefully where `design` isn't installed (same seam `lld-0013` already uses for the reverse
  direction).
- **`refresh-procedure.md` (docs, existing)** → **unchanged.** Purely procedural (footer stamping,
  refresh trigger, not-a-hook) — no visual content to migrate. Design's `shells-and-genres.md`
  states what a provenance footer looks like as a shell ELEMENT (placement, visual weight); docs'
  file keeps owning WHEN it gets stamped and WHEN staleness is declared. Neither restates the
  other's half.

**docs:artifact-rules' new consult table** (3 rows, down from 4, plus one top-of-body pointer to
the design pack for anything visual):

| Ask | Load |
|---|---|
| "Is this content a report, a handbook, or both?" | `references/content-structure.md` |
| "What does `css_build.py` actually take and emit?" | `references/script-interface.md` |
| "When/how does a shipped artifact get refreshed?" | `references/refresh-procedure.md` |

Anything about *how it should look* (theme, tokens, type, mermaid, shell taste) routes to
`design:artifact-styling-rules` instead — named explicitly in the SKILL.md body, not left implicit.

## Resolution 4 — Research wave: 4 sources gathered, cited per pack-writing-rules

One wave, 4 parallel `fact-finder` dispatches (2026-08-18), each logging dated `[verified]`
findings to a scratch ledger (`/scratchpad/research-ledgers/*.md`, not shipped — the pack's
`references/` files are the DISTILLED product, not the raw ledgers, per pack-writing-rules' wave
step 3 "distill ask-shaped"):

1. **Anthropic's own "Improving frontend design through Skills" blog** + dev.to/Postman/Fastio
   community artifact-constraint guides → feeds `platform-facts.md` (CSP/sandbox/size/storage
   constraints) and informs `type-and-layout.md`'s steering-lever framing (distinctive typography,
   one-dominant-color-plus-accents, asymmetry-over-generic-grid).
2. **jcmrs/claude-visual-style-guide** (shadcn-flavored community token guide) → feeds
   `token-architecture.md`'s comparison point: a semantic-role + light/dark-split + Tailwind-utility
   naming convention, cited as prior art the role-alias method is compatible with but does not copy
   verbatim (this project's own tokens are OKLCH `light-dark()` pairs, not a `dark` CSS-class
   toggle).
3. **Mermaid's own theming docs (mermaid.js.org) + Gordonby/MermaidTheming + dev-toolbox.tech** →
   feeds `mermaid-reference.md`: the `themeVariables` key set, "base" as the only user-modifiable
   theme, the derived-variable hierarchy, and — the load-bearing finding — mermaid's OWN injected
   styles carry `!important` scoped to the SVG id, so external CSS reliably wins ONLY if it too
   carries `!important` (this wave's finding independently confirms and sharpens the differentiator
   fact already carried from session evidence).
4. **Hermes' `creative-claude-design` skill + jiji262/claude-design-skill** (community genre
   taxonomies) → feeds `shells-and-genres.md`: named archetype systems (Monitor/Operate/Compare/
   Configure/Decide-Learn/Explore/Command-Inspect; the anti-"hero-plus-three-cards" rule except for
   Decide/Learn pages) cross-checked against, and folded under, this project's own two working
   shell classes (narrative single-scroll, tabbed handbook) rather than importing a 7-way taxonomy
   wholesale — the differentiator facts (mechanism-diagram-over-chip-wall, the 2026-07-16 taste
   ruling) stay primary; the external taxonomy is cited as corroborating prior art for
   "hero-as-thesis" and "collapsed rosters," not a replacement vocabulary.

**Differentiator facts** (session-evidenced, no seed source covers them — carried forward from the
existing docs pack, migrated verbatim, re-grounded under design's own corpus): CSP + tri-state +
injected-stylesheet specifics; role-alias/`light-dark()` build method; the surface-ladder rule;
`<br/>`-stripping. Each keeps its `[incident]`/`[verified]` marker and 2026-08-18 date on migration
(pack-writing-rules: "when a claim is corrected [or relocated], the old text is amended in place
with a dated note" — here, a straight migration, so the marker and date travel with the claim, not
re-derived).

## Resolution 5 — The reference-implementation token file, read and encoded

`~/Projects/adia/_shared/adia-design-system-files-aug-18/design-system-for-claude-code/artifact-adiaui.tokens.json`
[verified, 2026-08-18] is the artifact TRANSPOSITION layer over the Adia system's own
`--md-sys-color-*` roles — `_meta.description` states its own build-time contract verbatim: "Colors
flow from the design system; geometry and type flow from the artifact doctrine... Build-time:
css_build extracts only the consumed roles as light-dark() pairs... no prefers-color-scheme
triple-block." This is `token-architecture.md`'s primary citation for:

- **The artifact token inventory**: 14 live roles in `role-mapping` (`--paper`/`--card`/`--chip`/
  `--card-low`/`--ink`/`--muted`/`--fine`/`--line`/`--line-strong`/`--accent`(+`-hover`/`-soft`)/
  `--on-accent`/`--tertiary`/`--danger`/`--success`/`--warning`/`--info`(each `+-soft`)/`--on-intent`
  /`--mono-bg`), plus the `_unbound` tier-2 note (secondary, active/disabled ladders, dialog-backdrop
  — reserved, not yet bound on static pages).
- **The colors-from-system/geometry-type-from-doctrine split**: `_integration` states it explicitly
  — surfaces/containers/borders/families/radius/spacing are PROJECTIONS of the source system;
  `"themes+type": "NOT integrated: frozen projection, not live ramp binding; faces owned by the
  artifact type doctrine"` — i.e. colors bind live to the consuming project, faces (fonts,
  radius resolution) are the artifact doctrine's own fixed defaults.
- **The role-mapping file SHAPE**: `{role, resolved}` pairs, `resolved` already carrying the full
  `light-dark(<light>, <dark>)` CSS function value — this is the exact shape `css_build.py`
  consumes (docs' `script-interface.md` cites this same file for the input contract).
- **The mermaid token block**: `mermaid.node/edge/edgeLabel/cluster/emphasisNode/intentNodes/
  datastore` keys, the `_ladder_rule` ("nodes sit one surface tier ABOVE whatever they rest on...
  never card-over-paper"), and the `rounded sm — mermaid base theme ships rx=0; set rx/ry via CSS`
  note — all three become `mermaid-reference.md`'s rendering-half content verbatim.

## Resolution 6 — Rubric: R1-R8, gate/review split per the `rubric-md-to-markup` precedent

Same shape as `docs/skills/markdown-to-markup/references/rubric.md` (1-5 scale, `[gate]`/
`[review]` typed dimensions, 1→3→5 anchors, gate threshold stated once at the bottom):

| # | Dimension | Type | 1→3→5 anchor shape |
|---|---|---|---|
| R1 | Theme integrity | [gate] | 1: colors defined only inside a `prefers-color-scheme` block (or hardcoded, no dark pair) · 3: every color role is a `light-dark()` pair under `:root`, `color-scheme: light dark` present · 5: + a `[data-theme]` manual override proven to flip resolution with zero duplicated variables |
| R2 | Token binding | [gate] | 1: a literal hex/oklch value used directly in a rule body, outside `:root` · 3: every visual property reads a `var(--c-*/--text-*/--space-*/--r-*)`, roles traced to the source system · 5: + tier-2/`_unbound` roles are never silently invented — an unmapped need routes to a named gap, not an ad-hoc color |
| R3 | Type doctrine | [review] | 1: body/interactive faces ignore the artifact doctrine defaults with no override reason stated · 3: system-ui body, mono interactive (buttons/links/tabs/badges/kickers), width tier matches content class · 5: + an explicit override is named and justified where the source system's own faces are used instead |
| R4 | Diagram contract | [gate] | 1: multi-line `<br/>` node labels, or an unthemed/light-locked mermaid SVG in dark mode · 3: single-line node labels (detail on edges), `!important` re-theme block present and bound to page tokens, surface-ladder respected · 5: + `rx`/radius explicitly set (never bare `rx=0`), hidden-tab panels use `visibility:hidden` not `display:none` |
| R5 | Shell-genre fit | [review] | 1: a report/retro shipped as a dashboard/tile grid, or a chip-wall standing in for a mechanism diagram · 3: narrative single-scroll for reports/retros, tabbed chapters for handbooks, one mechanism diagram per HOW-explaining section · 5: + hero-as-thesis where a lead section exists, collapsed rosters instead of chip walls for long enumerations |
| R6 | CSP self-containment | [gate] | 1: an external stylesheet/font/script URL, or a resource load requiring network past the CDN allowlist · 3: fully single-file, only doctrine-approved system font stacks, no external `url()` in CSS · 5: + verified against `artifact_check.py`'s external-URL grep with zero findings |
| R7 | Readability | [review] | 1: prose width unconstrained (full-bleed text) or so narrow it fragments code/tables · 3: width tier matches content class (74/62/54rem), spacing scale consistent, two-tier radius (controls ≤12px, surfaces ≤16px) respected · 5: + specificity pitfalls avoided (no injected third-party inline style silently winning over a page rule) |
| R8 | Provenance | [gate] | 1: no footer, or a footer missing the source path/build date/invocation · 3: footer names source DESIGN.md/tokens.json path, `$generator` line where used, content source, build date, exact invocation · 5: + the footer alone is sufficient for a reader to detect staleness without re-running anything |

**Gate to promote:** R1, R2, R4, R6, R8 must each score ≥3 — theme integrity, token binding, the
diagram contract, CSP self-containment, and provenance are load-bearing; R3/R5/R7 are judgment
findings that don't block on their own but degrade the score.

## Resolution 7 — `artifact_check.py`: grep-gates from this record's own named bugs

Per `script-writing-rules` (stdlib-only, `selftest` mode, exit tri-state, verdict line first). Six
checks, each with a fixture pair (a passing snippet, a failing snippet the check must catch —
negative control) plus one reverse control (a fully-compliant fixture triggers zero findings):

| Check | Catches |
|---|---|
| `theme-block-only` | Color values that only ever appear inside an `@media (prefers-color-scheme...)` block, never as a `light-dark()` pair under `:root` — the R1 gate's mechanical half |
| `external-url` | Any `url(http...)`/`<link href="http...">`/`@import url(http...)` outside the doctrine-approved CDN allowlist — R6 |
| `literal-outside-root` | A bare hex/oklch/rgb color literal used directly in a non-`:root` rule instead of a `var(--c-*)` reference — R2 |
| `br-in-mermaid-label` | A literal `<br/>`/`<br>` inside a mermaid node-label bracket (`["...<br/>..."]`) — R4 |
| `missing-ground` | No `color-scheme` declaration on `:root`, or the `body`/page-root element's background not bound to a `--paper`/`neutral-background`-family token — R1/R7 |
| `doctrine-font-stack` | A `font-family` on a body or interactive-role selector that names neither the doctrine system-ui/mono stack nor an explicitly commented override — R3 |

`selftest` runs all six against inline fixtures, asserting each negative control fails and the
reverse-control fixture passes clean — same contract `css_build.py`'s own selftest already
demonstrates in this plugin family.

## Resolution 8 — Evals: real asks + reciprocal fences, 4 siblings

Trigger cases lifted from the actual asks this pack's differentiator facts trace to ("the colors
are a bit nuts," "why sharp corners," "diagrams look off-theme") plus 2-3 adjacent phrasings per
axis. No-trigger fences into every sibling this pack's vocabulary could leak into or from:

- **`docs:make-artifact`** — the BUILD ask ("turn this report into an artifact page") stays there;
  this pack only answers standards questions with no build verb.
- **`design:make-design-system`** — authoring/grading the design-system SOURCE stays there; this
  pack only consumes it into an artifact.
- **`dataviz`** — chart/graph/plot color and mark-spec questions stay there; this pack's mermaid
  axis is diagram STRUCTURE/theming, never chart data encoding.
- **`screens:break-down-layout`** — general UI layout critique (non-artifact screens) stays there;
  this pack is Artifact-page-specific.

Each sibling's own `evals/evals.json` gains one reciprocal no-trigger case in the same PR
(`.claude/rules/plugin-authoring.md`'s reciprocal-fence rule), and `/check-routing design` +
`/check-routing docs` + `/check-routing screens` (screens only if `break-down-layout`'s description
needs a fence line edit — a description-only diet, so its own suite gains one case without a
`/check-routing screens` re-run being strictly required, but it runs anyway since the fence line
changed).

## Components

Build sequence, a builder executes top to bottom:

1. **`design/skills/artifact-styling-rules/SKILL.md`** — knowledge species, `user-invocable:
   false`, `disable-model-invocation: false`. Consult table (5 rows), fences per Resolution 8,
   `Extension: governed by [[make-pack]]` footer.
2. **`design/skills/artifact-styling-rules/references/platform-facts.md`** — CSP single-file
   inlining, 16MB practical cap, viewer theme TRI-STATE (`[data-theme="light"]`/`[data-theme="dark"]`
   explicit stamps + a third un-stamped state that follows system `prefers-color-scheme` — this is
   why `light-dark()` + bare `color-scheme: light dark` on `:root`, with NO `[data-theme]`
   attribute present, is the correct default-state contract), body-ground rule, inert
   downloads/no persistent storage, native mermaid (no CDN import needed) — [verified] citations to
   this wave's platform/constraint research.
3. **`references/token-architecture.md`** — role-alias method (semantic roles never re-ramp from
   scale stops; an artifact ALIASES the consuming project's already-resolved role values), the
   `light-dark()`+`color-scheme` build-time pattern (retiring the `prefers-color-scheme`
   triple-block), the 14-role + tier-2 inventory (Resolution 5), the colors-from-system/
   geometry-from-doctrine split, the role-mapping file shape, jcmrs comparison point (Resolution 4
   item 2).
4. **`references/type-and-layout.md`** — system-ui body / ui-monospace interactive doctrine (#649's
   Kim-ruled defaults, cited forward since #650 is the shipped-doctrine home even though #649's
   composition phase isn't built yet), width system 74rem (content, extra-wide default)/62rem
   (handbook tabbed-chapter reading width)/54rem (narrative prose) — the first two [verified]
   against the reference token file's `layout.content-max-width`/`prose-max-width`; 62rem
   [inferred] from the ticket's own stated acceptance value as the third, unverified-elsewhere
   tier, named as such — spacing scale (named xs...5xl general grammar; the reference impl's own
   `_integration.spacing` subsets to 4/8/12/16/24/32/48 for static pages), two-tier radius
   (controls cap 12px, surfaces cap 16px — [verified], `_integration.radius`), specificity
   pitfalls (an injected third-party inline style — e.g. a syntax highlighter — can out-specificity
   a page rule; fix is `!important` scoped to that element class, same mechanism as the mermaid
   case), width-preserving tab hiding (migrated from docs' `mermaid-style.md`, generalized: ANY
   hidden-panel content that measures its own layout at render time, not just mermaid, wants this
   technique).
5. **`references/mermaid-reference.md`** — authoring half (single-line labels, detail on edges,
   mechanism over inventory, one `:::accent` per diagram, intent classes, LR/TB guidance) +
   rendering half (full CSS override class list from the reference token file's `mermaid` object;
   why `!important` beats mermaid's own injected in-SVG stylesheet — sharpened by this wave's
   Finding 6/7/8: mermaid's internal styles carry `!important` scoped to the SVG id, so external
   CSS must ALSO carry `!important` to win, `classDef`/`class`/inline `style` are mermaid's OWN
   in-syntax alternative but don't bind to the PAGE's live theme tokens the way a CSS override
   block does; surface-ladder rule; `rx=0` needs explicit radius; why CSS overrides beat
   `%%{init}%%` themeVariables — init bakes one static theme at parse time, a CSS override binds
   live custom properties that already re-theme with the rest of the page).
6. **`references/shells-and-genres.md`** — narrative report vs tabbed handbook (migrated taste
   ruling), mechanism-first cards with collapsed rosters (a compact enumeration pattern replacing a
   chip wall for long rosters — agents, skills, findings lists), hero-as-thesis (a lead section
   states the page's verdict/thesis up front — this project's own verdict-first doctrine, applied
   to shell design; cross-checked against Resolution 4 item 4's "anti hero-plus-three-cards except
   Decide/Learn" finding — a hero is earned by STATING the thesis, not by being a generic banner),
   provenance footer AS A SHELL ELEMENT (placement/visual weight only — the stamping procedure
   stays in docs).
7. **`references/rubric.md`** — Resolution 6, verbatim.
8. **`design/skills/artifact-styling-rules/scripts/artifact_check.py`** — Resolution 7. Positional
   contract: `artifact_check.py <page.html|page.css> [...]`; no args → docstring + exit 2; exit
   0/1/2; verdict line first (`artifact_check · ok · 0 fail`). `selftest` mode proves all six
   checks against inline fixtures.
9. **`design/skills/artifact-styling-rules/evals/evals.json`** — Resolution 8's trigger set + own
   negatives fencing the 4 siblings.
10. **Reciprocal fence edits** (same change, `.claude/rules/plugin-authoring.md`):
    - `design/skills/make-design-system/SKILL.md` — append one more NOT-clause naming this pack
      for artifact-STYLING questions (distinct from the existing `make-artifact` NOT-clause, which
      names the build itself) + one no-trigger case.
    - `docs/skills/make-artifact/SKILL.md` — Phase 4 now cites
      `design:artifact-styling-rules/references/mermaid-reference.md` directly (soft mention,
      degrades where `design` isn't installed) instead of the retired `mermaid-style.md`; NOT-list
      gains a clause naming the new pack for visual-styling questions + one no-trigger case.
    - `dataviz` and `screens:break-down-layout` SKILL.md — one NOT-clause each + one no-trigger
      case apiece.
11. **`docs/skills/artifact-rules/` reshape** (Resolution 3): rename+trim
    `design-system-consumption.md`→`script-interface.md`, `shell-doctrine.md`→
    `content-structure.md`, retire `mermaid-style.md`, leave `refresh-procedure.md` untouched;
    rewrite the SKILL.md consult table (3 rows) + body pointer to the design pack; rewrite
    `docs/skills/artifact-rules/evals/evals.json`'s notes/cases where a case's expected route now
    points elsewhere (a mermaid-rendering question moves from a docs-pack trigger to a design-pack
    trigger — update both suites' cases, don't leave a stale trigger in docs' suite pointing at a
    retired file).
12. **Plugin close-out, two plugins**, versions re-verified off `origin/main` immediately before
    PR-open (Phase 5's VALUE-race check):
    - `design/.claude-plugin/plugin.json`: 1.0.9 → **1.1.0** (a new skill/pack is a MINOR bump, not
      a patch — distinct from the description-only patch bumps design has taken recently).
      Manifest description gains an artifact-styling clause. README ledger line naming #650, the
      5-axis pack, the reciprocal fences, and the reshape.
    - `docs/.claude-plugin/plugin.json`: 1.19.3 → **1.19.4** (a reshape/trim of an existing pack +
      one reciprocal fence line — patch-shaped, no new skill minted in this plugin). README ledger
      line naming #650, the file renames/retirement, and the design-pack citation.
13. **Gates before PR**: `skill_lint.py` on every touched/new SKILL.md + evals.json (both
    plugins); `artifact_check.py selftest` green; `/check-routing design`, `/check-routing docs`,
    and `/check-routing screens` (fence line changed); `release_gate.py design --package` and
    `release_gate.py docs --package`; fresh-context `harness:skill-checker` pass on every
    semantically-edited SKILL.md (the new pack's SKILL.md, and the 3 reciprocal-fence sibling
    SKILL.mds, and docs' reshaped `artifact-rules/SKILL.md`) — batched per
    `plugin-authoring.md`'s reciprocal-fence precedent (lld-0013's own PR batched 6 checker passes
    similarly); a scoped blind routing-judge proof (unnamed synchronous dispatch) confirming the
    new pack's description doesn't leak into or steal from the 4 fenced siblings.

## Interfaces

- **`design:artifact-styling-rules` → `docs:make-artifact`**: soft cross-plugin mention only — the
  procedural skill cites the pack's file paths for doctrine, no preload, no
  `${CLAUDE_PLUGIN_ROOT}` cross-boundary path (plugin-authoring.md's hard boundary holds, same seam
  as `lld-0013`'s reverse-direction citation).
- **`design:artifact-styling-rules` → `docs:artifact-rules`**: same soft-mention shape, the
  opposite direction — docs' 3 remaining files each cite a design-pack file for "why," never
  restate it.
- **`artifact_check.py` → a page's CSS/HTML**: read-only grep-gate; never mutates, never runs as
  part of `css_build.py`'s own build (a separate, later verification step a builder or CI can run
  against ANY emitted page, not tied to one script's output).
- **Reference token file → `token-architecture.md`/`mermaid-reference.md`**: a READ citation only
  (Resolution 5) — this pack never bundles or copies the adia-specific json; it's the worked
  reference implementation the doctrine generalizes from, cited by path.

## Data

Static skill/reference markdown + one bundled script; no runtime store, no migration. Same shape
as `lld-0013`'s own Data section.

## Risks

- **R-1 (grounding gap on the 62rem width tier).** Only 2 of the 3 stated width numbers are
  [verified] against the reference token file; the third (62rem) is [inferred] from the ticket's
  own acceptance text alone. Detection: `type-and-layout.md`'s own marker states this plainly.
  Fallback: if a future build finds a different real source for 62rem, amend in place with a dated
  note (pack-writing-rules' correction discipline) — never silently upgrade the marker without a
  cited source.
- **R-2 (external community sources drift).** jcmrs' repo, Hermes' skill docs, and mermaid's own
  themeVariables table are live, externally-owned artifacts that can change under this pack.
  Detection: each citation carries its own [drift-prone]-eligible marker where the underlying
  source is itself unstable (community repos, not a dated spec). Fallback: the [drift-prone]
  inventory is the refresh checklist at the pack's next touch, per pack-writing-rules.
- **R-3 (fence drift across 4 siblings + 2 plugins).** Same class `lld-0013`'s R-4 named. Detection:
  reciprocal no-trigger cases in all 5 evals suites (the new pack's + 4 siblings') +
  `/check-routing` on all 3 touched plugins in this same PR. Fallback: routing-eval failures point
  at the exact description line to sharpen.
- **R-4 (docs-side reshape breaks `make-artifact`'s own Phase references).** `make-artifact`'s
  SKILL.md cites its sibling `artifact-rules` files by name at each phase; renaming/retiring 3 of
  4 files risks a stale pointer. Detection: grep `make-artifact/SKILL.md` for every retired/renamed
  filename post-edit — zero hits required. Fallback: this is exactly the reciprocal-fence
  requirement in Components step 10; the same PR that renames the files updates every citing
  phase.

## Rejected alternatives

- **Ship an `INDEX.md` for the new pack.** Rejected — 5 files is inside the flat-table threshold;
  an INDEX now would be a second copy of the same 5 lines with nothing to route (Resolution 2).
- **Leave `design-system-consumption.md`/`shell-doctrine.md`/`mermaid-style.md` in docs unchanged
  and just ADD the design pack alongside.** Rejected — this is precisely the duplication the
  ticket forbids ("hard fence... never duplicate the visual doctrine"); two live copies of the
  same doctrine drift the moment either changes (the CLAUDE.md stale-context defect, applied to a
  pack fork).
- **Import the Hermes/jiji262 7-archetype genre taxonomy wholesale.** Rejected — this project has
  exactly two working shell classes in production use (narrative single-scroll, tabbed handbook);
  importing a 7-way taxonomy with no artifacts built against 5 of the 7 archetypes would be
  manufactured process ahead of real use, the same "heroic single wave" failure mode
  pack-writing-rules already names. The external taxonomy is cited as corroborating prior art for
  two specific sub-patterns (hero-as-thesis, collapsed rosters), not adopted as the pack's own
  vocabulary.
- **A single merged pack spanning both plugins (no docs/design split at all).** Rejected by the
  ticket's own explicit ruling (Kim, 2026-08-18) and by `.claude/rules/plugin-authoring.md`'s hard
  plugin-boundary rule — a preload or bundled-script path can never cross plugins; two packs with a
  soft citation seam is the only legal shape here, same as `lld-0013`'s original authoring/
  consuming split.
- **Mint a new `object_vocab` entry for this pack's name.** Not needed — `artifact` is already
  registered (`lld-0013`'s Resolution 5); `styling`/`rules` follow the same established compound-
  modifier + ProcessLex-terminal pattern already shipped uncontested in `font-token-rules`/
  `design-md-rules`/`big-change-git-rules` (no individual registration for each compound-name
  substring). Verified with `authorkit/skills/naming-audit/scripts/validate.py --scope grammar`
  showing zero new errors after the skill directories land, not asserted from memory alone.

## Agent verification

Assert-layer choice per `docs/skills/agent-harness-rules/references/assert-layer-choice.md`,
same test `lld-0013` already applied: **`artifact_check.py selftest`** is the new payload-layer
instrument, carrying the ticket's own Acceptance criteria (the 6 named-bug fixture classes) as
executable predicates. Existing instruments cover the rest: `skill_lint.py`+`eval_check.py`
(mechanical), the new + 4 edited evals suites run via `/check-routing design`/`docs`/`screens`
(routing), `release_gate.py` on both touched plugins (enforcement, packages both). **Stated
exception (human layer):** whether a rendered page's shell/theme/mermaid diagram actually LOOKS
right in a real browser stays human review — same exception `lld-0013` already named, inherited
here rather than re-derived, since `make-artifact`'s own Done block already carries it and this
pack changes no rendering mechanism, only the doctrine consulted while authoring one.
