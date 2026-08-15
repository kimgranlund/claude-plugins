# Config precedence and reproducible setup

> Two adjacent axes in one file (both thin enough to share): which layer of STRUCTURED settings
> (not prose CLAUDE.md — that is instruction-layering-and-precedence) wins for a given value or
> hook, and how a harness or extension installs/updates reproducibly. Grounded in this session's
> own real, currently-loaded settings stack plus the `nonoun-plugins` workspace's real install
> sequence — both verified directly, 2026-07-13.

## Config precedence — settings files over duplicated prose

**Claim — a harness's configuration (model choice, permissions, env vars, which extensions are
active) belongs in structured, layered settings files, not restated as prose in a CLAUDE.md or
system prompt:** structured config is machine-read, mergeable, and diffable; the same fact stated
in prose drifts the moment the file it's describing changes underneath it. **Worked instance,
verified directly, this session's real stack:** `/Users/kimba/.claude/settings.json` (global,
user-scoped) sets `model: "fable"` (line 5) and `effortLevel: "high"` (line 60) and registers a
`PreToolUse` hook matching `Read|Bash` (lines 7-18) that applies across every project this user
opens. *(Amended 2026-08-15: that global hook registration has since been retired — the user file
now carries `permissions.deny` Read rules for `.env`/credential paths instead, and no `hooks` key.
The layering claim itself is unchanged; only this instance moved layers.)* `/Users/kimba/Projects/nonoun/agent-ui/.claude/settings.json` (project-scoped, checked into
that one repo) registers its OWN `PreToolUse`/`PostToolUse` hooks (lines 2-32) that apply only
inside that repo. `/Users/kimba/Projects/nonoun/agent-ui/.claude/settings.local.json` (this one
contributor's personal, gitignored override, same repo) adds `env` vars
(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) and a
`permissions.allow` entry (lines 2-10) that apply only for this one person, layered on top of the
shared project file.

## Two different composition rules under one "precedence" name

**Claim — scalar settings and hook registrations do NOT compose the same way, and conflating them
is a real defect class:** a scalar value (`model`, `permissions.defaultMode`) follows a strict
precedence ORDER where the narrowest scope that sets it wins outright, replacing wider scopes'
values; a hook registration instead MERGES additively across every scope that registers one — "hooks
from enterprise, project, user, local, and plugin scopes merge additively — everything that
matches runs; nothing overrides" (`harness/skills/hook-writing-rules/SKILL.md:32`,
cited fully in deterministic-rules-vs-prompted-guidance). Concretely, in the stack above: the
global `dotenv-guard.py` (`Read|Bash`) and the project's `adr-status-guard.py`/`
bundle-size-reminder.sh`/`css-comment-guard.py` (`Edit|Write`) ALL fire in that repo — none
silently disables another — *(amended 2026-08-15: `dotenv-guard.py` was retired that day in favor
of user-scope `permissions.deny` Read rules, so the live worked instance is now the project-scope
hooks alone; the additive-merge mechanism claim stands as quoted)* — while a scalar like `model` takes whichever single value the narrowest
scope that sets it declares. **Platform fact (verify against Claude Code's current settings
documentation, since this is exactly the kind of table that drifts across versions):** the
documented precedence order for scalar values runs enterprise-managed policy > CLI arguments >
local project settings > shared project settings > user settings, narrowest-wins.

## Route a "whenever X, do Y" ask to settings, never to memory

A request phrased as an automated standing behavior ("from now on, block edits that do Z",
"every time a plugin ships, remind me to bump the version") is a settings/hook change, never
something a prose instruction or a memory note can reliably fulfill on its own — the harness
executes hooks; prose is read and can be skipped. **Observed-harness-behavior citation** (this
session's own available-capability listing, not a plugin-authored file this session could open by
path — a BUILT-IN capability of the product itself, per `sources.md`'s trust-class split): this
environment's own menu names an `update-config` capability described as configuring "the Claude
Code harness via settings.json" — exactly this class of edit (permissions, hooks, env vars), never
papering over the request with a note.

## Reproducible bootstrap — one versioned install path, not a hand-copy

**Claim — a harness or extension should install and update through exactly one reproducible,
versioned command sequence, so a second machine or a new collaborator ends up identical to every
existing install, never through copying files by hand.** **Worked instance, verified directly:**
`/Users/kimba/Projects/nonoun/plugins/README.md`'s real Install section: register the
distribution once (`claude plugin marketplace add kimgranlund/claude-plugins`), then install each
wanted unit by name (`claude plugin install <name>@nonoun-plugins`) — opt-in per plugin, so a
consumer only pays the routing/context cost of what they actually use. The same file names the
non-reproducible alternative explicitly, scoped to development only: `claude --plugin-dir
"/path/to/a/working/copy"` — for iterating on a plugin's own source, not for consuming a
released one. After install or update, the documented next steps are `/reload-plugins` then, into
an existing large skill library, `/doctor` — because "descriptions share a 1%-of-context listing
budget across everything installed," so a stale or duplicated install silently taxes every other
skill's own trigger reliability, not just the new one's.

**Why the version is the actual reproducibility key:** `/Users/kimba/Projects/nonoun/plugins/CLAUDE.md`'s
own invariant: "Never re-ship a version — the version is the update cache key; bump every change."
A bootstrap sequence is only as reproducible as its version discipline — an unversioned or
same-versioned re-release means some installs never receive the update at all, silently.

## Small-scale calibration

A minimal, single-machine harness's entire "bootstrap" may be nothing more than "clone this repo,
export two env vars" — that is a completely valid, complete setup story at that scale, and does
not need a marketplace/versioned-plugin system invented to justify itself. The added machinery
above earns its cost only once more than one person or machine must independently reproduce, and
later re-sync with, the same setup as it evolves.

## What this file does NOT cover

Prose instruction layering (global/project/session CLAUDE.md content) — a different mechanism
from settings-file layering even though both compose by scope
(instruction-layering-and-precedence) · a hook's own CONTENT and whether a given rule deserves one
at all (deterministic-rules-vs-prompted-guidance) · whether a config value like
`permissions.allow` is itself standing in for a risk-tier decision made once at setup time rather
than re-asked per call (action-risk-tiers-and-confirmation-gates).
