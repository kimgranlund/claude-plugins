# Gates, Receipt, and the Divergence Rule

Make validates nothing — no linter, no schema — so **the generator run is the gate of
record**. A guidelines folder that was never gated is unverified, whatever it looks
like. Gate mechanics below; scoring anchors in `rubric.md` (same dimension ids).

## 1. Mechanical gates (run `scripts/make_guidelines_check.py <guidelines_dir>`)

| Dim | Gate | Check | Failure it catches |
|---|---|---|---|
| D1 | Routing integrity | `Guidelines.md` exists at the root (exact name); every routed `*.md` resolves (relative to the citing file, else the folder root); every leaf reachable from `Guidelines.md` transitively | a dangling route Make follows into nothing; an unrouted leaf Make never finds |
| D2 | Contrast, all pairs | every 4-color token row (fill L/D + foreground L/D) MEASURED against 4.5:1 in BOTH schemes; plus every `-on-surface*` text token × every surface/background token, both schemes. Misses under the kit's `onColorMode: fixed` (disclosed in the bundle README, ADR-003) report as measured-and-disclosed, not FAIL — kit fidelity, PR #229 | the constant-`#FFFFFF` trap now routes to the KIT (`onColorMode: contrast`), never a projection-side re-point |
| D3 | Scheme parity | every token table row carries a light AND a dark value | a role present in one scheme only — a build error, not a style choice |
| D4 | Runtime block + trap | ≥1 paste-ready `light-dark()` block; every file using `light-dark(` also declares `color-scheme: light dark` | the dark end silently never firing |
| D5 | States as values | every `components/*.md` leaf (overview excluded) names `hover` with literal or state-token values | adjective states ("brightens slightly") → per-generation drift |
| D6 | Hard rules | `Guidelines.md` carries ≥1 `Do NOT` and ≥1 `IMPORTANT` | soft rules the platform docs say generation ignores |
| D10 | Carrier equality | with `--compare sibling.json`: runtime-block tokens equal the sibling export's values — same sRGB 8-bit triple within ±1/255 per channel (notation-aware: colors compared, not strings) | the same build shipping different values to different platforms |
| D11 | Relative leading/tracking | no `line-height:`/`letter-spacing:` declaration ends in px; no px leading in type-table cells (`16 / 24px`) or `lineHeight` values — unitless factor, em, or % only (FAIL severity) | absolute leading baked into one optical size — px values that hold at one size and break every other size the model sets |

Non-fatal notes the checker prints: leaves > 200 lines (progressive-disclosure
tripwire — split the file), translucent text tokens (contrast is backdrop-dependent;
verify upstream over each surface), 3-color rows (ambiguous columns).

**Known gap (tracked, not yet fixed):** D2 and D4 as written only recognize the
pre-shadcn shape — a literal `--token` table row and a `light-dark()` runtime block.
Since `shadcn-tailwind-flavor.md` became the standing default, a conforming bundle's
color facts live in `styles.css` (`:root`/`.dark` blocks + `@theme inline`), not in
`color.md` prose tables, and dark mode is a `.dark` class, never `light-dark()`. A
shadcn-flavored bundle will correctly D2/D4-FAIL against today's checker — that is a
checker bug, not a bundle defect. Until the checker gains a `styles.css`-aware D2/D4
path, verify contrast and parity for the shadcn shape by hand (as the receipt
template's extension-role lines demonstrate) and say so in the receipt; do not read a
green run as covering these files, and do not read a red run on `styles.css` content
as a real defect without checking which shape produced it.

`--compare` payload: `{"--token-name": {"light": "<css color>", "dark": "<css color>"}}`
— produce it from the sibling export (e.g. Claude Design's `tokens.json` maps, the
Stitch frontmatter pairs). **Without a sibling export, D10 is UNMEASURED**: record it
UNMEASURED in the receipt with the reason — never mark it passed, never silently omit
it. UNMEASURED does not block promotion; a laundered pass does.

`selftest` runs the same check functions over embedded fixtures (one passing folder +
one failing fixture per gate) — run it after any edit to the checker.

## 2. What stays judgment (D7–D9 — score against `rubric.md`, evidence cited)

- **D7 register + doctrine:** imperative voice ("Do NOT…") carries the sentences; the
  universal prose doctrine governs content — a specific named-world reference over
  adjectives, negative constraints first-class, every signature color's prose promise
  delivered by a token (prose–token accord: no color sold in prose without a token row,
  no token row absent from prose or a component recipe).
- **D8 naming grammar:** every token parses `--{prefix}-{family}-{slot}` with slots
  from the registry (see `templates.md` §2a); prefix stated once; prefix-adaptivity
  instruction present; 15–25 roles.
- **D9 disclosure + routing quality:** many short files; routers route by question;
  decision trees present in token files and overview; closed variant sets in every
  component leaf.

## 3. The receipt (README.md beside `guidelines/`)

Regenerated every build — never hand-edited into a second source of truth. Template:

```markdown
# {export name} — Figma Make profile export

Figma Make kit guidelines for **{theme}**. Generated {date} by {generator}.
**Contents:** `guidelines/` — {file list}. Drop the `guidelines/` folder into the Make kit.

## Profile receipt (checks run {date})
- 🟢 `Guidelines.md` routes to every leaf that exists; no dangling routes
- 🟢 Tokens named by the Ultimate Tokens grammar (`--{prefix}-{family}-{slot}`), naming
  instructions + prefix-adaptivity rule in `foundations/color.md`
- 🟢 All fill/foreground pairs ≥ 4.5:1, both schemes
- 🟢 Scheme parity: every role row states light and dark
- 🟢 Signature families present with usage boundaries
- 🟢 Component states ship as literal per-scheme values
- 🟢/🔎 Cross-carrier equality with sibling exports — 🔎 UNMEASURED when none exist (say so)
- ℹ️ Intentional omissions with reasons (e.g. "`setup.md` absent: no code package to wire")
```

🟢 pass · 🔴 fail (never ship) · 🔎 UNMEASURED (reason stated) · ℹ️ intentional omission.

## 4. The divergence rule

Upstream and implicit token systems arrive with decisions already made — a prefix, a
family split, a weight scale, an on-color policy. **Call out any upstream decision you
would have made differently; never override it silently.** The guidelines carry the
upstream system's decisions verbatim; divergence notes go to the author in the handoff
(not into the guidelines), and follow-up is at the author's discretion. Silent
"corrections" break carrier equality with every sibling export and detach the
guidelines from the verified model they claim to carry.

Same rule at Make level: Make's auto-generated baseline is an upstream-made decision
set too — hand-authored guidelines override it deliberately and visibly (the receipt
says what was overridden), not by accident.
