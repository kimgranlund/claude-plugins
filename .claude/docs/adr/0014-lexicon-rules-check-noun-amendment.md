---
doc-type: adr
id: adr-0014
status: accepted
ratified: by Kim, 2026-08-16 (live AskUserQuestion round) — the execution follow-on named in
  Consequences was dispatched in the same change: `validate.py` gained D1/D2 (plus the
  `resolve_objects_union` helper and D3's `TopicLex`), `naming.manifest.json` seeded TopicLex,
  added D4's 12 ObjectVocab entries, removed `check`, and retired exactly the 32 named
  exemptions (156→124); `spec-naming-convention.md` gained §14.2 mirroring §14.1's own pattern.
date: 2026-08-16
owner: kim.granlund
supersedes: null
intent-refs: null
---
# ADR-0014 — Register a `-rules`/gerund object class and the `check-<noun>` tail in the naming-convention grammar

> **Ratified 2026-08-16 (Kim, live AskUserQuestion — see `ratified:` above).** Execution landed
> in the same change: `naming.manifest.json` and
> `authorkit/skills/naming-audit/scripts/validate.py` now carry D1–D4 exactly as decided below.
> This note is append-only per the accepted-ADR ledger-lock contract (doc_lint T4) — the
> flip from `proposed` to `accepted` above is itself the ratification act; nothing below this
> point is rewritten, only appended to going forward.

## Context

`.claude/docs/lld/lld-0005-estate-overhaul-2026-08-16.md` (PR #346, Gate A approved by Kim
2026-08-16) Row G names a systemic gap `authorkit:naming-audit`'s Phase-0 measurement surfaced
across all 8 plugins: the `-rules`/gerund object class has no lexicon production (present in
6/8 plugins), and the recurring `check-<noun>` skill-name tail is incomplete (4/8) — both are
"informational, not violations" only because ADR-0011 D8's grandfather-and-ratchet migration
posture lets every pre-existing name sit in `naming.manifest.json`'s `exemptions` array
indefinitely. That posture is correct for one-off names; it is the wrong tool for a *recurring,
predictable* shape a human keeps re-minting — every future `*-rules` standards skill or
`check-<noun>` report generator re-earns a hand exemption instead of parsing.

**Measured against the repo-root `naming.manifest.json` (156 exemptions today):**

- 22 exempted names end in `-rules` (a closed reference-doc-standards pattern: `agent-writing-rules`,
  `big-change-git-rules`, `blocked-by-rules`, `checking-rules`, `design-md-rules`,
  `doc-writing-rules`, `entry-file-rules`, `font-token-rules`, `hook-writing-rules`, `icon-rules`,
  `loop-rules`, `motion-rules`, `ops-write-sandbox-rules`, `pack-writing-rules`,
  `parallel-work-rules`, `plugin-writing-rules`, `prompt-wording-rules`, `script-writing-rules`,
  `size-and-shape-rules`, `skill-writing-rules`, `team-or-solo-rules`, `thinking-depth-rules`).
- 14 exempted names match `check-<noun>` (`check-a2a-isolation`, `check-all-agents`,
  `check-all-skills`, `check-colors`, `check-entry-file`, `check-everything`, `check-focus`,
  `check-routing`, `check-safety`, `check-speed`, `check-state`, `check-translations`,
  `check-ui-change`, `check-whole-ui`). Three siblings — `check-doc`, `check-skill`,
  `check-stage` — already parse clean today (PR #345 registered `check` itself into
  `ObjectVocab`), but **by accident, not by design**: the nominal-phrase production (spec
  §3.2/§5) and — for `check-stage` specifically — the *object-process* production (spec §3.2,
  `Grammar.parse`'s skill branch: terminal `stage` ∈ `ProcessLex`, residue `check` resolved
  against `ObjectVocab`) both lean on `check` sitting in `ObjectVocab` as if it were an ordinary
  noun. `check` is a verb, not a domain object, and registering it as one only works for the
  lucky subset of tails whose OTHER token also happens to be a registered noun — a real defect
  this ADR retires, not a feature to preserve as-is (D4 below; its removal is load-bearing, so
  D2/D4 together must keep covering all three already-passing siblings, not just the two PR #345
  named).
- **Two more `-rules` names already parse clean today, independent of the 22 exempted ones:**
  `naming-rules` (harness) and `product-lifecycle-rules` (docs) — both resolve via the existing
  object-process production (`naming` and the compound `product-lifecycle` are already
  `ObjectVocab` entries; `rules` ∈ `ProcessLex`). Cited here because D1's proposed union-pool
  production must be a strict superset of what already resolves these two, never a narrower
  check that could regress them (verified below, D1).

**Root cause, read directly off `Grammar.parse`'s skill branch (validate.py:319-337):** the
object-process production (`{object}-{process}`) checks only the *terminal* token against
`ProcessLex`; the nominal-phrase fallback checks *every* token, but only against `ObjectVocab`,
via `resolve_objects`. Neither production admits a token that is legitimately a `ProcessLex` word
sitting anywhere but the tail (`writing` in `agent-writing-rules`), nor a fixed verb sitting at
the *head* of a skill name (`check` in `check-routing`) — because skill-kind invocation grammar
has exactly one escape hatch for a non-object-process shape (the plain nominal phrase, ObjectVocab
only) and one reserved head (`-agent`, agent-kind only). `-rules` and `check-` are two different,
independently-recurring shapes that need two independently-scoped grammar extensions, not one
generic relaxation.

**Owner boundary (LLD Risk 2, previously unresolved):** this ADR proposes a resolution, taking
effect only upon ratification (never asserted as already-settled while `status: proposed`).
Authorship and
ratification of the grammar decision follow ADR-0011's own precedent — the spec and its
amendments are docs-owned documents (`.claude/docs/spec/`, `.claude/docs/adr/`) even though they
govern an authorkit-owned validator; ADR-0011's own execution order did exactly this split
(steps 1/4 documentation, steps 2-3 authorkit's build). This ADR is authored under that same
split: docs owns this record, authorkit owns the eventual `validate.py`/`naming.manifest.json`
implementation once ratified.

## Decision

**We propose two new, independently-scoped grammar productions plus one new closed lexicon** —
additive to spec §3.2/§4/§5, changing nothing about command grammar (§3.1), agent grammar (§3.3),
the `-agent` reserved head, the plain nominal-phrase fallback for every other skill, or the
`VerbLex ∩ ProcessLex = ∅` disjointness invariant.

### D1 — `-rules` becomes a second reserved TAIL (skills only), resolved against a union pool

```
skill := topic-phrase "-" "rules"
```

`rules` is the LITERAL terminal token (not merely a `ProcessLex` member — `rules` already sits in
`ProcessLex`, which is precisely why registering it there alone was insufficient: the
object-process production still forces every *other* token to resolve via `ObjectVocab` alone,
and `writing`/`checking`/`wording`/`icon`/`motion`/… are not domain objects). `topic-phrase`
(every token except the trailing `rules`) resolves via the SAME greedy longest-match algorithm
`resolve_objects` already implements, fed a **union pool**: `ObjectVocab ∪ ProcessLex ∪ TopicLex`
(TopicLex is new — D3 below).

**Insertion point, precisely.** `Grammar.parse`'s `kind == "skill"` branch currently reads
(validate.py:319-324):

```python
if tokens[-1] == "agent": return errs + ["reserved head -agent on a skill"]
if len(tokens) >= 2 and tokens[-1] in self.process_lex:
    ok, why = self.resolve_objects(tokens[:-1])
    return errs if ok else errs + [f"skill object: {why}"]   # <- HARD return, success or failure
```

Because `rules` ∈ `ProcessLex` already, every `-rules` name hits this existing branch FIRST and
`return`s unconditionally — success or failure — so a new branch placed "before the nominal
fallback" is unreachable dead code for this entire class; the existing branch never falls
through to it. D1's new branch must be inserted **before** this object-process check instead, as
its own reserved-tail branch, mirroring `-agent`'s hard-return shape:

```python
if tokens[-1] == "rules" and len(tokens) >= 2:
    ok, why = self.resolve_objects_union(tokens[:-1])   # ObjectVocab ∪ ProcessLex ∪ TopicLex
    return errs if ok else errs + [f"skill topic (rules tail): {why}"]
    # HARD return, like -agent — never falls through
```

Safe for the two names that already parse clean today outside the 22 exemptions
(`naming-rules`, `product-lifecycle-rules` — Context above): the union pool is a strict superset
of `ObjectVocab` alone (`ObjectVocab ⊆ ObjectVocab ∪ ProcessLex ∪ TopicLex`), so any token
sequence that already resolves via plain `ObjectVocab` still resolves via the union pool —
nothing that passes today can regress under this branch.

`resolve_objects_union` is `resolve_objects` with `self.objects` swapped for a merged dict built
once in `Grammar.__init__` (`ObjectVocab` entries ∪ single-token `ProcessLex` entries ∪ `TopicLex`
entries) — no change to the matching algorithm itself, only to which lexicon set it's built from.

**Why a union pool, not ObjectVocab alone:** 7 of the 22 exempted `-rules` names are exactly
`{noun}-writing-rules` (`agent-`, `doc-`, `hook-`, `pack-`, `plugin-`, `script-`, `skill-`) — the
noun is already an `ObjectVocab` entry and `writing` is already a `ProcessLex` entry (registered
for the ordinary `{object}-writing` skills, e.g. `doc-writing`-shaped names). Requiring those 7 to
re-register `writing` a second time in a new lexicon would duplicate a fact the manifest already
states once. The union costs nothing D5 below doesn't already have to check for lexicon
disjointness.

### D2 — `check-` becomes a reserved HEAD (skills only), independently scoped

```
skill := "check" "-" object-phrase
```

`check` is the literal token `tokens[0]`, not a `VerbLex`-head production generalized to every
verb (that would blur the invoker partition §2 exists to keep decidable — a skill front-loading a
verb is not what commands' object-first shape means, and admitting it for every `VerbLex` member
would let skill and command names collide in shape). `object-phrase` (`tokens[1:]`) resolves
against **`ObjectVocab` only** — deliberately NOT the D1 union pool: a `check-<noun>` name denotes
a real, checkable system object (a doc, a skill, a routing table, a color set), which is exactly
what `ObjectVocab` already means; a `-rules` name denotes a reference-doc *topic*, a different
contract (D3). Keeping the two escape hatches' resolution pools disjoint keeps each vocabulary
answering one question.

**Insertion point, same dead-code hazard as D1.** For the identical reason (the object-process
branch at validate.py:321-324 hard-returns whenever the TERMINAL token is in `ProcessLex`, before
any later branch runs), this production must also sit **before** that branch, not after it —
critically for `check-stage` (docs), a THIRD name that parses clean today only by accident
(Context above: terminal `stage` ∈ `ProcessLex`, residue `check` ∈ `ObjectVocab` today). Placed
after the object-process branch, D2 would never even see `check-stage` — the object-process
branch claims it first, and D4's removal of `check` from `ObjectVocab` would then make that
branch's own residue check fail with no D2 branch left to catch it, a silent regression from
passing to exempt. Inserted before, mirroring D1 and `-agent`'s hard-return shape:

```python
if tokens[0] == "check" and len(tokens) >= 2:
    ok, why = self.resolve_objects(tokens[1:])   # ObjectVocab only
    return errs if ok else errs + [f"skill object (check- head): {why}"]
    # HARD return — check-all-agents/check-all-skills/check-everything/check-whole-ui
    # correctly still fail here (their non-tail tokens are quantifiers, never
    # registered — see "What does NOT change" below), with a clearer diagnostic
    # than falling through to the generic nominal-phrase failure message.
```

This also retroactively fixes `check`'s own presence in `ObjectVocab` (D4 below removes it —
`check-doc`/`check-skill`/`check-stage` all keep passing, now because D2's head production
licenses them — `stage` joins D4's ObjectVocab additions specifically so `check-stage` keeps
resolving — not because `check` masquerades as a noun).

### D3 — New closed lexicon `TopicLex`

Structurally identical to `RoleLex` (flat list, `naming.manifest.json` top level, governed by
manifest PR). `TopicLex` exists because a `-rules` name's non-tail tokens are reference-doc
*topics* (`icon`, `motion`, `wording`) that the tooling never manipulates as objects and that
would otherwise pressure `ObjectVocab`'s own registration-ambiguity gate (§4) with words carrying
no relation semantics (`performs`/`wraps`/`requires` never target a topic word). Keeping them in
a separate lexicon preserves `ObjectVocab`'s existing meaning instead of diluting it — see
Alternatives, Alt B.

**Disjointness: none required against `ObjectVocab`/`ProcessLex`.** `TopicLex` is consulted only
inside D1's union-pool resolution, a context where `kind == "skill"` and the `-rules` production
are already fixed — a token sitting in both `TopicLex` and `ProcessLex` (or `ObjectVocab`)
creates no ambiguity there, only redundancy, which `manifest-authoring`'s own registration flow
can flag as a hygiene WARN if it chooses to. This ADR does NOT extend `Grammar.__init__`'s
existing `lexicon_errors` check beyond its current scope (`VerbLex ∩ ProcessLex = ∅`, unchanged)
— an earlier draft claimed a "4-way pairwise disjoint" requirement; that claim is withdrawn as
unnecessary and, worse, would have forced an artificial ordering dependency between D3's seeding
and D4's removal of `check` (which sits in both `VerbLex` and `ObjectVocab` today, with no
violation, because no such cross-lexicon invariant exists in the spec today either).

