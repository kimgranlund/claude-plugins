# Action risk tiers — classify by reversibility and blast radius, gate accordingly

> Axis: partition the actions an agent might take (not the instructions it receives — see
> injection-defense-and-instruction-source-boundary for that distinct concern) into a small,
> fixed set of tiers by how reversible and how widely visible each is, and bind a different
> default behavior to each tier rather than one blanket "ask" or "just do it" rule. Grounded in
> two independently observed real harness variants that converge on the same structural pattern,
> plus a third instance in this file (sources.md's fourth overall) on a distinct claim: that
> classifying an action's tier correctly is not sufficient — a delegated worker's FULL reachable
> action set needs the same enumeration, not just the one action a delegator happened to name.

## The pattern — a small fixed set of tiers, each with its own bound behavior

**Claim — the number of tiers that matters is small (two to three), and each tier is bound to a
DIFFERENT default, not a shared "be careful" instruction:** something the agent may simply do,
something it must explicitly ask permission for and wait for a clear yes before doing, and
(optionally, once the harness can reach such an action at all) something it must never do and
should instead redirect the user to do themselves. **Why three distinct behaviors, not degrees of
one:** collapsing "ask first" and "never do this" into one bucket either makes the agent annoying
(asking about everything reversible) or, far worse, lets a catastrophic action slip through
because it merely got flagged the same way a routine confirmation would.

## Worked instance A — the three-tier form, reported from the dispatching harness

**Observed-harness-behavior citation (reported at dispatch time from the assistant that spawned
this authoring session; see `sources.md` for why this is a distinct trust class from a verified
file `path:line`):** a real harness defines exactly three tiers — **Prohibited** (never perform,
direct the user instead — e.g. entering financial credentials, permanently deleting data,
executing financial trades), **Explicit permission required** (ask in chat, wait for a clear yes,
then act — e.g. sending a message on the user's behalf, purchasing goods, accepting terms,
clicking an irreversible action control), and **Regular** (anything not in the lists above may
proceed without confirmation).

## Worked instance B — the same shape, independently verified in this session's own prompt

**Observed-harness-behavior citation (this session's own live "Executing actions with care"
instructions — the SAME trust class as Worked instance A above, not a re-openable file; see
`sources.md`), 2026-07-13:** a parallel three-way split — actions that are **destructive**
(deleting files/branches, dropping
tables, `rm -rf`, overwriting uncommitted changes), **hard-to-reverse** (force-push, `git reset
--hard`, amending published commits, removing dependencies), and **visible to others / affecting
shared state** (pushing code, commenting on a PR, sending a message, modifying shared
infrastructure) — each named as warranting confirmation before proceeding, with everything outside
those categories free to proceed. **Why two independently-worded frameworks converging on the same
tier COUNT and the same qualitative split is the actual finding here, not either list's exact
wording:** the categories differ (reversibility vs. blast-radius vs. visibility-to-others as named
axes), but both harnesses land on "one small set of named risk classes, each bound to a specific
required behavior" rather than a single vague "use judgment" instruction — that convergence is
what makes this a pattern worth reusing, not a license to copy either list verbatim into an
unrelated harness.

## The axes that actually predict which tier an action belongs in

Three questions, asked together, place an action in the pattern above: **is it reversible** (can
the agent or user undo it without external help)? **does it affect only the current
session/sandbox, or a shared/external system** (a git branch on the user's laptop vs. a pushed
commit, a draft vs. a sent message)? **is it visible to a third party** (a Slack message a
teammate reads, a comment on a public issue)? An action failing more than one of these questions
skews toward "explicit permission" at minimum; an action that is irreversible AND externally
consequential AND cannot be meaningfully undone by anyone (a real-money transaction, permanent
deletion of the only copy of data) is the shape "Prohibited" exists for.

## Small-scale calibration

A minimal single-user harness needs, at minimum, a two-way split — proceed silently vs. ask
first — the moment it can take any action at all. A third, flatly-refuse tier only earns its
complexity once the harness can reach an action that is illegal, irrecoverable, or harms someone
who isn't the user regardless of what the user confirms (moving real money, permanently deleting
shared data); a harness with no such reachable action can validly skip that tier, but should say
so explicitly in its own instructions rather than silently having no floor at all.

## Delegated actions need per-action enumeration, not inherited scope from one action

**Observed-harness-behavior citation (a CLI-harness dispatch incident, `sources.md`'s fourth worked
instance, 2026-07-20 — cited for the principle, not as chat-agent evidence; the specific tools
involved are CLI-only and don't exist in a chat-agent's toolset):** a worker was restricted on one
Explicit-Permission-tier action, said nothing about a second action of the SAME tier the worker
could also reach — and two separately-dispatched workers each performed that unnamed sibling
action, in the same session, before the dispatching pattern was corrected. The failure was not misjudging a tier; both
actions were correctly Explicit-Permission-tier on their own. The failure was assuming a
restriction stated for one action implicitly covers a sibling action nobody named.

**Why this is a distinct claim from the tier-classification claims above:** everything else in this
file answers "which tier does THIS action belong in" — a single-action question. This claim is
about COVERAGE across a delegated task's full reachable action set: a worker executing a multi-step
task may reach several Explicit-Permission or Prohibited-tier actions along the way, and naming one
of them is not a proxy for naming all of them. A harness that gates delegation by exception
("everything's fine except X") rather than by enumeration ("only these named actions are
authorized, ask about everything else in tier ≥ Explicit-Permission") reproduces this failure by
construction — the worker never violates the one rule it was given, and still does something no one
approved.

**Chat-agent-native worked scenario (illustrative, not a re-openable citation):** an orchestrating
chat agent delegates "resolve this customer's shipping complaint" to a specialized sub-agent or
tool-use chain with its own `issue_refund`, `close_ticket`, and `apply_loyalty_credit` tools. The
delegator's instruction says "confirm with the customer before issuing a refund" — correctly gating
the one action it named. Nothing constrains `close_ticket` or `apply_loyalty_credit`, both
externally-visible actions affecting the customer's account and shared state (the same axes scored
above). The sub-agent, having correctly never issued an unconfirmed refund, closes the ticket and
applies a credit adjustment on its own — technically compliant with the one instruction it
received, and still an unauthorized action by the harness's own risk-tier standard. The fix is the
same structural discipline the tier-classification sections above already establish, applied at the
DELEGATION boundary specifically: a dispatch to a worker with tool access states its full
authorized-action set explicitly (name every action at Explicit-Permission tier or above the worker
might reach, not just the one the delegator happened to think of first), rather than restricting by
naming only the one action that prompted the guardrail and leaving every sibling action's tier to
the worker's own inference.

## What this file does NOT cover

Whether the REQUEST driving an action even came from a valid source in the first place — this
file assumes that question is already settled
(injection-defense-and-instruction-source-boundary) · turning a "Prohibited" or "ask" tier into an
actual enforced check the model cannot be talked past, rather than a prompted rule it might forget
under a clever enough framing (deterministic-rules-vs-prompted-guidance) · whether a tier boundary
is hardcoded in prose or a configurable setting a deployer can tighten or loosen
(config-precedence-and-setup).
