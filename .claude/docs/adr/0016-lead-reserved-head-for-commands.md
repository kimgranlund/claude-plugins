---
doc-type: adr
id: adr-0016
status: accepted
ratified: ratified 2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead), confirming
  the overnight standing-directive authorization
date: 2026-08-17
owner: kim.granlund
supersedes: adr-0011 (one clause of D7 only — the command production's requirement that every
  non-wrapper command name terminate in a VerbLex verb after an object phrase, as §3.1 adopted
  it. D7's skill/agent productions, D8's grandfather-and-ratchet posture, D9, and D10 all stand
  unamended; ADR-0014's §14.2 amendments and ADR-0015's §14.4 amendments stand unamended)
intent-refs: null
---
# ADR-0016 — The command grammar gains a reserved verb-first head `lead-`; `lead-{scope}` conforms when scope resolves against the orchestrator scope pool

> **Ratified 2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead, recorded in issue
> #433's 2026-08-17 Findings comment), confirming the overnight standing-directive
> authorization; from ratification this file is append-only (doc_lint T4) — a change of mind
> supersedes, never edits.** Drafted 2026-08-16 from issue #433 (Kim's
> explicit spec that the human-facing seat-adoption commands stay `/lead-*`) and issue #373's
> Findings (2026-08-16), which record the same standing-authorization pattern. ADR-0011 is NOT
> edited by this change — accepted ADRs are append-only; the partial supersession is recorded
> by this ADR's `supersedes:` field alone, exactly as ADR-0013 and ADR-0015 recorded theirs.

## Context

The `lead-*` command family is the human-facing seat-adoption surface: `/lead-team`,
`/lead-build`, `/lead-planning`, `/lead-review` (shipped, teamwork), `/lead-intake` (shipped,
docs), and `/lead-product` (planned — issue #433's product-seat leg). Each makes the HOST
session adopt an orchestrator seat's contract for one charter. Kim's spec on #433 is explicit:
these commands stay `/lead-*` — the verb-first shape IS the product surface ("lead the team"),
not an accident of history.

The command grammar cannot admit them:

- **ADR-0011 D7 / spec §3.1** makes commands object-first — `{object}-{verb}`, terminal token
  ∈ `VerbLex` — with one escape (the §7 wrapper production: a command named identically to the
  skill it wraps). `lead-team` is verb-FIRST: `lead` heads the name and `team` is no verb.
  `authorkit/skills/naming-audit/scripts/validate.py`'s `Grammar.parse` command branch rejects
  it (`command terminal 'team' not in VerbLex`), and the skill branch — which is where these
  names actually parse, see the surface-reality paragraph below — rejects it too (`lead`
  resolves in no lexicon or vocab).
- **ADR-0011 D8** makes the `naming.manifest.json` `exemptions` array a shrink-only CI ratchet.
  Four of the five #433 names sit in it today (`lead-build`, `lead-planning`, `lead-review`,
  `lead-team`; the manifest's fifth `lead-*` entry is `lead-intake`, outside #433's five). The
  planned `lead-product` cannot be admitted by exemption at all — D8 forbids growth — so
  without a grammar amendment #433's product-seat command leg is unbuildable under the canon.

**Surface reality (measured at HEAD 1389ac0, 2026-08-16):** none of the `lead-*` surfaces is
a `commands/*.md` file. All five shipped names are command-species SKILLS —
`teamwork/skills/lead-{team,build,planning,review}/`, `docs/skills/lead-intake/` — carrying
`user-invocable: true` + `disable-model-invocation: true` and invoked as `/lead-*`. Spec §6
decides kind by directory, so the validator parses them as `kind == "skill"`. Any amendment
that touched only the command branch would therefore be dead paper against the live estate —
the same dead-code hazard ADR-0014 documented for the `check-` head's placement. The precedent
runs deeper: `check` is a `VerbLex` verb, yet ADR-0014 D2's reserved `check-` head lives on the
SKILL branch, because that is where `check-*` names actually exist. This ADR follows that
precedent: the reserved head is defined at the command grammar (§3.1 — where it conceptually
belongs: `/lead-*` is a user-invoked imperative surface) and recognized by the validator on
both the command AND skill parse branches.