**Proposed seed (15 entries).** Precise mapping, since "one entry per name" undercounts:
`icon`, `loop`, `motion`, `checking`, `font-token` (compound), `design-md` (compound),
`ops-write-sandbox` (compound), `parallel-work` (compound), `size-and-shape` (compound),
`team-or-solo` (compound), `thinking-depth` (compound), `blocked-by` (compound), `big-change-git`
(compound) — 13 entries, each covering exactly one of 13 `-rules` names — plus `prompt` AND
`wording`, both needed for the ONE remaining name `prompt-wording-rules` (2 entries, 1 name).
15 entries total, covering 14 of the 22 `-rules` names. The other 8 need **zero** new `TopicLex`
entries: 7 are the `{noun}-writing-rules` pattern (D1's "why a union pool" note — `writing` is
already `ProcessLex`), and the 8th, `entry-file-rules`, resolves through **D4's** `entry-file`
addition to `ObjectVocab`, not through `TopicLex` at all — a cross-decision dependency stated
here explicitly so an implementer doesn't look for `entry-file` in the wrong lexicon. Multi-token
compounds are registered whole (mirroring `llm-client`/`site-docs`/`gen-ui`'s existing precedent
in `ObjectVocab`) specifically where the phrase contains a conjunction or preposition
(`size-and-shape`, `team-or-solo`, `blocked-by`) that has no home in any lexicon and never should
— decomposing `"and"`/`"or"`/`"by"` into registered tokens would be governance theater over
grammatical glue words, not domain vocabulary.

