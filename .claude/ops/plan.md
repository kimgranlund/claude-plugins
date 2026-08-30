# Ops plan: kimgranlund/claude-plugins

Rewritten whole by `chore-planner`, SWEEP dispatch, firing **2026-08-30T00:06:35Z**. Evidence:
three seat reports attached and complete; UNMEASURED this firing: **[]** (all three seats fired
and returned full reports — decision-watcher, issue-sorter, repo-cleaner). This dispatch's own
instruction was explicit: judge exactly the three attached reports, refetch nothing — no
supplementary live `gh`/`git` corroboration was run this firing. The only reads performed beyond
the three reports were this repo's own durable `.claude/ops/` state (prior `plan.md`,
`adr-checkpoint.json`, `adr-queue.json`, `watch-checkpoint.json`, `sweep-in-flight.json`) —
required for the prior-plan carry-forward and target-path/shape checks below, never used to
override or second-guess a seat's own judgment. Cross-check: the prior on-disk `plan.md`
(Dispatch `2026-08-28T22:57:00Z`) and the durable state files it applied were all committed
together in one commit (`a683a74b`) — the `2026-08-29T00:11–00:12Z` timestamps embedded in that
state are individual seat-completion stamps from that same single firing, not a missed
intervening dispatch; no process gap to flag.

**Payload audit (ops-write-sandbox-rules):**
- **decision-watcher**: clean. One block this firing (`adr-checkpoint.json`, 27 entries,
  `formula_version: 2`) — verified against the on-disk file: matches entry-for-entry except the
  19 amended ADRs' hashes (expected, per the report's own classify step) and the `adr-0027`
  `status` field, which the on-disk copy still carries corrupted
  (`"accepted        # proposed | accepted | superseded"`) and this firing's payload carries
  clean (`"accepted"`) — the self-heal claim checks out exactly. No `adr-queue.json` block:
  correctly omitted, on-disk copy already matches the report's "unchanged" claim verbatim
  (`adr-0027`, `queued_at: 2026-08-29T00:11:15Z`).
- **issue-sorter**: clean. Both blocks (own report at `.claude/ops/reports/2026-08-30T00:06:54Z.md`,
  `watch-checkpoint.json`) present, self-contained, checkpoint timestamps agree
  (`2026-08-30T00:06:54Z` on both `issues_checkpoint` and `prs_checkpoint`); on-disk
  `watch-checkpoint.json` still reads the prior `2026-08-29T00:11:19Z` stamp, consistent with
  nothing having applied this payload yet. `friendlies.json`/`held-items.md`/`.mcp.json` correctly
  named unchanged or not-applicable with no blocks.
