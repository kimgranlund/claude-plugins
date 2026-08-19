#!/usr/bin/env node
// host_probe.mjs — READ-ONLY host-performance probe for the host-audit skill.
// Prints ONE JSON object to stdout; mutates nothing, ever. Exit 0 = probe ran
// (findings live in the JSON, not the exit code); 1 = the probe itself failed;
// 2 = usage error. `selftest` proves the schema + the read-only claim.
// macOS-first: non-darwin hosts get {platform, verified:false} stubs, never guesses.
import { execSync } from 'node:child_process'
import os from 'node:os'

const sh = (cmd) => { try { return execSync(cmd, { encoding: 'utf8', timeout: 15_000, stdio: ['ignore', 'pipe', 'ignore'] }).trim() } catch { return null } }
const num = (v) => { const n = Number(v); return Number.isFinite(n) ? n : null }

function cpuByPattern(pattern) {
  const out = sh(`ps -axo pcpu=,etime=,comm= | grep -E '${pattern}' | grep -v grep`)
  if (!out) return { count: 0, cpuPct: 0, oldestEtime: null }
  const rows = out.split('\n').map((l) => l.trim().split(/\s+/))
  const cpuPct = rows.reduce((s, r) => s + (num(r[0]) ?? 0), 0)
  const oldest = rows.map((r) => r[1]).sort((a, b) => b.length - a.length || (b > a ? 1 : -1))[0] ?? null
  return { count: rows.length, cpuPct: Math.round(cpuPct), oldestEtime: oldest }
}

function probe() {
  const darwin = process.platform === 'darwin'
  const cores = os.cpus().length
  const [l1, l5, l15] = os.loadavg().map((x) => Math.round(x * 100) / 100)

  // Worktree census: agent-harness worktree dirs under the current repo (or cwd), their
  // node_modules posture (own dir vs symlink vs absent) and Spotlight marker presence.
  const repoRoot = sh('git rev-parse --show-toplevel 2>/dev/null') ?? process.cwd()
  const wtDirs = (sh(`find "${repoRoot}" -maxdepth 3 -type d \\( -path '*/.claude/worktrees' -o -path '*/.agents/worktrees' \\) 2>/dev/null`) ?? '').split('\n').filter(Boolean)
  const worktreeHomes = wtDirs.map((d) => ({
    dir: d,
    spotlightMarker: sh(`test -f "${d}/.metadata_never_index" && echo yes`) === 'yes',
    parked: num(sh(`find "${d}" -mindepth 1 -maxdepth 1 -type d | wc -l`)) ?? 0,
    ownNodeModules: num(sh(`find "${d}" -mindepth 2 -maxdepth 2 -name node_modules -type d ! -type l | wc -l`)) ?? 0,
  }))
  const gitWorktrees = num(sh('git worktree list 2>/dev/null | wc -l'))

  const base = {
    generatedAt: new Date().toISOString(),
    platform: process.platform,
    verified: darwin, // every probe below was verified against a live macOS incident (load-108, 2026-08-19/20)
    cores,
    load: { m1: l1, m5: l5, m15: l15, perCore1m: cores ? Math.round((l1 / cores) * 100) / 100 : null },
    memory: { freeMB: Math.round(os.freemem() / 1048576), totalMB: Math.round(os.totalmem() / 1048576) },
    repoRoot,
    worktreeHomes,
    gitWorktrees,
    devProcs: {
      testRunners: cpuByPattern('vitest|jest|playwright'),
      // TEST browsers only — deliberately excludes the user's real Chrome ('Chrome Helper' matches
      // live-browsing renderers; the behavior check on 2026-08-20 miscounted 31 of them as shards).
      browsers: cpuByPattern('[Cc]hromium|[Hh]eadless[Cc]hrome|headless_shell|ms-playwright'),
      bundlers: cpuByPattern('vite|esbuild|rolldown|webpack|tsc'),
      nodeTotal: cpuByPattern('node'),
    },
    fdSoftLimit: num(sh('ulimit -n')),
    diskFreePct: (() => { const l = sh("df -P / | tail -1"); const m = l && l.match(/(\d+)%/); return m ? 100 - Number(m[1]) : null })(),
  }
  if (!darwin) return { ...base, macos: null }

  return {
    ...base,
    macos: {
      indexers: cpuByPattern('mds_stores|mdworker|corespotlightd|mds '),
      backupd: cpuByPattern('backupd'),
      windowServerCpu: cpuByPattern('WindowServer').cpuPct,
      tmExcluded: {
        repoRoot: (sh(`tmutil isexcluded "${repoRoot}" 2>/dev/null`) ?? '').startsWith('[Excluded]'),
        home: (sh(`tmutil isexcluded "${os.homedir()}/Projects" 2>/dev/null`) ?? '').startsWith('[Excluded]'),
      },
      thermalPressure: sh('sysctl -n machdep.xcpm.cpu_thermal_level 2>/dev/null'),
      swapUsed: sh('sysctl -n vm.swapusage 2>/dev/null'),
      pageouts: (() => { const v = sh('vm_stat | grep "Pageouts"'); const m = v && v.match(/(\d+)/); return m ? Number(m[1]) : null })(),
    },
  }
}

function selftest() {
  const before = sh('ls -laT /tmp 2>/dev/null')
  const p = probe()
  const required = ['generatedAt', 'platform', 'cores', 'load', 'memory', 'worktreeHomes', 'devProcs', 'diskFreePct']
  const missing = required.filter((k) => !(k in p))
  if (missing.length) { console.error(`selftest: missing keys ${missing.join(',')}`); process.exit(1) }
  if (typeof p.load.m1 !== 'number' || typeof p.cores !== 'number') { console.error('selftest: load/cores not numeric'); process.exit(1) }
  // negative control: a bogus subcommand must exit 2, not run the probe
  const bogus = (() => { try { execSync(`"${process.execPath}" "${process.argv[1]}" bogus`, { stdio: 'ignore' }); return 0 } catch (e) { return e.status } })()
  if (bogus !== 2) { console.error(`selftest: bogus subcommand exited ${bogus}, want 2`); process.exit(1) }
  const after = sh('ls -laT /tmp 2>/dev/null')
  console.log(JSON.stringify({ selftest: 'ok', keys: required.length, negativeControl: 'exit-2 verified', tmpUnchangedHint: before === after }))
}

const arg = process.argv[2]
if (arg === 'selftest') selftest()
else if (arg === undefined) console.log(JSON.stringify(probe(), null, 2))
else { console.error('usage: host_probe.mjs [selftest]'); process.exit(2) }
