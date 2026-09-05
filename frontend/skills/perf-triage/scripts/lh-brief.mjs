#!/usr/bin/env node
/**
 * lh-brief.mjs, the perf-triage brief writer. Node 24, ESM, node built-ins only.
 *
 * Turns one or more Lighthouse JSON reports into a prioritised, size-bounded markdown brief an
 * agent can act on: a header (url, preset, version, fetch time, category scores, the six core
 * metrics), a DO NOT BREAK list (every passing audit id plus each metric with a tolerance), the
 * failing audits sorted by (score asc, wastedMs desc, wastedBytes desc) with a cause-family tag
 * from a fixed taxonomy, a fix order grouped by family, and a line cap with a truncation note.
 *
 *   node lh-brief.mjs <report.json...> [--out perf-brief.md] [--max-lines 400] [--items 5]
 *   node lh-brief.mjs --slim <out-dir> <report.json...>   (write trimmed fixtures, no brief)
 *   node lh-brief.mjs selftest
 *
 * Exit: 0 brief written, 2 usage error or a file that is not a Lighthouse report (no audits/categories).
 *
 * The cause-family taxonomy is FIXED (perf-triage SKILL.md): transport, build, css-loading,
 * runtime, images-fonts, a11y-name, a11y-structure, a11y-contrast, seo-meta, third-party, with
 * `content` as the catch-all for audits no family claims. lh-diff.mjs and lh-scoreboard.mjs
 * import the taxonomy and the metric tolerances from here so the three scripts never drift.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const METRICS = [
  ['first-contentful-paint', 'FCP', 'fcp_ms'],
  ['largest-contentful-paint', 'LCP', 'lcp_ms'],
  ['total-blocking-time', 'TBT', 'tbt_ms'],
  ['cumulative-layout-shift', 'CLS', 'cls'],
  ['speed-index', 'SI', 'si_ms'],
  ['interactive', 'TTI', 'tti_ms'],
];

// Tolerance per metric: ms metrics allow max(10%, 100ms) drift; CLS allows +0.01 absolute.
export function tolerance(key, value) {
  if (key === 'cls') return 0.01;
  return Math.max(100, Math.round((value || 0) * 0.1));
}

export const FAMILY_ORDER = ['transport', 'build', 'css-loading', 'runtime', 'images-fonts',
  'third-party', 'a11y-name', 'a11y-structure', 'a11y-contrast', 'seo-meta', 'content'];

const EXACT = {
  'cache-insight': 'transport', 'uses-long-cache-ttl': 'transport', 'uses-text-compression': 'transport',
  'redirects': 'transport', 'redirects-http': 'transport', 'server-response-time': 'transport',
  'uses-http2': 'transport', 'modern-http-insight': 'transport', 'network-server-latency': 'transport',
  'uses-rel-preconnect': 'transport', 'document-latency-insight': 'transport',
  'network-dependency-tree-insight': 'transport', 'critical-request-chains': 'transport',
  'unminified-javascript': 'build', 'unminified-css': 'build', 'unused-javascript': 'build',
  'valid-source-maps': 'build', 'legacy-javascript': 'build', 'legacy-javascript-insight': 'build',
  'duplicated-javascript': 'build', 'duplicated-javascript-insight': 'build', 'total-byte-weight': 'build',
  'render-blocking-insight': 'css-loading', 'render-blocking-resources': 'css-loading',
  'unused-css-rules': 'css-loading', 'uses-rel-preload': 'css-loading',
  'mainthread-work-breakdown': 'runtime', 'bootup-time': 'runtime', 'forced-reflow-insight': 'runtime',
  'long-tasks': 'runtime', 'dom-size': 'runtime', 'dom-size-insight': 'runtime',
  'errors-in-console': 'runtime', 'uses-passive-event-listeners': 'runtime',
  'no-unload-listeners': 'runtime', 'user-timings': 'runtime', 'viewport-insight': 'runtime',
  'layout-shifts': 'images-fonts', 'cls-culprits-insight': 'images-fonts',
  'non-composited-animations': 'images-fonts', 'unsized-images': 'images-fonts',
  'color-contrast': 'a11y-contrast',
  'label': 'a11y-name', 'button-name': 'a11y-name', 'link-name': 'a11y-name', 'image-alt': 'a11y-name',
  'input-image-alt': 'a11y-name', 'frame-title': 'a11y-name', 'object-alt': 'a11y-name',
  'select-name': 'a11y-name', 'video-caption': 'a11y-name', 'form-field-multiple-labels': 'a11y-name',
  'input-button-name': 'a11y-name', 'label-content-name-mismatch': 'a11y-name',
  'document-title': 'seo-meta', 'meta-description': 'seo-meta', 'robots-txt': 'seo-meta',
  'canonical': 'seo-meta', 'hreflang': 'seo-meta', 'link-text': 'seo-meta', 'crawlable-anchors': 'seo-meta',
  'is-crawlable': 'seo-meta', 'http-status-code': 'seo-meta', 'structured-data': 'seo-meta',
  'third-party-summary': 'third-party', 'third-party-facades': 'third-party', 'third-parties-insight': 'third-party',
  'third-party-cookies': 'third-party',
};
const PATTERNS = [
  [/^aria-.*-name$/, 'a11y-name'],
  [/^aria-/, 'a11y-structure'],
  [/^(landmark|list|dlitem|definition-list|heading-order|html-has-lang|html-lang-valid|valid-lang|duplicate-id|tabindex|accesskeys|bypass|skip-link|table|td-|th-|meta-viewport|target-size|focus|managed-focus|interactive-element|logical-tab|offscreen-content|use-landmarks|visual-order|custom-controls|empty-heading|identical-links|meta-refresh|nested-interactive|scrollable-region)/, 'a11y-structure'],
  [/(image|font|lcp|webp|responsive-images|offscreen-images|efficient-animated)/, 'images-fonts'],
  [/^third-part/, 'third-party'],
];
export function familyOf(id) {
  if (EXACT[id]) return EXACT[id];
  for (const [re, fam] of PATTERNS) if (re.test(id)) return fam;
  return 'content';
}

const SKIP_MODES = new Set(['informative', 'manual', 'notApplicable']);
export const PASS_SCORE = 0.9;

const METRIC_LIKE = new Set([...METRICS.map((m) => m[0]), 'max-potential-fid', 'first-meaningful-paint']);
function metricIds(report) {
  const refs = report.categories?.performance?.auditRefs || [];
  return new Set([...METRIC_LIKE, ...refs.filter((r) => r.group === 'metrics').map((r) => r.id)]);
}

export function isScored(audit) {
  return audit && audit.score !== null && audit.score !== undefined && !SKIP_MODES.has(audit.scoreDisplayMode);
}

/** Structured analysis of one report: header, metrics, passing/failing audits, families. */
export function analyze(report) {
  const audits = report.audits || {};
  const metrics = new Set(metricIds(report));
  const header = {
    url: report.finalDisplayedUrl || report.finalUrl || report.requestedUrl || '',
    preset: report.configSettings?.formFactor || 'unknown',
    throttling: report.configSettings?.throttlingMethod || 'unknown',
    lighthouseVersion: report.lighthouseVersion || 'unknown',
    fetchTime: report.fetchTime || 'unknown',
    scores: Object.fromEntries(Object.entries(report.categories || {}).map(([k, v]) => [k, v.score == null ? null : Math.round(v.score * 100)])),
  };
  const metricRows = METRICS.map(([id, label, key]) => {
    const a = audits[id];
    return { id, label, key, value: a?.numericValue ?? null, displayValue: a?.displayValue || 'n/a', score: a?.score ?? null };
  });
  const passing = [];
  const failing = [];
  for (const [id, a] of Object.entries(audits)) {
    if (!isScored(a) || metrics.has(id)) continue;
    if (a.score >= PASS_SCORE) { passing.push(id); continue; }
    const items = detailItems(a);
    failing.push({
      id,
      score: a.score,
      displayValue: a.displayValue || '',
      wastedMs: a.metricSavings ? Math.max(0, ...Object.values(a.metricSavings).map((n) => Number(n) || 0)) : (sumOf(items, 'wastedMs') || 0),
      wastedBytes: sumOf(items, 'wastedBytes'),
      itemCount: a.details?.itemCount ?? items.length,
      items,
      family: familyOf(id),
    });
  }
  failing.sort((x, y) => (x.score - y.score) || (y.wastedMs - x.wastedMs) || (y.wastedBytes - x.wastedBytes) || x.id.localeCompare(y.id));
  passing.sort();
  const diag = audits.diagnostics?.details?.items?.[0] || {};
  const transport = transportSignals(audits);
  return { header, metrics: metricRows, passing, failing, diag, transport, families: familyGroups(failing) };
}

