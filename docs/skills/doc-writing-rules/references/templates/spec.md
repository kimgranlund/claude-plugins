---
doc-type: spec
id: spec-<slug>
status: draft           # draft | approved | superseded
version: 0.1.0
date: YYYY-MM-DD
owner: 
prd: prd-<slug>         # the intent this contracts
---
# SPEC — <the contract, one line>

## Requirements
<!-- Every requirement a testable statement with an ID:
     REQ-001: p95 latency under 200ms at 1k RPS.
     "Fast" is not a requirement. -->

## Non-goals
<!-- The scope fence. For agent consumers, the most valuable section here. -->

## Examples
<!-- Worked input/output pairs. Mark each NORMATIVE or ILLUSTRATIVE — agents treat every
     example as a contract unless told otherwise. -->

## Acceptance
<!-- One criterion per requirement, same IDs (AC-001 ↔ REQ-001). Authored WITH the spec,
     never after. A requirement with no criterion is unverifiable. -->

## Agent verification
<!-- How the coding agent autonomously exercises this system and checks each Acceptance
     criterion, without a human in the loop: which layer it asserts at (JSON payload / API /
     browser / human), with what harness or fixtures — one line per AC-ID where the layer isn't
     obvious. A criterion that genuinely needs a human is named here as an explicit exception,
     never silently left unverifiable. See docs' agent-harness-rules for how to choose the
     layer and design the harness. -->
