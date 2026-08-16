# The alignment docs — IDR · ADR · RDD (the bible's PRP), and what each is FOR

Source: `.claude/docs/spec/product-lifecycle-bible.md` Part 4 · "The alignment docs: IDR · ADR ·
PRP." [verified] against the committed bible, v1.1.0, checked 2026-08-16. This file answers *why
this three-part grammar exists and what admits a record into each type* — the GENERAL doctrine.
For which doc TYPE to actually author in a given repo, its required sections, and its frontmatter,
see the boundary note at the end of this file and `SKILL.md`'s Boundaries.

Each loop (see `three-loops.md`) keeps **one living index + one locked record type.** The records
are how decisions stay traceable and assumptions stay contestable.

| | **IDR** — Intent Decision Record | **ADR** — Architecture Decision Record | **RDD*** — Roadmap Decision Record (the bible's own term: **PRP**, Product Release Plan) |
|---|---|---|---|
| Loop | North star | Foundation | Releases |
| Unit | One testable hypothesis or outcome claim | One system decision, rejected alternatives included | One release: scope, acceptance criteria, sequencing |
| Admission test | Would two reasonable builds differ on it? | A choice someone will later ask "why" about | Could two reasonable teams ship different releases from this roadmap line? |
| Contains | Claim · why · proof reference | Decision · context · alternatives rejected and why · IDR citations | Scope · acceptance criteria (IDR-grammar, feature grain) · sequencing · citations · DRI · completion clause |
| States | Draft → locked at Spec lock → superseded-with-reason | Proposed → accepted → superseded-with-reason | Draft → locked at release commitment → shipped-and-archived, or superseded-with-reason |
| Cites upward | — | ≥1 IDR | ≥1 ADR and/or IDR |
| Living index | Product brief | Architecture overview | Roadmap — "releases lock, the roadmap breathes" |

\* **RDD is this workspace's own chosen name for the bible's PRP concept** (a local realization
decision, not the bible's own vocabulary — see the boundary note below). A different adopting
project is free to name its own realization differently, or to map PRP onto existing types instead
of minting a new one, the way this repo's own `prd-idr-framework.md` initially did before
`prd-rdd-framework.md` reversed that call — see the boundary note.

[verified] bible Part 4, table, checked 2026-08-16.

## Rules that make the records real

- Locked records are never edited in place — a change is a new version citing its predecessor and
  the evidence that forced it. The "why we changed our minds" chain is the most valuable intent
  material the org owns.
- An ADR with no IDR citation is an **orphan ADR** — a decision serving no recorded intent.
- An IDR with no downstream citations after Build is **unimplemented intent**.
- A shipped RDD/PRP left "active" is a false fact a future reader will absorb as true.

[verified] bible Part 4, "Rules that make the records real," checked 2026-08-16.

## Escalation rides the citations

A release record (RDD/PRP) repeatedly failing against the same ADR is evidence for an ADR
revision. An ADR falsified by build reality climbs to an IDR revision. The general rule: **which
record does this evidence contradict? Fix at that grain** — never patch a symptom one level away
from where the assumption actually broke. This is the alignment-record-specific instance of
`three-loops.md`'s general escalation mechanic.

[verified] bible Part 4, "Escalation rides the citations," checked 2026-08-16.

## Boundary — general doctrine vs. this repo's realization

This file states the bible's GENERAL three-part grammar and admission tests, portable to any
project. **It is not a substitute for a specific repo's own doc-type contract, and it carries no
live state about any specific repo** (RDD's own local naming choice, above, is the one deliberate
exception — it names the realization decision itself, not whether any repo has built it yet). A
concrete question about which type to author, its required sections, its frontmatter schema, or
whether a specific repo's linter will accept it is a **this-repo** question — route it to
`doc-writing-rules` (docs plugin), which maintains the live, enforced type table for whichever
repo is asking. A question about whether a given type actually exists yet in a specific repo, or
what that repo has decided about it, is a `project-docs`-and-equivalent question, not this pack's.
