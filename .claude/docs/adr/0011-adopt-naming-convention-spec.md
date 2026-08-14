---
doc-type: adr
id: adr-0011
status: accepted
ratified: by Kim, 2026-08-13 (in-session, session "PLUGINS")
date: 2026-08-13
owner: kim.granlund
supersedes: null
---
# ADR-0011 — Adopt the harness naming-convention spec as estate-wide naming canon

> ACCEPTED — ratified by Kim 2026-08-13. Originally a live conversation capture (session "PLAN", 2026-08-13). The headline
> ruling (D7) was made in-session by Kim and REVERSES this session's own earlier
> rulings (recorded in Context for the audit trail). All open rulings were closed
> in-session 2026-08-13; nothing in this ADR awaits a decision — only acceptance.
> On acceptance this ADR supersedes the *grammar* halves of ADR-0001 and ADR-0006;
> their enforcement discipline (symmetry, lint gates) carries forward.

## Context

Kim opened a naming-system exploration scoped to the whole estate: nonoun-plugins
plus adia-ui-kit-forge and adia-ui-kit-factory. The conversation first converged on
extending the incumbent nonoun grammar (`harness:naming-rules`, ADR-0006): fold
knowledge skills into `-facts`, admit a `wire` verb, keep person-word agents, and
run an ADR-0006-style rename campaign over the 25 adia skills. A fully-ruled
25-row verb-first rename map was drafted.

Then `~/Downloads/naming-convention-spec.md` ("Harness Artifact Naming Convention",
Draft v1.0 — home turf: the adia-eng/agentic-tools estate, per its exemption seeds)
was checked against that draft. Findings:

- **Mechanism-level agreement** — brand tokens banned; `-knowledge-base` rejected
  verbatim; closed governed lexicons; folder==name==frontmatter symmetry,
  mechanically validated; two-hop reference-index discovery; plugin prefix owns
  namespacing.
- **Surface-grammar opposition** — each system's canonical form is the other's
  reject row: verb-first `make-skill` vs object-first `skill-create`; verb-first
  skills vs nominal `{object}-{process}`; person-word agents (`skill-checker`) vs
  derived `{skill}-agent` heads; kind-audible `-facts`/`-rules` vs no
  content-pattern suffixes at all; ratified rename campaigns vs
  grandfather-and-burn-down. Litmus: `find-unused` conforms under nonoun grammar
  and sits verbatim in the spec's exemption list.
- Both estates co-install in one flat menu (measured in this session), so two
  grammars side by side would make shape non-informative for both.

Offered the reconciliation menu (nonoun grammar + spec machinery · spec grammar
wins · two estates two grammars), **Kim ruled: spec grammar wins** (2026-08-13,
in-session). Earlier in-session rulings this reverses: person-word agent shapes
(old D2), the `wire` registry verb (old D4 — survives as `wiring` ∈ ProcessLex),
the verb-first adia rename map (old D6), and the -facts landing spot for knowledge
skills (old D1 — its *negative* half, rejecting `-knowledge-base`, survives; the
spec rejects that suffix independently).

### Census (measured 2026-08-13)

nonoun estate: 7 plugins, 127 skills (33 `-facts`, 21 `-rules`, 73 verb-first
runnables), 28 person-word agents — 100% conformant to the OLD grammar, ~0% to the
spec grammar. adia-ui-kit estate: 25 skills (9 forge + 16 factory) on legacy
`adia-{topic}` names, 7 agents. The spec self-reports ~30% conformance on its home
estate.

## Decision

### D7 — The spec grammar is estate-wide canon (RULED 2026-08-13)

The naming-convention spec's grammar governs all three estates (nonoun-plugins,
adia-ui-kit forge+factory, adia-eng/agentic-tools): three kinds partitioned by
invoker; object-first commands with VerbLex terminals; nominal
`{object}-{process}` skills with ProcessLex terminals (looser nominal production
for reference-shaped skills); `{skill-name}-agent` derived agent names with the
orchestrator escape hatch; four lexicons in `naming.manifest.json`; the §5 parse;
`folder == name`; frontmatter as validated agreement, never tiebreaker.

### D8 — Migration follows the spec's own posture: grandfather + ratchet, no campaign

Per spec §10: every existing name across all three estates enters the `exemptions`
array verbatim (~155 nonoun members + 32 adia-ui-kit members + adia-eng's
non-conformers). The array may shrink and may never grow — CI diffs it. New mints
conform in full from day one. Renames retire exemptions opportunistically, when an
artifact is otherwise touched. The verb-first big-bang campaign this session
originally drafted is dead; ADR-0006-style campaigns are retired as a migration
instrument.

**Sub-ruling (RULED 2026-08-13): bootstrap wave.** The 25 adia-`{topic}` skills and
the adia agents get ONE deliberate rename wave as an explicit, ADR-sanctioned
exception to §10 — the debt that motivated this conversation is cleared while the
map is fresh, then the ratchet governs everything thereafter. This exception is
single-use; it ratifies no future campaign.

### D9 — Standards succession

