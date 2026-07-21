---
name: check-all-agents
description: >-
  Audit a whole agents/ team as ONE team. Use whenever the target is the TEAM, not one agent — two modes.
  CORPUS pass: four cross-cutting properties no single-agent review can see (naming coherence, linguistic
  potency, front-matter as an auto-delegation interface, global-skill leverage): "review all my agents",
  "audit the agent team", "are my agent names consistent", "do my agents leverage the right skills", "map
  the agent-to-skill preload graph", "which agents are duplicates". CAMPAIGN: the deep-review loop against
  the agents standard of excellence — role-family templates, measured delegation, composition-edge probes,
  portfolio verdicts: "review this agent against the standard of excellence". Owns
  references/standard-of-excellence.md and the campaign/ ledger. NOT for a single agent's definition or why
  it won't auto-delegate (agent-writing-rules / make-agent); NOT for the skills corpus
  (check-all-skills); NOT for a product's UI (check-whole-ui); NOT for wiring decisions — subagent or team
  (team-or-solo-rules).
disable-model-invocation: true
user-invocable: true
---

# check-all-agents — the team as one system

A single-agent review is blind to the team: it cannot see a naming *grammar*, two agents that are
the *same role*, a *missing skill-preload edge*, or whether a dispatched team's seats actually name
each other — those exist only across the set. This skill owns the set-level eye and the standard
it judges by — `references/standard-of-excellence.md` (v1.2, living: every deep review may file
claims against it) — plus the campaign ledger at `campaign/batch-N/<agent>.findings.jsonl`. Two
modes, two contracts: a **corpus pass** (four cross-cutting axes, one sweep) and a **deep-review
campaign** (every agent scored against the standard, in batches, plus the team composed as a
whole). It audits, it never fixes: `agent-writing-rules`/`make-agent` repairs one agent;
`reshape-skill` executes renames or the concept-folder moves the audit's findings imply.

## Mode 1 — corpus pass (four axes, one sweep)

- **Two planes.** L (language) and F (front-matter) are per-agent — fan out one read per agent.
  N (naming) and S (skill leverage) are whole-team — one reader over the index, never per-agent.
- **The index is the spine.** `scripts/agent_corpus_index.py` extracts the naming histogram + role
  collisions, non-agent files, name uniqueness, the pairwise F-differentiation check (each agent's
  own quoted triggers tested against every sibling's description via `routing_eval`'s lexical-overlap
  proxy — no external corpus needed), and the agent→`skills:` preload graph in one deterministic,
  selftest-locked pass — the script counts, the agent judges.
- **Own vs delegate.** N and S are owned here; L defers to `prompt-wording-rules` and F to
  `agent-writing-rules` — cite the owning standard, never re-derive it.

