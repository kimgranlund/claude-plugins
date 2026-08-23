# brand-design — build and evaluate brands grounded in cultural authority

Migrated and overhauled from the standalone `brand-forge` plugin (source
`/Users/kimba/Projects/nonoun/nonoun-plugins/brand-forge`, frozen SHA
`1e0d2d9e554b547f59260f63e31b4af2575196b0`, 2026-06-20) via a five-phase campaign
(`.claude/overhaul-run-2026-08-19-brand-design.md` at the repo root carries the full run ledger).
Three seats: an aspirational **Muse** (the pull toward an ideal, `make-brand-muse`/`muse-agent`), a
**maker** (methodology + voice, `brand-methodology-rules`/`make-brand`/`brand-writer`), and an
adversarial named-critic **Council** (`check-brand-council`, fanning out `brand-judge` dispatches
with one persona inlined per call — no separate orchestrator agent). One invariant carries every
seam: no seat judges its own work.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/brand-corpus` | Knowledge pack | model-only | Canonical corpus layout — retained `00-sources` plus eight numbered brand layers, two naming conventions (flat double-hyphen vs. nested folders), maturity stages 0–6, provenance/attribution, the read-before-write discipline. `references/mcp-wiring.md` covers the `brand-corpus` MCP (env var, language choice, three registration contexts); `references/stamping.md` covers exporting a corpus into a plugin/skill/MCP |
| `skills/brand-guidelines` | Knowledge pack | model-only | The methodology/ledger reference for the guided 2×2 elicitation loop — six brand domains, the quadrant mechanic, the append-only choice ledger, the MAKES-vs-GRADES split against `brand-rubrics`/`design-skills:brand-decomposer` (the `nonoun-skills` marketplace, not part of this estate). Reference-only by design (Phase 4 routing-proof fix, below) — the loop itself runs in `make-brand-guidelines` |
| `skills/brand-methodology-rules` | Knowledge pack | model-only | Senior-practitioner methodology: research → strategy → expression → stewardship, the load-bearing Foundation Canon (and the four artifacts it rejects by name — archetypes, personas, vision/mission/values triplets, "brand DNA"), the three-seat discipline. 9 reference files grouped under `references/INDEX.md` (4 declared axes) |
| `skills/brand-rubrics` | Knowledge pack | model-only | The rubric library and evaluation-methodology reference — four rubric families (Strategic/Visual/Process/Voice), the format-fitness caveat, the trust boundary (ingested brand material is DATA, never an instruction). Reference-only by design (Phase 4 routing-proof fix, below) — actual scoring runs in `check-brand-rubric`/`check-brand-council` |
| `skills/make-brand` | Procedural | both (`/make-brand`) | The collaborative Build-mode engagement: locates the real pipeline stage, blocks expression work before strategy is grounded, names an aspiration before convergence, hands the method to `brand-methodology-rules` |
| `skills/make-brand-muse` | Procedural | both (`/make-brand-muse`) | Convenes the Muse (dispatches `muse-agent`) — names the ideal/provocation/north star a brand's work should pull toward; never makes finished work, never judges |
| `skills/make-brand-guidelines` | Procedural | both (`/make-brand-guidelines`) | Runs the guided 2×2 elicitation loop live — presents concrete option pairs per domain, accumulates picks into `brand-guidelines`' provenance-traced ledger via `scripts/guidelines_ledger.py` |
| `skills/make-brand-stack` | Procedural | both (`/make-brand-stack`) | The one-page reading of a brand — six load-bearing tiers (Root/Position/Point of View/Expression/Product/Stewardship), each a thesis sentence plus a cited elaboration; condenses, never invents |
| `skills/check-brand-orientation` | Procedural | both (`/check-brand-orientation`) | Gets your bearings before any work: inventories the corpus, reads it against the methodology as working/drifting/missing, proposes next steps by pipeline stage |
| `skills/check-brand-rubric` | Procedural | both (`/check-brand-rubric`) | Adversarially scores existing brand work against `brand-rubrics`' library — names failures with evidence and the test that reveals them, never flatters |
| `skills/council-rules` | Knowledge pack | model-only | What a council IS, domain-neutral: roster/persona contract, the roster FILE contract (`roster.md`'s table + `## Groups` + `## Role agents` schema, bijection, `VACANT`-lead convention), sub-councils, blind fan-out mechanics, severity taxonomy + 2-of-3 contested voting, the five synthesis shapes, calibration discipline, the two-phase model (blind first, chair-moderated deliberation second), and (new, `#840`) the role-agent contract (`references/role-agents.md`) — one addressable agent per role, its scoped convene semantics, and the `full`/`advisory` reserved-name rule — the machinery `check-brand-council` is an instance of, and what `make-council`/`make-critic` mint against. 8 reference files under `references/INDEX.md` (8 declared axes) |
| `skills/check-brand-council` | Procedural (orchestrator) | both (`/check-brand-council`) | Convenes the named-practitioner council as an INSTANCE of `council-rules`' machinery — roster membership is DATA (`references/roster.md`, roster-as-data, `#838`; role→agent mapping, `#840`), cited by this SKILL.md rather than restated in prose. Phase 1 (blind, unchanged): fans out unnamed `brand-judge` dispatches per persona (`skills/check-brand-council/references/critics/critic-*.md`, 14 files) by sub-council (strategy/design/voice/full) or a named roster group (e.g. `leads`) — this procedure's own sub-council enumeration is unchanged by `#840`'s new `creative` sub-council, which is convened directly via `agents/creative-convener` instead, 2-of-3 contested-severity voting, cross-critic synthesis (convergence, highest severity, productive tension, blind spot, verdict + 3 revisions). Phase 2 (`--deliberate`, new): dispatches `council-chair-agent` (renamed from `council-marshal`, `#840`) as Chair to moderate a deliberation round over the anonymized phase-1 findings. This procedure IS the phase-1 orchestrator — no separate agent for phase 1; phase 2 delegates to the Chair |
| `skills/file-brand` | Procedural | both (`/file-brand`) | Stamps a finished corpus into a distributable (plugin/Claude-chat skill/standalone MCP), or stamps the corpus repo itself into a Claude-ready seat (`project` form — `#841`), via `scripts/brand_stamp.py`, running `brand_lint.py` before ratifying. Always asks which form |
| `skills/file-brand-corpus` | Procedural | both (`/file-brand-corpus`) | Exports brand deliverables as a navigable Markdown corpus + self-contained site viewer (sticky nav, per-page ToC, GFM tables, mermaid, DOMPurify-sanitized) |
| `agents/brand-judge` | Agent | dispatched (unnamed, one persona inlined per call) | The read-only critic shell `check-brand-council` fans out to for phase 1, `council-chair-agent` fans out to for phase 2, and each `council-*-agent` role agent fans out to for its own scoped convene — carries the shared Critical/Major/Minor/Noise severity convention, the trust-boundary rule every persona file cites rather than restating, and the deliberation-round contract: respond to named peer findings, revise severity only with stated cause, propose a joint finding |
| `agents/council-chair-agent` | Agent | dispatched (unnamed, one call per council run with `--deliberate`) | The Chair — strict router/moderator for phase 2, patterned on `teamwork:fleet-marshal`'s contract (named mention only, no cross-plugin preload). Renamed from `council-marshal` (`#840`, plain-English naming ruling; contract/body unchanged). Routes the anonymized phase-1 finding set to each participating critic, collects each response through a channel that returns to it (never a named/mailbox dispatch — the stranding failure `council-rules` documents), and rolls up. Never judges, never revises a severity, never votes |
| `agents/strategy-convener`, `agents/design-convener`, `agents/voice-convener`, `agents/creative-convener` | Agent | dispatched directly (the EXTERNAL seat for a fleet/session — unlike `brand-judge`/`council-chair-agent`, never invoked by an orchestrating skill) | NEW (`#840`) — one addressable role agent per lens sub-council, named `<lens>-convener` (Kim's naming ruling: the orchestrator `{scope}-{role}` production, `convener` registered in `naming.manifest.json`'s `role_lex` — `council-<lens>-agent` was tried first and found structurally unreachable, `design` already sitting in `object_vocab` blocks it outright by the RoleLex/ObjectVocab disjointness invariant). Each reads `check-brand-council/references/roster.md`, fans `brand-judge` out unnamed over ONLY its own sub-council's seated active personas, and returns one phase-1-only rolled-up read (findings verbatim + the five synthesis shapes scoped to its lens); an empty/VACANT bench reports "no seats" and stops. `creative-convener` convenes the `creative` sub-council — seeded empty at minting, now seats `george-l`/`nick-l` (reseated `#849`, 2026-08-22); its lead stays VACANT (bench-seating ownership for the rest stays open). Deliberation stays `check-brand-council --deliberate`'s own job — out of scope for a role agent |
| `agents/muse-agent` | Agent | dispatched | The aspirational seat `make-brand-muse` dispatches — names the pull, never makes or judges |
| `agents/brand-writer` | Agent | dispatched | Extended voice/copy work — the words themselves, as distinct from `brand-guidelines`' voice *behavior* |
| `scripts/brand_corpus_mcp.py` | Script (MCP server) | `.mcp.json` (bundled) | ~160-line JSON-RPC 2.0 reference server: `list_brand_documents`, `search_brand`, `fetch_brand_section`, `outline_brand_document`, `get_brand_tokens` — read-only, path-guarded, scoped via `BRAND_CORPUS_DIR` |
| `scripts/brand_lint.py` | Script | CLI + selftest | Structural corpus check run before `file-brand`/`file-brand-corpus` ratify |
| `scripts/brand_stamp.py` | Script | CLI + selftest | Stamps a corpus into a plugin/skill/MCP distributable, or (`project` form) in place into the corpus repo's own `.claude/` scaffold — a facts consult skill, `/ask-brand`, `agents/brand-liaison.md`, `.mcp.json` — per `file-brand` |
| `scripts/build_sitemap.py` | Script | CLI + selftest | Builds the corpus site viewer's navigation, per `file-brand-corpus` |
| `scripts/guidelines_ledger.py` | Script | CLI + selftest | The append-only choice ledger + card-projection interface (`card` subcommand) `make-brand-guidelines` writes through and the `design-skills:brand-decomposer` seam (`nonoun-skills` marketplace, optional, when installed) reads |
| `scripts/corpus_migrate.py` | Script | CLI + selftest | Migrates a legacy corpus layout into the current numbered-layer convention |
| `scripts/corpus_provenance.py` | Script | CLI + selftest | Reads/writes per-document `contributors`/`sources` provenance frontmatter, per `brand-corpus` |
| `scripts/check_concepts.py` | Script | CLI + selftest | Checks a corpus for the Foundation Canon's rejected artifacts (archetypes, personas, vision/mission/values triplets, "brand DNA") |
| `scripts/calibration_check_strategy.py`, `scripts/calibration_check_design.py`, `scripts/calibration_check_voice.py`, `scripts/calibration_check_muse.py` | Script | CLI + selftest | Promoted from `skills/check-brand-council/assets/calibration/` — per-sub-council calibration fixtures for `check-brand-council`'s blind phase, unmodified by the S3 council-generalization refactor (the regression proof) |
| `scripts/calibration_check_deliberation.py` | Script | CLI + selftest | NEW (S3, `#826`) — calibrates the phase-2 deliberation round (`--deliberate`, `council-chair-agent` as Chair) against `skills/check-brand-council/assets/calibration/fixtures/deliberation-anonymized-finding-set.md`: cross-examination, defend-or-revise-with-cause, joint-finding proposal, and the trust-boundary probe |
| `scripts/calibration_replay.py` | Script | CLI + selftest | Promoted from `skills/make-brand-guidelines/assets/calibration/` — replays a recorded guidelines-ledger walkthrough against a fixture |
| `scripts/roster_check.py` | Script | CLI + selftest | NEW (`#838`, roster-as-data); extended `#840` — validates a council's `references/roster.md` against `council-rules`' roster-file contract: handle↔persona-file bijection both directions, non-empty sub-councils, `full` never a literal sub-council value, at most one `lead` row per sub-council, every `## Groups` entry resolving to a seated active handle or `VACANT`, and (new) the `## Role agents` mapping — a dangling agent handle FAILs, an unmapped role WARNs, a key naming `advisory` or an undeclared sub-council FAILs. A `VACANT` lead, and an ordinary sub-council seeded with zero active critics, are both named WARNINGs, never a FAIL |
| Per-skill `assets/calibration/` (in `check-brand-council`, `make-brand-guidelines`, `file-brand`) | Fixtures | n/a | The dated calibration runs + fixtures the promoted `calibration_*` scripts above formalize — re-homed under each owning skill by the S1 structure move (2026-08-20, `#824`); originals kept alongside the promoted scripts (their own READMEs document literal invocations that would need rewriting otherwise, disclosed rather than silently duplicated) |
| `.provenance/mcp-first-precedent.md` | Reference | n/a | brand-design is this estate's only MCP/`userConfig`-registered plugin — noted for any future plugin considering the same pattern |
| `.provenance/gate-lint-conversion.md` | Reference | n/a | Where `brand_lint.py`'s advisory checks are called from post-hook-retirement (Gate A ruling) — the exact CLI contract per calling command-skill |
| `.provenance/reviews/` | Reference | n/a | Three dated red-team records from the v0.2–v0.4 brand-forge cuts |

