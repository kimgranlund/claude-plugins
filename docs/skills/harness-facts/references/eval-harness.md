# Eval harness — proving the artifacts improve agent task performance, not just rubric-clean

Deliverable (c), this corpus's own version: a **WITH-vs-WITHOUT delta** run — genuinely different
from the sibling's single WITH-only Q&A design, because this corpus's consumer is a coding agent
whose harness either measurably helps or it doesn't; answerability of a prose corpus (the
sibling's own test) doesn't prove that a set of harness artifacts *improves* anything. Assert-layer
choice per `docs:agent-harness-rules`: **payload-layer** — the artifacts and the prompt/answer are
all text; a Q&A/task run against them measures value directly, no browser or human reviewer
needed.

## Sample project

**This workspace itself** (`kimgranlund/claude-plugins`) — same reasoning as the sibling's
`eval-harness.md`: this workspace's own `CLAUDE.md`, `.claude/rules/*.md`, and ratified ADRs
already constitute a known-answer key with no separate answer-key authoring needed. (Rejected
alternative, same as the sibling's: a synthetic sample project — would need a hand-authored answer
key with no independent ratification behind it.)

## The eval procedure

1. **Extract**: run this skill's Step 1–6 procedure (`extraction-procedure.md`) against this
   workspace, producing the staged artifact set (the four classes + run manifest,
   `output-artifacts.md`) at a staging path.
2. **Ask, twice**:
   - **WITHOUT**: a fresh answering context receives ONLY the bare F-prompt below — nothing else.
     No workspace `CLAUDE.md`, no `.claude/rules/`, no ADRs, no staged artifacts.
   - **WITH**: a fresh answering context receives the same bare F-prompt PLUS the staged artifacts
     from step 1 (never the workspace's own live entry files or rule tree directly — only what
     this run emitted).
3. **Score** each answer, in both arms, against the known-answer key (this workspace's own live
   `CLAUDE.md`, `.claude/rules/*.md`, and ratified ADRs — read by the SCORER, never by the WITHOUT
   answering context) and against `harvest-core.md`'s R3/R5/R6 dimensions, mapped per-prompt below.
4. **Report** the delta: WITH verdict vs WITHOUT verdict per prompt, the rubric dimension each maps
   to, and whether WITH strictly beat WITHOUT — this delta report, not a human's read of the
   artifacts, is the deliverable-c harness for this feature.

**CRITICAL isolation rule (R-4).** The WITHOUT arm's answering context must NEVER see this
workspace's own live `CLAUDE.md` or `.claude/rules/` files (or the staged artifacts) — only the
bare prompt. A WITHOUT answer that cites a source it was never given (quoting a `CLAUDE.md` line,
naming a rule file it couldn't have seen) invalidates that run — re-run it in a genuinely clean
context, don't just discard the citation and keep the score. This mirrors the sibling's own rule
(an answer that's accidentally right with no legitimate path to the answer is still a MISS on R6,
not a pass) — here it's stronger: it INVALIDATES the run, because contamination in the WITHOUT arm
poisons the entire delta the eval exists to measure.

## Fixed prompt set (v1 — extend per project as new zones surface)

| # | Prompt | Known-answer source | Rubric dim (operational) |
|---|---|---|---|
| F1 | "Which single command must pass before a plugin in this workspace can ship, and what does it check?" | `CLAUDE.md` Invariants, "Ship only through the gate" (`release_gate.py <plugin-root> --package`) | R3 mechanism — the answer must name the literal command, not just gesture at "there's a CI check somewhere" |
| F2 | "Where does a new work item's record live in this workspace, and what decision put it there?" | `CLAUDE.md` Invariants, "Work items are GitHub Issues in this workspace (ADR-0002)" | R6 traceability — a correct location with no ADR-0002 citation still scores a miss |
| F3 | "Which rule file governs an edit to a SKILL.md's model-invocable description, and what must ride along with that edit?" | `.claude/rules/plugin-authoring.md` ("Descriptions are the routing surface…") | R3 mechanism — must name the exact file, not paraphrase "there's probably a routing rule somewhere" |
| F4 | "Where does a multi-session campaign's git worktree live in this workspace, and is that path tracked by git?" | `CLAUDE.md` routing table, "campaign" row (`.claude/worktrees/`, gitignored) | R6 traceability — must trace to the routing-table row, not infer a generic worktree convention |
| F5 | "What does bumping a plugin's version number actually gate, mechanically, in this workspace's update flow?" | `CLAUDE.md`, "the version is the update cache key" / `.claude/rules/dist-output.md` | R5 weighting-visible — a WITH answer proves the corpus surfaced this as entry-file-grade (always-true, project-wide) truth; a WITHOUT answer has no way to know this is entry-file-grade at all |
| F6 | "Which command owns creating or growing a knowledge pack in this workspace, and what unit of work does it run per invocation?" | `CLAUDE.md` routing table, "Fill or grow a knowledge corpus" row (`/make-pack`, one axis per wave) | R5 weighting-visible — same test as F5: whether the artifact surfaced this prominently (routing-table-grade) rather than only as a buried pack-seed footnote |

## Report shape

```
Project: <workspace root>  ·  Rubric: harvest-core (harness-facts weighting: Inside-Out 60/Outside-In 40)
Staged artifacts: <staging path from the extract step>
| # | Prompt | WITH verdict | WITHOUT verdict | Delta | Rubric dim | Note |
Gate (R1,R4,R5,R7 from harvest-core.md): <pass/fail>
Eval verdict: WITH <beats/does not beat> WITHOUT — <n>/6 prompts improved, <n> unchanged, <n> regressed
Top misses: 1) … — fix: re-run Step <N> for zone <name>, or re-stage artifact class <N>
```

A prompt where WITH does not strictly beat WITHOUT is a top miss even if WITH scores "correct" in
isolation — the eval's own acceptance criterion (LLD Resolution 4) is the delta, not a WITH-only
pass.
