# The corpus-resolution ladder — full detail

The `SKILL.md` body states the ladder in summary; this is the canonical full definition. **Every
brand-design procedure that needs to know what actually exists in a brand's corpus resolves
through this ladder — cite it, never restate it.**

## Why a ladder, not one mechanism

`brand-corpus` runs in more than one host: Claude Code / Cowork (a real filesystem, MCP servers
reachable), and a Claude Project (single-context chat, no filesystem, no MCP unless the Project
itself has a connector wired) — see `brand-corpus`'s own "The brand-corpus MCP (rung 1 of the
ladder)" section for the MCP's own filesystem-fallback contract. A procedure that assumes
either substrate breaks on the other host. The ladder is the one resolution order every procedure
runs, in priority order, so behavior degrades predictably instead of failing silently.

## The three rungs, in priority order

1. **MCP tools** (`list_brand_documents`, `search_brand`, `fetch_brand_section`,
   `outline_brand_document`, `get_brand_tokens`) — when a `brand-corpus` MCP is configured and
   reachable, it is the fastest, most structured read: scoped, path-guarded, and already indexed
   by layer. Query it first.
2. **Filesystem corpus layout** — no MCP, but a real filesystem is available (Claude Code /
   Cowork with no MCP wired, or the MCP unreachable): read the corpus directly with `Read`/`ls`,
   search with `Grep`, against the eight numbered layers and the naming convention in force (flat
   or folder). Every MCP tool is a convenience wrapper over exactly this — nothing it returns is
   reachable only through the MCP.
3. **Claude Project knowledge** — no MCP and no filesystem (a Claude Project's single-context
   chat): the corpus exists only as whatever the user has uploaded to the Project's knowledge as
   flat, double-hyphen-named files (`01-foundation--the-position.md`). Resolve by searching the
   Project's own uploaded knowledge for the layer/topic in question — there is no directory to
   `ls`, so orientation depends on what was actually shared into this Project (below).

**Retrieval-before-claim.** At every rung, query before asserting. Never state what a corpus
"has" or "lacks" from memory or from a prior turn — re-resolve through whichever rung is live
right now. A corpus can change between turns (a new upload, a new file on disk); a stale claim is
a defect the same as a wrong one.

## Orientation: "absent from the uploaded set" vs. "missing from the brand"

Rung 3 (Project knowledge) introduces a distinction the other two rungs don't need, because a
filesystem or a live MCP sees the corpus's actual total contents — a Project only sees what was
uploaded to IT. When a procedure (`check-brand-orientation` above all) can't find something at
rung 3, it names which of two different findings that is, never collapsing them into one
"missing":

- **Absent from the uploaded set** — the artifact plausibly exists in the brand's real corpus
  (elsewhere on disk, in a different Project, in someone's drive) but wasn't shared into THIS
  Project's knowledge. The fix is asking the user to upload it, not building it from scratch.
- **Missing from the brand** — the artifact does not exist anywhere; the brand's corpus has
  never produced it. The fix is the methodology work that produces it (`make-brand` et al.), not
  a re-upload request.

Report which one a gap is, with the reasoning: e.g. "01-foundation isn't in this Project's
knowledge — if it exists elsewhere, upload it; if it's never been written, that's the real next
step, not an upload." Guessing wrong in either direction wastes a round (asking to build what
already exists elsewhere, or asking for an upload of something that was never made).

## Consumers cite, never restate

Every brand-design procedure that resolves corpus state — `check-brand-orientation`,
`make-brand`, `make-brand-stack`, and any future one — points here for the mechanism and states
only its own consequence of it (what IT does at each rung), never re-deriving the three rungs or
the absent-vs-missing distinction inline.
