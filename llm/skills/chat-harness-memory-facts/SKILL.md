---
name: chat-harness-memory-facts
description: >-
  How a chat-agent harness gets durable, citable knowledge and persists facts across
  sessions, not task state — project-agnostic. Use for a searchable
  knowledge base, organizing a reference corpus into retrieval axes (one topic per file), the
  Grep-then-Read consult discipline, a pack that answers instead of generating, when a knowledge
  base needs an admission gate and judge, a saved preference across conversations, memory vs. a
  task list, four memory types, relative-date conversion, verify-before-trusting. Grounded in Claude Code's mechanics. ANSWERS;
  does not build. NOT for routing (chat-harness-routing-facts); NOT for streaming
  (llm-streaming-facts); NOT for vendor-swap (llm-gateway-facts).
disable-model-invocation: false
user-invocable: false
---

# chat-harness-memory-facts — citable knowledge, durable memory

Answers two distinct concerns a chat-agent harness needs, both about what an agent carries
BEYOND the current prompt: how it gives itself **domain knowledge** it can search rather than
have pasted into every context window, and how it **remembers facts** past the current session
without confusing them with the current task's own scratch state. Neither concern is this repo's
own — this pack is grounded in two kinds of source, and the reference files say which for each
claim: Claude Code's own shipped auto memory system (a platform fact, dated to the session it was
observed in) and this workspace's own knowledge-pack skill convention (real, inspectable worked
instances — including the sibling packs in this very plugin).

| Ask | Load |
|---|---|
| Authoring a knowledge base as a cited, retrieval-by-search corpus — "build an expert pack", "why is my agent's context full of reference docs", "axis decomposition for a corpus", "grep-then-read discipline", "a curated/judged training corpus instead of a fact pack" | `references/knowledge-packs-and-cited-retrieval.md` |
| Durable memory vs. ephemeral task state — "remember this across sessions", "four memory types", "convert a relative date before saving", "why a Plan/Task list isn't memory", "verify a recalled memory before trusting it" | `references/durable-memory-vs-ephemeral-task-state.md` |
| Provenance — platform fact vs. worked-instance source | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`axis decomposition`, `Grep-first`, `user/feedback/project/reference`, `relative date`,
   `verify before trusting`, …) and Read that section — the files are cited catalogs, not linear
   reads.
2. Answer on the **answer contract**: the **claim + its grounding (a platform fact dated to the
   session it was observed in, or a worked instance's cited file/line) + the failure mode it
   prevents**. A knowledge or memory claim without the failure mode it exists to prevent is half
   an answer — both conventions this pack teaches exist BECAUSE of a specific, real failure mode,
   and the failure mode is the point.
3. **Distinguish "this is how Claude Code's shipped harness behaves" (a platform fact — verify
   against Anthropic's current Claude Code documentation if this pack ages, since a product's own
   system instructions can change between versions) from "this is how this workspace's own
   knowledge-pack skills chose to structure a corpus" (a convention this workspace adopted —
   a consumer's own harness may reasonably differ in mechanism while still honoring the same
   invariant).**
4. Route output work at the boundary (below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask is routed to the consumer's own build seat (this pack has none — it is
project-agnostic). **NOT done** while a claim ships without the failure mode it prevents, or a
worked-instance detail (Claude Code's exact four memory types, this workspace's exact axis split)
is presented as if every harness must replicate it verbatim rather than honor the invariant it
protects.

## The core invariants (why these conventions exist)

- **A corpus entered by search beats one pasted into context wholesale** — a knowledge base
  dumped into every prompt pays its full size as a tax on every turn regardless of whether the
  current ask needs it, and an agent that only "knows" something because it happened to be in
  the initial dump (rather than because it looked it up) stops working the moment the corpus
  outgrows what any one context can hold.
- **Memory is for future sessions; a Plan or a Task list is for this one** — collapsing durable
  memory with in-conversation scratch state either pollutes future-session recall with
  information nobody outside the current task will ever need again, or mis-files live,
  mutable progress as settled fact.
- **An exclusion list is as load-bearing as the inclusion rules** — a memory system that saves
  everything plausible (code patterns, git history, debugging recipes — all derivable from an
  authoritative live source) is exactly as broken as one that saves nothing; each excluded
  category already has a source of truth that a saved copy will drift out of sync with.
  Convert a RELATIVE date to an ABSOLUTE one before saving a memory for the same reason — a
  memory read back after the relative reference has stopped resolving looks precise but has
  gone silently stale.
- **A recalled memory or a cited reference is a claim about the past, not the present** — before
  acting on either (not merely discussing it), re-verify the specific artifact it names still
  exists as claimed; a stale-but-confident citation is more dangerous than an absent one because
  it looks authoritative right up until an action built on it fails against a reality that moved
  on.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build or fix a knowledge base, an INDEX, a retrieval index, or a memory-persistence
  mechanism in YOUR project** → your project's own build seat/agent (this pack has none — it
  teaches the conventions, it owns no codebase's source). For authoring a NEW knowledge-pack
  skill specifically → `make-pack` (axis decomposition, grounded research waves, index
  discipline), where installed.
- **Routing a live request to the right capability** (should this be a skill vs. hardcoded, why a
  skill never triggers, picking among skill/tool/subagent) — a distinct concern from persisting a
  fact across sessions → [[chat-harness-routing-facts]] (the sibling pack in this plugin
  family).
- **The wire format of a model's OWN live streaming output** (SSE framing, JSONL structured
  output, validate-then-stream) — a transport/content concern, not a knowledge or memory one →
  [[llm-streaming-facts]] (the sibling pack in this plugin).
- **A vendor-swap or trust-boundary concern for calling an LLM** → [[llm-gateway-facts]] (the
  other sibling pack in this plugin) — orthogonal to both concerns this pack answers.

## Extending this pack

A missing axis, a stale citation (Claude Code's memory mechanics moved, a workspace convention
changed), or a second worked instance proving a variant generalizes — route to `make-pack`
(axis decomposition, grounded research waves, index discipline), where installed; otherwise apply
its discipline inline: one reference per distinct class of ask, every claim grounded, never an
uncited file bolted on.
