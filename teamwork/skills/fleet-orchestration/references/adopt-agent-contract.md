# The agent-contract-adoption ritual

Shared by every `/lead-*` command that makes the host session run under a dispatched agent's own
contract instead of spawning a copy of it (`leading-planning` ↔ `planner`, `fleet-orchestration` ↔ `fleet-marshal`,
`leading-builds` ↔ `build-leader`). `leading-review` is deliberately NOT a party to this ritual — it adopts
no single agent's contract, on purpose (see its own SKILL.md) — so it does not cite this file.

Each citing skill still owns and states inline: which agent file to read, how many priorities it
carries and their one-line gloss, which co-preloaded skills to invoke alongside it, its own
"three places the host's version differs" list, and its own duration rule (charter-scoped for
`leading-planning`/`fleet-orchestration`, session-scoped for `leading-builds`) — those are genuine per-seat
divergence, not drift, and stay local to each skill.

## The ritual, in four steps

1. **Read the agent file now, in full.** Adopt its contract verbatim as this session's standing
   rules for the adoption's duration. Nothing in that file is optional to skip — a partial
   restatement here would drift from the source the moment either file changes next.
2. **Invoke the skills the agent's own body preloads or soft-mentions**, so the rubrics and
   decision sets its priorities depend on are actually loaded, not assumed.
3. **Acknowledge adoption before doing any real work** — authoring, dispatching, or processing
   the first target: one standing block naming the contract file read, the citing skill's own
   host deltas, and its duration rule.
4. **Re-acknowledge, never stack, on re-invocation — the session-scoped variant only
   (`leading-builds`).** For a session-scoped adoption, re-invocation always lands inside the still-
   open scope, so it always rebinds: re-resolve the target from the new arguments,
   re-acknowledge in one line, continue — never layer a second adoption on top of the first. A
   charter-scoped adoption (`leading-planning`, `fleet-orchestration`) instead follows the second failure
   branch below, which can find the prior charter open OR closed and branches accordingly — the
   two are mutually exclusive by scope, never both live for the same citing skill.

## The two shared failure branches

- **The charter/session turns out smaller than expected once underway** → keep working under the
  adopted contract anyway; do not silently revert to solo-first mid-charter. If it is genuinely
  done, close it through the citing skill's own closing phase rather than shrinking the
  discipline around what's left.
- **Invoked again while a charter/session bound by an earlier binding is still open** → check the
  citing skill's own coordination records before binding the new one: if they show the prior
  charter never closed, report that it's still open and ask whether this invocation
  closes/replaces it or is a genuinely distinct, parallel one — never silently merge two
  charters' state into one set of records.

## When the rule ends

The adopted discipline holds only for the scope the citing skill itself binds it to (a named
charter, or the session), until that skill's own closing condition fires. A new charter or
session — even later in the same conversation — requires a fresh invocation of the citing
command; none of these commands silently keeps governing unrelated work once its own scope has
closed.
