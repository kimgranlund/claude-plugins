// Metrics test runner — for modules that don't fit the space-module `toXYZ/fromXYZ`
// contract (ΔE family, APCA, chromatic adaptation).
//
// Every metric module exports `testCases: ReadonlyArray<MetricTest>` where each
// case is a thunk returning a number and an expected value with tolerance.
// CLI: `npx tsx src/test/metrics.ts`

import * as deltaE from '../metrics/deltaE.js';
import * as apca from '../metrics/apca.js';
import * as bradford from '../adaptation/bradford.js';
import * as cusp from '../gamut/cusp.js';
import * as mapping from '../gamut/mapping.js';
import * as linearInterp from '../interpolation/linear.js';
import * as cubehelix from '../interpolation/cubehelix.js';
import * as lightnessCurves from '../interpolation/lightness-curves.js';
import * as machado from '../cvd/machado-2009.js';
import * as reinhard from '../tonemap/reinhard.js';
import * as aces from '../tonemap/aces.js';
import * as spd from '../spectral/spd.js';
import * as kubelkaMunk from '../pigment/kubelka-munk.js';
import * as kmeans from '../quantize/kmeans.js';
import * as floydSteinberg from '../dithering/floyd-steinberg.js';
import * as spline from '../interpolation/spline.js';
import * as luminance from '../metrics/luminance.js';
import * as oklchPeak from '../gamut/oklch-peak.js';
import type { MetricTest } from '../metrics/deltaE.js';

type TestableMetric = { readonly testCases: ReadonlyArray<MetricTest> };

const registry: Readonly<Record<string, TestableMetric>> = {
  deltaE,
  apca,
  bradford,
  cusp,
  mapping,
  linearInterp,
  cubehelix,
  lightnessCurves,
  machado,
  reinhard,
  aces,
  spd,
  kubelkaMunk,
  kmeans,
  floydSteinberg,
  spline,
  luminance,
  oklchPeak,
};

export type FailureRecord = {
  readonly module: string;
  readonly test: string;
  readonly expected: number;
  readonly actual: number;
  readonly distance: number;
  readonly tolerance: number;
  readonly source: string;
};

export type ModuleResult = {
  readonly module: string;
  readonly passed: number;
  readonly failed: number;
  readonly failures: ReadonlyArray<FailureRecord>;
};

function runOne(modName: string, mod: TestableMetric): ModuleResult {
  const failures: FailureRecord[] = [];
  let passed = 0;
  for (const tc of mod.testCases) {
    let actual: number;
    try {
      actual = tc.fn();
    } catch (e) {
      failures.push({
        module: modName,
        test: tc.name,
        expected: tc.expected,
        actual: NaN,
        distance: Infinity,
        tolerance: tc.tolerance,
        source: tc.source + ` (threw: ${(e as Error).message})`,
      });
      continue;
    }
    const d = Math.abs(actual - tc.expected);
    if (d <= tc.tolerance) {
      passed++;
    } else {
      failures.push({
        module: modName,
        test: tc.name,
        expected: tc.expected,
        actual,
        distance: d,
        tolerance: tc.tolerance,
        source: tc.source,
      });
    }
  }
  return { module: modName, passed, failed: failures.length, failures };
}

export function runAllTests(): ReadonlyArray<ModuleResult> {
  return Object.entries(registry).map(([name, mod]) => runOne(name, mod));
}

export function formatResults(results: ReadonlyArray<ModuleResult>): string {
  const lines: string[] = [];
  let totalPassed = 0;
  let totalFailed = 0;
  for (const r of results) {
    const status = r.failed === 0 ? '✓' : '✗';
    lines.push(`${status} ${r.module}: ${r.passed} passed, ${r.failed} failed`);
    totalPassed += r.passed;
    totalFailed += r.failed;
    for (const f of r.failures) {
      lines.push(`  • ${f.test}`);
      lines.push(`    expected: ${f.expected}`);
      lines.push(`    actual:   ${f.actual}`);
      lines.push(`    distance: ${f.distance.toExponential(3)} (tolerance ${f.tolerance.toExponential(3)})`);
      lines.push(`    source:   ${f.source}`);
    }
  }
  lines.push('');
  lines.push(`TOTAL: ${totalPassed} passed, ${totalFailed} failed`);
  return lines.join('\n');
}

const proc = (globalThis as { process?: { argv?: string[]; exit?: (n: number) => never } }).process;
const isMain = !!(
  proc?.argv
  && typeof proc.argv[1] === 'string'
  && proc.argv[1].endsWith('metrics.ts')
);

if (isMain) {
  const results = runAllTests();
  // eslint-disable-next-line no-console
  console.log(formatResults(results));
  proc?.exit?.(results.some(r => r.failed > 0) ? 1 : 0);
}
