---
doc-type: lld
id: lld-0019-estate-maintenance-retrospective
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: kimgranlund/claude-plugins#629  # RENUMBERED 0018 -> 0019 at build time (2026-08-18,
  # builder pass): origin/main's spine max was lld-0016 when this LLD was first authored, then
  # gh#622 (worktree build-554) landed lld-0017-feedback-intake-door.md (PR #641), so the design
  # doc was minted as lld-0018. Before this PR opened, the builder re-read
  # `git ls-tree origin/main -- .claude/docs/lld/` fresh (doc-writing-rules' universal practice 3)
  # and found origin/main had ALSO gained lld-0018-estate-economy-ledger.md in the interim (PR
  # #642, "Wave 1 of gh#624", merged 2026-08-18T14:21:41Z) — a second, unrelated concurrent build
  # in this same live multi-agent fleet. This file renumbers to 0019 (verified free at the same
  # re-read) to avoid the #633 two-parallel-mints collision T10 exists to catch; a third such
  # collision on the SAME id remains possible in principle in a fast-moving fleet, mitigated only
  # by re-checking as late as possible before the PR actually opens, not eliminated.
spec: none
---
# LLD — `harness:estate-maintenance`: the periodic retrospective that mines memory, metrics, decision records, and issue history for negative patterns and proposes context-level fixes (#629)

