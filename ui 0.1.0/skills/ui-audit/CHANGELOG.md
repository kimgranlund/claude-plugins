# Changelog

## 2026-07-03 — real-world shakedown: 6 correctness bugs in ui-probe.mjs + inventory-scan.py
Not a review-driven pass — a shakedown agent ran `ui-probe.mjs` against a real multi-page,
auth-gated, design-system-driven SPA (adia-pay/prototype-002) for the first time since the
2026-07-02 review campaign hardened this corpus. Every prior review was desk-based (read the code,
run the selftest fixture, which is a single-page, no-auth, plain-`rgb()` static HTML page); none
of the four review batches caught any of these, because the fixture never exercised the failure
modes. All six bugs below are confirmed via direct evidence against the real app (exact ratios/
counts cited in each fix), not inferred. Full findings ledger:
`skills-audit/campaign/shakedown-2026-07-03.findings.jsonl`.

- **`joinURL()` broke on file-style/directory-style baseURLs (CRITICAL).** The hash-route branch
  (`base.replace(/\/?$/, '/') + route`) unconditionally forced a trailing slash onto `base` before
  string-concatenating — for a FILE-style base (`.../prototype-002.html`, the shape of any
  multi-page Vite app) this inserted a spurious `/` after the filename; the dev server's SPA
  fallback then silently 200'd that malformed URL as the WRONG page (the chooser/landing screen)
  for all 24 real screen/scheme captures, reporting "0 skipped" the whole time. The generic
  `new URL(route, base)` branch had a second, related bug: a directory-style base with no trailing
  slash gets its last path segment REPLACED by a bare relative route instead of appended-under.
  Fix: `joinURL` now routes fragment-only/query-only routes and absolute-path routes through
  `new URL()` directly (both are trailing-slash-independent by the URL spec), and normalizes a
  bare-relative-route base to carry a trailing slash first. Unit assertions cover both historical
  failure modes plus the exact real-world repro (`joinURL('http://localhost:5173/prototype-002.html',
  '#/statement')`).
