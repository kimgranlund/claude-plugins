# authorkit — harness artifact governance: naming, frontmatter, layout, audits

A meta plugin used to refactor existing and author new skills/commands/agents against one
naming convention (ADR-0011, **accepted** 2026-08-13) — grammar, frontmatter schema, folder
layout, and migration tooling — plus a separate busy-work/over-specification audit. Dogfoods
its own spec: `skills/naming-audit/scripts/validate.py` validates this plugin clean against
itself with an empty exemptions array.

**Enabled** in this workspace's own `.claude/settings.json` (`enabledPlugins` carries
`"authorkit@nonoun-plugins": true`; issue #197 is CLOSED) — the earlier disable-here boundary
retired once the v0.10.1 reciprocal NOT-fences (issue #282) closed the
`naming-conventions` ↔ harness `naming-rules` collision that boundary existed to guard
against. `fix-old-names` (moved here from harness under #197/D9) routes normally in this
workspace along with the rest of authorkit's surface. (Paragraph repaired 2026-08-15, issue
#283 rider — the prior text still described the pre-#197 disabled state.)

All six original skills stay model-invocable, none user-invocable (issue #196's shipped
dials) — a user's on-demand surface goes exclusively through the thin identical-name command
wrappers in `commands/` (issue #235: the last two, `manifest-authoring` and `rename-planning`,
gained theirs 2026-08-14, closing the gap left after #227's `overhaul-planning` wrapper —
every one of the six now has a wrapper).

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/naming-conventions` | Knowledge skill | model-only | The naming grammar itself — productions, lexicons (VerbLex/ProcessLex/RoleLex/ObjectVocab), frontmatter schema, folder layout, migration rules. The single authority every other authorkit skill cites; has no procedure of its own |
| `skills/naming-audit` | Procedural skill | model-only | Runs `scripts/validate.py` over an estate's `naming.manifest.json`, judges findings (violation/exempt/frontmatter-disagreement/orphaned relation), reports the exemption burn-down. Read-only — reports, never renames. Wrapped for user-invocation by `commands/naming-audit` |
| `skills/rename-planning` | Procedural skill | model-only | Plans one artifact rename: proposes the conforming target name and enumerates the full blast radius (invocation strings, relations, hooks, workflow configs). Produces a typed plan; never executes |
| `skills/manifest-authoring` | Procedural skill | model-only | Seeds or edits an estate's `naming.manifest.json` — lexicon proposals, ObjectVocab registration (anti-ambiguity gate), AuthorRegistry, exemptions enumeration/retirement |
| `skills/bloat-audit` | Procedural skill | model-only | Runs `scripts/measure.py` over any markdown corpus, judges busy-work/ceremony/restatement findings against `references/CALIBRATION.md`. Read-only — reports, never rewrites. Wrapped for user-invocation by `commands/bloat-audit` |
| `skills/pattern-audit` | Procedural skill | model-only | Compiles a caller-supplied literal pattern or natural-language instruction into labeled probes, runs `scripts/scan.py`, and optionally judges each match (`verdict: hit \| false-positive`). Emits a flat, structured match dataset (`id`/`file`/`line`/`col`/`match`/`context`/`kind` + totals) for a downstream step to consume — review, bulk edit, migration, or overhaul-planning's Phase 0. Read-only — reports, never rewrites. Distinct from naming-audit's grammar axis, bloat-audit's busy-work axis, and fix-old-names' retired-name-reference axis. Wrapped for user-invocation by `commands/pattern-audit` |
| `skills/overhaul-planning` | Procedural skill | model-only | Generates a phased estate-overhaul plan for a target spanning many members: composes naming-audit + bloat-audit + harness's check-routing/plan-plugin-split (Phase 0 steps 1–2, always) + a conditional fifth `pattern-audit` sweep (Phase 0 step 3, only when the campaign's charter names a pattern none of the other four instruments owns — issue #286), a per-member kill-switch design doc answering all four reorganization axes — where-it-lives, species, merge/split-candidate nomination (soft-mentions `plan-skill-merge`/`plan-skill-split`), and procedure-vs-knowledge with a context-optimization tier (`keep-inline`/`move-to-references`/`extract-to-pack`/`retire`, anchored to bloat-audit's own measured numbers) — any of which can come back "no move"/"no candidate"/"keep-inline" (#197's precedent, extended 2026-08-14 issue #229), then waved ticket seeds with Blocked-by edges (Phase 2, seed list only — never auto-minted, per this estate's capture, confirm, then build discipline). Generates only: never executes a move, rename, merge, split, or build. Wrapped for user-invocation by `commands/overhaul-planning` |
| `skills/overhaul-execute` | Procedural skill | model-only | The DRIVES half of the `overhaul-planning` pair (issue #241, enforcing #238's E1 sign-off): discover+scope-confirm, measure, plan, then gated wave execution (rename-planning → rename-execute per rename, `harness:reshape-skill` for merge/splits, `teamwork:build-lead` dispatches for moves/builds, `fix-old-names` sweeps after every rename wave) — under three live-user gates (scope, Gate A, Gate B), never self-approving. Extracted 2026-08-14 out of what shipped in PR #240 as a standalone command; exists as a skill at all only because of the reverse-wrapper grammar amendment below. Wrapped for user-invocation by `commands/overhaul-execute` |
| `skills/estate-audit` | Reference skill | model-only | The audit-family index (issue #293/#272) — no procedure of its own; names the four instruments (naming/bloat/attention/pattern) and the `instrument` parameter `agents/estate-audit-agent` takes. The backing skill for that agent's primary ADR-0011 naming production |
| `agents/estate-audit-agent` | Subagent | dispatch-only | Batch estate-audit sweeps across N estates/plugins/corpuses in an isolated context, parameterized by one `instrument` (naming/bloat/attention/pattern), one aggregated report. Replaces `naming-audit-agent`/`bloat-audit-agent`/`attention-audit-agent` (issue #293, executing #272's checker-seat consolidation ruling) |
| `commands/naming-audit` | Command | user-only (`/naming-audit`) | Thin user-invocable wrapper over `skills/naming-audit` — skills aren't user-invocable, this is the on-demand surface |
| `commands/bloat-audit` | Command | user-only (`/bloat-audit`) | Thin user-invocable wrapper over `skills/bloat-audit`, same reason |
| `commands/pattern-audit` | Command | user-only (`/pattern-audit`) | Thin user-invocable wrapper over `skills/pattern-audit`, same reason |
| `commands/overhaul-planning` | Command | user-only (`/overhaul-planning`), `confirm: required` | Thin user-invocable wrapper over `skills/overhaul-planning` — this one writes the plan doc + ticket-seed list to disk, so it gates on confirmation before writing, unlike the two read-only audit wrappers above |
| `commands/manifest-authoring` | Command | user-only (`/manifest-authoring`), `confirm: required` | Thin user-invocable wrapper over `skills/manifest-authoring` — mutating (seeds/edits the target estate's `naming.manifest.json`), so it gates on confirmation before writing, same posture as `rename-execute` |
| `commands/rename-planning` | Command | user-only (`/rename-planning`) | Thin user-invocable wrapper over `skills/rename-planning` — plan-only, never executes, same read-only posture as `naming-audit`/`bloat-audit` above |
| `commands/rename-execute` | Command | user-only (`/rename-execute`) | The estate's single mutation point — applies one `rename-planning` plan atomically (`confirm: required`), verifies via the validator, reverts whole on any new error |
| `commands/exemption-retire` | Command | user-only (`/exemption-retire`) | Opportunistic one-step chain: rename-planning → confirm → rename-execute → manifest shrink, for an artifact already being touched |
| `commands/overhaul-execute` | Command | user-only (`/overhaul-execute`), `confirm: required` | Thin user-invocable wrapper over `skills/overhaul-execute` (issue #241 — was a standalone command through PR #240/v0.8.0; the reverse-wrapper grammar amendment let the procedure move into a skill, this command adds nothing). The DRIVES counterpart to `overhaul-planning`'s GENERATES |
| `skills/fix-old-names` | Command skill | both (`/fix-old-names`) | Moved from harness 2026-08-14 (issue #197, ADR-0011/D9). Consumer-side rename migration: sweeps a repo that INSTALLS these plugins for references to retired names and rewrites the live ones, from the derived `renames.json`. Report-first, historical records left byte-identical, ambiguous names escalated to a human, filenames never rewritten |
| `hooks/hooks.json` (`PostToolUse`) | Hook | automatic | Three siblings on every `Write`/`Edit`, each self-scoping before doing any real work: `naming-audit/scripts/validate.py hook` (no-ops cleanly when the target estate has no manifest — governance is opt-in per estate); `attention-audit/scripts/collide_hook.py` (issue #294 — fires only on a `SKILL.md` whose `description:` changed, prints an advisory collision finding, never blocks); `attention-audit/scripts/trend_hook.py` (issue #294 — fires only on a plugin's own version bump, appends that plugin's row to `attention-trend.csv`) |
| `skills/naming-audit/scripts/validate.py` | Script | invoked by naming-audit | Deterministic checks only: name grammar, folder layout, frontmatter schema, relation graph, policy/capability coherence, provenance. `selftest` mode proves schema/grammar/lexicon counters bite. Gained `--scope {full,grammar}` 2026-08-14 (issue #197): `grammar` gates only naming-grammar findings, leaving the broader structural/provenance checks informational — how this validator wires into an estate (nonoun-plugins) that hasn't adopted the full frontmatter schema without failing on hundreds of non-naming findings |
| `skills/bloat-audit/scripts/measure.py` | Script | invoked by bloat-audit | Deterministic measurement: body size, phase-heavy headings, oversized Failure sections, dense descriptions, cross-file near-duplicate paragraphs. `selftest` mode proves flag/duplicate/empty-target counters bite |
| `skills/pattern-audit/scripts/scan.py` | Script | invoked by pattern-audit | Deterministic sweep: literal, labeled regex + glob probes in, a flat match dataset out — instruction-blind, all NL-compilation and judgment lives in the skill. `selftest` mode proves match/label/multi-probe/glob/skip-dir/binary/invalid-regex/id-stability/verdict-line counters bite |
| `scripts/fix_old_names.py` | Script | CLI + selftest | Moved from harness 2026-08-14 (issue #197). Classifies each stale-name hit LIVE (rewrite) vs HISTORICAL (byte-identical) vs AMBIGUOUS (escalated); report-only by default, `--write` applies, exit 1 on live hits. `derive` regenerates `renames.json` from git rename detection |

## Invocation dials

The five original skills are all model-invocable (`disable-model-invocation: false`) and none
are user-invocable (`user-invocable: false`) — every one of the five now carries a thin
identical-name command wrapper as its user-facing surface: `commands/naming-audit` and
`commands/bloat-audit` were the original two; `commands/manifest-authoring` and
`commands/rename-planning` (issue #235, 2026-08-14) close the gap for the remaining pair,
which until then were consulted only by the model, mid-workflow, via `naming-audit`'s own
hand-off step (or, for `rename-planning`, `rename-execute`'s own precondition step) — never
invocable directly by a user typing a skill name. `fix-old-names` (moved in
2026-08-14, issue #197) is the one exception — both dials `true`, since it carries its own
`/fix-old-names` invocation directly rather than through a thin wrapper command, unchanged from
its harness incarnation. `estate-audit-agent` (issue #293, replacing the three single-instrument
agents that used this pattern one-for-one) cites its four instrument skills via `requires:`
(authorkit's own existence-edge convention, not the `skills:` preload field) — every cited skill
therefore carries `disable-model-invocation: false`, since that dial blocks preloading outright
wherever it IS the real preload mechanism (verified 2026-08-13, PR #217's critic chain);
`estate-audit`, the agent's own backing skill for ADR-0011's primary naming production, carries no
procedure but the same dial pair. `overhaul-planning`
(2026-08-14, issue #225) follows the same wrapper pattern as `naming-audit`/`bloat-audit`:
model-invocable, not user-invocable, with `commands/overhaul-planning` as its identical-name
wrapper (the validator's wrapper-production exception — no VerbLex terminal required when a
command's name equals its wrapped skill's name). `overhaul-execute` (2026-08-14, issue #241)
joins the same dial pattern via a DIFFERENT grammar production — its terminal token (`execute`)
lives in `VerbLex`, not `ProcessLex`, so the object-process wrapper exception above doesn't
apply; the reverse-wrapper amendment (`.claude/docs/spec/spec-naming-convention.md` §14.1) is
what licenses this specific name shape, and it applies only because `commands/overhaul-execute`
exists in the same plugin root.

## Version ledger

v0.17.0 · 2026-08-16 · ADR-0015 follow-on (issue #433): the orchestrator agent production
(`{scope}-{role}`) no longer requires the `-agent` tail — `naming-audit/scripts/validate.py`'s
`Grammar.parse` agent branch tries a bare scope-role name (terminal ∈ RoleLex) alongside the
existing `-agent`-stripped path, both spellings resolving scope against a new
`ObjectVocab ∪ ProcessLex` pool (`resolve_orchestrator_scope`, deliberately narrower than
ADR-0014's `-rules` union — no TopicLex); `RoleLex` gains a D3 disjointness check against that
same pool. Selftest gains 6 fixtures (positive ObjectVocab/ProcessLex scopes, legacy-spelling
regression, bare non-role negative, skill-shaped negative, D3 manifest-collision negative).
Repo-root `naming.manifest.json`: `build` registered in `ObjectVocab` (needed for
`build-leader`); `$schema_note` gains a dated sentence; exemptions unchanged (124 → 124 — this
change admits nothing by exemption). `naming-conventions`'s GRAMMAR.md/SKILL.md/MIGRATION.md/
FRONTMATTER.md and `.claude/docs/spec/spec-naming-convention.md` (§3/§3.3/§4 AC-008/§5/§12,
new §14.4) updated to match. ADR-0011 itself untouched (append-only); the supersession is
recorded in ADR-0015's frontmatter alone.

v0.16.0 · 2026-08-16 · New `repo-audit` command+skill (issue #407) — one umbrella audit sweep:
Phase-0-style discover/scope-confirm (reusing `overhaul-execute`'s own scan, one
`AskUserQuestion` round), fans out all five instruments (`naming-audit`/`bloat-audit`/
`attention-audit`/`pattern-audit`/`doctrine-audit`, batched via `estate-audit-agent` over the
same >3-estates/>40-members threshold), adds `harness:check-routing` +
`skill-checker`/`agent-checker` FLOOR sweeps as cross-plugin axes where harness is installed
(absent → named `UNMEASURED`), and renders ONE verdict-first 🟢/🟡/🔴 roll-up per estate per axis.
Structurally read-only — its tool grants carry no `Write`/`Edit`/`Bash(git *)`. **Naming note**:
the originating ticket proposed `/audit-repo`; the ADR-0011 grammar check (this same plugin's own
`validate.py`) rejects that order — a command's terminal token must resolve in `VerbLex`
(`audit` sits only in `ProcessLex`), so `audit-repo` matches neither the object-verb command
production nor the object-process skill production. `repo-audit` (object=`repo`, tail=`audit`)
conforms via the same object-process wrapper production `naming-audit`/`bloat-audit`/
`estate-audit` already use — both `repo` and `audit` are already-registered vocabulary
(`object_vocab`/`process_lex`), so no manifest change was needed. Minor bump: new capability,
fully additive, no existing command/skill contract reshaped.
v0.15.1 · 2026-08-16 · `overhaul-execute`: wire `pattern-audit` + `doctrine-audit` into Phase 1
MEASURE and `doctrine-audit` re-run into Phase 6 PROVE (issue #408). Phase 1 gains the same two
conditional instruments `overhaul-planning`'s Phase 0 already composes (steps 3-4, cited not
restated) — doctrine-audit fires whenever the estate carries a `doctrine.manifest.json`,
pattern-audit fires when the campaign charter names a pattern none of the other four instruments
owns; both batch via `estate-audit-agent` under the existing >3-estates/>40-members threshold,
alongside naming/bloat/attention. No-manifest/no-pattern estates report those axes `absent`,
mirroring Phase 6's existing routing-report `absent` handling. Phase 6 re-runs `doctrine-audit`
on every wave-touched estate that had a Phase 1 baseline and diffs against it — new findings are
Gate-B-adjacent evidence named in the roll-up by estate and edge type, whether or not Gate B
fired. `requires` and the Bash allowlist (`scan.py`, `sweep.py`) extended to match. Contract-
extending, backward compatible (no existing Phase 1/6 step removed or reshaped) — patch bump,
mechanical wiring of two already-shipped instruments, no new capability of its own.
v0.15.0 · 2026-08-16 · `doctrine-audit` two-issue follow-up (#395, #396) on the v0.14.0
instrument. **#395:** `doctrine.manifest.json` extended from 5 to the full 8 edges
(D01–D08) — the 2026-08-16 team/coordination-surface review's source transcript surfaced
findings 6–8, recovered verbatim: D06 (`verbatim-line`/require) catches make-agent's
forge skeleton missing a `naming-rules` pointer (ADR-0006 supersession) — live-verified
firing against current `harness/skills/make-agent/SKILL.md`; its companion judgment
nuance (Gate A2's flat "≤ 60 lines" missing `agent-writing-rules`' 75-line
`-reviewer`/`-auditor` allowance) is folded into D06's title rather than a ninth edge, to
hold the manifest at the 8-edge acceptance. D07 (`judgment` → `teamwork:wiring-checker`):
the job-evidence test has no rubric anchor. D08 (`judgment` → `harness:agent-checker`):
team-lead's `sonnet` tier sits below its `opus`/`fable` subordinates with no recorded
justification. `unrecovered_findings` note removed — the gap it declared is closed.
**#396:** `sweep.py validate` now warns (never errors) when a `verbatim-line` dependent
pattern carries a literal space between word characters — the #393 line-wrap-fragility
class (a prose re-wrap silently breaks a require edge's match, or disarms a forbid
edge) — suggesting `\s+` instead; existing fragile manifests still validate VALID.
Selftest gains a positive control (fragile pattern warns), a negative control (a
`\s+`-tolerant pattern warns nothing), and unit-level `check_pattern_fragility()`
assertions. Minor bump — both are additive: more edges, one new advisory warning tier;
no existing contract changed.

v0.14.0 · 2026-08-16 · New capability (issue #379): `doctrine-audit`, a fifth estate-audit
instrument for canon-to-dependent DOCTRINE-drift conformance — a rule stated canonically in
one artifact (a standards skill, an ADR) violated, omitted, or paraphrased by a dependent (an
agent body, a forge skeleton, a README ledger row). Own manifest, `doctrine.manifest.json` at
the repo root (separate schema from `naming.manifest.json` per ADR-0011 D1 — Kim's
2026-08-16 ruling), with its own `sweep.py validate` subcommand. Four edge types:
`verbatim-line` (require/forbid an exact pattern), `ledger-sync` (a ledger row still matches
what's on disk), `vocab-term` (canonical term vs. banned aliases), and `judgment` (no
lexical anchor — routed to a named owning checker, reported "queued, not built", never
dispatched from the instrument per Kim's ruling — read-only like its four siblings).
`estate-audit-agent` grows a fifth `instrument` value; `overhaul-planning`'s measure-first
Phase 0 gains it as a sixth composed instrument (fires whenever the target carries a
`doctrine.manifest.json`), `requires` extended on both. Manifest seeded with 5 of the
2026-08-16 team/coordination-surface review's 8 findings (the other 3 could not be
recovered from any written record — seeded honestly as a documented gap, not fabricated);
running the sweep against this workspace right now catches 4 of the 5 live (findings 1/2/5
— #380/#381 are still open, not yet merged via PR #383 — and finding 4's stale README row),
with the 5th (finding 3/#382) correctly routed to `harness:wording-checker` as a judgment
edge. Minor bump — new capability, no existing contract changed.

v0.13.1 · 2026-08-16 · Reconciled `overhaul-planning`'s doc-type ruling with docs' own type
taxonomy (issue #369): PR #346's `docs:doc-checker` pass judged a generated overhaul-plan doc
plan-shaped (living checkboxes, no genuine Components/Interfaces/Data/Risks), not LLD-shaped as
the skill's Phase-1 doc-home paragraph claimed. Retargeted doc type to `plan` — PLAN's own
"sequenced steps, each with done-when and a status" and its living-state class (one canonical
copy, reviewed on a cadence) fit a wave-by-wave campaign plan; `PLAN-TEMPLATE.md` restructured
under the canonical `## Steps` / `## Validation` / `## Rollback` headings (a new Rollback
section authored: undo per irreversible step — reverted `git mv`, restored ledger entries,
reversing supersession notes, reverted reshape PRs). No description-field change (body-only).

v0.13.0 · 2026-08-16 · ADR-0014 ratified and executed (issue #353): `validate.py`'s
`Grammar.parse` skill branch gains two new reserved productions, both inserted before the
existing object-process check to avoid its dead-code hazard — D1 `-rules` becomes a reserved
tail (topic-phrase resolves via a new union pool, `ObjectVocab ∪ ProcessLex ∪ TopicLex`, through
a new `resolve_objects_union` method sharing a `_resolve` helper with `resolve_objects`), D2
`check-` becomes a reserved head (residue resolves via `ObjectVocab` alone). New closed lexicon
`TopicLex` (D3, 15 entries) added to `naming.manifest.json`'s schema (`TOP_LEVEL_LIST_FIELDS`
gains `topic_lex`). `ObjectVocab` gains 12 entries (D4: `entry-file`, `routing`, `state`,
`focus`, `safety`, `speed`, `translation`/`translations`, `color`/`colors`, `isolation`, `a2a`,
`ui-change`, `stage` — the last a deliberate dual membership with `ProcessLex`); `check` removed
from `ObjectVocab` (D2's reserved head supersedes it). Selftest gains D1/D2 fixture triads
(positive/negative/regression) plus a quantifier-non-goal control and a `stage` dual-membership
control, mirroring §14.1's own reverse-wrapper pattern. Estate-wide `--scope grammar` re-run
(all 8 plugins + the workspace `.claude/skills` tree): 182 artifacts, 0 grammar errors before
and after — the 32 named exemptions now parse clean via grammar (not exemption), the 5
already-clean names (`check-doc`/`check-skill`/`check-stage`/`naming-rules`/
`product-lifecycle-rules`) unaffected, the 4 quantifier non-goals (`check-all-agents`,
`check-all-skills`, `check-everything`, `check-whole-ui`) still exempt-only, never
grammar-passing. Root `naming.manifest.json`'s `exemptions` array shrunk 156 → 124 via
`authorkit:/exemption-retire`'s own discipline. `.claude/docs/spec/spec-naming-convention.md`
gains §14.2 mirroring §14.1's pattern (ruling, why, validator change, non-goals). Minor bump —
additive grammar productions, backward compatible (every previously-passing name still passes).
v0.12.1 · 2026-08-16 · Structural-hygiene fixes from the naming-audit's non-gating findings
(issue #350). `validate.py`'s agent schema was missing `model` from its optional fields —
`estate-audit-agent`'s deliberate sonnet pin (PR #328, per `agent-writing-rules`' seat ladder)
is a legitimate estate-wide convention, not a violation, so the fix widened the schema rather
than stripping the pin. `ALLOWED_SKILL_ENTRIES` was likewise missing `intent.md`, the
`make-skill`-scaffolded intent file present across many skills estate-wide (`attention-audit`
carries one); added to the closed set. The dispatch's other two items (missing frontmatter
fields on `manifest-authoring`/`naming-audit`/`naming-conventions`/`rename-planning`; stray
`.DS_Store` files) were already resolved by prior landed work — verified clean, no changes
needed. `fix-old-names`' deliberate negative-test fixture (9 structural errors) is untouched
by design. Structural errors: 11 -> 9 (the remaining 9 are all the `fix-old-names` fixture).

v0.12.0 · 2026-08-15 · Merges the three single-instrument batch-audit agents
(`naming-audit-agent`, `bloat-audit-agent`, `attention-audit-agent`) into one
parameterized `estate-audit-agent` (issue #293), executing `agent-writing-rules`'
"Checker-seat consolidation" merge test and issue #272's ruling: identical
isolated-context batch-sweep mechanics, one read-only script grant per instrument,
one aggregate-report shape, differing only in which validator script and `requires:`
skill each named. The dispatch now names an `instrument` (`naming`/`bloat`/`attention`/
`pattern`) instead of picking one of three (soon four) near-identical agents;
`pattern-audit` (#288 shipped it skill+command only, no standalone agent twin) joins
as the fourth instrument, gaining `scan.py`'s read-only grant on the merged agent
without ever having had its own agent to retire. Tool wall is the exact union of the
four instruments' read-only script grants (`validate.py`/`measure.py`/`rent.py`/
`collide.py`/`usage.py`/`trend.py`/`scan.py`) plus `Read`/`Glob`/`Grep` — no write
capability added. `estate-audit-agent`'s naming ('follow the audit-family pattern')
does not resolve under ADR-0011's primary agent-of-skill production as-is — the
residue `estate-audit` was no extant skill — so a new minimal `estate-audit` index
skill (no procedure of its own, `disable-model-invocation: false`/`user-invocable:
false`, small evals suite) backs the name, and `estate` is newly registered in both
the repo-root and this plugin's own `naming.manifest.json` `object_vocab` (a clean,
justified registration — the term is already pervasive in this estate's own prose,
just not yet an ObjectVocab token). `naming-audit-agent`/`bloat-audit-agent` are
removed from the repo-root manifest's exemptions array (retired names, no longer
grandfathered); `attention-audit-agent` was never in that list. The three retired
agent files are deleted; every live reference repointed estate-wide (the #266
chore-lead-retirement precedent) — this README's Map table and invocation-dials
paragraph, `naming-conventions/references/GRAMMAR.md`'s and `TOOL-GRANTS.md`'s
worked examples, `overhaul-execute`'s Phase 1 MEASURE dispatch line, `attention-audit`'s
Composition section, and harness's `agent-writing-rules`' "Checker-seat consolidation"
section (cross-plugin, since it named this ticket as the pending merge candidate).
Historical README ledger entries and dated ops/report snapshots that merely narrate
past events are left untouched, per this estate's append-only-history convention.
Fresh-context `harness:agent-checker` (FLOOR, no model override) passed on the new
agent definition before this PR opened — see the PR body for the verdict.
v0.11.4 · 2026-08-16 · `overhaul-planning`'s Phase 0 gains a conditional fifth instrument
(issue #286, the deferred `lld-0004-pattern-audit.md` acceptance-predicate-8 follow-up from
#257/PR #288): a new step 3 composes `authorkit:pattern-audit` when the campaign's charter names
a pattern none of the four fixed-axis instruments owns — never replacing naming-audit,
bloat-audit, check-routing, or `surface_map`, and never hand-authoring a one-off sweep script.
`requires` gains `pattern-audit`; `allowed-tools` gains `Bash(python3 */scripts/scan.py *)`.
**Resolves PR #288's deferred F2 finding** (the reviewer routed the compile-for-veto gap here as
an LLD-amendment concern): pattern-audit's own procedure states its compiled probes so a live
user can veto a bad translation before the scan runs, but a composed overhaul-planning call is
frequently unattended with no one to veto — the substitute ruling states the compiled probes and
the resulting verdict line in the plan doc's Phase 0 measurements instead, reviewed after the
fact rather than vetoed before it. `lld-0004-pattern-audit.md` amended to v0.3.0 (dated note) to
match: Risk 1's fallback gains the composed-call branch, and the Interfaces "Composition
contract" section is marked realized rather than deferred. Reciprocal eval fences: n12 added to
`overhaul-planning`'s suite (a raw sweep ask stays pattern-audit's own), n07 added to
`pattern-audit`'s suite (a campaign-plan ask stays overhaul-planning's own) — neither
skill's description changed, so no new `/check-routing` steal surface was opened, just proven
clean. Fresh-context `wording-checker` pass on the Phase 0 body edit: PASS-with-fixes (three
minor clarity nits — a dangling "instruction" antecedent, an unstated judgment-overlay
precondition on the noisy-result branch, a singular/plural probe mismatch), applied.
v0.11.3 · 2026-08-16 · `attention-audit` gains the structural-fix recommendation tier (issue
#297): a collision or rent finding can now recommend ONE fix from a named category set —
reciprocal fence (default) · demote-to-wiring · merge · centralize-boilerplate · retire —
instead of only fences, closing the treadmill where a fence fix grows both descriptions
(v0.10.1 had to diet `naming-conventions` just to afford its own fence). Criteria for when
reduction beats a fence live inline in `SKILL.md`'s step-3 classify judgment (not a separate
references file — the category assignment is the same judgment act as the existing
routing-twin/boilerplate-tax/coincidence three-bucket classify, and the criteria are short
enough to read on every run rather than earning their own indirection).
`collide.py` mechanically measures the W8-blown criterion (in scope, cheap): each flagged pair
now carries `headroom_a`/`headroom_b` (700 minus that side's current description length) and
`fence_tight` (true when either headroom is under 23 chars — this estate's own shortest
measured real NOT-clause, n=232, 2026-08-16) — a live real-estate run flagged
`ops-write-sandbox-rules`↔`sweep-chores` FENCE-TIGHT (`sweep-chores` already over 700 chars),
proving the signal fires on real data; `selftest` gained a positive/negative pair for it.
`REPORT-TEMPLATE.md`'s Collisions block gains the fix-category field (fence stays available,
no longer the only option); a rent finding with no collision partner draws from the same set
minus reciprocal fence. Instrument stays report-only — recommends, never rewrites.

