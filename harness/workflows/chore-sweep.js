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

// The Workflow tool's own loader extracts the `meta` literal above, then runs everything below
// it as the BODY of an async function it supplies itself — top-level `await`, `return`, and the
// phase()/log()/agent()/parallel()/args globals all come from that wrapper, not from anything
// this file declares. A second file-level `export` after `meta` (this file previously closed
// with `export default await runSweep()`) is invalid syntax inside that function body — that is
// exactly what produced the live "Unexpected keyword 'export'" failure (#529). Confirmed against
// a real prior Workflow run captured on this machine (a code-review-wf_*.js instance) that uses
// this same bare-body, single-export shape with top-level `return`. The earlier
// "stay standards-parseable for G11 eslint" constraint this file cited doesn't bind here either:
// eslint.config.mjs only targets `**/scripts/*.mjs|js`, never `**/workflows/*.js`.

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

phase('Sweep')
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

log(`Sweep done: ${returned.length} seat report(s), ${unmeasured.length} unmeasured`)

let plannerReport = null
if (returned.length > 0) {
  phase('Plan')
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
