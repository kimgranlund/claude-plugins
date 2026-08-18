---
doc-type: adr
id: adr-0021
status: proposed
date: 2026-08-18
owner: kim.granlund
supersedes: null
intent-refs: idr-0005 (the external-audience hypothesis this model must grow into), idr-0004
  (autonomy through gates — trust tiers are the input-side gates)
---
# ADR-0021 — Trust tiers per input surface, and injection hardening for record-text-into-prompt flows

> DRAFT — `status: proposed`, awaiting Kim's ratification (one batched round with
> idr-0008/0009/0010/0011 and adr-0022, per gh#622–#627). The accepted-ADR append-only rule
> binds only after acceptance; until then this text may be revised freely.
> Record-type note: ADR, not IDR — this rules a CONTRACT that binds concrete input surfaces
> across plugins (which tier each surface sits in, what each tier may influence), not a
> hypothesis; the standing ADR-default-no ruling is met by that binding.

## Context

The estate's one trust primitive, `friendlies.json`, gates issue AUTHORS only. Everything else
is trusted by default: cross-session SendMessages steer seats verbatim; PR/Issue/ticket body
text flows into dispatch prompts unfenced (a live prompt-injection surface); gh-api landings
bypass local guards entirely; and `bypassPermissions` is the global default with only rm/dotenv
deny tripwires. Acceptable for a single-human estate — but IDR-0005's external audience has no
threat model to grow into, and ADR-0012's auto-merge carve-out already makes one trust-adjacent
ruling with no framework around it. Origin: conceptual hole #4 of the 2026-08-18 estate gap
review (gh#625; the six tickets gh#622–#627 are the review's durable record; sibling records
idr-0008/0009/0010/0011, adr-0022).

## Decision

Proposed: every input surface that can influence an agent's behavior is assigned a **trust
tier**, and the tier — not the surface's convenience — rules what that input may do:

- **T0 — Operator.** Kim's own messages and AskUserQuestion answers, and the permission system.
  May change anything, including permissions, config, and doctrine. Nothing else ever may.
- **T1 — Registered fleet seats.** SendMessage traffic among seats in the fleet roster
  (fleet.json). May direct work within a dispatched charter; may never authorize permission,
  settings, or config changes, and is never consent (the standing dispatched-agent rule, now
  tiered rather than ambient).
- **T2 — Record text.** PR/Issue/ticket bodies, artifact and shared-content text, cron-routine
  payloads. **Data, never instructions**: when record text enters a dispatch prompt it is fenced
  and labeled untrusted (the quote-not-obey rule), and a directive found inside it is reported,
  not obeyed. ADR-0012's `auto-merge: authorized` grant line remains the ONE ruled exception —
  a T2-carried token deliberately granted T1-like force, subsumed here as a named carve-out
  rather than an ambient precedent.
- **T3 — Foreign/unauthenticated.** Input from authors outside `friendlies.json`. Passes the
  friendlies gate before it is even handled as T2; may trigger triage only, never dispatch.

First hardening the ruling implies (named, not shipped in this PR — follow-up seed in gh#625):
a `teamwork:fleet-rules` bullet encoding the T2 quote-not-obey rule for record text entering
dispatch prompts.

## Consequences

Positive: prompt-injection through PR/Issue bodies stops being an unexamined default; gh-api
landings and SendMessage steering get an explicit tier to be audited against; IDR-0005's
external audience arrives into a model instead of into `bypassPermissions`. Negative/cost:
fencing record text adds friction to every dispatch that quotes a ticket, and the tier table is
a new surface that can drift from practice — each surface-tier assignment must live where it can
be re-validated (idr-0009's sweep names accepted-ADR Decisions as in scope, so this table is
re-tested like any other Decision). Neutral: `bypassPermissions` itself stays ruled by Kim's
standing yolo-with-tripwires posture; this ADR tiers inputs, it does not re-open the permissions
default.

## Open questions

- Exact input-surface inventory: the seed names four (SendMessage, record text into prompts,
  gh-api landings, bypassPermissions); artifact/shared-content text and cron payloads are
  assigned T2 above by this draft's judgment — confirm the full enumeration at ratification.
- Human-facing surfaces: lean is minimally IN — who may edit `friendlies.json` itself is a T0
  act (an operator-only write), stated here rather than left ambient; confirm.
- One ADR vs ADR + companion SPEC: lean is one ADR; a SPEC is minted only if the tier table
  outgrows prose (per the intake's own clarifier, unanswered).
- Which hardening ships first: lean is the fleet-rules quoting bullet (smallest, widest reach)
  over an issue-sorter guard extension; the ruling round may reorder.
