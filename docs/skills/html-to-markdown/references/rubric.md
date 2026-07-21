# Rubric — HTML→markdown conversion quality (rubric-html-to-md)

Score a conversion (a one-off transcription or a converter). The oracle is round-trip semantic
equivalence: the emitted markdown, re-rendered through [[markdown-to-markup]], must mean what the
HTML meant. Scoring method (1–5, `[gate]`/`[review]`, findings by severity, gate threshold) is
summarized at the bottom.

| # | Dimension | Type | What it checks | 1 → 3 → 5 |
|---|---|---|---|---|
| C1 | Semantic fidelity | [gate] | Round-tripped, the markdown renders to the same *meaning* as the HTML input | 1: meanings lost or changed — a heading became plain text, a link dropped its href, emphasis vanished · 3: every mapped semantic (headings, strong/em, code, links, lists, quotes) survives the round-trip · 5: + edge constructs handled (image alt, ordered-list numbering, link without href → text) and any unmappable construct is flagged, not silently dropped |
| C2 | Escaping correctness | [gate] | Text that would read as markdown is escaped; emitted syntax is not | 1: text copied verbatim; a literal `*`/`_`/leading `-` re-parses as syntax on round-trip · 3: markdown-special characters in text nodes are escaped; code/pre content is left verbatim (not escaped) · 5: + line-start cases handled (a leading `#`/`-`/`1.`/`>` in text is escaped) and proven by a round-trip that preserves the literal |
| C3 | Presentation stripping | [review] | Presentational markup is dropped, not smuggled through | 1: `class`/`style`/wrapper `div`s smuggled through (raw HTML in the output for presentation) · 3: presentational wrappers unwrapped (children kept); no class/style survives · 5: + raw HTML appears only for a construct with no markdown form, never for styling, and that choice is noted |
| C4 | Structure & nesting | [review] | List and blockquote structure survives the transform | 1: nested lists/quotes flattened; list ordering lost · 3: list and blockquote nesting preserved (indent / repeated marker); ordered vs unordered correct · 5: + deep/mixed nesting (list-in-quote, quote-in-list) round-trips faithfully |
| C5 | Whitespace & separation | [review] | HTML whitespace normalizes to markdown's block rules | 1: HTML whitespace copied literally (stray indents open phantom code blocks); blocks run together · 3: inter-element whitespace collapsed; one blank line between blocks; `<pre>` whitespace preserved · 5: + no accidental code-block indents; trailing/leading per-block whitespace trimmed |

**Gate to promote:** C1 and C2 must each score ≥ 3. A conversion that loses meaning or corrupts
text via missed escapes fails regardless of the rest — fidelity and escaping are the round-trip's
load-bearing pair. C3–C5 below 3 are findings to fix.

---

**Scoring method.** `[gate]` = load-bearing, provable by a round-trip; `[review]` = judgment
against the anchors with cited evidence. Scale 1–5 (1 = failure anchor, 3 = adequate, 5 =
excellence anchor); do not round everything to 3. Every score below 4 needs cited evidence (the
offending construct + its round-trip result). A conversion that fails any gate dimension is not
done regardless of other scores.
