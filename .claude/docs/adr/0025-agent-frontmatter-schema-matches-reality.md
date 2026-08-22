---
doc-type: adr
id: adr-0025
status: accepted
ratified: Kim, 2026-08-21, close-session leftovers round (plan-2026-08-brand-design-bloat-overhaul
  seed S5, Gate A approved 2026-08-21) — "amend the spec, don't backfill."
date: 2026-08-21
owner: kim.granlund
scope: app
audience: any-agent, builder
supersedes: adr-0011 (§8's agent frontmatter schema only — the provenance/policy fields
  `kind`/`author`/`created`/`last_updated`/`performs`/`autonomous_write`/`context` drop out of
  the estate-wide agent schema; the identity fields `name`/`description`, the grammar/directory
  rules (§§2-6), the composition-relations mechanism (§7), and the migration posture (§10) all
  stand unamended. ADR-0011 is not edited — accepted ADRs are append-only; this citation is the
  entire mechanism of the supersession, exactly as ADR-0011's own partial supersessions by
  ADR-0014/0015/0016/0017/0018/0020/0024 work.)
intent-refs: null
---
# ADR-0025 — Agent frontmatter schema (§8) amended to match reality

> **Ratified 2026-08-21 by Kim**, in a `close-session` leftovers round closing out
> `plan-2026-08-brand-design-bloat-overhaul` seed S5, filed as issue #863. From ratification
> this file is append-only (doc_lint T4); a change of mind supersedes, never edits.

## Context

`spec-naming-convention.md` §8 documents an agent frontmatter schema — identity
(`name`/`kind`/`description`), relations (`performs`), invocation policy
(`autonomous_write`/`context`/`tools`), and provenance (`author`/`created`/`last_updated`) — as
a validated, enforced contract (§11 AC-004/AC-006/AC-007). It was never adopted.

Measured 2026-08-21 across every agent in this workspace (40 files, `*/agents/*.md`, one
plugin's own dogfooding copy excluded): 39/40 carry none of `kind`/`author`/`created`/
`last_updated`/`performs`/`autonomous_write`/`context` — only `authorkit/agents/
estate-audit-agent.md` carries the full documented schema, and it does so as a deliberate
self-dogfood (`authorkit/skills/naming-audit/scripts/validate.py`'s own `schema_scope`
mechanism, issue #226/#224 ruling b, already treats these fields as authorkit-internal
convention, not estate law, for exactly this reason). A cross-plugin sample the originating
ticket named directly — harness's `skill-checker`, teamwork's `builder`, docs' `doc-checker` —
carries none of it either.

What every one of the 40 files *does* carry, at real, measured frequency:

| Field | Files carrying it | Real role |
|---|---|---|
| `name` | 40/40 | identity — unchanged from §8.1 |
| `description` | 40/40 | the trigger/dispatch contract — unchanged from §8.1 |
| `model` | 40/40 | model-tiering ladder (`harness:agent-writing-rules`) |
| `tools` | 40/40 | the actual tool grant — the one real policy surface §8.3 got right |
| `effort` | 37/40 | reasoning-effort tier, paired with `model` |
| `skills` | 24/40 | preloaded skill dependencies — the real analogue of §7's `requires` edge, not `performs` |
| `color` | 12/40 | display grouping, cosmetic |
| `disallowedTools` | 1/40 | negative tool grant (rare) |

Origin: `plan-2026-08-brand-design-bloat-overhaul` seed S5 (Gate A approved 2026-08-21; ruled
2026-08-21 close-session: amend the spec, don't backfill — the same posture ADR-0024 D1 took for
`evals/`, applied here in the opposite direction: the *document* is the stale side, not the
practice).

## Decision

### D1 — §8's required/optional field lists are replaced with the measured convention

§8.1's Identity block drops `kind` as a frontmatter field (kind is still decided by directory
+ name-parse per §5/§6 exactly as before — it was never something an agent *declares*, so
nothing here touches decided-kind logic, only the now-defunct declared-`kind:` frontmatter key).
Required, all agents: `name`, `description`. Common, not schema-enforced: `model`, `tools`
(present on every sampled agent; `tools` is the real locus of least-privilege policy §8.3
gestured at). Optional: `effort`, `color`, `skills` (an agent's preloaded skill dependencies —
plays the role §7 assigned to `requires`, under the name every real agent actually uses),
`disallowedTools`.

### D2 — §8.2's `performs` relation field and §8.3's `autonomous_write`/`context` policy fields
drop out of the agent schema

