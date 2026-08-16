#!/usr/bin/env node
/**
 * chore_sweep_apply.mjs — apply an ops-family seat's fenced, target-pathed payload blocks
 * (ops-write-sandbox-rules) and flag any narrated-but-absent write claim.
 *
 * Mechanizes what chore-lead (retired, issue #266) used to do by eye in its own step 3: parse a
 * seat's raw report text, Write every fenced block headed by a `.claude/ops/...` target path to
 * that path verbatim, and name any first-person write claim (wrote/emitted/produced/saved paired
 * with a `.claude/ops/...`-shaped path) that has no matching fenced block behind it.
 *
 * Usage: chore_sweep_apply.mjs <report-file> [--root <repo-root>] [--dry-run]
 *   <report-file>   A file containing one seat's (or chore-planner's) raw report text.
 *   --root <dir>    Repo root every fenced block's target path resolves against. Default: cwd.
 *   --dry-run       Parse and report, write nothing — for inspection.
 *
 * Exit codes: 0 clean (blocks applied or none present, no findings) · 1 findings (a
 * narrated-but-absent claim, or a block whose target path falls outside the `.claude/ops/`
 * sandbox — never guessed at, never written) · 2 usage error.
 *
 * `chore_sweep_apply.mjs selftest` proves the two extraction/detection functions on inline
 * fixtures: a real block applies; a narrated-but-absent claim bites; a bare path mention with no
 * write verb does NOT false-positive; an out-of-sandbox target path is refused, never written.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname, resolve } from 'node:path'

const SANDBOX_PREFIX = '.claude/ops/'
const WRITE_VERBS = ['wrote', 'emitted', 'produced', 'saved']

// A fence line is exactly three backticks immediately followed by the target path (no language
// tag) — the ops-write-sandbox-rules shape: ```.claude/ops/adr-queue.json ... ```
const FENCE_RE = /^```(\S+)\r?\n([\s\S]*?)\r?\n```$/gm

/** Extract every fenced, target-pathed block. Returns { blocks: [{path, content}], sandboxed, outOfSandbox } */
export function extractBlocks(reportText) {
  const blocks = []
  let m
  FENCE_RE.lastIndex = 0
  while ((m = FENCE_RE.exec(reportText)) !== null) {
    blocks.push({ path: m[1], content: m[2] })
  }
  const sandboxed = blocks.filter((b) => b.path.startsWith(SANDBOX_PREFIX))
  const outOfSandbox = blocks.filter((b) => !b.path.startsWith(SANDBOX_PREFIX))
  return { sandboxed, outOfSandbox }
}

/**
 * Detect narrated-but-absent write claims: a WRITE_VERBS word sharing a line with a
 * `.claude/ops/...`-shaped token that has no matching fenced block. A bare path mention with no
 * write verb on the same line is never flagged (reverse control) — this mirrors
 * ops-write-sandbox-rules' own definition verbatim (verbs paired with a path, not any mention).
 */
export function detectNarratedButAbsent(reportText, sandboxedBlocks) {
  // Strip fenced-block bodies first so a verb *inside* a payload's own content never counts.
  const withoutFences = reportText.replace(FENCE_RE, '')
  const backedPaths = new Set(sandboxedBlocks.map((b) => b.path))
  const verbRe = new RegExp(`\\b(${WRITE_VERBS.join('|')})\\b`, 'i')
  const pathRe = /\.claude\/ops\/\S+/g
  const findings = []
  for (const rawLine of withoutFences.split(/\r?\n/)) {
    if (!verbRe.test(rawLine)) continue
    let pm
    pathRe.lastIndex = 0
    while ((pm = pathRe.exec(rawLine)) !== null) {
      const path = pm[0].replace(/[.,;:)\]]+$/, '') // trailing punctuation
      if (!backedPaths.has(path)) findings.push(path)
    }
  }
  return [...new Set(findings)]
}

function applyBlocks(sandboxed, root, dryRun) {
  const applied = []
  for (const { path, content } of sandboxed) {
    const target = join(root, path)
    if (!dryRun) {
      mkdirSync(dirname(target), { recursive: true })
      writeFileSync(target, content.endsWith('\n') ? content : content + '\n')
    }
    applied.push(path)
  }
  return applied
}

function usage() {
  console.log(
    [
      'Usage: chore_sweep_apply.mjs <report-file> [--root <repo-root>] [--dry-run]',
      '       chore_sweep_apply.mjs selftest',
      '',
      'Applies every fenced, target-pathed .claude/ops/ payload block in <report-file> and names',
      'any narrated-but-absent write claim. Exit 0 clean, 1 findings, 2 usage error.',
    ].join('\n'),
  )
}

