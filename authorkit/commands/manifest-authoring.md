---
name: manifest-authoring
kind: command
description: Seed or edit a target estate's naming.manifest.json — lexicon membership proposals, ObjectVocab registrations with the anti-ambiguity gate, AuthorRegistry, and exemptions enumeration.
argument-hint: "[path-to-estate-or-plugin]"
author: kim
created: 2026-08-14
last_updated: 2026-08-14
wraps: manifest-authoring
requires: [manifest-authoring]
mutates: true
confirm: required
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit(**/naming.manifest.json)
  - Write(**/naming.manifest.json)
---

Invoke the manifest-authoring skill against `$ARGUMENTS` (default: the current
project). Follow that skill's procedure exactly; this wrapper adds nothing —
it exists because skills are not user-invocable and manifest seeding/editing
is a deliberate, user-initiated act demanded on demand.

Before writing `naming.manifest.json`, present the proposed change (seed
contents, the vocab/lexicon entry, or the exemption(s) to enumerate/retire)
and wait for explicit confirmation — `confirm: required` is the contract, not
a suggestion. Every edit still ends with the skill's own validator run; a
manifest edit that creates new errors is reverted, not shipped.
