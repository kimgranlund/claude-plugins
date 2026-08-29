---
doc-type: adr
id: adr-0019
status: accepted
ratified: Kim, 2026-08-17, quoted verbatim in issue #514's seed text
date: 2026-08-17
owner: kim.granlund
supersedes: null
intent-refs: idr-0002    # where the cold-start memory idr-0002 claims actually lives on disk
---
# ADR-0019 — Docs-location convention: `docs/ops/` for repo/project records, `.claude/docs/` for agent docs, this workspace overrides to `.claude/docs/`-only

> **Ratified 2026-08-17 by Kim**, quoted verbatim from issue #514's seed text (routed through
> `/file-task`, originally phrased as a `/find-intent` ask that never ran its clarifying round).
> From ratification this file is append-only (doc_lint T4); a change of mind supersedes, never
> edits.

## Context

Some skills in the `docs` plugin propose organizing project documents under the local
`.claude/docs/` scope. Issue #514 flagged this as hard to find for certain agents and for
macOS users (a hidden dotfolder in Finder — asserted, not independently evidenced in this
ticket, but not the load-bearing part of the ruling). The issue's own Scope/Open section left
an ambiguity uncleared: is the ask (a) ratify a cross-repo convention, (b) amend the skills that
propose paths, or (c) only record this workspace's own carve-out? Kim's answer, per the
dispatch that built this record: **all three** — (a) and (c) are the ruling itself, verbatim
below; (b) is this same change.

## Decision

**Kim's ruling, quoted verbatim (the seed text of issue #514):**

> repo/project docs (ROADMAP, PLAN, IDR, ADR, RDD, etc.) generally live under `/docs/ops/`;
> agent-specific docs under `.claude/docs/`; THIS workspace keeps everything in `.claude/docs/`
> as an explicit carve-out because its `docs` plugin name collides.

Realized as a three-rung resolution ladder in `docs:doc-writing-rules`' "Where documents live"
section (the type-contract skill owns doc locations; this ADR is the ratifying record, not a
second copy of the mechanics):

1. **Host override** — a repo's own entry file (CLAUDE.md) states its docs root explicitly;
   when present it wins outright.
2. **Portable default** — `docs/ops/` for repo/project-level records (ADR, PRD, SPEC, LLD, PLAN,
   ROADMAP, BRIEF, TICKET, TASK, IDR, RDD).
3. **Agent docs** — `.claude/docs/` for an agent's own working files, independent of whichever
   root rung 1/2 picked for repo/project records.

**This workspace's carve-out (rung 1, applied to itself):** `kimgranlund/claude-plugins` states
the override in its own CLAUDE.md — everything stays under `.claude/docs/`, including
repo/project-level records the portable default would otherwise route to `docs/ops/`. Reason:
this workspace's `docs` plugin directory already owns the bare `docs/` path; a `docs/ops/` root
here would collide with the plugin's own name.

## Consequences

- **Durable home:** the ladder lives in `docs/skills/doc-writing-rules/SKILL.md`'s location
  bullet (the type contract already owned doc locations; no new skill was minted for this).
  This ADR is the ratifying record; doc-writing-rules is the enforced, consulted surface —
  sources-flow-outward applies.
- **This workspace's override statement:** added to the workspace CLAUDE.md's Invariants
  section, one line, pointing back to this ADR.
- **Skills swept for hardcoded proposals (issue #514's named targets), amended to consult the
  ladder instead of a hardcoded root:**
  - `docs:tidy-docs` — the migration destination now resolves `<root>` via the ladder rather
    than hardcoding `docs/`.
  - `docs:check-stage` (`lifecycle_census.py`) — the typed-record census now resolves the docs
    root as `docs/ops/` if present, else `.claude/docs/` if present, else the portable default
    `docs/ops/` (presence-based degrade; the script does not parse a host CLAUDE.md's override
    text). Selftest gained a reverse-control fixture proving the `.claude/docs/` fallback still
    reads when no `docs/ops/` exists.
  - `docs:product-lifecycle-rules` and `docs:make-doc` — audited, not amended: their
    `.claude/docs/` mentions cite this workspace's own bundled source doc
    (`product-lifecycle-bible.md`) or illustrate doc-writing-rules' canonical map generically
    (`docs/adr/`, ...) — neither hardcodes a destination independent of doc-writing-rules'
    now-ladder-governed map, so no drift to fix.
  - `docs:file-bug`/`file-feature`/`file-task`/`file-leftovers` — their `docs/tickets/`
    mentions are the TICKET work-item backend's Option-A local default (ADR-0003), a separate,
    already-ruled convention from repo/project-record location; out of this ADR's scope,
    left unamended.
- **No drift found requiring a separate follow-up ticket** — the two skills that hardcoded a
  root (`tidy-docs`, `check-stage`) were fixed in this same change, per the issue's acceptance
  criterion ("any drift filed or fixed").
- **Reversible in the ordinary sense:** a future repo choosing a different override states it in
  its own CLAUDE.md at rung 1; this ADR's portable default and this workspace's carve-out both
  stand until superseded.
