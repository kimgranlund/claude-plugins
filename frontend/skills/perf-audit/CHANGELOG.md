# Changelog

## 2026-09-05 · initial release (frontend 2.7.0)
- New skill: reproducible Lighthouse runs. `scripts/lh-run.mjs <url> [--preset desktop|mobile|both] [--runs 3] [--out dir]` pins `npx lighthouse@13`, headless Chrome, keeps the median-by-performance run per preset, writes `<slug>.<preset>.json` plus a runs sidecar; selftest parses the chat fixture (scores 78/92/96/91), locks slug/args/median selection, and runs the full audit path with a fake runner. DevTools download fallback, Chrome DevTools MCP and uimax-mcp named as optional with their caveats (no MCP dependency added). Provenance: 1rehfjf, 1rn63fb, 1s6fmjn.
