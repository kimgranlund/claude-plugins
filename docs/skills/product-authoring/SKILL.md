---
name: product-authoring
description: >-
  Makes this session a dedicated product seat: it adopts the product-leader-agent's own contract
  directly — loop authority (which of north star / foundation / releases is turning), the
  spec-lock hard gate, IDR/PRP authoring and their living indexes, bug-vs-requirement-gap
  adjudication at Verify, the written retro, and citation-driven escalation — operating from
  docs:product-lifecycle-rules and driving docs:check-stage for the lifecycle-position question.
  Holds until the charter closes. Run /product-authoring [charter]. NOT the dispatched sibling seat
  (product-leader-agent, Agent tool); NOT authoring PRD/SPEC/LLD (teamwork's /lead-planning, one
  loop-tier down); NOT enforcing the spec-lock gate at dispatch time (teamwork's /lead-team, which
  reads this seat's gate); NOT a one-off lifecycle-position report (docs:check-stage directly).
disable-model-invocation: true
user-invocable: true
argument-hint: "[charter — the loop/gate/IDR/PRP work needing the product seat]"
---

# product-authoring — the host runs the product seat, not a dispatched copy of it

`product-leader-agent` (`${CLAUDE_PLUGIN_ROOT}/agents/product-leader-agent.md`) is the dispatched
form of the standing product seat. This command is the other half of the pair — the
`/lead-team` ↔ `team-lead` pattern, ported to this plugin because the seat's own preloads
(`product-lifecycle-rules`, `check-stage`, `doc-writing-rules`) are docs-local (same-plugin-preload
precedent: `docs:lead-intake` ↔ `docs:intake-lead`). Under ADR-0006 the pair splits by species:
command = nominal object-process form conforming to ADR-0011's naming grammar
(`/product-authoring` — this is a NEW name, so the legacy `lead-*` verb form isn't available;
`lead-team`/`lead-review`/`lead-planning` stay grandfathered under naming-rules), agent = role
noun (`product-leader-agent`). Seed:
`$ARGUMENTS` (the charter — the loop-authority/spec-lock/IDR/PRP work needing this seat).

## Phase 1 — Bind the charter

`$ARGUMENTS` is the charter. Non-blank is required; see Failure branches for a blank invocation.
Restate it back in one sentence, naming which loop it appears to touch (north star / foundation /
releases) before any other action — a first-pass guess, corrected once `check-stage` runs in
Phase 3. Check for an existing intent layer (product brief, IDRs, roadmap) here: none found means
the agent file's cold-start branch runs first, ahead of the seven priorities (harvest → draft
provenance-marked intent → one batched human ratification round → close day 0 homes-not-content)
— a first-class entry, never treated as an error.

## Phase 2 — Adopt the contract as the host's own standing discipline

From this point until the charter closes, this session holds
`${CLAUDE_PLUGIN_ROOT}/agents/product-leader-agent.md`'s own contract as its own operating rules —
read that file and hold its seven priorities verbatim as this session's standing discipline for
the charter's duration, rather than re-derived inline here (the drift-pair defect class
`lead-team`'s own R5 finding named: restating a copy invites birth-drift against the source of
record). Acknowledge adoption in one line before processing anything: the file read, the
duration rule ("until this charter closes"), and the seat-tier deviation line stated verbatim
from the agent file (fable+high, dated 2026-08-16, D08/#395 precedent).

## Phase 3 — Work the charter

Work the charter under the seven adopted priorities until it closes — do not re-derive them here;
Phase 2 already holds them as this session's standing rules.

The charter ends when the loop-authority question it raised is resolved and recorded — the doc
spine reflects it (an IDR/PRP status change, a spec-lock reading delivered to the seat that asked,
a retro filed) — never on momentum alone. Close with a three-line report: the loop named, which
doc-spine artifact changed (or "none — reading only"), and whether any escalation this turn
surfaced was routed to its owning doc.

## Failure branches

- **Invoked with no `$ARGUMENTS`** → report that a charter is required and name what one looks
  like (a loop-authority question, a spec-lock reading request, an IDR/PRP to author or revise, a
  Verify-stage bug-vs-gap call, a retro to file).
- **`docs:check-stage` unavailable** → fall back to a manually narrated lifecycle-position
  judgment, labeled explicitly as judgment (per the agent file's own failure branch).
- **Asked to author a PRD/SPEC/LLD directly** → name that this is `teamwork:lead-planning`'s
  grain and hand off, rather than authoring it in this seat.
- **Invoked again while a charter bound by an earlier Phase 1 in this same session is still
  open** → name the open charter and require an explicit close-or-fold decision before starting a
  second one.

## Done

Done when the charter has closed with the doc spine updated accordingly and no escalation this
turn surfaced sits un-routed to its owning doc.