v0.11.2 · 2026-08-16 · `attention-audit`'s write-time and ship-time instruments (v0.10.0's
`collide.py --against` and `trend.py`) get wired into actual enforcement tiers instead of
staying manual-run-only (issue #294). Two new PostToolUse sibling hooks in `hooks/hooks.json`,
reusing #276/#287's derive-target-from-write plumbing: `collide_hook.py` fires only when a
written `SKILL.md`'s `description:` field changed (a body-only edit skips the sweep; measured
~0.04s no-op, ~0.12s on a real change against this workspace's ~140 skills) and prints an
advisory finding — judgment-shaped, never a hard block, per hook-writing-rules' routing test —
classifying each collision as routing twin / boilerplate tax / coincidence, the same three
buckets the skill's own procedure already names. `trend_hook.py` fires on a plugin's own
`.claude-plugin/plugin.json` `version` bump (this workspace's own ship signal) and appends that
plugin's row to `attention-trend.csv` automatically (dead/stolen/leaked record `absent` — no
routing report at hook time); scoped authorkit-side only, since the harness-native alternative
(`release_gate.py`'s own G6 package step) needs a harness file edit and a harness version bump
both off-limits while issue #313 holds that slot concurrently — left as a named follow-up.
Both hooks carry #287's shape guards (fail-open on any malformed event, unreadable file, or
internal exception) and their own `selftest`.

v0.11.1 · 2026-08-16 · `naming-audit`'s `validate.py` gains a malformed-manifest robustness
sweep before the adia estates campaign (issue #296): every top-level field
`MANIFEST-TEMPLATE.json` declares as a list is now type-checked (`_typed_list`, swept from the
template's own schema, not hand-picked) — a wrong-type field surfaces a named `manifest_errors`
finding and is treated as empty rather than crashing `Grammar.__init__`'s `set()`/`for` calls.
`object_vocab` entries gain three more guards, generalizing #252's author_registry-only shape
fix: a missing `canonical` key, a plain-string entry where a structured `{"canonical": ...}`
object is required (the mirror of #252's own direction), and a duplicate `canonical`
registration — ruled last-wins (matching the dict's own natural overwrite) but never silently:
a duplicate always surfaces a named finding, so the manifest is not clean until resolved by
hand. Each of the four classes carries a positive/CLI-exit-1/regression triplet in
`validate.py selftest`, following #252's worked pattern.

v0.11.0 · 2026-08-15 · `pattern-audit` joins as a fourth audit-family sibling (issue #257,
lld-0004-pattern-audit.md): a genuinely distinct instrument — sweeps a repo/corpus for an
arbitrary caller-supplied literal pattern or natural-language instruction and emits a flat,
structured match dataset (`id`/`file`/`line`/`col`/`match`/`context`/`kind` + totals), for a
downstream step (review, bulk edit, migration, or overhaul-planning's Phase 0) to consume —
never a replacement for naming-audit/bloat-audit/surface_map's own fixed-axis measures, which
stay exactly as they are. Skill+script+command wrapper, sibling-shaped
(`skills/pattern-audit/SKILL.md` + `scripts/scan.py` + `commands/pattern-audit.md`, same
model-only/not-user-invocable dial pair as naming-audit/bloat-audit). The measure-then-judge
split holds: `scan.py` accepts only literal, labeled regex/glob probes (deterministic,
selftest-proved: positive/reverse/label-plumbing/multi-probe/glob-narrowing/skip-dir+binary
pruning/invalid-regex-fail-clean/id-stability/verdict-line-shape); the skill compiles a
natural-language instruction into those probes first, stating the compilation for veto before
running, and optionally annotates matches with `verdict: hit | false-positive` — never deleting
or renumbering records. Script deliberately named `scan.py`, not `measure.py`, so it never
silently rides overhaul-planning's existing `Bash(python3 */scripts/measure.py *)` grant. New
`object_vocab` registration: `pattern` (repo-root manifest already carried it; this plugin's own
`naming.manifest.json` did not). Reciprocal NOT-for fences closed in naming-audit (n06),
bloat-audit (n07), and fix-old-names (n11) — the object cut (rename provenance vs. an arbitrary
pattern with no rename provenance) keeps fix-old-names' own t05/t08 read-only finds
unambiguously its own. NOT a generalization of `plan-plugin-split`'s `surface_map.py` (a typed
relation graph is not regex-expressible) and NOT a `make-script` one-off (a permanent instrument
with its own recurrence ratchet handing repeat ad-hoc sweeps to `make-script` instead). The
overhaul-planning Phase-0 wiring (a conditional fifth step, replacing none of the four existing
instruments) is explicitly deferred to its own follow-up ticket, filed as this build's own
acceptance predicate — this change touches no overhaul-planning file.
· v0.10.3 · 2026-08-15 · naming-audit `validate.py` gains the `hook` subcommand (issue #276): the PostToolUse hook derives its target from the write's own file_path, so worktree sessions validate their own tree (not the main checkout) and only the touched plugin; the plugin's own shipped `hooks/hooks.json` rewired off its worktree-blind `--target ${CLAUDE_PROJECT_DIR}` form too; critic pass added wrong-shape fail-open guards + fixtures
v0.10.4 · 2026-08-15 · `overhaul-planning`'s split/merge/partition NOT-clause is dieted (issue #280): now "a single-pair split/merge decision or single-plugin partition (plan-skill-split, plan-plugin-split — composed, not replaced)", dropping the separate `plan-skill-merge` name now that harness's `plan-skill-split` names `plan-skill-merge` as its own merge-direction sibling and is the stated canonical owner other skills fence back to by name only; n08/n09 gain dated owner-comments, no new cases (renumbered from 0.10.2 — that slot went to PR #285's rebump)
v0.10.3 · 2026-08-15 · naming-audit `validate.py` gains the `hook` subcommand (issue #276): the PostToolUse hook derives its target from the write's own file_path, so worktree sessions validate their own tree (not the main checkout) and only the touched plugin; the plugin's own shipped `hooks/hooks.json` rewired off its worktree-blind `--target ${CLAUDE_PROJECT_DIR}` form too; critic pass added wrong-shape fail-open guards + fixtures
v0.10.2 · 2026-08-15 · `naming-audit-agent` and `bloat-audit-agent` gain an explicit
`model: sonnet` pin (issue #283, the A7 defect-class follow-up deferred from #275's
`attention-audit-agent` fix — PR #126's original A7 gap: a missing/`inherit` model field
silently rides the dispatching session's model). `skill_lint` A7 passes clean on both agents.
Shipped standalone (no imminent authorkit release in flight to ride along with, per this
ticket's own Scope/Open note). Rebumped from 0.10.1 — that number shipped via PR #289 mid-flight.
v0.10.1 · 2026-08-15 · reciprocal NOT-fences added closing the collision-baseline twins with harness (issue #282, PR #278's recipe): `naming-conventions` ↔ harness's `naming-rules` and `bloat-audit` ↔ harness's `check-skill`; each description gains a NOT-clause and a reciprocal eval case (bloat-audit n07 new; naming-conventions n05's existing case gains a dated owner-comment closing the loop); `naming-conventions`'s description also dieted (tool-grant parenthetical de-duped, exemptions detail trimmed) to stay under the W8 700-char budget with the new clause added
v0.10.0 · 2026-08-15 · attention-audit joins as the third audit axis (issues #259/#261/#264;
the 2026-08-15 context-efficiency review): always-on menu rent (rent.py — dial-aware,
skill/agent split, agents bill unconditionally), IDF-ranked description-collision detection
(collide.py — per-artifact nearest-neighbors report after a fresh-critic FLOOR FAIL proved a
global top-N window buries real twins at ranks 171/1000/1682; two measured LLM-tier limitation
classes documented: common-words [check-skill↔bloat-audit, skill df=52] and crowded-commons
[naming-rules↔naming-conventions, naming df=23]; `--against` write-time pre-lint), usage
telemetry cross-reference (usage.py — lineage-aware + preload-aware by construction, both as
selftest fixtures from the live baseline), and the per-release trend series (trend.py —
separate columns, literal `absent`, no quotient ever). attention-audit-agent batch twin
(sonnet). overhaul-execute Phases 1+6 wired for the axis in the same change (Kim's
"open a project, run /overhaul-execute, all of authorkit unleashes" contract). Reciprocal
fences closed in bloat-audit (n05/n06) and harness check-skill/check-routing (n07 each).
Forge provenance in the skill's intent.md: P0–P5 gates PASS with the full critic exchange.
· v0.9.4 · 2026-08-14 · `validate.py`'s `Grammar.__init__` no longer crashes with a raw
`TypeError: unhashable type: 'dict'` when `naming.manifest.json`'s `author_registry` holds a
structured entry (`{"name": ..., "emails": [...]}`) instead of a plain string (issue #252,
found live by `overhaul-execute`'s first real dogfood run against agent-ui): malformed entries
are now skipped and surfaced as a named, actionable `manifest_errors` finding (never a silent
coercion — a structured entry has no single field that is obviously "the" author string) —
proven via a direct `run()` call and the CLI's own exit-code contract, plus a plain
string-list regression control. `naming-conventions/references/MANIFEST-TEMPLATE.json` now
documents the expected flat-string-list format inline; `manifest-authoring/SKILL.md`'s body
was deliberately left untouched (the template it points readers to is the fix, not a second
prompt edit needing its own checker pass).
v0.9.3 · 2026-08-14 · `overhaul-execute`'s move/build row repaired on two stale claims (issue #244): worktree isolation is `dispatch-ticket`'s conditional call, not an unconditional step (drifted since #204), and the PR-opened ceiling now names ADR-0012's quick-build carve-out plus the reason no overhaul row can ever reach it (a wave spans many files across more than one plugin and rewrites contracts by definition, so no grant line is placed)
v0.9.2 · 2026-08-14 · `overhaul-planning` gains the reciprocal NOT-for fence against harness's `plan-plugin-split` (issue #245): n05 was measured STOLEN 3-of-3 in #243's check-routing re-run (true owner not a menu entry on an authorkit-scoped run). Description re-trimmed to 699 chars (W8); evals.json n05/note updated; fresh-context skill-checker (FLOOR) clean. Mirror case n08 added to plan-plugin-split's own suite (harness), no description change there. Full /check-routing authorkit re-run: 114/114 cases, 8 suites clean, n05 now `none`.
v0.9.1 · 2026-08-14 · `naming-conventions` evals t08 was measured DEAD in PR #242's full
check-routing run (unanimous 3-judge none, issue #243). Ruled Branch A: the prompt ("explain
the allowed-tools grant syntax for a mutating command") genuinely belongs here —
`TOOL-GRANTS.md` already existed and was already indexed in the body's References table — but
the SKILL.md description never surfaced tool-grant/allowed-tools as a trigger phrase. Fixed by
adding it to the description in the same change as the evals note update. Swept all seven
sibling authorkit suites for the phrase: none claim it, so no reciprocal fence was needed.
/check-routing authorkit re-run proves t08 now routes with nothing else broken (see PR).
v0.9.0 · 2026-08-14 · Enforces #238's E1 sign-off, recorded on issue #241: (1) reverse-wrapper
grammar amendment — a skill MAY carry an object-verb name IFF an identically-named command
wraps it in the same plugin — dated section in `.claude/docs/spec/spec-naming-convention.md`
§14.1 (companion doc, never the accepted ADR-0011 file), `validate.py`'s skill-grammar
production gains the matching branch, selftest gains positive/negative/regression fixtures. (2)
`overhaul-execute` extracted from v0.8.0's standalone command into `skills/overhaul-execute`
(model-invocable, new evals suite) with `commands/overhaul-execute` reduced to the thin wrapper
per house pattern — mutation posture (`mutates: true`/`confirm: required`, tool grants)
unchanged from PR #240. `overhaul-planning`'s reciprocal fence (description + evals n10/n11)
re-pointed from the command name to the skill — the routing-judge's real competitor was always
going to be the skill, never the (non-model-invocable) command. Fresh-context
`harness:skill-checker` passed on both the new skill and the `overhaul-planning` edit (minor
findings applied). `release_gate authorkit` CLEAN (0 fail); G12 naming-grammar 0 errors,
including the new skill — the amendment's first real production proof. `/check-routing
authorkit`: 113/114 cases across 8 suites, no new steal/leak on any touched suite; one
pre-existing, unrelated `naming-conventions` dead case (unanimous 3-of-3 vote, orthogonal to
this ticket) reported, not fixed here.
v0.8.0 · 2026-08-14 · `commands/overhaul-execute` (issue #238): the DRIVES half of the
`overhaul-planning` pair — discover+scope-confirm, measure, plan, then gated wave execution
(rename-planning → rename-execute per rename, `harness:reshape-skill` for merge/splits,
`teamwork:build-lead` dispatches for moves/builds, `fix-old-names` sweeps after every rename
wave) — under three live-user gates (scope, Gate A, Gate B), with emergent items batched to the
next gate, each carrying a proposed solution. Shipped as a **standalone command, no companion
skill** — `execute` is registered in `verb_lex`, not `process_lex`, so a same-named skill has no
legal grammar production today (confirmed against the live manifest); the `rename-execute`/
`exemption-retire` commands in this same plugin are the existing precedent for exactly this
shape. `overhaul-planning`'s description gained the reciprocal NOT-for clause naming this
command, plus two reciprocal eval cases (n10/n11) proving a drive-shaped prompt doesn't
mis-route there; `commands/overhaul-planning`'s own body gained one pointer line for
user-surface symmetry. A skill+wrapper form (matching `overhaul-planning`'s own shape) would
need a real naming-grammar amendment — a decision left to a follow-up ticket with Kim's actual
sign-off, never assumed here. `release_gate authorkit` CLEAN; `/check-routing authorkit` clean
(no new suite — commands aren't model-routed, so this run only reproves the fenced side).
v0.7.1 · 2026-08-14 · `naming-audit`'s `validate.py` grant parser now recognizes a SCOPED write
grant (tool name + parenthesized scope, e.g. `Edit(**/naming.manifest.json)`) as that write tool
for policy/grant-coherence checks — previously it read as write-less, a false-negative class
found during #235's build (PR #236, issue #237). Fixes a real false positive on this plugin's own
`commands/manifest-authoring` (`mutates: true` with only scoped Edit/Write grants used to fail
"no write-capable tool granted"; now clean). Selftest gained three fixtures on `policy_checks`
directly: a scoped-grant positive control, a bare-name regression control, and a read-only
negative control. Estate-wide delta measured before/after across all 8 plugins: authorkit's own
structural-error count drops 10 → 9 (the fixed false positive); every other plugin's count is
unchanged — no new true positive surfaced elsewhere on this estate. `validate.py selftest` green;
`release_gate authorkit` CLEAN.
v0.7.0 · 2026-08-14 · New user surface (issue #235): `commands/manifest-authoring` (mutating —
`mutates: true` + `confirm: required`, same posture as `rename-execute`, since it writes the
target estate's `naming.manifest.json`) and `commands/rename-planning` (plan-only — `mutates:
false` + `confirm: none`, matching `naming-audit`/`bloat-audit`'s read-only posture, since the
wrapped skill carries no `Write`/`Edit` tool and never touches disk) — the identical-name wrapper
pattern (`naming-audit`'s own template; the validator's wrapper-production exception, PR #227's
precedent) applied to the last two of the six skills with no user-invocable surface. No SKILL.md
body or dial changes: both wrapped skills stay `disable-model-invocation: false` /
`user-invocable: false`, unchanged since #196. No description edits to either skill, so no eval
suite re-run is owed; `evals/evals.json` for both is untouched. `release_gate authorkit` CLEAN (0
fail / 1 warn, the warn pre-existing and unrelated — G8 prose-sibling names in `bloat-audit`/
`overhaul-planning`/`rename-planning`); naming grammar clean (`--scope grammar`, both new names
resolve via the wrapper-production exception, no new `ObjectVocab` registration needed — `rename`
and `manifest` were already registered). `harness:skill-checker` does not apply to `commands/*.md`
in this estate's convention — confirmed against all five pre-existing command wrappers, which
fail the same generic `skill_lint` invocation-lint identically (it expects a SKILL.md-shaped
dial/directory pair no command file carries); `release_gate`'s own G3 lint sweep already excludes
`commands/` from its targets, so this is a pre-existing, accepted gap, not a new one. README's Map
table and Invocation-dials section updated to match.
v0.6.2 · 2026-08-14 · `naming-audit` gains the reciprocal NOT-for fence against `fix-old-names`
(issue #233), killing the last routing steal in the plugin: `fix-old-names`' t10 ("Check whether
this project is still on retired plugin names before I ship.") scored 19/20 across PR #230's
first measurement and PR #232's re-run, the only non-clean case left. Ruling: `fix-old-names`
owns it — the prompt asks whether a repo still references RETIRED names (its sweep-and-rewrite
Phase 1 "report first" domain), not whether current names conform to the grammar (`naming-audit`'s
read-only domain). The description's fence is the tight boundary axis only; `naming-audit`'s
`evals.json` gains n05, `fix-old-names`' t10 prompt verbatim as a no-trigger twin naming the real
owner — the measuring prompt becomes the regression case, per PR #232's own pattern. Mirror-check
on `fix-old-names`' own suite found nothing open (it already correctly owned t10; the leak ran the
other way). Fresh-context `harness:skill-checker` (FLOOR) passed clean. A full `/check-routing
authorkit` re-run (95 cases, all 7 suites, single-judge pass, no contested cases) shows
`fix-old-names` 20/20 (t10 now routes home) and `naming-audit` 12/12 (n05 passes) — every other
suite (`bloat-audit` 11/11, `manifest-authoring` 11/11, `naming-conventions` 13/13,
`overhaul-planning` 16/16, `rename-planning` 12/12) stays clean, no new leak anywhere. The plugin's
deferred steal from PR #230 is closed.
v0.6.1 · 2026-08-14 · `naming-conventions` gains the reciprocal NOT-for fence against
`overhaul-planning` (issue #231): the description's "planning a migration" phrase is narrowed to
"resolving one artifact's rename/migration rule (exemptions array, grandfather-with-ratchet,
rename sequencing)" plus an explicit `NOT for planning or generating an estate-wide
overhaul/reshape/merge/split campaign across many members (overhaul-planning)`. `evals.json`'s
t06 ("How should I sequence renames when migrating a legacy, ungoverned estate?") — the exact
prompt PR #230's mandatory `/check-routing` measured as a 3-of-3 cross-suite steal to
`overhaul-planning` — is reclassified `n06`, no-trigger, owner `overhaul-planning`. Fresh-context
`harness:skill-checker` (FLOOR) passed clean; a full `/check-routing authorkit` re-run (94 cases,
all 7 suites) shows `naming-conventions` 13/13 and `overhaul-planning` 16/16, both clean — the
steal is dead. One unrelated pre-existing failure (`fix-old-names` t10 vs `naming-audit`, noted
in PR #230 as deferred) is untouched by this change and stays open as its own follow-up.
v0.6.0 · 2026-08-14 · `overhaul-planning` gains merge/split-candidate nomination + procedure-vs-knowledge
context-tier classification (issue #229), completing all four reorganization axes: Phase 1's
per-member kill-switch adds question 4 (MERGE/SPLIT CANDIDATE? — names a candidate set and
soft-mentions `harness:plan-skill-merge`/`harness:plan-skill-split`, executed later only via
`/reshape-skill`; nominates, never re-derives their own tests) and question 5 (PROCEDURE or
KNOWLEDGE? — classified per `harness:pack-writing-rules`, with a context-optimization tier —
`keep-inline`/`move-to-references`/`extract-to-pack`/`retire` — anchored to `bloat-audit`'s own
measured `chars`/flags/`duplicates` output, never a vibe). Both axes sit under the existing
kill-switch discipline (evidence can veto a nomination or a tier exactly like a move).
`PLAN-TEMPLATE.md`'s Phase 1 table gains the two columns; Phase 2 gains a Wave 0
(merge/split-nomination tickets, ordered before Waves 1–3 since a roll-up/break-up can change
which members even reach a rename ticket). `evals.json` gains t07 (both new axes in one ask)
and n08/n09 (a single-pair merge/split decision still routes to `plan-skill-merge`/
`plan-skill-split`, not here) since the description changed to name the new capability.
Contract-extending, backward compatible (no existing Phase 1 answer or ticket-seed shape
changed) — minor bump.
v0.5.1 · 2026-08-14 · `schema_scope` manifest flag (issue #226, executing #224's ruling b):
`validate.py` reads an optional `schema_scope: "grammar" | "full"` field off the estate's
own `naming.manifest.json` as the default operating scope when `--scope` is omitted (absent
-> `full`, back-compat); under `"grammar"`, structural findings for artifacts outside
authorkit's own tree are dropped entirely (not just non-gated) — authorkit keeps dogfooding
`"full"` on itself regardless. This estate's own manifest now sets `schema_scope: "grammar"`:
full estate audit goes from 2,111 structural findings (measured pre-change) to 9, all inside
authorkit. `--scope` CLI override, the PostToolUse hook, and `release_gate.py`'s G12 (which
always passes `--scope grammar` explicitly) are unaffected and re-verified green.
`manifest-authoring`'s consulted reference (`naming-conventions/references/MIGRATION.md`) and
`MANIFEST-TEMPLATE.json` document/carry the field.
v0.5.0 · 2026-08-14 · `overhaul-planning` (issue #225): a new skill + command generating a
phased estate-overhaul plan (measure-first, per-member kill-switch design doc, waved ticket
seeds) — the estate-scale sibling above `rename-planning`'s per-member blast radius, encoding
the #197 campaign's proven method. `overhaul` registered in the repo-root
`naming.manifest.json`'s ObjectVocab (object=overhaul + process=planning, same production as
`rename-planning`). Ticket seeds are generated as a plan-doc list, never auto-minted as
Issues — this estate's capture, confirm, then build discipline. Command wraps the skill under
the identical-name wrapper production (`naming-audit`/`bloat-audit`'s own pattern);
`mutates: true` / `confirm: required` since it writes the plan doc + seed list, unlike the two
read-only audit commands.
v0.4.0 · 2026-08-14 · ADR-0011 execution (issue #197): repo-root `naming.manifest.json` seeded (169 exemptions, D8); `validate.py` gains `--scope {full,grammar}` (the full schema fails hundreds of pre-existing structural findings estate-wide — grammar-only gating proved necessary) + a `-agent`-head fixture (W4 successor); `fix-old-names`/`fix_old_names.py`/`renames.json` moved in from harness, still unreachable here (authorkit disabled).
v0.3.0 · 2026-08-13 · Gate-clean (issue #196, REVIEW-209 follow-ups): both invocation dials declared on all 5 SKILL.md files; validate.py's schema/layout closed-set both gain the dials and `evals/` as accepted (else this ticket's own additions break its dogfooding); 4 ruff E701 fixes; both scripts gain `selftest` (argparse's required `--target` no longer swallows a bare call first); `evals/evals.json` for all 5 skills; a GRAMMAR.md line scoping `banned_aliases` to names only; this README; `gate.yml` now gates authorkit in CI.
v0.2.0 · 2026-08-13 · Initial land (issue #196): 4 skills (naming-conventions, naming-audit, rename-planning, manifest-authoring), plus bloat-audit as a fifth skill for busy-work/over-specification auditing; 2 agents, 4 commands, a PostToolUse validation hook, `naming.manifest.json`. Kept disabled in this workspace's `enabledPlugins`; ADR-0011 (status: proposed) and its companion spec doc committed alongside.
