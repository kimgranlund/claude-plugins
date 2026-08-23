# Plugin workspace — entry file

Each child directory here is one Claude Code plugin, named exactly its current plugin name — no
version suffix, no spaces; a plugin rename renames its dir in the same change (ADR-0007). The
version lives in the manifest and the README footer ledger. **harness is the
toolchain**: its commands and standards govern work on every plugin here, including harness
itself. Work on a plugin happens in its directory; decisions that span plugins happen here.

## Route the job before doing the job

**Live lane first.** A LIVE human prompt — typed at this session, this turn — for bounded work
that fits one context executes solo inline, record-last, bug- or feature-shaped asks included (PR
labeled `live-lane`, auto-merge on green). Sizing tripwires + escalation: teamwork `fleet-rules`
§7 decides "small", never the executor. The rows below bind only what falls outside the lane.

Most asks route through a resident skill description — trust the menu. The rows below carry only
what the menu can't: workspace-scoped norms, command-only surfaces, and topology.

| Job | Owner |
|---|---|
| New plugin from a domain | `/make-plugin` — never hand-scaffold |
| A user reports a bug | docs: `/file-bug` — never raw `/fork` for bug work (it drops the report on exit) |
| Domain topology | docs = functional docs + research artifacts · `agent-protocols` = A2UI/A2A knowledge · `design` = color/type/design-system exports · `frontend` = UI structure/motion/verification · `teamwork` = multi-agent delivery · `authorkit` = estate governance (naming/bloat/renames/overhauls) · `brand-design` = brand strategy/identity/voice/stewardship, the adversarial critic council |
| Periodic health sweep | `/check-everything` (read-only; proposes) |
| Unattended queue drain | `/mobilize-chores auto` — the explicit token, never inferred; grants + the ADR-0012 auto-merge carve-out live in that skill's own body |
| A drifted repo campaign | harness: `/clean-repo` |
| A campaign (multi-file, multi-session, or parallel work) | branch + git worktree + PR (ADR-0002); solo single-file fixes may still commit to main. Close/sync mechanics: `.claude/rules/campaign-close.md` |
| Ship | `/ship-plugin <plugin>` — the only way anything ships |

## Common commands

No installed harness required; every check is a plain script. Run from the workspace root.

- **Prove a script's own counters:** `python3 harness/scripts/skill_lint.py selftest` (same
  pattern for `release_gate.py`, `eval_check.py`, `docs_check.py`, `corpus_check.py`,
  `docs/scripts/doc_lint.py`).
- **Full pre-ship gate for a plugin:** `python3 harness/scripts/release_gate.py <plugin>
  [--package]` — plugin-agnostic; manifest/structure, lint sweep, bundled selftests,
  phantom-`[[handle]]` sweep, eval validation, docs-freshness; `--package` writes
  `<plugin>/dist/<name>-<version>.plugin`.
- **Lint one file by hand** (hooks retired, #466 — nothing runs this automatically):
  `python3 harness/scripts/skill_lint.py <path>`.
- **Regenerate a plugin's harness overlays** (Codex + Hermes land; Pi lands W3):
  `python3 harness/scripts/harness_emit.py <plugin> [--harness codex,hermes] [--verify | --probe]` —
  writes `.codex-plugin/plugin.json`, per-skill `agents/openai.yaml`, `plugin.yaml`,
  `__init__.py`, `hermes-mcp.yaml` (where `.mcp.json` exists), and `HARNESS-NOTES.md` in-tree
  (committed, never `dist/`); `release_gate.py`'s G15 verifies freshness (`codex,hermes`), the
  writer runs in `/ship-plugin`'s own preflight (LLD-0025).
- Once a plugin is installed, prefer its slash commands over raw script calls in a session.

## Invariants (all plugins, no exceptions)

- **Ship only through the gate.** `release_gate.py <plugin-root> --package` is plugin-agnostic.
  Never re-ship a version — the version is the update cache key; bump every change and log it in
  that plugin's README footer ledger. `dist/` handling: `.claude/rules/dist-output.md`.
- **Incident → infrastructure, same day.** A load failure, false positive, or skipped step
  becomes a lint rule, gate check, or selftest fixture before the fix ships. Selftest
  requirements: `.claude/rules/scripts.md`.
- **Skill/agent/hook authoring invariants** — description-routing-surface, the semantic-edit
  critic gate, plugin-boundary hygiene: `.claude/rules/plugin-authoring.md`.
- **Naming.** A NEW name must never contain `claude` or `anthropic` anywhere in a skill name or
  directory — the install rejects it and the whole plugin fails to load. Grammar canon and
  grandfathering: `.claude/docs/spec/spec-naming-convention.md` (ADR-0011; authorkit's
  naming-audit checks it). Term-of-art shelf (plugin-level `llm`, member stutter): harness's
  `naming-rules`.
- **Work items are GitHub Issues in this workspace (ADR-0002)** — decisions/contracts
  (ADR/PRD/SPEC/LLD) and README ledgers stay in-repo files; `docs/tickets/` is retired for new
  work items here. Docs mutability, `.refactor-attic/`, and this workspace's docs-root override
  (everything under `.claude/docs/`): `.claude/rules/docs-mutability.md`.
- **CI mirrors the local gates (ADR-0002).** `.github/workflows/gate.yml` runs `release_gate.py`
  over every plugin on each push/PR — the same plain scripts, no CI-only logic; style configs
  `ruff.toml`/`eslint.config.mjs` at this root.
- **Sources of record flow outward.** Standards skills in the plugins are canonical; corpus
  snapshots refresh *from* them at release boundaries. Falsified claims are
  amended in place with a dated note.

## Path-scoped rules (`.claude/rules/`)

Nothing auto-loads these by path (#262). Each file states its own path scope up top; the
Invariants bullets above point to the one that applies — read it explicitly when its scope
matches your edit.

## When starting anything

Read the target plugin's own `CLAUDE.md` and README footer ledger first (per-plugin invariants
and version history live there, not here). If a task has no owner in a resident description or
the table above, that absence is a finding: check it against the anti-matrix rule
(plan-plugin-split; job evidence required) before building anything new.
