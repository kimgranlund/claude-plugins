---
description: "Audit a whole skills/ corpus as ONE system, not one skill. CORPUS pass: naming, language, routing, peer composition — are names consistent, do skills compose. CAMPAIGN: the deep-review loop against the standard of excellence — themed batches, portfolio verdicts. NOT for reviewing one skill's rubric (skill-writing-rules); NOT for the agents estate (check-all-agents); NOT for executing the restructures (reshape-skill)."
---

# check-all-skills — the corpus as one system

A single-skill review is blind to the corpus: a naming *grammar*, a routing *collision*, a missing
*composition edge* exist only across the set. This skill owns the set-level eye and the standard it
judges by — `references/standard-of-excellence.md` (v2.2, living: every deep review may file claims
against it) — plus the campaign ledger at `campaign/batch-N/<skill>.findings.jsonl`. Two modes, two
contracts: a **corpus pass** (four cross-cutting axes, one sweep) and a **deep-review campaign**
(every skill scored against the standard, in batches). It audits, it never fixes:
`skill-writing-rules`/`make-skill` repairs one skill; `reshape-skill` executes the
restructures.

## Mode 1 — corpus pass (four axes, one sweep)

- **Two planes.** L (language) and F (front-matter) are per-skill — fan out one read per skill.
  N (naming) and P (peer leverage) are whole-corpus — one reader over the index, never per-skill.
- **The index is the spine.** `scripts/corpus_index.py` extracts the naming histogram, families,
  reserved-shadow check, the wikilink + `skills:` composition graph, and the bi-directionality
  advisory in one deterministic, selftest-locked pass — the script counts, the agent judges.
- **Own vs delegate.** N and P are owned here; L defers to `prompt-wording-rules` and F to
  `skill-writing-rules` — cite the owning standard, never re-derive it.

1. **Index (Phase 0):** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/check-all-skills/scripts/corpus_index.py" [skills_root]` — read its output before
   dispatching anything.
2. **Per-skill fan-out (Phase 1):** dispatch `wording-checker` (L — does the body instantiate
   or merely describe?) and run the skill gate (F — D1 trigger + listing budget, D10 identity).
   Independent by skill: pipeline them, one skill per chain.
3. **Corpus passes (Phase 2):** two single reads over the Phase-0 index — grammar coherence (N) and
   graph completeness (P: unwired pipeline chains, sibling pairs, standing deps that belong in
   `skills:` not prose). Cross-check descriptions pairwise for routing collisions (F).
4. **Score against `references/rubric.md`** — N/L/F/P on the 1–5 anchors, one line of cited
   evidence each, gate tiers first.
5. **Synthesize:** gate-fails first, then the cross-axis findings only synthesis catches (a one-way
   edge is P *and* reference hygiene; two near-identical descriptions are F *and* P).
6. **Validate:** re-run the index and per-skill gates after fixes land; a surface not re-run is
   UNMEASURED, never passed.

### Corpus contract

```
Corpus: <skills_root> · <N> skills · Rubric: rubric-skill-corpus
| Dim | Type | Verdict (PASS/FAIL/UNMEASURED) | Finding | Evidence |
Gate (N-shadow · F-trigger · L1 · P-dangling): <verdicts>
Cross-axis: 1) … — fix: …  ·  Top corpus moves: 1) …
```

## Mode 2 — deep-review campaign (every skill an organ)

The proven loop — four batches, 400+ ledger rows, standard revisions v1→v2.2:

1. **Batch by theme.** Exemplars first (they calibrate the standard), then makers, verifiers and
   bindings, packs and orchestrators. Version the standard between batches; reconcile claims
   before the next dispatch.
2. **Assemble each packet:** the whole bundle · the standard · the species template (§S1) · the
   graph neighborhood (frontmatter of every linked/linking skill, plus same-stem siblings).
3. **Dispatch a fresh-context critic per skill** (`skill-checker` at DEEP depth; generator ≠
   critic), scoring ALL dimensions — M1·M2 · N1–5 · A1–4 · L · S1–6 — with cited evidence and a
   prescriptive fix per finding.
