# Audit — what-shipped (FLOOR)

Skill: .claude/skills/what-shipped · Standards: skill-writing-rules · Lint: clean
Verdict: PASS

Audited 2026-07-27 by skill-checker (fresh context), replacing the 2026-07-25 report, whose
R7 findings were written against the pre-repair collector and no longer match the files.
Runtime checks performed, not derived from the bundle's own record: `skill_lint.py` (clean),
`bash -n` on the collector (ok), a live run of `collect-github.sh 2026-07-27 2026-07-27`
against adiahealth/adiav2 (exit 0, `## OK` trailer, 10 human PRs / 21 bot bumps, all five
BOT_NOISE categories tallied), and a forced-failure run (`WHAT_SHIPPED_REPO=adiahealth/does-not-exist-xyz`):
exit 3, `## ERROR` + the failing command on stderr, zero data sections leaked to stdout, no
`## OK` trailer. A bonus datapoint arrived unforced: a transient GitHub 502 during repo
resolution also produced exit 3 + `## ERROR` rather than a partial report.

Both prior R7 findings are confirmed repaired: every `gh` call now routes through `run_gh`
(fails loudly, collect-github.sh:51–55), and the Linear window is date-bounded on both ends
with the rolling duration demoted to a pre-filter (SKILL.md:86–97).

| ID  | Verdict | Severity | Evidence (file:line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Fix                                                                                                                                                                                            |
| --- | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | PASS    | —        | Sampled 4 load-bearing lines. (1) SKILL.md:67–71 `is_bot` lock — deleting it re-opens the bug that passes release bumps as human work; live run shows 21 `adiahealth[bot]` merges correctly binned. (2) SKILL.md:80–84 Linear cost/limit — unguessable numbers (~800 tok/issue, limit ≤ 25, overflow-returns-a-file-path); deletion reverts to the overflow failure recorded in intent.md:121–124. (3) SKILL.md:60–63 trailer check — deletion lets a truncated fetch read as a quiet day; forced-failure run proves the trailer is genuinely absent on failure. (4) SKILL.md:132–135 line-count grounding — deletion reverts `~<lines>` to a guess, since the collector emits only number/author/title. All four survive.                                                             | —                                                                                                                                                                                              |
| R2  | PASS    | minor    | Three plausible user queries — "what shipped today", "summarize PRs merged today", "give me a standup summary" — appear verbatim in the description (SKILL.md:5–7). Description 674 chars, under both caps. Minor: the fence `NOT for publishing the summary as a shareable page (session-review-artifact)` (SKILL.md:10–11) and the escape hatch's hand-off (SKILL.md:157–158) name an owner that exists nowhere — not in `.claude/skills/`, the admin app, `~/.claude/skills/`, or any plugin cache (checked by find). The fence still repels; the hand-off routes to nothing and the model would improvise the publish step. `release-notes/SKILL.md` carries the same stale reference, so this is estate-wide, not local drift.                                                    | Either point the fence/hand-off at the skill that actually owns publishing today (Artifact tooling, or `release-notes` if that absorbed it), or drop the owner parenthetical until one exists. |
| R3  | PASS    | —        | Procedural content + `disable-model-invocation: false` + `user-invocable: true` (SKILL.md:13–14) match the procedural species row. Name-head deviation ("what-shipped" is not a zero-derivation verb) stays dismissed: the name IS the user's verbatim trigger phrase (evals t03) and was explicitly confirmed (intent.md:30–32) — term-of-art/trigger-surface logic.                                                                                                                                                                                                                                                                                                                                                                                                                  | —                                                                                                                                                                                              |
| R4  | PASS    | —        | Zero uppercase hard gates in the body; locks lowercase with named forbidden neighbors ("always — never `.author.is_bot`", SKILL.md:67; "Widen by paging with the returned cursor, never by raising the limit", SKILL.md:83–84; "never 'moved' or 'changed state'", SKILL.md:95–96). Failure branches instantiate consequences, not just triggers (SKILL.md:142–149).                                                                                                                                                                                                                                                                                                                                                                                                                   | —                                                                                                                                                                                              |
| R5  | PASS    | nit      | The `is_bot` mechanic lives in three places: SKILL.md:65–71, collect-github.sh:11–14, intent.md:117–120. The body copy is annotated as edit-protection ("load-bearing if it is ever edited", SKILL.md:65) and the intent copy is forge record — sanctioned redundancy. The prior audit's suggested cross-pointer in the script header ("mirrored in SKILL.md §Collect") was not applied; the drift pair remains unmarked.                                                                                                                                                                                                                                                                                                                                                              | Add the one-line cross-pointer to the script header so an edit to one owes the other.                                                                                                          |
| R6  | PASS    | —        | Body 159 lines (~1,800 tokens), well inside the 5,000-token compaction head. Contracts ordered head-first: window (29) → collect (41) → report contract (105) → failure branches (140) → escape hatch last (154). No references/ needed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | —                                                                                                                                                                                              |
| R7  | PASS    | —        | The prior major is repaired and verified by real runs. Success path: exit 0, `## OK` trailer, correct human/bot split, five-category BOT_NOISE tally (collect-github.sh:115–121; live output confirms all five). Failure path: exit 3, stderr-only `## ERROR` (fail() routes to stderr precisely because most call sites sit inside `$(...)`, collect-github.sh:22–32), no partial sections, no trailer. New cap-saturation guard (collect-github.sh:67–76) applied to all five queries (:88,:90,:101,:105,:107) — a result set filling its `--limit` fails loudly instead of silently truncating; `return 0` correctly guards the false branch under `set -e`. SKILL.md:60–63 keys the model's failure branch on the trailer's absence, matching the script's positive-signal design. | —                                                                                                                                                                                              |
| R8  | PASS    | —        | Numeric anchors on every load-bearing dimension: `limit: 25` (SKILL.md:77), ~800 tokens/issue (:80), ≤5 workstreams (:126), ≤5 bullets (:137), still-open cap 5 (:123), 39-vs-18 worked bot-volume example (:71–73), `-P1D`/`-P7D` duration sizing worked example (:86–88). Step 0 identity resolution (SKILL.md:43–47) closes the last guess surface: `(you)` marking is grounded in `gh api user` + Linear `get_user("me")`, with a named degraded mode when the Linear MCP is absent.                                                                                                                                                                                                                                                                                               | —                                                                                                                                                                                              |

## Dismissed candidates (checks cited, per checking-rules)

- **Cap-saturation guard fails on exactly-full result sets** — considered filing as
  over-strict: a window with exactly 200 merged PRs fails despite being complete. Dismissed:
  truncated-or-exactly-full are indistinguishable from the caller's side (the script's own
  comment states this, collect-github.sh:69–71), and the failure message instructs the
  narrowing re-run. Failing loudly is the designed behavior, not a defect.
