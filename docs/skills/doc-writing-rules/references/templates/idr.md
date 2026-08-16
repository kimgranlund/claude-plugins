---
doc-type: idr
id: idr-0000
status: draft            # draft | locked | superseded
date: YYYY-MM-DD
owner: 
proof-ref:                # path/URL to the test, demo, or prototype state — fill before locking (authoring contract; not lint-gated)
supersedes: null          # idr-NNNN when replacing a prior claim, reason in ## Why
---
# IDR-0000 — <the testable hypothesis or outcome claim, stated so it could fail>

## Claim
<!-- One testable hypothesis or outcome claim — the founding belief this project (or this
     direction within it) is built on. Admission test before minting: "would two reasonable
     builds differ on it?" — if not, this isn't an IDR, it's a fact everyone already agrees on. -->

## Why
<!-- The reasoning and evidence behind the claim — context, not proof. What made this belief
     worth betting on now; what would make you doubt it. -->

## Proof
<!-- A REFERENCE only — a test, demo, or prototype path/URL that would confirm or falsify the
     claim. Never inline the evidence itself here; point at it, the same "point at the source,
     don't restate" discipline the ID spine enforces everywhere else. Fill this and proof-ref
     before flipping to `locked` — an authoring contract, same as the section's own presence
     (doc_lint's T3), not itself a separately lint-gated field. -->

<!-- LEDGER CLASS (second member alongside ADR): once status: locked, this file is append-only.
     To change the claim, write a new IDR with supersedes: this id — the hook blocks edits here.
     IDR sits upstream of ADR on the ID spine: an ADR MAY cite this record via its own
     `intent-refs:` field, answering "what belief justified this decision" (the bible's
     "orphan ADR" rule). Cardinality: plural and numbered, ADR-parallel — idr-0001 is the
     bootstrap-minted founding record, not a claim that the type itself is singular (ruling,
     issue #273, 2026-08-16: "the bible's shape wins — plural locked IDRs + ONE living index"). -->
