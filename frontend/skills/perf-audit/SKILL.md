---
name: perf-audit
description: >-
  Run a Lighthouse audit reproducibly and save the JSON. Use when the user asks to "run
  Lighthouse", "get a Lighthouse report for this URL", "measure the performance score of the
  deployed site", "audit desktop and mobile", or needs a saved before-report for a fix loop:
  pinned `npx lighthouse@13`, deployed URL over localhost, 3 runs with the median kept, one JSON
  per preset. NOT for reading the report or deciding what to fix first (perf-triage); NOT for
  perceived-latency judgment, skeleton vs spinner, CLS budgets (check-speed).
disable-model-invocation: false
user-invocable: true
---

# perf-audit, reproducible Lighthouse runs

One job: produce a Lighthouse JSON that a later run can be compared against. Every other
perf-* skill consumes this file; a run that cannot be repeated cannot be diffed.

## Procedure

1. **Pick the URL.** Prefer the deployed origin over localhost. A dev server serves unminified,
   uncached, uncompressed assets and hides the CDN and TLS costs, so its numbers describe a
   different product. Our own evidence: the site deploy pre-flight against a keyless static
   serve reports different scores from prod (gen-ui-kit, 2026-09-05). When only localhost
   exists, say so in the report name and the brief.
2. **Run.** `node scripts/lh-run.mjs <url> [--preset desktop|mobile|both] [--runs 3] [--out dir]`.
   The script pins `npx lighthouse@13`, passes `--chrome-flags="--headless=new --disable-extensions"` (a profile extension's
   `chrome-extension://` requests would otherwise skew request counts), runs each
   preset 3 times, keeps the run with the median performance score, and writes
   `<out>/<slug>.<preset>.json` plus `<slug>.<preset>.runs.json` (every run's category scores,
   so a noisy run stays visible). Desktop is `--preset=desktop`; mobile is Lighthouse's default.
   Verified 2026-09-05 on ui-kit.exe.xyz with the host's Playwright Chromium, this single
   command only; the 3-run median and the extension flag are proven by the selftest, not by a
   prod run:

   ```
   npx lighthouse@13 <url> --output=json --output-path=out.json --quiet --chrome-flags="--headless=new" --preset=desktop
   ```

3. **Keep the file.** Commit or attach the JSON under a name that carries url, preset and date.
   The report is the evidence for every later claim; a fix loop without the before-report has
   nothing to diff against (thread 1s6fmjn's commenter: "I really wish I had saved the report
   out").
4. **Hand off.** `perf-triage` turns the JSON into a brief; `perf-loop` diffs a later run
   against it.

## Fallback without the CLI

Chrome DevTools > Lighthouse tab > run the audit > click the download arrow and save as JSON
(thread 1rehfjf, the commenter's own steps). Same file shape; note the Lighthouse version the
DevTools build carries, since it may not be 13.

## Optional tooling, with caveats (not the procedure)

- Chrome DevTools MCP inside Claude Code (thread 1rn63fb): lets the model drive Lighthouse
  from the browser session. The thread names no package, version, or configuration, and a
  later commenter's rerun of the same site reportedly scored 32/76/81/100 (unverified: no
  report image in thread), so treat it as a convenience, not a source of record. This skill adds no MCP dependency.
- uimax-mcp (thread 1s6fmjn): `claude mcp add uimax -- npx -y uimax-mcp@latest` bundles
  Puppeteer, Lighthouse and axe-core. Unpinned `@latest`, and the thread's own tool count
  disagrees with itself (12 tools in the post, 7 of 35 in a later comment). Pin before relying
  on it; the saved JSON from step 2 stays the record.

## Done

A JSON per preset exists under a dated name, the runs sidecar shows the three scores, and the
brief step can start. NOT done: a screenshot of the scores, a localhost run labeled as prod, or
a single unsaved DevTools run.

## Provenance

- 1rehfjf (r/nextjs, "Downloading lighthouse report as json and dumping into coding agents is
  underrated"): the DevTools download path ("Open Chrome DevTools > go to Lighthouse tab > run an
  audit", "click the download arrow icon to save as JSON") and the CLI alternative
  (`npx lighthouse https://yoursite.com --output=json --output-path=report.json`). The deployed
  URL preference: "I usually run it on the deployed URL not localhost." The claim "Localhost
  perf numbers are basically fiction" is a commenter assertion with no comparison posted; our
  own pre-flight-vs-prod difference is the evidence this skill leans on.
- 1rn63fb (r/ClaudeAI): the Chrome DevTools MCP loop ("I told it to run Lighthouse", "read the
  scores", "fix whatever was dragging them down", "keep going until the numbers were green").
  Unverified in thread: the MCP package and version, the starting scores, the third-party
  explanation for the remaining gap.
- 1s6fmjn (r/ClaudeCode): the uimax-mcp install line. Unverified: "109 code findings", "32
  keyboard accessibility issues", the C to A accessibility grade, the tool count.
- Pinned version, the 3-run median, and `--disable-extensions` are this repo's additions, not
  thread procedures. Only the single pinned command was verified on prod 2026-09-05; the median
  selection is proven by the selftest with a fake runner.
