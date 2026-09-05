#!/usr/bin/env node
/**
 * lh-scoreboard.mjs, the perf-sweep scoreboard and budget seeder. Node 24, ESM, node built-ins only.
 *
 *   node lh-scoreboard.mjs <reports-dir> [--routes routes.json] [--out scoreboard] [--budgets-out budgets.json]
 *   node lh-scoreboard.mjs selftest
 *
 * Reads every Lighthouse JSON in <reports-dir> (lh-run.mjs output, `*.runs.json` sidecars are
 * skipped) and writes <out>.json + <out>.md: per route the category scores, the six core
 * metrics, transfer bytes, request count, the top 3 failing audit ids and the cause families;
 * then a cluster table (family -> failing audit -> routes) so one fix is validated on every
 * route that has it. `--budgets-out` seeds preserve-not-regress budget cards from the baseline
 * (check-speed's {page, metrics, budget} shape, budget = metric + lh-brief's tolerance, plus the
 * passing audit ids) for lh-diff.mjs --budgets. `--routes routes.json` ([{route, surface,
 * canary}]) tags each row with its surface and marks the canary set.
 *
 * Exit: 0 written, 1 no readable report in the dir, 2 usage error.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { analyze, readReport, tolerance, FIXTURES, FIXTURE_DIR } from '../../perf-triage/scripts/lh-brief.mjs';

function pageOf(url) {
  try { return new URL(url).pathname || '/'; } catch { return url || '/'; }
}

/** One scoreboard row from a report. */
export function rowOf(report, file, routes = []) {
  const a = analyze(report);
  const page = pageOf(a.header.url);
  const tag = routes.find((r) => r.route === page) || {};
  const metrics = {};
  for (const m of a.metrics) if (m.value != null) metrics[m.key] = m.key === 'cls' ? Number(m.value.toFixed(4)) : Math.round(m.value);
  return {
    file: path.basename(file || ''),
    url: a.header.url,
    page,
    preset: a.header.preset,
    surface: tag.surface || 'untagged',
    canary: Boolean(tag.canary),
    scores: a.header.scores,
    metrics,
    transferBytes: a.diag.totalByteWeight ?? null,
    requests: a.diag.numRequests ?? a.transport.requests ?? null,
    topFailing: a.failing.slice(0, 3).map((f) => f.id),
    failing: a.failing.map((f) => ({ id: f.id, family: f.family, score: f.score })),
    families: a.families.map((g) => g.family),
    passing: a.passing,
  };
}

/** family -> audit -> [pages], largest cluster first. */
export function clusters(rows) {
  const map = {};
  for (const r of rows) for (const f of r.failing) ((map[f.family] ||= {})[f.id] ||= []).push(`${r.page} (${r.preset})`);
  return Object.entries(map).map(([family, audits]) => ({
    family,
    audits: Object.entries(audits).map(([id, pages]) => ({ id, pages })).sort((x, y) => y.pages.length - x.pages.length || x.id.localeCompare(y.id)),
  })).sort((x, y) => Math.max(...y.audits.map((z) => z.pages.length)) - Math.max(...x.audits.map((z) => z.pages.length)));
}

/** Budget cards seeded as preserve-not-regress from the baseline rows. */
export function seedBudgets(rows) {
  return rows.map((r) => {
    const budget = {};
    for (const [k, v] of Object.entries(r.metrics)) budget[k] = k === 'cls' ? Number((v + tolerance(k, v)).toFixed(4)) : v + tolerance(k, v);
    if (r.scores.performance != null) budget.perf_score = r.scores.performance;
    if (r.requests != null) budget.requests = r.requests;
    return { page: r.page, preset: r.preset, metrics: { ...r.metrics, requests: r.requests }, budget, passing: r.passing, seededFrom: r.file, policy: 'preserve-not-regress' };
  });
}

export function renderMarkdown(rows, cl) {
  const L = ['# Perf scoreboard', '', `${rows.length} report(s); canary set: ${rows.filter((r) => r.canary).map((r) => r.page).join(', ') || 'none tagged'}`, ''];
  L.push('| route | preset | surface | perf | a11y | bp | seo | FCP | LCP | TBT | CLS | SI | TTI | KiB | req | top failing | families |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const r of rows) {
    const s = r.scores, m = r.metrics;
    L.push(`| ${r.page}${r.canary ? ' (canary)' : ''} | ${r.preset} | ${r.surface} | ${s.performance ?? '-'} | ${s.accessibility ?? '-'} | ${s['best-practices'] ?? '-'} | ${s.seo ?? '-'} | ${m.fcp_ms ?? '-'} | ${m.lcp_ms ?? '-'} | ${m.tbt_ms ?? '-'} | ${m.cls ?? '-'} | ${m.si_ms ?? '-'} | ${m.tti_ms ?? '-'} | ${r.transferBytes == null ? '-' : Math.round(r.transferBytes / 1024)} | ${r.requests ?? '-'} | ${r.topFailing.join(', ')} | ${r.families.join(', ')} |`);
  }
  L.push('', '## Clusters (one fix, validated on every route that has it)', '');
  for (const c of cl) {
    L.push(`### ${c.family}`);
    for (const a of c.audits) L.push(`- ${a.id} (${a.pages.length}): ${a.pages.join(', ')}`);
    L.push('');
  }
  return L.join('\n');
}