function sumOf(items, key) {
  let n = 0;
  for (const it of items) if (typeof it[key] === 'number') n += it[key];
  return n;
}

/** Flattens list-of-table details (forced-reflow-insight) into one item list. */
export function detailItems(audit) {
  const items = audit?.details?.items;
  if (!Array.isArray(items)) return [];
  const out = [];
  for (const it of items) {
    if (it && it.type === 'table' && Array.isArray(it.items)) out.push(...it.items);
    else if (it && Array.isArray(it.items) && !it.url && !it.node) out.push(...it.items);
    else out.push(it);
  }
  return out;
}

/** Derived transport facts the audit ids alone do not state: uncached vs uncompressed text assets. */
export function transportSignals(audits) {
  // Only http(s) requests count: a chrome-extension:// or data: entry from the audit profile is
  // not the page's transport (lh-run.mjs passes --disable-extensions; a DevTools run may not).
  const isHttp = (r) => typeof r?.url === 'string' && /^https?:\/\//.test(r.url);
  const reqs = detailItems(audits['network-requests']).filter(isHttp);
  const text = reqs.filter((r) => /script|stylesheet|document|font|xhr|fetch/i.test(r.resourceType || '') && (r.resourceSize || 0) > 1024);
  const uncompressed = text.filter((r) => (r.transferSize || 0) >= (r.resourceSize || 0));
  const cache = detailItems(audits['cache-insight']).filter(isHttp);
  const uncached = cache.filter((c) => !c.cacheLifetimeMs);
  return {
    requests: reqs.length,
    textAssets: text.length,
    uncompressed: uncompressed.length,
    uncached: audits['cache-insight']?.details?.itemCount ?? uncached.length,
  };
}