**Scope arithmetic (verified by hand against `naming.manifest.json` at HEAD):** ADR-0015 D2
defined the orchestrator scope pool `ObjectVocab ∪ ProcessLex` (and registered `build` in
`ObjectVocab`). Against that pool: `team` ∈ OV, `product` ∈ OV, `build` ∈ OV, `planning` ∈ PL,
`review` ∈ PL — all five of #433's scopes resolve. `intake` resolves in NO lexicon or vocab —
so `lead-intake` does not conform under this ADR and stays exempt (deliberately: see D3).

**Owner boundary — same split as ADR-0011/0014/0015.** This ADR is a docs-owned record
amending a docs-owned spec that governs an authorkit-owned validator and reference set.
Ratification provenance is the standing directive named in `ratified:`; the follow-on
implementation is authorkit's, executed in the same change under the same authorization.

## Decision

**The command grammar (spec §3.1) gains a RESERVED VERB-FIRST HEAD `lead-`.** A name
`lead-{scope}` conforms when `{scope}` resolves against the orchestrator scope pool ADR-0015 D2
defined (`ObjectVocab ∪ ProcessLex`), mirroring ADR-0014's reserved `check-` head precedent.

### D1 — The production, and why the pool is ADR-0015's

Spec §3.1 (and GRAMMAR.md's Productions block) gains:

```
command := "lead" "-" scope        lead-team, lead-review   (reserved head, §14.5, ADR-0016)
```

- `lead` is a **literal**, exactly as `check` is in ADR-0014 D2 — not a `VerbLex` member, not a
  lexicon token, not a template for other verbs. One reserved head, closed.
- `scope` resolves via the SAME greedy longest-match algorithm against the SAME pool as the
  orchestrator agent production (`Grammar.resolve_orchestrator_scope`, ADR-0015 D2:
  `ObjectVocab ∪ ProcessLex`, deliberately no `TopicLex`). This is not code reuse for its own
  sake — it is the semantics: a `/lead-{scope}` command makes the session ADOPT the
  orchestrator seat whose scope that is. The command and the agent it adopts coordinate the
  same thing or process (`/lead-team` adopts the team seat's contract; `/lead-review` the
  review seat's). One scope vocabulary for "what a seat coordinates", whether the seat is a
  dispatched agent or the host session itself.
- The head clears spec §9's stated bar for a new reserved head ("the validator or router must
  treat it differently"): the validator resolves the residue against a different pool than any
  other command shape, and the surface routes differently — `/lead-*` converts the host
  session rather than dispatching work.

### D2 — Validator recognition on BOTH parse branches

`validate.py`'s `Grammar.parse` recognizes the head twice, because kind is decided by
directory (§6) and the live surfaces are skills:

1. **`kind == "command"` branch:** before the terminal-verb check, a name whose first token is
   `lead` (≥ 2 tokens) resolves `tokens[1:]` against the orchestrator scope pool; conforms iff
   resolution succeeds. A verb-first command that is NOT `lead-*` still fails exactly as today.
2. **`kind == "skill"` branch:** the same check, placed BEFORE the object-process
   (ProcessLex-terminal) check — mandatory ordering, not style: `lead-review` and
   `lead-planning` have ProcessLex terminals, so a later placement is unreachable dead code
   for exactly the names this ADR exists for (the same hazard ADR-0014 documented for
   `check-stage`, and the same fix).

The skill-branch recognition does NOT license `lead-*` as a general skill shape divorced from
the command surface — it exists because command-species skills are how this platform ships
user-invoked surfaces (spec §14.1 already crossed that bridge for reverse-wrappers). A
`lead-{scope}` name remains, semantically, a command.

### D3 — Exemption retirement and the one that stays

- **Four exemptions RETIRE** (D8's burn-down direction, honored): `lead-build`,
  `lead-planning`, `lead-review`, `lead-team` leave `naming.manifest.json`'s `exemptions`
  (124 → 120). They conform by grammar from this ADR on.
- **`lead-intake` STAYS exempt.** `intake` resolves in no lexicon or vocab, and this ADR does
  not register it. Registering a word into `ObjectVocab`/`ProcessLex` solely to clear one
  exemption is the vocabulary dilution ADR-0014 Alt B and ADR-0015 Alt E both rejected; if
  `intake` earns registration later it goes through `manifest-authoring`'s ordinary AC-008
  gate, and `lead-intake`'s exemption retires then, opportunistically (§10's own posture).
- **`lead-product` mints as a new conforming name** — no exemption needed, which is the whole
  point: #433's product-seat command leg is unblocked without touching D8.

### D4 — What does NOT change (the fence)

- **`VerbLex` is untouched.** `lead` joins no lexicon; it is a reserved literal. No other verb
  gains a verb-first production (spec §14.2's own non-goal, restated: generalizing a reserved
  head to a lexicon-wide production is a rejected alternative, not a follow-on).
- **Agent grammar (§3.3, ADR-0015's two orchestrator spellings), skill grammar otherwise
  (§3.2, §14.1 reverse-wrapper, §14.2 `-rules`/`check-`), the `-agent` reserved head, the
  wrapper production, `VerbLex ∩ ProcessLex = ∅`, `RoleLex` disjointness (ADR-0015 D3)** — all
  unchanged. `lead-*` names in `agents/` still fail (no `RoleLex` terminal, no `-agent` tail);
  the agent seats (`team-lead`, `build-lead`, `intake-lead`) stay exempt person-word names
  exactly as ADR-0015 D4 left them.
- **The `leading-*` SKILL family (Kim's ruling #1 on #433, 2026-08-16; PR #442) is orthogonal
  and unaffected.** That ruling renames the seat-adoption SKILLS to `leading-{teams, builds,
  planning, review, product}`, conforming by ordinary lexicon registration (`leading` and the
  `teams` plural in `ObjectVocab`) under the existing §3.2 productions — no reserved head
  involved. This ADR's `lead-` head fires only on the exact token `lead`, so it neither
  licenses nor blocks `leading-*`; both rulings hold simultaneously (verified 2026-08-16:
  PR #442's teamwork tree plus a `lead-product` command audits 0 grammar errors under this
  ADR's validator with #442's manifest). The skill-branch recognition in D2 remains necessary
  for the interval where the live skills are still named `lead-*` with their exemptions
  retired (D3); once #442's renames land it simply matches no name, which is harmless — #442
  ships the surviving `/lead-*` surfaces as `commands/*.md` wrappers, moving them onto D2's
  command branch.
- **ADR-0011 D8's ratchet only shrinks.** This ADR retires four entries and admits zero; the
  array never grows.
- **ADR-0015 is amended by citation, not edited** — it is the sibling amendment whose scope
  pool this ADR reuses; its file is append-only and stays untouched.
- **Estate scope:** spec-level, so all three governed estates; only nonoun-plugins was
  measured. Other estates' manifests need no change unless they ship a `lead-*` surface.

### Alternatives considered

- **Alt A — keep the four exemptions and exempt `lead-product` too.** Killed: D8 forbids any
  addition outright (CI diffs the array), so `lead-product` cannot ship this way at all; and
  keeping retirable exemptions alive contradicts D8's burn-down direction when a one-production
  amendment retires four at once.
- **Alt B — rename the family object-first (`team-lead`, `build-lead`, …).** Killed by ruling
  (Kim, #433: commands stay `/lead-*`) and on the merits: `team-lead` and `build-lead` are the
  estate's AGENT seat names — the rename would collide a command surface with an agent name
  across plugins, and `/team-<tab>` autocomplete grouping buys nothing for a five-member family
  whose users know it as "the lead commands".
- **Alt C — register `lead` in `VerbLex` and invert §3.1 to admit verb-first commands
  generally.** Killed: object-first is §3.1's load-bearing ergonomic (autocomplete groups by
  object); a general verb-first production would dissolve it for every verb to serve one
  family. A single reserved literal is the narrowest cut — ADR-0014 made the identical
  argument for `check-` ("one literal reserved head, closed — not a VerbLex-wide production").
- **Alt D — command-branch recognition only (skip the skill branch).** Killed by the measured
  surface reality: zero of the five names is a `commands/*.md` file, so the amendment would
  validate nothing that exists, retire no exemption, and leave `lead-product` unmintable as
  the command-species skill it will actually be. Dead paper.

## Consequences

- **Ratification provenance:** Kim ratified live (2026-08-17, AskUserQuestion via
  plugins-team-lead, recorded in issue #433's Findings), confirming the overnight
  standing-directive authorization under which the draft was prepared. A change of mind is a
  superseding ADR (this file stays append-only), and the implementation below reverts by
  ordinary PR.
- **The follow-on execution (authorkit-owned, same PR as this ADR under the same
  authorization, authorkit version bump + README ledger row) is:**
  1. `validate.py` `Grammar.parse`: the D2 recognition on both branches, reusing
     `resolve_orchestrator_scope` (no new pool is built — ADR-0015 D2's pool is the pool).
  2. Validator selftest fixtures, mirroring §14.1/§14.2/§14.4's positive/negative/regression
     triad: positive — all five (`lead-team`, `lead-product`, `lead-build` as ObjectVocab
     scopes; `lead-planning`, `lead-review` as ProcessLex scopes) parse clean as skills, and
     `lead-team` parses clean as a command; negative — a non-`lead` verb-first command
     (`sweep-team`-shaped) still fails; negative — `lead-{unregistered}` (`lead-intake`'s
     class) still fails on both branches; regression — object-first commands and
     object-process skills unaffected.
  3. `naming.manifest.json`: `exemptions` −4 (D3, 124 → 120); `$schema_note` gains a dated
     sentence recording the `lead-` reserved head per this ADR, with D8's ratchet sentence
     left verbatim.
  4. `authorkit/skills/naming-conventions/references/GRAMMAR.md`: Productions block (command
     section), the reserved heads/tails line, and the Commands prose gain the `lead-`
     production with this ADR as authority.
  5. `.claude/docs/spec/spec-naming-convention.md`: §3 production block and §3.1 prose gain
     the production (D1); a dated **§14.5** appended mirroring §14.2/§14.4's pattern (ruling
     authority = this ADR, validator change, selftest fixtures, non-goals).
  6. **ADR-0011 and ADR-0015 are not edited, then or later** — both are accepted and
     append-only; supersession/citation live in this file's frontmatter and body.
  7. Re-run `authorkit:naming-audit --scope grammar` estate-wide and confirm 0 grammar errors,
     120 exemptions after (124 before).
- **`intent-refs: null` is deliberate** — same posture as ADRs 0001–0015; the T6 orphan-ADR
  WARN is accepted as-is.
- **Easier, once landed:** `lead-product` mints clean (unblocking #433's product-seat command
  leg); four exemptions burn down; any future seat-adoption command (`/lead-fleet`, say —
  `fleet` ∈ ObjectVocab already) conforms from day one; the command surface and the agent
  seats share one scope vocabulary.
- **Harder, once landed:** the estate now carries three reserved heads/tails beyond `-agent`
  (`check-`, `-rules`, `lead-`) — each future proposal must still clear §9's bar individually,
  and the accumulating list is itself a signal to watch (three literals is a grammar; ten
  would be a lexicon wearing a disguise).
- **Irreversible in the ratchet sense:** four retirements. A reversal ADR could not re-admit
  `lead-build`/`lead-planning`/`lead-review`/`lead-team` by exemption (D8 forbids re-growth) —
  it would have to keep some conforming production for them or force renames. Retirement is
  therefore the durable direction of travel, as D8 intends.
