---
name: perf-triage
description: >-
  Turn one or more Lighthouse JSON reports into a prioritised, size-bounded brief the agent can
  act on. Use when the user asks "what do I fix first", "read this Lighthouse report", "turn
  the report into a plan", "which audits matter", or hands over a report.json: header, a DO NOT
  BREAK list, failing audits ranked with a cause-family tag (transport, build, css-loading,
  runtime, images-fonts, a11y-name, a11y-structure, a11y-contrast, seo-meta, third-party), a fix
  order. NOT for running Lighthouse (perf-audit); NOT for applying fixes and re-auditing
  (perf-loop); NOT for a perceived-latency budget card (check-speed).
disable-model-invocation: false
user-invocable: true
---

# perf-triage, from report to brief

A raw Lighthouse JSON is 2 MB, half of it timing data (thread 1rehfjf: "the full JSON is
enormous and like half of it is timing data that doesnt help"). The brief keeps the
diagnostics and opportunities, ranks them, tags each with the cause family it belongs to, and
states what must not change. The brief is what a fix loop reads; the JSON stays as evidence.

## Procedure

1. **Brief.** `node scripts/lh-brief.mjs <report.json...> [--out perf-brief.md] [--max-lines 400] [--items 5]`.
   Per report it emits:
   - header: url, preset, Lighthouse version, fetch time, category scores, the six core
     metrics (FCP, LCP, TBT, CLS, SI, TTI), request/byte diagnostics, and two derived transport
     signals (uncached responses from `cache-insight`, uncompressed text assets from
     `network-requests`);
   - **DO NOT BREAK**: every passing audit id and each metric's current value with a tolerance
     (ms metrics: the larger of 10% and 100 ms; CLS: +0.01). The list is the regression guard
     thread 1tewaoi added after "Claude regressed passing audits when fixing failing ones";
   - failing audits sorted by score ascending, then wasted ms descending, then wasted bytes
     descending, each with audit id, displayValue, item count, the top 5 items (url, selector,
     snippet or `file:line:col`, trimmed) and a `[family]` tag;
   - **Fix order** grouped by family, largest blast radius first: transport, build,
     css-loading, runtime, images-fonts, third-party, a11y-name, a11y-structure, a11y-contrast,
     seo-meta, content;
   - a line cap (default 400) so the brief fits a context window; what got cut is named in a
     `> truncated` note, never silently dropped.
2. **Confirm each family against the codebase before touching anything.** Thread 1rehfjf's
   failure mode was an agent that "keeps tracking the wrong leads" and tried "to debug the
   build file": the report names `dist/everything.min.js:229:7447`, the fix lives in the
   source that produced it. For every family in the fix order, find the owning file or config
   (server headers for transport, the bundler config for build, the stylesheet loading path for
   css-loading, the component source for runtime and a11y) and write it next to the finding.
3. **Demand evidence per finding.** A finding without a file, selector, source location, or a
   reproducible step is a research task, not a fix (thread 1taw297's commenter: "for each real
   finding, require a failing test, repro step, or screenshot before fixing"). Label it
   `research` in the brief and move on; do not invent a fix for it.
4. **Hand off** the brief plus the report to `perf-loop` (one family per iteration) or, for
   a multi-page campaign, to `perf-playbook`.

## The taxonomy (fixed)

| Family | Audits it claims | Typical owner |
|---|---|---|
| transport | cache-insight, uses-long-cache-ttl, uses-text-compression, redirects, server-response-time, network-dependency-tree-insight | server or CDN headers |
| build | unminified-javascript, unminified-css, unused-javascript, valid-source-maps, legacy-javascript, duplicated-javascript | bundler config |
| css-loading | render-blocking-insight, render-blocking-resources, unused-css-rules | stylesheet loading path |
| runtime | mainthread-work-breakdown, bootup-time, forced-reflow-insight, long-tasks, dom-size, errors-in-console | component source |
| images-fonts | image and font audits, lcp-* insights, layout-shift culprits | asset pipeline, markup |
| third-party | third-party-summary, third-party-facades | tag loading |
| a11y-name | aria-*-name, label, button-name, link-name, image-alt | component markup |
| a11y-structure | other aria-*, landmark-*, valid-lang, heading-order, list | component markup |
| a11y-contrast | color-contrast | tokens |
| seo-meta | meta-description, document-title, canonical, robots-txt | page head |
| content | anything unclaimed | judgment |

The two 2026-09-05 prod reports (`assets/fixtures/`, slimmed) reproduce the findings the
taxonomy was built on: no Cache-Control (cache-insight, 1055 items) as transport; unminified
modules and a shared bundle without source maps as build; 221 render-blocking stylesheets as
css-loading; forced reflow inside `everything.min.js` as runtime; `select-ui` without an
accessible name as a11y-name; contenteditable with `aria-autocomplete`, a grid containing a
nav landmark, and a `code-ui` lang attribute failing valid-lang as a11y-structure; an 11px
label at 2.98 contrast as a11y-contrast. The selftest locks every one of those tags.

## Done

A brief under the line cap with a DO NOT BREAK list, every failing audit tagged, each family
mapped to a codebase owner, and evidence-less findings marked `research`. NOT done: the raw
JSON pasted into context, or a fix order with no codebase confirmation.

## Provenance

- 1rehfjf (r/nextjs): "Strip it down to just the diagnostics and opportunities arrays", "drop
  that JSON file into your project root", and the failure report "All my attempts doing this
  fail because it keeps tracking the wrong leads", including trying "to debug the build file"
  and "I tried enabling source maps but it just keeps chasing the wrong leads". Unverified:
  the claim that reduced JSON yields "way better suggestions" (no comparison posted).
- 1tewaoi (r/TheFounders): "Claude regressed passing audits when fixing failing ones", the
  response "added a 'DO NOT BREAK' list and stack-pack detection", and the output shape "Every
  failing audit comes with a concrete fix and the actual offending URLs/selectors/snippets."
  Unverified: the CLAUDE.md schema, the exact prompt, the usage analytics.
- 1taw297 (r/ClaudeCode), commenter only: work failing audits "in priority order" from a brief
  with "ranked offenders"; "for each real finding, require a failing test, repro step, or
  screenshot before fixing"; "a clean audit finding is acceptable. Do not invent issues simply
  to comply with your auditor role." No report or generated brief appears in the thread; the
  OP's own four-agent audit is not a Lighthouse procedure and is not adopted here.
- The taxonomy, the sort key, the tolerances, and the line cap are this repo's additions.
