---
name: html-to-markdown
description: >
  Convert HTML content into markdown source. Use when bringing HTML content into a markdown corpus,
  transcribing a rendered page or fragment back to markdown source, or producing the markdown a renderer
  will consume ("convert this HTML to markdown", "turn this page into markdown source", "make markdown
  from this fragment") — map semantic elements to markdown syntax (headings, strong/em, code/pre, links,
  lists, blockquotes), drop presentational markup, and escape text that would otherwise read as markdown.
  NOT for rendering markdown onto the page or into the DOM, or extending the doc renderer with
  bold/links/italics (markdown-to-markup).
disable-model-invocation: false
user-invocable: true
---

# Harness — HTML → Markdown (transcription)

Take HTML (a fragment, a rendered page, a pasted block) and produce equivalent **markdown source**. This is the inverse of `markdown-to-markup`: there, markdown is the data and DOM the output; here, HTML structure is the input and markdown the output. The transform is **semantic and lossy by design** — it keeps meaning (a heading, a list, emphasis) and discards presentation (a `div`, a class, an inline style).

## Map semantics to syntax, drop presentation

Walk the element tree; map each **semantic** element to its markdown; **unwrap** purely presentational containers (keep their children, drop the wrapper). The full element map is `references/best-practices.md` — that file is the canon; consult it rather than reconstructing the mapping. Pinned here are only the rows conversions actually miss:

| HTML | Markdown |
|---|---|
| `<div>` / `<span>` / class / style | **unwrapped** — children kept, wrapper dropped |
| `<pre><code>` | fenced ```` ``` ```` block — inner whitespace verbatim, inner text NOT escaped |
| text nodes | **escaped** (next section) — the element mapping alone is never the whole job |

## Escape text that would read as markdown

Plain text copied verbatim is a bug: a literal `*`, `_`, `` ` ``, `#`, `[`, `]`, or a leading `- ` / `1.` in the *text* must be backslash-escaped so it does not become syntax on re-render. **Escape the text content, not the syntax you emit.** This is the single most-missed step and the difference between a faithful round-trip and corrupted output.

## Round-trip is the correctness test

Good output, fed back through a markdown renderer, yields markup **semantically equivalent** to the input (same headings, emphasis, links, list structure) — not byte-identical HTML (presentation was intentionally dropped). If a round-trip changes meaning, the conversion is wrong.

## Don't

- Don't keep `class`/`style`/`id`/wrapper `div`s — markdown has no slot for them; unwrap.
- Don't copy text unescaped — escape markdown-special characters in text nodes.
- Don't flatten structure — preserve list nesting and blockquote depth (indent / repeat the marker).

## References & tools

| Path | Use when |
|---|---|
| `references/foundations.md` | The semantic-vs-presentation model, lossy-by-design, round-trip equivalence |
| `references/best-practices.md` | The full element map, the escaping rules, nesting/whitespace, code & link handling |
| `references/rubric.md` | Scoring a conversion — fidelity, escaping, presentation-stripping, structure |
| `scripts/routing-corpus.json` | The routing corpus of record — after any description change, re-run `skill-author`'s `routing_eval.py` against it |

## Validation loop (round-trip)

The inverse transform is the checker: render the emitted markdown back through
[[markdown-to-markup]] and diff the DOM shape against the source fragment — headings, emphasis,
links, list structure survive; presentational markup does not. A conversion that fails round-trip
is re-fixed at the mapping, never patched in the output.

No bundled checker script, deliberately: this transform is prose-in/prose-out — the checker IS the
round-trip through [[markdown-to-markup]]; there is no separate deterministic surface to script.

**Done** when the round-trip preserves every heading, emphasis span, link, and list/quote nesting,
no `class`/`style`/wrapper survives, and every literal special character is still literal after
re-render. **NOT done** while any meaning shifts on round-trip, presentational markup leaks
through, or unescaped text re-parses as syntax.
