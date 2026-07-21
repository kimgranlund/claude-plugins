# Session handoff — 2026-07-17 — ticketing backend generalization + ops agents

For the next agent/session opening this repo. Contract: forge's `handoff-compose`.

- **Status** — partial (uncommitted on `main`; scheduling routines unverified)

- **Summary** — Ratified ADR-0003 (generalizes ADR-0002's binary file/git-native backend seam into
  a 3-way choice — local / git-native / external-with-Linear-shipped — behind one shared resolver),
  authored two SPECs off it (`spec-ticketing-watch-triage`, `spec-linear-adapter`) and three
  versioned `system-decompose` manifests, built a new grounded knowledge pack
  (`forge:github-issue-pr-primitives`, real dated web research, forge bumped 1.31.0→1.33.0), and
  authored two new standing agents (`ops-issues`, `ops-repo`) implementing the SPECs — each passed
  independent fresh-context review (doc-reviewer ×3, skill-auditor, linguistics-reviewer,
  agent-reviewer ×2) with real findings caught and fixed, not rubber-stamped. Wired scheduling
  last: `ops-issues` as an hourly cloud routine, `ops-repo` as a session-scoped local cron.

- **Files changed** —
  New: `.claude/docs/adr/0003-backend-generalization.md` (status: `accepted`, ratified —
  ledger-class, append-only from here) · `.claude/docs/spec/spec-ticketing-watch-triage.md`
  (status: `draft`) · `.claude/docs/spec/spec-linear-adapter.md` (status: `draft`) ·
  `.claude/docs/decompositions/ticketing-backend-watch-manifest-v1.json`, `-v2.json`, `-v3.json`
  (v3 current; v1/v2 kept per the versioned-manifest rule) ·
  `forge 1.14.0/skills/github-issue-pr-primitives/` — `SKILL.md`, eight `references/*.md` files,
  `evals/evals.json` · `forge 1.14.0/agents/ops-issues.md` · `forge 1.14.0/agents/ops-repo.md` ·
  `.claude/docs/handoff/2026-07-17-ticketing-backend-and-ops-agents.md` (this file).
  Modified: `forge 1.14.0/.claude-plugin/plugin.json` (1.31.0→1.33.0) · `forge 1.14.0/README.md`
  (map rows + two ledger entries) · `forge 1.14.0/MANUAL.md` (new entries) ·
  `forge 1.14.0/scripts/release_gate.py` (G8 allow-set: `lifecycle-and-review`, `sub-issue` —
  verified false-positives).
  NOT mine, pre-existing on entry to this session: `design-systems 0.1.0/*` (5 files),
  `orchestration 0.1.0/skills/{loop-rules,team-or-solo-rules}/evals/evals.json`,
  `orchestration 0.1.0/skills/parallel-work-rules/`,
  `forge 1.14.0/skills/{agent-authoring-standards,entry-file-standards,hook-authoring-standards}/evals/evals.json`
  — `git status` shows these alongside mine; do not attribute them to this handoff.

- **Tests/checks run** —
  `python3 "forge 1.14.0/scripts/release_gate.py" "forge 1.14.0"` → pass, CLEAN 0 fail/0 warn (last
  run, after all fixes below). `coverage_check.py` on manifest v3 `--strict` → pass, clean (21
  nodes · 20 actions · 34 hosts · 12 edges). `doc_lint.py` on ADR-0003 + both SPECs → pass, clean
  ×3. `agent_corpus_index.py selftest` → ran mid-session (caught the preload bug below); folded
  into the clean release_gate pass above, not re-run standalone after. Independent reviews (all
  dispatched, all findings applied, none skipped): `doc-reviewer` ×3, `skill-auditor` +
  `linguistics-reviewer` on the knowledge pack, `agent-reviewer` ×2 on the two agents — pass, all
  fixed. `RemoteTrigger action:"run"` smoke test on the `ops-issues` cloud routine → UNMEASURED,
  fired but no tool here can read the cloud session's result.

- **Evidence** — ADR-0003 frontmatter: `status: accepted`,
  `ratified: 2026-07-17 (maintainer, in-session AskUserQuestion — two rulings, one session; a
  post-ratification doc-review pass then fixed wording/factual errors only...)`. The
  `agent_corpus_index.py` reverse-control caught a real bug: `ops-issues.md`'s first draft
  preloaded scribe's `doc-authoring-standards` in `skills:` — a hard cross-plugin preload
  violation (this workspace's own invariant: preloads are plugin-hard, mentions are plugin-soft);
  fixed by dropping the preload and stating the needed TICKET shape inline (`ops-issues.md`,
  Scope section). `ops-repo.md`'s first draft claimed `campaign_close.py` "discards the worktree" —
  read the script directly (`campaign_close.py:78-110`): it verifies `MERGED`, deletes the remote
  branch only, reverifies; never touches a worktree. Rewrote the agent's execution scope to match
  (only verified-remote-branch-delete and interactive-only dirty-`main` quarantine execute
  directly; worktree/local-branch cleanup is always propose-only now). The knowledge-pack review
  caught two arithmetic errors (Issue Fields GA 2026-07-02, access 2026-07-17 = 15 days, two files
  said "four") and an unfulfillable citation contract — both fixed. Cloud routine:
  `trig_01A2xZtAR9fwZQag4aqDFDaV` (hourly `:07`,
  https://claude.ai/code/routines/trig_01A2xZtAR9fwZQag4aqDFDaV). Local cron: job `12028929`
  (every 3 hours at `:13`, session-scoped).

- **Risks** — (1) The entire change set is uncommitted, directly on `main`, at
  multi-file/multi-session scale — ADR-0002's own doctrine names branch+worktree+PR as the default
  at this size; flagging for a maintainer call, locus: execution/process. (2) `ops-issues`'
  hourly cloud routine's first run is unverified — needs `gh` authenticated inside an isolated
  cloud sandbox, untested whether it is; locus: execution. (3) `ops-repo`'s cron dies with this
  session by definition — not a standing capability yet despite the agent file being
  production-ready; locus: plan. (4) `spec-linear-adapter.md` is a SPEC only, no adapter code
  exists yet — `ops-issues` correctly scopes to `gh`-only today, but don't assume Linear intake is
  live. (5) Several `[drift-prone]` markers in the new pack name very recent GitHub features
  (Issue Fields GA'd 15 days before research) — cheap to go stale, re-verify before trusting much
  past this quarter.

- **Open questions** — (1) Commit this directly to `main`, or stage as a campaign
  (branch+worktree+PR) per ADR-0002's own threshold? Nothing has been committed. (2) Is the
  `ops-issues` cloud routine actually working — check the routine link before trusting the hourly
  schedule; if `gh` isn't authenticated there it needs a different environment. (3) Re-arm
  `ops-repo` as a durable OS-crontab entry now that its session-scoped cron is about to disappear
  with this session close?

- **Recommended next action** — Maintainer (Kim) reviews `git status`/`git diff` for the full
  change set, decides commit-direct-vs-campaign, and checks the `ops-issues` routine's first-run
  result — stand by to commit, open the PR, or re-arm the cron once decided; none of the three open
  questions has a default that should be picked silently.
