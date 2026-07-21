# The Standard of Excellence — one system of skills

**Status: v2.2** (2026-07-03) — calibrated by the exemplar batch, hardened by the maker,
verifier/binding, and pack/orchestrator batches (36 claims reconciled across four batches). Owner: [[skills-audit]]. The per-skill floor
remains `skill-authoring-standards`; this document is the corpus-level ceiling: what a skill
must be to be excellent *in this system*, not merely sound in isolation. Claims against it remain
welcome in every deep review — it stays a living standard.

A skill here is one organ of ONE system: it shares the two-plane reasoning spine, the card→checker→
judgment discipline, a closed naming grammar, a composition graph, and a single vocabulary. A skill
can pass every local gate and still fail this standard — by duplicating a sibling, hoarding what the
spine owns, speaking synonyms, or being named for something it doesn't do.

## Scoring rules (the procedure lives in [[skills-audit]])

How a campaign runs — context assembly, batching, dispatch, the ledger, fix waves — is owned by
[[skills-audit]]'s deep-review mode; one canon per fact: procedure there, dimensions here. A review
is valid only when scored WITH the skill's **species template** (§S1) and its **graph neighborhood**
(the frontmatter descriptions of every skill it links to or is linked from, plus same-stem siblings)
in context — S1/S2 cannot be judged without them. Score every dimension with cited evidence
(file:line); end with **Claims** (where the skill beats the standard or the standard is wrong) and a
**Portfolio verdict** (§S4). A score without evidence and a prescriptive fix is not a finding.
**One finding, one home**: a defect scores in exactly one dimension (the most specific) and is
*referenced* by roll-ups — never double-counted.

