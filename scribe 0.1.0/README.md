# scribe — functional documents as interfaces

Sibling plugin to forge (which authors the harness; scribe authors what flows through it).
Doctrine source of record: the corpus's Vol 3 (data plane). Designed by the plugin-forge method;
shipped through the forge release gate.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/doc-authoring-standards` | Declarative skill | model-only | Mutability classes, universal practices, the type contract table; `references/templates/` — eight authoring contracts (adr, prd, spec, lld, plan, roadmap, ticket, task) |
| `skills/doc-forge` | Command | user-only (`/doc-forge`) | Type routing -> intent -> template draft -> language pass -> doc_lint clean |
| `skills/doc-review` | Procedural | both (`/doc-review`) | Mechanical pass first, then J1-J6 judgment; verdict-first report |
| `skills/bug-report` | Command (orchestrator) | user-only (`/bug-report`) | Capture -> classify -> record -> dispatch -> write-back: a bug-shaped TICKET (`kind: bug`) minted before any fork/agent starts, closing the loss window raw `/fork bug-name ...` left open |
| `skills/research-methods` | Declarative skill | model-only | Six measured-investigation methods (autoresearch, ablation, bisect, adversarial, hill-climb, sweep); the Phase −1/0/1/2 spine + investigation rubric; the `researcher` agent runs one method in isolation |
| `skills/rubric-author` | Procedural | both (`/rubric-author`) | Create · evaluate · improve · update a rubric against the bundled rubric-for-rubrics |
| `skills/markdown-to-markup` | Procedural | both (`/markdown-to-markup`) | Markdown source -> safe rendered markup (DOM); inline + block grammar, parsed via `textContent`, never `innerHTML` |
| `skills/html-to-markdown` | Procedural | both (`/html-to-markdown`) | HTML -> markdown source; semantic element map (headings, strong/em, code, links, lists), drops presentational markup |
| `skills/reference-author` | Procedural | both (`/reference-author`) | Author or review a referential knowledge doc (a skill's `references/` file, an @-imported doc, a Project Knowledge file) against its bundled rubric |
| `skills/knowledge-author` | Procedural | both (`/knowledge-author`) | Mint a knowledge pack: axis decomposition, grounded research waves, the INDEX + consult-table entry surface |
| `skills/llms-txt-author` | Procedural | both (`/llms-txt-author`) | Author or review an `llms.txt` (and `llms-full.txt`) to the standard shape |
| `skills/vision-memo-author` | Procedural | both (`/vision-memo-author`) | Author, or evaluate and improve, a vision memo (manifesto · reframe · case-for · synthesis); `doc-reviewer` grades the draft |
| `agents/researcher` | Agent | dispatched | Runs ONE systematic investigation of a scorable system to a measured conclusion in its own context; preloads `research-methods` |
| `agents/doc-reviewer` | Agent | dispatched | Fresh-context critic for one rubric-bearing document (PRD/SPEC/LLD/ADR/PLAN/ROADMAP/TICKET/TASK plus reference doc/llms.txt/vision memo/rubric/handoff block/decomposition manifest/DESIGN.md); preloads `doc-review` + `doc-authoring-standards` — closes the gap left by `doc-review` having no fresh-context agent pairing |
| `scripts/doc_lint.py` | Script | CLI + selftest + write hook | T1-T5: frontmatter/type/status/sections/ID-spine; hook blocks edits to accepted ADRs (ledger class, enforced) |
| `hooks/hooks.json` | Hook | PostToolUse Write/Edit | Routes doc writes through doc_lint; silent on non-documents |

Folded in from the personal skill corpus per a `plugin-decompose` partition decision: `measure`
(research-methods, rubric-author, the `researcher` agent), `markdown-render` (markdown-to-markup,
html-to-markdown), and `knowledge-docs` (reference-author, knowledge-author, llms-txt-author,
vision-memo-author) — all small enough to fold into scribe rather than ship as standalone plugins.
Both ported agents soft-mention forge's `handoff-compose` in body prose (not a preload — forge is a
sibling plugin) and fall back to a plain Status/Summary/Files changed/Tests run/Evidence/Risks/Open
questions/Recommended next action block where forge isn't installed.

Rejected members (the design ledger): per-type skills x8 (cross-type asks are the majority — the
types form a pipeline; 8x listing budget for entangled "write the X" vocabulary); a separate
plan/roadmap family (same tests); a ninth BUG type (bugs are TICKET-shaped work items —
`kind: bug` plus five extra sections, no new template or validator needed); general rubric/report
types beyond bugs (Vol 3 covers them — flagged as the next wave, not built without demand).

Cross-plugin seams (soft, by design): scribe uses the forge plugin's cross-cutting layer —
intent-extract, system-decompose, linguistic-techniques, reasoning-orders — when installed, and
degrades to inline judgment when not. No hard edges cross the boundary.

v0.4.0 · assembled 2026-07-07 · 0.4.0: bug-report's dispatch phase runs under orchestration's loop-design /goal recipe where installed (a dated Findings entry as the verifiable end-state, 5-try cap) instead of an open-ended fork · 0.3.0: measure (research-methods, rubric-author, researcher agent), markdown-render (markdown-to-markup, html-to-markdown), and knowledge-docs (reference-author, knowledge-author, llms-txt-author, vision-memo-author) folded in per a plugin-decompose partition; doc-reviewer agent closes scribe's generator≠critic gap (doc-review had no fresh-context agent pairing, unlike forge's skill-review/skill-auditor) · 0.2.0: bug-report orchestrator + TICKET `kind: bug` convention (Repro/Expected-vs-actual/Classification/Severity/Findings) — closes the /fork bug-loss gap · 0.1.0: initial: standards + forge + review + doc_lint + 8 templates + write hook