### D4 — `ObjectVocab` grows by 12 entries; `check` itself is REMOVED from it

Proposed additions, each covering exactly one currently-exempt (or currently-accidentally-passing)
`check-<noun>` name once D2 lands: `entry-file` (compound — also closes a standing spec/manifest
inconsistency: §4's own worked example text already cites `entry-file` as an `ObjectVocab`
illustration, but it was never actually added to the manifest), `routing`, `state`, `focus`,
`safety`, `speed`, `translation` (plural `translations`), `color` (plural `colors`), `isolation`,
`a2a`, `ui-change` (compound — registered whole rather than decomposing `ui` + the too-generic
bare word `change`, which would invite unrelated future collisions), and **`stage`** — needed
specifically to keep `check-stage` (Context above) resolving once `check` is removed; `stage`
already sits in `ProcessLex` for other object-process skill names, and registering it in
`ObjectVocab` too is deliberate, harmless dual membership (no disjointness invariant forbids it —
see D3 above), not an oversight. **Removed:** the `check` entry PR #345 added — D2's reserved
head supersedes the reason it was registered; leaving it in `ObjectVocab` too would let a skill
named e.g. `check-check` or a stray nominal phrase abuse `check` as an ordinary noun, which was
never the intent.

### What does NOT change

- Command grammar (§3.1), agent grammar (§3.3), the `-agent` reserved head, the reverse-wrapper
  amendment (§14.1) — untouched, independent productions.
