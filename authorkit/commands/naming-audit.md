---
name: naming-audit
kind: command
description: Audit this estate (or a named path) against its naming manifest and report conformance with the exemption burn-down.
argument-hint: "[path-to-estate-or-plugin]"
author: kim
created: 2026-08-13
last_updated: 2026-08-13
wraps: naming-audit
requires: [naming-audit]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/validate.py *)
---

Invoke the naming-audit skill against `$ARGUMENTS` (default: the current
project). Follow that skill's procedure exactly; this wrapper adds nothing —
it exists because skills are not user-invocable and audits are demanded on
demand.
