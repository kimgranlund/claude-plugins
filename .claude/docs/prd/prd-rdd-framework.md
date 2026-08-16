---
doc-type: prd
id: prd-rdd-framework
status: draft
version: 0.1.0
date: 2026-08-16
owner: kim.granlund
---
# PRD — RDD (Roadmap Decision Records): realizing the bible's PRP as a docs type

## Problem

This repo's docs type system has no locked, cited, DRI-accountable record of a *release
commitment*. `plan` (Steps/Validation/Rollback, `active → complete/abandoned`) is a living execution
runbook with no lock and no citation requirement. `roadmap` (Now/Next/Later, `active → retired`)
is a living index that never locks by design. `ticket` (`kind: feature`, Scope/Acceptance/Links)
is a work item whose `Links` section is unenforced prose, archived on close but never
citation-gated or DRI-accountable. None of the three carries what the corpus's own doctrine
(`.claude/docs/spec/product-lifecycle-bible.md`, Part 4) names as the Releases loop's locked
record — the **PRP** (Product Release Plan): scope, IDR-grammar acceptance criteria, sequencing,
citations (≥1 ADR and/or IDR), a DRI, and a completion clause, `draft → locked at release
commitment → shipped-and-archived, or superseded-with-reason`. Kim ruled 2026-08-16: this type
should exist in this repo, under the name **RDD**, not PRP — realizing the bible's concept rather
than leaving it a doctrine-only abstraction #273's sibling PRD (`prd-idr-framework.md`) mapped
away. This PRD scopes RDD as a docs-plugin type, mirroring #273 → `prd-idr-framework.md`'s shape:
a scoping PRD, not the type build (#316, the IDR implementation, is the same pattern's realized
precedent).

## Users

**Primary:** the seat locking a release commitment at Spec-lock/release-commitment time — the
same actor who today would otherwise write an unenforced TICKET `Links` line and call it done.
**Secondary:** an ADR author checking whether a PRP-grade release repeatedly failed against their
decision (the bible's escalation-rides-the-citations rule); `decision-watcher` and
`chore-planner`, which gain a new corpus to walk once RDD exists; a cold-start human or agent
answering "what did we actually commit to ship, and did it ship" from `project-docs` rather than
reconstructing it from closed GitHub issues.

## Outcomes

- **OUT-01** — `doc_lint.py` recognizes `doc-type: rdd` with the same structural rigor as `idr`:
  required sections present, status enum enforced, and a `locked` RDD whose HEAD commit is already
  `locked` is blocked from in-place content edits — verifiable by a selftest fixture pair
  (positive: locked-edit blocked; negative: draft-edit allowed), reusing the ADR/IDR ledger-lock
  mechanic (see Type contract — Mutability below for the one narrow extension this reuse needs).
- **OUT-02** — A `locked` RDD with an empty `decision-refs:` citation list, OR an empty `dri:`
  field, FAILS `doc_lint` (not merely WARNs) — verifiable by two selftest fixture pairs (locked +
  empty refs → FAIL; locked + ≥1 ref → clean; and the same pair for `dri:`). Deliberately
  stricter than T6's ADR-orphan WARN (Delta/Citation spine below explains why RDD earns FAIL where
  ADR only earns WARN); DRI-accountability rides the identical mechanism rather than staying an
  unenforced Problem-statement claim (see Type contract — Frontmatter, below).
- **OUT-03** — the `project-docs` consult table (or the equivalent consult skill in an adopting
  repo) contains a row pointing "what release commitments has this project made, and are they
  live" at `.claude/docs/rdd/` plus the ROADMAP — verifiable by the row's presence, same
  fixture-grade check `prd-idr-framework.md`'s own OUT-03 settled for.
- **OUT-04** — at least one `decision-watcher`-queued candidate, once the escalation-detection
  extension (Implementation surface item 6, deferred) ships, surfaces a case where ≥2
  `superseded` RDDs cite the same ADR — giving the bible's escalation rule a live, non-vacuous
  target. Gated on that deferred item; **not required for this PRD's own v0.1 approval**, listed
  here only so item 6 has a named, checkable target when it ships.

## Non-goals

