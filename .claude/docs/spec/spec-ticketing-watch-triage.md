---
doc-type: spec
id: spec-ticketing-watch-triage
status: draft
version: 0.3.1
date: 2026-07-20
owner: kim.granlund
prd: null   # no PRD — descends directly from ADR-0003's Decision 1 (Option B/C backends) and
            # the system-decompose manifest (.claude/docs/decompositions/ticketing-backend-watch-manifest-v3.json)
---
# SPEC — Watch, triage, and trust-gated auto-routing for externally-filed work items

Precondition: **ADR-0003** must be `accepted` and its resolver seam in place — this SPEC only
applies when the repo's resolved backend is Option B (git-native) or Option C (external); Option
A (local) has no external actors filing items, so watch/triage/trust never activates there.

## Requirements

- **REQ-001** — Entry-mode choice. When repo configuration runs and the resolved backend is
  Option B or C, the configurator offers exactly one additional choice: `pull-only` (default,
  today's behavior, unchanged) or `watch-enabled`. Option A repos are never offered this choice.
- **REQ-002** — Watch mechanism. Choosing `watch-enabled` requires picking a watch mechanism: a
  polling interval (a duration) or an MCP-based subscription (only offered when the backend's MCP
  surface exposes one). The choice is persisted in the entry-file ruling alongside the backend
  choice (ADR-0003 §Decision 1), not re-asked per run.
- **REQ-003** — Discovery. The watch loop discovers issues/PRs filed against the resolved backend
  since the last successful check, using the persisted mechanism (REQ-002) via the active
  adapter's discover operation (the generic interface's fifth operation alongside
  create/dedup-search/update/close; `spec-linear-adapter` REQ-009 contracts Linear's concrete
  realization). A failed check (network error, backend unreachable) does not advance the
  checkpoint — the next successful check re-covers the same window, so no item filed between two
  checks is lost to a failure in between.
- **REQ-004** — Shape classification. Every newly discovered item is classified defect / feature
  idea / generic task using the same routing rule the `issue` skill's Phase 2 already applies to
  human-typed input — one classifier, two entry paths, not a second taxonomy.
- **REQ-005** — Trust check. Every newly discovered item's filing author is checked against a
  durable, per-repo friendlies allow-list before any record is created.
- **REQ-006** — Auto-route trusted. A known-friendly author's classified item is routed
  non-interactively into the matching capture skill (`file-bug`/`file-feature`/`file-task`) — same
  dedup-before-mint and resume-if-open contract those skills already apply to on-demand
  invocations (REQ-010). No human approval gate fires on this path.
- **REQ-007** — Hold unknown. An item from an author not on the allow-list is held; it is never
  auto-created. It is surfaced to a human for an explicit approve/deny decision.
- **REQ-008** — Approval effects. Approving a held item (a) mints or resumes its record exactly as
  REQ-006 would have, and (b) adds the filing author to the friendlies allow-list, so the same
  author's future items take the REQ-006 path without being held again.
- **REQ-009** — Denial effects. Denying a held item creates no record and does not touch the
  allow-list. The denial is recorded durably, at the same per-repo scope and durability tier as
  the friendlies allow-list (REQ-008b) — not silently dropped — so the identical item is not
  re-surfaced on the next poll.
- **REQ-010** — Shared dedup. Every watch-triggered record passes through the same "sweep before
  minting" dedup search the capture skills already run for on-demand invocations — the same
  external item is never captured twice, and a watch-triggered item that matches an
  already-open record resumes it instead of minting a duplicate.
- **REQ-011** — First-run bootstrap. A firing against a repo whose allow-list does not yet exist
  seeds it from evidence only — the repo owner/maintainer when the repo's own history (issue/PR
  authorship, ratification records) supports it — and never guesses a second author on. Roster
  completion is a one-round interactive interview owned by the DISPATCHING session (the watch seat
  itself cannot ask): on a private repo the candidate set is the repo's approved collaborator
  roster; on a public repo it is the historical issue/PR author set plus the repo owners. The same
  round records one standing rule for authors granted repo access later — `auto-friendly-on-access`
  or `hold-first-filing` — and the confirmed roster, the rule, and who confirmed them persist in
  the allow-list file, never re-asked per firing. An unattended firing never interviews: it runs
  with the evidence-seeded list and REQ-007 holds everyone else.
