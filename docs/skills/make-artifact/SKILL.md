---
name: make-artifact
description: >-
  Build/rebuild a rendered Artifact/report page — consume a design system
  (DESIGN.md/tokens.json), or synthesize one via design if absent, plus a report, handbook, or
  records tree (composed into chapters) into one page: light/dark CSS, house shell, themed
  mermaid, provenance footer. Use for 'turn this into an artifact page', 'rebuild the Estate
  Handbook', 'render with our design system', 'compose a handbook from our records'. Runs via
  /make-artifact [design-system path] [content source]. NOT the standards
  (artifact-rules/artifact-styling-rules); NOT the source alone (make-design-system, make-palette,
  pick-fonts); NOT doc drafting (make-doc); NOT plain markdown render (markdown-to-markup).
disable-model-invocation: false
user-invocable: true
argument-hint: "[design-system path] [content source]"
---

# make-artifact

Turns a design system plus report/handbook content into one rendered Artifact page — the durable
owner #619 found missing (six hand-rolled Python rebuilds for the Estate Handbook because nothing
in the estate owned this job). Invoke `artifact-rules` now; the standards below are its, not
restated here — the `make-doc` → `doc-writing-rules` contract, adopted verbatim. Seed:
`$ARGUMENTS`; invoked with none (a model-triggered ask, not a typed `/make-artifact`), take the
design-system path and content source straight from the conversation instead.

## Phase 1 — Locate inputs

Resolve the design-system path (a DESIGN.md, a tokens.json, or both — either alone is legal) and
the content source (a report/retro draft, handbook chapters, a project records tree, or a raw seed
to shape). Where both DESIGN.md and tokens.json are present, tokens.json is the exhaustive-lookup
file (per its own Agent Prompt Guide) — prefer it as the `css_build.py` input; DESIGN.md's
frontmatter is the fallback when only it is available.

**Missing design system (lld-0013 v2 Resolution 9)** — when the target project has **neither**
DESIGN.md nor tokens.json, render never fails and never falls back to unstyled:

- **`design` plugin installed → synthesize.** Compose one via `design`'s own skills —
  `make-palette` (color), `pick-fonts` (only where the page legitimately needs brand faces; the
  type doctrine already owns the default faces, Phase 4 below), `make-design-system` (assembly) —
  emitting a project-local DESIGN.md/tokens.json that then feeds `css_build.py` exactly as a
  pre-existing system would. Stamp the provenance footer's design-system line **SYNTHESIZED** with
  the generator line naming which skills produced it (Phase 5). Soft cross-plugin mentions only —
  invocation by name, no preload, no cross-plugin `${CLAUDE_PLUGIN_ROOT}` path.
- **`design` NOT installed → doctrine-neutral fallback, gap named.** Emit a neutral-monochrome page
  on the artifact type doctrine's own faces and shell — Phase 2's `css_build.py` binds the
  14 live roles (`design:artifact-styling-rules`' `token-architecture.md`'s inventory) to neutral
  values, and Phase 4 binds system-ui body / mono interactive / doctrine widths — never an error
  exit, never a bare browser-default page. Name the gap in the provenance footer: "design system: none —
  doctrine-neutral fallback; install the design plugin to synthesize one."
- Either branch emits **resolved literals** (a frozen projection), never a live token/ramp binding
  — portable, CSP-friendly, and exactly what `css_build.py` already emits for a real source system.

## Phase 1b — Compose from a project records tree (records-tree content sources only)

Fires only when the content source IS a project's own records tree (`.claude/docs/**`), never for
a prose draft or pre-written handbook chapters — those two classes skip straight to Phase 2 exactly
as before. Per `artifact-rules/references/composition-model.md`: read the target project's typed
records (brief/IDR/PRD/ADR/SPEC/LLD — the hard inputs; harness-facts/project-facts harvest output
only where present, never a hard edge) and compose the section outline via the Intent/User-Story/
Concept/System layer map, one mechanism-first mermaid per resolved decision fork, never a
chip-wall. A records tree that doesn't follow the canonical type-prefix layout degrades to the
prose-draft path, with the degradation named in the provenance footer (Phase 5) — never a silent
fallback.

## Phase 2 — Run `css_build.py` (never hand-derive the CSS)

