---
doc-type: lld
id: lld-0009-harness-facts-project-context-harvest
status: approved
version: 1.0.0
date: 2026-08-17
owner: kim.granlund
ticket: nonoun-plugins#613
spec: none — same routing as lld-0008: the ticket's own Acceptance section carries the checkable
  criteria and its Scope/Open section names the exact design questions this LLD resolves, so a
  standalone SPEC would restate what the ticket already states (doc-writing-rules' own routing
  test)
---
# LLD — `harness-facts`: the project-context harvest skill (agent/harness-facing sibling of `project-facts`)

**Verdict, head-first:** one user-invocable docs skill (`harness-facts`), the mirror-image sibling
of `project-facts` (#612, lld-0008): same harvest substance, same shared core
(`../project-facts/references/harvest-core.md`, cited never duplicated), opposite axis weighting
(Inside-Out 60 / Outside-In 40), and a different consumer — a coding agent and its harness. The
two genuinely new decisions this LLD makes on its own: the **output contract is ready-to-install
harness artifacts** (a CLAUDE.md-grade entry-file section, `.claude/rules/` path-scoped files,
knowledge-pack seed candidates, a dispatch-context block — staged, never installed in place), and
the **eval is a WITH-vs-WITHOUT delta run** (the same agent-task prompts answered with and without
the produced artifacts in context, delta scored via the shared rubric). Naming follows #612's own
recorded precedent: the ticket's lean (`harvest-project-context`) fails ADR-0011's grammar gate
without new vocabulary, and there is no live user to ratify a mint, so the name is built entirely
from already-registered vocabulary. Resolutions below, each with its rejected alternatives.

## Resolution 1 — Surface shape: one skill, mirroring lld-0008 Resolution 1

**Resolved:** one user-invocable, model-invocable skill (`disable-model-invocation: false`,
`user-invocable: true`) at `docs/skills/harness-facts/`, citing the shared core by relative path.
lld-0008 Resolution 1 already litigated this exact fork for the sibling — command vs skill,
dual-mode single SKILL.md vs two skills citing one core — and every argument transfers unchanged:
a command surface would be unreachable from `dispatch-ticket`'s Skill-tool routing, and a dual-mode
SKILL.md would force one description to carry two audiences' trigger vocabulary, against
`plugin-authoring.md`'s routing-surface discipline. Adopted by citation, not re-derived.

**Rejected:** the same alternatives lld-0008 Resolution 1 rejected (command wrapper; single
dual-mode SKILL.md), for its recorded reasons. Additionally rejected here: folding this capability
into `project-facts` as a post-processing flag ("--for-agents") — the two corpora's weighting,
output contract, and eval design all differ, and a flag would bury the routing-relevant consumer
distinction below the description layer where `/check-routing` can't see it.

## Resolution 2 — Naming: `harness-facts`, not `harvest-project-context` or a `project-` prefix

**Resolved:** the skill is named `harness-facts` — ObjectVocab `harness` + ProcessLex `facts`,
both already registered in the repo-root `naming.manifest.json` (ADR-0011). Zero new vocabulary.
Grammar-validated clean against a drafted SKILL.md stub
(`authorkit/skills/naming-audit/scripts/validate.py --scope grammar`: 1 artifact, errors=0), and
grepped repo-wide with zero collisions. Semantically it is the exact mirror of the sibling's name:
`project-facts` = facts about the project, for a human reader; `harness-facts` = facts FOR the
harness — the consumer, which is the only real differentiator between the two corpora
(`harvest-core.md`'s own definition table), is in the name itself.

**Rejected:**
- `harvest-project-context` (the ticket's own stated lean) — requires registering `VerbLex:
  harvest` and an ObjectVocab for `context`/`project-context`, and `authorkit:manifest-authoring`'s
  confirm gate cannot fire unattended (no live user in this build). Identical precedent: lld-0008
  Resolution 5 and the `agent-harness-rules` ledger entry it cites. A future live-ratified mint +
  `rename-planning`/`rename-execute` pass remains open, exactly as it does for the sibling.
- `project-context-facts` or any `project-` prefix — fails twice: (a) `context` is not registered
  ObjectVocab, so the grammar gate rejects it regardless of prefix; (b) lld-0008's own
  "Consequence for #613" note — a `project-` prefixed sibling risks reading as a near-duplicate of
  `project-facts` by name alone.
- A `*-rules` tail (lld-0008's own suggestion, e.g. `harness-rules`) — considered and rejected on
  this estate's own usage evidence: every `*-rules` skill here (`naming-rules`,
  `entry-file-rules`, `doc-writing-rules`, `agent-harness-rules`, `prompt-wording-rules`, …) is a
  standards/doctrine pack, a thing you consult; this skill is a harvest capability, a thing you
  run. A `-rules` name would misroute consults toward it and — worse — collide head-on with
  `docs:agent-harness-rules`' trigger vocabulary in the same plugin.
- `entry-file-facts` — grammar-clean but too narrow: the output spans entry-file sections,
  path-scoped rules, knowledge-pack seeds, AND dispatch context; naming it for one artifact class
  would misdescribe three of four.
- `repo-facts` / `code-facts` — grammar-clean but they re-describe the SUBSTANCE, which both
  siblings share identically; the differentiator is the consumer. A substance-flavored name blurs
  the very fence the reciprocal evals exist to hold.

## Resolution 3 — Output contract: ready-to-install harness artifacts, staged, never installed in place

**Resolved:** the skill's write step (the Step 5 equivalent) emits **install-ready artifacts**,
not an author-shaped prose corpus — the consumer is the harness itself, so value shows only when
the output can drop into a harness with no translation pass. Four artifact classes plus a spine:

1. **A CLAUDE.md-grade entry-file section** — conforming to `harness:entry-file-rules`' residency
   test (identity-grade, declarative register, pointer-heavy, seed-class sizing); every line must
   pass "true on every turn, needed before task content frames it." Cross-plugin soft mention per
   `plugin-authoring.md` — the SKILL.md cites `harness:entry-file-rules` by name and carries the
   one-line residency test inline as the degraded-gracefully floor when harness isn't installed.
2. **`.claude/rules/` path-scoped rule files** — one per subtree-local zone finding, each stating
   its own path scope up top (this workspace's own `.claude/rules/` convention, which is itself
   `entry-file-rules`' eviction-table destination for subtree-local truth).
3. **Knowledge-pack seed candidates** — flagged entries naming the target pack and the
   `/make-pack` command a human runs next; the skill NEVER hand-scaffolds a pack (the workspace
   routing table owns pack creation via `/make-pack`).
4. **A dispatch-context block** — a paste-ready digest for dispatch prompts (the context a
   `dispatch-ticket`/`build-leader` seat would paste into a builder's dispatch).

Plus the **run manifest** — one index doc listing every emitted artifact with its per-zone
two-axis scores and source citations. The manifest is the corpus's spine: it is what the rubric
self-score (R1–R7) and the eval run score against, so "the corpus" stays one gateable thing even
though its payload is many files. All output lands at a staging path the invoking session directs
(mirroring `project-facts`' user/project-owned output rule) — **installation is the invoker's
act**, never the skill's.

**Rejected:** an author-shaped single reference doc (the sibling's Step 5 shape) — a
human-readable corpus would need a second translation pass before any harness could consume it,
which is exactly the gap between the two tickets; also the dispatching coordinator's stated lean
was ready-to-install. Also rejected: writing directly into the target project's live CLAUDE.md /
`.claude/rules/` — mutating a project's entry file is the highest-blast-radius write a harness
has (`entry-file-rules`: a stale line is *believed*, not ignored), and it belongs behind the
invoking human/host's own review, not inside an extraction skill's happy path.

## Resolution 4 — Eval design: WITH-vs-WITHOUT delta on this workspace

**Resolved:** the sample project is **this workspace itself** (`kimgranlund/claude-plugins`) —
adopting lld-0008 Resolution 3's reasoning by citation (ratified known-answer records already sit
in `.claude/docs/`, no answer key needs authoring). The eval is payload-layer per
`docs:agent-harness-rules` (assert-layer choice: the artifacts are text payloads; a Q&A/task run
against them measures value with no browser or human in the loop), with the design delta the
ticket demands: a **WITH vs WITHOUT** comparison. Fixed agent-task prompt set F1–F6, each an
Inside-Out-flavored question a dispatched coding agent actually needs answered from context (which
gate command must pass before a plugin ships; where a new work item is recorded; which rule file
governs a SKILL.md description edit; where a campaign worktree lives; what the version bump means
to the update cache; which command owns creating a new pack). Two runs: the answering agent sees
(WITH) only the produced artifacts, or (WITHOUT) no corpus — then answers are checked against the
known-answer key (the workspace's own CLAUDE.md, `.claude/rules/`, ADRs) and the delta is scored
through `harvest-core.md`'s dimensions (R3 mechanism legibility, R6 traceability, R5 weighting
visible in what the corpus chose to surface). The harness for this feature IS the scored delta
report: WITH must beat WITHOUT, and every WITH answer must trace to an emitted artifact.

**Rejected:** reusing the sibling's E1–E6 prompts verbatim — they probe Outside-In business
questions ("what problem does this solve, for a non-engineer"), the wrong consumer for this
corpus; structurally F1–F6 mirror E1–E6 (fixed table, axis-probed, known-answer-sourced,
extend-per-project header) but every prompt is an agent-task. Also rejected: a synthetic sample
project (lld-0008 Resolution 3's recorded rejection — hand-authored answer key, no independent
ratification) and a single WITH-only run (proves the corpus is answerable-from, not that it
*improves* performance — the ticket's acceptance criterion is the delta).

## Resolution 5 — Shared core and weighting: cite `harvest-core.md`, Inside-Out 60 / Outside-In 40

**Resolved (largely pre-resolved by lld-0008 Resolution 4, adopted by citation):** this skill
cites `../project-facts/references/harvest-core.md` by relative path from its own files — the
same-plugin citation lld-0008 established, not a copy, not a symlink. This corpus states only its
OWN weighting — **Inside-Out 60 / Outside-In 40**, the exact mirror the core's R5 paragraph
already forward-declares for #613 — and its own consumer framing. Deliverables (a) and (b) are
therefore satisfied by the existing core file plus this skill's weighting statement; nothing is
re-minted. Per the core's own rule, both axes are still scored for every zone (R4); the weighting
changes the aggregate arithmetic (`0.6 * InsideOut + 0.4 * OutsideIn`) and the ranking order, and
zone names lean mechanism-honest (a zone may be named "release gate (G1–G11)" here where the
sibling would say "quality assurance") — the naming register is the consumer framing, the
discovery rule is unchanged.

**Rejected:** duplicating any of the core's body text into this skill's references (the ticket's
own acceptance criterion forbids it); a symlink to the core (lld-0008 Resolution 4's recorded
rejection — a symlink asserts identity, a citation asserts use-with-own-weighting).

## Resolution 6 — Reciprocal fencing, both directions, in this same change

**Resolved:** three fence surfaces, all in the one docs-plugin PR (one version bump total):

1. **This skill's description** states consumer = coding agent/harness, output = ready-to-install
   harness artifacts, and carries an explicit NOT-line naming `project-facts` ("NOT for the
   human/business-facing domain-knowledge corpus — docs:project-facts, shares
   `references/harvest-core.md`, opposite weight").
2. **This skill's `evals/evals.json`** includes a negative case fencing the sibling's own trigger
   vocabulary ("extract the domain knowledge from this project, for a business reader" →
   no-trigger, note owner: project-facts), plus negatives for the adjacent neighbors
   (`entry-file-rules`/`check-entry-file` — auditing an EXISTING CLAUDE.md is not harvesting one;
   `make-pack` — filling a pack is not seeding candidates; `agent-harness-rules` — designing a
   test harness is not producing harness context; `save-lessons` — judging one fact's durability
   is not a corpus harvest).
3. **The sibling's placeholder forward-references get their real name**: `project-facts`'
   SKILL.md description ("project-context, #613" → "docs:harness-facts, #613"), its `evals.json`
   n05 note ("the project-context sibling (#613 …)" → "harness-facts (#613 …)"), and
   `harvest-core.md`'s three forward mentions ("#613 project-context, not yet built" header line,
   the definition-table column head, the R5 weighting paragraph and Sources line). Name-only
   corrections to a forward placeholder — no substance change, no separate re-ship of
   project-facts (docs bumps once for this whole PR).

**Rejected:** leaving the sibling's "#613/project-context" placeholders standing — a stale
forward-reference is exactly the stale-context defect the operating contract ranks with bugs, and
the dispatch explicitly assigns the fix here. Also rejected: filing a follow-up ticket for the
placeholder fix — three one-line edits in the same plugin and PR do not earn a work item.

## Components

Build order for the builder (project-facts edits last, once the new skill's name and files are
real):

1. **`docs/skills/harness-facts/references/extraction-procedure.md`** — this corpus's own Step 1–6
   procedure: Steps 1–3 structurally parallel to the sibling's (same sources, same intent-first
   order, same zero-source exit, same ≥2-source zone rule — cited to `harvest-core.md`, with
   mechanism-honest zone naming register per Resolution 5); Step 4 the Inside-Out 60/40
   arithmetic; Step 5 emits the Resolution 3 artifact classes (pointing to
   `output-artifacts.md` for each class's conformance contract); Step 6 the gate + eval pointer.
2. **`docs/skills/harness-facts/references/output-artifacts.md`** — the Resolution 3 contract per
   artifact class: entry-file section (residency test, seed-class sizing, `harness:entry-file-rules`
   soft citation + inline floor), path-scoped rule files (scope statement up top), pack seed
   candidates (`/make-pack` handoff, never hand-scaffolded), dispatch-context block, run manifest
   shape. This file is the genuinely new substance vs the sibling (whose Step 5 is one
   make-reference doc), which is why it earns a fourth reference file rather than bloating the
   procedure.
3. **`docs/skills/harness-facts/references/eval-harness.md`** — Resolution 4: sample project,
   WITH/WITHOUT procedure, F1–F6 table (prompt · axis/dimension probed · known-answer source),
   delta-scored report shape, extend-per-project header.
4. **`docs/skills/harness-facts/SKILL.md`** — routing surface (Resolution 6 fences), operating
   model, 6-step procedure summary, output contract block, references table (citing
   `../project-facts/references/harvest-core.md` in the table with "canonical, lives with the
   sibling" wording), composition section (`project-facts` sibling; `harness:entry-file-rules`;
   `docs:agent-harness-rules`; `docs:make-rubric`), Done/NOT-done block requiring the WITH>WITHOUT
   delta.
5. **`docs/skills/harness-facts/evals/evals.json`** — ~7 trigger / ~8 no-trigger per Resolution 6.
6. **Edits to `docs/skills/project-facts/`** — SKILL.md description, evals.json n05,
   harvest-core.md forward mentions (Resolution 6 item 3).
7. **Plugin close-out** — `docs/.claude-plugin/plugin.json` version bump (one bump for the whole
   PR, from 1.16.0) + README footer ledger line; `skill_lint.py` on every touched SKILL.md +
   evals.json; `/check-routing docs` (description boundary changed on two skills); `release_gate.py
   docs` before ship.

## Interfaces

- **`harness-facts` → shared core**: SKILL.md + extraction-procedure.md read
  `../project-facts/references/harvest-core.md` by relative path — same-plugin markdown citation,
  the contract lld-0008 established.
- **`harness-facts` → `harness:entry-file-rules`**: soft named mention only (cross-plugin) — the
  standard is cited, one-line floor inline, no preload, no `${CLAUDE_PLUGIN_ROOT}` path across
  plugins (`plugin-authoring.md` hard rule).
- **Artifacts → consumer**: staged files whose install targets are the invoker's own
  CLAUDE.md / `.claude/rules/` / pack pipeline / dispatch prompts; the run manifest is the single
  index the rubric and eval score against.
- **Eval → rubric**: the delta report cites `harvest-core.md`'s dimension IDs (R3/R5/R6) directly,
  same as the sibling's — the rubric table IS the interface.

## Data

Static markdown artifacts only — no runtime store, no migration. A harvest RUN's output (the
staged artifact set + run manifest) is user/project-owned, landing wherever the invoking session
directs; nothing run-produced ships inside the plugin tree.

## Risks

- **R-1 (naming, inherited).** `harness-facts` is registered-vocabulary-compromised exactly as
  `project-facts` is (lld-0008 R-1). Detection: a reader searching "project context" or "harvest"
  won't find it by file name. Fallback: the description carries the full trigger vocabulary
  ("project context", "CLAUDE.md", "rules", "dispatch context"), so routing is unharmed; a
  live-ratified mint + rename pass stays open for both siblings together.
- **R-2 (install-ready ≠ installed).** The staged-artifact contract (Resolution 3) means a run can
  "succeed" and its output never get installed. Detection: the run manifest names each artifact's
  intended install target; the eval's WITH run exercises the artifacts as they'd be consumed, so
  an artifact that couldn't actually serve its target fails F-prompts before install. Fallback:
  accepted by design — auto-installing was the rejected alternative, deliberately.
- **R-3 (fence drift between siblings).** Two same-plugin skills sharing substance vocabulary is
  the highest-collision routing pair this plugin has. Detection: both evals suites carry
  reciprocal negatives (Resolution 6) and `/check-routing docs` runs in this same PR after both
  descriptions settle. Fallback: routing-eval failures point at the exact description line to
  sharpen.
- **R-4 (WITHOUT-run contamination).** The WITHOUT arm of the eval runs in this very workspace,
  whose entry files already carry much of the answer key — an answering agent with the workspace's
  own CLAUDE.md loaded would score spuriously high WITHOUT the corpus. Detection/mitigation: the
  eval-harness file must state the isolation rule explicitly — the answering context gets ONLY
  the prompt (WITHOUT) or the prompt + staged artifacts (WITH), never the workspace's live entry
  files; a WITHOUT answer citing a source it was never given marks the run invalid, mirroring the
  sibling's "accidentally right is still a MISS on R6" rule.

## Agent verification

Payload-layer, per `docs:agent-harness-rules` (estate-mapping step checked: the sibling's
`eval-harness.md` is the nearest existing instrument, but it measures answerability of a prose
corpus by a reader's questions — it cannot measure whether HARNESS artifacts improve an agent's
task performance, which is this ticket's acceptance criterion, so the WITH/WITHOUT delta harness
is a genuine new instrument, not a duplicate). Mechanical half: `skill_lint.py` on every touched
artifact + the rubric self-score gate (R1, R4, R5, R7 ≥ 3) on the run manifest. Payload half: the
F1–F6 WITH-vs-WITHOUT delta run on this workspace, WITH strictly better than WITHOUT with every
WITH answer traceable to an emitted artifact (R6), under R-4's isolation rule. Routing half:
`/check-routing docs` green after both siblings' descriptions settle, both reciprocal negative
cases passing.
