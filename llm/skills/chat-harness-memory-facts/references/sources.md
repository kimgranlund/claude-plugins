# Sources — provenance for the knowledge-and-memory claims

This pack teaches two conventions, not one repo's implementation — each claim is grounded in one
of two kinds, and the reference files say which. Neither trust order below outranks the other;
they answer different questions ("is this how the shipped harness behaves" vs. "is this a sound
way to structure a corpus").

## Platform fact — Claude Code's own auto-memory system (verify against current docs if stale-sensitive)

The four-memory-type model (`user` / `feedback` / `project` / `reference`), the hard exclusion
list (code patterns, git history, debugging recipes, anything already in an entry file), the
relative-to-absolute date-conversion technique, the verify-before-trusting-a-recalled-memory
rule, and the explicit Plan/Task-are-not-memory distinction are all quoted directly from the
memory-system instructions present in the dispatching Claude Code session on 2026-07-13 (the
`# auto memory` section of that session's own system context — this pack's originating task
brief carries the exact quotes cited in `durable-memory-vs-ephemeral-task-state.md`). This is a
shipped product's own operating instructions, not this workspace's invention — treat every claim
in that reference file as a **platform fact that can drift between Claude Code versions**; verify
against Anthropic's current Claude Code documentation before relying on an exact mechanism
(memory-type names, file layout, or wording) if this pack has aged. The underlying INVARIANTS it
protects (future-session recall distinct from in-session scratch state; an exclusion list as
load-bearing as the inclusion rules; re-verify a stale citation before acting on it) are far more
durable than the exact implementation and are unlikely to reverse even if the mechanism's details
move.

## Worked instances — this workspace's own knowledge-pack skill convention (real, inspectable, cited for concrete grounding)

Unlike the platform-fact half above, these are files and directories directly readable in this
workspace right now — inspect them to verify a claim, not "verify against external docs":

- **harness's `pack-writing-rules` + `skill-writing-rules`** (`/Users/kimba/Projects/nonoun/plugins/harness/skills/pack-writing-rules/SKILL.md`,
  `/Users/kimba/Projects/nonoun/plugins/harness/skills/skill-writing-rules/SKILL.md`)
  — the authoring factory for this exact shape: axis decomposition → grounded research waves → the
  typed index (pack-writing-rules) → the entry-surface charter/boundary/deviation-doctrine
  (skill-writing-rules). docs' `knowledge-forge`, the original single-skill version of
  this factory, was retired 2026-07-19 and folded into these two forge skills as the estate-wide
  factory route. Cited throughout `knowledge-packs-and-cited-retrieval.md`.
- **This very skill family** (`/Users/kimba/Projects/nonoun/plugins/llm/skills/`) —
  `llm-gateway-facts` and `llm-streaming-facts` are live instances of the pattern this pack
  describes in the abstract: each carries its own consult table, Grep-first load discipline,
  answers-not-generates boundary statement, and `scripts/routing-corpus.json` corpus-of-record.
  This pack (`chat-harness-memory-facts`) is itself a third instance of the same shape,
  authored alongside its `chat-harness-*` siblings in this plugin.
- **`agent-protocols`'s `a2ui-training-facts`**
  (`/Users/kimba/Projects/nonoun/plugins/agent-protocols/skills/a2ui-training-facts/`) — a
  heavier, judged-dataset flavor of the same underlying idea, documenting `@agent-ui/a2ui`'s real
  corpus subsystem (`packages/agent-ui/a2ui/src/corpus/**`), governed by ADR-0060/0061/0062/
  0063/0064/0068. Cited in the "heavier flavor" section of
  `knowledge-packs-and-cited-retrieval.md`, itself verified 2026-07-07 per that pack's own
  `admission-gate-and-healing.md` header.

These worked instances are cited as PROOF the convention works in real, shipped skills — not as
the only valid shape a knowledge pack or corpus can take. A consumer's own harness may reasonably
differ in file layout or naming while still honoring the same invariants (see the SKILL.md's
"core invariants" section for what must hold regardless of implementation).

## Boundary — layers owned elsewhere

This pack answers the knowledge-and-memory pair; it does not restate its neighbors. The
per-file reference-document standard is `make-reference`. Routing a live request to a capability
is [[chat-harness-routing-facts]]'s territory. The wire format of a model's own streaming
output is [[llm-streaming-facts]]'s. When a cited worked instance and its own source repo disagree
about current behavior, the source repo wins and this pack's citation needs repair, not the other
way around.
