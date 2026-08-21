---
name: make-council
description: >
  Stand up a NEW council instance end-to-end for a domain that doesn't have one yet: domain intake
  (what's being judged, which role families the roster needs), the roster's file home under the new
  council's own skill directory, sub-council groupings, chair wiring (reusing `council-marshal`'s
  already-generic contract, or patterning a new critic-shell agent off `brand-judge`), a calibration
  seed, and both run modes (full Agent-tool fan-out + Project sequential persona simulation). Cites
  `council-rules` for every mechanic; never restates it. Use for "stand up a new council for X",
  "make a council that reviews Y", "give me an adversarial critic panel for Z", "I need a council
  like check-brand-council but for a different domain". NOT convening an already-existing council
  instance (that instance's own `check-<domain>-council` skill); NOT minting one critic inside an
  EXISTING council (`make-critic`); NOT the council mechanism itself (`council-rules`); NOT a
  generic multi-agent team (`teamwork:fleet-rules` — a council is a specific adversarial blind-then-
  deliberation panel shape, not a generic coordination pattern); NOT a generic subagent
  (`harness:make-agent`).
disable-model-invocation: false
user-invocable: true
argument-hint: "[domain name] [what's being judged]"
---

# make-council

Stands up a brand-new council instance — the domain-neutral minting procedure for everything
`council-rules` leaves to per-instance configuration, at the INSTANCE level rather than the
single-persona level `make-critic` mints at. `check-brand-council` is this procedure's own worked
reference instance throughout: its file layout, its Roster table shape, its `council-marshal` chair
wiring, and its calibration assets directory are what a new domain instance mirrors, not what it
restates.

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
     (`references/severity-and-voting.md`) is even possible within that sub-council OR a documented
     fallback to a cross-sub-council third opinion.
2. **Mint the new convening skill — the domain's own action-twin of `council-rules`, mirroring
   `check-brand-council`'s own dual role (roster home + orchestrator + convening surface, all one
   file).** New skill directory: `<domain>-council` or `check-<domain>-council` (pick the name that
   actually resolves against the naming manifest's ObjectVocab — run the estate's naming validator
   before committing to a name, never assume). Its SKILL.md:
   - States the domain's own Roster table (sub-council → member handles), its own trust-boundary
     restatement of `council-rules`' principle applied to the new artifact type, and its own Phase
     1/Phase 2 procedure — copied in SHAPE from `check-brand-council`'s own body, never its brand-
     specific content.
   - Cites `council-rules` for fan-out mechanics, severity/voting, synthesis shapes, calibration
     discipline, and the two-phase model — the same six citations `check-brand-council` already
     makes, never restated locally.
   - Houses its own critics at `<new-skill>/references/critics/critic-<handle>.md` — each one
     minted via `make-critic`, pointed at this new council as its target, never hand-authored here.
3. **Sub-council groupings** — a table in the new skill's own body, one row per role family from
   step 1, `full` reserved as the union (per `council-rules`' own reserved-name convention).
4. **Chair wiring — reuse `council-marshal` by default.** `council-marshal`'s own input contract
   already parameterizes the critic-shell agent by name (`agents/council-marshal.md`'s "the
   critic-shell agent's name (e.g. `brand-judge`)") — it carries no brand-specific logic anywhere in
   its body. A new domain instance dispatches the SAME `council-marshal` agent for its own phase 2,
   naming its own critic-shell agent in the sealed prompt — never a new Chair agent, unless the new
   domain's phase 2 genuinely needs a contract change to `council-marshal` itself, which is a fork
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
6. **Seed one calibration case.** `references/calibration-worked-example.md` walks a full worked
   example — a tiny two-critic demo council standing up and catching one planted defect end to end.
   Disclose the fixture as unpromoted markdown unless it has actually run enough live rounds to earn
   `calibration-discipline.md`'s promoted-script contract.
7. **Declare both run modes explicitly** in the new skill's own body — Full (Claude Code/Cowork:
   real `Agent`-tool fan-out to the new critic-shell agent, `council-marshal` for phase 2) and
   Project single-context (sequential persona simulation, Chair as an in-context role) — the exact
   two rungs `check-brand-council`'s own "Run modes" section already states, mirrored not copied
   verbatim (the domain names differ).
8. **Fresh-context checker pass — mandatory** on the new convening skill's SKILL.md and the new
   critic-shell agent file, before either is reported done (`plugin-authoring.md`'s semantic-edit
   invariant, same as any new SKILL.md or agent body). Dispatch `harness:skill-checker` for the
   skill and `harness:agent-checker` for the agent, unnamed, fresh context, never self-graded.
9. **Report.** The new skill's path, its roster (handles + sub-councils), the critic-shell agent
   minted, confirmation `council-marshal` was reused unchanged, the calibration fixture's location
   and promotion state, and both checkers' verdicts.

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
- `council-marshal`'s existing contract genuinely cannot serve the new domain (a structural gap, not
  a convenience) → name the gap, escalate to `planner` for a contract change, never fork
  `council-marshal`'s body in place for one domain.
- A checker dispatch FAILs on the new skill or agent → fix and re-dispatch; never report the new
  council done on an unresolved FAIL.

## Done / NOT done

**Done** when the new convening skill exists, cites `council-rules` for every shared mechanic
(fan-out, severity/voting, synthesis, calibration discipline, two-phase model) without restating
any of them, carries its own roster + sub-council table, has a critic-shell agent patterned off
`brand-judge`, reuses `council-marshal` for chairing (or names why it genuinely could not), carries
one calibration fixture, and passed independent fresh-context checks on both the new skill and the
new agent. **NOT done** when the new instance restates council-rules' machinery locally, mints a
redundant Chair agent where `council-marshal` would have served unchanged, or reports success with
an unresolved checker FAIL.

## References

| File | Use when |
|---|---|
| `references/domain-intake.md` | Step 1's full worked domain-intake checklist |
| `references/roster-and-chair-wiring.md` | Steps 4–5's chair-reuse default and the critic-shell-agent-is-configuration exception |
| `references/calibration-worked-example.md` | Step 6's worked two-critic demo council example |
