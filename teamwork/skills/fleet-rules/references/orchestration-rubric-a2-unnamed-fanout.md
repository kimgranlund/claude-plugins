# Orchestration rubric — A2: unnamed synchronous fan-out (checkers / judges)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

## Architecture & intended use

Parallel `Agent` calls WITHOUT `name:`, results return synchronously to the caller. Intended
use: independent verification/judgment — generator ≠ critic.

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A2-R1 | Unnamed discipline: a fanned-out dispatch never carries `name:` | gh#154/gh#157 — naming flips to mailbox mode and strands the report | mechanizable — grep the dispatching prompt/skill for a `name:` field on a fan-out `Agent` call |
| A2-R2 | Sealed dispatches: each prompt self-contained; a no-tools judge gets its menu INLINED, never a path | `routing-judge`'s own refusal contract | judgment |
| A2-R3 | Fresh-context critic: the maker never grades its own artifact | `checking-rules` | judgment |
| A2-R4 | Failure isolation: one failed dispatch → UNMEASURED, named; siblings proceed | — | judgment |
| A2-R5 | Verbatim relay: typed handbacks relayed, not lossily paraphrased | `dispatched-agent-report-delivery.md` | judgment |
| A2-R6 | Bounded rejection: contract-violating worker output is re-dispatched ONCE then flagged UNMEASURED, never hand-patched in the lead's own context | #671 (canon text lands in `harness:agent-writing-rules`; cited here, not restated) | judgment |
| A2-R7 | Synthesis-budget discipline: merge-cheap output contracts (rows not essays), batch sizing, chunked merges past ~10 workers | #671 (canon text lands in `harness:agent-writing-rules`; cited here, not restated) | judgment |

**Owning checker for A2:** `wiring-checker` (fleet-arrangement judgment) for A2-R2/A2-R3;
`code-checker` for a fan-out that reviews a code change specifically. X-R3's mechanizable
half confirms both files exist on disk.
