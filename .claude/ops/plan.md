# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-14 ~00:03Z window (UTC),
main at `de21cbd`, tree clean except this sweep's own ops writes. Evidence: the three
seat reports attached to this dispatch (decision-watcher checkpoint-only zero-delta;
issue-sorter 3 open issues / 0 open PRs, checkpoint 2026-08-14T00:01:27Z; repo-cleaner
full report at `.claude/ops/reports/2026-08-14T00-03-07Z-repo-cleaner.md`), the prior
plan (2026-08-13 ~16:39Z) as carry-forward source, plus dispatcher-authorized live
corroboration (git worktree/branch/status, gh issue/pr list, ADR-0011 frontmatter +
line 179, spec-dir listing, root-manifest absence — all consistent with the seats).
Overnight since the prior plan: 9 PRs merged (#209–#213, #215–#218), #196 closed,
open issues 7 → 3, remote branch estate fully reaped except one LOCAL remnant.

## Human-decision call-outs — nothing below executes autonomously next sweep

Four items only Kim advances; each is a queue entry, named here distinctly:
1. **Orphaned worktree removal** (entry 1) — verified safe, but no gated reap script
   exists; the command is human-run.
2. **ADR-0011 `supersedes: null` gap** (inside entry 4) — must be wired AT ratification
   or supersession of ADR-0001/0006's grammar halves never mechanically fires.
3. **#197's satisfied blocker** (entry 6) — `Blocked-by: #196` cleared; only Kim's own
   reopen trigger advances it.
4. **Checkpoint-bypass hygiene note** (entry 8) — decide guard-or-accept.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Remove PR #209's orphaned local worktree + branch
- **Action:** `git worktree unlock .claude/worktrees/declarative-wondering-scroll &&
  git worktree remove .claude/worktrees/declarative-wondering-scroll &&
  git branch -d worktree-declarative-wondering-scroll`
- **Owner:** human (Kim) — no gated reap script exists in this repo; removal is
  copy-paste of the sequence above, propose-only from the seat.
- **Evidence:** repo-cleaner — #209 MERGED (mergeCommit `cf86dbd8`), remote branch 404,
  worktree lock names pid 66795 confirmed not running. Planner live-verified: worktree
  present + locked at `efc49b5`, branch upstream `gone`.
- **Size:** ~2 min.

### 2. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Stage exactly `git add .claude/ops/plan.md .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-14T00-03-07Z-repo-cleaner.md`; read the status output,
  then commit as a separate step (gate ≠ commit), then push. `adr-checkpoint.json` is
  NOT part of this firing's delta (checkpoint-only, zero-delta; `git status` confirms
  unmodified). Never `git add -A`, even on a clean tree.
- **Owner:** the dispatching session if Bash-capable, else human. Carried note:
  chore-lead's own grant is Read/Write/Task — no Bash/git — so this routes past it.
- **Evidence:** `git status --porcelain` at planner runtime — `watch-checkpoint.json`
  modified, repo-cleaner report untracked, plus this plan rewrite once applied.
- **Size:** ~2 min.

