---
name: file-feature
description: >-
  Capture a feature idea as a durable record: a ticket, design docs, or a reference corpus when
  it's really knowledge to encode. Use when the user proposes a new capability or pitches an
  idea — "can we add a dark mode", "what if we supported CSV export". Intake only, never builds.
  /file-feature [idea, or a TKT-/#issue/adapter id] resumes. NOT for bugs (file-bug); NOT for
  chores (file-task); NOT for authoring docs (make-doc); NOT the UI-shaped intake SCHEMAS
  themselves (frontend:feature-intake-rules, design:token-feature-intake-rules) — this skill only
  routes to them.
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

**Backend seam (Phase 0):** resolve once via doc-writing-rules' `references/backend-resolver.md`;
every phase below follows whichever option it returns.

**Pre-fork grill for big/open-decision-space seeds only (ruled 2026-08-18, gh#654) — runs OUTSIDE
this fork, in the caller's live session, never as a phase below.** This skill is fixed at
`context: fork` above; Phase 2 below's gh#541 finding (the fork has no question channel at all)
is why the round can never run live once this skill's own body starts executing, no matter which
phase claimed it. So for a seed that is BIG or genuinely open in its decision space (not already a
small, concrete ask — a rough, caller-side call made before invocation; Phase 4 below still sizes
the eventual record formally, and the two need not agree), the session about to invoke
`/file-feature` — a human typing the command, or the model routing here via the Skill tool — runs
`teamwork:grill-the-ask` (soft cross-plugin mention, degrading gracefully to the phases below on
the raw seed where teamwork isn't installed) FIRST, live, before this skill is ever invoked, then
hands the sharpened result in as `$ARGUMENTS`. A seed that already reads small and concrete skips
this round entirely. `file-bug` and `file-task` keep their own existing intake shapes — this
ruling is `file-feature`'s alone.

**This fork cannot verify the grill ran — it only sees `$ARGUMENTS`.** A seed that reads BIG or
open-decision-space yet carries no sign the round above ran (no grilled/sharpened framing, no
`[grilled]` marker) is captured anyway, same as any other gap this fork can't resolve live (Phase
2's own discipline) — name "pre-fork grill skipped" in Scope/Open (it counts toward the
close-out's terse `owed-questions` total, gh#713 — the text itself never restates there), never
block the mint on a caller that skipped the round.

## Phase 1 — Route: fresh idea, or resume by record state

`$ARGUMENTS` contains a record id — `tkt-####`/`TKT-####` (case-insensitive) resolving to a file
in `docs/tickets/`, on the git-native backend `#NN`/a bare issue number resolving via
`gh issue view`, or under Option C an id in the resolved adapter's own native format (Linear:
`TEAM-123`) resolving via that adapter's `read` operation (`references/linear-adapter.md`,
REQ-010) — → resume by that record's state. On the git-native backend, apply `doc-writing-rules`'
Provenance-tagging convention (`references/backend-resolver.md`) to the resolved record right
here, before any branch below — every branch that follows exits this phase, so the tag is applied
at resolution time, not deferred to a phase a given resume might never reach. Trailing text that is EXACTLY the Phase 6 offer's own
resume word (verbatim `install-docs-index`, case-insensitive, nothing else trailing it) → skip
straight to Phase 6's write regardless of open/closed state — accepting the index offer is not a
scope change and needs no sizing. Anything more than the bare word (new detail, an answer, the
word plus other text) folds first under the branches below, same as any other trailing text; the
word only triggers the direct-to-Phase-6 route when it is the ENTIRE trailing text with nothing
else to fold. Otherwise: `done`/`wontfix`/closed → report and stop, echoing back any trailing text
unfolded (reopening is the user's call, but an answer to a question the record's own Scope/Open
names is not silently dropped); open with new detail following the id — including an answer to a named
clarifying question — → fold it into Summary/Scope/Open (clearing the answered gap from
Scope/Open once folded) and re-run Phase 4's sizing only if the new detail changes the size
class; otherwise (open, no new detail) → report the record's state, size, and placement, point at
`/build-feature` for momentum, and stop. An id that does not resolve (no such file; `gh issue view`
errors; Option C's `read` returns not-found, AC-010) is a fresh idea — say so, never proceed as if
a record existed.

## Phase 2 — Extract (no live clarify round — the fork has no question channel)

Invoke find-intent (harness, where installed; apply its discipline inline otherwise): root goal
vs literal ask, the delta taxonomy — but do not run its clarifying round as a live
`AskUserQuestion` call. **Measured 2026-08-17 (gh#541):** a `context: fork` background dispatch
has no question channel at all — `AskUserQuestion` is unreachable from inside it (confirmed two
ways: two independent thin captures, #1122 and #541's own filing, both minted clarify-less; and a
background dispatch cannot even discover the tool). This is this skill's only invocation shape
(`context: fork` is fixed above), so the round never runs live, full stop.

Corrected assumption (2026-08-09 text, falsified 2026-08-17 per gh#541, kept here as the dated
record of the mistake): the prior claim — "a live user is the default assumption; forking
relieves the caller's session, it does not remove the person" — is wrong. Do not restate it as
canon.

What happens instead: capture immediately from `$ARGUMENTS` alone (carries no conversation
history), naming every gap the clarifying round would have surfaced — including a seed that
references context the fork cannot see ("the idea we discussed", "what I just described"), which
is itself a named gap, never a guess — in the record's Scope/Open section. The close-out (Phase
5, at mint) then owes the round it couldn't run live: it reports their count in its one-line
terse form (gh#713) — their text already stands in the record's Scope/Open, above, never
restated in the close-out; the resume command — `/file-feature <id> <answers>` — folds the
answers into the record once a person supplies them (Phase 1's fold-in path already handles "open
with new detail following the id"). Name no clarify questions in the close-out when the seed
carries `[redirected-from:X]` (the round budget
was already spent upstream) or `[unattended]` (no live session to report back to at all) — the
shared marker protocol, canonical statement `file-task`'s Phase 2. Either way, a still-vague idea
never blocks persistence — vagueness is a named gap, never a gate.

**The testability question rides the same capture-or-gap treatment.** For a likely-Work idea
(Phase 4 confirms shape; extraction runs before that, so this asks provisionally rather than
waiting), extraction also captures *how the built result will be agent-verifiable* — which assert
layer (payload/API/browser/human) per `docs:agent-harness-rules` — same as every other extraction
question: the seed already answers it → capture it; it doesn't → name it as a Scope/Open gap
("needs a harness first") — it counts toward Phase 5's terse `owed-questions` total (gh#713),
never restated there. Never a blocking live round — this phase's own no-question-channel finding above applies here
too — and never a restatement of `agent-harness-rules` itself, only a cite. Phase 4 shaping the
idea Knowledge (or a Failure-branch redirect) moots this provisional gap — it never survives into
a non-Work record's Scope/Open.

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

**UI-shape detection (gh#711, lld-0024) — a Work-shaped seed only, soft named mention, degrades
gracefully.** A Work-shaped seed that reads as a component/module, a layout/shell, a UX-flow, or
a cross-cutting UX (motion/focus/i18n) ask consults `frontend:feature-intake-rules` for its
per-shape intake schema; one that reads as a token/palette/typography seed consults
`design:token-feature-intake-rules` instead — both by SOFT named mention
(`.claude/rules/plugin-authoring.md`'s hard boundary: no preload, no `${CLAUDE_PLUGIN_ROOT}`
cross-plugin path). Either pack's schema fields, once filled, become this record's own
Acceptance/Scope content directly — both plane columns answered or a named open fork (the
packs' own both-planes capture-completeness rule), plus the shape's `build-owner`/`dod-checker`
pair carried into this record's own frontmatter (a forward claim: `dispatch-ticket` reading and
routing on those fields is lld-0024's own follow-up, not yet a live consumer). **Degrade branch,
named explicitly:** `screens`/`design` not installed, or the seed doesn't read as any of the five
UI shapes (four screens' + one design's) → classify proceeds on this phase's own plain Size/Shape
decision alone, the gap named in Scope/Open ("UI-shape schema not consulted — plugin absent" or
"not UI-shaped") rather than silently skipped. This paragraph never fires for a
Knowledge/Defect/chore-shaped seed.

## Phase 5 — Record, lint, place

The payload contract, identical regardless of backend: Summary · Acceptance (from the extraction's
success criterion, plus — for a Work-shaped record — Phase 2's agent-verifiability answer, stated
as which assert layer per `docs:agent-harness-rules`; unanswered → carried in Scope/Open as "needs
a harness first" instead of blocking the record) · Links (the ID spine to any PRD/SPEC/LLD/corpus
minted in Phase 4) · Scope/Open (the named gaps) · the size class · an empty `## Findings` section
for the eventual build's write-back.

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

`.github/ISSUE_TEMPLATE/feature.yml` mirrors this contract for a human filing directly on GitHub —
this template, plus its `bug`/`task` siblings, IS the feedback intake door idr-0008 names; no
separate door exists or is owed. On Option B, apply `doc-writing-rules`' Provenance-tagging
convention (`references/backend-resolver.md`) at this record's creation — Phase 1 above applies
the same convention on resume.

Place it: add the line to ROADMAP (Now/Next/Later) or PLAN **only where those docs already
exist** — never mint living-state docs unprompted (both backends; queue docs stay files).

**The close-out is the terse one-line form (gh#713, uniform across all three intake siblings):**
`Filed: <id> · kind:feature · owed-questions:<N>` — `<id>` is whichever the backend resolved
(ticket path, issue URL, or adapter-native id), `<N>` counts whatever Phase 2 named as unasked
clarifying questions (no `[redirected-from:X]`/`[unattended]` marker on the seed); the questions'
own full text stays where Phase 2 already wrote it, in the record's Scope/Open section, never
restated here. This one line is the head line and the whole close-out in the normal case;
exception notes this skill names elsewhere (a skipped Issue Type, a backend-create fallback, the
project-docs offer below) append as extra lines only when they occur.

## Phase 6 — Bootstrap the project index (opt-in, when absent)

The record is durable but not yet DISCOVERABLE: a fresh session finds `docs/` only if told.
Direct entry only — the seed carries no `[redirected-from:X]` and no `[nested-intake]`
(`dispatch-ticket`'s marker — teamwork, renamed from `dispatch-feature` per ADR-0010 — when it
runs this skill's intake as part of `/build-feature`'s
pipeline): a nested run already owes `dispatch-ticket`'s own ambiguity question and this skill's
own Phase 2 round — skip this offer entirely on either marker (never mind the question channel:
per Phase 2's measured finding, none of these were ever live `AskUserQuestion` rounds anyway, only
named-in-the-close-out ones). When `.claude/skills/project-docs/SKILL.md` is absent from the
project, no `[unattended]` marker is on the seed, and entry is direct, this step does not attempt
a live `AskUserQuestion` offer either (same gh#541 finding as Phase 2: the fork has no question
channel) — it names the offer in the close-out instead: "no project-docs index skill found —
install it? reply `/file-feature <id> install-docs-index` and this skill will write it from
`assets/project-docs-skill-template.md` (fills `{{PROJECT_NAME}}` from the repo directory name or
the project manifest's name field)." That resume word, and ONLY that word with nothing else
trailing it, is Phase 1's own trigger (above) for routing straight to the write, skipping the
Summary/Scope fold-in a plain answer would take; the same word arriving alongside other text
folds first, same as any other trailing detail, and does not short-circuit to the write.
Writing into `.claude/skills/` changes the project's routing surface, which is why this stays an
offer named for a person to accept via that resume, never a default-yes write from the fork
itself. Unanswered → the offer simply stands in that close-out; no re-ask on a later resume that
doesn't invoke it, no marker files — the option is "not now", never "never": with no durable
record of a refusal, a standing no cannot be honored, so it is not offered again unprompted. The
skill already present → skip silently, nothing to name in the close-out.

## Failure branches

Phase 4 defers its Defect/generic-chore redirect here — this is that redirect's canonical
statement, not a re-narration:

- FIRST classification only (no `[redirected-from:X]` marker yet), the ask is bug-shaped
  ("X is broken") → invoke `file-bug` via the Skill tool, seed prefixed
  `[redirected-from:file-feature]`; report which sibling was invoked and why. One hop only
  (the shared rule, canonically stated in `file-task`'s SKILL.md); Phases 5–6 never run for a
  redirected seed.
- Same, a generic chore/follow-up with nothing to size or shape → invoke `file-task`, same
  marker and one-hop rule.
- A seed already carrying `[redirected-from:X]` (a DIFFERENT sibling) → captured regardless of
  fit: `kind: feature` with the mismatch named in Scope/Open — this skill's own redirect never
  fires twice.

Every other branch — a resume's shipped/queued dedup hit (Phase 3), `doc_lint.py` and
backend-fallback failures (Phase 5, and doc-writing-rules' backend-resolver.md for the fallback
shape), and a declined index bootstrap (Phase 6) — is handled inline at its own phase; not
restated here.

Done when a `kind: feature` record exists — a lint-clean file on disk, a labeled GitHub Issue (its
URL reported), or an Option-C adapter's record (its native id reported) — sized and shaped
correctly, linked into whatever queue docs exist, with
every extraction gap named, the index offer's disposition reported (installed path, offered and
unanswered, already-present skip, or skipped-nested) — and NO build was dispatched BY THIS SKILL (that is
`/build-feature`'s contract, teamwork plugin, where installed) — OR the seed was redirected to
`file-bug`/`file-task` under the one-hop rule (first classification only) and the sibling
invocation was reported; no feature record is owed on a redirected seed, and a sibling reached by
redirect runs its own contract, including its own build/no-build rule and its own investigation
dispatch where that applies.
