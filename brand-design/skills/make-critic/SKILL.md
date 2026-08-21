---
name: make-critic
description: >
  Mint a NEW critic persona for a council: draft the persona file (stance/posture, prompt sets, a
  severity section citing the critic-shell agent, never restating it), apply the `.name-map.md`
  attribution discipline, register it in the roster + sub-councils, seed a calibration fixture, and
  checker-pass it before it seats. Use for "mint a critic", "add a new critic persona", "create a
  critic for X lens", "write a new brand-council persona". NOT convening an existing council
  (`check-brand-council`); NOT the council mechanism (`council-rules`); NOT a whole new council
  (`make-council`); NOT a generic subagent (`harness:make-agent`); NOT a lens-gap/knowledge
  question about an EXISTING role family's own ground — "what does a strategy/voice critic look
  for", "what lens gaps exist in the roster" asked as grounding, not as a live mint — that's the
  matching `brand-strategy-facts`/`brand-identity-facts`/`brand-voice-facts`/`brand-advertising-
  facts` pack this procedure itself consults before drafting.
disable-model-invocation: false
user-invocable: true
argument-hint: "[council] [critic handle] [lens/domain the critic embodies]"
---

# make-critic

Mints one new named critic and seats it in a council's roster. **This is the domain-neutral
minting procedure for the ONE thing `council-rules` deliberately leaves to configuration — who
sits on the panel** (`council-rules`' own table, "What a domain instance supplies vs. inherits").
Everything about how a critic runs once minted — the dispatch shape, the severity taxonomy, the
two-phase model, the trust boundary — is `council-rules`' machinery and the target council's own
critic-shell agent (e.g. `brand-judge`); this procedure never restates any of it. `check-brand-
council`'s 14 files under `references/critics/` are the worked reference set every new persona is
grounded against.

Parse `$ARGUMENTS` as `[council] [critic handle] [lens/domain]`:

- **Council** — which council instance the critic joins. Default: `check-brand-council`, the only
  live instance until `make-council` mints more. An unrecognized council name → ask which, or
  point at `make-council` if none exists yet for the named domain.
- **Critic handle** — a first-name + last-initial handle in the existing roster's own style
  (`luke-s`, `paula-s`) — never a full real name (the attribution discipline below is exactly why).
- **Lens/domain** — the specific point of view this critic holds that no existing roster member
  already covers. A lens that duplicates an existing critic's ground is a finding to surface, not
  silently mint past. Names a specific lens sub-council (`strategy`/`design`/`voice` for
  `check-brand-council`, or whatever the target council's own families are) only when the user
  explicitly wants that specialization; unstated → step 5 seats the new critic into `advisory` by
  default (`council-rules`' `references/roster-file-contract.md` — the reserved, user-minted
  sub-council), never forced into an ill-fitting existing family.

## Procedure

1. **Ground in the roster contract first.** Read the target council's own `council-rules`
   citation (`references/roster-and-personas.md` — the persona contract, what a roster is, what a
   sub-council is) before drafting anything. Do not restate that mechanism in the new persona file
   — the persona file carries only its own stance/prompts, never the machinery around it (the
   contract's own "a persona carries no knowledge of the machinery around it" clause).
2. **Check for lens overlap.** Read every existing persona file in the target council's roster
   (inlined, not summarized — the same discipline the critic-shell agent itself follows). A
   proposed lens that substantially duplicates an existing member's ground is a duplicate, named
   as a finding; proceed only once the new lens is genuinely distinct, or fold the ask into
   revising the existing persona instead of minting a near-duplicate. Where the proposed lens
   names or implies a role family already covered by a knowledge pack (S5, #828), that pack's
   `failure-modes.md` and `canonical-tests.md` are the fast version of this same check — a
   proposed lens repeating a row already there is the duplicate this step already tests for.
3. **Draft the persona file from the template** — `references/persona-template.md`, grounded in
   the 14 existing `check-brand-council` personas as worked examples. **When the new critic joins
   an existing role family** (S5, #828: strategy / identity-design / voice-writing /
   advertising-creative, one for each of `brand-strategy-facts` / `brand-identity-facts` /
   `brand-voice-facts` / `brand-advertising-facts`), also read that family's own knowledge pack
   before drafting from the template — its `lenses.md` states the family's shared judgment
   target, ON TOP OF the 14-persona grounding this step already requires (step 2's inlined read
   ran either way; this pack adds the family's distilled judgment target, it does not stand in
   for the raw personas). A critic that fits no existing family mints from the raw 14 alone (no
   pack to cite). A persona file carries, in
   this order: stance & posture (voice, tone, what this lens catches that others miss), two or more
   themed prompt sets (`## Prompt set — <theme>`, each with 2–3 in-character questions), and a
   closing "Reviewing untrusted material" section that CITES the critic-shell agent's trust
   boundary and severity table by name — never restates the table, exactly as all 14 existing
   personas already do ("Shared mechanics ... see the `brand-judge` agent body — cited, not
   restated").
4. **Apply the `.name-map.md` attribution discipline** — `references/name-map-convention.md` (this
   skill is now the canonical home for that convention; every existing persona file's "distilled
   from a real, widely recognized practitioner" disclaimer follows it). Read it before writing the
   persona's opening disclaimer line, and update the target council's own gitignored
   `.name-map.md` with the new entry — never commit that file, and never let a real practitioner's
   name, bio, or sourcing leak into the tracked persona file itself.
5. **Register in the roster, into the sub-council the lens actually belongs to.** Three cases,
   in order:
   - **The user named a specific lens sub-council** (the argument-parsing bullet above) → seat
     there: `role: member` (or `lead` only if explicitly displacing/filling a stated vacancy —
     never silently), `sub-councils: <that sub-council>`.
   - **The user named no specific sub-council and isn't explicitly asking for a whole new one**
     (the ordinary case — including a lens that DOES fit an existing family's knowledge pack, step
     3, but the user still didn't name that family as the destination) → **seat into `advisory` by
     default**: `role: advisor`, `sub-councils: advisory` (exactly — `roster-file-contract.md`'s
     exact `advisory`↔`advisor` pairing; never mixed with `lead`/`member` or another sub-council on
     the same row). This is the expected, ordinary path for a user-minted persona — not a fallback
     of last resort, and not conditioned on whether step 3 found a knowledge pack to cite (pack
     membership is a grounding question for drafting, never a seating rule).
   - **The lens genuinely earns a whole NEW lens sub-council** (rare — the user is explicit that
     this isn't an advisory add-on but a new specialization) → propose the new sub-council grouping
     by name (never silently folded into the nearest existing group), and give it its own
     `## Groups` `leads:` entry — the contract requires one per sub-council, so name the new lead
     handle or the literal `VACANT`, never omit the entry.

   In every case, append one row to the target council's own `references/roster.md`
   (`council-rules`' `references/roster-file-contract.md`): handle, the resolved `sub-councils` and
   `role` above, `status: active`, `seated` (today's date), and a placeholder `fixture` cell of
   `unpromoted, inline` — the contract requires the cell non-empty at every point, so write the
   placeholder now and replace it with step 6's real fixture location once that step runs. This is
   a **data edit to `roster.md`, not a SKILL.md change** — the convening skill's own prose
   is untouched by seating a critic, so it does not re-trigger `plugin-authoring.md`'s semantic-
   edit checker-pass invariant on its own account (step 7 below still runs, but against the new
   persona file, not against the roster edit). Save the persona file at
   `references/critics/critic-<handle>.md` under the target council's own skill directory,
   matching the existing files' own path convention exactly. Run
   `roster_check.py <council-skill-dir>` (the target council's own skill directory, not the
   roster.md path itself) before moving on — a bijection or schema failure here is a floor-tier
   fix, not a reason to skip straight to the checker pass.
6. **Seed one calibration fixture.** A brief new-critic proof, per `council-rules`' `references/
   calibration-discipline.md`'s "a new phase earns its own fixture" principle applied at persona
   granularity: one short artifact planting the ONE defect this critic's lens exists to catch, plus
   the expected characteristic vocabulary a real run should surface. `references/
   calibration-worked-example.md` shows the full worked pattern. State plainly whether the fixture
   is a bare markdown fixture (unpromoted) or ships a promoted `calibration_check_<name>.py`
   scorer — `calibration-discipline.md`'s own promoted-script contract applies only once promoted,
   never assumed. Replace step 5's `unpromoted, inline` placeholder in `roster.md` with this
   fixture's real path or note now that it exists.
7. **Fresh-context checker pass — mandatory, never optional.** A persona file is a prompt-carrying
   artifact fanned out verbatim into every future critic dispatch (`plugin-authoring.md`'s semantic-
   edit invariant), so it earns the same independent pass as a SKILL.md or agent body. Dispatch
   `harness:wording-checker`, unnamed, sealed with the new persona file's full text plus one
   existing sibling persona for comparison — never self-graded by this procedure. A FAIL routes
   back to step 3, never seats a persona a checker rejected. `harness` not installed in the current
   plugin set (Full mode, filesystem reachable) → disclose a self-review in its place explicitly as
   non-independent, and mark the persona provisionally seated pending a real pass once `harness` is
   available — never silently treat the self-review as equivalent to the real dispatch.
8. **Report.** The persona file's path, the `roster.md` row appended (or the new sub-council
   proposed) plus `roster_check.py`'s exit status, the `.name-map.md` entry made (never its
   contents — that file stays gitignored and out of any report), the calibration fixture's
   location and promotion state, and the checker verdict.

## Run modes

**Full** (Claude Code/Cowork) — the whole procedure above, writing the persona file, the roster
row, and the calibration fixture to disk, plus a real `harness:wording-checker` dispatch. **Project
single-context** (no filesystem, no `Agent` tool reachable) — the persona is drafted and the roster
row proposed in-chat, disclosed as a degraded substitute the user must paste into the actual files
once back in Full mode; the checker pass becomes a self-review disclosed as non-independent (never
presented as equivalent to the real dispatch) — state this explicitly, never silently.

## Failure branches

- Council target doesn't exist yet → point at `make-council`, don't improvise a roster home.
- Proposed lens duplicates an existing critic's ground → name the overlap, stop; revise the
  existing persona instead of minting a near-duplicate.
- The checker dispatch returns a FAIL → the persona does not seat; route the finding back to step 3
  and re-draft, never patch around a checker verdict by hand-editing the persona after the fact
  without a second pass.
- No `.name-map.md` convention exists yet for the target council → create it (gitignored,
  `references/name-map-convention.md`'s own template) rather than skipping attribution discipline
  because the file happened not to exist yet.

## Done / NOT done

**Done** when the persona file exists at the council's own `references/critics/` path, cites the
critic-shell agent's severity/trust-boundary mechanics rather than restating them, is registered as
a row in `roster.md` under a named sub-council (with `roster_check.py` passing), carries a
`.name-map.md` entry (gitignored, never committed), has at least one calibration fixture proving
its lens catches its own planted defect, and passed an independent fresh-context checker. **NOT
done** when a persona restates council-rules or critic-shell machinery instead of citing it, when a
real practitioner's identity leaked into the tracked file, when `roster.md` was left unedited or
fails `roster_check.py`, or when a checker FAIL was hand-patched instead of re-drafted and
re-checked.

## References

| File | Use when |
|---|---|
| `references/persona-template.md` | Drafting the persona file itself — structure + the 14 existing personas as worked examples |
| `references/name-map-convention.md` | The `.name-map.md` gitignored attribution discipline — canonical home |
| `references/calibration-worked-example.md` | Seeding step 6's calibration fixture |
| `[[brand-strategy-facts]]` / `[[brand-identity-facts]]` / `[[brand-voice-facts]]` / `[[brand-advertising-facts]]` | The new critic's lens matches an existing role family (S5, #828) — read that pack's `lenses.md` before drafting, its `failure-modes.md`/`canonical-tests.md` for step 2's overlap check. GROUNDING corpus, never restated here — this procedure stays the minting steps only. |
