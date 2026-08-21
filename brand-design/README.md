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
| `skills/council-rules` | Knowledge pack | model-only | What a council IS, domain-neutral: roster/persona contract, sub-councils, blind fan-out mechanics, severity taxonomy + 2-of-3 contested voting, the five synthesis shapes, calibration discipline, and the two-phase model (blind first, chair-moderated deliberation second) — the machinery `check-brand-council` is an instance of, and what `make-council`/`make-critic` (S4) will mint against |
| `skills/check-brand-council` | Procedural (orchestrator) | both (`/check-brand-council`) | Convenes the named-practitioner council as an INSTANCE of `council-rules`' machinery — the brand roster + sub-councils are this skill's own configuration. Phase 1 (blind, unchanged): fans out unnamed `brand-judge` dispatches per persona (`skills/check-brand-council/references/critics/critic-*.md`, 14 files) by sub-council (strategy/design/voice/full), 2-of-3 contested-severity voting, cross-critic synthesis (convergence, highest severity, productive tension, blind spot, verdict + 3 revisions). Phase 2 (`--deliberate`, new): dispatches `council-marshal` as Chair to moderate a deliberation round over the anonymized phase-1 findings. This procedure IS the phase-1 orchestrator — no separate agent for phase 1; phase 2 delegates to the Chair |
| `skills/file-brand` | Procedural | both (`/file-brand`) | Stamps a finished corpus into a distributable (plugin/Claude-chat skill/standalone MCP) via `scripts/brand_stamp.py`, running `brand_lint.py` before ratifying. Always asks which form |
| `skills/file-brand-corpus` | Procedural | both (`/file-brand-corpus`) | Exports brand deliverables as a navigable Markdown corpus + self-contained site viewer (sticky nav, per-page ToC, GFM tables, mermaid, DOMPurify-sanitized) |
| `agents/brand-judge` | Agent | dispatched (unnamed, one persona inlined per call) | The read-only critic shell `check-brand-council` fans out to for phase 1 and `council-marshal` fans out to for phase 2 — carries the shared Critical/Major/Minor/Noise severity convention, the trust-boundary rule every persona file cites rather than restating, and (new) the deliberation-round contract: respond to named peer findings, revise severity only with stated cause, propose a joint finding |
| `agents/council-marshal` | Agent | dispatched (unnamed, one call per council run with `--deliberate`) | The Chair — strict router/moderator for phase 2, patterned on `teamwork:fleet-marshal`'s contract (named mention only, no cross-plugin preload). Routes the anonymized phase-1 finding set to each participating critic, collects each response through a channel that returns to it (never a named/mailbox dispatch — the stranding failure `council-rules` documents), and rolls up. Never judges, never revises a severity, never votes |
| `agents/muse-agent` | Agent | dispatched | The aspirational seat `make-brand-muse` dispatches — names the pull, never makes or judges |
| `agents/brand-writer` | Agent | dispatched | Extended voice/copy work — the words themselves, as distinct from `brand-guidelines`' voice *behavior* |
| `scripts/brand_corpus_mcp.py` | Script (MCP server) | `.mcp.json` (bundled) | ~160-line JSON-RPC 2.0 reference server: `list_brand_documents`, `search_brand`, `fetch_brand_section`, `outline_brand_document`, `get_brand_tokens` — read-only, path-guarded, scoped via `BRAND_CORPUS_DIR` |
| `scripts/brand_lint.py` | Script | CLI + selftest | Structural corpus check run before `file-brand`/`file-brand-corpus` ratify |
| `scripts/brand_stamp.py` | Script | CLI + selftest | Stamps a corpus into a plugin/skill/MCP distributable, per `file-brand` |
| `scripts/build_sitemap.py` | Script | CLI + selftest | Builds the corpus site viewer's navigation, per `file-brand-corpus` |
| `scripts/guidelines_ledger.py` | Script | CLI + selftest | The append-only choice ledger + card-projection interface (`card` subcommand) `make-brand-guidelines` writes through and the `design-skills:brand-decomposer` seam (`nonoun-skills` marketplace, optional, when installed) reads |
| `scripts/corpus_migrate.py` | Script | CLI + selftest | Migrates a legacy corpus layout into the current numbered-layer convention |
| `scripts/corpus_provenance.py` | Script | CLI + selftest | Reads/writes per-document `contributors`/`sources` provenance frontmatter, per `brand-corpus` |
| `scripts/check_concepts.py` | Script | CLI + selftest | Checks a corpus for the Foundation Canon's rejected artifacts (archetypes, personas, vision/mission/values triplets, "brand DNA") |
| `scripts/calibration_check_strategy.py`, `scripts/calibration_check_design.py`, `scripts/calibration_check_voice.py`, `scripts/calibration_check_muse.py` | Script | CLI + selftest | Promoted from `skills/check-brand-council/assets/calibration/` — per-sub-council calibration fixtures for `check-brand-council`'s blind phase, unmodified by the S3 council-generalization refactor (the regression proof) |
| `scripts/calibration_check_deliberation.py` | Script | CLI + selftest | NEW (S3, `#826`) — calibrates the phase-2 deliberation round (`--deliberate`, `council-marshal` as Chair) against `skills/check-brand-council/assets/calibration/fixtures/deliberation-anonymized-finding-set.md`: cross-examination, defend-or-revise-with-cause, joint-finding proposal, and the trust-boundary probe |
| `scripts/calibration_replay.py` | Script | CLI + selftest | Promoted from `skills/make-brand-guidelines/assets/calibration/` — replays a recorded guidelines-ledger walkthrough against a fixture |
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
