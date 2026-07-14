# Sources — provenance for the observability-pattern claims

This pack teaches how a chat-agent harness makes its own behavior legible — each claim is grounded
in one of two genuinely different kinds of evidence, and the reference files say which for every
claim. Neither kind outranks the other; they answer different questions ("is this how the platform
currently behaves" vs. "is this a real, measured instance of the discipline working").

## Claude Code's own hook and notification mechanics — a platform fact, verify against current docs if this pack ages

Facts about how this harness's own tooling behaves at the time this pack was written. These can
drift as the harness versions — if a claim here disagrees with the CURRENT tool descriptions or
hook documentation, the current behavior wins and this pack needs repair.

- **Lifecycle hooks** (`PreToolUse`, `PostToolUse`, and siblings) — registered against a `matcher`
  and a `command`, fire deterministically around a real tool-call event, and can log, block, or
  transform. Verified directly from a real, currently-installed hook registration:
  `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/hooks/hooks.json` (a
  `PostToolUse` hook, matcher `"Write|Edit"`, running `skill_lint.py --hook`, `statusMessage:
  "skill-postwrite-invocation-lint"`), cross-checked against the exact description-length
  finding it can produce in
  `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/scripts/skill_lint.py`
  (rules `F5`/`W1`, the file's own lines ~168-182).
- **Background-task notification** — a background-dispatched agent's completion is delivered to
  the caller automatically, without polling. Verified directly from this session's own governing
  tool instructions (the Agent tool's own description, this session): *"Agents run in the
  background by default. When an agent runs in the background, you will be automatically notified
  when it completes — do NOT sleep, poll, or proactively check on its progress... when
  harness-tracked work finishes, you are re-invoked automatically."*
- **A separate, deliberately poll-based mechanism for genuinely external state** — verified
  directly from this session's own Monitor tool description, including its own explicit cadence
  guidance (*"Poll intervals: 30s+ for remote APIs (rate limits), 0.5-1s for local checks"*) and a
  worked example of polling an external system ("Poll GitHub for new PR comments"). **Caveat, held
  once here rather than per-claim:** a THIRD, purely time-based scheduling primitive also exists in
  this harness — verified directly from this session's own `schedule` capability description
  ("scheduled cloud agents... on a cron schedule," explicitly covering "a one-time scheduled run"
  like "remind me tomorrow") — a distinct case from state-watching: a "check-again-later" ask, not
  an "is X done yet" ask. A fourth, narrower mechanism scoped to resuming a `/loop`'s own
  self-pacing between iterations was deliberately NOT named here, since it resumes one standing
  session's own recurring work rather than serving an arbitrary future-dispatch ask — naming it
  would have overreached this pack's own verification. Exact tool/skill names are this harness's
  own and may rename across versions; the multi-mechanism SHAPE (native completion notification vs.
  deliberately-paced external polling) is the portable claim, not any specific tool's name.

## The nonoun-plugins workspace's own measured eval-run history — a worked instance, real and dated

A genuine, inspectable measurement history from this workspace's own skill corpus — cited as proof
the routing-accuracy discipline works in practice, not as a universal template every project must
copy verbatim.

- **`agentic-ui` plugin, `skills/a2ui-conversational-agent/evals/evals.json`, its `"note"` field**
  — read and quoted in full in routing-accuracy-evals.md. A real, dated record (2026-07-09 blind
  run and estate-wide run, both 33/36) distinguishing judge noise, a real fixable regression, and a
  structural leak — three outcomes a routing-accuracy measurement must be able to tell apart.
- **The dual-schema `scripts/routing-corpus.json` / `evals/evals.json` pattern** — present, checked
  directly, in every skill of the `llm` plugin (`llm-provider-gateway`, `llm-jsonl-streaming`, and
  this pack), each a held-out `{id, prompt, expect}` case set mechanically validated by this
  workspace's own `eval_check.py` (`E1`-`E5` rules, verified directly from that script's own rule
  comments and code).
- **The `eval-judge` agent** — verified directly from its own definition file,
  `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/agents/eval-judge.md`: frontmatter
  `tools: []` (a genuinely empty allowlist, not merely a claim in prose), dispatched with only a
  skill-description menu and shuffled, expectation-stripped prompts as its stated "ENTIRE world."
  Cited as a real, worked instance of a deliberately blind measurer — not a hypothetical design
  this pack recommends in the abstract.

## Boundary — layers owned elsewhere

This pack answers how a harness observes and measures its own behavior; it does not restate its
neighbors. Composing the agents that DO the work being observed is
[[chat-harness-orchestration-and-workflows]]. The routing MECHANISM itself — how a skill gets
selected at discovery time, as opposed to how its accuracy is measured after the fact — is
[[chat-harness-skills-and-routing]]. Building an actual logging pipeline, eval harness, or
notification integration for a project is that project's own build seat; this pack teaches the
pattern, it owns no codebase's source.
