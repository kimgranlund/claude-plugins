---
name: doc-authoring-standards
description: >-
  Standards for authoring functional documents — ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK.
  Use when the user asks which document type a situation needs, what sections or frontmatter a type
  requires, whether a document can be edited (mutability classes — why an accepted ADR is
  append-only), how documents should reference each other (the ID spine), how plans track status,
  or why a doc failed doc_lint. Carries the type contract table the templates and validator
  enforce. NOT for drafting a document (doc-forge); NOT for reviewing one (doc-review).
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
| Ledger | Append-only; supersede, never edit | ADR | An edited accepted ADR is a forged memory (the write hook blocks it) |
| Versioned contract | Change via versioned release only | PRD, SPEC, LLD | Silent edits make every downstream reference incomparable |
| Living state | One canonical copy, an owner, a review cadence | PLAN, ROADMAP | Forking — two copies both "current", neither trusted |
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
6. **Location and naming are routing.** `docs/adr/adr-0042-postgres-over-dynamo.md` — type, then
   number/date, then slug; directory conventions are what let hooks and path-scoped rules fire.

## The type contract table

What each type is *for*, its class, and the sections `doc_lint.py` requires (templates in
`references/templates/` carry the full authoring contract per type):

| Type | One-line purpose | Class | Required sections |
|---|---|---|---|
| ADR | One decision, its context, its consequences — forever | ledger | Context · Decision · Consequences |
| PRD | The problem and outcomes, before any how | versioned contract | Problem · Users · Outcomes · Non-goals |
| SPEC | Intent as testable contract — the highest-leverage doc | versioned contract | Requirements · Non-goals · Examples · Acceptance |
| LLD | How it's built: components, interfaces, tradeoffs | versioned contract | Components · Interfaces · Data · Risks |
| PLAN | Sequenced steps, each with "done when" and a status | living state | Steps · Validation · Rollback |
| ROADMAP | Horizons of intent, reviewed on a cadence | living state | Now · Next · Later |
| TICKET | One shippable unit, traced to spec IDs (bug reports: `kind: bug`, see below) | work item | Summary · Acceptance · Links |
| TASK | One actor, one sitting, one done-when | work item | Goal · Done-when |

## Bug-shaped tickets

A bug report is a TICKET, not a ninth type: `kind: bug` in frontmatter (optional, filterable, not
gated by `doc_lint.py`) plus five sections beyond the type's minimum contract — Repro, Expected vs
actual, Classification, Severity, Findings. `bug-report` mints and updates these; the three
required sections (Summary, Acceptance, Links) are untouched, and `doc_lint.py`'s T3 check never
fails on extra sections, so no validator change was needed. Severity takes exactly one value —
`blocker | major | minor | cosmetic` — the same four everywhere; a per-ticket invented scale
defeats the filtering `kind: bug` exists for. `Findings` is append-only in practice (never enforced
mechanically): every dispatched investigation adds a dated entry at each significant result, not
only at the end — the record that survives a fork killed mid-investigation.

## Feature-shaped tickets

A feature idea is likewise a TICKET, not a ninth type: `kind: feature` plus `size: small | big`
in frontmatter (machine-read — orchestration's `/build` branches its dispatch machinery on it;
small = one context holds it, no contract change · big = multi-component, contract-changing, or
decision-ratifying — the estate's one materiality floor), and two sections beyond the type's
minimum: Scope/Open (the intake's named gaps) and Findings (same append-only dated-entry
discipline as bug tickets — the build's write-back lands here). Scribe's `/feature` mints and
updates these; big features link their earned PRD/SPEC/LLD through the standard Links section,
never inline.

**Which type?** Route by the question being answered: recording a decision → ADR; why build →
PRD; what exactly → SPEC; how internally → LLD; in what order → PLAN/ROADMAP; who does what next →
TICKET/TASK. A document answering two of these questions is usually two documents joined by IDs.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Class confusion | Editing ledgers, forking living state | Class in frontmatter; the hook blocks accepted-ADR edits |
| Verdicts in prose | Code can't read the gate | Structured frontmatter enums, always |
| Plans without "done when" | Guesses wearing plan frontmatter | Per-step validation criteria, decided upfront |
| Restated substrate | Spec repeats a skill or a sibling doc → drift pair | ID spine; reference, never restate |
| Type sprawl | One doc answering PRD and SPEC and PLAN questions | One question per type; split, join by IDs |
| Completed docs left active | Dead intent steering live agents | Archive on close; promote learnings on the way out |

## Provenance

Distilled 2026-07-07 from the corpus's Vol 3 (source of record; consult it for orchestration
handoffs and rubric/report types beyond bugs, which this plugin does not yet template — bug
reports route through TICKET's `kind: bug` convention above). Drafting workflow:
`doc-forge`. Judgment: `doc-review`. Method dependencies (sharpening the ask, structural
decomposition, wording, reasoning depth) are the forge plugin's cross-cutting layer —
`intent-extract`, `system-decompose`, `linguistic-techniques`, `reasoning-orders` — used when
installed, degraded to inline judgment when not.