function familyGroups(failing) {
  const groups = {};
  for (const f of failing) (groups[f.family] ||= []).push(f.id);
  return FAMILY_ORDER.filter((f) => groups[f]).map((f) => ({ family: f, audits: groups[f] }));
}

export function stripOrigin(url, origin) {
  if (!url) return '';
  if (origin && url.startsWith(origin)) return url.slice(origin.length) || '/';
  return url;
}

/** One trimmed line per item: url or selector or snippet or source location, plus the numbers. */
export function itemLine(it, origin) {
  if (!it || typeof it !== 'object') return String(it ?? '');
  const parts = [];
  if (it.type === 'node') it = { node: it };
  if (it.value && it.value.type === 'network-tree') {
    const chains = it.value.chains || {};
    const roots = Object.keys(chains).length;
    let depth = 0;
    const walk = (n, d) => { depth = Math.max(depth, d); for (const c of Object.values(n.children || {})) walk(c, d + 1); };
    for (const c of Object.values(chains)) walk(c, 1);
    return `network-tree: ${roots} root chain(s), longest depth ${depth}, longest chain ${Math.round(it.value.longestChain?.duration || 0)} ms`;
  }
  if (it.source && it.source.url) parts.push(`${stripOrigin(it.source.url, origin)}:${it.source.line ?? 0}:${it.source.column ?? 0}`);
  else if (it.sourceLocation && it.sourceLocation.url) parts.push(`${stripOrigin(it.sourceLocation.url, origin)}:${it.sourceLocation.line ?? 0}`);
  else if (typeof it.url === 'string') parts.push(stripOrigin(it.url, origin));
  else if (it.scriptUrl) parts.push(stripOrigin(it.scriptUrl, origin));
  if (it.node) {
    if (it.node.selector) parts.push(`sel: ${it.node.selector.slice(0, 120)}`);
    if (it.node.snippet) parts.push(`snip: ${it.node.snippet.replace(/\s+/g, ' ').slice(0, 100)}`);
    if (it.node.explanation) parts.push(it.node.explanation.replace(/\s+/g, ' ').replace(/^Fix any of the following:\s*/i, '').slice(0, 120));
  }
  if (it.groupLabel) parts.push(it.groupLabel);
  if (it.label && !it.groupLabel) parts.push(it.label);
  else if (it.subpart || it.phase) parts.push(it.subpart || it.phase);
  if (it.description && !it.node) parts.push(String(it.description).replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/\s+/g, ' ').slice(0, 120));
  const nums = [];
  if (typeof it.wastedMs === 'number') nums.push(`${Math.round(it.wastedMs)} ms wasted`);
  if (typeof it.reflowTime === 'number') nums.push(`${Math.round(it.reflowTime)} ms reflow`);
  if (typeof it.duration === 'number') nums.push(`${Math.round(it.duration)} ms`);
  if (typeof it.wastedBytes === 'number') nums.push(`${Math.round(it.wastedBytes / 1024)} KiB wasted`);
  if (typeof it.totalBytes === 'number' && typeof it.wastedBytes !== 'number') nums.push(`${Math.round(it.totalBytes / 1024)} KiB`);
  if (typeof it.cacheLifetimeMs === 'number') nums.push(`ttl ${it.cacheLifetimeMs}`);
  if (nums.length) parts.push(nums.join(', '));
  const line = parts.join(' | ');
  return line || JSON.stringify(it).slice(0, 140);
}