## The routing-proof fix (Phase 4, 2026-08-19)

A full blind-judge routing proof found `brand-rubrics` and `brand-guidelines` each losing every
one of their own trigger cases to a same-plugin action-twin (`check-brand-rubric`,
`make-brand-guidelines`) — both reference packs had copied near-duplicate action-phrased triggers
onto the skill that actually performs the action. Fixed by reframing both packs as
mechanics/methodology-lookup-only, with an explicit NOT-clause naming the action-twin; re-verified
live at 10/10 and 9/10. Read this as the standing convention for any future reference-pack +
action-twin pair in this plugin: the reference pack's description states *what the mechanism is*,
never *do this now* phrasing that its own action-twin already owns.

## Provenance and disposition

Ported from `brand-forge` v0.4.36 (source repo, frozen SHA above) via a five-phase overhaul
campaign: Phase 0/1 (governance skeleton, naming), Phase 2 (structural conversion — the
17-critic-agent council collapsed to 3 agents + `check-brand-council`'s own host-side fan-out
procedure), Phase 3 (knowledge-pack restructure to `pack-writing-rules`, doctrine edges, MCP
hardening), Phase 4 (eval suites, `collide.py` sibling-fence sweep, the full blind-judge routing
proof + fix, above). The source repo is left untouched — no pointer edit, no deprecation notice —
this migration is a fork, not a move.

