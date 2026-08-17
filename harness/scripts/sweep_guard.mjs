#!/usr/bin/env node
/**
 * sweep_guard.mjs — dispatch-time concurrency guard for sweep-chores.
 *
 * A second sweep-chores firing that starts while an earlier one is still fanning out its seats
 * duplicates the fan-out and can fully pre-empt the first firing's seats (observed live,
 * 2026-08-16T18:45Z vs. 18:55Z — decision-watcher pre-empted; a sync_main quarantine near-miss on
 * the same day showed the same race one step from corrupting `.claude/ops/` state). This script
 * is the mechanized check: a marker file at `<root>/.claude/ops/sweep-in-flight.json` holding the
 * firing's start timestamp and pid/session id.
 *
 * Usage: sweep_guard.mjs check [--root <repo-root>] [--stale-minutes <n>]
 *          Exit 0 clear to sweep (no marker, or a stale one — the stale marker is deleted here so
 *          the caller's subsequent `start` cannot collide with it). Exit 1 a fresh marker exists
 *          (payload printed to stdout as JSON) — decline the sweep, do not fan out.
 *        sweep_guard.mjs start --session <id> [--root <repo-root>]
 *          Writes the marker. Exit 0 always (assumes `check` already gated this call).
 *        sweep_guard.mjs end [--root <repo-root>]
 *          Removes the marker. Exit 0 whether or not one existed (end is idempotent — a sweep
 *          that never got a marker, e.g. `check` declined it, must not fail its own cleanup).
 *        sweep_guard.mjs selftest
 *
 * Default staleness window: 30 minutes (a crashed sweep must not deadlock every sweep after it).
 * Exit codes: 0 clear/success · 1 in-flight (check only) · 2 usage error.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync, mkdtempSync, realpathSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const MARKER_REL = '.claude/ops/sweep-in-flight.json'
const DEFAULT_STALE_MINUTES = 30

function markerPath(root) {
  return join(root, MARKER_REL)
}

/** Returns { state: 'clear' | 'fresh' | 'stale', marker } — never throws on a missing/bad file. */
export function readMarker(root, staleMinutes) {
  const p = markerPath(root)
  if (!existsSync(p)) return { state: 'clear', marker: null }
  let marker
  try {
    marker = JSON.parse(readFileSync(p, 'utf8'))
  } catch {
    return { state: 'stale', marker: null } // unparseable marker is always treated as stale
  }
  const startedAt = Date.parse(marker.startedAt ?? '')
  if (Number.isNaN(startedAt)) return { state: 'stale', marker }
  const ageMinutes = (Date.now() - startedAt) / 60000
  return { state: ageMinutes < staleMinutes ? 'fresh' : 'stale', marker }
}

function usage() {
  console.log(
    [
      'Usage: sweep_guard.mjs check [--root <dir>] [--stale-minutes <n>]',
      '       sweep_guard.mjs start --session <id> [--root <dir>]',
      '       sweep_guard.mjs end [--root <dir>]',
      '       sweep_guard.mjs selftest',
      '',
      'check: exit 0 clear-to-sweep (stale marker removed), exit 1 fresh marker in flight.',
      'start: writes the marker. end: removes it (idempotent). selftest: inline fixtures.',
    ].join('\n'),
  )
}

function parseFlags(argv) {
  let root = process.cwd()
  let staleMinutes = DEFAULT_STALE_MINUTES
  let session = null
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--root') root = resolve(argv[++i] ?? '.')
    else if (argv[i] === '--stale-minutes') staleMinutes = Number(argv[++i])
    else if (argv[i] === '--session') session = argv[++i]
    else {
      console.error(`Unknown flag: ${argv[i]}`)
      return null
    }
  }
  if (Number.isNaN(staleMinutes) || staleMinutes <= 0) {
    console.error('--stale-minutes must be a positive number')
    return null
  }
  return { root, staleMinutes, session }
}

function cmdCheck(argv) {
  const flags = parseFlags(argv)
  if (!flags) return 2
  const { root, staleMinutes } = flags
  const { state, marker } = readMarker(root, staleMinutes)
  if (state === 'clear') {
    console.log('sweep_guard · clear · no marker present')
    return 0
  }
  if (state === 'fresh') {
    console.log(`sweep_guard · IN-FLIGHT · ${JSON.stringify(marker)}`)
    return 1
  }
  // stale — override it now so the caller's subsequent `start` never collides with it, and note
  // that a crashed sweep left it behind (never a silent overwrite).
  rmSync(markerPath(root), { force: true })
  console.log(`sweep_guard · clear · stale marker overridden (crashed or abandoned sweep): ${JSON.stringify(marker)}`)
  return 0
}