**Verdict, head-first:** one new PROCEDURAL skill, `harness/skills/estate-maintenance/`
(`disable-model-invocation: false`, `user-invocable: true` — both routes, like `check-state`/
`sweep-chores`), that runs **in the host session, never `context: fork`** (the batched confirm is
an `AskUserQuestion`, and forks have no such channel — falsified 2026-08-17, gh#541), composed of
two bundled skill-level scripts (`collect.py` → one evidence bundle; `detect.py` → deterministic
findings with evidence pointers), a seeded fixture estate under `assets/fixture-estate/`, an evals
suite, and one report template. It **reads the durable outputs sibling seats already produce**
(the two trend CSVs, `.claude/ops/*` queues, the auto-memory index, `gh` issue history) and
**dispatches siblings by name only when their output is missing or stale** — it re-implements no
detection logic authorkit's audit family, `save-lessons`, `check-state`, `watch-adrs`/
`decision-watcher`, or docs' `file-leftovers` already own. Its own delta is the CROSS-SOURCE
join, the four temporal negative-pattern detectors (D1–D4), the fix-similarity/root-source
judgment layer, and the one-confirm diff bundle.

**Why no standalone SPEC/PRD/ADR (routing note, moved out of frontmatter 2026-08-18 per the
doc-checker's repair pass):** gh#629's own Acceptance section carries the checkable criteria
(restated below as predicates, AC-1..AC-3 — minted HERE, not a restatement of the ticket's own
Acceptance section, since they are sharper than it), and its Findings comment carries Kim's ruled
output contract (2026-08-18: report + proposed diffs behind ONE batched confirm). A standalone
SPEC would restate what the ticket and the ruling already state — the same routing test
lld-0008/0009/0013/0015/0016 applied. No PRD: the why/what is the ticket body +
idr-0006/0009/0010/0011's outer-loop family, not a new capability lacking a record. No ADR: no
hard-to-reverse fork was resolved here (name is grammar-derived, home follows the anti-matrix
rule, output contract was ruled upstream) — non-decisions are named in Risks, per this seat's
ADR-default-NO.

**Headline finding on the ticket's load-bearing premise (Resolution c): PARTIAL, redesigned.**
"System-only-invocable skills as instruments for shaping the context window" is true only for
ONE flag in ONE direction: `disable-model-invocation: true` removes a skill's description from
the model's resident routing listing (a subtractive lever, already authorkit `attention-audit`'s
"zero-rent" figure); `user-invocable` has **no context effect at all**; and the both-flags
"system-only" state is a **dead skill** (harness_checks D11 / skill-writing-rules' "treat it as a
misconfiguration"). The "fix via context" step is therefore designed around the levers that ARE
real — description rent, entry-file/rules/memory size, skill-body length on invoke — with flag
flips confined to the one legal move (a true command species). Evidence, verbatim, in
Resolution c. A **doctrine-drift finding surfaced while verifying** (attention-audit's
"demote-to-wiring" text contradicts harness canon on what the flag blocks) is recorded in Risks
R-6 for the coordinator to route — not fixed here.

## Resolution a — Name: `estate-maintenance` (registered tokens only, validator-clean, no collision)

**Resolved:** `estate-maintenance` — ADR-0011 skill production `{object}-{process}` with
`estate` ∈ ObjectVocab and `maintenance` ∈ ProcessLex (both already registered in
`naming.manifest.json`; no new token minted, no `manifest-authoring` gate needed).

- **Validator evidence:** a scratch fixture plugin carrying `estate-maintenance` (alongside
  `estate-review`, `estate-triage`, `harness-maintenance`, `check-estate` as controls) run through
  `authorkit/skills/naming-audit/scripts/validate.py --scope grammar` against this repo's own
  manifest: all five parse clean; the negative control `context-maintenance` fails exactly as
  expected (`token 'context' resolves in no lexicon or vocab`) — confirming the "no new token"
  constraint bites and that the chosen name is a grammar-conformant mint, not an exemption.
- **Collision grep:** `estate-maintenance` occurs nowhere in the estate (no `*/skills/`,
  `*/agents/`, `.md`, or `.json` hit); the only `estate-*` artifacts are authorkit's `estate-audit`
  (an INDEX skill — "which audit instrument fits") and `estate-audit-agent` (the batch audit seat).
- **Why a blind router won't confuse it with the named siblings:** the process token does the
  work. Every neighbour in the confusability set is an `*-audit` (pattern/attention/bloat/
  recurrence/doctrine/estate-audit-agent — static measurement instruments), a `check-*` (check-
  state = work-state, check-everything = plugin lint health), a `save-*`/`file-*` (one fact, one
  session's leftovers), or a `*-watcher` (ADR harvest). `maintenance` is a fresh token in this
  estate (zero prior skill/agent uses) and reads as what the skill IS: periodic upkeep — mine,
  diagnose, propose fixes. Its description fences all of them explicitly (Components §1) and the
  build runs `collide.py --against estate-maintenance` (attention-audit step 3's write-time
  pre-lint) to prove no unfenced routing twin remains (Components §9).
- **Rejected names, briefly:** `harness-maintenance` (stutters `harness:harness-maintenance` —
  the CLAUDE.md invariant "no /ui:ui-review stutter", and `harness` names the plugin, not the
  object under repair); `estate-review` (`review` is crowded — review-leader/bind-review/code
  review — and ProcessLex marks it ᵈ); `estate-triage` (triage = sorting inbound items, the
  issue-sorter sense, not a retrospective); `pattern-*` anything (a real trap: `pattern-audit`
  means a regex/instruction sweep, this skill means behavioural patterns — sharing the head would
  manufacture the exact confusion the charter warns about); `context-*`/`memory-*`/
  `retrospective`/`healing` (unregistered tokens — would need a manifest PR and the live
  anti-ambiguity gate this dispatch cannot run).

## Resolution b — Metrics inventory: two CSVs present, one documented future input, one registry

**Inventoried (this worktree, 2026-08-18):**

| Source | Rows | Columns | Cadence / writer | Negative-pattern signal as a row-over-time read |
|---|---|---|---|---|
| `attention-trend.csv` | 42 data rows, dates 2026-08-16..17, one row per (plugin, append) | `date, plugin, routable_skills, routable_chars, zero_rent_skills, zero_rent_chars, agents, agent_chars, dead, stolen, leaked` | Was appended per plugin-version bump by `trend_hook.py` (retired 2026-08-17, #466); now attention-audit step 6 by hand at release boundaries. **Multiple rows share one date** — series order is APPEND order, never date sort. | (i) monotonic `routable_chars` growth per plugin with no decrease (harness 19116 → 19707, +3.1 %, over the file's life; teamwork `agent_chars` 5325 → 8998 → 6299 — a spike then partial diet); (ii) `dead/stolen/leaked` = `absent` in 42/42 rows — the routing-report columns have NEVER been fed, i.e. the instrument runs half-blind; (iii) `zero_rent_skills` moving (docs 2→3→2) = command/knowledge flag churn worth a look. |
| `recurrence-trend.csv` | 1 data row (2026-08-18) | `date, seeded_classes, recurred_classes, bare_citations, files_scanned, routing_passed, routing_total, routing_pass_rate` | recurrence-audit step 6, per release cycle (idr-0006's instrument, lld-0011) | (i) `seeded_classes = 0` while `bare_citations = 3183` — the `LEDGER-CLASS:` ratchet is live but unadopted, so the primary success measure computes nothing; (ii) a series that never gains a second row is a loop not firing (idr-0011's own "detectable defect"); (iii) `routing_*` = `absent` again — same half-blindness as above. |
| **Cost ledger (FUTURE — gh#624 / idr-0010, not built)** | none | idr-0010's own lean: one row per firing — `date, event-kind, seat/command, tokens, outcome, verdict`, "shaped like `attention-trend.csv` and living under `.claude/ops/`" | per firing, close-out convention (no hook may own it) | once present: a firing class whose tokens rise while outcome stays flat; a class with rows but zero cited decisions across review cycles (idr-0010's own falsifier). Until present: reported as `UNMEASURED: cost ledger not yet shipped (gh#624)`, never as zero. |

**Design so the ledger slots in without a rewrite:** `collect.py` carries a **metric-source
registry** — a list of `{key, path (repo-relative), key_columns, series_columns, ordering:
"append"|"date"}` entries, feature-detected by path; an absent registered path yields a bundle
entry `{"present": false, "reason": "..."}` (AC-predicate: never an exception). The cost ledger
is a registry entry with `present: false` from day one, its path filled in by the #624 build
(one-line change) — and `detect.py`'s D3 detectors are written over the registry's generic
`series_columns` shape (per-key monotonic-growth and all-`absent` checks), so the ledger's
columns get D3 coverage the moment its row lands. Nothing about D1/D2/D4 changes.

## Resolution c — Premise verification: what the invocation flags actually do (PARTIAL; redesigned)

**Verified against the estate's own canon (file:line), not assumed:**

1. `harness/skills/skill-writing-rules/SKILL.md:40` (Command species row): `disable-model-
   invocation` = `true`, `user-invocable` = `true`, "Description's job: **Slash-menu documentation
   — it never enters model context**", "Preloadable into agents: **No**".
2. Same file `:39` (Knowledge species row): `disable-model-invocation: false` + `user-invocable:
   false` → "Trigger contract — **the model is the only router**" — i.e. with `user-invocable:
   false` the description IS still resident; the flag only hides the `/` menu entry.
3. Same file `:42`: "**`disable-model-invocation: true` blocks subagent preloading** (and
   scheduled-task firing, v2.1.196+) … Both flags set = invisible to the menu, to auto-discovery,
   *and* to `skills:` preloads — **a skill nothing can reach except a raw file read. Treat it as a
   misconfiguration**".
4. Same file `:23,:28`: the resident cost is the DESCRIPTION ("Description listing budget: 1 % of
   context window, shared by all descriptions; least-invoked dropped first"); the body "**Enters
   context once on invoke; never re-read**".
5. `harness/scripts/skill_lint.py:1020` (W8 selftest comment): "the same text under disable-
   model-invocation stays silent (**menu-only, never resident**)"; W8 itself (`:292-297`) budgets
   model-invocable descriptions at ≤ 700 chars.
6. `docs/skills/make-reference/scripts/harness_checks.py:209-217` (D11): both flags set is
   "unreachable by user (hidden from menu) AND by model (**hidden from context until invoked**)".
7. `harness/skills/sweep-chores/SKILL.md:27`: "a `disable-model-invocation: true` command skill
   **blocks BOTH paths at once** (issue #134's class)" — the Skill-tool-by-name path too.
8. `authorkit/skills/attention-audit/SKILL.md:48-51`: "Skills carrying `disable-model-invocation:
   true` are **zero-rent** (excluded from the routable figure, counted separately); **agent
   descriptions bill in full unconditionally**".

**Verdict: PARTIAL.** TRUE — `disable-model-invocation: true` is a real, subtractive context
lever: it takes the skill's description out of the resident listing (facts 1, 5, 6, 8). FALSE as
stated — (i) "system-only-invocable" (both flags) is not an instrument, it is a dead artifact
(facts 3, 6); (ii) `user-invocable` shapes nothing in context (fact 2); (iii) the flags can only
REMOVE a description — they cannot add, reweight, or promote anything; (iv) flipping the flag
also severs `skills:` preloads, scheduled firing, AND Skill-tool-by-name dispatch (facts 3, 7),
so it is legal only for a skill a human types as `/name` and nothing else ever calls — a true
Command species. **`plugin-install-facts` carries nothing on these flags** (checked; it is an
install-channel corpus) — skill-writing-rules is the sole authority, and it is marked
`[drift-prone]`, verified 2026-07 / 2026-08-15.

**Redesign of the "fix via context" step (Phase 3/4 below) around what is true.** The context
influencers, ranked by resident cost, and the ONE owning command each proposed diff names:

| Surface | Resident when | Lever the skill may propose | Owning command / gate |
|---|---|---|---|
| Skill descriptions (`disable-model-invocation: false`) | every turn, all skills, 1 % shared budget | diet to ≤ 700 chars, reciprocal fence, merge, retire, centralize boilerplate (attention-audit's category set); flip `disable-model-invocation: true` ONLY when the skill is human-`/`-only (no preload, no Skill-tool caller, no schedule — the build greps for all three before proposing) | owning plugin edits + `/check-routing <plugin>`; the flag flip additionally needs `eval_check`/check-routing's command-only exclusion (#593) |
| Agent descriptions | every turn, bill in full | diet / centralize | owning plugin + `agent-checker` |
| Workspace + global `CLAUDE.md` | every session start | trim, move to a `.claude/rules/*.md` pointer target (NOT auto-loaded — verified 2026-08-16, #262 — so moved text costs nothing until followed) | `/check-entry-file`, `entry-file-rules` (C1 200-line proxy) |
| `.claude/rules/*.md` | only when a pointer is followed | consolidate/retire a rule no pointer names | `/check-entry-file` |
| Auto-memory `MEMORY.md` index (+ entry on read) | index every session start | retire a stale/superseded entry; promote a ≥ 3-times feedback entry into a rule/skill line (then shrink the memory) | `save-lessons` (harvest bar) → `make-pack`/`make-skill`; memory edits are proposed diffs like any other |
| Skill/agent BODY | on invoke only, first 5 000 tokens survive compaction | contracts-first reorder, split to `references/` | `check-skill` / `bloat-audit` (authorkit, where installed) |
| `user-invocable` | never | **no proposal ever cites this flag as a context lever** | — |

## Resolution d — Home plugin: harness (confirmed against the anti-matrix rule, not asserted)

**Resolved: harness.** Reasoning under plan-plugin-split's guard ("an absence is a gap only with
job evidence … two members OWNING the same procedure with adjacent charters is a defect"):

- **Job evidence for the gap:** gh#629's Phase-3 dedup (intake, not re-litigated here) found no
  member of any plugin doing the cross-source retrospective; the workspace routing table has no
  row for it (absence = finding, closed by Components §7). AC-1 below is an ask no existing
  suite answers.
- **Surplus side, checked:** this skill OWNS no procedure a sibling owns — every detector class
  either consumes a sibling's durable output (trend CSVs, ops queues) or is a join no sibling
  performs (memory × issues × metrics × decision records). Where a sibling owns the judgment
  (bloat-audit for prose ceremony, save-lessons for the harvest bar, attention-audit for the
  structural-fix category), the skill hands off by name.
- **Why harness over authorkit:** authorkit's charter is estate GOVERNANCE instruments — five
  read-only static audits + rename/overhaul campaigns; its own umbrella (`repo-audit`) fences
  "NOT for the ops chore queue (harness:sweep-chores — live work-state, not static audit
  instruments)". This skill is temporal and behavioural (memory, issue history, decision queues),
  the outer-loop family harness already houses: `check-everything` ("the recurring outer loop"),
  `save-lessons`, `sweep-chores`, `check-state`, `decision-watcher`, `check-reconstructibility`
  (which already names the memory dir as a harness concern). Placing it in authorkit would put a
  harness-family loop behind a governance plugin's fence and make every harness handoff a
  cross-plugin mention.
- **Why not teamwork:** teamwork owns multi-agent DELIVERY (plan → build → review → coordinate);
  this is a solo-first, host-session procedure with no fleet seat (idr-0007's solo-first
  composition — a new coordination seat needs a named gap the skill itself cannot cover; none
  is named).
- **Cost of the choice, named:** three of its named siblings are cross-plugin (authorkit's audit
  family, docs' `file-leftovers`/`file-*` intakes). Per `.claude/rules/plugin-authoring.md` these
  stay SOFT mentions that degrade gracefully (UNMEASURED with reason when not installed) — no
  `${CLAUDE_PLUGIN_ROOT}` path or preload ever crosses a plugin boundary (Interfaces).

## Resolution e — Cadence: on-demand now; schedulable later, nothing here blocks it

**Resolved:** on-demand (user-invocable AND model-routable) in v1. Scheduled invocation is
**deferred to gh#626's calendar mechanism** (idr-0011), cited not built. Three design choices
keep the door open rather than closed:

1. **`disable-model-invocation: false`** — skill-writing-rules `:42`: the `true` value "blocks …
   scheduled-task firing (v2.1.196+)"; a command-species mint would have made #626's later
   scheduling impossible without a species flip.
2. **A defined no-human-channel branch (Phase 5).** A scheduled or forked firing has no
   `AskUserQuestion`; the procedure then writes NOTHING to context surfaces — it queues the
   report + diff bundle as one entry in `.claude/ops/held-items.md`'s "Kim's ruling/merge queue"
   section (lld-0015's channel; fleet-rules' batching default) via the ops write-sandbox payload
   convention (`ops-write-sandbox-rules`), and applies zero diffs. Same skill, same report,
   different confirm transport.
3. **A `.claude/ops/calendar.md` row** (Components §8) — "Estate maintenance retrospective |
   on-demand; cadence unassigned (tunable, idr-0011's ruling round pending) | `/estate-
   maintenance` | Kim / any interactive session | standing procedure, human-fired". The
   calendar's own contract is that every standing loop has a row; the row reserves the slot
   #626's round edits, and this LLD assigns no number (same posture as lld-0016 Resolution 5).

## Procedure — six phases (what the SKILL.md body encodes)

1. **Collect.** Resolve `<root>` (default `.`; the PRIMARY checkout — for a worktree, `git
   rev-parse --git-common-dir`'s parent — so the memory-dir slug matches). Run `python3
   ${CLAUDE_PLUGIN_ROOT}/skills/estate-maintenance/scripts/collect.py <root> [--memory <dir>]
   [--issues <issues.json>] [--rent <rent.json>] [--window-days N] --out <bundle.json>`. Before
   that, the SESSION (not the script — determinism, no network in a check) dumps issue history:
   `gh issue list --state all --limit 500 --json number,title,state,createdAt,closedAt,labels
   > issues.json`. Optional inputs feature-detected; each absent one → `UNMEASURED` with reason
   in the bundle (memory dir absent on a fresh clone — ADR-0022's named exception; `gh` absent;
   cost ledger not shipped; no `rent.json` because authorkit isn't installed). Where authorkit IS
   installed and `attention-trend.csv`'s last row is older than the newest plugin version bump,
   name `authorkit:attention-audit` step 2/6 as the refresh — never run its scripts by path.
2. **Detect.** `python3 …/scripts/detect.py <bundle.json> --json > findings.json` — the four
   deterministic classes below plus a non-finding `fix_clusters` helper block. Never hand-count
   what the script measures (attention-audit's own rule, cited).
3. **Judge (the LLM layer, over `findings.json` only).** (a) Fix-generalization: read
   `fix_clusters` (closed issues + ADRs + feedback memories inside `--window-days`, pre-clustered
   by title-token similarity), pull `gh issue view` on cluster members as needed, and infer
   sibling areas the same fix generalizes to. (b) Root-source attribution: for every finding
   confirm or override the detector's `default_artifact`/`default_owner` with the actual
   context surface (Resolution c's table) and owning command. (c) Ceremony judgment: where a
   fresh `bloat-audit`/`check-everything` report exists at `<root>/harness-audit-*/summary.md`,
   cite its rows rather than re-deriving; else name the command. (d) Any flag-flip proposal
   passes the three-grep test (no `skills:` preload, no `Skill(skill: "…")` caller, no routine
   prompt names it) or is dropped. A finding that ends this phase with neither artifact nor
   owning command renders as `UNROUTED` — never silently dropped.
4. **Propose.** Render `references/report-template.md`: verdict-first summary, the findings table
   (id · class · severity · evidence pointers · artifact · owning command · size), then the
   **diff bundle** — one unified diff per `size: diff` finding, each headed by its finding id and
   target path — and the **ticket list** — one `file-bug`/`file-feature`/`file-task` line per
   `size: ticket` finding, never minted here. All three artifacts land in the session scratchpad
   (`--out <dir>` persists them elsewhere for a fixture check); nothing lands in the repo.
5. **Confirm — exactly one gate.** Interactive: ONE `AskUserQuestion` (multi-select), header
   ≤ 4 words, one option per proposed diff/ticket, recommendation first, "apply none" always
   present (save-lessons Phase 3's shape, batched). No human channel (fork, schedule,
   unattended goal): write the held-items entry (Resolution e §2), apply nothing, stop.
6. **Apply.** Precondition worded exactly as save-lessons Phase 4: no confirmed selection on
   record → return to Phase 5, this phase has no independent authority. Apply only the confirmed
   diffs (Edit), report the applied/declined/queued status per finding id, and name the follow-up
   gate each edit owes (`/check-routing <plugin>` for a description, `/check-entry-file` for an
   entry file, `skill-checker` for a body — the semantic-edit critic invariant, `plugin-
   authoring.md`). Ticket items are handed to the named intake by the user or a follow-up turn.

**Detector classes (deterministic, thresholds in `detect.py`'s docstring, each flag-tunable):**

- **D1 repeated user nudge** — auto-memory entries with frontmatter `metadata.type: feedback`
  (12 of 30 files in this workspace's memory dir today) clustered by informative-token overlap
  **(name + description; overlap coefficient ≥ 0.2, ≥ 3 shared non-stopword tokens — corrected
  2026-08-18, gh#645: raw Jaccard at 0.3/2 shipped in this LLD's first draft never fires on real
  prose, since it punishes a short first-telling paired against a long third-telling too hard;
  the overlap coefficient — shared / min(len_a, len_b) — doesn't)**; a cluster of ≥ 2, or a
  single entry whose **description** (corrected 2026-08-18, gh#645: matches the description only,
  never the body — cheaper to keep the doc honest than to widen the lexicon match, which pulls in
  template boilerplate like "Why:"/"How to apply:" that inflates unrelated overlap) matches the
  recurrence lexicon (`third time|again|repeatedly|never re-ask|stop (doing|proposing)`) →
  finding, `default_owner: save-lessons` (frequency detector = "third telling"),
  `default_artifact`: the memory entry + the rule/skill line it should become.
- **D2 re-filed near-duplicate ticket** — issue titles normalized (lowercase, punctuation and
  stopwords stripped, `#NNN` removed), pairwise Jaccard ≥ 0.5 → clusters; a cluster where a member
  was CREATED after another member's `closedAt` = **re-filed** (the negative pattern); same-window
  duplicates = dedup miss (lower severity). `default_owner`: the intake's dedup-search step
  (`file-bug`/`file-feature`, backend-resolver op 2) or `issue-sorter`.
- **D3 metric drift** — over every registry source present: rows are GROUPED by that source's
  own registered `key_columns` first (corrected 2026-08-18, gh#645 MAJOR-1: the first build
  dropped `key_columns`/`series_columns` from the bundle and iterated every CSV column across
  ALL rows ungrouped, so on real multi-plugin data the series was never monotonic and rent-growth
  could never fire — verified fixed: authorkit's `routable_chars` genuinely grows 6327→7959,
  +25.8%, monotonically, once grouped by `plugin`), then per key a series column monotonic
  non-decreasing across ≥ 3 rows with ≥ 5 % total growth → `rent-growth`; a column `absent` in
  100 % of ≥ 3 rows of the WHOLE source (never-fed-ness stays source-wide, not per-key) →
  `instrument-half-blind`; a source with exactly 1 row older than `--window-days` →
  `series-not-firing`; recurrence `seeded_classes == 0` on the latest row → `ratchet-unadopted`.
  `default_owner`: attention-audit's structural-fix set for rent; the owning instrument's own
  procedure step for the others.
- **D4 ceremony proxy** — context-surface census: entry files > 200 lines (the shared threshold
  is `skill_lint` C1's — one constant, cited, not a new number); `.claude/rules/` count and total
  lines; `MEMORY.md` index lines; sum of the latest `routable_chars` + `agent_chars` per plugin
  from the trend source. Findings name the surface and hand prose judgment to
  `/check-entry-file` / `bloat-audit`. (Census only — no description parsing: that is
  `rent.py`'s job, consumed via the CSV or `--rent`.)

## Components

Build sequence, top to bottom:

1. **`harness/skills/estate-maintenance/SKILL.md`** — procedural species; frontmatter `disable-
   model-invocation: false`, `user-invocable: true`, `argument-hint: "[root] [--window-days N]
   [--out dir]"`, `allowed-tools`: Read, Glob, Grep, `Bash(python3 */scripts/collect.py *)`,
   `Bash(python3 */scripts/detect.py *)`, `Bash(gh issue list *)`, `Bash(gh issue view *)`,
   `Bash(git rev-parse *)`, AskUserQuestion, Edit (Phase 6 only — the body states the gate).
   **No `context: fork`** (Verdict). Description ≤ 700 chars (W8), third person, trigger
   vocabulary front-loaded — feature nouns ("retrospective", "self-improvement", "estate
   maintenance", "negative patterns"), symptom phrases ("what keeps going wrong", "why do I keep
   correcting you", "we keep re-filing the same ticket", "our context keeps growing"), lifecycle
   moment ("periodic upkeep of the harness/estate") — and parseable fences: NOT one audit
   instrument or their umbrella (authorkit's attention/bloat/pattern/doctrine-audit, repo-audit);
   NOT plugin lint health (check-everything); NOT work-state (check-state); NOT one fact's
   harvest (save-lessons); NOT this session's dropped work (docs file-leftovers); NOT a committing
   repo alignment campaign (clean-repo). Body: the six phases above, contracts-first (output
   contract + the single-gate rule + failure branches in the first 5 000 tokens), degraded modes
   (fresh clone / no memory dir; no `gh`; no authorkit; no human channel), and a "what this skill
   never reimplements" table naming each sibling and the output it consumes instead.
2. **`scripts/collect.py`** — skill-level (`script-writing-rules`: positional-first, `selftest`,
   exit 0/1/2, no network). Collectors: `memory` (frontmatter of every `*.md` in `--memory` +
   `MEMORY.md` index lines), `metrics` (the registry — `attention-trend.csv`, `recurrence-
   trend.csv`, `cost_ledger` present:false), `decisions` (ADR/IDR `status:` via frontmatter —
   reuse `adr_checkpoint.parse_frontmatter`/`parse_status_table` by same-plugin import from
   `${CLAUDE_PLUGIN_ROOT}/scripts/`, no re-derivation; plus `.claude/ops/adr-queue.json`,
   `revalidation-queue.json`, `plan.md` pending counts), `issues` (the supplied JSON, `--window-
   days` filter), `census` (D4's byte/line counts). Output: one bundle JSON with a top-level
   `inputs` map (`present`/`reason` per source). Selftest runs against `assets/fixture-estate/`.
3. **`scripts/detect.py`** — D1–D4 + `fix_clusters` over a bundle; emits `findings.json` in
   the template's schema (below); `selftest`: fixture bundle → all four seeded classes found
   (positive control), an empty/clean bundle → zero findings (negative control), every finding
   carries ≥ 1 `evidence[]` entry with `path` + `locator`. Same-date-row ordering (append order)
   is a named fixture case. Also carries a `--verify <findings.json>` flag (AC-1's own instrument
   — repaired 2026-08-18: this replaces an earlier hedge naming a `references/verify.md`
   one-liner as an alternative; the flag is the ONE instrument, payload-layer, agent-runnable).
4. **`assets/fixture-estate/`** — a seeded mini-estate: `memory/` with three feedback entries on
   one topic + one non-feedback control; `attention-trend.csv` with one plugin's monotonic rent
   growth and all-`absent` routing columns; `recurrence-trend.csv` with one `seeded_classes=0`
   row; `issues.json` with one closed/re-opened-later near-duplicate pair and one unrelated
   control; a 230-line `CLAUDE.md`; two `.claude/rules/*.md`; a `README.md` naming which file
   seeds which detector class. This is AC-2's fixture.
5. **`references/report-template.md`** — report shape + the `findings.json` schema: `run
   {date, root, inputs}`, `findings[] {id, class (D1|D2|D3|D4|J-generalization|J-root-source),
   severity (blocking|major|minor|nit), summary, evidence[] {path, locator, quote}, artifact
   {path, kind}, owning_command, proposed_diff|null, size (diff|ticket), status
   (proposed|confirmed|applied|queued|declined|unrouted)}`, `unmeasured[] {input, reason}`.
6. **`evals/evals.json`** — trigger cases from the description's three vocabularies; no-trigger
   cases for each fence target; reciprocal fence cases added to the sibling suites `collide.py
   --against` names (Components §9) — evals edits are additive and same-change per
   `plugin-authoring.md`.
7. **Workspace `CLAUDE.md` routing-table row** (directly under "Periodic health sweep"):
   "Periodic self-improvement retrospective — memory + metrics + decision records + issue history
   → negative patterns → context-level diffs behind one confirm | harness: `/estate-maintenance`
   (read-only until confirmed; proposes)".
8. **`.claude/ops/calendar.md` row** — Resolution e §3 wording; living state, no supersession.
9. **Reciprocal fences** — run `python3 authorkit/skills/attention-audit/scripts/collide.py
   --target <workspace> --against estate-maintenance --json` (a build-time gate in THIS
   workspace, where authorkit is present — not a runtime dependency of the skill); each pair it
   ranks above threshold and un-fenced gets a NOT-clause on the sibling side (owner-edited, same
   PR, W8-checked — if a fence would blow the sibling's 700-char headroom, prefer the diet or
   centralize move the category set already names). Expected twins: repo-audit, clean-repo,
   check-everything, save-lessons.
10. **Fresh-context critic passes** (`plugin-authoring.md`'s semantic-edit invariant):
    `harness:skill-checker` on the new SKILL.md; any sibling description edited in §9 gets its
    own `skill-checker` (or `agent-checker`) pass — floor depth (fence edits), full depth for the
    new skill.
11. **Gates before PR:** `collect.py selftest`, `detect.py selftest`, `skill_lint.py` on the new
    SKILL.md + every touched evals/description, `eval_check.py`, `/check-routing harness` (and
    `/check-routing authorkit` if any authorkit description changed), `doc_lint.py --spine`,
    `release_gate.py harness --package`.
12. **Plugin close-out:** `harness/.claude-plugin/plugin.json` bump (re-read off `origin/main`
    right before — 3.13.0 at authoring) + README footer ledger line naming #629, the skill, both
    scripts, the fixture, and the calendar/routing rows; dated Findings comment on gh#629 with
    the shipped paths and the Resolution c verdict.

**Acceptance predicates — minted HERE (LLD-owned acceptance IDs; gh#629's close-out cites these
back, sharper than the ticket's own Acceptance section, not a restatement of it):**
- **AC-1 (real estate run):** `collect.py <this workspace> …` then `detect.py` yields ≥ 1 finding
  in each of D1, D2 (if issue history is supplied), D3, and every finding's `evidence[]` paths
  exist and its `locator` resolves — proven by ONE instrument, `detect.py --verify
  <findings.json>` (payload layer, agent-runnable; repaired 2026-08-18 — this replaces an earlier
  hedge that also named a `references/verify.md` one-liner as an alternative instrument). Every
  finding carries `artifact` + `owning_command` or `status: unrouted`.
- **AC-2 (fixture):** `detect.py selftest` exit 0 with the positive/negative controls above.
- **AC-3a (read-only by default, unattended branch):** a run with no human channel leaves
  `git status` clean apart from the scratch outputs — the only repo-side write is the
  held-items payload the session applies.
- **AC-3b (read-only by default, interactive branch):** a run with the confirm answered "apply
  none" leaves `git status` equally clean — human-assert (the confirm gate itself is not
  payload-checkable; observing that "apply none" produced zero repo writes is).

## Interfaces

- **`estate-maintenance` → sibling seats:** name mentions only, degrade to UNMEASURED —
  `authorkit:attention-audit` (refresh the trend row / `rent.json`; structural-fix category set),
  `authorkit:bloat-audit` + `/check-entry-file` (ceremony judgment), `authorkit:recurrence-audit`
  (the recurrence row), `harness:save-lessons` (harvest bar + Phase 3 gate shape reused, its
  Phase 6 staleness loop cited for memory-retire proposals), `harness:check-everything`
  (`harness-audit-*/summary.md` consumed if fresh), `harness:check-state` (`state-checkpoint.json`
  read, never rerun), `harness:decision-watcher`/`watch-adrs` (`adr-queue.json`,
  `revalidation-queue.json` read), `docs:file-bug|file-feature|file-task` (named for
  `size: ticket` items), `docs:file-leftovers` (fenced, not called).
- **`collect.py` → `adr_checkpoint.py`:** same-plugin import of two parsers (`harness/scripts/`),
  the pattern lld-0016 already used for `revalidation_checkpoint.py`.
- **`collect.py` → the metric-source registry:** the ONLY seam a future metric input touches
  (Resolution b).
- **Phase 5 → `AskUserQuestion`** (interactive) **or → `held-items.md` payload block** per
  `ops-write-sandbox-rules` (unattended). Phase 6 → `Edit` on confirmed targets only.
- **The skill → `.claude/ops/calendar.md`:** a row, no cadence value (idr-0011 / gh#626).

## Data

No new persistent state file. Run outputs (`bundle.json`, `findings.json`, `report.md`, the diff
bundle) are session scratch, optionally persisted with `--out`. Repo-side writes happen only
post-confirm (Phase 6) or as the single held-items entry (unattended). Inputs read: the memory
dir (user-scoped, ADR-0022 exception), `attention-trend.csv`, `recurrence-trend.csv`,
`.claude/ops/{adr-queue,revalidation-queue,state-checkpoint}.json`, `.claude/ops/plan.md`,
`.claude/docs/{adr,idr}/`, entry files, `.claude/rules/`, plugin manifests, and a session-supplied
`issues.json`. The cost ledger is a registered-absent input. `findings.json` schema: Components §5.

## Risks

- **R-1 (judgment quality of Phase 3 — clustering "generalizes" a fix that doesn't).** Detection:
  every J-class finding cites its cluster members; a wrong generalization is a declined option at
  the confirm, not an applied edit. Fallback: none needed — the single gate is the design.
- **R-2 (D2 false positives from boilerplate titles — "teamwork: … (closes #NNN)").** Detection:
  the selftest's control pair; the stopword list carries the estate's ledger-line boilerplate
  tokens. Fallback: `--jaccard` flag; the judgment layer dismisses with one clause (attention-
  audit's "coincidence" bucket).
- **R-3 (memory dir absent or worktree-scoped).** A fresh clone or a worktree session resolves a
  different `~/.claude/projects/<slug>/memory`. Detection: `inputs.memory.present=false` with the
  resolved path in `reason`. Fallback: `--memory <dir>` explicit; D1 reports UNMEASURED, the other
  classes still run.
- **R-4 (thresholds are guesses).** D1/D2/D3 numbers are stated in the docstring, flag-tunable,
  and every threshold hit renders its value beside the finding so a reader can judge. Fallback:
  tune via flags; a threshold change is a script edit under selftest, not doctrine.
- **R-5 (the confirm becomes a rubber stamp for large diff bundles).** Detection: the report
  caps the diff bundle at 8 (remainder rendered as ticket lines) so one round stays reviewable —
  same reason find-open-questions batches into ONE round. **Corrected 2026-08-18, gh#645
  minor-6:** this was originally worded as a `--max-diffs N` CLI flag; neither script ever
  implements one, since the cap is Phase 4's own prose-rendering behavior (the host session,
  not a script pass) — reworded here to "capped at 8" rather than adding a flag neither script's
  own procedure would ever consume.
- **R-6 (doctrine drift surfaced during Resolution c — NOT fixed here, routed).**
  `authorkit/skills/attention-audit/SKILL.md:75-77` describes "demote-to-wiring" as "set
  `disable-model-invocation: true` on a side reachable only by dispatch — agent-preloaded or
  Skill-tool-only"; harness canon says that flag blocks exactly those two paths
  (`skill-writing-rules:42`, `sweep-chores:27`). Under the estate's own rules a dmi:true skill is
  reachable ONLY by human `/name`. Recommendation to the coordinator: `file-bug` against
  authorkit (owner edits its own doctrine; a `doctrine-audit` judgment-edge or a `skill_lint`
  rule could mechanize it later). This LLD's own Phase 3 rule (the three-grep test) is written
  against the verified mechanics, not the drifted text — and this is precisely the finding class
  the skill exists to surface (a context artifact teaching a wrong lever).
- **R-7 (rent: one more resident description in the estate's most crowded plugin — harness
  already 19 707 routable chars, 35 skills).** Detection: attention-trend's next row. Fallback:
  the ≤ 700-char description and the reciprocal-fence pass are the mitigation; a later
  `attention-audit` may rule a merge (e.g. into check-everything's outer loop) if usage stays
  zero — accepted, disclosed.
- **Non-decisions, named (no ADR):** name (grammar-derived), home (anti-matrix reasoning), cadence
  (deferred by ruling), output contract (ruled upstream 2026-08-18) — none is a fork this LLD
  resolved that a future reader would ask "why" about beyond the sections above.

## Rejected alternatives

- **A greenfield analyzer that parses skill descriptions/bodies itself.** Rejected — re-implements
  `rent.py`/`collide.py`/`measure.py`; consume the CSV and `--rent`, name the owner (charter's
  own finding, kept).
- **A new agent seat (`estate-maintainer`/`retrospective-agent`) or `context: fork`.** Rejected —
  idr-0007's job-evidence test (no coordination gap the skill can't cover) and, decisively, the
  batched confirm needs `AskUserQuestion`, which a fork/agent does not have (gh#541).
- **Report-only or ticket-only output.** Rejected upstream — Kim's ruling (Findings comment,
  2026-08-18) fixes report + diffs behind one confirm; not reopened.
- **Designing "fix via context" on the invocation flags as stated.** Rejected — Resolution c:
  partial premise; the both-flags state is dead, `user-invocable` is inert.
- **A `check-`-head name (`check-estate`) or `estate-audit`-adjacent naming.** Rejected — the
  skill proposes and (post-confirm) applies; `check-` signals verify-only, and `*-audit` is
  authorkit's static-instrument family.
- **A persistent per-run checkpoint (`estate-maintenance-checkpoint.json`) for census deltas.**
  Rejected for v1 — the trend CSVs already carry the series that matter, memory `modified` dates
  and issue timestamps carry the rest, and a third state file would be growth with no consumer
  (lld-0016's same rejection). Named as a possible v2 seam beside the cost ledger.
- **Building scheduling now via `CronCreate`/a routine file.** Rejected — gh#626 owns the
  calendar mechanism; this LLD ships the calendar row and the no-human-channel branch only.
- **Extending `check-everything`'s outer loop with a retrospective mode, instead of a new skill**
  (repair added 2026-08-18, doc-checker pass). Rejected — `check-everything` is a plugin
  LINT-HEALTH instrument (structural, re-run-to-verify-clean); this skill's join is TEMPORAL and
  BEHAVIOURAL (memory/issue/decision history, re-triggerable diagnostic over time, not a
  pass/fail gate) — a different axis, not a mode flag on the same procedure. Not foreclosed
  permanently: R-7 already names a later `attention-audit`-ruled merge into check-everything's
  outer loop as a possible v2 move if usage stays zero; this rejection is about v1's shape, not a
  standing prohibition.
- **The "excessive ceremony" reading of the ticket's premise** (repair added 2026-08-18,
  doc-checker pass). Rejected/deferred, scope named explicitly — "ceremony" has two readings:
  (a) process/behavioural ceremony (redundant gates, verbose output, a procedure re-confirming
  what it already confirmed) and (b) context-surface SIZE (resident chars, entry-file/rules/
  memory bulk). This build's D4 detector measures reading (b) ONLY. Reading (a) is UNMEASURED in
  v1 — no detector here scores a procedure's own gate count or output verbosity — named as a
  future seam, not silently folded into D4's census.

## Agent verification

**Payload layer:** `collect.py selftest` (fixture estate → bundle shape; absent registered
source → `present:false`, never an exception) and `detect.py selftest` (seeded positives, clean
negative, evidence-pointer completeness, append-order rows) — deterministic, no model judgment.
AC-1's evidence re-open check is `detect.py --verify <findings.json>` (the one instrument,
repaired 2026-08-18 — see AC-1). **Mechanical layer:**
`skill_lint.py`, `eval_check.py`, `/check-routing harness`, `doc_lint.py --spine`,
`release_gate.py harness`, `collide.py --against` (build-time only). **Fresh-context critic:**
`skill-checker` on the new body and on any fenced sibling. **Human/judgment layer, stated
exception:** whether Phase 3's generalizations and root-source attributions are RIGHT is not
payload-checkable — it is exactly what the single confirm gate exists to catch, and a run whose
proposals are mostly declined is itself the signal to re-tune (R-1, R-4). Cadence fitness is
human-assert at gh#626 (Resolution e).

## Decomposition record

Two-plane manifest (`break-down-problem`, domain `technical-architecture`, `plan: true`):
19 nodes · 24 actions · 29 hosts · 12 edges; `coverage_check.py --strict` → `[OK] coverage clean
— both planes cross-check`, exit 0 (2026-08-18). OUTSIDE-IN = the surfaces in Components §1–9;
INSIDE-OUT = read five sources (a1–a5), detect four classes (a6–a9), judge (a10–a11, a24),
propose (a12–a13), confirm/apply (a14–a15), prove on fixture (a16), route/wire/ship (a17–a21),
future-input seam (a22), UNMEASURED discipline (a23). Every leaf carries the `accept` predicate
that became Components' gates. The manifest JSON is the builder's plan; it was meant to land
beside this LLD as `.claude/docs/decompositions/estate-maintenance-manifest-v1.json` in the
build PR (this planning dispatch was scoped to the LLD file alone, so the manifest was to be
handed off with the design-status report rather than written here).

**Dated note (2026-08-18, gh#645 minor-9):** that manifest file was NOT produced in the build
PR that shipped this skill (PR #645) — the builder dispatch that landed the code never received
the planner's manifest JSON to write through, only this LLD's own summary counts above. Amending
in place rather than fabricating a plausible-looking manifest with invented node/action/host
detail this builder never had. If the counts above (19 nodes · 24 actions · 29 hosts · 12 edges)
matter as a durable artifact, the planner seat is the one holding the actual manifest content.
