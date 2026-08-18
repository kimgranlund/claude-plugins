---
name: make-artifact
description: >-
  Build or rebuild a rendered Artifact/report page — consume a design system (DESIGN.md +
  tokens.json) plus report or handbook content into a polished single-file page: light/dark
  custom-property CSS, house shell, themed mermaid diagrams, provenance footer. Use for 'turn
  this report into an artifact page', 'rebuild the Estate Handbook', 'render this with our
  design system'. Runs via /make-artifact [design-system path] [content source]. NOT the
  standards (artifact-rules; styling lives in design:artifact-styling-rules); NOT
  authoring/grading the design-system source (make-design-system); NOT drafting a functional
  document (make-doc); NOT generic markdown→DOM rendering (markdown-to-markup).
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
the content source (a report/retro draft, handbook chapters, or a raw seed to shape). Where both
DESIGN.md and tokens.json are present, tokens.json is the exhaustive-lookup file (per its own
Agent Prompt Guide) — prefer it as the `css_build.py` input; DESIGN.md's frontmatter is the
fallback when only it is available.

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

## Phase 5 — Stamp the provenance footer

Per `artifact-rules/references/refresh-procedure.md`: every page carries a footer naming the
source DESIGN.md/tokens.json path, the tokens.json `$generator` line (when used), the content
source, the build date, and the exact `css_build.py` invocation — the machine-readable interface
a future refresh reads its inputs from.

## Phase 6 — Verify

`css_build.py selftest` green (mechanical proof the token→CSS mapping still holds) plus a named
human render check: does the shell actually look right, does a themed mermaid diagram actually
re-theme in both schemes. This is the stated human/browser-layer exception
(`agent-harness-rules`' assert-layer-choice) — named here, never silently skipped.

**Done** = `css_build.py selftest` green, the emitted CSS carries the expected `--c-*`/
`--text-*`/`--font-*`/`--space-*`/`--r-*` custom properties, the shell matches the content class,
the provenance footer is stamped, and the human render check is named (passed or explicitly
deferred — never silently assumed). **NOT done** = CSS hand-edited past what `css_build.py`
emitted, a report page shipped as a dashboard/tile shell, a mermaid diagram assembled inside a
`display: none` tab panel, or no provenance footer.
