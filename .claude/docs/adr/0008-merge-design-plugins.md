---
doc-type: adr
id: adr-0008
status: accepted
ratified: by Kim
date: 2026-07-21
owner: kim.granlund
supersedes: null
---
# ADR-0008 — Merge design-kits + color + typography into one `design` plugin

## Context

The visual-design layer shipped as three plugins whose boundary carried the workspace's
heaviest coupling: 48 intra-trio cross-mentions (design-kits→color alone 28 — the export
bundles consume make-palette/check-colors; typography→design-kits 10 — the Material typescale
fences). The ui merge precedent (two clusters unified over 13 cross-mentions) set the bar this
trio clears three times over. plan-plugin-split's merge tests pass: 22 skills + 3 agents is
mid-sized (harness carries 26), the members are one distribution audience (anyone doing visual
design wants all three), and no portability seam is severed. Kim directed the merge 2026-07-21
and asked for a holistic naming review alongside it.

## Decision

1. **One plugin, `design` (1.0.0)** — absorbing design-kits 1.0.6, color 1.0.6,
   typography 1.0.6. Directory `design/` (per ADR-0007). Source ledgers preserved at
   `design/legacy/README-<old-plugin>.md`; the routing rows, marketplace entries, and installs
   collapse three-to-one.
2. **Member-level term-of-art stutter exception** (extends ADR-0006 Decision 7 from plugin
   names to member names): a member name may contain the plugin word when that name IS the
   real-world term — `design:make-design-system` (a design system is the artifact; "kit" was
   the euphemism) and `design:design-md-rules` (DESIGN.md is the literal filename). The
   no-stutter rule stands for names where the plugin word is decorative.
3. **`make-design-kit` → `make-design-system`**, and its agent
   `design-kit-checker` → `design-system-checker`. The three platform exporters keep their
   `make-*-kit` names — a kit is the per-platform bundle OF the design system; the vocabulary
   split is deliberate (hub = the system, spokes = platform kits).
4. **`color-material-facts` → `physical-color-facts`** — inside one plugin,
   `color-material-facts` and `material-color-facts` were a confusable pair with "material"
   meaning pigment in one and Material Design in the other; the rename frees "material" to
   mean only Material Design within `design`.
5. **Per-suite parity contract carries over from ADR-0006**: floors are the measured
   post-heal results from the ADR-0006 campaign (508/515 across the trio's 22 suites);
   post-merge re-measure runs on the union menu, where steals across the former plugin
   boundaries are NEW seams to fence (not regressions), and per-suite scores at or above
   floor otherwise.

## Consequences

- One install for the visual-design layer; cross-"plugin" fences inside the trio become
  ordinary sibling fences.
- The union menu (22 model-invocable skills) is the largest routing surface after harness —
  the post-merge measure is the acceptance gate.
- naming-rules gains the member-level exception clause; the estate map records the three
  renames as ADR-0008 rows.
