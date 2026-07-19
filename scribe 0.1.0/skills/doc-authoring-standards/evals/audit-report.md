# Audit — doc-authoring-standards after ADR-0003 (backend-resolver.md + linear-adapter.md)

Date: 2026-07-18 · Auditor: fresh-context skill audit (post-ADR-0003 edit)
Scope: `SKILL.md` (rewritten delegation bullet + new "Work-item backend delegation" section),
`references/backend-resolver.md`, `references/linear-adapter.md`, checked against
`.claude/docs/adr/0003-backend-generalization.md` and `.claude/docs/spec/spec-linear-adapter.md`.

## Verdict

🟢 **SHIP — yes, this reference-file pair is ready as scribe's authoritative ADR-0003
realization.** Zero blocking findings. All nine REQs have concrete realizations across the two
reference files; all nine ACs are satisfiable from what's documented. Mechanical lint clean
(`skill_lint.py` on SKILL.md), no dangling pointers, no phantom `[[handles]]`. Four minor,
non-blocking observations below.

## Resolution (2026-07-18, same session)

This audit ran alongside three sibling audits (bug-report/feature/issue) that independently
converged on a real gap: AC-004/AC-007 already required "read back through the adapter" but no
REQ named that operation. Fixed at the root — `spec-linear-adapter` amended to v0.2.0 with
REQ-010/AC-010 (a sixth `read` operation), and both reference files updated from a five- to a
six-operation interface accordingly (this SKILL.md's own delegation section text updated in the
same change). Of this audit's four minor notes: (b) the "Which type?" placement was moved back
next to the type contract table. (a) ADR-0003 Decision 1's four-operation wording is left
as-is — the ADR is `status: accepted` (ledger class, append-only); Decision 3 three lines later
already carries the accurate five-op (now conceptually six-op) list, so no reader is misled; a
dated amendment note is the correct mechanism if this is ever revisited, not an in-place edit.
(c)/(d) left as observed, non-blocking. `release_gate.py "scribe 0.1.0"` re-run clean after all
fixes.

## REQ-level conformance matrix (spec-linear-adapter 0.1.0)

| REQ | Realized where | Status |
|---|---|---|
| REQ-001 interface conformance | backend-resolver.md §"The five-operation adapter interface" (cites REQ-001 by name); linear-adapter.md §"The five operations" realizes all five | 🟢 |
| REQ-002 transport preference | linear-adapter.md §"Transport resolution (REQ-002)" — MCP preferred, GraphQL fallback, resolved at call time, `[verified]` grounding for both endpoints | 🟢 |
| REQ-003 configuration capture | linear-adapter.md §"Configuration (REQ-003)" + backend-resolver.md §"The ruling shape" (captured once, persisted in the entry-file row, never re-prompted) | 🟢 |
| REQ-004 payload fidelity | linear-adapter.md §"Payload-contract mapping (REQ-004)" — full element→field table incl. Findings-as-comments; "no section dropped or silently merged" restated verbatim | 🟢 |
| REQ-005 dedup search | linear-adapter.md §dedup-search bullet ("sweep before minting… a match updates that issue's fields instead of minting a duplicate") | 🟢 |
| REQ-006 findings-first close | linear-adapter.md §close bullet — Findings comment posted **before** the state transition; backend-resolver.md close row carries the same guarantee for A/B | 🟢 |
| REQ-007 status mapping | linear-adapter.md §"Status mapping (REQ-007)" — status→state-*type*→configured-state binding, read-back covering rule identical to the SPEC's (started→doing, completed→done, canceled→wontfix, else→open) | 🟢 |
| REQ-008 failure fallback | Both files carry a §"Failure fallback (REQ-008)" — per-operation fall-back-to-file + reported in close-out | 🟢 |
| REQ-009 discovery | Both files: discover as a distinct fifth operation with checkpoint + pagination contract, explicitly distinguished from dedup-search ("matches one candidate, not everything since X") | 🟢 |