- **repo-cleaner**: **anomaly, not a violation.** No fenced payload block appears anywhere in this
  firing's report — unlike the prior firing's own precedent of saving a full dated report
  (`.claude/ops/reports/2026-08-29T00-12-29Z-repo-cleaner.md`) when its classification set
  changed (which it explicitly says happened again this firing: "Classification set changed...
  full report, not abbreviated"). This does **not** meet the narrated-but-absent bar — the report
  never claims in prose to have written a `.claude/ops/reports/...-repo-cleaner.md` path this
  firing — so nothing is treated as a broken promise, but it diverges from its own stated
  precedent and is named here rather than silently absorbed. Nothing to apply for this seat this
  firing beyond the standing `git fetch --prune` exception it already executed directly.

No narrated-but-absent violations this firing.

**Prior plan (2026-08-28T22:57:00Z firing) reconciliation:** 4 of 6 entries resolved; 1 remains
open (carried forward); 1 (the human-decision batch-confirm) resolved between firings.
- Entry 1 (apply payloads): DONE — confirmed via durable state: `watch-checkpoint.json` and
  `adr-checkpoint.json`/`adr-queue.json` on disk exactly match what that firing's payloads
  specified.
- Entry 2 (commit and push): DONE — repo-cleaner's report confirms `main` `+0/-0` against
  `origin/main` with a clean tree.
- Entry 3 (confirm decision-watcher's adr-0027 harvest candidate): **NOT resolved — still open,
  carried forward again** (see Queue entry 3 below). decision-watcher's own report this firing
  explicitly reconfirms it as "still pending," untouched since `queued_at: 2026-08-29T00:11:15Z`.
- Entry 4 (batch-confirm repo-cleaner's local-disk cleanup — worktree `plugins-reviewer` +
  10 scratch clone dirs): **RESOLVED between firings** — repo-cleaner's report confirms both are
  now gone (presumably the human-executed version of that proposal); nothing to propose again.
- Entry 5 (#987, adr_checkpoint.py sha256 truncation): **RESOLVED** — repo-cleaner confirms #987
  is now CLOSED; its branch (`987-adr-checkpoint-py-periodically`) traced to merged PR #990,
  remote ref confirmed pruned this firing.
- Entry 6 (#978, tracking-issue post-merge check): **RESOLVED** — repo-cleaner confirms #978 is
  now CLOSED; its branch (`978-sweep-22-orphan-adrs`) traced to merged PR #989, remote ref
  confirmed pruned this firing. Note: decision-watcher's own classify trace shows PR #989's
  commit (`5aa2a523`) retrofitted intent-refs onto only 19 of #978's 22 orphan ADRs — no seat
  flags the remaining 3 as unaddressed scope, so this is recorded as context, not reopened as a
  finding.

**Parked-issue check (#611):** #617 stays dropped, parked #617 — not independently reconfirmed as
still `backlog`-labeled this firing (refetch-nothing precludes a live label check), carried
forward from the prior plan's own state per the carry-forward contract; no seat's report this
firing mentions or contradicts the parked classification. No focus instruction in this dispatch
names #617, so it is not un-parked.

**Blocked-by (#193):** no `Blocked-by:` line appears anywhere in the text of this firing's three
attached reports. Per this dispatch's own refetch-nothing instruction, open-issue bodies were not
independently fetched live to check further. Nothing reordered on this basis.

**needs-ruling lane:** empty. No seat names a `needs-ruling`-labeled issue this firing.

**Lock-file note:** `.claude/ops/sweep-in-flight.json` names session `plugins-c4` (pid 67870,
`startedAt` `2026-08-30T00:06:35.239Z`) — repo-cleaner's own report independently classifies this
as this firing's own coordinator lock, the same live-coordinator-state pattern every prior firing
has read it as, not cruft (confirmed against the on-disk file — exact match). Never quarantine it
via `sync_main.py`, never stage it in entry 2; it clears itself when the sweep exits. Apply all
fenced payloads at the shared checkout `/Users/kimba/Projects/nonoun/plugins/.claude/ops/...`.

## Queue

**Class 1, gated mutations verified safe:**

### 1. Apply this firing's payload blocks to their target paths (shared checkout)
- **Action:** write the fenced payloads verbatim: decision-watcher's `adr-checkpoint.json`
  (27 entries, `formula_version: 2`, self-healed `adr-0027` `status` field); issue-sorter's own
  report (`.claude/ops/reports/2026-08-30T00:06:54Z.md`) and `watch-checkpoint.json` (github
  source advanced to `2026-08-30T00:06:54Z`); plus this rewritten `.claude/ops/plan.md`. No
  `adr-queue.json` block (unchanged), no repo-cleaner block (none emitted this firing — see
  Payload audit), no `friendlies.json`/`held-items.md`/`.mcp.json` blocks (issue-sorter:
  explicitly unchanged/not-applicable).
- **Owner:** the dispatching session (apply step, per ops-write-sandbox-rules).
- **Evidence:** the two seats' fenced blocks; Payload audit above finds both clean.
- **Size:** ~2 min.

**Class 2, blocking other work:**

### 2. Commit and push this firing's applied ops state (recurring)
- **Action:** `main` is already `+0/-0` with `origin/main` (no pull needed first, per
  repo-cleaner). Once `sweep-in-flight.json` is confirmed cleared (this sweep's own marker,
  expected gone on exit), from `/Users/kimba/Projects/nonoun/plugins` on `main` stage exactly the
  ops-state paths entry 1 applied, never `git add -A`, never `sweep-in-flight.json`, read the
  status output, commit as a separate step, push, then re-verify via
  `git ls-remote origin refs/heads/main` against `git rev-parse HEAD` (push-verification
  convention, ops-write-sandbox-rules) before reporting it landed.
- **Owner:** Kim.
- **Evidence:** repo-cleaner's report (`main` `+0/-0`, clean tree); ops-write-sandbox-rules (state
  persists through the repo, or the next firing starts blind).
- **Size:** ~3 min.

**Class 3, human-decision items:**

### 3. Confirm decision-watcher's adr-0027 harvest candidate (carried forward, still pending)
- **Action:** unchanged proposal, unconfirmed since `queued_at: 2026-08-29T00:11:15Z` — extend
  `docs/skills/doc-writing-rules/references/`'s existing T4/ledger-lock material with ADR-0027's
  narrow carve-out (an already-accepted ADR may move `intent-refs:` from empty/`null` to a
  non-empty citation, verified as a single-field diff). decision-watcher re-verified this firing
  that no existing reference covers it and found zero new candidates besides it — this one
  remains the sole outstanding item. No human was present at dispatch (unattended firing), so the
  batch `AskUserQuestion` confirm was deferred again. On confirm: `/make-pack docs` targeting
  `docs/skills/doc-writing-rules/references/`, extend (not new-skill).
- **Owner:** Kim (confirm), then Kim or a dispatched builder (the `/make-pack` extend itself).
- **Evidence:** decision-watcher's report ("still pending," this firing's classify pass);
  `adr-queue.json`'s own unchanged content (verified on-disk this firing); ADR-0027 itself
  (`.claude/docs/adr/0027-narrow-t4-carve-out-for-intent-refs-backfill.md`).
- **Size:** ~5 min (confirm) + ~15-20 min (the extend-reference change itself, once confirmed).

**Class 4, hygiene debt:**

### 4. File + fix: adr_checkpoint.py's `FIELD_RE` truncates a multi-line `supersedes:` value (new, not yet ticketed)
- **Action:** decision-watcher found `FIELD_RE`
  (`^(id|status|supersedes)\s*:\s*(.+?)(?:\s+#.*)?\s*$`, MULTILINE but not DOTALL) captures only
  the first line of a multi-line frontmatter `supersedes:` value — confirmed by direct repro
  (`ac.superseded_ids(fm['supersedes'])` returns `['adr-0015']` for ADR-0020's real 4-target list
  `adr-0015; adr-0016; adr-0017; adr-0011`), silently dropping the `adr-0020→adr-0016/0017/0011`
  edges from `newly_superseded_edges`. Consequence found live: ADR-0020's real partial
  supersession of adr-0017's "RoleLex sizing posture" clause went **completely undetected** this
  round and would keep being missed on any future firing (two of the four targets happened to be
  re-announced by other ADRs this round, masking part of the loss; adr-0017 has no other
  announcer). Manual check found adr-0017's own citations already accurate, so no stale-citation
  resulted this time, but the detection gap is real and will recur silently. File a ticket against
  `harness/scripts/adr_checkpoint.py` covering both this and the related gap decision-watcher also
  named (`validate` doesn't catch a corrupted `status` field value, only hash well-formedness — it
  passed clean both before and after this firing's self-heal); fix is a DOTALL/continuation-line-
  aware capture for `supersedes:`, plus a `selftest` fixture per this workspace's
  `.claude/rules/scripts.md`.
- **Owner:** Kim (file + fix), or dispatch via issue-sorter's next firing to mint the ticket first.
- **Evidence:** decision-watcher's report ("Tool defect found" section); `FIELD_RE` in
  `harness/scripts/adr_checkpoint.py` (~line 142, per the report's own citation).
- **Size:** ~10 min to file; ~30-45 min to fix + add a selftest fixture.

### 5. #991 — confirm its PR fully resolved it before leaving it open
- **Action:** issue-sorter's check (00:06:54Z) named PR #992 as open against #991; repo-cleaner's
  check 37 seconds later (00:07:31Z) found zero open PRs repo-wide and named only #987 and #978 as
  newly closed since the prior firing — #991 was not in that closed list. Read together: PR #992
  merged in the gap between the two checks but did not carry a closing keyword against #991 (or
  the fix was deliberately partial), so #991 is likely stale-open post-merge — same shape as the
  resolved #978 finding above. Read #991 and PR #992's diff, confirm whether #992 fully addressed
  it, close or comment accordingly.
- **Owner:** Kim (or issue-sorter's next firing, once it re-touches #991).
- **Evidence:** issue-sorter's report (#991 bug+minor, "PR #992 already opened against it");
  repo-cleaner's report ("Open PRs: none," "#987 and #978 closed since prior firing" — #991 absent
  from that list); repo-cleaner's full-history count (299 MERGED, 1 CLOSED-not-merged, 0 open —
  #992 necessarily falls in the MERGED bucket).
- **Size:** ~5 min.

## Not queued (checked, found clean, parked, or deliberately left)

- **`sweep-in-flight.json`**: this firing's own lock (session `plugins-c4`, pid 67870); see
  Lock-file note; never queued as cleanup.
- **dropped: parked #617**: see Parked-issue check above; not a numbered entry, not un-parked.
- **#609**: open bug/major, zero assignees, unchanged this firing, buildable/tracked backlog
  (platform-defect record, not ops-sweep work), outside this queue; `doing` label not treated as a
  claim absent a ruling naming it as one (same precedent as every prior firing).
- **#993, #994, #995, #996**: new (opened 2026-08-29T23:4x), already correctly labeled
  `task`+`size:small` at mint, zero assignees — tracked backlog outside this ops queue, same
  precedent as #609.
- **3 PRs merged this window** (#989 closes #978, #990 closes #987, #992 against #991 — merged
  without auto-closing it, see Class 4 entry 5 above): context, all `kimgranlund`, already
  reflected above.
- **2 pruned remote refs this firing** (`978-sweep-22-orphan-adrs` → merged PR #989,
  `987-adr-checkpoint-py-periodically` → merged PR #990): already gone, repo-cleaner's standing
  `fetch --prune` exception, no further action.
- **Gitignore 3 WARN** (`dist/`, `harness-audit-*/`, `.name-map.md`): already RULED keep-all by
  Kim 2026-08-24 (commit `a871ea9`, covering all 3 entries); `dist/` re-entered the stale-match
  list this firing because it's currently empty (no build artifact present) — already covered by
  the standing ruling, no new review owed.
- **Stale-claim check**: clean — all open issues (#609, #617 [parked], #991, #993, #994, #995,
  #996) carry zero assignees under ADR-0005.
- **Off-main-primary**: none — `primary_checkout_check.py` reads clean/PASS.
- **Worktree/branch/remote-branch/open-PR surfaces**: all healthy per repo-cleaner — single
  primary checkout, no orphaned worktrees or scratch clones (prior firing's two findings both
  resolved between firings), no stray remote branches, zero open PRs, the one historical
  closed-not-merged PR (#437) already has its branch gone.

## Resolved since the prior plan (2026-08-28T22:57:00Z firing)

- Prior entry 1 (apply payloads): DONE.
- Prior entry 2 (commit and push): DONE, `main` `+0/-0` with origin.
- Prior entry 4 (batch-confirm local-disk cleanup — worktree `plugins-reviewer` + 10 scratch
  dirs): RESOLVED between firings.
- Prior entry 5 (#987): RESOLVED, closed via merged PR #990.
- Prior entry 6 (#978): RESOLVED, closed via merged PR #989 (19/22 orphan-ADR retrofit noted as
  context, not reopened).
- Prior entry 3 (confirm adr-0027 harvest): **not resolved** — carried forward as this plan's
  entry 3.

Dispatch: 2026-08-30T00:06:35Z
