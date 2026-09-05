#!/usr/bin/env node
/**
 * lh-diff.mjs, the perf-loop regression gate. Node 24, ESM, node built-ins only.
 *
 * Compares two Lighthouse JSON reports (before, after) and prints three sections: regressions
 * (an audit that went passing to failing, a metric that drifted past its tolerance, a category
 * score that dropped), improvements (failing to passing, a metric better than before by more
 * than its tolerance), and unchanged. Exit 1 on ANY regression, so the loop can gate on it.
 *
 *   node lh-diff.mjs <before.json> <after.json> [--json]
 *   node lh-diff.mjs --budgets budgets.json <after.json...>   (perf-sweep: each report vs its budget card)
 *   node lh-diff.mjs selftest
 *
 * Exit: 0 no regression, 1 regression found, 2 usage or parse error.
 *
 * Passing means score >= 0.9 on a scored audit (manual, informative and notApplicable audits are
 * ignored, the metric audits are compared as metrics). Metric tolerance comes from
 * perf-triage's lh-brief.mjs (max(10%, 100 ms) for ms metrics, +0.01 for CLS) so the DO NOT
 * BREAK list in the brief and this gate agree by construction. A budget card carries
 * {page, metrics, budget} (check-speed's budget-check.py shape): a metric over its budget is a
 * regression, a missing budget key is skipped and reported.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { analyze, readReport, tolerance, PASS_SCORE, isScored, FIXTURES } from '../../perf-triage/scripts/lh-brief.mjs';

function pageOf(url) {
  try { return new URL(url).pathname || '/'; } catch { return url || '/'; }
}

/** Metric map {key: value} plus the category scores of one report. */
export function metricsOf(report) {
  const a = analyze(report);
  const metrics = {};
  for (const m of a.metrics) if (m.value != null) metrics[m.key] = m.value;
  return { url: a.header.url, page: pageOf(a.header.url), formFactor: a.header.preset, metrics, scores: a.header.scores };
}

function scoredAudits(report) {
  const out = {};
  const metricIds = new Set(['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index', 'interactive', 'max-potential-fid', 'first-meaningful-paint']);
  for (const [id, a] of Object.entries(report.audits || {})) if (isScored(a) && !metricIds.has(id)) out[id] = a.score;
  return out;
}

