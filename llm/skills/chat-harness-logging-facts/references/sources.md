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

## The nonoun-plugins workspace's own measured check-routing history — a worked instance, real and dated

A genuine, inspectable measurement history from this workspace's own skill corpus — cited as proof
the routing-accuracy discipline works in practice, not as a universal template every project must
copy verbatim.

- **`agent-protocols` plugin, `skills/a2ui-chat-agent-facts/evals/evals.json`, its `"note"` field**
  — read and quoted in full in routing-accuracy-evals.md. A real, dated record (2026-07-09 blind
  run and estate-wide run, both 33/36) distinguishing judge noise, a real fixable regression, and a
  structural leak — three outcomes a routing-accuracy measurement must be able to tell apart.
- **The dual-schema `scripts/routing-corpus.json` / `evals/evals.json` pattern** — present, checked
  directly, in every skill of the `llm` plugin (`llm-gateway-facts`, `llm-streaming-facts`, and
  this pack), each a held-out `{id, prompt, expect}` case set mechanically validated by this
  workspace's own `eval_check.py` (`E1`-`E5` rules, verified directly from that script's own rule
  comments and code).
- **The `routing-judge` agent** — verified directly from its own definition file,
  `/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/agents/routing-judge.md`: frontmatter
  `tools: []` (a genuinely empty allowlist, not merely a claim in prose), dispatched with only a
  skill-description menu and shuffled, expectation-stripped prompts as its stated "ENTIRE world."
  Cited as a real, worked instance of a deliberately blind measurer — not a hypothetical design
  this pack recommends in the abstract.

## Boundary — layers owned elsewhere

This pack answers how a harness observes and measures its own behavior; it does not restate its
neighbors. Composing the agents that DO the work being observed is
[[chat-harness-workflow-facts]]. The routing MECHANISM itself — how a skill gets
selected at discovery time, as opposed to how its accuracy is measured after the fact — is
[[chat-harness-routing-facts]]. Building an actual logging pipeline, eval harness, or
notification integration for a project is that project's own build seat; this pack teaches the
pattern, it owns no codebase's source.

## Provenance — 2026-08-17 knowledge-harvest fold (issue #526)

`turn-trace-and-failure-diagnostics.md` and `metric-integrity-and-progress-delivery.md` were
added from agent-ui#1115's "Scope-conformant revision v2" comment (posted
2026-08-17T17:14:57Z), the litmus-filtered re-harvest of `@agent-ui/a2ui` lessons kept to
web-based virtual-chat-harness knowledge only. Lesson 39's dropped (CLI-tier) half — the
`prompt-drift`/`prompt-equivalence` test-gate mechanism — was already excluded by v2 itself as
development-side, not this pack's concern; the KEPT half of lesson 39 was evaluated and SKIPPED
here as hard dedup — already covered by [[chat-harness-guardrail-facts]]'s own
`config-schema-and-prompt-externalization.md`, even though v2 filed the kept half under this
pack's own axis.

## Provenance — 2026-08-19 provider-doctrine fold (agent-ui live-eval practice)

`live-turn-acceptance-and-replay-ci.md` was added 2026-08-19: the replay-CI/live-acceptance
two-tier split (agent-ui ADR-0200 clause 3 + Consequences, read via the GitHub API), the
fresh-server/OS-allocated-port/proven-teardown acceptance shape (agent-ui `scripts/e2e-devtools.mjs`,
GH #1145, read at that repo's HEAD 2026-08-19), and the bait-the-defect acceptance discipline
(agent-ui #1101's closing live-verification comment, 2026-08-17, quoted verbatim from the GitHub
API). Placement judgment, recorded: the dispatching brief offered `chat-harness-tool-facts` as the
default home "or the pack that owns testing patterns" — this pack owns the measurement/proof
axis (its own charter: "how a chat-agent harness proves what it actually did"), and tool-facts owns
extension surfaces, so the axis landed here; the fence against `routing-accuracy-evals.md` (many
judged routing cases vs. one engineered end-to-end turn) is stated in both the new file and the
consult table.
