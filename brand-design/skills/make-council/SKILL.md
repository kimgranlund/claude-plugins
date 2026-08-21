---
name: make-council
description: >
  Stand up a NEW council instance for a domain with none yet: domain intake, roster home + its
  role→agent mapping, sub-council groupings, chair wiring (reuse `council-chair-agent`; a critic
  shell off `brand-judge`; one role agent per sub-council off `strategy-convener`), a
  calibration seed, both run modes. Cites `council-rules`; never restates it. Use for "stand up a
  new council for X", "make a council that reviews Y", "I need a council like check-brand-council
  but for a different domain". NOT convening an existing council; NOT minting one critic inside one
  (`make-critic`); NOT the mechanism (`council-rules`); NOT a generic team or subagent
  (`teamwork:fleet-rules`, `harness:make-agent`).
disable-model-invocation: false
user-invocable: true
argument-hint: "[domain name] [what's being judged]"
---

# make-council

Stands up a brand-new council instance — the domain-neutral minting procedure for everything
`council-rules` leaves to per-instance configuration, at the INSTANCE level rather than the
single-persona level `make-critic` mints at. `check-brand-council` is this procedure's own worked
reference instance throughout: its file layout, its `references/roster.md` (cited by its SKILL.md,
never restated in prose, including its `## Role agents` mapping section), its `council-chair-agent`
chair wiring, its four lens role agents (`strategy-convener` and siblings), and its
calibration assets directory are what a new domain instance mirrors, not what it restates.

Parse `$ARGUMENTS` as `[domain name] [what's being judged]` — e.g. `code-review "pull request
diffs"`, `product-copy "marketing landing pages"`.

## Procedure

