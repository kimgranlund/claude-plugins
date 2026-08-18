---
name: estate-maintenance
description: >-
  Periodic self-improvement retrospective: mines memory, trend CSVs, decisions, and issues for
  negative patterns — repeated nudges, re-filed near-duplicate tickets, metric drift, context
  ceremony — proposing context fixes behind one confirm. Use for "what keeps going wrong", "why
  do I keep correcting you", "we keep re-filing the same ticket", "context keeps growing". NOT
  authorkit's attention-audit/bloat-audit/pattern-audit/doctrine-audit/repo-audit umbrella; NOT
  plugin lint health (check-everything); NOT work-state (check-state); NOT one fact's harvest
  (save-lessons); NOT session dropped work (file-leftovers); NOT a committing repo campaign
  (clean-repo).
disable-model-invocation: false
user-invocable: true
argument-hint: "[root] [--window-days N, default 90] [--out dir]"
allowed-tools: ["Read", "Glob", "Grep", "Bash(python3 */scripts/collect.py *)", "Bash(python3 */scripts/detect.py *)", "Bash(gh issue list *)", "Bash(gh issue view *)", "Bash(git rev-parse *)", "AskUserQuestion", "Edit"]
---

# estate-maintenance

The periodic retrospective that mines memory, metrics, decision records, and issue history for
negative patterns and proposes context-level fixes — read-only until a single confirm gate,
never `context: fork` (a fork has no `AskUserQuestion` channel, gh#541). This skill's own delta
is the cross-source join, four deterministic negative-pattern detectors (D1-D4), the
fix-generalization/root-source judgment layer, and the one-confirm diff bundle — it re-implements
no detection logic a sibling already owns (see "What this skill never reimplements" below).

## Output contract

Every run ends in exactly one of: a rendered report + diff bundle + ticket list, all confirmed
(some diffs applied, some declined/queued) via Phase 6; the same three artifacts held unconfirmed
at `.claude/ops/held-items.md` (no human channel this firing); or a stop with a named reason
(bad root, no readable inputs at all). Nothing lands in the repo before Phase 5's gate passes —
Phase 6 is the *only* phase with Edit authority, and only over confirmed targets.

## Phase 1 — Collect

Resolve `<root>` (default `.`; for a worktree session, the PRIMARY checkout's own path — so the
memory-dir slug matches, not the worktree's). Before invoking the script, dump issue history
yourself (determinism — no network inside a check):

```
gh issue list --state all --limit 500 --json number,title,state,createdAt,closedAt,labels > <scratch>/issues.json
```

Then:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/estate-maintenance/scripts/collect.py <root> \
  [--memory <dir>] --issues <scratch>/issues.json [--rent <rent.json>] \
  [--window-days N] --out <scratch>/bundle.json
```

Every optional input is feature-detected: absent -> `{"present": false, "reason": "..."}` in the
bundle, never an exception (memory dir absent on a fresh clone/worktree — ADR-0022's named
exception; no `gh` — skip the dump, omit `--issues`; no `rent.json` because authorkit isn't
installed; the cost ledger is a registered-absent input until gh#624 ships). Where authorkit IS
installed and `attention-trend.csv`'s last row is older than the newest plugin version bump, name
`authorkit:attention-audit` step 2/6 as the refresh this run should get before proceeding — this
skill consumes that instrument's output; it does not run its scripts by path.

## Phase 2 — Detect

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/estate-maintenance/scripts/detect.py <scratch>/bundle.json \
  --window-days N --out <scratch>/findings.json
```

Emits the four deterministic classes (D1-D4, thresholds in the script's own docstring,
flag-tunable) plus a non-finding `fix_clusters` helper block. The script owns the count; the
report quotes it verbatim. `findings.json`'s exact shape: `references/report-template.md`.

## Phase 3 — Judge (the LLM layer, over `findings.json` only)

1. **Fix-generalization.** Read `fix_clusters`; pull `gh issue view` on cluster members as needed;
   infer which sibling areas the same fix generalizes to.
2. **Root-source attribution.** For every finding, confirm or override its `artifact`/
   `owning_command` with the actual context surface (table below) and owning command.
3. **Ceremony judgment.** Where a fresh `bloat-audit`/`check-everything` report exists at
   `<root>/harness-audit-*/summary.md`, cite its rows rather than re-deriving; else name the
   command.
4. **Flag-flip discipline.** Any proposal to flip `disable-model-invocation: true` passes the
   three-grep test first — no `skills:` preload names the target, no `Skill(skill: "...")` caller
   names it, no routine/schedule prompt names it — or is dropped. This build's own verified
   mechanics (not the drifted text some sibling doctrine carries — R-6) are the ground truth.

A finding that ends this phase with neither `artifact` nor `owning_command` renders
`status: unrouted` — never silently dropped.

**Context surfaces, ranked by resident cost, and the one owning command each proposal names:**

| Surface | Resident when | Lever this skill may propose | Owning command |
|---|---|---|---|
| Skill descriptions | every turn, 1% shared budget | diet to <=700 chars, reciprocal fence, merge, retire, centralize boilerplate; flip `disable-model-invocation: true` ONLY when the three-grep test passes | owning plugin edits + `/check-routing <plugin>` |
| Agent descriptions | every turn, bill in full | diet / centralize | owning plugin + `agent-checker` |
| Workspace/global `CLAUDE.md` | every session start | trim, move to a `.claude/rules/*.md` pointer target | `/check-entry-file` |
| `.claude/rules/*.md` | only when a pointer is followed | consolidate/retire an unpointed rule | `/check-entry-file` |
| Auto-memory `MEMORY.md` index | every session start | retire a stale entry; promote a >=3-times feedback entry into a rule/skill line | `harness:save-lessons` -> `make-pack`/`make-skill` |
| Skill/agent BODY | on invoke only | contracts-first reorder, split to `references/` | `check-skill` / `bloat-audit` |
| `user-invocable` | never | no proposal ever cites this flag as a context lever | - |

## Phase 4 — Propose

Render `references/report-template.md`: verdict-first summary, the findings table, then the
**diff bundle** (one unified diff per `size: diff` finding, headed by its finding id and target
path, capped at `--max-diffs` default 8 — R-5) and the **ticket list** (one `file-bug`/
`file-feature`/`file-task` line per `size: ticket` finding, named, never minted here). All three
artifacts land in the session scratchpad; `--out <dir>` persists them elsewhere for a fixture
check. Nothing lands in the repo yet.

## Phase 5 — Confirm (exactly one gate)

**Interactive:** ONE `AskUserQuestion` (multi-select), header <=4 words, one option per proposed
diff/ticket, recommendation first, "apply none" always present (save-lessons Phase 3's shape).

**No human channel** (fork, schedule, unattended goal): write ONE entry to
`.claude/ops/held-items.md`'s "Kim's ruling/merge queue" section (the payload-fence convention,
`ops-write-sandbox-rules`), apply nothing, stop. Same skill, same report, different confirm
transport.

## Phase 6 — Apply

**Precondition:** no confirmed selection on record -> return to Phase 5; this phase has no
independent authority to write. Apply only the confirmed diffs (`Edit`), report applied/
declined/queued status per finding id, and name the follow-up gate each edit owes
(`/check-routing <plugin>` for a description, `/check-entry-file` for an entry file,
`skill-checker` for a body — `plugin-authoring.md`'s semantic-edit critic invariant). Ticket
items are handed to the named intake by the user or a follow-up turn — this skill never mints one
itself.

## What this skill never reimplements

| Sibling | What it owns instead | How this skill consumes it |
|---|---|---|
| `authorkit:attention-audit` | Rent measurement, collision detection | Reads `attention-trend.csv` / `--rent`; names it for a refresh, never runs its scripts |
| `authorkit:bloat-audit` | Prose-ceremony judgment | Cites a fresh report if present; hands D4 findings to it otherwise |
| `authorkit:recurrence-audit` | The recurrence-trend row, the ratchet | Reads `recurrence-trend.csv`; names it as D3's owning instrument |
| `harness:save-lessons` | The harvest bar, the Phase-3-shaped confirm | D1's `default_owner`; its Phase 6 staleness loop is cited for memory-retire proposals |
| `harness:check-everything` | Plugin lint health | Consumes `harness-audit-*/summary.md` if fresh, never re-derives it |
| `harness:check-state` | Work-state (git/tickets/docs) | Not read by this skill; a different axis entirely |
| `harness:decision-watcher`/`watch-adrs` | ADR/IDR status, the revalidation queue | Reads `adr-queue.json`/`revalidation-queue.json`, never rewrites them |
| `docs:file-bug`/`file-feature`/`file-task` | Ticket minting | Named for every `size: ticket` finding; never called directly |
| `docs:file-leftovers` | This session's dropped work | Fenced, not called — a different temporal scope (one session vs. the estate's history) |

## Degraded modes

- **Fresh clone / no memory dir** -> `inputs.memory.present=false`; D1 reports UNMEASURED, D2-D4
  still run on whatever else is present.
- **No `gh`** -> skip the issue dump, omit `--issues`; D2 and the issue half of `fix_clusters`
  report UNMEASURED.
- **authorkit not installed** -> `--rent` omitted, `rent.present=false`; the two trend CSVs (if
  present in the repo) still feed D3 directly.
- **No human channel** (fork/schedule/unattended) -> Phase 5's held-items branch; zero diffs
  applied this firing.

## Failure branches

- `<root>` not a git repo or unreadable -> report that and stop; nothing else is measurable.
- `collect.py`/`detect.py` exits 2 -> a usage error in this skill's own invocation; fix the
  arguments and re-run, never substitute hand-derived output for the missing JSON.
- A confirmed diff's `Edit` fails (target moved/changed since Phase 4) -> report the mismatch for
  that finding id as `declined`, apply the rest, never force a stale diff.

Done when Phase 5's gate has been passed (interactive or held-items) and every confirmed item's
Phase 6 status is reported by finding id, the follow-up gate each applied edit owes is named, and
every UNMEASURED input from Phase 1 is disclosed in the final report. NOT done when a diff lands
before its own confirm, a finding with no artifact/owning_command is silently dropped instead of
rendered `unrouted`, or a scheduled/forked firing writes anything other than the single
held-items entry.