- **Not building any of the implementation surface.** `doc_lint.py` support, `doc-writing-rules`
  template/table, `make-doc` routing, `project-docs` indexing, and the `decision-watcher`
  extension are enumerated below as follow-up build scope — this ticket's (#318) own acceptance
  line requires enumeration, not construction, here, exactly as #316 followed from #273.
- **Not retiring or restructuring `plan` or `roadmap`.** The Delta section below concludes RDD
  sits beside both, not instead of either — no type is deprecated by this PRD.
- **Not retrofitting closed TICKETs with `decision-refs:`-shaped citations.** RDD is a new type
  for new release commitments going forward; no backfill sweep over existing closed tickets is in
  scope.
- **Not resolving the residual `shipped-and-archived` mechanics question** (Type contract —
  Mutability below) with certainty — flagged as Open question 1 for Kim, a recommendation given,
  not silently picked, per the same discipline `prd-idr-framework.md`'s Cardinality section used.
- **Not an ADR.** Per the standing ADR-default-no ruling, no genuine architectural fork is
  ratified by this scoping alone — RDD extends the already-ratified IDR/ADR ledger-lock mechanic
  (T4, live since #316) rather than inventing a new mutability class.

## Source of truth

This PRD points at, rather than restates, `.claude/docs/spec/product-lifecycle-bible.md` Part 2
(the three loops) and Part 4 (the IDR/ADR/PRP table, "Rules that make the records real," and
"Escalation rides the citations") — read it directly for the full model; this document only
restates the fragments a type-contract decision turns on. It also reconciles with, and in part
supersedes a conclusion of, `.claude/docs/prd/prd-idr-framework.md`'s own Delta section — see
immediately below.

## Delta — resolving the DELTA/overlap with `plan`, `roadmap`, and TICKET

### Reconciling with `prd-idr-framework.md`'s prior reading

`prd-idr-framework.md` (#273, merged) read the bible's PRP as: *"maps closely onto this repo's
TICKET (`kind: feature`...) combined with PLAN... the union already covers PRP's contract; no new
PRP type is proposed."* Kim's 2026-08-16 ruling overrides that **conclusion** — not because the
underlying observation was wrong (TICKET+PLAN genuinely do cover PRP's *scope/sequencing* fields),
but because that observation under-weighted the fields TICKET+PLAN do **not** cover at all: a
`locked` state (append-only once committed), an enforced citation spine (`decision-refs:`, ≥1
ADR/IDR — TICKET's `Links` section is prose, never `doc_lint`-checked for count or presence), and
a DRI field (neither type carries one). At the time #273's PRD was written, IDR itself didn't yet
exist — the citation-spine gap PRP is supposed to close was abstract. Now that IDR is real (#316,
merged, `docs` 1.5.0) and ADR's own upstream citation gap is a live, `doc_lint`-enforced WARN
(T6), the parallel gap on the *Releases* side — nothing stops a "shippable unit" from existing
with zero traceability to the ADR/IDR it serves — is no longer abstract either. This PRD's
conclusion: **RDD is genuinely new, not a re-labeling of TICKET+PLAN** — see the three delta
comparisons below.

### vs. `plan` (Steps · Validation · Rollback, `active → complete`)

`plan` is an execution runbook: living state, no lock, no citation requirement, oriented around
*how to carry out a change safely* (validation steps, a rollback path) — the class is "Living
state" (doc-writing-rules' four-class table), meaning forking is the canonical failure, not
premature locking. RDD is the opposite shape on the axis that matters: a **locked commitment
record** — once `locked`, its Scope/Acceptance/Sequencing/citations/DRI are append-only (Ledger
class, mirroring ADR/IDR), and its failure mode is "renegotiating a locked PRP without a version"
(bible, Part 8 anti-patterns table) — the same "silent edit destroys the record" failure ADR/IDR
already guard against, which `plan` was never designed to guard against because `plan` is never
*supposed* to lock. **Delta:** `plan` answers "how do we execute this safely, with a rollback
path" (tactical, revisable); RDD answers "what release commitment did we lock in, cited to which
decisions, and who's accountable" (governance, append-only post-lock). A release's execution may
still use a `plan` document for a risky migration's own rollback steps — RDD doesn't replace that
use, it sits above it. **Verdict: sits beside `plan`, does not absorb or replace it** — even
though "sequencing" (RDD) and "Steps" (plan) sound adjacent, they answer different questions
(commitment vs. execution) and the honest answer here is genuinely not "RDD absorbs plan," despite
the ticket naming that as a live candidate to test for.

### vs. `roadmap` (Now · Next · Later, living)

No delta to design here — this is the same relationship ADR already has to its own "architecture
overview" living index, and IDR to its "product brief." The bible states this directly: RDD's
(PRP's) living index **is** the roadmap — "releases lock, the roadmap breathes." `roadmap`
already exists in this repo with exactly the right shape (`active → retired`, Now/Next/Later) to
serve as RDD's living index with **zero changes required** to the `roadmap` type itself. **Delta:
none** — RDD is the locked record the existing `roadmap` type already assumes exists upstream of
it; this PRD makes that assumption real rather than changing `roadmap`.

### vs. TICKET (`kind: feature`, Scope/Acceptance/Links, work item, archived on close)

TICKET is per-shippable-unit and freely editable while open (work-item class); RDD is per-release
(potentially bundling several TICKETs' scope into one committed release) and append-only once
locked (ledger class). A TICKET's `Links` section is informal prose with no `doc_lint`-enforced
minimum; RDD's `decision-refs:` is a structurally-required, FAIL-gated field (Outcomes OUT-02).
TICKET has no DRI field or completion-clause discipline distinct from its own `done`/`wontfix`
close verbs. **Delta:** TICKET is the shippable-unit work item; RDD is the release-grain
commitment ledger one or more TICKETs execute against — genuinely different grain and mutability,
not a synonym. **Verdict: sits beside TICKET too** — a release's RDD cites the TICKETs it bundles
(via ordinary prose links in `## Sequencing`, not a new ID-spine field — TICKET is a work item,
not a ledger citee, so it stays outside `decision-refs:`'s ADR/IDR-only scope).

### Conclusion

RDD is not a variant of `plan`, `roadmap`, or TICKET. It fills the same class of real gap
`prd-idr-framework.md` already proved for IDR: none of the existing types carry a falsifiable,
lock-gated, DRI-accountable, upward-cited release commitment — `plan` is tactical and unlocked,
`roadmap` is living and never locks by design, TICKET is per-unit and citation-unenforced. RDD
sits beside all three, filling the Releases loop's locked-record slot the bible's own three-part
table (IDR/ADR/PRP) says every loop needs exactly one of.

## Naming — collision test and recommendation

Ticket #318's Acceptance item 2 asks to test `rdd` against `doc_lint.py`'s lowercase-token
namespace, "same test class the IDR PRD ran."

**Namespace collision test (`doc_lint.py`'s `TYPES` dict).** Current keys: `adr` / `prd` / `spec`
/ `lld` / `plan` / `roadmap` / `ticket` / `task` / `idr`. `rdd` is a new lowercase, unhyphenated,
three-letter token — no collision, and consistent in shape with `adr`/`idr` (both three-letter
`X`+`D`+`R`-family tokens for "`X` Decision Record"). **This is itself the naming
recommendation's strongest argument** (below): `rdd` completes a symmetric family — `IDR` (Intent
Decision Record, North star), `ADR` (Architecture Decision Record, Foundation), `RDD` (Roadmap
Decision Record, Releases) — one grammar, one token shape, one suffix, across all three loops.
The bible's own literal term for the Releases-loop record is **PRP** (Product Release Plan), a
different acronym family entirely (no "Decision Record" suffix). Kim's ruling to use **RDD**
rather than reusing PRP verbatim is, read this way, not an arbitrary rename — it's completing the
`_DR` family grammar IDR and ADR already established, at the cost of diverging from the bible's
own literal PRP term (a deliberate, load-bearing choice worth stating plainly rather than treating
as a bare label swap).

**Full-name recommendation: `RDD` / "Roadmap Decision Record"** (singular, matching ADR's
"Architecture Decision Record" and IDR's "Intent Decision Record" — the ticket title's own
"Roadmap Decision Record**s**" plural is the type-family name, individual instances are singular:
`rdd-0001`, "the RDD," exactly as `idr-0001`/"the IDR"). **Rejected alternative: bare `PRP`.**
Costed and rejected for two reasons: (1) it breaks the `_DR` family grammar the other two loops
already use, reintroducing exactly the kind of "one home per fact, but two names for it" drift the
bible itself warns against (Part 5, Part 6 habit 2) — if `RDD` and `PRP` both circulate for the
same concept, that is itself a restated-fact violation; (2) `PRP` collides with real domain terms
outside this corpus (e.g. "platelet-rich plasma," "pull request pending" in casual dev shorthand)
that `RDD` does not carry, for no offsetting gain once the `_DR` family argument is in hand.

**Collision test against a routing surface (mirrors the IDR PRD's `find-intent` test).** No
skill in this estate's routing surface triggers on bare "roadmap" as an imperative phrase the way
`find-intent` triggers on "what am I really asking for" — the four `roadmap`-mentioning files
found (`project-docs`, `doc-writing-rules`, `make-vision-memo`, `check-state`) all reference it as
a **noun** (a document type or a section of one), never as a command-routing trigger phrase. Same
reasoning IDR's PRD already established and settled: doc types are id/command-addressed
(`/make-doc rdd`), never description-routed the way a skill is — **no collision is possible in
this namespace by construction**, so this test is confirmatory, not exploratory, for any new
`doc_lint` type token. **Verdict: no collision** — `RDD` is safe to adopt.

**ADR-0011 grammar test.** Already settled by `prd-idr-framework.md` for `idr` and cited here
rather than re-argued (one-home-per-fact): a `doc-type` frontmatter token is not an agent, command,
or skill name — ADR-0011's naming grammar (`spec-naming-convention.md`) does not bind this
decision at all; the binding namespace is `doc_lint.py`'s own `TYPES` dict, tested above.

## The citation spine — lintable vs. judgment-tier

Ticket #318's Acceptance item 3 asks how the bible's "escalation rides the citations" rule (Part
4: *"A PRP repeatedly failing against the same ADR is evidence for an ADR revision. An ADR
falsified by build reality climbs to an IDR revision."*) becomes lintable or stays judgment-tier.
This splits cleanly into two different mechanisms, at two different grains:

**Lintable today — citation presence, one file at a time (`doc_lint.py`).** A new frontmatter
field, `decision-refs:` (parallel to ADR's own `intent-refs:`), required once an RDD reaches
`locked` status. **Wire format, pinned:** `doc_lint.py`'s `parse_frontmatter` is a line-based
scalar parser (one `key: value` per line — it does not read YAML block lists; a `- adr-0001`
continuation line parses as nothing, leaving the key's value empty). `decision-refs:` is
therefore a single-line, comma-or-space-separated scalar of ids on the SAME line as the key —
`decision-refs: adr-0002, idr-0001` — exactly the form `intent-refs: idr-0001` already uses for
one id; T7 (below) splits on `,`/whitespace the same way any future multi-id ADR field would need
to. Unlike ADR's T6 (WARN-only, because 13 existing ADRs predate `intent-refs:` and a hard FAIL
would break every one of them retroactively), **RDD has zero existing instances** — there is no
retrofit debt, so this PRD recommends a hard **FAIL** (new check, next available code — `T7` at
the follow-up ticket's implementation time) the moment `status: locked` (or beyond) carries an
empty/missing `decision-refs:` **or an empty/missing `dri:`** (Outcomes OUT-02 folds both fields
into the same check — DRI-accountability is a Problem-statement claim this PRD makes, so it earns
the identical enforcement, not a softer judgment-tier carve-out). `draft` RDDs are exempt for
both fields (citations and DRI assignment may genuinely not be settled yet — the same "harvest
window" reasoning IDR's `draft` state already gets). This closes OUT-02: a release simply cannot
lock without at least one upward citation and a named accountable human, mechanically, from day
one — the ADR-orphan problem RDD would otherwise silently reproduce a third time, on two axes
instead of one.

**Judgment-tier — the escalation PATTERN itself, cross-document, over time.** "Repeatedly failing
against the same ADR" is a claim about **multiple** RDDs (a count ≥2, over an unspecified but
real time window) sharing a `decision-refs:` citation while ending `superseded` — `doc_lint.py`
lints exactly one file per invocation; it has no cross-corpus memory and should not grow one (that
would turn a fast structural linter into a stateful analytics job, a different tool). This is
squarely the shape `decision-watcher` (harness) already handles for the ADR corpus itself: a
content-hash-checkpointed periodic sweep that **queues a candidate, never authors the fix**. The
concrete, deferred extension (Implementation surface item 6, below): `decision-watcher`'s sweep
additionally globs `docs/rdd/*.md`, groups by `decision-refs:` entries, and queues a harvest
candidate when ≥2 `superseded` RDDs cite the same `adr-NNNN` — exactly decision-watcher's existing
"classify, judge against a frequency/impact bar, queue, never author" contract, extended to a new
corpus rather than given new authority. **The verdict — does this pattern actually warrant an ADR
revision — stays human**, same as every decision-watcher candidate today; this PRD does not
propose auto-triggering anything. The IDR-side half of the rule ("an ADR falsified by build
reality climbs to an IDR revision") is the same mechanism one hop further upstream and is not a
new instrument — once the RDD→ADR extension exists, chaining it to `intent-refs:` on the
implicated ADR is the identical pattern, not separately scoped here.

## Type contract

### Frontmatter

```yaml
doc-type: rdd
id: rdd-0001                  # rdd-NNNN, sequential like adr-NNNN/idr-NNNN
status: draft                  # draft | locked | superseded  (see Mutability, below, on
                                # shipped-and-archived — NOT a fourth enum value in the primary
                                # design)
date: YYYY-MM-DD
owner:
dri:                           # the named accountable human (bible: "a DRI can explain what
                                # shipped") — distinct from owner (who authored the record);
                                # required non-empty at `locked` (T7, FAIL)
decision-refs:                 # comma/space-separated adr-NNNN / idr-NNNN ids, ONE line —
                                # parse_frontmatter is a scalar parser, no YAML block lists;
                                # e.g. `decision-refs: adr-0002, idr-0001` — required non-empty
                                # at `locked` (T7, FAIL — see Citation spine above)
supersedes: null                # rdd-NNNN when replacing a prior release commitment
```

### Required sections (`doc_lint.py` T3)

Four sections, mapped directly off the bible's own "Contains" row (Part 4: *"Scope · acceptance
criteria (IDR-grammar, feature grain) · sequencing · citations · DRI · completion clause"*) — DRI
and citations move to frontmatter (single accountable fields, not prose, per doc-writing-rules'
own "frontmatter is the type; prose is the payload" practice), leaving four prose sections:

| Section | Contract |
|---|---|
| `## Scope` | What this release commits to shipping — feature grain, same admission test as the bible's own: *"could two reasonable teams ship different releases from this roadmap line?"* If no, the line doesn't earn its own RDD. |
| `## Acceptance` | Criteria in **IDR-grammar** — each phrased as a testable claim that could fail (the ticket's own Acceptance item 1 language), never a task checklist. Mirrors IDR's own `## Claim` discipline, applied per acceptance line rather than once for the whole document. |
| `## Sequencing` | Ordering/dependencies across the bundled TICKETs (plain prose links — TICKET is a work item, not an ID-spine citee, so this stays outside `decision-refs:`). |
| `## Completion` | The completion clause: what "shipped-and-archived" or "superseded-with-reason" concretely means for *this* release and where the evidence lives — mirrors IDR's `## Proof` discipline (a reference, never inlined content). |

### Mutability class & lifecycle

**Reuses the existing Ledger class** (doc-writing-rules' four-class table, alongside ADR/IDR) —
`draft` (freely editable, the harvest window) → `locked` (T4 blocks in-place content edits, the
release-commitment ratification act — legal exactly the way `proposed→accepted` and
`draft→locked` already are for ADR/IDR) → `superseded` (terminal; a new RDD cites `supersedes:`,
never an in-place edit).

**Primary design (recommended): `shipped-and-archived` is NOT a fourth status enum value.**
`LEDGER_LOCK["rdd"] = "locked"` reuses T4 **verbatim**, no new mechanic — the same one-line
extension #316 already proved for IDR. The bible's own framing, *"releases lock; the roadmap
breathes,"* is read literally: completion tracking (did it ship, is it still live) belongs to the
**living index** (`roadmap`), not a second in-place edit to the locked ledger record. A shipped
RDD stays `locked` forever, byte-identical, its evidence preserved exactly as committed at
lock-time (arguably a *more* faithful "never edit a locked ledger" reading than a status a human
must remember to flip); the `roadmap`'s own Now/Next/Later movement is where "this release
shipped" becomes visible over time, and a `superseded-with-reason` release gets a **new** RDD
citing `supersedes:`, exactly the ADR/IDR pattern.

**Alternative (not recommended): a fourth `shipped-and-archived` status plus a narrow T4
extension.** Would require generalizing T4's guard from "any edit to a committed-locked-status
file is blocked" to "blocked, EXCEPT a status-field-only flip from `locked` to
`shipped-and-archived`, content sections byte-identical" — genuinely new mechanics `doc_lint.py`
has never needed before (ADR/IDR never need an in-place terminal flip; their completion is always
"mint a new record"). Costed here rather than silently chosen against: it more literally matches
the bible's four-word status list, at the price of a new class of guard logic and a real risk of
the exact "renegotiating a locked PRP without a version" anti-pattern if the narrow allow-list is
ever mis-scoped.

**Open question 1 for Kim** (flagged, not silently picked, same discipline
`prd-idr-framework.md`'s Cardinality section used): does the primary design's "the roadmap tracks
completion, the RDD stays locked forever" reading satisfy the bible's literal four-state list, or
is the explicit `shipped-and-archived` status value load-bearing enough to warrant the T4
extension in the Alternative? This PRD proceeds on the primary design as its recommendation for
Implementation surface item 1.

### File & directory convention

`.claude/docs/rdd/rdd-0001-<slug>.md` — the canonical type-prefixed numbered-ledger form, matching
`idr-0001-<slug>.md`'s directory convention exactly (doc-writing-rules' directory map gains one
new row: `docs/rdd/`). Repo-rooted, never plugin-rooted, per doc-writing-rules' existing rule.

## ID-spine position

RDD sits at the Releases loop, downstream of both ADR (Foundation) and IDR (North star) — it
**cites** `≥1` of either via `decision-refs:`, never the reverse (ADR/IDR do not cite RDD; the
containment direction only runs outward-to-evidence, per the bible's own "inner loops emit
evidence outward" mechanic — an RDD climbing a failure to an ADR is the ADR gaining a NEW
`intent-refs:`-shaped citation pattern in the deferred escalation extension, not RDD being cited
FROM the ADR). Citable FROM `roadmap` (its own living index) and, informally, from the TICKETs it
bundles (plain links, `## Sequencing`). Position in the type contract table: a new row, class
`ledger` (third Ledger-class member alongside ADR and IDR), no reordering of the existing nine
rows needed.

## Implementation surface (follow-up build scope — enumerated, not built here)

1. **`doc_lint.py`** *(realizes OUT-01)* — add `"rdd"` to the `TYPES` dict (status enum
   `draft`/`locked`/`superseded`, sections `Scope`/`Acceptance`/`Sequencing`/`Completion`); add
   `"rdd": "locked"` to `LEDGER_LOCK` (verbatim reuse, per the primary Mutability design); add
   selftest fixtures (positive: locked-RDD-edit blocked; negative: draft-RDD-edit allowed;
   regression: existing ADR/IDR fixtures unaffected).
2. **`doc_lint.py` — new T7 citation+DRI-presence FAIL** *(realizes OUT-02)* — a `locked` (or
   beyond) RDD with an empty/missing `decision-refs:` OR an empty/missing `dri:` FAILs; `draft` is
   exempt on both. `decision-refs:` parses as a single-line comma/space-separated scalar (pinned
   wire format, Citation spine above — NOT a YAML list; `parse_frontmatter` cannot read one).
   Selftest fixtures: locked + empty refs → FAIL; locked + empty dri → FAIL; locked + ≥1 ref and
   non-empty dri → clean.
3. **`doc-writing-rules` SKILL.md** — add the RDD row to the type contract table and to the
   mutability-classes table (Ledger class, third member); add `references/templates/rdd.md`
   mirroring `adr.md`/`idr.md`'s structure; add `docs/rdd/` to the canonical directory list;
   update the failure catalog.
4. **`make-doc` routing** — recognize `rdd` as a mintable type; generate `rdd-000N-<slug>.md`
   under `.claude/docs/rdd/`; prompt the Scope section's own admission test ("could two reasonable
   teams ship different releases from this roadmap line?") before minting, same spirit as
   ADR's/IDR's own gates.
5. **`project-docs` consult-table row** *(realizes OUT-03)* (or the equivalent consult skill in an
   adopting repo) — add a row: *"A locked release commitment — scope, citations, DRI"* →
   `.claude/docs/rdd/` (`RDD-*`, `locked` = append-only) plus the `roadmap`'s own living view for
   what's currently shipping. Not touched by this PRD's own branch — real follow-up work.
6. **`decision-watcher` extension** *(realizes OUT-04, deferred)* — extend the standing ADR-review
   seat's sweep to also glob the repo-relative `.claude/docs/rdd/*.md` (this repo's actual file
   path — distinct from item 3's `docs/rdd/` shorthand, which is doc-writing-rules' own
   documentation-table notation, not a literal glob), parse each RDD's `decision-refs:` scalar,
   group by cited id, and queue a harvest candidate when ≥2 `superseded` RDDs cite the same ADR —
   the mechanized half of "escalation rides the citations" (Citation spine section, above). Lives
   in `harness`, cross-plugin from `docs` — explicitly out of this scoping PRD's own file set,
   same boundary #316's own PRD used for its bootstrap-auto-mint deferral.
7. **Selftest fixtures** — RDD joins the template self-consistency sweep (`doc_lint.py selftest`
   already walks every template in `references/templates/`; adding `rdd.md` there is the whole
   registration, no separate wiring).
8. **`docs` plugin version bump** — owed only once item 1 (or later) actually touches
   `docs/scripts/doc_lint.py` or another plugin-rooted file; **not owed by this PRD's own PR**
   (verified below — no plugin content touched here, mirroring `prd-idr-framework.md`/PR #304's
   own verified-clean precedent). **Named deviation:** ticket #318's own Acceptance item 5 reads
   "`docs` plugin version bump when the PRD itself lands (scoping-doc mint, not the type build)" —
   this PR does not bump it, for the mechanical reason just given (the PRD is a workspace doc
   under `.claude/docs/prd/`, outside every plugin's own directory; PR #304 set exactly this
   precedent for the sibling #273 PRD without a bump). Flagged explicitly here so #318's close-out
   reads this as a verified, reasoned deviation rather than an unmet acceptance line.

## Gate output

```
$ python3 docs/scripts/doc_lint.py .claude/docs/prd/prd-rdd-framework.md
doc_lint · clean · .claude/docs/prd/prd-rdd-framework.md
```

No docs-plugin content touched (the PRD is a workspace doc under `.claude/docs/prd/`, same as
`prd-idr-framework.md`) — no plugin version bump or README ledger entry needed; verified via `git
diff --stat` against `origin/main` (single new file, outside every plugin's own directory).

## Open questions for Kim

1. Mutability: does the primary design (`shipped-and-archived` tracked by the `roadmap`'s own
   living movement, RDD stays `locked` forever with only `draft`/`locked`/`superseded` as literal
   status values) satisfy the bible's literal four-state list, or is a fourth
   `shipped-and-archived` enum value — and the narrow T4 extension it requires — wanted instead
   (Type contract — Mutability, above)?
2. Should `decision-refs:` validate that each cited id structurally resolves to an existing
   `adr-*`/`idr-*` file (a stronger check than mere non-emptiness), or is presence-only sufficient
   for v1, with resolution-checking deferred alongside item 6's decision-watcher extension?
3. Is the `decision-watcher` extension (Implementation surface item 6) wanted as a near-term
   follow-up alongside the type build (item 1-5, 7-8), or should it wait until enough RDDs exist
   for the pattern to be non-vacuous — this PRD assumes the latter (deferred, not blocking).
