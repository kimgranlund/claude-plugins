# Script interface — the `css_build.py` mechanical contract

The question this file answers: **what does `css_build.py` actually take and emit?** This is the
INTERFACE only — the doctrine behind why the mapping looks this way (the role-alias method,
`light-dark()`, the token inventory, the naming grammar) lives in
`design:artifact-styling-rules`' `token-architecture.md`; this file never restates it, only cites
it (soft cross-plugin mention, degrades gracefully where `design` isn't installed).

## Input: two representations, either legal

`css_build.py` accepts JSON in either of two shapes:

- **`tokens.json`** — the exhaustive-lookup grammar: `colors`/`colorsDark` top-level objects keyed
  by role; `type.scale` for type roles; a flat ordered `spacing` array; a `radii` object.
- **`DESIGN.md` frontmatter, extracted to JSON** — a flat color map with `-dark`-suffixed sibling
  keys; a nested `typography:` map; `spacing:`/`rounded:` objects keyed by the same scale names.
  stdlib ships no YAML parser (script-writing-rules' stdlib-only constraint), so a DESIGN.md-only
  invocation needs its frontmatter extracted to JSON first — a stated, mechanical, lossless step
  the invoking session performs before handing the script its input. `tokens.json` is consumed
  directly.

A role missing its dark counterpart in either shape is a build failure (exit 1), never a silent
light-only variable.

## Invocation

```
python3 "${CLAUDE_SKILL_DIR}/scripts/css_build.py" <tokens.json|normalized-frontmatter.json> --out page.css
```

Exit 0 → CSS built. Exit 1 → a role is missing its dark counterpart or a scale-count mismatch —
the fix is in the SOURCE design system, never a hand-patch of the emitted CSS. Exit 2 → a usage
error (bad path, unparseable JSON).

## Output: emitted custom-property names

- **Colors** → `--<short-role>`, the UNPREFIXED artifact-page inventory name (`--paper`, `--ink`,
  `--accent`, …) — **never** `--c-<role>` (superseded 2026-08-18, #662; see lld-0013 Resolution
  6's supersede note). Each source color role is mapped onto its short name via the script's own
  `ROLE_ALIASES` table, a mechanical transcription of design's `token-architecture.md`'s
  14-live-roles table (its "Aliases" column) — that file is the authority for what the mapping
  IS; this file only names that the mapping happens and where the output lands. A source role
  absent from the table passes through unchanged, unprefixed (never re-derived, never dropped);
  two source roles aliasing to the same short name must resolve identically or the build fails
  (exit 1), naming the conflict. `--mono-bg` is a special case: no source role of its own —
  when the input carries no EXPLICIT source role that aliases to `mono-bg` (an explicit one always
  wins), it derives from whatever `--chip` resolves to; if `--chip` itself is unbound in that
  build, `--mono-bg` is simply not emitted (never invented from nothing).
- **Type roles** → `--text-<role>-size`/`-weight`/`-lh`/`-ls` + deduplicated `--font-<slug>` family
  variables (every emitted font-family carries a mandatory system-stack fallback tail — CSP blocks
  external font files, so a bare custom font with no fallback silently renders as browser default;
  the selftest's negative control asserts this holds for every emitted `--font-*` line). A page
  reading `font-family: var(--font-<slug>)` as its ENTIRE value is on-doctrine by construction —
  design's `artifact_check.py`'s `doctrine-font-stack` check treats a PURE `var(--font-*)`
  reference as conforming with no override comment needed (a mixed value naming a literal fallback
  alongside the token, e.g. `var(--font-x), 'Comic Sans MS'`, still warns — the skip is anchored to
  the whole value, never a bare substring match), AND independently verifies the `--font-*` token's
  own DEFINITION still carries the mandatory fallback tail (trusting a token's use is only as safe
  as the token itself).
- **Spacing** → `--space-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`2xl`/`3xl`/`4xl`/`5xl`.
- **Radii** → `--r-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`full`.
- **Mermaid re-theme block** — a fixed CSS section, `!important`-scoped, bound to the same short
  role custom properties as the rest of the page (`--card`/`--line`/`--ink`/`--muted` — never
  `--c-*` post-#662; design's `mermaid-reference.md` owns the full doctrine for why this shape).

## Cross-script regression fixture (#662)

LEDGER-CLASS: emitter-vs-checker-drift | ids: #662 | mechanized: 2026-08-18

Two maintained duplicates, not a live import (`css_build.py` and `artifact_check.py` sit in
different plugins; `.claude/rules/plugin-authoring.md`'s hard boundary forbids a bundled script
importing across it):

1. **`css_build.py`'s own `selftest`** asserts its emitted CSS carries the new short role names,
   never a `--c-<role>` line, AND mirrors `artifact_check.py`'s own `color-scheme`/`missing-ground`
   regexes inline (a dated, cited local copy — its own cross-script check, step 8 of its
   `selftest`) to prove its output would satisfy them without depending on the other script at all.
2. **`artifact_check.py`'s own `selftest`** carries the inverse: `CSS_BUILD_OUTPUT_FIXTURE`, the
   FULL VERBATIM output of `css_build.build(FIXTURE_TOKENS)` (every line, comments included,
   nothing trimmed — a prior trimmed draft of this fixture missed a real regression a full copy
   would have caught), asserted to pass this checker's six checks clean.

A future change to either script's naming/emission contract updates ALL of these in the same
change — the fixture in (2) and the mirrored regexes in (1) alike — never just one side.

## The mechanized authority

`docs/skills/make-artifact/scripts/css_build.py` IS the check — its `selftest` proves every rule
above against fixtures for both input representations, with a negative control (a role missing
its dark counterpart must fail) and a reverse control (a complete fixture emits every expected
pair). Consult that script, never hand-derive the CSS from this prose.

Extension: governed by [[make-pack]].
