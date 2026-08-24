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
 * write verb does NOT false-positive; a declarative report-path claim ("Report target: <path>",
 * issue #924) with no matching fenced block also bites, while the same phrase backed by a real
 * block does NOT false-positive; an out-of-sandbox target path is refused, never written; the
 * entry guard fires when the script lives under a path containing a space (the real plugin
 * install path) — the negative control for the silent-no-op guard bug fixed 2026-08-16; and (issue
 * #738) a stale payload — one whose `--firing` stamp predates the target file's own last commit —
 * is refused by name (exit 1, nothing written) while a fresh payload still applies, and a target
 * with no git history at all fails OPEN and DISCLOSES that in stdout rather than refusing silently.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync, mkdtempSync, rmSync, realpathSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { execFileSync } from 'node:child_process'

const SANDBOX_PREFIX = '.claude/ops/'
const WRITE_VERBS = ['wrote', 'emitted', 'produced', 'saved']
// Declarative report-path phrases (issue #924): a seat can name where a report landed without
// using any WRITE_VERBS word at all — "Report target: <path>" is the exact shape #922 fixed at
// the issue-sorter skill level, but nothing here caught it generically. Multi-word, so matched
// separately from the single-word WRITE_VERBS below rather than folded into that list.
const REPORT_PHRASES = ['report target', 'report destination']

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
 * Detect narrated-but-absent write claims: a WRITE_VERBS word, or a REPORT_PHRASES declarative
 * report-path phrase (issue #924 — "Report target:"/"Report destination:" carries no write verb
 * at all), sharing a line with a `.claude/ops/...`-shaped token that has no matching fenced
 * block. A bare path mention with neither a write verb nor a report phrase on the same line is
 * never flagged (reverse control) — this mirrors ops-write-sandbox-rules' own definition verbatim
 * (a claiming word/phrase paired with a path, not any mention).
 */
export function detectNarratedButAbsent(reportText, sandboxedBlocks) {
  // Strip fenced-block bodies first so a verb *inside* a payload's own content never counts.
  const withoutFences = reportText.replace(FENCE_RE, '')
  const backedPaths = new Set(sandboxedBlocks.map((b) => b.path))
  const verbRe = new RegExp(`\\b(${WRITE_VERBS.join('|')})\\b|(${REPORT_PHRASES.join('|')})`, 'i')
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

/**
 * The target file's own last-commit timestamp (ISO-8601, %cI), or null when git has no history
 * for that path (never committed) — the disclosed fail-open case, never a refusal.
 */
function targetCommitTime(root, relPath) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cI', '--', relPath], {
      cwd: root,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim()
    return out.length > 0 ? out : null
  } catch {
    return null
  }
}

/**
 * Staleness guard (issue #738): a payload whose own firing/dispatch stamp predates the target
 * file's last commit is refusing a rollback-over-newer-state write, mirroring the existing
 * outside-ops-path refusal's fail-closed shape — refused by name, exit 1, other blocks in the same
 * run still apply. No git history for the target at all (never committed) is the disclosed
 * fail-open case: apply normally, but name it in stdout rather than passing silently.
 */
function applyBlocks(sandboxed, root, dryRun, firingIso) {
  const applied = []
  const staleRefused = []
  const noHistoryDisclosed = []
  for (const { path, content } of sandboxed) {
    if (firingIso) {
      const commitIso = targetCommitTime(root, path)
      if (commitIso === null) {
        noHistoryDisclosed.push(path)
      } else if (new Date(firingIso).getTime() < new Date(commitIso).getTime()) {
        staleRefused.push({ path, commitIso })
        continue // refused: never written, other blocks in this run still proceed
      }
    }
    const target = join(root, path)
    if (!dryRun) {
      mkdirSync(dirname(target), { recursive: true })
      writeFileSync(target, content.endsWith('\n') ? content : content + '\n')
    }
    applied.push(path)
  }
  return { applied, staleRefused, noHistoryDisclosed }
}

function usage() {
  console.log(
    [
      'Usage: chore_sweep_apply.mjs <report-file> [--root <repo-root>] [--dry-run] [--firing <ISO-8601>]',
      '       chore_sweep_apply.mjs selftest',
      '',
      'Applies every fenced, target-pathed .claude/ops/ payload block in <report-file> and names',
      'any narrated-but-absent write claim. --firing names this payload\'s own dispatch stamp: a',
      'block whose target file was committed AFTER that stamp is refused as stale (never written);',
      'a target with no git history at all fails open and discloses that. Exit 0 clean, 1 findings,',
      '2 usage error.',
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
  let firingIso = null
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === '--root') root = resolve(argv[++i] ?? '.')
    else if (argv[i] === '--dry-run') dryRun = true
    else if (argv[i] === '--firing') firingIso = argv[++i] ?? null
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
  const { applied, staleRefused, noHistoryDisclosed } = applyBlocks(sandboxed, root, dryRun, firingIso)
  const narrated = detectNarratedButAbsent(reportText, sandboxed)

  let findings = false
  console.log(`chore_sweep_apply · ${applied.length} applied${dryRun ? ' (dry-run)' : ''}`)
  for (const p of applied) console.log(`  applied: ${p}`)
  if (outOfSandbox.length > 0) {
    findings = true
    for (const b of outOfSandbox) console.log(`  refused (outside ${SANDBOX_PREFIX}): ${b.path}`)
  }
  if (staleRefused.length > 0) {
    findings = true
    for (const { path, commitIso } of staleRefused) {
      console.log(`  refused (stale: firing ${firingIso} predates ${path}'s last commit ${commitIso}): ${path}`)
    }
  }
  if (noHistoryDisclosed.length > 0) {
    for (const p of noHistoryDisclosed) {
      console.log(`  fail-open (no git history for ${p} yet — applied without a staleness check): ${p}`)
    }
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

    // 3a. Positive (issue #924): a declarative report-path claim with no write verb at all —
    //     "Report target: <path>" — must still bite (exit 1), and must NOT write.
    const reportedNoVerb = 'Report target: .claude/ops/adr-queue.json\n'
    const reportedNoVerbFile = join(dir, 'reported-no-verb.md')
    writeFileSync(reportedNoVerbFile, reportedNoVerb)
    const reportedNoVerbCode = main([reportedNoVerbFile, '--root', dir])
    assert(reportedNoVerbCode === 1, 'a "Report target:" claim with no fenced block must exit 1, even with no write verb present')
    assert(!existsSync(join(dir, '.claude/ops/adr-queue.json')), 'a "Report target:" claim with no fenced block must never write a file')

    // 3b. Negative/reverse control (issue #924): the same declarative phrase, backed by a real
    //     fenced block, must NOT false-positive.
    const reportedBacked = 'Report destination: .claude/ops/plan-b.md\n```.claude/ops/plan-b.md\n{"queue":[]}\n```\n'
    const reportedBackedFile = join(dir, 'reported-backed.md')
    writeFileSync(reportedBackedFile, reportedBacked)
    const reportedBackedCode = main([reportedBackedFile, '--root', dir])
    assert(reportedBackedCode === 0, 'a "Report destination:" claim backed by a real fenced block must not be flagged narrated-but-absent')
    assert(existsSync(join(dir, '.claude/ops/plan-b.md')), 'the backing fenced block must still be written')

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

    // 7. Entry guard under a path containing a space (the plugin's real install path is under
    //    `~/Library/Application Support/...`). `import.meta.url` percent-encodes the space while
    //    process.argv[1] does not, so a string-compare guard was silently false: main() never ran
    //    and the process exited 0 with no output — a no-op indistinguishable from success
    //    (observed 2026-08-16). Copy this script under a spaced dir and run it as a child process.
    const spacedDir = join(dir, 'Application Support', 'scripts')
    mkdirSync(spacedDir, { recursive: true })
    const spacedScript = join(spacedDir, 'chore_sweep_apply.mjs')
    writeFileSync(spacedScript, readFileSync(fileURLToPath(import.meta.url)))
    let spacedOut = ''
    let spacedCode = 0
    try {
      spacedOut = execFileSync(process.execPath, [spacedScript, join(dir, 'does-not-exist.md')], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
    } catch (e) {
      spacedCode = e.status
      spacedOut = String(e.stdout ?? '') + String(e.stderr ?? '')
    }
    assert(spacedCode === 2, `entry guard must fire when the script path contains a space (got exit ${spacedCode}, expected 2 for a missing report file)`)
    assert(spacedOut.length > 0, 'a spaced-path invocation must produce output (a silent exit 0 means the entry guard never ran main())')

    // 8. Staleness guard (#738). Seed a real git repo with a target file, so its last-commit
    //    timestamp is real and comparable.
    const staleRoot = join(dir, 'stale-root')
    mkdirSync(join(staleRoot, '.claude/ops'), { recursive: true })
    execFileSync('git', ['init', '-q'], { cwd: staleRoot })
    execFileSync('git', ['config', 'user.email', 'test@test.invalid'], { cwd: staleRoot })
    execFileSync('git', ['config', 'user.name', 'test'], { cwd: staleRoot })
    writeFileSync(join(staleRoot, '.claude/ops/plan.md'), '{"queue":["already-newer"]}\n')
    execFileSync('git', ['add', '.'], { cwd: staleRoot })
    execFileSync('git', ['commit', '-q', '-m', 'seed newer state'], { cwd: staleRoot })
    const commitIso = execFileSync('git', ['log', '-1', '--format=%cI'], { cwd: staleRoot, encoding: 'utf8' }).trim()
    const commitMs = new Date(commitIso).getTime()

    const captureLog = (fn) => {
      const lines = []
      const orig = console.log
      console.log = (...args) => lines.push(args.join(' '))
      try {
        return { code: fn(), lines }
      } finally {
        console.log = orig
      }
    }

    // 8a. Stale payload: --firing predates the target's last commit → refused (exit 1), the
    //     newer committed content is never overwritten.
    const stalePayload = '```.claude/ops/plan.md\n{"queue":["rolled-back-by-stale-payload"]}\n```\n'
    const stalePayloadFile = join(dir, 'stale-payload.md')
    writeFileSync(stalePayloadFile, stalePayload)
    const staleFiring = new Date(commitMs - 60_000).toISOString()
    const { code: staleCode, lines: staleLines } = captureLog(() =>
      main([stalePayloadFile, '--root', staleRoot, '--firing', staleFiring]),
    )
    assert(staleCode === 1, "a stale payload (firing predates the target's last commit) must exit 1")
    assert(
      readFileSync(join(staleRoot, '.claude/ops/plan.md'), 'utf8').includes('already-newer'),
      'a stale payload must never overwrite the newer committed content',
    )
    assert(staleLines.some((l) => l.includes('refused (stale')), 'a stale refusal must be named by path in stdout')

    // 8b. Fresh payload: --firing postdates the target's last commit → still applies (exit 0).
    const freshFiring = new Date(commitMs + 60_000).toISOString()
    const freshCode = main([stalePayloadFile, '--root', staleRoot, '--firing', freshFiring])
    assert(freshCode === 0, "a fresh payload (firing after the target's last commit) must apply, exit 0")
    assert(
      readFileSync(join(staleRoot, '.claude/ops/plan.md'), 'utf8').includes('rolled-back-by-stale-payload'),
      'a fresh payload must be written once its firing postdates the last commit',
    )

    // 8c. No git history for the target at all: fails OPEN (still applies) and DISCLOSES that in
    //     stdout rather than passing silently.
    const noHistoryPayload = '```.claude/ops/brand-new.md\n{"queue":["first-write"]}\n```\n'
    const noHistoryFile = join(dir, 'no-history-payload.md')
    writeFileSync(noHistoryFile, noHistoryPayload)
    const { code: noHistoryCode, lines: noHistoryLines } = captureLog(() =>
      main([noHistoryFile, '--root', staleRoot, '--firing', freshFiring]),
    )
    assert(noHistoryCode === 0, 'a target with no git history must fail open (apply), exit 0')
    assert(
      existsSync(join(staleRoot, '.claude/ops/brand-new.md')),
      'a no-history target must still be written (fail-open, not refused)',
    )
    assert(
      noHistoryLines.some((l) => l.includes('fail-open') && l.includes('no git history')),
      'a no-history target must disclose the fail-open case by name in stdout, never pass silently',
    )
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }

  if (failures > 0) {
    console.log(`chore_sweep_apply selftest · FAIL · ${failures} failing assertion(s)`)
    return 1
  }
  console.log(
    'chore_sweep_apply selftest · PASS · apply/narrated-but-absent/reverse-control/report-phrase-narrated/report-phrase-backed/sandbox-refusal/usage/spaced-path-entry-guard/staleness-guard all correct',
  )
  return 0
}

// Entry guard: compare REAL filesystem paths, not URL strings. `import.meta.url` percent-encodes
// characters like the space in `~/Library/Application Support/...` while process.argv[1] does not,
// so a `file://${process.argv[1]}` string-compare is silently false under such an install path;
// and Node resolves the module URL through symlinks (macOS `/var` → `/private/var`) while argv[1]
// is whatever the caller typed, so both sides go through realpath before comparing.
function isEntryModule() {
  if (!process.argv[1]) return false
  try {
    return realpathSync(fileURLToPath(import.meta.url)) === realpathSync(resolve(process.argv[1]))
  } catch {
    return false
  }
}
if (isEntryModule()) {
  process.exit(main(process.argv.slice(2)))
}
