---
name: doc-writing-rules
description: >-
  Standards for authoring functional documents — ADR, PRD, SPEC, LLD, PLAN, ROADMAP, BRIEF,
  TICKET, TASK, IDR, RDD. Use when asking which document type fits, what sections/frontmatter a type requires,
  whether a document can be edited (why an accepted ADR, a locked IDR, or a locked RDD is
  append-only), how documents reference each other (the ID spine), how plans track status, or why
  doc_lint failed. NOT for drafting one (make-doc); NOT for reviewing one (check-doc); NOT the
  general "why do IDR/ADR/RDD exist, what's the build loop" doctrine, portable to any project
  (product-lifecycle-rules) — this skill owns the live, enforced type contract only.
disable-model-invocation: false
user-invocable: false
---

# Document Authoring Standards

Documents in an agentic harness are interfaces across three boundaries — context (a subagent's
plan file *is* the request), time (an ADR is the only institutional memory), and trust (code
cannot read prose). So they get interface discipline: a schema, a template, a validator, and a
declared **mutability class**. Provenance: distilled from the corpus's Vol 3 (data plane), which
is the source of record; this skill is the operating surface, `references/templates/` the
authoring contracts, `doc_lint.py` the enforcement. No validator, no type.

## The four mutability classes

| Class | Change rule | Types here | Canonical failure |
|---|---|---|---|
| Ledger | Append-only; supersede, never edit | ADR, IDR, RDD | An edited accepted ADR, locked IDR, or locked RDD is a forged memory (the write hook blocks it) |
| Versioned contract | Change via versioned release only | PRD, SPEC, LLD | Silent edits make every downstream reference incomparable |
| Living state | One canonical copy, an owner, a review cadence | PLAN, ROADMAP, BRIEF | Forking — two copies both "current", neither trusted |
| Work item | Living while open; archived on close, learnings promoted first | TICKET, TASK | Closed items left active — future agents act on dead intent |

The class lives in frontmatter and is enforced mechanically, not requested politely.

## Universal practices (every type)

1. **Frontmatter is the type; prose is the payload.** Anything code must read — `doc-type`,
   `status`, `id`, `owner`, `date`, `supersedes` — is structured. Anything needing judgment —
   rationale, tradeoffs — is prose. A status in a sentence cannot gate a pipeline.
2. **Head-first.** Verdict before evidence, decision before context, summary before detail — the
   opening is the only part guaranteed to survive compaction and fan-out.
3. **The ID spine.** Requirements get IDs (`REQ-012`); plan steps, criteria, tickets, and tasks
   reference them. Reference, never restate — restated content is a drift pair with a countdown.
4. **Non-goals are load-bearing.** Agents scope-creep enthusiastically; the out-of-scope section
   is the fence, and for agent consumers it may be the most valuable section in the document.
5. **Author the evaluator with the artifact.** A spec's acceptance criteria are written alongside
   it, one-to-one with requirement IDs — a requirement with no criterion is unverifiable; a
   criterion with no requirement is scope creep in the evaluator.