function fmtMetric(row) {
  if (row.value == null) return 'n/a';
  return row.key === 'cls' ? row.value.toFixed(3) : `${Math.round(row.value)} ms`;
}

/** Renders one report's brief as an array of lines; caps to maxLines with a truncation note. */
export function renderBrief(analysis, { maxLines = 400, items = 5 } = {}) {
  const { header, metrics, passing, failing, diag, transport, families } = analysis;
  let origin = '';
  try { origin = new URL(header.url).origin; } catch { origin = ''; }
  const L = [];
  L.push(`# Perf brief: ${header.url}`);
  L.push('');
  L.push(`- preset: ${header.preset} (throttling ${header.throttling}) | lighthouse ${header.lighthouseVersion} | fetched ${header.fetchTime}`);
  L.push(`- scores: ${Object.entries(header.scores).map(([k, v]) => `${k} ${v ?? 'n/a'}`).join(' | ')}`);
  L.push(`- metrics: ${metrics.map((m) => `${m.label} ${m.displayValue}`).join(' | ')}`);
  if (diag.numRequests != null) L.push(`- diagnostics: ${diag.numRequests} requests, ${diag.numScripts} scripts, ${diag.numStylesheets} stylesheets, ${Math.round((diag.totalByteWeight || 0) / 1024)} KiB, main thread ${Math.round(diag.totalTaskTime || 0)} ms`);
  L.push(`- transport signals: ${transport.uncached} uncached responses (cache-insight), ${transport.uncompressed} of ${transport.textAssets} text assets over 1 KiB served uncompressed`);
  L.push('');
  L.push('## DO NOT BREAK');
  L.push('');
  L.push('Every metric below holds within its tolerance and every listed audit stays passing. A fix that moves one of these is reverted, the list is never edited.');
  L.push('');
  for (const m of metrics) {
    if (m.value == null) continue;
    const tol = tolerance(m.key, m.value);
    L.push(`- ${m.label} (${m.id}): ${fmtMetric(m)}, tolerance +${m.key === 'cls' ? tol.toFixed(2) : `${tol} ms`}`);
  }
  L.push(`- passing audits (${passing.length}): ${passing.join(', ')}`);
  L.push('');
  L.push(`## Failing audits (${failing.length}, priority order)`);
  L.push('');
  const failStart = L.length;
  for (const f of failing) {
    const bits = [`score ${Math.round(f.score * 100)}`];
    if (f.displayValue) bits.push(f.displayValue);
    if (f.itemCount) bits.push(`${f.itemCount} items`);
    L.push(`### ${f.id} [${f.family}] (${bits.join(', ')})`);
    for (const it of f.items.slice(0, items)) L.push(`- ${itemLine(it, origin)}`);
    if (f.itemCount > items) L.push(`- (${f.itemCount - items} more items in the report)`);
    L.push('');
  }
  L.push('## Fix order (largest blast radius first)');
  L.push('');
  families.forEach((g, i) => L.push(`${i + 1}. ${g.family}: ${g.audits.join(', ')}`));
  L.push('');
  L.push('A finding without a file, selector or source location is a research task, not a fix. Confirm each family against the codebase before editing.');
  if (L.length <= maxLines) return L;
  // Truncate the failing-audit section, keep the fix order intact.
  const tail = L.slice(L.length - (families.length + 4));
  const budget = maxLines - tail.length - 2;
  const kept = L.slice(0, Math.max(failStart, budget));
  const shown = new Set();
  for (const line of kept) { const m = /^### ([a-z0-9-]+)/.exec(line); if (m) shown.add(m[1]); }
  const omitted = failing.map((f) => f.id).filter((id) => !shown.has(id));
  kept.push(`> truncated at ${maxLines} lines: ${omitted.length} failing audit(s) omitted (${omitted.join(', ')}); rerun with --max-lines or --items to see them`);
  kept.push('');
  return kept.concat(tail);
}

export function readReport(file) {
  const r = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!r.audits || !r.categories) throw new Error(`${file}: not a Lighthouse report (no audits/categories)`);
  return r;
}