**AC satisfiability:** AC-001…AC-009 each map onto documented behavior; AC-002, AC-004, AC-007,
and AC-008 are cited by ID inside linear-adapter.md at exactly the behavior that satisfies them.
Nothing documented contradicts any AC. (AC-009's boundary nuance: see observation 3.)

## The four requested checks

1. **Interface-table consistency (backend-resolver ↔ linear-adapter):** 🟢 consistent. Same five
   operation names in the same order (create · dedup-search · update · close · discover), same
   semantics — close is Findings-first in both; discover is checkpoint-driven and distinct from
   dedup-search in both; linear-adapter's "close is an `issueUpdate` state transition, Linear has
   no separate close mutation" is a realization detail, not a contract deviation.
2. **SKILL.md bullet ↔ new section ↔ references:** 🟢 no drift. The rewritten bullet (three-way
   choice, ruled 2026-07-17 ADR-0003 superseding the 2026-07-15 binary, Linear as scribe's own
   Option-C adapter, never-delegated tiers unchanged) matches the new "## Work-item backend
   delegation (ADR-0003)" section, which matches both references (shared resolver closing the
   three-way duplication; five operations named identically; "this skill owns the interface, not
   every implementation" matches backend-resolver's bring-your-own clause). The git diff confirms
   the frontmatter description was untouched, so no evals.json update was owed (the invariant
   fires on routing-surface edits only) — and indeed evals.json is unchanged.
3. **The triage/duplicate disclosure:** 🟢 reads as honest grounding, not hedging. It follows the
   `[verified]`/`[drift-prone]`/`[inferred]` convention (declared up top with a
   pack-authoring-standards attribution), names both first-party pages' enumerations concretely,
   states what IS confirmed (triage is real but opt-in per team) vs. what isn't (duplicate as a
   true type vs. a named state under `canceled`, with Linear's own worked example as the
   plausibility argument), and — decisively — gives the resolution mechanism: query the team's
   actual `workflowState.type` values at Configuration time, never trust the enumeration as
   exhaustive. The four statuses the adapter actually writes are fully grounded either way, so the
   discrepancy is contained to the tail it discloses. This is the disclose-don't-assert pattern
   done right.
4. **Dangling references / lint:** 🟢 clean. `skill_lint.py` clean on SKILL.md. Both SKILL.md
   pointers resolve to existing files. `spec-linear-adapter.md` and
   `spec-ticketing-watch-triage.md` both exist at `.claude/docs/spec/`. Cross-plugin mentions
   (`pack-authoring-standards`, `doc_lint.py`) are soft named mentions, per the boundary rule. No
   phantom `[[handle]]`s.

## Minor observations (non-blocking, none require changes to ship)

1. **ADR-0003 Decision 1's operation list is a four-op remnant** ("create, dedup-search, update,
   close") while Decision 3, the SPEC, and both references consistently say five (discover was
   added by the v3 replan the Context itself narrates). This is an ADR-side wording artifact, not
   a reference-file defect — the ADR is accepted/append-only, so if it ever grates, the fix is a
   dated amendment note, never an edit. The references correctly follow the five-op contract.
2. **SKILL.md's "**Which type?**" paragraph now sits under the new "## Work-item backend
   delegation" H2** (the section was inserted between "Feature-shaped tickets" and that
   paragraph). It's a type-routing note that belongs with the type table, not with delegation — a
   one-line move if anyone touches the file again.
3. **linear-adapter.md's discover bullet offers `endCursor` as one checkpoint candidate.** A Relay
   `endCursor` is generally query-scoped, not a durable cross-invocation checkpoint; the "latest
   `updatedAt` seen" alternative in the same sentence is the safe one (and AC-009's
   "second call returns nothing" needs strict-inequality care at the boundary either way). The
   whole bullet is already marked `[inferred]` with a mandatory-introspection instruction, so this
   sits inside the disclosed uncertainty envelope — an implementer following the file's own rules
   will catch it.
4. **backend-resolver.md refers to its sibling as "`references/linear-adapter.md`, this same
   skill"** — the path is skill-rooted, not file-relative. Prose, unambiguous, cosmetic only.

## Checks run

- `python3 "forge 1.14.0/scripts/skill_lint.py" "scribe 0.1.0/skills/doc-authoring-standards/SKILL.md"` → clean
- `git diff HEAD -- …/SKILL.md` → confirms body-only edit (bullet rewrite + new section); frontmatter/description untouched
- Existence checks: both reference files, both SPECs, templates dir, evals.json
- Full read: ADR-0003, spec-linear-adapter, SKILL.md, backend-resolver.md, linear-adapter.md

