# Unattended collision protocol — opaque peer lanes with no human to ask

The SKILL.md's escalation for an opaque session is "ask the human." In an unattended run (a
/goal loop, a scheduled session — the operator asleep or absent) that branch is unavailable, and
freezing every contested lane until morning wastes the run. This protocol is the unattended
branch: how to tell a LIVE opaque lane from a DEAD one, and what each verdict licenses.

Worked instance behind every rule here: the agent-ui overnight goal run of 2026-08-06 (PRs
#511–#521), where one session ran alongside three opaque peer worktree lanes and applied each rule
below at least once; memory record `session-2026-08-06-overnight-goal-run.md` in that project's
ledger.

## 1 · Liveness is a delta, never a snapshot

A single `git status`/`lsof` reading cannot distinguish "actively working" from "died mid-work" —
both show a dirty tree and (between tool calls) zero open file handles. Probe TWICE, minutes
apart, and compare:

- capture per probe: branch tip SHA, `git status --porcelain | md5`, `lsof +D <worktree>` holder
  count, wall-clock time;
- tip advanced or dirty-hash changed between probes → **LIVE** — hands off, re-probe later;
- identical across probes → not yet dead, just quiet — apply the adoption bar (§3) before touching.

(2026-08-06 instance: a lane judged quiet at probe 1 had advanced a commit by probe 2, three
minutes later — a snapshot would have adopted a live session's branch.)

## 2 · Duplicate lane discovered → zero-salvage stand-down

When two lanes turn out to hold the same work item, exactly one wins — by merge-first, else by
seniority (which lane started the item first) — and the loser is deleted whole: worktree, branch,
in-flight review, all of it, without mining it for parts. Salvaging fragments from the losing
lane re-imports the collision as merge conflicts. Post a dated comment on the work item naming
which lane owns it and that the duplicate was stood down. (2026-08-06 instance: the run deleted
its own gates-green but still-unreviewed #475 build — its in-flight review stopped mid-read,
not salvaged either — when a peer wave claimed the issue; later the same night it
dropped that peer's duplicate #476 commit at adoption time because main had merged the scope
first — the rule cuts both directions.)

Lane claims (a dated issue comment at dispatch: "being built on branch X") are still worth
posting — but they prevent duplicate SHIPPING, not duplicate BUILDING: a peer that never re-reads
the tracker mid-build will still duplicate the work on a stale base and must hit the same
stand-down rule at its own ship time.

## 3 · Adopting a frozen lane: the bar, then the duty

A dead lane's committed work may be adopted and shipped by the surviving session — the ship leg
was always going to run outside the builder anyway. Adopt only when ALL of:

1. clean tree in that worktree (`git status --porcelain` empty) — uncommitted work means either a
   live session or an unfinishable fragment; neither is adoptable,
2. zero `lsof` holders on the worktree,
3. quiet ≥ ~25 minutes by §1's delta probes (calibrate to the peer's observed commit cadence —
   the 2026-08-06 run saw intra-build gaps up to 15 minutes, so 25 was one comfortable stride
   past the longest observed gap, not a magic constant),
4. no gate run could explain the silence (a browser-shard run can exceed 15 quiet minutes —
   check for test-runner processes before declaring death).

Adoption then carries duties, not just rights: re-run the full gates yourself in that worktree
(exit codes, foreground), get an independent review of the diff (the dead session's own review
claims are unverifiable self-reports), and say plainly in the PR that the ship leg was adopted —
the evidence trail must show who verified what.

## 4 · The write-fence

Until a lane is adopted under §3 or stood down under §2, its worktree is read-only to you:
reviews may read it and run tests in it, but no edits, no checkouts, no branch operations. A
reviewer running inside a lane that its owner suddenly resumes will misread the moving tree as
sabotage (2026-08-06 instance: a review seat reported "someone checked out main under me" —
reflog showed the lane's own session had resumed); the fence plus §1's re-probe is what keeps
that a false alarm instead of a corrupted review.
