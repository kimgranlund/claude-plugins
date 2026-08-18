# Orchestration rubric — A5: forked intake skills (`context: fork`)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

## Architecture & intended use

Skill body runs in a background fork; NO `AskUserQuestion` channel (gh#541, falsified
2026-08-17). Intended use: capture/mint durable records without polluting the host context.

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A5-R1 | No-question design: clarification happens pre-fork, or folds back via the resume command; a fork never blocks on a question it cannot ask | gh#541 | judgment |
| A5-R2 | Record-first: the fork's FIRST durable act is the record — why raw `/fork` is banned for bug work (it drops the report on exit) | `file-bug`'s own doctrine | mechanizable — `orchestration-audit`'s `a5-record-first` check: the skill body creates/writes the ticket record before any other durable side effect, checked by grep ordering of the Write/`gh issue create` call relative to other mutating calls in the skill's numbered procedure |
| A5-R3 | Resume path: every fork handback names its fold-in command (e.g. `` /file-bug #NN `` ) | — | mechanizable — grep the skill's own handback contract text for a resume-command template string |
| A5-R4 | Unasked-question surfacing: questions the fork couldn't ask are NAMED in the handback, never guessed at | — | judgment |

**Owning checker for A5:** `skill-checker` (FLOOR depth) already grades a forked intake
skill's structure; A5-R1/A5-R4 stay judgment-queued to a human or fresh-context read of an
actual fork transcript/handback.