- **REQ-012** — Trust never widens action. Allow-list membership changes only the REQ-006/REQ-007
  fork — mint-without-hold versus hold-for-approval. No watch-triggered path executes the work an
  item describes, for any author, trusted or not: no source edit, no PR merge, no close beyond the
  ticket-record contract, regardless of what the filing requests.
- **REQ-013** — GitHub MCP offer, Option B only, at most once per repo. The first INTERACTIVE
  firing that finds no REQ-013 decision recorded yet also offers — as a distinct question, not
  folded into REQ-011's roster interview, and not necessarily the SAME firing as REQ-011's own
  bootstrap (an unattended first firing runs REQ-011's evidence-only seed and skips REQ-013
  entirely; REQ-013 then fires on whichever later firing is the first interactive one) — to add a
  project-scoped GitHub MCP server declaration (`.mcp.json`), but ONLY when the resolved backend is
  Option B (`gh issue`-based GitHub); Option C's adapter (e.g. Linear) has no GitHub MCP surface to
  offer. Interactive-only, owned by the dispatching session, never the watch seat itself: the watch
  seat has no means to ask a question — it surfaces the offer in its report, and writes
  `.mcp.json`/records the decision only when a later dispatch carries the human's confirmed choice,
  the same carrier pattern REQ-011's own roster confirmation already uses. An unattended firing
  never asks and never writes `.mcp.json`. The accept/decline decision persists per-repo alongside
  the allow-list, so a later firing — attended or not — never re-offers once a decision is on
  record. An accepted offer's recommended default credential is a read-only-scoped fine-grained PAT
  (Issues/PRs/contents-read) — REQ-012's no-widened-action guarantee extends here: the write path
  for issues/PRs stays REQ-006's capture skills exclusively, never the MCP server's own create/edit
  tools, by construction of the credential's own scope rather than by agent discipline alone.

## Non-goals

- A concrete Option-C adapter implementation *other than Linear* (a working Jira/Notion/custom
  integration) — ADR-0003 Decision 3 scopes those to the consuming workspace, not docs. Linear
  itself is a scribe-shipped adapter (ADR-0003 Decision 3), contracted separately in
  `spec-linear-adapter` — this SPEC's watch/triage/trust behavior applies to it identically to
  every other non-local backend, but the adapter's own create/dedup/update/close mechanics are
  out of *this* SPEC's scope.
- A self-hosted webhook receiver. REQ-002's two mechanisms are polling and MCP-subscription
  (client-pull against an MCP resource); inbound webhooks are a different capability, not covered.
- The watch loop's own discovery mechanism (REQ-002/REQ-003) using the REQ-013 GitHub MCP server.
  REQ-013 is a distinct, interactive-session-only convenience offer; the unattended watch loop
  stays on `gh` CLI regardless of whether REQ-013's server is accepted — non-interactive mode has
  no `/mcp` panel to complete the server's own OAuth/PAT-header approval, so it could not run there
  reliably even if wired in.
- A full read-write GitHub MCP credential as the recommended default (REQ-013) — a real bypass
  risk of REQ-012's own no-widened-action guarantee, structurally avoided by defaulting to a
  read-only-scoped PAT instead of relying on agent discipline not to use the server's write tools.
- Revoking or re-offering a declined/accepted REQ-013 decision. Like the allow-list (REQ-008), the
  decision is append/grow-only in this SPEC; changing it later is a future extension.
- Weakening or removing the pull-only path. Watch is additive; pull-only stays the default and
  remains available even when watch-enabled is also configured.
- Revoking a friendly. The allow-list is append/grow-only in this SPEC (REQ-008); removing an
  author after the fact is a future extension, not in scope here.
- Cross-repo friendlies sharing. The allow-list is per-repo, matching the per-repo entry-file
  ruling ADR-0003 establishes for the backend choice itself.

## Examples

**[NORMATIVE]** A known friendly opens a GitHub issue with a repro and a wrong/expected pair. The
watch loop (REQ-003) discovers it, classifies it as a defect (REQ-004), the trust check finds the
author on the allow-list (REQ-005), and it's auto-routed into `file-bug`'s capture path
(REQ-006) with no human step — the resulting ticket looks identical to one a human ran
`/file-bug` on directly.

