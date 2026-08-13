# Ops plan — kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, 2026-08-13 (~16:39Z window close),
main at 38e60fc. Evidence: the three seat reports attached to this dispatch
(decision-watcher, issue-sorter, repo-cleaner — none UNMEASURED, all three returned),
plus the prior plan (2026-08-12, ~17:20Z sweep) read as carry-forward source, plus one
live `git status` read to enumerate this sweep's own file writes. FOCUS this firing:
ADR-0011 (naming-v2, `.claude/docs/adr/0011-adopt-naming-convention-spec.md`, status
proposed, deliberately UNCOMMITTED — live work product riding in #196's PR, never to be
cleaned/reverted/quarantined) and its 6-step execution order, weighted above general
hygiene. Step 5 (adia-ui-kit rename wave) executes in a different repo and is out of
this queue's scope. Hygiene competition is near zero: repo-cleaner found 109/109 PRs
merged, one branch, one worktree, zero stale claims.

## Queue

**Class 1 — gated mutations verified safe:**

### 1. Fix ADR-0011's step-2 cited path to the landed filename (chain step 1 prerequisite)
- **Action:** In ADR-0011's Execution-order §2 prose, change the cited spec path
  `.claude/docs/spec/naming-convention-spec.md` → `.claude/docs/spec/spec-naming-convention.md`
  (the file actually landed). Fix the PROSE, not the file: the landed name already
  matches the directory's own `spec-{topic}` convention (decision-watcher's
  recommendation, independently endorsed by repo-cleaner). Edit rides inside the
  uncommitted ADR-0011 file — an advancement of live work product, not cleanup — and
  lands with #196's PR. Without this, a ratified ADR cites a nonexistent path.
- **Owner:** human (Kim), or the session landing #196 — the ADR is their in-flight
  work product.
- **Evidence:** All three seats independently confirmed the mismatch this sweep
  (decision-watcher found it; issue-sorter and repo-cleaner each re-confirmed
  independently).
- **Size:** ~2 min.

### 2. Commit this firing's ops artifacts — explicit pathspec only
- **Action:** Stage exactly the four ops paths this sweep touched —
  `git add .claude/ops/plan.md .claude/ops/adr-checkpoint.json
  .claude/ops/watch-checkpoint.json
  .claude/ops/reports/2026-08-13T16-38-58Z-repo-cleaner.md` — read the status
  output, then commit as a separate step (gate ≠ commit), then push. NEVER
  `git add -A`: the working tree also holds the three uncommitted ADR-0011-chain
  items (the ADR, the spec doc, `authorkit/` incl. its staged self-scoped manifest)
  that must ride in #196's PR, not an ops commit.
- **Owner:** chore-lead (the dispatching session), else human. NOTE (added on relay,
  not by chore-planner): chore-lead's own tool grant is Read/Write/Task only — no
  Bash/git — so this action cannot execute inside chore-lead itself; it routes to a
  human or a Bash-capable seat.
- **Evidence:** `git status --porcelain` at planner runtime — `adr-checkpoint.json`
  modified (decision-watcher classified ADR-0011 as `new`), `watch-checkpoint.json`
  modified (issue-sorter), repo-cleaner report untracked at the path above; plus this
  plan rewrite once applied. repo-cleaner: propose-only firing, zero mutations of its
  own.
- **Size:** ~2 min.

**Class 2 — items blocking other work:**

### 3. Ratify ADR-0011 — the single act gating chain steps 2–6
- **Action:** After entry 1 lands in the ADR text: flip frontmatter to
  `status: accepted` + `ratified: <date>` and commit. Routing sub-decision, human's
  call (no hard gate mandates either): via a PR per ADR-0002's campaign convention —
  #196's PR already carries the ADR file, though #196's own scope explicitly keeps it
  `proposed` — or direct-to-main as ADR-0010 did. Ratification also unblocks
  decision-watcher's harvest queue (save-lessons Phase 1 requires a ratified decision;
  the queue sits deliberately empty until then).
- **Owner:** human (the formal act is the maintainer's alone — decision-watcher found
  nothing else blocking it: fully ruled, no conflicting or open ruling).
- **Evidence:** decision-watcher this sweep — ADR-0011 fully ruled, `proposed`,
  uncommitted, no tracking issue/PR; issue-sorter — #196 lands the file but explicitly
  does not ratify.
- **Size:** ~10 min (decision + flip + commit/PR routing).

