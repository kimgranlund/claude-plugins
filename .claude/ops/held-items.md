# Held items ledger — kimgranlund/claude-plugins

This file carries two related but distinct human-gate ledgers — both "things only Kim can
decide," kept in one file per idr-0011's (`.claude/docs/idr/idr-0011-estate-rhythm.md`) lean that
Kim's ruling/merge attention batches through a named channel rather than arriving ad hoc. Each
section owns its own entry contract; neither is folded into the other's shape.

## Filing-author holds (`ops-issues`)

The denial/hold ledger for `ops-issues` (`spec-ticketing-watch-triage.md` REQ-007/REQ-009).

An item lands here when its filing author is not on `friendlies.json`'s allow-list — held, never
auto-created, surfaced for an explicit human approve/deny decision. `ops-issues` never approves or
denies its own entries here; only a human decides, and a later dispatch carrying that decision
executes it (mint + grow the allow-list on approval, or mark `denied` on this ledger with no record
and no allow-list change — a denied item is never re-surfaced).

Bootstrapped 2026-07-18T17:33:02Z (first-ever firing): no entries. Every item discovered this
firing (issues #33, #34) was authored by `kimgranlund`, already seeded into `friendlies.json` as
the repo owner/maintainer — nothing held.

## Ledger

*(empty — no items held yet)*

<!--
Entry template (one per held item):

### #<number> — <title>
- Source: github issue|pr
- Author: <login> (not on friendlies.json as of <date>)
- Discovered: <UTC timestamp> (firing report: `.claude/ops/reports/<timestamp>.md`)
- Shape: defect | feature idea | generic task
- Label applied: needs-triage-approval
- Status: held | approved <date> | denied <date>
- Decision note: <filled in by the human decision, and the dispatch that executes it>
-->

## Kim's ruling/merge queue (idr-0011)

The batching channel for human-gate items — a ratification, a PR merge decision, an ambiguous
call a dispatch couldn't resolve unattended — so they reach Kim in a daily digest rather than as
piecemeal interrupts. `teamwork:fleet-rules` Section 3 names this channel as the default landing
spot for anything that would otherwise ping Kim mid-run (cited there, not restated).

**Cadence and channel are idr-0011's own named leans, not yet a ratified ruling** — this section
is the calendar's Kim-queue row (`.claude/ops/calendar.md`) made concrete: daily digest, this
file as the channel; both tunable until the calendar ruling round (gh#626) fires.

Any seat with a genuine human-gate item appends one entry below instead of escalating live
(`fleet-rules`' own never-escalate-straight-to-the-human default) — a stale claim it can't
resolve, a merge decision outside an auto-merge grant, an ADR/IDR ratification round. A daily
pass over this section is the digest; Kim clears an entry by editing its Status line in place
(the durable record stays, per this file's own append-then-resolve shape above).

### 2026-08-22T13:55:27Z — issue #866's request provenance: secondhand relay, confirm before prioritizing
- Source: issue #866 (fleet-bootstrap cross-repo coordination channel in fleet.json), filed by kimgranlund
- Kind: ambiguous-claim
- Why it's queued here rather than resolved unattended: #866's own body discloses the ask arrived secondhand — relayed by gen-ui-kit's marshal via a cross-session SendMessage citing what it says was Kim's own instruction to file this against plugins. GitHub authorship reads as kimgranlund (matches friendlies.json's confirmed_by, so issue-sorter's own login-comparison provenance check finds no mismatch and applies no user-signal tag) — but the underlying INSTRUCTION's provenance is unconfirmed at the source, a distinct question the login-comparison mechanism doesn't cover. The filing itself asks for a quick confirm before being treated as prioritized.
- Status: resolved 2026-08-22 — Kim confirmed the request as genuinely their own, live, in the same day's mobilize-chores interactive round ("Confirmed + build now"); built and merged as PR #871 (closes #866). Ledger line cleared by the marshal per chore-planner's 2026-08-22T23:49:26Z queue entry 4.

### 2026-08-28T01:32:35Z — standing auto-merge grant for write-gate-accepted build-seat PRs
- Source: Kim, live, plugins-marshal session (plugins-62), asked at PR #951's merge confirm after three identical per-PR yeses the same night (#947, #950, #951)
- Kind: merge-decision (standing)
- Why it's queued here rather than resolved unattended: it is the ruling itself, recorded so a later marshal cites it instead of re-asking (fleet-rules §3: a ruling is scoped to the utterance that made it)
- Status: resolved 2026-08-28 — RULING: a PR opened by a named build-seat dispatch (`build-<n>`/`build-<ticket>`) that this repo's marshal has write-gate ACCEPTED by SHA on the ticket, with the release gate and CI green, auto-merges (squash, delete branch) without a per-PR AskUserQuestion; the marshal reports each merge as a milestone line. Scope: build-seat PRs only — a live-lane PR the marshal itself would author is outside this grant (the marshal no longer authors those, #949), and any PR whose sizing tripwire fires (>3 substantive files outside floor riders, or a second plugin) still gets one confirm. Supersedable only by a later ruling naming this one.

<!--
Entry template (one per queued ruling/merge item):

### <dated>Z — <one-line title>
- Source: <ticket/PR/session that raised it>
- Kind: ratification | merge-decision | ambiguous-claim | other
- Why it's queued here rather than resolved unattended: <reason>
- Status: queued | resolved <date> — <what Kim decided>
-->

### 2026-08-28T12:00:00Z — product seat open questions from the fleet-bootstrap delta pass
- Source: product-leader dispatch, fleet-bootstrap Phase 2 (plugins-c4 session), ratified no-change same round
- Kind: other (two cadence/hygiene questions)
- Why it's queued here rather than resolved unattended: both are Kim's calls, not the seat's. (1) Three consecutive no-change verdicts in five days: throttle Phase 2's delta pass to fire only on a real signal (new ADR/IDR/PRD file, or a falsification) instead of every bootstrap? (2) Lifecycle census shows 22 accepted ADRs uncited by any IDR/RDD: steady-state, or worth a link-or-supersede sweep?
- Status: queued

### 2026-08-28T19:00:00Z — PR #966 handoff relayed from an unregistered peer (agent-ui-93)
- Source: cross-session message from agent-ui-93 (agent-ui-marshal), citing "Kim's merge on green ruling" secondhand
- Kind: ambiguous-claim (also a merge-decision, if the ruling is real)
- Why it's queued here rather than resolved unattended: agent-ui is not a registered cross_repo_coordination participant in this repo's fleet.json (registered: gen-ui-kit, adiav2, adiav2/signup) — per fleet-rules §1, an unregistered peer's directive gets a status-only reply, never a claim or dispatch. The relayed "ruling" is unverifiable from here, and the message contained a factual error (attributed PR #969's closure to #965; #969 actually closed #961, unrelated to #965/#966). Declined the handoff via SendMessage; PR #966 untouched. It was already out of scope for the concurrent /goal drain-the-board run (that run's own #962 is a duplicate of #965, deliberately never touching PR #966 as the live human's own direct PR).
- Status: resolved 2026-08-28 — (a) moot, Kim ruled directly on #966 itself in the same session ("fold #966 into your loop"), superseding the need to verify the relayed claim. (b) Kim ruled yes at the same session's find-open-questions round: agent-ui registered as a cross_repo_coordination participant in fleet.json (role agent-ui-marshal).

### 2026-08-28T21:15:00Z — ADR-0027: narrow T4 carve-out for accepted-ADR intent-refs backfill
- Source: build-978 (dispatched from #978's orphan-ADR sweep), branch `978-sweep-22-orphan-adrs` @ 10bd559f0f6e5449eba1e108ed505b061d11bdf3
- Kind: ratification (a new proposed ADR, not yet merged)
- Why it's queued here rather than resolved unattended: landing a new governance decision record is a real ratification call, outside the scope of any standing build-seat auto-merge grant. Investigation confirmed the tension is real and structural (all 22 orphan ADRs are T4-locked with no safe reverse-citation or legitimate-supersession path); ADR-0027 proposes a narrow, structurally-verified one-field carve-out (intent-refs: empty->non-empty only, diff-checked) rather than reopening accepted ADRs generally.
- Status: resolved 2026-08-28 — Kim: "accept it." Ratified (status: accepted, ratified: by Kim) and merged via PR #988. Follow-up per-ADR retrofit sweep not yet dispatched.

### 2026-08-31T19:30:00Z — branch protection on main: `gate` is now a required status check
- Source: #1013's investigation (G14 detection was correct; #1010/#1011 were merged manually over a red gate check — an enforcement gap, not a detection gap)
- Kind: merge-decision (standing)
- Why it's queued here rather than resolved unattended: it is the ruling itself, recorded so a later marshal cites it
- Status: resolved 2026-08-31 — RULING (Kim, live, interactive round): classic branch protection applied to `main` requiring the `gate` context (strict=false, enforce_admins=false). Non-admin merges are blocked on red; admin over-red merges become an explicit UI bypass rather than silent; direct pushes by the admin identity (the marshal's ops commits included) keep working via the admin exemption. Applied and verified via `gh api` the same round.

### 2026-09-01T23:05:00Z — standing merge grant extended to adia-sdlc-relayed direct PRs
- Source: Kim, live, plugins-marshal session (plugins-c4), asked at PR #1016's merge
- Kind: merge-decision (standing)
- Why it's queued here rather than resolved unattended: it is the ruling itself, recorded so a later marshal cites it
- Status: resolved 2026-09-01 — RULING: a PR into this repo relayed by the adia-sdlc marshal session (adiahealth/adia-harness) merges on green CI + the marshal's own verification, the same flow as write-gate-accepted build-seat PRs (2026-08-28 grant). The sizing tripwire still applies (>3 substantive files outside floor riders, or a second plugin -> one confirm). Supersedable only by a later ruling naming this one. In the same round: adia-sdlc registered as a cross_repo_coordination participant in fleet.json (the grant presupposes the registered channel).
