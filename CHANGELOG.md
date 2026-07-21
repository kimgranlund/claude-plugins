# Changelog

Repo-level milestones only. Each plugin's own `README.md` footer carries its full, dated version
ledger — this file exists to show how the nine plugins came to exist relative to each other, not
to duplicate their per-version detail.

## 2026-07-20 — naming-rules: the simple naming paradigm lands in forge (1.40.0)

A session that started as "why are our naming conventions so odd" produced a full-estate naming
review (9 plugins, ~130 members: one "check" concept spelled four ways, "make" spelled five,
`decompose` carrying two meanings, four skill↔agent name twins) and ended as `naming-rules` — a
knowledge skill encoding the deliberately simple paradigm: five checkable tests, per-kind name
shapes, a one-verb-per-concept registry. It governs NEW names only; the legacy grammar keeps
governing shipped names (names are APIs), and the estate rename map ships inside the skill as an
illustrative worked example, not a ratified campaign. Forged through skill-forge's six gates with
fresh-session baselines proving the delta and a fresh-context audit (PASS, 0 blocking).

## 2026-07-20 — ops-adr: a standing periodic ADR-review agent, and a GitHub MCP offer for ops-issues

Closes the ADR-side gap next to the ticketing-backend agents from 2026-07-17. `ops-adr` checkpoints
an ADR corpus by content hash (`scripts/adr_checkpoint.py`), judging only the new/amended/
newly-superseded delta against `knowledge-harvest`'s own bar — cost stays proportional to what
changed, never to corpus size — and queues candidates durably (`scripts/adr_queue.py`) so a
scheduled firing never blocks on a human. Structurally barred from authoring: a confirmed
candidate's next step is always a named `/pack-forge`/`/skill-forge`/`knowledge-harvest` command,
never a write this agent performs itself. Designed via a `system-decompose` PLAN-mode manifest
before either script was written; a fresh-context `agent-reviewer` pass caught a real crash-safety
gap pre-ship (the checkpoint would have advanced before judgment ran), fixed by splitting the
script into separate `classify`/`advance` calls. The same week, `ops-issues` gained REQ-013: a
one-time, interactive-only offer to declare a read-only-scoped GitHub MCP server on a GitHub-backed
repo's first interactive firing — the existing capture skills stay the sole write path for
issues/PRs by construction of the credential's own scope, not agent discipline. (`forge` 1.35.0 →
1.37.0)

## 2026-07-19 — Retire scribe:knowledge-forge, fold into forge:pack-forge

A `plugin-decompose` gap analysis (job-to-be-done test, run alongside two other candidate groupings
kept as no-partition) found scribe's `knowledge-forge` duplicated forge's `pack-forge` end to end
while shipping no mechanical corpus-integrity gate of its own — a scribe-only install got the
weaker, ungated authoring path by default. Retired the skill; its genuinely unique entry-surface
conventions (answers-only boundary, Grep-first consult discipline, deviation doctrine,
corpus-of-record rule) were authored fresh into forge's `skill-authoring-standards`, not merely
moved. Retiring the name meant repointing every knowledge-pack skill across all 8 downstream
plugins that named `knowledge-forge` as its own factory route — 81 files in the initial campaign.
Verified via a full `/eval-run` (255 cases, 13 scribe suites) that no sibling skill wrongly grabbed
the orphaned trigger vocabulary once the model-routable skill was deleted. Two independent
fresh-context reviews caught real gaps before and after merge (a missed version bump, a genuinely
lost Grep-first convention, an overclaimed "confirmed pre-existing" framing later corrected and
filed as Issue #58). (`forge` 1.34.14 → 1.35.0; `scribe` 0.21.0 → 0.22.0; six domain plugins
patch-bumped)

## 2026-07-18 — ADR-0004 and ADR-0005: native GitHub Issue Types, and a ticket-claim protocol

Two ADRs ratified the same week. **ADR-0004**: dual-write GitHub's native Issue Type alongside the
existing `kind:` label on every capture skill's mint call — found and fixed a real same-day bug
before it could ship a second time: a combined `gh issue create --type` call was proven (via a
leftover test issue) to create the issue and only then silently fail the type-attach step, making a
naive "retry without --type" fallback mint a duplicate; redesigned as two always-separate calls,
create then a separate edit, eliminating the risk structurally rather than patching around it.
**ADR-0005**: a `claim` backend operation — write identity, re-read to confirm it wasn't outraced —
preventing two independent parallel agents from starting the same ticket before a git-tree
collision even exists; cross-referenced into `orchestration`'s `concurrency-design` skill as the
layer beneath its own git-tree collision response. (`forge` 1.34.9 → 1.34.12; `scribe` 0.18.1 →
0.20.0; `orchestration` 0.7.4 → 0.7.5)

## 2026-07-17 — ADR-0003: a three-way work-item backend, and the Linear adapter realized

