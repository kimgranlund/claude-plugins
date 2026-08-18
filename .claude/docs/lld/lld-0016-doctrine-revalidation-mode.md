---
doc-type: lld
id: lld-0016-doctrine-revalidation-mode
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: kimgranlund/claude-plugins#623  # renumbered TWICE: lld-0014 (fit at branch-cut, lld-0013
  # was max) -> lld-0016, because PR #636 (#627's reconstructibility-audit) merged lld-0014-
  # reconstructibility-audit.md, and PR #638 (#626's estate-rhythm) then took lld-0015 for the
  # same reason, both landing on origin/main before this PR opened (the #633 rule; re-verified via
  # `git ls-tree origin/main -- .claude/docs/lld/` immediately before this PR opens: max is 0015)
spec: none — idr-0009 (locked, doc-writing-rules' IDR contract) already carries the ratified CLAIM,
  Why, and Proof (falsification test) for the concept itself; this LLD resolves only the Scope/Open
  design questions #623's own body leaves open (instrument shape, sampling policy, queue routing),
  the same routing test lld-0008/lld-0009/lld-0013 already applied (a standalone SPEC would restate
  what idr-0009 + #623 already state).
---
# LLD — decision-watcher gains a Revalidation mode: re-test accepted doctrine, don't just accumulate it (#623)

**Verdict, head-first:** one new MODE on the existing `decision-watcher` agent/`watch-adrs` skill —
**not a sibling seat** (idr-0007's job-evidence test: a new coordination seat needs a named gap the
mode itself cannot cover, and none is named here — the existing checkpointed-scan machinery already
does 80% of the mechanical work this mode needs). One new bundled script,
`harness/scripts/revalidation_checkpoint.py`, mirrors `adr_checkpoint.py`'s classify/advance
non-mutating split and `adr_queue.py`'s add/pending/clear pattern for a **sampled, round-robin sweep**
over two claim corpora — every ACCEPTED ADR's Decision text, every LOCKED IDR's Proof section (the
Confirms/Falsifies text together, not a fragile "Falsifies:"-keyword extraction — see Rejected
alternatives) — handing each sampled claim to a judgment step that emits one of three verdicts:
confirmed / falsified / untestable. `falsified` and `untestable` verdicts queue as candidates
(`revalidation-queue.json`, same scratch-copy write-sandbox discipline as the existing ADR queue);
`confirmed` is reported and dropped, no state grows. The sweep **never rewrites doctrine** — a
queued `falsified` candidate's next step is the human-ratified amend/supersede path (a named owner
field, exactly the way a `harvest` candidate's next step is a named `/make-pack` command, never
something this agent runs itself). Cadence is explicitly **not** assigned here — idr-0011 owns it,
still open at gh#626 — this mode is invokable on-demand or via the same session-scoped `CronCreate`
decision-watcher already uses, and fires with whatever `--n` sample size the dispatching session
names.

## Resolution 1 — Instrument shape: a mode, not a sibling seat (idr-0007's job-evidence test)

**Resolved: a new mode on `decision-watcher`/`watch-adrs`**, per #623's own comment-thread lean and
idr-0009's Open-questions bullet ("a new seat fails idr-0007's job-evidence test until the mode is
tried and proves insufficient"):

- **The mechanical substrate already exists and is 80% reusable.** `adr_checkpoint.py` already
  parses all three ADR dialects this repo's corpus and two sibling repos' corpora ship (frontmatter,
  H1+blockquote-table, H1+bold-metadata) and already exposes `decision_content()` (heading-scoped
  extraction, generic across dialects) and `parse_frontmatter`/`parse_status_table`/
  `parse_bold_metadata` as importable pure functions. Re-deriving ADR-dialect parsing in a sibling
  seat's own script would duplicate ~500 lines of already-selftested logic for zero new capability.
- **The write-sandbox contract, the never-authors boundary, and the batched-confirm discipline are
  already stated once in `watch-adrs`/`ops-write-sandbox-rules`** and apply verbatim to this mode —
  a sibling seat would either restate all three or (worse) silently drift from them over time.
- **No named gap the mode itself cannot cover.** The one candidate gap — "revalidation judgment is a
  DIFFERENT kind of judgment than harvest-worthiness" — is not a coordination gap; it's a difference
  in what the SAME agent is asked to judge on a given firing (harvest-bar judgment on a classify
  delta vs. tri-state judgment on a sampled claim), which a mode flag already resolves cleanly (the
  same way `adr_checkpoint.py classify` vs `advance` are two verbs on one script, not two scripts).

## Resolution 2 — Sampling policy: round-robin over a sorted claim-id list, corpus-append-safe

**Resolved:** a **combined, lexicographically-sorted list of claim ids** — every `adr-NNNN` whose
live status is `accepted`, every `idr-NNNN` whose live status is `locked` — with one integer cursor
persisted at `.claude/ops/revalidation-checkpoint.json`. `sample --n N` slices the next `N` ids
starting at `cursor mod len(list)`, wrapping once (never duplicating an id within one sample call
even when `N > len(list)` — it caps at the corpus size and says so); `advance --n N` is the second,
separate call (never combined — same crash-safety split as `adr_checkpoint.py`'s classify/advance)
that bumps the persisted cursor only after the sampled claims have actually been judged.

- **Why round-robin over random sampling:** deterministic, reproducible from the checkpoint alone
  (no seed to manage), and the ADR/IDR corpora here are **append-only by this workspace's own T4
  discipline** (an accepted ADR's frontmatter never changes; a locked IDR is append-only) — so the
  sorted list only ever grows at its tail (or shrinks narrowly, when an accepted ADR is superseded
  and drops out of the accepted set). A growing, mostly-stable corpus is exactly the case round-robin
  handles well: newly ratified claims enter the rotation and get their turn as the cursor wraps,
  with no special-casing needed for "new" vs "old" claims the way the forward classifier needs it —
  this mode does not care when a claim was minted, only that it comes up for re-test on its turn.
- **Corpus-shrink edge case, named not hidden:** an ADR flipping `accepted` → `superseded` between
  two firings removes it from the list and can shift other claims' effective positions by one. This
  is accepted as a minor redistribution, not a correctness bug — the selftest's own round-robin
  fixture proves the cursor still advances sanely and no claim is silently skipped forever; a claim
  that never comes up because the corpus keeps shrinking faster than it's sampled would show up as
  the "sweep tests the wrong layer" falsification idr-0009 already names, not a hidden defect in
  this script.
- **`--n` default and who sets it:** the script takes no opinion on cadence-appropriate sample size
  (that's idr-0011's territory, still open); a bare `sample` with no `--n` defaults to 5 as a
  reasonable per-firing unit, always overridable by the dispatching prompt.

## Resolution 3 — Claim-text extraction: whole sections, not fragile keyword surgery

**Resolved:** the claim text handed to judgment is the **whole `## Decision` (+ `## Amendment*` /
`## Supersession*`) section** for an ADR (reusing `adr_checkpoint.decision_content()` verbatim,
already dialect-generic) and the **whole `## Proof` section** for an IDR — never a regex-extracted
"just the Falsifies clause." This was tested against the real corpus during authoring and falsified
its own first design: idr-0009 and idr-0011 phrase it `Falsifies: ...`, idr-0007/idr-0008 phrase it
mid-sentence (`... Falsifies: a measured run...`), idr-0006 phrases it `Falsifies on the first
review...`, and **idr-0001 never uses the word "Falsifies" at all** — its Proof section reads
"falsified by a ledger entry re-fixing a previously-mechanized incident class" (passive voice, a
different verb form entirely). A keyword-anchored extractor would either miss idr-0001's clause
outright or need an ever-growing list of phrasings — exactly the "chase a fragile extraction when a
coarser one already suffices" trap. Handing over the whole Proof section costs nothing extra (Proof
sections run 1–4 sentences in every sampled IDR) and gives judgment the Confirms condition for free,
which it needs anyway to reason about the untestable branch (a claim written so vaguely that neither
its confirm nor its falsify condition can actually be checked).

## Resolution 4 — Verdict routing: confirmed drops, falsified/untestable queue with a named owner

**Resolved**, per idr-0009's own Open-questions leans, realized as data:

- **`confirmed`** — reported in the firing's payload, nothing persisted to the queue. **The report
  itself still names every confirmed claim, individually, with a one-line reason** (a per-claim
  verdict table, not a bare tally) — a `confirmed` verdict is the one call this mode makes and
  resolves entirely on its own, no human gate anywhere in the loop, which is exactly the rubber-
  stamp risk idr-0009's own doubt names; the durable AUDIT trail is the report itself (this is
  what keeps repeated-confirmed sweeps CHEAP to persist while staying legible to catch a bad
  streak — the falsification test's own "repeated sweeps returning only confirmed" needs the
  per-firing report to be checkable, not a silently-dropped count).
- **`falsified`** — queued to `revalidation-queue.json` via `queue-add --claim <id> --kind falsified
  --evidence "<what broke>" --owner <name>`, same idempotent append-or-update-by-(claim,kind)
  discipline as `adr_queue.py`. **`--owner` is a required flag, not optional** — idr-0009's own
  Open-questions bullet names "who executes a falsified verdict" as unresolved at ratification, and
  the fix is structural: the field exists on every row, so a queued falsified candidate is never
  ownerless even before idr-0011's calendar assigns who checks the queue. The dispatching session (a
  human present, or the next on-demand sweep) supplies the owner from the claim's own record — the
  ADR/IDR's `owner:` frontmatter field is already right there to read. **No `owner:` field on the
  record** (the table/bold-metadata ADR dialects carry no frontmatter, so this only ever arises for
  an ADR claim) → the dispatching human's own name, or `unassigned` on an unattended firing, named
  explicitly in `--evidence` — never a fabricated name and never a stall.
