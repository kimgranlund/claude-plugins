---
doc-type: adr
id: adr-0024
status: accepted
ratified: Kim, 2026-08-21, close-session leftovers round (plan-2026-08-brand-design-bloat-overhaul
  seed S4, Gate A approved 2026-08-21) — "amend the spec, not the practice." `evals/`'s addition
  is this ruling's direct subject; `intent.md`'s addition is issue #861's own deferred
  sub-decision, ruled here on the evidence below rather than left open a second time (the ticket's
  own acceptance criterion #4 asked only that it be "ruled one way or the other," never that it
  wait for a second live round).
date: 2026-08-21
owner: kim.granlund
scope: app
audience: any-agent, builder
supersedes: adr-0011 (§6.1's closed skill-folder set only — the four-entry list `SKILL.md` /
  `references/` / `scripts/` / `assets/` grows to six; the partition-axis rationale, the
  no-nested-skills rule, and the validator's blind-below-the-boundary posture all stand
  unamended. ADR-0011 is not edited — accepted ADRs are append-only; this citation is the
  entire mechanism of the supersession, exactly as ADR-0011's own partial supersessions by
  ADR-0014/0015/0016/0017/0018/0020 work.)
intent-refs: null
---
# ADR-0024 — `evals/` and `intent.md` join the skill folder closed set (§6.1)

> **Ratified 2026-08-21 by Kim**, in a `close-session` leftovers round closing out
> `plan-2026-08-brand-design-bloat-overhaul` seed S4, recorded in that plan's Completion note
> and filed as issue #861. From ratification this file is append-only (doc_lint T4); a change
> of mind supersedes, never edits.

## Context

`plan-2026-08-brand-design-bloat-overhaul`'s naming-audit sweep (brand-design, 20 skills)
found two top-level skill entries outside spec-naming-convention.md §6.1's closed four-entry
set:

- **`evals/`** — present in 20/20 skills sampled. Not brand-design debt: `plugin-authoring.md`'s
  routing-surface invariant *mandates* an `evals/evals.json` for every model-invocable
  description edit, estate-wide, and has since before this plan existed. The spec is stale
  against an enforced practice, not the reverse.
- **`intent.md`** — present in 4/20 skills sampled there (27 estate-wide at this ADR's
  ratification tree, `find . -name intent.md`, 2026-08-21) — `make-skill`'s own living
  build-state record: phase gates, decisions, and accepted-with-note findings, written as they
  happen during a skill's forge (`harness:make-skill` Phase 1 / Phase 6).

S4 was ruled 2026-08-21 ("amend the spec, not the practice") but the ruling's own text covers
`evals/` squarely while explicitly deferring `intent.md`'s fate to this ticket: "add it to the
closed set, or route its 4 existing instances into `references/` as remediation" (issue #861
Acceptance item 4). That sub-decision is ruled below, not deferred again.

**The validator already treats both as closed-set members — a second, independent evidence
line.** `authorkit/skills/naming-audit/scripts/validate.py`'s `ALLOWED_SKILL_ENTRIES` reads
`{"SKILL.md", "references", "scripts", "assets", "evals", "intent.md"}` — both names already
sit in the enforced allow-list, ahead of the spec text. This ADR closes the gap the spec-side
direction (doc lags code), not the reverse; acceptance item 3 (authorkit's own check matches
the amended set) is satisfied by code that already existed before this ticket opened.

## Decision

### D1 — `evals/` joins the closed set

§6.1's closed skill-folder set gains a fifth entry: `evals/` — executable-adjacent matter
(trigger evals, behavioral assertions, baseline captures) that neither `scripts/`'s
"executes outside context" nor `references/`'s "selectively read into context" describes
cleanly on its own; it is context that a script (`skill_lint`'s routing checks, `check-routing`'s
judge) *evaluates against*, not prose the model re-derives and not passive lookup matter. Its
own partition-axis answer: *proof the routing surface holds*, distinct from all four existing
answers.

### D2 — `intent.md` joins the closed set (issue #861 Acceptance item 4, ruled)

`intent.md` joins as a sixth entry, alongside `SKILL.md` as a bare top-level *file* (the only
two of the six that are files rather than directories) — never routed into `references/`.

**Why not `references/`:** §6.2's own partition test for that folder is "passive contracts" and
"discoverable by two hops, loaded on demand" — matter that is read, never written, once a skill
ships. `intent.md` fails that test on both axes: it is actively *written to* during a skill's
own forge (`make-skill` Phase 1's slot-filling, Phase 3's audit-triage notes, Phase 6's
gate-by-gate PASS log) — a build ledger, not reference matter a routed session ever needs to
read at trigger time. Filing it under `references/` would additionally force a reference-index
row (§6.2) for a file no session-time trigger ever reads, manufacturing indexing overhead for
a file whose only real readers are the forge process itself and a future auditor.

