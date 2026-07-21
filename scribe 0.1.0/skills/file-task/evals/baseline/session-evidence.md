# Baseline — what happens WITHOUT /issue (recorded 2026-07-15..16, this workspace)

Eight work items were captured with raw `gh issue create` during the external-skill-review arc.
The variance this skill exists to remove, all observed live:

- **The label set didn't exist** — the first capture (#5/#6) failed with `could not add label:
  'feature' not found`; the session had to mint `feature`/`size:*`/`doing` labels mid-flight.
- **Section sets varied per issue** — #5/#6 carried Summary/Acceptance/Links/Findings; #19's
  first draft nearly shipped without a Findings section; the bundle issues (#8–#11, #13)
  improvised extra tables ad hoc.
- **No dedup sweep ever ran** — nothing checked whether an open issue, a ROADMAP line, or the
  codebase already covered the item.
- **Status changes were raw commands** — `doing` labels and closes were hand-typed `gh issue
  edit`/`comment` calls with no contract on what a close owes the record (a dated Findings
  entry was added by convention, not rule).
- **No file-backend fallback** — outside this git-native workspace the same ask would have
  produced nothing durable at all.

Issues cited as the artifact trail: kimgranlund/claude-plugins #5, #6, #8, #9, #10, #11, #13,
#19 (bodies + comment history show the improvised variance).