- **Ghost-author crash** — a PR whose `author` is null (deleted account) would error inside
  `BOT_TEST`'s `endswith` and abort the run. Checked the failure mode: `run_gh` catches the
  jq error and fails loudly (exit 3, command echoed), which is consistent with the script's
  fail-loud philosophy; no such PR exists in the live data to reproduce against. Speculative
  and loud-not-silent — not filed.
- **Relative script path in `allowed-tools` and Step 1** (SKILL.md:16,52) — assumes repo-root
  cwd; acceptable for a project-local skill whose sessions start at repo root, and the live
  run from repo root worked. Not filed, matching the prior audit's ruling.
- **"tickets updated" naming inconsistency** — checked the verdict line (`<K> tickets
updated`, SKILL.md:112), the section heading (`Tickets updated without a PR`, :119), and
  the Step 2 rule (:95–97): all three use "updated", with the transition-timestamp exception
  correctly scoped. Consistent; not filed.
- **Linear upper-bound enforcement missing** — checked SKILL.md:89–91: both bounds are
  explicit ("drop every returned issue whose `updatedAt` falls outside `SINCE..UNTIL`, both
  bounds"), with the leak mode named. The prior minor is repaired; not re-filed.

## Record nits (not blocking, not counted above)

- intent.md:53 still says "Description 686 chars"; measured 674 (yaml-parsed). Both far under
  the 1,024 cap; carried over from the original fold-artifact.

Top 3:

1. (minor, R2) The `session-review-artifact` fence and escape-hatch hand-off name a skill
   that exists nowhere on the machine — repoint at the real owner of "publish the summary"
   or drop the parenthetical; the same stale reference sits in `release-notes/SKILL.md` and
   deserves one estate-wide sweep.
2. (nit, R5) The SKILL.md↔collect-github.sh `is_bot` drift pair is still unmarked on the
   script side — add the one-line "mirrored in SKILL.md §Collect" pointer the prior audit
   asked for.
3. (nit, record) intent.md's 686-char description count is stale against the measured 674 —
   a one-word fix next time intent.md is touched.
