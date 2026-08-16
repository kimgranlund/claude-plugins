# The build loop — seven stages, one hard gate

Source: `.claude/docs/spec/product-lifecycle-bible.md` Part 3 · "The build loop, stage by stage."
[verified] against the committed bible, v1.1.0, checked 2026-08-16.

One turn, seven stages. **Spec lock is the only hard gate** — everything else overlaps by design.
This is the general shape of a build turn; it says nothing about which stage a specific project is
in right now (see this file's Boundary section).

| # | Stage | Done when |
|---|---|---|
| 1 | **Kickoff** | Every kind of fact has a home — homes, not content. The knowledge base stands up the same day the brief is written; context is never backfilled or big-banged. |
| 2 | **Explore & prototype** | Anything explained twice is written down, and every draft hypothesis has a draft test. The prototype transmits more intent per unit of attention than prose — to humans, and doubly to machines. |
| 3 | **Spec lock** | Acceptance criteria lock, each testable, each backed by a demo or test — the only hard gate, because Verify needs a frozen reference point (bug-vs-requirement-gap is only decidable against a locked spec). From here, changes are new versions with reasons, never silent edits. |
| 4 | **Build** | Team plus AI tools build from the knowledge base; specs point at the source of truth instead of paraphrasing it. Checks run inside the build, not after it. |
| 5 | **Verify** | A DRI signs off who can explain what shipped. Every defect is called **bug** (fix in place) or **requirement gap** (update the requirement, on the record, as a new IDR version). |
| 6 | **Ship** | Boring — because deployment was rehearsed continuously. |
| 7 | **Retro — written down** | Lessons, corrections, and why-we-changed-our-minds land in the knowledge base, where the next kickoff reads them. The test: the next kickoff starts smarter than this one did. |

[verified] bible Part 3, checked 2026-08-16.

## Why Spec lock, specifically

Every other stage boundary is soft — Kickoff and Explore overlap, Build and Verify overlap. Spec
lock alone is hard because the *bug-vs-requirement-gap* call at Verify (stage 5) requires a frozen
reference point: without a lock, "is this wrong" has no fixed target to compare against, and every
disagreement becomes a renegotiation instead of a decidable check.

[verified] bible Part 3, stage 3 entry, checked 2026-08-16.

## Not waterfall

The stages overlap by design — Explore and prototype run alongside Kickoff, Build and Verify
overlap continuously. Spec lock is a gate on the *spec*, not a phase boundary that halts all other
work. The bible states this explicitly in its closing note: "not waterfall — the loops run
concurrently, stages overlap, and Spec lock is the only hard gate."

[verified] bible, closing "What this is not" note, checked 2026-08-16.

## Boundary — general doctrine only

This file names the seven stages and their done-when tests as a portable model. It does not
determine which stage a specific project's current work sits in — that reading requires live
project state (recent commits, open PRs, ticket status, ADR/IDR/RDD lock states). As of
2026-08-16, `docs:check-stage` answers that live-placement question (issue #336,
`prd-lifecycle-stage-awareness.md`) — see `SKILL.md`'s Boundaries section for the pointer.