/** Trims a full report to a small fixture: audit scores, trimmed items, no screenshots/traces. */
export function slim(report, { items = 8, networkItems = 60 } = {}) {
  const trimItem = (it) => {
    if (!it || typeof it !== 'object') return it;
    if (it.type === 'table' && Array.isArray(it.items)) return { type: 'table', items: it.items.slice(0, items).map(trimItem) };
    const keep = {};
    for (const k of ['url', 'scriptUrl', 'sourceMapUrl', 'wastedBytes', 'wastedMs', 'totalBytes', 'cacheLifetimeMs', 'reflowTime', 'groupLabel', 'duration', 'transferSize', 'resourceSize', 'resourceType', 'mimeType', 'source', 'sourceLocation', 'description', 'subpart', 'phase', 'label']) if (it[k] !== undefined) keep[k] = it[k];
    if (it.node) keep.node = { selector: it.node.selector, snippet: it.node.snippet, explanation: it.node.explanation, nodeLabel: it.node.nodeLabel };
    return keep;
  };
  const audits = {};
  for (const [id, a] of Object.entries(report.audits || {})) {
    const out = { id, title: a.title, score: a.score, scoreDisplayMode: a.scoreDisplayMode };
    for (const k of ['displayValue', 'numericValue', 'numericUnit', 'metricSavings']) if (a[k] !== undefined) out[k] = a[k];
    if (a.details && Array.isArray(a.details.items)) {
      const cap = id === 'network-requests' ? networkItems : items;
      const keepWhole = id === 'diagnostics';
      out.details = { type: a.details.type, itemCount: a.details.itemCount ?? a.details.items.length, items: a.details.items.slice(0, cap).map((it) => (keepWhole ? it : trimItem(it))) };
    }
    audits[id] = out;
  }
  const categories = {};
  for (const [k, v] of Object.entries(report.categories || {})) categories[k] = { score: v.score, auditRefs: (v.auditRefs || []).map((r) => ({ id: r.id, weight: r.weight, group: r.group })) };
  return {
    lighthouseVersion: report.lighthouseVersion, requestedUrl: report.requestedUrl, finalDisplayedUrl: report.finalDisplayedUrl,
    fetchTime: report.fetchTime, configSettings: { formFactor: report.configSettings?.formFactor, throttlingMethod: report.configSettings?.throttlingMethod },
    categories, audits, slimmed: true,
  };
}

function parseArgs(argv) {
  const opts = { files: [], out: null, maxLines: 400, items: 5, slimDir: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opts.out = argv[++i];
    else if (a === '--max-lines') opts.maxLines = Number(argv[++i]);
    else if (a === '--items') opts.items = Number(argv[++i]);
    else if (a === '--slim') opts.slimDir = argv[++i];
    else if (a.startsWith('--')) throw new Error(`unknown flag ${a}`);
    else opts.files.push(a);
  }
  return opts;
}

