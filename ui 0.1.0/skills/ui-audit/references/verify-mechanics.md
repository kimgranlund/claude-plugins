# Verify-family mechanics — the shared discipline of every verifier

Ruled 2026-07-16 (Issue #8; informed by the 2026-07-15 external-skill review — type specimens
millionco/react-doctor@5915a5823, ibelick/ui-skills@ce91b8595, raphaelsalaja/skill@dc9eef22f).
This file is the canon for the verify species — focus-verify, i18n-verify, perf-verify,
safety-verify, ui-change-verify, this sweep, and color's check-colors (cross-plugin: cited
softly, degrades to the mechanics stated inline per consumer). Consumers wire a compact
"Family mechanics" block and cite this file; they do not restate it.

## 1 · Findings carry rule IDs

Every finding — mechanical or judgment — cites its rule: `file:line — [RULE_ID] finding → fix`.
Mechanical findings use the checker's own check name (`POSITIVE_TABINDEX`, `RING_LOW_CONTRAST`);
judgment findings use the verifier's declared judgment slugs (each consumer lists its own, e.g.
`focus.order-vs-task-flow`). An ID makes the finding greppable, comparable across runs, and
waivable at the right grain; a finding with no ID is an opinion with a line number.

## 2 · The scope ladder — match the check to the blast radius

| Scope | Instrument |
|---|---|
| One element / one rule | the owning verifier's checker on a one-entry card |
| One surface / view | the owning verifier, full card |
| One CHANGE (the diff's surfaces) | ui-change-verify — which composes the owning verifiers per affected dimension |
| The whole product / a flow set | ui-audit's sweep |

Running a whole-product sweep to bless a one-line fix wastes the session; blessing a
cross-surface change from a one-element check misses the blast radius. Declare the scope in the
verdict header.

## 3 · Monotonicity — re-verify after fix, never regress

After any fix driven by a finding: re-run the SAME check set at the SAME scope. The bar is
two-sided — the addressed findings are gone, AND no new finding appeared at that scope. A fix
that clears its finding while minting a new one is not done; report both, fix forward. A verdict
issued without the post-fix re-run is a prediction, not a verification.

## 4 · Repair scope is scored, not assumed

The fix a finding drives touches only what the finding names. The re-run's verdict carries a
**blast-radius row**: files/surfaces touched vs files/surfaces the finding named — an unrelated
refactor riding a fix is its own finding (`family.repair-scope`), same severity machinery as the
defect it rode in on. Fix the defect; file the temptation.

## 5 · Waivers — the narrowest control, never the convenient one

When a finding is disputed, descend this ladder and stop at the FIRST rung that fits:

1. **Fix it** — the default; most disputed findings are real.
2. **Per-instance exception, in the card** — the card schema's own exception flags
   (`inline_text`, `spacing_ok`) — documented at the element, checkable forever.
3. **Per-rule project waiver** — one rule ID waived for a named reason, recorded in the
   project's DESIGN.md (`waived: [RULE_ID] — <reason> — <date>`); the checker still runs, the
   verdict marks the finding WAIVED (visible), never deletes it.
4. **Never**: disabling a whole checker, category, or verifier because one finding annoyed —
   the over-broad move that silently drops every future real finding of that class.

Anti-sycophancy clause (the react-doctor specimen's, adopted): when the user asks to silence a
finding, first explain what the rule catches and confirm they understand the trade — many
"noisy" rules are catching real defects. Only then apply the narrowest rung. A verifier that
waives on request without the explanation is laundering its verdict. (This does not breach the
measurement fence below: responding to a USER-initiated dispute is not the verifier asking —
the fence bars verifier-initiated forks and option menus, not answering the user.)

## 6 · Armed mode — bare invocation as standing constraints

A verifier with NO artifact or card in play — none named in the ask, none present in context —
arms itself: its invariants become standing session constraints — every subsequent UI edit this
session is silently held to the verifier's invariants, and violations surface at edit time
instead of at the eventual audit. Armed mode changes when
checks happen, never what passes: the numbers stay the verifier's own. One-shot mode (an
artifact named) is unchanged.

## 7 · Symptom index — route from pain, not vocabulary

Each verifier carries a compact symptom index: the user-observed pain phrase → the rule ID that
owns it ("focus ring disappears on dark cards" → `RING_LOW_CONTRAST`). Users arrive with
symptoms, not SC numbers; the index is the reverse map the detection catalog implies but never
states. Keep it to the 3–6 pains actually observed; an exhaustive index is the catalog again.

## The fence (unchanged, restated as the family's own)

Measurement never asks. No verifier invokes a taste gate, offers an option menu, or asks
mid-measurement — findings are reported; forks belong to the DESIGN-side skill that owns the fix
(layout-decompose's taste-elicitation canon owns that discipline).
