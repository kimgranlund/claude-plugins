<!--
See CONTRIBUTING.md for the full workflow (ADR-0002: branch + git worktree + PR).
-->

## What & why

<!-- What changes, and the reason — link the Issue this closes. -->

Closes #

## Gate

<!-- release_gate.py output for every plugin this PR touches. CI re-runs this on the PR. -->

```
python3 harness/scripts/release_gate.py <plugin-root>
```

- [ ] Gate passes for every touched plugin
- [ ] Version bumped and logged in each touched plugin's README footer ledger
- [ ] `evals/evals.json` updated if this PR changes any model-invocable description

## Notes

<!-- Anything a reviewer needs that isn't obvious from the diff. -->
