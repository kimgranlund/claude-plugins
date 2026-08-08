# Audit report 2 — mobilize-chores (post task-kind extension)

Skill: /Users/kimba/Projects/nonoun/plugins/teamwork/skills/mobilize-chores/SKILL.md · Standards: skill-writing-rules · Lint: clean
Verdict: PASS

Audited 2026-08-08 at FLOOR depth, fresh context, focused per dispatch on step 5's new
`kind: task` branch (every gh CLI and tool reference runtime-verified, not assumed) and the
fork-vs-agent-gate purge. Prior audit: `evals/audit-report.md` (2026-08-07).

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | Deletion test on 3 load-bearing lines: SKILL.md:43-46 (flattened-form warning — deleting it re-opens the silent "never in flight" misread, re-proven live below); SKILL.md:57-61 (confirm-before-clarify ordering — deleting it licenses pre-confirm `find-intent` rounds the ruling explicitly forbids, intent.md:107-109); SKILL.md:84-93 (Findings write-back + read-back + one re-dispatch — deleting it leaves task dispatches with no verifiable completion). All three change output if removed. | — |
| R2 | PASS | — | Command species: description never reaches the model (SKILL.md:15 `disable-model-invocation: true`); scored as slash-menu documentation. SKILL.md:3-14 states run form, argument shape, all four fences, and the new task path ("a task ticket runs find-intent… then an Agent dispatch… Findings write-back contract" SKILL.md:8-9) — description updated in the same change as the capability. | — |
| R3 | PASS | — | Command species + `disable-model-invocation: true` + `user-invocable: true` (SKILL.md:15-16) + imperative-verb name + intent.md:3-4 dials all agree. Nothing preloads this skill. | — |
| R4 | PASS | — | 0 uppercase hard gates (`grep -c "NEVER\|MUST NOT"` → 0); load-bearing lines commit ("Nothing dispatches before this round returns" SKILL.md:58, "ambiguity is never a license to dispatch" SKILL.md:108) rather than describe. | — |
| R5 | FAIL | **minor** | (a) SKILL.md:80-81 attributes the null-unit reasoning to `agent-writing-rules`; the concept's home is teamwork's `team-or-solo-rules` (SKILL.md:30 "the host inline is the null unit", references/rubric.md:7). Grep of harness/skills/agent-writing-rules/SKILL.md for null-unit: zero hits. (b) SKILL.md:74 quotes `file-task`'s scope as "chores, follow-ups, docs, decisions"; file-task's own text reads "chores, follow-ups, research items, debts" (docs/skills/file-task/SKILL.md:17-18) — a colon-list presented as the source's own words that the source doesn't say. Same misquote propagated at intent.md:104. | (a) Cite `team-or-solo-rules` (same plugin — better than the cross-plugin cite anyway). (b) Match file-task's actual list or drop the quote-shaped colon list. |
| R6 | PASS | — | Body 127 lines (~1,600 tokens), entirely inside the compaction-survival head; no references/ needed. | — |
| R7 | PASS | — | Output contract SKILL.md:96-99; six named failure branches SKILL.md:101-115 including both new task branches (still-unclear-after-round :111-112, no-Findings-on-return :113-115); checkable stopping predicate SKILL.md:117-126, extended for the task path in the same change. | — |
| R8 | PASS | — | ONE batched confirm (:56-57), ONE clarifying round (:76), one re-dispatch (:91), at least one Findings entry before done (:88-89). | — |

## Dispatch focus 1 — step 5 task-kind branch: every command/tool reference, runtime-checked

