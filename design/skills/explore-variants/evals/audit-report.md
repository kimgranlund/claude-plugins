# check-skill audit — explore-variants (FLOOR)

Skill: /private/tmp/claude-501/-Users-kimba-Projects-nonoun-plugins/c19ebefb-c531-4a92-a485-715a44593df1/scratchpad/explore-variants-750/design/skills/explore-variants · Standards: skill-writing-rules · Lint: clean
Verdict: **PASS** (0 blocking, 0 major, 3 minor, 2 nit)

Reviewed 2026-08-19 for ticket #750. Depth: FLOOR (fresh draft). The known ADR-0011 grammar
failure on the name `explore-variants` is separately tracked and NOT re-flagged here per the
dispatch; checked for secondary damage — none found (F9 dir==frontmatter `name` match confirmed
by skill_lint clean; description and body use the name consistently).

## Mechanical gates (run live, not assumed)

- `skill_lint.py SKILL.md` → `skill-postwrite-invocation-lint · clean` (re-run, not trusted from dispatch)
- `potency_lint.py SKILL.md` → `-- within budget --` (vague quantifiers 2/3, hard-emphasis 0/3; re-run from harness/skills/prompt-wording-rules/scripts/)
- `eval_check.py evals/evals.json` → `eval_check · clean`
- Description: 693 chars ≤ 1,024 open-standard cap (measured). Hard gates: exactly 3 NEVERs (SKILL.md:46, 69, 74) — at the ≤3 ceiling, all catastrophic-tier, spent well.

## Criterion table

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | PASS | — | Sampled: stable-id derivation (SKILL.md:31-33), clipboard fallback chain (SKILL.md:42-44), null-vs-down failure branch (SKILL.md:73-74). Each fails the deletion test in the right direction — output would differ without it | — |
| R2 trigger fidelity | PASS w/ minor | minor (F3) | Description SKILL.md:6-8 carries 5 verbatim trigger phrasings + the JSON-paste resume clause; fences in parseable `NOT for <thing> (<owner>)` form (SKILL.md:8-11). But see F3: "iterate on a design" overlaps single-design refinement | Add the missing negative case (F3) |
| R3 species/dials | PASS | — | Procedural species; `disable-model-invocation: false` + `user-invocable: true` both explicit (SKILL.md:12-13); verb-head name consistent with procedural species (grammar-parse failure separately tracked, excluded here) | — |
| R4 register | PASS | — | Standing spec-present tense throughout ("The page keeps a live … block in sync", SKILL.md:40-41; "Done when …", SKILL.md:76-79); 3 hard gates, at the cap not over it | — |
| R5 no restatement | PASS w/ nit | nit (F5) | Visual craft deferred to `artifact-design` by name (SKILL.md:22-23, 39, 86); schema owned by references/feedback-schema.md and pointed at, not copied (SKILL.md:32-33, 42, 50) | See F5 |
| R6 position | PASS | — | 88-line body, whole file inside the first-5,000-token window; procedure and failure branches ahead of the Material table; references one level deep | — |
| R7 contracts | PASS w/ nit | nit (F4) | Failure branches present (SKILL.md:66-74); checkable stopping predicate ("Done when …", SKILL.md:76-79, plus termination step SKILL.md:52-54). Handoff-spec shape underspecified (F4) | See F4 |
| R8 quantities | PASS | — | "2-4 design axes" and "2-3 values per axis" (SKILL.md:27-28); three vote states enumerated (SKILL.md:37-38); N >= 2 anchored in evals/assertions.md:7 | — |
| DM gate | N/A | — | No subagent/fork/dispatch content in body or frontmatter; `context:` absent. Out of scope by the gate's own trigger condition | — |

## Cross-file consistency (SKILL.md ↔ references/feedback-schema.md)

- **Stable-id derivation**: identical contract both places — join chosen values in declared axis
  order (SKILL.md:31-32 vs feedback-schema.md:39-43, same `compact-sharp-quiet` exemplar). Consistent.
- **Null-vs-downvote invariant**: consistent and mutually reinforcing — SKILL.md:73-74 (hold like
  an anchor, never read as downvote) matches feedback-schema.md:44-48 and the resume-mode read at
  feedback-schema.md:60-61 ("held fixed exactly like an anchor, but never cited as evidence FOR").
  assertions.md:22-25 checks exactly this. No contradiction found.
- **Exhaustive-verdicts rule**: feedback-schema.md:33-34 and :49-50 agree; SKILL.md doesn't
  contradict. (Eval t11's `"verdicts": []` blob is a routing-trigger fixture, not a contract
  exemplar — acceptable, it tests the paste-detection predicate only.)
- **Resume predicate**: "first top-level key is literally `\"schema\": \"variant-feedback/v1\"`"
  stated identically in description (SKILL.md:8), body (SKILL.md:48-49), and
  feedback-schema.md:51-53. Internally consistent — but see F2 on the predicate itself.
- **Termination**: pick-or-all-up stated identically (SKILL.md:52-54, feedback-schema.md:65-67). Consistent.

## Findings (triaged)

### Blocking

None.

### Accepted-with-note (fix before ship where cheap; none blocks)

