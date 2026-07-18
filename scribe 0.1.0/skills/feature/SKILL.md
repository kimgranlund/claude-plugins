---
name: feature
description: >-
  Capture a feature idea — however vague — as a durable, scope-appropriate record BEFORE any
  building starts: a `kind: feature` record, the design docs the change earns (PRD/SPEC/LLD via
  doc-forge, never the bundle), or a reference corpus when the "feature" is really knowledge to
  encode. Use when the user proposes a new capability, pitches an idea, or asks "can we add X" —
  "can we add a dark mode", "what if we supported CSV export". Pure intake: sizes and records,
  never builds. Runs intent-extract (one round max), a
  dedup sweep, and system-decompose, then records by shape — the TICKET file by default, or the
  workspace's ruled backend (git-native, or a named external adapter). Also runs via /feature [raw
  idea, or a TKT-/#issue/adapter id]. Writes one record set, then stops — building is /build's
  job. NOT for bug-shaped
  reports (bug-report); NOT for generic chores/follow-ups/tasks needing no sizing (issue); NOT
  for dispatching or performing the build (/build); NOT for other document types (doc-forge).
disable-model-invocation: false
user-invocable: true
argument-hint: "[raw feature idea, or a TKT-/#issue/adapter-native id to resume]"
---

# feature — intake that ends in a record, never a build

Turns a raw feature idea into the smallest durable record that fully carries it, before anyone
spends build effort — the same loss-window fix `bug-report` made for bugs: an idea that lives
only in chat context vanishes with it. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run):** call doc-authoring-standards' backend resolver
(`references/backend-resolver.md`) once; it returns Option A (local — the file backend, doc-forge's
TICKET path), Option B (git-native — `gh issue`, an ADR-0002-style ruling), or Option C (external —
a named adapter; Linear's realization: `references/linear-adapter.md`, a bring-your-own adapter
documents its own). No ruling, or the ruled option's adapter is unreachable → Option A, exactly as
always. Every phase below follows whichever option the resolver returned: "ticket file" reads as
"GitHub Issue" under Option B, or as the named external adapter's own record under Option C — same
payload contract, same ordering, different store. Canonical statement: `bug-report`'s SKILL.md —
this is the same seam, not a second one.

## Phase 1 — Route: fresh idea, or resume by record state