6. **Location and naming are routing.** `docs/ops/adr/adr-0042-postgres-over-dynamo.md` — root,
   then type, then number/date, then slug; directory conventions are what let hooks and
   path-scoped rules fire. The canonical directory per type under that root (ruled 2026-07-12;
   make-doc and the project-docs index both consume THIS map — a second map is drift): `prd/` ·
   `spec/` · `lld/` · `adr/` · `idr/` · `rdd/` · `plan/` · `roadmap/` · `brief/` · `tickets/` ·
   `task/`. The two pluralization exceptions (`tickets`, `adr`) are historical and
   load-bearing (three command skills hardcode `<root>/tickets/`) — recorded, not to be "fixed".
   `<root>/idr/` and `<root>/rdd/` adopt the canonical type-prefixed numbered form
   (`idr-0001-<slug>.md` / `rdd-0001-<slug>.md`) rather than copying ADR's grandfathered
   exception. Aligning an EXISTING repo to this map is `/tidy-docs`'s job.
   Every canonical directory is repo-rooted, never plugin-rooted (ruled 2026-07-13): resolve
   against the **local or target repo's own root** — the repo the session is already working in
   by default, or a different repo the raw report/idea explicitly names or clearly implies —
   never against a plugin's own installed directory (`${CLAUDE_PLUGIN_ROOT}` names *scripts*, it
   never names a doc destination). Where more than one repo is plausibly in play and the ask
   doesn't disambiguate, name the resolved repo in the close-out report rather than guessing
   silently; never split one document's read (template, standards) from a different repo than its
   write (the instance file).

   **Where documents live (ratified, issue #514).** `<root>` above resolves through a three-rung
   ladder, checked in order:
   1. **Host override** — the target repo's own entry file (CLAUDE.md) states its docs root
      explicitly. When present, that value wins outright, no matter what the portable default
      below would otherwise pick.
   2. **Portable default for repo/project-level records** — `docs/ops/` (Kim's ruling, 2026-08-17:
      "repo/project docs (ROADMAP, PLAN, IDR, ADR, RDD, etc.) generally live under `/docs/ops/`").
      This is what every type directory in the map above hangs off when no override fires.
   3. **Agent-specific docs** — working files an agent produces for its own use (not the
      project's own doc corpus proper) live under `.claude/docs/`, independent of the
      repo/project root chosen above.
   A skill that proposes a doc path degrades gracefully through this ladder — read the host's
   entry file first, fall back to `docs/ops/<type>/` for repo docs or `.claude/docs/` for
   agent docs when the entry file states no override — never hardcodes one tier as the only
   answer.

   **This workspace's carve-out (Kim's ruling, 2026-08-17, issue #514).** *This* repo
   (kimgranlund/claude-plugins) states the override at rung 1: **everything stays under
   `.claude/docs/`**, including repo/project-level records that the portable default would
   otherwise route to `docs/ops/`. Reason: this workspace's `docs` plugin directory already
   owns the bare `docs/` path — a `docs/ops/` root here would collide with the plugin's own
   name — so the carve-out keeps the existing `.claude/docs/{adr,brief,decompositions,handoff,
   idr,lld,prd,spec}` tree as the one location, stated once in this workspace's own CLAUDE.md
   rather than re-derived per skill.
   Delegation is legal for the **work-item tier only** (TICKET/TASK), and generalizes to a
   three-way choice (ruled 2026-07-17, ADR-0003, superseding the 2026-07-15 binary ruling): a
   workspace's entry file names Option A (local — the file default, unchanged), Option B
   (git-native — `gh issue`, ADR-0002's own ruled instance), or Option C (external — a typed
   adapter interface; Linear ships as docs' own concrete Option-C adapter, everything else is
   bring-your-own against the same interface) — see "Work-item backend delegation" below for the
   full three-way contract. The decision/contract tiers (ADR, PRD, SPEC, LLD) and living-state
   docs (PLAN, ROADMAP, BRIEF) are never delegated — they stay files on this map, always.

## The type contract table

What each type is *for*, its class, and the sections `doc_lint.py` requires (templates in
`references/templates/` carry the full authoring contract per type):

| Type | One-line purpose | Class | Required sections |
|---|---|---|---|
| IDR | One testable founding hypothesis/outcome claim, upstream of any decision — plural, numbered (`idr-NNNN`), ADR-parallel lifecycle | ledger | Claim · Why · Proof |
| ADR | One decision, its context, its consequences — forever | ledger | Context · Decision · Consequences |
| PRD | The problem and outcomes, before any how | versioned contract | Problem · Users · Outcomes · Non-goals |
| SPEC | Intent as testable contract — the highest-leverage doc | versioned contract | Requirements · Non-goals · Examples · Acceptance |
| LLD | How it's built: components, interfaces, tradeoffs | versioned contract | Components · Interfaces · Data · Risks |
| PLAN | Sequenced steps, each with "done when" and a status | living state | Steps · Validation · Rollback |
| ROADMAP | Horizons of intent, reviewed on a cadence | living state | Now · Next · Later |
| BRIEF | The north-star loop's living index — one pointer per ratified IDR, never restated content | living state | Thesis · Confirmed · Open Questions |
| TICKET | One shippable unit, traced to spec IDs (`kind: bug`/`feature`, see below; `kind: task` — a generic chore/follow-up, `file-task`'s own convention, no dedicated section needed beyond this row) | work item | Summary · Acceptance · Links |
| TASK | One actor, one sitting, one done-when | work item | Goal · Done-when |
| RDD | One locked release commitment, cited to ≥1 ADR/IDR, DRI-accountable — plural, numbered (`rdd-NNNN`), ADR/IDR-parallel lifecycle | ledger | Scope · Acceptance · Sequencing · Completion |

**Agent verification, template-carried, not yet gated (issue #542, `prd-agent-testability.md`).**
SPEC, PRD, and LLD each carry a `## Agent verification` section in their templates — SPEC and PRD
answering "how would the coding agent tell this was achieved without a human in the loop" (per
requirement for SPEC, per Outcome for PRD), LLD naming which existing instrument already verifies
the design or what harness the build must create first. Deliberately template-carried prose, not
a `doc_lint.py` T-check: the substance (is the assert layer right, is the criterion actually
agent-runnable) is judgment, so it lands in `check-doc`'s J7 criterion — mechanizing presence into
a lint rule is explicitly deferred until the section's shape stabilizes across real instances (the
same retrofit-debt posture as T6's orphan-ADR warn). How to choose the assert layer and design the
harness itself is a separate, larger question — docs' `agent-harness-rules` knowledge pack.

**Rejected alternatives, required at close.** Every TICKET's close-out states what was
deliberately NOT done and why — one section (`## Rejected alternatives` in
`references/templates/ticket.md`), filled in when the ticket moves to `done`/`wontfix`, same
enforcement tier as the `## Findings` write-back convention below (a documented practice teams
follow, not a `doc_lint.py` T3 gate — a bare "nothing rejected" is a valid entry when the chosen
path was genuinely uncontested; an absent section at close is not). Prior art proving the value:
PR #343's scope note, PR #347's no-split writeup — both surfaced a real alternative a reviewer
would otherwise have had to ask about. `dispatch-ticket`'s (teamwork) Findings write-back contract
carries the same requirement for its build path.

**Which type?** Route by the question being answered: what do we believe, before any choice →
IDR; recording a decision → ADR; why build → PRD; what exactly → SPEC; how internally → LLD; in
what order → PLAN/ROADMAP; who does what next → TICKET/TASK; what release commitment did we lock
in, cited to which decisions → RDD; where do our ratified beliefs index, one pointer per IDR →
BRIEF. A document answering two of these questions is usually two documents joined by IDs.

**IDR — Intent Decision Record.** Sits upstream of ADR on the ID spine (more foundational, not
"instead of"): a testable belief about what's true, minted before any architecture choice exists
— admission-tested at authoring time ("would two reasonable builds differ on it?"), same spirit as
ADR's own "a choice someone will later ask why about" gate. Lifecycle mirrors ADR's proven
two-phase mechanic exactly: `draft` (freely editable, the harvest window) → `locked` (committed-HEAD
edits blocked — T4, same mechanism as an accepted ADR) → `superseded` (terminal; a new IDR cites
`supersedes:`). An ADR **may** cite `≥1` IDR via its own `intent-refs:` frontmatter field (parallel
to `supersedes:`) — an ADR with no upstream intent citation warns as an "orphan ADR" (T6) per the
corpus's product-lifecycle-bible (Part 4); ADRs 0001-0013 predate the field and correctly warn
until retrofitted, its own deferred follow-up. **Cardinality** (ruling, issue #273, 2026-08-16):
plural and numbered like ADR — one IDR per testable hypothesis; `idr-0001` is the bootstrap-minted
founding record, not a claim that the type itself is singular. The bible's shape wins in full:
plural locked IDRs **plus ONE living index** (a "product brief" aggregator over `idr-0*`) — the
living-index type landed as **BRIEF** (issue #404, 2026-08-16; row above, `docs/brief/`), one
instance per product/repo — `<scope>` names the product, never a second copy. Full scoping:
`prd-idr-framework.md`; concept authority: `product-lifecycle-bible.md` Part 4.

**RDD — Roadmap Decision Record.** Sits downstream of both ADR and IDR on the ID spine — a locked
release commitment (scope, IDR-grammar acceptance criteria, sequencing, DRI) that **cites** `≥1`
ADR/IDR via its own `decision-refs:` frontmatter field, never the reverse.

**RDD↔work-item binding (ruled 2026-08-18, issue #611):** the `roadmap`-labeled Issues an RDD
bundles bind in `## Sequencing` as plain prose citations — one `Tracked at
<owner>/<repo>#NNN` line per bundled Issue — exactly the template's existing TICKET
precedent (work items are backend-scoped and mutable, so they never enter `decision-refs:`,
which cites immutable in-repo records only); the reverse edge is the Issue's own `## Links`
line naming the RDD id.

RDD realizes the corpus's
product-lifecycle-bible (Part 4) PRP concept as a docs type, named RDD rather than PRP to complete
the `_DR` family grammar IDR/ADR already established. Lifecycle mirrors ADR/IDR's proven two-phase
mechanic: `draft` (freely editable, citations/DRI not yet required) → `locked` (T4 blocks
committed-HEAD content edits; `decision-refs:` and `dri:` become mandatory — T7 FAILs a
locked-or-beyond RDD carrying either empty) → `superseded` (terminal; a new RDD cites
`supersedes:`). **Deliberately no
fourth `shipped-and-archived` status value** (Kim's ruling, 2026-08-16, issue #332): completion
tracking belongs to the `roadmap` type's own living Now/Next/Later movement — "releases lock, the
roadmap breathes" — a shipped RDD stays `locked` forever, byte-identical; a renegotiated
commitment gets a new RDD, exactly the ADR/IDR supersession pattern, never an in-place terminal
flip. `decision-refs:` presence-only for v1 (ruled 2026-08-16): whether each cited id structurally
resolves to a real `adr-*`/`idr-*` file is a deferred stronger check, not built here. The
cross-document escalation pattern this citation spine feeds — "≥2 `superseded` RDDs citing the
same ADR" — is a deferred `decision-watcher` (harness) extension, out of this skill's own scope
(judgment-tier, cross-corpus, not a single-file lint). Full scoping: `prd-rdd-framework.md`;
concept authority: `product-lifecycle-bible.md` Part 4.

## Bug-shaped tickets

A bug report is a TICKET, not a ninth type: `kind: bug` in frontmatter (optional, filterable, not
gated by `doc_lint.py`) plus five sections beyond the type's minimum contract — Repro, Expected vs
actual, Classification, Severity, Findings. `file-bug` mints and updates these; the three
required sections (Summary, Acceptance, Links) are untouched, and `doc_lint.py`'s T3 check never
fails on extra sections, so no validator change was needed. Severity takes exactly one value —
`blocker | major | minor | cosmetic` — the same four everywhere; a per-ticket invented scale
defeats the filtering `kind: bug` exists for. `Findings` is append-only in practice (never enforced
mechanically): every dispatched investigation adds a dated entry at each significant result, not
only at the end — the record that survives a fork killed mid-investigation.

## Feature-shaped tickets

A feature idea is likewise a TICKET, not a ninth type: `kind: feature` plus `size: small | big`
in frontmatter (machine-read — orchestration's `/build-feature` branches its dispatch machinery on it;
small = one context holds it, no contract change · big = multi-component, contract-changing, or
decision-ratifying — the estate's one materiality floor), and two sections beyond the type's
minimum: Scope/Open (the intake's named gaps) and Findings (same append-only dated-entry
discipline as bug tickets — the build's write-back lands here). docs' `/file-feature` mints and
updates these; big features link their earned PRD/SPEC/LLD through the standard Links section,
never inline.

## Issue Type dual-write (Option B, ADR-0004)

On the git-native backend, `kind: bug`/`kind: feature`/`kind: task` also sets GitHub's native
Issue Type (`Bug`/`Feature`/`Task`) in addition to the label each capture skill already applies —
additive, not a replacement: the label stays the system of record, Issue Type is best-effort.
**Two separate calls, never combined into one:** `file-bug`, `file-feature`, `file-task`, and
`issue-sorter` (harness) first run the ordinary `gh issue create` (no `--type`) — the create step is
unchanged from before this ADR, atomic, and always succeeds or fails on its own pre-existing
terms; THEN, once the issue exists, a second call — `gh issue edit <id> --type <Kind>` — attempts
the type. If that second call fails (the org's type schema rejects it — renamed, disabled, or,
the verified case for a personal-account-owned repo: no Issue Types at all, an
organization-scoped feature — or an older `gh` doesn't recognize `--type`), the already-created
issue is simply left with the label alone; the skipped type is noted in the close-out. Never
blocks or fails a mint over a missing type, and — the reason for the two-call split — never risks
minting a second issue: a combined `gh issue create --type <Kind>` was verified (2026-07-19) to
create the issue and only THEN fail the type-attach step silently (no URL printed on that
error), so treating that error as "nothing was created" and retrying the create would duplicate
the record. Size (`size: small | big`) stays a label; migrating it to GitHub's newer Issue Fields is
an explicit non-goal (ADR-0004).

## Work-item backend delegation (ADR-0003)

`file-bug`, `file-feature`, and `file-task` each call one shared resolver instead of re-deriving their own
backend check — closing the hand-duplication ADR-0003 exists to fix, not extending it a third way.
The three-way choice (Option A/local, B/git-native, C/external), the ruling shape a repo's entry
file carries, and the seven-operation adapter interface (create · dedup-search · claim · update ·
close · discover · read) every backend realizes: `references/backend-resolver.md`. ADR-0005 adds
`claim` as the seventh operation — the ticket-layer primitive an agent uses to take ownership of an
existing record before starting execution work against it, distinct from `create` (which mints a
new one); it defines the primitive only, it does not require `file-bug`/`feature`/`issue`
(capture-only skills) to call it. Linear's own concrete realization of the full interface
(transport resolution, configuration, status-type mapping, payload mapping, claim):
`references/linear-adapter.md`. A bring-your-own Option-C adapter documents its own realization the
same way, in its own workspace — this skill owns the interface, not every implementation of it.

## Deliberate non-adoptions (DE-standards gap review, #377)

Two industry/DE-standard practices surfaced in the 2026-08-16 gap review and were deliberately
**not** adopted, because this estate's existing contract is already stricter than the norm they'd
import:

- **Generator ≠ critic.** Already the standing invariant (`plugin-authoring.md`'s semantic-edit
  gate, `checking-rules`) — a maker never grades its own semantic edit. The industry practice this
  would otherwise import (self-review checklists in lieu of a second reviewer) is a weaker
  substitute for a rule already enforced structurally here.
- **ID-spine traceability.** Already stricter than the common "link a ticket to an epic" norm — the
  ID spine (`REQ-###` ↔ plan step ↔ ticket ↔ ADR) is bidirectional and a ticket tracing to nothing
  is named scope creep, above.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Class confusion | Editing ledgers, forking living state | Class in frontmatter; the hook blocks accepted-ADR, locked-IDR, and locked-RDD edits |
| Verdicts in prose | Code can't read the gate | Structured frontmatter enums, always |
| Plans without "done when" | Guesses wearing plan frontmatter | Per-step validation criteria, decided upfront |
| Restated substrate | Spec repeats a skill or a sibling doc → drift pair | ID spine; reference, never restate |
| Type sprawl | One doc answering PRD and SPEC and PLAN questions | One question per type; split, join by IDs |
| Completed docs left active | Dead intent steering live agents | Archive on close; promote learnings on the way out |
| Release with no traceability | A locked RDD with zero cited ADR/IDR, or no named DRI | `decision-refs:`/`dri:` required non-empty at `locked` (T7, FAIL) |

## Provenance

Distilled 2026-07-07 from the corpus's Vol 3 (source of record; consult it for orchestration
handoffs and rubric/report types beyond bugs, which this plugin does not yet template — bug
reports route through TICKET's `kind: bug` convention above). Drafting workflow:
`make-doc`. Judgment: `check-doc`. Method dependencies (sharpening the ask, structural
decomposition, wording, reasoning depth) are the harness plugin's cross-cutting layer —
`find-intent`, `break-down-problem`, `prompt-wording-rules`, `thinking-depth-rules` — used when
installed, degraded to inline judgment when not.
