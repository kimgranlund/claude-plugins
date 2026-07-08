# intent.md — design-md-format

Forged via skill-forge (adapted run inside Claude Design; see design-md-author/intent.md for environment notes).

## Record
- **Trigger:** questions about / work on the DESIGN.md design-system spec format — reading, explaining, extending, validating, or supplying ground truth during an authoring run.
- **Behavior delta:** without this skill Claude improvises the format from prior art — it misses the token grammar, the -dark sibling requirement, the pairing law, the receipt/disclosure culture, and above all the file's identity as an open-ended prompt (a SKILL for a brand), not documentation.
- **Species + dials:** knowledge skill with `references/` corpus; model-invocable (auto-triggers), `user-invocable: true`.
- **Freedom:** low — the corpus is normative; the skill teaches, it does not redesign the format.
- **Type:** knowledge; writes nothing by itself.
- **Fences:** NOT for running the end-to-end authoring workflow (design-md-author); NOT for consuming a finished design system to build UI; never framework-prescriptive; accessibility is disclosed, never enforced.
- **Done-when:** answers about anatomy/grammar/architecture are grounded in the corpus files, and an authoring run that preloads this skill needs no external format references.
- **Audience:** public distribution — assume no context.

## Gates
- P0 route: PASS — on-demand knowledge → skill. 2026-07-08
- P1 interview: PASS — shared interview with design-md-author. 2026-07-08
- P2 evals: PASS — 20 trigger evals in evals/evals.json incl. near-miss no-triggers + fence reciprocals. 2026-07-08
- P3 draft: PASS — corpus authored (4 reference files), not an empty shell (skill-forge knowledge-species note satisfied without a pack-forge round: the ground truth was supplied in-conversation via uploads/DESIGN.md, tokens.json, README.md). 2026-07-08
- P4 language: PASS — manual instantiation pass. 2026-07-08
- P5 validate: PASS-with-note — no lint script (accepted); fence closure reciprocated in design-md-author/evals/evals.json. 2026-07-08
