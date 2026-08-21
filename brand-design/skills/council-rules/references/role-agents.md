# Role agents — one addressable seat per council role

## What a role agent is

A **role agent** is a standalone, directly-dispatchable `Agent`-tool seat that wraps ONE council
role — the Chair, or one ordinary sub-council — as an external interface. It exists for a
different consumer than everything else this pack describes: `check-brand-council` (or any domain
instance's own convening skill) is the host-side orchestrator a user or model invokes through the
skill menu; a role agent is what a **fleet or session** dispatches directly, by name, without going
through that skill at all — "get the Strategy sub-council's read on this," addressed the same way
any other named agent is. This is the one load-bearing difference from every critic-shell agent
this pack already assumes (`brand-judge` and its analogues): those are dispatch-only, fanned out
unnamed by an orchestrating procedure, never invoked directly; a role agent is invoked directly, on
purpose — it IS the addressable surface.

## Convene semantics — what a role agent does when dispatched

A **sub-council role agent**, dispatched (with an artifact and whatever context its domain
requires, inlined per this pack's own input-contract convention), runs a **scoped, phase-1-only**
convene:

1. Read the roster file (`roster-file-contract.md`) and resolve ITS OWN sub-council's seated,
   active handles — never a different sub-council, never `full`.
2. **Empty or all-`VACANT` bench → report "no seats" and stop cleanly.** This is not a failure
   branch to work around — a newly-declared sub-council with nobody minted into it yet is a legal,
   expected steady state (the same posture `check-brand-council` already takes for `advisory`),
   never silently substituted with a different sub-council's roster.
3. Otherwise, fan the domain's critic-shell agent out — unnamed, same-turn, inlined persona per
   dispatch (`blind-fanout-mechanics.md`, cited not restated) — over every seated active handle in
   ITS OWN sub-council only.
4. Resolve any contested finding via 2-of-3 voting, scoped to a third persona from the SAME
   sub-council (`severity-and-voting.md`) — a sub-council too small to seat a third opinion reports
   the contest as **hung** rather than borrowing a critic from a different sub-council.
5. Run the five synthesis shapes (`synthesis-shapes.md`) against the collected findings, scoped to
   this one sub-council's lens — including the blind-spot shape, which is where a scoped read
   explicitly names what it structurally cannot see and recommends the sub-council that could.
6. Return ONE rolled-up read: every finding relayed verbatim, plus the five synthesis shapes.

**Deliberation (phase 2) is out of scope for a sub-council role agent.** It returns a phase-1-only
read; cross-sub-council or chair-moderated deliberation stays the orchestrating convening skill's
own job (`--deliberate` or its domain equivalent), never something a lens-scoped role agent
triggers on its own initiative. A domain that wants a role agent to also run its own deliberation
round is a genuine contract extension, decided and stated explicitly by that domain instance — not
assumed by this pack.

**The Chair role agent** (`agents/council-chair-agent.md` in the brand instance) needs no separate
convene semantics here — its contract is already fully domain-neutral and already dispatched
directly by an orchestrating procedure (`two-phase-model.md`'s "The Chair" section). What's new for
it under this axis is only that it now has a durable, plain-English NAME an orchestrator or a
roster's mapping section can point at, not a behavior change.

## The reserved-name rule

A role agent exists for the Chair and for every **ordinary** sub-council — never for a reserved
name:

- **No role agent for `full`.** `full` is the computed union of every ordinary sub-council
  (`roster-and-personas.md`); convening it is the orchestrating convening skill's own job (it fans
  out across every sub-council at once, which is exactly the nested-orchestrator shape a
  single-sub-council role agent must never attempt — `blind-fanout-mechanics.md`'s own hazard
  record). A fleet wanting the full panel dispatches the convening skill, not a role agent.
- **No role agent for `advisory`.** `advisory` has no lead and carries no adversarial vote weight
  (`roster-file-contract.md`); it rides along whenever `full` convenes and is convened directly only
  through the orchestrating skill, never through a role agent of its own. A mapping section
  (below) naming `advisory` as a role is itself a schema violation.

This mirrors the exact two names `roster-file-contract.md` already reserves for the `sub-councils`
column — the same two names, applied to a second surface (the mapping section) rather than a new
reservation invented for this axis.

## The mapping-section schema

The roster FILE — not this pack — is where a domain instance states which agent handles which
role; that section's own shape (table/list format, required-vs-optional rows, the FAIL/WARNING
split for a dangling handle vs. an unmapped role) is `roster-file-contract.md`'s own concern
(cited from here, never restated), since it lives in the same data file as the roster table and
`## Groups` and is validated by the same `roster_check.py`. This axis states only the CONCEPT the
mapping section exists to name — that a role agent is machinery-shaped enough to deserve a
domain-neutral contract at all — not the file format itself.

## Why this doesn't reopen "cite, don't restate"

A role agent's OWN file (like a critic-shell agent's) is per-instance configuration, not shared
machinery — the same exception this pack already carries for a critic-shell agent's own IDENTITY
(`roster-and-personas.md`'s "what a domain instance supplies vs. inherits" table: a critic-shell
agent's model/tool tier is the domain instance's own, never this pack's fixed fact), extended here
to a second agent family: the mechanics (inlined-only input, unnamed fan-out, phase-1-only scope,
empty-bench stop) are shared and worth copying faithfully, but the IDENTITY (name, description,
which sub-council it's scoped to) is the domain instance's own. `make-council` (the minting
procedure that consumes this axis) mints one role agent per sub-council alongside its critic-shell
agent, patterned off an existing role agent's structure the same way a new critic shell is
patterned off `brand-judge`'s — its own `references/roster-and-chair-wiring.md` states the
practical wiring checklist for both agent families, cited from there, never restated here.
