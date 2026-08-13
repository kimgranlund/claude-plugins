# Blast-radius checklist — where invocation strings hide

Grep every ground; record zero-hit grounds as checked. A ground skipped is a
future silent break.

## All kinds
- frontmatter `name:` of the artifact itself; folder / file stem
- `requires:` arrays estate-wide (git grep the exact name)
- exemptions array in naming.manifest.json (retire on rename)
- prose mentions inside other artifacts' SKILL.md bodies and references/
- CI configs, harness_check scripts, workflow.json

## Commands
- the `/name` invocation string in docs, prompts, other skills' procedures
- hooks that shell out to it
- `wraps:` declarations pointing at renamed skills (wrapper must be renamed
  in the same plan — wrapper identity requires name equality)

## Skills
- `performs:` on the derived agent (agent must be renamed in the same plan —
  the string arithmetic is the check)
- `wraps:` on any wrapper command (same-plan rename, as above)
- scripts/ paths referenced by other estate tooling (should be none —
  encapsulation check — but verify)

## Agents
- delegation strings in orchestrator bodies and prompts
- `performs` arithmetic against the (possibly also renamed) skill

## Post-conditions the plan must state
- validator passes on the post-state (rename-execute runs it as the gate)
- exemption count decremented iff the old name was exempt