function main(argv) {
  if (argv[0] === 'selftest') return selftest()
  if (argv.length === 0 || argv[0].startsWith('--')) {
    usage()
    return 2
  }
  const reportFile = argv[0]
  let root = process.cwd()
  let dryRun = false
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === '--root') root = resolve(argv[++i] ?? '.')
    else if (argv[i] === '--dry-run') dryRun = true
    else {
      console.error(`Unknown flag: ${argv[i]}`)
      return 2
    }
  }
  if (!existsSync(reportFile)) {
    console.error(`Report file not found: ${reportFile}`)
    return 2
  }
  const reportText = readFileSync(reportFile, 'utf8')
  const { sandboxed, outOfSandbox } = extractBlocks(reportText)
  const applied = applyBlocks(sandboxed, root, dryRun)
  const narrated = detectNarratedButAbsent(reportText, sandboxed)

  let findings = false
  console.log(`chore_sweep_apply · ${applied.length} applied${dryRun ? ' (dry-run)' : ''}`)
  for (const p of applied) console.log(`  applied: ${p}`)
  if (outOfSandbox.length > 0) {
    findings = true
    for (const b of outOfSandbox) console.log(`  refused (outside ${SANDBOX_PREFIX}): ${b.path}`)
  }
  if (narrated.length > 0) {
    findings = true
    for (const p of narrated) console.log(`  narrated-but-absent: ${p}`)
  }
  return findings ? 1 : 0
}

function selftest() {
  const dir = mkdtempSync(join(tmpdir(), 'chore-sweep-apply-'))
  let failures = 0
  const assert = (cond, msg) => {
    if (!cond) {
      failures++
      console.error(`FAIL: ${msg}`)
    }
  }

  try {
    // 1. Positive: a real fenced block applies cleanly, exit 0.
    const clean = '```.claude/ops/plan.md\n{"queue":[]}\n```\n'
    const cleanFile = join(dir, 'clean.md')
    writeFileSync(cleanFile, clean)
    const cleanCode = main([cleanFile, '--root', dir])
    assert(cleanCode === 0, 'a real fenced block must apply with exit 0')
    assert(existsSync(join(dir, '.claude/ops/plan.md')), 'the fenced block must actually be written')

    // 2. Negative control: a narrated-but-absent claim must bite (exit 1), and must NOT write.
    const narrated = 'I wrote .claude/ops/adr-queue.json with the new candidates this firing.\n'
    const narratedFile = join(dir, 'narrated.md')
    writeFileSync(narratedFile, narrated)
    const narratedCode = main([narratedFile, '--root', dir])
    assert(narratedCode === 1, 'a narrated-but-absent claim must exit 1')
    assert(!existsSync(join(dir, '.claude/ops/adr-queue.json')), 'a narrated-but-absent claim must never write a file')

    // 3. Reverse control: a bare path mention with no write verb must NOT false-positive.
    const bareMention = 'See .claude/ops/plan.md for the prior queue before this firing.\n'
    const bareFile = join(dir, 'bare.md')
    writeFileSync(bareFile, bareMention)
    const bareCode = main([bareFile, '--root', dir, '--dry-run'])
    assert(bareCode === 0, 'a bare path mention with no write verb must not be flagged narrated-but-absent')

    // 4. Safety: a fenced block outside the .claude/ops/ sandbox is refused, never written.
    const outOfSandbox = '```harness/agents/decision-watcher.md\nmalicious content\n```\n'
    const oosFile = join(dir, 'oos.md')
    writeFileSync(oosFile, outOfSandbox)
    const oosCode = main([oosFile, '--root', dir])
    assert(oosCode === 1, 'an out-of-sandbox target path must exit 1 (refused)')
    assert(!existsSync(join(dir, 'harness/agents/decision-watcher.md')), 'an out-of-sandbox block must never be written')

    // 5. Usage error: missing file → exit 2.
    const usageCode = main([join(dir, 'does-not-exist.md')])
    assert(usageCode === 2, 'a missing report file must exit 2 (usage error)')

    // 6. No-args → exit 2.
    const noArgsCode = main([])
    assert(noArgsCode === 2, 'no args must exit 2 (usage error)')
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }

  if (failures > 0) {
    console.log(`chore_sweep_apply selftest · FAIL · ${failures} failing assertion(s)`)
    return 1
  }
  console.log('chore_sweep_apply selftest · PASS · apply/narrated-but-absent/reverse-control/sandbox-refusal/usage all correct')
  return 0
}

if (import.meta.url === `file://${process.argv[1]}`) {
  process.exit(main(process.argv.slice(2)))
}