On acceptance: `harness:naming-rules` (the SKILL.md and its five tests / shape
table / verb registry) receives a dated supersession note pointing at the spec.
**The spec lands as a plain document at `.claude/docs/spec/` in nonoun-plugins
(RULED 2026-08-13), with `naming.manifest.json` at the repo root** — not a
routable skill; agents reach it through the validator's failures and the doc tree,
accepted trade-off. **The validator is a greenfield build per spec §11 (RULED
2026-08-13)**; skill_lint's naming checks retire once it runs in both the
PostToolUse hook and the ship gate — enforcement never gaps, the stacks overlap
during transition. The verb registry's *governance pattern* (closed set, additions
by ratified event) continues as the manifest-PR gate. Old-D3 (brand prefixes die)
and old-D5 (plugin names stay put) carry forward unchanged — the spec
independently mandates both.

### D10 — Target-grammar map, adia forge + factory (informative until D8's sub-ruling)

Executed as D8's bootstrap wave. Lexicon seeds this map requires: ProcessLex +=
composition, wiring, scaffolding, selection, deployment, release, maintenance,
qa, catalog; ObjectVocab += a2ui, gen-ui, ssr, compatibility, primitive, demo,
screen, shell, host, site, package(s), project, app, surface, chart, table,
token, pattern, llm-client, site-docs.

Forge (9):

| current | target | note |
|---|---|---|
| adia-author | `primitive-authoring` | authoring ∈ ProcessLex |
| adia-a2ui | `a2ui-maintenance` | charter skill; maintenance names the dominant job |
| adia-llm-internals | `llm-client-maintenance` | |
| adia-release | `package-release` | release assigned to ProcessLex (disjointness: a command wrapping it uses run/ship ∈ VerbLex) |
| adia-deploy | `site-deployment` | |
| adia-dogfood | `demo-audit` | "dogfood" is unresolvable vocabulary either way |
| adia-gen-review | `gen-ui-review` | gen-ui registered as multi-token ObjectVocab entry; spelling normalized |
| adia-site-docs | `site-docs-authoring` | |
| adia-ssr | `ssr-compatibility` | reference-shaped, nominal production |

Factory (16):

| current | target | note |
|---|---|---|
| adia-orient | `app-planning` | |
| adia-compose | `screen-composition` | |
| adia-project | `project-scaffolding` | |
| adia-shells | `shell-selection` | |
| adia-host | `host-wiring` | old-D4's `wire` survives as the wiring process |
| adia-data | `data-wiring` | |
| adia-genui | `gen-ui-wiring` | |
| adia-llm | `llm-wiring` | |
| adia-migrate | `app-migration` | migration ∈ ProcessLex |
| adia-audit | `app-audit` | |
| adia-verify | `surface-qa` | qa ∈ ProcessLex (term-of-art) |
| adia-charts | `chart-selection` | answers "which component" — selection IS the process |
| adia-tables | `table-composition` | RULED over table-usage — reuses the composition head, no new lexicon entry |
| adia-tokens | `token-selection` | |
| adia-patterns | `pattern-catalog` | RULED — reference-shaped nominal; `catalog` joins the lexicon seeds |
| find-unused | (exemption) | already in the spec's own seed list; target if ever renamed: `unused-detection` |

Agents (6 → 7): `app-planner` → `app-planning-agent`, `screen-builder` →
`screen-composition-agent`, `component-author` → `primitive-authoring-agent`,
`release-builder` → `package-release-agent`, `a2ui-builder` →
`a2ui-maintenance-agent`, and — RULED 2026-08-13 — `framework-reviewer` SPLITS
into `demo-audit-agent` + `gen-ui-review-agent`: it performed two skills and the
spec's `performs` arithmetic requires exactly one per agent. Pure arithmetic over
seat economy, by ruling.

## Consequences

- The nonoun grammar (five tests, shapes-by-kind, verb registry) is superseded as
  canon; its 155 conforming names become the largest block of the exemptions
  array. What ADR-0006 called conformance becomes debt — by ruling, accepted
  knowingly.
- Kim's original opinion 2 in this session (person-word agent names) is
  overridden by this ruling; recorded here so the reversal is deliberate, not
  drift.
- The spec needs in-estate ratification work (its own §13): seed the four
  lexicons + ObjectVocab (D10's seed list is the starter), enumerate exemptions
  from live inventory across three estates, backfill frontmatter, build the
  validator. That is the real adoption cost — the machinery, not renames.
- nonoun's existing gates (skill_lint F9/A6, doc gates) keep running until the
  spec's validator replaces the naming checks; enforcement never gaps.
- `plugin:skill` invocation surfaces change only as exemptions burn down —
  consumers see a slow drift to spec names, never a flag-day break.

## Execution order (at acceptance)

All rulings are closed; what remains is execution, in dependency order:

1. Ratify this ADR (status → accepted).
2. Land the spec at `.claude/docs/spec/spec-naming-convention.md` + seed
   `naming.manifest.json` at the nonoun-plugins repo root (lexicons per D10's
   seed list; exemptions enumerated from the live three-estate inventory).
3. Build the greenfield validator (spec §11); wire it into the PostToolUse hook
   and the ship gate alongside skill_lint, then retire skill_lint's naming checks.
4. Dated supersession note in `harness:naming-rules` pointing at the spec.
5. adia bootstrap wave (D8/D10): rename PRs against adia-ui-kit forge + factory —
   frontmatter + directory + references move together; gen-ui-kit's AGENTS.md
   routing table and hooks are in-scope reference surfaces.
6. Exemption burn-down becomes a standing `harness_check` metric.
