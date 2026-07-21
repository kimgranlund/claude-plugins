---
name: check-translations
description: >-
  Reason about and verify the locale-shaped primitives a UI system must absorb. Use when auditing a UI for
  i18n — RTL/bidirectionality, logical-vs-physical CSS axes, script metrics (line-height — Arabic, CJK),
  locale-sensitive number/date/currency Intl formatting, pluralization, encoding/collation,
  and text-expansion budgets (German expansion): RTL support, dir/lang on text surfaces, icon mirroring,
  hardcoded/untranslated strings, or translation-expansion headroom across scripts and locales. NOT for
  choosing/pairing type or script anatomy (lettering-facts); NOT for text/background contrast, palette,
  or color-blind safety (check-colors); NOT for focus order, keyboard nav, hit-targets, or focus rings
  (check-focus); NOT for loading skeleton/spinner, CLS, or latency budgets (check-speed); NOT for
  undo/type-to-confirm or audit-trail UX (check-safety); NOT for color-space theory or palette math
  (color-space-facts); NOT for building a date-picker or language-switcher component (make-component).
disable-model-invocation: false
user-invocable: true
---

# check-translations — locale invariants, card-gated

Owns the locale layer of a product UI: text is not a string but a pair (content, locale). The
verify contract: **declare the text surfaces in a card → the checker gates the mechanical facts →
judgment covers only what code cannot see** (whether a line-height suits its script, whether a
mirroring policy is right, whether a translation reads naturally).

## The card