- The plain nominal-phrase fallback for every skill name that is neither `-rules`-tailed nor
  `check-`-headed — unchanged, still `ObjectVocab`-only.
- `VerbLex ∩ ProcessLex = ∅` — unchanged, and not extended: `TopicLex` carries no new
  disjointness requirement against any existing lexicon (D3 above).
- ADR-0011 D8's grandfather-and-ratchet migration posture — unchanged; this is additive
  registration, the exemptions array still only ever shrinks.
- **4 exemptions this ADR deliberately does NOT retire:** `check-all-agents`, `check-all-skills`,
  `check-everything`, `check-whole-ui`. Their non-tail tokens (`all`, `everything`, `whole`) are
  quantifiers, not domain objects — minting a `QuantifierLex` for 3 idiomatic superlative names is
  disproportionate to the recurring-pattern problem this ADR exists to fix. They stay exempt;
  cited explicitly so a future pass doesn't read their continued exemption as an oversight.
- No file under `naming.manifest.json` or `authorkit/skills/naming-audit/scripts/validate.py`
  changes as part of landing this ADR — see the header note and Consequences.

### Exemptions retired once D1–D4 are implemented and ratified

| Class | Exempted today | Retired by this design | Stays exempt (named non-goal) |
|---|---|---|---|
| `-rules` | 22 | 22 (all) | — |
| `check-<noun>` | 14 | 10 | 4 (`check-all-agents`, `check-all-skills`, `check-everything`, `check-whole-ui`) |
| **Total** | **36** | **32** | **4** |

