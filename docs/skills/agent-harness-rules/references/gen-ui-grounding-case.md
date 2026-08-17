# Gen-UI grounding case — the motivating example for this whole pack

Every other axis in this pack generalizes from one real, dated case: a Gen-UI chat system whose
verification burden was painful specifically because most of it ran through the highest-cost
layer by default, when a cheaper layer already carried the answer.

**Provenance note (read before citing this file as more than it is):** this case is stated as
issue #542 itself describes it (the motivating example in its Summary, 2026-08-17) — it is NOT
independently verified against the Gen-UI system's own codebase or test suite by this pack's own
authoring pass. Treat every claim below as `[inferred]` from that issue description, not
`[verified]` against the target system directly. A future wave that reads the actual Gen-UI
harness and confirms or corrects these claims should amend this file in place with a dated note
(pack-writing-rules' falsification discipline), not silently overwrite it.

## The case, as described

A Gen-UI system runs a chat interface: a fleet of agents, each with its own custom instructions,
tools, services, and integrations, driving conversations. The system's traditional QA path ran
through **`claude-in-chrome`-class browser automation, screenshots, and human-in-the-loop payload
exports** — a person (or a browser-driving agent standing in for one) opening the rendered chat
UI, interacting with it, and eyeballing or manually exporting the result to judge correctness.
**[inferred]**, per issue #542.

## Why this was the wrong default layer

The system's chat behavior — which tool got called, with what arguments, in what order, what the
agent said — is almost entirely representable as **structured JSON payloads** before any of it is
rendered into a chat bubble. Routing that verification through the browser layer bought no extra
fidelity for those questions (the render is a faithful, boring transform of the payload) while
paying the full browser-layer cost: slower runs, flakier under load, harder to run headless in CI,
and a human (or a screenshot a human has to look at) in the loop for a question a JSON diff could
answer deterministically in milliseconds. **[inferred]**, applying
`references/assert-layer-choice.md`'s choice test to this case retroactively — the case is the
evidence the choice test's own generalization is built from, not a separate confirmation of it.

## The available fix, per this pack's axes

- **Assert-layer choice**: most scenario verification moves to the JSON-payload layer
  (`references/assert-layer-choice.md`, rung 1) — reserve the browser layer for genuinely
  render-shaped criteria (does the chat bubble actually display, is the layout right), a small
  fraction of the system's total scenario count.
- **Agent-native harness design**: a fleet of DRIVER agents (distinct from the target system's own
  fleet) — one persona per scenario class, scoped tools limited to sending a message and reading
  the payload back, exercising the target's own agent fleet the way a real user's messages would
  (`references/agent-native-harness-design.md`).
- **Assertion/fixture grammar**: chat scenarios are naturally state-transition and
  golden-payload-shaped ("given this conversation history, does the next payload call this tool
  with these arguments") — exactly the assertion shapes `references/assertion-fixture-grammar.md`
  names as agent-runnable, with a genuinely render-only subset left as browser-layer or
  human-review exceptions, named explicitly rather than the whole suite defaulting there.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Default-to-highest-fidelity | Browser automation chosen because it's "closest to the real user," for questions the render doesn't actually affect | Apply the choice test per scenario class before building the harness |
| Human-export-as-QA | A human manually exports and eyeballs a payload that could have been asserted automatically | Treat "needs export" as a signal the payload layer is already available — assert on it directly |
| One fleet doing two jobs | The target system's own agents used to both perform AND verify their own behavior | A distinct driver agent fleet, scoped to probe only (`references/agent-native-harness-design.md`) |

## Sources

- `[inferred]` The entire case: issue #542's own Summary/motivating-example text (this repo,
  2026-08-17) — kimgranlund/claude-plugins#542. Not independently verified against the Gen-UI
  system's own repository or test suite by this authoring pass; corrections belong here, dated,
  in place, per the provenance note above.
