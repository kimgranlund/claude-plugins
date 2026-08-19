# Proving end-to-end behavior — deterministic replay in CI, one live turn for acceptance

> Axis: how a chat harness's END-TO-END behavior gets proven — the two-tier split between
> deterministic replay (the standing CI gate) and a single real model turn (the acceptance proof),
> and the shape of an honest live acceptance run. Distinct from routing-accuracy-evals: routing
> accuracy is a NUMBER over many judged description-menu cases; this file is about ONE engineered
> end-to-end turn proving a behavior change. Grounded in agent-ui's ratified devtools design
> (ADR-0200) and that repo's dated live-verification practice, both read at source 2026-08-19.

## Two tiers, opposite jobs — replay is the CI backbone, live is the acceptance

**Claim — run the harness's own turn pipeline in CI against DETERMINISTIC replay/script backends
(canned timelines behind the same transport seam the live path uses; two runs yield byte-identical
line sequences; no key, no network) as the standing gate, and reserve the LIVE model turn — real
provider, real key, real streaming — for ACCEPTANCE: a change's definition-of-done, never the
standing suite.** Failure modes on both sides: a CI gate built on live turns is slow, keyed,
costly, and cannot tell a regression from provider weather; a project with ONLY replay gates never
proves the live path at all and ships against a fixture of its own assumptions. A useful side
effect of the replay tier: determinism FENCES the capture format itself — anything nondeterministic
in a recorded timeline (timestamps in content events, unordered maps) is a format defect by
definition. · agent-ui ADR-0200 clause 3 (replay/script transports "the CI backbone and the
fixture source"; the proxy transport the live path) + Consequences ("Replay determinism fences the
capture format") · 2026-08-19 · [verified]

The backend SHELF this rides on — one `turn(input) → AsyncIterable` seam, replay/proxy/peer
implementations — is [[llm-streaming-facts]]'s territory (its stream-abstraction file); this file
owns only WHEN each tier is the right proof.

## The acceptance run's shape — fresh server, OS-allocated port, exit-code verdict, proven teardown

**Claim — boot a FRESH server for the acceptance run and let the OS allocate its port (bind port
0); never target a fixed well-known port.** Failure mode, both directions: a stale server from an
earlier session squatting the expected port answers for the new build — the acceptance "passes"
against OLD code, or a red run blames NEW code for an old server's behavior — and a fixed port
collides with the human operator's own dev loop. Run the acceptance standalone rather than inside
the fast standing gates (booting a server + browser pair costs tens of seconds cold), judge it by
EXIT CODE, and prove TEARDOWN instead of assuming it: signal the whole process group, verify no
survivor remains, and run twice back-to-back to prove nothing squats the port between runs.
· worked instance: agent-ui `scripts/e2e-devtools.mjs` (GH #1145) — `freePort()` binds `listen(0)`
with the comment "never 5173: the port is freshly OS-allocated every run"; the server child is
spawned detached in its own process group so teardown can `kill(-pid)` and then VERIFIES (direct
pid gone, `pgrep -g` finds no survivor); shipped as a standalone `npm run e2e:*` with exit codes
0/1/2 and its own `selftest` arm · read 2026-08-19 · [verified]

## Bait the defect — an acceptance ask that cannot fail proves nothing

**Claim — engineer the live turn's ASK so the defect class under test MUST fire if it is still
present; an acceptance turn that any behavior would pass proves only that the pipe is connected.**
If the defect was "the terminal marker gets dropped from multi-payload flows," the acceptance ask
drives a full flow to its closing turn and the assertion checks the marker arrived — a generic
"hello" cannot fail for that defect and therefore cannot accept its fix. This is the evals-first
principle applied at acceptance grain: state what would fail before running the turn. · worked
instance: agent-ui #1101's closing verification (2026-08-17, quoted from the issue's own closing
comment, read via the GitHub API 2026-08-19): "live end-to-end verification (host self-test,
2026-08-17 evening, proxyTransport → /__a2ui/agent → claude-sonnet-5, full 4-turn headache-intake
flow)" — the ask reproduced the defect's own trigger (a flow reaching its closing turn), and the
recorded trace shows the defect-adjacent machinery actually exercised ("rounds:2,
failureCodes:[FLOW_END_MISSING], flowEnd:true on the final meta line"), which is what let the
issue close on the script's verdict without waiting for a human pass · [verified]

**The corollary discipline:** a live acceptance run's evidence is the recorded trace/timeline (what
streamed, which correction rounds fired, what the final line carried), written into the change's
own record — not a bare "ran it, looked fine." One engineered turn with its trace attached is
acceptance; ten generic turns without one are anecdotes.

## What this file does NOT cover

Authoring or re-running description-routing eval suites — accuracy as a tracked number over many
judged cases (routing-accuracy-evals.md; and AUTHORING a new corpus is
[[chat-harness-routing-facts]]'s side of that fence) · how the transport seam and its
replay/live/peer backend shelf are SHAPED ([[llm-streaming-facts]]) · the retry/self-correct loop
running INSIDE a live turn ([[llm-streaming-facts]]'s validate-then-stream file) · building an
actual e2e harness for your project (your project's own build seat).