(`check-doc`, `check-skill`, `check-stage`, `naming-rules`, `product-lifecycle-rules` all already
parse clean today — none counted as "retired": none were ever in the exemptions array. Their
passing reason changes from accidental to designed under D1/D2/D4, and D4's `stage` addition is
what keeps `check-stage` passing at all once `check` is removed — see D2 and D4 above.)

### Alternatives considered

- **Alt A — `-rules` prefix fully unconstrained (no `TopicLex`, no lexicon check at all beyond
  banned/brand).** Cheapest to implement. Killed: sacrifices §5 rule 4's "every token must
  resolve" invariant for exactly this one class — a typo'd or synonym-drifted `-rules` name (or a
  future `-rules` name someone mints for a topic that should have used an existing `ObjectVocab`
  word instead) would never be caught, which is the exact drift class the closed-lexicon
  discipline exists to prevent everywhere else.
- **Alt B — Fold the new topic words straight into `ObjectVocab` instead of a separate
  `TopicLex`.** Fewer moving parts. Killed: conflates two contracts — `ObjectVocab` membership
  carries relation semantics (`performs`/`wraps`/`requires` target these names meaningfully);
  `-rules` topic words carry none. Folding them in lets `ObjectVocab`'s own registration-ambiguity
  gate (§4) face collisions from words that were never meant to be "things the tooling
  manipulates," and blurs what future authors should expect `ObjectVocab` to mean.
