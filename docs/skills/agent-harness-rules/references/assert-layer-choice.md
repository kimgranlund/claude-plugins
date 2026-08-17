# Assert-layer choice — where verification runs, and when each layer is the floor

Every scenario a coding agent needs to verify asserts at one of four layers. Higher layers cost
more (slower, flakier, harder to run headless/unattended) and buy more fidelity (closer to what a
real user actually experiences); the design question is never "which is best" but "which is the
CHEAPEST layer that still catches the failure this criterion cares about."

## The ladder

1. **Pure-data / JSON payload layer** — assert on the structured output a system produces or
   consumes, with no rendering, no network, no browser. Cheapest, fastest, fully deterministic,
   trivially parallelizable, runs in CI with no display server. **[inferred]** from general test
   pyramid practice (unit/contract tests sit here) — the floor for any system whose real behavior
   is representable as data before it's rendered.
2. **API / service layer** — assert against the system's own service boundary (HTTP/RPC calls,
   tool-call traces, database state) without driving a UI. Catches integration failures the
   payload layer alone misses (auth, persistence, cross-service contracts) at a fraction of
   browser-layer cost. **[inferred]**, same lineage.
3. **Browser / UI layer** — drive the actual rendered interface (`claude-in-chrome`, Playwright,
   Selenium-class tooling). Necessary when the criterion IS the render — visual regression, focus
   order, an interaction only expressible as clicks — never as a default for everything else. Most
   expensive to keep green: flaky under load, slow, needs a real or virtual display.
4. **Human review** — a person judges taste, aesthetic quality, or a criterion no automated
   assertion can currently express. The floor of last resort, not a comfortable default; every
   criterion routed here should be a stated exception (`## Agent verification`'s escape hatch),
   not a silent absence of the other three.

## The choice test

For each Acceptance criterion, ask **"what is the CHEAPEST layer at which this criterion's
failure would actually show up?"** — not "what layer is the system usually tested at." A chat
system's response CONTENT is almost always a payload-layer question ("did the agent call the
right tool with the right arguments") even though the system has a browser UI; a chat system's
LAYOUT is a browser-layer question even though the same system also emits JSON. **[inferred]**:
this is the generalization of the Gen-UI grounding case (`references/gen-ui-grounding-case.md`) —
most of that system's QA burden was content/behavior questions mistakenly routed through the
browser layer by default, when the payload layer already carried the answer.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Default-to-browser | Every scenario driven through the UI because that's how a human would check it | Ask the choice test per criterion; most content/logic questions resolve one layer down |
| Payload-only blind spot | Everything asserted at the JSON layer, a real rendering regression ships silently | Name which criteria are genuinely render-shaped and keep a thin browser-layer suite for those |
| Human-review sprawl | "needs a human" applied by default rather than as a stated exception | `## Agent verification`'s exception line forces the claim to be written down, not assumed |
| Layer mismatch cost blindness | A browser-layer suite built for a payload-shaped question, then complained about for being slow/flaky | The choice test run BEFORE the harness is built, not diagnosed after it's already slow |

## Sources

- `[inferred]` General test-pyramid practice (unit/contract/E2E cost-fidelity tradeoff) — widely
  documented industry convention, not tied to one primary source; applied here to the
  agent-verification question specifically rather than restated as generic testing advice.
- `[inferred]` The Gen-UI grounding case (issue #542's own motivating example, 2026-08-17) — see
  `references/gen-ui-grounding-case.md` for the full worked case this axis generalizes from.
