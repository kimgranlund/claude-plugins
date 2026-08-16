---
doc-type: rdd
id: rdd-0000
status: draft                   # draft | locked | superseded
date: YYYY-MM-DD
owner: 
dri:                            # the named accountable human (bible: "a DRI can explain what
                                 # shipped") — distinct from owner (who authored the record);
                                 # required non-empty at `locked` (T7, FAIL)
decision-refs:                  # comma/space-separated adr-NNNN / idr-NNNN ids, ONE line —
                                 # parse_frontmatter is a scalar parser, no YAML block lists;
                                 # e.g. `decision-refs: adr-0002, idr-0001` — required non-empty
                                 # at `locked` (T7, FAIL)
supersedes: null                 # rdd-NNNN when replacing a prior release commitment
---
# RDD-0000 — <the release commitment, stated as what ships>

## Scope
<!-- What this release commits to shipping — feature grain. Admission test before minting:
     "could two reasonable teams ship different releases from this roadmap line?" — if not, the
     line doesn't earn its own RDD. -->

## Acceptance
<!-- Criteria in IDR-grammar — each phrased as a testable claim that could fail, never a task
     checklist. Mirrors IDR's own `## Claim` discipline, applied per acceptance line rather than
     once for the whole document. -->

## Sequencing
<!-- Ordering/dependencies across the bundled TICKETs — plain prose links. TICKET is a work item,
     not an ID-spine citee, so this stays outside `decision-refs:`. -->

## Completion
<!-- The completion clause: what "shipped-and-archived" or "superseded-with-reason" concretely
     means for THIS release, and where the evidence lives — mirrors IDR's `## Proof` discipline
     (a reference, never inlined content). -->

<!-- LEDGER CLASS (third member alongside ADR/IDR): once status: locked, this file is append-only.
     To change the commitment, write a new RDD with supersedes: this id — the hook blocks edits
     here. `shipped-and-archived` is NOT a fourth status value: completion tracking belongs to the
     roadmap's own living index ("releases lock, the roadmap breathes") — a shipped RDD stays
     `locked` forever, byte-identical; a renegotiated commitment gets a NEW RDD citing
     `supersedes:`, exactly the ADR/IDR pattern. RDD sits downstream of ADR/IDR on the ID spine:
     it CITES `≥1` via `decision-refs:`, never the reverse. Cardinality: plural and numbered,
     ADR/IDR-parallel — rdd-0001 is the first release commitment, not a claim that the type itself
     is singular. -->