- **`untestable`** — queued the same way, `--kind untestable`, evidence naming WHY the claim resists
  a check (not merely "couldn't test it this time"). Per idr-0009's lean ("flag-for-rewrite, never
  silent exemption"), an untestable verdict is itself a doc defect finding against the owning record
  — the queued row IS that finding, and its next step (named in the report, never executed by this
  agent) is a `file-task` ticket asking for an appended amendment (or a superseding record — both
  stay append-only per T4) restating the clause checkably.
- **Never auto-filed as a GitHub Issue by this agent.** `decision-watcher`'s existing Boundaries
  section already bars it from running `/make-pack`/`/make-skill`/`save-lessons` Phase 6 itself; this
  mode adds no exception — a confirmed `falsified`/`untestable` candidate's next command
  (`file-bug`/`file-task`, per idr-0009's own lean) is named in the report exactly as a harvest
  candidate's `/make-pack` command already is, for a human or the dispatching session to run.

## Resolution 5 — Cadence: explicitly deferred, cited not assigned

**Resolved: this LLD assigns no cadence.** idr-0011 (locked the same 2026-08-18 round as idr-0009)
rules that every standing loop carries a ruled cadence, but its own Open Questions leave "which
loops + cadences are in the first calendar" open at gh#626 — this mode is the first candidate loop
for that calendar, not a loop that gets to self-assign one ahead of the ruling. The mode ships fully
invokable (on-demand dispatch, or the same session-scoped `CronCreate` decision-watcher's forward
mode already uses when a human arms it) with no opinion on how often it SHOULD fire; #626's ruling
round is the named next step for cadence, cited here rather than duplicated.

## Components

Build sequence — a builder executes top to bottom:

1. **`harness/scripts/revalidation_checkpoint.py`** — new bundled script, plugin-level (touches the
   forward classifier's own state directory, same tier as `adr_checkpoint.py`/`adr_queue.py`).
   Imports `parse_frontmatter`, `parse_status_table`, `parse_bold_metadata`, `decision_content`,
   `hash_adr` from `adr_checkpoint` (same-directory sibling import, no cross-plugin boundary
   crossed). New pure functions: `parse_idr_file` (frontmatter `doc-type: idr` gate, `## Proof`
   section extraction via a generic heading-bounded-section helper, reused for both ADR and IDR
   shapes); `scan_adr_claims`/`scan_idr_claims` (directory scan → `{claim_id: {"kind", "text",
   "status"}}`, accepted/locked filter applied). **Directory sources only** — unlike
   `adr_checkpoint.py`'s own `scan_source` auto-detect, `sample`/`advance` require both
   `<adr-source>` and `<idr-source>` to be directories and raise `SourceUnreadable` on a bare file
   path (the monolithic single-file dialect is out of scope for this mode: `decision_content`'s
   own extraction basis assumes a per-record file, which the monolithic dialect's own hash basis —
   the whole section per ADR — already satisfies differently; revisit only if a monolithic-dialect
   repo asks for this mode). Commands: `sample <adr-source> <idr-source>
   [--checkpoint <path>] [--n N]` (non-mutating, prints the sampled claims' full text + cursor
   state, `--n` defaults to 5); `advance <adr-source> <idr-source> [--checkpoint <path>] --n N`
   (persists the bumped cursor only); `queue-add <path> --claim <id> --kind falsified|untestable
   --evidence <text> --owner <name>`; `queue-pending <path>`; `queue-clear <path>
   --ids <id[:kind],...>`; `selftest`.
   Exit codes 0/1/2 per `script-writing-rules`. Selftest fixtures use the REAL idr-0001/idr-0006/
   idr-0007/idr-0009 body text (the phrasing-variance evidence Resolution 3 is built on) as positive
   controls, plus a proposed-status IDR and a superseded ADR as negative controls (excluded from the
   sample corpus), plus a round-robin cursor-wrap + corpus-growth control.
2. **`harness/skills/watch-adrs/SKILL.md`** — new `## Revalidation mode, one firing` section:
   procedure (sample → judge each claim tri-state against the claim's own text, using the same
   judgment-is-expensive-so-scope-it-to-the-delta economics the forward mode already states →
   queue falsified/untestable to a scratch copy → advance the cursor on a scratch copy → report
   payload, same fenced target-pathed contract as the forward mode's step 6) plus its own failure
   branches (an IDR/ADR source unreadable; a sampled claim whose text is empty after extraction —
   report as `untestable` immediately, never silently skip); explicit cross-reference to idr-0009
   (the ratified concept) and idr-0011 (cadence, deferred). Description gains one clause naming the
   new mode (routing-surface edit) — evals.json gains matching trigger/no-trigger cases in the same
   change (`.claude/rules/plugin-authoring.md`).
3. **`harness/agents/decision-watcher.md`** — description gains one clause: the agent now also
   supports a periodic re-validation sweep of accepted ADR Decisions + locked IDR falsification
   clauses (tri-state verdict), citing `watch-adrs`'s new section rather than restating it. One new
   `<example>` block (Revalidation-mode firing) alongside the existing two.
4. **Fresh-context checker pass** on both semantic edits (SKILL.md body + agent description) per
   `.claude/rules/plugin-authoring.md`'s critic invariant — `harness:skill-checker` on `watch-adrs`,
   `harness:agent-checker` on `decision-watcher`, both FLOOR depth (a mode addition to an existing,
   already-reviewed seat, not a from-scratch author or an estate-portfolio question).
5. **Gates before PR:** `python3 harness/scripts/revalidation_checkpoint.py selftest`; `skill_lint.py`
   on the edited SKILL.md + evals.json + the agent file; `eval_check.py`; `/check-routing harness`
   (description boundary changed); `release_gate.py harness --package`.
6. **Plugin close-out:** `harness/.claude-plugin/plugin.json` version bump (re-read off `origin/main`
   immediately before the PR opens, per the VALUE-race discipline — 3.11.0 at authoring time) +
   README footer ledger line naming #623, the new mode, the sampling policy, and the two touched
   files.
7. **Dated comment on #623** naming the shipped instrument's path (`harness/skills/watch-adrs/
   SKILL.md`'s new section + `harness/scripts/revalidation_checkpoint.py`) — never an edit to
   idr-0009 itself, which is locked/append-only (T4-adjacent, per the ticket's own instruction); the
   proof-ref already points at #623's seed comment, which this comment extends.

## Interfaces

- **`revalidation_checkpoint.py` → `adr_checkpoint.py`:** same-directory Python import of four pure
  parsing functions + `decision_content`/`hash_adr` — no new cross-plugin or cross-skill boundary;
  both live in `harness/scripts/`.
- **`watch-adrs`'s new mode → `ops-write-sandbox-rules`:** identical compute-only contract already
  governing the forward mode — every mutating call targets a scratch copy, the report carries the
  target-pathed payload for the dispatching session to apply.
- **A queued `falsified`/`untestable` candidate → `file-bug`/`file-task`:** named as the next command
  in the report, exactly as a `harvest` candidate names `/make-pack`; this agent never invokes either
  skill itself (Boundaries section, unchanged, extended not re-derived).
- **Cadence → idr-0011 / gh#626:** cited, never assigned here (Resolution 5).

## Data

New state file `.claude/ops/revalidation-checkpoint.json` (schema: `{"cursor": int,
"last_sampled_at": "<UTC>"}`), new state file `.claude/ops/revalidation-queue.json` (schema:
`{"candidates": [{"claim_id", "kind": "falsified"|"untestable", "evidence", "owner", "queued_at"}]}`)
— same convention as `adr-checkpoint.json`/`adr-queue.json`: checked into the repo, not gitignored,
mutated only via the write-sandbox scratch-copy contract. No migration: both files are absent until
this mode's first firing, at which point they're created via the standard payload-apply step.

## Risks

- **R-1 (phrasing variance defeats a narrower extractor later).** Resolution 3's whole-section
  choice is deliberately the coarser, robust option; a future contributor narrowing it back to
  keyword extraction re-introduces the idr-0001 miss. Detection: the selftest's four real-IDR
  fixtures are the negative control that would catch a regression. Fallback: none needed — the
  design is the fix.
- **R-2 (corpus-shrink cursor redistribution, accepted).** Named in Resolution 2. Detection: idr-0009's
  own falsification test (a claim that never comes up for re-test across many cadences). Fallback:
  none built here — a real recurrence would be evidence for a future supersession of this LLD's
  sampling design, per idr-0009's own supersede-on-falsification discipline.
- **R-3 (judgment quality — a sweep rubber-stamping "confirmed" without real testing).** This is
  idr-0009's own named doubt, not new to this build. Detection: idr-0009's Proof section already
  states the falsification test (repeated all-confirmed sweeps alongside independent incidents).
  Fallback: none in this LLD — it's the concept's own accepted risk, not this instrument's to solve.
- **R-4 (owner field goes stale — the record's frontmatter `owner:` changes after a candidate is
  queued).** Detection: none automated. Fallback: the human applying a batched confirm re-reads the
  record's current `owner:` before acting, same as any other stale-queue-row risk `adr_queue.py`
  already carries informally.

## Rejected alternatives

- **A sibling seat (`revalidation-watcher`) instead of a mode.** Rejected by Resolution 1's
  job-evidence test — no named gap the mode can't cover, and it would duplicate ~500 lines of already-
  selftested ADR-dialect parsing for zero new capability. idr-0007/idr-0009 both name this as the
  wrong default absent evidence.
- **Full-corpus re-test every firing.** Rejected per #623's own seed lean and idr-0010's economy
  concern (a sweep whose cost isn't proportional to a bounded per-firing sample would price itself
  out of idr-0010's worth-firing test on a 20-ADR/7-IDR-and-growing corpus); round-robin sampling
  (Resolution 2) keeps cost flat and cadence-configurable instead.
- **Regex-anchored "Falsifies:" clause extraction.** Tried first, falsified by the actual corpus
  (Resolution 3) — kept here as a named rejection, not silently dropped, since a future contributor
  reaching for the same shortcut should find this note before re-deriving the same miss.
- **This LLD assigning its own cadence** (e.g. "weekly, on-demand fallback"). Rejected — idr-0011
  reserves the calendar ruling for its own gh#626 round; a per-loop LLD self-assigning a cadence
  ahead of that ruling would pre-empt the very queue-discipline idr-0011 exists to impose.
- **Storing per-claim verdict HISTORY in the checkpoint** (not just a rotation cursor). Rejected as
  unneeded state: the report IS the durable record of each firing's verdicts (same "payload, not a
  write" discipline as the forward mode), and a `falsified`/`untestable` finding already gets its own
  durable row in `revalidation-queue.json` until resolved — a third, redundant history file would be
  state growth with no named consumer.

## Agent verification

Assert layer: **payload layer** — `revalidation_checkpoint.py selftest` proves the pure parsing/
sampling logic (extraction correctness against real corpus fixtures, round-robin correctness,
queue idempotency) deterministically, no model judgment needed to verify the MECHANICS. **Mechanical
layer:** `skill_lint.py` (both edited artifacts), `eval_check.py`, `/check-routing harness`,
`release_gate.py harness`. **Human/judgment layer, stated exception:** whether a given firing's
tri-state VERDICTS are themselves correct (did the sweep actually judge the claim well) is not
payload-checkable — that's idr-0009's own accepted risk (R-3 above), verified only by the
falsification test idr-0009's Proof section already names (repeated firings vs. independent incident
evidence over time), never by this LLD's own gates. Named here per assert-layer-choice's rule that
every human-routed criterion is written down, not a silent gap.
