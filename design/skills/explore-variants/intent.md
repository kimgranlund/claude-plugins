# intent — explore-variants

Forged 2026-08-19 from a design conversation with kim (gen-ui-kit marshal session); slots filled
from that agreement, confirmed in one round rather than a 7-turn interview.

## Slots

- **Trigger (verbatim):** "explore variants of this component" · "show me variants of X" ·
  "give me 5 takes on this layout" · "let's iterate on this design" · "variant exploration" ·
  a pasted JSON blob whose first key is `"schema": "variant-feedback/v1"` (resume mode).
- **Behavior delta:** today Claude produces one design, or several ad-hoc unlabeled takes with no
  structured feedback channel — the user's reactions arrive as prose the next round can't act on
  precisely. With the skill: N variants that differ along DECLARED axes, in ONE stable-URL
  artifact, each card carrying a 👍/👎 + free-text widget; the page serializes a versioned JSON
  block the user copies back; the skill's resume mode consumes that JSON and regenerates the same
  URL — anchors kept, rejected axes mutated — until convergence.
- **Species + dials:** procedural. `user-invocable: true` (/explore-variants),
  `disable-model-invocation: false` (model-routed from the trigger phrasings above).
- **Freedom:** HIGH on visual design of variants (artifact-design governs craft); LOW on the
  feedback contract (schema fixed at variant-feedback/v1), LOW on ID discipline (axis-derived,
  stable across rounds), LOW on the one-artifact-per-exploration rule (republish same path).
