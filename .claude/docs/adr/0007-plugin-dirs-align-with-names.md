---
doc-type: adr
id: adr-0007
status: accepted
ratified: by Kim
date: 2026-07-21
owner: kim.granlund
supersedes: adr-0006 (the frozen-dir clause of its install-identity decision only)
---
# ADR-0007 — Plugin directories align with plugin names

## Context

ADR-0006 renamed every plugin and member to the simple paradigm but kept directory names
FROZEN at `<name-and-version-at-creation>` (`forge 1.14.0/`, `scribe 0.1.0/`, …), bridging
old paths to current names through a CLAUDE.md alias table. With the campaign merged
(PRs #62–#70), the frozen paths stopped carrying information and started costing it: the
marketplace read `"name": "harness", "source": "./forge 1.14.0"`, every scripted path needed
quoting for the embedded space, and each reader needed the alias table to map dir → plugin.
Kim ruled on 2026-07-21 (post-merge, on seeing the marketplace mismatch): align the physical
folder names with the plugin names.

## Decision

1. Each plugin's directory is named exactly its CURRENT manifest `name` — no version suffix,
   no spaces: `harness/`, `docs/`, `teamwork/`, `screens/`, `design-kits/`, `agent-protocols/`,
   `color/`, `typography/`, `llm/`. The version lives in the manifest and the README footer
   ledger, never in the path.
2. A future plugin rename renames its directory in the same change, with the same sweep
   discipline ADR-0006 used for names (guarded replacements, ledger history untouched,
   insertion audit).
3. The CLAUDE.md alias table is retired; the frozen-dir clause of ADR-0006 is superseded.
   Ledgers, CHANGELOGs, and prior ADRs keep the old paths as history.

## Consequences

- Paths are self-describing and quote-free; the marketplace `source` matches the plugin `name`.
- `git log --follow` crosses the rename; the old paths remain greppable in history only.
- Anything caching absolute paths (installed-plugin caches, external notes) re-points on the
  next `claude plugin marketplace update` + plugin update.
