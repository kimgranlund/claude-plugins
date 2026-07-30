# Behavioral assertions — what-shipped

Checkable statements about the report. Each is verified with the skill and confirmed absent
from the un-skilled baseline in `2026-07-25-unskilled.md`.

| #   | Assertion                                                                                  | Un-skilled baseline                                                                                                                              |
| --- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| A1  | The first line states real-PR count and release-bot count **separately**.                  | Absent — baseline reported "58 PRs total" and only separated bot bumps after the reader could have been misled.                                  |
| A2  | The report names its resolved date window explicitly.                                      | Partial — baseline said "today" without resolving it to a date or naming the timezone.                                                           |
| A3  | Release-bot PRs are excluded from workstream sections, and their volume is still reported. | Achieved by hand in the baseline, by eyeballing `v0.NNNN.0` titles — a filter that breaks the moment a bot ships a differently-named PR.         |
| A4  | Every workstream section names an owner and a one-sentence purpose.                        | Partially achieved, invented ad hoc; no contract guaranteeing it next run.                                                                       |
| A5  | Linear tickets that changed state with **no** PR appear in their own section.              | **Absent entirely** — the baseline never queried Linear. ADIA2-6449 and ADIA2-6584 both moved to Done that day with no PR, and neither appeared. |

A5 is the assertion that most clearly separates skilled from un-skilled output: a PR-only
summary is structurally incapable of reporting it.
