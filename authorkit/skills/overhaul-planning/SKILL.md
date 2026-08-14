---
name: overhaul-planning
kind: skill
description: >
  Generate a phased estate-overhaul plan for a target (estate, plugin set, or member list):
  measure first (existing audits), one design doc with a per-member kill-switch (can return
  "no move"), then waved ticket seeds with Blocked-by edges. Use for planning a rename/reshape
  campaign across many members, "what would it take to overhaul this estate", or repeating
  the #197 campaign's method. Plan-only: writes the doc and seed list, never executes. NOT for
  one artifact's rename (rename-planning); NOT a plain audit (naming-audit, bloat-audit); NOT
  executing an approved plan (rename-execute, build-lead).
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
skill GENERATES only.** No move is executed here — `rename-execute`, `build-lead`, and the
human's own ratify/merge own execution, always in a later, separate step.

## Phase 0 — Measure first, never re-derive

Compose the existing instruments; do not reimplement any of them.

1. `authorkit:naming-audit` and `authorkit:bloat-audit` (this plugin — invoke via the Skill
   tool; both are always installed alongside this skill).
2. `harness:check-routing` and `harness:plan-plugin-split` (`surface_map.py check`'s
   dependency closure) — soft mentions: invoke via the Skill tool where harness is installed;
   where it is not, state plainly in the emitted doc that dependency-closure evidence is
   unavailable and the affected members' blast-radius rows are unverified, never guessed.

The plan builds from these numbers. A target with no naming.manifest.json or no prior audit
still gets a plan, but Phase 1's kill-switch table cites "no baseline measured" per member
rather than inventing a verdict.

## Phase 1 — One design doc, per-member KILL-SWITCH

One doc, three questions per member — and the analysis is ALLOWED TO SAY NO (#197's
precedent: 7 of 8 proposed moves were killed at this phase):

1. **Where it lives** — `harness:plan-plugin-split`'s job-evidence/anti-matrix method (an
   absence is a gap only with job evidence; two members owning one procedure is a surplus
   defect, the general subsumes the narrow).
2. **What species it is** — the invoker decides, per `naming-conventions`' taxonomy:
   user-typed → command, model-routed → skill, needs-own-context → agent; dual access →
   skill + thin command wrapper (this skill's own shape).
3. **Blast radius** — `rename-planning`'s enumeration method: every invocation string,
   relation edge, wrapper, hook, and workflow config the move would touch.

Render per `references/PLAN-TEMPLATE.md` — the template is the single home for its own
sections (the per-ticket execution contract, the closeout checklist, the five respect
invariants); this skill states only what varies by target, never restates the template's
body. **The doc's type and home:** an LLD (components/interfaces/risks maps directly onto
where-it-lives/species/blast-radius) — where `docs:make-doc` is installed, invoke it to
author and place the doc under its own LLD contract (gated by `docs:doc-checker`); where
docs is not installed, write the same sections (Phase 0 measurements through the ticket-seed
list, one file, seeds included) to `<target>/overhaul-plan-<YYYY-MM-DD>.md`, no doc-type
frontmatter claimed.

## Phase 2 — Tickets with Blocked-by edges, waved by risk

For every member the design phase did NOT kill: one ticket seed, not yet minted. Order by
wave:

1. **Wave 1 — mechanically-clean moves** (a plain `git mv`, no semantic change).
2. **Wave 2 — species changes** (semantic: critic passes + eval rewrites; never disguised as
   a move).
3. **Wave 3 — contested** (an open design question the doc could not close).

A member that can't move cleanly in any wave → grandfather-with-ratchet (ADR-0011 D8's
pattern: enter the exemptions array verbatim, shrink-only, never forced). Blocked-by edges
between ticket seeds are stated explicitly so wave order is enforceable, not just advisory.

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
path); every member Phase 0 measured has a kill-switch row in Phase 1; and every member not
killed there has exactly one ticket seed in Phase 2, in the right wave, with its Blocked-by
edges stated. Short of all three, the run is incomplete — report what's missing rather than
a silent partial doc.

## References

| File | Read when |
|---|---|
| PLAN-TEMPLATE.md | rendering the phased overhaul plan doc — sections, the kill-switch table, the waved ticket-seed list |