- **`parseCssColor()` couldn't parse `oklch()`/`oklab()` (CRITICAL).** Chromium's computed-style
  serialization returns `oklch(...)` for colors sourced from CSS custom properties in a modern
  design system (confirmed: adia-pay's `@adia-ai/web-components`) — every unparsed color was
  silently DROPPED, and enough drops emptied surface cards entirely (`pairs_unparsed ==
  pairs_total_raw`, `pairs: []`), which `contrast-check.py` then reported as a trivial false PASS
  on empty data — UNMEASURED laundered into PASS, the exact failure this skill's docstring forbids.
  Fix: full CSS Color 4 OKLab→XYZ_D65→linear-sRGB→gamma-sRGB conversion chain (oklch + oklab,
  percentage/`none` forms), matrices ported verbatim from this corpus's own `color-science` pack
  (`references/techniques/oklab-xyz-math.md`, `src/spaces/srgb.ts`, `src/transfer/srgb.ts`) rather
  than re-derived. Verified bit-exact against the shakedown's independent ground truth: re-running
  the fixed probe against the real app reproduces the SAME contrast ratios (e.g.
  `rgb(102,121,128)` on `rgb(240,248,252)` = 4.24:1) that a completely separate canvas-rasterization
  technique measured.
- **Settle strategy missed `setTimeout`-scheduled async content (HIGH).** `networkidle` +
  double-rAF waits for network quiet + one paint tick, not scheduled DOM updates with no further
  network activity (a loading-skeleton → real-content pattern) — confirmed: a screen's raw
  text-pair count was 2 (skeleton chrome only) at the old settle point, 72 (full real content)
  once the wait was extended. Fix: a bounded DOM-quiescence wait (`WAIT_FOR_DOM_QUIESCENCE`, a
  `MutationObserver`-based in-page collector — quiet window `SETTLE_QUIET_MS` = 200ms, hard cap
  `SETTLE_MAX_CAP_MS` = 4000ms so a live-clock/animation page can't hang the probe) runs before the
  existing double-rAF paint-settle step. Re-verified against the real app: the same screen now
  reports 72 raw text pairs, matching the shakedown's independently-confirmed settled count exactly.
- **Auth-gated routes captured as the login page, silently mislabeled (CRITICAL).** The probe has
  no auth model; a fresh unauthenticated context redirected to the login screen, and the probe
  captured + labeled the LOGIN page's content under the gated screen's id — 0 skipped, 0 errors,
  6 of 12 real screens affected. Fix, two parts: (a) mandatory, always-on detection —
  `routeMismatch(expectedURL, actualURL)` compares the landed path AND hash (a client-side
  auth-guard bounces the hash, not necessarily the path) against what was requested, checked AFTER
  the settle wait (a redirect can be a post-load JS bounce); a mismatch throws so the screen is
  honestly SKIPPED with both URLs named, never captured. (b) optional `--storage-state <path>` CLI
  flag threads a Playwright storage-state snapshot into every screen's context for callers who can
  pre-authenticate. Re-verified against the real app: re-running with genuine hash routes (no
  workaround) now correctly SKIPS all 6 gated screens with the exact redirect named
  (`landed on .../#/login`), and a 7th screen's own internal magic-link redirect
  (`#/s/valid-demo-token` → `#/summary`) is caught identically — while the 6 non-gated screens land
  on the right page and produce real, screen-specific cards.
- **Focus methodology couldn't detect `:focus-visible`-gated rings — mass false positives, THE
  MOST IMPORTANT FIX (CRITICAL).** The prior docstring's claim that "scripted focus with no prior
  pointer input matches `:focus-visible` in Chromium" is FALSE: Chromium's real `:focus-visible`
  heuristic keys off input modality, and a bare `el.focus()` call is not reliably treated as
  keyboard-equivalent. Confirmed via direct A/B on a real `:focus-visible`-only component (adia-ui's
  button, styled via `:scope:focus-visible{outline:none;box-shadow:var(--button-focus-ring)}`):
  programmatic focus never triggered the ring; genuine `page.keyboard.press('Tab')` did, every
  time. This produced ~60 false `NO_VISIBLE_FOCUS` findings across one real app — the single worst
  failure mode a "measured, not computed" probe can have (telling a team their accessibility is
  broken everywhere when it is correct). Fix: `COLLECT_FOCUS` split into `COLLECT_FOCUS_SETUP`
  (SEL-based enumeration + existence check via programmatic focus, unaffected — geometry/existence
  don't need real modality) and a new `driveKeyboardFocus` driver loop in `probeScreen` that
  alternates real `page.keyboard.press('Tab')` calls with small `page.evaluate` reads
  (`READ_ACTIVE_ELEMENT`), matching `document.activeElement` back to a candidate via a live
  `window.__focusEls` index. Bounded at 2x the enumerated count (floored at 6): a candidate never
  reached within the bound OMITS `visible_focus` entirely (UNMEASURED-for-this-element, matching
  `focus-check.py`'s existing omit-don't-guess handling — an absent key skips the gate) rather than
  guessing. Top docstring corrected to describe the real methodology. Re-verified against the real
  app: every real `button-ui` component across 4 unaffected screens (login, summary, assistance,
  insuranceExplainer) now correctly measures `visible_focus: true`; `tabindex="-1"` skip-targets
  (never reached by real Tab, by design) correctly omit the key instead of guessing.
- **`inventory-scan.py` silently dropped the real view file on an id collision (MEDIUM,
  companion fix).** When a route detector's slug matched a file-per-view detector's slug for the
  SAME logical screen, `setdefault()` let whichever ran first (always the route detector,
  attributing to a router/app file, not the real view) win — silently discarding the real view
  file for 7 of 12 real screens, which compounded into wrong verb counts and understated
  module-reuse spread (both computed against the `file` field) by more than half. Fix: the
  file-per-view detector now CORRECTS a route-detector's file attribution to the real view file
  (never silently no-ops) and disambiguates two genuinely DISTINCT view files that collide on the
  same slug (parent-directory-suffixed id) — either way, recorded in a new `meta.collisions[]`,
  never silent.
- **Filed, not fixed this wave:** ring detection only recognizes CSS `outline`, not `box-shadow`
  (adia-ui's actual ring technique) — SC 2.4.11 ring-contrast stays unmeasurable for that design
  system even after the `:focus-visible` fix above; noted in the top docstring as a known gap, not
  silently wrong. See the shakedown ledger for the full evidence trail.
- `ui-probe.mjs` gained an `import.meta.url` main-guard so importing it to reuse exported pure
  functions/card builders no longer re-executes the CLI entrypoint against the importer's argv.
- `buildBudgetCard`'s note field / the top docstring now flags that `bundle_kb` measured against a
  dev server (unbundled/unminified/HMR-served) isn't comparable to a production build's budget —
  a documentation caveat, not a computation change.

## 2026-07-02 — levers 5+6: task-weighted severity + audit ledger/diff
- `scripts/audit-diff.py` (new, stdlib-only, selftest-locked): baseline diffing over persisted
  audit runs. Consumes ONLY the normalized ledger `findings.jsonl` (one JSON object per gate
  finding: `{checker, gate, id, screen?, detail?}`; checker output formats vary, so the differ
  never re-runs or re-parses checker reports), keys findings by (checker, gate, id) — duplicates
  dedupe — and buckets NEW (in current, not baseline → regressions, exit 1: the CI gate) ·
  RESOLVED (baseline only) · STILL_FAILING (both). When both dirs carry a readable
  `inventory.json`, screens/modules added/removed are reported (informational, never gates);
  an absent inventory is a stated omission. First runs diff against an empty baseline with
  `--first-run` (everything NEW, gate off, exit 0 — a baseline is established, not regressed
  against); a missing baseline ledger without it is a clean exit-2 error, as is any malformed
  ledger line (line number named). `--json` for machine consumption. Selftest over embedded
  tempdir fixtures: 3-finding baseline vs 1-new/1-resolved/2-still current (buckets + exit 1),
  no-NEW exit 0, first-run, malformed lines, dedupe, inventory delta.
- `SKILL.md` lever 5 — task-weighted severity: optional `tasks.json`
  (`[{id, task, criticality: 1|2|3, flows: [], screens: []}]`; 3 = the product's reason to exist:
  money, core loop; 2 = supporting; 1 = peripheral) documented at step 1; step 6 ranks
  severity × spread × task-criticality (absent → spread-only, said in the report); the
  Cross-cutting contract line gains the criticality weight.
- `SKILL.md` lever 6 wiring: step 6 persists each run (cards, checker outputs, inventory.json,
  findings.jsonl) into a dated `audits/<date>/` dir in the target repo and diffs against the
  previous run via `scripts/audit-diff.py` — NEW findings lead the report; output contract gains
  `Delta vs baseline: <N new · M resolved · K still-failing>` (or: first run — baseline
  established).

## 2026-07-02 — measured-not-computed layer
- `scripts/inventory-scan.py` (new, stdlib-only, selftest-locked): static ASSISTED inventory of a
  web-app source tree → `inventory.json` for Step 1. Screens from hash-route literals (`'#/x'`),
  path-literal route registrations/navigations (`route('/x')` · `navigate('/x')` · `<Route path>`),
  and file-per-view conventions (`**/views|pages|routes|screens/`); shared modules from clusters
  used in ≥ 2 screen files (custom-element tags · UI-component imports · `x-*` classname families);
  per-screen verbs (event bindings by type). `--manifest` merges auditor-declared screens/flows/
  modules (flows are declared-only, never guessed) with per-entry `source: scanned|declared|
  scanned+declared`. Honesty metadata: `scanned_files` + `unmatched_route_hints[]`; a tree with no
  routes yields an honest empty inventory. Selftest over embedded fixtures (hash router ·
  component reuse · manifest merge · no-routes tree).
- `scripts/ui-probe.mjs` (new, Node ESM; playwright resolved CWD-first with exit-2 install
  guidance when absent): drives the RUNNING app and generates Step 3's verifier cards (step 3 at
  time of writing; now step 4, the invariant pass) from
  rendered truth, per screen × scheme (`prefers-color-scheme` emulated). `<screen>.<scheme>.
  surface.json` (visible text nodes; effective backgrounds alpha-composited down the ancestor
  chain; fg composited opaque so no `over`; WCAG large-text kind; deduped, capped at 80),
  `<screen>.focus.json` (measured `visible_focus` via focus/blur computed-style delta; tabindex;
  dom_order; hit targets; ring width + per-scheme outline-vs-background contrast; open modals with
  trap/restore OMITTED, never guessed), `<screen>.budget.json` (buffered LCP/CLS observers,
  transferSize bundle_kb with js/css split, inp/tbt omitted as UNMEASURED), `<screen>.i18n.json`
  (rendered `lang`/`dir` presence; hardcoded strings left to static review), plus
  `probe-manifest.json` (probed/skipped + reasons). Selftest: ephemeral node:http fixture with
  planted defects, probed headless, cards asserted AND piped through the real color-verify/
  focus-verify checkers (CONTRAST_FAIL_AA · TARGET_TOO_SMALL · NO_VISIBLE_FOCUS ·
  POSITIVE_TABINDEX must fire); `--no-browser` runs the pure-function unit checks only; no
  playwright ⇒ SKIP + guidance, exit 2 — never a fake pass.
- `SKILL.md`: Step 1 wires the scan (assisted, not gospel — confirm module identities before
  grading); Step 3 wires the probe (step 3 at time of writing; now step 4, the invariant pass —
  probed cards supersede hand-built ones; what the probe can't
  reach stays hand-built and reported as computed-not-measured).
