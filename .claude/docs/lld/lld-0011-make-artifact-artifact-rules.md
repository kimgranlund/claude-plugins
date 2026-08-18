---
doc-type: lld
id: lld-0011-make-artifact-artifact-rules
status: draft
version: 0.1.0
date: 2026-08-17
owner: kim.granlund
ticket: nonoun-plugins#619  # renumbered from lld-0619 to keep the sequential LLD spine (0001-0010); resolves ticket #619
spec: none — same routing as lld-0008/lld-0009: the ticket's own Acceptance section carries the
  checkable criteria and its Scope/Open section names the exact four design questions this LLD
  resolves (home plugin, shape split, assert layer, refresh mechanism), so a standalone SPEC would
  restate what the ticket already states (doc-writing-rules' own routing test). File number is
  ticket-keyed per the dispatch's named deliverable path.
---
# LLD — `make-artifact` + `artifact-rules`: an owner for Artifact and report-page authoring (#619)

**Verdict, head-first:** two new skills in the **docs** plugin, mirroring the plugin's own
`make-doc` / `doc-writing-rules` precedent pairing — `make-artifact` (procedural,
`user-invocable: true`) consumes a design system (DESIGN.md + tokens.json) plus report/handbook
content into a polished Artifact page, and `artifact-rules` (knowledge, `user-invocable: false`)
carries the standards it invokes: the token-consumption contract, the house shell doctrine, the
mermaid house style, and the refresh procedure — all four currently living only in session memory,
which is exactly the stale-context defect class the operating contract ranks with bugs. The
token→CSS mapping is mechanized as a bundled script (`css_build.py`, selftest-proven, payload-layer
asserts); shell rendering stays a stated human/browser-layer exception. One new `object_vocab`
entry (`artifact`) is minted, confirm-gated per `authorkit:manifest-authoring`. The four Scope/Open
questions are ratified below, each with its evidence.

## Resolution 1 — Home plugin: `docs` (anti-matrix verdict, job evidence named)

**Resolved: `docs`.** Per harness `plan-plugin-split`'s anti-matrix guard, an absence is a gap only
with job evidence — and the job evidence here is a dangling capability, not template symmetry:

- **The job exists and has no owner.** The Estate Handbook took six hand-rolled Python rebuilds
  (2026-08-18 finding, cited in #619's Summary) because nothing in the estate owns "design system +
  content → rendered Artifact page." That is repeated, evidenced work with no routing-table row.
- **`docs` already claims the surrounding territory.** Its own manifest description
  (`docs/.claude-plugin/plugin.json`, verified on `origin/main`) claims "Functional-document
  authoring… markdown↔markup conversion… knowledge/reference authoring," and it ships
  `markdown-to-markup` (markdown source → safe rendered DOM), `tidy-docs`, `make-reference`,
  `make-vision-memo`. Artifact/report-page authoring is a natural extension of doc rendering —
  the same plugin that renders markdown into DOM is the plugin that renders a report into a page.
- **`design` scopes itself OUT of this job.** `design/skills/make-design-system/SKILL.md`
  (verified in this clone) states its consumer model explicitly — "a design-system file for LLMs
  is a consumption artifact: its consumer is a generative design agent" — and scopes itself to
  AUTHORING and grading the design-system SOURCE across platforms (Claude Design / Stitch / Figma
  Make). Its routing table has no slot for "consume an already-authored DESIGN.md into a running
  artifact page." Consumption of the token source is a different job from authoring it; #619's own
  Links section already records "Token source of record: design plugin (this feature CONSUMES it)."

`make-artifact` is therefore a first-class *consumer* of `design`'s output, living in `docs`, with
a soft cross-plugin fence both ways (Resolution 6).

## Resolution 2 — Shape: procedural + knowledge pair, references/ split at 4 axes

**Resolved:** two skills, mirroring the exact precedent pairing already shipped in this plugin —
`make-doc` (procedural, `user-invocable: true`, thin phased command, `argument-hint`) invoking
`doc-writing-rules` (knowledge, `user-invocable: false`):

- **`docs/skills/make-artifact/`** — procedural. `user-invocable: true`,
  `argument-hint: "[design-system path] [content source]"`. Thin body: route → consume tokens
  (run the script) → choose shell → assemble → verify → stamp provenance. Invokes `artifact-rules`
  the way `make-doc` invokes `doc-writing-rules` ("the standards below are its, not mine").
- **`docs/skills/artifact-rules/`** — knowledge. `user-invocable: false`,
  `disable-model-invocation: false` (consultable when an artifact question arrives without the
  build ask).

**References split, not inline:** per `harness/skills/pack-writing-rules/SKILL.md` (read in this
clone), a corpus holds 3–7 declared axes and "two genuinely different question types never share a
file." Counting the actual axes here gives **4 distinct question types**: (1) design-system
consumption — how tokens become CSS; (2) shell doctrine — which page shell this content class
gets; (3) mermaid house style — how diagrams survive this pipeline; (4) refresh procedure — when
and how a shipped artifact is rebuilt. Four axes clears the ≥3 threshold, so `artifact-rules` gets
a `references/` corpus of 4 files with a flat 1:1 consult table in its SKILL.md body and **no
INDEX.md** — pack-writing-rules' enumerability rule (≤~7 files: "the table IS the retrieval map
and a separate INDEX would be a second copy that drifts"), the same worked precedent
`docs/skills/agent-harness-rules/SKILL.md` follows.

**Rejected here:** a `/make-pack` research-wave corpus — this is earned house practice (taste
rulings + the 2026-08-18 incident learnings), not an external knowledge domain needing gathered
sources; a wave would manufacture research where distillation of known rulings is the whole job.

## Resolution 3 — Assert layer: payload-layer on generated CSS + script selftest; rendering is a stated human exception

**Resolved,** per `docs/skills/agent-harness-rules/references/assert-layer-choice.md`'s choice
test ("the CHEAPEST layer at which this criterion's failure would actually show up"):

- **Payload layer (layer 1)** owns the token-consumption criteria. Given a DESIGN.md/tokens.json
  fixture, the emitted CSS either contains the right light/dark custom-property pairs, the right
  font stack WITH system fallback, and the right radius/spacing values — or it doesn't. Fully
  deterministic, no rendering, no browser. These asserts live in `css_build.py selftest` (fixtures
  for BOTH color representations, negative + reverse controls per
  `harness/skills/script-writing-rules/SKILL.md`'s selftest contract) and are exactly #619's
  Acceptance criterion 2 ("Given the Adia DESIGN.md + tokens.json, the capability emits artifact
  CSS with light/dark custom-property pairs, type roles, and radius/spacing scales.").
- **Mechanical layer**: `skill_lint.py` on both SKILL.mds + both evals suites; `eval_check.py`;
  `release_gate.py docs` (G4 runs the selftest).
- **Human/browser layer — the stated exception, not a silent gap** (assert-layer-choice's own
  failure catalog: "Human-review sprawl… the exception line forces the claim to be written down"):
  whether the tabbed handbook shell actually looks right and whether a rendered mermaid SVG
  actually re-themes visually are render-shaped criteria; they stay human review, named in both
  skills' Done blocks and in `## Agent verification` below. No browser-layer harness is built
  (rejected below).

## Resolution 4 — Refresh mechanism: a named procedure in the skill, never a hook

**Resolved:** `artifact-rules/references/refresh-procedure.md` names the discipline:

1. Every emitted artifact page carries a **provenance footer**: source DESIGN.md path,
   tokens.json `$generator` line, content source, build date, and the `css_build.py` invocation
   used — so any reader can tell what the page was built FROM and re-run the build.
2. **Refresh trigger:** re-run `/make-artifact` against the current DESIGN.md/tokens.json and
   current content at each release boundary of the source design system, or whenever the source
   doc or the content changes — the same doctrine this workspace's CLAUDE.md already applies to
   corpus snapshots ("stale context is a defect, equal in severity to a bug"; "sources of record
   flow outward… snapshots refresh FROM them at release boundaries").
3. **Explicitly NOT a hook.** Hooks are fully retired in this workspace (remove-all-hooks
   directive, #466, 2026-08-17); the refresh is a named procedure a human or dispatched session
   runs, and the provenance footer is what makes staleness *detectable* without automation.

This resolves #619 Scope/Open item (d): the Estate Handbook's own refresh = re-run
`/make-artifact` with its provenance footer's inputs.

## Resolution 5 — Naming: mint `artifact` into `object_vocab`, confirm-gated

**Verified in this clone's `naming.manifest.json`:** `artifact` is absent from `object_vocab`
(full list dumped); `make` ∈ `verb_lex`; `rules` ∈ `process_lex` (so `-rules` is a ProcessLex
terminal, not an object noun — the axis the existing `doc-writing-rules`/`naming-rules` pattern
uses). Under ADR-0011's grammar (`.claude/docs/spec/spec-naming-convention.md`: `make-` resolves
its residue against ObjectVocab alone; ProcessLex-terminal names take an ObjectVocab head, the
`entry-file-rules` production), **one new entry serves both names**:

```json
{ "canonical": "artifact", "plural": "artifacts", "banned_aliases": [] }
```

- **Anti-ambiguity gate** (`authorkit/skills/manifest-authoring/SKILL.md` step 2): passes —
  no existing multi-token `object_vocab` entry contains `artifact`, so longest-match resolution
  gains no new ambiguity. `banned_aliases` stays empty (no competing house synonym to ban yet).
- **Confirm gate:** `manifest-authoring` is mutating-confirm-required (#525): "No live user to
  confirm with → stop and report the gate SKIPPED rather than writing unconfirmed." The builder
  applies this edit only under a live confirmation (the coordinator relaying Kim's approval of
  this LLD, or Kim on the PR). If the build runs genuinely unattended, this is a
  **blocked(naming) handback**, never an improvised registered-vocab substitute — unlike
  lld-0008/lld-0009's cases, no registered token expresses "artifact" (`doc`, `reference`,
  `surface`, `screen` all mean different, already-fenced things), so the fallback that worked
  there does not exist here.
- **Gate before PR:** both drafted SKILL.md stubs pass
  `authorkit/skills/naming-audit/scripts/validate.py --scope grammar` (errors=0) after the
  manifest edit lands, and the manifest edit ends with the validator run per manifest-authoring
  step 5 (a manifest edit that creates new errors is reverted).

## Resolution 6 — CSS emission contract: `light-dark()`, per the source doc's own guide

**Resolved:** the emitted CSS uses `:root { color-scheme: light dark; }` +
`--c-<role>: light-dark(<light>, <dark>)` — this is the Adia DESIGN.md's **own Agent Prompt
Guide** pattern (verified in the source file:
`--c-primary: light-dark(oklch(0.5837 0.1265 236.48), oklch(0.6716 0.1414 234.43));`), and its
naming grammar `--c-{family}-{slot}` is adopted as-is. A manual theme toggle is one rule —
`[data-theme="light"] { color-scheme: light; }` / `[data-theme="dark"] { color-scheme: dark; }` —
flipping `light-dark()` resolution without duplicating any variable block (rejected alternative:
the `@media (prefers-color-scheme)` double-block, below). Additional emission rules, all
selftest-asserted:

- **Both color representations handled.** DESIGN.md frontmatter carries `-dark`-suffixed sibling
  keys in ONE flat map (`primary` / `primary-dark`); tokens.json splits into two parallel top-level
  objects (`colors` / `colorsDark` — verified in the source tokens.json). Either may arrive; the
  script normalizes both into role → (light, dark) pairs and fails (exit 1) on a role missing its
  dark counterpart.
- **Font fallback is mandatory.** CSP in Claude Artifacts blocks external font files, so a bare
  `'GT America'` renders as the browser default. Every emitted font property appends a system
  stack: `'GT America', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` and
  `'GT America Mono', ui-monospace, 'SF Mono', monospace`. The selftest's negative control asserts
  the output never contains a named custom font without a fallback tail.
- **Scales:** type roles → `--text-<role>-*` (size/weight/lh/ls) + `--font-*`; spacing array
  (0,4,8,12,16,24,32,48,64,96 — verified) → `--space-*` named none…5xl per DESIGN.md; radii
  (none/xs/sm/md/lg/xl/full → 0/4/8/12/16/28/9999 — verified) → `--r-*`.
- **Mermaid re-theme block** emitted as a standard section: token-keyed `!important` overrides of
  the rendered SVG's inline fill/stroke/color, referencing the same `--c-*` properties as the rest
  of the page, so both schemes re-theme through one mechanism (Resolution 7 carries the doctrine;
  the script carries the block).

## Resolution 7 — Encoded house doctrine (memory → shipped rules)

The three session-memory rulings become `references/` content, each with its grounding marker per
pack-writing-rules:

- **`shell-doctrine.md`:** narrative single-scroll for reports/retros — standing taste ruling
  2026-07-16 (session memory `review-page-shell-preference`), never a dashboard/tile shell for a
  report/retro page; tabbed chapters for handbooks (multi-section reference artifacts);
  mechanism-diagram-over-chip-wall — content explaining HOW something works gets one diagram of
  the real mechanism, not a wall of chips/badges/tiles. Marker: [incident]-grounded taste rulings,
  dated.
- **`mermaid-style.md`** (all three learned 2026-08-18 building the Estate Handbook, [incident]):
  `<br/>` is STRIPPED from mermaid node labels in this pipeline — node labels single-line,
  multi-line detail on EDGE labels; re-theming a rendered SVG requires token-driven CSS
  `!important` overrides (the SVG ships its own inline styles); hidden tab panels hide via
  `visibility: hidden` + a width-preserving technique (keep the layout box, or position
  off-screen), NEVER `display: none` — mermaid measures its container at render time and a
  zero-width container corrupts the diagram permanently even after the tab shows.
- **`design-system-consumption.md`:** the Resolution 6 contract in prose — input shapes (both
  representations), the `light-dark()` pattern, the font-fallback rule, scale mapping, the
  `--c-{family}-{slot}` grammar, and the pointer to `css_build.py` as the mechanized authority
  (the prose describes; the script IS the check, per script-writing-rules' mechanization test).
- **`refresh-procedure.md`:** Resolution 4.

## Components

Build sequence — a builder executes top to bottom:

1. **`naming.manifest.json`** (repo root) — add the Resolution 5 entry to `object_vocab`.
   CONFIRM-GATED: apply only with live confirmation (see Resolution 5); unattended → blocked
   handback. Then `python3 authorkit/skills/naming-audit/scripts/validate.py . --scope grammar`
   must show no new errors.
2. **`docs/skills/artifact-rules/references/design-system-consumption.md`** — Resolution 6/7
   content. Then **`shell-doctrine.md`**, **`mermaid-style.md`**, **`refresh-procedure.md`**
   (Resolution 7/4). Each file grounding-marked; each under pack-writing-rules' load budget.
3. **`docs/skills/artifact-rules/SKILL.md`** — knowledge surface: flat 4-row consult table
   (ask-pattern → file, 1:1, no INDEX.md), `user-invocable: false`. Description (draft):
   *"Standards for artifact/report-page authoring — consuming a design system (DESIGN.md +
   tokens.json) into light/dark `light-dark()` custom properties with mandatory font fallbacks,
   the house shell doctrine (narrative single-scroll for reports/retros, tabbed chapters for
   handbooks, mechanism-diagram-over-chip-wall), mermaid house style (single-line node labels,
   token-driven `!important` SVG re-theme, width-preserving tab hiding), and the artifact refresh
   procedure. Consulted by make-artifact. NOT the build procedure itself (make-artifact); NOT for
   authoring or grading the design-system source (design's make-design-system); NOT generic
   markdown rendering (markdown-to-markup)."* Draft only — superseded by the shipped SKILL.md on
   merge.
4. **`docs/skills/make-artifact/scripts/css_build.py`** — stdlib-only Python, skill-level
   `scripts/` (one skill owns it; invoked as `${CLAUDE_SKILL_DIR}/scripts/css_build.py`).
   Contract per script-writing-rules: positional-first
   `css_build.py <tokens.json | normalized-design-frontmatter.json> [--out page.css]`; no args →
   docstring + exit 2; exits 0/1/2; verdict line first (`css_build · ok · 0 fail`). Input is JSON
   in either color representation (stdlib has no YAML parser, so a DESIGN.md-only invocation has
   the session extract the frontmatter to JSON first — a stated, mechanical, lossless step;
   tokens.json is consumed directly). Emits the full Resolution 6 CSS including the mermaid
   re-theme block and the `[data-theme]` toggle rules. **`selftest` mode:** inline fixtures for
   BOTH representations; negative controls that bite (a role missing its `-dark`/`colorsDark`
   counterpart → exit 1; any named custom font in output without a fallback tail → fail);
   reverse control (complete fixture → exit 0, all expected `--c-*` pairs, `--space-*`, `--r-*`
   values present).
5. **`docs/skills/make-artifact/SKILL.md`** — procedural surface, `user-invocable: true`,
   `argument-hint: "[design-system path] [content source]"`. Phases: (1) locate inputs; (2) run
   `css_build.py` (never hand-derive the CSS); (3) choose shell per `artifact-rules`'
   shell-doctrine (report/retro → narrative single-scroll; handbook → tabbed chapters);
   (4) assemble page + mermaid per mermaid-style; (5) stamp the provenance footer
   (Resolution 4); (6) verify — selftest green, human render check named. Invokes
   `artifact-rules` explicitly, the `make-doc` → `doc-writing-rules` pattern. Description (draft):
   *"Build or rebuild a rendered Artifact/report page — consume a design system (DESIGN.md +
   tokens.json) plus report or handbook content into a polished single-file page: light/dark
   custom-property CSS, house shell, themed mermaid diagrams, provenance footer. Use for 'turn
   this report into an artifact page', 'rebuild the Estate Handbook', 'render this with our
   design system'. Runs via /make-artifact [design-system path] [content source]. NOT the
   standards themselves (artifact-rules); NOT for authoring/grading the design-system source
   (design's make-design-system); NOT for drafting a functional document (make-doc); NOT for
   generic markdown→DOM rendering (markdown-to-markup)."* Draft only — superseded by the shipped
   SKILL.md on merge.
6. **`docs/skills/make-artifact/evals/evals.json`** + **`docs/skills/artifact-rules/evals/evals.json`**
   — ~6 trigger / ~7 no-trigger each. No-trigger cases fence: make-doc's vocabulary ("write the
   PRD…" → make-doc), markdown-to-markup's ("render this markdown" → markdown-to-markup),
   make-design-system's ("port our design system to Stitch" → design), and each other
   (build ask → make-artifact; standards consult → artifact-rules).
7. **Reciprocal fence edits (sibling descriptions + their evals, same change per
   `.claude/rules/plugin-authoring.md`):**
   - `docs/skills/make-doc/SKILL.md` — append to the NOT-list: *"NOT for building a rendered
     Artifact/report page from a design system (make-artifact)."* + one no-trigger case in
     `docs/skills/make-doc/evals/evals.json`.
   - `docs/skills/markdown-to-markup/SKILL.md` — append: *"NOT for building a full
     design-system-styled Artifact page (make-artifact — that consumes tokens; this renders
     markdown grammar)."* + one no-trigger case in its evals.json.
   - `design/skills/make-design-system/SKILL.md` — append: *"NOT for consuming an already-authored
     system into a rendered artifact/report page (docs' make-artifact)."* — soft cross-plugin
     mention, degrades gracefully — + one no-trigger case in
     `design/skills/make-design-system/evals/evals.json`.
8. **Plugin close-out, two plugins:**
   - `docs/.claude-plugin/plugin.json`: **1.18.0 → 1.19.0** (verified 1.18.0 on `origin/main` in
     this clone at authoring time) + manifest description gains the artifact-authoring clause.
     `docs/README.md` ledger line: *"v1.19.0 · <date> · closes #619: new skills
     `make-artifact` (procedural; bundled `css_build.py` selftest-proven token→CSS build,
     `light-dark()` pairs, mandatory font fallbacks) + `artifact-rules` (4-axis references corpus:
     design-system consumption, shell doctrine, mermaid house style, refresh procedure — the
     2026-07-16/2026-08-18 memory rulings now shipped rules). Full resolutions in lld-0619.
     Reciprocal fences in make-doc/markdown-to-markup (+ design's make-design-system, shipped as
     design v1.0.9). New `object_vocab` entry `artifact` (confirm-gated). `release_gate.py docs`
     clean."*
   - `design/.claude-plugin/plugin.json`: **1.0.8 → 1.0.9** (verified 1.0.8 on `origin/main`;
     description-only fence edits precedented as patch bumps, cf. v1.0.7/v1.0.8) +
     `design/README.md` ledger line naming the reciprocal fence and #619.
9. **Gates before PR:** `skill_lint.py` on every touched SKILL.md + evals.json;
   `css_build.py selftest` green; naming validate per step 1; `/check-routing docs` and
   `/check-routing design` (description boundaries changed in both); `release_gate.py docs` and
   `release_gate.py design`; fresh-context `harness:skill-checker` pass over the semantic edits
   (plugin-authoring.md's critic invariant).

## Interfaces

- **`make-artifact` → `artifact-rules`:** same-plugin skill invocation + consult-table citation —
  the `make-doc` → `doc-writing-rules` contract, adopted verbatim.
- **`make-artifact` → `css_build.py`:** `${CLAUDE_SKILL_DIR}/scripts/css_build.py <json> [--out]`;
  JSON in (either color representation), CSS out, exit tri-state. The skill never hand-derives
  what the script emits.
- **`make-artifact` → design plugin:** soft named mention only (consumes DESIGN.md/tokens.json as
  FILES at a user-supplied path — no preload, no cross-plugin `${CLAUDE_PLUGIN_ROOT}` path;
  plugin-authoring.md's hard boundary holds).
- **Artifact page → future refresh:** the provenance footer is the machine-readable interface a
  refresh run reads its inputs from (Resolution 4).

## Data

Static skill/reference markdown + one bundled script; no runtime store, no migration. An artifact
BUILD's output (the page + its CSS) is user/project-owned, landing wherever the invoking session
directs; nothing run-produced ships inside the plugin tree. Input shapes owned upstream by the
design plugin's exports (tokens.json keys verified against the Adia source: `colors`/`colorsDark`,
`semantic`/`semanticDark`, `type`, `spacing`, `radii`, `geometry`, `icons`, `motion`).

## Risks

- **R-1 (naming confirm gate vs unattended build).** The `object_vocab` mint cannot be written
  unconfirmed (manifest-authoring, #525). Detection: the builder reaches step 1 with no live
  confirmation channel. Fallback: blocked(naming) handback naming the exact proposed entry — never
  an improvised substitute name (Resolution 5's reasoning; no registered token fits).
- **R-2 (input-shape drift).** The Adia system regenerates and a key shape changes
  (e.g. `colorsDark` folded into suffix keys). Detection: `css_build.py` exits 1 with the missing
  role named; the selftest fixtures encode both known shapes. Fallback: fixture + normalizer
  updated same-day (incident → infrastructure).
- **R-3 (render-layer blind spot, accepted).** Payload asserts cannot see a shell that renders
  wrong or a mermaid SVG that mis-themes visually. Detection: the human render check named in
  `make-artifact`'s Done block — a stated exception per assert-layer-choice, deliberately not a
  browser harness (Rejected alternatives). Residual risk accepted.
- **R-4 (fence drift across two plugins).** `make-artifact` overlaps trigger vocabulary with three
  siblings, one in another plugin. Detection: reciprocal no-trigger cases in all five evals suites
  + `/check-routing` on both plugins in this same PR. Fallback: routing-eval failures point at the
  exact description line to sharpen.
- **R-5 (YAML extraction left to the model).** DESIGN.md-frontmatter input requires a
  model-performed YAML→JSON extraction (stdlib-only constraint). Detection: the script validates
  the normalized JSON's shape and fails loudly on gaps; tokens.json (the common case) needs no
  extraction. Fallback: if this step misfires in practice, promote a constrained frontmatter
  parser into the script as its own selftest-covered mode — a contained follow-up, not this build.

## Rejected alternatives

- **Home = `design` plugin.** Rejected by the anti-matrix evidence (Resolution 1):
  `make-design-system` scopes itself to authoring/grading the SOURCE, its routing table has no
  consumption slot, and #619's Links already designate design as the token source this feature
  consumes. Putting a consumer next to the source would also put report/handbook CONTENT concerns
  (docs territory) inside a token-authoring plugin.
- **A `/make-pack` corpus instead of one knowledge skill.** The rules are earned house practice
  (dated taste rulings + one incident session), not a research domain; 4 axes fit one skill's flat
  references/ table under pack-writing-rules' own enumerability rule. A pack + research waves
  would be manufactured process.
- **A browser-layer visual-regression harness.** Assert-layer-choice's failure catalog names this
  exact trap ("default-to-browser"): every acceptance criterion in #619 except "looks right" is
  payload-shaped. The render check stays human, stated, cheap; a Playwright-class suite would be
  the most expensive layer bought for the fewest criteria.
- **A hook-based refresh mechanism.** Hooks are fully retired in this workspace (#466); also a
  hook could at best nag, not rebuild. The provenance footer + named procedure makes staleness
  detectable and refresh reproducible without automation.
- **`@media (prefers-color-scheme)` double-block or `[data-theme]`-only variable swaps** instead
  of `light-dark()`. The source DESIGN.md's own Agent Prompt Guide ships the `light-dark()`
  pattern; the double-block duplicates every variable (drift surface), and Artifacts run in
  current Chrome where `light-dark()` is supported — the CSS `light-dark()` function's browser
  support baseline is Chrome 123+ (shipped March 2024; also Edge 123+, Safari 17.5+, Firefox 120+),
  comfortably below the Artifacts runtime. The `[data-theme]` rules are kept only as the
  one-line `color-scheme` toggle, not a parallel variable tree.
- **Prose-only token mapping (no script).** The workspace CLAUDE.md's mechanization doctrine ("a
  hand-run check or prose checklist that could be code") and the six hand-rolled rebuilds that
  motivated #619 both say the same thing: the mapping is deterministic derivation — exactly
  script-writing-rules' "arithmetic, not judgment."
- **A single dual-mode skill** (procedure + standards in one SKILL.md). Rejected on the same
  grounds lld-0009 Resolution 1 recorded for its pairing: one description carrying two audiences'
  trigger vocabulary degrades the routing surface; the plugin's own `make-doc`/`doc-writing-rules`
  precedent is two surfaces.

## Agent verification

Assert-layer choice per `docs/skills/agent-harness-rules/references/assert-layer-choice.md`
(Resolution 3). New instrument this design needs: **`css_build.py selftest`** — the payload-layer
harness carrying #619's Acceptance criterion 2 ("Given the Adia DESIGN.md + tokens.json, the
capability emits artifact CSS with light/dark custom-property pairs, type roles, and
radius/spacing scales.") as executable predicates (light/dark
custom-property pairs, font stacks with mandatory fallback tails, radius/spacing scale values,
both input representations; negative + reverse controls per script-writing-rules). Existing
instruments covering the rest: `skill_lint.py` + `eval_check.py` (mechanical), the two new + three
edited evals suites with reciprocal negatives run via `/check-routing docs` and `/check-routing
design` (routing), `release_gate.py` G4 executing the selftest on both plugins' gates
(enforcement). **Stated exception (human layer):** shell rendering fidelity and visual mermaid
re-theme — named in `make-artifact`'s Done block, per assert-layer-choice's rule that every
human-routed criterion is a written exception, never a silent absence. The ticket names its
Acceptance inline; no SPEC exists to cite (frontmatter's routing note).
