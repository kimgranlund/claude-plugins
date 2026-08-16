# Grammar — productions, lexicons, parse algorithm

## Productions

```
command   := object "-" verb              skill-create, rename-execute
          |  wrapper: skill-name          naming-audit  (iff wraps: that skill)
skill     := object "-" process           skills-audit, rename-planning
          |  topic-phrase "-" "rules"     agent-writing-rules  (§14.2, ADR-0014 D1)
          |  "check" "-" object-phrase    check-routing        (§14.2, ADR-0014 D2)
          |  nominal-phrase               naming-conventions  (all tokens resolve)
agent     := skill-name "-" "agent"       estate-audit-agent  (primary)
          |  scope "-" role "-" "agent"   team-leader-agent   (orchestrators only)
```

Reserved heads/tails on a skill name: `-agent` (agents only, illegal on a skill), `-rules`
(reserved tail, §14.2), `check-` (reserved head, §14.2).

## Kind decision

Directory decides kind (`commands/`, `skills/`, `agents/`); the grammar
corroborates; frontmatter `kind` must agree. Disagreement anywhere is a lint
failure. Frontmatter never breaks a tie.

## Commands — object-first

`skill-create`, not `create-skill`: slash autocomplete groups operations by
object (`/skill-<tab>` surfaces every skill operation together). Terminal
token ∈ VerbLex. Objects of imperatives pluralize where natural
(`sweep-issues`); attributive objects do not (`issue-triage`).

**Wrapper production:** a command whose sole job is exposing a skill to the
user carries the skill's exact name and declares `wraps:` it. The `/` surface
disambiguates command from skill; the validator accepts the name by wrapper
identity, bypassing the object-verb shape.

## Skills

Canonical: `{object}-{process}`, terminal ∈ ProcessLex. Reference corpora,
routers, and report generators use the nominal production: every token must
resolve in ObjectVocab — the looseness is in the shape, never the vocabulary.

Reading tests: procedural — "this teaches how to do ___"; reference-shaped —
"consult ___ for this."

## Agents

Primary: `{existing-skill-name}-agent`; the peer audit strips `-agent` and
asserts the skill exists. An agent's capability must have an authored skill
spec. Escape hatch: `{scope}-{role}-agent` for orchestrators only (no patient
object); RoleLex stays ≤ 4 entries.

## Lexicons

| Lexicon | Membership | Governance |
|---|---|---|
| VerbLex | command terminals | closed; PR to change |
| ProcessLex | skill terminals | closed; PR to change |
| RoleLex | orchestrator roles | closed; ≤ 4 |
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

1. Strip the reserved head `-agent`, if present. What was stripped fixes kind
   candidacy.
2. Longest-match resolve remaining tokens against ObjectVocab, greedy,
   left-anchored (multi-token entries like `ui-layout` match before their
   prefixes).
3. Classify the terminal token of the residue against VerbLex / ProcessLex /
   RoleLex per the kind's production.
4. Every token must resolve. Anything in no lexicon and no vocab entry fails.

Ambiguity is prevented at write time: ObjectVocab registration rejects
entries that would make step 2 ambiguous.
