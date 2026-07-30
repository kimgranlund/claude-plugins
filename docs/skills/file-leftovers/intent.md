# intent — file-leftovers
status: shipped          # PR #120-era, docs 1.1.0, judged 44/44, 2026-07-30
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium (sweep is judgment over the transcript; minting is delegated to the file-* siblings)
type: capability-uplift

## trigger
should:      ["sweep this chat for leftover work", "ticket everything we didn't get to",
              "did we drop anything this session — turn it into tickets",
              "roll up everything we mentioned but never did into tickets",
              "file the leftovers", "/file-leftovers",
              "make tickets for all the loose work from this conversation"]
should_not:  ["anything still open or unanswered? (find-open-questions — decisions, no tickets)",
              "file a bug for this crash (file-bug — one known item)",
              "what should I work on next (chore-planner)",
              "wrap up this session (close-session)",
              "what's the state of the project (check-state — repo evidence, not conversation)"]

## delta
Proven live 2026-07-30 (evals/baseline/seeded-leftovers.md): the no-skill baseline, given a
synthetic "we talked about a login bug, CSV export, retry policy" prompt, MINTED THREE REAL
ISSUES (#114–#116) into the live backlog — placeholders with fabricated framing, "details
lost with session context", no approval gate, no evidence quotes. All three closed same-day
as test artifacts. The skill's table-then-approve contract and no-quote-no-candidate rule
exist to make exactly this impossible.

Without the skill, "ticket everything we left on the table" yields a prose list and at most an
ad-hoc `gh issue create` or two: no bug/feature/task classification, no dedupe against the
existing backlog, no owner routing through the intake contracts, and clarifications asked as
open prose questions instead of one batched round. Desired: one evidence-quoted candidate table
→ one AskUserQuestion round → every approved item minted through its owning file-* skill,
ending in orchestratable ticket ids.

## fences
- NOT for conversational decisions needing no ticket (find-open-questions)
- NOT for a single already-known item (file-bug / file-feature / file-task directly)
- NOT for prioritizing the backlog (chore-planner)
- NOT for session wrap-up verification (teamwork close-session)
- NOT for repo work-state evidence (harness check-state — repo, not conversation)

## assertions
1. The report's first block is the candidate table; every row carries a verbatim (≤15-word) evidence quote from the session and a proposed kind (bug/feature/task/question).
2. Clarifications arrive as exactly ONE AskUserQuestion round (multi-question allowed), never open prose questions scattered through the reply.
3. No ticket is minted before the user approves the table; minting goes through file-bug/file-feature/file-task (no raw `gh issue create` in the transcript).
4. An empty sweep says so explicitly ("no leftovers — everything mentioned was addressed, ticketed, or dropped") instead of inventing items.
5. The closing report lists minted ids with their kinds, plus discarded items with one-line reasons.

## gates
P0 route:      PASS 2026-07-30 — judgment sweep over conversation + gated minting; not a hook (no pass/fail function over a transcript), not entry-file (on-demand), not an agent (a subagent cannot see this session's conversation — the sweep MUST run in the host context)
P1 intent:     PASS 2026-07-30 — all slots from the user-agreed design; name file-leftovers user-approved (AskUserQuestion; 'sweep'/'extract' are retired registry synonyms, file owns intake)
P2 evals:      PASS 2026-07-30 — evals.json 10t/10n clean; 5 assertions; 2 baselines (one of which minted 3 real placeholder issues — the delta incident)
P3 draft:      PASS 2026-07-30 — SKILL.md procedural skeleton, both dials explicit, 100 lines
P4 language:   PASS 2026-07-30 — potency lint within budget after domain-vocabulary rephrase (the counter caught the skill's own subject words); one uppercase NEVER spent on the mint gate
P5 validate:   PASS 2026-07-30 — skill_lint + eval_check clean; FLOOR audit zero blocking, 3 minors fixed; behavior check FAILED then passed: with-skill v1 minted #117–#119 headless (approval gate in a tail branch didn't bind) → gate moved to Phase 4's head as the body's NEVER → v2 delivered the table, 0 minted, question row offered resolve-vs-ticket; fences closed six-way, suites compact-appended; blind judges on file-leftovers + find-open-questions at the wave boundary (results in PR)

## rulings
- 2026-07-30: docs plugin ownership — this is intake, the file-* family's home; the fourth sibling.
- 2026-07-30: P0 note worth keeping — the sweep cannot be delegated to a subagent or fork: only the host context holds the conversation. The body must state this so nobody "optimizes" it into a dispatch.
