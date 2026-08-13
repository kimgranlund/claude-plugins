---
name: manifest-authoring
kind: skill
description: >
  Seed or edit a target estate's naming.manifest.json — lexicon membership
  proposals, ObjectVocab registrations with the anti-ambiguity gate,
  AuthorRegistry, and exemptions enumeration. Use when an estate has no
  manifest, when a new vocabulary token is needed, or when the exemptions
  array must be enumerated or retired from.
author: kim
created: 2026-08-13
last_updated: 2026-08-13
requires: [naming-conventions]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit(**/naming.manifest.json)
  - Write(**/naming.manifest.json)
---

# manifest-authoring

The manifest belongs to the TARGET estate, never to authorkit — lexicons,
vocab, and exemptions are estate-local facts. This skill writes exactly one
file per estate.

## Procedure

1. **Seeding:** copy naming-conventions/references/MANIFEST-TEMPLATE.json to
   the estate root (or .claude/). Populate author_registry from the estate's
   actual committers. Enumerate exemptions from a first naming-audit run —
   every current violation goes in verbatim; the array only shrinks after.
2. **Vocab registration:** before adding an ObjectVocab entry, run the
   anti-ambiguity gate — the new token must not make longest-match resolution
   ambiguous against any existing multi-token entry. Record canonical,
   plural, banned aliases in one registration.
3. **Lexicon changes:** VerbLex/ProcessLex/RoleLex are closed; propose the
   change, state the disjointness check result (VerbLex ∩ ProcessLex must
   stay empty), and land it only as a reviewed edit.
4. **Exemption retirement:** remove entries only when the corresponding
   rename has landed and the validator passes — never speculatively.
5. Every edit ends by running the validator against the estate; a manifest
   edit that creates new errors is reverted, not shipped.