### 4. Author the estate-wide root-level `naming.manifest.json` seed (chain step 2, second half)
- **Action:** Create `naming.manifest.json` at the repo root covering the estate
  (155 nonoun names + 32 adia-ui-kit names + adia-eng non-conformers per step 2/D10).
  NOT satisfied by the existing `authorkit/naming.manifest.json` (8-entry object_vocab,
  empty exemptions, self-scoped to authorkit's own artifacts — a different
  deliverable). Sequence after entry 3 per the ADR's own execution order; track via
  entry 5's step-2 record. Step 3's validator and step 6's burn-down metric both
  consume this file, so it heads the post-ratification build line.
- **Owner:** human or a build seat, once entry 5's step-2 record exists to claim.
- **Evidence:** decision-watcher — no `naming.manifest.json` anywhere at root;
  issue-sorter — authorkit's staged manifest is explicitly not the estate-wide one;
  repo-cleaner independently confirmed the root manifest missing.
- **Size:** hours (estate-wide inventory), sized properly inside its own record.

**Class 3 — human decisions:**

### 5. Decide filing timing, then file four tracking records — chain steps 2, 3, 4, 6
- **Action:** Human rules issue-sorter's open question: file the four records NOW as
  deferred captures, or hold until #196 lands and ADR-0011 is ratified. Then file one
  record per step, each linking ADR-0011 and noting in prose "blocked until ADR-0011
  status: accepted" (no formal blocked-by field exists here). Required content per
  record, from this sweep's findings:
  - **Step 2** (estate manifest): the entry-4 scope; distinct from authorkit's manifest.
  - **Step 3** (greenfield validator per spec §11): `authorkit/skills/naming-audit/
    scripts/validate.py` + `authorkit/hooks/hooks.json` exist, but authorkit ships
    DISABLED in this workspace per #196's interim posture, so its PostToolUse hook
    cannot satisfy "wired into THIS repo's own ship gate" — the record's scope is the
    repo-own gate wiring, not the script.
  - **Step 4** (supersession note in harness:naming-rules): file as its OWN lightweight
    record, explicitly split from #197 (deferred with no reopen trigger — the silent-
    stall risk both seats flagged). Record must require hand cross-links to ADR-0001
    §grammar and ADR-0006 §grammar: ADR-0011's deliberate `supersedes: null` means the
    binary-supersession checkpoint tooling will never mechanically flag them.
  - **Step 6** (exemption burn-down metric): no issue anywhere mentions it — pure gap.
- **Owner:** human (the timing ruling + the #197 split ruling); filing then via the
  docs file-task path or issue-sorter.
- **Evidence:** issue-sorter this sweep — steps 2/3/4/6 have zero open issues tracking
  them across all 7 open issues; #196/#197 correctly cross-linked siblings, no
  duplicates; decision-watcher — steps 3/4/6 not started.
- **Size:** ~5 min (the ruling) + ~15 min (filing four records).

**Class 4 — hygiene debt:**

(none this firing — repo-cleaner: fully healthy, zero competing hygiene work.)

## Not queued (checked, found clean or deliberately left this sweep)

- The three uncommitted ADR-0011-chain items (the ADR, `spec-naming-convention.md`,
  `authorkit/`): confirmed coordinated in-flight landing tied to #196, cross-linked
  from #197 — left exactly as-is by explicit dispatch constraint and repo-cleaner's
  propose-only posture. Not cruft, not quarantined.
- `.gitignore` WARNs, same two (`dist/`, `harness-audit-*/`): fourth consecutive
  firing, reviewed, legitimate on/off paths. Recorded judgment, not a task.
- Issues #189–#193: scanned by issue-sorter — no duplicates, no staleness, no
  blockers, all unassigned with no ADR-0005 claims; too fresh for any staleness
  window (repo-cleaner concurs). Nothing to queue.
- PR/branch estate: 109/109 PRs merged, single local+remote branch (main), single
  worktree; no `campaign_close.py` or `sync_main.py` warranted; no host reap script
  exists — unchanged, no evidence one is needed.
- decision-watcher harvest queue: deliberately empty — save-lessons Phase 1 requires
  a ratified decision; unblocks at entry 3.
- Chain step 5 (adia-ui-kit rename wave): out of scope — executes in
  /Users/kimba/Projects/adia/gen-ui-kit, context only.

## Resolved since the prior plan (2026-08-12, ~17:20Z sweep)

- Prior entry 1 (commit the 17:20Z firing's ops artifacts) — RESOLVED: those paths no
  longer appear uncommitted; repo-cleaner this firing counts exactly three uncommitted
  items, all ADR-0011-chain.
- Prior entries 2–4 (#184 sizing ruling, #183 campaign routing, #185 batch confirm) —
  RESOLVED: none of #183/#184/#185 remains among the 7 open issues issue-sorter
  enumerated (#189–#193, #196, #197); merged-PR count advanced 106 → 109 across the
  gap, consistent with the three builds landing. The prior firing's whole
  human-decision block cleared inside one day.
