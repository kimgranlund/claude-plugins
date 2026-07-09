---
name: vision-memo-author
description: >-
  Use to author — or improve a drafted — vision memo: the class of document that argues
  *how to think* about a problem, not what to build: manifestos, reframe essays, strategic case-for
  pieces, and synthesis memos. Triggers: "write a vision memo / manifesto / strategic brief / position
  paper / think piece", "make the first-principles case for", "reframe this decision", "crystallize
  this thinking into a shareable doc", "synthesize these competing positions", "tighten this drafted
  memo's argument", or when accumulated conversation-thinking should become a
  standalone opinionated argument. Picks the archetype (manifesto · reframe · case-for ·
  synthesis), locates the thesis, performs the reduction, and drafts in an opinionated, physics-literal,
  compressed voice; scored by its rubric (doc-reviewer grades it). NOT for a PRD, product brief, or SPEC
  (prd-author / spec-author), an LLD / ADR (lld-author / adr-author), or a reference doc
  (reference-author) — those describe what to build or document; NOT for scoring or reviewing a finished memo against its rubric (doc-review); NOT for marketing
  copy, a tutorial, a
  status update, or a neutral balanced survey — a vision memo takes a stake and argues one thesis.
disable-model-invocation: false
user-invocable: true
---

# Vision Memo Author — the document that changes how the reader thinks

A vision memo is an **argument, not a description**. A spec says what should exist; a PRD says what to
build; a vision memo argues for a *way of seeing* the problem. The test is exact: if the reader finishes
knowing new facts but thinking the same way, the memo failed; if they finish with the same facts but a
changed mental model, it succeeded. Every memo therefore has a **thesis** — one claim about how to see
the problem that the reader probably doesn't hold yet — and everything in it exists to make that claim
compelling and defensible. The genre's signature quality is **density**: a lot of thinking per page.

The craft doctrine (the six principles, the voice, the anti-patterns, a worked example) is
`references/craft.md`; the four archetype templates are `references/archetypes.md`; a memo is scored
against `references/rubric.md` (gate: V1 thesis · V6 opinionated voice).

## Step 1 — Pick the archetype

Not every memo is the same shape. The archetype determines the structure; writing a reframe as a
manifesto bloats it, writing a manifesto as a reframe underdevelops it. Ask in order:

| Ask | Archetype | Shape | Words |
|---|---|---|---|
| Proposing an entire system or direction? | **Manifesto** | reduction → building blocks → principles → roadmap | 2500–4500 |
| Arguing one concept should be seen differently? | **Reframe** | current view → the reframe → leverage points → meta-point | 1500–2500 |
| Making the strategic/economic case for an approach? | **Case-For** | misdiagnosis → why-now → reduction → what changes → transition | 2000–3500 |
| Resolving competing positions into one path? | **Synthesis** | alignments → conflicts → gaps → net assessment | 1500–3000 |

When in doubt, pick the smaller form — a reframe that lands beats a manifesto that sprawls. Full
section-by-section templates + voice cues per archetype: `references/archetypes.md`.

## Step 2 — Run the method (six stages, each with its failure mode)

1. **Locate the thesis.** Find the one sentence the memo argues — the *claim*, not the topic. If you
   can't state it in one sentence, the memo isn't ready. *Fails as:* a survey with no stake (rubric V1).
2. **Perform the reduction.** Strip the problem to its irreducible atoms — what is this, really, with
   tooling and convention removed? A good reduction feels trivially true once stated and immediately
   rules solutions out. *Fails as:* jumping to solutions, or a "reduction" that's an abstract definition
   ruling nothing out (V2).
3. **Identify the reframe — if there is one.** Is the reader asking the wrong question? Name the
   received-wisdom misdiagnosis and what changes when it's seen correctly. Not every memo has one.
   *Fails as:* a manufactured straw-man reframe where no genuine misdiagnosis exists (V3) — skip the
   stage instead.
4. **Enumerate the primitives.** 3–7 named, opinionated, individually-justified, composable units carry
   the argument ("Intent Capture" not "Requirements Gathering" — the naming encodes the claim).
   *Fails as:* 10+ diluted or 1–2 shallow (V4).
5. **Design the arc.** Three movements regardless of archetype: **reduction** (what this is) →
   **structure** (the primitives/synthesis that follow) → **elevation** (why it matters beyond the
   topic). *Fails as:* ending tactical, with no elevation (V5).
6. **Write in voice, then cut.** Draft opinionated, physics-literal, compressed; then cut every
   paragraph that could appear in any memo on any topic. *Fails as:* a neutral, hedged voice that could
   have been written by anyone (V6). Voice doctrine: `references/craft.md`.

**The thesis gate is real:** if mid-draft you cannot state the thesis in one sentence, stop and find it
before writing another paragraph. A vaguely-scoped "write about why X is important" request usually has
no thesis yet — ask one sharpening question (what specifically? is there a reframe, or general
advocacy?) and offer to locate the thesis first, rather than producing a generic "X is important" piece.

## Output contract

A single markdown file, **1500–4000 words**, structured to the chosen archetype. Naming:
`{topic}-{archetype}.md` (e.g. `feature-store-case-for.md`, `types-as-physics-reframe.md`). It reads
well top-to-bottom for a newcomer AND is navigable by section header for a reader hunting one argument.
Produce it as a shareable artifact — the user will copy or upload it somewhere.

## Validation loop (finalize only when it clears)

draft in voice → **cut** every paragraph that doesn't advance the argument → self-score against
`references/rubric.md`; finalize only when the **thesis (V1)** and **opinionated-voice (V6)** gates
clear and the reduction (V2) genuinely constrains what follows. **Generator ≠ critic:** for a memo that
matters, dispatch **doc-reviewer** (fresh context, this rubric) rather than grading your own argument.

## Update — a memo is write-once

A vision memo is a **point-in-time argument**, not a living document. When the thinking moves, do NOT
patch prose — the reduction and thesis the memo is built on may no longer hold, and a patched memo
drifts into incoherence (a new leverage point bolted onto an old arc reads as two memos). Re-run the
loop: ship a *new* memo, or a superseding revision that re-derives the thesis and reduction from the
changed understanding. Re-dispatch, don't edit.

## References & composition

| Path | Use when |
|---|---|
| `references/archetypes.md` | The chosen archetype's full section template + voice cues |
| `references/craft.md` | The six principles, the voice/style doctrine, anti-patterns, a worked example |
| `references/rubric.md` | Score the memo (gate = V1 thesis, V6 voice); the standard **doc-reviewer** loads |
| `scripts/routing-corpus.json` | The routing eval corpus for this skill's description |

- **doc-reviewer** is the memo's independent critic — it loads `references/rubric.md` and scores.
- **[[intent-extract]]** / **[[intent-grill]]** sharpen a fuzzy "make the case for X" into a statable
  thesis *before* drafting (the V1 precondition).
- **[[prd-author]]** / **[[spec-author]]** / **[[lld-author]]** own what-to-build documents; this owns
  the argument for *how to think* about building it. Route a spec request there, not here.
- **[[rubric-author]]** owns `references/rubric.md`'s shape.

**Done** = an archetype chosen, the thesis statable in one sentence, the V1 (thesis) and V6 (voice)
gates cleared, and a cut pass run over the draft. **NOT done** = a survey shipped (no statable thesis),
a hedged or balanced voice, a "reduction" that rules nothing out, or a memo never scored against its
rubric.
