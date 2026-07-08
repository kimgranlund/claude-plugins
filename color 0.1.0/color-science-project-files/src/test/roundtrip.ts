// Round-trip identity test runner.
//
// For every registered space module, verifies three properties for each test
// vector (`input` is XYZ_D65, `output` is the space's branded value):
//
//   1. Forward:  fromXYZ(input)        ≈ output    (within tolerance)
//   2. RT-input: toXYZ(fromXYZ(input)) ≈ input     (within tolerance)
//   3. RT-output: fromXYZ(toXYZ(output)) ≈ output  (within tolerance)
//
// CLI: `bun src/test/roundtrip.ts` (or `tsx`, `ts-node`, etc.)
// Exit code: 0 = all pass, 1 = any failure.

import type { SpaceModule } from '../convert.js';
import type { TestVector, XYZ_D65 } from '../types.js';
import { lInfDistance } from '../types.js';

import * as xyz from '../spaces/xyz.js';
import * as srgb from '../spaces/srgb.js';
import * as p3 from '../spaces/p3.js';
import * as rec2020 from '../spaces/rec2020.js';
import * as oklab from '../spaces/oklab.js';
import * as oklch from '../spaces/oklch.js';
import * as cielab from '../spaces/cielab.js';
import * as cielch from '../spaces/cielch.js';
import * as hsl from '../spaces/hsl.js';
import * as hsv from '../spaces/hsv.js';
import * as xyy from '../spaces/xyy.js';
import * as okhsl from '../spaces/okhsl.js';
import * as ciecam16 from '../spaces/ciecam16.js';
import * as cam16ucs from '../spaces/cam16-ucs.js';
import * as hct from '../spaces/hct.js';
import * as jzazbz from '../spaces/jzazbz.js';
import * as rec709 from '../spaces/rec709.js';
import * as adobeRgb from '../spaces/adobe-rgb.js';
import * as prophoto from '../spaces/prophoto.js';
import * as cielabD50 from '../spaces/cielab-d50.js';
import * as cielchD50 from '../spaces/cielch-d50.js';
import * as lms from '../spaces/lms.js';
import * as ictcp from '../spaces/ictcp.js';
import * as okhsv from '../spaces/okhsv.js';

// ─── Module registry ──────────────────────────────────────────────────────────

type TestableModule<T> = SpaceModule<T> & {
  readonly testVectors: ReadonlyArray<TestVector<XYZ_D65, T>>;
};

/** Registry: map of module name → module. Add new space modules here as they're built. */
const registry: Readonly<Record<string, TestableModule<any>>> = {
  xyz,
  srgb,
  p3,
  rec2020,
  oklab,
  oklch,
  cielab,
  cielch,
  hsl,
  hsv,
  xyy,
  okhsl,
  ciecam16,
  cam16ucs,
  hct,
  jzazbz,
  rec709,
  adobeRgb,
  prophoto,
  cielabD50,
  cielchD50,
  lms,
  ictcp,
  okhsv,
};

// ─── Result types ─────────────────────────────────────────────────────────────

export type FailureRecord = {
  readonly vectorIndex: number;
  readonly check: 'forward' | 'rt-from-input' | 'rt-from-output';
  readonly expected: readonly number[];
  readonly actual: readonly number[];
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

// ─── Test logic ───────────────────────────────────────────────────────────────

function asTuple(v: unknown): readonly number[] {
  return v as readonly number[];
}

function checkOne<T>(
  mod: TestableModule<T>,
  vec: TestVector<XYZ_D65, T>,
  vectorIndex: number
): FailureRecord[] {
  const failures: FailureRecord[] = [];

  // 1. Forward: fromXYZ(input) ≈ output
  const computed = mod.fromXYZ(vec.input);
  const dForward = lInfDistance(
    asTuple(computed) as [number, number, number],
    asTuple(vec.output) as [number, number, number]
  );
  if (dForward > vec.tolerance) {
    failures.push({
      vectorIndex,
      check: 'forward',
      expected: asTuple(vec.output),
      actual: asTuple(computed),
      distance: dForward,
      tolerance: vec.tolerance,
      source: vec.source,
    });
  }

  // 2. Round trip from input: toXYZ(fromXYZ(input)) ≈ input
  const rtInput = mod.toXYZ(mod.fromXYZ(vec.input));
  const dRT1 = lInfDistance(
    asTuple(rtInput) as [number, number, number],
    asTuple(vec.input) as [number, number, number]
  );
  if (dRT1 > vec.tolerance) {
    failures.push({
      vectorIndex,
      check: 'rt-from-input',
      expected: asTuple(vec.input),
      actual: asTuple(rtInput),
      distance: dRT1,
      tolerance: vec.tolerance,
      source: vec.source,
    });
  }

  // 3. Round trip from output: fromXYZ(toXYZ(output)) ≈ output
  const rtOutput = mod.fromXYZ(mod.toXYZ(vec.output));
  const dRT2 = lInfDistance(
    asTuple(rtOutput) as [number, number, number],
    asTuple(vec.output) as [number, number, number]
  );
  if (dRT2 > vec.tolerance) {
    failures.push({
      vectorIndex,
      check: 'rt-from-output',
      expected: asTuple(vec.output),
      actual: asTuple(rtOutput),
      distance: dRT2,
      tolerance: vec.tolerance,
      source: vec.source,
    });
  }

  return failures;
}

export function testModule(name: string, mod: TestableModule<any>): ModuleResult {
  const failures: FailureRecord[] = [];
  let passed = 0;

  mod.testVectors.forEach((vec, i) => {
    const f = checkOne(mod, vec, i);
    passed += 3 - f.length;
    failures.push(...f);
  });

  return {
    module: name,
    passed,
    failed: failures.length,
    failures,
  };
}

export function runAllTests(): ReadonlyArray<ModuleResult> {
  return Object.entries(registry).map(([name, mod]) => testModule(name, mod));
}

// ─── Formatting ───────────────────────────────────────────────────────────────

function fmtTuple(t: readonly number[]): string {
  return '[' + t.map(n => n.toFixed(7)).join(', ') + ']';
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
      lines.push(`  [${f.vectorIndex}] ${f.check}: ${f.source}`);
      lines.push(`    expected: ${fmtTuple(f.expected)}`);
      lines.push(`    actual:   ${fmtTuple(f.actual)}`);
      lines.push(`    distance: ${f.distance.toExponential(3)} (tolerance ${f.tolerance.toExponential(3)})`);
    }
  }

  lines.push('');
  lines.push(`TOTAL: ${totalPassed} passed, ${totalFailed} failed`);
  return lines.join('\n');
}

// ─── CLI entry point ──────────────────────────────────────────────────────────

// Run when executed directly (works for `bun`, `tsx`, `node --loader`).
const proc = (globalThis as { process?: { argv?: string[]; exit?: (n: number) => never } }).process;
const isMain = !!(
  proc?.argv
  && typeof proc.argv[1] === 'string'
  && proc.argv[1].endsWith('roundtrip.ts')
);

if (isMain) {
  const results = runAllTests();
  // eslint-disable-next-line no-console
  console.log(formatResults(results));
  proc?.exit?.(results.some(r => r.failed > 0) ? 1 : 0);
}
