---
name: product-lifecycle-rules
description: >-
  General doctrine for how products get built: three nested loops (North star -> Foundation ->
  Releases), the seven-stage build loop (Kickoff..Spec lock..Verify..Retro; Spec lock the only
  hard gate), the IDR/ADR/RDD alignment doc grammar, knowledge-base maturation, habits, named
  anti-patterns. Portable -- orients ANY project. Use for "what's an IDR/ADR/RDD for", "why Spec
  lock matters", "how a knowledge base matures", "the relearn rate", "admission test, ADR vs
  IDR". NOT which doc type/sections/frontmatter to use here (doc-writing-rules); NOT what THIS
  repo decided/queued (project-docs); NOT this project's live stage (docs:check-stage); NOT /goal or /loop
  mechanics (loop-rules).
disable-model-invocation: false
user-invocable: false
---

# product-lifecycle-rules — the general doctrine of how products get built

The canonical home (per this workspace's own sources-flow-outward invariant) for the doctrine
`.claude/docs/spec/product-lifecycle-bible.md` names: three nested loops, one seven-stage build
turn, the IDR/ADR/RDD alignment doc grammar, a knowledge base that matures rather than gets
authored, seven habits, and named anti-patterns. **The bible file is now a dated snapshot pointing
here** (see its own header) — this skill and its `references/` corpus are the operating surface;
consult the bible directly only for historical provenance or the exact original prose.

This pack answers **general, portable** doctrine — "how do teams build software, generally" — not
what any one project has actually decided. Three fences keep it that way (see Boundaries).

## Consult table

| Ask | Load |
|---|---|
| The three nested loops, cadence, escalation, version numbering, the POC boundary | `references/three-loops.md` |
| The seven-stage build turn, why Spec lock is the only hard gate | `references/build-loop-stages.md` |
| What an IDR/ADR/RDD (the bible's PRP) is *for*, admission tests, citation direction, escalation-rides-the-citations | `references/alignment-record-types.md` |
| How a knowledge base matures (born → harvest → amend → prune), the grounding doc, the seven habits, what gets measured | `references/knowledge-base-habits.md` |
| Named anti-patterns, and the glossary (IDR/ADR/PRP/DRI/pivot/relearn rate, etc.) | `references/anti-patterns-glossary.md` |

Five files, all reachable 1:1 from this table — no separate INDEX (pack-writing-rules' 2026-07-09
ruling: a flat corpus at or under ~7 files makes the table itself the retrieval map).

## Consult procedure

1. Classify the ask against the table above; Grep the matching file for the term first on a long
   or multi-topic ask, then Read the matching section — this is a lookup corpus, not a linear
   read.
2. Answer with the **claim + the file it came from** (e.g. "`references/alignment-record-types.md`: an
   ADR with no IDR citation is an orphan ADR"). Every reference file cites the bible by Part
   number — trace back to `.claude/docs/spec/product-lifecycle-bible.md` for the full original
   prose if the fragment doesn't settle the question.
3. Check the Boundaries below before answering — a question that turned into "which type do I
   file here" or "what did we decide" crossed out of this pack's territory mid-answer; route the
   rest to the owning skill rather than guessing.

**Worked example — a cold session orienting on a new repo:**
*"What's the difference between an IDR and an ADR, and which one do I write for this decision?"*
splits into two asks. The first — what's the difference — is this pack's: load
`references/alignment-record-types.md` → IDR is a testable belief about what's true, admitted by "would two
reasonable builds differ on it?"; ADR is a HOW choice, admitted by "a choice someone will later ask
why about" — IDR precedes ADR and ADR **may** cite it upward. The second — which one to write
*here*, in what section shape, with what frontmatter — crosses the first fence below: that's
`doc-writing-rules`' live type-contract table, not this pack's; hand it off rather than guessing at
this repo's own schema.

## Boundaries

- **NOT which doc type to use, its sections, or frontmatter.** `doc-writing-rules` (docs plugin)
  owns the live, `doc_lint`-enforced type contract for whichever repo is asking — including
  whether a type this pack names (like RDD) is actually built yet there. This pack explains what a
  type is *for* in general; `doc-writing-rules` explains what to *file*.
- **NOT what THIS repo has decided, queued, or shipped.** `project-docs` answers from the live
  `.claude/docs/` tree and GitHub Issues. This pack carries no live state about any specific repo.
- **NOT what lifecycle stage THIS project is in right now.** Determining a live project's current
  position in the loops/stages this pack describes needs a project-status reading — as of
  2026-08-16, `docs:check-stage` answers it (issue #336, `prd-lifecycle-stage-awareness.md`,
  closing the forward gap issue #321 opened). If asked, hand off to `check-stage` rather than
  guessing live placement from context.
- **NOT the agentic continuation-loop mechanics** (`/goal`, `/loop`, Stop hooks, autonomy caps) —
  a different, unrelated "loop": teamwork's `loop-rules` owns that word for a different concept
  entirely. This pack's "loop" is always North star/Foundation/Releases or a build turn.
- **NOT authoring or editing the source doctrine.** A correction to the doctrine itself is a
  `save-lessons`/`make-pack` question against this skill, never an inline restatement here.

## Provenance

Realizes `.claude/docs/spec/product-lifecycle-bible.md` v1.1.0 as a portable knowledge pack per
`pack-writing-rules` (issue #320). Canon decision: this skill is now the operating source within
this workspace (CLAUDE.md's sources-flow-outward invariant); the bible file is a dated snapshot —
see its own header for the pointer and for the outer-tier "internal doctrine corpus" it still
traces to, unaffected by this ruling. Owning plugin: `docs` — the plugin already citing this
doctrine as concept authority for its own IDR (`doc-writing-rules`, `prd-idr-framework.md`) and RDD
(`prd-rdd-framework.md`) types, and already indexing it from `project-docs`; checked against
`plan-plugin-split`'s anti-matrix rule, no competing charter claims this job.
