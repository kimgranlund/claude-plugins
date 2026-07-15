---
name: repo-alignment
description: >
  Run a structured alignment campaign on a repo whose agent harness and context records
  have drifted — duplicated instruction trees, bloated entry files, dead automation, orphaned
  files, unwritten conventions, and a stale living design-doc corpus (ADRs, PRDs, SPECs,
  LLDs, RFCs). Use when the user says "align/recalibrate this repo", "run a harness
  consolidation / hygiene campaign", "our CLAUDE.md is bloated and stale", "consolidate the
  .claude setup", "audit and clean up the agent harness", "our ADRs/specs have drifted from
  reality", "this repo's context has drifted". A deliberate, multi-phase, committing
  campaign — never auto-fires; invoke explicitly via /repo-alignment (the trigger phrases
  above are what a session should recognize and SUGGEST this command for). NOT for the
  estate's own plugin workspace (harness-audit); NOT for layout-only migration of docs to
  the canonical docs/ map (docs-alignment, scribe, where installed — this campaign's corpus
  lenses go deeper: liveness, supersession, status-vs-reality).
user-invocable: true
disable-model-invocation: true
argument-hint: "[repo path] [--phases 0-6 | audit-only]"
---

# Repo Alignment

A campaign, not a cleanup: phased, evidence-driven, human-checkpointed, self-instrumenting.
The output is not just a tidier repo — it is a repo whose exit criteria became **standing,
machine-enforced gates**, plus a distilled lessons skill so the next drift is cheaper to fix.

## Prime directive: verify every premise against THIS repo

This playbook is a template, and templates lie. Before executing any phase, verify its
premise against the actual repo — expect some phases to be N/A and others to change shape
(a "hardcoded schema to extract" may not exist; a "duplicate tree" may be one dir; the
"agents to audit" may be zero). A false premise discovered mid-phase goes in the calibration
log (below) and the phase adapts; it is never executed on the template's say-so.

## Standing disciplines (all phases)

- **CALIBRATION.md** in the report root, appended continuously: every deviation from plan,
  every guess where instructions underspecified, every human correction, every check failure
  and its cause, every premise that proved false. An empty log means deviations went
  unrecorded — treat that as a finding. This log is Phase 6's primary corpus.
