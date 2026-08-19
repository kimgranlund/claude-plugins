# Deliverable schema — research-leader findings record

One row per finding, six fields beyond the claim itself. Fixed by
`lld-0023-research-specialist-deliverable-plan`'s `## Data` section — this file transcribes it
verbatim as the schema `research-leader` writes to and `rubric.md` grades against; it does
not re-derive or extend it.

| Field | Type | Required | Notes |
|---|---|---|---|
| `finding` | text | yes | The claim, stated as the source states it — never paraphrased into a stronger claim than the source supports. |
| `category` | enum | yes | One of: `fact` \| `real-result` \| `unique-insight` \| `best-practice` \| `case-study` \| `practitioner-conversation`. |
| `source` | URL/citation | yes | Primary source preferred over an aggregator (mirrors `harness:fact-finder`'s own preference rule). |
| `access-date` | ISO date | yes | Dated per this repo's `save-lessons`/`fact-finder` convention. |
| `confidence` | enum | yes | `[verified]` (primary + current) \| `[inferred]` \| `[drift-prone]` (+ a one-line reason) — `fact-finder`'s own vocabulary, reused, not reinvented. |
| `actionable-note` | text | yes | What a builder does with this finding, or the literal string `none` — an honest empty beats a padded one. |
| `novelty` | enum + ref | yes | `new-to-corpus` \| `already-documented-at: <citation>` — checked against this repo's own skills/ADRs/prior research ledgers, never assumed. |

A deliverable closes with the agent's own rubric self-score (`references/rubric.md`, all four
axes) and a list of any question left unanswered — the same generate-then-self-score shape
`experiment-runner`'s typed report already has, applied to a lookup-plus-synthesis task instead
of a measured loop.