export function build(dir, { routes = [], out = 'scoreboard', budgetsOut = null } = {}) {
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json') && !f.endsWith('.runs.json') && f !== 'routes.json' && f !== 'budgets.json').map((f) => path.join(dir, f)).sort();
  const rows = [];
  for (const f of files) {
    try { rows.push(rowOf(readReport(f), f, routes)); } catch (e) { console.error(`skip ${f}: ${e.message}`); }
  }
  if (!rows.length) throw new Error(`no readable Lighthouse report in ${dir}`);
  const cl = clusters(rows);
  fs.writeFileSync(`${out}.json`, JSON.stringify({ generated: new Date().toISOString(), rows, clusters: cl }, null, 2));
  fs.writeFileSync(`${out}.md`, renderMarkdown(rows, cl));
  const written = [`${out}.json`, `${out}.md`];
  if (budgetsOut) { fs.writeFileSync(budgetsOut, JSON.stringify(seedBudgets(rows), null, 2)); written.push(budgetsOut); }
  return { rows, clusters: cl, written };
}

function assert(cond, msg) { if (!cond) throw new Error(`selftest: ${msg}`); }

function selftest() {
  const routes = [{ route: '/site/playground/chat', surface: 'playground', canary: true }, { route: '/site/examples/admin-dashboard', surface: 'examples' }];
  const tmp = fs.mkdtempSync(path.join(path.dirname(FIXTURE_DIR), 'scoreboard-selftest-'));
  try {
    fs.writeFileSync(path.join(tmp, 'ignored.runs.json'), '{}');
    fs.writeFileSync(path.join(tmp, 'not-a-report.json'), '{"hello":1}');
    const res = build(FIXTURE_DIR, { routes, out: path.join(tmp, 'scoreboard'), budgetsOut: path.join(tmp, 'budgets.json') });
    assert(res.rows.length === 2, `two rows from two fixtures, got ${res.rows.length}`);
    const chat = res.rows.find((r) => r.page === '/site/playground/chat');
    assert(chat && chat.canary && chat.surface === 'playground', 'routes.json tags surface and canary');
    assert(chat.scores.performance === 78 && chat.metrics.lcp_ms === 2368 && chat.requests === 1152, `chat row scores/metrics/requests, got ${JSON.stringify([chat.scores.performance, chat.metrics.lcp_ms, chat.requests])}`);
    assert(chat.topFailing.length === 3 && chat.topFailing[0] === 'cache-insight', 'top 3 failing led by cache-insight');
    const transport = res.clusters.find((c) => c.family === 'transport');
    assert(transport && transport.audits[0].id === 'cache-insight' && transport.audits[0].pages.length === 2, 'cache-insight clusters across both routes');
    const a11yStructure = res.clusters.find((c) => c.family === 'a11y-structure');
    assert(a11yStructure && a11yStructure.audits.some((a) => a.id === 'valid-lang' && a.pages.length === 1), 'valid-lang clusters on the one route that has it');
    const budgets = JSON.parse(fs.readFileSync(path.join(tmp, 'budgets.json'), 'utf8'));
    const bc = budgets.find((b) => b.page === '/site/playground/chat');
    assert(bc.budget.lcp_ms === bc.metrics.lcp_ms + tolerance('lcp_ms', bc.metrics.lcp_ms), 'budget = baseline + tolerance');
    assert(bc.budget.cls === Number((bc.metrics.cls + 0.01).toFixed(4)), 'cls budget +0.01');
    assert(bc.passing.includes('aria-allowed-attr') && bc.budget.perf_score === 78, 'card carries passing audits and the perf score floor');
    assert(['page', 'metrics', 'budget'].every((k) => k in bc), 'check-speed card shape');
    const md = fs.readFileSync(path.join(tmp, 'scoreboard.md'), 'utf8');
    assert(md.includes('| /site/playground/chat (canary) |') && md.includes('### transport'), 'markdown table and cluster sections');
    // Negative control: a dir with no reports fails loudly.
    const empty = fs.mkdtempSync(path.join(tmp, 'empty-'));
    let threw = false;
    try { build(empty, { out: path.join(tmp, 'x') }); } catch { threw = true; }
    assert(threw, 'an empty dir is an error, not an empty scoreboard');
    assert(FIXTURES.length === 2, 'fixture list intact');
    console.log(`selftest ok: ${res.rows.length} rows, ${res.clusters.length} families clustered, budgets seeded for ${budgets.length} routes`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

function main(argv) {
  if (argv[0] === 'selftest') { selftest(); return 0; }
  const opts = { routes: [], out: 'scoreboard', budgetsOut: null };
  let dir = null;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--routes') opts.routes = JSON.parse(fs.readFileSync(argv[++i], 'utf8'));
    else if (a === '--out') opts.out = argv[++i];
    else if (a === '--budgets-out') opts.budgetsOut = argv[++i];
    else if (a.startsWith('--')) { console.error(`unknown flag ${a}`); return 2; }
    else dir = a;
  }
  if (!dir || !fs.existsSync(dir)) { console.error('usage: lh-scoreboard.mjs <reports-dir> [--routes routes.json] [--out scoreboard] [--budgets-out budgets.json] | selftest'); return 2; }
  try {
    const res = build(dir, opts);
    console.log(`scoreboard: ${res.rows.length} route(s), ${res.clusters.length} families; wrote ${res.written.join(', ')}`);
    return 0;
  } catch (e) { console.error(e.message); return 1; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
