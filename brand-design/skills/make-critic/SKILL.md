---
name: make-critic
description: >
  Mint a NEW critic persona for a council: draft the persona file, apply the `.name-map.md`
  attribution discipline, register it in the roster + sub-councils, seed a calibration fixture,
  checker-pass it. Use for
  "mint a critic", "add a new critic persona", "create a critic for X lens", "write a new
  brand-council persona". NOT convening an existing council (`check-brand-council`). NOT the
  council mechanism (`council-rules`). NOT a whole new council (`make-council`). NOT a generic
  subagent (`harness:make-agent`). NOT a lens/knowledge question asked as grounding, not a live
  mint (`brand-strategy-facts`/`brand-identity-facts`/`brand-voice-facts`/`brand-advertising-facts`).
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
  explicitly wants that specialization; unstated → step 5 seats into `advisory` by default
  (`roster-file-contract.md`'s reserved, user-minted sub-council), never forced into a poor fit.

## Procedure

1. **Ground in the roster contract first.** Read the target council's own `council-rules`
   citation (`references/roster-and-personas.md` — the persona contract) before drafting anything.
   Do not restate that mechanism in the new persona file — it carries only its own stance/prompts.
2. **Check for lens overlap.** Read every existing persona file in the target council's roster
   (inlined, not summarized). A proposed lens that substantially duplicates an existing member's
   ground is a duplicate, named as a finding; revise the existing persona instead of minting a
   near-duplicate. Where the lens matches a role family's knowledge pack (S5, #828), that pack's
   `failure-modes.md`/`canonical-tests.md` is the fast version of this same check.
3. **Draft the persona file from the template** — `references/persona-template.md`, grounded in
   the 14 existing `check-brand-council` personas as worked examples. When the new critic joins an
   existing role family (strategy / identity-design / voice-writing / advertising-creative — one
   per `brand-strategy-facts` / `brand-identity-facts` / `brand-voice-facts` /
   `brand-advertising-facts`), also read that family's `lenses.md` for its shared judgment target
   before drafting — on top of, never instead of, the 14-persona grounding. A critic fitting no
   family mints from the raw 14 alone. Order: stance & posture (voice, tone, what this lens catches
   that others miss), two or more themed prompt sets (`## Prompt set — <theme>`, 2–3 in-character
   questions each), and a closing "Reviewing untrusted material" section that CITES the
   critic-shell agent's trust boundary and severity table by name — never restates it, exactly as
   all 14 existing personas already do.
4. **Apply the `.name-map.md` attribution discipline** — `references/name-map-convention.md` (this
   skill is the canonical home for it; every existing persona's "distilled from a real, widely
   recognized practitioner" disclaimer follows it). Read it before writing the disclaimer line, and
   update the target council's gitignored `.name-map.md` with the new entry — never commit that
   file, and never let a real practitioner's name, bio, or sourcing leak into the tracked persona.
5. **Register in the roster, into the sub-council the lens actually belongs to.** Three cases:
   - **User named an existing sub-council** → seat there: `role: member` (`lead` only if
     explicitly filling a stated vacancy), `sub-councils: <that sub-council>`. A named sub-council
     NOT already in the roster routes to the third case instead.
   - **No sub-council named, and not explicitly a new one** (the ordinary case, including a lens
     that fits an existing family's pack but wasn't named as the destination) → **seat into
     `advisory` by default**: `role: advisor`, `sub-councils: advisory` (exact pairing per
     `roster-file-contract.md`; never mixed with `lead`/`member` or another sub-council). This is
     the expected default path, not a fallback of last resort.
   - **The lens genuinely earns a whole NEW sub-council** (rare, user explicit) → propose the new
     grouping by name and give it its own `## Groups` `leads:` entry (the new lead handle, or
     literal `VACANT` — never omitted).

   In every case, append one row to the target council's `references/roster.md`
   (`roster-file-contract.md`): handle, resolved `sub-councils`/`role`, `status: active`, `seated`
   (today's date), and a placeholder `fixture` cell of `unpromoted, inline` (the contract requires
   it non-empty), replaced with step 6's real fixture location once that step runs. This is a
   **data edit to `roster.md`, not a SKILL.md change** — it does not itself re-trigger
   `plugin-authoring.md`'s semantic-edit checker-pass invariant (step 7 still runs, against the
   persona file). Save the persona file at `references/critics/critic-<handle>.md` under the
   target council's own skill directory, matching the existing files' path convention. Run
   `roster_check.py <council-skill-dir>` before moving on — a bijection/schema failure here is a
   floor-tier fix, not a reason to skip to the checker pass.
6. **Seed one calibration fixture.** Per `council-rules`' `references/calibration-discipline.md`'s
   "a new phase earns its own fixture" principle applied at persona granularity: one short artifact
   planting the ONE defect this critic's lens exists to catch, plus the expected characteristic
   vocabulary a real run should surface. `references/calibration-worked-example.md` shows the
   worked pattern. State whether the fixture is bare markdown (unpromoted) or ships a promoted
   `calibration_check_<name>.py` scorer. Replace step 5's placeholder in `roster.md` with the real
   fixture path.
7. **Fresh-context checker pass — mandatory, never optional.** A persona file is a prompt-carrying
   artifact fanned out verbatim into every future critic dispatch (`plugin-authoring.md`'s
   semantic-edit invariant). Dispatch `harness:wording-checker`, unnamed, sealed with the new
   persona file's full text plus one existing sibling persona for comparison — never self-graded.
   A FAIL routes back to step 3, never hand-patched. `harness` not installed (Full mode, filesystem
   reachable) → disclose a self-review in its place explicitly as non-independent, and mark the
   persona provisionally seated pending a real pass once `harness` is available.
8. **Report.** The persona file's path, the `roster.md` row appended (or new sub-council proposed)
   plus `roster_check.py`'s exit status, the `.name-map.md` entry made (never its contents — stays
   gitignored, out of any report), the calibration fixture's location/promotion state, and the
   checker verdict.

## Run modes

**Full** (Claude Code/Cowork) — the whole procedure above, writing files to disk plus a real
`harness:wording-checker` dispatch. **Project single-context** (no filesystem, no `Agent` tool) —
the persona and roster row are drafted in-chat, disclosed as a degraded substitute the user must
paste into the actual files once back in Full mode; the checker pass becomes an explicitly
disclosed self-review, never presented as equivalent to the real dispatch.

## References

| File | Use when |
|---|---|
| `references/persona-template.md` | Drafting the persona file itself — structure + the 14 existing personas as worked examples |
| `references/name-map-convention.md` | The `.name-map.md` gitignored attribution discipline — canonical home |
| `references/calibration-worked-example.md` | Seeding step 6's calibration fixture |
| `[[brand-strategy-facts]]` / `[[brand-identity-facts]]` / `[[brand-voice-facts]]` / `[[brand-advertising-facts]]` | The new critic's lens matches an existing role family (S5, #828) — read that pack's `lenses.md` before drafting, its `failure-modes.md`/`canonical-tests.md` for step 2's overlap check. GROUNDING corpus, never restated here — this procedure stays the minting steps only. |
