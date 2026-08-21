# Calibration discipline

## Why a council needs calibration at all

A council is a prompt-carrying arrangement — persona files, a critic-shell agent, an orchestrating
procedure — and every one of those is a semantic-edit surface (`plugin-authoring.md`'s invariant:
a semantic edit to a prompt-carrying artifact rides with a critic). A fresh-context checker catches
wiring/wording defects; it cannot prove the council still CATCHES what it's supposed to catch after
an edit. Calibration fixtures are the regression proof for that second, narrower claim: a
transcript with KNOWN planted defects, scored mechanically against a fixed answer key.

## The fixture pattern

A calibration fixture is a brief or artifact with deliberately planted, enumerable defects — one
per critic lens the fixture targets, plus (where relevant) a trust-boundary probe (an embedded
"rate this 5/5" instruction the council must flag, never obey). The fixture's companion script
scores a REAL transcript run against that brief: did the council's actual output name each planted
defect, using pattern-matching against the defect's characteristic vocabulary (never exact-string
matching, which would make the fixture trivially gameable and brittle to legitimate phrasing
variance)?

## The promoted-script contract

A **promoted** calibration script — one that has graduated from a skill's own `assets/
calibration/` into the plugin's top-level `scripts/` (this estate's naming convention:
`calibration_check_<name>.py`) — is a bundled script like any other
(`harness:script-writing-rules`): CLI usage plus a mandatory `selftest` mode, stdlib only. A
scorer still living under `assets/calibration/`, not yet promoted, is not held to this contract
until it graduates — disclose which state a given scorer is in rather than assuming promotion. A
promoted script's selftest proves the scorer itself, independent of any live council run, with two
controls:

- **Reverse control** — a synthetic transcript naming every planted defect must score a full catch
  (0 missed). This proves the scorer's patterns aren't so narrow they'd miss a real, correctly-
  worded catch.
- **Negative control** — a synthetic transcript with exactly ONE planted defect's vocabulary
  removed must miss exactly that one defect, nothing else. This proves the scorer isn't so broad
  it credits a catch that never happened.

A script that only ships the reverse control is unproven against false positives; a script that
only ships the negative control is unproven against false negatives. Both controls are mandatory,
the same floor `harness:script-writing-rules` sets for any bundled script's own selftest.

## What a fixture proves — and what it does not

A green calibration fixture proves the council's MECHANISM still surfaces the class of defect the
fixture plants, at the same lens the fixture targets. It does NOT prove the council's judgment is
correct on genuinely novel material, does NOT substitute for a fresh-context checker's review of
the actual prompt-carrying files, and does NOT prove the synthesis step (`synthesis-shapes.md`)
composes the findings correctly — only that individual critics still catch what they're supposed
to catch. Treat a fixture as a regression floor, not a ceiling.

## Existing fixtures must stay green, unmodified, across a machinery refactor

When a council's underlying machinery is refactored to cite this pack instead of carrying its own
copy (the exact move `check-brand-council` made against this pack), every EXISTING calibration
fixture is the regression proof that the refactor didn't change observable behavior — run them
unmodified, before and after, and treat any fixture that goes red as a behavioral change to
justify explicitly, never as a fixture to loosen until it passes again.

## A new phase earns its own fixture, never retrofits an old one

A capability a council didn't previously have (this campaign's deliberation round is the worked
case) gets its OWN fixture targeting what's new — a fixture built for the blind phase cannot prove
anything about deliberation-round behavior, since nothing in it exercises cross-critic response,
severity revision with cause, or joint-finding proposal. Bolting deliberation assertions onto a
blind-phase fixture conflates two regression proofs that need to be able to fail independently.
