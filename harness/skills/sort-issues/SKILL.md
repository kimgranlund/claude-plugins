---
name: sort-issues
description: >-
  Runs the standing issue-sorter agent on demand against this repo — a plain intake sweep, or a
  specific instruction (approve/deny a held item, answer the first-run roster or GitHub-MCP-offer
  interview). Shows the agent's operating-contract banner before the first confirmed dispatch and
  runs the REQ-011/REQ-013 interview here when the agent's report surfaces one pending. Run
  /sort-issues [blank, or an instruction].
disable-model-invocation: true
user-invocable: true
argument-hint: "[blank for a sweep | an approve/deny instruction | an interview answer]"
allowed-tools: ["Read", "Glob", "Agent", "AskUserQuestion"]
---

# issue-sorter

Dispatches the standing `issue-sorter` agent (`agents/issue-sorter.md`) for an on-demand run against
this repo, states its own operating contract up front rather than leaving it undocumented in a
file the human has to go find, and — because the agent has no `AskUserQuestion` tool of its own
(`agents/issue-sorter.md:69-70`) — owns running the first-run interview `spec-ticketing-watch-
triage.md` assigns to "the dispatching session," since on this path that session is this command's.

A skill and an agent sharing one literal name is a deliberate, first-of-this-kind pairing in this
workspace (a Skill-routed command dispatching an Agent-routed standing seat of the identical name),
recorded here so a later audit reads it as a ruling, not drift: `disable-model-invocation: true`
keeps this skill off every surface the model routes against, and the Agent tool's `subagent_type` namespace is
disjoint from the Skill tool's — the two never compete for a routing decision.

## Procedure

1. **Dispatch.** Call the `issue-sorter` agent (Agent tool, `subagent_type: "harness:issue-sorter"`),
   carrying `$ARGUMENTS` verbatim as the dispatch context — blank for a plain on-demand sweep, or a
   specific instruction (an approval/denial, a roster or GitHub-MCP-offer answer) exactly as the
   agent's own `<example>` blocks describe. This command never classifies or pre-validates an
   agent-owned instruction shape in `$ARGUMENTS` — that judgment belongs entirely to the dispatched
   agent.
2. **Show the banner** (text below) before relaying anything, whenever `.claude/ops/
   friendlies.json` is absent OR present with no confirmed roster recorded in its `policy` block
   (an unattended firing's REQ-011 evidence-only seed writes the file but records no confirmation —
   checking bare file existence would miss this and silently never show the banner to the human the
   disclosure exists for). Once a confirmed roster is on record, never show it again.
3. **Run the interview, if the report surfaces one pending.** The agent's report names REQ-011's
   roster interview and/or REQ-013's GitHub MCP offer as surfaced-but-unconfirmed exactly when no
   confirmed decision exists yet for either — this command runs the AskUserQuestion round FOR both
   in the same turn when both are pending (never two separate rounds), then re-dispatches the agent
   (step 1's same call) carrying the confirmed answer(s) as `$ARGUMENTS`, so the agent can record
   them per its own Procedure steps 7/8. If the report surfaces neither, skip straight to step 4.
4. **Relay.** Return the (possibly re-dispatched) agent's own final report unmodified. The banner
   and the interview round are the only content this command owns; everything else is the agent's
   report, passed through as-is.

## The banner

```
issue-sorter — standing intake/triage seat for this repo's features, bugs, tasks, issues, and PRs.

What it does: classifies, dedupes, and routes each item onto the resolved ticketing backend.
What it never does: edit source, merge a PR, or close anything beyond the ticket record — for ANY
author, trusted or not (REQ-012, spec-ticketing-watch-triage.md). Enforced by contract, not a
config flag — there is nothing to turn on or off here.
```

## Failure branches

- The agent's report surfaces the REQ-011/REQ-013 interview → this command runs it (Procedure step
  3), never defers it back to the agent — the agent structurally cannot ask (no `AskUserQuestion` in
  its own `tools`).
- A human asks to see the banner again after a confirmed roster is already on record → answer from
  the banner text above directly, inline; do not dispatch the agent for this — re-displaying it via
  a real dispatch is exactly the noise a one-time disclosure exists to avoid, and the ask carries no
  agent-owned instruction to pass through.
- The Agent tool dispatch itself fails to return (a tool error, not an agent-reported failure) →
  report the dispatch failure plainly; never fabricate an agent report to fill the gap.
- `.claude/ops/` itself doesn't exist yet (never run in this repo at all) → same as "no confirmed
  roster," step 2's banner fires; the directory is created by the agent's own first successful
  write, not by this command.

Done when the agent has been dispatched, the banner has been shown whenever step 2's condition is
met, any pending REQ-011/REQ-013 interview has been run and its answer carried on a re-dispatch, and
the agent's final report has been relayed unmodified. NOT done while a confirmed-roster check is
skipped in favor of bare file-existence, an interview surfaces in the report but goes unrun, or a
dispatch failure is reported as if the agent itself had returned a finding.