**Phase 3 Track D (2026-08-19).** `brand-corpus`'s, `brand-guidelines`'s, and `brand-rubrics`'s
own `references/` were each ported from brand-forge (source repo + frozen SHA above) as part of
this same migration campaign — cited once here rather than restated identically in each pack's
own `## Provenance` section (centralized by the S1 structure move, 2026-08-20, `#824`).

Self-contained; the only soft cross-plugin mention is `design-skills:brand-decomposer` (the
`nonoun-skills` marketplace — a separate repo, not part of this estate, and not bundled here),
consulted for a deeper operability grade `brand-guidelines`/`make-brand-guidelines` optionally
hand off to.

---

v0.11.7 · 2026-08-23 · fixes #899: `harness_emit.py`'s Hermes `__init__.py` template emitted plain-str `os.path.join(...)` skill paths; Hermes's `register_skill` (`hermes_cli/plugins.py:3355`) calls `path.exists()` on that argument, so the first registration raised `AttributeError` and zero skills registered. Fixed upstream in harness (`Path`-joined paths + `description=` passthrough on every `register_skill()` call, sourced from each skill's own frontmatter); this plugin's `__init__.py` and `HARNESS-NOTES.md` regenerated to match. PATCH: overlay bytes only, no behavior change to this plugin's own skills.
v0.11.6 · 2026-08-23 · closes #895 (LLD-0025 W4): `HARNESS-NOTES.md`'s Pi section corrected from MCP drop-with-note to passthrough — this plugin's own `.mcp.json` (`brand-corpus`) already works with the third-party `pi-mcp-adapter` as-is (T-2 amendment, #887), no glue generated; its `${CLAUDE_PLUGIN_ROOT}`/`${user_config.corpus_dir}` tokens now flagged `[needs-substitution]` under the Pi row same as the Codex/Hermes rows already were. PATCH: overlay bytes only, no behavior change to this plugin's own skills.
v0.11.5 · 2026-08-23 · closes #891 (LLD-0025 W3): new plugin bytes — `harness_emit.py` (harness) now also derives a Pi overlay (`package.json` with `"pi": {"skills": ["./skills"]}`, plus `"prompts": ["./prompts"]` and one `prompts/<name>.md` template per command-only skill — R-5 amendment, #888: the human-only guard is preserved natively, a Pi prompt template expands only from a human keystroke) from this plugin's own manifest/SKILL.md frontmatter, alongside the Codex and Hermes overlays; `HARNESS-NOTES.md` gains a real Pi section, gated fresh by release_gate.py's widened G15 (`codex,hermes,pi`) — a cached install must refresh to receive the overlay. PATCH: overlay bytes only, no behavior change to this plugin's own skills.
v0.11.4 · 2026-08-23 · closes #890 (LLD-0025 W2): new plugin bytes — `harness_emit.py` (harness) now also derives a Hermes overlay (`plugin.yaml`, `__init__.py`'s `register(ctx)` — one `ctx.register_skill()` line per skill, nothing else registered this wave, `hermes-mcp.yaml` where `.mcp.json` exists) from this plugin's own manifest/SKILL.md frontmatter, alongside the Codex overlay; `HARNESS-NOTES.md` gains a real Hermes section, gated fresh by release_gate.py's widened G15 (`codex,hermes`) — a cached install must refresh to receive the overlay. PATCH: overlay bytes only, no behavior change to this plugin's own skills.
v0.11.3 · 2026-08-23 · closes #886 (LLD-0025 W1): new plugin bytes — `harness_emit.py` (harness) derives a Codex overlay (`.codex-plugin/plugin.json`, per-skill `agents/openai.yaml`, `HARNESS-NOTES.md`) from this plugin's own manifest/SKILL.md frontmatter, gated fresh by release_gate.py's new G15; a cached install must refresh to receive the overlay. PATCH: overlay bytes only, no behavior change to this plugin's own skills.
v0.11.2 · 2026-08-22 · creative sub-council SEATING phase (`#849`): Kim's 2026-08-21 vacancy
ruling lifted for two seats — `george-l` (voice→creative) and `nick-l` (strategy→creative)
reseated per the candidate mapping on `#849`'s Findings; `john-h`/`tim-d` stay put (borderline,
not seated). `check-brand-council/references/roster.md` and `council-rules`'
`role-pack-scaffolding.md` updated to reflect the new membership/counts; `creative` still has no
designated lead (VACANT).
v0.11.1 · 2026-08-22 · agent model retier (Kim's estate-wide ruling, live session): muse-agent → sonnet+xhigh; brand-judge → sonnet+high.
v0.11.0 · 2026-08-21 · Wave 2 of the bloat + spec-staleness overhaul (`plan-2026-08-brand-design-
bloat-overhaul`, seeds S1/S2/S3, `#844`/`#845`/`#846`): **S1** dieted `make-critic` (813→≤700),
`brand-methodology-rules` (857→≤700), `check-brand-rubric` (776→≤700) description content chars,
each verified `skill_lint` W8-clean and re-judged blind, scoped, against the full menu (0 dead/
stolen/leaked once one contested case — make-critic's t05, ".name-map.md attribution convention"
— was fixed and re-voted 2-of-3, per the v1.0.4/t05 dead-trigger class). **S2** deduped the 4
`*-facts` packs' three shared scaffolding blocks into a new `council-rules` reference
(`references/role-pack-scaffolding.md`, stating each pack's own lens count so it can't drift
again) and centralized the corpus/guidelines/rubrics provenance sentence onto this README's
existing "Provenance and disposition" § Phase 3 Track D — `measure.py duplicate_pairs` for the 20
cited pairs: 20 → 0. **S3** re-measured and trimmed the long-body flags per `bloat-audit`'s
CALIBRATION.md load-bearing test: `brand-judge`/`muse-agent` now clean (under 6 000); `check-
brand-council`/`make-council`/`make-critic` trimmed (16 735→15 010, 13 429→9 677, 12 929→8 763)
but remain over threshold — each overage justified line-by-line in the plan doc's Validation
section (dense, non-restated procedural content, not ceremony). Fresh-context checker passes on
every semantic trim caught and fixed two real regressions in the same change (a dropped
"no artifact named" failure branch in check-brand-council, two dropped file citations in
make-council) before landing. Semantic/description changes — minor bump.

v0.10.0 · 2026-08-21 · `brand_stamp.py` gains a fourth form, `project` (`#841`, modality 6+7):
stamps the corpus repo itself IN PLACE (no `-o`) into its own Claude-ready seat — `.claude/skills/
<brand>-facts/SKILL.md` (a consult skill reading the live in-repo corpus), `.claude/skills/
ask-brand/SKILL.md` (the `/ask-brand` command surface), `.claude/agents/brand-liaison.md` (the
judgment surface for cross-session perspective asks — cited, read-only, never invents a brand
position outside the corpus), and `.mcp.json` wiring the bundled `brand-corpus-mcp.py` at the
in-repo corpus. `--linked` (the live corpus, not a snapshot) is the effective default for this
form — the corpus already lives in the repo being stamped, so bundling a copy of a repo into
itself is the special case (`--snapshot`); repo root is derived by walking up from `<corpus>` to
the nearest `.git`, overridable with `--repo-root`. The modality-7 cross-session contract (message
the project's own session, or dispatch its `brand-liaison`; the MCP serves data only, never
opinion) is documented in `skills/brand-corpus/references/stamping.md`, per that file's
conventions — no separate PRD/SPEC. Ride-along fix: `brand_stamp.py --help`'s stale `/brand-stamp`
handle corrected to `/file-brand` (readiness/quality judgment line). `file-brand`'s "always asks
which form" step now offers four forms. New selftest fixtures for the `project` form (derive-root,
`--repo-root` override, `--snapshot`, a missing-liaison negative control, drift detection on the
in-repo MCP copy) — the existing `plugin`/`skill`/`mcp` fixtures untouched and still green.
Mechanical scaffolding only, per the existing contract — `verify`'s `_frontmatter_keys` helper
also gained hyphen support (`user-invocable:` wasn't matching before; needed for the new
`ask-brand` check, and a latent gap for every prior form's own hyphenated keys). A fresh-context
`skill-checker`/`agent-checker` pass on the generated templates (generator ≠ critic) caught real
gaps, folded in before ship: the facts skill was missing `disable-model-invocation`/
`user-invocable` dials entirely (lint-blocking) and had no `NOT for` fence; `ask-brand` competed
with the facts skill for model routing instead of staying a pure command surface (now
`disable-model-invocation: true`); `brand-liaison` cited a path that doesn't exist inside a
stamped repo, claimed a skill-loading capability the agent structurally lacks, stated `INDEX.md`
as unconditional when it's `--snapshot`-only, and had no dispatch-shape clause for its own
stated cross-session use. Semantic + structural change — minor bump.

v0.9.0 · 2026-08-21 · Council role agents (`#840`): one addressable agent per council role, the
EXTERNAL seat surface for fleets/sessions, distinct from the dispatch-only critic shell/Chair. NEW
domain-neutral axis `council-rules/references/role-agents.md` (8th axis) — what a role agent is,
its scoped phase-1-only convene semantics (read the roster, fan the critic-shell agent out unnamed
over ONLY its own sub-council's seated active personas, 2-of-3 voting scoped to that same
sub-council, the five synthesis shapes scoped to its lens, empty/VACANT-bench clean stop), and the
`full`/`advisory` reserved-name rule; `roster-file-contract.md` gains the `## Role agents` mapping
section's own data-file shape (dangling handle FAIL, unmapped role WARNING, a reserved-name or
undeclared key FAIL) plus the empty-ordinary-sub-council WARNING (same severity as a `VACANT`
lead, distinct from `advisory`'s quieter INFO). **RENAME**: `agents/council-marshal` →
`agents/council-chair-agent` (contract/body unchanged — Kim's 2026-08-21 plain-English naming
ruling: domain vocabulary, not fleet jargon); every reference repaired across
`check-brand-council`, `brand-judge`, `make-council` and its references, and
`calibration_check_deliberation.py` — a `fix-old-names`-style sweep found zero live stale
`council-marshal` mentions outside this ledger's own historical entries (append-only, never
rewritten). **NEW agents**: `strategy-convener`, `design-convener`, `voice-convener`,
`creative-convener` — one per lens sub-council, patterned off `brand-judge`'s own dispatch shape
but dispatched DIRECTLY rather than fanned out unnamed. Named `<lens>-convener` per Kim's naming
ruling (mid-build correction): the first-minted `council-<lens>-agent` shape was found
structurally unreachable — `design` already sits in `naming.manifest.json`'s `object_vocab`, and
RoleLex/ObjectVocab disjointness (ADR-0015 D3) blocks it outright, the same class of gap
`muse-agent` hit in S4/#827 — so the four agents mint as the orchestrator `{scope}-{role}`
production instead (`convener` newly registered in `role_lex`, a genuine profession word, no
disjointness collision), while `council-chair-agent` keeps its own name (`chair` registered in
`role_lex` too, cleanly — no collision, mirrors `marshal`/`judge`). Zero exemptions granted for
any of the five. `creative-convener` convenes a genuinely empty bench today (`creative` — a new
ORDINARY sub-council, not reserved like `advisory` — seeded with zero rows; bench-seating
ownership stays open, Kim seats it later). `roster.md` (`check-brand-council`) gains the
`creative` section and the `## Role agents` mapping (chair/strategy/design/voice/creative → their
five agents); `roster_check.py`'s selftest gains 7 new cases (empty-ordinary-sub-council, mapping
positive, dangling handle, unmapped role, section-absent, reserved-name key, undeclared key) — all
green. `make-council` now mints one role agent per sub-council alongside its critic-shell agent
(`references/roster-and-chair-wiring.md` gains the role-agent wiring checklist, patterned off
`strategy-convener`) and seeds the `## Role agents` mapping when standing up a new instance.
Non-goals (ruled in the seed): `check-brand-council`'s own phase-1 host-side orchestration and
sub-council enumeration are UNCHANGED — `creative` is convened today only via `creative-convener`,
never through `/check-brand-council` directly; no advisory role agent (no
lead, no adversarial vote weight — `advisory` never gets one). Calibration coverage for the
convene behavior itself stays a named open (payload/script layer — `roster_check.py` + the fresh
agent-checker passes — is the whole harness this round). **Post-build scope addition, same
ticket:** Kim designated the two prior `VACANT` leads — `paula-s` (design) and `david-a` (voice) —
leaving `creative` as the roster's only remaining `VACANT` seat (its bench itself stays open, per
the ruling above). Semantic + description changes throughout (`council-rules`, `make-council`) —
minor bump.

