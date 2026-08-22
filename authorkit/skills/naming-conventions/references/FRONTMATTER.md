# Frontmatter — schema, relations, policy, grants, provenance

Frontmatter is the authoring surface for everything the tooling reads.
**Every field in the schema is validated; no field enters the schema unless
something reads it.** Fields nothing validates are prohibited, not optional.
This posture holds for commands and skills; agents carry a common-but-not-
schema-enforced tier alongside it — see the Invocation policy and Provenance
caveats below (ADR-0025).

## Identity (required, all kinds)

```yaml
name: skills-audit          # canonical; == folder / file stem; parseable
kind: skill                 # command | skill | agent — must match directory
description: >              # the trigger contract (see skill-authoring
  Use when ...              # standards; not restated here)
```

**Agents (ADR-0025 D1):** `kind` is not a declared frontmatter field for
agents — it is decided by directory + name-parse (§5/§6) exactly as before,
never something an agent declares. Required for an agent is only `name` and
`description`; see the estate-wide-agent caveat under Invocation policy below.

## Relations (on the depending artifact — never a central registry)

```yaml
performs: skills-audit          # primary-production agents; must equal name minus -agent
                                 # (orchestrator agents carry no performs — ADR-0015 D4)
wraps: naming-audit             # commands; dual-access wrapper
requires: [naming-conventions]  # any kind; "must exist and be available"
```

One authority per fact. The estate graph is compiled from these fields.
`performs` is redundant with string arithmetic by design — the redundancy is
the check; a rename touching one side fails loudly. `requires` is the single
dependency edge: whether the dependent invokes the target's procedure or
consults its references is body content, not metadata.

Graph checks: every endpoint exists; `performs` arithmetic holds; `wraps`
targets a model-invocable skill; `requires` graph is acyclic.

## Invocation policy and tool grants (agents; mutating commands; skills)

```yaml
# agents
autonomous_write: false     # fail-closed default; report-only
context: isolated           # isolated | inherited
tools: Read, Glob, Grep, Bash(python */scripts/validate.py *)

# commands
mutates: true
confirm: required           # human gate; allowlist is the only exception
allowed-tools:
  - Read
  - Edit
  - Bash(git mv *)

# skills — the Claude Code invocation dials, both mandatory, always explicit
disable-model-invocation: false   # true blocks agent preloading outright — verify
                                   # nothing cites this skill before setting it true
user-invocable: false              # true if a user may type this skill's name directly;
                                   # false is the norm here — a `wraps:` command is the
                                   # deliberate user-facing surface instead
```

Rules (all validated):
- `mutates: true` ⇒ `confirm: required` unless allowlisted.
- Agents lacking `autonomous_write` fail closed (treated false).
- **Coherence:** `autonomous_write: false` ⇒ no Edit/Write/unscoped Bash.
  `mutates: true` ⇒ a write-capable grant exists; `mutates: false` ⇒ none.
- `Bash` grants are always scoped patterns, never blanket.
- Net effect: the estate's mutation topology is grep-decidable from
  frontmatter alone.

**Agents, estate-wide (ADR-0025, 2026-08-21 — supersedes ADR-0011 §8):**
`performs`, `autonomous_write`, and `context` above are NOT part of the
estate-wide agent schema. Measured 2026-08-21 across every agent in this
workspace (40 files, one plugin's own dogfooding copy excluded): 39/40
carry none of `performs`/`autonomous_write`/`context` — `performs`'s
relation is already checked structurally from the name itself (§5's parse),
and the platform's own dispatch mechanics (tool grant, fresh-context vs.
fork) already express the distinction `autonomous_write`/`context` would
restate. Required for an agent, estate-wide: `name`, `description`. Common,
not schema-enforced: `model`, `tools`, `effort`, `skills` (an agent's
preloaded skill dependencies — the real analogue of `requires`), `color`,
`disallowedTools`. `performs`/`autonomous_write`/`context` remain valid
ONLY as authorkit's own internal `schema_scope: "full"` dogfood
(`estate-audit-agent.md`) — a deliberate single-plugin convention, not
estate law.

## Provenance (required, all kinds — commands and skills; agents, authorkit-internal only)

```yaml
author: kim                 # ∈ AuthorRegistry in the manifest
created: 2026-08-13
last_updated: 2026-08-13    # staleness input; may not postdate last git touch
review_after: 180d          # optional override of the estate default
```

Staleness past the review window is a warning tier — stale files are drift's
incubation stage.

**Agents, estate-wide (ADR-0025 D3):** this whole provenance block —
`author`/`created`/`last_updated`/`review_after` — drops out of the
estate-wide agent schema. Zero adoption outside authorkit's own
`schema_scope: "full"` self-dogfood; the staleness-tracking rationale is
reasonable but was never wired to anything outside that one plugin's own
validator. Commands and skills are unaffected — this caveat is agents-only.

## What stays out

`version` (git + plugin.json are the version authorities), `tags` (a parallel
folksonomy forks the routing surface), free-form `notes` (body content). New
fields enter by manifest PR, like lexicon entries.
