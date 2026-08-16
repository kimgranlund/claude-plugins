---
name: repo-audit
kind: command
description: Run the full audit battery over this repo — Phase-0-style discover/scope-confirm, fan out all five authorkit instruments (naming/bloat/attention/pattern/doctrine, batched via estate-audit-agent), the harness cross-plugin axes where installed, and one verdict-first 🟢/🟡/🔴 roll-up per estate per axis. Reports only, never mutates.
argument-hint: "[target: estate-root, plugin-set, or member list — blank scans the current project]"
author: kim
created: 2026-08-16
last_updated: 2026-08-16
wraps: repo-audit
requires: [repo-audit]
mutates: false
confirm: not-required
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Agent
  - AskUserQuestion
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
  - Bash(python3 */scripts/rent.py *)
  - Bash(python3 */scripts/collide.py *)
  - Bash(python3 */scripts/usage.py *)
  - Bash(python3 */scripts/trend.py *)
  - Bash(python3 */scripts/scan.py *)
  - Bash(python3 */scripts/sweep.py *)
---

Invoke the repo-audit skill against `$ARGUMENTS` (default: the current project). Follow that
skill's procedure exactly; this wrapper adds nothing except the on-demand, user-typed entry
point — the skill itself is not user-invocable.

`mutates: false` / `confirm: not-required` is this command's own contract: every composed
instrument is read-only, and this skill's own `disallowed-tools: [Write, Edit, NotebookEdit]`
plus a `Bash` allowlist naming only read-only audit scripts back that up — nothing here ever
needs a mutation gate. The one `AskUserQuestion` round in Phase 0 is a SCOPE question, not a
mutation confirm, and degrades to a named skip under no live user rather than blocking the
report.
