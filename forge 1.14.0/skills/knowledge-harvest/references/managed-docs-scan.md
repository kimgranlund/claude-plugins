# Managed-docs scan — default location, document-type allowlist, override

Phase 1's third detector reads a project's own curated docs corpus as a second candidate source
and as a calibration set for the frequency/impact detectors. This file names the default so the
scan works out of the box in this workspace's own projects, and how a different project overrides
it — the mechanism stays portable, the default is not a hardcoded path.

## Default location

Both projects this skill has been designed against already converge on the same root:
`.claude/docs/` (agent-ui: `.claude/docs/{adr,tickets,references,prd,spec,lld}`; nonoun-plugins:
`.claude/docs/adr` so far). Default to `<project-root>/.claude/docs/` when present. If it does not
exist, the managed-docs detector simply has nothing to scan — this is not an error, just an absent
source; detectors 1 and 2 still work from live conversation alone.

## Default document-type allowlist

Only these carry enough pre-vetting to count as a candidate on sight (no frequency threshold
needed — they are already ratified/closed, by construction):

- An ADR's **Decision** section (a ratified architectural choice).
- A ticket's **Findings** section, once its status is `done` (an open ticket's findings are
  still moving; do not harvest from work in flight).
- A SPEC or PRD's ratified clause (a section the document's own status marks accepted, not draft).
- An existing `references/*.md` file's own claims, when scanning for a SECOND project's corpus
  that doesn't yet have an equivalent entry (cross-project gap-filling, not re-harvesting the same
  project's own reference back into itself).

Do not treat an entire docs folder as fair game — a PRD's open questions, a draft SPEC section, or
an ADR's "Context"/"Alternatives considered" prose are exploratory, not ratified; harvesting from
them captures noise, not knowledge.

## Override

A project that wants a different root or allowlist states it in its own `CLAUDE.md` or an
equivalent standing-instructions file — this skill reads that override the same way it would read
any other project convention, rather than requiring a new config file format. Absent an override,
the default above applies.

## What this file does NOT cover

Placement (which skill/reference an admitted candidate lands in) is `placement-heuristics.md`. The
frequency/impact detector logic itself is Phase 1 of `SKILL.md`, not repeated here.
