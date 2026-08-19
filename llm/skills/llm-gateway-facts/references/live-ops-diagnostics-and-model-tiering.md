# Operating a live gateway — first diagnostics, storm posture, and model tiering

> Axis: the ops side of a gateway that is already built and running — what to check FIRST when "model
> X doesn't work", how to behave while an upstream is 503-storming, and which model tier gets pointed
> at which class of work. Grounded in dated field incidents from the same worked repo the rest of
> this pack cites (`@agent-ui`), each cited as a real instance of the pattern paying rent — not as
> the only valid ops playbook.

## The per-model curl matrix — isolate the layer before blaming the UI

**Claim — when a specific provider or model "doesn't work in the chat", the FIRST diagnostic is a
curl matrix against the gateway itself: one minimal request per `{provider, model}` pair (and per
gateway endpoint, where there are several), from the command line, bypassing the entire client
stack.** Read the matrix before touching any UI code: a green matrix localizes the defect to the
client layer (rendering, state, event wiring); a red CELL localizes it to that pair's adapter, its
env key, or the vendor; a red COLUMN localizes it to the provider; a matrix that flickers across
runs points at infrastructure (a restarting dev server, a dying process), not at code at all.
**Failure mode this prevents:** hours of client-side debugging — or worse, client-side "fixes" —
against a defect that lives in an adapter or was never a code defect to begin with.
· [incident] agent-ui live-agent triage, 2026-07-16/17 (the TKT-0075/0080 wave, recorded in that
project's own debug-craft ledger): "model X doesn't work in the chat" was answered by curling the
dev proxy's two endpoints per model first, one line each; the green matrix re-attributed the
failures to transient dev-server restarts — no client code was touched.

The matrix's row/column set comes for free from the committed registry (the same
`providers.json` the picker and allowlist read — registry-and-trust-boundary): enumerate the
`implemented` pairs, never a hand-remembered list.

## An upstream 503 storm — the richer API surface dies first; ride plain REST and verify writes

**Claim — during an upstream service's 503 storm, its aggregated or derived API surfaces (a
GraphQL endpoint, batch/composite verbs, computed-state queries) degrade BEFORE the plain REST
resources they are built over — so the storm posture is three moves, not just "retry":** (1) route
must-land calls over the plain REST surface with a bounded, spaced retry; (2) treat every write's
success/failure REPORT as unreliable while the storm lasts — re-read to verify the write actually
landed before believing either answer; (3) treat derived/cached state the service reports (e.g. a
computed mergeability) as potentially stale — re-query before acting on it. **Failure mode:**
retrying the already-dying rich endpoint harder, double-applying writes that had in fact landed, or
acting on a stale derived answer the storm froze.
· [incident] 2026-08-17, agent-ui fleet ops under a real GitHub 503 storm: `gh`'s GraphQL-backed
verbs failed first while plain `gh api` REST kept working; PRs were created and merged over REST
with a single ~20 s-spaced retry, each write verified landed before proceeding; one merge attempt
reported conflicts from STALE mergeability and succeeded on re-query + re-push. The upstream there
was GitHub, not an LLM vendor — cited as the dated instance of a pattern that applies to any
upstream a gateway-shaped client depends on, LLM providers included.

This layers ON TOP of the normal retry policy (idempotent-only defaults, full jitter,
`Retry-After` — retry-policy-and-streaming-passthrough); the storm-specific additions are the
surface selection and the write verification, neither of which a backoff parameter expresses.

## Planning-vs-execution model tiering — a standing config decision, not a per-call vibe

**Claim — when the registry offers multiple models, tier them by WORK CLASS and declare the
assignment once, in the consumer's own seat/role config: deep-reasoning (expensive, slow) tiers
for design/planning-class work — decomposition, contract authoring, open-ended judgment — and
faster/cheaper tiers for execution-class work that builds mechanically to an already-settled
contract.** The registry's `models[]`/`defaultModel` (registry-and-trust-boundary) expresses which
tiers EXIST; the tier ASSIGNMENT belongs with the caller's configuration, recorded where it can be
audited and re-ruled, never improvised per call site. **Failure mode both directions:** paying the
deep-reasoning price on every mechanical call — or letting a cheap tier make the design decisions
everything downstream then builds on.
· [verified] agent-ui's own standing seat config, ruled by the repo owner 2026-06-29 and in force
since: the planning seat runs `model: opus` / `effort: xhigh`, the execution seat `model: sonnet` /
`effort: high`, declared in the seats' own frontmatter (`.claude/agents/`), with the rationale
recorded in the project ledger ("builds mechanically to a ratified LLD… a faster/cheaper tier
suffices"). Cited as a worked instance of the ops pattern — the split criterion (reasoning-heavy
design vs. contract-faithful execution) is the portable claim, not any vendor's specific tier names.

## What this file does NOT cover

The general retry policy defaults a storm posture layers over
(retry-policy-and-streaming-passthrough) · the registry the curl matrix enumerates its pairs from
and the pair validation itself (registry-and-trust-boundary) · debugging the streamed body's
CONTENT once the transport layer is proven green ([[llm-streaming-facts]]).