An **i18n surface card** (`*.i18n.json`) declares the text-bearing surfaces plus the system-wide
locale posture — per surface (only `id` required): `has_lang` / `has_dir` (true when the surface
**or a declared ancestor** carries it — inheritance counts for both), `hardcoded_strings[]`
(untranslated literals), `user_content` (user-authored text renders here — gates a missing `dir`;
use `dir="auto"`), `expansion_safe`, `string_regime: shortString|runningText` (which expansion
regime the surface's copy lives in — labels vs sentences; default runningText), `text:false` to
exempt a non-text surface; top-level: `rtl_supported`, `rtl_in_scope` (RTL locales are in product
scope — gates missing `dir` card-wide), `locale_formats.{dates,numbers,currency}`. A pre-i18n
project declares `i18n_layer: false` once: the per-surface gates collapse into ONE design-decision
finding (`LOCALE_POSTURE_UNDECLARED` — "no i18n layer exists — declare the locale posture in the
spec"), not 2×N red lines; adding `declared_posture` (e.g. "en-US only, prototype") softens that to
a single advisory. If no inventory exists, enumerate every surface that renders text or formatted
values (numbers, dates, currency, plurals, lists) from the codebase, and build a locale matrix
`{locale, script, direction, expansion}` — expansion read per regime from
`assets/locales/expansion-factors.json` (unknown locales take its `default`: shortString ×2.5,
runningText +40% / −30%). The card never carries the judgment tier: translation naturalness,
metric fit (whether a line-height suits its script), and mirroring rightness are step-3 judgment —
no card boolean can attest them.

## Procedure

1. **Enumerate** text-bearing and formatted surfaces plus target locales; build the card.
2. **Gate:** `python3 scripts/i18n-check.py <card.json | dir>` — a FAIL blocks the emit; fix the
   surface, not the card. `selftest` proves the checker itself.
3. **Judge what the checker can't:** check script metrics against the bands below; hunt
   physical-axis CSS on text surfaces; match each icon to its mirroring policy
   (`assets/mirroring/icon-policies.json`); verify bidi isolation at every interpolation point
   (`assets/bidi/isolation-points.json`) and Intl routing on every formatted surface
   (`assets/formatting/intl-surfaces.json`).
4. **Emit** the verdict — every violation cites the surface/CSS rule it evaluates and routes its
   fix to the artifact that can make it — plus per-locale entries where asked:
   `{tag, script, direction, expansion: {shortString, runningText}, lineHeightBand, minBodyPx}`.

## Invariants (the numbers)

| Invariant | Value | Source |
|---|---|---|
| Line-height bands | Latin 1.4–1.7 · CJK 1.55–1.8 · Arabic 1.6–2.0 · Devanagari 1.5–1.8 — one `line-height` rule is locale-incorrect | `assets/locales/script-metrics.json` |
| Min body size | Latin ≥ 14px · CJK ≥ 15px for equivalent legibility; `:lang()` may raise size 1 step for tall-ink scripts | `assets/locales/script-metrics.json` |
| Expansion budgets | regime-split (`string_regime`): **shortString** (≤ ~10 en chars — labels, buttons) +100–200% (de/fi/it ~×3, fr/pt ~×2.6, ru ~×2.5) · **runningText** (> ~70 chars) +30–50% European incl. Russian · CJK contracts (~×0.7) but glyphs run ~2× Latin width; unknown locale → shortString ×2.5 / runningText +40%; squish only to `contractionFactor` | `assets/locales/expansion-factors.json` (W3C/IBM-cited canon) |
| Axes | logical only (`inline-start`, `block-end`, `padding-inline-*`) on anything that holds or positions text — never `left`/`right` | — |
| dir/lang | declared on every text root (`dir="auto"` for user content); inheritance from a declared ancestor counts for BOTH `lang` and `dir` (an LTR-only app with `html lang` and default direction passes); gate `dir` absence only when RTL is in scope or user content renders | — |
| Bidi isolation | `<bdi>` or `unicode-bidi: isolate` around every runtime interpolation — user names, queries, filenames, tag chips | `assets/bidi/isolation-points.json` |
| Intl | numbers/dates/currency/relative-time/plurals/lists via `Intl.*` at render; `formatToParts` for mixed markup; currency carries `{amount, currency}`, never `"$12.50"` | `assets/formatting/intl-surfaces.json` |
| Truncation | `text-overflow: ellipsis` only where a tooltip/disclosure exists; silent truncation refused | — |

**Icon mirroring** (`assets/mirroring/icon-policies.json`): every icon declares
`mirroring ∈ {"always", "never", "ltr-only", "rtl-only"}` — no unset defaults. Directional
semantics (arrows, chevrons, undo/redo, indent/outdent) → `"always"`; logos, clocks, checkmarks,
media-play triangles (by convention) → `"never"`; progress direction flips with the writing
direction via logical-axis CSS, not icon mirroring (the file's note). Logical axes handle layout;
mirroring is a per-icon policy, never a blanket `scaleX(-1)` — that flips the clock and the logo.

## Detection catalog (what a review hunts)

Physical-axis CSS on text surfaces · build-time left↔right swap "for RTL" · one `line-height: 1.5`
across Latin + CJK + Arabic · server pre-formatted `"$12.50"` interpolated as a string ·
concatenated fragments (`"Welcome, " + name`) instead of ICU MessageFormat · silent truncation ·
locale-specific component forks (`ButtonRtl`) · Hebrew treated as interchangeable with Arabic ·
default `Intl.Collator` without `sensitivity`/`numeric` · direction toggled by a JS class instead
of `:root[dir]`.

## Mechanism gate — `scripts/i18n-check.py`

Whether a surface declares `dir`/`lang` and whether it carries hardcoded literals are mechanical
attributes — routed to code, never inference. The checker (stdlib-only, selftest-locked):

| Check | Severity | Fires when |
|---|---|---|
| `MISSING_LANG` | gate | a text surface with `has_lang` false or absent (own or inherited) |
| `MISSING_DIR` | gate | a text surface with `has_dir` false/absent (own or inherited) — gated **only** when `rtl_in_scope: true` or the surface has `user_content: true`; otherwise a default-direction LTR app passes |
| `HARDCODED_STRING` | gate | a surface whose `hardcoded_strings[]` is non-empty |
| `LOCALE_POSTURE_UNDECLARED` | gate | `i18n_layer: false` with no `declared_posture` — the three per-surface gates above collapse into this one finding; with `declared_posture` it reports once as the `LOCALE_POSTURE_DECLARED` advisory instead |
| `NO_EXPANSION_ROOM` | advisory | `expansion_safe:false` — the advisory names its regime (`string_regime`, default runningText): shortString ≤ ~10 en chars +100–200% · runningText +30–50% European incl. Russian (`assets/locales/expansion-factors.json`) |
| `NO_RTL` | advisory | `rtl_supported:false`; escalated when a surface declares `dir` handling |
| `NO_LOCALE_FORMAT` | advisory | a `locale_formats` family is false — route it through `Intl.*` |

Absent card sections are **skipped and reported**, never silently passed — an empty card is never
a false "OK"; a malformed card errors cleanly. The gate is **necessary, not sufficient** — a clean
run proves `dir`/`lang` are present and no literals were declared; step 3 proves the metrics,
mirroring, and isolation actually hold.

## Family mechanics (canon: [[check-whole-ui]]'s `references/verify-mechanics.md` — cited, not restated)

- **Findings format:** `file:line — [RULE_ID] finding → fix` — checker names above for
  mechanical; judgment findings take the slugs `i18n.mirroring` (what flips vs what doesn't) ·
  `i18n.bidi-isolation` · `i18n.intl-formats` · `i18n.naturalness` (translation register).
- **Symptom index:** "the text is cut off in German" → `NO_EXPANSION_ROOM` · "the layout breaks
  in Arabic" → `NO_RTL` / `MISSING_DIR` · "dates/numbers look wrong for French users" →
  `NO_LOCALE_FORMAT` · "translators can't reach this string" → `HARDCODED_STRING`.
- **Armed mode:** no card/artifact in play → the invariants become standing session constraints for
  subsequent UI work; one-shot mode unchanged.
- **Disputed finding** → the canon's waiver ladder — the card's per-surface flags
  (`text: false`, `string_regime`, `rtl_in_scope`) are rung 2; `declared_posture` is not a
  waiver instrument, it is the posture-gate's own resolution (card-wide, spec-tier). After any
  fix: same-scope re-run, none new (canon §3).

## Material & routing

| Path / peer | Use |
|---|---|
| `assets/locales/script-metrics.json` | per-script line-height bands + min body sizes |
| `assets/locales/expansion-factors.json` | canonical per-locale expansion / contraction factors |
| `assets/mirroring/icon-policies.json` | mirroring-policy table for common icon types |
| `assets/formatting/intl-surfaces.json` | the surfaces that must route through `Intl.*` |
| `assets/bidi/isolation-points.json` | slot types that require bidi isolation |
| [[lettering-facts]] | script-metrics ground truth behind the bands |
| [[make-component]] | fix owner for surface/markup findings — dir/lang wiring, logical-axis CSS, truncation affordances land there |
| docs' `make-doc` (where installed) | fix owner for the posture — `declared_posture` is a spec/PRD decision, not a UI patch |
| [[check-whole-ui]] | the set-scoped sweep that composes this verifier |

**Done** = card built, `i18n-check.py` green (or the posture gate resolved in the spec), step 3
judged per surface (metrics · mirroring · isolation · Intl), every finding routed to its fix
owner. **NOT done** = a green gate with step 3 unwalked (necessary, not sufficient), a posture gap
patched in the card instead of the spec, or a finding left without an owner.
