# Calibration worked example — step 6

A worked, disclosed-as-fixture example of minting one new critic's calibration case, per
`council-rules`' `references/calibration-discipline.md` applied at single-persona granularity. This
is a demonstration of the PATTERN `make-critic` step 6 asks for — not a live, roster-registered
critic in `check-brand-council` (minting a permanent 15th critic there is outside this procedure's
own scope; `check-brand-council`'s live roster is untouched by this file).

## Worked example — a hypothetical "accessibility-first" critic

Suppose a new critic, `critic-devi-r`, is minted for `check-brand-council`'s `design` sub-council,
with a lens on accessibility as a design-integrity question (not a compliance checklist item) —
distinct ground from Paula S. (scale/liquidity), Massimo V. (timelessness), Matt W. (editorial
type), and Jessica W. (the weird over the safe brief).

**Fixture — a real, bundled file** (`${CLAUDE_PLUGIN_ROOT}/skills/make-critic/assets/calibration/fixtures/demo-accessibility-gap.md`,
unpromoted — markdown only, scored by inspection): a short brief planting exactly one defect —
a low-contrast primary palette pairing plus a "solve later" deferral line.

**Expected catch (characteristic vocabulary, not exact-string):** the critic should name the low-
contrast pairing as a design-integrity failure — not a deferred technical detail — and should flag
the "solve later" framing as the actual defect (accessibility treated as a bolt-on rather than a
constraint the identity system itself must satisfy).

**Scoring approach:** pattern-match the returned findings for contrast/legibility vocabulary tied
to the palette pairing, AND a named objection to the "later"/deferral framing — a fixture that only
plants the color pairing without the deferral line would not distinguish this critic's lens
(design-integrity) from a plain WCAG contrast-checker script, which is not what a council seat is
for.

## What promotion would look like (not done here)

Per `calibration-discipline.md`'s promoted-script contract, this fixture stays **unpromoted** —
disclosed as markdown-only, scored by inspection rather than a `calibration_check_<name>.py`. It
would earn promotion (a stdlib CLI script with a `selftest`, reverse control + negative control)
only once it has actually run a handful of times against real critic output — promoting a fixture
that has never been exercised live would ship an unproven scorer, the exact hazard
`script-writing-rules`' selftest floor exists to catch.
