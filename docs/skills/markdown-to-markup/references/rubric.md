# Rubric — markdown→markup rendering quality (rubric-md-to-markup)

Score a markdown-rendering change (a new inline/block form, or a renderer). The oracle pair is
injection safety + grammar correctness, proven by round-trip through [[html-to-markdown]].
Scoring method (1–5, `[gate]`/`[review]`, findings by severity, gate threshold) is summarized at
the bottom.

| # | Dimension | Type | What it checks | 1 → 3 → 5 |
|---|---|---|---|---|
| P1 | Injection safety | [gate] | Body text can never mint elements; hrefs can never smuggle a scheme | 1: `innerHTML` / `insertAdjacentHTML` anywhere on body content, or an unvalidated href scheme · 3: all text via `textContent`/Text nodes; elements via `createElement`; hrefs scheme-validated · 5: + a test proves a markup-bearing source string (`<img onerror>`, `[x](javascript:…)`) renders inert/rejected |
| P2 | Grammar correctness | [gate] | Parse order and nesting match the inline/block grammar | 1: wrong nesting/ordering; a form mis-parses (e.g. stars inside backticks get bolded) · 3: earliest-span-wins; code is verbatim (no inner parse); strong/em/link re-parse their inner; blocks delegate to the one inline pass · 5: + nesting cases proven (bold-wrapping-code renders; code-with-literal-stars stays literal) and blocks share the inline parser (no duplicate inline logic) |
| P3 | Graceful degradation | [review] | Malformed input degrades to literal text, never breaks the run | 1: an unpaired/malformed delimiter throws or corrupts the run · 3: an unpaired marker renders literally; malformed input never throws · 5: + the literal-vs-parsed boundary is tested for each form |
| P4 | Inline-class completeness | [review] | A change covers the whole inline class it touches, sized against the consuming corpus | 1: one delimiter added in isolation while sibling forms still render literally · 3: the change covers the inline class it touches (not a single-delimiter patch), and states what is deferred · 5: + the renderer handles the consuming corpus's full inline + block set — bind that set when instantiating in a repo (worked example: a docs corpus using code/bold/italic/link + paragraph/list/heading/fence) — deferrals named with their reason |
| P5 | Treatment & tokens | [review] | Rendered elements ride the target repo's semantic token roles, owned by its token layer | 1: a hardcoded colour/size on the rendered element; the inline-code treatment leaks into fenced blocks · 3: styling rides the target repo's semantic token roles — its token layer (the token-builder seat) owns the values; never a literal colour — and inline code reads distinctly from a fenced block (the inline treatment reset in blocks; worked example: a repo whose roles are `--c-*`/`--ui-*` styles the inline chip with them and resets the chip inside `<pre>`) · 5: + scheme + forced-colors safety verified for the rendered element |

**Gate to promote:** P1 and P2 must each score ≥ 3. An unsafe or mis-parsing renderer fails
regardless of polish — injection safety and grammar correctness are the load-bearing pair. P3–P5
below 3 are findings to fix.

---

**Scoring method.** `[gate]` = load-bearing, provable by a fixture or round-trip; `[review]` =
judgment against the anchors with cited evidence. Scale 1–5 (1 = failure anchor, 3 = adequate,
5 = excellence anchor); do not round everything to 3. Every score below 4 needs cited evidence
(the offending form + what it renders). A change that fails any gate dimension is not done
regardless of other scores.