- **Alt C — Generalize `check-` into a full `VerbLex`-head production for skills** (any `VerbLex`
  verb may front-load a skill name, not just `check`). Killed: breaks the invoker-mood
  decidability §2 is built on ("the grammatical mood of a name mirrors how the artifact is
  invoked"). §14.1's own reverse-wrapper amendment already licenses exactly one narrow way for a
  skill name to carry a verb-shaped token — a `VerbLex`-terminal skill name, and ONLY when an
  identically-named command in the same plugin root wraps it (the wrapper's existence is the
  license, explicitly not a general grant). Generalizing `check-` to every `VerbLex` verb opens
  a SECOND, broader avenue for verb-shaped skill names that needs no such wrapper precondition —
  undermining §14.1's own narrowness rationale and making "is this a skill or could it be read as
  command-shaped" no longer decidable from the lexicon alone, since any `VerbLex` member could
  now head either kind. Narrower is correct here: one literal reserved head (`check`, closed,
  ratified one entry at a time like `RoleLex`), not a lexicon-wide production.
- **Alt D — Do nothing; keep grandfathering both classes under D8's ratchet indefinitely.** Zero
  implementation cost, zero risk. Killed: this is the status quo issue #353 was filed against —
  D8's ratchet is correct for one-off legacy debt, wrong for a *recurring, predictable* shape a
  human keeps re-minting; declining to register the pattern means every future `-rules` standards
  skill or `check-<noun>` report generator re-earns a hand exemption forever, which is exactly the
  toil this ADR exists to retire.

## Consequences

- **Nothing executes from this ADR alone.** Status stays `proposed` until Kim ratifies (this ADR
  is never self-ratifying, per docs' ledger-class contract — an accepted ADR is append-only, so
  the flip itself is the ratification act).
- **On ratification, the follow-on execution (a separate ticket, authorkit-owned per the resolved
  owner boundary above) is:** (1) implement D1/D2 in `validate.py`'s `Grammar.parse` skill branch,
  both inserted before the existing object-process check (D1/D2's insertion-point notes above),
  plus the `resolve_objects_union` helper — no lexicon-disjointness extension needed (D3); (2) seed
  `TopicLex` (D3) and the 12 `ObjectVocab` additions, remove `check` (D4), in
  `naming.manifest.json`; (3) add validator selftest fixtures mirroring the existing
  reverse-wrapper-amendment pattern (§14.1's positive/negative/regression triad) for both new
  productions; (4) re-run `authorkit:naming-audit` estate-wide and confirm exactly the 32 named
  exemptions clear with zero new grammar errors; (5) shrink `naming.manifest.json`'s exemptions
  array by those 32 entries via `authorkit:/exemption-retire`; (6) append a dated `§14.2` to
  `.claude/docs/spec/spec-naming-convention.md` documenting the ratified amendment, mirroring
  `§14.1`'s own pattern (ruling authority, validator-change description, non-goals) — the spec
  itself is edited only at that point, under a real Sign-off, never as part of this design pass.
- **Easier, once landed:** every future `-rules` standards skill and every future
  `check-<noun>` report/audit skill mints clean from day one, with no hand exemption and no
  `naming-audit` "systemic gap" line item.
- **Harder, once landed:** `ObjectVocab` and the new `TopicLex` both carry slightly more entries
  to keep straight, including one deliberate dual-membership (`stage`, in both `ObjectVocab` and
  `ProcessLex` — D3/D4) an implementer must not "clean up" by removing either registration.
- **Irreversible in the ratchet sense:** once the 32 exemptions retire per D8's shrink-only rule,
  they may never be re-added to `exemptions` — a future regression in one of those 32 names would
  have to be fixed forward (rename or re-conform), never grandfathered back in.

### Execution record (2026-08-16, append-only per the ledger-lock contract)

All six follow-on steps named above landed in the same change that ratified this ADR (PR
referencing this ADR and issue #353):

1. D1/D2 implemented in `validate.py`'s `Grammar.parse` skill branch, both inserted before the
   existing object-process check; `resolve_objects_union` added (backed by a shared `_resolve`
   helper so `resolve_objects`/`resolve_objects_union` differ only in which lexicon pool they
   search).
2. `TopicLex` (D3, 15 entries) seeded; the 12 `ObjectVocab` additions registered; `check` removed.
3. Validator selftest fixtures added mirroring §14.1's positive/negative/regression triad for
   both D1 and D2, plus a quantifier-non-goal control and a `stage` dual-membership control (D4).
4. `authorkit:naming-audit`'s validator re-run estate-wide (`--scope grammar`, all 8 plugins +
   the workspace `.claude/skills` tree): 182 artifacts, 0 grammar errors before and after: the
   exact 32 named exemptions now parse clean via grammar (not exemption), the 5 already-clean
   names (`check-doc`, `check-skill`, `check-stage`, `naming-rules`, `product-lifecycle-rules`)
   are unaffected, and the 4 quantifier non-goals remain exempt-only, never grammar-passing.
5. `naming.manifest.json`'s `exemptions` array shrunk by exactly those 32 entries: 156 → 124.
6. `.claude/docs/spec/spec-naming-convention.md` §14.2 added, mirroring §14.1's own pattern.

### Post-execution corrections (2026-08-16, append-only, fresh-context doc-checker findings)

- **Item 4's "182 artifacts" reproducibility, pinned exactly.** Per-plugin `--scope grammar`
  counts, same invocation each: `python3 authorkit/skills/naming-audit/scripts/validate.py
  --target <target> --manifest naming.manifest.json --scope grammar --json`, run once per
  target listed — `agent-protocols` 8, `authorkit` 21, `design` 25, `docs` 21, `harness` 59,
  `llm` 9, `screens` 18, `teamwork` 20, `.claude` 1 (the workspace-root `.claude/skills` tree,
  reached via `--target .claude`, NOT `--target .claude/skills` directly — the latter path
  under-resolves to 0 because `discover()` expects an estate/plugin root, not the `skills/`
  folder itself, and would silently undercount the total by 1). Sum: 182, matching item 4 above
  exactly; 0 grammar errors in every one of the 9 runs, before and after.
- **Item (1)'s "a separate ticket" deviation, named.** The Consequences bullet above (before this
  Execution record) said the follow-on execution would land as "a separate ticket,
  authorkit-owned." It landed instead in this same change, same PR, same commit as the
  ratification itself — Kim's live ratification round authorized executing inline rather than
  opening a second ticket first. The "No file … changes as part of landing this ADR" line earlier
  in this document (Decision section, "What does NOT change") is likewise superseded by this
  Execution record for the same reason: it described the state before ratification, not after.
- **`intent-refs: null` (frontmatter, unchanged by this ratification).** This ADR carries no
  upstream IDR citation, same as ADRs 0001–0013 predating the `intent-refs:` field (doc_lint T6,
  WARN tier — an accepted retrofit debt, not a blocker). No IDR exists for issue #353's
  underlying claim at ratification time; the orphan-WARN is accepted as-is rather than backfilled
  under this change, consistent with T6's own documented retrofit-deferral posture.
