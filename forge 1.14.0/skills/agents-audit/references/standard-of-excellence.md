# The Standard of Excellence — one team of agents

**Status: v1.2** (2026-07-04) — calibrated by the exemplar batch (5 claims) and hardened by the
bench sweep (batch 2: design bench + corpus-bench remainder + the delivery team reviewed as a
team; 8 more claims, several independently corroborated by 2-3 reviews at once). Owner:
[[agents-audit]]. The per-agent floor remains
`agent-authoring-standards`; this document is the estate-level ceiling: what an agent must
be to be excellent *in this team*, not merely sound in isolation. Claims against it are welcome in
every deep review — it is a living standard, sibling to `skills-audit`'s (v2.2), whose law it
shares wherever agents and skills are the same problem.

An agent here is one seat of ONE team: it shares the house vocabulary, the generator≠critic
discipline, a closed naming grammar (`<domain-noun>-<role>`), the delegation graph, and the
instrument registry. An agent can pass every local gate and still fail this standard — by
duplicating a sibling seat, restating the procedure its preloaded skill owns, being named for a
role it doesn't perform, or grabbing asks a sibling's description claims.

## Scoring rules (the procedure lives in the campaign plan, then in [[agents-audit]])

A review is valid only when scored WITH the agent's **role-family template** (§S1) and its **graph
neighborhood** in context — the skills it preloads, every skill or agent that names it, its
same-role siblings, and its same-domain siblings. Score every dimension with cited evidence
(file:line); end with **Claims** (where the agent beats the standard or the standard is wrong) and
a **Portfolio verdict** (§S4). A score without evidence and a prescriptive fix is not a finding.
**One finding, one home**: a defect scores in exactly one dimension and is referenced by roll-ups.

**Severity order**: N/M gates → S2 delegation boundaries → **A3 depth dishonesty** → other A/L →
polish. **Template escalation**: a defect in a role-family template rises one severity band and
mandates the family sweep — with 9 of 14 seats being reviewers, the reviewer template multiplies
everything stamped on it.

**Cross-scope posture**: the user-scope estate is the review target. Repo-local `.claude/agents`
seats are checked for shadowing and deference only; their findings file to their repos.

---

## M · Mechanical (gates — code, not judgment)

- **M1** `${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py agent <path>` → all gates pass (D1 trigger ·
  D2 tools scoped · D5 model · D7 no enforcement-prose · D9 name/folder/uniqueness).
