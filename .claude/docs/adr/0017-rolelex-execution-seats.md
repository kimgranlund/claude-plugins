---
doc-type: adr
id: adr-0017
status: accepted
ratified: Kim, 2026-08-17, live AskUserQuestion via plugins-team-lead
date: 2026-08-17
owner: kim.granlund
supersedes: adr-0011 (D7's "RoleLex ≤ 4 entries to start" sizing clause, as spec §4 adopted
  it) and adr-0015 (D1's coordinator-only framing of the {scope}-{role} production; D2's
  scope pool, D3's disjointness requirement, and D4's exemption posture all stand unamended)
intent-refs: idr-0003    # same naming-grammar chain, the {scope}-{role} production amendment
---
# ADR-0017 — RoleLex grows by 10 members; the `{scope}-{role}` production covers execution seats, not only coordinators

> **Ratified 2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead), recorded in
> issue #477's Findings comment referencing #464's proposal** — from ratification this file
> is append-only (doc_lint T4); a change of mind supersedes, never edits. Drafted 2026-08-16
> as part of #464's S8 lexicon-amendment proposal (overhaul #373 Wave-3), executed 2026-08-17
> under this ratification. ADR-0011 and ADR-0015 are NOT edited — accepted ADRs are
> append-only; the partial supersession is recorded by this ADR's `supersedes:` field alone,
> exactly as ADR-0013/0015/0016 recorded theirs.

## Context

