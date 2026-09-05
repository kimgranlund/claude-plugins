#!/usr/bin/env node
/**
 * lh-run.mjs, the perf-audit runner. Node 24, ESM, node built-ins only; shells out to
 * `npx lighthouse@13` (pinned major) with headless Chrome.
 *
 *   node lh-run.mjs <url> [--preset desktop|mobile|both] [--runs 3] [--out dir] [--chrome-flags "..."]
 *   node lh-run.mjs selftest
 *
 * Per preset: runs Lighthouse N times, keeps the run with the MEDIAN performance score, writes
 * it to <out>/<slug>.<preset>.json and a sidecar <slug>.<preset>.runs.json listing every run's
 * category scores (so a noisy run is visible, never hidden). The slug derives from the URL
 * (host + path). Desktop uses `--preset=desktop`; mobile is Lighthouse's default config.
 *
 * Exit: 0 every preset wrote a report, 1 a Lighthouse run failed, 2 usage error or npx missing.
 *
 * Verified 2026-09-05 on ui-kit.exe.xyz with the host's Playwright Chromium:
 *   npx lighthouse@13 <url> --output=json --output-path=out.json --quiet --chrome-flags="--headless=new" --preset=desktop
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const LIGHTHOUSE_SPEC = 'lighthouse@13';

export function slugOf(url) {
  const u = new URL(url);
  const p = u.pathname.replace(/\/+$/, '').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '');
  return (u.hostname + (p ? '-' + p : '')).toLowerCase();
}

export function lighthouseArgs(url, preset, outPath, chromeFlags) {
  const args = [LIGHTHOUSE_SPEC, url, '--output=json', `--output-path=${outPath}`, '--quiet', `--chrome-flags=${chromeFlags}`];
  if (preset === 'desktop') args.push('--preset=desktop');
  else if (preset === 'mobile') args.push('--form-factor=mobile');
  return args;
}

/** Category scores {performance, accessibility, ...} as 0-100 integers. */
export function scoresOf(report) {
  return Object.fromEntries(Object.entries(report.categories || {}).map(([k, v]) => [k, v.score == null ? null : Math.round(v.score * 100)]));
}

