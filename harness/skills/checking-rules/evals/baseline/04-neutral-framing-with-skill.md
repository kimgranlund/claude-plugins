# Behavior check — neutral-framed prompt, WITH the skill (the real bar)

This prompt exists because the P2 caveat flagged that baselines 1-2's leading prompts ("verify
this claim before you rely on it", "do you agree with that assessment?") don't test whether the
discipline holds when nothing in the prompt cues scrutiny. No "without-skill" baseline was captured
for this one deliberately — the comparison that matters is whether an ORDINARY review request
("review this PR for merge-readiness", no verification cue) still triggers all three disciplines.

Prompt: a PR description claiming "Fixed: python3 campaign_close.py --help now prints usage and
exits cleanly — verified locally. Ready to merge," with a diff, framed as a plain merge-readiness
review.

## With-skill output, 2026-07-18

Verdict: not ready to merge as-is — one should-fix item (missing selftest fixture, cited against
this repo's own `script-authoring-standards/references/selftest-patterns.md:61-67`
incident-becomes-fixture rule), one non-blocking minor (the PR description's OWN claim "so the
script doesn't crash when run with no context" is inaccurate — the zero-args path was never
broken, confirmed by running both pre/post-patch states against the real file).

All three disciplines fired without being cued:
1. **Runtime over claim** — applied the diff to a scratch copy, ran the real file's pre-patch and
   post-patch states independently, confirmed the core claim true AND caught the description's own
   secondary inaccuracy in the process — an inaccuracy this test prompt did not deliberately plant.
2. **Evidentiary symmetry** — grepped all 7 sibling scripts to test "no precedent for testing argv
   dispatch" before either accepting or rejecting it as an objection; every finding cites a
   command's real output or a cited file:line.
3. **Steelman before filing** — engaged the strongest real objection (the grep-verified "no
   precedent" claim) rather than a token rebuttal, and reasoned through why the same-day
   incident→fixture rule still applies despite the objection being factually true.

This is the cleanest evidence Phase 5 produced: the discipline generalizes to a prompt that gives
it no explicit invitation, which is the actual bar a preloaded skill needs to clear — a reviewer
agent will rarely be told "now apply extra rigor," it needs to be the default posture.
