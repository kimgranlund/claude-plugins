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
