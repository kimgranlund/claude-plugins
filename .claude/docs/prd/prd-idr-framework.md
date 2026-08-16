---
doc-type: prd
id: prd-idr-framework
status: draft
version: 0.1.0
date: 2026-08-16
owner: kim.granlund
---
# PRD — Intent Decision Records (IDR): a founding-hypothesis ledger for the docs type system

## Problem

This repo's docs type system has no place to record *why a project believes what it's building
matters* before any architecture choice exists. ADR captures "we chose X over Y" — a HOW decision
that already presupposes a goal worth pursuing. Nothing upstream of ADR captures the goal itself as
a falsifiable, cited, superseded-on-evidence claim. Issue #273 asks to scope that missing type —
"a project starts with an initial INTENT record, then builds context, documentation, and captured
knowledge against it." Mid-build, Kim surfaced that this repo's own internal doctrine corpus
already names this concept: **IDR — Intent Decision Record** (`.claude/docs/spec/product-lifecycle-bible.md`,
Part 4). This PRD scopes IDR as a docs-plugin type, not a fresh invention beside it — realizing
existing doctrine rather than duplicating it, per the corpus's own "one home per fact" rule
(bible Part 6.2).

## Users

**Primary:** any session doing Kickoff-stage work on a project that adopts this pattern — the seat
that starts a plugin/project and needs a place to record the founding hypothesis before any
architecture decision is defensible. **Secondary:** ADR authors who need to cite the intent a
decision serves (closing the "orphan ADR" gap the bible names); `project-docs`/equivalent
consult surfaces answering "what is this project's founding claim"; a cold-start human or agent
joining later, for whom the IDR ledger is the fastest way to recover *why*, not just *what*.

## Outcomes

- **OUT-01** — `doc_lint.py` recognizes `doc-type: idr` with the same rigor as `adr`: required
  sections present, status enum enforced, and a `locked` IDR whose HEAD commit is already `locked`
  is blocked from in-place edit — verifiable by a selftest fixture pair (positive: locked-edit
  blocked; negative: draft-edit allowed), mirroring the existing accepted-ADR fixture.
- **OUT-02** — A newly bootstrapped project/plugin using this pattern has exactly one `idr-0001`
  in `draft` status created in the same commit as its skeleton — verifiable by
  `find .claude/docs/idr -name 'idr-0001*'` after a bootstrap run.
- **OUT-03** — `project-docs` (or the equivalent consult skill in an adopting repo) answers "what
  hypothesis is this project built on" by pointing at `.claude/docs/idr/`, not "absent."
- **OUT-04** — at least one ADR in the adopting repo carries a non-empty `intent-refs:` field
  citing an IDR, giving the eventual "orphan ADR" check a non-vacuous target. Gated on
  Implementation surface item 7 (deferred); **not required for this PRD's own v0.1 approval** —
  listed here only so item 7 has a named, checkable target when it ships.

## Non-goals

- **Not building any of the implementation surface.** doc_lint support, make-doc routing,
  project-docs indexing, and bootstrap auto-mint are enumerated below as follow-up build scope —
  ticket #273's own acceptance line requires enumeration, not construction, here.
- **Not retrofitting existing ADRs (0001–0013) with `intent-refs:` citations.** Deferred
  (Implementation surface, item 7); this scoping doesn't force a backfill sweep.
- **Not ratifying the product-lifecycle-bible's full three-loop model** (North star / Foundation /
  Releases) repo-wide. This PRD scopes only the IDR record type per #273's explicit ask; the
  DELTA section below maps the bible's PRP concept onto this repo's existing PLAN/ROADMAP/TICKET
  types rather than proposing a new PRP type — no ticket asks for one, and the existing types cover
  that ground.
- **Not resolving the residual cardinality question** in the "Cardinality" section below — flagged
  for Kim's confirmation, not silently picked.
- **Not an ADR.** Per the standing ADR-default-no ruling, no genuine architectural fork is being
  ratified by this scoping alone. If Kim confirms the cardinality reconciliation below and/or
  formally adopts the bible's framework in this repo, *that* decision earns an ADR — named as
  follow-up items 6 and 8, not this PRD's own deliverable class.

