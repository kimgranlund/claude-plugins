# Plugin workspace — entry file

Each child directory here is one Claude Code plugin, named `<name-and-version-at-creation>`
(e.g. `forge 1.14.0`, `scribe 0.1.0`) — quote the path, it contains a space. The dir name is
FROZEN at creation and drifts from the manifest by design (amended 2026-07-21, ADR-0006: the
rename campaign changes manifest NAMES too, so the dir records the name-and-version at creation;
the current name and version live in `.claude-plugin/plugin.json` and the README footer ledger,
never in the path). Dir → current-name aliases as renames land: `agentic-ui 0.1.0` →
`agent-protocols`. **forge is the toolchain**:
its commands and standards govern work on every plugin in this workspace, including forge itself.
Work on a plugin happens in its directory; decisions that span plugins happen here.

## Route the job before doing the job

| Job | Owner |
|---|---|
| New plugin from a domain | `/plugin-forge` (never hand-scaffold) |
| Partition or merge existing plugins, gap analysis | `/plugin-decompose` |
| New skill / agent / hook / entry-file work | `/skill-forge` · `/agent-forge` · `/hook-forge` · `/entry-file-audit` |
| A hand-run check or prose checklist that could be code | forge: `/script-forge` (mechanize as `scripts/taskname.py\|mjs` + proven selftest) |
| Fill or grow a knowledge corpus | `/pack-forge` (one axis per wave) |
| Split or merge a pack; execute the verdict | `/skill-decompose` · `/skill-synthesize` → `/skill-refactor` |
| Functional docs (ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK) | scribe: `/doc-forge` · `/doc-review` |
| A user reports a bug | scribe: `/bug-report` — never raw `/fork` for bug work (it drops the report on exit). In THIS workspace the record lands as a GitHub Issue (ADR-0002); `/bug-report` and `/feature` detect this row natively |
| Scattered docs in an existing repo to organize into the canonical layout | scribe: `/docs-alignment` (one approval gate, git mv, never rewrites prose) |
| A feature idea to capture, or a feature to build | scribe: `/feature` (pure intake → sized ticket/doc/corpus) · orchestration: `/build` (record-first build — runs the intake when no record exists) |
| Research methods, rubrics, knowledge/reference docs, llms.txt, vision memos, markdown↔markup | scribe (folded in, not a separate plugin) — browse `scribe 0.1.0/README.md`'s artifact table |
| A2UI or A2A knowledge — protocol / renderer / catalog / agent design / isolation proofs / training corpora | `agent-protocols` (the A2UI four + the A2A four) |
| Color science, palette design, contrast/CVD verification | `color` |
| Typography system design, pairing, tokens | `typography` |
| Design-system export bundles (Claude Design/Figma Make/Google Stitch) + Material Design tokens | `design-systems` |
| UI structure (layouts, flows, components, patterns), motion knowledge (durations/easing/reduced-motion), or non-functional verification (focus/i18n/perf/safety) | `ui` |
| Multi-agent feature-delivery team (plan → build → review → coordinate), composition/continuation design | `orchestration` |
| Routing proof after description edits | `/eval-run <plugin>` |
| Periodic health sweep | `/harness-audit` (read-only; proposes) |
| Periodic ADR review — surface ratified Decisions worth a knowledge-pack entry, or stale citations of a superseded ADR | forge: `ops-adr` agent (scheduled via `CronCreate` or on-demand) — checkpointed, never authors; queues candidates for one batched confirm, names the `/pack-forge`/`/skill-forge` command a human runs next |
| A drifted repo — duplicated instruction trees, stale corpus, dead automation: the committing campaign | forge: `/repo-alignment` |
| A campaign (multi-file, multi-session, or parallel work) | branch + git worktree + PR (ADR-0002) — the PR is the merge gate; CI runs the release gates on it; solo single-file fixes may still commit to main. EnterWorktree worktrees live in-repo at `.claude/worktrees/` (gitignored); a change that retires a path a `.gitignore` rule names repairs the rule in the same change (rulings + history: ADR-0002, the git-native memory, forge's repo-alignment razor). **Close it with `campaign_close.py <pr-number> --repo <owner/repo> --gate <plugin-root>...`** — verifies MERGED, deletes the remote branch and REVERIFIES it's gone (the ten-branch silent-delete-failure class, 2026-07-16), gates the touched plugins. **A dirty main before pulling parallel-session work: `sync_main.py`** — quarantines local dirt as a named stash, `--ff-only` pulls, reverifies HEAD by SHA (never trust a command's print alone) |
| Ship | `/plugin-release <plugin>` — the only way anything ships |

## Common commands

No installed harness required; every check is a plain script. Run from the workspace root, and
quote plugin paths (the version suffix contains a space).

- **Prove a script's own counters:** `python3 "forge 1.14.0/scripts/skill_lint.py" selftest`
  (same pattern for `release_gate.py`, `eval_check.py`, `docs_check.py`, `corpus_check.py`, and
  `scribe 0.1.0/scripts/doc_lint.py`).
- **Full pre-ship gate for a plugin:** `python3 "forge 1.14.0/scripts/release_gate.py"
  "scribe 0.1.0" [--package]` — plugin-agnostic (works on forge or scribe or any future plugin);
  runs manifest/structure checks, the full lint sweep, bundled selftests, a phantom-`[[handle]]`
  sweep, eval-suite validation, and docs-freshness (G10), in that order; `--package` additionally
  writes `<plugin>/dist/<name>-<version>.plugin`.
- **Lint one file by hand** (what the PostToolUse hook runs automatically on every `Write`/`Edit`):
  `python3 "forge 1.14.0/scripts/skill_lint.py" <path-to-SKILL.md-or-agent.md-or-hooks.json>`.
- Once a plugin is installed, prefer its slash commands over raw script calls inside a session:
  `/plugin-release`, `/eval-run`, `/harness-audit`. The commands above are for scripting, CI, or
  a plugin that isn't installed yet.

## Invariants (all plugins, no exceptions)

- **Ship only through the gate.** `release_gate.py <plugin-root> --package` (see Common commands
  above) is plugin-agnostic; artifacts land in `<plugin>/dist/`. Never hand-zip. Never re-ship a
  version — the version is the update cache key; bump every change and log it in that plugin's
  README footer ledger. `dist/` is gate output: read-only.
- **Incident → infrastructure, same day.** A load failure, false positive, or skipped step becomes
  a lint rule, gate check, or selftest fixture before the fix ships. Every `scripts/*.py|mjs|js`
  in every plugin carries a `selftest` mode and it stays green (anatomy, exit tri-state, and
  placement: forge's `script-authoring-standards`; the gate's G4 sweeps all three extensions).
- **Descriptions are the routing surface.** Any model-invocable description edit updates its
  `evals/evals.json` in the same change, closes reciprocal fences in sibling suites, and gets an
  `/eval-run` after boundary changes.
- **Plugin boundaries are hard for preloads and `${CLAUDE_PLUGIN_ROOT}` paths, soft for mentions.**
  Cross-plugin handoffs are named mentions that degrade gracefully when the other plugin isn't
  installed; an agent preload or script path crossing plugins is a defect (plugin-decompose's `surface_map.py check`
  kills it).
- **Naming:** the canon is forge's `naming-rules` (ADR-0006, 2026-07-21). Plugin names are
  distribution-scoped, disjoint from member domain prefixes (no `/ui:ui-review` stutter) — with
  the recorded term-of-art shelf exception for `color` and `llm` (ADR-0006 Decision 7) — and
  never contain `claude` or `anthropic` anywhere in a skill name or directory — the install
  rejects it and the whole plugin fails to load.
- **Docs and ledgers:** functional documents follow scribe's type contracts and mutability classes
  (the accepted-ADR append-only rule is hook-enforced — doc_lint T4; supersede, never edit).
  `.refactor-attic/` directories are the undo for non-git-reversible merges — never deleted
  casually. **Work items are GitHub Issues in this workspace (ADR-0002)** — decisions/contracts
  (ADR/PRD/SPEC/LLD) and README ledgers stay in-repo files; `docs/tickets/` is retired for new
  work items here.
- **CI mirrors the local gates (ADR-0002).** `.github/workflows/gate.yml` runs `release_gate.py`
  (G1–G11, incl. the ruff/eslint style tier — configs `ruff.toml`/`eslint.config.mjs` at this
  root) over every plugin on each push/PR — it executes the same plain scripts, no CI-only
  logic.
- **Sources of record flow outward.** Standards skills in the plugins are canonical; corpus
  snapshots and project-knowledge copies refresh *from* them at release boundaries, never the
  reverse. Falsified claims are amended in place with a dated note.

## When starting anything

Read the target plugin's own `CLAUDE.md` and README footer ledger first (per-plugin invariants and
version history live there, not here). If a task has no owner in the routing table above, that
absence is a finding: check it against the anti-matrix rule (plugin-decompose; job evidence required) before
building anything new.
