# Behavioral assertions — make-figma-skill

Checkable against the produced artifact (the exported `.md`) and the run's receipt.

1. The output is exactly one `.md` file with Agent Skills frontmatter (`name`, `description`) and no Claude-Code-only keys; `figma_skill_check.py` F1/F2 pass.
2. The output body contains zero sidecar references (`references/`, `scripts/`, `[[handle]]`, `${CLAUDE_PLUGIN_ROOT}`, `python3`, `AskUserQuestion`); F3 passes.
3. In convert mode, every `##`/`###` heading of the source SKILL.md and its cited references appears in the output or under `## Dropped` with a reason from the closed set, and every numeric anchor in the source appears verbatim; F6 passes (never UNMEASURED on a conversion).
4. The description opens with the job, carries an active "Use when …" clause with ≥ 3 verbatim source `t*` phrasings, and a "Not for: …" clause; no "only when/if".
5. The output ends with `## Dropped` and `## Provenance` (source path @ version, date, sha256 prefix, inventory counts).
6. The skill asks the user for the destination path in chat before writing (no default is assumed) and writes a receipt naming every checker gate's outcome, including UNMEASURED ones.
