---
doc-type: adr
id: adr-0015
status: accepted
ratified: by Kim, 2026-08-16 (live AskUserQuestion, relayed by plugins-team-lead — accepted as
  drafted after the fresh-context doc-checker pass; the authorkit follow-on in Consequences
  runs after this ratification, unblocking #433's agent leg)
date: 2026-08-16
owner: kim.granlund
supersedes: adr-0011 (three clauses of D7 only — the orchestrator agent production's hardcoded
  `-agent` tail; the orchestrator scope-resolution pool inside "the §5 parse"; and the lexicon
  disjointness set the §4 registration gate checks. D7's command/skill/primary-agent
  productions, D8's grandfather-and-ratchet posture, D9, and D10 all stand unamended)
intent-refs: null
---
# ADR-0015 — Orchestrator agents are named `{scope}-{role}`; the `-agent` tail becomes optional on the role production

> **Ratified 2026-08-16 (Kim, live AskUserQuestion — see `ratified:` above); from this point the
> file is append-only (doc_lint T4).** Drafted 2026-08-16 from Kim's ruling on issue #433 ("amend
> the grammar", latest Findings comment). ADR-0011 is NOT edited by this change and will not be edited at
> ratification either — accepted ADRs are append-only and doc_lint T4 blocks every hook-mediated
> write to one; the supersession is recorded by this ADR's `supersedes:` field alone, exactly as
> ADR-0013 recorded its partial supersession of ADR-0012.

## Context

Issue #433 (the five-triad `leading-*` / `*-leader` rename campaign) hit a hard conflict the
moment its agent leg was planned. Kim's decision #2 on that issue (2026-08-16) names the agent
files literally: `team-leader.md`, `product-leader.md`, `build-leader.md`, `planning-leader.md`,
`review-leader.md` — no `-agent` suffix. The naming canon says those names cannot conform:

- **ADR-0011 D7** adopts the spec grammar verbatim, and the spec (REQ-002 §3, §3.3) hardcodes the
  `-agent` tail into *both* agent productions: `skill-name "-" "agent"` (primary) and
  `scope "-" role "-" "agent"` (orchestrators). `-agent` is a literal, not a lexicon token — no
  manifest edit can remove it. `authorkit/skills/naming-audit/scripts/validate.py`'s
  `Grammar.parse` agent branch (lines 319-332 at HEAD `f52b2c9`) returns
  `"agent name must end in -agent"` before any other check runs, and
  `authorkit/skills/naming-conventions/references/GRAMMAR.md` (Productions block, "Agents"
  section) restates the same two productions.
- **ADR-0011 D8** makes the `naming.manifest.json` `exemptions` array a shrink-only CI ratchet
  ("may shrink and may never grow"). So a non-conforming new name cannot be admitted by
  exemption either — the only door D8 leaves open for a new mint is grammar conformance.

Kim ruled the conflict (issue #433, Findings 2026-08-16, relayed by plugins-team-lead): **amend
the grammar** — a new ADR supersedes ADR-0011's suffix rule so `{scope}-{role}` agent files
conform without exemptions; authorkit's spec/validator/GRAMMAR.md/manifest follow; #433's agent
leg is blocked on this ADR's ratification, all other legs proceed.

**Why bare role names are the right shape (not merely the ruled one).** The spec's own reading
test for agents (§3.3) is "hand this off to the ___." A role noun already passes it — "hand this
off to the team leader" — because `leader`, `orchestrator`, `coordinator` (the whole of `RoleLex`)
are *agentive nouns*: the role word IS the agent marker. On the primary production the `-agent`
tail carries information (it turns a skill name into its executor: `estate-audit` →
`estate-audit-agent`); on the orchestrator production it is redundant — `team-leader-agent`
says "agent" twice. The spec justifies its single reserved head by "the validator or router must
treat it differently" (§9); for orchestrators the validator never strips `-agent` to find a
skill (there is none — that is the production's whole point), so the tail buys the parser
nothing there.

**Measured at HEAD (2026-08-16):** 29 agent files across the 8 plugins. 2 carry the `-agent`
tail and parse by grammar today — `authorkit/agents/estate-audit-agent.md` (primary production;
untouched by this ADR) and `docs/agents/product-leader-agent.md` (orchestrator production; the
one live name this ADR's legacy-spelling clause exists for). The other 27 are person-word names
(`team-lead`, `doc-checker`, `builder`, …) sitting in `exemptions` under D8; this ADR neither
retires nor touches them. `naming.manifest.json` `role_lex` = `[leader, orchestrator,
coordinator]`; `exemptions` = 124 entries.

**Owner boundary — same split as ADR-0011 and ADR-0014.** This ADR is a docs-owned record
(`.claude/docs/adr/`) amending a docs-owned spec (`.claude/docs/spec/spec-naming-convention.md`)
that governs an authorkit-owned validator and reference set. Ratification is Kim's; the
follow-on implementation is authorkit's, executed only after ratification (or inline in the
ratifying change, if Kim authorizes that as with ADR-0014).

## Decision

**We amend the agent-kind grammar so the orchestrator production no longer requires the
`-agent` tail.** One production changes (D1), plus the scope-resolution pool that production
reads (D2 — a §5/REQ-004 parse detail) and one manifest invariant (D3 — a §4/REQ-003 gate
detail); nothing else in the grammar does.

### D1 — Orchestrator production: `{scope}-{role}`, with `-agent` optional (legacy spelling)

Spec REQ-002 §3 (and GRAMMAR.md's Productions block) becomes:

```
agent     := skill-name "-" "agent"             estate-audit-agent   (primary — unchanged)
          |  scope "-" role                     team-leader          (orchestrators — canonical)
          |  scope "-" role "-" "agent"         product-leader-agent (orchestrators — legacy spelling)
```

- `role` is the terminal token of the name (after stripping an optional `-agent`) and must be a
  member of `RoleLex`, exactly as today. `RoleLex` stays a closed manifest-governed lexicon
  (≤4 entries to start, grows only by manifest PR — ADR-0011 D7 / spec §3.3, unchanged).
- The **bare form is canonical**: a new orchestrator agent is minted `{scope}-{role}` (issue
  #433's five: `team-leader`, `product-leader`, `build-leader`, `planning-leader`,
  `review-leader`). The reason is the one given in Context — the role noun is already the
  agent marker; the tail is redundant on this production and only this production.
- The **suffixed form remains conformant by grammar**, not by exemption — this is what keeps D8's
  ratchet whole (D4 below). It is documented as the *legacy spelling*: valid, never rejected,
  not chosen for new mints. This ADR mandates no rename of `product-leader-agent`; #433's
  product-seat leg renames it on its own authority as part of the docs → teamwork move Kim
  already ruled, and any future orchestrator still spelled `*-agent` may keep that name until it
  is otherwise touched (D8's opportunistic-retirement spirit, applied to a spelling rather than an
  exemption).
- The **primary production is untouched**: an agent that performs a skill still MUST be
  `{existing-skill-name}-agent`, and the peer audit still strips `-agent` and asserts the skill
  exists (§3.3, §7 `performs` arithmetic, AC-005). A bare skill name in `agents/` (`estate-audit`
  as an agent file) still fails: it ends in no `RoleLex` token and carries no `-agent` to strip.

### D2 — Scope resolves against `ObjectVocab ∪ ProcessLex`; `build` joins `ObjectVocab`

Today `Grammar.parse` resolves the orchestrator scope-phrase via `resolve_objects` (`ObjectVocab`
only). Under that pool only two of #433's five scopes resolve (`team`, `product` ∈ ObjectVocab);
`planning` and `review` are `ProcessLex`-only, and `build` is in no lexicon at all. Two changes:

1. **Scope pool = `ObjectVocab ∪ ProcessLex`, for BOTH orchestrator spellings** (bare and
   legacy `-agent`-tailed — one production, one pool). An orchestrator coordinates either a *thing*
   (`team`, `product`, `fleet`) or a *process* (`planning`, `review`) — both are legitimate scopes
   for a coordinating seat, and both vocabularies already exist. Resolution uses the SAME greedy
   longest-match algorithm (`Grammar._resolve(tokens, pool)`, the shared helper ADR-0014's
   execution record introduced), fed this two-lexicon pool. **Deliberately NOT ADR-0014 D1's
   three-way union** (`ObjectVocab ∪ ProcessLex ∪ TopicLex`): ADR-0014 D3 scopes `TopicLex` to the
   `-rules` production only, and a reference-doc topic word (`motion`, `wording`) is not something a
   seat coordinates. Keeping the two escape-hatch pools distinct keeps each lexicon answering one
   question, the same argument ADR-0014 D2 made for `check-`.
2. **`build` registers in `ObjectVocab`** (canonical `build`, plural `builds`, no banned aliases)
   — needed for `build-leader`; issue #433's own plan flagged this ("register `build` in ObjectVocab
   first, or exempt" — exemption is closed by D8, so registration it is). Registered by
   `authorkit:manifest-authoring`'s ordinary flow, subject to AC-008's ambiguity gate; `build` sits
   in no other lexicon today (verified against `naming.manifest.json` at HEAD), so no
   disjointness question arises. **Why `ObjectVocab` and not `ProcessLex`** (either would satisfy
   the union pool): the seat coordinates *a build* — the thing, as `builder`/`build-lead` already
   use the word — and registering `build` as a process would additionally license `<object>-build`
   as a skill-name shape (`{object}-{process}`), a side effect nobody asked for.

Verified by hand against the manifest at HEAD, all five #433 names then parse: `team`·OV,
`product`·OV, `build`·OV (new), `planning`·PL, `review`·PL — each followed by `leader` ∈ RoleLex.

### D3 — `RoleLex` becomes disjoint from `ObjectVocab ∪ ProcessLex` (AC-008 gate extension)

While `-agent` was mandatory, a `RoleLex` word doubling as an object or process was harmless —
the reserved head fixed kind candidacy before any lexicon was consulted. Once a bare
`{scope}-{role}` name is a legal agent shape, a role word that also lived in `ObjectVocab` or
`ProcessLex` would let one string parse as a skill in `skills/` (`{object}-{process}`) and as an
agent in `agents/`. Kind is decided by directory (spec §6, GRAMMAR.md "Kind decision"), so this is
not a runtime ambiguity — but it would let a role noun be minted as a skill name, eroding the
"shape is informative" property ADR-0011 adopted the spec for. Therefore AC-008's manifest gate
gains one check alongside `VerbLex ∩ ProcessLex = ∅`: **`RoleLex ∩ (ObjectVocab ∪ ProcessLex) =
∅`**, a manifest error like the existing disjointness check. `ObjectVocab` here means the
validator's resolve pool — every `canonical` AND `plural` key of `Grammar.objects` (the same keys
`_resolve` matches against); `banned_aliases` are excluded (they are rejections, not vocabulary).
Holds today (`leader`, `orchestrator`, `coordinator` are in no other lexicon — verified at HEAD);
it costs one set intersection. `TopicLex` is not in this intersection (its words never head or tail an agent
name — a `-rules` name in `agents/` fails on the reserved tail regardless).

### D4 — What does NOT change (the fence)

- **ADR-0011 D8's ratchet is untouched.** The `exemptions` array still only shrinks; nothing this
  ADR needs is admitted by exemption; no exemption is retired by this ADR (the 27 person-word agent
  names stay exempt exactly as they are — renaming them is #433's leg-by-leg work under
  `rename-planning` → `rename-execute`, or nobody's). An implementer who finds themself wanting to
  add to `exemptions` to land this has misread D1/D2 — the design is complete without it.
- **The primary agent production, `performs` arithmetic (§7, AC-005, `validate.py`'s
  `performs != name minus -agent` structural check), and the `-agent` reserved head on skills**
  (`"reserved head -agent on a skill"`, still an error) — unchanged. `-agent` remains the estate's
  one reserved head; this ADR makes it non-mandatory on one production, it does not add a second
  reserved head, so spec §9's "one reserved head is the complete set" stays true as written.
- **Command grammar (§3.1), skill grammar (§3.2 incl. §14.1 reverse-wrapper, §14.2 `-rules`/`check-`),
  `VerbLex ∩ ProcessLex = ∅`, `TopicLex`'s scope, the §5 parse order** — unchanged. §5 step 1
  ("strip the reserved head `-agent`, if present") already says *if present*; its second sentence
  ("what was stripped fixes kind candidacy") stops being the whole story for a bare orchestrator
  name (kind candidacy then comes from the directory plus a `RoleLex` terminal) and is reworded
  in the amendment — the enumerated touchpoint list is Consequences items 4–5.
- **Estate scope.** ADR-0011 D7 governs three estates (nonoun-plugins, adia-ui-kit forge+factory,
  adia-eng/agentic-tools); this amendment is spec-level and therefore applies to all three. Only
  nonoun-plugins was measured for this ADR. The other estates' manifests need no change unless
  and until they mint an orchestrator; any `*-{role}-agent` name they already carry keeps
  conforming under D1's legacy spelling.
- **Frontmatter schema (§8 / `FRONTMATTER.md`'s `performs` field being required on every agent)**
  — out of scope. This estate runs `schema_scope: grammar`; orchestrator agents carrying no
  `performs` are a `full`-scope structural question that predates this ADR and is not changed by
  it. Named so nobody reads the silence as a ruling.
- **No file other than this ADR changes in the change that lands it.** ADR-0011 is not edited
  (T4). Spec, GRAMMAR.md, `validate.py`, `naming.manifest.json`, `naming-conventions/SKILL.md` all
  change only after ratification (Consequences).

### Alternatives considered

- **Alt A — Keep the grammar; name the files `*-leader-agent.md`** (issue #433 plan §5 Q1's own
  recommendation: "free grammar conformance, zero exemption debt"). Killed by ruling (Kim,
  #433, 2026-08-16) and on the merits above: the tail is redundant on a role noun, and five new
  files would carry a shape whose only justification is that the parser demanded it — the spec
  says shape should be informative, and here it would be padding.
- **Alt B — Grow the ratchet: add the five bare names to `exemptions`.** Killed: D8 forbids it
  outright (CI diffs the array; any addition fails the build), and weakening D8 to admit five
  names would convert a shrink-only burn-down into a negotiable list — the exact failure D8 exists
  to prevent. This ADR must not, and does not, weaken D8.
- **Alt C — Drop the `-agent` tail from the orchestrator production entirely (no legacy
  spelling).** Cleaner grammar: one shape per production. Killed: `product-leader-agent` would stop
  conforming the moment the validator changed, and D8 forbids re-admitting it by exemption — so
  landing the grammar would force a same-change rename of a live agent that #433's product-seat
  leg is already about to move, coupling two campaigns for no gain. The legacy spelling costs the
  validator one branch it already has and gives every existing orchestrator a conforming name
  until it is otherwise touched. Revisit when zero `*-{role}-agent` names remain in the estate;
  then Alt C is a one-line, zero-risk tightening.
- **Alt D — Register the five names via a new lexicon (`AgentNameLex`) or a per-name allowlist
  outside `exemptions`.** Killed: an allowlist that isn't the exemptions array is the exemptions
  array with the ratchet filed off; and a lexicon of whole agent names is not a grammar, it is a
  list — the same objection ADR-0014 Alt A raised to unconstrained productions.
- **Alt E — Resolve scope against `ObjectVocab` only and register `planning`/`review`/`build`
  as objects.** Killed: `planning` and `review` are processes and already live in `ProcessLex`;
  dual-registering them as objects to satisfy one production dilutes what `ObjectVocab` means (the
  argument ADR-0014 Alt B won on) when a two-lexicon scope pool expresses the actual semantics —
  a seat coordinates a thing or a process.

## Consequences

- **Nothing executes from this ADR alone.** Status is `proposed`; it becomes canon only when Kim
  flips `status: accepted` and adds `ratified:` (the flip is the ratification act — docs'
  ledger-class contract; from then on this file is append-only). #433's agent leg stays
  Blocked-by this ratification, per Kim's sequencing on that issue.
- **On ratification, the follow-on execution (authorkit-owned, one change, authorkit version bump
  + README ledger row) is:**
  1. `authorkit/skills/naming-audit/scripts/validate.py` `Grammar.parse`, `kind == "agent"`
     branch — the contract, not the code: a `-agent`-tailed name strips the tail and tries
     primary (residue ∈ skills) then orchestrator (residue's terminal ∈ `RoleLex`, scope resolved
     against D2's pool); a bare name tries orchestrator only (terminal ∈ `RoleLex`, same pool); a
     name that is neither fails with a diagnostic naming both roads. D2's pool is one more
     `_resolve` pool built once at init; D3 is one more `lexicon_errors` intersection.
  2. Validator selftest fixtures, mirroring §14.1/§14.2's positive/negative/regression triad:
     positive `team-leader` and `review-leader` (a `ProcessLex` scope) parse; legacy
     `product-leader-agent` still parses (regression); negative `estate-audit` bare in `agents/`
     fails; negative `team-leader` in `skills/` fails; a manifest fixture with a `RoleLex` word
     also in `ObjectVocab` raises the D3 manifest error.
  3. `naming.manifest.json`: `object_vocab` += `build` (D2, via `manifest-authoring`);
     `$schema_note` gains a dated sentence — "orchestrator agents mint as `{scope}-{role}` per
     ADR-0015 (2026-08-16); the `-agent` tail on that production is legacy spelling, still
     conformant" — with the D8 ratchet sentence ("may only shrink, never grow") left verbatim.
     `exemptions` count unchanged (124 → 124) — the ADR retires and admits nothing.
  4. authorkit's `naming-conventions` reference set, every touchpoint: `references/GRAMMAR.md`
     (Productions block, "Agents" section, parse step 1's "what was stripped fixes kind
     candidacy" sentence, the RoleLex row's "≤ 4" reading); `SKILL.md`'s "One reserved head"
     line (still the only reserved head; optional on the orchestrator production);
     `references/MIGRATION.md`'s "the reserved `-agent` head stays fully policed" line (true for
     skills and the primary production; qualified for orchestrators); `references/FRONTMATTER.md`'s
     `performs` comment ("must equal name minus -agent" — applies to the primary production only;
     orchestrators carry no `performs`).
  5. `.claude/docs/spec/spec-naming-convention.md`: REQ-002 §3 production block and §3.3 prose
     (D1); §5 step 1's second sentence and step 2's scope pool (D2); §4/AC-008's disjointness
     list (D3); a `team-leader` row beside `team-leader-agent` in §12; and a dated **§14.4**
     appended mirroring §14.1/§14.2's pattern (ruling authority = this ADR, validator change,
     non-goals) — §14.3 is already taken by the 2026-08-16 SPEC-type restructure (issue #372).
     The spec is edited only then, under a real sign-off.
  6. **ADR-0011 is not edited, then or later.** It is `accepted` in committed history; doc_lint
     T4 blocks every hook-mediated write to it (appends included), and the ledger contract's
     remedy is exactly a new ADR carrying `supersedes:` — this one. Precedent: ADR-0013's partial
     supersession of ADR-0012 left ADR-0012 untouched; ADR-0011's own supersession of ADR-0001 /
     ADR-0006's grammar halves left both untouched (the pointer went into `harness:naming-rules`
     instead). Anyone looking for "which ADR amended 0011" reads this file's frontmatter, not
     0011.
  7. Re-run `authorkit:naming-audit --scope grammar` estate-wide (the 9-target invocation
     ADR-0014's post-execution note pins) and confirm 0 grammar errors before and after, 124
     exemptions before and after.
- **`intent-refs: null` is deliberate.** No IDR exists for issue #433's underlying claim at
  drafting time; the T6 orphan-ADR WARN is accepted as-is (same posture as ADRs 0001–0014 and
  T6's own documented retrofit-deferral) rather than backfilled here.
- **Easier, once landed:** #433's agent leg (`team-leader`, `product-leader`, `build-leader`,
  `planning-leader`, `review-leader`) mints clean from day one; every future orchestrator seat
  names itself by role without a redundant tail; the spec's reading test and its grammar agree.
- **Harder, once landed:** the orchestrator production has two conforming spellings until the
  last `*-{role}-agent` name is gone (Alt C names the tightening for that day); `RoleLex`
  registration now carries a disjointness obligation (D3) that `manifest-authoring` must check
  before adding a role word.
- **Irreversible in the ratchet sense:** none — this ADR retires no exemption. Reversal would be a
  further ADR restoring the mandatory tail, which D8 would then force to be paired with renames
  of every bare-named orchestrator (they could not be re-admitted by exemption).
