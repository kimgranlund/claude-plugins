# Audit report — plugin-install-facts (FLOOR, fresh-context, 2026-07-25)

**Verdict: PASS WITH FIXES — 0 blocking · 2 major · 3 minor.** The pack surface is
structurally complete (all five pack sub-species elements present, lint clean, corpus_check
skip sanctioned, reciprocal fences closed in adopt-plugin and plugin-writing-rules suites),
but the lifecycle axis is unrouted in the eval suite and shares an unfenced boundary with
plugin-writing-rules' "why an update isn't picked up" claim. Both majors are same-change
fixable before ship.

Auditor: skill-audit (generator ≠ critic). Standards: skill-writing-rules (incl. the
knowledge-pack sub-species surface rules) + pack-writing-rules, as installed (harness 2.0.11).
Mechanical baseline: `skill_lint.py` clean (exit 0); `corpus_check.py` reports "not a pack (no
INDEX.md)" — the sanctioned ≤7-file flat-corpus skip (2026-07-09 ruling); description 653
chars (under the 1,024 open-standard cap and the 1,536 listing cap).

## Major

### M1 — Update-ask boundary with plugin-writing-rules is unfenced on both sides

- `SKILL.md:6` claims "trust/scope/update facts"; the consult table row `SKILL.md:40` claims
  "update/autoUpdate, **why an update didn't arrive**".
- `plugin-writing-rules/SKILL.md:5` already claims "**why an update isn't picked up**" — a
  near-verbatim identical ask, on the routing surface of a sibling in the same plugin.
- Neither description fences the other; neither eval suite carries a case on either side of
  this ask (the new suite's only "update" hits are the suite note and n07;
  plugin-writing-rules' suite gained only the "all the ways a plugin can be installed" fence).
- Supporting drift pair: `references/install-lifecycle.md:32-36` restates plugin-writing-rules'
  version-cache-key rule and `install-lifecycle.md:27-28` restates its trust-recurs rule
  (cf. `plugin-writing-rules/SKILL.md:30,60,79`) — cited, but restated rather than pointed at
  (skill-writing-rules body rule 8: reference, never restate).
- Fix: decide the owner of the *user-side* "why didn't the update arrive" ask (this pack's
  lifecycle file is the natural home for the user-side symptom; plugin-writing-rules keeps the
  author-side "my shipped change isn't reaching users"), add the reciprocal fence to whichever
  description loses the ask, add one trigger + one no-trigger case across the two suites, and
  thin `install-lifecycle.md:27-36` to point at plugin-writing-rules for the rule's canonical
  statement while keeping only the user-side diagnostic framing.

### M2 — The lifecycle axis is unrouted: zero eval cases exercise install-lifecycle.md

- The consult table registers three axes (`SKILL.md:38-40`), but all 13 trigger cases in
  `evals/evals.json` land on the commands axis (t01-t08, t11-t12), the choice axis (t10), or
  the README consumer (t07, t09). No case asks about the trust prompt, install scope,
  autoUpdate, uninstall/disable, or an update that never arrived — the entire
  `references/install-lifecycle.md` territory.
- pack-writing-rules, Research waves step 4: the eval suite gains the new axis's trigger
  phrasings in the same change — "an unrouted axis is invisible." `intent.md:55` records
  "eval suite carries the ratified phrasings", but the 21 cases predate the corpus (authored
  evals-first in Phase 2) and were never extended when wave 1 landed the lifecycle axis.
- Compounding: the description's only lifecycle vocabulary is the terse "trust/scope/update
  facts" tail (`SKILL.md:6`) — feature nouns, no symptom phrasing — so lifecycle asks will
  plausibly leak to plugin-writing-rules (see M1) or adopt-plugin.
- Fix: add 2-3 lifecycle trigger cases (e.g. "why didn't my plugin update arrive after the
  author shipped a fix", "how do I uninstall a plugin without losing its data", "what does the
  trust prompt on plugin install mean") and one symptom phrase to the description tail; rerun
  `/check-routing harness` at the wave boundary.

## Minor

### m3 — Worked example unlabeled (normative/illustrative)

`SKILL.md:49-56`: the knowledge-species rule requires every example marked **normative** or
**illustrative**; the answer-contract example carries neither label. It is meant as the
contract's normative instance — label it so.

### m4 — `[verified absence]` is an undeclared fifth grounding class

`references/install-commands.md:47,85` and `references/channel-choice.md:32` use
`[verified absence]`; pack-writing-rules sanctions exactly four classes ([verified],
[inferred], [drift-prone], [incident]). The marker is well-formed (dated, sourced) and the
absence-as-fact idea is genuinely useful — but an unsanctioned class is invisible to any
tooling keyed on the four. Either normalize to `[verified]` with "absence" in the prose, or
amend pack-writing-rules to admit the class (the standard's own amendment discipline).

### m5 — Corpus-of-record path deviates from the standard's named location

`SKILL.md:64-68` places the routing corpus at `evals/evals.json` where skill-writing-rules'
pack sub-species rule names `scripts/routing-corpus.json`. The deviation is house-wide (every
suite in this workspace lives at `evals/evals.json`, and the SKILL.md says so in place), so
this is a standards-reconciliation note, not a defect in this skill: skill-writing-rules
should either bless the house path or the estate should converge — tracked best as a
follow-up against skill-writing-rules, not a change here.

## Verified clean (for the record)

- All five pack sub-species surface elements present: answers-only boundary with named peers
  (`SKILL.md:23-29`, no phantom boundary — adopt-plugin / ship-plugin / make-plugin /
  plugin-writing-rules all named), Grep-first consult discipline (`SKILL.md:33-34`), deviation
  doctrine with rationale (`SKILL.md:58-62`), corpus-of-record (`SKILL.md:64-68`), answer
  contract + one worked example (`SKILL.md:42-56`).
- Species story consistent three ways: knowledge content, both dials explicit
  (`SKILL.md:12-13`, model-only), `facts` noun head per naming-rules/W5.
- Description: third person, what+when, verbatim user phrasings front-loaded, three parseable
  NOT-fences with owners; 653 chars.
- Reciprocal fences closed in sibling suites in the same change: adopt-plugin evals gained
  "how do I install this plugin" and "write the install section" no-triggers (fence-closed
  2026-07-25); plugin-writing-rules gained "all the ways a plugin can be installed".
- Corpus: 3 ask-shaped files, each opening with the question it answers; grounding markers
  throughout incl. 2 [incident] with dates and 1 [inferred] naming its derivation; consult
  table ↔ tree 1:1 (3/3); file sizes 34-87 lines, far under load budgets.
- Body: 68 lines, contracts in the head, one lowercase hard gate ("never emit an install
  command absent from references/"), zero uppercase NEVER spend, spec-present tense
  throughout, no one-time-step phrasing, no hardcoded machine paths.
- `intent.md` at skill top level matches the estate's forge convention (adopt-plugin,
  checking-rules, find-open-questions, naming-rules all carry one).
