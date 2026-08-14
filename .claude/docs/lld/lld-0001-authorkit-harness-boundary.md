---
doc-type: lld
id: lld-0001-authorkit-harness-boundary
status: draft
version: 0.1.0
date: 2026-08-13
owner: kim.granlund
spec: spec-naming-convention
ticket: nonoun-plugins#197
adr: adr-0011
---
# LLD — authorkit↔harness boundary (design phase, issue #197)

**Verdict, head-first: the boundary does NOT proceed as originally scoped.** Of the eight
candidates named in #197 (`make-skill`, `make-agent`, `make-hook`, `skill-writing-rules`,
`agent-writing-rules`, `prompt-wording-rules`, `naming-rules`' grammar half, `fix-old-names`'
rename machinery), mechanical dependency-closure (`surface_map.py check`) and ADR-0011's own
ratified text together permit exactly **one** clean move today — `fix-old-names` — and even that
one is gated on ADR-0011's ratification for a routing reason, not a dependency one. Everything
else fails a hard edge, or is asking for something ADR-0011 itself already ruled against. This is
a defended no-partition-as-scoped verdict (`plan-plugin-split`'s own escape hatch), not a forced
roster. Design phase only — nothing below is executed; extraction, renames, and ADR-0011's status
flip all wait for Kim's word.

## Components

### The roster, verdict-first (`/plan-plugin-split` analysis over the harness↔authorkit cut)

Method: `surface_map.py map harness` — 75 nodes (skills+agents+scripts+hooks), 367 edges,
re-measured 2026-08-13 — and `authorkit`, then `check` against a candidate partition manifest —
the mechanical half; job clustering / dependency closure / namespace / lifecycle (the four
tests) as judgment on top.

| Candidate | Verdict | Evidence |
|---|---|---|
| `fix-old-names` (+ `fix_old_names.py`) | **MOVE** — mechanically clean | `surface_map.py check` on a 2-member partition: 0 fail, 1 soft seam (6 mentions: `big-change-git-rules`, `clean-repo`, `make-script`, `make-skill`, `naming-rules`, `sort-issues` — all stay in harness). Job fit: its stated job is propagating a rename wave to repos that merely *install* a plugin — exactly authorkit's own charter ("used to refactor existing... skills/commands/agents" in the estates it audits, disabled here). Self-contained script, no shared-script dependency. |
| `make-skill`, `make-agent`, `make-hook` | **DO NOT MOVE — dead on arrival** | All three template `${CLAUDE_PLUGIN_ROOT}/scripts/skill_lint.py` directly in their own lint-and-fix loop (verified by grep, not just the graph: `make-skill` SKILL.md:86, `make-agent` SKILL.md:87, `make-hook` SKILL.md:62). `skill_lint.py` is harness's OWN PostToolUse-hook + ship-gate validator for every harness skill/agent, not authoring-family-scoped — moving the three forges without it strands their own lint step; moving `skill_lint.py` too multiplies the blast radius past every other harness member's hook enforcement. `surface_map.py check` FAILs this cut mechanically: `script edge crosses plugins authorkit -> harness (['make-agent->skill_lint.py', 'make-hook->skill_lint.py'])` — the tool prints only its first two offending edges (`surface_map.py`'s own truncation, not evidence `make-skill` is clean; its identical `skill_lint.py` script edge is confirmed directly by grep above). |
| `skill-writing-rules`, `agent-writing-rules`, `prompt-wording-rules` | **DO NOT MOVE — dead on arrival** | Hard `preload` edges: `skill-checker` preloads `skill-writing-rules`; `agent-checker` and `chore-lead` preload `agent-writing-rules`; `wording-checker` preloads `prompt-wording-rules`. These four checker/coordinator agents review or preload standards for **every** harness skill and agent, not just the authoring family, and are dispatched from inside harness (`check-all-skills`, `check-all-agents`, `chore-lead`) while authorkit stays **disabled in this workspace** (its own README, verbatim: "enabled only in the estates it audits... the permanent boundary between the two is deferred to a companion feature record (issue #197)"). Moving the standards without the checkers strands the preloads; moving the checkers into a disabled plugin breaks harness's own self-hosting quality gate here. |
| `naming-rules`' "grammar half" | **REFRAME, not move — contradicts ADR-0011's own ratified text** | ADR-0011 D9 (already ruled, not this phase's call): "On acceptance: `harness:naming-rules`... receives a dated supersession note pointing at the spec." The spec "lands as a plain document at `.claude/docs/spec/`... **not a routable skill**." Nothing in D9 sends `naming-rules`' content to authorkit. authorkit's own `naming-conventions` skill (already shipped via #196) independently carries the *new* grammar for the estates authorkit audits (the adia estates) — a separate, legitimate artifact, not a destination for harness's retiring one. The ticket's Acceptance framing and the ADR it depends on disagree; reported here, not silently reconciled. |

### Cross-cutting blocker: the enablement collision (applies even to the one clean mover)

authorkit ships **disabled** in this workspace's `enabledPlugins` specifically to avoid its
`naming-conventions` skill colliding with harness's `naming-rules` for the same "what should I
name this" trigger space (authorkit README, verbatim, citing #197 as the record that owns lifting
this). Moving `fix-old-names` to authorkit doesn't help anyone in *this* repo unless authorkit is
also enabled here — which reopens exactly that collision unless `naming-rules` is retired/
superseded first, which is itself gated on ADR-0011 ratification. So the one mechanically-clean
move is still ratification-sequenced, for a routing reason rather than a dependency-closure one.

### Rejected-alternatives ledger

| Alternative considered | Killed by |
|---|---|
| Move the full 8-candidate roster as literally named | Test 2 (dependency closure): 3 hard preload edges + 1 hard script edge, both mechanically FAIL |
| Move the 3 standards skills alongside their checker agents (`skill-checker`, `agent-checker`, `wording-checker`, `chore-lead`) | Those checkers audit the *whole* harness estate, not just the authoring family; relocating harness's own self-hosting gate into a plugin disabled in this very workspace is worse than the problem it solves |
| Duplicate `skill_lint.py` into authorkit for the 3 forges | "Sources of record flow outward... never the reverse" (this repo's own CLAUDE.md invariant) — a duplicate validator is a drift pair from day one |
| Treat `naming-rules`' content as movable to authorkit's `naming-conventions` | ADR-0011 D9 already rules a different destination (in-place supersession note + a plain doc, not a skill move); overriding a ratified Decision text is not this design phase's call |
| One-plugin (no authorkit at all, fold everything back into harness) | Not evaluated in depth — out of scope for a boundary-refinement charter; authorkit already shipped independently via #196 with its own audience (external adia estates) that predates and doesn't depend on this refactor |

## Interfaces

### Seam list (surviving cross-plugin edges under the one-member move)

`surface_map.py check` on the `fix-old-names`-only partition: **PASS, 0 fail, 1 seam** —
`authorkit -> harness (mention x6)`: `fix-old-names` mentions `big-change-git-rules`,
`clean-repo`, `make-script`, `make-skill`, `naming-rules`, `sort-issues` — all soft (prose
handoffs), all degrade gracefully if authorkit isn't installed, none are preload/script edges.

### Structural mismatch worth naming (not a blocker, an open question for whoever executes)

The spec's grammar (§3) models **two separate artifact kinds** — object-first commands
(VerbLex-terminal) and nominal skills ({object}-{process}, ProcessLex-terminal) — but
`make-skill`, `make-agent`, `make-hook`, and `fix-old-names` are each **one file playing both
roles** (`disable-model-invocation: false` *and* `user-invocable: true` on the same artifact).
Deriving a single spec-conforming name for each requires picking a lead role or accepting a
command/skill split that doesn't exist today. Not resolved here — flagged for whoever eventually
retires these exemptions (see Data, below).

### Blast-radius surface touched if any of the 8 named candidates ever move or rename

- **Eval suites:** 19 `evals/evals.json` files **within harness** reference one of the 8 names —
  6 are the candidates' own suites; 13 are **reciprocal fences** in sibling harness suites
  (`script-writing-rules`, `make-script`, `save-lessons`, `thinking-depth-rules`, `find-intent`,
  `big-change-git-rules`, `plan-skill-merge`, `hook-writing-rules`, `plugin-install-facts`,
  `plan-plugin-split`, `pack-writing-rules`, `check-routing`, `ops-write-sandbox-rules`). **Estate-wide, the count is 28 files** — 9 more outside harness would break as reciprocal fences on a
  cross-plugin move: `docs/skills/research-methods`, `docs/skills/markdown-to-markup`,
  `docs/skills/html-to-markdown`, `docs/skills/make-reference`, `docs/skills/make-rubric`,
  `llm/skills/chat-harness-routing-facts`, `llm/skills/agent-residency-facts`,
  `teamwork/skills/parallel-work-rules`, and `authorkit/skills/naming-conventions` itself. Any
  move needs all 28 reciprocal-fence-checked, not just the 19 harness carries.
- **README rows:** harness's own `README.md` carries 28 matching *lines* (37 total occurrences,
  since one line can reuse a name) across the 8 names — member table rows, invocation notes.
- **This repo's own entry file:** root `CLAUDE.md` names four of the eight candidates directly —
  `naming-rules` (Invariants: "the canon is harness's `naming-rules` (ADR-0006, 2026-07-21)"),
  and `make-skill`/`make-agent`/`make-hook` (the routing table's "New skill / agent / hook /
  entry-file work" row, plus a `decision-watcher` cross-reference and the semantic-edit
  invariant's own `make-skill`'s P5 citation) — concrete, first-party dependencies on names
  ADR-0011 supersedes or this analysis rejects moving.
- **Memories:** none of MEMORY.md's current entries cite these 8 names directly — zero blast
  radius there today.
- **Cross-plugin mentions inside harness:** 35 mention edges point *into* the 8 candidates from
  other harness members (measured on the reduced partition's seam count); ~20 point *out* from
  the candidates to the rest of harness. All soft, all survive a move without hook enforcement,
  but every one is a line a human reading either skill would expect to still resolve.
- **The adia estates (ADR-0011's own context, not independently re-verified here — external to
  this repo):** adia-ui-kit-forge (9 skills) + adia-ui-kit-factory (16 skills, 6→7 agents) per
  ADR-0011's own census, plus adia-eng/agentic-tools (the spec's home turf, ~30% self-conformant).
  ADR-0011 D8's bootstrap wave already scopes a rename campaign to exactly these — never to
  nonoun-plugins.

## Data

### The rename map — informational only, per ADR-0011 D8's own ruled migration posture

**ADR-0011 D8 (already ruled, verbatim): "grandfather + ratchet, no campaign."** Every existing
nonoun-plugins name — all ~155 members, including all 8 candidates named in #197 — enters
`naming.manifest.json`'s `exemptions` array **verbatim** on ratification. The array may shrink,
never grow; new mints conform from day one; **existing names rename only opportunistically, when
an artifact is otherwise touched.** The "estate-wide rename campaign executed" language in #197's
own Acceptance item 3 is not what D8 authorizes for this estate — D8's one-time bootstrap-wave
exception is scoped explicitly to the adia-ui-kit forge + factory estates, not nonoun-plugins.
**This is a real conflict between the ticket's captured acceptance criteria and the ADR it
depends on, reported here rather than silently split the difference on.**

Given that, the table below is exemption-list annotation for opportunistic future renames, never
an execution plan:

| Current name | Informational spec-conforming target | Basis | Status |
|---|---|---|---|
| `make-skill` | skill role: `skill-authoring`; command role: `skill-create` | §3.2 nominal `{object}-{process}`, ProcessLex `authoring`; §3.1 VerbLex `create` | Grandfathered — one-artifact-two-roles mismatch unresolved (see Interfaces) |
| `make-agent` | skill role: `agent-authoring`; command role: `agent-create` | same | Grandfathered, same mismatch |
| `make-hook` | skill role: `hook-authoring`; command role: `hook-create` | same | Grandfathered, same mismatch |
| `fix-old-names` | skill role: `reference-migration` or `name-migration` (needs an ObjectVocab call this doc doesn't make unilaterally) | §3.2, ProcessLex `migration` (per ADR-0011 D10's `adia-migrate` → `app-migration` precedent) | Grandfathered; ObjectVocab choice open |
| `skill-writing-rules`, `agent-writing-rules`, `prompt-wording-rules` | reference-shaped nominal-phrase, largely as-is (`skill-writing-rules` already reads as a nominal phrase under §3.2's looser production) | §3.2 reference-shaped exception | Grandfathered, low rename pressure either way |
| `naming-rules` | superseded in place, not renamed — see D9 | ADR-0011 D9 | Not a rename candidate at all; a supersession note |

### Ratification package — exactly what accepting ADR-0011 changes

1. **Frontmatter edits to `.claude/docs/adr/0011-adopt-naming-convention-spec.md`:**
   `status: proposed` → `accepted`; add `ratified: <the acceptance date>` (currently `null`);
   **`supersedes:` currently `null` and must be wired explicitly** — the estate's own sweep
   finding is that `supersedes: null` never fires any mechanical linkage — set it to the grammar
   halves of `adr-0001` and `adr-0006` (D7/Consequences: "the nonoun grammar... is superseded as
   canon"). This is a same-file frontmatter edit at ratification time, not a new document.
2. **What survives from ADR-0006:** its enforcement discipline — the symmetry hardline
   (frontmatter `name:` = directory/file stem), `skill_lint` F9/A6 lint gates — carries forward
   per ADR-0011's own header ("their enforcement discipline... carries forward") until the
   greenfield validator (step 3 below) actually replaces the naming-specific checks. Nothing
   about symmetry enforcement changes at ratification; only the *grammar* being enforced does.
3. **Execution order after ratification:** the six-step sequence is ADR-0011's own §"Execution
   order" — cite it there rather than restate it here; none of it runs in this design phase, all
   of it waits on Kim's ratify word. The deltas this design pass adds on top of that section
   (verified against the live tree, not in the ADR's own text):
   - Step 2 ("land the spec + seed the manifest") is **half-done**: the spec doc is committed at
     `.claude/docs/spec/spec-naming-convention.md`, stale path already fixed (6bcbfbe). The
     **repo-root `naming.manifest.json` is verified absent** — only `authorkit/naming.manifest.json`
     exists, and it dogfoods authorkit itself with an *empty* exemptions array; it is not the
     repo-root manifest D9/step-2 calls for. Do not read authorkit's own manifest as satisfying
     this step.
   - The `supersedes: null` wiring (frontmatter, above) is this design pass's own addition to
     step 1 — the ADR's own text names the supersession in prose (D7/Consequences) but never
     states the frontmatter field must be set at the same time; the estate's sweep finding is
     that an unset `supersedes:` fires nothing mechanically, so the ratify-time PR must carry
     both the status flip and the field.

## Risks

1. **Ratifying ADR-0011 without also landing the repo-root manifest (step 2 above) ships a
   status flip with no enforcement behind it** — the `supersedes: null` sweep finding exists
   precisely because a frontmatter edit alone fires nothing mechanically. Detection: `git ls-files
   naming.manifest.json` at repo root stays empty after ratification. Fallback: block the status
   flip in the same PR that lands the manifest, never split across two changes.
2. **Enabling authorkit here before `naming-rules` is superseded recreates the exact collision
   authorkit's README says it exists to avoid.** Detection: `/naming-rules` and
   `authorkit:naming-conventions` both routable in one `/plugin` menu. Fallback: keep authorkit
   disabled in this workspace until the supersession note (D9) lands, re-run `/check-routing`
   before flipping `enabledPlugins`.
3. **The one-artifact-two-roles mismatch (Interfaces) has no ruled resolution** — whoever executes
   an opportunistic rename on `make-skill`/`make-agent`/`make-hook`/`fix-old-names` will hit an
   undecided command-vs-skill split. Detection: a rename PR proposes a name for "the skill" that
   silently drops the command surface's own naming question. Fallback: route that one call to
   `naming-rules`/`authorkit:rename-planning` at the time, not decided speculatively here.
4. **`surface_map.py`'s dangling-reference sweep over-fires on prose-shaped kebab tokens** (e.g.
   `world-state`, `per-plugin`) that aren't real artifact references. Detection: a `gaps` finding
   whose `name` matches no node in *any* installed plugin's own map (not just harness's) is
   almost certainly a false positive, not a real gap. Fallback: cross-check against the full
   estate's node inventory before treating a `gaps` hit as actionable.

## Findings write-back

See issue #197's dated Findings comment (this design phase's summary + this doc's path),
posted alongside this doc's PR.
