# House shell doctrine — which page shell this content class gets

The question this file answers: **given a content class (report, retro, handbook), which page
shell does it get, and what does it never get?**

## Narrative single-scroll for reports/retros

[incident] Standing taste ruling, 2026-07-16 (session memory `review-page-shell-preference`,
folded into this shipped rule so it survives past session memory). A report or retro page is a
**narrative single-scroll stack** — one continuous vertical read, head-first, never a dashboard
or tile shell with cards/widgets scattered across a grid. Re-litigated and re-affirmed since; do
not re-ask whether a report page should be a dashboard — it should not.

- **Do:** one scrolling column, sections in read order, head-first summary before supporting
  detail.
- **Don't:** a grid of metric tiles, a sidebar nav splitting the report into fragments, a
  dashboard-style KPI wall standing in for the narrative.

## Tabbed chapters for handbooks

A handbook (a multi-section reference artifact meant to be consulted, not read start-to-finish —
the Estate Handbook is the worked case) gets **tabbed chapters**: one tab per major section,
each a self-contained chapter, a persistent tab strip for navigation. This is the one shell class
where tabs are correct — a report/retro never gets them (above), and a handbook never gets the
narrative single-scroll (the whole point of a handbook is non-linear lookup, which a single long
scroll defeats).

**The tab/mermaid interaction is load-bearing** — see `mermaid-style.md`'s width-preserving
hidden-panel rule; a handbook shell that gets the tab mechanics wrong corrupts any mermaid
diagram inside an initially-hidden tab.

## Mechanism-diagram-over-chip-wall

Content explaining **how something works** (an architecture, a data flow, a decision pipeline)
gets **one diagram of the real mechanism** — a mermaid flowchart/sequence/state diagram showing
the actual boxes and arrows — never a wall of chips, badges, or pill-shaped tiles standing in for
structure. A chip wall ("Phase 1 ✓ Phase 2 ✓ Phase 3 ⏳") reads as decoration; a mechanism diagram
reads as the mechanism. This is a content-shape rule, not a shell-class rule — it applies inside
both the narrative single-scroll and the tabbed-handbook shells wherever the content explains a
HOW.

## Choosing the shell — `make-artifact`'s Phase 3

`make-artifact` classifies its content source once, before assembly: does this page answer "what
happened / what did we decide" (report/retro → narrative single-scroll) or "how do I look this
up" (handbook → tabbed chapters)? A content source spanning both — a handbook chapter that is
itself a retro — is named explicitly in the build's Done report rather than silently defaulting
to one shell.