---

# Audit — doc-authoring-standards after ADR-0004 (Issue Type dual-write section)

Date: 2026-07-18 · Auditor: fresh-context skill audit (post-ADR-0004 edit, worktree
`issue-44-adr-0004-dual-write`)
Scope: the new `## Issue Type dual-write (Option B, ADR-0004)` section (SKILL.md:115–126, the
file's only diff vs HEAD), checked against `.claude/docs/adr/0004-issue-types-for-bug-feature-task.md`,
the three sibling capture skills' Option-B bullets (bug-report:94–99, feature:107–112,
issue:114–119), `forge 1.14.0/agents/ops-issues.md:90–94`, and the updated
`github-issue-pr-primitives/references/bug-task-feature-mapping-nuances.md`.

```
Skill: scribe 0.1.0/skills/doc-authoring-standards · Standards: skill-authoring-standards · Lint: clean
Verdict: PASS
```

🟢 **SHIP.** Zero blocking findings. The section restates ADR-0004's ratified Decision faithfully
and completely at the standards altitude, is word-consistent with all four implementation
siblings, sits in a defensible structural position, and keeps the repo-specific fact OUT of the
general standards file (the right division — see check 4). One minor finding (`kind: task` is
referenced but never defined in this file — a pre-existing gap the new section surfaces), one
date question for the change-set author, three nits.

## The four dispatched checks

