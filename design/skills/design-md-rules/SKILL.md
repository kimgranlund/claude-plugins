---
name: design-md-rules
description: >-
  Ground-truth knowledge of the DESIGN.md design-system spec format consumed by Claude Design and
  Claude Code. Use when reading, explaining, extending, or validating a DESIGN.md (or "design spec",
  "design system file"): file anatomy, "explain the frontmatter schema" (the YAML token layer), the --{prefix}-{family}-{slot}
  grammar, light/-dark scheme pairing, the pairing law, prose spine sections, Root Brand Architecture,
  @dsCard preview cards, disclosure-over-correction. Also loads as the knowledge substrate when
  creating a design system from a corpus of design files/css/descriptions. NOT for the end-to-end
  authoring workflow (make-dscard-kit); NOT for --md-sys-* role semantics
  (material-design-*-tokens); NOT for Stitch exports/lint (make-stitch-kit);
  NOT for grading a bundle someone else authored (design-system-checker agent); NOT for consuming
  a finished design system to build UI (the brand's own skill). Never framework-prescriptive;
  accessibility is disclosed, never enforced.
disable-model-invocation: false
user-invocable: true
---

# design-md-rules

A DESIGN.md is a **prompt, not documentation** — a SKILL for a brand: name + description in frontmatter, then knowledge (tokens), laws (rules), and a work order (procedures). Answer every format question from that identity, grounded in the corpus below; where the corpus and your prior-art instincts disagree, the corpus wins.

## Corpus

| File | Carries |
|---|---|
| `references/anatomy.md` | What the file is; the two layers (YAML frontmatter schema + prose spine); the 10 spine sections; open-endedness — the spine is a floor, not a ceiling; consumption contract |
| `references/grammar.md` | The `--{prefix}-{family}-{slot}` naming grammar; the five color laws; the `color-scheme` + `light-dark()` runtime idiom; disclosure over correction; scale/geometry rules |
| `references/brand-architecture.md` | The six Root Brand Architecture slots (values, voice, visual territories, cultural references, refusals, signature details); extraction vs invention; the sufficiency (stranger) test |
| `references/preview-cards.md` | `@dsCard` tag syntax; self-containment rule; what a bundle's card set covers |

Read the file whose subject matches the question; read all four before validating a whole DESIGN.md.

## Standing rules (apply to every answer)

1. **Openness is normative.** When asked "can a DESIGN.md have a section for X?", the answer is yes if a fresh agent would generate differently with it — the anatomy file's section test. Never present the reference spine as a closed schema.
2. **Values verbatim, consequences disclosed.** Recommend measuring contrast and disclosing misses; never recommend silently correcting a brand's values, and never impose accessibility gates the brand didn't set.
3. **Framework-neutral.** The format names roles, scales, and laws. If an example needs markup, plain HTML/CSS only — a DESIGN.md that mentions React/Svelte/Tailwind has leaked implementation; flag it when validating.
4. **Validation = laws first.** Checking a DESIGN.md, test in order: scheme parity → pairing law → complete typography levels → closed ladders → state-complete component recipes → the three-hard-rules block exists → Root Brand Architecture sufficiency (the stranger test). Report misses as a flat, specific list.
