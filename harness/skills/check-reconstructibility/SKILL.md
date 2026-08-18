---
name: check-reconstructibility
kind: skill
description: >-
  ADR-0022's own instrument ("the repo is the backup"): a read-only sweep reporting what a fresh
  machine plus a clone of `origin/main` could NOT recover today, classified into ADR-0022's own
  trichotomy — committed / enrolled-with-mitigation / defect (plus OPEN for exception 4's own
  still-unruled mitigation mechanism). Sweeps git-ignored-and-present paths, `.claude/ops/`
  tracking, a global `core.excludesFile` dependency, and the four named exceptions (memory dir,
  plugin cache, credentials, user-scoped `~/.claude`/`~/.config` state). Use for "what would we
  lose from a fresh clone", "run the reconstructibility audit", "check the estate against
  ADR-0022", "is anything load-bearing sitting uncommitted", or "did the plugin-reinstall/
  credential-runbook mitigations actually land". Report-only; mitigations ride tickets, never this
  skill. NOT for naming/bloat/attention/pattern/doctrine conformance across skills and agents
  (authorkit's estate-audit family — a different axis, estate GOVERNANCE not estate RECOVERY);
  NOT for worktree/branch/PR git-surface hygiene or executing a cleanup (harness:clean-git /
  repo-cleaner — this skill only reports what a FRESH machine couldn't recover, never proposes or
  executes a repair on THIS machine's git surface); NOT a point-in-time work-state report
  (harness:check-state — branches/PRs/drift, not the ADR-0022 recoverability delta); NOT the
  plugin-packaging/release health sweep (harness:check-everything).
author: kim
created: 2026-08-18
last_updated: 2026-08-18
disable-model-invocation: false
user-invocable: true
argument-hint: "[repo-root]"
---

# check-reconstructibility

ADR-0022's ratified contract: everything operationally load-bearing must be reconstructible from
a fresh machine plus a clone of `origin/main`, or it is committed, or it is enrolled in the ADR's
own named exception list with a stated mitigation, or it is a defect. This skill is the
instrument the ADR's own acceptance named but did not ship — the seed comment on gh#627 is
explicit: build only after Kim accepts adr-0022 (accepted 2026-08-18).

## Procedure

1. Run the bundled script against the repo root:
   ```
   python3 <this skill>/scripts/audit_reconstructibility.py --repo-root <path> [--json]
   ```
   `<this skill>` — chosen over `${CLAUDE_PLUGIN_ROOT}` here for consistency with this plugin's
   own script-invocation convention elsewhere in its skills (`clean-git`, `check-state`'s own
   procedure text) — a fresh-context skill-checker pass on this file confirmed no clash with
   `skill-writing-rules`' stated `${CLAUDE_SKILL_DIR}` preference is load-bearing enough to break
   that consistency for one skill alone.
2. Read the report verdict-first: `defects=<n> enrolled=<n> open=<n>`. Zero defects is the
   healthy state, not silence about the other two buckets — `enrolled` and `open` are both
   EXPECTED nonzero (the ADR names four real exceptions), never mistaken for a problem.
3. For every DEFECT, name the fix's owner rather than fixing it inline (this skill reports, never
   mutates): an uncategorized git-ignored-and-present path routes to whoever owns that local
   state (a chore, or `.gitignore` itself per `.claude/rules/gitignore-repair.md` if the path was
   genuinely retired); a missing mitigation doc (exceptions 2/3) routes back to the ticket that
   owes it (gh#627 at this writing); an untracked `.claude/ops/` file routes to `repo-cleaner` or
   a direct `git add`.
4. For every OPEN item (exception 4's own class), state it as an ADR-0022 ratification gap, not
   a build failure — `adr-0022`'s own Open questions section already names this as unresolved;
   this skill's job is to keep surfacing it accurately release over release, not to resolve it.
5. Re-run after any of the ADR's four exceptions changes shape (a new committed mitigation doc, a
   `.gitignore` edit, a global `core.excludesFile` change) — the delta between two runs IS the
   signal this instrument exists to produce; a single run is a snapshot, not a trend.

Done when the report's three buckets are read out loud with their evidence (not just the totals
line), every defect names its owning next step, and the open bucket is stated as an
ADR-0022-acknowledged gap rather than silently folded into "clean."

## Day-one baseline (this repo, run at ship time)

The first real run against this estate found the settings.local.json ignore rule living entirely
in the LOCAL machine's global `core.excludesFile` (`~/.config/git/ignore`), never in this repo's
own `.gitignore` — invisible to a fresh clone unless that global file is also provisioned, which
is exactly exception 4's "entirely outside any repo" case made concrete. `.claude/ops/` itself
proved fully tracked (ADR-0022's own stated fact, confirmed rather than assumed). Full numbers are
in this ticket's PR body and Findings write-back, not restated here — this section documents the
FINDING SHAPE (a real global-excludes dependency), not a number that goes stale the next run.
