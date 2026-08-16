# Anti-patterns, named — and the glossary

Source: `.claude/docs/spec/product-lifecycle-bible.md` Part 8 ("Anti-patterns, named"), Part 9
("Glossary"). [verified] against the committed bible, v1.1.0, checked 2026-08-16.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| **Roadmap as contract** | The roadmap is the living index over release records; committing the index freezes learning. Releases lock instead. |
| **Renegotiating a locked release record without a version** | Silent renegotiation destroys the record's meaning. |
| **Backfilled documentation** | Context written after the fact is reconstruction from whoever still remembers; capture happens during Explore. |
| **POC ossification** | Shipping the prototype codebase into production skips the rebuild-to-the-contract step; inherit the knowledge, not the code (`three-loops.md`'s POC boundary). |
| **The growing grounding doc** | Per-incident growth means lessons aren't routing to skills and checks. |
| **Restated facts** | Every copy is a future contradiction. |
| **Docs for docs' sake** | Fails the pruning habit; documentation is judged by behavior change, not coverage. |
| **The big-bang knowledge base** | Authoring "robust context" upfront produces speculation, not knowledge — robustness is grown through the harvest/amend/prune arc, and a day-0 library is a day-0 drift farm. |

[verified] bible Part 8, checked 2026-08-16.

## Glossary

- **IDR** — Intent Decision Record: one testable hypothesis with a changelog.
- **ADR** — Architecture Decision Record.
- **PRP** — Product Release Plan (a launch plan); this workspace realizes it as **RDD** (Roadmap
  Decision Record) — see `alignment-record-types.md`'s boundary note.
- **DRI** — Directly Responsible Individual: the named human who can explain what shipped.
- **Acceptance criteria** — the testable conditions locked at Spec lock; collectively, the rubric.
- **Pivot** — a North-star turn: a hypothesis superseded on evidence, on the record.
- **Knowledge base / source of truth** — the project's captured context: skills, records,
  glossary, domain layer.
- **Grounding doc** — the one-screen entry point that orients a cold executor.
- **Harvest** — returning lessons to the knowledge base as a scheduled step, not a hope.
- **Relearn rate** — the score: how often we re-learn what we already knew.

[verified] bible Part 9, checked 2026-08-16.

## Boundary

Named anti-patterns and glossary terms are general doctrine — recognizing the *shape* of these
failures anywhere. This file does not audit a specific repo for whether one of these anti-patterns
is currently live in it (a `project-docs`-and-beyond reading, requiring inspection of that repo's
actual history and tree).
