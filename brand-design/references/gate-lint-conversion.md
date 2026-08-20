# gate-lint-conversion — where brand-lint's advisory checks land post-hook-retirement

> Track B note for Track C (the command-skill author). `hooks/` was never copied into
> brand-design — correctly: #466 retired all plugin hooks estate-wide, so the source's
> `PostToolUse Write|Edit → brand-lint --hook` wiring has no home here. Gate A's ruling: the
> same advisory check moves from a hook into the command-skills' own procedures, called
> explicitly at a gate step instead of firing on every write. This doc is the CLI contract
> `scripts/brand_lint.py` ships with, precise enough to call it correctly without re-reading
> the script.

## Where to call it from (per Gate A)

Call `scripts/brand_lint.py` — plain file-argument mode, NOT `--hook` mode (see below) — from
inside each of these three command-skills' own procedures, at the named gate step:

| Command-skill | Gate step | What to lint |
|---|---|---|
| `make-brand` | before presenting a draft to the user | the draft brand doc(s) just written |
| `check-brand-rubric` | before presenting a draft to the user | the doc(s) under review |
| `file-brand-corpus` | before export | the corpus doc(s) about to be written to `references/` / exported |

This is **advisory, never blocking** (the script's own docstring: "a clean brand-lint says 'no
structural tells,' never 'this brand is good'" — cultural-authority judgment stays with the
council, not this script). The calling procedure's shape:

1. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brand_lint.py <path-to-draft.md>...`.
2. If it exits 1, surface the printed findings to the user/draft as a flagged callout — do NOT
   halt the skill or refuse to present the draft. Findings are a prompt to reconsider, not a gate
   that blocks completion.
3. If it exits 0, say nothing (a clean brand-lint is not itself worth reporting as a finding).

## CLI usage (exact, as of this pass)

```
brand_lint.py <file.md>...     lint one or more files; prints per-file findings
brand_lint.py -                lint stdin (also: no args at all — same as passing a bare "-")
brand_lint.py --hook           PostToolUse hook-event mode (see note below) — NOT what to call
                                from a skill procedure; kept only because the script still ships
                                it, harmless if unused
brand_lint.py selftest         proves the checker's own counters; not for skill use
```

Invoke it as `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brand_lint.py ...` (plugin-level `scripts/`,
per this workspace's pathing convention — never a relative path).

**`--hook` mode is a dead end for a command-skill.** It expects a hook-event JSON blob
(`{"tool_input": {"file_path": ..., "content": ...}}`) on stdin, and it **always exits 0**
regardless of findings (advisory-by-construction for the retired PostToolUse wiring — it must
never block a write). A command-skill calling it this way would never see a non-zero exit to
react to. Use plain file-argument mode instead — that is the mode whose exit code actually
carries the verdict.

### Exit codes

- **0** — clean: no structural smells found in any file argument.
- **1** — at least one structural smell was found in at least one file argument (or in stdin).
- There is currently no dedicated usage-error (2) path in file-argument mode — an unreadable path
  is reported to stderr (`brand-lint: cannot read <path>: <OSError>`) and skipped, not treated as
  a hard failure; the exit code still reflects only the smell findings across the readable files.

### Output format

Per dirty file:
```
brand-lint: <N> structural smell(s) in <path>
  [<CODE>] line <N>: <line snippet, truncated to 90 chars>
      → <why this is a smell, one line>
```
(repeated per finding; a doc-level finding — currently only `VALUES-WITHOUT-TRADEOFFS` — prints
`document` in place of a line number.)

Per clean file: `brand-lint: clean — <path>`.

Stdin mode prints the same per-file block under the literal path `<stdin>`, or
`brand-lint: clean (no structural smells)` if clean.

### The five finding codes (what gets flagged)

| Code | Trigger |
|---|---|
| `ARCHETYPE` | "brand archetype(s)", a named Jungian archetype ("the Hero archetype", etc.), "12/twelve archetypes" |
| `VMV-TEMPLATE` | "vision, mission, (and) values", "mission statement", "our mission is to", "our vision is", "core values:" |
| `PERSONA` | "buyer/user/customer/audience persona(s)", or "meet <Name>, a NN-year-old …" |
| `BRAND-DNA` | "brand DNA" / "brand essence" |
| `VALUES-WITHOUT-TRADEOFFS` | a values-shaped block (has "value" or a bulleted/numbered list) naming ≥3 of a fixed empty-values vocabulary (integrity, excellence, innovation, passion, quality, respect, teamwork, authenticity, trust, collaboration, accountability, transparency) with no trade-off marker (" over ", " instead of ", "we choose", "even when", "at the expense", "rather than", " never ", " refuse", " sacrifice", " trade ") anywhere in that block |

Precision note: this is a **structural pattern match only** — it catches template language, not
whether a brand is actually good. A false negative (real bullshit phrased differently) is
expected; that judgment stays with the council/critics, never this script.
