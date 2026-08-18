---
name: check-reconstructibility
kind: skill
description: >-
  ADR-0022's own instrument ("the repo is the backup"): a read-only sweep reporting what a fresh
  machine + clone of `origin/main` could NOT recover today, classified committed /
  enrolled-with-mitigation / defect / open (the four named exceptions: memory dir, plugin cache,
  credentials, user-scoped state). Use for "what would we lose from a fresh clone", "run the
  reconstructibility audit", "check the estate against ADR-0022". Report-only. NOT estate naming/
  bloat/pattern conformance (authorkit's audit family — governance, not recovery); NOT
  worktree/branch/PR hygiene on THIS machine (harness:clean-git / repo-cleaner); NOT
  point-in-time work-state (harness:check-state).
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
own named exception list with a stated mitigation, or it is a defect. This skill is that
contract's own instrument.

## Procedure

1. Run the bundled script against the repo root:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-reconstructibility/scripts/audit_reconstructibility.py \
     --repo-root <path> [--claude-home <path>] [--config-home <path>] [--json]
   ```
2. Read the exit code and report first: 0 = swept clean; 1 = at least one defect (details in the
   `defects` list); 2 = usage error — `--repo-root` missing/not-a-dir, or no `.gitignore` at its
   root (never treated as "nothing ignored," always reported as the audit not having run). On
   exit 2, report the usage error itself, not a defect/enrolled/open classification.
3. Read the report verdict-first: `defects=<n> enrolled=<n> open=<n>`. Zero defects is the
   healthy state, not silence about the other two buckets — `enrolled` and `open` are both
   EXPECTED nonzero (the ADR names four real exceptions), never mistaken for a problem.
4. For every DEFECT, name the fix's owner rather than fixing it inline (this skill reports, never
   mutates): an uncategorized git-ignored-and-present path routes to whoever owns that local
   state (a chore, or `.gitignore` itself per `.claude/rules/gitignore-repair.md` if the path was
   genuinely retired); a missing mitigation doc (exceptions 2/3) routes back to the ticket that
   owes it; an untracked `.claude/ops/` file routes to `repo-cleaner` or a direct `git add`; a
   stray `.env*` file is escalated immediately, never left for a routine sweep.
5. For every OPEN item (exception 4's own class), state it as an ADR-0022 ratification gap, not
   a build failure — `adr-0022`'s own Open questions section already names this as unresolved;
   this skill's job is to keep surfacing it accurately release over release, not to resolve it.
6. Re-run after any of the ADR's four exceptions changes shape (a new committed mitigation doc, a
   `.gitignore` edit, a global `core.excludesFile` change, a new local build/cache artifact) — the
   delta between two runs IS the signal this instrument exists to produce; a single run is a
   snapshot, not a trend.

Done when the report's three buckets are read out loud with their evidence (not just the totals
line), every defect names its owning next step, and the open bucket is stated as an
ADR-0022-acknowledged gap rather than silently folded into "clean."
