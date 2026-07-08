# Rubric — Claude Design Export Bundle

Scores one bundle (DESIGN.md + tokens.json + components/*.html + README receipt).
`[gate]` = mechanically checkable (`../scripts/bundle_gates.py <bundle-dir>`);
`[review]` = judgment with cited evidence on the 1–5 anchors. Derived from the
design-system-files-for-llms spec §7–§8 gates + prose doctrine (2026-07-05); one
rubric drives author, evaluate, and regenerate.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| B1 | Mechanical gates | [gate] | `bundle_gates.py` exit 0: contrast both schemes, scheme parity, carrier equality ±1/255, preview self-containment, reference resolution, section grammar, on-partner coverage, relative leading/tracking (any `lineHeight`/`letterSpacing` in px, in any carrier — unitless/em/% only), pill/chip padding consistency across previews (G9 — one value bundle-wide; the value itself being below the spacing scale is a sanctioned exception, `gates.md`, not a violation) | 1: any FAIL line (a DISCLOSED contrast line is NOT a FAIL — it is the kit-fidelity measurement under `onColorMode: fixed`, ADR-003, and must be count-exact vs the receipt) · 3: exit 0 with unexplained WARNs · 5: exit 0, every WARN/DIVERGENCE/DISCLOSED explained in the receipt |
| B2 | Theme specificity | [review] | Overview fixes ONE named world, not an adjective region | 1: "modern, clean, premium" · 3: a genre named but generic · 5: a specific reference that imports its own negative space, echoed by the Don'ts |
| B3 | Prose–token accord | [review] | Both directions: every color/face/effect the prose sells exists as a token; every role is narrated with usage boundary + refusals | 1: prose promises the tokens can't deliver (F2) or mute tokens · 3: roles listed, boundaries thin · 5: role-by-role prose with refusals; cut families have no prose residue |
| B4 | Role budget & signature coverage | [review] | 15–25 roles; the brand's signature colors present as bindable roles | 1: <15 roles or a signature color missing · 3: in band, signatures present but underspecified · 5: in band, every signature a named role with a scheme-correct pair and a small-read boundary |
| B5 | States & focus | [review] | hover/active/disabled as variant tokens; focus ring color AND geometry (width, offset) stated | 1: states as adjectives only · 3: hover/active tokenized, focus prose-only · 5: full state set as values + focus geometry explicit; Components section restates them |
| B6 | Preview pedagogy | [review] | Cards teach states, the pairing law, and the scale — not just resting states | 1: resting-state screenshots · 3: states shown on buttons only · 5: cards demonstrate states, on-pair bindings, type scale, spacing scale, AND the sanctioned badge/chip padding exception at a single consistent value; one `:root` light-dark block, no media-query fork |
| B7 | Receipt honesty | [review] | README receipt matches a fresh gate run; divergences and aliases called out, dated | 1: no receipt, or claims contradicting a fresh run · 3: results recorded, divergences omitted · 5: per-gate measured results + every DIVERGENCE/alias/known-cost named, dated, regenerated with the build |

**Gate to ship:** B1 must pass (exit 0) and every [review] dimension ≥ 3. A bundle
with green gates but a vague theme (B2) or a broken accord (B3) generates off-brand
screens with perfect contrast — the gates bound correctness, the review dimensions
bound fidelity.

**Top failures to look for first:** (1) constant on-colors that survive B1 only
because both ends happen to pass AA — check the DIVERGENCE lines against authorial
intent (B7); (2) a spine selling colors the reduction dropped (B3/B4 — F2); (3) cards
that render only resting states (B6) — the model imitates what it sees.
