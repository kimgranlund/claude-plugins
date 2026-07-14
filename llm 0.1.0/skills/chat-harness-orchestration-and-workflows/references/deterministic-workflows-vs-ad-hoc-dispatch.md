# Deterministic scripted pipelines vs ad hoc agent dispatch

> Axis: when the shape of a multi-agent fan-out is known before anything runs, a pre-written
> script that owns the control flow is a distinct, reviewable-before-execution alternative to an
> agent deciding "now dispatch agent B" turn by turn. Grounded in this harness's own Workflow tool
> primitives (`agent()` / `parallel()` / `pipeline()`), a real shipped official-plugin workflow
> script, and real workflow scripts generated on this machine — all directly inspected, cited as
> worked instances, not the only valid shape.

## Two different tools for two different shapes of work

**Claim — an agent deciding, turn by turn, "now I should dispatch agent B" (this session's own
Agent tool, used repeatedly across a conversation) and a deterministic script that orchestrates
several agents from pre-written control flow (a Workflow tool) solve different problems, and
neither subsumes the other.** Ad hoc dispatch adapts to what the first agent actually found — the
shape of the work isn't knowable until then. A scripted pipeline is reviewable and versioned
*before any agent runs at all*, runs the identical fan-out/fan-in shape every time, and pays no
per-step model-deliberation latency between stages. **Failure mode on each side:** scripting a
shape you don't yet know forces premature structure onto discovery work; conversely, dispatching
turn-by-turn for a shape that was fully knowable in advance (audit these N files, review this diff
from 4 fixed lenses) pays repeated per-turn deliberation cost and produces a run that isn't the
same shape twice.

## The three primitives

**Claim — a Workflow script's control flow is built from three primitives:** `agent(prompt,
opts?)` spawns one subagent and returns its final text or schema-validated structured output;
`parallel(thunks)` runs an array of tasks concurrently behind a **synchronization barrier** — the
call does not resolve until every thunk has; `pipeline(items, ...stages)` streams items through a
sequence of stages **with no barrier between them**, so item A can be in stage 2 while item B is
still in stage 1 (wall-clock tracks the slowest single chain, not the sum of all items × all
stages). **Grounding — a real, official worked instance directly inspected on this machine:**
`plugins/marketplaces/claude-plugins-official/plugins/code-modernization/workflows/portfolio-assess.js`
— a shipped Anthropic-marketplace plugin workflow. Its `Survey` phase is exactly one `pipeline()`
call:

```js
const rows = await pipeline(
  systems,
  (sys, _orig, i) => agent(`Measure the legacy system at ${parentDir}/${sys}...`,
    { agentType: 'code-modernization:legacy-analyst', label: `survey:${sys}`, phase: 'Survey', schema: SYSTEM_SCHEMA },
  ).then(r => (r ? { system: systems[i], ...r } : null)),
)
```

one metrics agent per system, each independent, no cross-item dependency — the canonical
`pipeline()` case: per-item work, no stage needs to see a sibling item's result before proceeding.
The script itself notes *why* the aggregate math (a COCOMO-II complexity index) runs **after** the
pipeline returns, in the script, not inside any agent call: "computed here so every row uses the
identical formula" — the deterministic part of the job (arithmetic every row must apply
identically) belongs in code, not in a prompt an agent might interpret slightly differently per
item.

## The barrier — `parallel()` when the next step needs every result at once

**Claim — reach for `parallel()`'s barrier specifically when what comes after genuinely needs
cross-item context from *all* of the prior stage's outputs before it can proceed** — a dedup pass,
an aggregate score, or (the case below) a return value that is incomplete until every parallel
branch has reported. **Worked instance — a real generated workflow script inspected on this
machine** (`.claude/projects/-Users-kimba-Projects-nonoun-nonoun-color-tokens/.../workflows/
scripts/tokens-matrix-overrides-p3-wf_deb0d3d4-590.js`): a single `agent()` build step runs first
(a worktree-isolated implementation agent), and only once it reports `build.pushed === true` does
the script fan out four independent review lenses concurrently:

```js
reviews = await parallel([
  () => agent(reviewPrompt('engine + resolution correctness', ...), { label: 'review:engine', ... }),
  () => agent(reviewPrompt('export identity + override flow', ...), { label: 'review:export', ... }),
  () => agent(reviewPrompt('UI + headless-shim safety', ...), { label: 'review:ui', ... }),
  () => agent(reviewPrompt('persist + clamp + round-trip', ...), { label: 'review:persist', ... }),
])
return { build, reviews: (reviews || []).filter(Boolean) }
```

The barrier is load-bearing here: the script's final `return` is a single object carrying `build`
plus *all four* review verdicts together — there is no meaningful partial return with only two of
four lenses done, so `parallel()`'s wait-for-all behavior is exactly the right primitive, not an
accidental cost. Contrast this against a same-plugin script
(`destale-spec-docs-wf_66fce8c6-2a7.js`) that also uses `parallel()` over independent doc-group
audits with **no** cross-group merge afterward beyond `results.filter(Boolean)` — still a
legitimate `parallel()` use (the groups are independent, and the script wants them all done before
returning), but it is not exploiting the barrier for cross-item aggregation the way the four-lens
review does; know which reason you're reaching for it.

## Sequencing build then review is a serial dependency, not a fan-out

**Claim — when stage 2 depends on stage 1's concrete output (a review needs the build's branch
name and pushed status to exist first), that dependency is a plain `await`, not something
`pipeline()` or `parallel()` need to express** — those two primitives are for *fanning across
multiple independent items*, not for ordinary sequential steps within one script. **Worked
instance:** the same `tokens-matrix-overrides-p3` script runs `const build = await agent(...)`
to completion, checks `build.pushed`, and only then enters the `parallel()` block — a plain
sequential `await` handles the single-item, single-dependency case; reaching for a pipeline
primitive here would misname a two-step sequential script as a fan-out.

## Provenance note on the two generated-script examples

The `tokens-matrix-overrides-p3` and `destale-spec-docs` scripts are real, unedited Workflow
scripts found in this user's own Claude Code session history on this machine (a different project,
`nonoun-color-tokens`) — genuine evidence of the primitives' real behavior, but not an
officially-shipped example the way `portfolio-assess.js` (an Anthropic marketplace plugin) is.
Treat the marketplace script as the higher-provenance citation if the two ever appear to disagree
on a mechanic; both were read directly, not summarized from memory.

## What this file does NOT cover

The chain-of-command / escalation-loop pattern for when a coordinator IS the one making the
per-turn dispatch decision, rather than a pre-written script
(multi-agent-decomposition-and-chain-of-command.md) · the typed hand-off shape a single `agent()`
call's structured-output `schema` plays a similar role to (typed-handoff-contracts.md) — a
Workflow's per-agent `schema` option is that same "checkable, not narrated" discipline applied to
one call inside a script, rather than to a whole subagent's final report.
