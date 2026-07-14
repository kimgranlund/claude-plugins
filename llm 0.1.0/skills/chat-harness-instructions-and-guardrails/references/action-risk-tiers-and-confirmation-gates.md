# Action risk tiers — classify by reversibility and blast radius, gate accordingly

> Axis: partition the actions an agent might take (not the instructions it receives — see
> injection-defense-and-instruction-source-boundary for that distinct concern) into a small,
> fixed set of tiers by how reversible and how widely visible each is, and bind a different
> default behavior to each tier rather than one blanket "ask" or "just do it" rule. Grounded in
> two independently observed real harness variants that converge on the same structural pattern.

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

## What this file does NOT cover

Whether the REQUEST driving an action even came from a valid source in the first place — this
file assumes that question is already settled
(injection-defense-and-instruction-source-boundary) · turning a "Prohibited" or "ask" tier into an
actual enforced check the model cannot be talked past, rather than a prompted rule it might forget
under a clever enough framing (deterministic-rules-vs-prompted-guidance) · whether a tier boundary
is hardcoded in prose or a configurable setting a deployer can tighten or loosen
(config-precedence-and-setup).
