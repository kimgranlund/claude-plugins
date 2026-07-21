---
doc-type: adr
id: adr-0006
status: proposed
date: 2026-07-20
owner: kim.granlund
supersedes: null
---
# ADR-0006 — Execute the simple-naming-paradigm rename campaign, estate-wide

## Context

The `naming-rules` skill (forge 1.40.0, PR #61) established the simple naming paradigm: five
checkable tests, per-kind name shapes, one verb per concept. Its worked example,
`forge 1.14.0/skills/naming-rules/references/estate-rename-map.md`, maps the full estate —
9 plugins, ~130 members — from the legacy grammar to the paradigm, and as of 2026-07-20 every
row carries a human ruling (the four originally-open rows were closed in one batched round:
`checking-rules`, the chore family, `agent-residency-facts`, `break-down-*`).

Offered the choice (new-names-only · pilot · full campaign · defer), the maintainer chose
**full campaign** (2026-07-20, in-session). Names are APIs here: plugin names are install
identity and the `/plugin:skill` invocation surface, skill names are the routing surface, agent
names are dispatch types. ADR-0001 executed the same class of change at 1/15th the scale
(8 skills, ~200 references) and its discipline held; this ADR scales that discipline.

## Decision

1. **The manifest is the map.** `estate-rename-map.md` at this ADR's commit is the ratified
   old→new manifest, the single source of truth. Plugin layer: forge→`harness`,
   scribe→`docs`, orchestration→`teamwork`, ui→`screens`, design-systems→`design-kits`,
   agentic-ui→`agent-protocols`; color, typography, and llm keep their names (term-of-art
   shelves — the `llm-facts`/`llm-protocols` candidates are ratified OUT: each stutters
   against every member, see Decision 7; flagged for maintainer override since `llm-facts`
   was the in-session lean). After acceptance, map edits are row-status marks only
   (done/blocked); a substantive old→new change needs a superseding ADR.
2. **Standards flip first (Phase 0).** Before any rename PR: `naming-rules` becomes the
   estate's naming canon; agent-/skill-authoring-standards §Naming sections and the corpus
   Vol 2 grammar get dated supersession notes pointing at it; `skill_lint` W5's
   `KNOWLEDGE_NOUNS` set gains `facts` and `rules` with selftest fixtures (W4 needs no
   change — its check keys on the name's last segment, and no ratified name ends `-er`/`-or`
   outside the agent tier where that head is correct) — so every subsequent rename lints
   clean on arrival.
3. **One plugin per PR, leaf-first** (campaign branches per ADR-0002): color → typography →
   llm → agentic-ui → design-systems → ui → orchestration → scribe → forge last (the toolchain
   renames itself only after every consumer of its old handles is gone).
4. **Per-PR contract** (each plugin): baseline blind `/eval-run` captured and recorded BEFORE
   the rename commit; rename per manifest; every live reference rewritten in the same change
   (descriptions, fences, preloads, suites' `skill:` fields, READMEs, MANUAL, root CLAUDE.md
   routing rows, cross-plugin soft mentions workspace-wide — grep proof); reciprocal fences
   re-closed; full blind `/eval-run` re-measure — including every sibling suite whose fences
   changed; `release_gate` CLEAN; **major version bump** + ledger entry naming this ADR for
   the renamed plugin AND a version bump + ledger line for every sibling plugin the sweep
   touched.
5. **Plugin renames change install identity.** No alias mechanism exists (ADR-0001): old names
   fail visibly. Directory names keep their existing paths — this ADR AMENDS the workspace
   dir-naming convention (`<manifest-name> <version-at-creation>` becomes historical: the dir
   records the name-and-version at creation, the manifest carries the current name). The root
   CLAUDE.md's opening paragraph and entry table are named repair targets in the FIRST rename
   PR (stale-context invariant), recording the dir→name aliases.
6. **Deprecation path** = announcements, not shims: a transition table (old→new) in each
   renamed plugin's README, CHANGELOG entries, and the rule that old MEMBER handles are
   greppable only in CHANGELOGs, ADRs, and `.refactor-attic/`.
7. **Term-of-art shelf exception to the stutter invariant.** The root CLAUDE.md bans plugin
   names equal to member domain prefixes. For `color` and `llm`, de-prefixed member names
   would lose their standalone meaning (`perception-facts`, `streaming-facts`), so the
   fully-qualified stutter (`/color:color-theory-facts`, `/llm:llm-gateway-facts`) is
   accepted as a recorded, reasoned exception: routing is description-driven and the
   qualified form is rare. The invariant's wording gains a pointer to this exception in
   Phase 0.

## Consequences

- **Breaking everywhere, paid once**: external installs re-add plugins under new names; anyone
  typing old skill handles migrates via the README transition tables.
- One grammar estate-wide; the paradigm's "governs NEW names" scope line in `naming-rules`
  amends to "governs all names" when the last PR lands.
- Estimated 9–10 PRs across multiple sessions; each is independently shippable and
  gate-clean, so the campaign can pause at any boundary without a broken estate.
- Routing-regression risk during transition is bounded per-plugin by the eval-run parity gate
  (ADR-0001's acceptance pattern).

## Alternatives considered

- **New-names-only** (the session's recommendation): zero cost, zero breakage; rejected by the
  maintainer — it preserves two grammars indefinitely.
- **Pilot one plugin first**: pricing information only; rejected — every piloted rename would
  be re-touched when the campaign proper ran.
- **Aliasing old names**: no platform mechanism; rejected as in ADR-0001.

## Acceptance

- Every plugin manifest and member name matches the map. For every old MEMBER handle in the
  map, and every invocation-shaped token of a renamed plugin (`/forge:`, `"name": "forge"`
  manifest fields, `skill: forge:` suite fields, `forge:` skill-qualified mentions),
  `grep -rn` across the workspace returns only CHANGELOG/ADR/attic hits. Frozen directory
  paths (`forge 1.14.0/…`) and bare-word English collisions are explicitly exempt — the map's
  rows are the grep manifest.
- `skill_lint.py` estate sweep: zero warnings under the Phase-0 grammar.
- Post-rename blind eval-run per plugin: routing at parity or better vs pre-rename scores.
- `release_gate.py` CLEAN 0 fail / 0 warn for all nine plugins; CI green on every campaign PR.
- Root CLAUDE.md routing table, memory index, and corpus snapshots refreshed from the renamed
  sources of record.
