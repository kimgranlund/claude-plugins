# Rubric — Figma Make guidelines/ folder

Scores a generated `guidelines/` folder (plus its receipt) for conformance and
generation-worthiness. `[gate]` = mechanically checkable — run
`scripts/make_guidelines_check.py <guidelines_dir>`; `[review]` = judgment with cited
evidence on the 1–5 anchors. One rubric drives all three operations (create ·
evaluate · regenerate): the standard that scores a folder is the one that builds and
repairs it.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| D1 | Routing integrity | [gate] | `Guidelines.md` at root; every route resolves; every leaf reachable from the entry | 1: dangling route or unrouted leaf · 3: all routes resolve, flat file-list routing · 5: complete two-level routing (entry + overview), routed by question, no orphans |
| D2 | Contrast | [gate] | every declared fill/foreground pair ≥ 4.5:1 in both schemes; `-on-surface*` × surface all-pairs included | 1: any UNDISCLOSED pair below 4.5:1 (misses under the kit's `onColorMode: fixed`, disclosed in the bundle README per ADR-003, report as measured-and-disclosed — kit fidelity, PR #229) · 3: all pairs pass or every miss disclosed · 5: all pairs pass with headroom on body-text pairs, translucent tokens annotated with their backdrop proof |
| D3 | Scheme parity | [gate] | every token row states a light AND a dark value; identical role inventory across schemes | 1: any single-scheme row · 3: parity holds · 5: parity holds and per-scheme differences (e.g. inverted on-pairs) are stated, not implied |
| D4 | Runtime block + trap | [gate] | a paste-ready `:root` block: `color-scheme: light dark` + one `light-dark()` line per role | 1: no block, or `light-dark()` without `color-scheme` · 3: block present, trap satisfied · 5: block covers every table role exactly, trap named in prose beside it |
| D5 | States as values | [gate] | component leaves ship hover/active/focus/disabled with literal or state-token values per scheme | 1: adjective states or none · 3: hover with values in every leaf · 5: full state set incl. focus ring geometry and disabled mechanism, per scheme, per variant |
| D6 | Hard rules | [gate] | `Guidelines.md` carries `Do NOT` prohibitions under an `IMPORTANT` marker | 1: no prohibitions · 3: generic prohibitions present · 5: prohibitions carry the theme's specific refusals and usage boundaries |
| D7 | Register + prose doctrine | [review] | imperative voice; specific named-world reference over adjectives; prose–token accord (every prose promise is a token; no orphan tokens) | 1: adjective soup or prose selling colors no token delivers · 3: imperative, reference present, accord mostly holds · 5: one named world, refusals first-class, accord exact in both directions |
| D8 | Naming grammar | [review] | tokens parse `--{prefix}-{family}-{slot}`, slots from the registry; prefix stated once; prefix-adaptivity instruction present; 15–25 roles | 1: invented names or no grammar section · 3: grammar section + conforming names · 5: fully constructed vocabulary, slot subset stated, adaptivity rule verbatim |
| D9 | Disclosure + routing quality | [review] | many short files (leaves ≲ 200 lines); decision trees in token files + overview; closed variant sets per leaf | 1: one monolith or leaf dumps · 3: short files, trees present · 5: every leaf single-purpose, trees route every case, variant sets closed with "nothing else" |
| D10 | Carrier equality | [gate] | with `--compare`: runtime tokens equal the sibling export (same sRGB triple ±1/255); without: UNMEASURED, recorded | 1: unequal values, or UNMEASURED laundered into a pass · 3: equal, or honestly UNMEASURED with reason · 5: compared against every sibling export of the build, receipt cites the run |
| D11 | Relative leading/tracking | [gate] | no px `line-height`/`letter-spacing` declarations; no px leading in type-table cells or `lineHeight` values | 1: any px lineHeight/letter-spacing · 3: all values unitless/em/% · 5: 3 plus the typography file states the rule |

**Gate to promote:** D1–D6 and D11 must pass the checker; D10 must be pass or an honest
UNMEASURED (reason in the receipt); D7–D9 must each score ≥ 3 with cited evidence. A
folder with a dangling route (D1), a failing pair (D2), or a missing `color-scheme`
declaration (D4) is not shippable regardless of prose quality — Make will not catch it.

**Top failures to look for first:** (1) the silent reduction bug — constant foreground
values that pass in light and fail in dark (D2); (2) an unrouted leaf added after the
router was written (D1); (3) states written as adjectives in a late-added component
leaf (D5); (4) a receipt that claims carrier equality no run ever measured (D10).
