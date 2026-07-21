# The Lint Gate — Running, Reading, and Receipting

The mechanical gate for every Stitch DESIGN.md this skill produces or evaluates. Facts derived from `github.com/google-labs-code/design.md` README (fetched 2026-07-05) + measured runs; rule table in `stitch-spec.md` §5.

## 1. The command and the bar

```bash
npx -y @google/design.md lint DESIGN.md                      # JSON to stdout; exit 1 on errors only
npx -p @google/design.md designmd lint DESIGN.md             # Windows-safe alias (bin-name collision)
```

**The bar: zero errors, every warning classified.** Exit code 0 is necessary, not sufficient — the linter never reads the dark scheme, the prose, or the pairing law, so the receipt (§4) records what the author verified beyond it.

## 2. Reading the JSON

```json
{
  "findings": [
    { "severity": "warning",
      "path": "colors.primary-base-dark",
      "message": "Color token defined but never referenced by any component" }
  ],
  "summary": { "errors": 0, "warnings": 29, "info": 2 }
}
```

- `findings[]` — one entry per finding: `severity` (`error` | `warning` | `info`), `path` (token path or section), `message`. Some builds add a `rule` field; when absent, infer the rule from path + message.
- `summary` — the counts; `summary.errors > 0` is the hard fail (and the CLI's exit-1 condition).
- **Read the message, not just the severity.** Upstream's own README shows a contrast finding at `warning` severity whose message ends "passes WCAG AA" — a *passing* check being reported. A finding whose message says "passes" is informational regardless of its severity label.
- `python3 scripts/prelint.py classify lint.json` applies §3 mechanically and exits 1 on errors or ACTION-class findings.

## 3. Interpretation table — expected vs action

*(Mirrored in `scripts/prelint.py classify` — the script is the executable source; change both together in the same edit.)*

| Finding | Class | Response |
|---|---|---|
| `broken-ref` (error) | **ACTION** | Fix the reference or define the token. The only error-severity rule; never ship. |
| Duplicate `##` heading / invalid color value (e.g. `light-dark()`) | **ACTION** | File is rejected at parse. Fix before anything else is meaningful. |
| `orphaned-tokens` on a `-dark`-suffixed token | **EXPECTED** | The documented inherent cost of scheme siblings: the alpha schema has no scheme axis, so components can only reference the light end. Count them, name the cause in the receipt, ship. |
| `orphaned-tokens` on a non-dark token | **REVIEW** | Legitimate when the token is prose-bound with no component property slot to reference it (e.g. `background`, `outline-variant` — no component property exists for page background or border color). Verify the prose actually uses it, record in the receipt. A token in *neither* prose nor components is a real orphan — cut it. |
| `contrast-ratio` below 4.5:1 | **ACTION**, or **EXPECTED** with the receipt | Without a disclosure: fix the pair — never waived. With the bundle README passed to classify (`prelint.py classify <lint.json> <README.md>`) carrying the `onColorMode: fixed` ADR-003 disclosure (kit fidelity, PR #229): the disclosed measurement — verify it is recorded, never silently fix. |
| `contrast-ratio` "passes WCAG AA" | **OK** | Informational pass despite the warning label. |
| `missing-primary` | **ACTION** | Add the documented `primary` compat alias of the brand's base fill — otherwise Stitch's agent auto-generates key colors. |
| `missing-typography` | **ACTION** | Ship the type scale — otherwise agents fall back to default fonts. |
| `section-order` | **ACTION** | Reorder to canonical. Costs nothing; forfeiting the parse does. |
| `unknown-key` (typo-like top-level key) | **REVIEW** | `colours:` → fix the typo. A deliberate extension group (`motion:`) does not trigger this rule; if it somehow flags, document it. |
| `token-summary`, `missing-sections` | **INFO** | Counts and absent optional groups. No response required. |

## 4. The receipt

Ship a short receipt (README or PR note) with every delivered DESIGN.md — the worked example's shape (Studio 54 build, 2026-07-05):

```markdown
## Profile receipt (checks run <date>)

- 🟢 `npx @google/design.md lint`: 0 errors — all 56 OKLCH values (incl. the alpha
  border) parsed and contrast-checked; tokens follow the `{family}-{slot}` grammar
- 🟡 29 warnings, all `orphaned-tokens`: the `-dark` siblings (inherent — the alpha
  schema has no scheme axis to reference them from; documented spec cost, not a
  defect) plus `primary-base-background`/`-outline-variant` (prose-referenced; no
  component property slot exists)
- 🟢 `primary` present as a documented compat alias of `primary-base`
- 🟢 Sections in Stitch canonical order; appended sections ride the unknown-section rule
- 🟢 Every `{path.to.token}` reference resolves
- 🟢 All fill/foreground pairs ≥ 4.5:1 in BOTH schemes (all-pairs policy, stricter
  than Stitch's component-pair warning) — [how verified, e.g. check-colors proof]
- 🟢 Standalone: the file passes every check with no sibling files present
```

Every 🟡 line must name its cause and class; an unclassified warning is an unfinished evaluation.

## 5. Pre-lint offline checklist

Run before touching npm — `python3 scripts/prelint.py check DESIGN.md` automates all of it:

1. Frontmatter fences present and the YAML subset parses; **no duplicate keys** in any map (YAML last-wins silently — a duplicate is a stealth value change).
2. **No duplicate `##` headings** (file rejection).
3. Canonical sections in canonical order; unknown sections noted as riding tolerance.
4. Every `{path.to.token}` reference (frontmatter *and* prose) resolves.
5. `primary` present in `colors` (alias counts).
6. **Scheme parity**: every `-dark` sibling has its base and vice versa — when any `-dark` key exists.
7. **No `light-dark()`** anywhere in frontmatter values.
8. Every base component entry with `backgroundColor` also declares `textColor` (else the contrast rule has nothing to check and the on-pair is probably missing).
9. Top-level keys outside the schema listed as extension keys; near-miss typos flagged.

## 6. What the linter never checks (the author still owns)

- **Dark-scheme contrast** — all fill/on pairs at the `-dark` end. Dispatch [[check-colors]] for the all-pairs × both-schemes proof.
- **Prose–token accord** — both directions (prose promises delivered; tokens explained).
- **Pairing-law integrity** — no crossed on-pairs in component definitions.
- **Role budget and reduction quality** — 15–25 roles, signature colors surviving, states as values.

These are rubric dimensions (`rubric.md`), verified by the author, recorded in the receipt.