- **One commit per phase / work package**, on a dedicated branch; VCS-native moves/deletes
  (`git mv` / `git rm` or the repo's VCS equivalent), no attic dirs — version history is the
  attic (the corpus `archive` disposition, which files docs under the repo's declared archive
  convention, is the sanctioned exception). Working tree clean before starting (log exceptions).
- **Nothing is moved or deleted without first appearing in a manifest or ratified table.**
- **Report root** (`reports/<campaign>-<date>/` or the repo's own convention) with a
  FINDINGS.md index updated every phase; all verdicts land as files, not chat.
- **Ratification checkpoints:** pause for explicit human approval before (a) the first
  destructive swap, (b) executing any manifest, (c) the final lessons-distillation phase.
  A denied ratification is re-derived from the objection and re-presented — never argued
  past; the gated phase does not proceed.
- **Sanctioned-exception classes** for reference sweeps: ignore-lists, exclusion globs,
  self-descriptions of the new state, and historical records (dated analyses, CHANGELOGs,
  archives, plan docs) are never rewritten — exclude them from mechanical sweeps BY DEFAULT.

## Evidence rules (how verdicts earn trust)

- **Path-grep, never word-grep** — common dir names match English prose everywhere; grep the
  path string or exact filename.
- **A keep-verdict needs WRITE/READ-target evidence** — a file *mentioning* a directory is
  not a referrer; check what actually consumes it.
- **Hash-compare before relocating a stray** — root orphans are often byte-identical
  duplicates of a tracked canonical copy: delete, don't archive twice.
- **Read before delete-classing** — a garbage filename may conceal real content; rename on
  relocation instead.
- **Recency from `git log`, not memory** — when two copies diverge, per-file last-commit
  dates decide which side was maintained.
- **Green CI is not alive CI** — verify a workflow's invoked files/modules exist on disk and
  its trigger source is itself alive; `continue-on-error` + advisory modes paint corpses green.
- **Tracked does not imply not-ignored** — gitignored dirs can contain force-added tracked
  files; new files there need `git add -f`, `git mv` of tracked files works.
- **.gitignore is a record and drifts like one** — sweep it both directions: a rule naming a
  retired path (a migrated docs tree, a removed worktree dir, a renamed build output) is stale
  context, repaired by the same change that invalidated it; and an in-repo worktree or
  generated dir sitting unignored is one `git add -A` from being committed. Worktrees are
  routinely IN-repo — Claude Code's own EnterWorktree creates them at `.claude/worktrees/` —
  so verify the ignore rule exists rather than assuming out-of-repo placement (this razor's
  first wording assumed exactly that; amended 2026-07-15, same day, when the tool's own
  contract falsified it).
- **Hooks fire on tool writes, not scripted writes** — after any batch/scripted sweep, run
  the lints in batch mode.
- **A status field is a claim, not evidence** — a document's liveness comes from whether its
  subject and consumers are live, not from what its frontmatter says; verify `accepted`,
  `draft`, and `superseded` against the artifacts they describe.
- **Ambiguous classification is flagged, never applied silently** — a doc that can't be told
  apart from reference or archive material stays where it is with a finding attached;
  misfiling a live spec as reference is worse drift than leaving it unaudited.

## The phases

### Phase 0 — Inventory & reconcile (execute; ends in a checkpoint)

Map the harness surfaces: instruction/entry files (and any twins like AGENTS.md vs
CLAUDE.md), skill/command/agent dirs (and any duplicate trees), hooks and settings, CI
workflows, repo root. For duplicate trees: per-file content-hash diff; classify identical /
A-only / B-only / diverged; run a rename-drift pass (cross-tree hash matching) so renamed
twins aren't misread as two singletons; gather per-side recency. Produce a reconciliation
table with a declared winner rule (typically: the tree the runtime actually loads wins).

**Design-doc corpus sweep** (same phase): discover the living decision/spec corpus by
convention signals, never a hardcoded layout — directory conventions (`decisions/`, `adr/`,
`docs/adr/`, `rfcs/`, `specs/`, `prds/`, `design/`), filename spines (`ADR-*`, `PRD-*`,
`SPEC-*`, `LLD-*`, `RFC-*`, `TDD-*`), and content shapes (status frontmatter/headers,
Decision/Context/Consequences sections). Classify every hit **active / archive / reference**
using the repo's own signals in priority order: explicit archive markers and archive-path
membership → status vocabulary (`superseded`, `deprecated`, `archived`) → reference/lookup
placement → recency plus inbound-reference liveness. Output a corpus map with counts per
class; the archive and reference classes are excluded from all downstream phases (that
exclusion is itself evidence-based, per the classification rule above).

**CHECKPOINT: the reconciliation table + corpus map are ratified by a human before Phase 1
swaps anything.**

### Phase 1 — Unify (execute)

Collapse ratified duplicates: canonical content wins; the duplicate becomes a symlink (or is
deleted). Repair every live reference that asserts the dead path as authority — enumerate the
sanctioned exceptions explicitly. Verify with `readlink` on exact paths (a leftover
non-empty dir can swallow a symlink silently — check placement, don't assume). Smoke-test
that at least one OTHER consumer (a second agent harness, CI, an editor) resolves the new
shape. Note symlink portability (Windows needs core.symlinks).

### Phase 2 — Orphan sweep (manifest only — nothing moves yet)

Derive a root allowlist from the repo's own documented structure plus live-referrer
evidence. Everything outside it gets a **typed disposition**: `delete` (dead or
byte-duplicate) · `prototype` (experiments → a prototypes/ convention) · `relocate` (with
target) · `keep` (evidence overturned suspicion — record why). Every non-keep item carries a
**referrer-repair map** (configs, CI, skill bodies, generated indexes — noting which indexes
are regenerated, never hand-edited).

### Phase 3 — Schema & standing guards (execute; gates Phase 4)

Establish the canonical contract for harness metadata (skill/agent/command frontmatter or
this repo's equivalent) — extracted from wherever it's hardcoded, or **authored from a survey
of observed practice** when (as often) no canonical statement exists. Distinct config
grammars get distinct validation profiles — never force one tree's grammar onto another.
Survey the **design-doc grammar** the same way: the corpus's observed status vocabulary, ID
spine, and cross-reference convention (`depends_on` / `supersedes` / `relates_to` or their
equivalents). An existing schema or validator is the contract; absent one, the documented
majority practice becomes it — so Phase 4's corpus verdicts have terms to be expressed in.
Then split enforcement from semantics:
- **semantics** → a compact (≤120-line) authoring standards knowledge skill in the repo;
- **deterministic checks** → a write-time lint hook where the harness supports hooks
  (repo-committed, so it travels with any checkout — personal hooks are invisible to other
  contributors); otherwise the batch mode of the check script below is the enforcement point;
- **the campaign's exit criteria** → a committed two-tier check script: **structural** tier
  (must pass now; gates) and **hygiene** tier (pending later phases; reported, promoted to
  gating once the backlog clears). Run it after every phase — expect it to catch your own
  mistakes; that is it working.
- Entry files get one pointer line to the schema's home, not an inlined copy.
- **Plugin/tool dependencies are declared-or-absent:** repo files may require external
  plugins/tools only if the repo declares them installable (with a native fallback stated);
  operator-local tooling is never assumed.

### Phase 4 — Audit (verdicts only — no migrations)

Parallel audit lenses, each producing verdict files (in Phase-3 schema-legal terms):
- **Entry-file residency:** per line/section — does this earn always-on residency? Evictions
  route down a ladder, each with a **named landing artifact**: deterministic check → hook;
  subtree truth → scoped rule/subtree entry file; judgment lore → the Phase 6 lessons skill;
  duplicated content → the reference file that owns it (SYNC THE TARGET FIRST — evicting
  into a stale home converts drift into data loss); true always-on context → stays. Report
  the projected line delta.
- **Skills/commands/config species:** per item — correct invocation species, undeclared or
  dangling dependencies, oversize bodies, deprecated zombies (a deprecation banner without a
  dated retirement plan is itself drift; tombstones must not stay invocable), dual-home twins
  (mark explicitly whether a twin mirrors by design or has diverged), stale provenance vs actual liveness
  (liveness = who invokes it today, not whether its citations resolve).
- **Wiring:** hooks/settings semantics (env-var placement, matcher syntax, double
  registrations where only one disable key governs), CI liveness per the evidence rules,
  orphaned scripts, duplicate charters.
- **Design-doc corpus liveness** (over Phase 0's active class only): per doc —
  *status-vs-reality drift* (an accepted decision whose subject was deleted; a draft
  untouched while its feature shipped; a body still saying "Open" under a RESOLVED heading);
  *reference integrity* (dangling supersession chains, unresolvable depends-on targets,
  active docs citing archived material as authority); *duplicate or conflicting decisions*
  (two records claiming the same territory; sibling specs covering identical scope where one
  was executed and the other never materialized); *orphans* (no inbound references, nothing
  they govern exists). Typed dispositions mirror the orphan sweep: `current` ·
  `update-in-place` · `mark-superseded` (with pointer) · `archive` · `merge` — each item that
  moves or changes status with a referrer-repair map.
Reconcile cross-lens verdict conflicts NOW, at manifest-compile time — not at execution.

### Phase 5 — Execute (work packages, one commit each)

Land the ratified manifests and verdicts in dependency order (typically: file moves →
settings/CI → migrations/archival → metadata sweeps → entry-file rewrite last, after its
eviction targets exist). Amend earlier manifests visibly (strikethrough + correction note)
when execution disproves them — never silently rewrite a ratified table. Re-run the Phase-3
check after every package. Corpus dispositions execute here too, with a hard split between
mechanical and authorial: supersession markers set; archives moved under the repo's archive
convention — never deleted; establish the convention if none exists, recorded in the
calibration log; merges executed mechanically only (verbatim consolidation + a pointer left
at the absorbed doc's id). Where the RATIFIED grammar is scribe's canonical docs/ map, the
corpus-relocation packages may delegate to `/docs-alignment` (scribe, where installed) — the
grammar decision stays here; only the mechanical migration is delegated, and the campaign commits the staged result as that work package's commit (docs-alignment itself never commits, by design). **`update-in-place` items are NOT executed in-campaign** — content
revision is authoring, so they route to Phase 6's follow-up work queue addressed to the
repo's own authoring process; only their mechanical residue (metadata, broken references) is
fixed here. Extend the check script with a **corpus tier**: no dangling supersession chains,
no archive citations in active docs, status vocabulary schema-legal. Finish by **promoting**
the hygiene tier to gating and wiring the check into CI.

### Phase 6 — Distill (GATED: separate pass)

Runs only after (a) findings ratified, (b) execution landed or explicitly deferred, (c) the
calibration log reviewed by the human. Mint ONE repo-hygiene **knowledge** skill in the repo
from: the calibration log, the audit lore that fit no hook or rule, and the repo's now-true
shape. Hard boundary: judgment and rationale in the skill; deterministic rules stay in the
checks — the skill cites them, never restates them. Default model-invocable knowledge
species; never pre-split. Validate with a fresh-context review (generator ≠ critic), fix its
findings, and close the campaign with the FINDINGS index complete and a **durable follow-up
work queue** (typed: mechanical / decisions / engineering / strategic) committed to the
repo's plan convention — chat and PR bodies are not tracking.

## Scoping smaller runs

`audit-only` = Phases 0 + 4, **plus Phase 3's survey steps read-only** (derive both the
harness-metadata contract and the design-doc grammar from observed practice, commit nothing)
so Phase 4's verdicts have schema-legal terms to be expressed in; where no contract is
derivable, Phase 4 judges against observed majority practice and flags the missing schema as
a finding. Nothing is executed — right
when the user wants findings before committing to change. A single-surface ask ("just fix CLAUDE.md") takes
that phase's method alone, but still gets a calibration log and the sync-target-first rule.

## When NOT to use

- A single mechanical fix (one stale path, one dead file) — just fix it.
- Layout-only docs reorganization to the canonical docs/ map, no harness drift → scribe's
  `/docs-alignment` alone.
- Application-code refactors, dependency upgrades, or test-suite work — this skill owns the
  agent-harness/context layer and the living design-doc corpus, not the code they describe.
- Authoring or substantively rewriting individual design docs — corpus verdicts here are
  liveness/placement dispositions; content revision routes to the repo's own authoring
  process.
- A repo with no harness surfaces yet — that's initialization, not an alignment campaign.
