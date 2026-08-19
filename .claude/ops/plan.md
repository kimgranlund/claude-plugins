# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-19T22:20:00Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing**
(dispatch-named UNMEASURED list: empty). One sub-measurement unmeasured by the seats' own
content: the primary's ahead/behind count vs `origin/main` (repo-cleaner reports
`primary_checkout_check.py` → **clean, on `main`** but no behind-count this firing).

decision-watcher: 23 ADRs scanned (22 previously known) — **1 new: adr-0023** (fleet stays
canon over native `agent-teams`), judged harvest-worthy, queued as the only pending candidate;
placement resolved to `teamwork:fleet-rules` (origin/main grep clean for `agent-teams`);
batched confirm deferred (no live AskUserQuestion channel in the dispatch); also flagged, not
acted on: adr-0023's body still carries a stale `PROPOSED` blockquote under an
`status: accepted` frontmatter. Two payloads (`adr-queue.json`, `adr-checkpoint.json`).
issue-sorter: window 2026-08-19T18:59:21Z→21:38:34Z, 7 issues + 12 merged PRs (#750–#769
range), all trusted-author; 3 missing-severity repairs applied via `gh` API (#766, #760, #752
→ `minor`); 0 mints, 0 held, 0 needs-ruling, 0 roster changes. One payload
(`watch-checkpoint.json`).
repo-cleaner: executed `campaign_close.py 769` (PR #769 independently re-verified MERGED;
C1/C2/C4/C5 ok, C3 WARN spurious — wrong gate-root arg `.`); 6 merged worktrees + 10 merged
local branches proposed for reap (no host reap script — propose-only); fix-684 (this session's
own worktree) deferred: branch merged (PR #699) but **uncommitted dirt** on no open PR; stash
inventory finally measured — **2 stashes**, both `On main: sync_main quarantine`; no open PRs
at all; stale-claim clean (all 5 open issues zero-assignee). One payload (its report).

**Prior plan (2026-08-18T22:03Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(checkpoint continuity: intermediate firings advanced issue-sorter's checkpoint to
2026-08-19T18:59:21Z, and decision-watcher reads 22 previously known — the applied value; no
chore-planner rewrite landed between, so this file still carried the 08-18 stamp). Entry 2
(sync_main, 42 behind) — RESOLVED BY EVENTS as far as measured: primary reads clean on `main`;
behind-count unmeasured this firing — the persist half re-scopes as entry 2 below. Entry 3
(review/merge PR #678) — DONE BY EVENTS (repo-cleaner: zero open PRs; the 12-PR merge wave
landed this window). Entry 4 (stashes) — carried forward, NOW MEASURED (2 stashes) → entry 5.
Entry 5 (worktree reaps) — still open, grown five→six runnable (fix-667's PR #702 merged; the
deferred slot moves to fix-684) → entry 6. Entry 6 (branch deletes) — still open, grown
seven→ten → entry 6.

**Parked-issue check (#611):** no carried-forward entry id carries `backlog`/`roadmap` in this
firing's evidence — nothing dropped. #617 (the `backlog`-labeled fixture) appears only in
repo-cleaner's zero-assignee list, was never a plan entry, stays excluded per the parking rule.
issue-sorter's discovery already excluded both labels at read time.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline on their own entries: the
fix-684 reap (entry 6) is blocked by entry 4's dirt decision AND by this live session; the
`/make-pack` run in entry 3 is blocked by its own human confirm; entry 2 persists what entry 1
applies.

**needs-ruling lane:** empty — issue-sorter reports 0 ruling-shaped candidates, 0 held; no §3
reference owed.

**Sandbox hazard, named:** this sweep runs inside `.claude/worktrees/fix-684`, whose branch
(`fix-684-font-var-resolve`, PR #699) is already MERGED — any payload written to THIS
worktree's `.claude/ops/` path strands on a dead branch. Apply every fenced block at the
SHARED checkout: `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`. The sandbox wall
(cd/`-C` refusal toward the primary) was reconfirmed live by repo-cleaner this firing.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout, not this worktree)
- **Action:** write the fenced payloads verbatim: `.claude/ops/adr-queue.json` (decision-watcher
  — 1 pending candidate, adr-0023 harvest), `.claude/ops/adr-checkpoint.json` (23 ADRs,
  adr-0023 added at fdc9b07f), `.claude/ops/watch-checkpoint.json` (issue-sorter — checkpoint
  21:38:34Z, strictly newer than the applied 18:59:21Z),
  `.claude/ops/reports/2026-08-19T21-42-54Z-repo-cleaner.md`, plus this rewritten
  `.claude/ops/plan.md`. `friendlies.json`, `held-items.md`, `.mcp.json` explicitly unchanged
  — no blocks owed, none applied. Target the shared checkout
  `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...` — this worktree's branch is merged;
  a write here strands.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** all five fenced blocks present in this firing's reports (four seat payloads +
  this plan); narrated-but-absent audit below reads clean for all three seats.
- **Size:** ~2 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from a primary (non-worktree) session — the next scheduled firing starts blind until it lands
- **Action:** from a session actually checked into `/Users/kimba/Projects/nonoun/plugins`:
  stage exactly the paths entry 1 applied (never `git add -A`), read the status output, commit
  as a separate step (gate ≠ commit), push. Primary reads clean on `main`
  (`primary_checkout_check.py`); behind-count unmeasured this firing — if the push is refused,
  `sync_main.py` first, per the workspace campaign row. Whether the 18:59Z-era applied state
  ever reached the remote is unverified — this sitting settles both.
- **Owner:** Kim (the sandbox wall refuses primary-targeted git ops from this session —
  reconfirmed live this firing; never improvise around it).
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); repo-cleaner §Sandbox + §Other findings.
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 3. Confirm the adr-0023 harvest candidate, then run the named authoring command
- **Action:** one batched confirm on decision-watcher's single pending candidate (adr-0023 ·
  harvest — the fleet-vs-`agent-teams` substrate axis, not yet covered anywhere on
  origin/main). On confirm, run `/make-pack teamwork/skills/fleet-rules` with the wave charter
  the seat drafted (fleet-canon rationale, the two named re-evaluation triggers + the soft
  #673 cost recheck, the fleet-native write-gate follow-up). Blocked by its own confirm —
  never run by the seat or this planner.
- **Owner:** Kim (confirm + command).
- **Evidence:** decision-watcher §Judged/§Queued — impact detector fired, origin/main
  `git grep` clean for `agent-teams` across skills/references; `adr-queue.json` payload
  (applied in entry 1) carries the full candidate record.
- **Size:** ~2 min confirm; the pack wave itself ~1 h (hours-class, separate sitting).

### 4. Decide worktree fix-684's uncommitted dirt — rescue or discard
- **Action:** the worktree this sweep runs in carries uncommitted edits
  (`docs/skills/artifact-rules/references/script-interface.md`,
  `docs/skills/make-artifact/scripts/css_build.py`) on a branch already merged (PR #699,
  remote gone) with no open PR — ambiguous fresh in-progress work vs leftover dirt. Inspect
  the diff; either branch-and-PR it or discard it. Gates the fix-684 reap (entry 6, named
  inline there); the reap is additionally blocked by this live session — decide first, reap
  after the session exits. Not `sync_main.py`-eligible (feature-branch dirt, not main).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Deferred — explicit human-call flag.
- **Size:** ~5 min.

### 5. Resolve the 2 quarantine stashes at the primary — measured at last, after four silent firings
- **Action:** `git stash list` confirms 2 stashes, both `On main: sync_main quarantine`
  (repo-cleaner finally carried the inventory this firing). Inspect each; selectively restore
  only anything a live flow still owns, then drop. Judgment call — no gated script path
  exists for stash resolution; same sitting as entry 2 works.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Standing — first firing with an actual count (prior plans
  carried this unverified since the 02:32Z-era dirt).
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 6. Reap 6 merged worktrees + 10 merged local branches — one paste block; fix-684 deferred
- **Action:** from the primary checkout, run repo-cleaner's proposed block verbatim —
  worktrees `629-self-improvement-retrospective` (#645), `build-554` (#646), `fix-647`
  (#648), `fix-656-rdd-revalidation-rotation` (#653), `fix-660` (#661), `fix-667` (now
  holding `fix-683-container-grammar-role-aliases`, #702); branches
  `608-dispatch-ticket-file-bug-claim-fix` (#610), `611-backlog-roadmap-releases-loop`
  (#621), `612-harvest-domain-knowledge` (#614), `613-harvest-project-context` (#615),
  `622-feedback-intake-door` (#641), `637-drain-queue-command` (#643),
  `650-artifact-styling-rules` (#651), `657-scope-audience-frontmatter` (#664),
  `670-unnamed-checker-dispatch` (#689), `fix-667-build-feature-gh541-doctrine` (#668).
  Verify with `git worktree list` / `git branch -vv`. **Deferred, named inline:**
  `.claude/worktrees/fix-684` — blocked by entry 4 (open) and by this live session; reap only
  after both clear. Stays propose-only from the seat (no host reap script exists).
- **Owner:** Kim (same sitting as entries 2/5).
- **Evidence:** repo-cleaner §Propose-only — every item independently verified merged with
  its PR id; full paste block in its per-firing report (applied in entry 1).
- **Size:** ~5 min (+ ~1 min later for fix-684).

### 7. Repair adr-0023's stale PROPOSED blockquote — dated amendment, append-shaped
- **Action:** adr-0023 reads `status: accepted` (ratified 2026-08-18) but its body still
  carries a `> PROPOSED 2026-08-18 ... stays status: proposed until...` blockquote under the
  title — a stale-context defect a future reader or `save-lessons` author will trip on.
  Repair per docs-mutability: accepted ADRs are append-only (T4, gate-checked at
  `docs_check.py`/G10) — add a dated correction note superseding the blockquote rather than
  silently rewriting it.
- **Owner:** Kim (small doc fix; solo single-file, may commit to main per the campaign row).
- **Evidence:** decision-watcher §Note — flagged plainly, correctly not acted on by the seat
  (ADR content is data to classify).
- **Size:** ~3 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — both narrated state paths (`adr-queue.json`,
  `adr-checkpoint.json`) have matching fenced, target-pathed blocks.
- **issue-sorter:** clean — `watch-checkpoint.json` fenced; `friendlies.json` /
  `held-items.md` / `.mcp.json` explicitly declared unchanged and omitted entirely (no
  conditional naming); no per-firing report path narrated, none owed. The 3 label repairs are
  `gh` API edits — outside the sandbox's scope by design.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block;
  `campaign_close.py 769` was executed (gated, verified-safe — within its contract), all
  reaps explicitly propose-only.

## Not queued (checked, found clean or deliberately left)

- **#766** (dispatch_envelope.py first-use findings, `bug`+`minor` after this firing's label
  repair) — buildable backlog → teamwork's `/mobilize-chores`, outside this queue.
- **#759, #609, #490** — open, zero assignees, kind-labeled; buildable backlog →
  `/mobilize-chores`. #490 open by design (upstream pin-race tracking).
- **#617** — `backlog`-labeled fixture, excluded per the #611 parking rule; never a plan entry.
- **campaign_close.py C3 spurious WARN** — caused by passing `.` (workspace root) as the gate
  arg, not a plugin root; a seat-procedure nit, not repo debt. If it recurs next firing, it's
  a finding for issue-sorter to mint, not this plan's to fix.
- **`gitignore_check.py` WARNs** — standing 2-WARN (primary) / 4-WARN (worktree) sets,
  unchanged, no FAIL.
- **12 merged PRs this window** — discovery/context only; all corresponding issues closed by
  their merges per issue-sorter; nothing left open behind them.
- **Stale session gitStatus** — the dispatch context's gitStatus block (branch `fix-423-...`,
  dirty roster/settings/csv) does not match this worktree's real branch (`fix-684-...`);
  noise, not state — flagged, not acted on (same class as the prior plan's flag).

## Resolved since the prior plan (2026-08-18T22:03Z firing)

- Prior entry 1 (apply the 22:03Z payloads) — DONE (checkpoint continuity to 18:59:21Z via
  intermediate firings; decision-watcher reads 22 previously known).
- Prior entry 2 (sync_main, 42 behind) — RESOLVED BY EVENTS as measured (primary clean on
  `main`); the persist half re-scoped → entry 2.
- Prior entry 3 (PR #678) — DONE BY EVENTS (zero open PRs this firing).
- Prior entry 4 (stashes) — MEASURED at last (2 quarantine stashes) → entry 5.
- Prior entry 5 (worktree reaps) — grown to six runnable; deferred slot moved fix-667 →
  fix-684 → entries 4/6.
- Prior entry 6 (branch deletes) — grown seven → ten → entry 6.
- PR #769 — closed clean by repo-cleaner's own gated `campaign_close.py` run this firing
  (remote branch verified absent).

Dispatch: 2026-08-19T22:20:00Z
