# Parallel-session reconcile — pulling onto a checkout someone else is using

This workspace routinely has more than one session working the same main checkout concurrently
(a property of the environment, not a mistake to prevent). The protocol below is what makes that
safe, refined across two real incidents on the same day.

## The core rule: quarantine foreign work before touching HEAD

[verified, this session's own protocol design synthesizing the incidents below, 2026-07-17] Before pulling onto a dirty checkout, classify every
locally-modified file against the files the incoming commits touched:
- **Foreign-only** (dirty here, untouched by the incoming commits) — safe to quarantine and
  reapply blind afterward; nothing about the pull can have invalidated this work.
- **Overlap** (dirty here AND touched by the incoming commits) — the danger zone; a blind
  reapply after the pull risks silently discarding either side. Read both before resolving.

`sync_main.py` (forge 1.30.0, `ce05fcb`) mechanizes exactly this classification, then stashes
everything dirty under one named, greppable message (`"sync_main quarantine"`) BEFORE pulling —
never staging foreign work into the pulling session's own commit — pulls `--ff-only` (so a
genuine divergence FAILS loudly instead of silently creating a merge commit), and re-verifies
HEAD matches `origin/main` by SHA afterward (the `silent-failure-catalog.md` doctrine, applied
here specifically).

## Live proof: dogfooded on this exact workspace, 2026-07-17

[verified, observed directly in this authoring session's own tool-call transcript,
2026-07-17 — not externally documented; one evidentiary tier below a linked commit/PR, same
weight as a cited worked instance] The script's first live run
(extracted from `origin/main` and pointed at this workspace's own main checkout, moments after
`ce05fcb` merged) classified 13 dirty files against 7 incoming —
ZERO overlap, all 13 foreign-only. It quarantined them as `stash@{0}`, pulled clean, verified
HEAD by SHA, and reported the safe-to-reapply-blind set. `git stash pop` afterward restored all
13 files with no conflicts — exactly the outcome the zero-overlap classification predicted.

## The failure this replaces: resolving a merge conflict by keeping the wrong side

[incident, 2026-07-17] A `git stash pop` (or equivalently, a merge-conflict resolution during a
`git pull`) was resolved by keeping the STALE local copy over the incoming change — nothing
caught it at the time; the error surfaced only when a later push failed against an out-of-date
base. **The lesson this bakes in:** a conflict resolution is not "pick a side and move on" — it
requires reading BOTH sides and understanding what each one is claiming before choosing, exactly
the distinction the OVERLAP/foreign-only classification exists to surface. When genuinely unsure
which side is current, re-checkout the file from the incoming ref (`git checkout origin/main --
<file>`) and reapply only the specific delta you know is yours — never resolve a conflict marker
block by simply keeping "the side that was already there."

## What conflict resolution is NOT — it stays judgment

The classification report names which files are foreign-only (safe to reapply blind) vs. overlap
(read both sides) — it does not attempt to AUTO-RESOLVE an overlap conflict. That decision
requires understanding what each side's change means, which is exactly the kind of judgment call
a mechanical script cannot safely make; the report's job is narrowing where that judgment is
needed, not replacing it.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| A `git pull` on a dirty checkout appears to hang, do nothing, or silently discard local work | uncommitted foreign work wasn't quarantined before pulling | `sync_main.py` — never a raw `git pull` on a dirty tree with parallel-session content present |
| A later push fails against an out-of-date base | a conflict was resolved by keeping the wrong (stale) side | re-checkout the specific file from the incoming ref; never resolve blind |
| Uncertainty about whether a file is safe to reapply after a stash pop | the overlap/foreign-only distinction was skipped | run the classification before popping, not after |
