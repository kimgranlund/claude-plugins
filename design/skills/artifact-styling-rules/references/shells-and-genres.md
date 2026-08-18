# Shells and genres — which page shape this content gets, and what it looks like

The question this file answers: **given a content class, which page shell does it get, and what
should that shell actually LOOK like?** `docs:artifact-rules`' `content-structure.md` owns the
CLASSIFICATION task (is this content a report, a handbook, or spanning both); this file owns the
visual doctrine for each answer.

## Narrative single-scroll for reports/retros

[incident] Standing taste ruling, 2026-07-16, re-affirmed since. A report or retro page is **one
continuous vertical read, head-first**, never a dashboard or tile shell with cards/widgets
scattered across a grid.

- **Do:** one scrolling column, sections in read order, head-first summary before supporting
  detail, prose width 54rem (`type-and-layout.md`).
- **Don't:** a grid of metric tiles, a sidebar nav fragmenting the report, a dashboard-style KPI
  wall standing in for the narrative.

## Tabbed chapters for handbooks

A handbook (multi-section, consulted not read start-to-finish) gets **tabbed chapters**: one tab
per major section, each self-contained, a persistent tab strip, 62rem chapter width
(`type-and-layout.md`). This is the ONE shell class where tabs are correct — a report never gets
them, a handbook never gets the narrative single-scroll (the whole point of a handbook is
non-linear lookup, which one long scroll defeats). The tab/mermaid interaction is load-bearing —
see `mermaid-reference.md`'s width-preserving hidden-panel rule.

## Mechanism-first cards with collapsed rosters

Content explaining **how something works** gets one diagram of the real mechanism
(`mermaid-reference.md`), never a wall of chips/badges/pill tiles standing in for structure — a
chip wall ("Phase 1 ✓ Phase 2 ✓ Phase 3 ⏳") reads as decoration; a mechanism diagram reads as the
mechanism. Where a LONG enumeration is genuinely needed (a roster of agents, skills, or findings —
not a mechanism), a **collapsed roster** — a compact list or table, disclosed on demand rather than
laid out as a grid of individually-styled tiles — is the pattern: enumerate without a chip wall's
per-item visual weight. This content-shape rule applies inside both shells above wherever the
content explains a HOW or enumerates a LONG set.

**[verified, jiji262/claude-design-skill, accessed 2026-08-18]** an "anti-slop" component
discipline from community prior art independently names the same failure mode from the opposite
direction: explicit prohibitions against "gradient-orbs," decorative rounded cards with left
borders standing in for real content structure, and CSS silhouettes substituting for genuine
detail — corroborating evidence for treating decoration-over-structure as a defect class, not a
style preference.

## Hero-as-thesis

A lead section, where one exists, **states the page's thesis or verdict up front** — this
project's own verdict-first doctrine (CLAUDE.md: "Status reports use... never as decoration, never
instead of stating what is wrong"), applied to shell design. A hero is earned by SAYING the
conclusion, not by being a generic banner.

**[verified, Hermes `creative-claude-design` skill docs, accessed 2026-08-18]** community prior art
names the same failure mode by its generic-output name: "avoid the hero-plus-three-cards
composition except for Decide/Learn surfaces" — a marketing-page pattern (one banner + three
feature cards) that reads as competent when the content is genuinely a landing/decision page, and
as empty filler everywhere else (a report, a handbook chapter). This pack narrows that finding to
its own two shells: neither the narrative single-scroll nor the tabbed handbook is a Decide/Learn
surface, so neither gets a generic hero-plus-three-cards — a hero earns its place only by carrying
the actual verdict.

**[verified, Hermes docs, accessed 2026-08-18]** the wider community taxonomy this finding comes
from names seven interaction-pattern archetypes (Monitor/Operate/Compare/Configure/Decide-Learn/
Explore/Command-Inspect). This pack does NOT adopt that 7-way vocabulary — this project has two
working shell classes in production use, and importing five untested archetypes ahead of any real
build against them would be manufactured process (pack-writing-rules' "heroic single wave" failure
class, applied to premature taxonomy import). The finding above is cited narrowly, for the one
anti-pattern it corroborates.

## Provenance footer, as a shell element

Every page carries a provenance footer (source path, build date, invocation — the full stamping
CONTRACT is `docs:artifact-rules`' `refresh-procedure.md`, not restated here). As a SHELL element,
the footer is visually de-emphasized relative to content — small type, `--fine`/`--muted` role,
placed after all content, never competing with the hero or the narrative body for attention. This
file states what it looks like; the docs-side file states when it gets stamped and how staleness
is detected.

## Choosing the shell

`docs:artifact-rules`' `content-structure.md` runs the actual classification (report/retro vs
handbook vs spanning-both) at `make-artifact`'s Phase 3; this file is what that classification
routes TO. A content source spanning both classes is named explicitly rather than silently
defaulting to one shell — the docs-side file's own rule, cited here rather than restated.

Extension: governed by [[make-pack]].