export const FIXTURE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'assets', 'fixtures');
export const FIXTURES = ['chat.desktop.slim.json', 'admin-dashboard.desktop.slim.json'].map((f) => path.join(FIXTURE_DIR, f));

function assert(cond, msg) { if (!cond) throw new Error(`selftest: ${msg}`); }

function selftest() {
  const [chat, admin] = FIXTURES.map(readReport);
  const A = analyze(chat);
  const B = analyze(admin);
  assert(A.header.scores.performance === 78, `chat performance score 78, got ${A.header.scores.performance}`);
  assert(A.metrics.length === 6 && A.metrics.every((m) => m.value != null), 'six metrics with values');
  const famA = Object.fromEntries(A.failing.map((f) => [f.id, f.family]));
  const famB = Object.fromEntries(B.failing.map((f) => [f.id, f.family]));
  // The cause families the two 2026-09-05 prod reports must reproduce (spec finding list).
  assert(famA['cache-insight'] === 'transport', 'cache-insight is transport');
  assert(famA['unminified-javascript'] === 'build', 'unminified-javascript is build');
  assert(famA['valid-source-maps'] === 'build', 'valid-source-maps is build');
  assert(famA['forced-reflow-insight'] === 'runtime', 'forced-reflow is runtime');
  assert(famA['render-blocking-insight'] === 'css-loading', 'render-blocking is css-loading');
  assert(famA['aria-input-field-name'] === 'a11y-name', 'aria-input-field-name is a11y-name');
  assert(famA['color-contrast'] === 'a11y-contrast', 'color-contrast is a11y-contrast');
  assert(famA['meta-description'] === 'seo-meta', 'meta-description is seo-meta');
  assert(famB['aria-allowed-attr'] === 'a11y-structure', 'aria-allowed-attr is a11y-structure');
  assert(famB['aria-required-children'] === 'a11y-structure', 'aria-required-children is a11y-structure');
  assert(famB['valid-lang'] === 'a11y-structure', 'valid-lang is a11y-structure');
  assert(famB['aria-command-name'] === 'a11y-name', 'aria-command-name is a11y-name');
  assert(A.failing.find((f) => f.id === 'cache-insight').itemCount === 1055, 'cache-insight keeps its 1055 item count');
  assert(A.failing.find((f) => f.id === 'render-blocking-insight').itemCount === 221, 'render-blocking keeps 221 items');
  assert(A.transport.uncached === 1055, 'uncached count from cache-insight');
  assert(!A.failing.some((f) => f.id === 'speed-index'), 'metric audits are excluded from the failing list');
  assert(A.passing.includes('aria-allowed-attr'), 'chat passes aria-allowed-attr (DO NOT BREAK)');
  // Priority order: score asc, then wastedMs desc.
  const zeros = A.failing.filter((f) => f.score === 0);
  for (let i = 1; i < zeros.length; i++) assert(zeros[i - 1].wastedMs >= zeros[i].wastedMs, 'score-0 audits sorted by wastedMs desc');
  assert(A.failing[0].id === 'cache-insight', `top fix on chat is cache-insight, got ${A.failing[0].id}`);
  assert(A.families[0].family === 'transport' && A.families[1].family === 'build', 'fix order leads transport then build');
  // Item lines carry a file, selector or source location, never a JSON blob.
  const reflow = A.failing.find((f) => f.id === 'forced-reflow-insight');
  const line = itemLine(reflow.items[0], 'https://ui-kit.exe.xyz');
  assert(/everything\.min\.js:\d+:\d+/.test(line), `reflow item names url:line:col, got ${line}`);
  const sel = itemLine(A.failing.find((f) => f.id === 'aria-input-field-name').items[0]);
  assert(sel.includes('select-ui#workspace-select'), `a11y item carries the selector, got ${sel}`);
  // Size cap: the cap bites and names what it dropped; uncapped fits.
  const full = renderBrief(A, { maxLines: 100000 });
  const capped = renderBrief(A, { maxLines: 60 });
  assert(capped.length <= 60, `capped brief is at most 60 lines, got ${capped.length}`);
  assert(capped.some((l) => l.startsWith('> truncated at 60')), 'truncation note present');
  assert(capped.some((l) => l.startsWith('## Fix order')), 'fix order survives truncation');
  assert(full.some((l) => l.startsWith('## DO NOT BREAK')), 'DO NOT BREAK section present');
  assert(full.some((l) => l.includes('tolerance +')), 'metric tolerances rendered');
  // Taxonomy: every failing audit lands in a listed family.
  for (const f of [...A.failing, ...B.failing]) assert(FAMILY_ORDER.includes(f.family), `${f.id} family ${f.family} is in the taxonomy`);
  assert(tolerance('cls', 0.02) === 0.01 && tolerance('lcp_ms', 2400) === 240 && tolerance('tbt_ms', 90) === 100, 'tolerance rule');
  // Negative control: a JSON file that is not a Lighthouse report is rejected (exit 2), and a
  // report whose network-requests carry extension entries counts only http(s) transport.
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lh-brief-selftest-'));
  const bogus = path.join(tmp, 'bogus.json');
  fs.writeFileSync(bogus, JSON.stringify({ hello: 1 }));
  const silent = { error() {}, log() {} };
  assert(main([bogus], silent) === 2, 'a non-Lighthouse JSON exits 2');
  assert(main([path.join(tmp, 'missing.json')], silent) === 2, 'a missing file exits 2');
  assert(main([], silent) === 2, 'no input is a usage error');
  fs.rmSync(tmp, { recursive: true, force: true });
  const ext = JSON.parse(JSON.stringify(chat));
  ext.audits['network-requests'].details.items.push({ url: 'chrome-extension://abc/content.js', resourceType: 'Script', transferSize: 50000, resourceSize: 50000 });
  ext.audits['cache-insight'].details.items.push({ url: 'chrome-extension://abc/content.js', cacheLifetimeMs: 0 });
  ext.audits['cache-insight'].details.itemCount = undefined;
  const extSignals = transportSignals(ext.audits);
  assert(extSignals.uncompressed === A.transport.uncompressed && extSignals.requests === A.transport.requests, 'chrome-extension:// entries are ignored in transport signals');
  assert(extSignals.uncached === detailItems(chat.audits['cache-insight']).filter((c) => !c.cacheLifetimeMs).length, 'extension entries do not count as uncached');
  // slim() keeps counts and the fields the brief relies on.
  const s = slim(chat, { items: 2 });
  assert(s.audits['cache-insight'].details.itemCount === 1055 && s.audits['cache-insight'].details.items.length === 2, 'slim keeps itemCount');
  console.log(`selftest ok: ${A.failing.length} failing / ${A.passing.length} passing on chat; ${B.failing.length} failing / ${B.passing.length} passing on admin-dashboard; families ${A.families.map((g) => g.family).join(',')}`);
}

