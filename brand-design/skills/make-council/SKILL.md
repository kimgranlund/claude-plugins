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
reference instance throughout: its file layout, its `references/roster.md`, its
`council-chair-agent` chair wiring, its four lens role agents (`strategy-convener` and siblings),
and its calibration assets directory are what a new domain instance mirrors, not what it restates.

Parse `$ARGUMENTS` as `[domain name] [what's being judged]` — e.g. `code-review "pull request
diffs"`, `product-copy "marketing landing pages"`.

## Procedure

1. **Domain intake.** Resolve, explicitly, before drafting anything (`references/domain-intake.md`
   has the full worked checklist):
   - **What artifact type is under review** — a brief, a diff, a spec, a design file. This decides
     what "the artifact" means throughout the new convening skill.
   - **Which role families the roster needs** — the distinct lenses a real practitioner panel for
     this domain would bring (analogous to brand's strategy/design/voice split). A domain that
     genuinely needs only one lens may not need sub-councils at all — state that explicitly rather
     than inventing a split with one member.
   - **Minimum viable roster size** — no fixed number; as a floor, a sub-council needs enough
     members that a 2-of-3 contested-finding vote (`council-rules`' `references/severity-and-
     voting.md`) is even possible within it, or a documented fallback to a cross-sub-council third
     opinion.
2. **Mint the new convening skill — the domain's own action-twin of `council-rules`, mirroring
   `check-brand-council`'s dual role (roster home + orchestrator + convening surface, all one
   file).** New skill directory: `domain-council` or `check-domain-council` (substitute the actual
   domain name; run the estate's naming validator against the manifest's ObjectVocab before
   committing to one, never assume). Its SKILL.md:
   - Carries a "Roster" section that **cites `references/roster.md`** (seeded in step 3) — never a
     prose sub-council table — plus its own trust-boundary restatement of `council-rules`'
     principle applied to the new artifact type, and its own Phase 1/Phase 2 procedure copied in
     SHAPE from `check-brand-council`'s body, never its brand-specific content.
   - Cites `council-rules` for fan-out mechanics, severity/voting, synthesis shapes, calibration
     discipline, and the two-phase model — never restated locally.
   - Houses its own critics at `<new-skill>/references/critics/critic-<handle>.md`, each minted via
     `make-critic`, never hand-authored here.
3. **Seed `references/roster.md`** — `council-rules`' `references/roster-file-contract.md` schema
   (table + `## Groups` + `## Role agents`), one row per critic minted in step 2,
   `role`/`status`/`seated`/`fixture` filled in as each critic seats. A role family with no lead
   yet gets its own `## Groups` `leads:` entry naming that seat `VACANT` — one `leads:` entry per
   sub-council is required, never left undeclared. Seed `## Role agents` too, mapping `chair` to
   `council-chair-agent` (reused, step 4) and each ordinary sub-council to the role agent minted in
   step 6 — every other key must match a `leads:` key exactly, `advisory` never appears as a key.
   Run `scripts/roster_check.py <new-skill-dir>` against the seeded file before step 9's checker pass — a
   bijection, mapping, or schema failure is fixed and re-run, never carried forward.
4. **Chair wiring — reuse `council-chair-agent` by default.** Its input contract already
   parameterizes the critic-shell agent by name and carries no brand-specific logic. A new domain
   instance dispatches the SAME `council-chair-agent` for its own phase 2, naming its own
   critic-shell agent in the sealed prompt — never a new Chair agent, unless phase 2 genuinely needs
   a contract change to `council-chair-agent` itself, which forks back to `planner`
   (`references/roster-and-chair-wiring.md` states the escalation path in full).
5. **Mint the domain's own critic-shell agent, patterned off `brand-judge`.** Every council needs
   ONE critic-shell agent — the embodiment shell every persona in ITS roster runs inside. Pattern
   the new agent file off `brand-judge`'s body structurally verbatim (input contract, severity
   table, method, both output contracts) — only the `name:`, the domain-specific description line,
   and any domain-appropriate severity-table wording substitute. This copying is NOT the
   restatement `council-rules` warns against: that pack's citation duty covers the shared COUNCIL
   machinery, while a critic-shell agent's own body is per-instance configuration, exactly like the
   roster it embodies (`references/roster-and-chair-wiring.md`).
6. **Mint ONE role agent per ordinary sub-council, patterned off `strategy-convener`.** Every
   sub-council needs its own addressable external seat (`council-rules`' `references/role-agents.md`)
   that a fleet or session can dispatch directly, bypassing the convening skill, to convene ONLY
   that one sub-council and return a phase-1-only rolled-up read. Pattern each new agent file off
   `strategy-convener`'s body structurally verbatim (input contract, method, output contract) —
   only the `name:`, the sub-council/domain noun, and the description substitute. **Never one for
   `full` or `advisory`** — the same reserved names `roster-file-contract.md` excludes from the
   `sub-councils` column apply here. A sub-council seeded empty at mint time still gets its role
   agent minted — its own empty-bench branch handles that at dispatch time.
7. **Seed one calibration case.** `references/calibration-worked-example.md` walks a full worked
   example — a tiny two-critic demo council standing up and catching one planted defect end to end.
   Disclose the fixture as unpromoted markdown unless it has actually run enough live rounds to earn
   `calibration-discipline.md`'s promoted-script contract.
8. **Declare both run modes explicitly** in the new skill's own body — Full (real `Agent`-tool
   fan-out to the new critic-shell agent, `council-chair-agent` for phase 2) and Project
   single-context (sequential persona simulation, Chair as an in-context role) — the same two rungs
   `check-brand-council`'s "Run modes" states, mirrored not copied verbatim.
9. **Fresh-context checker pass — mandatory** on the new convening skill's SKILL.md and every new
   agent file (critic-shell agent AND every role agent minted in step 6) before any is reported
   done. Dispatch `harness:skill-checker` for the skill and `harness:agent-checker` once per new
   agent file, unnamed, fresh context, never self-graded.
10. **Report.** The new skill's path, its `roster.md` (handles + sub-councils + any `VACANT` leads
    + `## Role agents`) plus `roster_check.py`'s exit status, the critic-shell agent minted, every
    role agent minted, confirmation `council-chair-agent` was reused unchanged, the calibration
    fixture's location/promotion state, and every checker's verdict.

