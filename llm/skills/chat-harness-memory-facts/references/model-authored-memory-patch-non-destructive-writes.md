# Model-authored memory writes must be non-destructive by construction

> Axis: when a model itself is allowed to propose a write to durable, cross-session memory (not
> just read it), what write semantics keep a hallucinated or malformed patch from destroying
> state. Grounded in a worked instance: `@agent-ui/a2ui`'s persona-patch envelope,
> `packages/agent-ui/a2ui/src/agent/meta-line.ts`.

## Merge law: last-writer-wins scalars, append-only lists, no deletes

**Claim — a persona patch is a model-declared delta with a partial-record merge law: scalar
`values` merge last-writer-wins at whole-value granularity (an absent key stays untouched, no
deep merge); list `entries` APPEND through the host's validated add path, never replace; no
delete semantics exist in v1.** Intent (set vs. contribute) is declared structurally by which arm
of the patch is used, never inferred from a key-name table. Because there is no delete path, a
hallucinated patch cannot destroy existing state — the worst it can do is add a wrong scalar or
list entry, both individually correctable, never a silent full-record loss. ·
`meta-line.ts:93-109` (ADR-0178/SPEC-R29) · 2026-08-17 · [verified]

## The wire is gate-blind; the GATE governs consumption and teaching, never framing

**Claim — a volunteered patch on a gate-OFF turn still rides the envelope unchanged; what the
gate withholds is host-side CONSUMPTION (a separate three-filter apply step) and the prompt's
teaching block, never the wire framing itself.** Splitting the gate this way leaves zero
gate-conditional wire branches to drift — the envelope's shape never depends on whether this
particular deployment currently has the memory feature turned on. · `produce.ts:167-177,594-600`
· 2026-08-17 · [verified]

## What this file does NOT cover

Keeping the AMBIENT disclosure cost of a capability roster cheap while switchable — a related but
distinct concern about read-side cost, not write-side safety:
`capability-availability-tiering-and-ambient-cost.md`. The envelope's own structural discriminator
that lets a persona-patch line be told apart from ordinary content: [[chat-harness-routing-facts]]'s
`envelope-framing-and-out-of-band-signals.md`.