**F1 · minor · evals.json:3 — suite annotation's arithmetic and sibling claim don't match the cases.**
The note claims "5 verbatim trigger phrasings + 1 JSON-paste resume trigger + 6 near-miss
paraphrases" = 12 positives; the file has 11 (t01-t05 verbatim, t06 JSON paste, t07-t10 paraphrases,
t11 resume+pick — i.e. 5 paraphrase-family cases, not 6). The note also claims "two adjacent
design-plugin skills (pick-fonts, make-palette) as a sibling-neighborhood check" — grepped the
cases: pick-fonts is fenced (n10, evals.json:117-121), **no make-palette case exists**. Runtime
over claim: the annotation is falsified by its own file. Fix: correct the count to 5, and either
add the make-palette negative (e.g. "build a 5-step OKLCH palette from our brand blue") or drop
the claim from the note.

**F2 · minor · SKILL.md:8, SKILL.md:48-49, SKILL.md:68-69; feedback-schema.md:51-53 — the resume
predicate is positional ("first top-level key"), which false-rejects reordered valid blobs.**
A user who round-trips the copied JSON through any tool that re-serializes keys (a formatter, a
notes app, jq) can hand back a semantically valid v1 blob whose `schema` key is no longer first;
the stated failure branch (SKILL.md:68-69) then silently reroutes it as a *new* exploration,
discarding every anchor. Steelman (its author's rebuttal): the skill generates the block itself
and clipboard copy preserves order, so first-position holds in the happy path, and strictness is
the anti-guess-parse point. The rebuttal half-survives: strictness against *unversioned or
differently-shaped* blobs is right and stays — but checking key *presence + exact value*
(`obj["schema"] === "variant-feedback/v1"` at top level) loses zero safety versus checking
position, while deleting the false-reject class. Fix: change the predicate to
presence-and-value in all four locations; keep the never-guess-parse gate for blobs failing it.

**F3 · minor · SKILL.md:7 (description trigger "iterate on a design"); evals.json — no fencing
negative for single-design refinement iteration.**
"Iterate on a design" is the broadest of the five verbatim triggers: "let's iterate on this
design — make the header bolder and tighten the spacing" is a single-artifact refinement that
belongs to the design canvas skill / artifact-design territory the description itself fences
(SKILL.md:8-9), yet lexically it matches this trigger verbatim. The negatives (n01-n03) cover
fresh single designs and doctrine checks but not the *refine-the-one-existing-design* phrasing
that shares the trigger's exact vocabulary — the one near-miss class most likely to grab.
Steelman: t04 legitimately claims the bare "let's iterate on this design" (variant exploration
IS a defensible reading of the bare phrase, and the documented platform bias is
under-triggering). Confirmed to survive for the positive case — the finding stands only as a
missing negative, not as a trigger to remove. Fix: add one negative case pairing the "iterate"
verb with a single named concrete edit, expected no-trigger, noted to the canvas/artifact-design
fence.

### Nits (never block)

**F4 · nit · SKILL.md:52-54 — the terminating "winning spec" handoff has no stated shape.**
Step 7 hands "the winning axis combination as a spec" to the build skill, but doesn't say what
the spec carries (axis/value pairs only? the winning card's notes? the accumulated round
history?). Downstream, `screens:make-component` will parse improvised prose. Fix: one sentence —
e.g. "the spec = the winning id, its axis/value map, and every note attached to it across rounds."

**F5 · nit · SKILL.md:73-74 — the null-vs-downvote rule is stated in both files.**
The failure branch restates the invariant feedback-schema.md:44-48 owns, creating a small drift
pair. Dismission-with-check considered and rejected as a *removal*: the restatement is the
pointer form the standard sanctions (it names the canonical home in the same sentence), and it's
the catastrophic invariant most worth surviving compaction in the head. Keep as-is; noted only so
a future edit to the schema file knows its twin exists.

## Evals coverage verdict

- 21 cases, well-formed (eval_check clean), 11 positive / 10 negative.
- Required trigger set: all 5 description-verbatim triggers present one-to-one (t01↔"explore
  variants of a component", t02↔"show variants of X", t03↔"give N takes on a layout",
  t04↔"iterate on a design", t05↔"run a variant exploration") + the JSON-paste resume trigger
  (t06, first key literally `schema`), plus a second resume-with-pick case (t11). **Complete.**
- Negatives are genuine near-misses, not throwaways: each names its owning fence and uses that
  owner's own vocabulary (n05/n06 explicitly use the checkers' flagship phrasings; n09 is the
  sharpest — a post-pick build ask that mentions "variant" yet must route away). Gaps: F1's
  phantom make-palette claim, F3's missing refine-iteration case.
- assertions.md: 5 assertions, each checkable and each naming its baseline counterpart; matches
  SKILL.md's Done-when clause point-for-point (cards+labels, 3-state vote+note, live copyable
  block, same-URL republish, null-vs-down).
- baseline.md: documented-delta form, honestly labeled as such with the rationale (structural
  contract, no ambiguous middle case). Accepted per the ticket's recorded pattern.

## Top 3

1. **F1** — fix the evals.json annotation: correct "6 near-miss paraphrases" to 5, and add the
   claimed-but-absent make-palette negative or delete the claim (evals.json:3).
2. **F2** — change the resume predicate from "first top-level key" to top-level
   presence-and-value of `"schema": "variant-feedback/v1"` in the description, body (steps 6 +
   failure branch), and feedback-schema.md; keeps the anti-guess-parse gate, deletes the
   reordered-blob false-reject.
3. **F3** — add one negative eval: "iterate" + a single concrete edit to an existing design,
   expected no-trigger (fences the broadest verbatim trigger).

Recommended next action: maker applies F1-F3 (all small, same change), F4 optional one-liner;
re-run eval_check after the evals.json edit. The naming-grammar blocker proceeds on its own track.
