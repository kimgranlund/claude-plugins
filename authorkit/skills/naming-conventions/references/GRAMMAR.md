# Grammar — productions, lexicons, parse algorithm

## Productions

```
command   := object "-" verb              skill-create, rename-execute
          |  wrapper: skill-name          naming-audit  (iff wraps: that skill)
          |  ("bind"|"fork"|"sub") "-" scope   bind-team, fork-agent, sub-agent (reserved
                                          heads, §14.5, ADR-0020 D3 — supersedes `lead-`)
          |  "lead" "-" scope             RETIRED (ADR-0020 D3; open production removed
                                          outright, no grandfather set — wave 5/#523
                                          renamed the six former live names to bind-{scope})
skill     := object "-" process           skills-audit, rename-planning
          |  topic-phrase "-" "rules"     agent-writing-rules  (§14.2, ADR-0014 D1)
          |  "check" "-" object-phrase    check-routing        (§14.2, ADR-0014 D2)
          |  "make" "-" object-phrase     make-doc             (§14.7, ADR-0018 D1)
          |  "file" "-" object-phrase     file-bug             (§14.7, ADR-0018 D1)
          |  nominal-phrase               naming-conventions  (all tokens resolve)
agent     := skill-name "-" "agent"       estate-audit-agent  (primary)
          |  scope "-" role               team-leader         (orchestrators — canonical, ADR-0015 D1)
          |  scope "-" role "-" "agent"   product-leader-agent (orchestrators — legacy spelling, ADR-0015 D1)
```

Reserved heads/tails on a skill name: `-agent` (agents only, illegal on a skill), `-rules`
(reserved tail, §14.2), `check-` (reserved head, §14.2), `bind-`/`fork-`/`sub-` (reserved
heads, §14.5, ADR-0020 D3 — defined on the command grammar and recognized on the skill parse
too, since the surfaces ship as a mix of true commands and command-species skills), `lead-`
(RETIRED as an open production, §14.5, ADR-0020 D3 — no grandfather set left as of wave 5/#523:
the six former live `/lead-*` names all renamed to `bind-{scope}`, `LEAD_HEAD_GRANDFATHER` and
its two parse branches deleted outright; any `lead-*` mint now fails, old name or new), `make-`/
`file-` (reserved heads, §14.7, ADR-0018 — residue resolves against ObjectVocab only). The
literal head set is closed at exactly `{check, bind, fork, sub, make, file}` — never a template
for other VerbLex members.

## Kind decision

Directory decides kind (`commands/`, `skills/`, `agents/`); the grammar
corroborates; frontmatter `kind` must agree. Disagreement anywhere is a lint
failure. Frontmatter never breaks a tie.

## Commands — object-first

`skill-create`, not `create-skill`: slash autocomplete groups operations by
object (`/skill-<tab>` surfaces every skill operation together). Terminal
token ∈ VerbLex. Objects of imperatives pluralize where natural
(`sweep-issues`); attributive objects do not (`issue-triage`).

**`bind-`/`fork-`/`sub-` reserved heads (§14.5, ADR-0020 D3):** `{head}-{scope}` conforms
when `{scope}` resolves against the orchestrator scope pool (ObjectVocab ∪ ProcessLex,
ADR-0015 D2's pool — the command makes the session adopt the orchestrator seat whose scope
that is; the head names which platform mechanic does the adopting: `bind-` seat adoption
in-session, `fork-` a `context: fork`, `sub-` an `Agent` dispatch). Each head is a literal,
exactly like `check-`: not a VerbLex member, never a template for other verbs. These three
supersede `lead-` (ADR-0016 D1/D2), retired below.

