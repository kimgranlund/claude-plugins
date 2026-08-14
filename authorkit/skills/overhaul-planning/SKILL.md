---
name: overhaul-planning
kind: skill
description: >
  Generate a phased estate-overhaul plan for a target (estate, plugin set, or member list):
  measure first, one design doc with a per-member kill-switch (can return "no move") that also
  nominates merge/split candidates and tiers each member procedure-vs-knowledge cost, then
  waved ticket seeds with Blocked-by edges. Use for a rename/reshape/merge/split campaign
  across many members. Plan-only: writes the doc and seeds, never executes. NOT for one
  artifact rename (rename-planning); NOT for a plain audit (naming-audit, bloat-audit); NOT
  for a single-pair merge/split (plan-skill-merge/plan-skill-split); NOT for executing or
  driving the campaign (rename-execute, /overhaul-execute).
author: kim
created: 2026-08-14
last_updated: 2026-08-14
requires: [naming-audit, bloat-audit, rename-planning, naming-conventions]
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - Bash(python3 */scripts/validate.py *)
  - Bash(python3 */scripts/measure.py *)
---

# overhaul-planning

The estate-scale sibling above `rename-planning`'s per-member blast radius — proven live by
the #197 campaign, where the design phase killed 7 of 8 proposed moves. **Hard boundary: this
skill GENERATES only.** No move is executed here — `rename-execute`, `/overhaul-execute`
(which drives the whole campaign, composing `rename-execute` and `build-lead` per approved
wave), and the human's own ratify/merge own execution, always in a later, separate step.

## Phase 0 — Measure first, never re-derive

Compose the existing instruments; do not reimplement any of them.

1. `authorkit:naming-audit` and `authorkit:bloat-audit` (this plugin — invoke via the Skill
   tool; both are always installed alongside this skill). `bloat-audit`'s `measure.py` output
   is also the evidence for Phase 1's two new columns: per-member body `chars` and
   `flags` (`long-body` past 6000, `dense-description` past 700) feed the knowledge-tier
   answer; `duplicates`/`duplicate_pairs` (Jaccard ≥ 0.5 near-duplicate paragraphs across
   files) feed the merge/split-candidate answer.
2. `harness:check-routing` and `harness:plan-plugin-split` (`surface_map.py check`'s
   dependency closure) — soft mentions: invoke via the Skill tool where harness is installed;
   where it is not, state plainly in the emitted doc that dependency-closure evidence is
   unavailable and the affected members' blast-radius rows are unverified, never guessed.
   `check-routing`'s *stolen*/*leaked* counts between siblings are the other merge/split
   evidence source — a steal is one corpus serving two audiences read the other way round.

The plan builds from these numbers. A target with no naming.manifest.json or no prior audit
still gets a plan, but Phase 1's kill-switch table cites "no baseline measured" per member
rather than inventing a verdict.

## Phase 1 — One design doc, per-member KILL-SWITCH

One doc, five questions per member — and the analysis is ALLOWED TO SAY NO (#197's
precedent: 7 of 8 proposed moves were killed at this phase; the same veto now covers the two
new questions — evidence can kill a merge/split nomination or a knowledge-tier verdict
exactly like it kills a move):

1. **Where it lives** — `harness:plan-plugin-split`'s job-evidence/anti-matrix method (an
   absence is a gap only with job evidence; two members owning one procedure is a surplus
   defect, the general subsumes the narrow).
