---
name: make-critic
description: >
  Mint a NEW critic persona for a council: draft the persona file (stance/posture, prompt sets, a
  severity section citing the critic-shell agent, never restating it), apply the `.name-map.md`
  attribution discipline, register it in the roster + sub-councils, seed a calibration fixture, and
  checker-pass it before it seats. Use for "mint a critic", "add a new critic persona", "create a
  critic for X lens", "write a new brand-council persona". NOT convening an existing council
  (`check-brand-council`); NOT the council mechanism (`council-rules`); NOT a whole new council
  (`make-council`); NOT a generic subagent (`harness:make-agent`).
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
  silently mint past.

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
5. **Register in the roster.** Add one row to the target council's own Roster table (e.g.
   `check-brand-council`'s SKILL.md), under the sub-council the lens belongs to — or propose a new
   sub-council grouping, named explicitly, if the lens doesn't fit an existing one (never silently
   folded into the nearest group). Save the persona file at
   `references/critics/critic-<handle>.md` under the target council's own skill directory,
   matching the existing 14 files' own path convention exactly.
6. **Seed one calibration fixture.** A brief new-critic proof, per `council-rules`' `references/
   calibration-discipline.md`'s "a new phase earns its own fixture" principle applied at persona
   granularity: one short artifact planting the ONE defect this critic's lens exists to catch, plus
   the expected characteristic vocabulary a real run should surface. `references/
   calibration-worked-example.md` shows the full worked pattern. State plainly whether the fixture
   is a bare markdown fixture (unpromoted) or ships a promoted `calibration_check_<name>.py`
   scorer — `calibration-discipline.md`'s own promoted-script contract applies only once promoted,
   never assumed.
7. **Fresh-context checker pass — mandatory, never optional.** A persona file is a prompt-carrying
   artifact fanned out verbatim into every future critic dispatch (`plugin-authoring.md`'s semantic-
   edit invariant), so it earns the same independent pass as a SKILL.md or agent body. Dispatch
   `harness:wording-checker`, unnamed, sealed with the new persona file's full text plus one
   existing sibling persona for comparison — never self-graded by this procedure. A FAIL routes
   back to step 3, never seats a persona a checker rejected. `harness` not installed in the current
   plugin set (Full mode, filesystem reachable) → disclose a self-review in its place explicitly as
   non-independent, and mark the persona provisionally seated pending a real pass once `harness` is
   available — never silently treat the self-review as equivalent to the real dispatch.
8. **Report.** The persona file's path, the roster row added (or the new sub-council proposed),
   the `.name-map.md` entry made (never its contents — that file stays gitignored and out of any
   report), the calibration fixture's location and promotion state, and the checker verdict.

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
critic-shell agent's severity/trust-boundary mechanics rather than restating them, is registered in
the roster table under a named sub-council, carries a `.name-map.md` entry (gitignored, never
committed), has at least one calibration fixture proving its lens catches its own planted defect,
and passed an independent fresh-context checker. **NOT done** when a persona restates council-rules
or critic-shell machinery instead of citing it, when a real practitioner's identity leaked into the
tracked file, when the roster table was left unedited, or when a checker FAIL was hand-patched
instead of re-drafted and re-checked.

## References

| File | Use when |
|---|---|
| `references/persona-template.md` | Drafting the persona file itself — structure + the 14 existing personas as worked examples |
| `references/name-map-convention.md` | The `.name-map.md` gitignored attribution discipline — canonical home |
| `references/calibration-worked-example.md` | Seeding step 6's calibration fixture |
| `[[brand-strategy-facts]]` / `[[brand-identity-facts]]` / `[[brand-voice-facts]]` / `[[brand-advertising-facts]]` | The new critic's lens matches an existing role family (S5, #828) — read that pack's `lenses.md` before drafting, its `failure-modes.md`/`canonical-tests.md` for step 2's overlap check. GROUNDING corpus, never restated here — this procedure stays the minting steps only. |
