---
doc-type: adr
id: adr-0026
status: accepted
ratified: by Kim
date: 2026-08-23
owner: kim.granlund
supersedes: null
scope: app
audience: any-agent, planner
intent-refs: idr-0005
---
# ADR-0026 — IDR-0005's zero-further-investment clause binds audience-facing surface only

## Context

gh#885 (cross-harness packaging: Codex + Hermes + Pi overlays, `harness_emit.py`) raised
whether IDR-0005 — the locked hypothesis that the portability discipline built for a future
external audience is "warranted to keep as-is at zero further investment until [a real
adoption signal] does" — governs that work. Kim's ruling at the fleet-bootstrap gate
(2026-08-23): it does not. Cross-harness/agent-runtime interop (a second host tool reading
this estate's plugins) is a distinct concern from external-audience portability (a third-party
installer outside this estate); IDR-0005's claim and proof-ref (README Install framing, MIT
LICENSE, `plugin-authoring.md`'s hard-boundary rule, `issue-sorter`'s friendlies allow-list)
are all audience-facing signals, none of them cross-harness ones. IDR-0005 is `locked` —
append-only, never edited — so this ruling is recorded as a citing ADR rather than a change to
the IDR itself.

The sibling record for gh#914 (a retroactively minted RDD for the harness-emit roadmap work)
cites IDR-0001 (self-governing toolchain) rather than IDR-0005 for the same reason: that work
is toolchain self-governance, not audience portability.

## Decision

IDR-0005's "zero further investment" clause is narrowed to bind audience-facing surface only —
README/marketplace framing, LICENSE terms, plugin-boundary hygiene for third-party installers,
and adoption-signal tooling (`issue-sorter`'s friendlies allow-list). It does not bind
cross-harness or agent-runtime interop work (gh#885's Codex/Hermes/Pi overlay emission and
similar), which is scoped, planned, and invested in on its own merits under the doc-writing-rules
type ladder, independent of whether an external-audience adoption signal has landed.

IDR-0005 itself stays locked and unedited; this ADR is the citing record future campaigns
consult before re-litigating the clause's scope.

## Consequences

- gh#885's cross-harness packaging work (and future cross-harness/agent-runtime work) is not
  gated on IDR-0005's adoption-signal proof/falsify condition.
- A future campaign proposing new audience-facing surface (adoption tooling, expanded
  marketplace framing) still checks IDR-0005's proof/falsify condition first, unchanged.
- `decision-watcher`'s revalidation sampling may sample IDR-0005's falsification clause per
  idr-0009; this ADR narrows what that clause is understood to cover, it does not alter the
  clause's text or review cadence.
