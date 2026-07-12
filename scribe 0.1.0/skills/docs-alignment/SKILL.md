---
name: docs-alignment
description: >-
  Align an existing repo's scattered documents to the canonical docs/ layout — inventory what
  document reality the repo actually has (rfcs/, design-docs/, NOTES.md, spec-shaped README
  sections, near-miss dirs like docs/specs/), classify each artifact by the question it answers,
  propose ONE batched migration plan, and on approval execute it with git mv (history preserved),
  minimal frontmatter, link repair, and the project-docs index installed at the end. Run
  /docs-alignment [optional: a subtree to scope the sweep]. Human-timed; one approval gate for the
  whole plan; migration only — content is never rewritten. NOT for authoring a document
  (doc-forge); NOT for reviewing content quality (doc-review); NOT for capturing a new idea or
  bug (/feature, /bug-report); NOT for repos with no documents (the index bootstrap alone is
  /feature's Phase 6); NOT for whole-harness drift — entry files, dead
  automation, corpus liveness (repo-alignment, forge — it decides a repo's grammar; this
  command executes the canonical-map case).
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional subtree to scope the sweep]"
---

# docs-alignment — migrate the corpus, never the content

Turns a repo's scattered document reality into the canonical layout the tooling and the
project-docs index assume — `doc-authoring-standards`' directory-per-type map is the single
target; this command owns getting an EXISTING corpus there. Migration only: files move and gain
frontmatter; **prose is never rewritten** — a document's content quality is doc-review's
question, on a later day. Seed: `$ARGUMENTS` (a subtree scopes the sweep; empty = whole repo).

## Phase 1 — Inventory: what document reality exists

Sweep three surfaces and classify every hit by the question it answers (the standards' type
test: why→PRD · what exactly→SPEC · how internally→LLD · ratified fork→ADR · sequence→PLAN ·
horizons→ROADMAP · work item→TICKET/TASK):

1. **Canonical dirs** — already-right content stays put; note records missing frontmatter.
2. **Near-miss locations** — `docs/specs/`-style misnames, `rfcs/`, `design/`, `design-docs/`,
   `adrs/`, `doc/`, `notes/`.
3. **Loose files** — `NOTES.md`, `TODO.md`, `DECISIONS.md`, `ARCHITECTURE.md` (whole-file
   moves), and doc-shaped README sections — the one EXTRACTION case: offered, and marked in the
   plan as creating a new file rather than moving one.

Nothing found → report the repo is already clean (or empty), offer only the index bootstrap,
stop. The inventory is a deliverable in itself: a rejected plan still leaves the user knowing
what they have and where.

## Phase 2 — Plan: one table, one gate

Build the migration manifest — per artifact: source → canonical destination
(`docs/<type>/<type>-<number-or-date>-<slug>.md` per the standards; ticket exception:
`docs/tickets/tkt-…`) · frontmatter to add (`doc-type`, `id` — derived from the minted
filename — and `status`; nothing more: doc_lint's T1 requires exactly these three) · links that
will need repair. Classification genuinely
ambiguous → ONE batched AskUserQuestion round (≤4 questions, concrete options); ambiguity beyond
that round lands in an **unresolved bucket — left in place and listed**, never force-classified.
The plan's last line is always "install/update the project-docs index skill."

Present the whole table for ONE approval (the working tree's state stated on it — pre-existing
uncommitted changes are flagged so the migration's diff stays separable). Approved → Phase 3.
Rejected → write nothing; the inventory is the report.

## Phase 3 — Execute (approved plan only, nothing beyond it)

1. `git mv` every approved move — history preserved; extractions (README sections) create the
   new file and replace the section with a one-line pointer to it.
2. Add the minimal frontmatter where records lack it. **Exception: an accepted ADR is
   append-only — move it untouched; needed frontmatter is noted in the report, not added.**
3. Repair inbound links: grep by BASENAME first (relative links — `../rfcs/foo.md`, bare
   `foo.md` — never match a full-path sweep), then the full old path as the confirming pass;
   rewrite references; a reference too ambiguous to rewrite mechanically is listed, not guessed.
4. `doc_lint.py` on every migrated record — repairs limited to frontmatter. A NAMING failure
   means the Phase 2 manifest was wrong — report it, never rename past the approval gate; a
   record whose CONTENT fails lint is recorded as a doc-review candidate, not rewritten here.
5. Install or update `.claude/skills/project-docs/SKILL.md` from /feature's template (its
   consult table now true of this repo).
6. Report: moves made · extractions (new files — git history does not follow a section out of
   a README) · frontmatter added · links repaired · the unresolved bucket · lint results ·
   doc-review candidates. **Committing is the user's** — the changes sit staged-ready
   in the working tree with a suggested message; this command never commits.

## Failure branches

- Plan rejected → inventory report only; zero writes.
- A basename or old-path grep still hits after repair → fix before reporting; a false "links
  repaired" is the command's own failure mode.
- Accepted ADR needing more than a move → note and skip (the append-only class outranks tidiness).
- `doc_lint` content failures → doc-review candidates list, never in-place rewrites.
- The ask was really "write me a doc" or "review this doc" → doc-forge / doc-review.

Done when every approved move landed via `git mv`, no repo reference to an old path survives,
migrated frontmatter lints clean, the index skill matches the new layout, and the unresolved
bucket + doc-review candidates are reported. NOT done if any file moved without plan approval,
any prose was rewritten, or the report claims a repair a grep would refute.
