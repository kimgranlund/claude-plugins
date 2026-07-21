# Behavioral assertions — make-dscard-kit (authoring run)

Inherited from design-md-author (Claude Design, 2026-07-08) at its synthesis merge into this
skill; the assertions are the behavior contract for the corpus→bundle authoring path. Compare a
with-skill run against a baseline (no-skill) run on the same corpus. All four must hold.

1. **Frontmatter is normative and complete.** The output DESIGN.md opens with YAML frontmatter in
   which every color role carries a `-dark` sibling, every typography level sets size + lineHeight
   (unitless) + weight together, and spacing/rounded are closed ladders. Baseline runs typically
   emit prose-only files or hex lists without scheme pairs.
2. **Root Brand Architecture is captured, not skipped.** The file contains committed lines for
   values, voice, visual territories, and cultural references — each with a design consequence,
   not adjectives. Baseline runs jump straight to tokens.
3. **The file reads as instructions.** The opening line addresses the consuming agent ("Read this
   file as your instructions" or equivalent), and an agent work-order section exists near the
   tail. Baseline runs read as documentation *about* a system.
4. **Fences hold.** Zero framework names (React, Svelte, Vue, Tailwind) appear as prescriptions;
   accessibility numbers appear only as measured, count-exact disclosures in the receipt, never as
   "must meet WCAG" gates.
