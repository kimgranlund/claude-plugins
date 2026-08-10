# lead-build — forge intent record

Forged 2026-08-10 via /make-skill, third artifact of the /lead-* family (after the intake-lead
agent, PR #162, and /lead-intake, PR #163). Slots ruled during the family design; recorded, not
re-asked.

## Gate P0 — Route (PASS)

Primitive = **skill, command species**. The agent twin (`agents/build-lead.md`, ADR-0010)
exists; this is the host-adoption half — the `/lead-team` ↔ `team-lead` pattern, teamwork's
second instance, docs' `/lead-intake` being the first estate-wide sibling.

## Gate P1 — Interview slots (PASS, pre-ruled)

- **Trigger:** human types `/lead-build` when converting a session into a dedicated build seat
  (Kim's hand-rolled BUILD sessions, formalized). Command species — menu-register description.
- **Behavior delta:** ad hoc "you are my BUILD session" priming carries no record-first
  discipline, no state check on resumed tickets, no sizing floors — baseline evidence in
  `evals/baseline/`. With the skill: every target runs `dispatch-ticket`'s full procedure with
  the interactive branches ALIVE.
- **Species + dials:** Command — `disable-model-invocation: true`, `user-invocable: true`.
- **Freedom:** medium — read-and-adopt the agent file; drive each target through
  `dispatch-ticket` via the Skill tool.
- **Fences:** NOT the dispatched agent (`build-lead`, Agent tool); NOT one forked build
  (`/build-feature <id>` — one ticket, off-session); NOT batch find-and-confirm
  (`/mobilize-chores`); NOT a generic coordination charter (`/lead-team`).
- **Done-when:** adoption acknowledged; every target driven to dispatch-ticket's typed result
  (Findings write-backs included) or its named blocker; record-first never violated.

**The mechanism differs from /lead-intake, deliberately:** `dispatch-ticket` carries NO
`context: fork` (ADR-0010's design — no double hop from /build-feature's fork, no third hop
from build-lead). A host-session Skill invocation of it therefore runs INLINE in this session's
own turn — the fork hazard that forced /lead-intake's read-and-apply-inline workaround does not
exist here. The adoption is thin: read the agent file for the contract, then invoke
`dispatch-ticket` (Skill tool) per target, exactly as `/build-feature`'s own body does inside
its fork. One engine, three entries: forked one-shot (/build-feature), unattended seat
(build-lead), live standing seat (this command).

**Host deltas from the build-lead agent:**
1. **The interactive branches are ALIVE.** dispatch-ticket's Phase 1 ambiguous-match branch
   asks its one question instead of reporting a blocker, and the task-kind clarify round runs
   instead of straight-to-SKIPPED — the exact branches the agent's unattended context disables.
2. **Delivery is direct** — no teammate mode; each target's typed result is this session's own
   reply.
3. **Serial builds, one tree.** The agent's callers own the parallelism guard; here one session
   drives targets one at a time — mobilize-chores' mutating-dispatches-serialize rule holds by
   construction.

## Gate P2 — Evals (PASS)

- Trigger evals: skipped, recorded — command species, house precedent.
- Behavioral assertions: `evals/assertions.md` (4).
- Baseline: `evals/baseline/` — ad-hoc-primed BUILD session vs a CLOSED ticket id (state-check
  probe) and a raw vague ask (record-first probe).

## Gate P3 — Draft (PASS)

SKILL.md on disk; dials explicit; menu-register description; body lean — the engine is
referenced, never restated.

## Gate P4 — Language pass (PASS)

Instantiation core applied: adoption imperatives with checkable objects, deltas declarative,
branches named, predicate checkable, ≤ 3 hard gates.

## Gate P5 — Validate

- Lint: clean (one F3 angle-bracket catch in the description on first write, fixed; clean
  since).
- Fresh-context audit (`evals/audit-report.md`, 2026-08-10): verdict ship-after-one-major, the
  MAJOR in the ENGINE's files, not this skill. F1 (dispatch-ticket's caller enumeration
  excluded its third sanctioned caller — description said "never from a direct user ask",
  intro said "two reachable entry points"; build-feature's no-fork rationale enumerated two
  callers) — FIXED across all three sites, dispatch-ticket's description re-dieted to ≤700 in
  the same edit; boundary-tier disposition: dispatch-ticket owns no suite (disclosed since
  1.3.0) and its fences are unchanged, the routing re-judge rides the next wave boundary per
  the edit ladder's batching clause. F2 (baseline dir empty at audit read) — timing, landed
  minutes later; P2 stands. F3 (one copied engine line) — replaced with a citation. F4 (delta
  1 overclaim vs /build-feature's fork) — reworded to the true differentiator (the standing
  unforked seat). Checkpoint nit (three-entries line too narrow) — fixed.
- Behavior check (`evals/behavior-check.md`, 2026-08-10): assertions 1/2/4 PASS on grounded
  probes (real gh state behind both); assertion 3 PASS-by-audit (no ambiguity arose to fire a
  live question; the branch's wiring verified against the engine's shipped text — mechanism is
  first-use territory, /lead-intake's disclosure class). Mechanism note disclosed: the
  no-match branch's [nested-intake] intake forks from a host session and routes back to it
  (host = root) — one asynchronous hop, holds.

**Gate summary: P0 PASS · P1 PASS · P2 PASS · P3 PASS · P4 PASS · P5 PASS. Forge complete
2026-08-10.**
- Fence closure: all fenced siblings are command-species or agents (no routing collision from
  dmi:true); `/build-feature`'s description gains the reciprocal menu-clarity fence in the same
  change — recorded as the closure disposition.

## Gate P6 — Ship

teamwork 2.0.1 → 2.1.0, README row, ledger, gate, branch + PR.
