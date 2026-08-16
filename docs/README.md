# docs — functional documents as interfaces

Sibling plugin to harness (the authoring toolchain; docs authors what flows through it).
Doctrine source of record: the corpus's Vol 3 (data plane). Designed by the make-plugin method;
shipped through the harness release gate.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/doc-writing-rules` | Declarative skill | model-only | Mutability classes, universal practices, the type contract table; `references/templates/` — ten authoring contracts (adr, prd, spec, lld, plan, roadmap, ticket, task, idr, rdd) |
| `skills/product-lifecycle-rules` | Knowledge pack | model-only | Realizes `product-lifecycle-bible.md` v1.1.0 (issue #320) as portable, this-repo-agnostic doctrine: the three nested loops, the seven-stage build loop, IDR/ADR/RDD alignment doc grammar, knowledge-base maturation, habits, anti-patterns. Now this workspace's canonical operating source for that doctrine (CLAUDE.md's sources-flow-outward invariant); `.claude/docs/spec/product-lifecycle-bible.md` is a dated snapshot pointing here. Fenced from `doc-writing-rules` (which type/sections/frontmatter here), `project-docs` (what this repo decided), and `check-stage` (this repo's live lifecycle-position reading — this pack is doctrine only) |
| `skills/check-stage` | Procedural (read-only report) | both (`/check-stage`) | Live lifecycle-position report (issue #336, `prd-lifecycle-stage-awareness.md`): which of the three loops is currently emphasized, the build-turn stage, and the version triple — a bundled census script (`lifecycle_census.py`) reads `.claude/docs/{adr,idr,rdd}/*.md` typed-record counts/status distributions/orphan-ADR density plus ROADMAP presence (mechanized), crossed with narrated judgment calls (POC-boundary crossed, loop emphasis, bug-vs-requirement-gap, Retro lessons landed) — every signal labeled mechanized or judgment, never a bare verdict. Modeled on and fenced against harness's `check-state` (work-state, not lifecycle-position); report-only v1, no ambient/write surface (deferred) |
| `skills/make-doc` | Procedural | both (`/make-doc`) | Type routing -> intent -> template draft -> language pass -> doc_lint clean |
| `skills/check-doc` | Procedural | both (`/check-doc`) | Mechanical pass first, then J1-J6 judgment; verdict-first report |
| `skills/file-bug` | Procedural (orchestrator) | both (`/file-bug`) | Capture -> classify -> record -> dispatch -> write-back: a bug-shaped TICKET (`kind: bug`) minted before any fork/agent starts, closing the loss window raw `/fork bug-name ...` left open |
| `skills/file-feature` | Procedural skill | both (`/file-feature`) | Feature intake, the file-bug mirror: find-intent → three-surface dedup → size (materiality floor) + shape (work → `kind: feature` ticket ± earned docs; knowledge → make-reference / harness's make-pack) → lint-clean record placed into existing ROADMAP/PLAN; never builds — `/build-feature` (orchestration) is the momentum half |
| `skills/file-task` | Procedural skill | both (`/file-task`) | The generic third sibling: any work item that is neither bug- nor feature-shaped (chore, follow-up, research item, debt) — shape-gate → dedup → `kind: task` record on the ruled backend (`task` label + optional size), plus the full resume surface: fold detail, dated Findings, status verbs (done/doing/wontfix) with the Findings-first close |
| `skills/file-leftovers` | Procedural skill | both (`/file-leftovers`) | The fourth sibling, batch intake from the CONVERSATION: sweeps the session for work mentioned but not advanced, presents one evidence-quoted candidate table (no verbatim quote → no candidate), one batched clarification round, then mints each approved row through its owning file-* sibling — minting is authorized only by per-run table approval, so a headless run delivers the table and mints nothing |
| `skills/lead-intake` | Command skill | user-only (`/lead-intake`) | Makes THIS session the standing intake seat: adopts `agents/intake-lead`'s contract directly (the `/lead-team` ↔ `team-lead` host-adoption pattern, docs' first instance) — every raw seed becomes a record via the four file-* procedures applied inline, with the one thing the agent structurally lacks: a live AskUserQuestion clarifying round. Intake-only held by stated discipline; ends when the session ends or the human stands the seat down |
| `skills/tidy-docs` | Command skill | user-only (`/tidy-docs`) | Migrate an existing repo's scattered docs to the canonical directory-per-type map: three-surface inventory (canonical dirs, near-miss locations, loose files/README extractions) → ONE batched plan approval → git mv + minimal frontmatter (doc-type/id/status) + basename-first link repair + doc_lint → project-docs index installed; prose never rewritten, never commits |
| `skills/research-methods` | Declarative skill | model-only | Six measured-investigation methods (autoresearch, ablation, bisect, adversarial, hill-climb, sweep); the Phase −1/0/1/2 spine + investigation rubric; the `experiment-runner` agent runs one method in isolation |
| `skills/make-rubric` | Procedural | both (`/make-rubric`) | Create · evaluate · improve · update a rubric against the bundled rubric-for-rubrics |
| `skills/markdown-to-markup` | Procedural | both (`/markdown-to-markup`) | Markdown source -> safe rendered markup (DOM); inline + block grammar, parsed via `textContent`, never `innerHTML` |
| `skills/html-to-markdown` | Procedural | both (`/html-to-markdown`) | HTML -> markdown source; semantic element map (headings, strong/em, code, links, lists), drops presentational markup |
| `skills/make-reference` | Procedural | both (`/make-reference`) | Author or review a referential knowledge doc (a skill's `references/` file, an @-imported doc, a Project Knowledge file) against its bundled rubric |
| `skills/make-llms-txt` | Procedural | both (`/make-llms-txt`) | Author or review an `llms.txt` (and `llms-full.txt`) to the standard shape |
| `skills/make-vision-memo` | Procedural | both (`/make-vision-memo`) | Author, or evaluate and improve, a vision memo (manifesto · reframe · case-for · synthesis); `doc-checker` grades the draft |
| `agents/experiment-runner` | Agent | dispatched | Runs ONE systematic investigation of a scorable system to a measured conclusion in its own context; preloads `research-methods` |
| `agents/intake-lead` | Agent | dispatched | The standing intake seat: mints durable records from raw seeds by applying the preloaded `file-bug`/`file-feature`/`file-task`/`file-leftovers` procedures inline — capture through record, then stop. Intake ONLY, structurally: its tool wall omits Agent and Skill, so it cannot dispatch builds or investigations (a bug record reports its resume command instead). Twin of the planned `/lead-intake` host-adoption command; lives HERE, not teamwork's lead family, because preloads cannot cross plugin boundaries |
| `agents/doc-checker` | Agent | dispatched | Fresh-context critic for one rubric-bearing document (PRD/SPEC/LLD/ADR/PLAN/ROADMAP/TICKET/TASK plus reference doc/llms.txt/vision memo/rubric/handoff block/decomposition manifest/DESIGN.md); preloads `check-doc` + `doc-writing-rules` — closes the gap left by `check-doc` having no fresh-context agent pairing |
| `scripts/doc_lint.py` | Script | CLI + selftest + write hook | T1-T5: frontmatter/type/status/sections/ID-spine; hook blocks edits to accepted ADRs (ledger class, enforced) |
| `hooks/hooks.json` | Hook | PostToolUse Write/Edit | Routes doc writes through doc_lint; silent on non-documents |

Folded in from the personal skill corpus per a `plan-plugin-split` partition decision: `measure`
(research-methods, make-rubric, the `experiment-runner` agent), `markdown-render` (markdown-to-markup,
html-to-markdown), and `knowledge-docs` (make-reference, make-llms-txt, make-vision-memo —
knowledge-pack authoring, originally `knowledge-forge` in this group, retired 2026-07-19 in favor
of harness's `make-pack`, the estate-wide factory-route name) — all small enough to fold into docs
rather than ship as standalone plugins.
Both ported agents soft-mention harness's `write-handoff` in body prose (not a preload — forge is a
sibling plugin) and fall back to a plain Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open
questions/Recommended next action block where harness isn't installed.

Rejected members (the design ledger): per-type skills x8 (cross-type asks are the majority — the
types form a pipeline; 8x listing budget for entangled "write the X" vocabulary); a separate
plan/roadmap family (same tests); a ninth BUG type (bugs are TICKET-shaped work items —
`kind: bug` plus five extra sections, no new template or validator needed); general rubric/report
types beyond bugs (Vol 3 covers them — flagged as the next wave, not built without demand).

Cross-plugin seams (soft, by design): docs uses the harness plugin's cross-cutting layer —
find-intent, break-down-problem, prompt-wording-rules, thinking-depth-rules — when installed, and
degrades to inline judgment when not. No hard edges cross the boundary.

Directories align with plugin names (ADR-0007).

v1.10.1 · 2026-08-16 · product-authoring cold-start + schema follow-up, binding addenda landed after v1.10.0 merged (#404): first-class cold-start branch (orient→harvest→draft→council→ratify, `product-forge` soft mentions); new BRIEF doc type (north-star living index); explicit PRP→RDD+PLAN/ROADMAP/TICKET mapping. Details in issue #404.
v1.10.0 · 2026-08-16 · fleet bootstrap seat 4 (#404): new standing product seat — `agents/product-leader-agent.md` (WHY/WHAT + loop authority, spec-lock gate, IDR/PRP + living indexes, escalation-rides-citations; fable+high, dated tier-deviation line) plus its host-adoption pairing `skills/product-authoring` (`lead-product`'s working name was unavailable under ADR-0011's new-name grammar). Details in issue #404.
v1.9.4 · 2026-08-16 · doctrine-audit D05 fix (closes #398, teamwork-side sibling): `agents/intake-lead.md`'s `disallowedTools` dropped the redundant, retired `Task` alias — `Agent` (already present) remains the sole block. A4 dispatch smoke test confirmed the wall still blocks `Agent` outright post-edit, recorded in issue #398. No behavior change.
v1.9.3 · 2026-08-16 · file-bug Phase 6 merged-state close criterion (#397): `done`/close now requires the fix ON MAIN — direct commit for a solo single-file fix, MERGED PR for campaign work, or an explicit deferral to the PR's own `Closes #` line; an unmerged fix leaves the record open with a dated Findings entry naming the PR. Closes the #380/#383 premature-close class (issue closed 13:41 on an unmerged branch, PR merged 15:01 — "landed in-tree" was ambiguous). Body-only edit, routing surface untouched, no evals.json change owed; fresh-context skill-checker pass per plugin-authoring.md.
v1.9.2 · 2026-08-16 · DE-standards adoption (#377): TICKET contract gains a required-at-close `## Rejected alternatives` section (ticket.md template + SKILL.md's type-contract note), same enforcement tier as the `## Findings` write-back convention — prior art PR #343's scope note, PR #347's no-split writeup. Two deliberate non-adoptions recorded (generator≠critic, ID-spine traceability — already stricter than the industry norm they'd import). No doc_lint.py T3 change — prose-tier, not a hard gate, matching Findings' own enforcement tier.
v1.9.1 · 2026-08-16 · checker-agent description diet (#357): doc-checker's description drops the shared fresh-isolated-context / maker-never-grades-own-document / gap-map boilerplate (collide.py's top cross-plugin *-checker collision baseline, 6 agents, 103.9-158.4); doctrine already lived in the body, strengthened with an explicit never-grades-own clause. collide.py re-run: ↔design-system-checker 158.4→78.3, ↔layout-checker 136.7→62.4, ↔flow-checker 92.7→58.9. Batched fresh-context critic pass (6 files) clean; no evals.json changes owed. Siblings in design/screens/teamwork trimmed same PR.
v1.9.0 · 2026-08-15 · overhaul W2-D (Issue #351): `file-bug`/`file-feature`/`file-task`'s restated ~330-char backend-seam paragraph (Jaccard 0.54–0.75, authorkit bloat-audit's own worked example) collapsed to a one-line pointer at `doc-writing-rules/references/backend-resolver.md`, already the canonical definition of the three options/ruling shape/fallback — behavior unchanged, only the retelling moved
v1.8.0 · 2026-08-16 · `check-stage` (Issue #336): read-only lifecycle-position report skill + `lifecycle_census.py` + evals; three `product-lifecycle-rules` forward-fences repointed (closes #321); `harness:check-state` gains the reciprocal disambiguation (harness 3.8.9)
v1.7.0 · 2026-08-16 · RDD doc type (Issue #332, `prd-rdd-framework.md`): doc_lint TYPES gains `rdd` (draft/locked/superseded, Scope/Acceptance/Sequencing/Completion), T4's ledger-lock guard generalized a third time (locked-RDD), new T7 FAIL (locked-or-beyond RDD missing `decision-refs:`/`dri:`), `references/templates/rdd.md`, doc-writing-rules/make-doc/project-docs gain the RDD row; `decision-watcher`'s RDD-escalation extension stays deferred until enough RDDs exist
v1.6.0 · 2026-08-16 · `product-lifecycle-rules` knowledge pack (Issue #320): realizes `product-lifecycle-bible.md` v1.1.0 as a portable, this-repo-agnostic pack (three loops, seven-stage build loop, IDR/ADR/RDD alignment doc grammar, knowledge-base habits, anti-patterns) — now this workspace's canonical operating source for that doctrine (the bible file demoted to a dated snapshot, v1.2.0); reciprocal routing fences added to `doc-writing-rules` (evals + description) and `project-docs` (SKILL.md consult table + description + its first-ever evals suite)
v1.5.0 · 2026-08-16 · IDR doc type (Issue #316, `prd-idr-framework.md`): doc_lint TYPES gains `idr` (draft/locked/superseded, Claim/Why/Proof), T4's ledger-lock guard generalized to cover both accepted-ADR and locked-IDR, new T6 WARN (orphan-ADR — no `intent-refs:` citation), `references/templates/idr.md`, doc-writing-rules' type/mutability tables gain the IDR row, make-doc routes `idr`; bootstrap auto-mint (cross-plugin, harness's `/make-plugin`) and the ADR 0001-0013 `intent-refs:` retrofit stay deferred follow-ups
v1.4.9 · 2026-08-16 · checker retier (Kim's ruling): 1 *-checker agent move effort high→medium, model fable unchanged — review quality held at medium across the 2026-08-15/16 rounds while inherited-xhigh runs added cost, not findings
v1.4.8 · 2026-08-15 · make-reference gains the save-lessons fence (NOT whether a fact EARNS an entry — save-lessons judges the bar, this skill writes the doc) + reciprocal eval n12, and a W8 description diet back under the 700-char budget (triggers preserved verbatim); twin found by authorkit attention-audit's first live run (PR #275)
v1.4.7 · 2026-08-13 · footer ledger regenerated to one line per version (issue #203) — governed by harness's plugin-writing-rules cap; no docs-side contract change
v1.4.6 · 2026-08-13 · `file-bug` Phase 5 gains a verified teardown clause (issue #190, tracked from gen-ui-kit#1151)
v1.4.5 · 2026-08-12 · `references/backend-resolver.md`'s `claim` operation row gains its first real caller (teamwork's `dispatch-ticket` Phase 3, issue #183/#184)
v1.4.4 · 2026-08-11 · two checker-prescribed fixes from the first /check-everything estate audit — intake-lead's team-lead-sender rule restored, file-bug's fix-inline branch gains the three-strikes checker-pass contract
v1.4.3 · 2026-08-10 · intake-lead's standing-mode contract written into the body (issue #167) — the description already advertised a long-lived sibling seat the body never defined; no behavior changed
v1.4.2 · 2026-08-10 · the intent record evicted from agents/ entirely
v1.4.1 · 2026-08-10 · intake-lead's forge intent record relocated to `agents/intents/`
v1.4.0 · 2026-08-10 · /lead-intake
v1.3.1 · 2026-08-10 · intake-lead A4 smoke findings applied — Skill tool now hard-blocked via disallowedTools, fork-from-agent confirmed to run in the BACKGROUND and route completion to the ROOT session
v1.3.0 · 2026-08-10 · new agent `intake-lead`
v1.2.1 · 2026-08-10 · ADR-0010 rename sweep
v1.2.0 · 2026-08-09 · file-bug/file-feature/file-task run forked (`context: fork`) by default
v1.1.0 · 2026-07-30 · file-leftovers
v1.0.9 · 2026-07-30 · ADR-0009 find-intent-rename sweep
v1.0.8 · 2026-07-25 · description diet (PR #92)
v1.0.7 · 2026-07-25 · retired the stale ADR-0006 transition-table section
v1.0.6 · 2026-07-22 · the #79 description diet
v1.0.5 · 2026-07-21 · #84 remainder fix
v1.0.4 · 2026-07-21 · ADR-0008 design-merge sweep
v1.0.3 · 2026-07-21 · ADR-0007 dir alignment
v1.0.2 · 2026-07-21 · make-llms-txt's best-practices.md symlink repointed (reference-forge → make-reference; the docs rename stranded it — symlink targets are invisible to text sweeps, macOS glob masked it locally, Linux CI crashed).
v1.0.1 · 2026-07-21 · ADR-0006 harness-rename sweep
v1.0.0 · 2026-07-21 · ADR-0006 rename PR 8/9
v0.22.4 · 2026-07-21 · ADR-0006 teamwork-rename sweep
v0.22.3 · 2026-07-21 · ADR-0006 screens-rename sweep
v0.22.2 · 2026-07-21 · ADR-0006 design-kits-rename sweep
v0.22.1 · 2026-07-21 · ADR-0006 color-rename sweep
v0.22.0 · 2026-07-19 · `knowledge-forge` retired
v0.21.0 · 2026-07-19 · ADR-0004 dual-write, corrected
v0.20.0 · 2026-07-19 · ADR-0005 ticket-claim protocol
v0.19.0 · 2026-07-19 · ADR-0004 dual-write, implemented (Issue #44)
v0.18.1 · 2026-07-18 · `research-methods` gains a reciprocal NOT-for fence against forge's `reasoning-orders`
v0.18.0 · 2026-07-18 · README artifact-table species sweep
v0.17.0 · 2026-07-18 · `doc-forge` converted from Command to Procedural species (`disable-model-invocation: true` → `false`), mirroring `skill-forge`'s own 2026-07-14 conversion
v0.16.0 · 2026-07-18 · the ADR-0003 Linear adapter (Issue #34)
v0.15.0 · 2026-07-17 · `.github/ISSUE_TEMPLATE/{task,bug,feature}.yml` (Issue #25)
v0.14.0 · 2026-07-16 · /issue
v0.13.2 · 2026-07-15 · /docs-alignment gains .gitignore discipline (ruled 2026-07-15)
v0.13.1 · 2026-07-15 · subfolder conformance (ruled 2026-07-15) — research-methods' examples/ folded into references/, consult-table row repaired
v0.13.0 · 2026-07-15 · the git-native work-item backend (closes the estate's Issue #1, per ADR-0002): /bug-report and /feature gain a Phase-0 backend seam
v0.12.0 · 2026-07-15 · doc_lint T4 made git-aware (ADR-0002's own authoring exposed the false-positive class same-day): the ledger protection now guards COMMITTED history
v0.11.1 · 2026-07-14 · displayName 'Scribe' added to the manifest
v0.11.0 · 2026-07-13 · doc-authoring-standards' location-and-naming rule gains repo-rootedness (ruled 2026-07-13)
v0.10.0 · 2026-07-12 · seat-ladder realignment (forge 1.22.0): doc-reviewer opus→fable+high, researcher opus→fable+high (review/hard-bug-analysis row — root-causing a resistant defect is the row's charter)
v0.9.0 · 2026-07-12 · BREAKING — docs-align renamed docs-alignment hours after 0.8.0, all seven references repaired same-change, reciprocal repo-alignment fence added
v0.8.0 · 2026-07-12 · /docs-align (renamed docs-alignment at 0.9.0)
v0.7.0 · 2026-07-12 · /feature Phase 6
v0.6.1 · 2026-07-10 · author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder)
v0.6.0 · 2026-07-09 · /feature
v0.5.1 · 2026-07-09 · hygiene pass
v0.5.0 · 2026-07-09 · BREAKING (ADR-0001) — *-author renamed *-forge estate-wide (rubric/reference/knowledge/llms-txt/vision-memo), old handles fail visibly, no alias
v0.4.2 · 2026-07-09 · vision-memo-forge narrowed from 'evaluate and improve' to 'improve' with an explicit doc-review fence; doc-review's suite gains the reciprocal trigger
v0.4.1 · 2026-07-09 · agent fallback blocks 'Tests run'→'Tests/checks run' (harness-audit finding: the inline fallback failed forge handoff_check's H1 gate as written)
v0.4.0 · 2026-07-07 · bug-report's dispatch phase runs under orchestration's loop-design /goal recipe where installed (a dated Findings entry as the verifiable end-state, 5-try cap) instead of an open-ended fork
v0.3.0 · 2026-07-07 · measure/markdown-render/knowledge-docs folded in per a plugin-decompose partition; doc-reviewer agent closes scribe's generator≠critic gap
v0.2.0 · 2026-07-07 · bug-report orchestrator + TICKET `kind: bug` convention (Repro/Expected-vs-actual/Classification/Severity/Findings)
v0.1.0 · 2026-07-07 · initial: standards + forge + review + doc_lint + 8 templates + write hook