v0.8.1 · 2026-08-21 · Closing-pass fix on the merged `#838` roster-as-data + advisory work: a
final independent fresh-context `harness:skill-checker` re-read (requested at handback, since
several post-review fixes had landed without a second pass) found the substantive advisory
machinery internally consistent end to end (pairing, vote/push exclusion, zero-advisor INFO — all
verified against a live `roster_check.py` run), with one real minor gap of its own: `make-critic`
step 5's case 1 (seat into a user-named sub-council) didn't say what happens when the named
sub-council doesn't exist in the target roster yet — it could read as seating directly under an
unregistered name instead of routing to case 3's explicit new-sub-council proposal (which alone
carries the mandatory `## Groups` `leads:` entry). One-line guard added; no other changes. The
pass's other findings (several split code-spans in make-critic's description/body, one
restated-not-cited passage in check-brand-council's pre-existing phase-1 step 5) predate this
ticket entirely and are out of its scope — logged here rather than silently fixed, for a future
pass.

v0.8.0 · 2026-08-21 · Roster-as-data (`#838`): councils/committees/leadership moved out of
SKILL.md prose tables into maintained data — `references/roster.md` per council instance (schema:
handle↔persona-file bijection, non-empty sub-councils, `full` reserved as the union, `## Groups`
resolving only to seated handles or `VACANT`, `role`/`status` enums), plus a mechanical check
(`scripts/roster_check.py`, selftest per `.claude/rules/scripts.md`) proving it. `council-rules`
gains the roster FILE contract (`references/roster-file-contract.md`, 7th axis) as the schema
every instance cites. `check-brand-council` drops its inline 14-critic roster table for a citation
to `references/roster.md` and resolves sub-council/group tokens (e.g. `leads`) against the file —
seeded from the CURRENT roster: strategy (6, `luke-s` lead), design (4) and voice (4) both carry
no designated lead, declared `VACANT` in the `leads` group rather than invented. `make-critic`
step 5 (seat a critic) now appends a `roster.md` row instead of editing SKILL.md — a data edit at
floor-tier verification (`roster_check.py`'s exit code), never a SKILL.md semantic edit under
`plugin-authoring.md`'s checker-pass invariant. `make-council` seeds a `roster.md` per the same
contract when minting a new council instance. Resolved two owed questions from the seed: the
script forks standalone (`roster_check.py`, not a `brand_lint.py` extension — a different
structural-smell-vs-roster-schema job) and the file format is a markdown table + `## Groups`
section (not frontmatter-structured md). **Mid-build addition (same PR/version, Kim's live
ruling):** a reserved, user-minted `advisory` sub-council — seeded with zero critics on purpose
(personas are minted via `/make-critic`, never shipped). `roster-file-contract.md` gains `role:
advisor`, paired bidirectionally and exactly with `sub-councils: advisory`; advisors ride along in
fan-out and feed synthesis but are excluded from 2-of-3 contested-severity voting and from
`check-brand-council`'s adversarial-calibration push (`severity-and-voting.md` gained a one-line
eligibility pointer). `check-brand-council` convenes `advisory` cleanly when empty rather than
erroring. `make-critic` seats a new critic into `advisory` by default whenever the user names no
specific lens sub-council. `roster_check.py` reports a zero-advisor state as a named INFO line,
distinct from the VACANT-lead WARNING, never a failure.