/** before/after diff. Returns {regressions, improvements, unchanged, summary}. */
export function diff(before, after) {
  const R = [], I = [], U = [];
  const b = scoredAudits(before), a = scoredAudits(after);
  for (const id of Object.keys({ ...b, ...a }).sort()) {
    const wasPass = b[id] != null && b[id] >= PASS_SCORE;
    const isPass = a[id] != null && a[id] >= PASS_SCORE;
    if (b[id] == null && a[id] != null && !isPass) { R.push(`audit ${id}: new failure (${a[id]}), not scored before`); continue; }
    if (wasPass && a[id] == null) { R.push(`audit ${id}: passing (${b[id]}) -> missing from the after report (dropped, notApplicable, or a different config)`); continue; }
    if (b[id] == null || a[id] == null) { U.push(`audit ${id}: only in ${b[id] == null ? 'after' : 'before'} (score ${b[id] ?? a[id]})`); continue; }
    if (wasPass && !isPass) R.push(`audit ${id}: passing (${b[id]}) -> failing (${a[id]})`);
    else if (!wasPass && isPass) I.push(`audit ${id}: failing (${b[id]}) -> passing (${a[id]})`);
    else if (!wasPass && !isPass && a[id] < b[id]) R.push(`audit ${id}: failing got worse (${b[id]} -> ${a[id]})`);
    else U.push(`audit ${id}: ${isPass ? 'passing' : 'failing'} (${b[id]} -> ${a[id]})`);
  }
  const mb = metricsOf(before), ma = metricsOf(after);
  for (const key of Object.keys(mb.metrics)) {
    const x = mb.metrics[key], y = ma.metrics[key];
    if (y == null) { U.push(`metric ${key}: missing in after`); continue; }
    const tol = tolerance(key, x);
    const fmt = (v) => key === 'cls' ? v.toFixed(3) : `${Math.round(v)} ms`;
    if (y > x + tol) R.push(`metric ${key}: ${fmt(x)} -> ${fmt(y)} (tolerance +${fmt(tol)})`);
    else if (y < x - tol) I.push(`metric ${key}: ${fmt(x)} -> ${fmt(y)}`);
    else U.push(`metric ${key}: ${fmt(x)} -> ${fmt(y)} (within +${fmt(tol)})`);
  }
  for (const cat of Object.keys(mb.scores)) {
    const x = mb.scores[cat], y = ma.scores[cat];
    if (x != null && y == null) { R.push(`score ${cat}: ${x} -> missing from the after report`); continue; }
    if (x == null || y == null) continue;
    if (y < x - 1) R.push(`score ${cat}: ${x} -> ${y}`);
    else if (y > x + 1) I.push(`score ${cat}: ${x} -> ${y}`);
    else U.push(`score ${cat}: ${x} -> ${y}`);
  }
  const warnings = [];
  if (mb.url !== ma.url) warnings.push(`urls differ: before ${mb.url}, after ${ma.url}`);
  if (mb.formFactor !== ma.formFactor) warnings.push(`form factors differ: before ${mb.formFactor}, after ${ma.formFactor}; metric drift across presets is not a regression signal`);
  return { regressions: R, improvements: I, unchanged: U, warnings, before: { url: mb.url, formFactor: mb.formFactor }, after: { url: ma.url, formFactor: ma.formFactor } };
}

/** One report against its budget card ({page, metrics, budget}); unmatched page is a skip. */
export function diffBudget(report, cards) {
  const m = metricsOf(report);
  const samePage = cards.filter((c) => c.page === m.page || c.page === m.url);
  const card = samePage.find((c) => !c.preset || c.preset === m.formFactor);
  const R = [], I = [], U = [];
  if (!card) {
    const why = samePage.length ? `no budget card for ${m.page} with preset ${m.formFactor} (cards carry ${samePage.map((c) => c.preset).join(', ')})` : `no budget card for ${m.page}`;
    return { regressions: R, improvements: I, unchanged: [`${why}: SKIPPED (seed one with lh-scoreboard.mjs --budgets-out)`], page: m.page, formFactor: m.formFactor, skipped: true };
  }
  const budget = card.budget || {};
  for (const key of Object.keys(m.metrics)) {
    if (budget[key] == null) { U.push(`metric ${key}: no budget, skipped`); continue; }
    const v = m.metrics[key];
    const fmt = (x) => key === 'cls' ? Number(x).toFixed(3) : `${Math.round(x)} ms`;
    if (v > budget[key]) R.push(`metric ${key}: ${fmt(v)} over budget ${fmt(budget[key])}`);
    else U.push(`metric ${key}: ${fmt(v)} within budget ${fmt(budget[key])}`);
  }
  if (budget.perf_score != null && m.scores.performance != null && m.scores.performance < budget.perf_score) R.push(`score performance: ${m.scores.performance} under budget ${budget.perf_score}`);
  for (const id of card.passing || []) {
    const audit = report.audits?.[id];
    if (!isScored(audit)) R.push(`audit ${id}: budgeted passing, missing or unscored in this report`);
    else if (audit.score < PASS_SCORE) R.push(`audit ${id}: budgeted passing, now ${audit.score}`);
  }
  return { regressions: R, improvements: I, unchanged: U, page: m.page, formFactor: m.formFactor, skipped: false };
}

