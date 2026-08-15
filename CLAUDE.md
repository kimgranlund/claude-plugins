# Plugin workspace — entry file

Each child directory here is one Claude Code plugin, named exactly its CURRENT plugin name —
no version suffix, no spaces (ADR-0007, 2026-07-21, superseding ADR-0006's frozen-dir rule:
dirs align with `.claude-plugin/plugin.json` names; a plugin rename renames its dir in the
same change). The version lives in the manifest and the README footer ledger, never in the
path. **harness is the toolchain**:
its commands and standards govern work on every plugin in this workspace, including harness itself.
Work on a plugin happens in its directory; decisions that span plugins happen here.

## Route the job before doing the job

| Job | Owner |
|---|---|
| New plugin from a domain | `/make-plugin` (never hand-scaffold) |
| Partition or merge existing plugins, gap analysis | `/plan-plugin-split` |
| New skill / agent / hook / entry-file work | `/make-skill` · `/make-agent` · `/make-hook` · `/check-entry-file` |
| A hand-run check or prose checklist that could be code | harness: `/make-script` (mechanize as `scripts/taskname.py\|mjs` + proven selftest) |
| Fill or grow a knowledge corpus | `/make-pack` (one axis per wave) |
| Split or merge a pack; execute the verdict | `/plan-skill-split` · `/plan-skill-merge` → `/reshape-skill` |
| Functional docs (ADR, PRD, SPEC, LLD, PLAN, ROADMAP, TICKET, TASK) | docs: `/make-doc` · `/check-doc` |
| A user reports a bug | docs: `/file-bug` — never raw `/fork` for bug work (it drops the report on exit). In THIS workspace the record lands as a GitHub Issue (ADR-0002); `/file-bug` and `/file-feature` detect this row natively |
| Scattered docs in an existing repo to organize into the canonical layout | docs: `/tidy-docs` (one approval gate, git mv, never rewrites prose) |
| A feature idea to capture, or a feature to build | docs: `/file-feature` (pure intake → sized ticket/doc/corpus) · teamwork: `/build-feature` (record-first build — runs the intake when no record exists) |
| Research methods, rubrics, knowledge/reference docs, llms.txt, vision memos, markdown↔markup | docs (folded in, not a separate plugin) — browse `docs/README.md`'s artifact table |
| A2UI or A2A knowledge — protocol / renderer / catalog / agent design / isolation proofs / training corpora | `agent-protocols` (the A2UI four + the A2A four) |
| Color science, palettes, typography systems, design-system exports (Claude Design/Figma Make/Google Stitch) + Material Design tokens | `design` |
| UI structure (layouts, flows, components, patterns), motion knowledge (durations/easing/reduced-motion), or non-functional verification (focus/i18n/perf/safety) | `screens` |
| Multi-agent feature-delivery team (plan → build → review → coordinate), composition/continuation design | `teamwork` |
| Routing proof after description edits | `/check-routing <plugin>` (plugin root, or a bare `.claude/skills` project estate — auto-detected, `--estate` to force) |
| Estate governance — naming grammar (ADR-0011), conformance audits, bloat audits, blast-radius-planned renames, exemption ratchet, manifest seeding, whole-estate overhauls | `authorkit` — `/naming-audit` · `/bloat-audit` · `/rename-planning` → `/rename-execute` · `/exemption-retire` · `/manifest-authoring` · `/overhaul-planning` → `/overhaul-execute` (the end-to-end driver) |
| Periodic health sweep | `/check-everything` (read-only; proposes) |
| Sweep the ops queue AND drive buildable tickets to an actual build | teamwork: `/mobilize-chores` (wraps harness's `/sweep-chores`, never reimplements it; `/sweep-chores` alone stays report-only). Gated by one batched confirm — or unattended via `/mobilize-chores auto` (2026-08-11: the explicit token, never inferred; ceiling PR-opened, with ADR-0012's one carve-out — a dispatch carrying the explicit `auto-merge: authorized` grant line AND clearing the full quick-build predicate may land merged; everything else still waits for a human, and nothing ever auto-reviews), the entry point a `/goal` loop calls to drain the queue overnight |
| Periodic ADR review — surface ratified Decisions worth a knowledge-pack entry, or stale citations of a superseded ADR | harness: `decision-watcher` agent (scheduled via `CronCreate` or on-demand) — checkpointed, never authors; queues candidates for one batched confirm, names the `/make-pack`/`/make-skill` command a human runs next |
| A drifted repo — duplicated instruction trees, stale corpus, dead automation: the committing campaign | harness: `/clean-repo` |
| A campaign (multi-file, multi-session, or parallel work) | branch + git worktree + PR (ADR-0002) — the PR is the merge gate; CI runs the release gates on it; solo single-file fixes may still commit to main. EnterWorktree worktrees live in-repo at `.claude/worktrees/` (gitignored); a change that retires a path a `.gitignore` rule names repairs the rule in the same change (rulings + history: ADR-0002, the git-native memory, harness's clean-repo razor). **Close it with `campaign_close.py <pr-number> --repo <owner/repo> --gate <plugin-root>...`** — verifies MERGED, deletes the remote branch and REVERIFIES it's gone (the ten-branch silent-delete-failure class, 2026-07-16), gates the touched plugins. **A dirty main before pulling parallel-session work: `sync_main.py`** — quarantines local dirt as a named stash, `--ff-only` pulls, reverifies HEAD by SHA (never trust a command's print alone) |
| Ship | `/ship-plugin <plugin>` — the only way anything ships |

## Common commands

No installed harness required; every check is a plain script. Run from the workspace root.

- **Prove a script's own counters:** `python3 harness/scripts/skill_lint.py selftest`
  (same pattern for `release_gate.py`, `eval_check.py`, `docs_check.py`, `corpus_check.py`, and
  `docs/scripts/doc_lint.py`).
- **Full pre-ship gate for a plugin:** `python3 harness/scripts/release_gate.py
  docs [--package]` — plugin-agnostic (works on harness or docs or any future plugin);
  runs manifest/structure checks, the full lint sweep, bundled selftests, a phantom-`[[handle]]`
  sweep, eval-suite validation, and docs-freshness (G10), in that order; `--package` additionally
  writes `<plugin>/dist/<name>-<version>.plugin`.
- **Lint one file by hand** (what the PostToolUse hook runs automatically on every `Write`/`Edit`):
  `python3 harness/scripts/skill_lint.py <path-to-SKILL.md-or-agent.md-or-hooks.json>`.
- Once a plugin is installed, prefer its slash commands over raw script calls inside a session:
  `/ship-plugin`, `/check-routing`, `/check-everything`. The commands above are for scripting, CI, or
  a plugin that isn't installed yet.

## Invariants (all plugins, no exceptions)

- **Ship only through the gate.** `release_gate.py <plugin-root> --package` (see Common commands
  above) is plugin-agnostic; artifacts land in `<plugin>/dist/`. Never hand-zip. Never re-ship a
  version — the version is the update cache key; bump every change and log it in that plugin's
  README footer ledger. `dist/` is gate output: read-only.
- **Incident → infrastructure, same day.** A load failure, false positive, or skipped step becomes
  a lint rule, gate check, or selftest fixture before the fix ships. Every `scripts/*.py|mjs|js`
  in every plugin carries a `selftest` mode and it stays green (anatomy, exit tri-state, and
  placement: harness's `script-writing-rules`; the gate's G4 sweeps all three extensions).
- **Descriptions are the routing surface.** Any model-invocable description edit updates its
  `evals/evals.json` in the same change, closes reciprocal fences in sibling suites, and gets an
  `/check-routing` after boundary changes.
- **A semantic edit rides with a critic.** A semantic edit to a prompt-carrying artifact (a
  SKILL.md body, an agent definition, a hook prompt) gets a fresh-context `*-checker` pass before
  its loop closes, whichever flow applied it — inline fix, unattended dispatch, or a host session.
  Lint and gates prove mechanics, not semantics (2026-08-11 audit: every recent unaudited semantic
  edit carried a real gap). The contract is encoded where those flows live — `file-bug`'s
  fix-inline branch, `dispatch-ticket`'s build path, `make-skill`'s P5. Pure code/config under the
  repo's own test gates is exempt.
- **Plugin boundaries are hard for preloads and `${CLAUDE_PLUGIN_ROOT}` paths, soft for mentions.**
  Cross-plugin handoffs are named mentions that degrade gracefully when the other plugin isn't
  installed; an agent preload or script path crossing plugins is a defect (plan-plugin-split's `surface_map.py check`
  kills it).
- **Naming:** for names shipped through 2026-08-13, the canon is harness's `naming-rules`
  (ADR-0006, 2026-07-21) — grandfathered verbatim, no rename campaign (ADR-0011 D8). For a
  NEW name, the canon is the harness artifact naming convention spec (ADR-0011, accepted
  2026-08-13): `.claude/docs/spec/spec-naming-convention.md`, checked by authorkit's
  naming-audit validator (`--scope grammar`); `naming-rules` carries the dated supersession
  note. Plugin names are
  distribution-scoped, disjoint from member domain prefixes (no `/ui:ui-review` stutter) — with
  the recorded term-of-art shelf exceptions: `llm` at plugin level (ADR-0006 Decision 7), and
  at member level a name containing the plugin word when it IS the term of art —
  `design:make-design-system`, `design:design-md-rules` (ADR-0008) — and
  never contain `claude` or `anthropic` anywhere in a skill name or directory — the install
  rejects it and the whole plugin fails to load.
- **Docs and ledgers:** functional documents follow docs' type contracts and mutability classes
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
absence is a finding: check it against the anti-matrix rule (plan-plugin-split; job evidence required) before
building anything new.
