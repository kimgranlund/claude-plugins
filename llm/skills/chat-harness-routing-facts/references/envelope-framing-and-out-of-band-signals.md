# Envelope framing — routing an out-of-band signal on the SAME stream as content

> Axis: once a chat harness's wire carries more than one KIND of line (conversational content,
> plus notes/traces/progress/errors/plans), how a consumer tells them apart reliably and what
> happens when one kind is malformed. A distinct axis from *which skill fires for a request*
> (this pack's other files) — this is routing a single incoming LINE to the right handler once it
> has already arrived. Grounded in a worked instance: `@agent-ui/a2ui`'s meta-line envelope,
> `packages/agent-ui/a2ui/src/agent/meta-line.ts`.

## A provable structural discriminator, not a convention

**Claim — meta-lines (notes, traces, progress, errors) ride the same JSONL stream as content,
distinguished by carrying the reserved wrapper key and provably NO `version` key — the protocol
discriminator — so a meta-line can never be mistaken for a protocol message and vice versa.**
Framing conventions ride BESIDE a protocol, never inside it. · `meta-line.ts:185-207` (ADR-0088) ·
2026-08-17 · [verified]

## Shallow-validate independently — one broken field drops only itself

**Claim — a malformed field (`ask`/`plan`/`progress`/`personaPatch`) drops ONLY itself, never the
whole envelope, so the conversational `note` channel it rides alongside never breaks.** Exception:
a COMPOUND arm like a persona patch validates as a WHOLE — a half-parsed patch is the one shape an
apply loop must never receive. · `meta-line.ts:199-304` · 2026-08-17 · [verified]

## Peel reserved kinds before the content validator ever sees them

**Claim — the leading meta-line and any genui-shaped line are stripped from raw model output
AHEAD of heal/validate, unconditionally, whether or not this turn invited it — stream handling
never branches on prompt-composition flags.** Skipping this peel step burns a self-correct round
on a legitimate note line, misread as a parse failure. · `produce.ts:583-681` · 2026-08-17 ·
[verified]

## Closed vocabularies + drop-at-guard is the honesty law for status lines

**Claim — turn lifecycle stages are a closed union (`sent…done`); an out-of-vocabulary stage is
dropped at the parse guard, never rendered.** A stage never observed is never shown. Growing the
table is a versioned spec amendment, never an ad-hoc string. · `meta-line.ts:112-122` (ADR-0146
F1/F2) · 2026-08-17 · [verified]

## What this file does NOT cover

Which skill/tool/subagent a REQUEST routes to in the first place (this pack's own
`authoring-a-skill-vs-a-hardcoded-feature.md`/`invocation-species-model-vs-user-invoked.md`/
`description-routing-and-adversarial-evals.md` — a request-routing concern, distinct from a
wire-line-routing one). Namespacing a surface/resource id across multiple producers on the same
envelope: `multi-producer-namespacing.md`. Checking a model-declared routing FACT (an `ask`)
against what the payload actually did: `model-declared-routing-integrity-check.md`.
