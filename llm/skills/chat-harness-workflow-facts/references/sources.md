# Sources — provenance for the orchestration/workflow claims

This pack teaches a PATTERN, not one team's implementation — each claim is grounded in one of two
kinds, and the reference files say which for each claim.

## Claude Code's own Agent/Workflow tool mechanics — a platform fact, verify against current docs if stale

Facts about how this harness's own dispatch primitives behave. These can drift as the tool
versions — if a claim here disagrees with the CURRENT tool schemas or docs, they win and this pack
needs repair.

- **The Agent tool's `subagent_type`, `isolation`, and `run_in_background` options** — a persona +
  tool-allowlist preset per subagent type, worktree isolation for a build seat, and sync-vs-async
  dispatch. Directly verifiable in-session: this exact reply was produced using the Agent tool
  whose own description carries the "Trust but verify" language cited in
  `typed-handoff-contracts.md`, and the roster of available `subagent_type` values (each with its
  own `(Tools: ...)` allowlist) is enumerable from the same tool surface.
- **The Workflow tool's `agent()` / `parallel()` / `pipeline()` primitives** — one subagent spawn,
  a barrier fan-out, and a no-barrier per-item stream, respectively. Corroborated by
  `~/.claude/plugins/cache/nonoun-factory/agent-ops/0.1.19/skills/agent-loops/references/
  composition.md` §6 (the substrate-adapter table's "Workflow tool (durable, resumable,
  scheduled)" row) independently of the worked examples below, and by direct inspection of two
  classes of real scripts (below). Verify against this harness's current Workflow tool
  documentation if this pack has aged — script authoring conventions (the `meta` export, `phase()`
  labeling, `agentType`/`schema` options) are the part most likely to move.

## The worked examples — real, shipped or generated instances (cited for concrete grounding, not sole authority)

**Official, marketplace-shipped —** highest-provenance worked instance:
`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-modernization/workflows/
portfolio-assess.js` — a `pipeline()` fan-out, one agent per surveyed system, with a deterministic
post-pipeline aggregation (a COCOMO-II index) computed in script code rather than inside any
agent's prompt, specifically so every row uses an identical formula.

**Real, generated on this machine, a different project (`nonoun-color-tokens`) —** genuine
unedited Workflow scripts found in this user's own Claude Code session history, cited as real
behavior but lower-provenance than the official plugin above:
- `.../workflows/scripts/tokens-matrix-overrides-p3-wf_deb0d3d4-590.js` — a serial `agent()` build
  step, gated on its `pushed` result, then a four-lens `parallel()` review whose barrier is
  load-bearing (the final return needs all four verdicts together).
- `.../workflows/scripts/destale-spec-docs-wf_66fce8c6-2a7.js` — a `parallel()` fan-out over
  independent doc-group audits, contrasted against the above as a barrier used for "all done before
  returning" rather than for cross-item aggregation.
- `.../workflows/scripts/author-engine-mcp-skills-wf_44374737-8e2.js` — a `pipeline()` with TWO
  stages per item (draft → adversarial review-and-revise), the two-stage-per-item shape
  `pipeline()` is built for.

**The `orchestration` plugin's five-seat delivery team**,
`/Users/kimba/Projects/nonoun/plugins/teamwork/`:
- `agents/team-lead.md` — the apex/chain-of-command seat: routing by task shape,
  sealed dispatch, the generator≠critic gate, the discovered-reality escalation loop.
- `agents/planner.md` — the design seat: decompose-before-author, "report, don't grade."
- `skills/fleet-rules/SKILL.md` — the solo-first null-unit doctrine this pack's chain-of-
  command file opens with.
- `README.md` — the recorded model/effort re-tiering by role (v0.7.0 changelog entry).

**Harness's `write-handoff` skill**,
`/Users/kimba/Projects/nonoun/plugins/harness/skills/write-handoff/`:
- `SKILL.md` — the eight-field block, in order, quoted verbatim in `typed-handoff-contracts.md`.
- `references/foundations.md` — the "verifiable, not narrative" and "consumer-as-critic" models.
- `scripts/handoff_check.py` — the mechanical H1 gate the block is checked against before any
  rubric judgment.

These examples are cited as PROOF each pattern works in a real, running system — not as the only
valid way to implement it. A consumer's own team may reasonably differ in seat names, script
authoring conventions, or file layout while still honoring the invariants named in each reference
file's "why this matters" claims.

## Boundary — layers owned elsewhere

This pack answers how MULTIPLE agents compose for one job; it does not restate its siblings. A
single skill's own trigger/description routing is [[chat-harness-routing-facts]]. Measuring or
logging what an agent run actually did (tokens, latency, tool calls fired) is
[[chat-harness-logging-facts]]. Designing the wiring itself for a specific project — which unit,
which frontmatter keys, `skills:` preloads — is that project's own fleet-rules seat or
skill, not this pack.

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`self-correct-feedback-design.md`, `settled-answer-state-law.md`, and
`model-declared-plan-vs-host-execution.md` were added from agent-ui#1115's "Scope-conformant
revision v2" comment (posted 2026-08-17T17:14:57Z), the litmus-filtered re-harvest of
`@agent-ui/a2ui` lessons kept to web-based virtual-chat-harness knowledge only. Lessons 1, 5, 6,
and 7 of that same v2 export were evaluated and SKIPPED here as hard dedup — already substantively
covered by [[llm-streaming-facts]]'s `validate-then-stream-self-correct.md` (1, 5) and
[[llm-gateway-facts]]'s `stateless-session-and-turn-model.md` (6, 7); they are not restated in
this pack even though v2's own section header filed them under this pack's axis.
