# Config schema and prompt externalization

> A third axis alongside config-precedence-and-setup (which SETTINGS LAYER wins) and
> instruction-layering-and-precedence (which PROSE layer wins): how to STRUCTURE an agent
> harness's own tunable config and hand-authored instruction text in the first place — one typed,
> shared config schema instead of scattered loose params, and prompt prose in individually-
> editable files instead of hardcoded string literals. Grounded in one real, directly verified
> worked instance — the `agent-ui` repo's ADR-0135 — not sole authority; the pattern generalizes
> past that one repo. Verified directly, 2026-07-14.

## Describe agent config as one typed, shared schema — not scattered loose params

**Claim — once more than one consumer needs the same tunable knobs (a settings UI and a backend
turn-loop, say), the config belongs in ONE described, typed schema those consumers share, not as
independent loose function params or ad hoc constants each consumer half-invents on its own.**
Scattered params drift silently: a knob added to one consumer's signature has no shared shape a
second consumer can discover, validate against, or default consistently.

**Worked instance, verified directly:** before, `agent-ui`'s live-agent turn loop
(`packages/agent-ui/a2ui/tools/agent/produce.ts`) took its tuning knobs — `mode`, `model`, `k`
(retrieval top-k), `maxRounds` — as independent optional function params, and the mini-skill
selection cap was a hardcoded module constant (`mini-skills.ts:60`'s `DEFAULT_MINI_SKILL_CAP`)
threaded positionally into a call site, not a param at all. After ADR-0135, a single
`liveAgentConfigSchema(providers)` (`packages/agent-ui/a2ui/tools/agent/agent-config-schema.ts:69`)
describes every knob — `mode`/`model`/`k`/`maxRounds`/`miniSkillCap` — as one typed
`SettingsSchema`, each field carrying its own type, default, and validation bounds; a
`resolveProduceOptions(read, schema)` reader (same file, line 139) resolves a bring-your-own config
store against that SAME schema, fail-closed on an out-of-range or unrecognized stored value (never
let a bad value reach a live turn verbatim).

## The model/option list has exactly one source of truth — never a second hardcoded copy

**Claim — where a config field's valid options are already enumerated somewhere real (a provider
registry, a catalog, a manifest), the schema PROJECTS its options from that registry at
build/read time — it never re-lists them as a second, independently-maintained constant.** Two
hand-maintained lists of "the same" options drift the moment one changes and the other doesn't.

**Worked instance:** ADR-0135's `model` field derives its `SettingsFieldOption[]` list from the
real, already-validated `providers.json` registry (via `providers-config.ts`'s parsed
`ProvidersConfig`) — the exact registry a dev proxy actually allowlists against — rather than
hardcoding a parallel `SUPPORTED_MODELS`-shaped constant inside the schema itself. The same repo
also shows the CALIBRATED exception: a sibling consumer (`ui-agent-admin`'s
`agent-admin-schema.ts`) DOES hardcode its own small model list, deliberately — because that
consumer has no real registry to project from yet, and hoisting a list cross-package before a
second real consumer exists would be premature. The rule is "derive from the real registry once
one exists," not "never hardcode anything, ever" — a placeholder list is fine until the thing it
would otherwise duplicate actually exists.

## Hoist the shared schema to the lowest layer every consumer can reach

**Claim — in a layered/package architecture, a config schema (and its pure, side-effect-free
validation guards) that more than one layer needs belongs at the LOWEST layer every consumer
already depends on — not duplicated once per consumer, and not left stranded in whichever
consumer happened to define it first.** A schema stranded in an upper layer is invisible to a
lower or sibling layer that could otherwise reuse it (a strict one-directional dependency graph
can't reach upward), forcing either a duplicate definition or an architecture violation.

**Worked instance:** `agent-ui`'s own package DAG is `shared ← components ← a2ui ← app` (nothing
imports upward, enforced by real trip-wire tests). `SettingsSchema`'s pure types — and, per one of
ADR-0135's ruled forks, its pure `sanitizeNumber`/`sanitizeSelect`/`findField`/`initialValuesFor`
guards — used to live inside `@agent-ui/app` (the TOP of that chain), so the `a2ui` package's
Node-only agent tooling literally could not import them (an upward edge the DAG forbids). The fix
was a real hoist: `packages/agent-ui/shared/src/settings-schema.ts:17-98` now holds the pure types
(lines 17-54) + guards (lines 67-98), `@agent-ui/shared`'s own barrel gained its FIRST TypeScript
export to carry them, and the
original `app`-side module re-exports the same symbols so every existing app-side consumer kept
its import path byte-unchanged. The two things that made this safe to do were separating the
PURE half (types + guards, zero DOM dependency) from the half that was genuinely
layer-specific (the DOM/component-registry code that renders the schema into a real settings UI,
which stayed in `app` where it belongs) — hoist only what's actually pure.

