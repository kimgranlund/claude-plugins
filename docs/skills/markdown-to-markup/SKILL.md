---
name: markdown-to-markup
description: >-
  Render markdown source into safe DOM markup, or extend the renderer with a new
  inline/block form. Use for "render this markdown", "the backticks/stars show up
  literally", "add bold/links/italics to the doc renderer", or "is this markdown
  rendering safe from injection, it uses innerHTML" — inline/block grammar built via
  textContent, never innerHTML. NOT for converting HTML into markdown source, or
  defects a CONVERTER produced — stray divs, converted text re-rendering wrong
  (html-to-markdown). NOT for building a full design-system-styled Artifact page
  (make-artifact — that consumes tokens; this renders markdown grammar).
disable-model-invocation: false
user-invocable: true
---

# Harness — Markdown → Markup (rendering)

Turn markdown **source** into safe rendered **markup** (DOM elements). The unit is the target repo's renderer — a hand-rolled, **zero-dependency** pair: one block-level entry (called `renderMarkdownBody` throughout this skill) + one inline pass (`appendInline`). Binding requirement: when instantiating in a repo, name its actual renderer file first (a docs site typically keeps it beside the page code) — that repo owns the code, and renderer changes ship through the consuming repo's review seat, not through this skill. Extending the renderer IS the same transform: a new inline or block form implements markdown→DOM for its span, with the same return contract (elements appended to the parent) — which is why one skill owns both jobs. Two constraints define the work: the body is untrusted **data** (rendered via `textContent` — the one safety rule below), and any form the parser does not handle renders as **literal characters** — the failure mode that produces one-form-at-a-time churn.

## The one safety rule — `textContent`, never `innerHTML`

Every text run is placed with `textContent` or a Text node; an element (`<code>`, `<strong>`) is `createElement`'d and its text set with `textContent`. The *markup* comes from the parser's structure, never from the source string. `innerHTML` on markdown body is an injection hole — markdown is data, and data must not be able to mint elements.

## Inline grammar — `appendInline`, earliest-span-wins, recurse

One left-to-right pass over a text run; the earliest-starting span wins; the remainder after it recurses:

- `` `code` `` → a `<code>` element, text **verbatim** — no markup parsed inside (so `**x**` inside backticks stays literal).
- `**bold**` → `<strong>`, inner text **re-parsed** (so inline `` `code` `` inside **bold** still renders).
- `_italic_` → `<em>` (re-parsed); `[text](url)` → `<a>` with `href` via `setAttribute` (validate the scheme — no `javascript:`).
- An **unpaired** marker (`` ` ``, `*`, `_`, `[`) stays **literal** — the parser degrades gracefully.

The pattern for adding a form: a matcher for its delimiters, slotted into the earliest-match selection, producing a `createElement` + `textContent` (or a recursive `appendInline` for a container span). See `references/best-practices.md`.

## Block grammar — `renderMarkdownBody`, line-oriented

Blank-line-separated runs → `<p>`; `- ` lines → `<ul>`/`<li>` (each item's text through `appendInline`); `#`…`######` → `<h1>`…`<h6>` (heading text through `appendInline`); a fenced ```` ``` ```` run → a `<pre><code>` block, a **plain panel** (the inline-code chip treatment is reset inside a block). Each block delegates its inline content to `appendInline`, so inline parsing lives in exactly one place.

## Anti-patterns

- Hand-roll the small grammar and keep it zero-dep — no `innerHTML`, `dangerouslySetInnerHTML`, or markdown library (`references/foundations.md`).
- Cover the whole inline **class** when you touch the inline parser — one-form-at-a-time is what produced the code→bold→… churn.

## References & tools

| Path | Use when |
|---|---|
| `references/foundations.md` | The data-not-markup model, the inline/block split, why zero-dep |
| `references/best-practices.md` | The `appendInline` pattern, per-form mappings, escaping, the safety do/don'ts |
| `references/rubric.md` | Scoring a markdown→markup change — safety, completeness, graceful degradation |
| `scripts/routing-corpus.json` | The routing corpus of record — after any description change, re-run harness's `routing_eval.py` against it (where harness is installed) |
| `[[html-to-markdown]]` | The inverse direction — HTML *into* markdown source |

## Validation loop (round-trip)

The inverse transform is the checker: transcribe the rendered DOM back through
[[html-to-markdown]] and diff against the source markdown — a renderer that fails round-trip is
fixed at the grammar rule, never with output-specific patches.

No bundled checker script, deliberately: this transform is prose-in/prose-out — the checker IS the
round-trip through [[html-to-markdown]]; there is no separate deterministic surface to script.

**Done** when every form in the touched class renders as elements (nothing literal that should
parse), a markup-bearing source string renders inert, and the DOM transcribed back through
[[html-to-markdown]] matches the source markdown in meaning. **NOT done** while any covered form
still shows literal delimiters, any body text reaches the DOM via `innerHTML`, or the round-trip
shifts meaning.
