# Knowledge packs and cited, retrieval-by-search corpora

> Axis: authoring a knowledge base as a cited corpus retrieved by search, not prose dumped
> wholesale into context. Grounded in this workspace's own knowledge-pack skill convention —
> forge's `pack-authoring-standards` + `skill-authoring-standards` (retired 2026-07-19 from
> docs' `knowledge-forge`, folded into forge as the estate-wide factory), this very skill
> family as a live instance, and `agent-protocols`'s `a2ui-training-facts` as a heavier variant —
> cited as worked instances of the pattern, not as its only valid shape.

## The core distinction — dump vs. retrieve

**Claim — a knowledge base is a corpus BEHIND a boundary, entered by search, never pasted into
context wholesale.** Two failure modes this prevents: (1) a context window that fills with
reference material on every turn regardless of whether the current ask needs it, and (2) an
agent that "knows" something only because it happened to be in the initial dump rather than
because it looked it up — a distinction that matters the moment the corpus grows past what any
one context can hold. **Grounding:** forge's own `skill-authoring-standards` states this directly —
"a knowledge pack is a corpus behind a boundary: `references/` organized by question type"
(`forge`'s `skill-authoring-standards/SKILL.md:97`).

## Axis decomposition — subdirectories are the retrieval taxonomy

**Claim — the question space splits into 3-7 retrieval axes, each landing as one
`references/` file, chosen by how users ASK, not how the literature organizes the topic.**
`pack-authoring-standards` names this explicitly: "Files are ask-shaped, never literature-shaped...
two genuinely different question types never share a file, however related their subject"
(`forge`'s `pack-authoring-standards/SKILL.md:34-38`). **Worked instance — this very skill family:** the sibling packs
in this plugin split on exactly this principle — `llm-gateway-facts` axes on "adapter seam /
registry+trust-boundary / dev-proxy+bundler footguns / stateless session model" (four rows in its
own consult table, `llm-gateway-facts/SKILL.md:29-35`) and `llm-streaming-facts` axes on
"chunk-buffering technique / the vendor contract worked / validate-then-stream" — a genuinely
different split of the SAME underlying "how do I use an LLM safely" question space, because the
two packs' users ask different classes of question. **Failure mode this prevents:** an
alphabetical or literature-mirrored axis set makes retrieval a guessing game — a consult table
only works if an ask maps to exactly one row without the reader needing to already know the
answer.

## Grounded research waves — one topic per file, cited and dated

**Claim — each reference file is written FROM verified research, not filled in from
recollection, and every claim inside it cites its source** (a `file:line`, an ADR/SPEC clause, or
a dated vendor-doc citation). `pack-authoring-standards`' research-wave step: "Distill ask-shaped —
one file per question type, grounding-marked, within load budgets" (`forge`'s
`pack-authoring-standards/SKILL.md:100`), with every claim wearing a grounding marker —
`[verified]` / `[inferred]` / `[drift-prone]` / `[incident]` (`pack-authoring-standards/SKILL.md:79-86`).
**Worked instance:**
`llm-gateway-facts/references/provider-adapter-seam.md` cites `agent-transport.ts:81-88` for
its interface-shape claim and `anthropic.ts:124` for its factory-injection claim — a reader can
open those exact lines and check the claim rather than trust the pack's paraphrase. An invented
or stub reference — a file with no citation behind its claims — is a dangling pointer in this
convention, not a lesser-quality entry: "a claim with none of these [markers] is an orphan; a
corpus of orphans is vibes with a directory structure" (`forge`'s `pack-authoring-standards/SKILL.md:88`).

## The entry surface — a typed index entered by search, never read start-to-finish