## Externalize hand-authored instruction prose into files, not source-code string literals

**Claim — a system prompt's (or a prompt-injected idiom/skill library's) hand-authored PROSE
belongs in individually-editable files loaded at runtime, not hardcoded template-literal/string
constants inside source code.** Prose living as a code constant is hard to read, diff, and review
as prose — every wording tweak is a code change, and a long prompt buried in a `.ts`/`.py` file
reads worse than the same prose in a plain `.md` file a non-engineer could also edit.

**Worked instance:** before ADR-0135, `agent-ui`'s `system-prompt.ts` hardcoded ~9 large
template-literal constants (the emission grammar, several mode-scaled variants) and `mini-skills.ts`
hardcoded a 6-entry idiom registry as inline object literals. After, each piece of prose lives
under `packages/agent-ui/a2ui/tools/agent/prompts/*.md` (one file per constant, one frontmatter
file per mini-skill — `id`/`triggers` as a tiny `---`-delimited frontmatter block, the prose body
below it, deliberately mirroring this workspace's own `SKILL.md` frontmatter+body shape), loaded
via `readFileSync` at module load — safe specifically because that code is Node-only tooling never
bundled into a browser, a fact worth actually checking before assuming filesystem reads are
available at the point prose gets loaded.

## When a derivation already exists over the pre-externalized text, preserve it exactly — never re-derive by concatenation

**Claim — if the ORIGINAL hardcoded prose had a load-bearing derivation applied to it (e.g.
slicing one larger literal into an invariant sub-block reused everywhere, and a variant-scaled
sub-block), externalizing that prose into files must apply the SAME derivation to the loaded
string — never pre-split the source into separate fragment files and reconstruct the original by
concatenating them.** Reconstruction-by-concatenation reintroduces exactly the silent-drift risk
(a join separator off by one whitespace, a missing blank line, an ordering change) that a
byte-identity-by-construction derivation was built to eliminate in the first place.

**Worked instance:** `agent-ui`'s original `GRAMMAR` constant was sliced at runtime
(`GRAMMAR.slice(0, GRAMMAR.indexOf(marker))`) to derive an invariant `INTRO_AND_NOTE` block reused
across every prompt "mode," specifically so the default mode reproduced the literal `GRAMMAR`
value byte-for-byte "by construction, never by re-transcription" — a prior ADR's own stated
design principle, enforced by a module-load assertion that throws if the slice markers ever go
stale. Post-externalization, `system-prompt.ts:62` loads `GRAMMAR` whole from one file and
`system-prompt.ts:71-72` runs the SAME slice-based derivation against the loaded string; it was
never split into pre-sliced fragment files. The change was
verified, not assumed: a byte-identity gate asserts every mode's fully-composed prompt is
`.toBe()`-identical to a baseline captured from the ORIGINAL, pre-externalization source, committed
as a real fixture — proof the move was byte-neutral, not a claim taken on faith. One live
interpolation the original literal contained (a value drawn from a separate catalog module,
embedded mid-string) got a `{{PLACEHOLDER}}` marker in its file, filled from the same live source
after load — so the derived value stays genuinely live, not baked in stale at externalization
time.

## Small-scale calibration

A single-file harness with one hardcoded system-prompt string and no second consumer of its
config has no schema to hoist and no cross-file drift risk yet — none of this is worth building
until a SECOND consumer (a settings UI, a CLI, a second entry point) genuinely needs the same
config shape, or the prompt prose itself grows past what's comfortable to read as an embedded
string. Building the schema/hoist/file-split machinery preemptively, before a second consumer
exists, is the same premature-abstraction mistake as any other — see the calibrated
`SUPPORTED_MODELS` exception above for a real instance of "not yet, and that's fine."

## What this file does NOT cover

Which settings LAYER (global/project/user/local) wins for a given value — that composition
question is config-precedence-and-setup's own scope, a different axis from how one layer's schema
is itself structured. Which PROSE layer (global/project/session CLAUDE.md) wins — that is
instruction-layering-and-precedence. The provider/secret trust boundary a `providers.json`-style
registry sits behind — that is [[llm-provider-gateway]]'s own scope, not this file's.
