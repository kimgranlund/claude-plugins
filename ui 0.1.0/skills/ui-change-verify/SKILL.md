---
name: ui-change-verify
description: >-
  Verify a UI change end-to-end against the running artifact before declaring it done — start the
  app, interact with the change directly, screenshot before/after, check the console, and audit
  performance. Use when the user asks to verify, check, or confirm a UI change — a new control, a
  layout edit, a style change, "is this button working", "did that fix the layout", "verify this
  UI change" — or whenever about to report a frontend change complete. NOT for reasoning about a
  UI's properties in the abstract with no
  live artifact to drive (check-colors, focus-verify, i18n-verify, perf-verify, safety-verify —
  this skill drives what they reason about); NOT for launching the app itself (the `run` skill,
  where installed); NOT for the whole-product sweep (ui-audit).
disable-model-invocation: false
user-invocable: true
---

# ui-change-verify

A UI change is not done because the edit applied and the type-check passed — it is done once the
change was seen working, the way a human reviewer would check it. This skill is the enforcement:
never hand back a UI change without having driven it live.

## Procedure

1. Launch the app via the `run` skill where installed; otherwise start the project's own dev
   server (its `package.json` dev script, or the project's documented run command).
2. Open the changed surface and interact with it directly — click the button, submit the form,
   trigger the state change — matching exactly what a human would do to confirm the change, not
   merely load the page.
3. Screenshot the before and after states for anything visual. A change with no observable state
   difference is itself a finding, not a pass.
4. Check the browser console: zero new errors or warnings introduced by this change is the bar,
   not "the app still renders."
5. Where the change affects load or interaction cost, run this plugin's `perf-verify` dimensions
   against it (or a performance trace via whatever tooling the project has); where it affects
   focus, keyboard, or contrast, run `focus-verify`'s / `color`'s equivalents. This skill drives
   the artifact; those skills own the pass/fail bar for what it's measured against.

## Family mechanics (canon: [[ui-audit]]'s `references/verify-mechanics.md` — cited, not restated)

- **Scope declaration:** the verdict header names the scope driven — this change's surfaces (the
  default), a single interaction, or "route to [[ui-audit]]" when the change's blast radius is
  the whole product. A whole-product sweep to bless a one-line fix, or a one-element check to
  bless a cross-surface change, are both scope mismatches (canon §2).
- **Monotonicity:** after any fix this verification drives, re-run the SAME steps at the SAME
  scope — the addressed findings gone AND none new (a new console warning after the fix blocks
  exactly like the original). A verdict without the post-fix re-run is a prediction (canon §3).
- **Blast radius (repair scope):** the verdict carries what the fix touched vs what the finding
  named; an unrelated refactor riding the fix is its own finding — `family.repair-scope`
  (canon §4).
- **Findings format:** `file:line — [RULE_ID] finding → fix`; composed dimensions keep their
  owning verifier's IDs (a focus defect found here cites focus-verify's rule names).

## Output contract

```
Scope: <this change's surfaces | single interaction | routed to ui-audit>
Findings: <file:line — [RULE_ID] finding → fix>   (owning verifiers' IDs; this skill's own:
  `change.no-observable-diff` · `change.console-regression`)
Blast radius (when a fix occurred): <files/surfaces touched> vs <what the finding named>
Evidence: <screenshots · console log · trace — as the change type warrants>
Verdict: <verified | NOT verified: why | UNMEASURED: what's missing>
```

## Failure branches

- The app won't start → report the blocker; do not report the change as verified from source
  reading alone.
- A console error or warning appears → fix and rerun from step 1; a change with unexplained new
  console output is not done.
- No way to observe the change (no browser access, no display) → mark verification UNMEASURED and
  say so plainly; never report "done" on an edit that was never driven.

Done when the change was driven live, before/after evidence exists (screenshot, console log, or
trace, as the change type warrants), no new console error or warning was introduced, and any fix
made along the way got its same-scope re-run with nothing new introduced. NOT done
when a change is reported complete from a successful edit, a passing type-check, or a test suite
alone with no live interaction — those verify code, not the product a user touches.
