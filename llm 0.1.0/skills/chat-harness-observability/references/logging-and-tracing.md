# Logging and tracing — what the harness actually did, not what the user typed

> Axis: how a chat-agent harness makes its own actions legible as structured, queryable events —
> distinct from the raw conversation transcript. Grounded in this harness's own lifecycle-hook
> mechanics (a platform fact) and a worked instance: the forge plugin's own `PostToolUse` hook.

## The core distinction — a transcript proves what was SAID, a hook proves what HAPPENED

**Claim:** a session transcript (the full back-and-forth of user and assistant turns) is a record
of what was *communicated* — it is unstructured, not filterable ahead of time by event type, and
it conflates "the model said it would do X" with "X actually happened and produced a specific,
mechanical outcome." A lifecycle hook is a different kind of record entirely: it fires
**deterministically**, tied to a **named event class** (a tool about to run, a tool that just
ran), and it can carry a **structured finding**, not prose. **Why this distinction matters (the
failure mode it prevents):** if the only observability a harness has is "read back the
conversation," there is no way to answer "did the enforcement mechanism actually fire" without
re-reading and interpreting the whole exchange — a hook log answers that in one line, keyed by
event and matcher, with no interpretation required.

## Platform fact — hooks fire around real events, not around what the model narrates

**Platform fact (this harness):** lifecycle hooks (e.g. `PreToolUse`, matching *before* a tool
call executes; `PostToolUse`, matching *after* one completes) are registered against a `matcher`
(a tool-name pattern) and a `command` to run; the hook can log, block, or transform the
surrounding action. This is enforced by the harness itself, independent of anything the model
decides to say about its own behavior — a hook fires on the event class it's bound to, every
time, or it does not fire at all.

**Worked instance — a real, currently-installed hook:**
`/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/hooks/hooks.json` registers a
`PostToolUse` hook (matcher `"Write|Edit"`) that runs
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/skill_lint.py" --hook`, with
`"statusMessage": "skill-postwrite-invocation-lint"`. This hook fires on **every** `Write` or
`Edit` tool call in a session where this plugin is installed — it does not need the model to
decide to check its own work; the check runs regardless. The script it invokes,
`skill_lint.py`, carries a specific, mechanically-checkable rule (`F5`/`W1`,
`skill_lint.py:175-182`) that a `SKILL.md` file's `description` (+ `when_to_use` if present) must
stay under fixed character caps (1536 combined, 1024 for `description` alone) — a violation
produces an exact, quotable finding string (e.g. `"description+when_to_use is {N} chars -> cut to
<=1536"`), not a vague "this seems long." **This is the concrete shape a hook-based observability
signal takes:** a specific tool call, a specific matcher, a specific mechanical finding — logged
or surfaced the moment the event happens, not reconstructed later from prose.

## What to log — the event class and the finding, not a narrative summary

**Recommendation, not a universal law:** a hook-based trace record should carry (1) which event
fired (`PreToolUse` vs `PostToolUse` — before vs after matters, since a `PreToolUse` hook can still
block the action, while a `PostToolUse` hook can only react to something already done), (2) the
matcher that caught it (which tool, or tool pattern), and (3) the deterministic outcome (allowed /
blocked / transformed, plus the specific finding text if the hook's script produced one) — never a
paraphrased narrative of "the agent tried to do something and it got sorted out." **Failure mode
this prevents:** a narrative log ("the write was handled correctly") is unfalsifiable after the
fact — a structured log entry naming the exact matcher and exact finding string can be grepped,
diffed against a prior run, and used as regression evidence; a narrative summary cannot.

## Hooks are not the only structured signal, but they are the deterministic one

**Claim:** a harness may expose other structured signals alongside hooks (e.g. this harness's own
background-task notifications, covered in background-task-notification — a different event class
entirely, tied to async work completing rather than to a tool call). The property that makes a
hook specifically useful for *tracing what the harness did* is that it is bound to a **matcher**
at **registration time**, before any specific session runs — it is not something the model can
choose to skip narrating. A background-task notification is deterministic in the same sense (it
fires on completion, always) but answers a different question (did the async work finish, not did
this specific tool call get enforced).

## What this file does NOT cover

Measuring whether the harness's *routing* decisions (which skill fired, or didn't) are accurate
over time — a distinct concern from logging that a tool call happened at all
(routing-accuracy-evals) · notifying a human when a background task completes, as opposed to
logging a synchronous tool-call event (background-task-notification) · the provenance split
between "this is how the platform's hook mechanism behaves" and "this is one plugin's own hook
instance" (sources).
