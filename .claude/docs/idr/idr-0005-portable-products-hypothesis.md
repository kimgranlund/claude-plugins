---
doc-type: idr
id: idr-0005
status: locked
date: 2026-08-16
owner: kim.granlund
proof-ref: harness/agents/issue-sorter.md (friendlies allow-list — the adoption-signal instrument)
provenance: decided-by-human
supersedes: null
---
# IDR-0005 — A real external audience warrants the portability cost (ratified, low urgency)

## Claim

An external audience for these eight plugins will materialize eventually, though not yet — Kim's
2026-08-16 ratification: "others eventually, I'm the user for now" — and the portability
discipline already built (marketplace framing, degrade-gracefully mentions, hard plugin
boundaries) is warranted to keep as-is at zero further investment until it does. No new adoption
tooling, no expanded external-audience surface, until a real adoption signal lands.

## Why

Provenance: decided-by-human — originally minted `inferred` (a hypothesis about the past, not an
asserted decision): the codebase behaves as if the plugins are portable products for third-party
installation — the README's Install section (marketplace `kimgranlund/claude-plugins`, and its
"rather than just installing them" framing), the MIT LICENSE, and
`.claude/rules/plugin-authoring.md`'s hard-boundary rule (preloads and script paths never cross
plugins; mentions degrade gracefully when a plugin isn't installed). No record stated who the
product was for, and no adoption signal was found as of 2026-08-16. Kim's 2026-08-16 ratification
answer (live `AskUserQuestion`, ratification round) confirmed the inference — external audience,
low urgency, keep the machinery, don't invest further yet — and is the decision of record from
this lock onward; the `inferred` origin stays disclosed here rather than erased.

## Proof

Confirms: a real adoption signal — e.g. a non-owner filer exercising `issue-sorter`'s friendlies
allow-list (proof-ref), or a marketplace install from outside this estate. Falsifies: no such
signal across a stated window (three consecutive monthly brief reviews, per
`brief-nonoun-plugins.md`'s `review-cadence`) with no change in the portability machinery's actual
use — supersede with the internal-only reading at that point, never edit this locked file.
