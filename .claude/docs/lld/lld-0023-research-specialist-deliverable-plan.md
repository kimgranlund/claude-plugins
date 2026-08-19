---
doc-type: lld
id: lld-0023-research-specialist-deliverable-plan
status: draft
version: 0.1.0
date: 2026-08-19
owner: kim.granlund
ticket: nonoun-plugins#710
idr: idr-0007 (LOCKED — .claude/docs/idr/idr-0007-solo-first-composition.md; cited for the
  job-evidence test applied in Resolution 1, never edited)
spec: none — gh#710's own Acceptance section carries the checkable criteria this LLD resolves
  against, and no externally-consumed surface is introduced (the sibling agent this plan sizes
  is a follow-up build's own component, not a contract this document exposes); a standalone SPEC
  would restate what the ticket and this LLD's Acceptance section already state (the same
  routing test lld-0017/lld-0021/lld-0022 each already applied).
scope: component
audience: builder, reviewer
---
# LLD — Research-specialist deliverable schema and evaluation rubric plan (gh#710)

**Verdict, head-first.** No new standing agent ships from this ticket — its Acceptance is the
plan, not the build (Non-goals, below). What this LLD actually resolves: (1) the deliverable
schema a web-search research dispatch must produce — a typed, dated, sourced findings record,
one row per finding, four fields beyond the raw claim (source, access-date, confidence, category)
plus two grading hooks (actionable note, novelty flag); (2) a four-axis evaluation rubric —
**knowledge, actionable, grounding, novelty-vs-known** — with real 1/3/5 anchors, not bare labels;
(3) the four planner decisions the ticket named as open, each resolved with reasons rather than
deferred: fact-finder's own contract stays untouched and a **sibling** agent is sized instead
(Resolution 1 — IDR-0007's job-evidence bar, applied, not waived); the axis set is **finalized at
four**, matching the marshal's lean exactly (Resolution 2); the checker path is **doc-checker,
unedited** — its existing "reference doc... against the owning skill's bundled rubric.md" charter
already covers this deliverable class generically (Resolution 3); and yes, an LLD was owed and
this document IS it (Resolution 4, closing gh#710's own Phase 3.6 citation). The sibling agent's
own build (its `.md` file, its rubric.md's real home, wiring it under doc-checker's grading) is
named as a follow-up (Build sequence's final row) rather than minted as a second ticket this PR
doesn't own — "names" rather than "mints," the option gh#710's own Non-goal explicitly leaves
open.

## Non-goals

- **Not building the research-specialist agent itself.** gh#710's own Acceptance is "a design/
  plan record exists" — the agent `.md` file, its final tool grants verified against a live
  build, and its rubric.md's real bundled home are follow-up work (Build sequence, final row).
- **Not rebuilding `research-methods` doctrine.** That skill's own NOT-for line already excludes
  "lookup (web search)" work — this plan reconciles against that boundary (Resolution 1), it does
  not edit the skill.
- **Not editing `harness:fact-finder`.** Resolution 1 keeps its contract — model, tool wall, body
  — untouched; this plan's sibling-not-upgrade decision is exactly what protects that.
- **Not editing `docs:doc-checker`.** Resolution 3 finds its existing charter already covers the
  new deliverable class generically; no new NOT-for line, no new artifact-class bullet is owed.
- **Not shipping a `references/rubric.md` file in this PR.** The rubric's four axes and anchors
  are fully specified below (Data), but the FILE a `make-rubric`-authored rubric.md becomes has no
  owning skill or agent to bundle under until the follow-up build lands one (Rejected
  alternatives) — authoring it homeless now would either misplace it or force a premature
  agent-shell solely to hold a file.

## Resolution 1 — Sibling agent, not a `fact-finder` contract upgrade

**Fork:** upgrade `fact-finder`'s own contract to also produce the new deliverable schema
(synthesis included), or size a sibling agent that leaves `fact-finder` untouched?

**Decision: sibling.** `fact-finder`'s own body states its no-synthesis rule is structural, not
incidental — it is deliberately Edit-less "so the allowlist itself enforces the gather≠distill
phase boundary (interleaving them is how literature-shaped files happen)," a boundary every
`/make-pack` wave depends on (parallel gatherers write raw ledgers; one distiller catches
synthesis mistakes independently, in its own later pass). This new deliverable's `knowledge` axis
explicitly grades "unique insights" and "best practices" — synthesized judgment, not raw claims —
so satisfying it inside `fact-finder`'s own contract would weaken the exact invariant every
existing `/make-pack` caller relies on, for the benefit of a caller that isn't one. That is
concrete, named job-evidence under IDR-0007's bar (a real interface conflict, not "it's different
so mint something new" — the reasoning IDR-0007 and `plan-plugin-split`'s anti-matrix both
reject): the host (or `fact-finder` itself) provably cannot hold both jobs in one contract without
one caller class paying for the other's needs. A dispatched sibling also independently earns its
place on IDR-0007's isolation ground alone — the same evidence already accepted for `fact-finder`
and `experiment-runner`'s own existence (a wide open-ended multi-`WebSearch`/`WebFetch` task
belongs in its own context, not the host's) — so this is not a new argument, it is the same one
applied a third time.

**Sibling ≠ parallel seat, in the sense the marshal's lean warned against.** The marshal's lean
(gh#710's own Findings, 2026-08-19) read "extend the existing research surfaces, don't mint a
parallel seat" as a caution against duplicating *doctrine* — and this plan does exactly that:
the sibling reuses `fact-finder`'s own confidence-marker vocabulary verbatim (Data, below), cites
`research-methods` and `pack-writing-rules` as reconciled-against doctrine rather than
reimplementing grounding rules from scratch, and routes its checking through `doc-checker`'s
already-general charter (Resolution 3) rather than a new critic. What's new is one agent
*definition* file, not a new doctrine tree — the smallest unit IDR-0007's job-evidence gap
actually requires.

## Resolution 2 — Axis set: four, as the marshal's lean proposed, with anchors

**Fork:** the seed's own axis list is open-ended ("etc.") — does the plan close it at the
marshal's proposed four, or leave it open for the build to finalize?

**Decision: closed at four** — `knowledge`, `actionable`, `grounding`, `novelty-vs-known` (Data,
below, carries full 1/3/5 anchors for each). Closing it now, rather than deferring to the build,
is itself the deliverable gh#710's Acceptance names ("evaluation rubrics... on named axes"); a
plan that reopens the axis question at build time hasn't actually decided anything. `grounding`
and `novelty-vs-known` were the seed's own "presumably" candidates — both earn their place on
inspection: `grounding` operationalizes exactly what `fact-finder`'s confidence markers already
demand (a claim without a dated, primary-preferred source is not a finding, it's an assertion),
and `novelty-vs-known` is what stops the deliverable from re-gathering what the estate's own
corpus (skills, ADRs, prior research ledgers) already states — the one failure mode raw web
search has no structural defense against on its own.

## Resolution 3 — Checker path: `doc-checker`, unedited

**Fork:** extend `doc-checker`'s charter to name this deliverable class explicitly, or mint a new
checker under `agent-writing-rules`' checker-seat consolidation test?

**Decision: `doc-checker`, as-is — no edit at all.** Applying the consolidation test's own two
prongs (`agent-writing-rules` §"Checker-seat consolidation," cited not restated): (1) identical
mechanics — `doc-checker`'s tool wall (`Read/Grep/Glob/Bash`) and its "mechanical gates first
(`doc_lint.py`), then judgment against the owning skill's bundled `references/rubric.md`" shape
apply to this deliverable with zero variation; (2) one grading standard survives — the deliverable
IS "a reference doc... scored against the owning skill's bundled rubric.md," which is already the
literal artifact class `doc-checker`'s own description names, not a near-miss requiring a new
bullet. There is no interface gap to close, so there is nothing to edit — the follow-up build
simply dispatches `doc-checker` at the rubric.md the same way any other rubric-bearing document
already does. **Rejected: a new `research-checker` agent.** Fails the consolidation test's own
negative-proof pattern (the `agent-checker`/`hook-checker`/`plugin-checker` trio, same shape,
different owning rulebook, correctly NOT merged) run in reverse — here the shapes and the owning
rulebook (whatever skill/agent ends up bundling the rubric.md) are not even distinct yet, so
minting a checker ahead of that would be inventing a seat for an artifact class `doc-checker`
already grades.

## Resolution 4 — An LLD was owed, and this is it

**Fork:** does gh#710's own materiality clear the owed-ladder's `+LLD` rung (`docs:
doc-writing-rules`'s Owed chain, `ticket only → +LLD (size: big) → +ADR → ...`), and if so, does
authoring it now resolve dispatch-ticket's Phase 3.6 spec-lock gate rather than trip it?

**Decision: yes to both.** The decision resolved in this document is contract-shaping (a seat
boundary decision under IDR-0007, a rubric that a future build and its checker will both depend
on) — squarely past the `+LLD` rung, and gh#710's own body states the same conclusion
independently ("per the owed ladder this planning task likely mints an LLD before any build").
Phase 3.6 fires on a missing owed-ladder citation with no upstream to cite; the resolution named
there for exactly this shape — "the LLD you author IS the resolution... cite it in ## Links before
PR-open" (the #649 precedent, `649-lld-v2-extension`) — is what this document performs, not a
blocker to route around. No `+ADR` rung is separately owed: both decisions this LLD makes
(Resolution 1's sibling-not-upgrade, Resolution 3's no-new-checker) are *applications* of
already-ratified canon (IDR-0007's job-evidence test; `agent-writing-rules`' consolidation test),
not new canon — the same "LLD applies, doesn't ratify" shape lld-0022 and lld-0021 both already
used against their own upstream ADRs/IDRs.

## Components

### `docs/agents/research-specialist.md` (future build, sketched here — NOT shipped by this PR)

**Amended 2026-08-19 (gh#721's own build, dated note, no history rewritten):** the follow-up
build shipped this sketch as `docs/agents/research-leader.md` / `docs:research-leader`, not
`research-specialist` — G12's naming-grammar gate rejected the sketch's own name (neither
`research` nor `specialist` resolved in any lexicon at build time); Kim's live ruling registered
`research` in `topic_lex` only and directed the rename to `research-leader` (`leader` ∈
`RoleLex`, the `*-leader` dispatched-seat production this agent's shape already fits — `research-
finder` was rejected as colliding semantically with `fact-finder`'s own no-synthesis contract).
Every other decision below (tools, model, skills, seed-prompt shape, the deliverable schema and
rubric in `## Data`) shipped as sketched, unchanged by the rename.

A new sibling agent, docs-plugin-scoped (beside `research-methods`, `make-rubric`, and
`experiment-runner`, whose doctrine it reconciles against rather than reimplements):

- **`tools`**: `Read, Grep, Glob, WebSearch, WebFetch, Write` — no `Edit`. Mirrors `fact-finder`'s
  own Write-without-Edit shape (append a fresh deliverable record, never rewrite the corpus this
  agent doesn't own), while `Grep/Glob` (absent from `fact-finder`'s own wall, which carries only
  `Read` alongside `WebSearch/WebFetch/Write`) are load-bearing here specifically for the
  `novelty-vs-known` axis — grading it requires searching the estate's own existing corpus
  (skills, ADRs, prior ledgers), not just the open web.
- **`model: fable` / `effort: high`** — per `agent-writing-rules`' seat ladder, the
  "measured-loop and queue-synthesis seats, not rubric critics" row `experiment-runner` and
  `chore-planner` already occupy (cited verbatim, not re-derived): this agent synthesizes
  judgment (unique insights, best-practice extraction) rather than executing a fully-specified
  gather with no discretion, so it does not qualify for `fact-finder`'s `haiku` floor; nor is it a
  rubric CRITIC (that's `doc-checker`, `fable + medium`) — it is a generator whose output a critic
  later grades, the same shape `experiment-runner` already has relative to `code-checker`.
- **`skills:`** — none preloaded. `research-methods` is deliberately NOT preloaded: its own
  NOT-for line excludes "lookup (web search)" work by name, and its six methods (autoresearch,
  hill-climb, ablation, sweep, bisect, adversarial) all presuppose a fixed, reproducible *scorer*
  over a *system* — this agent has neither, it has an open topic and a web. Reconciled against as
  a named sibling in the body text instead (soft mention, per `plugin-authoring.md`'s hard-for-
  preloads/soft-for-mentions boundary rule) so a reader isn't left wondering why the obvious
  doctrine skill is absent.
- **Seed prompt sketch** (body, not frontmatter): "You research ONE topic via web search and hand
  back a typed, dated, sourced findings record — never a prose report. Your dispatch names the
  topic/question cluster, any source constraints (domains, recency floor), and the deliverable
  path you own exclusively. Per finding: the claim, its category (fact | real-result |
  unique-insight | best-practice | case-study | practitioner-conversation), source, access-date,
  a confidence marker (`[verified]` only for a primary, current source; else `[inferred]` or
  `[drift-prone]` with the reason — `fact-finder`'s own vocabulary, reused verbatim, never
  reinvented), an actionable note (what a builder does with this, or 'none' — honestly, not
  padded), and a novelty flag (`new-to-corpus` or `already-documented-at: <citation>`, checked
  against this repo's own skills/ADRs/prior ledgers before the deliverable is called done). End
  by self-scoring against the four-axis rubric (Data) and listing any question left unanswered."

### `.claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md` (this file — ships now)

The plan itself: the four Resolutions above, the deliverable schema and rubric (Data), and the
Build sequence a follow-up build executes against.

## Interfaces

- **Dispatch → agent:** one sealed charter — topic/question cluster, source constraints, output
  path — same shape `fact-finder`'s own dispatch contract already uses (no new dispatch pattern
  invented).
- **Agent → deliverable file:** the agent's sole `Write` target; one row per finding (Data), plus
  the agent's own closing rubric self-score appended as a final section — the same
  generate-then-self-score shape `experiment-runner`'s "typed report + rubric self-score" already
  has, applied to a lookup task instead of a measured loop.
- **Deliverable → `doc-checker`:** once the follow-up build bundles a `references/rubric.md`
  realizing Data's four axes under whichever skill ends up owning it, `doc-checker` grades the
  deliverable against it via its existing, unmodified charter (Resolution 3) — no new interface,
  the same "reference doc against its owning skill's bundled rubric.md" contract every other
  `doc-checker` target already uses.
- **Agent ↔ `fact-finder`:** disjoint by design (Resolution 1) — no shared code, no shared file,
  no call from one to the other; the only relationship is the confidence-marker vocabulary this
  agent reuses verbatim rather than reinventing (a citation, not a coupling).
- **Agent ↔ `research-methods`:** reconciled-against, not preloaded (Components) — no interface
  at all today; if a future need arises to run one of the six methods AGAINST a research-specialist
  deliverable (e.g. autoresearch on the deliverable's own recall), that is new scope for whichever
  ticket raises it, not assumed here.

## Data

**Deliverable schema — one row per finding, six fields beyond the claim itself:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `finding` | text | yes | The claim, stated as the source states it — never paraphrased into a stronger claim than the source supports. |
| `category` | enum | yes | One of: `fact` \| `real-result` \| `unique-insight` \| `best-practice` \| `case-study` \| `practitioner-conversation` — the seed's own `knowledge` sub-facets, made typed rather than left as prose. |
| `source` | URL/citation | yes | Primary source preferred over an aggregator (mirrors `fact-finder`'s own preference rule). |
| `access-date` | ISO date | yes | Dated per this repo's `save-lessons`/`fact-finder` convention. |
| `confidence` | enum | yes | `[verified]` (primary + current) \| `[inferred]` \| `[drift-prone]` (+ a one-line reason) — `fact-finder`'s own vocabulary, reused, not reinvented. |
| `actionable-note` | text | yes | What a builder does with this finding, or the literal string `none` — an honest empty beats a padded one (mirrors `fact-finder`'s own "an empty answer honestly recorded" rule). |
| `novelty` | enum + ref | yes | `new-to-corpus` \| `already-documented-at: <citation>` — checked against this repo's own skills/ADRs/prior research ledgers, never assumed. |

**Evaluation rubric — four axes, `[review]` throughout (no axis here is mechanically gate-able;
`doc_lint.py`'s own T-checks cover the document's SHAPE, never a finding's substance):**

| Axis | 1 | 3 | 5 |
|---|---|---|---|
| **knowledge** | Findings are generic or restate the obvious; no real-result, case-study, or practitioner-conversation entries present. | A mix of facts and at least one real-result or case-study entry; some best-practice claims present but thinly sourced. | Multiple categories represented (facts + real-results + at least one unique insight or practitioner-conversation entry) with specific, checkable substance — not summary-of-summaries. |
| **actionable** | Every `actionable-note` reads `none` or restates the finding with no builder-facing implication. | Most findings carry a concrete note, but several are vague ("consider this") rather than a specific next step. | Every non-`none` note names a specific, checkable action a builder could take today, and a genuine `none` appears only where the finding truly has no build implication. |
| **grounding** | Sources are aggregator/secondary, dates absent or stale, `[verified]` claimed without a primary source backing it. | Sources are mostly primary; dates present; confidence markers used but not always matched to their own definition (e.g. `[verified]` on a source that's actually secondary). | Every source primary-preferred, every entry dated, every confidence marker matches its own stated definition — a spot-check of any three rows confirms the marker. |
| **novelty-vs-known** | No novelty check performed, or every entry marked `new-to-corpus` with no evidence a search against the existing corpus ran. | Some entries correctly flagged `already-documented-at`, but the check reads shallow (one keyword search, not a real sweep). | Every entry's novelty flag is checkable against a named citation (for `already-documented-at`) or a stated, specific negative-search scope (for `new-to-corpus`) — a reviewer can verify either claim directly. |

**Gate:** all four axes are `[review]` — no numeric gate rule beyond the follow-up build's own
`doc-checker` dispatch converging on the same scores an independent read would give; this LLD
does not itself impose a numeric threshold, deferring that to the rubric.md's own authoring pass
(`make-rubric`'s own "Create" step, owed to the follow-up build per Rejected alternatives below).

## Risks

- **R-1 — the sibling agent, once built, drifts back toward `fact-finder`'s own job over time**
  (scope creep: someone dispatches it for a plain gather-only task because it's "the research
  agent now"). Mitigated by Resolution 1's disjointness being stated explicitly in both agents'
  own descriptions once built — `fact-finder`'s NOT-for line and this agent's own would each name
  the other as the wrong tool for a gather-only vs. synthesis-required task. Locus: spec (the
  follow-up build's own agent description is where this is actually enforced).
- **R-2 — `novelty-vs-known` grading is only as good as the corpus search actually run**, and a
  shallow keyword search could pass the rubric's own 3-anchor without catching a real duplicate.
  Named as a real limitation of a `[review]`-only axis rather than hidden; the rubric's own 5-anchor
  requires a "specific, checkable... scope," which gives a reviewer something to spot-check against,
  but does not make the check mechanical. Locus: plan (a future `novelty_check.py`-style script
  is a legitimate follow-up extension this LLD doesn't build).
- **R-3 — deferring the rubric.md file itself to the follow-up build means gh#710's Acceptance
  ("evaluation rubrics" as a plan deliverable) is satisfied by this document's Data section, not
  by a shippable artifact.** Disclosed rather than assumed away: the axes and anchors above ARE
  the rubric's real content, fully specified; what's deferred is only the physical `make-rubric`-
  authored file and its bundling location, which has no home until an owning skill/agent exists
  (Rejected alternatives). Locus: spec (this document IS the spec for that future file's content).

## Rejected alternatives

- **Upgrading `fact-finder`'s own contract to add synthesis.** Rejected — Resolution 1; breaks
  the structural no-synthesis invariant every `/make-pack` caller depends on.
- **A new `research-checker` agent.** Rejected — Resolution 3; `doc-checker`'s existing charter
  already covers this artifact class generically, and the consolidation test's negative-proof
  pattern (same tool wall ≠ same seat) applies here in reverse — there isn't even a distinct
  owning rulebook yet to justify a split.
- **Leaving the axis set open for the follow-up build to finalize.** Rejected — Resolution 2;
  gh#710's own Acceptance names "evaluation rubrics... on named axes" as this ticket's own
  deliverable, not the next one's.
- **Shipping a `references/rubric.md` file in this PR.** Rejected — R-3; no owning skill or agent
  exists yet to bundle it under. Authoring it homeless now would either misplace it (guessing a
  plugin location the follow-up build might reverse) or force minting a premature agent-shell
  solely to hold one file — real cost for a distinction (this PR vs. the next) that buys nothing
  the follow-up build's own `make-rubric` pass doesn't already owe.
- **Filing the follow-up build as a second GitHub issue from inside this dispatch.** Rejected —
  gh#710's own Non-goal explicitly offers "mints or names" as alternatives; naming it here (Build
  sequence's final row) keeps this PR's scope to the plan alone, and a human or the next
  `mobilize-chores` sweep can mint the ticket from this LLD's own Components/Data sections when
  ready to build.

## Agent verification

Per `docs:agent-harness-rules`, the assert layer is the cheapest one that catches this document's
own failure modes — pure text/structure, no browser or live-human layer needed for THIS ticket's
own Acceptance (the plan, not the built agent). **Mechanical layer:** `doc_lint.py` on this LLD
(frontmatter fields, required sections, spine-ID uniqueness against `origin/main`). **Fresh-context
checker:** `docs:doc-checker` on this LLD before merge (a design decision document, judged against
`doc-writing-rules`' own LLD contract) — the semantic-edit-rides-a-critic invariant
(`.claude/rules/plugin-authoring.md`), applied to a new mint rather than an edit. **Deferred to
the follow-up build:** the sibling agent's own instrument (a `doc-checker` dispatch at its bundled
`rubric.md`, per Resolution 3 — no new instrument to design, the existing one already reaches it)
and any script this LLD's R-2 might eventually justify (`novelty_check.py`) — neither is owed by
this ticket's own Acceptance.

## Build sequence

| # | Step | Path | Done when |
|---|---|---|---|
| 1 | Draft this LLD, resolve the four forks | `.claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md` | fresh-context `docs:doc-checker` pass recorded, findings fixed |
| 2 | Dated Findings write-back on gh#710, citing this LLD in `## Links` | gh#710 | comment posted, Links section updated |
| 3 | *(follow-up build, not this ticket)* Author `docs/agents/research-specialist.md` per Components | `docs/agents/research-specialist.md` | `harness:agent-checker` pass green |
| 4 | *(follow-up build)* Author the rubric.md realizing Data's four axes via `make-rubric`'s own Create step, bundled under whichever skill the build lands it in | TBD at build time | `make-rubric`'s own gate + a `docs:doc-checker` pass |
| 5 | *(follow-up build)* One worked dry-run dispatch against a real topic, scored against the rubric | — | self-score recorded, `doc-checker` verdict converges |

## Acceptance (checkable predicates)

1. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md` → exit 0.
2. `grep -n "^| Field" .claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md` shows the
   deliverable-schema table header present under `## Data`.
3. `grep -n "^| Axis" .claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md` shows the
   four-axis rubric table header present, and `grep -c "^| \*\*" .claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md`
   returns at least `4` (one row per axis, each bold-named).
4. `grep -n "^## Resolution [1-4]" .claude/docs/lld/lld-0023-research-specialist-deliverable-plan.md`
   returns exactly four matches — the four planner decisions gh#710 named as open, each resolved.
5. Fresh-context `docs:doc-checker` verdict on this LLD recorded in gh#710's dated Findings
   write-back, zero unresolved blocker/major findings.
6. gh#710's `## Links` section cites this LLD's path before the PR opens (the #649 precedent,
   closing dispatch-ticket's own Phase 3.6 citation requirement).
