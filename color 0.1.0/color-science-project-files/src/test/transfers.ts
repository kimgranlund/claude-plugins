// Transfer-function test runner — for sRGB / Rec.2020 / PQ / HLG encode↔decode.
//
// Transfer modules don't fit the space-module (toXYZ/fromXYZ) or metric-module
// (testCases) shape. They have `encode/decode` pairs and tabulated `testVectors`
// of (linear, encoded) pairs. This runner verifies:
//   1. Forward:    encode(input.linear) ≈ output.encoded
//   2. Inverse:    decode(output.encoded) ≈ input.linear
//   3. Round-trip: decode(encode(linear)) ≈ linear
//
// CLI: `npx tsx src/test/transfers.ts`

import { lInfDistance } from '../types.js';
import * as srgb from '../transfer/srgb.js';
import * as rec2020 from '../transfer/rec2020.js';
import * as pq from '../transfer/pq.js';
import * as hlg from '../transfer/hlg.js';
import * as adobeRgb from '../transfer/adobe-rgb.js';
import * as prophoto from '../transfer/prophoto.js';

// All transfer modules export the same shape but with brand-specific input types.
// We treat them as runtime tuples and ignore the brand for testing purposes.
type TransferModule = {
  readonly encode: (x: any) => any;
  readonly decode: (x: any) => any;
  readonly testVectors: ReadonlyArray<{
    readonly input: readonly [number, number, number] | any;
    readonly output: readonly [number, number, number] | any;
    readonly tolerance: number;
    readonly source: string;
  }>;
};

const registry: Readonly<Record<string, TransferModule>> = {
  srgb: srgb as unknown as TransferModule,
  rec2020: rec2020 as unknown as TransferModule,
  pq: pq as unknown as TransferModule,
  hlg: hlg as unknown as TransferModule,
  adobeRgb: adobeRgb as unknown as TransferModule,
  prophoto: prophoto as unknown as TransferModule,
};

type FailureRecord = {
  readonly module: string;
  readonly vectorIndex: number;
  readonly check: 'forward' | 'inverse' | 'round-trip';
  readonly distance: number;
  readonly tolerance: number;
  readonly source: string;
};

function runModule(name: string, mod: TransferModule): {
  module: string;
  passed: number;
  failed: number;
  failures: FailureRecord[];
} {
  const failures: FailureRecord[] = [];
  let passed = 0;
  mod.testVectors.forEach((vec, i) => {
    // Forward
    const fwd = mod.encode(vec.input) as readonly [number, number, number];
    const dFwd = lInfDistance(fwd, vec.output as any);
    if (dFwd <= vec.tolerance) passed++; else failures.push({
      module: name, vectorIndex: i, check: 'forward',
      distance: dFwd, tolerance: vec.tolerance, source: vec.source,
    });

    // Inverse
    const inv = mod.decode(vec.output) as readonly [number, number, number];
    const dInv = lInfDistance(inv, vec.input as any);
    if (dInv <= vec.tolerance) passed++; else failures.push({
      module: name, vectorIndex: i, check: 'inverse',
      distance: dInv, tolerance: vec.tolerance, source: vec.source,
    });

    // Round-trip
    const rt = mod.decode(mod.encode(vec.input)) as readonly [number, number, number];
    const dRT = lInfDistance(rt, vec.input as any);
    if (dRT <= vec.tolerance) passed++; else failures.push({
      module: name, vectorIndex: i, check: 'round-trip',
      distance: dRT, tolerance: vec.tolerance, source: vec.source,
    });
  });
  return { module: name, passed, failed: failures.length, failures };
}

export function runAllTests() {
  return Object.entries(registry).map(([name, mod]) => runModule(name, mod));
}

export function formatResults(results: ReturnType<typeof runAllTests>): string {
  const lines: string[] = [];
  let totalPassed = 0, totalFailed = 0;
  for (const r of results) {
    const status = r.failed === 0 ? '✓' : '✗';
    lines.push(`${status} ${r.module}: ${r.passed} passed, ${r.failed} failed`);
    totalPassed += r.passed;
    totalFailed += r.failed;
    for (const f of r.failures) {
      lines.push(`  [${f.vectorIndex}] ${f.check}: ${f.source}`);
      lines.push(`    distance: ${f.distance.toExponential(3)} (tolerance ${f.tolerance.toExponential(3)})`);
    }
  }
  lines.push('');
  lines.push(`TOTAL: ${totalPassed} passed, ${totalFailed} failed`);
  return lines.join('\n');
}

const proc = (globalThis as { process?: { argv?: string[]; exit?: (n: number) => never } }).process;
const isMain = !!(proc?.argv && typeof proc.argv[1] === 'string' && proc.argv[1].endsWith('transfers.ts'));
if (isMain) {
  const results = runAllTests();
  // eslint-disable-next-line no-console
  console.log(formatResults(results));
  proc?.exit?.(results.some(r => r.failed > 0) ? 1 : 0);
}
