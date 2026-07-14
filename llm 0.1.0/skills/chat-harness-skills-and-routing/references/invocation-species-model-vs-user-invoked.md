# Deciding model-invoked vs user-invoked skill invocation

> Axis: once a capability has earned being a skill (see authoring-a-skill-vs-a-hardcoded-feature),
> which of the two invocation dials it should carry — auto-discovered by the model against a
> description, explicitly invoked by the user as a slash command, or both at once. Grounded in
> `forge:skill-authoring-standards` (installed at
> `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.23.0/skills/skill-authoring-standards/SKILL.md`),
> the single most directly-inspectable primary source on this exact mechanism.

## The two dials and the three coherent species

**Platform fact — two independent YAML frontmatter fields govern invocation:**
`disable-model-invocation` (does the model consider this skill when matching the user's request
against the loaded description menu) and `user-invocable` (can the user reach it with an explicit
`/skill-name`). **Worked instance:** `skill-authoring-standards/SKILL.md:37-41` lays out the exact
three-way species table these two dials realize:

| Species | `disable-model-invocation` | `user-invocable` | Description's job |
|---|---|---|---|
| Procedural (a workflow with a contract — review, audit, migrate) | `false` | `true` | Trigger contract for auto-discovery |
| Knowledge (patterns, conventions, domain context — this skill's own species) | `false` | `false` | Trigger contract — the model is the only router |
| Command (side effects, phase entries, human-timed workflows) | `true` | `true` | Slash-menu documentation only — never enters model context |

**Claim — a skill can be BOTH model- and user-invoked at once (Procedural), or either alone
(Knowledge is model-only; Command is user-only).** There is no species that is neither: an
unreachable skill (both dials effectively off) is `SKILL.md:43`'s named misconfiguration, not a
fourth species — see below.

## Why declaring both dials explicitly matters

**Claim — omitting either dial couples the skill's behavior to whatever the current Claude Code
version defaults to, rather than pinning what was actually meant.** `skill-authoring-standards`
states this as a hard rule at `SKILL.md:45`: "Declare both dials on every skill, explicitly,
including at their defaults... The lint fails omission." **Failure mode this prevents:** a skill
authored against one version's defaults silently changes behavior on a version bump with no edit
to the skill itself — the kind of regression that is nearly impossible to trace back to "nothing
changed in this file."

## The corrected finding: `disable-model-invocation: true` also blocks preloading

**Platform fact, verified against live docs at authoring time (July 2026), explicitly flagged as
correcting an EARLIER, now-falsified belief:** `skill-authoring-standards/SKILL.md:43` states
"`disable-model-invocation: true` blocks subagent preloading" (and scheduled-task firing, from
v2.1.196+) — not merely hiding the skill from the auto-discovery menu, as an older understanding
had it. **Consequence:** the state most people reach for when they want a skill "available as a
library, not auto-triggered" — both dials off — actually makes the skill unreachable by ANY
path except a raw file read: not the menu, not auto-discovery, and not a `skills:` preload list
either. `SKILL.md:43` names this plainly: "a misconfiguration unless a future release documents
a role for it." **The species table above is exhaustive for a REASON** — a skill meant to be
preloadable into a subagent must be the Knowledge species (`disable-model-invocation: false,
user-invocable: false`), never the both-off state.

## Choosing among the three in practice

**Claim — the choice is a direct read of the content, not a separate decision:** a workflow with
an explicit contract (steps, a done-condition, an output shape) that a user would ALSO plausibly
want to invoke directly by name is Procedural (both dials on); a pattern catalog with no actor to
command — this very skill is an instance — is Knowledge (model-only, since prose the model should
consult on a matching question has no reason to appear in a human-facing slash menu); a workflow
with side effects, or one whose timing only a human should decide (a deploy, a migration cutover)
is Command (user-only, `disable-model-invocation: true`, since a model-triggered side effect a
user didn't ask for this turn is the failure mode a Command dial exists to prevent).

**Failure mode this prevents (species/dial mismatch):** the standard's own enforcing lint,
`skill_lint.py:209-210` (same `forge` 1.23.0 install, rule `W5`), names a specific, checkable
instance — a "knowledge-noun head with `user-invocable` left true" is flagged because "knowledge
species is model-only." A knowledge pack (a noun-headed name, no actor, no side effects) left
reachable by slash command invites a user to "invoke" something that was only ever meant to be
consulted — the dial should say what the content actually is.

## What this file does NOT cover

Deciding WHETHER a capability should be a skill at all versus a hardcoded, always-standing
instruction or hook — see authoring-a-skill-vs-a-hardcoded-feature. How a request among several
model-invocable skills gets routed to the correct one, and how that routing is tested with an
adversarial eval corpus — see description-routing-and-adversarial-evals. The repo-structural
standard for writing the SKILL.md file itself once a species is chosen (frontmatter shape, body
budgets, per-species templates) — `skill-authoring-standards` directly, where installed.
