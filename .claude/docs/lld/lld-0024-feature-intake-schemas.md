---
doc-type: lld
id: lld-0024-feature-intake-schemas
status: draft
version: 0.1.0
date: 2026-08-19
owner: kim.granlund
ticket: nonoun-plugins#711
spec: none — #711's own body IS the ratified design (Kim, 2026-08-19 in-session; the pre-fork
  grill was already paid, zero owed questions) and already carries the checkable Acceptance
  criteria; a standalone SPEC would restate what the ticket already states (the same routing
  test lld-0017/lld-0021/lld-0022/lld-0023 each already applied).
scope: feature
audience: builder, reviewer
---
# LLD — UI-feature intake enrichment: two-plane intake schemas (gh#711)

**Verdict, head-first.** Two new knowledge skills ship the ticket's design almost verbatim: a
screens-plugin pack (four per-shape intake schemas — component/module, layout/shell, UX flow,
cross-cutting UX — each schema field lifted from its owning skill's own two-plane axes) and a
design-plugin pack (one schema for token/palette/typography seeds, same two-plane shape). Both
state the both-planes capture-completeness rule and the scope/build-owner/DoD-checker invariant
verbatim. `docs:file-feature`'s classify step gains one UI-shape detection paragraph naming both
packs by soft mention. One resolved deviation from the ticket's own suggested names (Resolution
1): `ui-` and `visual-` are not registered tokens under ADR-0011's naming grammar, so the two
skills ship as `screens:feature-intake-rules` and `design:token-feature-intake-rules` instead of
the ticket's `ui-feature-intake-rules`/`visual-feature-intake-rules` — grammar-conforming names
built from already-registered `ObjectVocab` tokens, never a manifest edit. Ships as three small
PRs (the ticket's own ratified shape), screens and design independent and first, docs (the
file-feature wiring) last since it cites both by name.

## Non-goals

- **Not registering `ui`/`visual` in `naming.manifest.json`.** The dispatch contract is explicit
  ("record any deviation, never edit the manifest unattended") — Resolution 1 below is the
  recorded deviation, not a manifest PR this ticket doesn't own.
- **Not editing `make-component`, `break-down-layout`, `break-down-flow`, `make-palette`, or
  `pick-fonts`'s own procedures.** Only their `description`/NOT-for line gains one reciprocal
  fence clause each (Resolution 4) — no procedure duplication, per the ticket's own invariant (d).
- **Not minting any new agent.** IDR-0007's bar: the DoD checkers this ticket cites
  (`component-checker`, `layout-checker`, `flow-checker`, `check-focus`/`check-safety`/
  `check-translations`, `check-colors`, `design-system-checker`) already exist; nothing here
  earns a new seat.
- **Not adding a hook.** #466's remove-all-hooks directive stands; detection is a routing-table
  paragraph in `file-feature`, not an enforced gate.
- **Not building a `token-builder` skill.** `token-builder` is an existing AGENT (design
  plugin); the ticket cites it as a build owner by name (soft mention in prose), the same way it
  cites `make-palette`/`pick-fonts` — no reciprocal skill-routing fence is owed to an agent
  (fences guard model-routing between SKILLS competing for the same trigger; an agent is reached
  by dispatch, not description-match, so there is no routing collision to fence against).

## Resolution 1 — Naming: `ui-`/`visual-` are unregistered; grammar-conforming names chosen instead

**Fork:** ship the ticket's own suggested names (`ui-feature-intake-rules`,
`visual-feature-intake-rules`) as exemptions, register `ui`/`visual` in `ObjectVocab`, or rename
to already-conforming tokens?

**Decision: rename.** Direct inspection of `naming.manifest.json` (this clone, off `origin/main`)
confirms: `ui` resolves in no lexicon (`ObjectVocab`, `ProcessLex`, or `TopicLex`) — the two
existing `ui-*` names in the estate, `screens:ui-genre-facts` and `screens:ui-pattern-facts`, are
both listed in `exemptions` (pre-2026-08-13 grandfather, ADR-0006), not conforming names; `visual`
resolves nowhere either. `feature`, `intake`, `screen`, and `token` ARE registered `ObjectVocab`
entries, and `rules` is the `-rules` reserved tail (§14.2 D1, ADR-0014) whose `topic-phrase`
resolves against the `ObjectVocab ∪ ProcessLex ∪ TopicLex` union pool. Two options both close
without any manifest edit:

