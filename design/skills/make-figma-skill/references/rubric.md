# Rubric — a single-file Figma custom skill

Score every new or converted skill. Mechanical dimensions (F1–F7) are
`scripts/figma_skill_check.py`'s; judgment dimensions (R1–R5) are scored here with cited
evidence — a score without a fix is not a finding. Gate = every F passes (WARN allowed) AND
R1, R2 ≥ 3.

## Mechanical (the checker)

| Gate | Passes when |
|---|---|
| F1 frontmatter | `name` 1-64 `[a-z0-9-]`, no leading/trailing/double hyphen; `description` 1-1024 |
| F2 portable keys | No Claude-Code-only keys |
| F3 no sidecars | No `references/`, `scripts/`, `assets/`, `[[handle]]`, `${CLAUDE_PLUGIN_ROOT}`, `python3`/`node` invocations, `AskUserQuestion`, `Bash(` |
| F4 active trigger | "Use when / Use for / Trigger when" present; WARN on "only when/if" |
| F5 provenance | `## Provenance` with `source:` and `date:` (required for conversions); WARN without `hash:`/`inventory:` |
| F6 resolution | With `--source`: every source heading carried or Dropped; every `## Dropped` bullet carries a closed-set reason; every numeric anchor verbatim. UNMEASURED without `--source` — reported, never laundered into a pass |
| F7 head-first | > 300 lines ⇒ routing table/TOC in the first 60 lines |
| F8 trigger vocab | WARN: with `--source`, each source `expect: trigger` prompt sharing no content word with the description is named |

## Judgment

| Dim | 1 | 3 (gate floor) | 5 |
|---|---|---|---|
| **R1 Fidelity** | Rules paraphrased; thresholds rounded; failure branches gone | Every rule survives in meaning; every threshold verbatim; `## Dropped` explains each omission from the closed reason set | Byte-faithful where the source was normative; good/bad pairs intact with labels; a reader could reconstruct the source's contract from the export alone |
| **R2 Figma-native tooling** | Verbs still say "read the repo", "run the script", "dispatch the checker" | Every verb maps to a canvas/Make action per the tool map; transposed checks state an observable pass condition | Transposed checks name WHERE in Figma to look (variables panel, layer tree, code preview); self-review carries the rubric inline |
| **R3 Trigger quality** | Generic name; description is a label | Specific name; active "Use when" with ≥ 3 verbatim source `t*` phrasings; "Not for" names the `n*` neighbors | Description front-loads the highest-frequency phrasings; no phrase also appears in a sibling Figma skill's description |
| **R4 Navigability** | One wall of text | `## Contents` routes by question; hard rules + output contract in the head | Routing table entries name the exact heading; examples in the tail; nothing load-bearing past the fold |
| **R5 Regenerability** | No provenance | `## Provenance` names source path, version, date | Adds a content hash of the source tree and the inventory counts, so a later run can diff instead of re-reading |

## Receipt (write next to the export, or in the source's ledger)

```
figma-skill receipt — <name>
source: <path> @ <version> (hash <sha256[:12]>)   | net-new: <charter>
date: <YYYY-MM-DD>
checker: F1 ✓ F2 ✓ F3 ✓ F4 ✓ F5 ✓ F6 ✓|UNMEASURED F7 ✓   (exit 0)
judgment: R1 <n> R2 <n> R3 <n> R4 <n> R5 <n>   — evidence lines below
dropped: <count> (<reasons>)
in-figma check: <3 prompts run inside Figma with the skill loaded — fired? output matched assertions?> | UNMEASURED
```

**Done** = checker exit 0, R1/R2 ≥ 3 with evidence, receipt written with honest
UNMEASURED entries. **NOT done** = a green checker with R1–R5 unscored, an F6 UNMEASURED
on a conversion (the `--source` flag was available), or a receipt claiming an in-Figma
check that was never run.
