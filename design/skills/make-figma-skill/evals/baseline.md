# Baseline — what a no-skill session does today (2026-08-27)

Documented-delta baseline (the same shape make-variants used): the delta here is a
structural contract a no-skill run cannot partially have, so the baseline is the observed
failure class rather than three captured transcripts.

Prompt: "convert design/skills/make-figma-make-kit into a Figma custom skill"

Without this skill, a fresh session:
- Produces a SUMMARY of the source (~80 lines), keeping the heading names but dropping the
  reference files' content entirely — `references/format.md`, `gates.md`, `rubric.md` are
  cited by path, not inlined (Figma has no `references/`, so every citation is dead).
- Keeps `disable-model-invocation`/`user-invocable` in the frontmatter.
- Rounds or drops thresholds ("good contrast" for `4.5:1`).
- Leaves "run `scripts/make_guidelines_check.py`" as an instruction the Figma agent cannot
  execute.
- Writes the file wherever it likes without asking.
- Has no notion of `## Dropped` or `## Provenance`, so the export cannot be regenerated or
  diffed later.

With this skill the same prompt produces one file that passes `figma_skill_check.py --source`
(F6 measured), with every reference inlined whole, every script transposed to an
observable checklist, and a receipt. The Phase-5 behavior check re-runs this prompt in a
fresh session with the skill installed and compares against `assertions.md`.