## Source of truth

This PRD points at, rather than restates, `.claude/docs/spec/product-lifecycle-bible.md` — Part 2
(the three loops), Part 4 (the IDR/ADR/PRP table), and Part 5 (knowledge-base maturation) are the
sections load-bearing for this design. Per the bible's own Part 3 rule ("specs point at the source
of truth instead of paraphrasing it"), read it directly for the full model; this document only
restates the fragments a type-contract decision turns on.

**Provenance note:** `product-lifecycle-bible.md` was forwarded as a mid-build input by the
coordinator (corroborated by a session charter record, ops-local and untracked:
"SUPERSEDING INPUT forwarded mid-build... bible = concept authority") while still untracked in
this worktree. It has since been committed to `main` directly by Kim
(commit `5044c0c`, "docs: commit the Product Lifecycle Bible spec (IDR/ADR/PRP doctrine, v1.1.0)")
— closing the dangling-citation risk before this PRD lands. No ADR yet formally ratifies its
adoption in this repo; whether one is warranted stays Implementation surface item 6 below, now
narrowed to "ratify," not "commit."

## Delta — what IDR adds over adjacent artifacts

**vs. `make-vision-memo`'s vision memo.** A vision memo "argues how to think about a problem, not
what to build" — a persuasive essay with no admission test, no lock/supersede state machine, and
no ID-spine citation requirement; `doc_lint.py` doesn't govern it at all (it isn't a `doc-type`).
IDR is the opposite shape: one testable hypothesis or outcome claim, admission-tested ("would two
reasonable builds differ on it?"), `draft → locked → superseded-with-reason`, cited upward by ADRs,
and `doc_lint`-enforced. **Delta:** IDR is a falsifiable, gated, cited *claim*; a vision memo is an
ungated *argument*. Not a variant — a different mutability and verification contract entirely.

**vs. ROADMAP/PLAN.** ROADMAP is living state — "Now/Next/Later," reviewed on a cadence, never
locked, describing *sequencing* of what ships. PLAN is living steps with done-when, archived on
completion. Neither preserves *why a prior belief was later judged wrong* — they just move forward.
IDR is the locked claim those sequencing choices are supposed to serve; its supersession chain is
the actual "why we changed our minds" record neither ROADMAP nor PLAN keeps. **Delta:** IDR is the
locked hypothesis ROADMAP/PLAN execute against; ROADMAP/PLAN are the unlocked queue built from
validated IDRs, not a substitute for recording the validation itself.

**vs. an ADR-0001-style founding decision.** An ADR is "one system decision, rejected alternatives
included" — a HOW choice. This repo's actual ADR-0002 ("git-native execution") is exactly that: it
presupposes goals worth pursuing and picks a mechanism. IDR precedes it: a claim like "this
workspace's issue backend should double as the durable memory a cold agent starts from" is a
testable belief about what's true, not yet a choice about how to implement it. Under the bible's
own rule, "an ADR with no IDR citation is an orphan" — a discipline this repo does not currently
have (no existing ADR cites an upstream intent record at all, because none exists). **Delta:** ADR
answers *how we'll act*, given a claim already believed true; IDR answers *what we believe is true
and why*, before any implementation choice. Genuinely new — not a rename of ADR, and not something
PRD/SPEC/LLD cover either (those describe an *approved* solution's shape, not the founding belief
that justified building at all).

**Conclusion:** IDR is not a variant of an existing type. It fills a real gap — none of vision
memo, ROADMAP/PLAN, or ADR carry a falsifiable, lock-gated, upward-cited claim about product/domain
truth.

**Mapping the bible's PRP and product-brief onto existing types.** The bible's **PRP** (Product
Release Plan — "scope · acceptance criteria · sequencing · citations · DRI · completion clause,"
locked at release commitment, shipped-and-archived) maps closely onto this repo's **TICKET**
(`kind: feature`, Findings write-back, `Closes #id`) combined with **PLAN** (steps, done-when,
rollback) — the union already covers PRP's contract; no new PRP type is proposed. The bible's
**roadmap** ("the living index over PRPs; releases lock, the roadmap breathes") is close to a
restatement of this repo's own **ROADMAP** row ("Horizons of intent, reviewed on a cadence") —
effectively the same artifact under two names, no delta to design. The bible's **product brief**
(the living index over IDRs) has **no existing counterpart** in this repo's eight types — the one
genuine gap the mapping surfaces, and it is deliberately out of scope here (see Non-goals and
Cardinality below): ticket #273 asks for one record type, and the aggregation question it would
answer is already reachable by querying `idr-0*` files directly once follow-up item 4 ships.

## Naming — collision test and recommendation

Ticket #273's own Scope/Open section names this as the one gap left unresolved by Kim's batched
rulings: *"does the type collide with harness:find-intent's routing surface, and what does
ADR-0011's naming grammar say about the type name?"* Both tests, run explicitly:

**Collision test against `harness:find-intent`.** find-intent is a per-ask extraction *procedure*,
triggered by imperative phrasing in its own description — "what am I really asking for", "figure
out what they actually want", "clarify this before we build it". ADR-0009 deliberately retired
`find-the-ask` in favor of plain **"intent"** as that skill's memorable head noun. A bare `INTENT`
doc-type (the ticket's own placeholder name) would collide directly with that investment: "let's
write the intent doc" and "let's run find-intent" become indistinguishable from the bare word
alone — **rejected**. **IDR** carries zero lexical overlap with find-intent's trigger phrases at
the form actually used in speech or reference ("file an IDR", "`idr-0001`", "the IDR ledger") — no
router ever matches a noun-reference doc-type token against an imperative trigger phrase in the
first place, since doc types are addressed by id/command (`/make-doc idr`), never by
description-routing the way a skill is. The long form, *Intent Decision Record*, keeps "Intent" as
its first word but paired with "Decision Record" — the same structural pattern as *Architecture
Decision Record* not colliding with any "architecture" skill, because the disambiguating head
noun carries the weight, not the leading word alone. **Verdict: no collision** — IDR is safe to
adopt.

**ADR-0011 grammar test.** `.claude/docs/spec/spec-naming-convention.md` states its own scope in
line 3: *"Applies to: `.claude/` harness artifacts (agents, commands, skills)."* A `doc-type`
frontmatter token is none of those three kinds — it isn't parsed by `VerbLex`/`ProcessLex`/
`ObjectVocab` at all, and isn't a name a router ever description-matches. **The grammar does not
bind this decision** — applying it to `idr` would be a category error, and the ticket's framing
(which asks the scoping to check the type's name "against" it) slightly conflates the artifact
namespace with the docs plugin's own, already-established doc-type namespace (the `TYPES` dict in
`doc_lint.py`, lowercase short tokens: `adr`/`prd`/`spec`/`lld`/`plan`/`roadmap`/`ticket`/`task`).
The actual binding check is that namespace: `idr` is a new lowercase, unhyphenated, three-letter
token — consistent in shape with every existing entry, and directory-mapped
(`.claude/docs/idr/`) the same way. ADR-0011 *does* apply, and should be checked at that time, to
any new **skill or command** the implementation surface below mints (e.g. if `make-doc` gains a
distinct routing token beyond its existing type-dispatch) — flagged there, not required here.

**Recommendation: `IDR` / `Intent Decision Record`.** Rejected alternative considered: `FIR` /
`Founding Intent Record` — avoids "Intent" in the acronym but invents a synonym for a concept this
repo's own doctrine corpus (the bible) already names, which is exactly the "one home per fact/term"
violation the bible warns against (Part 5, Part 6 habit 2, Part 9 glossary). IDR reuses the
existing term-of-art and is strictly better on that axis, not merely equal.

## Type contract

### Frontmatter

```yaml
doc-type: idr
id: idr-0001                # idr-NNNN, sequential like adr-NNNN
status: draft                # draft | locked | superseded
date: YYYY-MM-DD
owner:
proof-ref:                   # path/URL to the test, demo, or prototype state — required at lock
supersedes: null              # idr-NNNN when replacing a prior claim, reason in ## Why
```

### Required sections (`doc_lint.py` T3)

Three sections, directly off the bible's own "Contains" row (Part 4) — deliberately the same count
and shape as ADR's three (`Context`/`Decision`/`Consequences`), so the two types read as a matched
pair:

| Section | Contract |
|---|---|
| `## Claim` | One testable hypothesis or outcome claim, stated so it could fail. |
| `## Why` | The reasoning and evidence behind the claim — context, not proof. |
| `## Proof` | A **reference** (test, demo, prototype path/URL) — never inlined content; same "point at the source, don't restate" discipline the bible names and this repo's ID-spine rule already enforces. |

The bible's admission test ("would two reasonable builds differ on it?") is a **minting-time
question**, not a required section — asked by whoever authors the IDR (`/make-doc idr`, follow-up
item 3), the same way ADR's "a choice someone will later ask why about" gates ADR authoring today
without being its own heading.

### Mutability class & lifecycle

**Reuses the existing Ledger class verbatim** (doc-writing-rules' four-class table), rather than
inventing a fifth. The state mapping is a direct rename of ADR's already-verified two-phase
mechanic (ADR-0013 just live-proved this exact T4 behavior):

| IDR state | ADR-equivalent | T4 behavior |
|---|---|---|
| `draft` | `proposed` | Freely editable — corrections during Explore are the "harvest window" (bible Part 3, stage 2), not forgery. |
| `locked` | `accepted` | Committed-`locked` at HEAD blocks in-place edits — the amendment path is a new IDR citing `supersedes:`, exactly as an accepted ADR is superseded, never edited. |
| `superseded` | `superseded` | Terminal; the file stays, the chain is the record. |

The `draft → locked` flip is the ratification act (mirrors the `proposed → accepted` flip T4
already permits), triggered at whatever this repo calls "Spec lock" for the adopting project — not
prescribed here; a project without a formal Spec-lock stage locks an IDR when the claim is
considered ready to build against.

### File & directory convention

`.claude/docs/idr/idr-0001-<slug>.md` — the canonical type-prefixed numbered-ledger form
doc-writing-rules already specifies for new types (frontmatter `id: idr-0001`, filename carries the
same number). This deliberately diverges from this repo's own `.claude/docs/adr/` directory, whose
files are grandfathered *unprefixed* (`0002-git-native-execution.md`, not `adr-0002-...`) — IDR
adopts the canonical form rather than copying that grandfathered exception. Repo-rooted, never
plugin-rooted, per doc-writing-rules' existing directory rule.

## Cardinality — reconciling "one founding document" with a plural ledger

Kim's ruling #2 (2026-08-16, batched confirm): *"ONE founding document per project (not a numbered
series)."* The bible defines IDR as **plural and numbered**, ADR-parallel — one record per testable
hypothesis, with cardinality identical to ADR's own. Read as literal cardinality constraints on the
same artifact, these two inputs are in real tension.

**This PRD's reconciliation (recommended, not unilaterally decided):**

- IDR is the record type: plural, numbered, ADR-parallel lifecycle — this is the only reading that
  satisfies the ticket's own acceptance text ("ADR-like lifecycle") and body text ("analogous to
  how ADRs are handled," "a project starts with an *initial* INTENT record" — "initial" implying
  more may follow, not that none do).
  Ruling #2's "ONE founding document" is read as describing `idr-0001` **specifically**: the record
  auto-minted once, at project bootstrap (ruling #4 / follow-up item 5), which is *the* founding
  document every ADR's upward citation and every later IDR's `supersedes:` chain ultimately traces
  back to — not a claim that the type itself is forever singular.
- The bible's separate "product brief" living index is out of scope for this ticket's minimal
  contract (see Delta and Non-goals) — deferred rather than built as a second new type alongside
  IDR.

**Residual ambiguity — flagged for Kim, not silently resolved:** if ruling #2 meant literally one
record ever, with no `idr-0002` following, the design above is wrong and an **Alternative B**
applies instead — IDR's three sections embedded inside a single non-recurring project-brief-style
document, sacrificing independent lock/supersede per-claim and the ticket's own "ADR-like
lifecycle" acceptance criterion. The primary design above is recommended because it is the only one
satisfying all four of: the ticket's ADR-like-lifecycle criterion, the ticket's own body text, the
append-only+supersede ruling (#3) applied per-record, and the bible's now-surfaced doctrine — but
it is a judgment call, surfaced here for confirmation rather than picked with no visibility, per
the mid-build instruction's own hedge.

## ID-spine position

IDR sits upstream of ADR (more foundational, not "instead of"): an ADR **may** cite `≥1` IDR via a
new `intent-refs:` frontmatter field (parallel to `supersedes:`); this PRD does not mandate
retrofitting ADRs 0001–0013 (Non-goals, Implementation surface item 7 — deferred). IDR is also
citable from PRD and ROADMAP per ruling #4's "ID-spine links from PRD/ROADMAP/ADRs." Position in
the type contract table: a new row, class `ledger` (second Ledger-class member alongside ADR), no
reordering of the existing seven rows needed.

## Implementation surface (follow-up build scope — enumerated, not built here)

1. **`doc_lint.py`** *(realizes OUT-01)* — add `"idr"` to the `TYPES` dict (status enum
   `draft`/`locked`/`superseded`, sections `Claim`/`Why`/`Proof`); generalize the existing
   `head_is_accepted_adr` guard into a ledger-lock guard covering both `doc-type: adr,
   status: accepted` and `doc-type: idr, status: locked`; add selftest fixtures (positive:
   locked-IDR-edit blocked; negative: draft-IDR-edit allowed; regression: existing ADR fixtures
   unaffected).
2. **`doc-writing-rules` SKILL.md** — add the IDR row to the type contract table and to the
   mutability-classes table (Ledger class, second member); add
   `references/templates/idr.md` mirroring `adr.md`'s structure and inline comments.
3. **`make-doc` routing** — recognize `idr` as a mintable type; generate
   `idr-000N-<slug>.md` under `.claude/docs/idr/`; prompt the admission test ("would two
   reasonable builds differ on it?") before minting, same spirit as ADR's "a choice someone will
   later ask why about" gate.
4. **`project-docs` consult-table row** *(realizes OUT-03)* (or the equivalent consult skill in an
   adopting repo) — add a row: *"A founding hypothesis or testable claim this project is built
   on"* → `.claude/docs/idr/` (`IDR-*`, `locked` = append-only). Not touched by this PRD's own
   branch — `.claude/skills/project-docs/SKILL.md` is real follow-up work, not scoping.
5. **Bootstrap auto-mint** *(realizes OUT-02)* — `/make-plugin` and equivalent project-bootstrap
   commands (harness) gain a step minting `idr-0001` (`status: draft`) as part of scaffolding a new
   plugin/project. Not touched here; harness's `make-plugin` command is out of this PRD's file set.
6. **Provenance closure (partially done)** — `product-lifecycle-bible.md` is committed
   (`5044c0c`); an ADR formally ratifying adoption of its IDR/ADR/PRP framing in this repo remains
   optional, not required before item 1 ships.
7. **Deferred** — retrofit `intent-refs:` citations onto ADRs 0001–0013 and add an "orphan ADR"
   `doc_lint` WARN check (bible: "an ADR with no IDR citation is an orphan"). Not required for the
   type to exist; gives OUT-04 a non-vacuous target once done.
8. **Deferred** — an ADR resolving the Cardinality section's open question, once Kim confirms which
   reading (primary or Alternative B) is intended; only earns an ADR if it ratifies a genuine fork
   from what's already decided (ADR-default-no).

## Open questions for Kim

1. Cardinality: does ruling #2 ("ONE founding document, not a numbered series") mean `idr-0001` is
   the singular founding record with a plural ledger following (this PRD's recommendation), or
   literally one record forever (Alternative B, sections in Non-goals/Cardinality)?
2. `product-lifecycle-bible.md` is now committed (`5044c0c`) — is a dedicated ADR formally
   ratifying its adoption in this repo still wanted, or does the committed spec alone suffice as
   this PRD's cited source of truth (Implementation surface item 6)?
3. Is a "product brief" living-index type (the bible's IDR aggregator) wanted as a near-term
   follow-up, or does querying `idr-0*` directly suffice indefinitely (this PRD assumes the
   latter)?
