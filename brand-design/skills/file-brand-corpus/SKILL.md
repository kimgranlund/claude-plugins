---
name: file-brand-corpus
description: >-
  Exports a brand engagement's deliverables as a navigable Markdown corpus plus a self-contained
  site/ viewer (sticky nav, per-page ToC, GFM tables, mermaid, DOMPurify-sanitized). Use when the
  user wants to export, publish, or turn brand work into a shareable corpus or site — "export the
  brand corpus", "make this brand a shareable site", "turn the brand docs into a navigable
  folder", "build the corpus site". Requires existing brand deliverables (run make-brand first if
  none exist yet). NOT for packaging into a distributable plugin/skill/MCP (file-brand) and NOT
  the one-page brand-stack summary (make-brand-stack).
disable-model-invocation: false
user-invocable: true
argument-hint: "[corpus dir — default ./brand-corpus]"
---

# file-brand-corpus

Lays out a brand engagement's deliverables as a clean Markdown corpus, then generates a
self-contained `site/` viewer beside it.

Target corpus dir: `$ARGUMENTS` (default `./brand-corpus`, the same default `make-brand-stack` and
`file-brand` use).

## Procedure

1. **Check the precondition.** There must be real brand work products to export. If the
   engagement hasn't produced any yet, say so and stop — point at `make-brand`; never invent
   deliverables to fill sections.
2. **Write the corpus.** Author the real deliverables as Markdown into `<corpus>/`, grouped into
   ordered top-level sections (a leading `NN-` orders a section and is stripped from the display
   name; include only what exists):
   - `00-strategy/` — positioning, brand strategy, the Foundation Canon
   - `01-research/` — cultural research, competitive landscape, audience
   - `02-identity/` — visual identity, logo, color, type, the expression system
   - `03-voice/` — voice & tone, messaging, copy patterns
   - `04-stewardship/` — guidelines, governance, do / don't

   Give each page a frontmatter `title:` (else its first `# H1` is used). Add `<corpus>/README.md`
   whose H1 is the brand name — it becomes the site title + home hero. Keep the corpus root clean
   Markdown, browsable and diffable on its own — no app files mixed in.
3. **Generate the viewer**, in one command:
   ```sh
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_sitemap.py" --init "<corpus>"
   ```
   This copies the reader (machinery only, never a bundled example) into `<corpus>/site/`, builds
   its sitemap, and drops a root `index.html` redirect → `site/` if the corpus root has none.
   Re-run it after editing the corpus. Optional polish: a `<corpus>/reader.config.json`
   (`{"title": "…", "sections": {"00-strategy": "one-line description"}}`) sets the site title and
   the home cards' section descriptions.
4. **Serve + verify.** `cd "<corpus>" && python3 -m http.server`, open
   `http://localhost:8000/site/`. Confirm the home cards list your sections (with descriptions if
   configured), and that a doc containing a raw `<script>` produces no dialog (DOMPurify strips
   it).

## Failure branches

- No deliverables exist yet → stop, point at `make-brand`; never fabricate sections.
- `build_sitemap.py --init` reports a missing or malformed `reader.config.json` → fix the JSON,
  re-run step 3; the site still builds without it (optional polish only).

## Done / NOT done

Done when `<corpus>/` is self-contained and portable (zip/share it, or host it on any static
server) and step 4's verification passes. NOT done if the site was generated once and never
re-run after a later corpus edit — the reader reads the sitemap, not the live files.