1. **Domain intake.** Resolve, explicitly, before drafting anything (`references/domain-intake.md`
   has the full worked checklist):
   - **What artifact type is under review** — a brief, a diff, a spec, a design file. This decides
     what "the artifact" means throughout the new instance's own convening skill.
   - **Which role families the roster needs** — the distinct lenses a real practitioner panel for
     this domain would bring (analogous to brand's strategy/design/voice split). Two or more
     families is the usual shape; a domain that genuinely needs only one lens may not need
     sub-councils at all (state that explicitly rather than inventing a split with one member).
   - **Minimum viable roster size** — `council-rules`' `references/roster-and-personas.md` fixes no
     number; as a floor, a sub-council needs enough members that a 2-of-3 contested-finding vote
     (council-rules' `references/severity-and-voting.md`) is even possible within that sub-council OR
     a documented fallback to a cross-sub-council third opinion.
2. **Mint the new convening skill — the domain's own action-twin of `council-rules`, mirroring
   `check-brand-council`'s own dual role (roster home + orchestrator + convening surface, all one
   file).** New skill directory: `domain-council` or `check-domain-council` (substitute the actual
   domain name; pick whichever form resolves against the naming manifest's ObjectVocab — run the
   estate's naming validator before committing to a name, never assume). Its SKILL.md:
   - Carries a "Roster" section that **cites `references/roster.md`** (seeded in step 3) — never a
     prose sub-council table (`roster-file-contract.md`'s "cite, never restate" rule applies to the
     new instance from its first draft, exactly as it binds `check-brand-council`) — plus its own
     trust-boundary restatement of `council-rules`' principle applied to the new artifact type, and
     its own Phase 1/Phase 2 procedure — copied in SHAPE from `check-brand-council`'s own body,
     never its brand-specific content.
   - Cites `council-rules` for fan-out mechanics, severity/voting, synthesis shapes, calibration
     discipline, and the two-phase model — the same six citations `check-brand-council` already
     makes, never restated locally.
   - Houses its own critics at `<new-skill>/references/critics/critic-<handle>.md` — each one
     minted via `make-critic`, pointed at this new council as its target, never hand-authored here.
3. **Seed `references/roster.md`** — `council-rules`' `references/roster-file-contract.md` schema
   (table + `## Groups` + `## Role agents`), one row per critic minted in step 2,
   `role`/`status`/`seated`/`fixture` filled in as each critic seats. A role family with no lead
   yet gets its own `## Groups` `leads:` entry naming that seat `VACANT` — the contract requires
   one `leads:` entry per sub-council, so this is never left undeclared, never invented. Seed the
   `## Role agents` section too, mapping `chair` to `council-chair-agent` (reused, step 4) and each
   ordinary sub-council to the role agent minted for it in step 6, below — every OTHER key (every key
   besides the literal `chair`) must match a `leads:` key exactly, `advisory` never appears as a key
   (`roster-file-contract.md`'s reserved-name enforcement). Run `roster_check.py <new-skill-dir>`
   (this plugin's `scripts/roster_check.py`, the new convening skill's own directory as the
   argument) against the seeded file before step 9's checker pass — a bijection, mapping, or schema
   failure here is fixed and re-run, never carried into the checker pass.
4. **Chair wiring — reuse `council-chair-agent` by default.** `council-chair-agent`'s own input contract
   already parameterizes the critic-shell agent by name (`agents/council-chair-agent.md`'s "the
   critic-shell agent's name (e.g. `brand-judge`)") — it carries no brand-specific logic anywhere in
   its body. A new domain instance dispatches the SAME `council-chair-agent` agent for its own phase 2,
   naming its own critic-shell agent in the sealed prompt — never a new Chair agent, unless the new
   domain's phase 2 genuinely needs a contract change to `council-chair-agent` itself, which is a fork
   back to `planner` (a shared-agent contract change, never edited in place for one domain's
   convenience — `references/roster-and-chair-wiring.md` states the escalation path in full).
5. **Mint the domain's own critic-shell agent, patterned off `brand-judge`.** Every council needs
   ONE critic-shell agent — the embodiment shell every persona in ITS roster runs inside
   (`brand-judge`'s own role for brand). Pattern the new agent file off `brand-judge`'s body
   structurally verbatim (input contract, severity table, method, both output contracts) — only the
   `name:`, the domain-specific description line, and any domain-appropriate severity-table wording
   substitute; the mechanics (inlined-only input contract, cold-read method, deliberation-round
   contract) are not brand-specific despite living in a brand-named file today, and copying them is
   NOT the restatement `council-rules` warns against (that pack's citation duty covers the shared
   COUNCIL machinery; a critic-shell agent's OWN body is per-instance configuration, exactly like
   the roster it embodies — `references/roster-and-chair-wiring.md` states why this one exception
   to "cite, don't restate" holds).
6. **Mint ONE role agent per ordinary sub-council, patterned off `strategy-convener`.** Every
   sub-council needs its own addressable external seat (`council-rules`' `references/role-agents.md`
   — concept and scoped convene semantics, cited not restated): a fleet or session dispatches it
   directly, bypassing the convening skill entirely, to convene ONLY that one sub-council and
   return a phase-1-only rolled-up read. Pattern each new agent file off `strategy-convener`'s
   body structurally verbatim (input contract, method, output contract) — only the `name:`, the
   sub-council/domain noun throughout, and the description substitute
   (`references/roster-and-chair-wiring.md`'s practical wiring checklist, extended to this second
   per-instance agent family). **Never one for `full` or `advisory`** — the same reserved names
   `roster-file-contract.md` already excludes from the `sub-councils` column apply here
   (`role-agents.md`'s reserved-name rule). A sub-council seeded empty at mint time (no members yet)
   still gets its role agent minted — the agent's own empty-bench branch handles that at dispatch
   time, never a reason to defer minting the agent itself.
7. **Seed one calibration case.** `references/calibration-worked-example.md` walks a full worked
   example — a tiny two-critic demo council standing up and catching one planted defect end to end.
   Disclose the fixture as unpromoted markdown unless it has actually run enough live rounds to earn
   `calibration-discipline.md`'s promoted-script contract.
8. **Declare both run modes explicitly** in the new skill's own body — Full (Claude Code/Cowork:
   real `Agent`-tool fan-out to the new critic-shell agent, `council-chair-agent` for phase 2) and
   Project single-context (sequential persona simulation, Chair as an in-context role) — the exact
   two rungs `check-brand-council`'s own "Run modes" section already states, mirrored not copied
   verbatim (the domain names differ).
9. **Fresh-context checker pass — mandatory** on the new convening skill's SKILL.md and every new
   agent file — the critic-shell agent AND every role agent minted in step 6 — before any is
   reported done (`plugin-authoring.md`'s semantic-edit invariant, same as any new SKILL.md or
   agent body). Dispatch `harness:skill-checker` for the skill and `harness:agent-checker` once per
   new agent file, unnamed, fresh context, never self-graded.
10. **Report.** The new skill's path, its `roster.md` (handles + sub-councils + any `VACANT` leads
    + the `## Role agents` mapping) plus `roster_check.py`'s exit status, the critic-shell agent
    minted, every role agent minted, confirmation `council-chair-agent` was reused unchanged, the
    calibration fixture's location and promotion state, and every checker's verdict.

## What this procedure does NOT do

It does not run the new council (that's the new convening skill's own job, exactly as
`check-brand-council` runs itself once minted). It does not mint every critic the new roster names
— it dispatches `make-critic` once per critic rather than hand-authoring personas inline (never a
restatement of that procedure). It does not seat a live, permanent demo product as part of this
ticket's own scope — the full end-to-end walkthrough proof (mint → seat → run blind + deliberation)
is a later campaign step's job (this plugin's own overhaul plan), and this procedure's calibration
seed is a disclosed worked example, not a shipped demo council.

## Run modes

**Full** (Claude Code/Cowork) — the whole procedure above, writing every file to disk and running
real checker dispatches. **Project single-context** — the new skill's body, roster table, and
critic-shell agent are drafted in-chat and disclosed as needing to be pasted into actual files once
back in Full mode; the checker passes become self-review, disclosed as non-independent.

## Failure branches

- Domain intake surfaces only one role family → state explicitly that this instance runs with no
  sub-council split (a single `full`-equivalent roster), never invent a second family to force a
  split nobody asked for.
- The proposed new skill name fails the naming validator → revise the name against
  `ObjectVocab`/`ProcessLex` before minting anything, never ship a name the estate's own gate would
  reject.
- `council-chair-agent`'s existing contract genuinely cannot serve the new domain (a structural gap, not
  a convenience) → name the gap, escalate to `planner` for a contract change, never fork
  `council-chair-agent`'s body in place for one domain.
- A checker dispatch FAILs on the new skill or any new agent → fix and re-dispatch; never report
  the new council done on an unresolved FAIL.
- `roster_check.py` fails on the step-3 seeded roster (a bijection gap, an empty sub-councils
  cell, a dangling `## Groups` handle, a dangling `## Role agents` handle, or a reserved-name key)
  → fix the data file and re-run before proceeding to step 9; never carry a failing roster into
  the checker pass or report the new council done on it.
- A sub-council role agent would be minted for `full` or `advisory` → stop, name the reserved-name
  violation, never mint it (`role-agents.md`'s reserved-name rule is mechanically enforced by
  `roster_check.py` too — this failure branch is the authoring-time mirror of that check).

## Done / NOT done

**Done** when the new convening skill exists, cites `council-rules` for every shared mechanic
(fan-out, severity/voting, synthesis, calibration discipline, two-phase model, role-agent convene
semantics) without restating any of them, carries its own `roster.md` (schema:
`roster-file-contract.md`, including a complete `## Role agents` mapping) passing
`roster_check.py`, has a critic-shell agent patterned off `brand-judge`, has ONE role agent per
ordinary sub-council patterned off `strategy-convener`, reuses `council-chair-agent` for
chairing (or names why it genuinely could not), carries one calibration fixture, and passed
independent fresh-context checks on the new skill and every new agent file. **NOT done** when the
new instance restates council-rules' machinery locally, carries its roster in SKILL.md prose
instead of `roster.md`, mints a redundant Chair agent where `council-chair-agent` would have served
unchanged, mints a role agent for `full` or `advisory`, leaves a sub-council with no role agent at
all, or reports success with an unresolved checker FAIL or a failing `roster_check.py`.

## References

| File | Use when |
|---|---|
| `references/domain-intake.md` | Step 1's full worked domain-intake checklist |
| `[[council-rules]]`'s `references/roster-file-contract.md` | Step 3's `roster.md` schema — table + `## Groups` + `## Role agents` shape, bijection, `VACANT`-lead convention |
| `[[council-rules]]`'s `references/role-agents.md` | Step 6's role-agent concept, scoped convene semantics, and the `full`/`advisory` reserved-name rule |
| `references/roster-and-chair-wiring.md` | Steps 4–6's chair-reuse default and the critic-shell-agent-/role-agent-is-configuration exception |
| `references/calibration-worked-example.md` | Step 7's worked two-critic demo council example |
