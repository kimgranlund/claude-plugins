# Worktree/branch teardown — Phase 3's full procedure

Cited from `dispatch-ticket/SKILL.md`'s Phase 3 "Tear down a no-longer-needed scratch
branch/worktree" bullet rather than restated inline (the same F6 split-to-references pattern as
`de-stale-premise-check.md` and `spec-lock-gate.md`).

Two cases reach this bullet: the Release-on-abandonment bullet above (claim already released), and
Phase 2's bug hand-off, only once the post-hand-off read-back (Phase 6's verbs) shows a terminal
state (issue closed, or a `file-bug` Findings entry marking its own run done) with nothing landed
on the branch. Short of that, the worktree stays standing, reported as residue — never torn down
while `file-bug`'s own fork may still be live inside it.

Never retire with a raw `git branch -D` plus worktree removal — that force-deletes work on this
seat's own say-so alone. Feature-detect the host repo's own gated reap script (reference shape:
gen-ui-kit's `scripts/ops/reap-branches.mjs --verify-branch <name>` — a differently-located script
counts only if the host repo's own docs declare the same 0/1/2 contract) and gate the delete on
its exit code alone. Order: `git worktree remove` first (refuses on a dirty tree, so nothing is
lost on a wrong call), THEN `--verify-branch`, THEN — only on exit 0 (a merge-base ancestor of
`origin/main`, or an exactly-matching MERGED PR) — `git branch -d` (never `-D`, even after a
verified 0). Exit 1 (KEPT/PROPOSED), or either verb refusing outright, → leave standing and report
why, never force. Exit 2 is a usage error, not a verdict — report it. No such script → fall back to
an unverified `git worktree remove` then `git branch -d`, never silently — name what went
unverified.
