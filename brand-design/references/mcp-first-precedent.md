# brand-design is the first MCP-registered plugin in this estate

Confirmed 2026-08-19: across every plugin in the `kimgranlund/claude-plugins` estate (agent-protocols,
authorkit, brand-design, design, docs, harness, llm, screens, teamwork), `brand-design` is the ONLY
one that ships a `.mcp.json` (`brand-design/.mcp.json`, wiring the `brand-corpus` stdio server at
`${CLAUDE_PLUGIN_ROOT}/scripts/brand_corpus_mcp.py`) or declares a `userConfig` block in its
`.claude-plugin/plugin.json` (`corpus_dir`, the per-instance corpus path the server reads). No other
plugin in the estate registers an MCP server or a `userConfig` — this is a first, not a pattern with
existing siblings to match.

The server itself is a thin, read-only convenience layer: `list_brand_documents` and `search_brand`
are wrappers over a plain directory read + grep against `BRAND_CORPUS_DIR` (confirmed by reading the
server's own `call()` function, `brand-design/scripts/brand_corpus_mcp.py`). The real fallback for
"no MCP configured" needs no server at all — a Claude Code session already carries Read/Grep tools
that can do the identical directory read + grep directly against the corpus. That fallback statement
is documented in the `brand-corpus` skill itself (skills/brand-corpus/SKILL.md), not here.

**Action for Phase 5:** the root README's plugin-roster table should note brand-design as the
estate's first (and, as of this note, only) MCP-registered plugin when Phase 5 rewrites it — a fact
worth surfacing for anyone auditing what MCP wiring looks like in this workspace, since there is
nowhere else in the estate to look for a worked example.
