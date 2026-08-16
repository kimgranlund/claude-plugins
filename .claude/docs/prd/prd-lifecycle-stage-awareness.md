---
doc-type: prd
id: prd-lifecycle-stage-awareness
status: draft
version: 0.1.0
date: 2026-08-16
owner: kim.granlund
---
# PRD — Lifecycle-stage awareness: detect and surface which loop/stage a project is in

## Problem

No skill in this estate answers "what lifecycle stage is THIS project in right now." The doctrine
exists and is portable (`docs:product-lifecycle-rules` — three nested loops, the seven-stage build
turn, the IDR/ADR/RDD alignment grammar), but every one of that pack's own reference files ends
with the same disclaimer, verbatim in spirit across three separate files:
`three-loops.md` — *"No skill in this estate currently answers 'what stage is THIS project in' as
of 2026-08-16 — a named forward gap, not this pack's job."*; `build-loop-stages.md` — the identical
sentence; the pack's own `SKILL.md` Boundaries section names it explicitly as *"tracked in this
repo as issue #321's territory."* This PRD is that gap's scoping resolution — the pack's own three
forward-fences already point here.

The cost of the gap is concrete, not abstract: a session orienting cold on a repo has no way to
know whether it should be in harvest-mode (pre-Spec-lock — corrections are free, nothing is locked
yet) or bug-vs-requirement-gap discipline (post-lock — a mismatch is either a bug, fixed in place,
or a requirement gap, recorded as a new version) without a human first explaining where the project
stands. `harness:check-state` already answers the adjacent-but-different "what's in flight" axis
(branches, PRs, ticket status) — this PRD scopes the *lifecycle-position* axis check-state
deliberately does not carry (verified directly in this PRD's Fencing section below), per its own
explicit Boundaries exclusion.

## Users

**Primary:** any session (human or agent) orienting cold on a repo and needing to know which
lifecycle discipline currently applies — pre-lock harvest-mode vs post-lock
bug-vs-requirement-gap, which loop (North star/Foundation/Releases) is currently emphasized, and
what the version triple reads. **Secondary:** the standing ops seats that consult doctrine today
without a live reading — `decision-watcher` (ADR review cadence could differ by loop), `chore-planner`
(prioritization could differ pre- vs post-Spec-lock) — named here as future consumers, not as
consumers this PRD builds for (routing-bias is explicitly deferred, resolution (d) below); a human
running `/check-state` who also wants the lifecycle axis alongside the work-state one.

## Outcomes

- **OUT-01** — A skill exists that, given a repo root, reports a lifecycle-stage reading — loop
  emphasis, build-turn stage, and the version triple — sourced from the repo's own typed records,
  and the reading is a real, non-"unknown" answer when run against THIS workspace at the time the
  follow-up build ships (verifiable: running it here reports concrete counts, not a placeholder).
- **OUT-02** — Every signal the report cites is labeled mechanized (script-derived, from a typed
  record census) or judgment (narrated with the signals that informed the call) — never presented
  as a flat verdict with no visible evididence class. Verifiable: a fresh reader can tell, line by
  line, which parts to trust as fact and which are a call.
- **OUT-03** — The new skill's own Boundaries section and `harness:check-state`'s description both
  name each other explicitly, and neither collector re-derives data the other already collects
  (verified today, this PRD's Fencing section: `check-state`'s `doc_state.py` collector structurally
  excludes the `adr/` directory and never matches `adr`/`idr`/`rdd` filenames — zero overlap exists
  to fence against retroactively; this PRD's job is to keep it that way going forward).
- **OUT-04** — The three dangling forward-fences named in Problem (`three-loops.md`,
  `build-loop-stages.md`, `product-lifecycle-rules/SKILL.md`) are updated, in the same PR that ships
  the follow-up build, to point at the new skill by name instead of naming issue #321 — closing the
  loop those fences opened, per this workspace's stale-context-is-a-defect invariant.

## Non-goals

- **Not building the skill, script, or any doc edit named in Implementation surface below.** Per
  the ticket's own acceptance line ("a scoping PRD... resolving the four named gaps... with a named
  implementation surface"), this PRD scopes and enumerates; the follow-up ticket builds — same
  precedent `prd-idr-framework.md` → #316 and `prd-rdd-framework.md` → #332 already set.
- **Not proposing any routing-biasing tier as part of v1.** Resolution (d) below names one as a
  distinct future phase, gated behind its own PRD/ADR — never smuggled in as an implementation
  detail of the report-only build this PRD scopes.
- **Not resolving whether #332 (RDD implementation) must land first.** Resolution (c) below states
  the dependency is soft, with reasoning — not a blocking gate on the follow-up build starting.
- **Not designing the ambient-convention half of shape resolution (a).** Named as its own
  deferred follow-up (Implementation surface item 7) — a second scoping question (which grounding
  doc or manifest field, and its staleness-repair discipline) this PRD does not answer.
- **Not an ADR.** Per the standing ADR-default-no ruling: this PRD scopes a new skill using an
  already-ratified pattern (a read-only collector-and-report skill, the same shape `check-state`
  and `decision-watcher` already use) — no genuine architectural fork is ratified by this scoping
  alone. If a routing-biasing tier is later built (Non-goals above, resolution (d)), *that* decision
  earns its own ADR, not this one.

## Source of truth

This PRD points at, rather than restates, three files in `docs:product-lifecycle-rules`:
`references/three-loops.md` (the three nested loops, the version triple, the POC boundary),
`references/build-loop-stages.md` (the seven build-turn stages, Spec lock as the only hard gate),
and `references/alignment-record-types.md` (the IDR/ADR/RDD table, admission tests, states,
escalation-rides-the-citations) — read them directly for the full model; this document only
restates the fragments a shape/mechanizability/dependency/routing decision turns on. It also points
at `docs/scripts/doc_lint.py` (the live `TYPES`/`LEDGER_LOCK` dicts — the actual typed-record
contract any census script must parse against) and `harness/skills/check-state/` (the sibling
collector-and-report skill this PRD's proposed skill is modeled on and fenced against). This PRD
follows the same scoping-first shape as `prd-idr-framework.md` (#273) and `prd-rdd-framework.md`
(#318) — the two prior PRDs in this same lineage, cited throughout below.

## (a) Shape — on-demand skill and ambient convention, phased; v1 is on-demand only

**Resolution: both are eventually wanted, but v1 ships only the on-demand assessment skill —
the ambient convention is a named later phase, not bundled in.**

The on-demand skill (modeled directly on `check-state`'s own procedure: bundled collectors →
cross-reference → verdict-first report, mutating nothing but its own checkpoint) is the correct v1
shape because it is **read-only** — the same property that makes `check-state` safe to run
speculatively and often. An ambient convention (a lifecycle line in a grounding doc, or a manifest
field) is a **write surface**: the moment a project's stage changes and nothing re-derives that
line, it goes stale — precisely the class of defect this workspace's own CLAUDE.md names as
"equal in severity to a bug" ("a change that invalidates a record... repairs that record in the
same change"). A written lifecycle line has no natural trigger forcing that repair; an on-demand
skill has no staleness risk at all, because it recomputes from source every time it runs. Shipping
the write surface first would create the exact defect class this workspace's own doctrine already
flags — so v1 proves the read-only value, and the ambient convention (if it's still wanted once
that value is demonstrated) is deferred to its own follow-up scoping (Implementation surface item
7, Open question 3).

## (b) Mechanizability — a concrete split, with THIS workspace's own numbers as the worked example

Splitting stage signals into script-detectable (a `make-script` candidate — a typed-record census)
vs judgment requires naming both lists concretely, not in the abstract:

**Script-detectable (the census, checked directly against `docs/scripts/doc_lint.py`'s live
`TYPES`/`LEDGER_LOCK` dicts, not invented):**

- Presence and count of `.claude/docs/{adr,idr,rdd}/*.md`. **This workspace's own numbers, read
  while drafting this PRD:** 13 files under `.claude/docs/adr/`, zero under `.claude/docs/idr/`
  (the directory does not exist — IDR is lintable per #330 but no `idr-0001` has ever been minted
  here), zero under `.claude/docs/rdd/` (the type doesn't exist yet — `rdd` is absent from
  `TYPES`, see resolution (c) below).
- Status distribution per type, against each type's own enum (ADR: `proposed`/`accepted`/
  `superseded`; IDR/RDD: `draft`/`locked`/`superseded`) — a locked-vs-draft ratio per type.
- ROADMAP presence/absence and its own `active`/`retired` status, once minted (`roadmap` is
  already a `TYPES` entry; **this workspace has no ROADMAP.md at its root today** — another
  concrete zero-signal reading, checked directly).
- Orphan-ADR density — `doc_lint.py`'s own T6 WARN (`intent-refs:` empty/missing) is already a
  live, script-emitted signal; a high orphan count is itself a stage tell (heavy pre-IDR-discipline
  activity, or an early Foundation loop that predates IDR's own existence in this repo — both true
  here: all 13 existing ADRs predate IDR, per `prd-idr-framework.md`'s own Non-goals).
- A derived version-triple candidate (outer≈IDR-cycle count, inner≈ADR count, innermost≈RDD/release
  count) — explicitly flagged as **derived**, not a literal read, since no file states "thesis 2"
  anywhere.

**Judgment-tier (never scripted — narrated with the signals that informed the call, per OUT-02):**

- "Is the POC boundary crossed" — the bible's own definition ("a fairly complete proof of concept
  that functionally proves the core hypotheses") is a qualitative sufficiency call; the skill
  states the inputs (POC presence, locked-IDR count, does a Foundation-grade test/CI backbone
  exist) and narrates the call — never emits a bare boolean.
- "Which of the three loops is currently emphasized" — `three-loops.md`'s own concurrency doctrine
  ("all three run at once... differ in emphasis, never exclusivity") makes this inherently a
  weighted read across signals, not a single flag one script can resolve alone.
- "Is this a bug or a requirement gap" (the Verify-stage discipline `build-loop-stages.md` names) —
  explicitly project- and context-loaded per instance; never a generalizable script rule.
- Whether a Retro's lessons actually landed in the knowledge base — no typed record type exists yet
  to check this against; named here as a real gap this PRD does not propose closing.

## (c) Dependency on #332 (RDD implementation) — soft, with reasoning

**Resolution: soft.** Checked directly against `docs/scripts/doc_lint.py`'s live `TYPES` dict
(lines 34–44, read while drafting this PRD): `idr` is **already present** (#330, merged) — the
North-star-loop signal (IDR presence, locked/draft ratio) is typed-record-driven **today**, with
zero dependency on #332. `rdd` is **absent** — the Releases-loop signal is not yet typed-record-
driven; until #332 lands, the follow-up build's Releases-loop reading falls back to judgment-tier
signals already available without RDD (ROADMAP presence, ticket status counts via
`check-state`'s own `ticket_state.py`, release cadence) rather than blocking outright. Concretely:
**the follow-up build can start and ship a real, non-degenerate report the moment it's built** —
#332 is not a hard blocker on that build starting or landing. #332 landing measurably *improves*
the Releases-loop signal's precision (a mechanized locked/draft RDD ratio, instead of a judgment
fallback) but does not gate the follow-up ticket's own existence. The follow-up ticket's own Links
section should carry this as a soft "related, sequencing-note" pointer to #332 — the same house
convention `prd-rdd-framework.md` used for its own #316 relationship, and exactly the pattern
ticket #321's own Links section already used for #316/#318 ("detection quality rises sharply once
these exist... builder's call whether hard or soft" — this PRD is that builder's call, decided
soft).

## (d) Report-only vs routing-biasing — report-only v1; biasing is a named, gated future phase

**Resolution: report-only for v1**, per this estate's disclose-not-enforce precedent —
`check-state`'s own output contract states it directly ("Findings are proposals — acting on any of
them is a separate, user-initiated step") and `mobilize-chores`' batched-confirm gate is the same
doctrine applied to execution. The new skill's report states the lifecycle reading and the
signals behind it; it does not surface stage-appropriate skills, alter routing, or bias any other
skill's behavior.

**A future routing-biasing phase is explicitly named, not silently foreclosed**, because the
ticket's own gap (d) asks for it to be named rather than ruled out: a later phase could, for
example, surface a note when a session is doing Build-stage work pre-Spec-lock ("harvest-mode
still applies — nothing is locked yet"). That phase is **out of this scoping's authority to
approve** — it needs its own PRD (to design what "biasing" concretely means and its blast radius)
and, given it would be the first routing-biasing instrument standing in this estate, plausibly its
own ADR, ratified the same deliberate way ADR-0012 gates quick-build auto-merge behind an explicit,
non-inferred grant line rather than a default. This PRD's Implementation surface (below) lists it
as a deferred item with no build authorized.

## Fencing against `harness:check-state` — checked both directions, not merely asserted

**From check-state's side (verified directly in its bundled collector, `doc_state.py`):**
`find_docs()`'s `skip_parts` set is `{".refactor-attic", "node_modules", "templates", "adr"}` — the
`adr` directory is **structurally excluded**, with the collector's own comment stating why:
*"ADRs are decision-watcher's territory."* Its `DOC_NAME` regex matches only
`roadmap|plan|backlog|ticket|tkt-\d+` — never `adr`, `idr`, or `rdd` filenames, at all. **Check-state
carries zero ledger-type signal today.** There is no overlap to fence retroactively — the proposed
skill would be the first and only reader of `.claude/docs/{adr,idr,rdd}/*.md` typed-record census
data in this estate, a genuinely disjoint input from check-state's own git/ticket/ROADMAP-shaped
collectors.

**From the new skill's side (a design commitment, not yet built):** its own Boundaries section
must state explicitly *"NOT work-state — branches, worktrees, stashes, blocked-on-you,
ready-to-close (`check-state`)"*, and its report should, where a signal already exists in
check-state's own JSON (e.g. release cadence / PR velocity, useful for the Releases-loop turn-
cadence read), **consume that JSON as an input rather than re-implementing `git_state.py`** —
sources-flow-outward, applied to a sibling skill's own collector output rather than only to
canonical doctrine files. `check-state`'s own description already reserves "work-state axis"
language in its routing surface; the new skill's name and description must not collide with it —
flagged as a `/check-routing` obligation for the follow-up ticket (Implementation surface item 5).

## Implementation surface (follow-up build scope — enumerated, not built here)

1. **New skill** (working name `lifecycle-state`, final name subject to Open question 2) —
   plugin home recommended `harness`, as a direct sibling of `check-state` (same collector →
   cross-reference → report architecture, same read-only contract); flagged for confirmation
   against `plan-plugin-split`'s anti-matrix before minting, per Open question 1 — not silently
   assumed.
2. **Bundled census script** (a `make-script` candidate, e.g. `lifecycle_census.py`) — walks
   `.claude/docs/{adr,idr,rdd}/*.md`, parses `doc_lint`-compatible frontmatter, emits per-type
   counts, status distributions, and the orphan-ADR (T6) count; reuses `doc_lint.py`'s own
   `TYPES`/`LEDGER_LOCK` contract rather than re-declaring it, per sources-flow-outward; carries a
   `selftest` per `.claude/rules/scripts.md`.
3. **Judgment-narration procedure** inside the new skill's own body — the four judgment-tier
   questions named in resolution (b), each always narrated with the signals that informed the
   call, per OUT-02; never emitted as a bare boolean.
4. **Three forward-fence updates**, owed by the SAME PR that ships the skill (per OUT-04, and per
   this workspace's stale-context-is-a-defect invariant): `docs:product-lifecycle-rules`'s
   `references/three-loops.md` and `references/build-loop-stages.md` (each currently states "no
   skill in this estate currently answers this... as of 2026-08-16"), and the pack's own
   `SKILL.md` Boundaries bullet ("tracked in this repo as issue #321's territory") — all three
   repointed at the new skill by name.
5. **`check-state`'s own description** gains a one-line disambiguation naming the new skill as
   the sibling that owns the lifecycle-position axis (mirrors this PRD's own Fencing section);
   run `/check-routing` after, per `.claude/rules/plugin-authoring.md`.
6. **`evals/evals.json`** for the new skill, per `skill-writing-rules`.
7. **Deferred** — the ambient-convention half of resolution (a): which grounding doc or manifest
   field carries the lifecycle line, and its staleness-repair discipline. A second, smaller
   scoping question of its own; not resolved or authorized here (Open question 3).
8. **Deferred** — the routing-biasing tier named in resolution (d). Needs its own PRD, and
   plausibly its own ADR, before any build ticket is minted for it. No build authorized here.
9. **Plugin version bump** — owed by whichever plugin (`harness` and/or `docs`) the follow-up
   build actually touches; **not owed by this PRD's own PR** (verified below — this PR touches no
   plugin-rooted file, mirroring `prd-idr-framework.md`/PR #304's and `prd-rdd-framework.md`/PR
   #331's own verified-clean precedent).

## Gate output

```
$ python3 docs/scripts/doc_lint.py .claude/docs/prd/prd-lifecycle-stage-awareness.md
doc_lint · clean · .claude/docs/prd/prd-lifecycle-stage-awareness.md
```

No plugin content touched — the PRD is a workspace doc under `.claude/docs/prd/`, outside every
plugin's own directory, verified via `git diff --stat` against `origin/main` (single new file); no
plugin version bump or README ledger entry needed, same precedent `prd-idr-framework.md` and
`prd-rdd-framework.md` already set.

## Open questions for Kim

1. **Plugin home** for the new skill: `harness` (this PRD's recommendation, as `check-state`'s
   direct sibling) vs `docs` (as `product-lifecycle-rules`'s sibling, since it consults that
   pack's doctrine) vs a new home — flagged for confirmation against `plan-plugin-split`'s
   anti-matrix rather than silently assumed.
2. **Skill name** — `lifecycle-state` (this PRD's working name) vs `project-stage` vs another,
   checked against `naming-audit`/`/check-routing` before minting (never reusing bare "state," to
   avoid collision with `check-state`'s own routing surface).
3. **Timing of the ambient-convention half of resolution (a)** — wanted as a near-term follow-up
   alongside v1's on-demand skill, or deferred until the on-demand skill's read-only value is
   proven first? This PRD assumes the latter (prove read-only value before adding any write
   surface) — flagged for confirmation, not silently picked.
