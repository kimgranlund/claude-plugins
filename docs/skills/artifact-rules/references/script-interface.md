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

- **Colors** → `--c-<role>` (design's `token-architecture.md`'s `--c-{family}-{slot}` grammar).
- **Type roles** → `--text-<role>-size`/`-weight`/`-lh`/`-ls` + deduplicated `--font-<slug>` family
  variables (every emitted font-family carries a mandatory system-stack fallback tail — CSP blocks
  external font files, so a bare custom font with no fallback silently renders as browser default;
  the selftest's negative control asserts this holds for every emitted `--font-*` line).
- **Spacing** → `--space-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`2xl`/`3xl`/`4xl`/`5xl`.
- **Radii** → `--r-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`full`.
- **Mermaid re-theme block** — a fixed CSS section, `!important`-scoped, bound to the same `--c-*`
  roles as the rest of the page (design's `mermaid-reference.md` owns the full doctrine for why
  this shape).

## The mechanized authority

`docs/skills/make-artifact/scripts/css_build.py` IS the check — its `selftest` proves every rule
above against fixtures for both input representations, with a negative control (a role missing
its dark counterpart must fail) and a reverse control (a complete fixture emits every expected
pair). Consult that script, never hand-derive the CSS from this prose.

Extension: governed by [[make-pack]].
