---
doc-type: lld
id: lld-0012-fleet-state-rollup
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#620
spec: none — #620's own Acceptance section states the checkable criteria; the shape/depth
  questions it left open (Scope/Open) are exactly what this LLD rules on, so a standalone SPEC
  would duplicate rather than add (doc-writing-rules' own routing test; same call as lld-0007).
---
# LLD — Fleet-wide cross-repo state rollup: `check-state` gains a `--fleet` scope (#620)

**Verdict, head-first: this is a SCOPE on the existing seat, not a new one.** `check-state`
already owns the collector/report/checkpoint pattern this ticket needs; `teamwork:fleet-rules`
already owns the fleet CONCEPT (coordination scope, claim protocol, version-slot rules) but is a
knowledge/doctrine skill, not a report generator — nothing there executes a sweep. A brand-new
teamwork skill would duplicate `check-state`'s collector/report/checkpoint machinery wholesale for
zero new job evidence (the anti-matrix test, `plan-plugin-split`'s job-evidence rule, restated by
`fleet-rules`' own Design §9 for new seats/flows): no isolation need, no concurrency, no
generator≠critic split distinguishes "state of one repo" from "state of several repos read the
same way." Home: **harness, `check-state/scripts/fleet_state.py`**, a fourth collector alongside
`git_state`/`ticket_state`/`doc_state`, gated behind an explicit `--fleet <repo-list>` flag so the
existing single-repo path is behaviorally untouched.

The four charter rulings (#620 Scope/Open), verdict-first:

1. **Home (harness vs. teamwork)** — harness, per the anti-matrix reasoning above. `fleet-rules`
   gains one citation line pointing at this collector as its worked report-side realization
   (mirroring how it already cites `dispatch-ticket` for the claim mechanics) — never a
   restatement of collector logic in a doctrine file.
2. **Repo-set enumeration** — **explicit list only** (`--fleet <path1,path2,...>`, local
   filesystem paths — every repo this machine can read is a normal sibling checkout, e.g. a
   worktree or an adjacent clone). `fleet.json` extension (a durable, named repo roster) is
   explicitly REJECTED for this ticket (Rejected alternatives RA1) — a follow-up, not this slice.
   Auto-discovery (walking the filesystem for git repos) is never considered: unbounded,
   security-relevant (surfacing repos never intentionally in scope), and explicitly ruled out by
   the seed.
3. **Drift-detection depth** — the #582 stale-copy shape: for every path in `--fleet` that is
   itself a **marketplace source repo** (carries `.claude-plugin/marketplace.json`), diff each
   listed plugin's own `.claude-plugin/plugin.json` version against the version directories
   present under this machine's shared `~/.claude/plugins/cache/<marketplace>/<plugin>/` — the
   plugin cache is a per-machine, per-user directory (not per-repo), so this is the actual
   observable proxy for "a repo's session hasn't reloaded a shipped fix yet." A `--fleet` path
   that is a pure plugin *consumer* (no marketplace.json of its own — the ordinary shape for a
   sibling repo like gen-ui-kit) reports its drift row as N/A, not UNMEASURED — it is not a
   source repo, so there is nothing to diff; conflating "not applicable" with "couldn't measure"
   would misreport a healthy consumer as broken. Cross-repo consolidating-record citation edges
   ride the same per-repo open-issue collection this slice already does (Components C2).
4. **Assert layer** — script-shaped (Acceptance's own fallback: "if delivered as a
   script/collector … payload-layer asserts on the report structure against fixture repos").
   `fleet_state.py` ships a `selftest` mode with inline fixtures per `.claude/rules/scripts.md` —
   negative + reverse controls on every classifier (reachable/unreachable, drift/in-sync/N-A,
   citation-edge resolved/unresolved, tracker pair OPEN/CLOSED/mismatched) — never a live network
   call in the fixture path.

## Components

### C1 — `fleet_state.py`: the fourth collector

New file: `harness/skills/check-state/scripts/fleet_state.py`, same anatomy as its three
siblings (`git_state.py`, `ticket_state.py`, `doc_state.py`): JSON out, exit 0/1/2, `selftest`
subcommand, read-only — issues zero mutating git/gh command, matching the skill's own charter
("never issues a mutating git/gh command").

```
fleet_state.py --repos <path1,path2,...> [--trackers <path-to-json>]
fleet_state.py selftest
```

Per-repo row (never omitted, always present even when unreachable):

| Field | Meaning |
|---|---|
| `path` | as given |
| `reachable` | bool — `git rev-parse --git-dir` succeeds AND `gh` (if invoked) doesn't error |
| `reason` | populated only when `reachable: false` — "path not found" / "not a git repo" / "`gh` unauthenticated" / "non-GitHub backend" |
| `owner_repo` | parsed from `git remote get-url origin`, or `null` when unreachable/non-GitHub |
| `open_work` | `{issues_open, prs_open, in_flight: [...]}` — `in_flight` reads the `in-flight` label (ADR-0005/`fleet-rules` §2) via `gh issue list --label in-flight --json number,title,url`; `null` when unreachable |
| `marketplace` | `{name, plugins: [{name, repo_version, cache_versions: [...], status}]}` when the repo carries its own `.claude-plugin/marketplace.json`; else the literal string `"not-a-source-repo"` (N/A, not UNMEASURED, per ruling 3) |
| `citation_edges` | `[{from_issue, to, target_state}]` — every OPEN issue's body matching a cross-repo reference (I3's amended pattern below), each resolved via one `gh issue view <owner/repo> <num> --json state,title,url`; an unresolvable target reports `target_state: "UNMEASURED"` with the raw ref preserved, never dropped. Resolution is memoized per run keyed on the fully-resolved `owner/repo#number` — never the raw match text, so the same bare shorthand cited under two DIFFERENT default owners (two different fleet repos both citing `gen-ui-kit#5`, implying different owners) resolves independently rather than colliding on one cache slot (code-checker finding, 2026-08-18) |

`status` values for a marketplace plugin row, precisely (amended 2026-08-18 per code-checker
review — the implementation's actual overlap handling, not the flattened summary this table
originally carried): `in-sync` (repo version present among cache versions AND is the highest);
`stale-cache` when EITHER the cache is empty, OR the repo version is absent from the cache and
numerically HIGHER than the highest cached version (the #582 case: a fix shipped in the repo,
ahead of what the local cache has ever seen); `repo-behind-cache` when EITHER the repo version is
absent from the cache and numerically LOWER than the highest cached version (the repo's working
copy hasn't pulled a release the cache already has), OR the repo version IS present in the cache
but a strictly higher version also exists there. The absent-and-lower case is not a second
"stale-copy" instance — it is the repo, not the cache, that's behind — so it takes the
behind-cache reading rather than folding into stale-cache.

### C2 — Trackers (platform-defect pairing)

`--trackers <path>` (optional) points at a JSON file: `[{"local": "owner/repo#NN", "upstream":
"owner/repo#NN"}, ...]`. Never invented by the script — the caller supplies it, or it's absent
and the section reports "no trackers file given" (a disclosed scope choice, not a failure). For
this repo, a seed file ships at `.claude/ops/fleet-trackers.json` naming the concrete pairing the
ticket names (#490/#609 vs `anthropics/claude-code#87349`) so a `--fleet` run against this repo
reproduces the Acceptance example directly. Each pair resolves both sides via one `gh issue view`
call each (read-only), reporting `local_state`/`upstream_state`; an unresolvable side reports
`UNMEASURED` for that side only — the pair itself is never dropped.

### C3 — `check-state` SKILL.md wiring

- `argument-hint` gains the two new flags: `"[repo-root] [--artifact] [--fleet <repo1,repo2,...>] [--trackers <path>]"`.
- Collect step (step 1) gains a fourth bullet, gated: "When `--fleet` is given, additionally run
  `fleet_state.py --repos <list> [--trackers <path-if-present>]`; feature-detect
  `<repo-root>/.claude/ops/fleet-trackers.json` and pass it automatically when no explicit
  `--trackers` was given." An unreachable repo in the list is a per-ROW UNMEASURED, never a
  whole-run failure — the report still renders for every repo that measured.
- Output contract gains a sixth section, **Fleet rollup**, rendered only when `--fleet` was
  passed: one sub-block per repo (open work, marketplace drift or N/A, citation edges), then the
  trackers block. Headed 🟢/🟡/🔴 per repo like every other section; an unreachable repo's row is
  🟡 by construction ("degrade gracefully… never silent").
- Failure branches gains one line: "`--fleet` repo unreachable → that repo's row reports
  UNMEASURED with the reason; every other repo's row and every other section still render."
- `description` frontmatter gains one clause naming the fleet scope (routing surface,
  `.claude/rules/plugin-authoring.md`) — `evals.json` gets matching cases (C4) in the same change.

### C4 — Evals + reciprocal fences

Two new `expect: trigger` cases exercising fleet-shaped phrasing ("give me a state rollup across
the repos our fleet touches", "check for version drift between this repo and gen-ui-kit"). No new
`no-trigger` fence is owed against a SIBLING skill: `fleet-rules` is a knowledge skill with
`disable-model-invocation` semantics distinguishing it as doctrine, not a competing report
generator, and the ticket's own "obvious steal risk" is exactly what choosing a `--fleet` SCOPE on
the same skill avoids (ruling 1) — there is no second skill to reciprocally fence against. One
existing case (`n05`, `/sweep-chores`) already fences the ops-family batch sweep; unchanged.

### C5 — `fleet-rules` citation (teamwork, one line, non-semantic)

`fleet-rules`' References table gains one row: `harness:check-state --fleet` → "the report-side
realization of fleet-wide state visibility; cited here, never restated — collector logic and
report shape live in `check-state` alone." A pointer, not a procedure copy; no version bump forced
on teamwork by this alone unless the file's own edit tier requires one (a table-row addition is
mechanical per `checking-rules`, not a semantic edit — no fresh-context checker owed for this
line, unlike the harness-side SKILL.md body edit in C3, which is semantic and does ride one).

## Interfaces

### I1 — CLI contract

```
fleet_state.py --repos /path/a,/path/b [--trackers /path/to/trackers.json]
```
Comma-separated, no spaces (consistent with existing skill conventions elsewhere in this repo);
a malformed invocation (missing `--repos`, empty list) exits 2 with `__doc__` printed, matching
the sibling collectors' usage-error contract.

### I2 — Marketplace/cache diff (the ruling-3 mechanism)

```
for repo in --repos:
  if <repo>/.claude-plugin/marketplace.json exists:
    for plugin in marketplace.json["plugins"]:
      repo_version   = read <repo>/<plugin.source>/.claude-plugin/plugin.json ["version"]
      cache_dir      = ~/.claude/plugins/cache/<marketplace.name>/<plugin.name>/
      cache_versions = sorted(dirnames in cache_dir) if cache_dir exists else []
      status = in-sync | stale-cache | repo-behind-cache   (per C1's table)
  else:
    marketplace = "not-a-source-repo"
```
Version comparison is semver-aware (tuple compare on dot-split integers), matching G14's own
monotonicity check elsewhere in this repo — cited, not re-derived; `fleet_state.py` implements
its own small comparator rather than importing G14's (different plugin-boundary — no
`harness/scripts/*` import crosses into a skill's own `scripts/`, per plugin-authoring's
boundary-hardness rule for preloads/paths, applied here to intra-plugin script imports too, kept
simple by duplication of ~5 lines rather than a cross-boundary import).

### I3 — Citation-edge resolution

**Amended 2026-08-18 (code-checker review), widening the pattern from the original owner/repo-only
draft.** Regex `\b(?:[\w.-]+/)?[A-Za-z][\w.-]*#\d+\b` over every OPEN issue body already fetched
for `open_work`, matching BOTH this workspace's actual citation shapes — a full `owner/repo#NN`
form (`anthropics/claude-code#87349`) and the bare-repo shorthand implying the SAME owner as the
citing repo (`gen-ui-kit#1593`, as #620's own body demonstrates live) — while a plain in-repo `#NN`
(no repo-name segment at all) never matches. Ruled in rather than reverted to the narrower
owner/repo-only form because the bare shorthand is this workspace's own attested convention (#620
Links: "gen-ui-kit#1593"), and reverting would silently miss the single concrete example the
ticket's own Acceptance section names. Accepted trade-off (Risk 2, amended): the wider pattern
raises the false-positive surface slightly (e.g. a stray `word#NN`-shaped token in prose) — a
false match resolves to `UNMEASURED` on a failed `gh issue view`, never crashes and never
misreports a wrong state as real. Each match resolved via `gh issue view <owner/repo> <number>
--json state,title,url` once, memoized per run keyed on the fully-resolved `owner/repo#number`
(never the raw match text — a bare shorthand's true owner varies by which repo is citing it, so
keying on raw text would collide two different targets under one cache slot).

## Data

### D1 — Build-slice manifest

| # | Slice | Files | Depends on |
|---|---|---|---|
| 1 | New collector `fleet_state.py` (C1, C2, I1–I3) + inline selftest fixtures | `harness/skills/check-state/scripts/fleet_state.py` (new) | this LLD |
| 2 | SKILL.md wiring (C3): argument-hint, step 1 bullet, Output contract section 6, failure-branch line, description clause | `harness/skills/check-state/SKILL.md` | 1 |
| 3 | Evals (C4) | `harness/skills/check-state/evals/evals.json` | 2 |
| 4 | Seed trackers file (C2) | `.claude/ops/fleet-trackers.json` (new, repo root) | 1 |
| 5 | `fleet-rules` citation row (C5) | `teamwork/skills/fleet-rules/SKILL.md` | 2 |
| 6 | Version bumps + ledger lines (both touched plugins) | `harness/.claude-plugin/plugin.json`, `harness/README.md`, `teamwork/.claude-plugin/plugin.json`, `teamwork/README.md` | 1–5 |
| 7 | Gates: `release_gate.py harness`, `release_gate.py teamwork`; `/check-routing harness` (description edit); fresh-context skill-checker pass over the SKILL.md body edit (C3, semantic) | — | 2–6 |

Acceptance predicates, checkable before the PR is called done:
- `doc_lint.py` green on this LLD.
- `python3 harness/skills/check-state/scripts/fleet_state.py selftest` exits 0.
- `release_gate.py harness` and `release_gate.py teamwork` both exit 0.
- Grep proofs: `fleet_state.py` contains no `git push`, `git commit`, `gh issue edit`, `gh pr
  merge`, or any other mutating verb; `SKILL.md`'s Output contract contains a `Fleet rollup`
  heading; `evals.json`'s case count increases by exactly 2, both `expect: trigger`.
- Behavioral acceptance (from #620's Acceptance, restated as predicates): a repo lacking
  `marketplace.json` reports `not-a-source-repo`, never `UNMEASURED`; an unreachable repo path
  reports `UNMEASURED` with a reason and does not abort the run; a stale-cache plugin version is
  distinguishable from an in-sync one in the JSON `status` field; the trackers section renders
  "no trackers file given" when neither `--trackers` nor the seed file is present.

## Risks

1. **Plugin-cache resolution assumption may not hold on every machine** (a machine with a
   differently-rooted `~/.claude` — e.g. `CLAUDE_CONFIG_DIR` override). Mitigation: read
   `CLAUDE_CONFIG_DIR` env var first, fall back to `~/.claude`; undetectable → the marketplace row
   reports `cache_versions: []` with a note, never a crash.
2. **Citation-edge regex over-matches** (a code snippet or file path inside an issue body
   resembling `owner/repo#NN`). Mitigation: accepted as a bounded false-positive risk — an
   unresolvable "match" simply reports `target_state: "UNMEASURED"` on `gh issue view` failure,
   which is indistinguishable from a real unreachable target but never crashes the run or reports
   a wrong state as if it were real.
3. **A large `--fleet` list inflates `gh` call volume** (N repos × per-repo issue/PR/citation
   calls). Mitigation: no pagination beyond the existing single-page `--limit` conventions
   `ticket_state.py` already uses; a fleet large enough to matter is a future follow-up (noted,
   not solved here — bounded scope per ruling 2's explicit-list-only choice).
4. **Non-decisions (no ADR here, per ADR-default-no):** (a) `--fleet`'s comma-separated CLI shape
   vs. a JSON list file is a convenience choice, reversible in one edit; (b) the trackers file's
   location convention (`.claude/ops/fleet-trackers.json`) mirrors `fleet.json`'s existing
   neighbor without ratifying a new durable-record contract — RA1 already defers the bigger
   fleet-roster question whole.
5. **Findings from the fresh-context `code-checker` pass (2026-08-18), fixed in the same change:**
   a slow or hung `gh` call inside citation/tracker resolution could raise
   `subprocess.TimeoutExpired` past the narrower except tuples and abort the WHOLE run instead of
   marking one edge/pair `UNMEASURED` — fixed by adding it to both catch sites; `gh auth status`
   ran once PER REPO (redundant subprocesses) and a missing `gh` binary raised `FileNotFoundError`
   out of `collect_repo` instead of a per-row reason — fixed by hoisting the check to once per
   run in `collect()`, with the binary-missing case folded into the same reason string; a
   malformed trackers-file pair (missing `local`/`upstream`, or a non-dict entry) raised an
   uncaught `KeyError`/`TypeError` — fixed by validating pair shape and reporting a
   `malformed pair` row instead of crashing. The G8 allowlist edit in `release_gate.py`
   (`cross-repo`, `source-repo`) was independently verified legitimate — neither token names any
   real skill or agent, both are ordinary prose the `-repo` suffix (already live via authorkit's
   `repo-audit`) would otherwise flag as phantom sibling citations.

## Rejected alternatives

- **RA1 — `fleet.json` extension for repo-set enumeration.** Rejected for THIS ticket: `fleet.json`
  today enumerates SEAT roles within one repo (roster of standing agents), not a cross-repo list;
  overloading it to also carry foreign repo paths conflates two different registries and the seed
  itself names this as a deliberate follow-up, not this slice's job.
- **RA2 — Auto-discovery of sibling repos on disk.** Rejected: unbounded (walks arbitrary
  directories), and silently including a repo never intentionally listed is exactly the kind of
  scope creep `fleet-rules` §1's coordination-scope ladder already rules out for peer discovery
  generally (`ListAgents` for discovery is banned there for the same reason) — never inferred,
  always explicit.
- **RA3 — A brand-new `teamwork:fleet-state` skill.** Rejected per the anti-matrix job-evidence
  test (Verdict, above): no isolation/concurrency/generator≠critic justification distinguishes
  this from `check-state`'s existing single-repo job; a new skill would duplicate the
  collector/report/checkpoint pattern for zero new capability.
- **RA4 — Live-cloning each foreign repo to inspect its plugin source directly**, rather than
  relying on the local `--repos` path already being a checkout. Rejected: mutating-adjacent
  (network calls, disk writes outside the scratchpad), and the seed's own "read-only across
  foreign repos" framing is satisfied more simply by requiring the caller to name an already-local
  path — cloning is the caller's job if they want a fresh copy, not this collector's.
- **RA5 — Deep drift semantics (comparing installed plugin CONTENT hash, not just version
  string).** Rejected: version string comparison is what #582 actually needed, and content-hash
  drift with an unchanged version number is a different, unreported defect class (a version bump
  discipline violation) this ticket's Acceptance doesn't ask for.

## Agent verification

No new harness-of-harnesses is required. `fleet_state.py selftest` (inline fixtures, no live `gh`/
network calls) proves every classifier — reachable/unreachable, in-sync/stale-cache/
repo-behind-cache/not-a-source-repo, citation-edge resolved/UNMEASURED, tracker pair resolved/
mismatched/UNMEASURED — per `.claude/rules/scripts.md`'s selftest requirement. `release_gate.py`
on both touched plugins (harness, teamwork) covers manifest/structure/lint/selftest-sweep/eval
validation. The semantic quality of the SKILL.md body edit (C3) is covered by a fresh-context
`harness:skill-checker` pass, per `.claude/rules/plugin-authoring.md`'s semantic-edit invariant —
an existing instrument, not a new one.