`$ARGUMENTS` contains a record id — `tkt-####`/`TKT-####` (case-insensitive) resolving to a file
in `docs/tickets/`, on the git-native backend `#NN`/a bare issue number resolving via
`gh issue view`, or under Option C an id in the resolved adapter's own native format (Linear:
`TEAM-123`) resolving via that adapter's `read` operation (`references/linear-adapter.md`,
REQ-010) — → resume by that record's state: `done`/`wontfix`/closed → report and stop
(reopening is the user's call); open with new detail following the id → fold it into
Summary/Scope and re-run Phase 4's sizing only if the new detail changes the size class;
otherwise (open, no new detail) → report the record's state, size, and placement, point at
`/build` for momentum, and stop. An id that does not resolve (no such file; `gh issue view`
errors; Option C's `read` returns not-found, AC-010) is a fresh idea — say so, never proceed as if
a record existed.

## Phase 2 — Extract

Invoke intent-extract (forge, where installed; apply its discipline inline otherwise): root goal
vs literal ask, the delta taxonomy, ONE batched clarifying round maximum — and only when a human
is actually present to answer (a sibling redirect, a subagent dispatch, or a scheduled/unattended
firing has no one to ask — skip straight to capture-with-gaps). A still-vague idea after that
round, or no round at all, is captured anyway — the named gaps go into the record's Scope/Open
section; vagueness is a note, never a blocker to persistence.

## Phase 3 — Dedup: it may already exist

Before minting anything, sweep three surfaces and report what's found:
1. **Records** — `docs/tickets/`, ROADMAP/PLAN entries, on the git-native backend the open issues
   (`gh issue list --search`), or under Option C the resolved adapter's own `dedup-search`
   operation (`references/backend-resolver.md` REQ-005): already queued → this is a resume (Phase
   1 semantics); update placement or detail, don't re-mint.
2. **The codebase** — Grep the feature's nouns/verbs: already shipped → report where it lives and
   stop; partially shipped → the record captures the delta, not the whole.
3. **Docs/corpora** — an existing PRD/SPEC already covering it → link, don't duplicate (the ID
   spine joins records; a second doc answering the same question is type sprawl).

## Phase 4 — Size and shape

Invoke system-decompose (forge, where installed; its two-plane lens inline otherwise) and decide
TWO things:

**Size** (the materiality floor, same law as orchestration's seats): **small** = one context can
hold it, no contract change · **big** = multi-component, contract-changing, or
decision-ratifying.

**Shape** — what kind of thing is this "feature" really?
- **Work** (something to build) → a TICKET always; big work additionally earns only the docs the
  change earns via doc-forge — PRD (why/what) / SPEC (behavior) / LLD (how) — never the bundle by
  default, and ADR only for a ratified fork (the standing ADR-default-no ruling).
- **Knowledge** (the ask is really reference material, standards, or a world model to encode) →
  AUTHOR it at intake via reference-forge (one document) or knowledge-forge (a corpus), scribe's
  own seats — encoding knowledge IS the record, so "never builds" is intact (that clause bars
  SOFTWARE builds, /build's territory); the TICKET records the routing, links the authored
  result, and closes.
- **Defect** (this "feature" is actually a bug) or **generic chore** (nothing to size or shape) →
  neither Work nor Knowledge; redirect instead (Failure branches) rather than forcing a size/shape
  decision onto something that isn't one.

## Phase 5 — Record, lint, place

The payload contract, identical regardless of backend: Summary · Acceptance (from the extraction's
success criterion) · Links (the ID spine to any PRD/SPEC/LLD/corpus minted in Phase 4) ·
Scope/Open (the named gaps) · the size class · an empty `## Findings` section for the eventual
build's write-back.

- **Option A (local/file backend):** mint the `kind: feature` TICKET via doc-forge's TICKET path
  (`docs/tickets/` of the local or target repo — repo-rooted per doc-authoring-standards'
  location-and-naming rule, never written under a plugin's own installed directory — frontmatter
  `doc-type: ticket, kind: feature`, `size: small | big` in FRONTMATTER, machine-read — /build
  branches on it). Run `doc_lint.py` — fix until clean; an unlintable record is not a captured one.
- **Option B (git-native):** `gh issue create` — title = the Summary line; body = the sections
  above as `##` headings; labels `feature` + `size:small`/`size:big` (the machine-read size lives
  in the label). The section contract is this skill's own gate here (doc_lint validates files, not
  issues): an issue missing a required section is not a captured record.
- **Option C (external, e.g. Linear):** the resolved adapter's `create` operation
  (`doc-authoring-standards` references/linear-adapter.md for Linear; a bring-your-own adapter
  documents its own) — the same payload contract mapped onto that backend's native fields, `size`
  carried as a label. A create call that fails partway falls back to the file backend for this
  operation and reports the fallback in the close-out; never leave the idea uncaptured because the
  preferred store was unreachable.

`.github/ISSUE_TEMPLATE/feature.yml` mirrors this contract for a human filing directly on GitHub.

Place it: add the line to ROADMAP (Now/Next/Later) or PLAN **only where those docs already
exist** — never mint living-state docs unprompted (both backends; queue docs stay files).

## Phase 6 — Bootstrap the project index (opt-in, when absent)

The record is durable but not yet DISCOVERABLE: a fresh session finds `docs/` only if told. When
`.claude/skills/project-docs/SKILL.md` is absent from the project AND a human is actually present
to answer (never on a sibling redirect, a subagent dispatch, or a scheduled/unattended firing —
skip straight to the pointer line below on any of those), offer — once, via ONE
AskUserQuestion — to install the project-docs index skill from this skill's
`assets/project-docs-skill-template.md` (fill `{{PROJECT_NAME}}` from the repo directory name,
or the project manifest's name field where one exists), so doc-shaped asks ("what are the
requirements for X", "which tickets are open") route to the corpus in every future session.
Options: install (recommended) · not now. Installing writes exactly one file and reports the
path. Declined → one pointer line in the close-out report ("index skill not installed — a later
/feature run can add it; a scattered existing corpus is /docs-alignment's job"), no re-ask this session, no marker files — which is why the option is
"not now", never "never": with no durable record of a refusal, a standing no cannot be honored,
so it is not offered. This step is opt-in by design: writing into `.claude/skills/` changes the
project's routing surface, and that earns a knowing yes whenever a human is actually present to
give one. The skill already present → skip silently.

## Failure branches

- Idea too vague after one round → capture with gaps named (Phase 2); never stall persistence.
- Dedup finds it shipped → report location, stop; found queued → resume, not re-mint.
- `doc_lint.py` fails → fix and re-run (file backend).
- On the FIRST classification only, the ask is actually bug-shaped ("X is broken") → invoke
  `bug-report` directly via the Skill tool, carrying the seed; report which sibling was invoked
  and why. Don't force a feature ticket onto a defect. One hop only (the siblings' shared
  redirect rule, `issue`'s SKILL.md); feature ends there — Phases 5–6 never run for a redirected
  seed.
- Same, first classification only, for a generic chore/follow-up with nothing to size or shape →
  invoke `issue` via the Skill tool, same one-hop rule and stop.
- A seed arrives HERE already redirected from a sibling → captured regardless of fit: `kind:
  feature` with the mismatch named in Scope/Open, per this skill's own named fallback in the
  shared rule (Phase 2's capture-anyway rule already covers the mechanics). This skill's own
  redirect (above) never fires on a seed it did not originate the classification for.
- Index bootstrap declined → the pointer line, nothing else this session.
- Workspace rules git-native but `gh` fails partway through a run → fall back to the file backend for THIS
  record, say so, and note the migration in the record — never leave the idea uncaptured because
  the preferred store was unreachable (bug-report's rule, shared).
- Workspace rules Option C but the adapter operation fails partway (auth, API error, MCP
  disconnect) → same fallback discipline, to the file backend for that operation, noted in the
  record.

Done when a `kind: feature` record exists — a lint-clean file on disk, a labeled GitHub Issue (its
URL reported), or an Option-C adapter's record (its native id reported) — sized and shaped
correctly, linked into whatever queue docs exist, with
every extraction gap named, the index offer's disposition reported (installed path, pointer line,
or already-present skip) — and NO build was dispatched BY THIS SKILL (that is `/build`'s
contract, orchestration plugin, where installed) — OR the seed was redirected to
`bug-report`/`issue` under the one-hop rule (first classification only) and the sibling
invocation was reported; no feature record is owed on a redirected seed, and a sibling reached by
redirect runs its own contract, including its own build/no-build rule and its own investigation
dispatch where that applies.
