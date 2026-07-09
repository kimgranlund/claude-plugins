# ui — design, critique, and verify UI structure

Sibling plugin to forge (which authors the harness) and scribe (which authors functional
documents); ui authors and reviews UI structure — layouts, flows, components, patterns — and
verifies it against the non-functional bars every surface owes (focus, i18n, perf, safety).
Merges what plugin-decompose surfaced as two candidate clusters (ui-architecture and ui-verify)
into one plugin on explicit direction: 13 cross-mentions between them was the single
highest-coupling boundary found in the analysis.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/layout-decompose` | Procedural skill | both (`/layout-decompose`) | Two-axis (outside-in space x inside-out behavior) layout decomposition/grading method; `references/decomposition-method.md`, `examples/walkthrough.md`; four archetypes consumed from `ui-patterns` |
| `skills/flow-decompose` | Procedural skill | both (`/flow-decompose`) | Cross-screen flow decomposition (task->journey x transitions->whole); `scripts/flow-check.py` — reachability, dead-end, exit-truth, recovery gates; `examples/one-time-pay.flow.json` |
| `skills/component-author` | Procedural skill | both (`/component-author`) | Compose x Realize two-axis component method; `references/` — api-policy, attributes-as-api, composition-patterns, decomposition-method, family-controls, family-overlays, geometry-system, platform-baseline; `scripts/` — component-contract-check.py, composition-check.py, geometry-check.py |
| `skills/ui-patterns` | Declarative skill | model-only | Macro/micro UI pattern catalog (page templates, module catalog, screen-state grammar); `references/` — macro-patterns, micro-patterns, state-patterns, sources, four archetype-*.md files consumed by `layout-decompose` |
| `skills/ui-genres` | Declarative skill | model-only | Product-genre world model — which patterns a category expects; `references/INDEX.md` + `references/genres/` — thirteen genre files (dashboards-analytics through travel) |
| `skills/ui-audit` | Procedural skill | both (`/ui-audit`) | Whole-product UI sweep composing the other nine members over a set of screens/flows; `scripts/` — inventory-scan.py, audit-diff.py, ui-probe.mjs (live DOM probe) |
| `skills/ui-change-verify` | Procedural skill | both | Drives a UI change against the running artifact (launch, interact, screenshot before/after, console check, perf trace) before it's reported done — the live-artifact half of what `focus-verify`/`i18n-verify`/`perf-verify`/`safety-verify` reason about in the abstract |
| `skills/focus-verify` | Procedural skill | both (`/focus-verify`) | Focus-ring, keyboard affordance, and hit-target verification; `scripts/focus-check.py`; `focus-ring/recipes.json`, `keyboard/affordances.json`, `offsets/per-surface.json`, `targets/minimums.json` |
| `skills/i18n-verify` | Procedural skill | both (`/i18n-verify`) | RTL/bidi, locale Intl formatting, and text-expansion verification; `scripts/i18n-check.py`; `bidi/isolation-points.json`, `formatting/intl-surfaces.json`, `locales/expansion-factors.json`, `locales/script-metrics.json`, `mirroring/icon-policies.json` |
| `skills/perf-verify` | Procedural skill | both (`/perf-verify`) | Perceived-latency and Core Web Vitals verification; `scripts/budget-check.py`; `cancellation/contract.json`, `cls/budget.json`, `decisions/skeleton-vs-spinner.json`, `optimistic/eligibility.json`, `streaming/posture.json`, `thresholds/perception.json` |
| `skills/safety-verify` | Procedural skill | both (`/safety-verify`) | Blast-radius, reversibility, and friction verification for destructive UI actions; `scripts/safety-check.py`; `audit/event-schema.json`, `blast-reversibility/matrix.json`, `defaults/confirm-posture.json`, `friction/recipes.json`, `permissions/error-ux.json`, `recall/windows.json` |
| `agents/layout-reviewer.md` | Subagent (fresh-context critic) | dispatched (Task tool, model `fable`) | Grades ONE layout against `layout-decompose`'s two-axis rubric; preloads `layout-decompose` only |
| `agents/flow-reviewer.md` | Subagent (fresh-context critic) | dispatched (Task tool, model `opus`) | Grades ONE cross-screen flow against `flow-decompose`'s two-axis rubric and its `flow-check.py` gate; preloads `flow-decompose` only |
| `agents/component-reviewer.md` | Subagent (adversarial critic) | dispatched (Task tool, model `opus`) | Grades ONE component/composition against `component-author`'s Compose x Realize method and its three checkers; preloads `component-author` only |

Cross-plugin seam (soft, by design): all three reviewer agents return through forge's
`handoff-compose` block where forge is installed, and fall back inline
(Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action)
when it is not — no hard preload crosses the plugin boundary.

v0.2.3 · assembled 2026-07-09 · 0.2.3: eval-run tuning — ui-genres/ui-patterns dashboard-modules fence closed both ways; safety-verify fenced optimistic-UI to perf-verify and gained 'actions silently disabled by missing permission' (second-strike confirmed); layout-decompose's 'what shell is this app using' case reassigned to ui-patterns (blind judges routed it there in two consecutive runs — they were right) · assembled 2026-07-09 · 0.2.2: agent fallback blocks 'Tests run'→'Tests/checks run' (harness-audit finding, estate-wide sweep) · assembled 2026-07-07 · 0.2.1: ui-change-verify's evals/evals.json added (G7 coverage gap closed) · 0.2.0: ui-change-verify — drives a UI change against the running artifact (launch/interact/screenshot/console/perf) instead of reasoning about it in the abstract, closing the gap the getting-started-with-loops guide's turn-based-loop example named · 0.1.0: initial: ported from ~/.claude/skills + ~/.claude/agents/design/{layout,flow,component}-reviewer as part of a plugin-decompose partition; merges the ui-architecture and ui-verify candidate clusters on explicit direction (13 cross-mentions between them was the single highest-coupling boundary found)