1. **ADR-0004 fidelity (Decision + Consequences):** 🟢 complete and accurate. All four ratified
   elements restated: additive dual-write at create time ("in addition to the label… additive,
   not a replacement", SKILL.md:118–119 ↔ ADR Decision 1); label stays system of record
   ("the label stays the system of record, Issue Type is best-effort", :119–120 ↔ ADR Decision 4
   + Consequences); size stays a label with Issue Fields an explicit non-goal (:125–126 ↔ ADR
   Decision 2); never blocks a mint (:124–125 ↔ ADR Decision 4, verbatim discipline). The
   `gh issue create --type <Kind>` mechanism claim — one of the ADR's own named open
   verification items — is verified against the live CLI in this audit (`gh issue create --help`
   shows `--type name · Set the issue type by name`, example literally `gh issue create --type
   Bug`), matching the nuances-file's empirical confirmation (gh 2.96.0). Deliberate,
   correctly-scoped omissions: dedup-search-unchanged (ADR Decision 3) and no-backfill
   (Consequences) are non-changes with no standards surface — the ADR's own Consequence scopes
   this file's change to the create-time line. Do not "fix" their absence.
2. **Sibling consistency:** 🟢 no contradiction. All three capture skills carry the same fallback
   clause ("fallback: retry without `--type` if the org's type schema doesn't resolve — label
   alone still lands, note the skipped type in the close-out"); ops-issues carries the identical
   discipline with "sweep report" in place of "close-out" (correct per its artifact). This
   section's phrasing ("the call retries without `--type`, the label alone still lands, and the
   skipped type is noted in the close-out") is the same rule in standards register. The
   per-kind type names (`Bug`/`Feature`/`Task`) match across all five files.
3. **Structural placement:** 🟢 standalone section is the right call; current position is
   defensible. Folding into "Bug-shaped tickets"/"Feature-shaped tickets" would mint two copies
   of the same kind-agnostic rule (a drift pair) and leave `kind: task` homeless (no task-shaped
   section exists). The rule is backend-specific, not kind-specific, so it earns its own H2;
   adjacency to "Work-item backend delegation (ADR-0003)" groups the backend material, and the
   header's `(Option B, ADR-0004)` parallels the sibling header's `(ADR-0003)`. Nit: it could
   equally sit AFTER the ADR-0003 section (dual-write refines Option B, which that section
   owns), but Option B is already defined upstream at Universal practice 6 (:63–70), so reading
   order is not broken. No move required.
4. **Overclaim / repo-specific drift risk:** 🟢 clean — and the division of facts is exactly
   right. The section states only the platform-general truth ("a personal-account-owned repo…
   has no Issue Types at all; Issue Types is an organization-scoped feature"), dated per the
   estate's grounding convention. The repo-specific consequence ("THIS repo's dual-write will
   always take the label-only fallback path" — kimgranlund/claude-plugins is User-owned) lives
   where it belongs: forge's `bug-task-feature-mapping-nuances.md` update, a dated finding in
   the researched pack, NOT in this general standards file. If GitHub later extends Issue Types
   to user-owned repos, the dated stamp marks the claim's freshness boundary.

## Criteria table

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | pass | — | "never blocks or fails a mint" :124 (deletion → a failed `--type` could abort a mint); "size stays a label… explicit non-goal" :125–126 (deletion → someone migrates size to Issue Fields); "label stays the system of record" :119 (deletion → label removal looks legal) | — |
| R2 trigger fidelity | pass | — | Description untouched (git diff: body-only change) — "what sections a TICKET requires", "which document type", "why a doc failed doc_lint" all still route here; no evals.json owed per the tier ladder | — |
| R3 species/dials | pass | — | knowledge species, `false`/`false` dials, noun name — unchanged, consistent | — |
| R4 register | pass | — | New section is declarative throughout ("also sets", "the call retries", "Never blocks") — knowledge register, no imperatives, no new uppercase gates | — |
| R5 no restatement | pass | minor (obs.) | Fallback clause now exists in 5 copies (this + 3 siblings + ops-issues), word-consistent today; ADR-mandated shape — operational skills need the mechanism inline. This section is the standards-of-record master | Any future change to the fallback discipline owes a 5-file sweep — recorded here as the drift-watch |
| R6 position | pass | — | Section at :115–126 of a 159-line body; contracts ahead of it, references/failure catalog behind | — |
| R7 contracts | N/A | — | knowledge species | — |
| R8 quantities | pass | — | No vague quantifiers in the new section; type names and kind values enumerated exactly | — |

## Findings

1. **[minor] `kind: task` is referenced but never defined in this file.** SKILL.md:117 names
   `kind: bug`/`kind: feature`/`kind: task`, but this file's own TICKET material defines only the
   first two (type-table row :85 "bug reports: `kind: bug`, see below"; "Bug-shaped tickets" :92;
   "Feature-shaped tickets" :104). `kind: task` is the `issue` skill's established convention
   (issue/SKILL.md:9, :111 "`doc-type: ticket, kind: task`", :145) — a pre-existing gap in this
   standards file that the new section now surfaces, not a defect introduced by this edit. Fix is
   half a line, e.g. extend the TICKET row's parenthetical to "(bug reports: `kind: bug`; plain
   tasks: `kind: task` via `issue` — see below)". Sibling-applicability: none — this gap is local
   to doc-authoring-standards.
2. **[nit — verify intent] The section's verification date is 2026-07-19; the audit session's
   context date is 2026-07-18.** The date is uniform across the whole change set (both README
   ledgers say "assembled 2026-07-19", the nuances update is dated 2026-07-19), so it is
   internally consistent and possibly just the author's timezone; but the ADR it implements is
   dated/ratified 2026-07-18. If the 19th is unintended, the sweep is six occurrences across the
   PR (SKILL.md:123, nuances:33, forge README:112, scribe README:47 + any sibling ledger lines),
   not just this file. Flagged to the change-set author; not blocking.
3. **[nit] Two-home platform fact.** The org-scoped/personal-account fact now lives here and in
   forge's `bug-task-feature-mapping-nuances.md` (the researched home). The copy here is one
   clause, degradation-graceful when forge isn't installed — acceptable under the soft-mention
   boundary rule; keep it this size.

## Checks run (this audit)

- `python3 …/skill_lint.py "…/doc-authoring-standards/SKILL.md"` → clean
- `git diff HEAD -- "scribe 0.1.0/skills/doc-authoring-standards/"` → single 13-line section
  insertion, frontmatter/description untouched → no evals.json owed (tier ladder: semantic body
  edit → lint + fresh-context critic, which is this audit)
- `gh issue create --help` → `--type name` flag confirmed live
- Full reads: ADR-0004, SKILL.md; targeted reads: three sibling Option-B bullets,
  ops-issues.md:90–94, nuances-file diff; greps: "Issue Type" estate-wide, "2026-07-19",
  `kind:` in issue/SKILL.md

Top 3: 1) Ship as-is — zero blocking. 2) Half-line fix available for the undefined `kind: task`
(finding 1, this file only). 3) Confirm the 2026-07-19 date is intended (finding 2, change-set-wide
if not).
