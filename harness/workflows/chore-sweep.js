export const meta = {
  name: 'chore-sweep',
  description:
    'Fan out the ops-family sweep seats (decision-watcher / issue-sorter / repo-cleaner) in parallel, then hand their reports to chore-planner for one prioritized queue — the deterministic choreography chore-lead (retired, issue #266) used to run as a model-in-the-loop coordinator. #265 measured that chain at 1.92x output tokens / 3.6x wall-clock vs. solo for equivalent outcome quality on a quiet estate.',
  whenToUse:
    'Invoked by /sweep-chores (harness) or /mobilize-chores (teamwork) when the Workflow tool is available in the invoking session. Requires args {scope: ["decision-watcher","issue-sorter","repo-cleaner"]} (a subset is legal). This script has no filesystem access — applying any fenced, target-pathed payload block a seat or chore-planner returns stays the invoking session\'s own job (ops-write-sandbox-rules), same as chore-lead always did it; the invoking session runs scripts/chore_sweep_apply.mjs against the returned report text.',
  phases: [
    { title: 'Sweep', detail: 'one agent per in-scope seat, all independent, barrier-waited' },
    { title: 'Plan', detail: 'chore-planner reads every seat report and returns one prioritized queue' },
  ],
}

const KNOWN_SEATS = ['decision-watcher', 'issue-sorter', 'repo-cleaner']

const SEAT_PROMPT = {
  'decision-watcher':
    'Run your standing per-firing procedure now (watch-adrs) — one bounded ADR-checkpoint sweep. Return your report exactly as you always have: prose findings plus any fenced, target-pathed payload block for computed .claude/ops/ state (ops-write-sandbox-rules) — you still carry no Write tool, nothing here changes that contract.',
  'issue-sorter':
    'Run your standing per-firing procedure now (watch-tickets) — one bounded intake/triage sweep. Return your report exactly as you always have: prose findings plus any fenced, target-pathed payload block for computed .claude/ops/ state (ops-write-sandbox-rules) — you still carry no Write tool, nothing here changes that contract.',
  'repo-cleaner':
    'Run your standing per-firing procedure now (clean-git) — one bounded repo-hygiene sweep. Return your report exactly as you always have: prose findings plus any fenced, target-pathed payload block for computed .claude/ops/ state (ops-write-sandbox-rules) — you still carry no Write tool, nothing here changes that contract.',
}

// Top-level `return` is not valid standard JS/ESM — the two real cited Workflow-script instances
// use it, which means the platform's own loader must wrap a file's body some non-standard way
// before executing it. This file instead stays standards-parseable (this repo's own G11 eslint
// gate has to pass it) and hands its result back via `export default` from an awaited async
// function — unverified against the live Workflow tool same as the rest of this path; adjust the
// export shape once a live run proves what the loader actually reads.
async function runSweep() {
  // `args` may arrive as the caller's raw JSON string rather than the parsed object, depending on
  // the invoking runtime; normalize so both work (same defensive parse the marketplace
  // code-modernization plugin's portfolio-assess.js workflow uses).
  const ARGS = typeof args === 'string' ? (() => { try { return JSON.parse(args) } catch (e) { return args } })() : args

  const requestedScope = ARGS && Array.isArray(ARGS.scope) && ARGS.scope.length > 0 ? ARGS.scope : KNOWN_SEATS
  const scope = requestedScope.filter((s) => KNOWN_SEATS.includes(s))
  const unrecognized = requestedScope.filter((s) => !KNOWN_SEATS.includes(s))
  if (scope.length === 0) {
    throw new Error(
      `chore-sweep workflow requires at least one known seat in args.scope (decision-watcher | issue-sorter | repo-cleaner) — got ${JSON.stringify(requestedScope)}`,
    )
  }

  const seatResults = await parallel(
    scope.map((seat) => () =>
      agent(SEAT_PROMPT[seat], { agentType: `harness:${seat}`, label: `seat:${seat}` }).then((report) => ({
        seat,
        report: report || null,
      })),
    ),
  )

  const returned = seatResults.filter((r) => r && r.report)
  const unmeasured = seatResults
    .filter((r) => !r || !r.report)
    .map((r) => r.seat)
    .concat(unrecognized.map((s) => `${s} (unrecognized seat name — valid menu: ${KNOWN_SEATS.join(', ')})`))

  let plannerReport = null
  if (returned.length > 0) {
    const bundle = returned.map(({ seat, report }) => `## ${seat}\n\n${report}`).join('\n\n---\n\n')
    plannerReport = await agent(
      `The following are this sweep's seat reports, verbatim — judge exactly these, refetch nothing. Produce ONE rewritten .claude/ops/plan.md exactly per your own contract (compute-only — return it as a fenced, target-pathed block, never write it yourself). Name every UNMEASURED seat in the plan itself: ${JSON.stringify(unmeasured)}.\n\n${bundle}`,
      { agentType: 'harness:chore-planner', label: 'planner' },
    )
  }

  return {
    scope,
    seatReports: Object.fromEntries(returned.map(({ seat, report }) => [seat, report])),
    unmeasured,
    plannerReport,
  }
}

export default await runSweep()
