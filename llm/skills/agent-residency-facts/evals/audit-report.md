# Floor audit — agent-residency-facts

Skill: /Users/kimba/.claude/plugins/marketplaces/nonoun-plugins/llm 0.1.0/skills/agent-residency-facts · Standards: skill-authoring-standards · Lint: clean
Verdict: PASS

Lint verdict line (run 2026-07-20): `skill-postwrite-invocation-lint · clean · .../agent-residency-facts/SKILL.md`

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | pass | — | SKILL.md:27–28 (the check itself), SKILL.md:48–50 (per-axis hybrid rule), SKILL.md:61–68 (workspace routing table) — all three fail the deletion test in the right direction: baselines (evals/baseline/prompt-1:22–24, prompt-3:20–23) show the model produces the abstract content but NOT the named vocabulary, the hybrid rule, or the workspace routing map | — |
| R2 | pass | — | Description phrasings SKILL.md:7–11 match evals.json t01–t05 verbatim; fences SKILL.md:11–14 repel n01 (→guardrails sibling), n02 (→concurrency-design), n05 (→agent-authoring-standards); cross-tier cases t06–t12 covered by "which agent tier does this pattern belong to" + "does this guidance apply to…". Reasoned check only — measured routing is a DEEP-depth M2 gate, not run here | — |
| R3 | pass | — | intent.md:3–4 (knowledge, false/false) = SKILL.md:15–16; name head "taxonomy" is a knowledge noun; dmi:false keeps it preloadable | — |
| R4 | pass (with note) | minor | SKILL.md:27–28, 49–50, 76–77 carry imperatives inside a Knowledge-species body ("name the tier…", "apply the row…", "cite directly"). Steelman recorded: the Knowledge zero-imperative rule's mechanism ("no actor mid-catalog to command") doesn't apply here — there IS an actor at knowledge-harvest time, and the lines are standing instructions in spec-present tense, not one-time steps. Hard-gate budget fine: lowercase `never` at :50 is lock-register; CAPS spent only on **Done/NOT done** (:84–88) and the fence NOTs | Accept as-is; if a future pass wants pure catalog register, recast :27–28 as "A finding is cited only after its observed tier and the target skill's tier are both named" |
| R5 | pass (with note) | minor | The 5-axis table survives as a coverage-forcing enumeration (per-line content is partly model knowledge — prompt-1/prompt-3 baselines reproduce trust-boundary and context-assembly rows — but deleting the TABLE changes which axes get checked and removes the named handles; intent.md:49–55 states this honestly). One drift-pair risk: the Orchestration row (SKILL.md:45) restates concurrency-design mechanics ("no self-resume for background async work once a dispatched subagent's own turn ends") in enough operational detail to drift when that skill's substrate changes | Compress SKILL.md:45 to the classification fact (worktree/subagent dispatch over a shared file tree vs per-conversation backend isolation) and leave the resume-semantics specifics to `orchestration:concurrency-design`, already named at :53 |
| R6 | pass (with nit) | nit | Body 72 lines (~1,000 tokens); the residency check (the gate) at :25–30, incident + worked-example material in the tail — head/tail order correct. `references/` exists but is EMPTY (ls 2026-07-20: zero files) — scaffolding residue | Delete the empty `references/` dir (or land intended content); G2 tolerates the dir but an empty one misleads the next reader |
| R7 | n/a | — | Knowledge species; no output contract owed. The skill volunteers a checkable done/NOT-done predicate anyway (SKILL.md:84–88) | — |
| R8 | pass | — | "five structural axes" (SKILL.md:22) matches 5 table rows (:42–46); routing table 3 Resident + 3 Ephemeral entries (:63–68) exceeds intent.md:37's "at least 2 + 2" floor | — |

## Findings outside the R-grid

| ID | Severity | Evidence | Fix |
|----|----------|----------|-----|
| F1 | **major** | intent.md:38 assertion 4 requires a reciprocal named-mention pointer in `chat-harness-guardrail-facts/SKILL.md`. Runtime check (grep -rn "agent-residency-facts" across the llm skills tree, 2026-07-20): the string appears ONLY in this skill's own SKILL.md and intent.md — the reciprocal pointer does not exist. The boundary is currently one-way: cross-tier asks arriving via the sibling's vocabulary won't route back here. P5 is honestly PENDING (intent.md:46), so this is an unmet acceptance criterion, not a laundered claim | Add the pointer to the sibling's SKILL.md in the P5 pass — and re-budget the sibling's description first if it lands as a fence (standards' re-budget clause) |
| F2 | minor | SKILL.md:29 points a consumer at `evals/baseline/prompt-2-lesson-transfer.md`, and :32 opens with "this session, 2026-07-20" — self-referential deixis in a persistent artifact. The parenthetical at :32–33 ("not independently re-openable — treat as a dated incident report") largely defuses it, and the load-bearing claim ("under real multitasking dispatch load it doesn't reliably fire on its own") survives without the eval pointer | Reword "this session" → "the 2026-07-20 authoring session"; optionally drop the baseline-file pointer and keep the claim |
| F3 | nit | SKILL.md description = 1,001 chars — 23 chars of headroom under the 1,024 portability cap. The next fence (e.g. F1's reciprocal fence, if one is added here rather than in the sibling) forces the predictable trim round-trip | Re-budget before the next description edit |
| F4 | nit | intent.md:56 "(none yet)" sits under `## rulings` directly after a real ruling (:49–55) — template residue contradicting the line above it | Delete "(none yet)" |

## Verified citations (reviewer-discipline rule 2 — runtime over claim)

- `references/sources.md` trust-class-2 claim (SKILL.md:79–82): confirmed — sources.md:13 reads "Observed harness behavior — a real system's stated rule OR a directly-witnessed incident", exactly the widening the body cites. Dismissed as a concern.
- All 6 routing-table owners (SKILL.md:63–68): confirmed present on disk — `forge/*/skills/agent-authoring-standards`, `orchestration/*/skills/{concurrency-design,orchestration-design}` in the plugin cache; `chat-harness-{instructions-and-guardrails,knowledge-and-memory,skills-and-routing}` as llm siblings (ls, 2026-07-20). No phantom targets; dismissed.
- Lint-clean claim from the dispatch: re-run for real (verdict line above), not taken from the handoff.

Top 3: 1) F1 — add the reciprocal pointer in `chat-harness-guardrail-facts/SKILL.md` at P5 (the only major). 2) R5 — compress the Orchestration axis row to the classification fact; leave resume-semantics detail to `concurrency-design`. 3) F2 — fix the "this session" deixis before the incident note outlives its author-session context.