`performs` (asserting, in frontmatter, that an agent's name minus `-agent` equals a real skill)
is not how the estate actually verifies that relation — §5's parse algorithm already checks it
structurally, from the name itself, with no frontmatter field needed; zero agents duplicate it
in frontmatter, and none need to. `autonomous_write` and `context` (`isolated`/`inherited`) are
dropped identically — no agent declares either, and the platform's own dispatch mechanics (an
agent's tool grant, and whether it is dispatched via a fresh context or a fork) already carry
the distinction these fields would have restated. §7's `requires` relation, and the `performs`
row in §7's own relation table, are unamended by this ADR — this decision touches only §8's
*frontmatter schema* claim that agents carry these as declared fields, not §7's account of the
relation graph itself, which stays available for a future artifact that does want to declare it.

### D3 — §8.4's provenance block (`author`/`created`/`last_updated`/`review_after`) drops out
of the agent schema

Zero adoption outside authorkit's own self-dogfooding copy. The staleness-tracking rationale
§8.4 gave is a real and reasonable idea, but it was never wired to anything outside one
plugin's own validator running in `--scope full` on itself — restating it as estate-wide schema
when the estate that would enforce it never adopted the enforcement is exactly the aspiration-
over-reality drift this ADR exists to close. `authorkit`'s own internal convention is untouched
by this decision (`schema_scope: "full"` inside its own tree stands; issue #226/#224 already
drew this exact line without touching §8's estate-wide text, which is the actual gap this ADR
closes now).

### D4 — No backfill

This ADR licenses no rename, no mass-edit, and no new required field on any of the 40 sampled
agents (or any other agent in the estate). The fix is the spec text — describing what agents
already carry — never a campaign to make agents carry what the spec used to describe. This
mirrors ADR-0024 D1's own "the spec was stale, not the practice" framing, applied to a different
section of the same document.

## Consequences

- **§8 is rewritten in place** (this file's own convention, matching how §3.1/§3.2/§6.1 already
  carry prior ADR amendments inline): `kind`/`performs`/`autonomous_write`/`context`/`author`/
  `created`/`last_updated`/`review_after` drop out of the documented agent schema; `model`/
  `tools`/`effort`/`color`/`skills`/`disallowedTools` are documented as the real, measured
  convention. A dated §14.11 is appended to the amendments log.
- **§11's AC-004/AC-006/AC-007 acceptance checks, as written against the OLD §8, described
  validation this estate's own gates never ran outside authorkit's self-dogfooding tree** — no
  validator code anywhere in this estate enforces the dropped fields against agents outside
  authorkit (confirmed: `naming.manifest.json`'s `schema_scope: "grammar"` already routes
  estate-wide agents around the full structural schema; `--scope full` is authorkit's own choice
  on itself, unaffected by this ADR). Nothing here changes gate behavior — it changes what the
  spec *claims* the gate behavior means.
- **No exemption or migration debt created.** Every agent in the estate already conforms to the
  amended §8 as of this ADR — nothing newly passes or fails naming-audit's frontmatter channel
  that did not already pass or fail it before this change (`schema_scope` decided that outcome
  in 2026-08-14/#226, independently of this document edit).
- **`authorkit`'s own internal dogfooding convention is untouched.** `estate-audit-agent.md`
  keeps carrying the fuller field set as its own plugin's internal choice; this ADR narrows what
  the *estate-wide* spec claims of every other agent, not what any one plugin may choose to
  additionally track on itself.
- **Reversible the ordinary way:** a future amendment could re-widen §8's schema if a real
  consumer for `performs`/`author`/`created`/`last_updated` ever materializes estate-wide — it
  would supersede this ADR by the same citation-only mechanism this file uses on ADR-0011.

## Alternatives considered

- **Alt A — backfill `kind`/`author`/`created`/`last_updated`/`performs`/`autonomous_write`/
  `context` onto all 40 agents instead of amending the spec.** Killed by the originating
  ruling itself ("amend the spec, don't backfill") and by proportion: retrofitting seven fields
  nothing reads across 40 files, to make reality match an aspirational document, is exactly the
  busy-work the spec's own §8 preamble warns against ("no field enters the schema unless
  something reads it").
- **Alt B — leave §8 as written, rely on `schema_scope` to keep it non-blocking.**
  Killed: `schema_scope` only controls the *validator's* gating behavior; it does nothing to
  stop the spec's own text from misdescribing the estate's actual convention to the next reader
  who consults it, which is the drift this ADR exists to close (`entry-file-rules`' stale-context
  standing conviction: an invalidated record is a defect, same severity as a bug).
- **Alt C — widen the validator's `FIELDS` schema to match §8 exactly and enforce it
  estate-wide (the reverse direction from ADR-0024's `evals/`/`intent.md` fix).** Killed: unlike
  `evals/`/`intent.md` (an enforced, cross-plugin invariant the spec had fallen behind), zero
  evidence exists that the dropped provenance/relation/policy fields are load-bearing anywhere
  outside authorkit's own tree — widening enforcement to match aspiration, rather than narrowing
  aspiration to match practice, is the opposite of what the measured evidence supports.

## Execution order (at acceptance)

1. Ratify this ADR (status → accepted, done at authoring time per the ratification recorded
   above).
2. `.claude/docs/spec/spec-naming-convention.md` §8: identity/relations/policy/provenance
   subsections rewritten to the measured convention (D1-D3); a dated §14.11 appended to the
   amendments log.
3. Re-run `authorkit:naming-audit` on brand-design's 4 agents to confirm zero frontmatter
   findings under the amended schema (issue #863's own acceptance criterion) — a confirmation
   step, since `schema_scope: "grammar"` already meant no findings gated there before this change.
4. Issue #863 Findings: dated entry closing the ticket, citing this file and the confirmation
   run.