**Why not leave it exempt/ungoverned:** the estate-wide count (27 instances, 2026-08-21) shows
continued, unslowing minting — every `make-skill` run produces one — the same "still being
minted, not one-off" bar ADR-0018 D3 already applied to reserved-head registrations. Leaving a
routinely-produced artifact permanently outside the closed set means every skill that uses
`make-skill` fails `naming-audit`'s boundary check forever; that is a standing false-positive,
not a debt ratchet doing its job.

**Remediation-into-`references/` alternative — considered and rejected:** routing the 27 live
instances into `references/INTENT.md` (or similar) was the ticket's own offered alternative.
Rejected: it contradicts D2's own passive-vs-active-matter rationale (the file would still be
actively written to, now from inside a folder whose contract says otherwise), forces 27
mechanical moves plus 27 reference-index insertions purely to satisfy a boundary check the
validator itself already accepts as of today, and buys no clarity a `references/`-scoped index
row can express better than the file's own well-understood, singular convention already
does (`agent-writing-rules`' own frontmatter-hazard entry names `intent.md`'s placement history
directly — three same-day placements before `<skill-dir>/intent.md` held).

## Consequences

- **§6.1 prose is edited in place** (this file's own convention, matching how §3.1/§3.2 already
  carry ADR-0014/0015/0016/0017/0018/0020's amendments inline rather than only in the §14
  amendment log): the four-entry closed set becomes six —
  `SKILL.md` / `references/` / `scripts/` / `assets/` / `evals/` / `intent.md`. A dated §14.10
  is appended to the amendments log mirroring §14.2–§14.9's own pattern.
- **No code change owed.** `validate.py`'s `ALLOWED_SKILL_ENTRIES` already reads exactly this
  six-entry set; this ADR ratifies the spec to match code already shipped, not the reverse.
  Acceptance item 3 (issue #861) is satisfied as-is, verified by re-reading the constant at this
  ADR's ratification tree.
- **No exemption or remediation debt created.** Every skill carrying `evals/` or `intent.md`
  today already passes `naming-audit`'s boundary check (D1/D2's own decision matches what the
  validator enforces) — nothing newly conforms and nothing newly needs a rename or a move.
- **`intent-refs: null` is deliberate** — same posture as ADRs 0001–0020; the T6 orphan-ADR WARN
  is accepted as-is.
- **Reversible in the ordinary sense, harder in the ratchet sense that matters:** unlike D8's
  exemption ratchet, this ADR governs closed-set MEMBERSHIP, not an exemptions array — a future
  ADR could narrow the set again without needing to re-admit anything by exemption. Nothing here
  forecloses a future proposal to route `intent.md` differently; it would simply supersede D2 by
  the same citation-only mechanism this file uses on ADR-0011.

## Alternatives considered

- **Alt A — leave `evals/` exempt/ungoverned, same as any other estate debt.** Killed:
  `evals/` is not debt — it is a standing, cross-plugin *invariant* (`plugin-authoring.md`), so
  leaving it outside the closed set makes every conforming skill fail a boundary check the
  estate itself requires it to pass. The stale artifact is the spec, not the skills.
- **Alt B — route `intent.md` into `references/` as remediation (the ticket's own named
  alternative).** Killed — see D2's own rejection above (contradicts the passive-matter
  partition test; 27 mechanical moves + 27 index rows to satisfy a check the validator already
  passes).
- **Alt C — defer `intent.md` a second time, ship only D1.** Killed: issue #861's own Acceptance
  item 4 asked for a ruling, not a further deferral, and explicitly said the sub-decision
  "should not block items 1–3" — read together, that is instruction to rule it now on whatever
  evidence is in hand, not license to reopen it as a new ticket.

## Execution order (at acceptance)

1. Ratify this ADR (status → accepted, done at authoring time per the ratification already
   recorded above).
2. `.claude/docs/spec/spec-naming-convention.md` §6.1: closed set gains `evals/` and
   `intent.md`; a dated §14.10 appended to the amendments log.
3. Re-run `authorkit:naming-audit --scope grammar` (or the equivalent boundary check) estate-wide
   to confirm zero new violations open and zero close — `ALLOWED_SKILL_ENTRIES` is unchanged, so
   this is a confirmation step, not a migration.
4. Issue #861 Findings: dated entry closing items 1–4, citing this file and the confirmation run.
