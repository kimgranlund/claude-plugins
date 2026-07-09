---
name: knowledge-forge
description: >-
  Author a knowledge pack — a noun-named, answers-only skill with a cited reference corpus and a
  typed retrieval index. Use when minting or extending a world-model skill: "build an expert pack on
  X", "make a skill like ui-patterns / color-science-perception", "turn this research into a knowledge skill",
  "our corpus needs a retrieval surface", "add an axis to this pack". Covers the axis decomposition
  (subdirs = retrieval taxonomy), grounded research waves (one topic per file, cited and dated), the
  INDEX + consult-table entry surface, and the answers-not-generates boundary with routed builder
  peers. NOT for a single reference document (reference-forge); NOT for a procedure skill
  (forge's skill-forge — which also owns the entry surface's final gate); NOT for maintaining a Claude
  Project knowledge base (that is a different substrate).
disable-model-invocation: false
user-invocable: true
---

# knowledge-forge — mint world models

A knowledge pack is **a corpus behind a boundary**: cited references organized as a retrieval
taxonomy, fronted by a lean entry surface that ANSWERS and routes all making to builder peers. The
reference instances are [[ui-patterns]] (hand-authored, canon-cited) and the `color-science-*`
family (research-wave scale; split into four packs 2026-07-06) — match their shape, not their size: a pack earns exactly the corpus its
questions need. (The broad `knowledge` stem is deliberate: this factory's territory is the
species itself — every domain's world model — so the stem's breadth equals the charter's.)

## Procedure

1. **Charter.** Name the domain and its breadth (the stem must match exactly — over-broad
   false-triggers, over-narrow misses); pick a **noun-compound name** (knowledge packs take no verb
   — forge's skill-authoring-standards §species); write the ANSWERS-only
   boundary first: which builder peers receive the making (and where a builder doesn't exist yet,
   an explicit "not installed — derive inline" dead-end, never a phantom handle).
2. **Axis decomposition.** Decompose the question space into 3–7 retrieval axes — e.g.
   *ui-patterns*: asks split macro ("what template?") / micro ("how should this module behave?") /
   state ("what does empty look like?") → three axes, one consult-table row each
   (`module behavior → ui-patterns/references/micro-patterns.md`). Each axis is one
   `references/` subdir, each ask-class landing in exactly one. Axes follow how users ASK, not how
   the literature is organized (macro/micro/state beats alphabetical; per-script beats
   per-standard). Run [[system-decompose]] when the axes aren't obvious.
3. **Research waves — forge's pack-authoring-standards grounding rules govern.** Write each reference from solid
   knowledge or research it first (`WebSearch`/`WebFetch`, several authoritative sources; a
   deep-research skill, where installed, for contested or fast-moving domains). One topic per file ·
   claims cite their source · editions/dates on canon · a `sources.md` axis carrying provenance in
   trust order. An invented, filler, or stub reference is a dangling pointer — cut the axis instead.
   Distinguish corpus-backed answers from general-knowledge answers and say which is which.
4. **The typed index, scaled to corpus size.** Research-wave scale ships an `INDEX.md` at the
   corpus root (one line per file); for a hand-authored pack the SKILL.md consult table suffices.
   Either way the entry is typed (ask-class → axis → file) with the load discipline stated: Grep
   for the term first, Read with offset — a corpus is a lookup structure, entered by search. State
   the true file count once; a wrong count is a false manifest that gets absorbed as fact. The
   count's mechanical check is owned by [[skills-audit]]'s corpus-level integrity check — this
   factory ships no checker of its own, because its one mechanizable surface (cross-file
   pointer/count integrity) already has that owner.
5. **Entry surface, then the loop.** Author SKILL.md on the knowledge-pack shape — identity ·
   consult table · Grep-first discipline · consult procedure with ONE worked example on the
   **answer contract** (base form: claim + cited file + the failure mode or caveat; pattern-packs
   extend it with name / anatomy / when-it-fits) · the **deviation doctrine** (every default
   carries its rationale, so the consumer knows when deviating is legal) · boundaries that route
   ALL making · the factory route (the pack names this skill as its factory) · the
   corpus-of-record rule (the pack checks its routing corpus in at `scripts/routing-corpus.json`)
   — then run forge's skill-forge loop: all harness gates green, its skill-auditor +
   `linguistics-reviewer` dispatch (**generator ≠ critic**), fix, re-gate.

## Update (re-sync after drift)

A pack drifts when its canon moves — a spec revision, a new edition, a renamed standard. Re-run
the research wave for the affected axis (the same grounding rule governs), re-date the touched
references and `sources.md`, and re-verify the stated counts. A pack answering from a superseded
edition is a false manifest with citations.

## Detection catalog

Verb-named packs (a pack that "does" has the wrong species) · axes mirroring the literature instead
of the asks · references restating what the model already knows cold (the calibration test: cut it)
· a generation leak ("use these when generating…" inside an answers-only surface) · counts/status
claims that drift from the tree · phantom builder peers · one file serving two axes (split or cite,
never duplicate).

## Routing

| Peer | For |
|---|---|
| [[reference-forge]] | the per-file standard each reference is written to |
| forge's `skill-forge` + `skill-authoring-standards` (where installed) | the entry surface's gates + the create/evaluate/improve loop |
| [[rubric-forge]] | when the pack needs a scoring standard alongside the corpus |
| [[system-decompose]] | deriving the axis taxonomy when it isn't obvious |
| [[ui-patterns]] | the hand-authored reference instance of the shape |
| `WebSearch` / `WebFetch` (+ a deep-research skill where installed) | the research waves |

**Done** when the pack answers on the contract from a cited, dated corpus, its index matches the
tree, every making-ask has a routed peer, all gates are green, and the independent critics
(generator ≠ critic) have converged. **NOT done** while any reference is invented, stubbed, or
undated, a stated count disagrees with the tree, a builder handle dangles, or the only review the
pack carries is its maker's own.