1. **Index (Phase 0):** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/check-all-agents/scripts/agent_corpus_index.py" <agents_dir> [skills_root ...]` —
   the role histogram + collisions + non-agent-file + uniqueness check (N), the pairwise
   routing-collision report (F's differentiation leg), and the agent→skill preload graph (S). Read
   its output before dispatching anything.
2. **Per-agent fan-out (Phase 1):** dispatch `agent-checker` (F — against the agent-writing-rules rubric
   + harness) and `wording-checker` (L — does the body instantiate or merely describe?).
   Independent by agent: pipeline them, one agent per chain.
3. **Corpus passes (Phase 2):** two single reads over the Phase-0 index — grammar coherence (N —
   one grammar or a split; is each role collision a distinct domain or a duplicate agent to merge?)
   and leverage completeness (S — which agents preload nothing yet carry standing expertise their
   role implies). Judge each Phase-0 F-differentiation hit: a real ambiguity needs a fence or a
   scope split; a shared-domain-vocabulary proxy artifact needs neither.
4. **Score against `references/rubric.md`** — N/L/F/S on the 1–5 anchors, one line of cited
   evidence each, gate tiers first.
5. **Synthesize:** gate-fails first, then the cross-axis findings only synthesis catches (two
   same-role agents are N *and* F *and* S; a non-agent file is N *and* often a dead artifact a
   skill now owns).
6. **Validate:** re-run the index and per-agent gates after fixes land; a surface not re-run is
   UNMEASURED, never passed.

### Corpus contract

```
Team: <agents_dir> · <N> agents · Rubric: rubric-agent-corpus
| Dim | Type | Verdict (PASS/FAIL/UNMEASURED) | Finding | Evidence |
Gate tiers, three-valued: N-unique/no-non-agent <…> · F-harness <…> · L1 <…> · S-dangling <…>
Per-agent gate-fails: <agent: dim> …  ·  Cross-axis: 1) … — fix: …  ·  Top team moves: 1) …
Ledger: findings.jsonl (per-pass; diffed via check-whole-ui's audit-diff.py, or: first pass — baseline)
```

## Mode 2 — deep-review campaign (every agent a seat, the team a system)

The proven loop — 2 batches, the folder-taxonomy move, standard v1→v1.2:

1. **Batch by theme.** Exemplars first (they calibrate the standard — pick the role-family
   template(s) plus the widest-fan-in agent), then the bench sweep grouped by role-family/composed
   team. Version the standard between batches; reconcile claims before the next dispatch.
2. **Assemble each packet:** the whole agent `.md` (agents carry no bundle — one file + its
   sidecar corpus) · the standard · the role-family template (§S1's table; look up the target's
   role suffix to find which agent IS the template) · the graph neighborhood (every skill it
   preloads, every skill/agent that names it, same-role and same-domain siblings). For a
   dispatched team (a coordinator + its seats), assemble ALL member files together — composition
   findings need the whole set in context at once.
3. **Dispatch a fresh-context critic per agent** (a general-purpose deep reviewer briefed with the
   packet above — never the agent's own role dispatched onto itself); generator ≠ critic. Score
   ALL dimensions — M1·M2 · N1–5+folder · A1–4 · L · S1–6 — with cited evidence and a prescriptive
   fix per finding. For a composed team, also probe each member's **composition edges** to its
   named siblings (does it name them for real, is the reference reciprocated, does the artifact
   handoff line up) — quote exact lines; this is the raw material for the team-level synthesis.
4. **Measure, never vibe.** M1 = the harness gate (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py" agent <target>`).
   M2 = `routing_eval` on a **sidecar** `<name>.corpus.json` beside the agent file (≥8 pos / ≥8 neg,
   drawn from sibling triggers + preloaded-skill triggers, since the delegate-vs-inline boundary is
   an agent's extra axis); every miss and grab dispositioned into the standard's six classes
   (five skill-inherited + the agent-specific inline-answerable grab). The `agent_corpus_index.py`
   F-section must be clean or every hit dispositioned — but note its known blind spot: it only
   tests agent-vs-agent, never agent-vs-preloaded-skill (the sidecar corpus is the only check that
   covers that class).
5. **Ledger every finding:** `campaign/batch-N/<agent>.findings.jsonl`, rows
   `{agent, dim, tier, finding, fix, status: open|fixed|filed|wontfix}`.
6. **Fix wave, severity-ordered:** N/M gates → S2 boundaries → A3 drift → other A/L → polish; a
   role-family template defect escalates one band and mandates the family sweep. The MAKER applies
   fixes (`agent-writing-rules`/`make-agent` and the finding's owner) — this skill never edits what it judged.
7. **Reconcile claims into the standard.** Accepted claims become the next revision in the same
   change; rejected claims are recorded with the refuting evidence.
8. **Verdict the portfolio:** KEEP / MERGE / SPLIT / RETIRE / RE-CHARTER per agent; missing seats
   are set-level findings too — name the gap, bind an interim instrument if one exists, and don't
   invent a new agent mid-fix-wave (that's a portfolio decision for the standard's owner).
   `reshape-skill` executes the restructures.
9. **Fold back.** The pass's lessons re-derive THIS skill's procedure and anchors in the same
   change — an orchestrator's governed reality moves with every pass it runs.

### Campaign contract (per agent)

```
Agent: <name> · role family: <family> (template: <ref>) · folder: <concept>
| Dim | M1 M2 · N1–N5+folder · A1–A4 · L · S1–S6 | gate/review | score | finding + evidence | fix |
Delegation: F1 <n> · every miss/grab: <class → disposition> · F-section: clean|dispositioned
Claims against the standard: 1) … (or none)
Portfolio: KEEP|MERGE|SPLIT|RETIRE|RE-CHARTER — <one sentence of team-level why>
```

## References & tools

| Path | Use when |
|---|---|
| `references/standard-of-excellence.md` | Campaign mode's rubric — the estate-level M/N/A/L/S standard (v1.2, living; owner: this skill) |
| `references/rubric.md` | Corpus mode's four axes and anchors (N/S owned, L/F delegated) |
| `scripts/agent_corpus_index.py` | Phase 0 — the deterministic backbone (selftest-locked) |
| `${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py` | M1 gate — same script `skill-checker`'s siblings use, `agent` mode |
| `${CLAUDE_PLUGIN_ROOT}/scripts/routing_eval.py` | M2 gate — lexical-overlap proxy against a sidecar corpus |
| `campaign/` | The plan of record (`PLAN.md`) + the sharded findings ledger, one directory per batch |
| `agent-writing-rules` / `make-agent` | The per-agent standard — and the tool to FIX what either mode finds |
| `reshape-skill` | Executes MERGE/SPLIT/RETIRE and concept-folder moves the campaign verdicts |
| `check-all-skills` | The sibling audit for a whole *skills* corpus (the same two-mode shape), same plugin |
| `prompt-wording-rules` | L scoring — dispatch `wording-checker` per agent, same plugin |
| `team-or-solo-rules` | S framing — static (`skills:` preload) vs dynamic wiring, descriptions as connective tissue — lives in the `teamwork` plugin |
| `make-rubric` | Author / score / repair this skill's own rubrics — lives in `docs` |

## Failure branches

- `agents_dir` missing or empty → report the path and stop; an audit of nothing is not a clean pass.
- `agent_corpus_index.py` errors or exits 2 → the run stops at Phase 0; fix the script or the
  input, never hand-derive the index it failed to produce.
- No `campaign/` directory yet (first-ever campaign) → create it with an empty `PLAN.md` and say
  so; batch-1 exemplars calibrate the standard, they are not graded against prior batches.
- A dispatched critic returns off-contract → one re-dispatch with the contract quoted, then the
  agent is marked UNMEASURED with the reason; never aggregate improvised prose.

**Done** when every agent in scope carries a scored review with its delegation dispositioned, every
finding is a ledger row with an owner, claims are reconciled into a standard revision, and the
fold-back has been applied. **NOT done** while any verdict is two-valued where a surface was
skipped (UNMEASURED, never laundered), a finding lacks an owner, the ledger lags the pass, or this
skill fixed what it judged.
