# Harvest core — shared definitions + the two-axis rubric

**Canonical home.** This file is the single shared core for two sibling harvest capabilities
(#612 `project-facts`, this skill; #613 `harness-facts`) — it lives here because
#612 is first in the serial build chain and mints it. The sibling skill cites this file by
relative path (`../project-facts/references/harvest-core.md`) rather than duplicating its body —
cross-skill citation within one plugin is an ordinary mention, not a plugin-boundary violation
(`plugin-authoring.md`'s hard/soft split governs preloads and `${CLAUDE_PLUGIN_ROOT}` paths, not a
same-plugin reference like this one). No body text is duplicated between the two skills; each
cites this file and states only its own axis weighting and consumer framing.

## The two corpora this core defines

Both corpora harvest the **same substance** from the **same sources** — a project's business
logic, technical architectures, and unique-IP structures, discovered from functional prototypes,
PRDs, intent records (brief/IDRs), ADRs, and roadmaps. They differ only in **who consumes the
output** and **which axis that consumer needs weighted higher**:

| | Domain knowledge (`project-facts`, #612) | Harness facts (`harness-facts`, #613) |
|---|---|---|
| **Definition** | The project-specific business logic, technical architectures, and unique-IP structures — structured and filled in by main topic zone, written for a human or business reader to understand *what this project is and why it works the way it does*. | The same harvestable substance, reframed for a coding agent's own harness — the output feeds CLAUDE.md-grade entry files, path-scoped rules, knowledge packs, and dispatch context, never human reading. |
| **Consumer** | Humans / business | A coding agent and its harness |
| **This corpus's axis weighting** | Outside-In weighted higher | Inside-Out weighted higher |

Neither definition is a subtype of the other — they are the same extraction run scored against
the same rubric with a different weighting, the way one photograph can be graded for composition
or for exposure without being two different photographs.

## Topic zones — discovered, not fixed

The "main topic zones" a harvest fills in are **discovered per project**, never a fixed checklist.
A fixed taxonomy would force every project's genuinely different shape (a data pipeline's zones
are not a chat product's zones) into a template that either overfits or leaves real zones
unscored. Discovery procedure: read every harvest source (prototypes, PRDs, briefs/IDRs, ADRs,
roadmaps) once, extract every recurring subject those sources treat as a first-class concern (a
bounded context, a business rule cluster, an architectural seam, a named subsystem), and name each
one a topic zone. The rubric below then scores **zone coverage** directly — a project with three
real zones and a project with twelve both score cleanly, because coverage is measured against the
zones the harvest itself discovered, not against a template's fixed count.

## The two-axis rubric

Every discovered topic zone is scored through **both** lenses below, every time — the rubric never
skips an axis because a topic "obviously" belongs to one side. A topic scores low on one axis and
high on the other constantly; recording both is the point (Kim's ruling, verbatim: "both points of
view for each topic, indexing higher on the more appropriate axis").

- **Outside-In** — starting from the frame a human or business reader brings: what is this
  project *for*, who are its users/stakeholders, what business outcome does this topic zone serve,
  how would someone unfamiliar with the code describe it. Scores whether the harvest captured the
  zone's *purpose and shape from the outside*.
- **Inside-Out** — starting from the mechanism: what verbs/operations does this topic zone expose,
  what does it bind to (data, other zones, external systems), what feedback or failure signal it
  surfaces, how coherent is it with the zones around it. Scores whether the harvest captured the
  zone's *actual working mechanics from the inside*.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| R1 | Zone discovery | [gate] | Topic zones were discovered from the actual sources, not assumed from a template | 1: a fixed checklist applied blind · 3: zones drawn from sources but incomplete · 5: zones traceable to specific source passages, no template imposed |
| R2 | Outside-In coverage | [review] | Every zone scored for purpose/audience/business-outcome legibility | 1: purpose absent or guessed · 3: purpose stated but thin · 5: a reader unfamiliar with the code could explain why the zone exists |
| R3 | Inside-Out coverage | [review] | Every zone scored for mechanism/binding/feedback legibility | 1: mechanism absent or guessed · 3: mechanism named but not traced to bindings/feedback · 5: verbs, bindings, and feedback are all named and traceable to source |
| R4 | Dual-axis completeness | [gate] | Both axes are recorded for every zone, never only the "obvious" one | 1: zones carry one axis only · 3: most zones carry both · 5: every zone carries both, no exceptions |
| R5 | Per-corpus weighting applied | [gate] | The corpus's own stated weighting (Outside-In-higher or Inside-Out-higher) is visible in the aggregation, not just asserted in prose | 1: weighting named but scores unweighted · 3: weighting applied inconsistently · 5: the weighted aggregate is computable directly from the two raw axis scores |
| R6 | Source traceability | [review] | Every scored claim in the corpus cites the harvest source it came from | 1: unsourced assertions · 3: mostly sourced · 5: every zone's every claim cites its source (prototype/PRD/brief/IDR/ADR/roadmap) |
| R7 | Aggregation/gating rule | [gate] | States which dimensions gate promotion and the threshold | 1: no rule · 3: a rule exists · 5: explicit gate set + threshold + top-failure pointer (this file's own "Gate to promote" line) |

**Gate to promote:** R1, R4, R5, R7 must each score ≥ 3 — a corpus that skipped zone discovery,
recorded one axis only, never applied its weighting, or states no gate/threshold at all is not a
usable harvest, whichever corpus it's feeding.

**Per-corpus weighting — the mechanism, not just the label.** Each corpus states its own weight as
a simple ratio applied to the two raw per-zone axis scores (R2, R3) before aggregating: this
corpus (`project-facts`, #612) weights Outside-In 60/Inside-Out 40; `harness-facts` (#613) mirrors
it at Inside-Out 60/Outside-In 40. The ratio is a starting point, not a law — a harvest run may record a
different split when a project's own shape warrants it, as long as R5 requires the split be
stated and the aggregate be computably derived from it, never asserted without the arithmetic
behind it.

**Top failure to look for first:** a harvest that scored every zone on only its "obvious" axis
(R4 = 1) — the entire reason this rubric is two-axis instead of one is lost the moment either
axis is skipped, and the corpus silently degrades to a single-lens document that reads well but
was never actually checked from the other side.

## Sources

- Ticket #612 (`harvest-domain-knowledge`) and its sibling #613 (`harness-facts`), both
  minted via `find-intent` 2026-08-18, Kim's rulings quoted verbatim above.
- `docs:make-rubric`'s rubric-for-rubrics governs this table's own shape (criteria × levels ×
  descriptors × aggregation); `docs:make-reference`'s reference-authoring standard governs this
  file's own retrievability.
