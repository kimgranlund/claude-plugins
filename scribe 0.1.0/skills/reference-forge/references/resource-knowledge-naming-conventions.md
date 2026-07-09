# Resource & Knowledge Naming Conventions

**Best practices for naming knowledge files, references, records, and indexes in agent-consumed corpora**

Companion documents: *Skill Naming Conventions*, *Agent Naming Conventions*.

---

## 0. What a Knowledge Name Has To Do

Knowledge files differ from skills and agents in one decisive way: they are **retrieval targets, not invocation targets**. Nobody calls `@oklch-ramp-construction` — the file is found by grep, by `ls`, by an INDEX lookup, or by model attention scanning a directory listing. The name is therefore optimized for a different consumer: a search process (human, script, or model) with a query in hand.

Four constraints:

1. **The filesystem is often the query interface.** Agents without index tooling navigate by `ls` and `grep`. Names must sort meaningfully and match on the tokens queries actually contain.
2. **Mutation semantics drive name shape.** A file that is continuously updated and a file that is written once and appended to the record are different types, and their names should be structurally distinguishable at a glance.
3. **Stable identity in the name; volatile metadata in frontmatter** — with one principled exception (§2) where a sortable facet *is* the access pattern.
4. **Retrieval surface over prose.** These files feed both grep and model attention. Distinctive tokens front-loaded, stop-words banned, one concept per file.

---

## 1. Type the Files by Mutation Semantics First

Before choosing any name, classify the file. The classification determines the name grammar:

```
evergreen reference   — continuously true, updated in place
                        references/{axis}/{topic}.md
                        no date in name; `updated:` in frontmatter

append-only record    — true as of a moment, never edited after
                        decisions/YYYY-MM-DD--{slug}.md
                        adr/NNNN-{slug}.md
                        temporal/sequence key IS the name prefix

index                 — enumeration of a directory's contents and axes
                        INDEX.md   (one per directory; sorts first)

working / ephemeral   — drafts, scratch, generated intermediates
                        _scratch/ or /tmp — segregated by location,
                        never by suffixing "-draft" onto a real name
```

This split is the document's central rule. Most knowledge-corpus naming failures are type errors: a decision log named like a reference (`decisions/caching.md` — which decision? when? superseded?), or a reference named like a record (`references/2025-11-oklch-notes.md` — is this still true? the date says "maybe not" and the name can't be updated without breaking links).

---

## 2. Evergreen References

```
references/{axis}/{topic}.md

axis  := closed enum, declared in the root INDEX.md
topic := 2–4 kebab-case content tokens; the grep surface
```

**No dates in names.** For a reference, the date is metadata — it answers "how fresh," not "which file." It lives in frontmatter (`updated: 2026-06-14`) where it can change without breaking every inbound link. A date in a reference filename is a promise of staleness: it will be wrong within a quarter and un-renameable forever.

**Axes are a closed enumeration** with the root `INDEX.md` as the source of truth — the same closed-set discipline as skill suffixes and agent role families. `references/color-science-materials/`, `references/component-contracts/`, `references/clinical-coding/`. Creating an axis is a manifest edit, not a filing improvisation; the moment `references/misc/` exists, the axis system is dead.

**Topic naming is retrieval engineering:**

- **One concept per file.** A file answering three questions matches three queries poorly. Split until each name states exactly what its file settles: `oklch-ramp-construction.md`, `oklch-gamut-mapping.md` — not `oklch-notes.md`.
- **Front-load the distinctive token.** `oklch-ramp-construction.md` over `constructing-ramps-in-oklch.md`. In a sorted listing, the discriminating token should be the first thing the eye and the model hit.
- **Ban stop-words and meta-words.** `notes-on-`, `thoughts-about-`, `how-we-`, `misc-`, `stuff` carry zero query overlap. Every token in the name should plausibly appear in a grep.
- **Use the corpus's own vocabulary.** If the domain says `RAF` and `HCC`, the filename says `raf-scoring-mechanics.md`, not `risk-adjustment-factor-scoring.md` — names should match the tokens queries will actually contain, and queries use the working vocabulary.

---

## 3. Append-Only Records

Records invert the reference rule: here the temporal or sequence key **is** the primary access pattern, so it earns the name prefix. This is the principled exception to "no volatile facets in names" — a record's date is not volatile; it is the immutable fact that identifies it.

```
decisions/2026-06-14--adopt-typed-generation-grammar.md
adr/0042-a2ui-validation-moves-into-generation.md
incidents/2026-05-30--corpus-regen-drift.md
```

Rules:

- **ISO-8601 dates, always, so lexical sort equals temporal sort.** `2026-06-14`, never `06-14-26` or `jun-14`. This single rule is what makes `ls` a timeline.
- **Sequence numbers (`NNNN-`) when ordering must survive same-day entries** or when the sequence itself is referenced ("per ADR-0042"). Zero-pad to a fixed width decided once; `adr/42-` and `adr/0042-` interleave wrongly forever.
- **Double-hyphen (`--`) between key and slug** so the key parses unambiguously even when slugs contain hyphens.
- **Records are never renamed and never edited — superseded.** A reversed decision gets a new record that names the old one (`2026-07-02--supersede-0042-...`), plus a `superseded_by:` field in the old record's frontmatter. The filename's immutability is what makes records citable.
- **The slug states the decision, not the topic.** `adopt-typed-generation-grammar` (an outcome) beats `generation-grammar-discussion` (a subject). A record listing should read as a history, not an agenda.