- **Adding an exemption** is illegal on its face — §10's own rule: "enforce for new names;
  grandfather existing ones... the array may shrink and may never grow." These are new mints.
- **Registering `ui`/`visual` in `ObjectVocab`** is a real manifest PR with its own anti-ambiguity
  gate (§4, AC-008) — legitimate in general, but the dispatch contract this build runs under is
  explicit that this ticket never edits the manifest unattended. Deferred to a human/manifest-
  authoring pass if a future second consumer wants the bare `ui`/`visual` token; not blocking this
  ticket.

**Chosen names — probed, not just asserted.** `authorkit:naming-audit`'s `validate.py --scope
grammar` run against probe directories confirms the split precisely: `feature-intake-rules` and
`token-feature-intake-rules` both parse clean; `ui-feature-intake-rules` fails with `[ERROR] token
'ui' resolves in no lexicon or vocab` — the exact mechanism Resolution 1 predicts, not a guess.
Re-run against the real, shipped directories at Build sequence step 4 for the final proof (same
command, real paths, same expected clean result):

| Ticket's suggested name | Shipped name | Why it parses |
|---|---|---|
| `screens:ui-feature-intake-rules` | `screens:feature-intake-rules` | `feature` ✓ ObjectVocab, `intake` ✓ ObjectVocab, `rules` reserved tail — `ui` dropped (the `screens` plugin is already the UI-domain namespace; re-encoding "ui" inside the local name is exactly the double-prefix §4 already discourages for brand tokens, applied here to a domain word) |
| `design:visual-feature-intake-rules` | `design:token-feature-intake-rules` | `token` ✓ ObjectVocab (design's own token/palette/typography domain), `feature` ✓, `intake` ✓, `rules` tail |

Neither collides with an existing skill name in either plugin (verified: `ls screens/skills`,
`ls design/skills`, this clone).

## Resolution 2 — Shape: flat, no `INDEX.md`, per pack-writing-rules' threshold

Same test `lld-0020`/`lld-0023` already applied (`harness:pack-writing-rules`: 3–7 axes, flat
consult table when the corpus is ≤~7 files):

- **`screens:feature-intake-rules`** — 5 files: `component-module.md`, `layout-shell.md`,
  `ux-flow.md`, `cross-cutting-ux.md`, `fixtures.md`. 5 clears the threshold cleanly; flat table,
  no INDEX.
- **`design:token-feature-intake-rules`** — 2 files: `token-visual-schema.md`, `fixtures.md`.
  Below the threshold where an INDEX would ever earn its keep; flat table, same shape for
  consistency with its sibling pack.

## Resolution 3 — Every schema field is LIFTED, never restated, from its owning skill's own axes

The ticket's own invariant (d), made mechanical: each schema file's OUTSIDE-IN/INSIDE-OUT (or
task/journey, or Compose/Realize) column headers and field list are read directly off the owning
skill's own SKILL.md/rubric — never re-derived or paraphrased. Concretely, per file:

| File | Owning skill/axes read | Owner cited | DoD checker cited |
|---|---|---|---|
| `component-module.md` | `screens:make-component` — Compose (whole→part) × Realize (part→whole) | `make-component` | `component-checker` |
| `layout-shell.md` | `screens:break-down-layout` — OUTSIDE-IN (frame→regions→groups→atoms) × INSIDE-OUT (verbs→bindings→feedback→coherence) | `break-down-layout` (DESIGN mode) | `layout-checker` |
| `ux-flow.md` | `screens:break-down-flow` — task→journey axis, transitions→whole | `break-down-flow` | `flow-checker` |
| `cross-cutting-ux.md` | `screens:check-focus`/`check-safety`/`check-translations`/`motion-rules` budget vocabulary | the named `check-*` skill per concern | same `check-*` skill (self-checking) |
| `token-visual-schema.md` | design's own token/contrast/interaction-state doctrine (`check-colors`'s rubric, `design-system-checker`'s export contract) | `make-palette` / `pick-fonts` / `token-builder` | `check-colors` / `design-system-checker` |

Each reference file cites its owning skill's file path for the axis definition itself (a soft
in-plugin cite, same skill, no cross-plugin boundary issue) rather than re-explaining the axis —
the schema is the INTAKE FIELD LIST derived from that axis, not a second copy of the axis
doctrine.

## Resolution 4 — Reciprocal fences: 6 sibling skills, not the DoD-checker set

**Fork:** fence every named owner AND every named checker, or only the skills whose ROUTING could
actually collide?

**Decision: fence only the routing-collision set.** A reciprocal fence exists to stop a
model-invocable skill's description from stealing or leaking a trigger it shouldn't own
(`.claude/rules/plugin-authoring.md`'s "Descriptions are the routing surface" bullet). The real
collision surface is: an ask
shaped like "what fields does a UI ticket for a button need" must never route to `make-component`
(a BUILD skill), and "build me a button" must never route to the new intake-rules pack (a
CAPTURE skill) — same pair for `break-down-layout`/`break-down-flow` and, cross-plugin, for
`file-feature` itself (the ticket's own explicit "must not steal file-feature's... routing"
line). A DoD *checker* (`component-checker`, `layout-checker`, `flow-checker`, `check-focus`, …)
is reached by a GRADE-shaped ask ("review this component") — a structurally different trigger
class already fenced against `make-component` et al. by their own existing NOT-for lines; the new
intake pack adds no new collision risk there, so no edit is owed to any checker's description.

**Fenced set (6 skills total: 5 build-owner siblings + `file-feature` itself, all reciprocal
fences; the file-feature classify-step PARAGRAPH is separate — Component 3, Resolution 5, not a
fence):**

| Skill | New NOT-for clause (paraphrase) | New no-trigger eval case |
|---|---|---|
| `screens:make-component` | "NOT for what fields a UI-feature TICKET should capture before build (`feature-intake-rules`)" | "what fields does a button component ticket need" → `feature-intake-rules` |
| `screens:break-down-layout` | same pattern, DESIGN-mode-adjacent | "what should a dashboard-shell ticket capture" → `feature-intake-rules` |
| `screens:break-down-flow` | same pattern | "what does an onboarding-flow ticket need to state" → `feature-intake-rules` |
| `design:make-palette` | "NOT for what fields a token/palette-seed TICKET should capture (`token-feature-intake-rules`)" | "what should a new-accent-color ticket capture" → `token-feature-intake-rules` |
| `design:pick-fonts` | same pattern | "what fields does a typography-seed ticket need" → `token-feature-intake-rules` |
| `docs:file-feature` | "NOT the UI-shaped intake SCHEMAS themselves (`screens:feature-intake-rules`, `design:token-feature-intake-rules`) — this skill only routes to them" | "what fields does a UI ticket for a button need" → `feature-intake-rules` (not absorbed into plain `file-feature` capture) |

Each of these 6 skills' own `evals/evals.json` gains one reciprocal no-trigger case in the same
PR as the new pack (the `.claude/rules/plugin-authoring.md` reciprocal-fence rule, same shape
`lld-0020`'s Resolution 8 already used) — `file-feature`'s own no-trigger case rides in the SAME
edit as Resolution 5's classify-step paragraph (Components step 13), not a separate touch.

## Resolution 5 — `file-feature`'s UI-shape detection: soft mention, degrade-gracefully named

Per the ticket's Component 3: the classify step gains one paragraph — a component/layout/flow/
visual-shaped seed consults the matching pack (`screens:feature-intake-rules` for the first
three shapes, `design:token-feature-intake-rules` for the fourth) by soft named mention only
(`.claude/rules/plugin-authoring.md`'s hard boundary: a preload or `${CLAUDE_PLUGIN_ROOT}` path
crossing plugins is a defect; a named-mention citation is not). The degrade branch is named
explicitly in the paragraph itself: `screens`/`design` not installed → classify proceeds on the
ticket's own stated fields alone, gap named in the record rather than silently skipped. This is
Component 3's own content, not a reciprocal fence — `file-feature`'s own evals gain the
reciprocal no-trigger case as part of Resolution 4's table above, but the classify-step paragraph
itself is new capability, not a fence.

## Components

Build sequence, executed top to bottom, screens and design independent/parallel, docs last:

1. **`screens/skills/feature-intake-rules/SKILL.md`** — knowledge species,
   `disable-model-invocation: false`, `user-invocable: false`. Flat 5-row consult table
   (Resolution 2). Both-planes capture-completeness rule + invariants (b)/(c)/(d) stated verbatim
   (Data, below — the exact text both packs ship). Fences per Resolution 4's own reciprocal
   language (the pack's own NOT-for lines pointing back at `make-component`/`break-down-layout`/
   `break-down-flow`/`file-feature`).
2. **`screens/skills/feature-intake-rules/references/component-module.md`** — Compose×Realize
   intake fields (Resolution 3 row 1): OUTSIDE-IN placement/parents-children/composition-nesting/
   consuming-surfaces; INSIDE-OUT states/API-surface/geometry(incl. nested-radius-class)/
   token-bindings/feedback. Owner `make-component`, checker `component-checker`.
3. **`screens/skills/feature-intake-rules/references/layout-shell.md`** — OUTSIDE-IN×INSIDE-OUT
   pairs (Resolution 3 row 2): frame→regions→groups/archetype/region-ownership;
   verbs/bindings/focus-order. Owner `break-down-layout` DESIGN mode, checker `layout-checker`.
4. **`screens/skills/feature-intake-rules/references/ux-flow.md`** — task→journey axis
   (Resolution 3 row 3): journey-placement/entries/sequencing; per-transition
   mechanics/exit-asserts/failure-interrupt-states. Owner `break-down-flow`, checker
   `flow-checker`.
5. **`screens/skills/feature-intake-rules/references/cross-cutting-ux.md`** — motion/focus/i18n
   budget vocabulary (Resolution 3 row 4), one sub-section per named `check-*` skill, each citing
   that skill's own budget fields as the intake questions.
6. **`screens/skills/feature-intake-rules/references/fixtures.md`** — 4 worked fixture tickets
   (one per shape class), each demonstrating a capture-complete grid (both plane columns answered
   or a named open fork) per invariant (a).
7. **`screens/skills/feature-intake-rules/evals/evals.json`** — trigger cases per shape + the 4
   reciprocal no-trigger cases (Resolution 4, screens half) + one `file-feature` no-trigger case.
8. **`design/skills/token-feature-intake-rules/SKILL.md`** — same species/flags, 2-row flat
   table. Identical verbatim both-planes rule + invariants (Data).
9. **`design/skills/token-feature-intake-rules/references/token-visual-schema.md`** — OUTSIDE-IN:
   roles/ramps touched, both-theme reach, consumers; INSIDE-OUT: specific token values, contrast
   gates, interaction-state ladder (Resolution 3 row 5). Owners `make-palette`/`pick-fonts`/
   `token-builder`, checkers `check-colors`/`design-system-checker`.
10. **`design/skills/token-feature-intake-rules/references/fixtures.md`** — 1 worked fixture
    ticket (the visual/token shape).
11. **`design/skills/token-feature-intake-rules/evals/evals.json`** — trigger cases + the 2
    reciprocal no-trigger cases (Resolution 4, design half) + one `file-feature` no-trigger case.
12. **Reciprocal fence edits, same PR as each pack** (Resolution 4): `screens:make-component`,
    `screens:break-down-layout`, `screens:break-down-flow` SKILL.md + evals.json (screens PR);
    `design:make-palette`, `design:pick-fonts` SKILL.md + evals.json (design PR).
13. **`docs/skills/file-feature/SKILL.md`** — classify step gains the UI-shape detection
    paragraph (Resolution 5); `docs/skills/file-feature/evals/evals.json` gains the reciprocal
    no-trigger case owed back from Resolution 4's table (a UI-ticket-fields ask must stay routed
    to the two new packs, never absorbed by `file-feature` itself).
14. **Plugin close-out, three plugins**, versions re-verified off `origin/main` immediately before
    each PR's own PR-open (Phase 5's VALUE-race check, re-run per plugin at that time — the
    numbers below are this LLD's own claim-time read, 2026-08-19):
    - `screens/.claude-plugin/plugin.json`: 1.0.16 → **1.1.0** (new skill/pack — MINOR, per the
      `lld-0020` precedent's own rule: "a new skill/pack is a MINOR bump, not a patch").
    - `design/.claude-plugin/plugin.json`: 1.1.5 → **1.2.0** (new skill/pack — MINOR, same rule).
    - `docs/.claude-plugin/plugin.json`: 1.20.0 → **1.20.1** (one classify-step paragraph + one
      reciprocal fence — PATCH-shaped, no new skill minted in this plugin).
15. **Gates before each PR-open**: `skill_lint.py` on every touched/new SKILL.md + evals.json in
    that plugin; `authorkit:naming-audit`'s `validate.py --target <new-skill-dir> --scope grammar`
    on both new skill directories (Resolution 1's own proof); `/check-routing screens`,
    `/check-routing design`, `/check-routing docs` (all three touched, since fences ride in every
    plugin); `release_gate.py <plugin> --package` per touched plugin; fresh-context
    `harness:skill-checker` on both new SKILL.md files (UNNAMED synchronous); fresh-context
    `docs:doc-checker` on this LLD before its own PR context closes (UNNAMED synchronous,
    already run per Build sequence step 1 below).

## Interfaces

- **`screens:feature-intake-rules` → `make-component`/`break-down-layout`/`break-down-flow`**:
  soft in-plugin citation only — each reference file names the owning skill's file path for the
  axis definition, never preloads it, never restates the axis doctrine (Resolution 3).
- **`design:token-feature-intake-rules` → `make-palette`/`pick-fonts`/`token-builder`**: same
  soft-citation shape, cross-artifact (two skills, one agent) — the agent citation is prose-only,
  no relation field, since `token-builder` is dispatched, not routed-to (Non-goals).
- **`docs:file-feature` → `screens:feature-intake-rules` / `design:token-feature-intake-rules`**:
  soft CROSS-PLUGIN mention, degrades gracefully where either plugin isn't installed
  (`.claude/rules/plugin-authoring.md`'s hard boundary — no preload, no
  `${CLAUDE_PLUGIN_ROOT}` path). This is the one interface this LLD adds that didn't exist before.
- **Both packs → their own DoD checkers** (`component-checker`/`layout-checker`/`flow-checker`/
  `check-*`/`check-colors`/`design-system-checker`): named in the schema's own owner/checker
  columns (invariant (c)), read by a builder or `dispatch-ticket`'s own Phase 4 sizing, never
  invoked by the pack itself — the pack is intake-time knowledge, not a dispatcher.

## Data

**The both-planes capture-completeness rule (invariant (a)) — shipped VERBATIM in both SKILL.md
files, the ticket's own wording, unedited:**

> A UI feature ticket is capture-complete only when both plane columns carry an answer or a named
> open fork. Single-plane capture ships the known failure quadrants: outside-in-only ("looks
> clean but nothing does anything"), inside-out-only (orphan components).

**Invariant (b) — schema fields double as the pre-fork grill's fork menu, shipped verbatim:**

> These schema fields double as the pre-fork grill's fork menu for big seeds (gh#654) — the
> grill's own step picks the highest-leverage unanswered cells (2 structural + 2 mechanism) from
> this same grid; one artifact, never two drifting lists.

**Invariant (c) — scope/owner/checker geometry, shipped verbatim:**

> The ticket records scope: frontmatter, the named build owner, and the pre-named DoD checker so
> capture → build → verify speak one geometry — `dispatch-ticket` routes the build against the
> same owner this schema names, and the checker it dispatches at DoD is the same checker this
> schema names.

**Invariant (d) — no duplication, shipped verbatim:**

> No new agents (IDR-0007's bar — the checkers already exist), no procedure duplication (every
> schema field cites its owning skill's own axis, never restates it — doctrine-audit safe), no
> hooks (gh#466).

**Deliverable schema shape — one shared table shape across all 5 reference files (4 screens + 1
design), so a fixture ticket's own grid is grep-comparable across shapes:**

| Column | Plane | Required | Notes |
|---|---|---|---|
| `outside-in` (or `task→journey`/`Compose`) | structural | yes, or a named open fork | Placement, composition, sequencing — the "where does this sit" half. |
| `inside-out` (or `transitions→whole`/`Realize`) | mechanism | yes, or a named open fork | States, bindings, feedback, token values — the "how does this behave" half. |
| `scope:` | frontmatter | yes | component \| layout \| flow \| visual — names which schema file this ticket was captured against. |
| `build-owner` | frontmatter | yes | The exact skill name from Resolution 3's table. |
| `dod-checker` | frontmatter | yes | The exact checker name from Resolution 3's table. |

## Risks

- **R-1 (fence drift across 6 siblings + 3 plugins).** Same class `lld-0020`'s R-3 and
  `lld-0013`'s R-4 already named. Detection: reciprocal no-trigger cases in all 8 evals suites
  (2 new packs' own + 5 fenced siblings' + `file-feature`'s) plus `/check-routing` on all 3
  touched plugins in the same wave. Fallback: a routing-eval failure names the exact description
  line to sharpen.
- **R-2 (the `ui`/`visual` rename reads as a naming surprise against the ticket's own suggested
  names).** Mitigated by Resolution 1's table stating the mapping explicitly, cited in the PR
  body and the ticket's own dated Findings write-back — never a silent substitution.
- **R-3 (three independent PRs let the two knowledge packs' invariant text drift apart over
  time, since it's duplicated prose, not a shared citation).** Named, not solved: Data's verbatim
  block above is the SOURCE text both SKILL.md files copy at mint time; a future edit to one
  pack's invariant wording that isn't mirrored into the other is a doctrine-audit finding this LLD
  doesn't itself mechanize a check for (a legitimate follow-up, out of this ticket's own
  Acceptance).
- **R-4 (docs' PR lands before screens/design merge, leaving a soft mention pointing at
  not-yet-merged skills).** Not a defect: soft mentions degrade gracefully by design (Resolution
  5) — a reader hits a real, if not-yet-installed-from-this-branch, skill name once all three
  land; the dependency order (Components, "screens and design independent/parallel, docs last")
  is a merge-ORDER preference for review clarity, not a technical dependency the code enforces.

## Rejected alternatives

- **Registering `ui`/`visual` in `naming.manifest.json` to ship the ticket's own literal
  suggested names.** Rejected — Resolution 1; the dispatch contract this build runs under
  forbids an unattended manifest edit, and a grammar-conforming rename costs nothing the ticket's
  own Acceptance actually needs (the schemas' CONTENT is unchanged, only the two skill names).
- **Fencing every named DoD checker in addition to the 5 routing-collision siblings.** Rejected —
  Resolution 4; a checker is reached by a grade-shaped trigger already fenced against the
  matching builder skill, so fencing it again against the new intake pack adds cost with no real
  collision to close.
- **A single merged pack spanning screens + design (no split).** Rejected by the same hard
  plugin-boundary rule `lld-0020`'s own rejected-alternatives already cites — a preload or
  bundled-script path can never cross plugins; two packs with a soft citation seam (here: neither
  pack even cites the other, both only cite `file-feature`) is the only legal shape.
- **Shipping this as one combined PR instead of three.** Rejected — the ticket's own body already
  ratifies "ONE campaign, three small PRs, all under the write-gate" as the shipped design; this
  LLD's Components section states the dependency order that decision implies rather than
  re-opening the one-PR-vs-three question.
- **An `INDEX.md` for either new pack "for future growth."** Rejected — same reasoning
  `lld-0020`'s Resolution 2 already gave: both packs are inside the flat-table threshold; an
  INDEX now would be a second copy of the same short table with nothing to route yet.

## Agent verification

Per `docs:agent-harness-rules`, the assert layer is the cheapest one that catches this campaign's
own failure modes — pure text/structure and routing, no browser or live-human layer needed.
**Mechanical layer:** `skill_lint.py` on every new/edited SKILL.md + evals.json (3 plugins);
`doc_lint.py` on this LLD; `authorkit:naming-audit`'s `validate.py --scope grammar` on both new
skill directories (Resolution 1's own proof, mechanized rather than asserted from memory).
**Routing layer:** `/check-routing screens`, `/check-routing design`, `/check-routing docs` — the
routing-judge's blind matrix is the direct proof against R-1 (fence leaks/steals). **Fresh-context
checkers:** `docs:doc-checker` on this LLD (the semantic-edit-rides-a-critic invariant, applied to
a new mint); `harness:skill-checker` on both new SKILL.md files. **Enforcement:** `release_gate.py`
on all three touched plugins, `--package` on each. **Deferred, no instrument owed by this
ticket's own Acceptance:** a live human read of the two packs' prose for tone/voice — the same
class of exception every prior LLD in this spine already names for prose-only artifacts.

## Build sequence

| # | Step | Path | Done when |
|---|---|---|---|
| 1 | Draft this LLD, resolve the five forks | `.claude/docs/lld/lld-0024-feature-intake-schemas.md` | fresh-context `docs:doc-checker` pass recorded, findings fixed |
| 2 | Dated Findings write-back on gh#711, citing this LLD in `## Links` | gh#711 | comment posted, Links section updated |
| 3 | Build `screens:feature-intake-rules` + 3 reciprocal fences + evals | `screens/skills/feature-intake-rules/`, 3 sibling SKILL.md+evals | `skill_lint.py`/`/check-routing screens` green, `harness:skill-checker` pass |
| 4 | Build `design:token-feature-intake-rules` + 2 reciprocal fences + evals | `design/skills/token-feature-intake-rules/`, 2 sibling SKILL.md+evals | `skill_lint.py`/`/check-routing design` green, `harness:skill-checker` pass |
| 5 | Wire `docs:file-feature`'s classify-step paragraph + reciprocal evals | `docs/skills/file-feature/SKILL.md`, evals.json | `skill_lint.py`/`/check-routing docs` green |
| 6 | Version bump + README ledger, all three plugins, re-verified off `origin/main` at each PR's own PR-open | 3× `plugin.json` + `README.md` | `release_gate.py <plugin> --package` green per plugin |
| 7 | Push 3 branches, post the plan-approval write-gate hold comment on gh#711 naming each branch's HEAD SHA (ADR-0023 (c)) | gh#711 (3 comments or 1 consolidated) | branches pushed, hold comment(s) posted |