function cmdStart(argv) {
  const flags = parseFlags(argv)
  if (!flags) return 2
  const { root, session } = flags
  if (!session) {
    console.error('start requires --session <id>')
    return 2
  }
  const p = markerPath(root)
  mkdirSync(dirname(p), { recursive: true })
  writeFileSync(p, JSON.stringify({ startedAt: new Date().toISOString(), pid: process.pid, session }, null, 2) + '\n')
  console.log(`sweep_guard · marker written · ${p}`)
  return 0
}

function cmdEnd(argv) {
  const flags = parseFlags(argv)
  if (!flags) return 2
  rmSync(markerPath(flags.root), { force: true })
  console.log('sweep_guard · marker removed (or already absent)')
  return 0
}

function main(argv) {
  const [cmd, ...rest] = argv
  if (cmd === 'selftest') return selftest()
  if (cmd === 'check') return cmdCheck(rest)
  if (cmd === 'start') return cmdStart(rest)
  if (cmd === 'end') return cmdEnd(rest)
  usage()
  return 2
}

function selftest() {
  const dir = mkdtempSync(join(tmpdir(), 'sweep-guard-'))
  let failures = 0
  const assert = (cond, msg) => {
    if (!cond) {
      failures++
      console.error(`FAIL: ${msg}`)
    }
  }

  try {
    // 1. Positive: no marker → check is clear, exit 0.
    assert(main(['check', '--root', dir]) === 0, 'no marker must be clear (exit 0)')

    // 2. start writes a marker; a subsequent check within the staleness window is exit 1.
    assert(main(['start', '--root', dir, '--session', 'sess-a']) === 0, 'start must exit 0')
    assert(existsSync(join(dir, MARKER_REL)), 'start must write the marker file')
    assert(main(['check', '--root', dir]) === 1, 'a fresh marker must decline a second firing (exit 1)')

    // 3. Negative control: a marker older than the staleness window is overridden, not honored.
    writeFileSync(
      join(dir, MARKER_REL),
      JSON.stringify({ startedAt: new Date(Date.now() - 45 * 60000).toISOString(), pid: 1, session: 'crashed' }, null, 2),
    )
    assert(main(['check', '--root', dir, '--stale-minutes', '30']) === 0, 'a marker older than the staleness window must be overridden (exit 0)')
    assert(!existsSync(join(dir, MARKER_REL)), 'an overridden stale marker must actually be removed')

    // 4. end is idempotent: removing an absent marker still exits 0.
    assert(main(['end', '--root', dir]) === 0, 'end on an absent marker must exit 0 (idempotent)')

    // 5. Reverse control: a marker inside the staleness window (just under it) stays fresh.
    main(['start', '--root', dir, '--session', 'sess-b'])
    const nearFreshPath = join(dir, MARKER_REL)
    writeFileSync(nearFreshPath, JSON.stringify({ startedAt: new Date(Date.now() - 5 * 60000).toISOString(), pid: 2, session: 'sess-b' }))
    assert(main(['check', '--root', dir, '--stale-minutes', '30']) === 1, 'a marker well inside the staleness window must still be in-flight (exit 1)')
    assert(main(['end', '--root', dir]) === 0, 'end must remove a fresh marker too')
    assert(!existsSync(nearFreshPath), 'end must actually delete the marker file')

    // 6. Usage errors: unknown flag, missing --session, bad --stale-minutes, unknown command.
    assert(main(['check', '--root', dir, '--bogus']) === 2, 'an unknown flag must exit 2')
    assert(main(['start', '--root', dir]) === 2, 'start with no --session must exit 2')
    assert(main(['check', '--root', dir, '--stale-minutes', 'nope']) === 2, 'a non-numeric --stale-minutes must exit 2')
    assert(main(['bogus-command']) === 2, 'an unknown command must exit 2')
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }

  if (failures > 0) {
    console.log(`sweep_guard selftest · FAIL · ${failures} failing assertion(s)`)
    return 1
  }
  console.log('sweep_guard selftest · PASS · clear/fresh/stale-override/idempotent-end/reverse-control/usage all correct')
  return 0
}

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