export function render(d, label) {
  const L = [`# lh-diff ${label}`];
  if (d.before && d.after) L.push(`before: ${d.before.url} (${d.before.formFactor})`, `after:  ${d.after.url} (${d.after.formFactor})`);
  for (const w of d.warnings || []) L.push(`WARNING: ${w}`);
  for (const [title, rows] of [['Regressions', d.regressions], ['Improvements', d.improvements], ['Unchanged', d.unchanged]]) {
    L.push('', `## ${title} (${rows.length})`);
    for (const r of rows) L.push(`- ${r}`);
  }
  L.push('', d.regressions.length ? `VERDICT: REGRESSION (${d.regressions.length})` : 'VERDICT: no regression');
  return L.join('\n');
}

function assert(cond, msg) { if (!cond) throw new Error(`selftest: ${msg}`); }

function selftest() {
  const [chat, admin] = FIXTURES.map(readReport);
  // Identical reports: nothing regresses.
  const same = diff(chat, chat);
  assert(same.regressions.length === 0, 'identical reports carry no regression');
  // The two fixtures treated as before/after report the audits that differ.
  const d = diff(chat, admin);
  assert(d.regressions.some((r) => r.startsWith('audit aria-allowed-attr: passing')), 'aria-allowed-attr passing on chat, failing on admin is a regression');
  assert(d.regressions.some((r) => r.startsWith('audit valid-lang: new failure')), 'valid-lang, not scored on chat and failing on admin, is a new failure');
  assert(d.regressions.some((r) => r.startsWith('metric tbt_ms')), 'TBT 90 -> 2930 ms is outside tolerance');
  assert(d.regressions.some((r) => r.startsWith('score performance: 78 -> 44')), 'performance score drop named');
  assert(d.improvements.some((r) => r.startsWith('audit errors-in-console')), 'errors-in-console failing on chat, passing on admin is an improvement');
  const back = diff(admin, chat);
  assert(back.improvements.some((r) => r.startsWith('audit aria-allowed-attr')), 'reverse direction reports the improvement');
  // Negative control: flip one passing audit to failing in a copy and expect a regression.
  const flipped = JSON.parse(JSON.stringify(chat));
  const victim = Object.entries(flipped.audits).find(([id, a]) => isScored(a) && a.score === 1 && !/paint|blocking|layout-shift|speed-index|interactive|fid/.test(id))[0];
  flipped.audits[victim].score = 0;
  const neg = diff(chat, flipped);
  assert(neg.regressions.length === 1 && neg.regressions[0].startsWith(`audit ${victim}: passing`), `flipping ${victim} yields exactly one regression, got ${JSON.stringify(neg.regressions)}`);
  // Negative control 2: a passing audit and a whole category deleted from the after report.
  const dropped = JSON.parse(JSON.stringify(chat));
  delete dropped.audits['is-on-https'];
  delete dropped.categories.seo;
  const drop = diff(chat, dropped);
  assert(drop.regressions.some((r) => r.startsWith('audit is-on-https: passing (1) -> missing')), 'a passing audit missing from after is a regression');
  assert(drop.regressions.some((r) => r.startsWith('score seo: 91 -> missing')), 'a missing category score is a regression');
  assert(drop.regressions.length === 2, `exactly two regressions from the drop, got ${JSON.stringify(drop.regressions)}`);
  // Plain mode names both urls and form factors and warns when they differ.
  assert(same.warnings.length === 0 && same.before.formFactor === 'desktop', 'identical reports carry no warning');
  const mobile = JSON.parse(JSON.stringify(chat));
  mobile.configSettings.formFactor = 'mobile';
  const mixed = diff(chat, mobile);
  assert(mixed.warnings.some((w) => w.startsWith('form factors differ')), 'preset mismatch warns');
  assert(d.warnings.some((w) => w.startsWith('urls differ')), 'url mismatch warns');
  assert(render(mixed, 'x').includes('WARNING: form factors differ') && render(mixed, 'x').includes('before: https://ui-kit.exe.xyz/site/playground/chat (desktop)'), 'render prints urls, form factors and warnings');
  // Metric drift inside tolerance is unchanged; outside is a regression.
  const drift = JSON.parse(JSON.stringify(chat));
  drift.audits['largest-contentful-paint'].numericValue += 50;
  assert(diff(chat, drift).regressions.length === 0, '50 ms LCP drift on 2400 ms is within tolerance');
  drift.audits['largest-contentful-paint'].numericValue += 300;
  assert(diff(chat, drift).regressions.some((r) => r.startsWith('metric lcp_ms')), '350 ms LCP drift is a regression');
  // Budget mode: baseline card passes, tightened card fails, unknown page skips.
  const m = metricsOf(chat);
  const card = { page: m.page, metrics: m.metrics, budget: { ...m.metrics, perf_score: m.scores.performance }, passing: ['aria-allowed-attr'] };
  assert(diffBudget(chat, [card]).regressions.length === 0, 'a report meets its own baseline budget');
  const tight = { ...card, budget: { ...card.budget, lcp_ms: card.budget.lcp_ms - 1 } };
  assert(diffBudget(chat, [tight]).regressions.some((r) => r.startsWith('metric lcp_ms')), 'a tightened budget bites');
  assert(diffBudget(admin, [card]).skipped === true, 'no card for the page is a skip, never a silent pass');
  assert(diffBudget(admin, [{ ...card, page: metricsOf(admin).page }]).regressions.some((r) => r.startsWith('audit aria-allowed-attr')), 'a budgeted passing audit that fails is a regression');
  const mobileCard = { ...card, preset: 'mobile' };
  assert(diffBudget(chat, [mobileCard]).skipped === true, 'a card for another preset does not match');
  assert(diffBudget(chat, [mobileCard, { ...card, preset: 'desktop' }]).skipped === false, 'the card with the matching preset is picked');
  const droppedBudget = diffBudget(dropped, [{ ...card, passing: ['is-on-https'] }]);
  assert(droppedBudget.regressions.some((r) => r.startsWith('audit is-on-https: budgeted passing, missing')), 'a budgeted passing audit missing from the report is a regression');
  const text = render(d, 'chat -> admin');
  assert(text.includes('VERDICT: REGRESSION'), 'render names the verdict');
  console.log(`selftest ok: chat->admin ${d.regressions.length} regressions / ${d.improvements.length} improvements / ${d.unchanged.length} unchanged; negative control on ${victim} exits 1`);
}