| Reference (SKILL.md line) | Check performed | Result |
|---|---|---|
| `Skill(harness:find-intent)` reachable via Skill tool (:75) | Read find-intent frontmatter | CONFIRMED — `disable-model-invocation: false` (harness/skills/find-intent/SKILL.md:9) |
| find-intent "caps at ONE batched round, only fires when genuinely ambiguous" (:76-77) | Read find-intent body | CONFIRMED — "Ask in one batched round… never drip" (:44), "Resolve silently anything inferable" (:40) |
| `Agent` tool, `subagent_type: general-purpose` (:80) | Tool roster + allowed-tools | CONFIRMED — real dispatch mechanism; `Agent` granted (SKILL.md:18) |
| `gh issue comment` as write-back verb (:87) | `gh issue comment --help`; file-bug cross-read | CONFIRMED — real subcommand, granted (:18); verbatim match to file-bug's own contract (docs/skills/file-bug/SKILL.md:118-119) |
| `gh issue view --comments` (:88) | `gh issue view --help` | CONFIRMED — real flag (`-c, --comments`) |
| `doing`/`done`/`wontfix` status verbs "matching file-bug's Phase 6" (:89-90) | Read file-bug Phase 6; `gh label list` | CONFIRMED both ways — file-bug:134-136 git-native row is exactly this (`doing` label, `done` closes, `wontfix` closes with label); all three labels exist in this repo's live label set |
| One re-dispatch, contract quoted, then recorded loss (:91-93) | Read file-bug failure branches | CONFIRMED — file-bug:159-160, same discipline verbatim |
| **"close" verb coverage** (:89-90 "`done` + close", "`wontfix` + close") | `gh issue edit --help` + `gh issue close --help` | **FINDING (minor)** — `gh issue edit` has NO close/state capability (verified against its full flag list); closing requires the separate `gh issue close` subcommand, which is absent from allowed-tools (SKILL.md:18). Since `allowed-tools` grants rather than restricts, the close still works — but prompts mid-flow, in a skill whose grant list otherwise covers every verb step 5 uses. Fix: add `"Bash(gh issue close *)"`. Same finding class the 2026-08-07 audit graded minor. |
| Step 2 flattened-form warning (:43-46, unchanged text) | Re-verified live anyway: `gh issue view 131 --json closedByPullRequestsReferences` | RE-CONFIRMED — returns a PR node (#141) with NO `state` key, exit 0: exactly the silent "never in flight" misread the warning names. The GraphQL-only rule stands. |

Nit (steelmanned, survives only as a nit): ":90 '`wontfix` + close with the reason'" — `gh issue
close --reason` accepts only `completed|not planned|duplicate`, so a literal `--reason wontfix`
fails. The rebuttal that clears it to nit: the line defers to "file-bug's own Phase 6 status
verbs", and file-bug:136 defines the mechanism as wontfix-label + close, with the reason as
comment text. Consider "`wontfix` label + close, reason in the closing comment" to remove the
misread surface.

## Dispatch focus 2 — fork-vs-agent-gate purge

- **SKILL.md: fully purged.** `grep -rn "fork-vs-agent\|fork/agent"` over the skill directory:
  zero hits in SKILL.md. The replacement is the concrete Agent-tool dispatch description asked
  for (SKILL.md:79-83: `Agent` tool, `subagent_type: general-purpose` default, named-agent
  escalation criteria).
- **intent.md: NOT purged — FINDING (major).** intent.md:21-22 still reads "then a fork/agent
  dispatch (harness's fork-vs-agent gate) executes it", and assertion 3 (intent.md:43) still
  reads "find-intent-clarify-then-fork/agent-dispatch". The delta and assertions sections are
  living spec-present records (the dated `rulings` entries are the history), so they now
  contradict the shipped mechanism — the next editor inherits a wrong design memory naming an
  authoring-time-only concept as the runtime dispatch. Steelman ("intent.md is just history")
  fails on exactly that section split, and the workspace contract makes a stale record
  same-severity as a bug. Fix: intent.md:21-22 → "then an Agent-tool dispatch
  (`subagent_type: general-purpose` default) executes it"; intent.md:43 →
  "find-intent-clarify-then-Agent-dispatch". Not blocking: SKILL.md runtime behavior is
  unaffected.
- The 2026-08-08 rulings entry itself (intent.md:100-110) is clean and accurately matches the
  shipped shape (option c, confirm-before-clarify, skip-when-still-vague).

## Checking-rules compliance

Every dismissal above names its check (command run or file:line read); the one "fixed/shipped"
claim taken as true — the 2026-08-07 flattened-form fix — was re-verified at runtime against
issue #131 rather than trusted from intent.md's P5 note. Steelman pass covered all findings; the
`--reason wontfix` finding cites its own surviving rebuttal (demoted major → nit), and the
allowed-tools finding's rebuttal ("grants don't restrict, so it still works") is what holds it
at minor rather than clearing it.

## Top 3

1. **(major)** intent.md:21-22 + :43 — "harness's fork-vs-agent gate" / "fork/agent dispatch"
   survived the purge in the intent record; replace with the Agent-tool dispatch wording that
   SKILL.md already carries.
2. **(minor)** SKILL.md:18 — add `"Bash(gh issue close *)"`; step 5's `done`/`wontfix` closes
   need it and `gh issue edit` cannot close (verified against both subcommands' real flag sets).
3. **(minor)** SKILL.md:80-81 — cite `team-or-solo-rules` (the null unit's actual home,
   team-or-solo-rules/SKILL.md:30), not `agent-writing-rules`; and SKILL.md:74 + intent.md:104 —
   align the file-task scope list with file-task's own words ("chores, follow-ups, research
   items, debts", file-task/SKILL.md:17-18).