**Claim — the pack's front door is a table mapping ask-class to file, with an explicit
Grep-first, Read-the-section discipline**, not "read this whole folder." `skill-authoring-standards`
names this as one of the entry surface's required elements: "the body states, in the consult
procedure itself, that the corpus is entered by search — Grep the matching file for the term
first, then Read the section" (`forge`'s `skill-authoring-standards/SKILL.md:100`). Every pack in
this plugin states the same load discipline near-verbatim: "Grep the matching file for the term
first... and Read that section — the files are cited catalogs, not linear reads"
(`llm-gateway-facts/SKILL.md:39-41`; `llm-streaming-facts/SKILL.md:40-42` states the identical
discipline with its own term list). At larger corpus scale, `pack-authoring-standards` promotes
this table to a root `INDEX.md` (one line per file) rather than folding it into the SKILL.md body:
"when the SKILL.md consult table lists every reference file 1:1 (a flat corpus of ≤~7 files), the
table IS the retrieval map... ship no INDEX. An INDEX.md earns its keep the moment files outgrow
what the table enumerates" (`forge`'s `pack-authoring-standards/SKILL.md:50-55`); this skill family
(small, hand-authored) uses the SKILL.md-table form, the same form this pack uses.

## The answers-not-generates boundary

**Claim — a knowledge pack ANSWERS from its cited corpus and routes every making-ask to a
builder peer; it never produces the artifact its domain concerns.** Every sibling pack in this
plugin states this boundary in its own description ("ANSWERS from a cited corpus; does not
build") and repeats it in a dedicated Boundaries section naming the exact peer for each kind of
making ask. **Failure mode this prevents:** a pack that both answers questions AND does the work
drifts toward doing the work from its own paraphrase of the corpus instead of the corpus's cited
source, and a maker that also grades its own knowledge pack never notices when its corpus
generalized wrong from the worked example it cites (see the sibling
durable-memory-vs-ephemeral-task-state reference file in this skill for the analogous
generator-vs-memory distinction on the persistence side).

## A heavier flavor — a curated, judged TRAINING corpus, not a grep-and-cite reference pack

**Claim — when the "knowledge" being built is itself a growing, admitted, judged dataset rather
than a fixed set of reference facts, the retrieval-by-search shape above is necessary but not
sufficient; the corpus needs an admission gate, deduplication, and a judge/verdict adapter
deciding what enters at all.** **Worked instance:** `agent-protocols`'s `a2ui-training-facts` pack
documents exactly this heavier architecture over `@agent-ui/a2ui`'s real corpus subsystem — an
11-stage admission pipeline (`admit.ts:5-9`: heal, schema/field, facet gate, pin check, tier-1
deterministic validation, pointer resolution, leak gate, canonical hash, dedup, tier-2 rubric
judgment, write), a closed, form-only healer that repairs formatting defects but never semantic
ones ("an over-eager healer would launder invalidity into a corpus whose whole point is provable
validity", `a2ui-training-facts/references/admission-gate-and-healing.md`), and an injected judge
seam that fails closed when absent rather than silently skipping quality grading
(`admit.ts:176-177`, ADR-0060 Decision clause 1). **The distinction that matters:** a reference
pack like this one or its siblings needs only citation discipline — the facts are already true,
the work is organizing and citing them. A training corpus needs admission discipline — each
candidate record is untrusted input that must be proven valid (and non-duplicate, and above a
quality bar) BEFORE it joins the corpus, because the corpus's value depends on every member being
provably sound, not merely plausible. Reach for the heavier shape only when the knowledge itself
is a growing set of judged records (exemplars, verdicts, training data) rather than a fixed body
of facts about how something works.

## What this file does NOT cover

Persisting a fact or preference so it survives past the current session, as distinct from a
task's in-session state (the sibling durable-memory-vs-ephemeral-task-state reference file in
this same skill) · the per-file reference-document standard itself (`make-reference`, a docs
skill) · routing a live request to the right capability (a distinct harness concern this skill
does not own) · the concrete rubric a training corpus's judge scores against
(`a2ui-training-facts`'s own `judge-and-verdict-adapter.md`, cited above as an instance, not
restated here).
