# Extraction procedure — harvesting a project's domain-knowledge corpus

This corpus (`project-facts`) extracts domain knowledge: the project-specific business logic,
technical architectures, and unique-IP structures, written for a human/business reader. Shared
definitions and the scoring rubric live once in `harvest-core.md`; this file is the step-by-step
procedure specific to this corpus's own weighting and output shape.

## Step 1 — Gather the harvest sources

Read, in this order (earliest-intent-first, so later sources are read against the belief they
ratified rather than cold):

1. **Functional prototypes** — working or demoed code that embodies a business rule before it was
   ever written down.
2. **Intent records (brief/IDRs)** — the project's own stated beliefs about what's true, upstream
   of any architecture choice.
3. **PRDs** — why the project exists, its outcomes, its non-goals.
4. **ADRs** — ratified architecture decisions and the constraints that forced them.
5. **Roadmaps/PLANs** — sequencing, showing which zones the project itself treats as separable
   units of work (a strong topic-zone signal — a roadmap phase boundary is frequently a real zone
   boundary).

A source that doesn't exist for this project is skipped, not faked — an absent PRD means the
harvest leans harder on prototypes + ADRs for that zone's Outside-In read, and the gap is named in
the corpus rather than silently backfilled.

**Zero-source exit.** If none of the five source kinds exist for this project at all — no
prototype, no brief/IDR, no PRD, no ADR, no roadmap/PLAN — stop here and report the gap; do not
proceed to Step 2 and discover zones from reading application code alone. Code-only discovery is
a materially different procedure (it substitutes inference for the sources' own stated intent)
and is out of scope for this skill unless a future revision explicitly sanctions it — this
extraction is a HARVEST of what the project already said about itself, not a from-scratch reverse
engineering pass.

## Step 2 — Discover topic zones

Per `harvest-core.md`'s discovery rule: extract every recurring subject the sources treat as a
first-class concern. A zone earns its place by recurrence across at least two independent sources
(a prototype alone naming something is a candidate, not yet a zone; the same subject surfacing in
an ADR or PRD too confirms it). Name each zone in plain business language, not an
implementation-internal name — the domain-knowledge corpus is written for the human/business
reader, so a zone is named "Billing & entitlements," not "the `BillingService` class."

## Step 3 — Score every zone on both axes

For each discovered zone, fill in both lenses from `harvest-core.md`'s rubric:

- **Outside-In**: who does this zone serve, what business outcome depends on it, how would a
  stakeholder unfamiliar with the code describe why it exists. Cite the source passage this came
  from (R6).
- **Inside-Out**: what the zone actually does mechanically — its operations, what it binds to,
  what signals success/failure. Cite the source passage this came from too; a zone's Inside-Out
  read is frequently thinner for a domain-knowledge corpus than a harness-facts one (this
  corpus's own weighting, below, is exactly this fact made explicit rather than left implicit).

## Step 4 — Apply this corpus's weighting

`project-facts` weights **Outside-In 60 / Inside-Out 40** (per `harvest-core.md`'s R5). Compute
each zone's weighted score as `0.6 * OutsideIn + 0.4 * InsideOut`; the corpus's own top-level
summary ranks zones by this weighted score, so a reader scanning the corpus sees the
business-relevance ordering the human/business consumer actually needs, not a mechanism-first
ordering that would suit the harness-facts sibling instead.

## Step 5 — Write the corpus

One reference doc per project run (`docs:make-reference` shape — canonical, one topic, headed,
dated), structured:

```
# <Project name> — domain knowledge

## <Zone 1 name> (weighted score: N.N)
- Outside-In: <finding> — source: <citation>
- Inside-Out: <finding> — source: <citation>

## <Zone 2 name> (weighted score: N.N)
...
```

Zones ordered by weighted score, descending. A zone missing either axis fails R4 at review time
and is not shipped as done — the extraction returns to Step 3 for that zone rather than
publishing a partial read as if it were complete.

## Step 6 — Score the corpus, then run the eval

Self-score the produced corpus against `harvest-core.md`'s rubric (R1–R7); gate on R1, R4, R5, R7
≥ 3 per its own promote rule. Then run `eval-harness.md`'s eval prompts against the corpus — the
harness for deliverable (c), proving the extraction produced a *valuable* corpus, not merely a
rubric-passing one.