v0.7.0 · 2026-08-21 · S6 campaign proof (`#829`, wave 4 — the final wave of the council-as-
platform overhaul): full blind `/check-routing brand-design` (20 suites/182 cases, all
model-invocable, none excluded) — clean at 0 dead/0 stolen/0 leaked, `.claude/ops/
routing-report.json` updated. The blind run surfaced two REAL routing defects, both fixed
same-change per the standard stolen-tuning treatment: (1) `brand-methodology-rules` lost 5 of its
own trigger cases to `make-brand` (identical action-vs-reference collision S2's own
`brand-guidelines` fix already solved) — narrowed to a pure methodology reference, its evals.json
rewritten reference-lookup-first with `make-brand` as the no-trigger fence; (2) `make-critic` and
`check-brand-rubric` each leaked into two of the four role-family packs' own lens-grounding
questions (`brand-strategy-facts`/`brand-voice-facts` "I'm minting a critic — what lens gaps
exist" and "does our house style hold consistent" cases) — both gained a NOT-clause fencing
grounding/knowledge questions back to the matching pack; a scoped re-judge confirmed both fixes
live. `authorkit:fix-old-names` swept zero LIVE stale-handle references (0 FAIL/27 WARN, every
warn a pre-existing dated/filename mention in the unrelated `docs/` plugin, none in
`brand-design`). The mint-and-run walkthrough: minted a demonstration critic (`sam-r` —
brand-as-lived-experience, the promise-delivery gap; a genuinely uncovered lens verified against
all four role packs' own `failure-modes.md`/`lenses.md`), seated it in `check-brand-council`'s
strategy sub-council, ran phase 1 (blind, 3 critics against a planted-defect sample artifact —
independently caught its target defect, checker-passed against a sibling persona), phase 2
(chair-moderated deliberation, the council-marshal pattern), and the declared Project
single-context sequential mode — then unseated it (persona file, roster row, calibration fixture,
and `.name-map.md`/`.gitignore` entry all reverted) per the mint procedure's own rollback path,
since a one-artifact demo doesn't earn a permanent 15th seat. `.claude/docs/plan/
plan-2026-08-brand-design-overhaul.md` flipped to `status: complete` (no `.claude/docs/` archive
convention exists yet for a finished PLAN, so it stays in place per that file's own fallback,
noted inline). Semantic + description + eval changes — minor bump.

v0.6.0 · 2026-08-20 · S5 role-category knowledge packs (`#828`, wave 2 of the council-as-platform
overhaul): the 14 `check-brand-council` critics clustered into 4 role families from their OWN
personas (working hypothesis confirmed, not forced) — **strategy** (Brian C., John H., Luke S.,
Mark P. — substance-over-assembly tests on the strategic artifact: becoming/transformation,
zag-vs-zig, primary-source provenance, the language bow tie), **identity-design** (Jessica W.,
Massimo V., Matt W., Paula S. — the visual/systemic identity: find-the-weird/human-signature,
three-level coherence, editorial typography as recurring grammar, liquid identity/editorial
refusal), **voice-writing** (David A., Mary N., Tim D. — the written voice: respect for the
reader, query-not-assertion house style, the premium brief), **advertising-creative** (George L.,
Nick L., Rory S. — creative execution: the Big Idea/word-image collision, inventive-vs-expressive
+ creative infrastructure, psycho-logic/cheap alchemy). Full per-critic evidence lines recorded in
each pack's own `references/lenses.md`. NEW knowledge packs `brand-strategy-facts`,
`brand-identity-facts`, `brand-voice-facts`, `brand-advertising-facts` — pack-writing-rules
conformant (4 declared axes each: lenses/failure-modes/canonical-tests/vocabulary, flat corpus, no
INDEX at this size, `sources.md` provenance in trust order distinguishing `[verified]`
persona-file quotes from explicitly marked `[inferred]` general-knowledge parallels, none
fabricated); own eval suites. Fresh-context `harness:skill-checker` pass on all four new
SKILL.md files plus a `harness:wording-checker` pass on the `make-critic` edit — all 5 **PASS**,
zero `[verified]`-claim mismatches against the 14 persona files on spot-check; each pack carried
2-3 minor fixes (description fence reformatted to the parseable `NOT for <thing> (<owner>)` form,
a Grep-first consult-entry line + one-line answer contract added, one "mint a new brand-X critic"
use-phrase reworded to "grounding for minting an X critic" to de-conflict with `make-critic`'s own
eval, a typo, and a fragile hardcoded step-number citation loosened) — every fix applied before
this version closed (full per-pack verdicts: issue #828 Findings). Scoped blind re-judge (3
unnamed `harness:routing-judge` dispatches, full 20-skill brand-design menu post-fix) over the 5
new/fence-touched suites (the 4 packs + `make-critic`, 58 cases): 57/58 clean on the first pass;
one contested case (`brand-strategy-facts` t02, "why did the council flag...") stolen once by
`check-brand-council` on single-judge noise, resolved 2-of-3 for the expected owner on the vote
round — annotated in `evals.json` per the re-judge convention, no description chase since the
vote resolved clean. Fenced against each other (disjoint role/critic
coverage), against `council-rules` (machinery vs. role knowledge), against
`brand-methodology-rules` (the maker's method vs. the judge's lens on the same territory — e.g.
`brand-voice-facts` vs. `references/editorial-style-guide.md`, `brand-advertising-facts` vs.
`references/creative-collaboration.md`), and against `make-critic` (procedure vs. grounding
corpus) — reciprocal: `make-critic` now reads the matching family pack before drafting a
same-family persona (additive to, never a replacement for, its existing 14-persona grounding
read), its overlap check now reads a pack's `failure-modes.md`/
`canonical-tests.md` directly, and its References table + evals gained the four packs (4 new
no-trigger cases). 4 new `ObjectVocab` entries registered in the root `naming.manifest.json` —
`brand-strategy`, `brand-identity`, `brand-voice`, `brand-advertising` (multi-token, `{object}-
facts` production per REQ-002 §3.2/ADR-0011; anti-ambiguity checked against the full 129-entry
`object_vocab` plus `VerbLex`/`ProcessLex`/`TopicLex`/`RoleLex` — no collision, no shadowing of the
existing single-token `brand`/`critic` entries under longest-match resolution) — grammar-clean
per `authorkit:naming-audit` (24 artifacts, 0 errors, exemptions unchanged at 55). Semantic
changes throughout — minor bump.

v0.5.0 · 2026-08-21 · S4 minting (`#827`, wave 2 of the council-as-platform overhaul): NEW
procedure `make-critic` — mints one new critic persona end to end (persona template grounded in
the 14 existing `check-brand-council` files as worked examples; the `.name-map.md` gitignored
real-practitioner attribution discipline gains its canonical documented home here; roster + sub-
council registration; a calibration fixture; a mandatory fresh-context `harness:wording-checker`
pass before a persona seats); NEW procedure `make-council` — stands up a whole new council
instance (domain intake, the new instance's own roster file home mirroring `check-brand-council`'s
layout, sub-council groupings, chair wiring that REUSES `council-marshal` unchanged by default —
its input contract already parameterizes the critic-shell agent by name — a new critic-shell agent
patterned off `brand-judge`'s structure, a calibration seed, both run modes); both new procedures
cite `council-rules` for every shared mechanic throughout, never restating it, and reciprocally
fence against each other, `council-rules`, `check-brand-council`, and `harness:make-agent`
(a critic is a persona-inlined prompt fanned out through an existing critic-shell agent, never a
standalone dispatched agent of its own) — `council-rules`' own description retires its "forthcoming
make-council/make-critic" forward reference now that both exist. `critic` registered in the root
`naming.manifest.json` ObjectVocab (anti-ambiguity checked against every existing lexicon —
no collision) so `make-critic`'s own name conforms as a new mint (ADR-0011 D8). **`muse`
RoleLex registration — attempted, found structurally blocked, NOT landed:** the ticket's own
ask (register `muse` in RoleLex so `muse-agent`'s exemption retires, 0 errors, no rename) is
mechanically unreachable as specified — verified empirically against
`authorkit:naming-audit`'s validator two ways: (1) `muse` is already a registered `ObjectVocab`
canonical (load-bearing for `make-brand-muse`'s own name resolution), so adding it to `RoleLex`
violates ADR-0015 D3's RoleLex/ObjectVocab disjointness invariant outright; (2) independent of
(1), the orchestrator `{scope}-{role}` production requires a scope token before the role
(`authorkit/skills/naming-conventions/references/GRAMMAR.md`: "A bare RoleLex word with no scope
token still fails — the production always requires `{scope}-{role}`, never a bare role") —
`muse-agent`'s residue is the single bare token `muse`, which can never satisfy that production
regardless of RoleLex membership. `authorkit:manifest-authoring`'s own procedure additionally bars
retiring an exemption "only when the corresponding rename has landed" — no rename runs under this
ticket's own kill-switch ruling. The exemption stays standing (55 unchanged, `muse-agent` still
`[EXMPT]`); this is named as a discovered blocker for Kim's call (a follow-up rename ticket, e.g.
`brand-muse` or `brand-muse-agent`, vs. leaving the exemption under D8's grandfather clause
permanently) rather than silently forced through or silently dropped. Evals updated on
`make-critic`/`make-council` (fresh suites) and on `council-rules`/`check-brand-council`
(reciprocal no-trigger cases added). Semantic changes throughout — minor bump.

v0.4.0 · 2026-08-20 · S3 council generalization (`#826`, wave 2 of the council-as-platform
overhaul): NEW knowledge pack `council-rules` — the domain-neutral council machinery (roster/
persona contract, sub-councils, blind fan-out mechanics, severity taxonomy + 2-of-3 voting, the
five synthesis shapes, calibration discipline, the two-phase model) — extracted once so
`check-brand-council` becomes a configuration of it rather than the machinery's only copy, and so
S4's `make-council`/`make-critic` have something to mint against; `check-brand-council` refactored
to cite it throughout, blind-phase behavior preserved byte-for-byte (all four blind calibration
fixtures pass unmodified); NEW agent `council-marshal` — the Chair, patterned on
`teamwork:fleet-marshal`'s strict-router contract (named mention, no cross-plugin preload), owns
phase-2 orchestration/collection/roll-up, never judges; two-phase council in `check-brand-council`
(`--deliberate`): phase 1 unchanged, phase 2 chair-moderated deliberation over the anonymized
phase-1 finding set, collected only through channels that return to the Chair (never a named/
mailbox dispatch — the 2026-08-20 stranding incident this encodes); `brand-judge` gains the
deliberation-round contract (respond to named peer findings, revise severity only with stated
cause, propose a joint finding), blind-phase contract untouched; NEW deliberation calibration
fixture + `calibration_check_deliberation.py` (selftest green); both phases declare the Project
single-context degraded mode (sequential persona simulation, Chair as an in-context role, per S2's
run-modes convention); `council`/`marshal`/`rules` were all already-registered manifest tokens
(anti-ambiguity check: verified against the root `naming.manifest.json`'s 128+-entry
`object_vocab`/`role_lex`/`process_lex` before minting — no new vocabulary required). Semantic
changes throughout — minor bump.

v0.3.0 · 2026-08-20 · S2 portability (`#825`, wave 2 of the council-as-platform overhaul): the
corpus-resolution ladder (MCP tools → filesystem corpus layout → Claude Project knowledge, with
the absent-from-uploads vs. missing-from-the-brand orientation) defined once in `brand-corpus`,
cited by its consumers; every procedural skill declares its run modes (Full Claude Code/Cowork vs.
Project single-context, or filesystem-only disclosed where bundled scripts are load-bearing —
`file-brand`, `file-brand-corpus`; `make-brand-guidelines` degrades to an in-chat ledger the user
re-uploads); `brand-corpus`/`brand-methodology-rules`/`brand-rubrics`/`brand-guidelines` dieted
(long-body flags cleared, nothing load-bearing cut — moved to `references/`) and
`brand-methodology-rules`'s description diet to ≤700 chars; the manifest's migration-placeholder
description replaced with an evals-first rewrite. Semantic/description changes — minor bump.

v0.2.0 · 2026-08-20 · S1 structure re-home (`#824`, wave 1 of the council-as-platform overhaul):
zero stray root dirs (`references/`, `calibration/`, `reviews/`, `templates/` moved under their
owning skill or `.provenance/`), every referrer path repaired (SKILL/agent bodies, the promoted
`calibration_*`/`build_sitemap`/`brand_stamp` scripts' fixture paths), the stale
`design-skills:brand-decomposer` handle disambiguated with its real (`nonoun-skills`) marketplace
everywhere it's cited live, and the triplicated brand-forge provenance paragraph centralized to
this README's "Provenance and disposition" section. Structural/breaking path move — minor bump.

v0.1.0 · 2026-08-19 · initial migration from brand-forge, full Phase 0-4 overhaul (council
restructure, knowledge-pack modernization, eval suites, routing-proof fix)