/** Index of the run holding the median performance score (upper median on even counts). */
export function medianIndex(runs) {
  const order = runs.map((r, i) => [r.scores.performance ?? -1, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  return order[Math.floor(order.length / 2)][1];
}

function runOnce(url, preset, chromeFlags, tmp) {
  const outPath = path.join(tmp, `run-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.json`);
  const r = spawnSync('npx', lighthouseArgs(url, preset, outPath, chromeFlags), { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 600000 });
  if (r.status !== 0 || !fs.existsSync(outPath)) {
    throw new Error(`lighthouse ${preset} run failed (exit ${r.status}): ${(r.stderr || r.stdout || '').trim().split('\n').slice(-5).join(' | ')}`);
  }
  return JSON.parse(fs.readFileSync(outPath, 'utf8'));
}

export function audit(url, { preset = 'both', runs = 3, out = 'perf-reports', chromeFlags = '--headless=new', runner = runOnce } = {}) {
  const presets = preset === 'both' ? ['desktop', 'mobile'] : [preset];
  fs.mkdirSync(out, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lh-run-'));
  const slug = slugOf(url);
  const written = [];
  for (const p of presets) {
    const results = [];
    for (let i = 0; i < runs; i++) {
      const report = runner(url, p, chromeFlags, tmp);
      results.push({ index: i + 1, fetchTime: report.fetchTime, scores: scoresOf(report), report });
      console.log(`${p} run ${i + 1}/${runs}: ${Object.entries(results[i].scores).map(([k, v]) => `${k} ${v}`).join(', ')}`);
    }
    const keep = medianIndex(results);
    const target = path.join(out, `${slug}.${p}.json`);
    fs.writeFileSync(target, JSON.stringify(results[keep].report));
    fs.writeFileSync(path.join(out, `${slug}.${p}.runs.json`), JSON.stringify({ url, preset: p, lighthouse: LIGHTHOUSE_SPEC, kept: keep + 1, runs: results.map(({ index, fetchTime, scores }) => ({ index, fetchTime, scores })) }, null, 2));
    console.log(`${p}: kept run ${keep + 1} (median performance ${results[keep].scores.performance}) -> ${target}`);
    written.push(target);
  }
  return written;
}

function assert(cond, msg) { if (!cond) throw new Error(`selftest: ${msg}`); }

const FIXTURE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'perf-triage', 'assets', 'fixtures');

function selftest() {
  // Parses a fixture and prints the category scores.
  const fixture = path.join(FIXTURE_DIR, 'chat.desktop.slim.json');
  const report = JSON.parse(fs.readFileSync(fixture, 'utf8'));
  const scores = scoresOf(report);
  assert(scores.performance === 78 && scores.accessibility === 92, `fixture scores parsed, got ${JSON.stringify(scores)}`);
  console.log(`fixture ${path.basename(fixture)}: ${Object.entries(scores).map(([k, v]) => `${k} ${v}`).join(', ')}`);
  assert(slugOf('https://ui-kit.exe.xyz/site/playground/chat/') === 'ui-kit.exe.xyz-site-playground-chat', 'slug from host + path');
  assert(slugOf('https://example.com') === 'example.com', 'root slug is the host');
  const a = lighthouseArgs('https://x.y', 'desktop', '/tmp/o.json', '--headless=new');
  assert(a[0] === 'lighthouse@13' && a.includes('--preset=desktop') && a.includes('--chrome-flags=--headless=new'), 'desktop args pin the major and the preset');
  assert(!lighthouseArgs('https://x.y', 'mobile', '/tmp/o.json', '--headless=new').includes('--preset=desktop'), 'mobile args carry no desktop preset');
  const runs = [{ scores: { performance: 90 } }, { scores: { performance: 70 } }, { scores: { performance: 80 } }];
  assert(medianIndex(runs) === 2, 'median of 90/70/80 is the 80 run');
  assert(medianIndex(runs.slice(0, 2)) === 0, 'upper median on two runs');
  // audit() end to end with a fake runner: writes <slug>.<preset>.json holding the median run.
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lh-run-selftest-'));
  let n = 0;
  const fake = () => { n += 1; const r = JSON.parse(JSON.stringify(report)); r.categories.performance.score = [0.9, 0.5, 0.7][(n - 1) % 3]; r.fetchTime = `run-${n}`; return r; };
  const written = audit('https://ui-kit.exe.xyz/site/playground/chat', { preset: 'both', runs: 3, out: tmp, runner: fake });
  assert(written.length === 2 && n === 6, 'both presets, three runs each');
  const kept = JSON.parse(fs.readFileSync(written[0], 'utf8'));
  assert(Math.round(kept.categories.performance.score * 100) === 70, 'the median run is the one kept');
  const side = JSON.parse(fs.readFileSync(written[0].replace(/\.json$/, '.runs.json'), 'utf8'));
  assert(side.runs.length === 3 && side.kept === 3, 'runs sidecar lists every run and names the kept one');
  assert(path.basename(written[1]) === 'ui-kit.exe.xyz-site-playground-chat.mobile.json', 'mobile file name');
  // Negative control: a failing runner surfaces as an error, never a partial pass.
  let threw = false;
  try { audit('https://x.y/', { preset: 'desktop', runs: 1, out: tmp, runner: () => { throw new Error('boom'); } }); } catch (e) { threw = /boom/.test(e.message); }
  assert(threw, 'runner failure propagates');
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('selftest ok');
}

function main(argv) {
  if (argv[0] === 'selftest') { selftest(); return 0; }
  const opts = { preset: 'both', runs: 3, out: 'perf-reports', chromeFlags: '--headless=new' };
  let url = null;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--preset') opts.preset = argv[++i];
    else if (a === '--runs') opts.runs = Number(argv[++i]);
    else if (a === '--out') opts.out = argv[++i];
    else if (a === '--chrome-flags') opts.chromeFlags = argv[++i];
    else if (a.startsWith('--')) { console.error(`unknown flag ${a}`); return 2; }
    else url = a;
  }
  if (!url || !['desktop', 'mobile', 'both'].includes(opts.preset) || !(opts.runs >= 1)) {
    console.error('usage: lh-run.mjs <url> [--preset desktop|mobile|both] [--runs 3] [--out dir] [--chrome-flags "--headless=new"] | selftest');
    return 2;
  }
  if (/^https?:\/\/(localhost|127\.0\.0\.1)/.test(url)) console.error('note: auditing localhost; numbers from a dev server differ from the deployed origin (perf-audit SKILL.md), prefer the deployed URL');
  if (!spawnSync('npx', ['--version'], { encoding: 'utf8' }).stdout) { console.error('npx not found on PATH; install Node 24 or use the DevTools fallback in perf-audit SKILL.md'); return 2; }
  try { audit(url, opts); return 0; } catch (e) { console.error(e.message); return 1; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