**Severity order** (calibrated): N/M gates → S2 boundary defects → **A3 depth dishonesty** (drift is
the corpus's first disease) → other A/L → polish. **Template escalation**: a defect in a species
template rises one severity band (stamping multiplies it) and mandates a family-inheritance sweep.

---

## M · Mechanical (gates — code, not judgment)

- **M1** `${CLAUDE_PLUGIN_ROOT}/scripts/harness_checks.py skill <dir>/SKILL.md` → all gates pass (invoke with
  the directory in the path; a bare filename blinds D10).
- **M2 routing, measured.** Build a labeled corpus — ≥8 positives across phrasings (imperative /
  diagnostic / symptom / indirect) + ≥8 negatives from the *neighbors'* trigger vocabulary — run
  `${CLAUDE_PLUGIN_ROOT}/scripts/routing_eval.py`, and READ every named miss. Five miss classes, five fixes:
  **lexical hole** (add the trigger token) · **proxy artifact** (surface-overlap blindness — note,
  don't chase) · **fence-repelled positive** (an owned phrase repelled by a truthful NOT-clause —
  counterbalance the positive vocabulary, never weaken the fence) · **fenceless grab** (an
  over-trigger where no fence exists to repel — the fix is adding the fence, never weakening
  positives) · **reciprocity grab** (sibling-family shared phrasing settled by an S2 fence on the
  owning description, never an M2 token fix — file it to S2 with the owner named). Caveats: corpus-universal stopwords ("review", "my", "Claude") produce 1.00 proxy
  grabs — don't over-fence them; for hub skills consumed chiefly via agent `skills:` preloads, the
  description's routing weight is secondary to its preload legibility. **Pass anchor**: tripwire clear
  AND every miss/grab dispositioned (fixed here, or filed to S2 with an owner). The corpus is
  **checked into the bundle** (`scripts/routing-corpus.json`) so it survives ports and diffs across
  passes — a review-time corpus that evaporates is not a test of record. **The `_measured` block**
  (house practice, ref: `design-system-hub` / `vision-memo-forge` / `make-palette` corpora): the
  corpus file also carries a `_measured` field recording the *result* (F1, precision/recall, date), the
  *disposition of every miss and grab* (which of the five classes, and why kept or filed), and the
  *description-fix history* that produced the number. The corpus proves the test exists; `_measured`
  preserves the review-time reasoning — so a later pass reads why each residual is acceptable instead of
  re-litigating a documented structural limit or misreading a known proxy artifact as a fresh regression.

## N · Naming rigour (gates — canon: `skill-authoring-standards`'s own naming section)

- **N1 Parse.** Procedure `domain-verb` with a registered verb · knowledge pack noun-compound with
  NO verb · transform `x-to-y`. An unregistered verb is a schema change, never a coinage.
- **N2 Verb–behavior binding.** The skill DOES what its verb returns. A generative *mode* of a
  registered verb is legal only where the registry says so (e.g. `-decompose` may emit its breakdown
  forward from intent — the return type stays the breakdown, never the built thing); a `-verify`
  that *leads* with a generation verb, a `-review` that rewrites, a pack that emits: gate failures,
  fixed in the charter or the name, never by silently loosening the registry.
- **N3 Stem breadth, exact.** The stem's promise equals the charter's breadth. A deliberate
  hub/breadth exception is legal only when CITED in the bundle (why the extra territory lives here);
  per the standing naming stance, offer keep-as-is + citation before proposing a rename.
- **N4 Trigger–stem overlap.** Stem tokens appear verbatim in the trigger phrases (M2 measures; N4
  judges whether honest triggers *could* carry the stem — if not, rename).
- **N5 Registry uniqueness + species.** No skill handle equals an agent name; actor=agent,
  action=skill, consulted-corpus=pack; singular stem unless the unit of work is the set (pack noun
  plurality follows the content, e.g. `ui-patterns`).

## A · Artifact depth

- **A1 Roll-up (not a separate defect class).** Every D-gate passes and every D-review ≥4 — scored
  from the D-findings referenced, not re-counted (D8≈A3, D4≈A2, D3≈A4 evidence lives in ONE home).
- **A2 Calibration test — SKILL.md body scope.** Nothing the model knows cold, nothing a script
  should own, nothing the description already said, nothing said twice (state once, invoke the
  handle). *References are exempt*: a pack's or maker's references exist to PIN diffusely-known
  canon into one citable shape — they are governed by A3's grounding, not A2's cut-test.
- **A3 Depth honesty.** Every count/status/manifest/citation claim true against the tree (a
  CHANGELOG asserting artifacts that don't exist, a mis-cited WCAG SC, a pointer to a file that
  isn't there — all A3=2); ONE canonical source per fact with the canon NAMED (checker docstring vs
  table, floors, ownership of shared material); no diverged twin files posing as two canons;
  references cited-not-copied when owned elsewhere — and **symlink-into-canon is the sanctioned
  strongest form** (one inode, divergence impossible; port-fragile, so the canon owner is still
  DECLARED in prose on both sides); a deliberately tighter **design margin** than a downstream gate
  is legal when stated as margin, not as the gate; grounding met (researched or known cold).
- **A4 Mechanization — species-shaped.** Everything mechanizable routed to a **selftest-locked**
  script with fixtures and a negative control that bites; judgment retained only where argued
  ("arithmetic, not judgment" / "the checker can never see X" stated explicitly, in the bundle).
  Species answers: verifiers/orchestrators — the card+checker spine; **makers** — deterministic
  derivation (formulas, table lookups, trace walks) routes to a selftest-locked build/check script;
  the *critic's* downstream checker is never the maker's excuse; **bindings** — a checker where
  the artifact admits one, else the exception argued in §SelfAudit; **packs** — the mechanizable
  surface is cross-file pointer/count integrity, satisfied by the corpus-level integrity check
  (skills-audit) plus the harness D9 in-bundle pointer gate (relative markdown links in every
  bundle .md must resolve — promoted from queued on four batch-4 data points). Fact-level
  drift devices (△ verify-against-your-build markers) are a recognized micro-Update mechanism —
  they mitigate, never replace, the Update organ. Exemplar negative-control shapes worth copying:
  **inversion fixtures** (prove the wrong leg/state is detectable, not merely that a good input
  passes), **reverse controls** (assert valid inputs are NOT flagged), and **fact×fact consistency
  gates** (a declared design choice cross-checked against a measured value, e.g. RECIPE_MISMATCH).
  The script anatomy this dimension scores against — selftest contract, exit tri-state, placement,
  the mechanization test itself — is canon in `script-authoring-standards` (2026-07-14); this
  section names what A4 *scores*, that skill owns what a compliant script *is*.

## L · Language (the potency rubric — `linguistic-techniques/references/rubric.md`)

- **L-gate**: L1/L3/L6 pass. **L-excellence**: no L-dimension below 4; the house strengths present —
  frame-led lines, handles defined once then invoked, a **done/NOT-done predicate closing the
  file** (packs may close on boundaries instead — their "done" is the consult contract), contrastive
  examples where behavior could be misread, and — the house exemplar bar for procedure skills — a
  **dated, real-session worked example** that shows the procedure's value rather than asserting it.

## S · System (the dimensions only the set reveals)

- **S1 Species conformance.** Score structural fidelity to the species template; for the template
  itself, score **template-worthiness**: every organ load-bearing, and NO defect that stamping would
  multiply (a template A3/N2 defect triggers the family sweep, per the severity rule).
  | Species | Template | Shape (all organs required or argued) |
  |---|---|---|
  | maker (`-author`/`-design`/`-compose`) | `skill-authoring-standards` | one artifact · create/evaluate/improve/update on ONE rubric · conditional reference depth (no filler mandate) · Update = re-derive from the changed source, never patch prose (for doc-family makers the family-sync section IS the Update organ; for write-once artifacts, argue re-dispatch-not-edit) · gen≠crit organ (route-reality is S5's) |
  | verifier (`-verify`) | `focus-verify` | card (typed, elicit fallback, judgment-tier boundary stated) → checker gates → judgment → Invariants(numbers) → Detection catalog → Mechanism table (skipped-not-passed · necessary-not-sufficient) · a **posture collapse** where a pre-mature artifact would otherwise emit 2×N red lines (declare-once → one design-decision gate) |
  | two-axis binding (`-decompose`) | `layout-decompose` | axes A/B with gates+reviews · defect quadrant · modes · report template · Verify Target · card+checker where the artifact admits one, else exception argued (the SPINE instantiates these as manifest+coverage-gate and plan/strict modes — same organs, machine-shaped) |
  | knowledge pack (noun) | `ui-patterns` | ANSWERS-only · consult table · Grep-first discipline · worked consult · **answer contract** (base form: claim + cited file + failure-mode/caveat; pattern-packs add name/anatomy/when-it-fits) · **deviation doctrine** (a default with a rationale; contested-knowledge packs may carry it as "name the camp/system when systems disagree") · **typed index scaled to corpus size** (research-wave scale ships INDEX; a consult table suffices hand-authored) · provenance in one of the two sanctioned forms — the `**Source:/Date:/URL:**` block (researched) or `curated:` frontmatter + INDEX provenance + CHANGELOG triangulation (harvested); the pack declares which · boundaries route ALL making · factory + corpus-of-record routes · **declared-hybrid variant** (2026-07-04): a pack that ALSO carries an execution spine + a run rubric — `linguistic-techniques`, `research-methods` — where the answers are runnable protocols, not only consulted facts; legal only when the hybridity is DECLARED in a species paragraph AND the running is delegated to a named actor seat (the pack answers *which method / run how / judged by what*; the seat runs it), never a pack silently executing |
  | orchestrator (set verbs: `-audit`/`-refactor`) | `ui-audit` | composes instruments, never restates them · inventory/ledger spine (recurring sweeps: baseline + diff ledger; one-shot mutations: a persisted inventory reconciled at the prove step) · findings route to owners · three-valued verdicts · **post-pass fold-back** — the pass's lessons re-derive the skill's own anchors in the same change (an orchestrator's governed reality moves with every pass it runs) |
  | transform (`x-to-y`) | `html-to-markdown` | mapping + round-trip validation via its inverse — the round-trip diff IS the species' A4 answer, and the named inverse is its critic (S5's inverse-as-critic) |
- **S2 Place in the graph.** Charter unique (no capability twin at any scope); **boundary
  reciprocity at DESCRIPTION altitude** — fences live where routing happens: every NOT-clause names
  a neighbor whose description claims that territory, and every neighbor fencing *toward* this skill
  is fenced back in this skill's description (a body `[[edge]]` is composition, not a fence); altitude
  correct (screen/flow/product, one/set, within/between). **Fence form is load-bearing**: a fence is
  written in the house form — a `NOT for … (owner)` clause — because that is the only form the
  measurement layer (`routing_eval.py`) parses; a semantic fence invisible to measurement is not a
  fence. **Ledger rule**: a one-way fence is
  recorded on BOTH skills; the fix is owned by the skill lacking the fence. A **latent fence**
  (territory claimed by a parked/uninstalled twin that may return) is recorded in the ledger and
  the naming canon's status note — never shipped against a ghost, never left untracked. An
  **out-of-corpus fence** (wire latency, prompt-injection, back-end authz — territory no corpus
  skill claims) is legal with no named owner; it disclaims, it does not route.
- **S3 Vocabulary coherence.** One language, used by name: `[gate]`/`[review]` (rubric tiers) ·
  checker verdict tiers **gate / advisory / skip** · card · checker · selftest · negative control ·
  harness · defect quadrant · generator ≠ critic · skipped-not-passed · necessary-not-sufficient ·
  UNMEASURED · ledger/baseline · world model / knowledge pack · Verify Target · blast radius ×
  reversibility · generator ≠ ratifier (the lifecycle-strengthened gen≠crit, provenance-checked) ·
  **eval** (a repeatable metric over a labeled corpus — one of the four registered instruments;
  canon: the instrument registry in `skill-authoring-standards`'s own naming section). Axis names (A/B, outside-in/inside-out, "two planes") are OVERLOADED across the
  corpus — a skill using them must define its pair locally in one clause. A synonym for a named
  concept fails S3; extending the vocabulary is a deliberate edit to this list.
- **S4 Portfolio verdict (mandatory).** KEEP / MERGE(with) / SPLIT(into) / RETIRE / RE-CHARTER —
  judged against the set; "KEEP" requires naming what the corpus loses without it.
- **S5 Routes are real.** Maker names its critic, pack its factory, evaluator its makers — and the
  named agent/skill exists AND its charter accepts the handoff (S5 owns route-reality; S1 only
  checks the organ is present). Every finding class the skill can emit has a routable owner.
  Legal critic forms: a dedicated reviewer agent · the shared `doc-reviewer` agent (fresh-context
  critic for any rubric-bearing document artifact) · **consumer-as-critic** where the consumer is
  fresh-context by construction (a handoff's recipient; a ratifying coordinator seat) — named, not
  implied · **inverse-as-critic** for transforms (the round-trip through the named inverse) ·
  **composite-critic** for a multi-layer artifact whose rubric spans owners (ref:
  `design-system-hub` v1, 2026-07-04 — checker for the mechanical dims, `linguistics-reviewer`
  for potency, `component-reviewer` per preview, `doc-reviewer` for the spine's document slice; that
  charter now lives in `design-system-author-claude-code`, whose rubric keeps the
  checker/potency/document demarcation): legal ONLY when the
  rubric **demarcates which dimensions each critic scores** so every dimension has exactly one
  fresh-context owner and each critic scores a coherent closed slice — not one seat handed a partial
  rubric ad hoc. A composite route with any dimension left to self-score is an S5 defect, same as a
  missing owner. "A fresh-context score" with no owner is an S5 defect.
- **S6 Spine fidelity.** Where the skill reasons, it reasons on the shared spine (two crossing
  planes; gates before reviews; two scores never averaged) or argues the exception.

## Output contract (per deep review)

```
Skill: <name> · species: <species> (template: <ref>)
| Dim | M1 M2 · N1–N5 · A1–A4 · L · S1–S6 | gate/review | score | finding + evidence | fix |
Routing: F1 <n> · every miss/grab: <class → disposition>
Claims against the standard: 1) … (or none)
Portfolio: KEEP|MERGE|SPLIT|RETIRE|RE-CHARTER — <one sentence of set-level why>
```

The campaign ledger is sharded per batch — `skills-audit/campaign/batch-N/<skill>.findings.jsonl` —
each row `{skill, dim, tier: gate|review, finding, fix, status: open|fixed|filed|wontfix}`;
`ui-audit/scripts/audit-diff.py --ledger` diffs passes (mapping skill→id, dim→checker, tier→gate).
