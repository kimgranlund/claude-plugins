# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-21T21:37:39Z**. Evidence:
all three seat reports attached and complete — **no seat UNMEASURED this firing**
(dispatch-named UNMEASURED list: empty). One sub-measurement the seats' own content leaves
ambiguous: the liveness of the `plugins-marshal` session named in `sweep-in-flight.json`
(pid 35586 — `ps` found no matching process, but startedAt 2026-08-21T21:37:30.381Z is 9s
before this firing key; repo-cleaner correctly treated it as live-until-proven-dead).

decision-watcher: clean no-op — 23 ADRs scanned, all previously known, zero delta;
`adr-queue.json` already `{"candidates": []}`; per its no-op clause no payloads owed or
emitted. issue-sorter: window 2026-08-21T17:19:43Z→21:39:00Z, 3 new issues (#861–#863, all
trusted-author `task`s, correctly labeled at discovery), 7 already-tracked issues closed via
6 merged PRs; 0 repairs, 0 mints, 0 held, 0 needs-ruling; two payloads
(`watch-checkpoint.json`, its per-firing report). repo-cleaner: executed nothing beyond the
standing `git fetch --prune` (pruned 1 stale ref behind merged #851); `sync_main.py`
explicitly withheld — primary `main` carries a live peer session's in-flight dirt
(mid-edit teamwork 2.28.23→2.28.24 bump, `fleet-roster.md` gaining a `plugins-marshal
(takeover)` row); zero open PRs, no `campaign_close.py` target; classification set changed
materially (reap-safe worktrees 5→4, merged branches 10→12); one payload (its report).

**Prior plan (2026-08-21T17:18:52Z firing) reconciliation:** entry 1 (apply payloads) — DONE
(issue-sorter's window opens exactly at the applied 17:19:43Z checkpoint; repo-cleaner cites
the applied `2026-08-21T17-21-08Z-repo-cleaner.md` on disk as its prior-firing baseline).
Entry 2 (commit+push ops state) — RESHAPED: repo-cleaner's current primary-dirt list no
longer names the three previously-untracked prior reports or the plan file — that specific
debt no longer appears in evidence — but this firing's applied payloads recreate the same
persist obligation, and new ops-adjacent dirt (`fleet-roster.md`, the brief) sits tangled
with a possibly-live marshal session → entry 2. Entry 3 (three dirty worktrees) — still
open, unchanged → merged into entry 3. Entry 4 (fix-684 dirt) — still open, unchanged, no
longer separately session-blocked → merged into entry 3. Entry 5 (stashes) — still open,
unchanged → entry 4. Entry 6 (reap) — RESHAPED: `council-role-agents-840` (#843) and
`brand-design-wave2` (#848) resolved between firings with no trace; two branches NEW
(`fix-850-fleet-bootstrap-phase5-wall` #851, `post-series-cleanups` #823) → entry 5. Entry 7
(adr-0023 stale PROPOSED blockquote) — still open: decision-watcher's second consecutive
zero-delta scan proves the ADR body unchanged, still unrepaired → entry 6.

**Parked-issue check (#611):** no carried-forward entry id carries `backlog`/`roadmap` in
this firing's evidence — nothing dropped.

**Blocked-by (#193):** no literal `Blocked-by:` line in any evidence this firing — nothing
reordered by the convention. Operational dependencies named inline: the dirty-worktree reaps
wait on entry 3's decisions; entry 2 persists what entry 1 applies.

**needs-ruling lane:** empty — issue-sorter tested all three new issues (#861–#863) against
the ruling-shaped test and left all plain buildable tasks; no §3 reference owed.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` at the primary names session
`plugins-marshal` (pid 35586, startedAt 9s before this firing key) — almost certainly this
sweep's own dispatching session's coordination lock. Never quarantine it via `sync_main.py`,
never stage it in entry 2; it clears itself when the sweep exits. Apply all fenced payloads
at the shared checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: `.claude/ops/watch-checkpoint.json`
  (issue-sorter — github source advanced to 2026-08-21T21:39:00Z, strictly newer than the
  applied 17:19:43Z), `.claude/ops/reports/2026-08-21T21:39:00Z.md` (issue-sorter report),
  `.claude/ops/reports/2026-08-21T21-39-51Z-repo-cleaner.md` (repo-cleaner report), plus this
  rewritten `.claude/ops/plan.md`. decision-watcher owes no blocks this firing (clean no-op,
  declared). `friendlies.json` / `held-items.md` / `.mcp.json` explicitly unchanged — no
  blocks owed, none applied.
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** all four fenced blocks present (three seat payloads + this plan);
  narrated-but-absent audit below reads clean for all three seats.
- **Size:** ~2 min.

**Class 2 — blocking other work:**

### 2. Commit + push the applied ops state from the primary — the next scheduled firing starts blind until it lands (carried, reshaped)
- **Action:** from `/Users/kimba/Projects/nonoun/plugins` on `main`: stage exactly the
  ops-state paths entry 1 applied — never `git add -A`. **Exclude `sweep-in-flight.json`**
  (the live lock, per the lock-file note) and **exclude the live marshal session's own
  in-flight dirt** — `fleet-roster.md` (mid-edit takeover row), the brief, and the three
  `teamwork/` files (an in-progress 2.28.24 version bump) all belong to that session's flow,
  not this persist step. Read the status output, commit as a separate step, push. If the
  marshal session is still live at this sitting, coordinate before touching `main` at all.
- **Owner:** Kim.
- **Evidence:** ops-write-sandbox-rules (state persists through the repo or the next firing
  starts blind); repo-cleaner §Executed — `sync_main.py` withheld on live-session evidence.
  Carried from the prior plan's entry 2; the three previously-untracked prior reports no
  longer appear in repo-cleaner's dirt list (evidently persisted between firings).
- **Size:** ~3 min.

**Class 3 — human decisions:**

### 3. Decide the four dirty worktrees — rescue (branch + PR) or discard, each (carried, unchanged; prior entries 3+4 merged)
- **Action:** unchanged dirt across firings: `629-self-improvement-retrospective` (merged
  #645; untracked `lld-0018-estate-maintenance-retrospective.md`);
  `fix-656-rdd-revalidation-rotation` (merged #663; `revalidation_checkpoint.py` +
  `watch-adrs/SKILL.md` modified); `fix-667` (checked out on
  `fix-683-container-grammar-role-aliases` — HEAD `83fade5` fully contained in `origin/main`
  via #697 under a different branch name, **no PR under this branch's own name, orphaned** —
  plus `css_build.py` modified); `fix-684` (merged #699; 2 modified + 3 untracked
  `overhaul-run-*.md`, reads actively-in-use — verify no live session owns it first).
  Inspect each diff; branch-and-PR what's live, discard what's dead. Gates their reaps
  (entry 5, named inline there).
- **Owner:** Kim.
- **Evidence:** repo-cleaner §NOT safe to reap — explicitly unchanged from the prior firing.
- **Size:** ~15 min.

### 4. Resolve the 2 quarantine stashes at the primary — carried, unchanged
- **Action:** `git stash list` still shows 2 stashes, both `On main: sync_main quarantine`,
  unchanged across firings. Inspect each; selectively restore anything a live flow still
  owns, then drop. Judgment call — no gated script path exists for stash resolution; same
  sitting as entry 2 works.
- **Owner:** Kim.
- **Evidence:** repo-cleaner §Standing — unchanged.
- **Size:** ~4 min.

**Class 4 — hygiene debt:**

### 5. Reap 4 clean worktrees + 12 merged local branches — one paste block; four worktrees deferred
- **Action:** from the primary checkout, reap the verified-clean set: worktrees `build-554`
  / `634-req-infix-prefix` (#646), `fix-647` (#648), `fix-660` (#661),
  `fix-794-marketplace-drift` (#795); branches `608-dispatch-ticket-file-bug-claim-fix`
  (#610), `611-backlog-roadmap-releases-loop` (#621), `612-harvest-domain-knowledge` (#614),
  `613-harvest-project-context` (#615), `622-feedback-intake-door` (#641),
  `637-drain-queue-command` (#643), `650-artifact-styling-rules` (#651),
  `657-scope-audience-frontmatter` (#664), `670-unnamed-checker-dispatch` (#689),
  `fix-667-build-feature-gh541-doctrine` (#668), `fix-850-fleet-bootstrap-phase5-wall`
  (#851, new), `post-series-cleanups` (#823, new). Verify with `git worktree list` /
  `git branch -vv`. **Deferred, named inline:** worktrees `629-self-improvement-retrospective`,
  `fix-656`, `fix-667`, `fix-684` — blocked by entry 3 (open). Zero open PRs this firing —
  no healthy-in-flight exceptions. Stays propose-only from the seat (no host reap script
  exists).
- **Owner:** Kim (same sitting as entries 2/4).
- **Evidence:** repo-cleaner §Propose-only — every item independently verified merged with
  its PR id, remote gone, worktree clean; §Resolved confirms #843/#848 left the set cleanly.
- **Size:** ~5 min (+ a later pass as entry 3 clears).

### 6. Repair adr-0023's stale PROPOSED blockquote — dated amendment, append-shaped (carried)
- **Action:** carried forward, re-evidenced a third time: decision-watcher's zero-delta scan
  proves every ADR body unchanged, so adr-0023 still reads `status: accepted` over a stale
  `> PROPOSED 2026-08-18 ...` blockquote. Repair per docs-mutability: append a dated
  correction note superseding the blockquote — never silently rewrite an accepted ADR.
- **Owner:** Kim (small doc fix; solo single-file, may commit to main per the campaign row).
- **Evidence:** prior plan entry 7 + decision-watcher (zero delta, all 23 previously known).
- **Size:** ~3 min.

## Narrated-but-absent audit

- **decision-watcher:** clean — no-op clause explicitly invoked; no state paths narrated as
  written, no report path named, no blocks owed.
- **issue-sorter:** clean — both narrated paths (`watch-checkpoint.json`, the per-firing
  report `2026-08-21T21:39:00Z.md`) have matching fenced, target-pathed blocks;
  `friendlies.json` / `held-items.md` / `.mcp.json` declared unchanged and omitted, no
  conditional naming. Same data quirk as the prior firing, not a violation: its prose calls
  this "a standalone issue-sorter dispatch" — it ran inside this sweep; the payloads stand
  regardless.
- **repo-cleaner:** clean — its per-firing report present as a target-pathed block; nothing
  executed beyond the standing `git fetch --prune`; all reaps explicitly propose-only,
  `sync_main.py` explicitly withheld with its reasoning stated.

## Not queued (checked, found clean or deliberately left)

- **`sweep-in-flight.json` + the marshal session's in-flight dirt** (`fleet-roster.md`, the
  brief, three `teamwork/` files) — a live peer session's work, flagged in the lock-file
  note and entry 2's exclusions; never queued as cleanup.
- **#861, #862, #863 (new tasks) + #849, #617, #609, #490 (open, zero assignees)** —
  correctly labeled buildable backlog → teamwork's `/mobilize-chores`, outside this queue.
  (#490 is the upstream platform-bug tracker.)
- **`gitignore_check.py` WARNs** — primary 3-WARN (`dist/`, `harness-audit-*/`,
  `.name-map.md`, all stale-rule matches-nothing, unchanged; the `.name-map.md` worktree
  instance left with the #843 reap); all 8 worktrees uniform 4-WARN, expected
  partial-checkout shape; no FAIL anywhere.
- **1 pruned remote ref** (`origin/fix-850-fleet-bootstrap-phase5-wall`) — behind merged
  #851; its local branch is entry 5's new reap item.
- **7 issues closed + 6 PRs merged in issue-sorter's window** — discovery/context only;
  every merge already verified closed with remote branch gone or pruned.
- **Stale-claim check** — clean: all 7 open issues carry zero assignees.

## Resolved since the prior plan (2026-08-21T17:18:52Z firing)

- Prior entry 1 (apply the 17:18:52Z payloads) — DONE (checkpoint continuity + the applied
  repo-cleaner report cited on disk as this firing's prior baseline).
- Prior entry 2's specific untracked-reports debt — no longer in evidence: repo-cleaner's
  current primary-dirt list omits all three prior reports and the plan file (evidently
  persisted between firings); the persist obligation itself recurs as this plan's entry 2.
- Prior entry 6's `council-role-agents-840` (#843) and the #848 wave-2 worktree — RESOLVED
  BY EVENTS: both worktree and branch removed between firings, no trace remains.
- Open issues #850, #842, #840 — closed via this window's merged PRs.

Dispatch: 2026-08-21T21:37:39Z
