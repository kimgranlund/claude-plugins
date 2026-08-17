# Sources — provenance for the skills-and-routing claims

This pack teaches a PATTERN — how a chat-agent harness should expose and route capabilities — not
one workspace's own routing corpus. Every claim in the three axis files is one of two kinds, and
each file says which for each claim. Neither trust order below outranks the other; they answer
different questions ("is this how Claude Code's own mechanism behaves" vs "is this a sound way to
test and structure routing").

## Claude Code's own skill-loading mechanics — a platform fact, verify against current docs

Facts about how the Claude Code harness itself loads, triggers, and routes skills and tools. These
can drift as the platform versions — if a claim here disagrees with CURRENT Claude Code docs, the
docs win and this pack needs repair.

- **`harness:skill-writing-rules`** (installed at
  `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.23.0/skills/skill-writing-rules/SKILL.md`,
  identical at `1.21.0`) — the single most directly-inspectable primary source on this exact
  mechanism, itself dated "verified 2026-07, Claude Code 2.1.20x [drift-prone]." Cited by exact
  line across all three axis files: the description-is-the-API/body-is-the-payload framing
  (`:16`), the description-listing-budget physics (`:23`), the description-engineering rule and
  its bad/good contrast (`:61-74`), the three-species table (`:37-41`), the corrected
  preload-blocking finding (`:43`), the both-dials-explicit rule (`:45`), the capability-uplift
  vs encoded-preference axis (`:48`), and the baseline-comparison evaluation check (`:115`).
- **`skill_lint.py`** (same `harness` install, identical across `1.21.0`/`1.23.0`) — the mechanical
  enforcement of the standard above; cited for the `W5` knowledge-noun/`user-invocable` mismatch
  rule (`:209-210`).
- **The deferred-tool, load-on-demand mechanic for TOOLS** — observed directly in this session's
  own environment (a live protocol state at authoring time, not a repo file): tool names appearing
  without their full parameter schema until a search-style lookup resolves it. This is the single
  highest-drift-risk citation in the pack, since it describes live runtime behavior rather than a
  committed file — verify against current Claude Code documentation before relying on it, and treat
  it as illustrative of the SAME underlying principle as skill `description`-first loading, not as
  a permanently-fixed mechanism name.
- **Subagent description routing carrying the same `NOT for <thing> (<owner>)` fence** — likewise
  observed directly in this session's own subagent registry (entries such as `a2ui-composer`,
  `a2ui-builder`), not a committed file citation.

## This workspace's routing-corpus + evals convention — a worked instance you can inspect directly

A real, shipped instance of testing routing adversarially and measuring it over time, in THIS
workspace — cited as proof the discipline works and as a schema to imitate, not as the only valid
shape a routing corpus could take.

- **`llm-gateway-facts/scripts/routing-corpus.json`** and **`llm-gateway-facts/evals/evals.json`**
  (this same plugin, sibling skill) — the `{skill, _note/note, positives/negatives or cases}`
  schema pair, and the `_note` field's explicit adversarial-negative-selection rationale (dangerous
  near-neighbors named by category: sibling pack, cross-plugin pack, genuine build ask).
- **`a2ui-chat-agent-facts/evals/evals.json`** (`agent-protocols` plugin,
  `/Users/kimba/Projects/nonoun/plugins/agent-protocols/skills/a2ui-chat-agent-facts/evals/evals.json`)
  — the `note` field's dated, two-entry measurement history (a 2026-07-09 blind run at 33/36, a
  same-day estate-wide re-run also at 33/36 with different cases resolved), the clearest evidence
  in this workspace that routing is measured and re-measured, not assumed after one write.
- **`harness`'s `release_gate.py` G7 gate** (`/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/scripts/release_gate.py`)
  — enforces that every model-invocable skill's eval suite is schema-valid (`FAIL`s the release)
  and warns (does not fail) when a model-invocable skill ships with no suite at all — the
  mechanical backstop behind "write a corpus" actually being checked, not merely encouraged.

## Boundary — layers owned elsewhere

This pack answers the skill-vs-hardcode decision, the invocation-species dial, and single-request
routing; it does not restate its siblings. Layering standing instructions and enforced guardrails
across a whole harness is [[chat-harness-guardrail-facts]]. Composing multiple skills,
tools, or subagents into a multi-step workflow is [[chat-harness-workflow-facts]]. The
repo-structural standard for writing a SKILL.md file to spec (frontmatter shape, body budgets,
per-species templates) is `skill-writing-rules` directly, where installed — this pack teaches
the upstream DECISIONS that standard's file format then encodes, and should never restate its
checkable rules.

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`envelope-framing-and-out-of-band-signals.md`, `multi-producer-namespacing.md`,
`model-declared-routing-integrity-check.md`, and `client-side-label-auto-attach.md` were added
from agent-ui#1115's "Scope-conformant revision v2" comment (posted 2026-08-17T17:14:57Z), the
litmus-filtered re-harvest of `@agent-ui/a2ui` lessons kept to web-based virtual-chat-harness
knowledge only. Lesson 18 of that same v2 export ("the server's validated selection beats
client-supplied fields") was evaluated and SKIPPED here as hard dedup — already substantively
covered by [[llm-gateway-facts]]'s `registry-and-trust-boundary.md` (`resolvePair`'s own
discriminated-result story); it is not restated in this pack even though v2's own section header
filed it under this pack's axis. This fold routes an ENVELOPE-line-routing question (which kind of
line is this, on the same stream as content) as a distinct axis from this pack's existing
REQUEST-routing question (which skill/tool answers this ask) — both are "routing," at different
grains, and this pack now answers both.