export function main(argv, log = console) {
  if (argv[0] === 'selftest') { selftest(); return 0; }
  let opts;
  try { opts = parseArgs(argv); } catch (e) { log.error(e.message); return 2; }
  if (!opts.files.length) {
    log.error('usage: lh-brief.mjs <report.json...> [--out perf-brief.md] [--max-lines 400] [--items 5] | --slim <out-dir> <report.json...> | selftest');
    return 2;
  }
  const out = [];
  for (const f of opts.files) {
    let r;
    try { r = readReport(f); } catch (e) { log.error(`${f}: ${e.message}`); return 2; }
    if (opts.slimDir) {
      fs.mkdirSync(opts.slimDir, { recursive: true });
      const target = path.join(opts.slimDir, path.basename(f).replace(/\.json$/, '') + '.slim.json');
      fs.writeFileSync(target, JSON.stringify(slim(r), null, 1));
      log.log(`slim: ${target}`);
      continue;
    }
    out.push(...renderBrief(analyze(r), { maxLines: opts.maxLines, items: opts.items }), '');
  }
  if (opts.slimDir) return 0;
  const text = out.join('\n');
  if (opts.out) { fs.writeFileSync(opts.out, text); log.log(`brief: ${opts.out} (${out.length} lines)`); }
  else process.stdout.write(text);
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