- **Type/home:** design plugin (`design/skills/explore-variants/`), kimgranlund/claude-plugins.
- **Fences:** NOT for producing one finished design or a hand-editable canvas (`design` canvas
  skill / artifact-design); NOT for judging an existing artifact or component
  (design-system-checker / screens:component-checker); NOT for building the chosen winner
  (screens:make-component or the host repo's build skills — this skill ends at a winning spec).
- **Done-when:** artifact renders N axis-labeled variant cards with working vote+note widgets in
  both themes; the JSON block live-updates and copies; a pasted variant-feedback/v1 blob
  regenerates round N+1 at the SAME URL with anchors preserved; unvoted ≠ downvoted in the
  serialization.

## Gates

- P0: PASS 2026-08-19 — skill (on-demand judgment procedure; not hook/entry/agent).
- P1: PASS 2026-08-19 — record confirmed by kim (interactive confirm, this session).
- P2: PASS 2026-08-19 (ticket #750) — `evals/evals.json`: 22 cases (11 trigger incl. the 5
  verbatim phrasings + the JSON-paste resume trigger + 5 near-miss/resume paraphrases; 11
  no-trigger fencing the design canvas skill, artifact-design, design-system-checker,
  screens:component-checker, screens:make-component, pick-fonts, and the broadest verbatim
  trigger's own single-design-refinement near-miss). `evals/assertions.md`: 5 behavioral
  assertions. `evals/baseline.md`: documented-delta baseline note (no live fresh-session capture —
  the delta is a structural feedback contract a no-skill run cannot partially have).
  `eval_check.py` clean.
- P3: PASS 2026-08-19 (ticket #750) — `SKILL.md` (86 lines, well under 200) +
  `references/feedback-schema.md`; `user-invocable: true`, `disable-model-invocation: false`
  explicit; description 693/1024 chars (W1), 693/700 (W8 budget).
- P4: PASS 2026-08-19 (ticket #750) — `harness:prompt-wording-rules` Audit + Rewrite applied:
  `potency_lint.py` first flagged prohibitions/NEVER over budget (10/9 vs budgets 5/3); rewritten
  to exactly 3 hard-gate NEVERs (resume-parse guess-parsing, the one-path republish rule, the
  null-vs-downvote invariant), everything else reframed affirmatively. Re-run: all dimensions
  within budget.
- P5: PASS-WITH-NAMED-BLOCKER 2026-08-19 (ticket #750) — `skill_lint.py` clean.
  Fresh-context `skill-checker` (UNNAMED, synchronous, generator≠critic): **PASS, 0 blocking**
  (3 minor findings, 2 fixed in this change — an inaccurate evals.json note count/claim, and a
  new n11 fencing "iterate on this design" against single-design refinement; 1 accepted-with-note
  below). `harness:check-routing` run over the FULL design plugin (25 skills, single-judge pass
  per suite — the full 3-judge contested-voting round was not run, named as a scope
  simplification, not silently skipped): 556/575 cases clean. **explore-variants itself scored
  22/22 clean (zero stolen/leaked/dead) and never won a case in any of the other 24 suites** — the
  new menu entry introduced no routing contamination in either direction. 19 pre-existing failures
  surfaced elsewhere (color-space-facts↔color-perception-facts/color-contrast-facts boundary
  noise, make-dscard-kit↔make-design-system, make-stitch-kit↔design-md-rules/make-design-system,
  material-type-facts↔font-token-rules/material-shape-facts, one figma-plugin-facts leak) — all
  pre-date this ticket, are unrelated to explore-variants, and are named here as an out-of-scope
  finding for a separate ticket, not fixed under #750. **NAMED BLOCKER, not fixed here:**
  `explore-variants` FAILS ADR-0011's naming grammar (authorkit `validate.py --scope grammar`:
  "neither object-process ... nor nominal (token 'explore' resolves in no lexicon or vocab)") —
  `explore` is a bare verb with no legal skill-grammar head (not one of the closed
  `check-/make-/file-/lead-/bind-/fork-/sub-` heads), so no manifest registration can fix this
  under the current name; the exemptions array is shrink-only (may never grow) per ADR-0011 §10,
  so this also blocks `release_gate.py`'s G12 naming-audit gate. Nearest structurally-valid
  alternative (informational only, NOT applied): `make-variants` (reuses the existing `make-`
  head this very plugin already uses for `make-palette`/`make-design-system`; needs one new
  ObjectVocab registration for `variant`/`variants`, not yet registered). Kim personally named
  this skill; the rename call belongs to the marshal, not this build — held as a named blocker
  rather than renamed unilaterally.

## Accepted-with-note findings

- Baseline (P2.3) recorded as documented-delta rather than live fresh-session captures — the
  behavior delta is structural (a feedback CONTRACT that cannot exist without the skill), so a
  no-skill baseline trivially lacks it; noted per the challenge rule rather than staged.
- Fence reciprocity (P5.4): CORRECTED as of this build — the intent's original "design-plugin
  skills ship no evals/ suites, recorded N/A" line is stale; design now has eval suites
  estate-wide (25/25 skills, this one included). Reciprocal no-trigger cases were added instead:
  `screens:make-component`'s own evals.json gained n26 (explore-variants' flagship phrasing).
  `design-system-checker` and `screens:component-checker` are AGENTS, not skills — neither
  carries an evals.json in this estate (agents aren't routed by trigger-description suites), so no
  reciprocal case exists to add for either. The built-in design canvas skill and `artifact-design`
  are global/platform skills outside this repo entirely — no evals.json exists to reciprocate
  into for either.
- skill-checker minor findings (2026-08-19): (a) resume-mode trigger depends on the user pasting
  raw JSON into chat — accepted, that IS the contract; (b) clipboard fallback path untestable in
  lint — accepted, runtime concern documented in the body; (c) the positional
  first-top-level-key resume check would silently reroute a reordered-but-otherwise-valid v1 blob
  (e.g. round-tripped through a formatter) as a new exploration rather than resume input — accepted
  with note: presence-and-value-at-top-level loses no anti-guess-parse safety over strict
  positional matching, and no evidence exists that a real user's paste path reorders keys; revisit
  if a reordering case is ever actually reported.
- A worked full-page reference example was suggested for `references/`, deferred — the schema
  reference already carries the load-bearing contract, and the SKILL.md procedure states the
  page-construction steps explicitly.
