# Gate-first mode — validator-authored executable acceptance gates (gh#939, LLD-0026)

Cited from `dispatch-ticket/SKILL.md`'s Phase 4 (grant + validator dispatch) and Phase 5 (the
gate-green precondition on stage 2a's hold) rather than restated inline — the same F6
split-to-references pattern as `isolation-ladder.md` and `spec-lock-gate.md`.

**Default is off.** With no `gate-first: authorized` line in the sealed dispatch prompt, this
mode does not exist — Phase 4's text path is byte-for-byte today's behavior.

## Grant detection

Read the sealed dispatch prompt for the literal line `gate-first: authorized` — the
`auto-merge: authorized` / `accept-grant: authorized` idiom: explicit, never inferred from
`size:small`, "unattended", or tone. Absent → this file's procedure does not run. Present →
continue to the kind guard below.

## Kind guard (Resolution 2)

Gate-first ships on the feature path only: `kind: feature` and Phase 2's default arm. A `task`-
or `bug`-kind record never reaches this file (task has no round structure for FAIL-feedback to
thread through; bug is `file-bug`'s lifecycle).

## Qualifying test — is the Acceptance section mechanizable

The validator applies `script-writing-rules`' own mechanization test to the ticket's Acceptance
section as its first act: every explicit requirement must map to a pass/fail function over repo
state, command exit codes, or observable behavior. A record whose acceptance is judgment wearing
a costume (wording quality, "reads well", consolidating/administrative/knowledge-shaped records)
fails the test.

- **Fails →** return `gate-infeasible: <the requirement that fails the mechanization test>`.
  The dispatch proceeds on the DEFAULT (no-gate) path with this return recorded in Findings —
  never a weakened gate, never an existence check standing in for content/behavior, never checks
  the request didn't ask for.
- **Passes →** author the gate (below).

## Validator dispatch contract

The validator is a checker-CLASS dispatch, not a named agent (anti-matrix bar: one caller, one
moment in one skill's lifecycle) — `general-purpose`, **`model: sonnet` stated explicitly**
(#313/#919's ad-hoc-dispatch tiering, same as this skill's own task-kind dispatch), **unnamed and
synchronous** (the no-nested-wait preamble's discipline — its tool-result IS the return value).
Tools: read-only against the build's scratch clone (`Read`, `Grep`, `Glob`, `Bash` for read-only
inspection only) plus `Write` scoped to the gate directory alone (Resolution 1, below) — the
validator never writes inside the clone.

The sealed prompt hands the validator: the ticket's Acceptance section verbatim, the clone path
(read-only), and the gate directory path to write into. It authors ONE script,
`gate_<id>.py`, per `harness:script-writing-rules` (tri-state exit: 0 green / 1 FAIL lines on
stdout / 2 usage-or-tamper; one PASS/FAIL line per check; each FAIL naming expected-vs-actual +
exact path + exactly what to do; a `selftest` mode where sensible per the acceptance predicates
being checked).

**Authored-gate acceptance rules (the validator's own contract, prose not code):**

- **No proxy.** A file existing is not the same as its content or behavior being correct — check
  the thing the Acceptance line actually asserts, not a cheaper stand-in.
- **No scope creep.** Check only what the ticket's Acceptance section asks; inventing additional
  checks the ticket never named is out of bounds, same as under-checking.
- **Fails against current state.** The gate is authored to fail on the clone AS IT STANDS
  (pre-build) and pass once the build satisfies it — never authored to already pass trivially.

Validator return (typed): `gate-authored: <path> · checks: <n> · ticket-comment: <url>` (once the
gate is posted per Resolution 1 below) or `gate-infeasible: <requirement>` (Qualifying test
above).

## Resolution 1 — where the gate lives, and the durable copy

The executable gate lands at `<scratch-parent>/gate-<id>/gate_<id>.py` — a sibling of the build's
scratch clone (isolation-ladder Rung 2's own parent directory), never inside it. The builder's
sealed dispatch prompt enumerates ONLY the clone path, so the gate sits outside everything the
builder was handed. `gate_guard.py` (below) SHA-256-hashes the gate before every run and refuses
a changed hash with a loud `gate-tampered` failure — directory-scoping plus hash-detection, not
OS-level enforcement; the stack has no stronger primitive today. **The leader (never the
validator, whose own tools are read-only-plus-Write-to-the-gate-dir, never a hash-recording
Bash call) runs `gate_guard.py record <gate>` immediately on the validator's `gate-authored`
return** — before the first `gate_guard.py run` of Resolution 3's loop, since `run` hard-refuses
to execute a gate with no recorded hash at all.

Because scratch clones are torn down (Phase 3's teardown bullet), the moment the validator
finishes, post the gate script verbatim as a `gh issue comment` on the ticket — the same
write-back verb the Findings contract already uses. This is the durable "ticket artifact" for a
backend (git-native) with no other artifact store.

The one legitimate write to the gate after authoring is `loop-rules`' gate-repair privilege
(#938/#941, cited not restated): scoped to this one file, its byte-diff + audit-copy +
immediate-drop mechanics apply as written there, and the repaired gate is re-posted to the ticket
as a second comment naming the repair. **The leader re-runs `gate_guard.py record <gate>`
immediately after any repair lands** (the LLD's own Data section: the `.sha256` is recorded at
authoring AND after any triage repair) — the repaired-gate re-run this charges no try to
(Resolution 4) still requires a fresh recorded hash before it can run at all.

## Resolution 3 — the round loop (gate rounds ARE the existing `/goal` try-cap's tries)

No second loop. Phase 5 already wraps the feature path in a `/goal` with capped tries and an
escalate-on-same-failure clause; gate-first makes that loop's stopping predicate mechanical.
Per round:

1. Builder builds in the clone (small: inline in the dispatching seat's own tree, per the
   no-nested-wait rule; big: the `builder` seat, re-dispatched sealed).
2. The seat running `dispatch-ticket` (the leader) runs `gate_guard.py run <gate> <clone>` —
   hash-check, bounded execution, exit + per-check lines captured.
3. Exit 0 → gate green; proceed to the untouched fresh-context checker pass and Phase 5 stage 2a.
   The gate-green line and round count join stage 4's typed handoff.
4. Exit 1 → the FAIL lines — verbatim, unedited, unsummarized (a leader paraphrase is a second
   hallucination surface) — become the entire work instruction of the next round's sealed prompt,
   alongside the unchanged ticket reference. Loop to step 1.

The gate runs BEFORE stage 2a's hold: a build that cannot pass its own ticket's letter never
reaches the accept marker. On a big build the coordinator owns steps 2–4; on a small build the
`build-leader`/host seat does — either way the BUILDER never runs or reads the gate file
directly, only its output lines relayed by the leader.

## Resolution 4 — round cap: 3, triage inside it not beside it

Default cap of 3 gate rounds (matching this workspace's established gate-as-goal convention —
`loop-rules`' gates table). The FAIL loop feeds the SAME `loop-rules` triage-diagnostician
mechanism (`teamwork/skills/loop-rules/SKILL.md` §Escalation, cited not restated) — it is not a
separate budget. The same named PASS/FAIL check failing twice consecutively fires the
diagnostician mid-loop; its gate-repair privilege (scoped to `gate_<id>.py` alone, exactly once,
if and only if the gate itself is defective) is available exactly there, and a repaired-gate
re-run charges no try.

A second identical failure AFTER diagnosis, or the 3-round cap exhausting, ends the run through
`dispatch-ticket`'s existing "unresolved gate failure" Failure branch (claim released per Phase
3, failure recorded in Findings, ticket stays `doing`), naming `gate-rounds-exhausted` with the
final FAIL lines quoted verbatim.

## Handoff fields (Phase 5 stage 4, only when the mode armed)

`gate-rounds: <k>/3 · gate-final: green|gate-rounds-exhausted|gate-infeasible|gate-tampered ·
gate-comment: <url>`

## The critic non-conflation rule (Non-goals, stated here as the standing rule)

**A green gate never discharges the fresh-context semantic-edit critic invariant**
(`.claude/rules/plugin-authoring.md`). The gate proves the LETTER of the request mechanically
(files, exit codes, behavior); the checker judges QUALITY and semantics. The existing
fresh-context checker pass on any prompt-carrying-artifact edit stays exactly where it is,
unchanged, as the semantic layer on top of a green gate — never skipped, never weakened, never
treated as redundant with it. A future reader who conflates the two has misread this section,
which exists to be cited against exactly that conflation.
