# Rubric — Cross-Platform Design-System Engagement

Scores one hub engagement — the routing decision, the platform strategy, the canonical
core, the sibling dispatches, and the generation-context work — for whether the whole
arrangement holds: one truth, right seats, potent context. Built via `rubric-author`;
doctrines it scores against live in `../references/shared-doctrines.md` and
`../references/platform-map.md`. Platform *exports* are scored by the owning sibling's
rubric (B1–B7 claude-code; the stitch/make rubrics) and graded independently by the
design-system-reviewer agent — an export's internals are the sibling rubric's to score.
`[gate]` = definitional, carried in the ship set; `[review]` = judgment with cited
evidence on the 1–5 anchors.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| H1 | Routing fidelity | [gate] | Each part of the ask lands at its owning seat: named single-platform execution → the sibling, grading → design-system-reviewer, palette/tokens → upstream; the hub keeps only cross-platform strategy, core, and context work | 1: the hub executes a single-platform export or grades its own output · 3: routed correctly, hand-offs thin · 5: every hand-off named with its reason; dispatches carry the core, doctrines, and divergence callouts |
| H2 | One canonical core | [gate] | Every design fact stated once in the core; exports and receipts derive from the same build; no fact introduced inside one export | 1: a design fact lives only in one export (a fork) · 3: core canonical, provenance of one carrier unclear · 5: core owns all facts; carriers value-equal (±1/255) from one build; receipts regenerated with each build |
| H3 | Doctrine adherence | [review] | The core and recommendations carry the shared doctrines: naming grammar, terminal values, 15–25 role band, scheme parity, prose–token accord | 1: invented names, derived-at-consumer values, or ramps shipped whole · 3: doctrines mostly applied, accord unchecked in one direction · 5: grammar-constructed names, terminal verified pairs, accord proven both directions |
| H4 | Context potency | [gate] | The generation context instantiates rather than describes (linguistic-techniques L1): named world, contrastive pairs, numeric anchors, budgeted gates, right altitude | 1: adjective theme + described guardrails ("keep it clean") · 3: mixed; key rules still prose · 5: every load-bearing rule commits, demonstrates, or slots the behavior; altitude right — neither hex dump nor vibes |
| H5 | Reduction & verification honesty | [review] | R1–R5 applied to any reduction; gates run on the reduced artifacts via the siblings' checkers; receipts dated with UNMEASURED recorded, never laundered | 1: an upstream proof trusted across a reduction, or a claimed check with no run behind it · 3: gates run, a receipt stale or thin · 5: fresh gate runs per export, every UNMEASURED and divergence recorded |
| H6 | Standing rules | [review] | Leading/tracking relative (factor/em/%, never px) in every carrier; upstream made decisions called out, never silently overridden; imported content treated as data | 1: px leading shipped, or an upstream decision silently rewritten · 3: rules held, one divergence uncalled · 5: rules held everywhere; every divergence named with its reason in the deliverable |
| H7 | Strategy justification | [review] | The platform choice (and any new profile) derives from the consumption model — reader type, native gates, tolerance — cited from platform-map or the platform's published spec | 1: platform picked by fashion or memory · 3: reasonable choice, reasoning thin · 5: choice argued from the reader model; new profiles minted from the published spec via the four questions |

**Gate to promote: H1, H2, H4 each ≥ 3.** All three are definitional: a hub that
executes what a sibling owns (H1) forks the estate's truth; a forked core (H2) is the
root drift defect the architecture exists to prevent; a context that only describes
(H4) generates generic output however clean the files are — the artifact's whole point.

**Top failures to look for first:** (1) the hub quietly authoring a platform export
inline (H1) — the sibling gates go unrun, so nothing is actually verified; (2) a design
fact patched into one export "just to ship" (H2) — the next build silently reverts it;
(3) fluent, well-organized context that describes instead of instantiating (H4) — it
reviews well and generates badly, the highest-cost class because it passes casual read.
