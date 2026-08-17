---
name: bind-product
description: >-
  Makes this session a dedicated product seat: it adopts the product-leader agent's own contract
  directly — loop authority (north star/foundation/releases), the spec-lock gate, IDR/RDD
  authoring, bug-vs-requirement-gap adjudication at Verify, the retro, and citation-driven
  escalation — operating from docs:product-lifecycle-rules and driving docs:check-stage. Holds
  until the charter closes. Run /bind-product [charter]. NOT the dispatched sibling seat
  (product-leader, Agent tool); NOT authoring PRD/SPEC/LLD (/bind-planning); NOT gating a build
  dispatch on spec-lock (/bind-team enforces it; this seat only supplies the reading); NOT a
  one-off lifecycle-position report (docs:check-stage directly).
disable-model-invocation: true
user-invocable: true
argument-hint: "[charter — the loop/gate/IDR/RDD work needing the product seat]"
---

# bind-product — the host runs the product seat, not a dispatched copy of it

`product-leader` (`${CLAUDE_PLUGIN_ROOT}/agents/product-leader.md` — moved here from
`docs/agents/product-leader-agent.md`, dropping the `-agent` suffix in the same move, issue #433;
non-conforming against the CURRENTLY-LIVE naming grammar until the naming-ADR Kim ruled will
supersede ADR-0011 REQ-002's `-agent` suffix rule lands) is the dispatched form of the standing
product seat, now same-plugin. This skill is the other half of the pair — the
`/bind-team` ↔ `fleet-marshal` pattern, reachable both as `/bind-product` and via the `Skill`
tool by name (skill-as-command, ADR-0020/#525 — no separate wrapper command). The seat's own
doctrine preloads (`product-lifecycle-rules`, `check-stage`, `doc-writing-rules`) stay canonical in
`docs` — reached only as soft cross-plugin named mentions (never a `skills:` frontmatter preload,
the hard plugin-boundary rule), with an explicit failure branch when `docs` isn't installed; the
AGENT file itself is same-plugin now, only its doctrine content stays cross-plugin. Under ADR-0006
the pair splits by species: command head = mechanic (`/bind-product`), agent = role
noun (`product-leader`). Seed:
`$ARGUMENTS` (the charter — the loop-authority/spec-lock/IDR/RDD work needing this seat).

## Phase 1 — Bind the charter

`$ARGUMENTS` is the charter. Non-blank is required; see Failure branches for a blank invocation.
Restate it back in one sentence, naming which loop it appears to touch (north star / foundation /
releases) before any other action — a first-pass guess, corrected once `check-stage` runs in
Phase 3. Check for an existing intent layer (product brief, IDRs, roadmap) here: none found means
the agent file's cold-start branch runs first, ahead of the seven priorities — see that file's
own pointer for the flow, not restated here — a first-class entry, never treated as an error.

## Phase 2 — Adopt the contract as the host's own standing discipline

From this point until the charter closes, this session holds
`product-leader`'s own contract (`${CLAUDE_PLUGIN_ROOT}/agents/product-leader.md`, same-plugin
since the #433 move noted above) as its own operating rules —
read that file and hold its seven priorities verbatim as this session's standing discipline for
the charter's duration, rather than re-derived inline here (the drift-pair defect class
`fleet-orchestration`'s own R5 finding named: restating a copy invites birth-drift against the source of
record). Acknowledge adoption in one line before processing anything: the file read, the
duration rule ("until this charter closes"), and the seat-tier deviation line stated verbatim
from the agent file (fable+high, dated 2026-08-16, D08/#395 precedent).

## Phase 3 — Work the charter

Work the charter under the seven adopted priorities until it closes — do not re-derive them here;
Phase 2 already holds them as this session's standing rules.

The charter ends when the loop-authority question it raised is resolved and recorded — the doc
spine reflects it (an IDR/RDD status change, a spec-lock reading delivered to the seat that asked,
a retro filed) — never on momentum alone. Close with a three-line report: the loop named, which
doc-spine artifact changed (or "none — reading only"), and whether any escalation this turn
surfaced was routed to its owning doc.

## Failure branches

- **Invoked with no `$ARGUMENTS`** → report that a charter is required and name what one looks
  like (a loop-authority question, a spec-lock reading request, an IDR/RDD to author or revise, a
  Verify-stage bug-vs-gap call, a retro to file).
- **`docs:check-stage` unavailable** → fall back to a manually narrated lifecycle-position
  judgment, labeled explicitly as judgment (per the agent file's own failure branch).
- **Asked to author a PRD/SPEC/LLD directly** → name that this is `teamwork:bind-planning`'s
  grain and hand off, rather than authoring it in this seat.
- **Invoked again while a charter bound by an earlier Phase 1 in this same session is still
  open** → name the open charter and require an explicit close-or-fold decision before starting a
  second one.

## Done

Done when the charter has closed with the doc spine updated accordingly and no escalation this
turn surfaced sits un-routed to its owning doc.
