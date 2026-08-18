---
doc-type: lld
id: lld-0010-backlog-roadmap-system
status: draft
version: 0.1.1
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#611
spec: none
---
# LLD — Backlog + roadmap system: labels, sweep immunity, de-staling pickup, releases-loop homes (#611)

**No SPEC/PRD/ADR** (doc-checker finding 5, frontmatter is machine-read — rationale moved here,
out of the field): acceptance is verbatim in #611's own Acceptance section and restated here as
checkable predicates (D2); no requirement was ambiguous enough to need sign-off before build, so a
standalone SPEC would be manufactured process (doc-writing-rules' own routing test). No PRD (the
why/what is #611 + the brief's releases-loop line) and no ADR (all forks here were already
resolved by Kim's 2026-08-18 find-intent ruling; the two open items this LLD closes are recorded
below with rationale, and neither is hard-to-reverse — non-decisions in Risks R7; RA5 restates
this in Rejected Alternatives).

**Verdict, head-first.** Two new labels — `backlog` (`#D4C5F9`) and `roadmap` (`#BFDADC`) — make
an Issue PARKED. Parked means: invisible to all three board-clearing surfaces (mobilize-chores
discovery, chore-planner queueing, issue-sorter/watch-tickets triage) unless a dispatch names the
id explicitly — naming IS the pickup. Pickup of a parked ticket pays one new stage in
dispatch-ticket (**Phase 3.5 — de-stale**): re-verify the ticket's own stated premises against
live repo state before Phase 4's sizing; a positively falsified premise returns a **fourth typed
outcome, `stale-premise`** (with evidence, claim released), never a build. The releases-loop homes
are minted: the ROADMAP index at `.claude/docs/roadmap/roadmap-nonoun-plugins.md` with real
Now/Next/Later content, and the RDD↔Issue binding ruled as **plain prose citations in the RDD's
`## Sequencing`** (the template's own TICKET precedent), recorded in docs' `doc-writing-rules`.
The brief's 2026-08-16 deferral is amended append-style (existing wording untouched). Three
plugins bump: teamwork 2.23.1→2.24.0, harness 3.9.7→3.10.0, docs 1.17.0→1.18.0. **No first RDD
instance is minted** — the acceptance bar is types-lint-clean + index + binding mechanics, and an
RDD with nothing in Now would fail its own template admission test.

The two open decisions #611 left, now closed:

1. **RDD↔Issue binding = prose citation in `## Sequencing`, never a frontmatter field.** The rdd
   template already rules "TICKET is a work item, not an ID-spine citee, so this stays outside
   `decision-refs:`" — a `roadmap`-labeled GitHub Issue is exactly a work item on this workspace's
   backend (ADR-0002), so it takes the identical treatment: one plain `Tracked at
   <owner>/<repo>#NNN` line per bundled Issue inside `## Sequencing`. Rationale: the ID spine
   (`decision-refs:`) cites immutable in-repo ledger records only; issue ids are backend-scoped
   and mutable (a backend migration renumbers them, a frontmatter field would then be a forged-
   looking edit on a locked ledger doc), and a new frontmatter key would also need new
   `doc_lint.py` parsing/T-check surface for zero added machine value — nothing consumes the edge
   mechanically today. The decision is written down permanently in TWO homes (C7): one clause in
   `doc-writing-rules` SKILL.md's RDD section (the canonical standard) and one sentence in the rdd
   template's `## Sequencing` comment (where an author's eyes actually are).
2. **ROADMAP index = `.claude/docs/roadmap/roadmap-nonoun-plugins.md`**, per this workspace's
   docs-root override (CLAUDE.md, issue #514: everything under `.claude/docs/`, matching the
   sibling `brief/brief-nonoun-plugins.md` naming). Initial content is REAL living state (C6):
   Now honestly empty (the brief's own deferral confirms no release-grain commitment is locked —
   nothing in flight at release grain), Next carries the two ratified roster-growth migrations
   from the brief's Confirmed section, Later carries two evidenced standing intents (Linear
   adapter activation; the deferred decision-watcher RDD escalation).

## Components

### C1 — Labels: `backlog` and `roadmap` (registry act, one-time)

**Correction (build-time re-verification, 2026-08-17):** both labels already existed in the live
registry before this build (minted by an earlier dispatch in this same build session) — `backlog`
at `#D4C5F9` ("board-clearing immunity: excluded from sweep/queue/triage unless ticket-filtered")
and `roadmap` at `#BFDADC` ("releases-loop item: same board-clearing immunity as backlog;
RDD-bound work tracked here"). Per the read-and-correct discipline (registry state is ground
truth over a planning-time sketch), the builder did NOT run the creates below or recolor/redescribe
either label — this section is corrected in place to the actual live values; the sketch is kept
for provenance:

```
gh label create backlog --color 6A737D \
  --description "parked work item — sweep/queue/triage-immune; picked up only by explicit id (#611)"
gh label create roadmap --color 0052CC \
  --description "release-grain item bound to an RDD — sweep-immune; the roadmap index tracks it (#611)"
```

Colors verified fresh against the live registry (2026-08-18, `gh label list`): the planning-time
sketch (`6A737D`/`0052CC`) did not collide with any existing label at authoring time, and neither
reuses `in-flight`/`doing`'s `FBCA04` or `queued`'s `C5DEF5`; the ACTUAL minted colors
(`D4C5F9`/`BFDADC`) likewise collide with nothing. Semantics: `backlog` = parked, no release-grain commitment implied;
`roadmap` = parked AND bound to (a future) RDD via C7's citation. Both labels carry identical
immunity/de-staling behavior everywhere below — the distinction is purely what the item means,
never how machinery treats it. The durable canon for what the labels mean lives in the prose that
consumes them (C2/C4/C5) plus the ROADMAP index's header comment (C6) — no separate registry doc.

### C2 — teamwork/skills/mobilize-chores/SKILL.md: sweep immunity + relay vocabulary

1. **Frontmatter `description`** — after the `Blocked-by:` clause, add: "— and never a ticket
   parked under a `backlog` or `roadmap` label (#611): parked ids are invisible to a sweep; a
   ticket-id list naming one explicitly still mobilizes it (naming IS the pickup)". Decision,
   recorded: mobilize-chores is `disable-model-invocation: true`, so **no evals.json exists or is
   owed** for this description edit (the plugin-authoring rule binds model-invocable routing
   surfaces; this description is human documentation for `/mobilize-chores`) — and `/check-routing
   teamwork` **still runs at build** as the cheap boundary-regression proof, the exact lld-0007 C3
   precedent, not because it is owed.
2. **Step 2, the backend-generic predicate paragraph** ("Regardless of backend, a ticket is
   mobilizable only if: …") gains a FIFTH conjunct alongside label-exactness, no-claim, no-open-PR
   and no-open-`Blocked-by:` (doc-checker finding 2: that's four existing conjuncts, so the
   addition is the fifth, not the fourth): "AND carries neither parking label — `backlog`/`roadmap` (#611;
   git-native: the `labels` array already fetched by this step's `--json` calls, a post-filter
   costing zero new `gh` calls; local/adapter backends: no parking realization defined yet —
   disclosed in the step-6 report as N/A, never silently assumed)."
3. **Step 2, the TICKET FILTER sentence** ("Every other exclusion below … still applies to each
   named id") gains the exception carve-out: "— with ONE deliberate exception (#611): the
   `backlog`/`roadmap` parking exclusion does NOT apply to a filter-named id. Naming a parked id
   explicitly is exactly how parked work gets picked up; every other check (label ambiguity,
   claim, in-flight PR, `Blocked-by:`) still runs on it, and its pickup pays `dispatch-ticket`'s
   Phase 3.5 de-stale before any build." SWEEP SCOPE discovery is where the exclusion bites;
   the filter path's behavior on a parked id is the exception clause, working by design.
4. **Step 5 relay list** — the typed results relayed from `build-lead` gain the fourth class:
   "(path/URL, status, what shipped, a recorded blocker, a SKIPPED gap, or a `stale-premise`
   report with its evidence, #611)".
5. **Step 6 vocabulary** — the skipped-and-why enumeration gains "parked (`backlog`/`roadmap`
   label, #611 — only reachable via a stale hand-check, since SWEEP discovery never lists parked
   ids; named here so a boundary case is observable, not invisible)", and the outcome table
   admits `stale-premise` as a relayed `build-lead` outcome distinct from SKIPPED and from a named
   blocker (it gets a one-line evidence summary in the table, no breakdown paragraph — nothing is
   blocking it; the ticket itself is wrong, and the evidence already sits on the record).
6. **Done-when / NOT-done** — NOT-done gains: "a parked (`backlog`/`roadmap`-labeled) ticket is
   mobilized from a SWEEP SCOPE (a TICKET FILTER naming it explicitly is the one legitimate
   path, #611)".
7. **`references/unstick-ordering.md`, B5 row only** — the parenthetical predicate enumeration
   "(exactly one of feature/bug/task, no active claim, no open PR, not sweep-excluded)" gains
   "not parked (#611)". Surfaced by this design's coverage check: without it, a chain whose
   blocker is parked would let the enumerated shorthand contradict step 2's predicate it claims
   to cite. A parked blocker therefore classifies B4-adjacent (not mobilizable → still-stuck),
   which is correct: parking is a deliberate human shelving, and un-shelving via a chain side
   door would defeat the label.

### C3 — harness/agents/chore-planner.md: queueing immunity (body-only)

One new paragraph after the evidence-precedence paragraph ("Evidence, in precedence order: …"):

> A `backlog`/`roadmap`-labeled issue is parked strategy state, never ops debt (#611): standalone
> live-`gh` evidence excludes both labels at read time, and prior-plan carry-forward DROPS an
> entry whose id now carries either label — one "dropped: parked #NN" note in the rewritten plan,
> never a silent vanish — unless the dispatch's focus instruction names that id explicitly, which
> un-parks it for this dispatch only (still an attention scope, never a new entry contract).

Decision, recorded per the dispatch's own question: the `description:` frontmatter **does not
change**. It says "reads durable ops state plus live `gh` evidence directly" — which evidence a
seat reads is internal procedure, not a routing boundary; adding an exclusion filter alters no
when-to-dispatch semantics. Therefore no `/check-routing harness` is owed for this file (agent
files carry no evals in this estate regardless), and the edit is a body-only semantic change
riding one `harness:agent-checker` pass (D2 slice 8). Sweep-mode (attached seat reports) needs no
clause: the planner judges exactly the reports it was handed, and the upstream seats (C2/C4) now
exclude parked items at their own source.

### C4 — harness/skills/watch-tickets/SKILL.md: triage immunity (body-only)

**Step 1** gains, after the existing discovery sentence:

> Discovery excludes parked items (#611): append `-label:backlog -label:roadmap` to each
> `gh issue list --search` query, so a parked item edited while parked never re-enters triage on
> its own (`gh pr list` is untouched — parking is an Issue concept). The exception takes the same
> already-made-decision shape as an approve/deny dispatch (this seat's existing held-item
> pattern): a dispatch that names a specific item id explicitly processes that item regardless of
> parking labels — read it directly (`gh issue view <id>`) instead of relying on the search
> window. No new ticket-filter concept is added; an explicit id in the dispatch prompt is the
> whole mechanism.

Decisions, recorded: (a) issue-sorter gets **no new ticket-filter machinery** — the "dispatch
names the id" realization already exists in this seat's grammar (the approve/deny `<example>` in
`agents/issue-sorter.md` is a dispatch executing an already-made human decision; naming a parked
id is the same shape), so the exception is one sentence, not a new concept; (b) the
`description:` frontmatter **does not change** (it describes discover/classify/trust/mint at the
routing grain; a discovery filter is internal procedure), therefore
`harness/skills/watch-tickets/evals/evals.json` is **structurally untouched** — verified present,
and deliberately not edited; (c) `agents/issue-sorter.md` itself is **not touched at all** (it is
thin by design; the procedure lives here), so no `agent-checker` pass is owed for it — the
body-only semantic edit to THIS file rides one `harness:skill-checker` pass (D2 slice 8).

### C5 — teamwork/skills/dispatch-ticket/SKILL.md: Phase 3.5, the de-stale stage

**Insertion: a new `## Phase 3.5 — De-stale a parked ticket (backlog/roadmap labels only)`
heading between Phase 3 and Phase 4.** Decision, recorded: fractional numbering, never
renumbering — "Phase 4"/"Phase 5"/"stage 2b" are load-bearing cross-references inside this file
and from other files (mobilize-chores steps 2/5 cite Phase 3/Phase 4/stage 2b verbatim;
`build-leader`'s contract carries Phase 5's stage names) — a renumber would be a blast-radius
campaign for zero semantic gain. Placement AFTER Phase 3 (claim already taken) is deliberate:
the premise re-check is real effort that should run under a won claim so two concurrent pickups
never both re-analyze, and a stale exit then exercises the existing release machinery instead of
needing a pre-claim special case.

New phase body (buildable sketch — the builder lands this substantively verbatim):

> Runs on the feature path between Phase 3 and Phase 4's sizing, and on the task path between
> Phase 3 and the Agent dispatch — Phase 2's task branch gains "then Phase 3.5" inserted verbatim
> into its exact sentence (doc-checker finding 3, quoted precisely so the builder greps the right
> anchor): "Otherwise run Phase 3 (claim, then isolate) first, then dispatch via the `Agent` tool"
> becomes "…first, then Phase 3.5, then dispatch via the `Agent` tool". **Trigger:** the record carries the `backlog` or `roadmap` label (#611;
> git-native: the labels Phase 1 already read; file backend: no parking realization defined —
> stage N/A, disclosed). Label absent → **this phase does not exist**: skip silently, continue —
> the same absent-field shape as stage 2b's grant line. The Phase 2 bug hand-off never runs it
> (`file-bug` owns its own record lifecycle; a parked bug's hand-off proceeds unchanged —
> disclosed non-goal).
>
> A parked ticket was written against a repo that has since moved. #583 (`campaign_close.py` C4
> unguarded against branch-name reuse) and #584 (decision-watcher prose-form supersession ruled
> out-of-contract) were both caught only because someone independently re-checked the ticket's
> premise against live state before building. Mechanize that check: enumerate the ticket's own
> load-bearing premises — files/paths it names (do they exist in the described shape: `Read`/
> `Glob`), issues/PRs it references (in the state assumed: `gh issue view`/`gh pr view`),
> current-state claims it makes ("X lacks Y", "Z is unguarded" — still true, checked against the
> live file), records it cites (ADR/IDR/RDD superseded?). Bounded to premises the ticket itself
> states — a premise audit, never a fresh design review and never a re-size.
>
> - **Every premise verified — or unverifiable but uncontradicted** → write ONE dated Findings
>   entry ("de-stale pass: N premises re-verified, M unverifiable (named), proceeding") and
>   continue to Phase 4 exactly as today. Only a POSITIVELY falsified premise stales the ticket;
>   fail-open on the merely-unverifiable, disclosed in the entry (fail-closed would make every
>   parked ticket unbuildable via one ambiguous sentence — the #583/#584 class is positive drift,
>   not ambiguity).
> - **Any premise positively falsified → `stale-premise`**, a fourth typed outcome alongside
>   built / SKIPPED / named blocker: write the evidence as a dated Findings comment (per
>   falsified premise: what the ticket asserts, what live state shows, the command or path that
>   proves it), release the claim per Phase 3's Release-on-abandonment bullet, tear down the
>   worktree per the teardown bullet, and return `stale-premise` carrying the evidence. Never
>   build past a falsified premise; never close, relabel, or rewrite the ticket (re-triage is a
>   human/planner act on the evidence left behind); never report it as SKIPPED (that means
>   under-specified) or as a named blocker (nothing external blocks it — the ticket itself is
>   wrong).

Decision, recorded — **`stale-premise` is a NEW fourth outcome class**, not a reuse: SKIPPED
already means "under-specified, clarify and re-run", a named blocker already means "something
external must move first", and both imply the ticket text is still right. A stale premise demands
a different human act (rewrite or retire the ticket), so overloading either existing class would
hide that in the artifact of record. Cost: one vocabulary entry in this file + C2 items 4–5.

**Three wiring edits in the same file:** (a) Phase 3's Release-on-abandonment bullet's enumerated
post-claim exits gain "a stale-premise exit (Phase 3.5)"; (b) Failure branches gain "Phase 3.5
finds a falsified premise → `stale-premise` is a reported outcome, not a failure: claim released,
evidence on the record, ticket left open for re-triage"; (c) the closing "Done when" clause's
"dated evidence of the shipped work (or the recorded blocker/skip)" becomes "(or the recorded
blocker/skip/stale-premise report)".

### C6 — The ROADMAP index (new file, docs plugin untouched by it — repo-root doc tree)

`.claude/docs/roadmap/roadmap-nonoun-plugins.md` (new dir + file), exact initial content:

```markdown
---
doc-type: roadmap
id: roadmap-nonoun-plugins
status: active
date: 2026-08-18
owner: kim.granlund
review-cadence: monthly
---
# ROADMAP — nonoun-plugins

<!-- Issues carrying the `roadmap` label are release-grain items; each binds to its RDD via that
     RDD's ## Sequencing prose citation ("Tracked at <owner>/<repo>#NNN" — docs:doc-writing-rules,
     RDD section, ruled gh#611). This index is the living completion tracker: releases lock, the
     roadmap breathes. -->

## Now
<!-- Committed, in flight; each item links its PLAN or TICKET. -->
- (empty — no release-grain commitment is locked yet, per the brief's own former deferral; the
  first locked RDD lands here as `rdd-0001 — <commitment>` with its roadmap-labeled issue ids.)

## Next
<!-- Decided direction, undated by design. -->
- `product-management` plugin migration (product-forge fold-in) — deliberate roster growth per the
  brief's Confirmed roster bullet (ratified 2026-08-16); gated by `harness:plan-plugin-split`'s
  anti-matrix rule before minting.
- `brand-design` plugin migration (brand-forge fold-in) — same Confirmed bullet, same anti-matrix
  gate.

## Later
<!-- Intent, explicitly reversible. Items here carry no promises. -->
- Option C (Linear) ticket-backend activation — the shipped adapter spec's discovery/polling
  turn-on (`spec-linear-adapter.md`; watch-tickets' own "until then, discovery is gh-only"
  deferral) plus the adapter listing primitive mobilize-chores discloses as missing.
- decision-watcher cross-corpus RDD escalation ("≥2 superseded RDDs citing the same ADR") — the
  deferred extension doc-writing-rules' RDD section already names out of its own scope.

<!-- LIVING STATE: staleness is a bug. The review cadence is the contract. -->
```

Lint-true by construction: `doc-type: roadmap`, `status: active` (legal enum), `id` present, all
three required sections (`Now`/`Next`/`Later`) present. Every line is mined from a live record
(the brief's Confirmed bullet; watch-tickets' Scope deferral; mobilize-chores' Option C gap;
doc-writing-rules' RDD deferred-extension sentence) — no invented commitments, and Now's
emptiness is stated as a fact with its successor named, not left as a stub.

### C7 — RDD↔Issue binding, written down permanently (docs plugin, two small edits)

1. **`docs/skills/doc-writing-rules/SKILL.md`, RDD section** — one new sentence appended to the
   RDD paragraph (after the "…never the reverse" citation-direction sentence):

   > **RDD↔work-item binding (ruled 2026-08-18, gh#611):** the `roadmap`-labeled Issues an RDD
   > bundles bind in `## Sequencing` as plain prose citations — one `Tracked at
   > <owner>/<repo>#NNN` line per bundled Issue — exactly the template's existing TICKET
   > precedent (work items are backend-scoped and mutable, so they never enter `decision-refs:`,
   > which cites immutable in-repo records only); the reverse edge is the Issue's own `## Links`
   > line naming the RDD id.

2. **`docs/skills/doc-writing-rules/references/templates/rdd.md`**, the `## Sequencing` comment
   gains one sentence: "Roadmap-labeled Issues bind here the same way: a plain `Tracked at
   <owner>/<repo>#NNN` line per bundled Issue (ruled gh#611) — never a frontmatter field."

No first RDD instance is minted (verdict paragraph — acceptance demands the TYPES lint clean and
the index + binding mechanics exist, not a populated instance; an instance with Now empty would
fail the template's own admission test and could not reach `locked` honestly). doc-writing-rules'
`description:` is unchanged → its evals suite is untouched; the body edit rides one
`docs`-side skill-checker pass (D2 slice 8).

### C8 — Brief amendment (repo-root doc, NO plugin version implication)

`.claude/docs/brief/brief-nonoun-plugins.md`, `## Open Questions`: the existing bullet stays
byte-identical; ONE new bullet appends directly after it:

```markdown
- 2026-08-18 (Kim, resolved via find-intent, gh#611): the HOMES half of the line above is lifted —
  the `roadmap` index is minted at `.claude/docs/roadmap/roadmap-nonoun-plugins.md` and the
  RDD↔Issue binding rule is recorded in docs' `doc-writing-rules` (RDD section). The question
  itself stays open in its remaining half: no release-grain commitment is locked yet — the first
  `locked` RDD (which lands in the roadmap's Now) closes this bullet whole.
```

Decision, recorded — placement under **Open Questions, not Confirmed**, deliberately diverging
from idr-0007's Confirmed-bullet placement while copying its append mechanics (dated, names the
ratifying event, cites the record id, never rewords an existing line): idr-0007 ratified a belief,
so Confirmed was its home; here the question is only HALF answered — the homes exist, but "when
does a real release-grain commitment land?" is still genuinely open until a first RDD locks.
Moving the bullet to Confirmed would overstate the state; the dated in-place note keeps the brief
truthful and gives the first-RDD author the exact closing condition.

### C9 — Version bumps + ledgers (three plugins; the brief/roadmap/LLD are repo-root, unversioned)

| Plugin | origin/main (re-verified 2026-08-18, this dispatch) | Bump to | Why minor |
|---|---|---|---|
| teamwork | 2.23.1 | **2.24.0** | new behavior: parked-exclusion + Phase 3.5 + `stale-premise` outcome |
| harness | 3.9.7 | **3.10.0** | new behavior: parked-exclusion in chore-planner + watch-tickets |
| docs | 1.17.0 | **1.18.0** | new standard clause: RDD↔Issue binding rule + template sentence |

Per the VALUE-race discipline (dispatch-ticket Phase 5 stage 2, #445): the builder re-reads each
`plugin.json` off `origin/main` immediately before PR-open and bumps from THAT value — these
numbers are the plan, the re-read is the truth. One README ledger line each, sketched:
teamwork — "2.24.0 — #611 backlog/roadmap parking: mobilize-chores sweep immunity (ticket-filter
exempt), dispatch-ticket Phase 3.5 de-stale + `stale-premise` outcome"; harness — "3.10.0 — #611
parking immunity: chore-planner queueing + watch-tickets discovery exclude `backlog`/`roadmap`
unless a dispatch names the id"; docs — "1.18.0 — #611 RDD↔Issue binding ruled (prose citation in
`## Sequencing`, never frontmatter): doc-writing-rules RDD section + rdd template comment".

## Interfaces

### I1 — The parked-exclusion predicate (one shape, three realizations, one exception each)

Predicate: *labels ∩ {`backlog`, `roadmap`} ≠ ∅ → excluded from discovery/queueing/triage.*
Realizations: mobilize-chores — post-filter on the already-fetched `labels` array (zero new `gh`
calls); chore-planner — exclusion at live-`gh` read time + carry-forward drop with a named note;
watch-tickets — `-label:backlog -label:roadmap` appended to the search query. Exception (one per
surface, same doctrine — explicit naming, never inference): a TICKET FILTER id (mobilize-chores
step 0), a focus instruction naming the id (chore-planner), a dispatch naming the id
(issue-sorter/watch-tickets). Every exception un-parks for THAT run only; the label itself is
never edited by any of the three surfaces.

### I2 — The `stale-premise` outcome (producer → relays → human)

Producer: dispatch-ticket Phase 3.5. Shape: outcome name + per-premise evidence triple (asserted
/ observed / proof command-or-path), mirrored as a dated Findings comment on the record. Relays:
`build-leader` carries it verbatim in its typed return — **resolved (doc-checker finding 1,
2026-08-18): NO edit to `teamwork/agents/build-leader.md`.** Its own charter line is generic by
construction — "relay whatever it reports — result, status, blocker, or redirect — verbatim as
your own final text… This one rule governs every phase and branch below; it is not restated
again" (`agents/build-leader.md`) — a fourth outcome class is exactly a new value of "whatever it
reports," already covered without a literal enumeration edit. `mobilize-chores` step 5/6 name it
as a distinct table class (C2.4–5). Terminal human act: re-triage (rewrite/retire/un-park), never
automated. State side-effects: claim released, `in-flight` removed, worktree torn down, issue
left OPEN.

### I3 — The RDD↔Issue binding edge (C7)

Forward edge: RDD `## Sequencing` → `Tracked at <owner>/<repo>#NNN` prose line per bundled Issue.
Reverse edge: the Issue's `## Links` section names the `rdd-NNNN` id. Completion movement: the
roadmap index's Now/Next/Later lines, never a status flip on the locked RDD ("releases lock, the
roadmap breathes"). Nothing consumes the edge mechanically in v1 — same presence-only posture as
`decision-refs:` v1, upgradeable later without breaking the format.

### I4 — Ticket-filter pickup of a parked id, end to end

`/mobilize-chores "<id>"` → step 0 TICKET FILTER → step 2 reads the id directly, parking
exclusion exempt, all other checks run → confirm/dispatch → `build-lead` → dispatch-ticket Phase
1–3 (claim, isolate) → **Phase 3.5 de-stale** → Phase 4 sizing (premises held) or
`stale-premise` return (falsified). This is the acceptance path D1's F2 fixture drives.

## Data

### D1 — Verification fixtures (payload/API layer, per docs:agent-harness-rules)

- **F1 (immunity):** `gh issue create --title "FIXTURE #611 — immunity probe (do not build)"
  --label task --label backlog --body "Fixture for #611 acceptance. Summary: none. Acceptance:
  this issue is never mobilized from a sweep. Links: #611."` Assertions (each a runnable command):
  - Sweep-discovery probe: `gh issue list --state open --label task --json number,labels --jq
    '[.[] | select(((.labels | map(.name)) | any(. == "backlog" or . == "roadmap")) | not) |
    .number]'` does NOT contain F1 (this is step 2's post-filter, executed literally).
  - Triage probe: `gh issue list --search "-label:backlog -label:roadmap <window>" ` does NOT
    return F1; `gh issue view <F1>` still resolves (the explicit-id path works).
  - Queueing probe: one chore-planner standalone dispatch → returned `plan.md` payload contains
    no F1 entry.
  - Filter-exception probe: a `/mobilize-chores "<F1>"` run CONSIDERS F1 (step-6 table row
    present) — proving the exception clause, not just the exclusion.
- **F2 (de-staling):** `gh issue create` labeled `feature` + `size:small` + `backlog`, body
  premising a file that does not exist (e.g. "harness/scripts/premise_probe_611.py currently
  lacks a selftest — add one"). Drive I4 (`/mobilize-chores "<F2>"` or `/build-feature <F2>`).
  Assertions: returned outcome names `stale-premise`; `gh issue view <F2> --comments` shows a
  dated Findings comment with the asserted/observed/proof evidence; `gh issue view <F2> --json
  assignees,labels` shows empty assignees and no `in-flight`; the issue is still OPEN; no PR was
  opened for it.
- Both fixtures are closed with a "fixture retired, #611 acceptance evidence: <PR link>" comment
  once the PR's evidence section quotes the assertion outputs. **No new script is minted and no
  existing script changes**, so `.claude/rules/scripts.md`'s selftest rule is N/A this build
  (rationale in Rejected alternatives RA4).

### D2 — Build-slice manifest (the plan the builder executes from, in order)

| # | Slice | Files | Depends on |
|---|---|---|---|
| 1 | Mint labels per C1 (record actual `gh label create` output) | GitHub registry only | LLD approved |
| 2 | mobilize-chores edits per C2.1–6 + unstick-ordering B5 per C2.7 | `teamwork/skills/mobilize-chores/SKILL.md`, `teamwork/skills/mobilize-chores/references/unstick-ordering.md` | 1 |
| 3 | dispatch-ticket Phase 3.5 + wiring per C5 | `teamwork/skills/dispatch-ticket/SKILL.md` | 1 |
| 4 | chore-planner paragraph per C3; watch-tickets step-1 edit per C4 | `harness/agents/chore-planner.md`, `harness/skills/watch-tickets/SKILL.md` | 1 |
| 5 | RDD binding clause + template sentence per C7 | `docs/skills/doc-writing-rules/SKILL.md`, `docs/skills/doc-writing-rules/references/templates/rdd.md` | — |
| 6 | ROADMAP index per C6 (new `.claude/docs/roadmap/` dir) | `.claude/docs/roadmap/roadmap-nonoun-plugins.md` | 5 (cites the ruled binding) |
| 7 | Brief amendment per C8 (append-only) | `.claude/docs/brief/brief-nonoun-plugins.md` | 6 |
| 8 | **Checker passes — required, one fresh-context pass per touched prompt-carrying artifact** (`.claude/rules/plugin-authoring.md`): `harness:skill-checker` × 4 — `teamwork/skills/mobilize-chores/SKILL.md`, `teamwork/skills/dispatch-ticket/SKILL.md`, `harness/skills/watch-tickets/SKILL.md`, `docs/skills/doc-writing-rules/SKILL.md` (each pass also covers its skill's edited reference file); `harness:agent-checker` × 1 — `harness/agents/chore-planner.md`. `harness/agents/issue-sorter.md` is untouched → no pass owed (C4c). No model override on checker dispatches (they pin fable·medium themselves) | — | 2–5 |
| 9 | Fixture runs per D1 (F1 four probes, F2 full I4 drive), evidence quoted in the PR | GitHub fixtures | 2–4 |
| 10 | Version bumps + ledger lines per C9 (re-read origin/main values at PR-open, VALUE race) | 3× `plugin.json`, 3× `README.md` | 2–5 |
| 11 | Gates: `release_gate.py` exit 0 for teamwork, harness, docs; `/check-routing teamwork` (C2.1's precedent proof); `doc_lint.py` green on the roadmap index, the amended brief, and this LLD | — | all |

Acceptance predicates (checkable before the PR is called done — #611's bar, mechanized):
- `gh label list` shows `backlog` (`D4C5F9`, actual — corrected from the `6A737D` planning sketch)
  and `roadmap` (`BFDADC`, actual — corrected from the `0052CC` planning sketch).
- F1 survives untouched: all four D1/F1 probes pass, and F1 shows zero assignees and zero
  comments beyond the fixture-retirement comment (doc-checker finding 4: the absolute form,
  never an unfalsifiable attribution to "sweep machinery").
- F2 reports stale-with-evidence instead of building: all five D1/F2 assertions pass.
- `python3 docs/scripts/doc_lint.py .claude/docs/roadmap/roadmap-nonoun-plugins.md` exits green;
  same for the amended brief; the brief's original deferral bullet is byte-identical in the diff
  (append-only proof: `git diff` on that file shows only added lines).
- Grep proofs: dispatch-ticket contains `Phase 3.5` and `stale-premise` (and its Done-when clause
  contains `stale-premise`); mobilize-chores contains `backlog` in both the predicate paragraph
  and the TICKET FILTER exception sentence; watch-tickets contains `-label:backlog`;
  chore-planner contains `parked`; doc-writing-rules contains `Tracked at`; watch-tickets'
  `evals/evals.json` and doc-writing-rules' evals are UNCHANGED in the diff; `description:` in
  chore-planner.md, issue-sorter.md, and watch-tickets' SKILL.md unchanged in the diff;
  `teamwork/agents/build-leader.md` UNCHANGED in the diff (doc-checker finding 1, resolved —
  see I2/Risk 5: its generic verbatim-relay charter already covers the new outcome class).
- Three version bumps land monotonic over the origin/main values re-read at PR-open (G14).

## Risks

1. **A parked id silently vanishes from human view** (excluded everywhere, forgotten forever).
   Mitigation: that is the label's DESIGN — parking is deliberate shelving; the `roadmap` half is
   tracked by the index (C6, review-cadence monthly), and `backlog` items remain one
   `gh issue list --label backlog` away. The roadmap index's cadence is the anti-forgetting
   contract; no per-sweep nagging is added (it would defeat the immunity).
2. **De-stale false positives** — Phase 3.5 misreads a still-valid premise as falsified and
   blocks a good build. Mitigation: only POSITIVE falsification stales (fail-open on
   unverifiable, C5); the evidence triple makes a wrong verdict cheap to overturn (human re-runs
   with the filter after checking the quoted proof); the ticket is never closed or rewritten.
3. **De-stale scope creep** — the stage drifts into re-design or re-sizing. Mitigation: the
   phase text bounds it to "premises the ticket itself states" and names re-size/re-review as
   non-goals; the skill-checker pass (D2.8) grades exactly this boundary.
4. **Exception-clause drift** — a future edit re-applies the parking exclusion to filter-named
   ids, silently making parked work unpickable. Mitigation: C2.3's carve-out sentence sits inside
   the same TICKET FILTER sentence any such edit must touch; NOT-done clause names the sweep-only
   scope; D1/F1's filter-exception probe is the regression fixture any re-verification can rerun.
5. **Cross-file vocabulary skew** — `stale-premise` spelled or classed differently across
   dispatch-ticket, mobilize-chores, build-leader relay. Mitigation: D2's grep predicates pin the
   literal token in both files; build-leader needs no edit at all (doc-checker finding 1,
   resolved: its charter relays "whatever it reports" generically and by design — see I2) — D2's
   grep predicates confirm `teamwork/agents/build-leader.md` is UNCHANGED in the diff, closing
   the conditional this risk used to carry.
6. **Renumber temptation** — a builder "cleans up" Phase 3.5 into a full renumber. Mitigation:
   C5 records the fractional-numbering decision and its blast-radius rationale; the grep
   predicate pins `Phase 3.5`; cross-file citations of Phase 4/5 stay valid by construction.
7. **Non-decisions noted (ADR-default-no):** (a) label hex values are display choices, one
   `gh label edit` to change — nothing to ratify; (b) no file-backend parking realization is
   designed (this workspace is git-native per ADR-0002; the N/A is disclosed at each surface,
   and a future backend adds its realization in the backend-resolver's own home); (c)
   `stale-premise` handling for the BUG kind is deliberately out (file-bug owns its lifecycle);
   (d) no auto-un-park (label removal stays a human act everywhere). None of these resolved a
   contested fork; none is hard to reverse — no ADR is authored (the closest candidate, the
   binding mechanics, follows the template's own already-stated precedent rather than resolving
   a genuine fork against it).

## Rejected alternatives

- **RA1 — RDD↔Issue binding as a frontmatter field** (`work-items:` or widening
  `decision-refs:`). Rejected: the template's own charter rules work items off the ID spine;
  issue ids are backend-mutable while locked RDDs are byte-frozen; a new key buys lint surface
  with no mechanical consumer. The prose citation costs nothing and matches the TICKET precedent
  exactly.
- **RA2 — Search-side exclusion in mobilize-chores** (`gh issue list --search "-label:backlog"`).
  Rejected in favor of post-filtering the already-fetched labels array: zero new `gh` calls, no
  reliance on search-qualifier semantics inside a `--label`-driven listing, and the predicate
  lands in the same paragraph as the other three conjuncts (one home, not two).
- **RA3 — Pre-claim de-staling** (run the premise check before Phase 3, saving claim/worktree
  cost on a stale ticket). Rejected: the re-check is real effort that should run under a won
  claim (two concurrent pickups would both re-analyze), the stale exit then reuses the existing
  Release-on-abandonment machinery instead of a new pre-claim branch, and #611's own scope pins
  the stage inside the Phase 3→4 boundary.
- **RA4 — A fixture-assertion script** (mechanize D1 as `scripts/parked_check.py` + selftest).
  Rejected: the behaviors under test are model-executed prose — a script can only re-prove `gh`'s
  own filter semantics, not the skill's; the honest payload/API layer is fixture issues + the
  runnable assertion commands D1 states, quoted in the PR. If a recurring need appears (say, a
  scheduled immunity audit), that is a later `/make-script` with its own selftest — named, not
  smuggled in here.
- **RA5 — A SPEC/PRD/ADR alongside this LLD.** Rejected: acceptance is verbatim in #611 (SPEC
  would be manufactured sign-off); why/what live in #611 + the brief (no PRD); every fork was
  either pre-resolved by Kim's ruling or closed here along an already-stated precedent (Risks R7
  — no ADR).
- **RA6 — Minting a first RDD instance now.** Rejected: Now is honestly empty; an RDD must pass
  "could two reasonable teams ship different releases from this line?" and reach `locked` with
  `decision-refs:`+`dri:` — none of which exists for a null commitment. The index states exactly
  what the first real RDD will look like when one lands.
- **RA7 — Moving the brief's deferral bullet to Confirmed** (the literal idr-0007 placement).
  Rejected: the question is half-open (no locked commitment yet); a Confirmed bullet would
  overstate. The dated Open-Questions append copies idr-0007's mechanics, not its address.

## Agent verification

No new harness. Existing instruments cover the design end to end: `release_gate.py` ×3 (lint
sweep over every edited SKILL.md/agent/reference, G10 docs-freshness, G14 monotonic versions),
`/check-routing teamwork` (C2.1's boundary proof), `doc_lint.py` on the roadmap index / amended
brief / this LLD, and D1's fixture assertions — every one a runnable command with an observable,
per docs:agent-harness-rules' payload/API layer (fixture issues + assertions on sweep output and
the stale report, exactly #611's named bar). The one thing no script proves — the semantic
quality of five prose edits — is covered by D2 slice 8's mandatory fresh-context checker passes
(4× skill-checker, 1× agent-checker), which are a required build step here, not an afterthought.
No script changes → no selftest owed this build (`.claude/rules/scripts.md` N/A, disclosed).