2. **What species it is** — the invoker decides, per `naming-conventions`' taxonomy:
   user-typed → command, model-routed → skill, needs-own-context → agent; dual access →
   skill + thin command wrapper (this skill's own shape).
3. **Blast radius** — `rename-planning`'s enumeration method: every invocation string,
   relation edge, wrapper, hook, and workflow config the move would touch.
4. **Merge/split candidate?** — read against Phase 0's evidence: `bloat-audit` near-duplicate
   pairs between this member and a sibling, `check-routing` steals/leaks (one corpus serving
   two audiences, read the other way), or a member `naming-audit`/Phase-0 already flagged as
   too thin to stand alone. A hit **names the candidate set** (this member + its sibling(s))
   and the owning harness instrument — `harness:plan-skill-merge` for a roll-up, or
   `harness:plan-skill-split` for a break-up, both soft mentions, both executed later only via
   `/reshape-skill`. This skill **nominates, never re-derives**: it never runs
   `plan-skill-merge`'s inverse tests or `plan-skill-split`'s four tests itself — naming the
   candidate set and citing the Phase-0 evidence is the whole job. No evidence, or the evidence
   doesn't clear either instrument's own bar → `NO — <reason>`, same discipline as a killed
   move.
5. **Procedure or knowledge, and what tier?** — classify per `harness:pack-writing-rules`'
   own test (changes behavior → PROCEDURE; informs it, corpus-shaped, retrieval wants it split
   → KNOWLEDGE), a soft mention. A PROCEDURE member is always `keep-inline` — behavior-changing
   steps run from the body every trigger, so no other tier applies. A KNOWLEDGE member gets a
   context-optimization tier from `bloat-audit`'s own measured numbers, never a vibe. **[drift-
   prone]** the specific numbers below mirror two owned-elsewhere constants —
   `authorkit:bloat-audit`'s `scripts/measure.py` (`LONG_BODY_CHARS`, the dense-description
   char cap, `DUPLICATE_JACCARD`) and `harness:pack-writing-rules`' axis/file/INDEX-line
   budgets — re-read those owners' current values before trusting this mirror at plan time; a
   threshold change on either side does not auto-propagate here:
   - **keep-inline** — the SKILL.md body trips neither `bloat-audit` flag (`long-body`
     ≤6000 chars, `dense-description` ≤700 chars) — current cost already clears bloat-audit's
     own bar, whether the content sits in the body or in a references/ folder already sized to
     match. (A thin corpus below `pack-writing-rules`' 3-axis floor is a **merge/split**
     signal, question 4's job, not a knowledge-tier concern — don't double-count it here.)
   - **move-to-references/** — trips `long-body` (>6000 chars) or `dense-description`
     (>700 chars), or shows up in a `duplicates` pair (Jaccard ≥ 0.5, restated instead of
     centralized) — but the resulting corpus still fits `pack-writing-rules`' healthy
     single-pack range (≤7 axes/files, the flat-table enumerability ceiling): push the
     overflow into a (new or existing) `references/` file; the consult table alone still
     works as the retrieval map, no INDEX earned yet.
   - **extract-to-pack** — axis count or file count (existing `references/`, or the count the
     overflowing body implies) would blow past that 7-axis/7-file ceiling, or a projected
     INDEX would exceed `pack-writing-rules`' ~150-line budget — this member has outgrown
     being one skill among siblings and needs its own SKILL.md + INDEX.md + `references/`
     home (`harness:make-pack`, soft mention, executed later, never here).
   - **retire** — `bloat-audit`'s own CALIBRATION.md test finds nothing load-bearing to cut
     (no dated incident, no safety prohibition, no non-default convention survives the cut), or
     the member is a `duplicates` hit at similarity ≥0.5 with no citation of its own — fully
     redundant, not merely miscategorized.
   Cite the specific `bloat-audit` number (chars, flag, or duplicate pair) behind every
   non-`keep-inline` tier — a tier with no cited measurement is a guess, not a verdict.

Render per `references/PLAN-TEMPLATE.md` — the template is the single home for its own
sections (the per-ticket execution contract, the closeout checklist, the five respect
invariants); this skill states only what varies by target, never restates the template's
body. **The doc's type and home:** an LLD (components/interfaces/risks maps directly onto
where-it-lives/species/blast-radius, with the merge/split-candidate and knowledge-tier
answers as two more risk-adjacent columns) — where `docs:make-doc` is installed, invoke it to
author and place the doc under its own LLD contract (gated by `docs:doc-checker`); where
docs is not installed, write the same sections (Phase 0 measurements through the ticket-seed
list, one file, seeds included) to `<target>/overhaul-plan-<YYYY-MM-DD>.md`, no doc-type
frontmatter claimed.

## Phase 2 — Tickets with Blocked-by edges, waved by risk

For every member the design phase did NOT kill: one ticket seed, not yet minted. Order by
wave:

0. **Wave 0 — merge/split nominations** (a nominated candidate set from Phase 1's question 4)
   — one seed per nomination, naming the owning harness instrument as a soft mention
   (`harness:plan-skill-merge` for a roll-up, `harness:plan-skill-split` for a break-up,
   executed later only via `/reshape-skill`). Wave 0 runs before Waves 1–3 because a merge or
   split can change which members even reach a rename/species ticket — a member headed for a
   roll-up doesn't also earn its own Wave-1 seed.
1. **Wave 1 — mechanically-clean moves** (a plain `git mv`, no semantic change).
2. **Wave 2 — species changes** (semantic: critic passes + eval rewrites; never disguised as
   a move). A knowledge-tier verdict of `move-to-references`/`extract-to-pack`/`retire`
   (Phase 1's question 5) folds into this member's Wave 2 seed as its stated reason, rather
   than minting a second, competing seed for the same member.
3. **Wave 3 — contested** (an open design question the doc could not close).

A member that can't move cleanly in any wave → grandfather-with-ratchet (ADR-0011 D8's
pattern: enter the exemptions array verbatim, shrink-only, never forced). Blocked-by edges
between ticket seeds are stated explicitly so wave order is enforceable, not just advisory —
every Wave 1–3 seed for a member also named in a Wave 0 nomination carries a Blocked-by edge
to that nomination's seed.

**Ticket seeds are a list in the plan doc, never minted as Issues at generation time.** This
estate's own discipline is capture, then confirm, then build (`file-feature`/`file-task` capture,
a human confirms, `dispatch-ticket` builds) — auto-minting Issues here would skip the human
confirm gate that ties every other work item to an explicit decision. The seed list is what a
human reviews and approves; each approved row is then minted through its owning intake skill
(`file-feature`/`file-task`) exactly like any other captured idea.

## Phase 3 — Per-ticket execution contract (stated, never run)

`references/PLAN-TEMPLATE.md`'s Phase 3 section is the contract, verbatim, for every ticket
seed: claim → worktree → `git mv` → supersession note/`renames.json` entry → gates + critics
→ PR → human merge → verified close. This skill never runs any of these steps itself.

## Phase 4 — Prove it, after execution (stated, never run)

`references/PLAN-TEMPLATE.md`'s Phase 4 checklist names the closeout a human/builder runs per
wave once tickets land (`/check-routing`, a `fix-old-names` sweep, dated supersession notes).
This skill never runs it.

## The five respect invariants

Emit `references/PLAN-TEMPLATE.md`'s invariants section verbatim in every plan doc — the
plan's own contract, not just this skill's.

## Done when

The plan doc exists at its stated home (LLD under `docs:make-doc`, or the dated fallback
path); every member Phase 0 measured has a kill-switch row in Phase 1 answering all five
questions (where-it-lives, species, blast-radius, merge/split-candidate, procedure-or-knowledge
+ tier); every member not killed there has exactly one ticket seed in Phase 2, in the right
wave, with its Blocked-by edges stated; and every merge/split nomination that survived Phase
1's veto has a Wave 0 seed naming its owning harness instrument. Short of all four, the run is
incomplete — report what's missing rather than a silent partial doc.

## References

| File | Read when |
|---|---|
| PLAN-TEMPLATE.md | rendering the phased overhaul plan doc — sections, the kill-switch table, the waved ticket-seed list |
