---
name: runtime-state
description: >-
  Locate — never export — session .jsonl transcripts: the CURRENT session's own transcript path
  plus its recent subagent transcripts (agent-*.jsonl, project/worktree-scoped dir), or a PAST
  session's by repo path or slug. Prints or clipboard-copies the path(s); zero new data written.
  Use for "where is my transcript", "find this session's jsonl", "path to grab for a bug report",
  "locate the subagent logs from this run", "transcript path for that old session". NOT the
  maximal debug-export bundle (fenced out, heavier follow-up); NOT a Stop hook (#466); NOT
  reading/summarizing transcript content (paths only).
disable-model-invocation: false
user-invocable: true
---

# runtime-state

A locator, not a bundler. The whole job is answering one question — "where on disk is the
transcript I want" — for the live session or a past one, and it never writes anything new: no
zip, no copy of transcript bytes, no export directory. The one write this skill ever performs is
an OS clipboard copy of a path STRING, opt-in, when asked.

## Why this exists (and why it's this small)

Issue #605 asked, over three folded findings, for progressively less: first a maximal custom
debug-export bundle (2026-08-17), then a re-home to a different repo entirely (2026-08-18), then
— on the actual `find-intent` round that made this ticket buildable (2026-08-19) — a plain
locator over transcripts that already exist. The heavier bundle stays fenced out on the record;
build it only if this locator turns out insufficient for filing a platform bug. No Stop hook:
this estate retired every plugin hook (#466) and that ruling isn't reopened for this ticket.

## What it resolves

Every session's transcripts live under `~/.claude/projects/<slug>/` (or the host's own configured
Claude home), where `<slug>` is the session's own working directory with every `/` and `.`
character replaced by `-` — a plain checkout (`/Users/x/proj`) becomes `-Users-x-proj`; a
worktree-scoped one (`/Users/x/proj/.claude/worktrees/fix-1`) becomes
`-Users-x-proj--claude-worktrees-fix-1` (yes, double-dash — the `/` before `.claude` and the `.`
itself each become their own `-`; verified against this machine's own real `~/.claude/projects/`
directory names during this build, not assumed from documentation alone).

Under that directory:

- the session's own transcript: `<session-id>.jsonl`, directly at the top level
- its subagents' transcripts: `<session-id>/subagents/agent-*.jsonl` (a sibling
  `agent-*.meta.json` per subagent is metadata, never a transcript — never counted or listed)

## Resolving "current"

The live Claude Code process sets `CLAUDE_CODE_SESSION_ID` in every session's own environment —
verified to match the on-disk transcript filename stem exactly. So the zero-setup path is: derive
the slug from cwd, read that env var, done. No env var (or an explicit ask about a DIFFERENT,
past session) falls back to the newest top-level `*.jsonl` under the resolved project dir, and
says so — it never silently guesses without disclosing which branch fired and how many
candidates it saw.

## Running it

```
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py                      # current session, cwd-derived
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --repo-root <path>    # a specific checkout/worktree
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --slug <slug>         # a slug you already have
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --session-id <id>     # pin an exact past session
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --limit 10            # more/fewer subagent rows
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --copy                # clipboard-copy the path
${CLAUDE_SKILL_DIR}/scripts/transcript_locate.py --json                # machine-readable
```

No args is the deliberately-meaningful default (disclosed in the script's own docstring, same
shape as `check-state`'s `doc_state.py`): it resolves the CURRENT session, live, which is this
skill's entire reason to exist — a bare invocation should never dead-end on a usage message.

Exit 0 = the main transcript resolved and exists on disk. Exit 1 = it does not (wrong slug, no
session, or a genuinely un-journaled one) — a findings result, not a crash; the report still
prints whatever WAS resolved. Exit 2 = a usage error.

## Fenced explicitly (do not re-litigate here)

- **Not the maximal bundle.** Full transcript export form, settings snapshot, output files from
  background tasks, workflow `journal.jsonl` — all deliberately out (2026-08-17 finding). Revisit
  only if this locator proves insufficient for filing a platform bug against transcript-derived
  evidence.
- **Not a hook.** No Stop-hook auto-export, ever, per #466's estate-wide retirement.
- **Not a content reader.** This resolves and prints PATHS. Reading, summarizing, or grepping a
  transcript's own JSONL content is a different job for a different turn.

## References
None — the procedure above and the script's own docstring are the whole contract; no
`references/` corpus earns a place here.
