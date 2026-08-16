---
name: project-docs
description: >-
  Answers what THIS project (plugins) has decided, planned, queued, and specified — from the
  .claude/docs/ corpus and GitHub Issues. Use for "what are the requirements for X", "which
  tickets are open", "what's on the roadmap / the plan", "what did we decide about Y", "is there
  a spec for Z", "what's the status of issue #NN", "what's already been queued or shipped".
  Consult table → the .claude/docs/ files and `gh issue`; Grep/gh first, read the matching
  section. ANSWERS from the corpus only. NOT for authoring or editing a document (/make-doc,
  docs); NOT for capturing a new feature idea (/file-feature) or bug (/file-bug); NOT for
  building from a record (/build-feature, teamwork).
user-invocable: false
disable-model-invocation: false
---

# project-docs — this project's decision and work record

The routing surface over `.claude/docs/` and GitHub Issues — so any session can find what this
project has decided, planned, and queued without being told where to look. Answers come from the
files or `gh issue`/`gh pr` output, cited by path or issue number; a question the corpus doesn't
answer is reported as absent, never guessed.

| Ask | Look in |
|---|---|
| How we build — the three loops, IDR/ADR/PRP doctrine, knowledge-base habits, the glossary | `.claude/docs/spec/product-lifecycle-bible.md` (the canonical reference; on disagreement the internal doctrine corpus wins, per its own header) |
| Requirements, exact behavior, acceptance criteria | `.claude/docs/spec/` (spec-* files; the dir also holds the lifecycle bible above) |
| A ratified decision and its alternatives | `.claude/docs/adr/` (ADR-*, accepted = append-only) |
| What's queued, in flight, or done | GitHub Issues (`gh issue list`; bare labels `bug`/`feature`/`task` + `size:small`/`size:big` — this repo's ADR-0002 git-native ticket backend, NOT `docs/tickets/` — see #267 for a live specimen of the scheme) |
| A system decomposition or partition manifest | `.claude/docs/decompositions/` |
| A subagent's handback / handoff record | `.claude/docs/handoff/` |
| A founding hypothesis or testable claim this project is built on | `.claude/docs/idr/` (`idr-*`, `locked` = append-only; not yet present in this repo as of 2026-08-16 — the type ships in this same change, no instance minted here) |
| PRD (why/what) | `.claude/docs/prd/` (first instance 2026-08-15: `prd-idr-framework.md`, the IDR scoping) |
| LLD (how) | `.claude/docs/lld/` (lld-0001…0004 as of 2026-08-15) |
| PLAN, ROADMAP (Now/Next/Later), TASK | Not present in this repo as of 2026-08-15 — a request for one of these types routes to `/make-doc`, never assumed absent-forever |

(This repo's docs directory is `.claude/docs/`, not `docs/` — a plugin-workspace convention,
recorded here so a future session doesn't waste a sweep looking in the wrong place. Before
answering "absent" on any row, sweep for near-miss locations: misnamed dirs, loose files
(`NOTES.md`, `DECISIONS.md`), doc-shaped README sections. A hit → answer with the real location,
marked non-canonical.)

## Consult procedure

1. Classify the ask against the table; Grep the corpus for the feature's nouns or the SPEC-/
   ADR-id first — the files are records, not linear reads. For ticket status, `gh issue view <n>`
   or `gh issue list --search <nouns>` — GitHub Issues ARE the ticket record here, not a file.
2. Answer with **the claim + the file path or issue URL (+ the record's status/labels)**. An open
   issue and a closed one answer "is X built?" oppositely.
3. Cross-references between records use ids where they exist (an ADR's own `supersedes:` field,
   an Issue linking a PR) — follow them rather than assuming one file/issue is complete.
4. Route all making: a new idea → `/file-feature`; a bug → `/file-bug`; building a queued record →
   `/build-feature`; authoring or revising any document → `/make-doc` — otherwise name the record
   that would be touched and hand back to the user.
