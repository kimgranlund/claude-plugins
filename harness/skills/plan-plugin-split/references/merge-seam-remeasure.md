# Merge-seam re-measure — proving routing parity after plugins merge into one menu

When a merge verdict executes, every member skill that used to live behind its own plugin's
description menu now competes in one union menu. That union creates a failure class the source
plugins' green baselines cannot predict, and this file carries the measured method for closing it.
Worked instance throughout: the ADR-0008 design merge (design-kits + color + typography → `design`,
22 skills, PR #73, 2026-07-21) — three blind-judge rounds, 515-case baseline 508/515 (98.6%) →
union raw 488/515 (94.8%) → healed 515/524 (98.3%).

## The seam mechanism: grammar-bare prompts relied on menu scope

An eval prompt like "what type token for this heading" routed correctly inside its source plugin
because the menu itself disambiguated — the only type-token skill visible was the right one. In
the union menu, two skills legitimately claim the same bare phrasing (Material's
`--md-sys-typescale-*` guide vs the default `--type-*` grammar), and BOTH descriptions are
correctly fenced by token grammar. The prompts, not the descriptions, are the defect: in a real
session the project's ambient grammar disambiguates, but a blind judge has no ambient context.
ADR-0008 Decision 5 names the rule: **cross-former-plugin steals after a merge are NEW seams to
fence, not regressions against the source baselines.** (The material-type-facts suite went 11/19
raw — eight steals by typography's skills — and 20/20 after healing, with zero description-boundary
changes.)

## The three healing instruments, in order

1. **Ordered context split** (the primary fix): the suite prompt gains the disambiguating marker a
   real session's ambient context would supply — "what md-sys type token for this heading",
   "should this table cell text be the --type-ui voice or the code voice". ADR-0008 applied 22
   splits across three rounds; every split case passed all subsequent rounds. A split is honest
   exactly because the marker restores information the plugin-scoped menu used to carry — it is
   not watering down the eval.
2. **Thief-side description fence carrying the stolen verbatim**: the winning skill gains a
   `NOT for <stolen phrasing> (<owner>)` clause — e.g. make-stitch-kit (whose description mentions
   "-dark siblings") gained the missing design-md-rules fence after stealing a DESIGN.md format
   question.
3. **Reciprocal no-trigger case in the thief's suite**: the fence is closed suite-side so the next
   `/check-routing` run re-proves it (9 added in ADR-0008).

## Noise calibration: when NOT to heal

Single-judge scoring carries ~1.5% noise per round (ADR-0008 measured 7–10 randomly-placed misses
per ~520-case round; near-identical prompts flipped within one judge's own batch — "what padding
for this card" passed at q402 and failed at q413, same round, same judge). Two disciplines follow,
extending the "never tune to chase" ruling recorded at the color-plugin baseline:

- **A fail that passes 2 of 3 rounds is noise** — record it, never chase it with wording edits.
  Three ADR-0008 suites ended one case "below floor" on exactly such flips and shipped anyway,
  with the flips named in the PR evidence comment.
- **A fail that persists 3 of 3 rounds with a verbatim fence already in place is
  known-ambiguous** — the fence is saturated; annotate the case in the suite (`note:` field) and
  stop. ADR-0008's instance: material-token-facts n07, a glossary-claim false-positive that
  survived two rounds of fence sharpening including the exact phrase.

Compare per-suite **fail counts**, not raw pass numbers, wherever healing moved cases between
suites or added reciprocals — denominators shift, and "24/25 vs a 27/28 floor" is parity, not a
three-point regression.

## The run mechanics (what a re-measure round is)

The base procedure is `check-routing`'s (Phases 2–4: menu from live descriptions,
expectation-stripped shuffled prompts, blind no-tools judges) — consult it there, including its
answer-count clause; this file adds only the merge deltas: the menu is the merged plugin's UNION;
all suites' cases pool into one fixed-seed shuffle split across ~5 judges; scoring floors are the
SOURCE plugins' measured baselines; and one FULL round per heal wave — description edits change
the menu every suite sees, so partial re-runs are not parity evidence. Full trail: PR #73's
parity comment and the design plugin's v1.0.0 ledger line.
