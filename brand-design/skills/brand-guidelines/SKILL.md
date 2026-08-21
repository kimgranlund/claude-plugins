---
name: brand-guidelines
description: >
  The methodology and ledger reference for building brand guidelines by GUIDED CHOICE — the six
  brand domains, the 2×2 quadrant mechanic, the append-only choice ledger, and how choices assemble
  into corpus docs. Use when the user asks about the mechanism itself — "what domains does the
  guidelines loop cover", "how does the choice ledger work", "how do choices assemble into the
  corpus". NOT for actually running the guided loop now — that's make-brand-guidelines, which owns
  the "build brand guidelines" / "give me a 2x2" triggers and cites this pack for posture. NOT for
  strategy (brand-methodology-rules) or copy (brand-writer).
disable-model-invocation: false
user-invocable: true
---

# Brand Guidelines — the guided 2×2 elicitation loop

Most brand-guidelines docs are written by one person guessing, then policed. This skill **builds them by guided choice**: for each brand domain the system proposes a **2×2 of concrete options**, you pick a quadrant and comment, and the choices **accumulate** into a coherent, evidence-traced guidelines section in the corpus. The model proposes the options; **you supply the taste**; code owns the accumulating state and (later) the assembly.

2 declared axes — below pack-writing-rules' 3-7 floor. This pack's own retrieval surface stays
thin because most of the mechanism (the loop, the seven axes, the ledger shape) lives in this
SKILL.md body itself; `references/` only carries the two things too long to inline. Flat consult
table below, no `references/INDEX.md`.

## Consult table

| Ask | Load |
|---|---|
| The full loop mechanism — the 2×2 recipe, the design-move card, drill-down, the coherence graph, assembly, the brand-decomposer seam | `references/the-loop.md` |
| Which real-brand exemplar grounds a given domain/axis quadrant | `references/exemplars.md` |

This file is the table of contents; the full mechanism is in [`references/the-loop.md`](references/the-loop.md).

## The loop (per domain)

The loop walks **six domains** — `mark · voice · color · type · expression · governance` — with the **brand idea** (from `01-foundation`) sitting above them as what every option must trace to. For each domain:

1. **Frame** — read `01-foundation` + the accumulated choice-ledger (run **`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guidelines_ledger.py" coherence --domain <d>`** to surface prior commitments + any contradictions); pick the domain's **two axes** (a default pair, below; the model may swap with a stated reason; you may override) → a 2×2.
2. **Generate** — four **design-move cards** (A/B/C/D), one per quadrant, each a concrete move grounded in the foundation + a cited exemplar (per-domain/axis seeds in [`references/exemplars.md`](references/exemplars.md) — cite the mechanism, never the asset) + the quality bar. Never generic, never "on-brand" — each names a causal mechanism.
3. **Present** — the 2×2 as a Markdown grid + the four lettered cards; ask for **A/B/C/D + free-text comments/corrections**.
4. **Capture** — append a typed **choice** to the ledger (the chosen move, amended by your comment, with contributors + exemplar evidence). A comment like *"B but warmer"* records the amended move **and** re-renders a refined card for confirmation.
5. **Drill or advance** — if the domain's capture spec has unresolved sub-decisions, spawn a **finer 2×2** within the chosen quadrant; else advance. Earlier choices **constrain** later domains (coherence).

The ledger is the state — the loop resumes at the frontier. It MAKES; it never grades its own output (that split is below).

## The seven axes (cross two → a 2×2)

`functional↔expressive · product-led↔human-led · quiet↔loud · literal↔metaphorical · premium-restraint↔campaign-loudness · institutional↔conversational · systematic↔organic`

Default axis pair per domain (the model may swap with a reason): **mark** literal↔metaphorical × systematic↔organic · **voice** institutional↔conversational × functional↔expressive · **color** functional↔expressive × restraint↔loudness · **type** systematic↔organic × functional↔expressive · **expression** quiet↔loud × premium-restraint↔campaign-loudness · **governance** systematic↔organic × product-led↔human-led.

## The choice-ledger (mechanized state)

Each pick appends a typed entry to a **choice-ledger** (the cumulative knowledge), kept in the corpus and **validated by `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guidelines_ledger.py"`** (well-formed by construction — the score-record/assess-record discipline). Append-only with `supersedes` for revisions (never rewrite a decision). → the entry shape + enums: `guidelines_ledger.py schema`, and [`references/the-loop.md`](references/the-loop.md).

## Assembly + scoring (the loop closes)

Check progress with **`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guidelines_ledger.py" coverage`** (per-domain resolved/absent + the frontier). When the domains are covered, **`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guidelines_ledger.py" assemble [--out <corpus>] [--apply]`** (defaults to **`./brand-corpus`**, like `file-brand-corpus`) compiles the live ledger into corpus docs in their layers (dry-run by default; matches the corpus's flat/folder convention; refuses a mixed corpus; **non-destructive** — never clobbers a hand-authored layer doc, writing a flagged `.elicited.md` sibling instead, `--force` to replace, re-assembly idempotent) — each choice a typed rule (`must/should/may`), carrying **`sources:`** + **`contributors:`** frontmatter — so **`corpus_provenance.py` gates the trace** and **`brand-rubrics` scores** the result. The build loop closes into the provenance + evaluate loops.

**The brand-decomposer seam:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/guidelines_ledger.py" card <ledger> --idea "<from 01-foundation>" -o card.json` projects a `*.brand.json` card that `design-skills:brand-decomposer` (the `nonoun-skills` marketplace) can GRADE + operability-check (`brand-spec-check.py lint card.json`) when installed — the optional make→grade handoff (verified: a projected card clears brand-decomposer's operability gate). brand-design stays self-contained.

## Relationship to brand-decomposer (parallel, not a dependency)

`design-skills:brand-decomposer` (the `nonoun-skills` marketplace) is the **grader/operability lens** for a brand spec — the 100-pt rubric, the typed schema, the WCAG/provenance checker, the six domains + seven axes this skill mirrors. The split is **by verb: brand-decomposer GRADES/decomposes/critiques; brand-guidelines MAKES.** They are **parallel** (brand-design is self-contained; brand-decomposer is a different marketplace) joined by an **optional seam**: the assembler can project a `*.brand.json` card that brand-decomposer grades when installed. We mirror its vocabulary; we do not depend on it.

## Provenance

This pack's `references/` were ported from brand-forge, Phase 3 Track D — full citation (source
repo, frozen SHA, date) in the plugin root README's "Provenance and disposition" section.

## Boundaries

- **Makes, doesn't grade** — scoring is `brand-rubrics` (in-plugin) + `brand-decomposer` (when installed).
- **Guidelines, not strategy** — the position/POV is `brand-methodology-rules` (this loop *descends from* `01-foundation`, it doesn't decide it).
- **Structure, not copy** — voice *behavior* here; the actual words are the `brand-writer` agent.
- → Full mechanism, the design-move card, drill-down, coherence graph, assembly, the seam: [`references/the-loop.md`](references/the-loop.md).
