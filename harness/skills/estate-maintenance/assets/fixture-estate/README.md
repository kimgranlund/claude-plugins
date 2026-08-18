# fixture-estate — what seeds which detector

A seeded mini-estate, synthetic end to end, consumed only by `collect.py selftest` and
`detect.py selftest` (AC-2). Nothing under this directory describes a real project, and nothing
outside `estate-maintenance`'s own scripts reads it.

| File / dir | Seeds | What it proves |
|---|---|---|
| `memory/feedback-absolute-paths-{1,2,3}.md` | **D1** (repeated user nudge) | Three `type: feedback` entries on one topic (absolute vs. relative Bash paths), Jaccard-clustered on name+description tokens; entries 2 and 3 also match the recurrence lexicon (`third time`, `repeatedly`) on their own |
| `memory/fact-typescale-canon.md` | **D1 negative control** | `type: fact`, no shared vocabulary with the trio above — must NOT cluster in |
| `memory/MEMORY.md` | D4 census (memory index lines) | The index file `collect.py`'s memory collector also line-counts |
| `attention-trend.csv` | **D3** (`rent-growth`, `instrument-half-blind`) | One plugin (`demo-plugin`), 4 append-ordered rows, `routable_chars` 10000→10800 (+8%, ≥3 rows, ≥5% growth) and `dead`/`stolen`/`leaked` = `absent` in all 4 rows |
| `recurrence-trend.csv` | **D3** (`series-not-firing`, `ratchet-unadopted`) | Exactly 1 row, dated 2026-08-18, `seeded_classes=0` — mirrors the real recurrence-trend.csv's own shape at authoring time |
| `issues.json` | **D2** (`re-filed`) + negative control | #501 (closed 2026-06-05) and #588 (opened 2026-07-01, near-duplicate title, Jaccard ≥ 0.5) form a re-filed pair; #512 (dark mode toggle) shares no vocabulary — the same-window/no-match control |
| `CLAUDE.md` | **D4** (`entry-file > 200 lines`) | Exactly 230 lines (padded numbered block, named inline as padding) |
| `.claude/rules/demo-widget-shipping.md`, `.claude/rules/demo-fixture-retirement.md` | **D4** (`rules_count`, `rules_total_lines`) | Two short synthetic rule files |

No `.claude/ops/adr-queue.json`, `.claude/docs/adr/`, or `.claude/docs/idr/` are seeded here
deliberately — `collect.py`'s `decisions` collector must report those as absent
(`present: false`, never an exception) against this fixture, proving Resolution b's
never-an-exception predicate on the decisions side too.
