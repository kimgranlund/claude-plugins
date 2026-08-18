# Rubric — Artifact styling quality (rubric-artifact-styling)

**[verified, this pack's own axis files, 2026-08-18]** every numeric/structural anchor below
(74/62/54rem, ≤12px/≤16px radius, the tri-state, the surface-ladder rule) derives from
`platform-facts.md`, `token-architecture.md`, `type-and-layout.md`, `mermaid-reference.md`, and
`shells-and-genres.md` — this file states no new fact, it only grades against what those five
already establish.

Score a rendered Claude Artifact page (or a page's source CSS/HTML) against this pack's doctrine.
The oracle pair is theme integrity + token binding — a page that hardcodes colors or skips
`light-dark()` fails regardless of how good it otherwise looks. Scoring method (1-5, `[gate]`/
`[review]`, findings by severity, gate threshold) is summarized at the bottom.

| # | Dimension | Type | What it checks | 1 → 3 → 5 |
|---|---|---|---|---|
| R1 | Theme integrity | [gate] | Every color resolves correctly across the light/dark/system tri-state | 1: colors only inside a `prefers-color-scheme` block, or hardcoded with no dark pair · 3: every role is a `light-dark()` pair under `:root`, `color-scheme: light dark` present, `[data-theme]` overrides present · 5: + a manual `[data-theme]` toggle proven to flip resolution with zero duplicated variables |
| R2 | Token binding | [gate] | Every visual property traces to a role, never a literal | 1: a bare hex/oklch/rgb literal used directly in a non-`:root` rule · 3: every visual property reads a `var(--c-*/--text-*/--space-*/--r-*)`, roles traced to the source system · 5: + a tier-2/`_unbound` need routes to a named gap, never an ad-hoc invented color |
| R3 | Type doctrine | [review] | Faces match artifact doctrine unless explicitly overridden | 1: body/interactive faces ignore doctrine with no stated reason · 3: system-ui body, mono interactive (buttons/links/tabs/badges/kickers), width tier matches content class · 5: + an explicit override is named and justified where the source system's own faces are deliberately used |
| R4 | Diagram contract | [gate] | Mermaid diagrams survive the pipeline and re-theme | 1: multi-line `<br/>` labels, or an unthemed/light-locked SVG in dark mode · 3: single-line labels (detail on edges), `!important` re-theme block bound to page tokens, surface-ladder respected · 5: + `rx`/radius explicitly set, hidden-tab panels use `visibility: hidden` not `display: none` |
| R5 | Shell-genre fit | [review] | The page shape matches its content class | 1: a report/retro shipped as a dashboard/tile grid, or a chip-wall standing in for a mechanism diagram · 3: narrative single-scroll for reports/retros, tabbed chapters for handbooks, one mechanism diagram per HOW section · 5: + hero-as-thesis where a lead section exists, collapsed rosters instead of chip walls for long enumerations |
| R6 | CSP self-containment | [gate] | Nothing the runtime would block | 1: an external stylesheet/font/script URL, or a network dependency past the CDN allowlist · 3: fully single-file, only doctrine-approved system font stacks, no external `url()` · 5: + verified against `artifact_check.py`'s external-URL grep with zero findings |
| R7 | Readability | [review] | Width/spacing/radius match the doctrine's scales | 1: prose width unconstrained or so narrow content fragments · 3: width tier matches content class (74/62/54rem), spacing scale consistent, two-tier radius (controls ≤12px, surfaces ≤16px) respected · 5: + specificity pitfalls avoided (no injected third-party inline style silently winning over a page rule) |
| R8 | Provenance | [gate] | The footer makes staleness detectable | 1: no footer, or missing source path/build date/invocation · 3: footer names source path, `$generator` line where used, content source, build date, exact invocation · 5: + the footer alone is sufficient for a reader to detect staleness without re-running anything |

**Gate to promote:** R1, R2, R4, R6, and R8 must each score ≥ 3 — theme integrity, token binding,
the diagram contract, CSP self-containment, and provenance are load-bearing; a page that fails any
one of these is not done regardless of how the review-tier dimensions score. R3/R5/R7 are
judgment findings that degrade the score but don't block alone.

---

**Scoring method.** `[gate]` = load-bearing, provable by `artifact_check.py` or a fixture;
`[review]` = judgment against the anchors with cited evidence. Scale 1-5 (1 = failure anchor, 3 =
adequate, 5 = excellence anchor); do not round everything to 3. Every score below 4 needs cited
evidence (the offending selector/rule/line). A page that fails any gate dimension is not done
regardless of other scores.