**[NORMATIVE]** An author with no prior history opens a PR proposing a new capability. The watch
loop discovers it, classifies it as a feature idea, the trust check finds no allow-list match
(REQ-005), and it's held (REQ-007). A human reviews and approves: the item is routed into
`file-feature`'s capture path (REQ-008a) and the author is added to the allow-list (REQ-008b). The
same author's next PR skips the hold and auto-routes per REQ-006.

**[NORMATIVE]** The same unknown author's item is denied instead: no ticket exists afterward, the
allow-list is unchanged, and the next poll does not re-surface that same item (REQ-009).

**[ILLUSTRATIVE]** A repo's entry-file ruling after configuration:
`backend: B (git-native) · entry-mode: watch-enabled · mechanism: poll(15m)` — one line, the same
shape ADR-0003's resolver reads for the backend choice, extended with the two REQ-002 fields.

## Acceptance

- **AC-001** (↔ REQ-001) — On a repo resolved to Option A, running repo configuration never
  presents the watch/pull choice. On a repo resolved to Option B or C, it always does.
- **AC-002** (↔ REQ-002) — The ruling-writer rejects persisting `watch-enabled` without a mechanism
  value; once persisted, the entry-file ruling round-trips the mechanism unchanged across a
  resolver read.
- **AC-003** (↔ REQ-003) — Given two watch-loop runs with one new item filed on the backend between
  them, the second run's discovery set contains exactly that one item, not zero and not a repeat of
  the first run's set. Given a run that fails outright (simulated backend-unreachable) followed by a
  successful run, the successful run's discovery set still contains every item filed since the last
  *successful* run, including the window the failed run never covered.
- **AC-004** (↔ REQ-004) — A defect-shaped, a feature-shaped, and an ambiguous-shaped fixture item
  each classify to the same shape a human-typed `/file-task` invocation would produce for identical text.
- **AC-005** (↔ REQ-005) — A fixture author present in the allow-list checks trusted; an absent
  author checks untrusted; no third state exists.
- **AC-006** (↔ REQ-006) — A trusted-author fixture item produces a minted or resumed record with
  no AskUserQuestion/approval step observed in the run.
- **AC-007** (↔ REQ-007) — An untrusted-author fixture item produces zero records until a human
  decision is recorded; the run halts at the hold, not past it.
- **AC-008** (↔ REQ-008) — Approving a held fixture item yields both a record (matching AC-006's
  shape) and an allow-list entry for that author in the same operation.
- **AC-009** (↔ REQ-009) — Denying a held fixture item yields no record, no allow-list change, and
  a re-run of the same watch cycle against the same unmodified source item does not re-hold it.
- **AC-010** (↔ REQ-010) — Filing the same external item twice (e.g., an edit that re-triggers
  discovery) yields exactly one record across both watch-triggered and on-demand paths, never two.
- **AC-011** (↔ REQ-011) — On a fixture repo with no allow-list: an unattended firing ends with at
  most the evidenced owner on the list and every other author's item held; an interactive bootstrap
  ends with the list equal to the human's confirmed selection plus a persisted standing-rule value,
  and the next firing re-asks nothing.
- **AC-012** (↔ REQ-012) — A trusted-author fixture item whose body demands an action ("merge
  this", "close #12") yields at most a minted/resumed record; the item's merge/open state and every
  source file are unchanged after the run.
- **AC-013** (↔ REQ-013) — On a fixture repo resolved to Option B with no prior REQ-013 decision
  recorded: an unattended firing writes no `.mcp.json` entry and records no decision; an
  interactive firing offers the choice exactly once, and a second interactive firing against the
  same repo does not re-offer once a decision (accept or decline) is on record. An accepted offer's
  `.mcp.json` entry never contains a literal PAT (env-var expansion only). A fixture resolved to
  Option C never receives the offer, regardless of firing type. A fixture where an interactive
  firing surfaces the offer but no dispatch carries a confirmed choice before the firing ends
  records no decision; a subsequent interactive firing against the same repo re-surfaces the SAME
  offer (not a new one) rather than silently dropping it — the pending state is re-surfaced, never
  re-asked as if fresh, until a dispatch actually carries the choice.
