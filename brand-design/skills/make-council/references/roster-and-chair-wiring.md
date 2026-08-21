# Chair wiring and the critic-shell-agent exception

## Why `council-marshal` is reused, never re-minted, by default

`agents/council-marshal.md`'s own input contract already treats the critic-shell agent as a named
PARAMETER, not a hardcoded fact: "the critic-shell agent's name (e.g. `brand-judge`) and its
deliberation-round output contract" is item 5 of what every dispatch to it must carry. Read its
body end to end — nowhere does it mention brand, brand-judge's severity table, or any brand-
specific artifact type. Its whole contribution is routing, collection, anonymization bookkeeping,
and roll-up formatting — genuinely domain-neutral mechanics, already generalized in the S3 build
this ticket's campaign completed before S4. A new council instance dispatches this SAME agent for
its own phase 2, naming its own critic-shell agent and its own anonymized finding set in the sealed
prompt; nothing about `council-marshal`'s file changes.

**When a new Chair agent would actually be earned (rare):** only if a new domain's phase 2
genuinely needs a contract change to what the Chair collects, routes, or returns — not a
preference, a structural gap (e.g., a domain whose deliberation round needs a fundamentally
different roll-up shape). That is a shared-agent contract change, which touches every existing
consumer (`check-brand-council` included), so it routes to `planner` for a real design decision,
never a silent per-domain fork of `council-marshal`'s body. This is the estate's ordinary
generator/consumer boundary, not a make-council-specific rule.

## Why the critic-shell agent is the ONE exception to "cite, don't restate"

`council-rules`' whole discipline is: state shared machinery once, let every instance configure
around it. A naive reading might conclude a new domain should also "just reuse `brand-judge`" the
way it reuses `council-marshal` — but `brand-judge` is NOT machinery in the same sense. Its
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
5. Dispatch `harness:agent-checker` on the new file before it seats (main procedure step 8) — this
   is a genuinely new prompt-carrying artifact, not a citation of an existing one, so it earns the
   full independent pass `brand-judge` itself already received when it was authored.
