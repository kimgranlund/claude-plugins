# Authoring a capability as a skill vs a hardcoded feature

> Axis: when a chat-agent harness should expose a capability as a discoverable, load-on-demand
> skill versus baking it directly into the harness's own standing instructions or its
> always-loaded tool surface. Grounded in Claude Code's own skill-loading mechanics (a shipped
> platform mechanism, verify against current docs if stale-sensitive) plus a directly-inspectable
> primary source on the same mechanics: `forge:skill-authoring-standards` (installed at
> `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.23.0/skills/skill-authoring-standards/SKILL.md`).

## The load-on-demand shape

**Platform fact** — a skill is a directory carrying a `SKILL.md` (YAML frontmatter + markdown
body); the frontmatter's `description` field is the ONLY text weighed to decide whether the body
loads for a given turn, and the body itself enters context only on invocation, never eagerly.
**Worked instance:** `skill-authoring-standards/SKILL.md:16` states this directly — "the
**description is the API** — the only text that controls triggering; the **body is the
payload**" — and its physics table at `SKILL.md:23` gives the exact mechanism: "Description
listing budget | 1% of context window, shared by all descriptions; least-invoked dropped first."

**Failure mode this prevents:** a harness that instead hardcodes every capability into its base
system prompt or tool list pays that capability's FULL context cost on every single turn,
forever, whether the current request needs it or not — cost then scales with everything the
harness COULD do, not with what THIS turn actually needs.

## The same principle, one level down: tool catalogs

**Platform fact** — the identical load-on-demand shape applies to TOOLS, not just skills: a large
tool catalog can be held "deferred" (name-only) until a search-style lookup resolves the full
parameter schema for just the matched subset, instead of every tool's complete definition sitting
in context from turn one. **Worked instance, observed directly in this session's own
environment** (a live protocol state at authoring time, not a repo file — verify against current
Claude Code docs, since this is exactly the kind of mechanic that can change): this session's own
system-reminder listed tool names such as `SendMessage`, `WebFetch`, and `TaskCreate` as
"deferred," stating plainly "Their schemas are NOT loaded — calling them directly will fail with
InputValidationError," resolved on demand via a `ToolSearch`-shaped lookup. Same principle as a
skill's `description`-first loading, applied to tool schemas instead of skill bodies — load a menu
of names cheaply, pay the full definition's cost only for what's actually used.

## Deciding hardcode vs skill

**Claim — the deciding question is turn-frequency-independent-of-phrasing, not importance.** A
capability genuinely needed on nearly every turn, regardless of how the user phrases the request,
earns a standing instruction (or a hook, for anything that must be enforced rather than merely
suggested) — it isn't worth spending a trigger-match on something that's always relevant anyway.
A capability that's occasional, optional, or domain-specific earns a skill, because the cost of
NOT loading it on the turns that don't need it is exactly the point.

**Two design axes from the same source, worth naming explicitly:** `skill-authoring-standards`
(`SKILL.md:48`) draws a further distinction at "capability uplift" (Claude can't do the thing at
all, or not consistently, without the skill) vs "encoded preference" (Claude can already do each
piece; the skill only sequences them a particular way). Uplift skills earn detailed bodies;
preference skills earn brevity — state the sequence and stop. Neither of these is a case FOR
hardcoding; both are cases for a skill, just at different lengths.

## Failure catalog reversed — skill-ifying something that needed to be standing

A skill's trigger is probabilistic, never guaranteed: model-invocation depends on the router
matching the CURRENT description menu against THIS turn's actual words. `skill-authoring-standards`
(`SKILL.md:63`) names the documented bias explicitly as "under-triggering, not over-triggering." A
behavior that
must hold on every single turn regardless of phrasing — a hard safety invariant, a "never do X" —
is a standing instruction or an enforced hook, not a skill that might simply not get picked the one
turn it mattered. See invocation-species-model-vs-user-invoked for the dial that governs a skill
that IS the right shape but is failing to trigger for a narrower reason (species mismatch, not a
hardcode-vs-skill mismatch).

## What this file does NOT cover

Choosing BETWEEN the two invocation species once something IS a skill — model-invoked automatic
discovery vs an explicit user-invoked slash command, and the subagent-preloading consequence of
each — see invocation-species-model-vs-user-invoked. How a request gets routed to the correct
skill among several once multiple exist, and how that routing is tested and re-measured over
time — see description-routing-and-adversarial-evals. Layering standing instructions and enforced
guardrails across a whole harness once something HAS been decided to be standing rather than a
skill ([[chat-harness-instructions-and-guardrails]]). Composing multiple skills, tools, or
subagents into a multi-step workflow ([[chat-harness-orchestration-and-workflows]]).
