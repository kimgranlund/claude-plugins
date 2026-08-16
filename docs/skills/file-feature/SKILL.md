---
name: file-feature
description: >-
  Capture a feature idea as a durable record: a ticket, design docs, or a reference corpus when
  it's really knowledge to encode. Use when the user proposes a new capability or pitches an
  idea — "can we add a dark mode", "what if we supported CSV export". Intake only, never builds.
  /file-feature [idea, or a TKT-/#issue/adapter id] resumes. NOT for bugs (file-bug); NOT for
  chores (file-task); NOT for authoring docs (make-doc).
disable-model-invocation: false
user-invocable: true
context: fork
argument-hint: "[raw feature idea, or a TKT-/#issue/adapter-native id to resume]"
---

# feature — intake that ends in a record, never a build

Turns a raw feature idea into the smallest durable record that fully carries it, before anyone
spends build effort — the same loss-window fix `file-bug` made for bugs: an idea that lives
only in chat context vanishes with it. Runs as a background fork (`context: fork`) by default: the
fork sees no conversation history — `$ARGUMENTS` is the only channel in. Seed: `$ARGUMENTS`.

**Backend seam (Phase 0, decided once per run):** call doc-writing-rules' backend resolver
(`references/backend-resolver.md`) once and follow whichever option it returns for every phase
below — canonical definition of the three options, the ruling shape, and the failure fallback
lives there, not restated here.

## Phase 1 — Route: fresh idea, or resume by record state

`$ARGUMENTS` contains a record id — `tkt-####`/`TKT-####` (case-insensitive) resolving to a file
in `docs/tickets/`, on the git-native backend `#NN`/a bare issue number resolving via
`gh issue view`, or under Option C an id in the resolved adapter's own native format (Linear:
`TEAM-123`) resolving via that adapter's `read` operation (`references/linear-adapter.md`,
REQ-010) — → resume by that record's state: `done`/`wontfix`/closed → report and stop
(reopening is the user's call); open with new detail following the id → fold it into
Summary/Scope and re-run Phase 4's sizing only if the new detail changes the size class;
otherwise (open, no new detail) → report the record's state, size, and placement, point at
`/build-feature` for momentum, and stop. An id that does not resolve (no such file; `gh issue view`
errors; Option C's `read` returns not-found, AC-010) is a fresh idea — say so, never proceed as if
a record existed.

## Phase 2 — Extract

Invoke find-intent (harness, where installed; apply its discipline inline otherwise): root goal
vs literal ask, the delta taxonomy, ONE batched clarifying round maximum — asked via
`AskUserQuestion`. A live user is the default assumption — running forked (`context: fork`) does
not change it: forking relieves the caller's session, it does not remove the person. Skip straight
to capture-with-gaps only when the seed carries `[redirected-from:X]` (the round budget was
already spent upstream) or `[unattended]` (no live user backs the run at all) — the shared marker
protocol, canonical statement `file-task`'s Phase 2. A seed that references context the fork
cannot see ("the idea we discussed", "what I just described") is itself a gap, not a reason to
guess: ask for the actual idea via the same round — `$ARGUMENTS` carries no conversation history.
A still-vague idea after that round, or no round at all, is captured anyway — the named gaps go
into the record's Scope/Open section; vagueness is a note, never a blocker to persistence.

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

Invoke break-down-problem (harness, where installed; its two-plane lens inline otherwise) and decide
TWO things:

**Size** (the materiality floor, same law as teamwork's seats): **small** = one context can
hold it, no contract change · **big** = multi-component, contract-changing, or
decision-ratifying.

**Shape** — what kind of thing is this "feature" really?
- **Work** (something to build) → a TICKET always; big work additionally earns only the docs the
  change earns via make-doc — PRD (why/what) / SPEC (behavior) / LLD (how) — never the bundle by
  default, and ADR only for a ratified fork (the standing ADR-default-no ruling).
- **Knowledge** (the ask is really reference material, standards, or a world model to encode) →
  AUTHOR it at intake via make-reference (one document, docs' own seat) or harness's `make-pack`
  (a corpus, where installed) — encoding knowledge IS the record, so "never builds" is intact (that
  clause bars SOFTWARE builds, /build-feature's territory); the TICKET records the routing, links the
  authored result, and closes.
- **Defect** (this "feature" is actually a bug) or **generic chore** (nothing to size or shape) →
  neither Work nor Knowledge; redirect instead (Failure branches) rather than forcing a size/shape
  decision onto something that isn't one.

## Phase 5 — Record, lint, place

The payload contract, identical regardless of backend: Summary · Acceptance (from the extraction's
success criterion) · Links (the ID spine to any PRD/SPEC/LLD/corpus minted in Phase 4) ·
Scope/Open (the named gaps) · the size class · an empty `## Findings` section for the eventual
build's write-back.

- **Option A (local/file backend):** mint the `kind: feature` TICKET via make-doc's TICKET path
  (`docs/tickets/` of the local or target repo — repo-rooted per doc-writing-rules'
  location-and-naming rule, never written under a plugin's own installed directory — frontmatter
  `doc-type: ticket, kind: feature`, `size: small | big` in FRONTMATTER, machine-read — /build-feature
  branches on it). Run `doc_lint.py` — fix until clean; an unlintable record is not a captured one.
- **Option B (git-native):** `gh issue create` (no `--type`) — title = the Summary line; body =
  the sections above as `##` headings; labels `feature` + `size:small`/`size:big` (the
  machine-read size lives in the label). Once created, a second call — `gh issue edit <id> --type
  Feature` (ADR-0004) — attempts the native Issue Type; if it fails (the org's type schema doesn't
  resolve, or `gh` doesn't recognize `--type`), the issue already exists with the label alone,
  note the skipped type in the close-out — never retry the create itself over a type failure (two
  separate calls, never combined: a combined `gh issue create --type` was found to create the
  issue and only then fail the type step, so treating that error as "nothing created" would mint
  a duplicate). The section contract is this skill's own gate here (doc_lint validates files, not
  issues): an issue missing a required section is not a captured record.
- **Option C (external, e.g. Linear):** the resolved adapter's `create` operation
  (`doc-writing-rules` references/linear-adapter.md for Linear; a bring-your-own adapter
  documents its own) — the same payload contract mapped onto that backend's native fields, `size`
  carried as a label. A create call that fails partway falls back to the file backend for this
  operation and reports the fallback in the close-out; never leave the idea uncaptured because the
  preferred store was unreachable.

`.github/ISSUE_TEMPLATE/feature.yml` mirrors this contract for a human filing directly on GitHub.

Place it: add the line to ROADMAP (Now/Next/Later) or PLAN **only where those docs already
exist** — never mint living-state docs unprompted (both backends; queue docs stay files).

## Phase 6 — Bootstrap the project index (opt-in, when absent)

The record is durable but not yet DISCOVERABLE: a fresh session finds `docs/` only if told.
Direct entry only — the seed carries no `[redirected-from:X]` and no `[nested-intake]`
(`dispatch-ticket`'s marker — teamwork, renamed from `dispatch-feature` per ADR-0010 — when it
runs this skill's intake as part of `/build-feature`'s
pipeline): a nested run already owes `dispatch-ticket`'s own ambiguity question and this skill's
own Phase 2 round, and a third `AskUserQuestion` from one background run is one too many — skip
straight to the pointer line below on either marker. When `.claude/skills/project-docs/SKILL.md`
is absent from the project AND a live user backs the run (file-bug's Phase 2 test, shared) AND
entry is direct, offer — once, via ONE AskUserQuestion — to install the project-docs index skill
from this skill's
`assets/project-docs-skill-template.md` (fill `{{PROJECT_NAME}}` from the repo directory name,
or the project manifest's name field where one exists), so doc-shaped asks ("what are the
requirements for X", "which tickets are open") route to the corpus in every future session.
Options: install (recommended) · not now. Installing writes exactly one file and reports the
path. Declined → one pointer line in the close-out report ("index skill not installed — a later
/file-feature run can add it; a scattered existing corpus is /tidy-docs's job"), no re-ask this session, no marker files — which is why the option is
"not now", never "never": with no durable record of a refusal, a standing no cannot be honored,
so it is not offered. This step is opt-in by design: writing into `.claude/skills/` changes the
project's routing surface, and that earns a knowing yes from the live user backing the run. The
skill already present → skip silently.

## Failure branches

- Idea too vague after one round → capture with gaps named (Phase 2); never stall persistence.
- Dedup finds it shipped → report location, stop; found queued → resume, not re-mint.
- `doc_lint.py` fails → fix and re-run (file backend).
- On the FIRST classification only (the seed carries no `[redirected-from:X]` marker yet), the ask
  is actually bug-shaped ("X is broken") → invoke `file-bug` directly via the Skill tool, carrying
  the seed prefixed `[redirected-from:file-feature]`; report which sibling was invoked and why.
  Don't force a feature ticket onto a defect. One hop only (the siblings' shared redirect rule,
  `file-task`'s SKILL.md); file-feature ends there — Phases 5–6 never run for a redirected seed.
- Same, first classification only, for a generic chore/follow-up with nothing to size or shape →
  invoke `file-task` via the Skill tool, seed prefixed `[redirected-from:file-feature]`, same
  one-hop rule and stop.
- A seed already carrying a `[redirected-from:X]` marker (naming a DIFFERENT sibling) → captured
  regardless of fit: `kind: feature` with the mismatch named in Scope/Open, per this skill's own
  named fallback in the shared rule (Phase 2's capture-anyway rule already covers the mechanics).
  This skill's own redirect (above) never fires on a seed that already carries the marker — one
  hop only, detected from the seed itself, not from history the fork doesn't have.
- Index bootstrap declined → the pointer line, nothing else this session.
- Workspace rules git-native but `gh` fails partway through a run → fall back to the file backend for THIS
  record, say so, and note the migration in the record — never leave the idea uncaptured because
  the preferred store was unreachable (file-bug's rule, shared). A failed `gh issue edit --type`
  (Phase 5) is not this failure — the record already exists by the time that call runs; it never
  triggers the file-backend fallback, only the skipped-type note.
- Workspace rules Option C but the adapter operation fails partway (auth, API error, MCP
  disconnect) → same fallback discipline, to the file backend for that operation, noted in the
  record.

Done when a `kind: feature` record exists — a lint-clean file on disk, a labeled GitHub Issue (its
URL reported), or an Option-C adapter's record (its native id reported) — sized and shaped
correctly, linked into whatever queue docs exist, with
every extraction gap named, the index offer's disposition reported (installed path, pointer line,
already-present skip, or skipped-nested) — and NO build was dispatched BY THIS SKILL (that is
`/build-feature`'s contract, teamwork plugin, where installed) — OR the seed was redirected to
`file-bug`/`file-task` under the one-hop rule (first classification only) and the sibling
invocation was reported; no feature record is owed on a redirected seed, and a sibling reached by
redirect runs its own contract, including its own build/no-build rule and its own investigation
dispatch where that applies.