Generalizes scribe's bug-report/feature/issue capture skills beyond the single git-native
assumption ADR-0002 ruled for this workspace: a repo now resolves to Option A (local TICKET file,
unchanged default), Option B (git-native, `gh issue` — this workspace's own ruled instance), or
Option C (a named external adapter) behind one resolver seam, decided once per repo and never
re-asked per capture. The watch/triage/trust SPEC this ADR's Decision 1 anticipates
(`spec-ticketing-watch-triage.md`) followed the same wave as `ops-issues`/`ops-repo` — the estate's
first standing operational agents, scheduled via `CronCreate`, structurally barred from doing the
captured work themselves. Linear shipped as the first Option C adapter shortly after, proven live.
(`forge` 1.32.0 → 1.33.0; `scribe` 0.15.0 → 0.16.0)

## 2026-07-15 — ADR-0002: git-native execution — Issues, PRs, worktrees, CI, and the style-lint tier

Three maintainer rulings (in-session AskUserQuestion), one ADR, executed as the estate's **first
branch → PR**. (1) **Git-native max**: GitHub Issues become the work-item canon for this
workspace, PRs the merge gate, branch+worktree the campaign vehicle — motivated by three
concurrent-session working-tree collisions in one week; decisions/contracts/ledgers stay in-repo
files (no second canon), and adapting scribe's `/bug-report`//`/feature` to a git-native backend
is queued as Issue #1 rather than redesigned inline. (2) **Local + CI**: `.github/workflows/
gate.yml` runs the same plain gate scripts (G1–G11 across all nine plugins + the scripts' own
selftests) on every push/PR, closing the human-editor/parallel-session bypass of the in-session
hook. (3) **Style lint both ecosystems**: ruff + eslint join as gate **G11** (forge 1.26.0) with
dependency-free workspace-root configs; 13 real defects fixed estate-wide on arrival. The
campaign also refined scribe's T4 same-day (scribe 0.12.0): its own ADR's authoring exposed that
the ledger hook blocked legitimate ratification — T4 is now git-aware, guarding COMMITTED history
only.

## 2026-07-14 — Mechanization becomes a first-class capability; every plugin gets a display name

Two estate-wide changes landed the same day. **The mechanization pair** (`forge` 1.25.0):
`script-authoring-standards` (the deterministic tier's canon — selftest contract with a negative
control that bites, exit tri-state 0 pass / 1 fail / 2 dependency-skip, placement, the
arithmetic-not-judgment boundary) and `/script-forge` (qualify → plan → confirm → author →
validate), designed via a `system-decompose` manifest and proven by blind `/eval-run` (4 suites
clean after one symmetric intra-pair steal was fenced). Grounding the standard exposed and closed
a live gate hole the same day: `release_gate.py` G4 swept only `scripts/*.py`, so every `.mjs`
selftest in the estate shipped unrun — G4 now sweeps all three extensions and ratifies
`ui-probe.mjs`'s exit-2 SKIP convention house-wide. The workspace invariant and routing table
widened to match; the audits' A4 dimension now cites the standard as canon. **Naming hygiene**:
all nine plugins and their marketplace entries gained `displayName` (Title Case, `UI`/`LLM`
acronyms uppercased — the /plugin UI otherwise title-cases kebab names into "Ui"/"Llm"); verified
field semantics recorded in `plugin-authoring-standards`. Eight patch bumps;
`design-systems` separately reached 0.7.2 the same day (its own ledger: the Material re-sync
campaign, the new `material-design-token-semantics` glossary skill, and its 12-suite eval-run
proof).

## 2026-07-13 — `llm`: a ninth plugin, authored fresh via `system-decompose`

Unlike the six `plugin-decompose`-partitioned domain plugins, `llm` was greenfield-designed: ran
`forge`'s `system-decompose` (technical-architecture domain) against "everything learned about
Anthropic LLM gateways and JSONL streaming" while building `@agent-ui/a2ui`'s live-agent system,
producing a 2-node/21-action/0-unhosted manifest (`coverage_check.py` clean) before a line of
content was written. Two knowledge packs resulted — `llm-provider-gateway` (the swappable-provider
adapter seam, registry + trust boundary, dev-proxy, the bundler env-inlining footgun,
stateless-session/turn model) and `llm-jsonl-streaming` (SSE chunk-buffering technique, the
Anthropic SSE contract as a worked instance, validate-then-stream self-correction) — each grounded
in TWO kinds of sources (a platform/vendor fact, or the `@agent-ui/a2ui` implementation cited as a
worked example, never as sole authority), a deliberate posture split from `agentic-ui`'s own packs,
which document that repo's actual dated behavior. Independently reviewed (`skill-auditor` ×2,
`plugin-reviewer` ×1) before landing: fixed an intra-skill `[[cross-reference]]` convention error
(18 handles wrongly double-bracketed — that syntax is reserved for cross-*skill* links only), one
worked-instance citation that overclaimed its scope (`nextTurn` narrowed to the continuation-only
half it actually implements), two loose citation ranges tightened, both descriptions trimmed under
the 1024-char portability cap, and this file's + the top-level `README.md`'s stale plugin counts
corrected. (`llm` 0.1.0; marketplace + README updated to nine plugins/seven domain plugins)

## 2026-07-07 — Repo goes public

- `git init`, initial commit (913 files, all eight plugins), pushed to
  `github.com/kimgranlund/claude-plugins`.
- Added `.claude-plugin/marketplace.json` (`nonoun-plugins`), `README.md`, this file. Marketplace
  manifest validated clean via `claude plugin validate` and end-to-end tested (`marketplace add` →
  `install` → `claude plugin details` confirmed the correct component inventory → uninstalled the
  test install, since a permanent global install is the user's call, not this session's).

## 2026-07-07 — orchestration: fixed an inherited over-eager ADR mandate

`system-planner`'s charter (ported from the legacy corpus) mandated authoring a PRD+SPEC+LLD+ADR
bundle on every planning dispatch, regardless of whether any one of them was warranted — a
user-reported "painfully slow to build anything" symptom traced to this one instruction. Rewritten
as four independent routing decisions; ADR now defaults to **no** unless a genuine fork with real
rejected alternatives was resolved. (`orchestration` 0.3.0 → 0.4.0)

## 2026-07-07 — Closed the last two confirmed migration gaps

A rigorous coverage re-check (comparing every one of the legacy corpus's 61 skills + 19 agents
against what had actually been ported, rather than trusting the original plan) found two skills
(`agents-audit`, `skills-audit` — corpus-wide deep-review campaigns, ~74 files) and one agent
(`orchestration-reviewer`, which fell through the cracks between forge's reviewer batch and
orchestration's original member list) never migrated anywhere. Ported all three; restored the DEEP
review tier on `agent-reviewer` and `skill-auditor` (stripped earlier only because the audit skills
didn't exist yet); found and fixed a real parser bug along the way (`agent_corpus_index.py`
silently corrupted any multi-line `skills:` YAML list — forge's own house style — to a single
dangling entry). (`forge` 1.16.0 → 1.17.0, `orchestration` 0.2.0 → 0.3.0)

## 2026-07-07 — Loop doctrine and model tiering

Read through Anthropic's "Getting Started with Loops" guide and closed the gaps it surfaced: a
goal-conditions recipe table in `orchestration/loop-design` mapping this workspace's own gates to
verifiable `/goal` stop conditions; a proactive-intake worked example (`/schedule` + `/goal` +
`bug-report`); a model-tiering doctrine in `forge/agent-authoring-standards` (mechanical fan-out /
capable execution / adversarial judgment), applied concretely to `eval-judge` and
`pack-researcher`; pilot-slice guidance before a large fan-out in `harness-audit` and
`plugin-forge`; and `ui-change-verify` — a new skill that drives a UI change against the running
artifact instead of reasoning about it in the abstract. (`forge` 1.15.0 → 1.16.0, `scribe` 0.3.0 →
0.4.0, `ui` 0.2.0 → 0.2.1)

## 2026-07-07 — Six new plugins from a plugin-decompose partition

Ran `forge`'s own `plugin-decompose` skill against the legacy `~/.claude/skills` +
`~/.claude/agents` corpus (61 skills, 19 agents) to decide how the rest of it should partition.
Built the six resulting plugins — `agentic-ui`, `color`, `typography`, `design-systems`, `ui`,
`orchestration` — porting each cluster's content and converting every cross-plugin hard preload
(`skills:` frontmatter naming a skill in a different plugin, or a hardcoded script path) into a
soft mention with an inline fallback, the same pattern `scribe` already used for its own
dependency on `forge`. `forge` gained `handoff-compose` as a fourth cross-cutting layer (needed by
every agent across every plugin, so no single narrow home would have worked) plus four new
reviewer agents (`agent-`/`hook-`/`plugin-`/`linguistics-reviewer`) closing its own reviewer-agent
gap. Real bugs surfaced and fixed during the port: a reserved-word install-blocker
(`design-system-author-claude-code` → `-dscard`), six broken symlinks pointing at a sibling that
no longer existed post-partition, and several latent `corpus_check`/path bugs in ported content.
(`forge` 1.14.0 → 1.15.0; `scribe` 0.2.0 → 0.3.0; six plugins at 0.1.0)

## 2026-07-07 — bug-report: closing the /fork bug-loss gap

Added `bug-report` to `scribe`: captures a bug-shaped TICKET (`kind: bug`, with Repro/Expected vs
actual/Classification/Severity/Findings sections) *before* dispatching any investigation, so a
fork killed mid-investigation still leaves the report — and incremental findings — on disk. Root
workspace `CLAUDE.md` routes bug reports here explicitly, since it stayed a command (never
model-invoked) like every sibling `-forge`. (`scribe` 0.1.0 → 0.2.0)

## Earlier

`forge` (skill/agent/hook/entry-file/plugin authoring, `intent-extract`/`system-decompose`/
`linguistic-techniques` absorbed as its cross-cutting layer) and `scribe` (functional-document
authoring) predate this changelog.