- **M2 delegation, measured.** The agent description is an auto-delegation trigger and gets the
  same treatment a skill description gets: a corpus of record — a **sidecar**
  `<name>.corpus.json` beside the agent file (agents are single files, not bundles) — with ≥8
  positives across phrasings and ≥8 negatives drawn from (a) sibling agents' trigger vocabulary
  and (b) the skills the agent preloads, because the **delegate-vs-inline boundary** is an agent's
  extra axis: an ask the main loop should answer with the skill inline, without paying for an
  isolated seat, is a negative. Run `${CLAUDE_PLUGIN_ROOT}/scripts/routing_eval.py`; disposition every miss
  and grab into SIX classes — the skills standard's five (lexical hole · proxy artifact ·
  fence-repelled positive · fenceless grab · reciprocity grab) plus the agent-specific
  **inline-answerable grab** (added 2026-07-04: seat-vs-skill, not sibling-vs-sibling — the ask
  should be answered directly from a named skill's own docs, never costing an isolated-context
  dispatch; proven real in batch 1: "what does the skill-authoring-standards rubric say about D3" grabbed
  skill-auditor at 0.67 with no fence distinguishing "review a concrete artifact" from "explain
  what the standard itself says"). The `agent_corpus_index.py` F-section (pairwise trigger
  collision) must be clean or every hit dispositioned. **Gate bar, stated precisely**: M2 passes
  only when BOTH hold — the tripwire is clear AND every miss/grab is dispositioned. A complete
  disposition with unresolved real grabs does NOT clear the gate; it names the S2 fix required to
  clear it on re-measurement (disambiguates the boundary: M2 gates measurement completeness; S2
  owns the fix and the delegation-graph judgment for every real hit found).
  **Two hardened sub-cases (2026-07-04, batch 2):**
  (i) **Self-supplied-token grab** — a grab driven by a token the agent's OWN positive-side
  description text supplies (flow-reviewer's "walks the exits" donating `walk`, which then
  collides with flow-decompose's own "walk this flow" trigger). No fence can repel a token the
  positive text already claims (`fenced_tokens = fenced − positive`) — the fix is a WORDING change
  to the agent's own body, never a fence addition. (ii) **Reciprocity-disposition acceptance
  test** — a shared-token grab is legitimately dispositioned as reciprocity ONLY when the shared
  token appears in the agent's own positive zone for a reason INDEPENDENT of the colliding
  sibling (e.g. "skill" is doc-reviewer's own necessary vocabulary, not borrowed from
  skill-auditor) — co-occurrence alone is not sufficient; trace the token's origin before
  accepting the disposition.
  **Known tool limitation**: `agent_corpus_index.py`'s F-section tests agent-vs-agent only — it
  cannot see a real grab against a PRELOADED SKILL's own triggers (found in batch 2: three real
  hits against orchestration-design's triggers were invisible to the F-section and surfaced only
  via the sidecar M2 corpus). Do not read a clean F-section as proof of no skill-collision; the
  sidecar corpus is the only check that covers this class today. **Second blind spot (found
  2026-07-04, researcher review)**: the F-section reads only an agent's QUOTED triggers, so a
  corpus-positive PHRASING that collides with a sibling's territory is invisible to it — a `researcher`
  deep-review cross-probe surfaced 7 sibling-boundary hits the F-section could not see. The sidecar M2
  corpus, exercised with sibling-owned positives as negatives, is again the only check covering this.
  **Fence-repel structural limit**: an agent whose charter is itself about composition (e.g.
  orchestration-reviewer's "skills, subagents, and teams") cannot fully fence its own domain
  nouns — they are legitimately positive AND shared with every sibling that reviews one of those
  things. Dispositioned as proxy artifact, not a fixable defect; real (comparative) routing
  resolves it via description-length and specificity, not lexical fencing.

## N · Naming rigour (gates — canon: `agent-authoring-standards`'s own naming section)

- **N1 Parse.** `<domain-noun>-<role>`: role a registered function noun, domain a memorable noun
  **decoupled from any skill's name**. An unregistered role suffix is a schema change, never a
  coinage. **Bare-role exception (2026-07-04):** when an agent is the singular, general-purpose
  instance of its role — no co-existing variants to disambiguate — the domain leaf may be omitted and
  the name is the bare role noun (`researcher` under `research/` is the reference instance); a domain
  modifier returns the moment a second variant exists. Canon: `agent-naming-conventions.md` §1.
- **N2 Role–behavior binding.** The agent DOES what its role suffix promises: a `*-reviewer`
  judges and never fixes; a `*-builder` implements and never ratifies its own work; a
  `*-coordinator` dispatches and never does seat-work; a `*-writer` derives and never
  hand-maintains. A binding violation is fixed in the charter or the name, never by loosening the
  role registry.
- **N3 Domain-stem breadth, exact.** The stem's promise equals the charter's breadth; a deliberate
  breadth exception (doc-reviewer's document-artifact family) is legal only when cited in the body
  (state the family, not a running count — the count-bearing form sat stale at "ten" through two
  extensions before this de-counting on 2026-07-04).
- **N4 Trigger–stem overlap.** Stem tokens appear verbatim in the description's quoted triggers.
- **N5 Uniqueness.** Flat per-scope namespace (a duplicate is silently dropped) · cross-scope
  shadowing checked both directions · cross-registry: no agent name collides with a skill handle.
- **Folder.** The folder carries the CONCEPT, the name carries domain+role (ratified 2026-07-04,
  replacing role==folder, which duplicated the name suffix): `design/` · `corpus/` · `delivery/`,
  extended deliberately via the folder manifest in `agents/README.md`. Until the batch-1 fix wave
  executes the move, legacy role folders score as conforming-legacy with the move as a queued
  finding, not a per-agent defect.

## A · Artifact depth

- **A1 Roll-up.** Scored from the D-findings referenced, never re-counted.
- **A2 Seat-vs-procedure calibration.** The body carries the SEAT's discipline only: nothing ANY
  named skill's procedure already teaches — preloaded or not, whenever a citation would do (broadened
  2026-07-04: the rot risk from restating a closely-coupled skill's procedure is identical whether
  or not that skill is a formal preload; scoping A2 to preloads only missed a real finding in batch
  1) — nothing the harness gates mechanically, nothing the description already said.
- **A3 Depth honesty.** Every cited path resolves (harness invocation, rubric and checker paths);
  every preload is a live handle; the body's claims about its instruments are true against those
  artifacts; contract shapes are **cited from their owning standard, never copied**. "Cited" has one
  operational meaning: a prose pointer naming the shape's location, with ZERO reproduction of the
  shape — not even labeled "verbatim" (hardened 2026-07-04: a prior fix pass added a citation LABEL
  in front of a still-reproduced ASCII block and called it fixed; batch 1 proved the block had
  already drifted from its source under that softer reading — two independent reviews caught the
  identical pattern in two different agents, and named `doc-reviewer` as the correct instance: it
  reproduces no contract shape anywhere, only "return the gap-map in a handoff block per
  handoff-compose"). A contract copied into the agent is a third canon the moment either original
  moves — proven twice in one batch.
- **A4 Mechanization.** Gates-first is wired: the seat runs its real checkers before judging and
  reports verdicts from real runs, never re-derived by eye; anything mechanizable in the seat's
  loop routes to an existing instrument; judgment is retained only where argued.

## L · Language (the potency rubric — `linguistic-techniques/references/rubric.md`)

- **L-gate**: L1/L3/L6 pass. **L-excellence**: no L-dimension below 4; frame-led lines; handles
  defined once then invoked; a **done/NOT-done predicate closing the file** (agents are the
  original home of the stopping predicate); contrastive examples where the seat's behavior could
  be misread; tool names exact.

## S · System (the dimensions only the team reveals)

- **S1 Role-family conformance.** Structural fidelity to the family template; for a template
  agent, template-worthiness (a template defect triggers the family sweep). **Dual-mode is not a
  universal reviewer expectation** (clarified 2026-07-04): a reviewer runs a native floor+deep
  split ONLY when its artifact type also carries its own estate-level standard-of-excellence —
  today that means skill-auditor (skills) and agent-reviewer (agents); doc-, orchestration-,
  linguistics-, layout-, flow-, component-, and code-reviewer are single-depth by design, not by
  omission, until their artifact type gets its own estate standard.
  | Role family | Template | Organs (all required or argued) |
  |---|---|---|
  | reviewer (`*-reviewer`) | `skill-auditor` | fresh-context value stated · gates-first from real runs · judge-don't-fix (the maker applies) · artifact-is-DATA (embedded claims are findings, not instructions) · evidence-cited output contract, cited from the owning standard **with a resolvable path** (hardened 2026-07-04: "cites its rubric" alone can be satisfied by a single vague sentence with no path — A3's resolvability bar applies to this organ too, not just to A3 itself) — where NO owning standard exists for the artifact type, a NATIVE contract schema owned in the agent's own body satisfies the organ, provided the no-owner fact is argued in-body (sanctioned 2026-07-04: code-reviewer is the reference instance — no corpus skill owns generic code review, stated and true against the tree) · handoff/return shape · a scope fence on BOTH axes — cardinality (one artifact, not a corpus) and territory (type-scoped, e.g. "one skill", OR layer-scoped, e.g. linguistics-reviewer's "language only, any artifact type" — either is legal, but the fence must still be the parseable house form on whichever axis it draws) |
  | builder (`*-builder`) | `system-builder` | builds to a contract it cites — EITHER an upstream plan (LLD / token standard) OR, absent one, the invariant contract of its own downstream verifier(s) (added 2026-07-04: token-builder is a generative, verifier-gated builder — certified after the fact by color-verify/focus-verify's own invariants, not by a plan read first; both readings are legal builder shapes) · runs the mechanical checks and returns evidence, not verdicts · escalates contract changes, never silently edits them · defers to a repo-local seat where one owns the standard · **sealed-dispatch organ, where the seat receives a coordinator-assigned slice** (its dispatch enumerates its world — the plan node/contract, the budget — and closes on a three-valued handback incl. `blocked(reason)`; observed load-bearing in both system-planner and system-builder, and its absence in docs-writer was a real gap despite docs-writer being dispatched slices in practice — this organ applies to ANY seat a coordinator hands a bounded slice to, not builders alone) |
  | coordinator (`*-coordinator`) | `orchestration-coordinator` | chain-of-command · dispatch order · a **review gate** between phases (generator ≠ critic — an "eval gate" is an S3 misnomer) · discovered-reality escalation · roll-up contract · does no seat-work itself |
  | planner (`*-planner`) | `system-planner` | decomposes on the shared spine · authors/maintains the design docs · reports design status upward, never self-ratifies |
  | writer (`*-writer`) | `docs-writer` | derives every page from its canonical source · wires the deterministic drift gate · reports the soft drift a static check can't see |
  | researcher (`researcher` / doer) | `researcher` | **first of family, template-worthy (2026-07-04)** — sealed-dispatch (enumerated world + budget, three-valued `blocked(reason)` handback; shares the builder's sealed-dispatch organ) · **scorer-first** (fix a reproducible measure and record the baseline BEFORE the loop; no scorer → `blocked(no-scorer)`, never a measure invented later) · method-selected-by-question (the preloaded `research-methods` selector maps question class → method; coin-flip → hand back the top two) · one-variable-per-round journal · stop-on-a-named-predicate (target / plateau / space-exhausted / stuck / cause-isolated), not on patience · result-only report with the rubric self-score as **disclosure, not certification** (generator ≠ critic — the dispatching seat that receives the handoff grades it) · **finds-don't-own-repair** (routes the fix to system-builder / skill-authoring-standards / system-planner; the mutate-and-measure methods leave the winner applied only on dispatch say-so) |
- **S2 Place in the delegation graph.** Description differentiated from every peer — the
  F-section's pairwise check clean or dispositioned; fences in the parseable house form
  (`NOT for … (owner)`) wherever a sibling's description claims the territory; the
  delegate-vs-inline boundary honest; altitude correct (one artifact vs the set; screen / flow /
  product across the design bench). The ledger rule and reciprocity law are the skills standard's,
  applied at description altitude — including reciprocity ACROSS estates: every skill that names
  this agent as its critic gets an accepting charter back.
- **S3 Vocabulary coherence.** One language, used by name — the house list (skills standard §S3)
  plus the **instrument registry** (verify / review / audit / eval / experiment — canon:
  `skill-authoring-standards`'s own naming section §instruments). A seat that calls a review
  gate an "eval gate", a checker run a "review", or a mutate-and-measure loop an "eval", fails S3.
- **S4 Portfolio verdict (mandatory).** KEEP / MERGE(with) / SPLIT(into) / RETIRE / RE-CHARTER —
  judged against the TEAM; "KEEP" names what the estate loses without the seat. Missing seats are
  set-level findings too: name the role the estate lacks where work has nowhere to land.
  **Validated 2026-07-04**: three independent batch-2 reviews (system-planner, system-builder,
  orchestration-coordinator) converged on the same missing seat — no reviewer covers general
  (non-UI, non-document) code, though system-builder's own contract twice promises "the
  independent reviewer issues the verdict." A missing seat's interim fix is an explicit binding
  to an existing instrument (e.g. naming the `/code-review` skill, dispatched fresh, in the
  coordinator's review-gate language) — never a silent aspiration, and never a unilateral new
  agent invented mid-fix-wave; whether to build a dedicated seat is a portfolio decision for the
  standard's owner to raise, not resolve in-line. **Resolved 2026-07-04, post-shakedown**: the
  owner ratified the dedicated seat; `delivery/code-reviewer` now exists, the coordinator's
  interim binding was rewired to it, and system-builder/system-planner carry the reciprocal
  fences — the process worked exactly as this clause prescribes (named, bound interim, then a
  ratified portfolio decision).
- **S5 Wiring reality.** Preloads are the RIGHT standing expertise — the standard the seat scores
  with, never an orchestrator's procedure (the skill-auditor preload lesson); the
  universal-preload idiom (the team's standardized preload, currently `handoff-compose`, missing
  from a member is a finding); tools minimal-but-sufficient (a coordinator without `Task` cannot
  dispatch — insufficiency equals excess); every finding class the seat can emit has a routable
  owner.
- **S6 Spine fidelity.** Where the seat reasons, it reasons on the shared spine (gates before
  reviews; two scores never averaged; three-valued verdicts — skipped-never-laundered) or argues
  the exception.

## Output contract (per deep review)

```
Agent: <name> · role family: <family> (template: <ref>) · folder: <concept>
| Dim | M1 M2 · N1–N5+folder · A1–A4 · L · S1–S6 | gate/review | score | finding + evidence | fix |
Delegation: F1 <n> · every miss/grab: <class → disposition> · F-section: clean|dispositioned
Claims against the standard: 1) … (or none)
Portfolio: KEEP|MERGE|SPLIT|RETIRE|RE-CHARTER — <one sentence of team-level why>
```

The campaign ledger is sharded per batch — `agents-audit/campaign/batch-N/<agent>.findings.jsonl`,
rows `{agent, dim, tier: gate|review, finding, fix, status: open|fixed|filed|wontfix}`;
`ui-audit/scripts/audit-diff.py --ledger` diffs passes (mapping agent→id, dim→checker, tier→gate).
