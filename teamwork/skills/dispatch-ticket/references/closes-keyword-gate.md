# The Closes-keyword gate — why the mechanical check exists (gh#930)

Split from `SKILL.md`'s Phase 5 stage 2 (F6 line-budget split), the same pattern as this skill's
`plan-approval-write-gate.md` and `gate-run-time-budget.md` — read this once for the "why", the
inline instruction is enough to apply the check itself.

## The failure

Phase 5 stage 2 tells the dispatcher to open the PR "carrying `Closes #<id>`" so that GitHub's
own auto-close runs the moment the PR merges — Phase 6's read-back is written expecting exactly
that: a closed issue at merge time is the ordinary, expected end state, not something this seat
performs itself.

GitHub's auto-close keyword parser is narrower than a human reader: it requires a bare `#NNNN`
immediately adjacent to `Closes`/`Fixes`/`Resolves`. A repo whose commit/PR convention shortens
issue references as `gh#NNNN` — or a PR body that uses "Closes" as a prose verb rather than the
literal keyword form — reads to a human as satisfying the instruction above, but never matches
the parser. The merge lands, the PR closes, and the issue stays open with no signal that anything
went wrong. Nothing in the old instruction verified what actually got written against what GitHub
actually requires — it told the dispatcher what to write, never checked the result.

## Confirmed repro (2026-08-23)

A peer session (`gen-ui-kit-marshal`) found this live against 3 real merged PRs in
`adiahealth/gen-ui-kit`, all built via `teamwork:dispatch-ticket` 2.28.45–2.28.49:

- PR #1931 — body reads "Fixes gh#1925." — pattern not recognized (the `gh` prefix breaks
  adjacency between the keyword and the bare `#NNNN`).
- PR #1942 — body reads "- gh#1927 —" as a bullet — no `Closes`/`Fixes`/`Resolves` keyword
  present at all.
- PR #1938 — body reads "Closes the site-docs gap gh#1937 flags" — `Closes` used as a prose verb,
  not immediately adjacent to a bare `#1937`.

The reporter hit this 10+ times across builds in that one repo in a single day, each occurrence
needing a manual `gh issue close` to repair what the dispatch itself should have closed.

## The fix

A mechanical pre-PR-open check, run against the fully composed body immediately before the
`gh pr create` (or equivalent) call: `\b(Closes|Fixes|Resolves)\s+#\d+\b`, case-insensitive on the
keyword, must match for every id this dispatch closes. A miss fails loud — report the composed
body and the missing bare `#<id>`, and block PR-open — rather than silently shipping a
non-closing reference. This is the same discipline as the stage's other pre-open gates
(version-collision re-checks, the accept marker) — verify before the irreversible step, don't
trust that the instruction alone was followed correctly.

This closes the defect only inside `dispatch-ticket`'s own PR-body-composition step; it does
nothing for a PR opened by hand outside this skill's own dispatch. Naming the `gh#` shorthand
collision explicitly, here and in the inline instruction, is this fix's own secondary mitigation
for that gap — a human composing a PR body by hand at least has the trap named.