ADR-0011 D7 sized `RoleLex` at "≤4 entries to start" (spec §4), and ADR-0015 D1 framed the
`{scope}-{role}` production as the *orchestrator* shape — "agents that coordinate rather than
execute." Measured reality at #464's evidence base (`authorkit/skills/naming-audit/scripts/
validate.py --scope grammar`, all 8 plugins, exemptions emptied, 2026-08-16): 19 of the
estate's agent name exemptions are execution seats — reviewers, watchers, sorters, cleaners —
named exactly `{scope}-{agentive-role}`: `doc-checker`, `experiment-runner`, `intake-lead`
(docs); `agent-checker`, `chore-planner`, `decision-watcher`, `fact-finder`, `hook-checker`,
`issue-sorter`, `plugin-checker`, `repo-cleaner`, `routing-judge`, `skill-checker`,
`wording-checker` (harness); `builder`, `code-checker`, `docs-writer`, `planner`,
`wiring-checker` (teamwork). This is the estate's dominant agent-naming pattern, not an
edge case — the "reviewer-per-artifact-class" shape (`agent-writing-rules`' own family
template) mints a new one every time a new checkable artifact class appears. Re-exempting
each one by hand is exactly the recurring-shape toil ADR-0011 D8's ratchet and ADR-0014 exist
to retire.

`RoleLex`'s three members (`leader`, `orchestrator`, `coordinator`) all name a seat that
coordinates other work rather than doing it directly. None of the 19 measured names fit that
shape — they execute a bounded check, sweep, or build directly. The `{scope}-{role}`
production already exists and already resolves scope against `ObjectVocab ∪ ProcessLex`
(ADR-0015 D2); the only gap is which role words qualify.

**Scope arithmetic (verified against `naming.manifest.json` at the ratification tree,
2026-08-17):** of the 19 measured agent exemptions, 16 resolve cleanly once `RoleLex` grows by
the 10 words below (their scope tokens already sit in `ObjectVocab`/`ProcessLex`, or are
supplied by the sibling ObjectVocab registrations in ADR-0018). Three do not: `builder` and
`planner` (teamwork) are bare role words with no scope token — the production requires
`{scope}-{role}`, never a bare role, so conforming them is a rename question, out of this
amendment's scope. `intake-lead` (docs) uses the token `lead`, not a `RoleLex` member at all
(`lead` is ADR-0016's reserved *command* head; `leader` already covers the role) — it
conforms instead via the `intake-lead → intake-leader` rename executed alongside this ADR
(issue #477), once `intake` enters `ObjectVocab` (ADR-0018).

**Owner boundary — same split as ADR-0011/0014/0015/0016.** This ADR is a docs-owned record
amending a docs-owned spec that governs an authorkit-owned validator and reference set.
Ratification provenance is the live AskUserQuestion named in `ratified:`; the follow-on
implementation is authorkit's, executed in the same PR under the same authorization.

## Decision

**`RoleLex` grows from `{leader, orchestrator, coordinator}` by 10 members: `checker`,
`runner`, `planner`, `watcher`, `finder`, `sorter`, `cleaner`, `judge`, `builder`, `writer`.**
The `{scope}-{role}` production's semantics widen from "orchestrator seats" to "any agent seat
whose terminal is a RoleLex member" — no grammar-production change, since §3.3's shape already
covers any `RoleLex` terminal; only the lexicon's membership changes.

### D1 — The 10 members and why these

Each is an agentive noun already in live use as an agent-name terminal, with no plausible
reading as an object or process:

`checker` (doc-checker, code-checker, skill-checker, …), `runner` (experiment-runner),
`planner` (chore-planner, review-planner), `watcher` (decision-watcher), `finder`
(fact-finder), `sorter` (issue-sorter), `cleaner` (repo-cleaner), `judge` (routing-judge),
`builder` (docs-writer's sibling shape, teamwork's `builder` agent, design's `token-builder`),
`writer` (docs-writer, wording-checker's sibling class).

### D2 — Anti-ambiguity gate (ADR-0015 D3)

ADR-0015 D3 requires `RoleLex ∩ (ObjectVocab ∪ ProcessLex) = ∅` — once a bare `{scope}-{role}`
name is a legal agent shape, a role word double-booked as an object/process would let the same
string parse as a skill AND an agent. Each of the 10 candidates was checked against the live
manifest at the ratification tree:

| Candidate | Nearest ObjectVocab/ProcessLex term | Verdict |
|---|---|---|
| `builder` | ObjectVocab `build` | no collision — disjointness is exact-token; `build` ≠ `builder` |
| `planner` | ProcessLex `planning` | no collision — different token |
| `writer` | ProcessLex `writing` | no collision — different token |
| `checker` | TopicLex `checking` | no collision — `TopicLex` carries no disjointness requirement (ADR-0014 D3) |
| `runner`, `watcher`, `finder`, `sorter`, `cleaner`, `judge` | none | no near-miss at all |

**Gate: PASS × 10.** No candidate makes any existing skill name dual-parse as an agent — a
skill parse never consults `RoleLex` (§3.2's productions have no `RoleLex` branch), and D3
keeps the reverse direction closed by construction.

### D3 — Cost, stated up front (ADR-0015's own caveat, carried forward)

Each `RoleLex` member is now permanently barred from future `ObjectVocab`/`ProcessLex`
registration by D3's disjointness — e.g. no skill will ever be nameable `*-judge`, and
`checker` can never become an ObjectVocab token. This is a one-way door. All 10 are agentive
nouns with no plausible object/process reading, so the bar is cheap here, but the ADR states
it rather than leaving it implicit — the same discipline ADR-0015 D1 applied to its original
three.

### D4 — What deliberately does NOT get admitted

- **Bare `RoleLex` terminals with no scope token** (`builder`, `planner`) stay exempt. The
  `{scope}-{role}` production is `{scope}-{role}`, not `{role}` alone — a bare role word
  supplies no scope information a reviewer could use to know what it checks. Conforming these
  two is a rename question (e.g. `feature-builder`), explicitly out of this amendment's scope.
- **`lead` is deliberately not added to `RoleLex`.** `RoleLex` already has `leader`; `lead-` is
  ADR-0016's reserved *command* head (a different grammatical role — a literal head token, not
  a role suffix). Two spellings of one role would invite drift. `intake-lead` follows the
  `team-lead → team-leader` rename precedent instead (executed same-change, issue #477), never
  a lexicon bend.
- **The optional screens extension** (registering `component`/`flow`/`layout` in ObjectVocab
  to retire `component-checker`/`flow-checker`/`layout-checker`) is NOT part of this
  ratification — #464's proposal offered it but Kim's ratification covers Proposals A/B/C only.
  Those three checkers stay exempt pending a future amendment.

### D5 — Validator recognition

No new branch: `Grammar.parse`'s `kind == "agent"` orchestrator-production check
(`rtoks[-1] in self.role_lex`) already tries any `RoleLex` member as the terminal role; growing
the manifest's `role_lex` array is the entire validator-side change. The scope resolution
(`resolve_orchestrator_scope`, ADR-0015 D2's `ObjectVocab ∪ ProcessLex` pool) is unchanged and
shared.

## Consequences

- **Ratification provenance:** Kim ratified live (2026-08-17, AskUserQuestion via
  plugins-team-lead), per #464's proposal comment (Proposal A) and #477's execution ticket. A
  change of mind is a superseding ADR (this file stays append-only); the implementation below
  reverts by ordinary PR.
- **The follow-on execution (authorkit-owned, same PR as this ADR, executed same-change under
  this authorization):**
  1. `naming.manifest.json`: `role_lex` gains the 10 members (D1); no production change.
  2. Validator selftest fixtures (mirroring §14.2/§14.4/§14.5's triad): positive —
     `code-checker`, `experiment-runner`, `decision-watcher` (ObjectVocab scopes),
     `review-planner` (ProcessLex scope) parse clean as agents; negative — a bare `RoleLex`
     terminal with no scope token (`builder`) still fails.
  3. `authorkit/skills/naming-conventions/references/GRAMMAR.md`: the RoleLex lexicon-table
     row and the Agents section gain the 10 members and the execution-seat framing.
  4. `.claude/docs/spec/spec-naming-convention.md`: a dated **§14.6** appended mirroring
     §14.2/§14.4/§14.5's pattern.
  5. **ADR-0011 and ADR-0015 are not edited, then or later** — both accepted and append-only;
     supersession/citation live in this file's frontmatter and body.
  6. `intake-lead → intake-leader` rename (docs plugin), full blast radius, executed
     same-change (issue #477) — not part of this ADR's grammar decision but the dependent
     rename this ADR's D4 names explicitly.
  7. Re-run `authorkit:naming-audit --scope grammar` estate-wide; combined with ADR-0018 in the
     same PR, confirm the measured exemption count after (§14.7 carries the joint arithmetic,
     since both amendments landed as one PR against one shared re-run).
- **`intent-refs: null` is deliberate** — same posture as ADRs 0001–0016; the T6 orphan-ADR
  WARN is accepted as-is.
- **Easier, once landed:** every future reviewer/standing-execution seat named
  `{what-it-works-on}-{agentive-role}` conforms from day one, without a fresh exemption; 16 of
  19 measured in-scope agent exemptions retire immediately.
- **Harder, once landed:** `RoleLex` no longer fits the "small, obviously enumerable" shape
  ADR-0011 D7 assumed (3 → 13 members) — a future proposal to add an 11th execution-seat word
  must still clear D2's disjointness gate individually; the list itself becomes worth
  periodically re-auditing for near-miss collisions as ObjectVocab keeps growing.
- **Irreversible in the ratchet sense:** each RoleLex addition is a one-way disjointness door
  (D3) — those 10 words can never later enter ObjectVocab/ProcessLex without a reversal ADR
  that first proves no live agent name depends on the RoleLex membership.
