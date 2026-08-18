# Eval harness — proving the corpus is valuable, not just rubric-clean

Deliverable (c): eval prompts proving a valuable corpus was extracted. Assert-layer choice per
`docs:agent-harness-rules`: **payload-layer** — the extracted corpus is itself the payload, so the
harness runs a fixed prompt set against it and scores the *answers* through `harvest-core.md`'s
rubric, rather than driving a browser or a human reviewer. This is deliberately the cheaper,
more deterministic layer (`agent-harness-rules`' own trap-naming discipline): a domain-knowledge
corpus's value shows in whether a reader's questions get answered from it, which a payload-layer
Q&A run measures directly without needing any UI or human in the loop.

## Sample project

**This workspace itself** (`kimgranlund/claude-plugins`) — its own brief, IDRs, ADRs, and PRDs
already constitute a rich, known-answer corpus: every fact the harvest should surface has a
ratified, checkable source already sitting in `.claude/docs/`. (This workspace carries no
`ROADMAP`-type record as of this writing — named here rather than silently assumed, per
`extraction-procedure.md`'s own "skipped, not faked" rule: E2's known-answer key below draws on
recurring ADR/PRD subjects alone, not roadmap phase boundaries, until one exists.) A sample
project chosen from outside this workspace would need its own known-answer key authored from
scratch before any eval could run; this workspace already has one. (Rejected alternative: a
synthetic toy project — would need a hand-authored answer key with no independent ratification
behind it, weaker grounding than this repo's own accepted ADRs/IDRs.)

## The eval procedure

1. **Extract**: run this skill's Step 1–6 procedure (`extraction-procedure.md`) against this
   workspace, producing a domain-knowledge corpus.
2. **Ask**: run the fixed prompt set below against the corpus alone (payload-layer — the answering
   agent sees only the corpus text, never the original sources) and record each answer.
3. **Score**: for each prompt, check the answer against the known-answer key (drawn from the
   actual ratified `.claude/docs/adr/`, `.claude/docs/idr/`, `.claude/docs/prd/` records this
   workspace already carries) and against `harvest-core.md`'s R2/R3/R6 — was the answer traceable
   to a real zone, scored on the right axis, sourced.
4. **Report**: a scored report (prompt → answer → correct/partial/wrong → which rubric dimension
   the miss maps to) is the harness for this feature — the report itself, not a human's read of
   the corpus, is the deliverable-c artifact.

## Fixed prompt set (v1 — extend per project as new zones surface)

| # | Prompt | Axis it probes | Known-answer source |
|---|---|---|---|
| E1 | "What business problem does this project solve, in one paragraph a non-engineer would understand?" | Outside-In | the workspace's own brief |
| E2 | "Name the main topic zones this project's domain knowledge breaks into, and why each one is a zone (not just a file)." | Zone discovery (R1) | recurring ADR/PRD subjects (plus roadmap phase boundaries, once one exists — this workspace has none as of this writing) |
| E3 | "For zone X [substitute a real discovered zone], who benefits from it and what would break for them if it were removed?" | Outside-In (R2) | the PRD/brief passage that motivated that zone |
| E4 | "For zone X, what does it actually do mechanically, and what does it depend on?" | Inside-Out (R3) | the ADR/implementation passage for that zone |
| E5 | "Which zone does this corpus treat as most business-critical, and how is that ranking computed?" | Weighting (R5) | the weighted-score ordering from `extraction-procedure.md` Step 4 |
| E6 | "Cite the source for the claim that [a specific fact from the corpus] is true." | Source traceability (R6) | the exact ADR/IDR/PRD passage |

A prompt answered correctly with no traceable source is scored as a MISS on R6 even if the
business content is accidentally right — the eval is checking the corpus's grounding, not merely
whether the answering agent happens to already know the workspace.

## Report shape

```
Project: <workspace root>  ·  Corpus: <path to the produced domain-knowledge doc>
| # | Prompt | Verdict | Rubric dim | Note |
Gate (R1,R4,R5,R7 from harvest-core.md): <pass/fail>
Top misses: 1) … — fix: re-run Step <N> for zone <name>
```