`css_build.py` is bundled at `${CLAUDE_SKILL_DIR}/scripts/css_build.py` (this skill owns it).
tokens.json is valid input as-is; a DESIGN.md-only input needs its YAML frontmatter extracted to
JSON first — a stated, mechanical, lossless step (stdlib has no YAML parser), never a
hand-derivation of the CSS itself:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/css_build.py" <tokens.json|normalized-frontmatter.json> --out page.css
```

Exit 0 → the CSS is built; consult `artifact-rules/references/script-interface.md` if the output
shape needs explaining (for the doctrine WHY, `design:artifact-styling-rules`'
`token-architecture.md`). Exit 1 → a role is missing its dark counterpart (or a
scale-count mismatch) — the fix is in the SOURCE design system, never a hand patch of the emitted
CSS. Exit 2 → a usage error (bad path, unparseable JSON) — fix the invocation.

## Phase 3 — Choose the shell

Classify per `artifact-rules/references/content-structure.md` (report/retro vs handbook vs
spanning both); the visual doctrine for each — narrative single-scroll for reports/retros, tabbed
chapters for handbooks — lives in `design:artifact-styling-rules`' `references/shells-and-genres.md`.
Content spanning both is named explicitly here, not silently defaulted.

## Phase 4 — Assemble the page + mermaid diagrams

Assemble the chosen shell around the content, wiring the CSS from Phase 2. Any mermaid diagram in
the content follows `design:artifact-styling-rules`' `references/mermaid-reference.md` (soft
cross-plugin mention, degrades gracefully where `design` isn't installed): single-line node labels
(detail on edges, never `<br/>`), and — if the shell is tabbed — hidden tab panels use the
width-preserving `visibility`-based hide the CSS already emits, never `display: none`.

**Type-doctrine binding (lld-0013 v2 Resolution 10).** Body/reading text binds the system-ui stack
and interactive elements (buttons, links, tabs, badges, kickers) bind the mono stack **by
default**, regardless of the source design system's own faces — `css_build.py` emits this binding;
color still flows from the design system (or the fallback branch above), faces and geometry from
the artifact type doctrine. When a source-system face is deliberately bound to body/interactive
text instead (a real, sourced reason — the invoker's stated choice, or the design system's own
explicit face doctrine — never boilerplate), emit the adjacent `/* override: <stated reason> */`
comment immediately before that rule: the exact suppression path `design:artifact-styling-rules`'
`artifact_check.py` already honors. An unjustified brand face with no override comment is supposed
to WARN at Phase 6 — that is the checker working as designed, not a defect to silence.

## Phase 5 — Stamp the provenance footer

Per `artifact-rules/references/refresh-procedure.md`: every page carries a footer naming the
source DESIGN.md/tokens.json path — or its SYNTHESIZED/doctrine-neutral-fallback state (Phase 1) —
the tokens.json `$generator` line (when used), the content source (or its records-tree-degraded
state, Phase 1b), the build date, and the exact `css_build.py` invocation — the machine-readable
interface a future refresh reads its inputs from.

## Phase 6 — Verify

`css_build.py selftest` green (mechanical proof the token→CSS mapping still holds), `design`'s
`artifact_check.py` run over the assembled page **where the design plugin is installed** (soft
mention; not installed → the skip is named in the verify output, never silent) — this is what
catches an unjustified brand-face WARN (Phase 4) before it ships unnoticed — plus a named human
render check: does the shell actually look right, does a themed mermaid diagram actually re-theme
in both schemes. This is the stated human/browser-layer exception (`agent-harness-rules`'
assert-layer-choice) — named here, never silently skipped.

**Done** = `css_build.py selftest` green, `artifact_check.py` run (or its skip named) where
`design` is installed, the emitted CSS carries the expected unprefixed short role custom properties
(`--paper`/`--ink`/`--accent`/… — never `--c-<role>`, superseded #662)/`--text-*`/`--font-*`/
`--space-*`/`--r-*`, body/interactive text bind the doctrine faces by default (any deliberate
override carries its `/* override: <reason> */` comment), the shell matches the content class, a
records-tree source composed per `composition-model.md` (or degraded with the gap named), the
provenance footer is stamped (including its design-system state and any content degradation), and
the human render check is named (passed or explicitly deferred — never silently assumed).
**NOT done** = CSS hand-edited past what `css_build.py` emitted, a report page shipped as a
dashboard/tile shell, a mermaid diagram assembled inside a `display: none` tab panel, a missing
design system rendered unstyled or failed instead of synthesized/doctrine-neutral, an unjustified
brand face with no override comment left unreported, or no provenance footer.
