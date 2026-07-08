---
name: ui-change-verify
description: >-
  Verify a UI change end-to-end against the running artifact before declaring it done — start the
  app, interact with the change directly, screenshot before/after, check the console, and audit
  performance. Use when the user asks to verify, check, or confirm a UI change — a new control, a
  layout edit, a style change, "is this button working", "did that fix the layout", "verify this
  UI change" — or whenever about to report a frontend change complete. NOT for reasoning about a
  UI's properties in the abstract with no
  live artifact to drive (focus-verify, i18n-verify, perf-verify, safety-verify — this skill drives
  what they reason about); NOT for launching the app itself (the `run` skill, where installed).
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

## Failure branches

- The app won't start → report the blocker; do not report the change as verified from source
  reading alone.
- A console error or warning appears → fix and rerun from step 1; a change with unexplained new
  console output is not done.
- No way to observe the change (no browser access, no display) → mark verification UNMEASURED and
  say so plainly; never report "done" on an edit that was never driven.

Done when the change was driven live, before/after evidence exists (screenshot, console log, or
trace, as the change type warrants), and no new console error or warning was introduced. NOT done
when a change is reported complete from a successful edit, a passing type-check, or a test suite
alone with no live interaction — those verify code, not the product a user touches.
