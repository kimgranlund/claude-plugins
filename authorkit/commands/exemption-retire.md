---
name: exemption-retire
kind: command
description: Retire one exemption opportunistically — chain rename-planning, confirmation, rename-execute, and the manifest shrink for an artifact that is being touched anyway.
argument-hint: "[exempt-name]"
author: kim
created: 2026-08-13
last_updated: 2026-08-13
requires: [rename-planning, naming-audit, manifest-authoring]
mutates: false
confirm: none
allowed-tools:
  - Read
  - Glob
  - Grep
---

Thin orchestration; owns no writes. Verify `$ARGUMENTS` is in the estate's
exemptions array (else stop — nothing to retire), invoke rename-planning for
it, then hand the plan to /rename-execute, whose own confirm gate governs
the mutation. The manifest shrink happens inside rename-execute's atomic
apply. This command exists so the burn-down is a one-step habit instead of a
four-step chore.
