# Figma custom skills — platform ground truth

Verified 2026-08-27 against Figma's own help pages and the Agent Skills specification.
Every fact below is [drift-prone]: re-verify on any Figma agent / Figma Make release note
that mentions skills.

## What a custom skill is

A custom skill is ONE markdown file that teaches the Figma agent (in Figma Design) and
Figma Make how to do a task the way your team does it. It is authored inside a Figma
file, persists across all your files, and can be published to a team or organization.
Source: <https://help.figma.com/hc/en-us/articles/40283639496599-Custom-skills-for-the-Figma-agent-and-Figma-Make>

This is NOT the same thing as "Figma skills for MCP" (`figma-use`, `figma-generate-design`,
… in `figma/mcp-server-guide` on GitHub) — those are ordinary Agent Skills directories a
CODING agent installs to drive Figma's MCP server, and they DO ship `references/`. This
skill authors the in-Figma kind only.

## The five platform facts that govern authoring

| # | Fact | Consequence for authoring |
|---|---|---|
| 1 | **Single file.** "Custom skills do not support optional directories such as `scripts/`, `references/`, and `assets/`." | Everything the skill needs is inlined in the one `.md`. A pointer to a sidecar is a dead pointer. |
| 2 | **Agent Skills frontmatter.** `name` (1-64, `a-z0-9-`, no leading/trailing/double hyphen) + `description` (1-1024, non-empty). Optional: `license`, `compatibility` (≤500), `metadata` (string map), `allowed-tools` (experimental). Source: <https://agentskills.io/specification> | Claude Code runtime keys (`disable-model-invocation`, `user-invocable`, `context`, `model`, `paths`, …) are not part of the standard and are stripped. |
| 3 | **`name` is the slash command.** `/follow-ds-guidelines` invokes the skill explicitly. Figma asks for "a specific, non-generic name" so published skills don't collide. | Name the job AND the system: `acme-button-rules`, not `buttons`. |
| 4 | **Automatic invocation keys on the description, and soft phrasing fails.** Figma's own note: "soft phrasing like 'use only when X is selected' tends to get read as 'don't use it unless X'." | Trigger clauses are active requirements: "Use when the user asks for a button…", never "only when". |
| 5 | **No validation, no size cap documented.** Figma checks nothing beyond the file loading. | `scripts/figma_skill_check.py` is the gate of record; length is governed by fidelity (the user's ruling: as long as it needs to be, never lose resolution), navigated by a head-first routing table. |

## The runtime the skill executes in

The skill runs INSIDE Figma's agent or Figma Make, not in a terminal. Concretely:

- **Tools available**: the canvas (selection, layers, components, variables, styles, auto
  layout, prototype links), Make's code generation (React + Tailwind + shadcn/ui by
  default), and chat with the user. **Not available**: a shell, file reads outside the
  Figma file, subagent dispatch, a `Skill` tool, `AskUserQuestion`, git.
- **Context**: the current file, current selection, published libraries the file can reach,
  and the chat. A rule that depends on repo state ("read the DESIGN.md at the root") has no
  root to read — the equivalent is "read the file's local variables / the linked library".
- **Invocation**: explicit (`/name` in chat) or automatic (description match). A skill fires
  as a whole; there is no progressive disclosure across files, only across headings inside
  the one file — hence the routing table at the top.

## Progressive-disclosure inside one file

The Agent Skills spec recommends `SKILL.md` under 500 lines and splitting to `references/`.
Figma removes the split. The substitute is structure inside the file:

1. Head (first ~60 lines): identity line, `## Contents` routing table (question → heading),
   hard rules, output contract.
2. Body: one `##` per source section, in source order, every threshold verbatim.
3. Tail: worked examples, then `## Dropped` (what was deliberately not carried, with
   reasons), then `## Provenance` (source, version, date, content hash).

Compaction/attention favors the head; the routing table lets the agent jump instead of
scanning. This is the same "structure is the prompt" principle `make-figma-make-kit`
applies to a Make `guidelines/` folder, collapsed into one document.