---

## 4. Indexes

- **One `INDEX.md` per directory that has more than a handful of files.** Uppercase so it sorts first in listings — the model or human scanning `ls` output hits the map before the territory.
- **The root INDEX.md is the axis enum's source of truth** (§2) and the first file an agent should be pointed at. Each entry: filename plus a one-line contract of what the file settles. An index that just re-lists filenames adds nothing; an index that states each file's *question answered* is a routing table.
- **Indexes are generated or gate-checked, never trusted by hand.** A stale index is worse than none — it is an authoritative-looking lie sitting at the top of the retrieval path. Either a script regenerates it or CI fails when directory contents and index entries diverge (§6).

---

## 5. Anti-Patterns

**Type confusion.** Decision content in a reference-shaped name (`references/caching.md` recording a choice made last March) or reference content behind a date prefix (`2025-11--oklch-notes.md` that is still the living truth). The mutation-semantics split (§1) exists to make this a visible, checkable error.

**Dates as freshness theater in references.** `component-contracts-2026.md` — will be wrong in January, un-renameable now.

**Volatile quality tokens.** `-final`, `-v2`, `-new`, `-latest`, `-updated`, `-old`, `-backup`. The canonical horror `spec-final-v2-ACTUAL.md` is what happens when identity and version share a namespace. Versions live in git; the name is the identity.

**Multi-concept omnibus files.** `design-system-notes.md` covering tokens, components, and process. It matches every query weakly and no query well, and it grows without bound. Split; name each fragment by the question it settles.

**Prose titles as filenames.** `how-we-think-about-color-ramps-at-adia.md` — six stop-words, distinctive token buried at position five.

**Draft suffixes on real names.** `raf-scoring-mechanics-draft.md` sitting next to the canonical file. Ephemeral work goes in `_scratch/`, segregated by *location*; when it graduates, it takes the real name and the scratch copy dies.

**Hand-maintained indexes drifting from reality.** The index says twelve files; the directory holds fifteen. Every retrieval that starts at the index now silently misses three files.

**Duplicate truths under different names.** `oklch-ramps.md` and `color-ramp-construction.md` both alive, diverging quietly. One question, one file, one name; the loser becomes a tombstone or dies.

---

## 6. Enforcement

What exists today: no knowledge-corpus validator is wired. The nearest live gates are `skill-author/scripts/harness_checks.py` (D9 — the files a skill references exist and are substantive) and `skills-audit`'s `scripts/corpus_index.py` (corpus-wide naming histogram + shadow check); this family follows the same gated-vs-advised discipline as `skill-author/references/skill-naming-conventions.md` §6. The manifest below is the *target* validator config — a spec for the next enforcement revision, not a live file:

```jsonc
{
  "knowledge_axes": [
    "color-science-materials", "component-contracts", "clinical-coding",
    "generation-grammar", "design-tokens"
  ],
  "record_dirs":    { "decisions": "date", "incidents": "date", "adr": "sequence" },
  "banned_tokens":  ["new", "old", "final", "v2", "latest", "draft",
                     "misc", "notes", "stuff", "temp", "backup"]
}
```

Validator checks, in CI and pre-commit (target state; until wired, these run as audit-time checks under `skills-audit`):

1. Every file under `references/` lives in a manifest-declared axis; no undeclared directories.
2. No date-pattern (`\d{4}-\d{2}-\d{2}`) in any reference filename; every reference has `updated:` frontmatter.
3. Every file in a record dir matches its declared key shape (`YYYY-MM-DD--slug` or `NNNN-slug`); record files are append-only in git history (edits to existing records fail the gate, `superseded_by:` additions excepted).
4. No banned token in any filename, corpus-wide.
5. Every directory over N files has an `INDEX.md`; index entries and directory contents reconcile exactly.
6. Near-duplicate detector across reference topics (flags the two-names-one-truth case).

---

## 7. Quick Reference

| Rule | Statement |
|---|---|
| Type first | Classify by mutation semantics: reference, record, index, ephemeral — the type picks the grammar |
| References | `references/{axis}/{topic}.md`; no dates in names; `updated:` in frontmatter |
| Records | Immutable key prefix (`YYYY-MM-DD--` or `NNNN-`); never renamed, only superseded |
| ISO-8601 | Always — lexical sort must equal temporal sort |
| Axes | Closed enum, declared in root INDEX.md, extended by manifest edit |
| Retrieval | One concept per file; distinctive token first; corpus vocabulary; no stop-words |
| Indexes | One per populated directory; state each file's question-answered; generated or gate-checked |
| Ephemeral | Segregated by location (`_scratch/`), never by suffix |
| Enforcement | Axes, record shapes, and banned tokens in the target manifest (§6 — spec, not live); audit-time under `skills-audit` until wired |

*The reduction: a knowledge filename is a retrieval key typed by its mutation semantics — references carry topic identity and hide time in metadata; records carry time as identity and never change; indexes are the checked map between them.*
