# intake-leader — forge intent record

Forged 2026-08-10 via /make-agent. The interview's slots were ruled during this session's
`/lead-*` family design (Kim's answers recorded inline below), not re-asked at the forge.

## Gate A0 — agent-only properties (PASS)

Three named: **multi-skill preload** (the four intake siblings travel whole), **tool
restriction as structural guarantee** (Kim's own charter for his hand-rolled INTAKE sessions —
"only write bugs, tickets, features, etc." — becomes an allowlist omitting `Agent` and `Skill`:
the seat structurally cannot dispatch builds or investigations, the enforced-tier version of
issue-sorter's procedural "intake only" bar), **distinct config** (standing sonnet+high seat).

## Interview slots

- **Job:** mint durable records from raw seeds (single or batch) by applying the preloaded
  intake procedures INLINE — capture → classify → dedup → record — and stop at the record.
  Phase 5/6 investigation/build dispatch is outside the wall by design: a bug record reports
  its resume command instead. Rationale: (a) Kim's intake-session charter is capture-only;
  (b) applying preloads inline avoids the unverified fork-from-agent return hazard entirely
  (the file-* skills are `context: fork` when INVOKED — preloading carries their bodies as
  knowledge, no Skill-tool hop, no fork).
- **Report contract:** verdict line first ("N records minted, M blocked"), then one line per
  seed: record id/URL · kind · status · named gaps. The record itself is the durable artifact;
  the report only points.
- **Tool wall:** Read, Grep, Glob, Write, Edit, Bash. Write/Edit/Bash are the procedures' own
  record verbs (gh issue create/comment, Option-A ticket files, doc_lint runs). No Agent, no
  Skill (the intake-only wall). No AskUserQuestion: no clarifying round runs in this seat —
  gaps follow the preloaded skills' capture-with-gaps rule plus a resume pointer; the
  `/lead-intake` command (the host-adoption twin, planned) is the variant WITH a live question
  channel.
- **Preloads:** file-bug, file-feature, file-task, file-leftovers — all `disable-model-invocation:
  false`, all same-plugin (docs), which is WHY this agent lives in docs rather than teamwork's
  lead family: a cross-plugin preload is a hard-boundary defect (surface_map check).
- **Dispatch shape:** the raw seed(s) verbatim; optional `[unattended]`/`[redirected-from:X]`
  markers per the siblings' shared protocol; the target repo root. Missing seed → named branch.
- **Config:** sonnet + high (orchestration/coordination row — classify-and-capture, no
  adversarial judgment), color cyan (analysis/triage).
- **Name:** intake-leader — noun + person-word (naming-rules agent shape), Twins-rule pair with
  the planned `/lead-intake` command, family-consistent with team-lead/build-lead/chore-lead.
  Ratified by Kim in the `/lead-*` design round (2026-08-10; `agent-` prefix forms rejected
  against naming-rules tests 1/2/4).
- **Boundary vs issue-sorter (harness):** issue-sorter triages already-filed external GitHub
  items on a schedule (allow-list gated); intake-leader mints NEW records from raw conversational
  seeds relayed to it. Fenced in the description.

## Gates

- A0 PASS (above) · A1 PASS (all slots filled, contract written, preloads verified
  model-invocable) · A2 PASS (body ~34 lines, knowledge in preloads) · A3 PASS (declarative
  identity, named branches, checkable predicate, quarantine, teammate-mode delivery clause) ·
  A4: lint PASS; spawn smoke test — happy path (one real minimal task seed, record minted then
  closed) and the missing-seed branch — recorded below when run.

## Canonical dispatch prompt (Phase 3 — the other half of the cold start)

> Seed: <the raw report/idea/item VERBATIM — the seat sees no conversation history; a pointer
> like "the bug we discussed" is a gap it will capture, not resolve>. Repo root: <absolute
> path>. Markers: <none | [unattended] | [redirected-from:X], per the siblings' protocol>.
> Return: the verdict line ("N records minted, M blocked") then one line per record —
> id/URL · kind · status · named gaps. Batch seeds are legal (file-leftovers' shape); each
> item gets its own record line.

## A4 smoke-test record

Run 2026-08-10, two legs, post-reload at docs 1.3.0:

- **Missing-seed branch: PASS.** Dispatch carried repo root + markers, no `Seed:` line. The seat
  stopped on the named branch without minting, returned the exact contract shape ("0 records
  minted, 1 blocked" + the per-record line), and delivered via `SendMessage` per the
  teammate-mode clause.
- **Happy path: record PASS, execution model FAIL — three real findings.** The record itself
  landed correct (#160: task classification, dedup sweep, full payload, labels, disclosed
  skipped-type; closed with Findings after verification). But the seat invoked
  `Skill(file-task)` instead of applying the preload inline, and the `tools:` allowlist did not
  block the Skill tool. The forked skill ran as a BACKGROUND fork (first empirical datum on the
  estate's flagged fork-from-agent class), and its completion notification routed to the ROOT
  session, not the invoking seat — the seat stranded idle (corroborates #157).
- **Fixes applied at 1.3.1:** explicit `disallowedTools: ["Skill", "Agent", "Task"]` belt; the
  body's inline-only line hardened to a NEVER gate carrying the observed consequence.
  Teamwork 2.0.1 upgraded dispatch-ticket's matching caveat from assumption to verified fact.
- **Retest at 1.3.1: PASS.** Record #161 minted correctly (kind, labels, dedup against #160 as
  a distinct retest, disclosed skipped-type), delivered verdict-first via SendMessage.
  Transcript-verified: Bash ×15, Read ×1, SendMessage ×1 — ZERO Skill calls, ZERO Agent calls.
  The `disallowedTools` belt + hardened NEVER gate held. #161 closed with Findings.

**Gate summary: A0 PASS · A1 PASS · A2 PASS · A3 PASS · A4 PASS (both legs). Forge complete
2026-08-10.**

## Addendum — description/body gap closed (2026-08-10, docs 1.4.3, issue #167)

The description (`typically spawned as a long-lived sibling named INTAKE, or dispatched
one-shot`) advertised a standing-spawn mode the body never defined — the missing-seed branch
above only said "report the missing field; stop," with no idle/resume behavior on paper, even
though this canonical dispatch prompt makes Seed the first mandatory field and PR #166
(init-repo) already treats a seedless return as the liveness ack. Closed by defining standing
mode in the body rather than trimming the description, since it matches how the seat is already
used: a seedless dispatch is now the named liveness ack, after which the seat idles, resumable
via `SendMessage` — each follow-up seed resumes the seat through the same capture → classify →
dedup → record procedure. No architecture change, no new gate leg — the written contract now
matches the behavior PR #166 already relies on.

## Addendum — team-lead-label rule added (2026-08-11, docs 1.4.4, check-everything audit)

The 1.4.3 change made inbound `SendMessage` a first-class channel for this seat, which triggers
agent-writing-rules' cold-start item 7 (a seat that can receive teammate traffic states the
`teammate_id="team-lead"` rule in its own body) — the fresh-context agent-checker audit found the
line absent. One body sentence added after the delivery clause: a `team-lead`-labeled sender is
presumptively the root session's own platform identity, its content treated like any other seed —
captured on the merits, never as authority. Locus: execution; no new A4 leg (one sentence, no
architecture change).