## Acceptance (checkable predicates)

1. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0024-feature-intake-schemas.md` → exit 0.
2. `python3 authorkit/skills/naming-audit/scripts/validate.py --target screens/skills/feature-intake-rules --scope grammar` and the same `--target design/skills/token-feature-intake-rules` → both exit 0/clean grammar.
3. `grep -rn "capture-complete only when both plane columns" screens/skills/feature-intake-rules/SKILL.md design/skills/token-feature-intake-rules/SKILL.md` → 2 matches (invariant (a) shipped verbatim in both).
4. `grep -c "build-owner\|dod-checker" screens/skills/feature-intake-rules/references/*.md` and the `design` equivalent → every shape file names both fields.
5. `python3 harness/scripts/skill_lint.py screens/skills/feature-intake-rules/SKILL.md` (and the `design` sibling, and every reciprocal-fenced sibling) → exit 0.
6. `/check-routing screens`, `/check-routing design`, `/check-routing docs` → no stolen/leaked/dead findings against the two new packs or their 6 fenced siblings.
7. gh#711's `## Links` section cites this LLD's path before any PR opens (the #649/#710 precedent, closing `dispatch-ticket`'s own Phase 3.6 citation requirement).
8. Fresh-context `docs:doc-checker` verdict on this LLD recorded in gh#711's dated Findings write-back, zero unresolved blocker/major findings.
