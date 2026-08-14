# authorkit — harness artifact governance: naming, frontmatter, layout, audits

A meta plugin used to refactor existing and author new skills/commands/agents against one
naming convention (ADR-0011, **accepted** 2026-08-13) — grammar, frontmatter schema, folder
layout, and migration tooling — plus a separate busy-work/over-specification audit. Dogfoods
its own spec: `skills/naming-audit/scripts/validate.py` validates this plugin clean against
itself with an empty exemptions array.

Kept **disabled** in this workspace's own `.claude/settings.json` (`enabledPlugins`) — enabled
only in the estates it audits, so its own `naming-conventions` routing never collides with
harness's `naming-rules` here. `naming-rules` now carries an in-place ADR-0011/D9 supersession
note (2026-08-14) rather than retiring outright, so the collision this boundary guards against
is still live — this stays disabled here until that note itself retires (issue #197).
`fix-old-names` moved here from harness the same day (issue #197, D9 — a mechanically clean
move, no shared-script dependency) but is, for the same reason, temporarily **unreachable in
this workspace**: authorkit's own routing surface (including `fix-old-names`) only activates
once `enabledPlugins` flips, which this ticket does not do.

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
| `skills/overhaul-planning` | Procedural skill | model-only | Generates a phased estate-overhaul plan for a target spanning many members: composes naming-audit + bloat-audit + harness's check-routing/plan-plugin-split (Phase 0, soft-mentioned where harness isn't installed), a per-member kill-switch design doc answering all four reorganization axes — where-it-lives, species, merge/split-candidate nomination (soft-mentions `plan-skill-merge`/`plan-skill-split`), and procedure-vs-knowledge with a context-optimization tier (`keep-inline`/`move-to-references`/`extract-to-pack`/`retire`, anchored to bloat-audit's own measured numbers) — any of which can come back "no move"/"no candidate"/"keep-inline" (#197's precedent, extended 2026-08-14 issue #229), then waved ticket seeds with Blocked-by edges (Phase 2, seed list only — never auto-minted, per this estate's capture, confirm, then build discipline). Generates only: never executes a move, rename, merge, split, or build. Wrapped for user-invocation by `commands/overhaul-planning` |
| `skills/overhaul-execute` | Procedural skill | model-only | The DRIVES half of the `overhaul-planning` pair (issue #241, enforcing #238's E1 sign-off): discover+scope-confirm, measure, plan, then gated wave execution (rename-planning → rename-execute per rename, `harness:reshape-skill` for merge/splits, `teamwork:build-lead` dispatches for moves/builds, `fix-old-names` sweeps after every rename wave) — under three live-user gates (scope, Gate A, Gate B), never self-approving. Extracted 2026-08-14 out of what shipped in PR #240 as a standalone command; exists as a skill at all only because of the reverse-wrapper grammar amendment below. Wrapped for user-invocation by `commands/overhaul-execute` |
| `agents/naming-audit-agent` | Subagent | dispatch-only | Batch conformance sweeps across N estates/plugins in an isolated context, one aggregated report |
| `agents/bloat-audit-agent` | Subagent | dispatch-only | Batch busy-work sweeps across N skills/plugins/corpuses in an isolated context, one aggregated report |
| `commands/naming-audit` | Command | user-only (`/naming-audit`) | Thin user-invocable wrapper over `skills/naming-audit` — skills aren't user-invocable, this is the on-demand surface |
| `commands/bloat-audit` | Command | user-only (`/bloat-audit`) | Thin user-invocable wrapper over `skills/bloat-audit`, same reason |
| `commands/overhaul-planning` | Command | user-only (`/overhaul-planning`), `confirm: required` | Thin user-invocable wrapper over `skills/overhaul-planning` — this one writes the plan doc + ticket-seed list to disk, so it gates on confirmation before writing, unlike the two read-only audit wrappers above |
| `commands/manifest-authoring` | Command | user-only (`/manifest-authoring`), `confirm: required` | Thin user-invocable wrapper over `skills/manifest-authoring` — mutating (seeds/edits the target estate's `naming.manifest.json`), so it gates on confirmation before writing, same posture as `rename-execute` |
| `commands/rename-planning` | Command | user-only (`/rename-planning`) | Thin user-invocable wrapper over `skills/rename-planning` — plan-only, never executes, same read-only posture as `naming-audit`/`bloat-audit` above |
| `commands/rename-execute` | Command | user-only (`/rename-execute`) | The estate's single mutation point — applies one `rename-planning` plan atomically (`confirm: required`), verifies via the validator, reverts whole on any new error |
| `commands/exemption-retire` | Command | user-only (`/exemption-retire`) | Opportunistic one-step chain: rename-planning → confirm → rename-execute → manifest shrink, for an artifact already being touched |
| `commands/overhaul-execute` | Command | user-only (`/overhaul-execute`), `confirm: required` | Thin user-invocable wrapper over `skills/overhaul-execute` (issue #241 — was a standalone command through PR #240/v0.8.0; the reverse-wrapper grammar amendment let the procedure move into a skill, this command adds nothing). The DRIVES counterpart to `overhaul-planning`'s GENERATES |
| `skills/fix-old-names` | Command skill | both (`/fix-old-names`) | Moved from harness 2026-08-14 (issue #197, ADR-0011/D9). Consumer-side rename migration: sweeps a repo that INSTALLS these plugins for references to retired names and rewrites the live ones, from the derived `renames.json`. Report-first, historical records left byte-identical, ambiguous names escalated to a human, filenames never rewritten |
| `hooks/hooks.json` (`PostToolUse`) | Hook | automatic | Runs `scripts/validate.py --hook` after every `Write`/`Edit`; no-ops cleanly when the target estate has no manifest (governance is opt-in per estate) |
| `skills/naming-audit/scripts/validate.py` | Script | invoked by naming-audit | Deterministic checks only: name grammar, folder layout, frontmatter schema, relation graph, policy/capability coherence, provenance. `selftest` mode proves schema/grammar/lexicon counters bite. Gained `--scope {full,grammar}` 2026-08-14 (issue #197): `grammar` gates only naming-grammar findings, leaving the broader structural/provenance checks informational — how this validator wires into an estate (nonoun-plugins) that hasn't adopted the full frontmatter schema without failing on hundreds of non-naming findings |
| `skills/bloat-audit/scripts/measure.py` | Script | invoked by bloat-audit | Deterministic measurement: body size, phase-heavy headings, oversized Failure sections, dense descriptions, cross-file near-duplicate paragraphs. `selftest` mode proves flag/duplicate/empty-target counters bite |
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
its harness incarnation. `naming-audit-agent` and `bloat-audit-agent` each cite their matching
skill via `requires:` (authorkit's own
existence-edge convention, not the `skills:` preload field) — both matching skills therefore
carry `disable-model-invocation: false`, since that dial blocks preloading outright wherever it
IS the real preload mechanism (verified 2026-08-13, PR #217's critic chain). `overhaul-planning`
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
