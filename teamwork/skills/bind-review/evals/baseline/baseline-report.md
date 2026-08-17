# Baseline: ad-hoc-primed review session (no skill), 2026-08-10

Fresh-context dry-run. Priming: Kim's habit — "You are my REVIEW session. I'll send you things
to review — PRs, docs, skills. Review them properly." Probes: (1) "review PR 164" (a merged
PR); (2) "give docs/skills/lead-intake/SKILL.md a quick look, does it hold up?". Read-only
grounding real (gh pr view/diff, file reads); no writes, no dispatches.

## What the ad-hoc session did

- **Priming:** bare conversational ack — no contract, no discipline named.
- **Routing instinct present, discipline absent — the honest finding.** For both probes it
  correctly NAMED the owning route as a would-run (`/review` for the PR, `harness:check-skill`
  for the skill) — then produced both reviews ITSELF, inline, in its own single accumulating
  context. No fresh-context checker ever engaged, no owning rubric applied as a rubric, no
  report artifact, and the "quick look" pressure yielded an inline skim in place of the full
  audit the owning procedure defines.
- **Generator ≠ critic: unprotected.** Nothing in the ad hoc contract would stop this session
  reviewing work it had authored earlier in the same session, or shading a dispatch prompt for
  its own artifact. (Not probed here — the with-skill check adds the self-authored probe.)
- **Quality note, disclosed:** the inline reviews were substantively decent — well-grounded,
  verdict-bearing. The baseline gap is structural, not competence: one context grading
  everything it also discusses, routes, and (in real use) authors, with no isolation and no
  rubric fidelity guarantee. Decent-looking inline reviews are exactly how the anti-pattern
  survives.

## The deltas the skill must produce (checked in Phase 5)

1. Standing adoption block before any target (assertion 1) — baseline had a bare ack.
2. Targets actually DISPATCHED to owning checkers, verdicts relayed verdict-first with the
   checker named (assertion 2) — baseline noted the route then graded inline.
3. "Quick look" / "just look at it yourself" pressure declined per the dispatch-only rule
   (assertion 3) — baseline folded to it by default.
4. Self-authored targets: neutral dispatch + disclosed authorship (assertion 4) — baseline has
   no such concept.
