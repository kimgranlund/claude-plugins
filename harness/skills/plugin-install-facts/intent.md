# intent record — plugin-install-facts

Living state for the /make-skill forge. Started 2026-07-25.

## Slots (Phase 1)

- **Trigger (verbatim, from the ask + interview):** "create knowledge skills for appropriate
  install instructions for plugins for ALL the ways plugins can be installed — npx…,
  git@github.com…, local paths, etc"; "how do I install this plugin"; "install instructions";
  "plugin install command"; "install from a local path"; "install via npx / npm"; "write the
  install section for the README"; "how do users install our marketplace".
- **Behavior delta:** BOTH failure classes (user-confirmed): (a) hallucinated install syntax —
  plausible-but-wrong npm-style commands, wrong `/plugin` forms, missing marketplace-add
  precondition; (b) wrong channel choice for the situation — e.g. HTTPS git where this estate's
  ruling is SSH, a marketplace declaration where a local-path dev install fits.
- **Species + dials:** knowledge · `disable-model-invocation: false` · `user-invocable: false`.
- **Freedom:** LOW on command syntax — exact verified forms only, never improvised; MEDIUM on
  channel choice — a decision table maps situation → channel.
- **Type:** capability uplift — drift-prone platform facts that must be verified, not recalled.
- **Consumer:** both (user-confirmed) — in-session "how do I install X" answers AND generating
  the install section that ships in a plugin README.
- **Fences:** NOT for declaring a plugin/marketplace in a repo's settings.json (adopt-plugin);
  NOT for authoring or shipping a plugin (plugin-writing-rules / ship-plugin); NOT for
  settings.json edits with no plugin object (update-config).
- **Done-when:** any install question is answered with the right channel + the exact verified
  command(s), cited to the corpus; README install sections come out copy-pasteable and correct
  per channel; both baseline failure classes demonstrably fixed.

## Decisions

- Name `plugin-install-facts` (user-chosen; `github-facts` precedent — verified-facts pack,
  knowledge noun head). Home: `harness` (owns the plugin domain).
- Shape: ONE skill (user-chosen); revisit via /plan-skill-split only if the corpus outgrows it.
- **Corpus: full /make-pack research wave (user-chosen), one axis — install channels.**
  DELIVERABLE GAP until the wave lands: this forge produces the entry surface only; the
  `references/` corpus is /make-pack's, per the knowledge-species note.
- Campaign shape: worktree `worktree-plugin-install-facts` (ADR-0002), PR is the merge gate.

## Gates

- **P0 PASS 2026-07-25** — primitive = skill: knowledge needed on demand; not mechanically
  checkable (hook), not an every-turn fact (entry file), no tool walls (agent). Ownership gap
  verified: adopt-plugin owns settings.json declaration, plugin-writing-rules owns
  authoring/shipping; neither owns per-channel install instructions.
- **P1 PASS 2026-07-25** — all seven slots filled and user-confirmed via two AskUserQuestion
  rounds (delta=both, consumer=both, shape=one skill, name, corpus depth).
- P2 PASS 2026-07-25 — evals.json clean (13 trigger / 8 no-trigger, lint pass after
  expect-value fix); assertions.md (5); baselines landed and verified non-empty
  (a-github-install 44 ln · b-npx-npm 33 ln · c-readme-section 93 ln).
- P3 PASS 2026-07-25 — SKILL.md drafted (pack sub-species surface: answers-only boundary,
  Grep-first consult table, answer contract + worked example, deviation doctrine,
  corpus-of-record); corpus DELIVERED via make-pack wave 1: charter ratified (9 questions,
  3 files), 2 fact-finder ledgers gathered (all 9 questions covered, dated, marked), distilled
  to install-commands.md · channel-choice.md · install-lifecycle.md, ledgers deleted.
  Registration: consult table ↔ files 1:1 (3/3); eval suite carries the ratified phrasings.
  [Amended 2026-07-25, audit M2: the original claim overstated — Q7/Q8 lifecycle phrasings had
  NOT been added at registration; corrected same-day with t14–t17.]
  corpus_check verdict: "not a pack (no INDEX.md)" = the sanctioned flat-corpus skip
  (≤7 files ship no INDEX, 2026-07-09 ruling).
  make-pack report — plugin-install-facts · wave 1: install-channels · Questions: 9 ratified ·
  Files: 3 written (~210 lines) · Markers: verified-dominant + 2 [incident] + 2 [drift-prone] +
  2 [verified absence] · Registered: consult table 3 rows, evals 21 cases · Next wave: none.
- P4 PASS 2026-07-25 — prompt-wording-rules Audit: potency lint within budget after rewrite
  (4 nevers → 1 budgeted gate, three lines reframed affirmative, quoted-ask false positive
  reworded); rubric gates L1=4 / L3=5 / L6=5 PASS.
- P5 PASS 2026-07-25 — skill_lint clean (incl. W8 description diet 728→653). Fresh-context
  audit (skill-checker): PASS WITH FIXES, 0 blocking / 2 major / 3 minor. Triage: M1 fixed
  (update-didn't-arrive boundary vs plugin-writing-rules — drift pair trimmed to
  claim+canonical-pointer in install-lifecycle.md, person-side t14 + author-side n09 here,
  reciprocal n06 in plugin-writing-rules); M2 fixed (lifecycle axis routed, t14–t17); minor
  fixed (worked example labeled normative-shape/illustrative-values); minor fixed
  ([verified absence] declared as a local marker sub-class in SKILL.md); minor ACCEPTED WITH
  NOTE (corpus-of-record path evals/evals.json vs pack-writing-rules' scripts/
  routing-corpus.json — a workspace-vs-standard reconciliation to report against
  pack-writing-rules, not a defect here). Behavior check: 3/3 with-skill runs meet all 5
  assertions; baselines hallucinated marketplace/npm syntax, with-skill runs cite the corpus
  and correct the npm invention. Fence closure: adopt-plugin n07/n08, plugin-writing-rules
  n05/n06, naming-rules reciprocals pre-existing; /check-routing owed at the wave boundary
  (ship step).

- P6 SHIP 2026-07-25 — wave-boundary /check-routing: 5 blind judges over 111 cases
  (plugin-install-facts 26 · adopt-plugin 16 · plugin-writing-rules 12 · big-change-git-rules 35
  · naming-rules 22): 107/110 scored (1 judge-skipped id re-judged, PASS). 3 findings triaged:
  adopt-plugin t05 stolen -> its description gains the no-marketplace.json verbatim, re-judged
  PASS; plugin-writing-rules n06 leaked -> author-side scoping ("the update you SHIPPED") plus
  the person-side symptom verbatim added here, re-judged PASS with author-side controls holding;
  naming-rules n05 leaked -> annotated as dated finding, suite untouched by this wave, fence not
  weakened. release_gate harness CLEAN at v2.1.0.
