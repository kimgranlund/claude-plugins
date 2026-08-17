---
doc-type: adr
id: adr-0020
status: rejected
ratified: NOT RATIFIED — drafted 2026-08-17 from Kim's live AskUserQuestion answers in a Cowork
  session; D5 ruled by Kim in a second AskUserQuestion round the same day (merge). Ready for
  ratification; no open blockers.
date: 2026-08-17
owner: kim.granlund
supersedes: adr-0015 (D1's role production insofar as RoleLex membership is closed to the
  coordinative three — the {scope}-{role} production itself stands unamended); adr-0016
  (D1 and D2 in full — the reserved `lead-` command head and its scope-resolution clause;
  D4's fence stands); adr-0017 (the RoleLex sizing posture only — its 10 execution-seat
  additions stand unamended); adr-0011 (D7's command production, already partially superseded
  by adr-0016, now superseded again by the three-head scheme in D3)
intent-refs: null
---
# ADR-0020 — The fleet vocabulary (`marshal`, `orchestration`) and the mechanism-revealing command heads `bind-` / `fork-` / `sub-`

> **REJECTED 2026-08-17 (Kim, live review; see gh#518).** Reversed ADR-0015/0016 <48h after ratification; `marshal` below ADR-0018 bar (self-admitted); ~633-site blast radius for zero behavior change. The bind-/fork-/sub- mechanism-revealing INSIGHT survives as documentation-only work (gh#527-class ticket), no renames.
> **DRAFT — not ratified.** Drafted 2026-08-17 in a Cowork session from Kim's answers to a live
> AskUserQuestion (four decisions, recorded verbatim in Context below). This draft is offered for
> review, not adopted: **D5 below is an unresolved collision that blocks ratification as drafted.**
> Once D5 is ruled and this file is ratified, it becomes append-only (doc_lint T4) like its
> predecessors — a change of mind supersedes, never edits.

## Context

The naming canon has moved four times in 48 hours — ADR-0015 (2026-08-16), ADR-0016, ADR-0017,
and ADR-0018 (all 2026-08-17). Three of those four were drafted from Kim's own rulings on issue
#433, the five-triad `leading-*` / `*-leader` rename campaign. ADR-0016 in particular records the
spec that *"the human-facing seat-adoption commands stay `/lead-*`"* and that *"the verb-first
shape IS the product surface ('lead the team'), not an accident of history."*

This ADR reverses that. The reversal is deliberate and was made with the prior rulings on the
table; it is recorded here rather than argued, per the estate's supersede-never-edit posture.

**Kim's four decisions (live AskUserQuestion, 2026-08-17):**

1. **Role word** — `fleet-marshal`, registering `marshal` in RoleLex. The alternative
   (`fleet-orchestrator`, conforming today at zero ADR cost) was offered and declined. The
   third option — add `marshal` *and* retire a synonym to keep RoleLex flat — was also declined,
   so RoleLex grows to 14.
2. **Command heads** — replace `lead-` entirely. `/lead-*` becomes `/bind-*`.
3. **Bind shape** — hybrid: a parameterized general form plus per-seat aliases for the seats used
   often enough to earn a menu row.
4. **Skill scope** — the full `fleet-*` family, absorbing both `leading-teams` and
   `team-or-solo-rules` alongside the existing `fleet-rules` and `fleet-bootstrap`.

**Why the mechanism-revealing heads are the substantive win.** The estate today exposes one seat
through three doors whose names share nothing: `/lead-build` (the host adopts the contract),
`/build-feature` (`context: fork`), and `build-leader` (an `Agent` dispatch). Three genuinely
different platform mechanics, three unrelated names. `bind-` / `fork-` / `sub-` names the
mechanic, which is what a reader actually needs to predict what a command will do to their
session. The `lead-` head names the *seat*, which the skill and agent names already carry.

**Measured blast radius (`git grep`, `origin/main` @ `d60569b`, 2026-08-17):**

| Name | Hits | Files |
|---|---|---|
| `lead-team` | 122 | 43 |
| `team-or-solo-rules` | 116 | 54 |
| `lead-intake` | 80 | 27 |
| `team-leader` | 71 | 22 |
| `lead-review` | 58 | 24 |
| `leading-teams` | 55 | 26 |
| `lead-build` | 54 | 28 |
| `lead-planning` | 47 | 22 |
| `lead-product` | 30 | 11 |

≈633 string sites. The grammar layer adds `authorkit/skills/naming-audit/scripts/validate.py`,
`naming-conventions/references/GRAMMAR.md`, `references/MANIFEST-TEMPLATE.json`,
`naming-audit/references/CALIBRATION.md`, `manifest-authoring/SKILL.md`,
`.claude/docs/spec/spec-naming-convention.md`, and the repo-root `naming.manifest.json`
(NOT `authorkit/`s own — see "Where the canon actually lives").
Six ADRs cite the rules and are append-only — superseded by citation, never edited.

The campaign crosses a plugin boundary: `lead-intake` is `docs`, everything else is `teamwork`.

## Decisions

### D1 — `marshal` joins RoleLex; the fleet coordinator is `fleet-marshal`

`RoleLex` gains `marshal`, bringing it to 14 members. `fleet` is already in `ObjectVocab`, so
`fleet-marshal` conforms under ADR-0015's `{scope}-{role}` production with no change to the
production itself. `teamwork/agents/team-leader.md` → `teamwork/agents/fleet-marshal.md`.

**Recorded cost.** `marshal` is the fourth coordinative role word alongside `leader`,
`orchestrator`, and `coordinator`, and at ratification it has exactly one consumer. This is the
vocabulary dilution ADR-0015 Alt E rejected and ADR-0018 restated as its bar ("recurring AND
still being minted"). D1 does not meet that bar and does not claim to; it is a deliberate
exception on the grounds that the fleet metaphor is the product surface. Recording the exception
here is what keeps the bar meaningful for the next proposal.

### D2 — `orchestration` joins ProcessLex

Required for `fleet-orchestration` to parse under the `{object}-{process}` skill production.
`ProcessLex` grows from 20 to 21. Unlike D1, `orchestration` has no existing synonym in
`ProcessLex` — `composition` and `wiring` name narrower things — so no dilution cost is recorded.

### D3 — `bind-` / `fork-` / `sub-` become reserved command heads; `lead-` is retired

Three literal verb-first heads replace the single `lead-` head ADR-0016 reserved. Residue after
each head resolves against `ObjectVocab ∪ ProcessLex`, exactly as ADR-0016 D2 specified for
`lead-`. Per ADR-0014's dead-code precedent and ADR-0016's own surface-reality finding, each head
is recognized on **both** the command and skill parse branches — the `/bind-*` surfaces ship as a
mix of true `commands/*.md` files (teamwork, post-#433) and command-species skills (docs).

Semantics, one head per platform mechanic:

| Head | Mechanic | Effect on the caller's session |
|---|---|---|
| `bind-` | seat adoption | the host session itself takes the contract; no spawn |
| `fork-` | `context: fork` | a forked context runs one target, returns, dies |
| `sub-` | `Agent` dispatch | a subagent runs unattended in its own context |

**Retiring `lead-` is the largest single reversal in this ADR** — it supersedes a head ratified
the same day, and `lead` also remains unavailable as a role word (ADR-0017 already ruled
`intake-lead` non-conformant in favour of `intake-leader`). After this ADR, `lead` is a token with
no home in the grammar. That is intended, not an oversight.

### D4 — Bind commands take a hybrid shape

`/bind {agent}` is the general form: one command, one menu description, any registered seat as
argument. Per-seat aliases (`/bind-marshal`, and others as usage justifies) are minted only where
a seat is invoked often enough that its own menu row earns its attention rent. The alias set is
expected to stay small and is reviewed against `attention-audit` output, not grown by default.

`/fork-agent {agent-name}` and `/sub-agent {agent-name}` take the parameterized form only — no
per-seat aliases — since neither mechanic has a seat used often enough to justify one.

### D5 — `team-or-solo-rules` merges into the existing `fleet-rules`

D4's decision to absorb **both** `leading-teams` and `team-or-solo-rules` into the `fleet-*`
family had no conforming realization as first stated: `leading-teams` → `fleet-orchestration` is
clean, but `team-or-solo-rules`' natural family name is `fleet-rules`, **which already exists** as
a distinct skill (the standing fleet's shared doctrine, hard-wired as a `skills:` preload on both
`team-leader` and `build-leader`). Two skills cannot share a name.

**Ruled (Kim, 2026-08-17): merge.** `team-or-solo-rules`' content folds into the existing
`fleet-rules`; the merged skill keeps the `fleet-rules` name and both preload edges. One skill,
one menu description, and the family closes with no fourth token.

**Recorded cost, so the merge is entered with eyes open.** This joins a 15-in-degree
design-decision substrate ("should this be a subagent or a team?" — asked at design time, by
anyone) with a 2-in-degree fleet-operations doctrine ("what may a seat tell a peer?" — asked at
run time, by a bound seat). Different questions, different readers, different moments. Two risks
follow and should be checked rather than assumed:

- **Routing.** One description must now win both classes of ask. The merged description is a
  routing surface with 15 upstream citers; `check-routing` after the merge is not optional, and a
  measurable rise in *leaked* or *stolen* cases against neighbouring skills is the signal to
  revisit.
- **Rent.** `bloat-audit` and `attention-audit` should run on the merged file. A merge that halves
  the menu rows but doubles the description length has not banked the win it was chosen for.

If either check fails, the fallback is D5 alternative (b) — `fleet-composition` or `fleet-wiring`,
both already in `ProcessLex`, conforming at zero lexicon cost — recorded here so a later session
inherits the escape hatch rather than re-deriving it.

**Alternatives declined:** (b) distinct process token, above; (c) leaving `team-or-solo-rules`
outside the family entirely, which was cheapest — it is the single widest-blast-radius name in
the estate at 116 hits / 54 files — but leaves the family incoherent, which was the point of
choosing "both."

## Consequences

**Implementation is authorkit's, under this ADR's ratification** — same owner split as
ADR-0011/0014/0015/0016/0017/0018. Suggested wave order, cheapest-first so each wave's validator
run gates the next:

1. **Lexicon** (#519). Register `marshal` (RoleLex) and `orchestration` (ProcessLex) in the
   **repo-root `naming.manifest.json` only**, plus the same-change `GRAMMAR.md` correction. No
   renames yet. Scope corrected 2026-08-17 against the live tree — see "Where the canon actually
   lives" below; the earlier draft said "both manifests" and named the validator, both wrong.
2. **Grammar heads** (#520). Teach `validate.py` the three heads on both parse branches; retire `lead-`.
   Wave 2 is where the CI ratchet will fail loudest — the five `lead-*` exemptions cannot simply
   be dropped, they must become conformant or the shrink-only array blocks the change.
3. **Agent** (#521). `team-leader` → `fleet-marshal` (71 hits / 22 files). Smallest of the renames and
   it proves the `{scope}-{role}` path end to end.
4. **Skill** (#522). `leading-teams` → `fleet-orchestration` (55 / 26).
5. **Commands** (#523). The six `lead-*` surfaces → `/bind-*`, plus the new `/fork-agent` and
   `/sub-agent` (≈391 hits / ~155 file-touches, crossing into `docs`). Largest wave; splitting
   `lead-intake` into its own sub-wave keeps each PR inside one plugin.
6. **The D5 merge** (#524). `team-or-solo-rules` (116 hits / 54 files) folds into `fleet-rules`. Largest
   single-name blast radius in the estate and it lands on a skill two agents preload, so it goes
   last among the renames. Gates: `check-routing` on the merged description, then `bloat-audit`
   plus `attention-audit` on the merged file, per D5's recorded risks.
7. **Vocabulary sweep (non-grammar)** (#517, executed early). "review desk" → "review seat" in prose — ~45 occurrences,
   ~40 of them inside the `leading-review` family. `seat` is the estate's established word
   (1042 uses); `desk` is an unregistered synonym for it with one consumer. Not governed by the
   grammar, so it needs no lexicon entry — but it is the same dilution in prose that D1 records
   in names, and the campaign is the cheap moment to fix it.

**Every wave is a `rename-planning` → confirm → `rename-execute` cycle**, not a hand edit — the
enumerated-invocation-string and relation-edge legs are exactly what makes a 633-site campaign
survivable. `fix-old-names` ships the CI gate that fails when a config still references a retired
name; it should run against every dependent estate after wave 5.

**Routing surfaces change, so the semantic-edit invariant applies:** same-change `evals/evals.json`
updates plus a fresh-context checker pass inside each build loop, and `check-routing` after
waves 4 and 5 to prove the new heads actually route.

**Issue #475** (teamwork residual description diet) overlaps waves 4–5 and should be sequenced
against them rather than built independently — both edit the same descriptions.

## Where the canon actually lives

`authorkit` is the operative source of truth for naming: `naming-conventions/references/
GRAMMAR.md` is the grammar reference every authorkit skill cites, and
`naming-audit/scripts/validate.py` is the gate. ADRs and the spec are docs-owned decision records
that *govern* that authorkit-owned set — the same owner split ADR-0011/0014/0015/0016/0017/0018
each recorded. Three consequences, all verified against the live tree 2026-08-17:

- **The validator needs no change for D1 or D2.** `validate.py` reads `role_lex` and
  `process_lex` out of the manifest (lines 179-180) rather than hardcoding them. Registering
  `marshal` and `orchestration` is a data edit. Only D3's reserved heads are code.
- **Only the repo-root manifest changes.** `authorkit/naming.manifest.json` is authorkit's
  *estate-local* governance file ("lexicons are closed, change by PR", `exemptions: []` — the
  plugin dogfoods its own spec), and `references/MANIFEST-TEMPLATE.json` is the seed a NEW estate
  copies. Both still carry the original three RoleLex members, which is the proof: ADR-0017's ten
  additions correctly did not propagate to either. Pushing `marshal` — a word with one consumer —
  into the template would seed it into every future estate.
- **`GRAMMAR.md` hardcodes a count.** Line 82 reads "closed; 13 entries", and line 73 enumerates
  role words in prose. D1 makes both wrong, so GRAMMAR.md is a same-change target in wave 1 even
  though the validator is not.

**Gap found while scoping this, not fixed here — filed as #527.** `GRAMMAR.md` restates productions the
docs-owned spec defines, and hardcodes a lexicon count — but `doctrine.manifest.json` carries
**no edge** binding either to its canon. Nothing mechanically catches the reference drifting from
the spec; `doctrine-audit` sweeps only what the manifest declares. A `verbatim-line` or
`ledger-sync` edge would close it. Filed separately rather than folded in — it predates this ADR
and outlives it.

## Records

Filed 2026-08-17. The umbrella carries this ADR; each wave is a child ordered by `Blocked-by:`
per `blocked-by-rules`, so `chore-planner` sequences the queue without hand-tracking.

| Issue | Role |
|---|---|
| [#518](https://github.com/kimgranlund/claude-plugins/issues/518) | **Umbrella** — this ADR, ratification is gate zero |
| [#519](https://github.com/kimgranlund/claude-plugins/issues/519) | Wave 1 — lexicon registration · blocked-by #518 |
| [#520](https://github.com/kimgranlund/claude-plugins/issues/520) | Wave 2 — grammar heads, retire `lead-` · blocked-by #519 |
| [#521](https://github.com/kimgranlund/claude-plugins/issues/521) | Wave 3 — `team-leader` → `fleet-marshal` · blocked-by #520 |
| [#522](https://github.com/kimgranlund/claude-plugins/issues/522) | Wave 4 — `leading-teams` → `fleet-orchestration` · blocked-by #520 |
| [#523](https://github.com/kimgranlund/claude-plugins/issues/523) | Wave 5 — the command surface · blocked-by #520 |
| [#524](https://github.com/kimgranlund/claude-plugins/issues/524) | Wave 6 — the D5 merge · blocked-by #523 |

**Adjacent, not children.** [#517](https://github.com/kimgranlund/claude-plugins/issues/517) is
wave 7 executed ahead of ratification (the desk→seat sweep) and carries only its own routing
gates. [#525](https://github.com/kimgranlund/claude-plugins/issues/525) — which command
entry-point paradigm is the successor — **should be ruled before wave 5 runs**, or the `lead-*`
surfaces get converted twice. [#526](https://github.com/kimgranlund/claude-plugins/issues/526)
sharpens if wave 6 lands. [#527](https://github.com/kimgranlund/claude-plugins/issues/527) —
bind `GRAMMAR.md` to its canon with a doctrine edge — was found while scoping wave 1 and is the
reason this ADR's "Where the canon actually lives" section exists; it predates this campaign and
is not gated on it.

## Alternatives considered

- **`fleet-orchestrator`, no ADR at all.** Conforms today; `orchestrator` is already in RoleLex
  and `fleet` in ObjectVocab. Declined by Kim in favour of the specific word.
- **Add `fork-`/`sub-` only, keep `lead-` for binding.** Names the two genuinely unnamed mechanics
  and supersedes nothing. Declined in favour of the complete scheme.
- **Parameterized `/bind {agent}` with no aliases.** One menu row total. Declined in favour of
  the hybrid, which keeps per-seat argument-hints and tool grants where they earn their cost.
- **`marshal` replacing `leader` in RoleLex.** Would keep the lexicon flat at 13. Declined;
  `leader` has 4 live consumers (`build-leader`, `planning-leader`, `product-leader`,
  `review-leader`) that would all have to move in the same campaign.