function main(argv) {
  if (argv[0] === 'selftest') { selftest(); return 0; }
  const files = [];
  let budgets = null, asJson = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--budgets') budgets = argv[++i];
    else if (argv[i] === '--json') asJson = true;
    else if (argv[i].startsWith('--')) { console.error(`unknown flag ${argv[i]}`); return 2; }
    else files.push(argv[i]);
  }
  try {
    if (budgets) {
      if (!files.length) { console.error('usage: lh-diff.mjs --budgets budgets.json <after.json...>'); return 2; }
      const cards = JSON.parse(fs.readFileSync(budgets, 'utf8'));
      const list = Array.isArray(cards) ? cards : (cards.cards || [cards]);
      let worst = 0;
      const results = [];
      for (const f of files) {
        const d = diffBudget(readReport(f), list);
        results.push(d);
        if (d.regressions.length) worst = 1;
        if (!asJson) console.log(render(d, `${path.basename(f)} vs budget ${d.page}`), '\n');
      }
      if (asJson) console.log(JSON.stringify(results, null, 2));
      return worst;
    }
    if (files.length !== 2) { console.error('usage: lh-diff.mjs <before.json> <after.json> [--json] | --budgets budgets.json <after.json...> | selftest'); return 2; }
    const d = diff(readReport(files[0]), readReport(files[1]));
    if (asJson) console.log(JSON.stringify(d, null, 2));
    else console.log(render(d, `${path.basename(files[0])} -> ${path.basename(files[1])}`));
    return d.regressions.length ? 1 : 0;
  } catch (e) {
    console.error(e.message);
    return 2;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
