---
doc-type: idr
id: idr-0005
status: draft
date: 2026-08-16
owner: kim.granlund
proof-ref: pending-ratification
supersedes: null
---
# IDR-0005 — A real external audience warrants the portability cost (inferred)

## Claim

A real external audience exists for these eight plugins, and that audience warrants the
portability discipline's cost. Confirm or supersede: an internal-only reading sheds part of the
marketplace and degrade-gracefully machinery; an external reading keeps it and adds adoption
measurement.

## Why

Provenance: inferred — a hypothesis about the past, not an asserted decision. The codebase
behaves as if the plugins are portable products for third-party installation: the README's
Install section (marketplace `kimgranlund/claude-plugins`, and its "rather than just installing
them" framing), the MIT LICENSE, and `.claude/rules/plugin-authoring.md`'s hard-boundary rule
(preloads and script paths never cross plugins; mentions degrade gracefully when a plugin isn't
installed). No record states who the product is for, and no adoption signal was found as of
2026-08-16. Needs the DRI's confirmation before anything load-bearing cites it.

## Proof

The DRI's audience decision, recorded as this IDR's own ratification (the `status` flip to
`locked`) or its supersession by the internal-only reading — hence `proof-ref:
pending-ratification`. If the external reading is confirmed: any adoption signal, e.g.
`issue-sorter`'s friendlies allow-list being exercised by a non-owner filer.
