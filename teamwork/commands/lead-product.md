---
name: lead-product
kind: command
description: Makes this host session a dedicated product seat, adopting the product-leader agent's own contract directly.
argument-hint: "[charter — the loop/gate/IDR/RDD work needing the product seat]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: leading-product
requires: [leading-product]
mutates: true
confirm: none
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash
  - Skill
  - Agent
---

Invoke the `leading-product` skill against `$ARGUMENTS` (the charter). This command is the
human-typed entry point only; `leading-product` carries the full procedure. NOT the dispatched
sibling seat (`product-leader`, Agent tool); NOT authoring PRD/SPEC/LLD (`/lead-planning`, one
loop-tier down); NOT enforcing the spec-lock gate at dispatch time (`/lead-team`, which reads this
seat's gate); NOT a one-off lifecycle-position report (`docs:check-stage` directly).