4. **Measure, never vibe.** M1 = the harness gate (`python3
   "${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py" skill <dir>/SKILL.md`, directory in the
   path). M2 = `routing_eval` on a corpus checked into the bundle (`scripts/routing-corpus.json`
   or this plugin's own `evals/evals.json`, ≥8 pos / ≥8 neg, four phrasings); every miss and grab
   dispositioned into the standard's five classes.
5. **Ledger every finding:** `campaign/batch-N/<skill>.findings.jsonl`, rows
   `{skill, dim, tier, finding, fix, status: open|fixed|filed|wontfix}`. Diff passes with the
   `frontend` plugin's `check-whole-ui/scripts/audit-diff.py --ledger`, where installed.
6. **Fix wave, severity-ordered:** N/M gates → S2 boundaries → A3 drift → other A/L → polish;
   a template defect escalates one band and mandates the family sweep. The MAKER applies fixes
   (`skill-writing-rules`/`make-skill` and the finding's owner) — this skill never edits
   what it judged.
7. **Reconcile claims into the standard.** Accepted claims become the next revision in the same
   change; rejected claims are recorded with the refuting evidence.
8. **Verdict the portfolio:** KEEP / MERGE / SPLIT / RETIRE / RE-CHARTER per skill;
   `reshape-skill` executes the restructures.
9. **Fold back.** The pass's lessons re-derive THIS skill's procedure and anchors in the same
   change — an orchestrator's governed reality moves with every pass it runs.

### Campaign contract (per skill)

```
Skill: <name> · species (template: <ref>) · Gate: PASS/FAIL/UNMEASURED [harness N/N]
| Dim | tier | score | finding + evidence | fix |
Routing: F1 <n> · every miss/grab dispositioned
Claims against the standard: … (or none) · Portfolio: KEEP|MERGE|SPLIT|RETIRE|RE-CHARTER
```

## References & tools

| Path | Use when |
|---|---|
| `references/standard-of-excellence.md` | Campaign mode's rubric — the corpus-level M/N/A/L/S standard (v2.2, living; owner: this skill) |
| `references/rubric.md` | Corpus mode's four axes and anchors (N/P owned, L/F delegated) |
| `scripts/corpus_index.py` | Phase 0 — the deterministic backbone (selftest-locked) |
| `${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py` | M1 gate, `skill` mode |
| `${CLAUDE_PLUGIN_ROOT}/scripts/routing_eval.py` | M2 gate — lexical-overlap proxy against a routing corpus |
| `campaign/` | The sharded findings ledger, one directory per batch |
| `skill-writing-rules` / `make-skill` | The per-skill standard — and the tool to FIX what either mode finds |
| `reshape-skill` | Executes MERGE/SPLIT/RETIRE and rename verdicts corpus-wide |
| `check-all-agents` | The sibling estate: agent definitions, preload graph, team shape — same plugin |
| `prompt-wording-rules` | L scoring — dispatch `wording-checker` per skill, same plugin |
| `fleet-rules` | P framing — static vs dynamic wiring, descriptions as connective tissue — lives in the `teamwork` plugin |
| `make-rubric` | Author / score / repair this skill's own rubrics — lives in `docs` |

## Failure branches

- `skills_root` missing or empty → report the path and stop; an audit of nothing is not a clean pass.
- `corpus_index.py` errors or exits 2 (including the RESERVED twin-gate divergence) → the run stops
  at Phase 0; fix the script or the canon, never hand-derive the index it failed to produce.
- No `campaign/` directory yet (first-ever campaign) → create it and say so; batch-1 exemplars
  calibrate the standard, they are not graded against prior batches.
- A dispatched critic returns off-contract → one re-dispatch with the contract quoted, then the
  skill is marked UNMEASURED with the reason; never aggregate improvised prose.

**Done** when every skill in scope carries a scored review with its routing dispositioned, every
finding is a ledger row with an owner, claims are reconciled into a standard revision, and the
fold-back has been applied. **NOT done** while any verdict is two-valued where a surface was
skipped (UNMEASURED, never laundered), a finding lacks an owner, the ledger lags the pass, or this
skill fixed what it judged.
