# Sources and provenance

This pack distills four independent, dated, read-only field-report corpora plus one repo's live
core source files — not a live re-audit of all four cited repos end to end. Each corpus was
authored 2026-08-20 by a dedicated reader session in its own repo; this pack's own synthesis
(2026-08-20) draws its four axes from them, per the frontend knowledge series' master outline
(ticket #808, itself citing the 2026-08-20 synthesis of the same four report corpora that seeded
`reactivity-facts`, `state-model-rules`, and `persistence-facts`).

## The grounding files

| Axis | Repo | File(s) consulted |
|---|---|---|
| `streaming-stack.md` | `adia/gen-ui-kit` | `packages/web-components/core/{data-stream,streams-bridge,transport}.js` + `.claude/docs/specs/data-stream-protocol.md` (§10.1, §10.5) |
| `bridge-protocol.md` | `nonoun/ultimate-tokens` | `.claude/docs/reports/reactivity-2026-08-20/04-context-and-messaging.md` |
| `no-di-taxonomy.md` | `nonoun/ultimate-tokens` + `adia/adia-v2` + `nonoun/agent-ui` + `adia/gen-ui-kit` | `reactivity-2026-08-20/04-context-and-messaging.md` §C; `.claude/docs/reports/2026-08-20-reactivity-data-audit/04-context-di-patterns.md`; `.claude/docs/reports/data-model-review-2026-08-20/framework-state-idioms.md`; `.claude/docs/reports/2026-08-20-reactivity-review/02-web-modules-state.md` §4 |
| `wiring-menu.md` | `adia/gen-ui-kit` | `.claude/docs/reports/2026-08-20-reactivity-review/04-doctrine-vs-practice.md` Part 2, reporting `packages/plugins/adia-ui-factory/skills/data-wiring/SKILL.md` |

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary field-report file or live source file
  cited above, on 2026-08-20 (this pack's authoring date). Every substantive claim in this pack's
  four axis files carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated, real (not hypothetical) failure the source
  material itself documents as having actually occurred or as currently, confirmedly live in
  production code (e.g. the `sweepBusy` permanent-wedge bug). Distinguished from [verified] because
  the evidentiary weight is "this actually broke or is still broken," not just "this is what the
  code currently does."

No claim in this pack is [inferred] as of authoring — every axis traces to a specific report
section or file:line the source material itself provides. `streaming-stack.md` is the one axis
grounded directly in live gen-ui-kit source rather than a report distilling that source — its
citations are file:line references into the actual `core/{data-stream,streams-bridge,transport}.js`
modules, current as of the commit checked at authoring time. If any cited repo's code changes
after 2026-08-20, this pack's specific file:line citations become [drift-prone] and should be
re-verified at the next refresh boundary rather than assumed current.

## What this pack deliberately does NOT re-verify

This pack distills the field reports' own stated findings (and, for `streaming-stack.md`, a direct
read of the cited live source) — it does not independently re-read the full source tree of any of
the four repos. Where a report states a verdict in its own words (e.g. ultimate-tokens' "one
designed protocol... sitting inside an accumulated, un-systematized context layer"), this pack
cites that verdict rather than re-deriving it from a fresh read. A reader confirming one specific
claim against CURRENT code should re-read the cited file:line in the named repo, not treat this
pack as a live source of truth for a moving codebase.

## Fence provenance

The data-wiring-vs-reactivity-mechanism, data-wiring-vs-state-architecture, and
data-wiring-vs-persistence fences in this pack's SKILL.md were negotiated against the three
sibling packs already shipped in this series (`reactivity-facts`, wave 1; `state-model-rules`,
wave 2; `persistence-facts`, wave 3) — see this pack's own Boundaries section and each sibling's
own updated Boundaries bullet naming this pack in return.

Extension: governed by [[make-pack]]
