---
name: estate-audit
kind: skill
description: >
  The estate-audit family index — naming-audit, bloat-audit, attention-audit,
  pattern-audit, doctrine-audit, and orchestration-audit are six read-only
  diagnostic instruments sharing one batch-sweep mechanic, consolidated
  behind one parameterized agent (estate-audit-agent, issue #293/#272).
  Use when the user asks which audit instrument fits an ask, or how to
  name the batch agent's `instrument` parameter. NOT for running any one
  sweep directly — reach the owning instrument skill (naming-audit/
  bloat-audit/attention-audit/pattern-audit/doctrine-audit/
  orchestration-audit) for that; this skill has no procedure of its own.
author: kim
created: 2026-08-15
last_updated: 2026-08-18
disable-model-invocation: false
user-invocable: false
requires: [naming-audit, bloat-audit, attention-audit, pattern-audit, doctrine-audit, orchestration-audit]
---

# estate-audit

Reference index. This skill has no procedure — it names the family and
routes to the instrument that owns the actual sweep.

## The six instruments

| Instrument value | Owning skill | Script | Axis |
|---|---|---|---|
| `naming` | `naming-audit` | `validate.py` | grammar/frontmatter conformance |
| `bloat` | `bloat-audit` | `measure.py` | busy-work / ceremony |
| `attention` | `attention-audit` | `rent.py`/`collide.py`/`usage.py`/`trend.py` | menu rent, description collisions, usage |
| `pattern` | `pattern-audit` | `scan.py` | caller-supplied pattern/instruction sweep |
| `doctrine` | `doctrine-audit` | `sweep.py` | canon-to-dependent doctrine-drift conformance |
| `orchestration` | `orchestration-audit` | `audit.py` | orchestration-archetype rubric conformance (A1..A8), mechanizable slice only |

Each instrument's own skill owns its procedure, judgment criteria, and
report shape — this index restates none of it. Run one directly for a
single estate; dispatch `agents/estate-audit-agent` (Agent tool) with the
`instrument` parameter for a batch sweep across more than ~3 estates or
any single estate over ~40 members — the same threshold `overhaul-execute`
uses for its own Phase 1 MEASURE step.

## Failure branches

- Asked to run a sweep directly rather than choose an instrument → route to
  the owning skill; this index never runs `validate.py`/`measure.py`/
  `rent.py`/`scan.py`/`sweep.py`/`audit.py` itself.
