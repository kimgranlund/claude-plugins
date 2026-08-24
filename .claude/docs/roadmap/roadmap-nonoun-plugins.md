---
doc-type: roadmap
id: roadmap-nonoun-plugins
status: active
date: 2026-08-18
owner: kim.granlund
review-cadence: monthly
---
# ROADMAP — nonoun-plugins

<!-- Issues carrying the `roadmap` label are release-grain items; each binds to its RDD via that
     RDD's ## Sequencing prose citation ("Tracked at <owner>/<repo>#NNN" — docs:doc-writing-rules,
     RDD section, ruled gh#611). This index is the living completion tracker: releases lock, the
     roadmap breathes. -->

## Now
<!-- Committed, in flight; each item links its PLAN or TICKET. -->
- `rdd-0001` — every plugin ships Codex, Hermes, and Pi overlays alongside Claude Code, generated
  by `harness_emit.py` and verified fresh by G15. Shipped and archived (locked, DRI kim.granlund,
  cites `idr-0001`); tracked at kimgranlund/claude-plugins#885.

## Next
<!-- Decided direction, undated by design. -->
- `product-management` plugin migration (product-forge fold-in) — deliberate roster growth per the
  brief's Confirmed roster bullet (ratified 2026-08-16); gated by `harness:plan-plugin-split`'s
  anti-matrix rule before minting.

## Later
<!-- Intent, explicitly reversible. Items here carry no promises. -->
- Option C (Linear) ticket-backend activation — the shipped adapter spec's discovery/polling
  turn-on (`spec-linear-adapter.md`; watch-tickets' own "until then, discovery is gh-only"
  deferral) plus the adapter listing primitive mobilize-chores discloses as missing.
- decision-watcher cross-corpus RDD escalation ("≥2 superseded RDDs citing the same ADR") — the
  deferred extension doc-writing-rules' RDD section already names out of its own scope.

<!-- LIVING STATE: staleness is a bug. The review cadence is the contract. -->
