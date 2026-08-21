# Chair wiring, the critic-shell-agent exception, and role-agent wiring

## Why `council-chair-agent` is reused, never re-minted, by default

`agents/council-chair-agent.md`'s own input contract already treats the critic-shell agent as a named
PARAMETER, not a hardcoded fact: "the critic-shell agent's name (e.g. `brand-judge`) and its
deliberation-round output contract" is item 5 of what every dispatch to it must carry. Read its
body end to end — nowhere does it mention brand, brand-judge's severity table, or any brand-
specific artifact type. Its whole contribution is routing, collection, anonymization bookkeeping,
and roll-up formatting — genuinely domain-neutral mechanics, already generalized in the S3 build
this ticket's campaign completed before S4. A new council instance dispatches this SAME agent for
its own phase 2, naming its own critic-shell agent and its own anonymized finding set in the sealed
prompt; nothing about `council-chair-agent`'s file changes.

**When a new Chair agent would actually be earned (rare):** only if a new domain's phase 2
genuinely needs a contract change to what the Chair collects, routes, or returns — not a
preference, a structural gap (e.g., a domain whose deliberation round needs a fundamentally
different roll-up shape). That is a shared-agent contract change, which touches every existing
consumer (`check-brand-council` included), so it routes to `planner` for a real design decision,
never a silent per-domain fork of `council-chair-agent`'s body. This is the estate's ordinary
generator/consumer boundary, not a make-council-specific rule.

## Why the critic-shell agent is the ONE exception to "cite, don't restate"

`council-rules`' whole discipline is: state shared machinery once, let every instance configure
around it. A naive reading might conclude a new domain should also "just reuse `brand-judge`" the
way it reuses `council-chair-agent` — but `brand-judge` is NOT machinery in the same sense. Its
contract shape (inlined-only input, cold-read method, severity table, deliberation-round contract)
IS shared and worth copying faithfully — but its actual IDENTITY (its name, its description, and
arguably its severity-table wording if a domain's judgment calls for a different scale) is
per-instance configuration, exactly like the roster it embodies. Two agents both literally named
`brand-judge` fanned out for two different domains would be confusing at the dispatch call site
(which domain is this dispatch even for?) and would tie a non-brand domain's critic shell to a
brand-specific name forever. So: **pattern a new critic-shell agent off `brand-judge`'s structure,
under its own domain-appropriate name** — this is configuration-by-copying, not the restatement
`council-rules` warns against, because `council-rules` never claimed critic-shell AGENT BODIES as
its own shared machinery in the first place (it explicitly leaves "the critic-shell agent's
model/tool tier" to the domain instance, per its own "what a domain instance supplies" table).

## Practical wiring checklist for a new domain

1. Copy `brand-judge`'s frontmatter and body structurally: `tools: Read, Grep, Glob`, `model:
   fable`, `effort: medium` (the same Review/hard-bug-analysis tier — `harness:agent-writing-rules`'
   ladder, unchanged by domain) unless the new domain's judgment task is demonstrably lighter or
   heavier weight, stated explicitly if so.
2. Rename: the agent file, its `name:` field, its description's council/domain reference.
3. Keep the input contract's SHAPE (inlined persona, inlined artifact, inlined context; the
   deliberation-phase additions) verbatim — only the domain noun changes.
4. Keep the severity table's STRUCTURE (four tiers, escalating) — the LABELS may stay
   Critical/Major/Minor/Noise (recommended, for cross-domain legibility) or adapt to the domain's
   own convention if one already exists elsewhere in that domain's plugin, stated explicitly either
   way.
5. Dispatch `harness:agent-checker` on the new file before it seats (main procedure step 9) — this
   is a genuinely new prompt-carrying artifact, not a citation of an existing one, so it earns the
   full independent pass `brand-judge` itself already received when it was authored.

## Role-agent wiring — a second per-instance agent family, patterned off `council-strategy-agent`

A council instance needs a critic-shell agent (above) AND a separate agent family: one **role
agent** per ordinary sub-council, the addressable external seat `council-rules`'
`references/role-agents.md` describes (concept and convene semantics, cited not restated). These
are NOT the same exception restated twice — a critic-shell agent is dispatch-only, fanned out
unnamed by an orchestrating procedure, embodying ONE persona per call; a role agent is dispatched
directly, by name, and itself orchestrates a fan-out over an entire sub-council. Both are
per-instance configuration for the same underlying reason (`council-rules` never claimed either
agent family as its own shared machinery — it explicitly leaves both to the domain instance), but
they are minted, checked, and reasoned about separately.

**Why `council-strategy-agent` is the pattern source, not a new invention:** it is brand's own
first worked instance of this agent family — read it end to end and nowhere does it mention brand
beyond its own domain noun (`strategy`) and the `check-brand-council`/`brand-judge` names it cites
as the roster/critic-shell it wraps. Copying its structure for a new domain is the same
configuration-by-copying `brand-judge`'s own exception already establishes, applied to a second
agent family.

### Practical wiring checklist — one role agent per ordinary sub-council

1. Copy `council-strategy-agent`'s frontmatter and body structurally: `tools: Read, Grep, Glob,
   Agent`, `model: sonnet`, `effort: medium` (the same bounded collection-and-roll-up tier as
   `council-chair-agent` — this agent orchestrates, it never itself judges) unless the new domain's
   convene job is demonstrably heavier, stated explicitly if so.
2. Rename: the agent file, its `name:` field, every sub-council/domain-noun mention throughout
   (roster path, sub-council name in the Method steps, the blind-spot synthesis line, the output
   contract's header) — the SHAPE stays verbatim, only the noun changes. Do this once per ordinary
   sub-council; a domain with three sub-councils mints three role agents, never one shared agent
   parameterized by an argument (that would reopen the same "which domain is this dispatch even
   for" ambiguity `brand-judge`'s own exception already rejected for critic shells).
3. Keep the Method's SHAPE verbatim: resolve the roster, empty/VACANT-bench clean stop, unnamed
   same-turn fan-out to the new critic-shell agent (never a different domain's), bounded rejection,
   verbatim collection, 2-of-3 voting scoped to the SAME sub-council, the five synthesis shapes
   scoped to this lens, phase-1-only (deliberation stays the convening skill's own job).
4. **Never mint one for `full` or `advisory`** — `role-agents.md`'s reserved-name rule, mechanically
   enforced by `roster_check.py` on the `## Role agents` section too.
5. Add its row to the new `roster.md`'s `## Role agents` section (main procedure step 3) — the key
   is the sub-council's own token, the value is the new agent's `name:` handle.
6. Dispatch `harness:agent-checker` on the new file before it seats (main procedure step 9) — same
   independent-pass requirement as the critic-shell agent, once per role agent minted.
