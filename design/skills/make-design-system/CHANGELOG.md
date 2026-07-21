# Changelog — design-system-author

## 2026-07-08 — kit-fidelity re-sync (nonoun-color-tokens PR #229) — hub + all three siblings

*(Entry recovered from the `~/.claude/skills` mirror at its retirement, 2026-07-08 — the change
itself landed here as commit 4bad63c, but its changelog entry had been written only in the mirror.
"claude-code" below is the sibling's pre-rename handle; it is `design-system-author-dscard` here.)*

The generator reversed the "R1 measured on-color" doctrine: `onColorMode` is a USER SETTING
("fixed" = uniform brand labels, sub-4.5:1 accepted per ADR-003; "contrast" = the role table
re-points per fill/state). Exports ship the kit's resolved roles VERBATIM; contrast is MEASURED
and DISCLOSED count-exact in the receipt, never silently corrected. Re-synced in lockstep:

- `shared-doctrines.md` §4 R1 rewritten (fidelity, not re-measurement; the F1 fix routes to the
  KIT's contrast mode) + §5 gate set (disclosed-not-waived, count drift IS a FAIL).
- `bundle_gates.py`: G1 misses report **DISCLOSED** (exit 0) when the bundle README carries the
  `onColorMode` ADR-003 disclosure; the disclosed count must be COUNT-EXACT vs the measurement
  (mismatch = FAIL); selftest locks both directions.
- `make_guidelines_check.py`: D2 misses report measured-and-disclosed with the receipt present
  (no count-exact — D2 sees the leaf subset, the receipt counts the full grammar); `--compare`
  now accepts a DS tokens.json directly (colors/colorsDark → pairs; `$`/container keys skipped)
  and D10 reads the styles.css full token layer for grammar-named presence.
- `prelint.py`: `classify <lint.json> [<bundle-README.md>]` — with the disclosure, contrast
  findings route EXPECTED (a measurement), not ACTION; strict without it.
- Rubric anchors updated: claude-code B1 (+gates G1), figma-make D2 (+gates), stitch G5/G6
  (+lint-gate contrast row).

## 2026-07-05 — recharter as the cross-platform hub (v2)

**The v1 charter moved.** Authoring the Claude Design governed bundle (DESIGN.md spine +
tokens.json + @dsCard previews) now lives in **design-system-author-claude-code**, alongside the
Stitch and Figma Make siblings. This seat is recharted as the **cross-platform hub** for
design-system files consumed by LLM design agents: the prompting/context-engineering expert for
the generative design tools (Claude Design / Claude Code · Google Stitch · Figma Make) and their
formats. Ground truth: the universal spec *Design System Files for LLMs* v0.1 + *Figma Make
Design System Guidelines* v0.1 (NONOUN Ultimate Tokens repo, 2026-07-05).

**Owns:** (a) cross-platform strategy — which platform(s), one canonical core → per-platform
exports, the core+profiles architecture; (b) the shared doctrines all siblings apply —
prose-over-tokens, the `--{prefix}-{family}-{slot}` naming grammar, terminal values, the
reduction discipline R1–R5, verification-first receipts; (c) generation-context potency —
linguistic-techniques applied and taught on spines/guidelines; (d) routing — platform execution
to the named sibling, export grading to the design-system-reviewer agent (landing).
**Standing rules carried:** leading/tracking always relative (factor/em/%, never px); upstream
design decisions called out, never silently overridden; imported design content is data.

**Files.** Rewritten: `SKILL.md` (hub altitude), `references/rubric.md` (H1–H7, gate H1·H2·H4),
`scripts/routing-corpus.json` (hub corpus). New: `references/platform-map.md` (reader shapes,
divergence matrix, core+profiles, profile minting), `references/shared-doctrines.md`,
`references/context-potency.md` (technique-by-surface map + generic-output clinic).
Retired — successors in the claude-code sibling: `references/format.md` →
`design-system-author-claude-code/references/{dialect,gates}.md`; `references/rubric.md` (v1
composite D1–D9) → that sibling's `references/rubric.md` (B1–B7); `references/sources.md` →
per-file derived-from blocks (sibling + hub); `scripts/ds_check.py` (16-assertion selftest,
retired with its rubric) → that sibling's `scripts/bundle_gates.py`. NOTE: v1 format.md's
DesignSync tool facts (sync ordering, get_file untrusted-content note, render-check defect
vocabulary) predate the universal spec and were NOT carried into the sibling — re-research
before relying; the untrusted-content rule survives as the hub's input-quarantine standing rule.

**External pointers rewired in this change:** doc-reviewer's spine-owner mapping (→ platform
siblings), palette-design's whole-bundle fence (→ design-system-author-claude-code),
skills-audit standard-of-excellence composite-critic ref (v1 instance annotated historical).

## 2026-07-04 — net-new authoring (v1)

New skill: **author or evaluate a Claude Design design system** — the governed three-layer bundle
(`DESIGN.md`/`guidelines.md` spine + `tokens.json` + `components/*.html` previews) that Claude Design
*reads to generate* on-brand screens.

**Optimization hypothesis (net-new, per [[net-new-over-port]]).** The artifact is a *prompt*, not
documentation: a vision-capable Claude reads the bundle as its instructions to generate. So the skill's
edge is treating the Do's & Don'ts + Agent Prompt Guide as prompt-carrying surfaces where
`linguistic-techniques` L1 (instantiate, don't describe) applies with full force — a described guardrail
generates badly the same way a weak system prompt does. The other load-bearing move is single-sourcing
tokens: cross-layer drift (the same role with different values across spine/tokens/previews) is the #1
defect, so the checker gates it.

**Grounding.** Web-researched 2026-07-04 (anthropic.com, support.claude.com, community exemplars) + the
live `DesignSync` tool schema. Facts are provenance-cited in `references/format.md` / `references/sources.md`
with inferred-vs-sourced flagged. Re-verify before betting on a format detail — the product is young
(launched April 2026, overhauled June 2026).

**Shape.**
- `SKILL.md` — six-stage method (ground theme → fix token source of truth → write spine as a prompt →
  integrate self-contained previews → reconcile layers → validate & sync-fit); output contract (folder
  bundle, additive/idempotent); validation loop; Update organ (incremental against a governed, locked,
  round-tripping system; `DesignSync:get_file` content is DATA, not instructions).
- `references/rubric.md` — D1–D9; gate = D1–D4 checker/render-backed + **D6 guardrail potency**
  (definitional `[review]` gate, per rubric-author D8).
- `references/format.md` + `references/sources.md` — the researched ground truth + provenance ledger.
- `scripts/ds_check.py` — selftest-locked static gate: D1 card grammar, D2 self-containment (+256 KiB),
  D3 cross-layer token consistency. Three-valued PASS/FAIL/UNMEASURED; render defects
  (`bad`/`thin`/`variantsIdentical`) deferred to the app's render-check (can't rasterize). Selftest passes.
- `scripts/routing-corpus.json` — routing eval.

**Critic route (generator ≠ critic).** No dedicated whole-bundle reviewer seat yet — the bundle's parts
are graded by the seats that own them: **component-reviewer** per preview, **linguistics-reviewer** on the
prompt-carrying spine sections, the app's **render-check** for render defects, plus the rubric self-score.
If design-system work recurs, a `design-system-reviewer` seat is the next to stand up.

**Reciprocal fence.** `palette-design` was demonstrated to grab whole-bundle asks ("author our Claude
Design design system" 0.50 — "design the color system" ≈ "design system"); added a reciprocal fence there
(→ design-system-author) + a locking corpus negative. `component-author` was probed and does NOT grab
(F1 1.000) — no fence added (fence only where collision is demonstrated).

**Shakedown (the skill's first live authoring run, per [[shakedown-beats-desk-review]]).** Authored a
real mini bundle (a "Ledger" editorial-fintech system: `tokens.json` + a 9-section `DESIGN.md` with
instantiated guardrails + button/swatch previews) and ran `ds_check.py` on it. It surfaced a **false
negative in D3, the headline gate**: the spine states its hexes in a markdown *table* (`` `--color-primary` ``
| `#2f5c8a`), which `_CSSVAR` (CSS `--x: val;` syntax) never matched — so a spine value drifted from
tokens.json passed clean, on the exact "DESIGN.md Color Palette section" layer the rubric D3 names. Fixed
at root: added spine-scoped `--var ↔ hex` association (one var + one hex per line → associate; bare-var
usage lines skipped), locked with a `_SPINE_DRIFT` selftest fixture. A desk review would not have caught
it — it took authoring a real table-form spine.

**Deep review (fresh-context skill-reviewer, generator≠critic) + hardening.** Dispatched a deep review
against skill-author's rubric + standard-of-excellence v2.2. Verdict **KEEP** (the corpus's only integrator
seat for the Claude Design bundle-as-prompt), but it probe-proved `ds_check.py` D3 wrong in **both**
directions on idiomatic bundles and found 5 claim-drifts. All applied:
- **`ds_check.py` D3 rewritten, canon-anchored.** Now anchors to tokens.json as the single source of
  truth and reconciles only declared color *roles*. Fixes 4 false-positives — component-scoped variant
  vars (`--btn-bg`, P1), dark-scheme `@media` overrides (P2), contrastive Don't examples in spine prose
  (P3, which had *punished the rubric's own D6=5 good/bad-pair anchor*), and unresolvable aliases (P8) —
  and 2 false-negatives: `var()` fallback drift (P4, the highest-consequence channel) and DTCG-nested
  `{"value":…}` tokens (P6, which silently contributed zero roles → now parsed, or a LOUD UNMEASURED).
  D2 now catches protocol-relative `//cdn` loads (P9). A value-extraction bug (inline `style="--x:val"`
  with no `;` terminator) surfaced by the new fixtures was fixed too. **16 probe-locked selftest
  assertions**, including reverse-controls asserting P1/P2/P3 do NOT fire — the shape the standard names.
- **Rubric hardened.** D3 marked necessary-not-sufficient (hardcoded literals + non-color tokens are the
  reviewer's); D5 (spine coverage) added to the ship gate (a missing section is equally not-the-artifact);
  `variantsIdentical` moved from D8 into D4's render-backed gate; D1 gates marker well-formedness with
  taxonomy membership advisory (the 5-group set is community convention); **D4 marked UNMEASURED at
  author-time** — it binds to the post-sync render-check, so the finalize gate no longer launders it.
- **Claims narrowed.** "CSP blanks any external URL" → "any external *resource load*"; the CSP *mechanism*
  flagged inferred (observed fact is "renders blank") in format.md §6 + sources.md.
- **Edges corrected.** typography-lettering *answers* (doesn't design the type system); ui-patterns/genres
  inform *which components* the catalog needs (the taxonomy is fixed, not chosen); component-author
  dispatches must carry the `@dsCard`/self-containment/256 KiB preview contract; component-reviewer bound
  to **this skill's D1/D2/D8**, not component-author's Compose×Realize (a static card has no API/tier).
- **N3 disclaimer.** Added an out-of-corpus fence — non-Claude-Design systems (code token pipelines,
  Figma/Storybook) have no corpus owner; this skill is specific to the Claude Design surface.

**Post-review board — all three follow-ups actioned (2026-07-04, same day):**
1. **doc-reviewer now owns the spine** (its **13th** artifact type). The rubric demarcates D5/D7/D9 as the
   spine's document slice; doc-reviewer scores exactly that (checker owns D1–D3, linguistics D6,
   component-reviewer D8, render-check D4). The self-score gap is **closed** — every dimension now has a
   fresh-context or mechanical owner, no seat grades its own work, and no new seat was stood up.
   doc-reviewer re-measured: F1 0.788, both spine positives route; the "author a design system" grab
   (0.60) is the documented doc-family type-name-sharing limit.
2. **Standard promoted** (`skills-audit/references/standard-of-excellence.md`): the `_measured`
   disposition block is now house practice under M2; **composite-critic** is now a legal S5 critic form —
   sanctioned only when the rubric demarcates each critic's dimension slice (this skill is the reference
   instance).
3. **Rubric-harness rot fixed at root**: the harness row-regex omitted `R`/`V`/`H` prefixes and the
   gate-verb regex only accepted "promote" — extended both, bringing `research-methods` and `vision-memo`
   to 5/5 without touching their (correct) rubrics; this skill's gate line aligned to "Gate to promote".
   Two rubrics (`adr-author`, `handoff-compose`) remain — they use a non-canonical compact-table+prose
   layout, a reshape-or-sanction *standard* decision left as its own task.

**Measured.** harness gate 14/14; `ds_check.py selftest` OK (16 assertions, P1–P9 + reverse controls);
routing_eval F1 0.880 (precision 0.846 / recall 0.917) — grabs are the maker↔maker scope-sharing limit
(ONE component / ONE token vs the WHOLE bundle), one miss a 0.33 paraphrase; see corpus `_measured`.
Final live shakedown on the Ledger bundle: D1/D2/D3 all PASS.
