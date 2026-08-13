# Calibration — load-bearing vs. hand-holding

The test: **would cutting this lose a real instruction, or only its
retelling?** Apply it per flagged section, not per file — a file can be
long and still earn every word.

## Keep (load-bearing, do not flag)

- A dated, specific incident a capable model couldn't infer ("a combined
  `gh issue create --type` call was found to create the issue and only
  then silently fail the type step") — the LESSON is non-obvious; state it
  once, briefly, where it's cited.
- A safety-critical prohibition ("never `-D` a branch even after a
  verified-clean check").
- A convention that differs from the language/tool default — the model
  would guess wrong without being told.
- A short worked example that's the ONLY one — it teaches the pattern.

## Flag (hand-holding a capable model doesn't need)

- **Ceremony for a judgment call.** A multi-phase breakdown of "audit, get
  it approved, execute in order, write down what you learned" — a capable
  model produces this shape itself from a two-sentence brief. Worked
  example: `harness/skills/clean-repo/SKILL.md` compressed 7 named phases
  into "audit before touching anything, get destructive moves ratified,
  distill lessons after" with no loss.
- **Restatement across siblings.** The same paragraph copied into 3 files
  instead of stated once and cited — `measure.py`'s duplicate-pair output
  (Jaccard ≥ 0.5 on 8-word shingles) catches this mechanically. Worked
  example: docs' file-bug/file-feature/file-task shared the backend-seam
  paragraph verbatim while each claimed a "canonical statement" pointer it
  didn't actually use.
- **A second retelling of the same worked example.** One example teaches
  the pattern; a second and third narrate the same lesson in different
  words.
- **Boilerplate present out of habit.** A "Failure branches" or "Done/NOT
  done" section that restates the procedure just above it in a different
  grammatical register, rather than adding a genuinely new edge case.
- **A meta-framework for something the model does by default.** A named
  taxonomy + escalation protocol + anti-pattern table to teach "match
  effort to stakes" — the instruction is one sentence; the rest is naming
  ceremony around it.

## When unsure

If a flagged section cites a real, dated, specific incident anywhere in
it, keep the citation and cut the narration around it. If it cites
nothing and restates a rule already stated elsewhere in the same file,
flag it.
