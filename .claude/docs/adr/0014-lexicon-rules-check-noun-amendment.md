---
doc-type: adr
id: adr-0014
status: proposed
date: 2026-08-16
owner: kim.granlund
supersedes: null
intent-refs: null
---
# ADR-0014 — Register a `-rules`/gerund object class and the `check-<noun>` tail in the naming-convention grammar (PROPOSED — pending Kim's review)

> **Not ratified.** This ADR is a design artifact for review (issue #353, CONTESTED by the
> ticket's own framing). Nothing in `naming.manifest.json` or
> `authorkit/skills/naming-audit/scripts/validate.py` changes as part of landing this document.
> Kim's ratification (a status flip to `accepted`) is the only event that authorizes the
> execution follow-on named in Consequences.

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
  `check-ui-change`, `check-whole-ui`). Two siblings — `check-doc`, `check-skill` — already parse
  clean (PR #345 registered `check` itself into `ObjectVocab`), but **by accident, not by
  design**: the nominal-phrase production (spec §3.2/§5, `validate.py`'s `Grammar.parse`, skill
  branch, final fallback) requires *every* token to resolve in `ObjectVocab`, and `doc`/`skill`
  already happened to be registered nouns. `check` sitting in `ObjectVocab` at all is the actual
  defect this ADR retires — "check" is a verb, not a domain object, and registering it as one
  only works for a lucky subset of tails.

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

**Owner boundary (LLD Risk 2, previously unresolved):** resolved by this ADR. Authorship and
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
(TopicLex is new — D3 below). Validator change, precisely: in `Grammar.parse`'s `kind == "skill"`
branch, insert one new branch before the existing nominal-phrase fallback —

```python
if tokens[-1] == "rules" and len(tokens) >= 2:
    ok, why = self.resolve_objects_union(tokens[:-1])   # ObjectVocab ∪ ProcessLex ∪ TopicLex
    if ok:
        return errs
    # falls through to the existing nominal-phrase production on failure — never a
    # regression for a name that already resolves some other way
```

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
answering one question. Validator change, in the same branch, ahead of the nominal fallback:

```python
if tokens[0] == "check" and len(tokens) >= 2:
    ok, why = self.resolve_objects(tokens[1:])   # ObjectVocab only
    if ok:
        return errs
```

This also retroactively fixes `check`'s own presence in `ObjectVocab` (D4 below removes it —
`check-doc`/`check-skill` keep passing, now because D2's head production licenses them, not
because `check` masquerades as a noun).

### D3 — New closed lexicon `TopicLex`

Structurally identical to `RoleLex` (flat list, `naming.manifest.json` top level, governed by
manifest PR, disjoint from `VerbLex`/`ProcessLex`/`ObjectVocab` — `Grammar.__init__`'s existing
`lexicon_errors` disjointness check extends to a 4-way pairwise check, not just
`VerbLex ∩ ProcessLex`). `TopicLex` exists because a `-rules` name's non-tail tokens are
reference-doc *topics* (`icon`, `motion`, `wording`) that the tooling never manipulates as
objects and that would otherwise pressure `ObjectVocab`'s own registration-ambiguity gate (§4)
with words carrying no relation semantics (`performs`/`wraps`/`requires` never target a topic
word). Keeping them in a separate lexicon preserves `ObjectVocab`'s existing meaning instead of
diluting it — see Alternatives, Alt B.

**Proposed seed (15 entries, covering the 15 `-rules` names D1's union pool doesn't already
resolve via existing `ObjectVocab`/`ProcessLex` membership):** `icon`, `loop`, `motion`, `prompt`,
`wording`, `checking`, `font-token` (compound), `design-md` (compound), `ops-write-sandbox`
(compound), `parallel-work` (compound), `size-and-shape` (compound), `team-or-solo` (compound),
`thinking-depth` (compound), `blocked-by` (compound), `big-change-git` (compound). Multi-token
compounds are registered whole (mirroring `llm-client`/`site-docs`/`gen-ui`'s existing precedent
in `ObjectVocab`) specifically where the phrase contains a conjunction or preposition
(`size-and-shape`, `team-or-solo`, `blocked-by`) that has no home in any lexicon and never should
— decomposing `"and"`/`"or"`/`"by"` into registered tokens would be governance theater over
grammatical glue words, not domain vocabulary.

### D4 — `ObjectVocab` grows by 11 entries; `check` itself is REMOVED from it

Proposed additions, each covering exactly one currently-exempt `check-<noun>` name once D2 lands:
`entry-file` (compound — also closes a standing spec/manifest inconsistency: §4's own worked
example text already cites `entry-file` as an `ObjectVocab` illustration, but it was never
actually added to the manifest), `routing`, `state`, `focus`, `safety`, `speed`, `translation`
(plural `translations`), `color` (plural `colors`), `isolation`, `a2a`, `ui-change` (compound —
registered whole rather than decomposing `ui` + the too-generic bare word `change`, which would
invite unrelated future collisions). **Removed:** the `check` entry PR #345 added — D2's reserved
head supersedes the reason it was registered; leaving it in `ObjectVocab` too would let a skill
named e.g. `check-check` or a stray nominal phrase abuse `check` as an ordinary noun, which was
never the intent.

### What does NOT change

- Command grammar (§3.1), agent grammar (§3.3), the `-agent` reserved head, the reverse-wrapper
  amendment (§14.1) — untouched, independent productions.
- The plain nominal-phrase fallback for every skill name that is neither `-rules`-tailed nor
  `check-`-headed — unchanged, still `ObjectVocab`-only.
- `VerbLex ∩ ProcessLex = ∅` — unchanged; `TopicLex` joins the disjointness check as a THIRD
  pairwise-disjoint set, never overlapping the other three.
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

(`check-doc`, `check-skill` already parse clean today — not counted as "retired": they were never
in the exemptions array. Their passing reason changes from accidental to designed under D2/D4.)

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
  verb may front-load a skill name, not just `check`). Killed: breaks the invoker-partition
  decidability §2 is built on — a skill name shaped exactly like a command's object-first
  production (`verb-object`, e.g. `create-skill`) would become ambiguous by SHAPE ALONE between
  the two invoker kinds, exactly the confusion the grammar's kind-audible design intentionally
  prevents. Narrower is correct here: one literal reserved head (`check`), not a lexicon-wide
  production.
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
  owner boundary above) is:** (1) implement D1/D2 in `validate.py`'s `Grammar.parse` skill branch
  plus the `resolve_objects_union` helper and the 4-way lexicon-disjointness extension; (2) seed
  `TopicLex` (D3) and the 11 `ObjectVocab` additions, remove `check` (D4), in
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
  to keep straight; the 4-way disjointness check is one more thing `Grammar.__init__` proves on
  every run (cheap, mechanical, already the existing pattern).
- **Irreversible in the ratchet sense:** once the 32 exemptions retire per D8's shrink-only rule,
  they may never be re-added to `exemptions` — a future regression in one of those 32 names would
  have to be fixed forward (rename or re-conform), never grandfathered back in.