## What this procedure does NOT do

It does not run the new council (the new convening skill's own job, once minted). It does not
hand-author critic personas — it dispatches `make-critic` once per critic. It does not seat a live,
permanent demo product — the full walkthrough proof (mint → seat → run blind + deliberation) is a
later campaign step; this procedure's calibration seed is a disclosed worked example only.

## Run modes

**Full** (Claude Code/Cowork) — the whole procedure above, writing every file to disk and running
real checker dispatches. **Project single-context** — the new skill's body, roster table, and
critic-shell agent are drafted in-chat and disclosed as needing to be pasted into actual files once
back in Full mode; the checker passes become self-review, disclosed as non-independent.

## Failure branches (not already covered in the steps above)

- Domain intake surfaces only one role family → state explicitly that this instance runs with no
  sub-council split, never invent a second family to force one nobody asked for.
- The proposed new skill name fails the naming validator → revise against `ObjectVocab`/`ProcessLex`
  before minting anything.
- `council-chair-agent`'s existing contract genuinely cannot serve the new domain (a structural gap,
  not a convenience) → name the gap, escalate to `planner`, never fork the Chair in place.

## Done / NOT done

Done when every checklist item in steps 1–10 above is satisfied and every checker pass is green
(never an unresolved FAIL or a failing `roster_check.py`) — most notably: the new skill cites
`council-rules` rather than restating it, `roster.md` passes `roster_check.py` including its
`## Role agents` mapping, and no role agent was minted for `full` or `advisory`.

## References

| File | Use when |
|---|---|
| `references/domain-intake.md` | Step 1's full worked domain-intake checklist |
| `[[council-rules]]`'s `references/roster-file-contract.md` | Step 3's `roster.md` schema — table + `## Groups` + `## Role agents` shape, bijection, `VACANT`-lead convention |
| `[[council-rules]]`'s `references/role-agents.md` | Step 6's role-agent concept, scoped convene semantics, and the `full`/`advisory` reserved-name rule |
| `references/roster-and-chair-wiring.md` | Steps 4–6's chair-reuse default and the critic-shell-agent-/role-agent-is-configuration exception |
| `references/calibration-worked-example.md` | Step 7's worked two-critic demo council example |
