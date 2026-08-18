---
doc-type: adr
id: adr-0022
status: proposed
date: 2026-08-18
owner: kim.granlund
supersedes: null
intent-refs: idr-0002 (git substrate as the durable cold-start memory — this ADR extends that
  claim from seat recovery to estate recovery and makes it a binding contract)
---
# ADR-0022 — The repo is the backup: everything operationally load-bearing is reconstructible from origin/main

> DRAFT — `status: proposed`, awaiting Kim's ratification (one batched round with
> idr-0008/0009/0010/0011 and adr-0021, per gh#622–#627). The accepted-ADR append-only rule
> binds only after acceptance; until then this text may be revised freely.
> Record-type note (confirming ADR against the standing ADR-default-no ruling, as gh#627 asks):
> ADR is correct — this is a CONTRACT binding every operationally load-bearing artifact to a
> reconstructibility requirement with an enumerated exception list, not a hypothesis; gh#627's
> intake is the ratified fork the default-no requires, and the upstream intent already exists
> locked (idr-0002), so no new IDR is owed.

## Context

The estate's bus factor is one, everywhere: one human, one GitHub account, one machine hosting
every worktree, session memory on one disk, ops state reconstructible only in theory.
Records-as-bus (idr-0002) makes SEATS recoverable — any successor context can resume from the
records — but nothing makes the ESTATE recoverable: no ruling says what a fresh machine plus a
clone of origin/main could and could not restore, so the answer today is unknown rather than
designed. Origin: conceptual hole #6 of the 2026-08-18 estate gap review (gh#627; the six
tickets gh#622–#627 are the review's durable record; sibling records idr-0008/0009/0010/0011,
adr-0021).

## Decision

Proposed: **the repo is the backup.** Everything operationally load-bearing must be
reconstructible from a fresh machine plus a clone of origin/main — anything load-bearing that is
not reconstructible is either committed, or enrolled in the named-exception list below with a
mitigation, or it is a defect. The named exceptions, each with its mitigation:

1. **Memory directory** (`~/.claude/projects/.../memory/`) — session-derived judgment, not
   canon. Mitigation: anything in memory that has become load-bearing doctrine is promoted into
   a committed record (skill, rule, ADR/IDR); the residue is accepted as lossy by design.
2. **Plugin cache / installed-plugin state** — regenerable from source; the repo's manifests are
   the canon. Mitigation (owed at lock, does not exist yet): a documented reinstall path from
   this repo's plugin roots — a deliverable this ADR's acceptance creates, seeded as a ticket
   line in gh#627.
3. **Credentials** (gh auth, API keys, `.env`-class material) — never committed, by standing
   deny rules. Mitigation (owed at lock, does not exist yet): a re-issuance runbook naming each
   credential and where it is re-obtained, committed in place of the secrets themselves — same
   owed-at-lock deliverable class, seeded in gh#627.
4. **User-scoped `~/.claude` / `~/.config` state** — the global CLAUDE.md, the `settings.json`
   deny tripwires (the rm/dotenv guards), and the git-ignore convention keeping
   `settings.local.json` untracked: operationally load-bearing, entirely outside any repo.
   Mitigation lean: a committed canonical copy or dotfiles pointer for the global CLAUDE.md and
   the deny-rule set, plus a re-derivation note for the remainder — exact mechanism ruled at
   ratification (open question 2).

The ruling's instrument (named, not shipped in this PR — follow-up seed in gh#627): a
**read-only reconstructibility audit** — a selftest-bearing script that sweeps the estate and
reports the delta: every load-bearing item a fresh clone could NOT recover, checked against the
exception list. Report-only; mitigations ride tickets, never the audit itself.

## Consequences

Positive: recoverability becomes a designed property with a measurable delta instead of an
untested assumption; uncommitted-but-load-bearing ops state becomes a nameable defect class; the
exception list turns "what would we lose" from a guess into a ratified enumeration. Negative/
cost: the audit is one more standing sweep whose firing must earn its cost under idr-0010's
pricing test, and the exception list can rot — idr-0009's re-validation sweep covers accepted-ADR
Decisions, so this list is re-tested like any other Decision. Neutral: single-human/single-account
concentration itself is NOT solved here — this ADR makes the estate restorable by whoever holds
the account, not resilient to losing the account; that larger question stays open below.

## Open questions

- Audit instrument home: lean is harness `scripts/` (a workspace-generic sweep in the toolchain
  plugin); routing owes the anti-matrix check before minting (gh#627 names authorkit/ops as the
  alternative).
- Scope edges to ratify: `.claude/ops/` is ALREADY fully committed — verified on this branch,
  11 top-level ops files (fleet.json, friendlies.json, plan.md, held-items.md, roster and
  checkpoints) plus the tracked `reports/` archive — so it sits inside the rule, not the
  exception list; that is a fact, not a lean. Still to rule: `settings.local.json` OUT with a
  documented re-derivation note (lean), worktrees OUT (regenerable by definition), and the
  exact mitigation mechanism for exception 4's user-scoped state (committed canonical copy vs
  dotfiles pointer vs enroll-with-re-derivation-note).
- Whether the account/organization single-point (one GitHub account owns the canon) gets its own
  mitigation line or is explicitly accepted — the seed is silent; drafted here as accepted-for-now.
- Exact exception list at lock: the three above are the seed's; ratification may add or strike.
