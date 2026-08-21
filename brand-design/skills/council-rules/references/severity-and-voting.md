# Severity taxonomy & 2-of-3 contested voting

## The four-tier taxonomy

| Tier | Criteria |
|---|---|
| Critical | Fails the domain's own coherence/authority standard — unfit to ship as-is. |
| Major | A significant gap that will compound over time (drift, a shallow foundation). |
| Minor | Suboptimal but not load-bearing. |
| Noise | True but not actionable now. |

This exact four-tier shape is the machinery; the CRITERIA prose for what counts as "coherence" or
"a shallow foundation" is domain-specific and lives in that instance's own critic-shell agent
(brand's is `agents/brand-judge`), cited by every persona file rather than each persona restating
its own copy. A council instance never invents a fifth tier or renames one — the taxonomy is what
lets findings from different critics, and across blind and deliberation phases, compare at all.

**A panel returning only Minor/Noise findings across the board is a calibration signal, not a
clean bill of health by default** — it means either the work is genuinely excellent, or the
council isn't being adversarial enough. Push for real findings, or state explicitly why the work
meets the standard it's being held to. `calibration-discipline.md`'s planted-defect fixtures exist
specifically to catch a council that has drifted toward the second case while reading as the
first.

## 2-of-3 contested-finding voting

**Eligibility.** A row seated with `role: advisor` (the reserved `advisory` sub-council,
`roster-file-contract.md`) is never eligible here — not as the contested finding being resolved,
and not as one of the three verdicts cast to resolve a peer's. Advisory informs a council's
synthesis; it carries no adversarial vote weight (cited from the roster contract, not restated).

When two critics in the SAME sub-council return genuinely conflicting severity for the SAME cited
finding — the same quoted excerpt or claim, scored at materially different severity tiers, not a
stance-level disagreement (that's `synthesis-shapes.md`'s productive tension, never resolved by a
vote) — dispatch ONE more unnamed critic call: a third persona from the same sub-council with
bearing on that specific point, scoped to just the one contested finding, with the same
artifact/context. That's three independent severity verdicts on the one finding:

- **Majority (2-of-3)** becomes that finding's recorded severity for synthesis.
- **All three differ** (no majority) → log the finding as **hung**: report it exactly as such,
  never resolved by fiat. A hung vote is evidence the finding itself is genuinely ambiguous — the
  same shape `harness:check-routing`'s own contested-case voting round takes, cited here as the
  precedent this convention mirrors rather than a coincidence.

This resolves the SEVERITY score only. It never erases or overrides a genuine stance-level
disagreement between critics — that disagreement is still reported, verbatim, as productive
tension; 2-of-3 voting and productive tension are answering two different questions (how severe
vs. what does the disagreement itself reveal) and neither substitutes for the other.

## Scope of the vote

The tie-break dispatch is scoped as narrowly as possible: one finding, not the whole artifact —
re-running a full critic pass to settle one contested severity wastes the third critic's read on
everything they'd agree with the first two about anyway, and risks introducing a fresh contested
finding the vote wasn't meant to adjudicate.