### 3. Fix ADR-0011's step-2 cited spec path (carried; landing vehicle changed)
- **Action:** In `.claude/docs/adr/0011-adopt-naming-convention-spec.md:179`, change
  `.claude/docs/spec/naming-convention-spec.md` → `.claude/docs/spec/spec-naming-convention.md`
  (the file that actually landed, matching the dir's `spec-{topic}` convention). The
  ADR is committed on main now but still `status: proposed` — mutable class; this MUST
  land before entry 4 flips it append-only. Single-file fix may commit direct to main
  per workspace convention.
- **Owner:** human (Kim), or one dispatched build seat under a batched confirm.
- **Evidence:** live grep this dispatch — line 179 still stale; spec dir carries
  `spec-naming-convention.md`. Carried from prior plan entry 1: its #196-PR landing
  vehicle merged (#218) WITHOUT the fix.
- **Size:** ~5 min.

**Class 2 — items blocking other work:**

### 4. Ratify ADR-0011 — with the `supersedes:` wiring, in the same act
- **Action:** After entry 3: flip frontmatter `status: accepted` + `ratified: <date>`
  AND set `supersedes:` to the partial-supersession strings naming the grammar halves
  of ADR-0001 and ADR-0006 (the string convention ADR-0007/0009 already use).
  Ratification checklist item, not optional: supersession detection reads ONLY that
  field — left `null`, the D7–D9 supersession never mechanically fires and downstream
  citations of ADR-0001/0006's naming-grammar rulings are never flagged stale.
  Ratification unblocks chain steps 2–6 and decision-watcher's harvest queue
  (re-review fires automatically once ratified).
- **Owner:** human — the formal act is the maintainer's alone.
- **Evidence:** decision-watcher this sweep (the supersedes gap); planner live-verified
  frontmatter `status: proposed` / `ratified: null` / `supersedes: null` (lines 4–8).
- **Size:** ~15 min.

### 5. Author the estate-wide root `naming.manifest.json` (carried)
- **Action:** Create `naming.manifest.json` at the repo root covering the estate per
  ADR-0011 step 2/D10. NOT satisfied by `authorkit/naming.manifest.json` (self-scoped,
  different deliverable). Sequence after entry 4; track via entry 7's step-2 record.
  Step-3 validator and step-6 burn-down metric both consume this file.
- **Owner:** human or a build seat, once entry 7's step-2 record exists to claim.
- **Evidence:** planner live-verified root manifest still absent this dispatch;
  prior-sweep triple confirmation carried.
- **Size:** hours (estate-wide inventory), sized properly inside its own record.

**Class 3 — human decisions:**

### 6. Rule #197's next state — its blocker is now satisfied
- **Action:** #197 (authorkit absorbs the authoring family, deferred) had
  `Blocked-by: #196`; #196 closed via merged PR #218 overnight. Kim decides: activate
  the option-3 boundary refactor, re-defer with a NEW named reopen trigger (the old
  trigger is spent — leaving it trigger-less recreates the silent-stall risk prior
  sweeps flagged), or close. The seat correctly did not touch it.
- **Owner:** human (Kim) — by design, only Kim's own trigger advances #197.
- **Evidence:** issue-sorter this sweep; planner live-confirmed #197 open, unassigned.
- **Size:** ~5 min.

### 7. Rule filing timing, then file the four chain-step records (carried, half-resolved)
- **Action:** The prior open question was "file now, or hold until #196 lands AND
  ADR-0011 ratifies" — the #196 half is now satisfied; only entry 4 remains. Rule
  now-vs-after-ratification, then file one record each for steps 2, 3, 4, 6, content
  as specified in the 2026-08-13 plan (step-2 estate-manifest scope distinct from
  authorkit's; step-3 repo-own gate wiring — authorkit ships DISABLED here; step-4
  supersession note in harness:naming-rules, split from #197 — entry 4's `supersedes:`
  wiring covers mechanical detection but the skill's own prose note is still owed;
  step-6 exemption burn-down metric, pure gap).
- **Owner:** human (the ruling); filing via docs' file-task path or issue-sorter.
- **Evidence:** issue-sorter this sweep — exactly 3 open issues (#189, #197, #207),
  none tracking steps 2/3/4/6.
- **Size:** ~5 min (ruling) + ~15 min (filing).

### 8. Rule the adr-checkpoint bypass: guard or accepted one-off
- **Action:** Something wrote an `adr-0011` entry directly to
  `.claude/ops/adr-checkpoint.json` outside decision-watcher's own classify/advance
  calls. Harmless this time (content was unratified) but it bypasses the seat's
  integrity path. Decide: file an issue per the incident→infrastructure invariant
  (a guard on checkpoint writers), or record as an accepted one-off here. Either way
  the ruling gets recorded so it stops resurfacing.
- **Owner:** human (Kim).
- **Evidence:** decision-watcher this sweep (attention item, elevated to a
  decision-shaped entry per dispatch).
- **Size:** ~5 min.

**Class 4 — hygiene debt:**

(none this firing — the only hygiene item, entry 1, graduated to class 1 as a
verified-safe mutation.)

## Not queued (checked, found clean or deliberately left)

- **#207 / #189:** deliberately-open CLI-level tracking records per explicit in-thread
  ruling; the only two ADR-0005 claims outstanding, both healthy (claimed 22:38Z,
  linked to merged #216). Untouched.
- **8 of 9 overnight PR branches (#210–#218):** zero remnant — remote branches
  independently verified gone (404 each); nothing for `campaign_close.py` to close.
- **Main:** clean, in sync with origin — no `sync_main.py`.
- **`.gitignore` G1 WARNs** (`dist/`, `harness-audit-*/`): fifth consecutive review,
  legitimate on/off generated paths. Recorded judgment, not a task.
- **Friendlies allowlist:** all authors already allow-listed; no gating.
- **`watch-checkpoint.json` @ 2026-08-14T00:01:27Z:** current state — do not redo.
- **decision-watcher harvest queue:** deliberately empty until entry 4 ratifies;
  re-review fires automatically then.
- **Chain step 5** (adia-ui-kit rename wave): other repo, out of this queue's scope.

## Resolved since the prior plan (2026-08-13, ~16:39Z sweep)

- Prior entry 2 (commit that firing's ops artifacts) — RESOLVED: only this firing's
  own writes remain uncommitted.
- Prior entry 1 (ADR-0011 path fix) — NOT resolved; carried as entry 3 with a changed
  landing vehicle (#196's PR merged without it).
- Prior entries 3/4/5 — carried as entries 4/5/7, each updated: entry 4 gains the
  `supersedes:` wiring requirement; entry 7's timing question is half-answered by
  #196 landing.
- #196 closed via merged PR #218; open issues 7 → 3; 9 PRs merged overnight, remote
  estate fully reaped bar #209's local remnant (entry 1).

## Session rulings appended (2026-08-14, Kim via mobilize round)

- Entry 6 (checkpoint-bypass): ACCEPTED AS ONE-OFF — likely the overnight ops commit; re-litigate only on recurrence.
- Entry 1 (orphaned worktree): DONE — removed + branch deleted, verified.
- Entry 3 (ADR-0011 stale path): DONE — fixed at 6bcbfbe while still proposed.
- Entries 4/5 (ratify ADR-0011, naming.manifest.json): ride inside #197's campaign, now MOBILIZED — plan-plugin-split analysis dispatched; ratification is Kim's explicit word at the campaign's design gate.