**`lead-` retired (§14.5, ADR-0020 D3, 2026-08-17; grandfather set removed wave 5/#523):** no
`lead-{scope}` mint conforms, even when `{scope}` resolves fine in the orchestrator scope pool.
Between wave 2 (#520, which could not rename the six live `/lead-*` surfaces in the same change)
and wave 5 (#523, which did), those six parsed via a closed, never-grown grandfather set
(`LEAD_HEAD_GRANDFATHER` in `validate.py`) rather than the shrink-only `exemptions` array
(ADR-0011 D8). Wave 5 renamed all six to `bind-{scope}` and deleted the grandfather set plus
both `lead-` code branches outright — deprecated scaffolding, never a permanent third mechanism.

**Wrapper production:** a command whose sole job is exposing a skill to the
user carries the skill's exact name and declares `wraps:` it. The `/` surface
disambiguates command from skill; the validator accepts the name by wrapper
identity, bypassing the object-verb shape.

**Reverse-wrapper on skills (§14.1, extended §14.9):** a skill MAY carry a verb-terminal name
(terminal ∈ VerbLex, not ProcessLex) when EITHER an identically-named command wraps it (§14.1's
original dual-access realization) OR the skill itself is `user-invocable: true` with no sibling
command at all (§14.9's skill-as-command realization, issue #525 — the successor dual-access
shape carries both surfaces on one file). Object-prefix resolution against ObjectVocab still
applies either way — the license is the dual-access fact, never the skill's say-so alone.

## Skills

Canonical: `{object}-{process}`, terminal ∈ ProcessLex. Reference corpora,
routers, and report generators use the nominal production: every token must
resolve in ObjectVocab — the looseness is in the shape, never the vocabulary.

Reading tests: procedural — "this teaches how to do ___"; reference-shaped —
"consult ___ for this."

## Agents

Primary: `{existing-skill-name}-agent`; the peer audit strips `-agent` and
asserts the skill exists. An agent's capability must have an authored skill
spec. Orchestrator production (no patient object): `{scope}-{role}` is
canonical (ADR-0015 D1 — the role noun is already the agent marker, so the
`-agent` tail is redundant on this production only); `{scope}-{role}-agent`
remains a legal legacy spelling, never rejected, not chosen for new mints.
`scope` resolves against ObjectVocab ∪ ProcessLex (ADR-0015 D2 — a seat
coordinates a thing or a process); RoleLex is disjoint from ObjectVocab ∪
ProcessLex (ADR-0015 D3) and covers execution seats as well as coordinators
(ADR-0017, §14.6, 2026-08-17) — `leader`, `orchestrator`, `coordinator`,
`checker`, `runner`, `planner`, `watcher`, `finder`, `sorter`, `cleaner`,
`judge`, `builder`, `writer`, `marshal`, `chair`, `convener` (ADR-0020, 2026-08-17; `chair`/`convener`
added 2026-08-21 — see `naming.manifest.json`'s `role_lex`, and the resolution note below). A bare
RoleLex word with no scope token still fails — the production always requires `{scope}-{role}`,
never a bare role.

**Resolving a RoleLex/ObjectVocab collision.** A new agent name sometimes fails to parse because
one of its candidate tokens already sits in the OTHER lexicon — the disjointness invariant then
makes that word permanently unreachable on the blocked side. The worked resolution, twice
precedented: register the colliding word on the side that actually matches its nature — never
force it through with an exemption (the exemptions array is shrink-only; grandfathering a
brand-new name defeats the ratchet), and never leave some siblings fixed while one stays
permanently blocked.
- **The word IS a domain object → ObjectVocab.** `muse-agent` (S4, `#827`, 2026-08-20): `muse`
  names a thing (the aspirational seat's own subject), so it registered to ObjectVocab to support
  the `{skill}-agent` production — no new RoleLex word needed.
- **The word IS a generic profession, but the RESIDUE token collides → mint a new RoleLex word
  and shift the domain noun to `{scope}`.** `chair`/`convener` (`#843`, 2026-08-21):
  `council-design-agent` couldn't resolve because `design` was already ObjectVocab-registered
  elsewhere, blocking that residue from ever reaching RoleLex. `convener` (a generic profession
  word, mirroring `marshal`/`judge`; `chair` registered in the same change for
  `council-chair-agent`, the `{scope}-{role}-agent` legacy spelling) was registered to RoleLex
  instead, and the four lens agents renamed to `<lens>-convener` — `design` now serves as
  `{scope}`, where disjointness never applies.

## Lexicons

| Lexicon | Membership | Governance |
|---|---|---|
| VerbLex | command terminals | closed; PR to change |
| ProcessLex | skill terminals | closed; PR to change |
| RoleLex | orchestrator + execution-seat roles | closed; count/membership canonical in `naming.manifest.json`'s `role_lex` (currently 16), enumerated above; disjoint from ObjectVocab ∪ ProcessLex (ADR-0015 D3, ADR-0017, ADR-0020) |
| ObjectVocab | domain objects | registered; anti-ambiguity gate |
| TopicLex | `-rules` reference-doc topic words (§14.2) | closed; PR to change |

**Disjointness invariant:** VerbLex ∩ ProcessLex = ∅. Position plus membership
decides kind; a token in both would break that. TopicLex carries no such
requirement — it's consulted only inside the `-rules` production's own
union-pool resolution (ObjectVocab ∪ ProcessLex ∪ TopicLex), where a token in
more than one pool is redundant, never ambiguous. ObjectVocab entries register
canonical form, plural, and banned aliases (`pr`, never `pull-request`).
`banned_aliases` scopes to artifact NAMES only — it governs what token a
command/skill/agent name may use, never general prose, documentation, or
conversational wording, which may still say "pull request" freely.
Brand tokens (`adia`, `authorkit`) are banned from local names — the
marketplace prefix supplies the namespace; embedding brand double-prefixes.

## Parse algorithm (normative — implement exactly this)

1. Strip the reserved head `-agent`, if present. For the primary production
   (and a skill's own reserved-head rejection) what was stripped still fixes
   kind candidacy; for a bare orchestrator name (ADR-0015 D1) there is nothing
   to strip — kind candidacy then comes from the directory (`agents/`) plus a
   RoleLex terminal, tried alongside the stripped form rather than instead of
   it.
2. Longest-match resolve remaining tokens against ObjectVocab (commands,
   skills, the primary agent production) — or, for the orchestrator agent
   production's scope phrase specifically, against ObjectVocab ∪ ProcessLex
   (ADR-0015 D2) — greedy, left-anchored (multi-token entries like `ui-layout`
   match before their prefixes).
3. Classify the terminal token of the residue against VerbLex / ProcessLex /
   RoleLex per the kind's production.
4. Every token must resolve. Anything in no lexicon and no vocab entry fails.

Ambiguity is prevented at write time: ObjectVocab registration rejects
entries that would make step 2 ambiguous.
