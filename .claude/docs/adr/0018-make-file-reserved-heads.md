---
doc-type: adr
id: adr-0018
status: accepted
ratified: Kim, 2026-08-17, live AskUserQuestion via plugins-team-lead
date: 2026-08-17
owner: kim.granlund
supersedes: adr-0016 (D3's `intake` non-registration clause ONLY, per this ADR's own D3 —
  the lead- head, D1/D2, D4's fence all stand unamended; amends spec §3.2 by the §14.2
  mechanism ADR-0014 established; ADR-0014 and ADR-0016 are not edited — accepted ADRs are
  append-only, supersession recorded here by citation alone)
intent-refs: null
---
# ADR-0018 — `make-` and `file-` join `check-`/`lead-` as reserved skill heads; ObjectVocab gains 10 registrations including `intake`

> **Ratified 2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead), recorded in
> issue #477's Findings comment referencing #464's proposal** — from ratification this file
> is append-only (doc_lint T4); a change of mind supersedes, never edits. Drafted 2026-08-16
> as part of #464's S8 lexicon-amendment proposal (overhaul #373 Wave-3), executed 2026-08-17
> under this ratification. ADR-0014 and ADR-0016 are NOT edited — accepted ADRs are
> append-only.

## Context

ADR-0014 established one literal reserved skill head, `check-`, on the mechanism: a literal
verb-first token, residue resolving against `ObjectVocab` alone, placed before the
`ProcessLex`-terminal object-process check to avoid a dead-code hazard (`check-stage`'s
terminal `stage` sits in `ProcessLex`; a later placement would never reach it). ADR-0016
extended the same closed-head pattern to the command grammar with `lead-`.

#464's measured evidence (`validate.py --scope grammar`, all 8 plugins, exemptions emptied,
2026-08-16) finds two more literal verb-first families that are recurring and still being
minted, not one-off names: `make-*` (18 exempted names estate-wide; `/make-plugin`,
`/make-skill`, `/make-doc`, `/make-reference`, `/make-rubric`, `/make-vision-memo`,
`/make-llms-txt` among them — the routing table's own named owners, new mints certain) and
`file-*` (4 live: `file-bug`, `file-feature`, `file-task`, `file-leftovers` — the intake
family, growing with the intake seat). ADR-0014 Alt C (generalizing the reserved-head
mechanism to every `VerbLex` member) was rejected there on the "narrowest cut" argument; this
amendment does not revisit that rejection — it applies the SAME narrow mechanism to two more
specific, evidenced literals, keeping the head set closed and enumerable.

**Why these two and no others (the bar restated):** recurring AND still being minted.
Verb-head one-offs and small families (`plan-*` ×4, `find-*` ×2, `clean-*` ×2, `watch-*` ×2,
and 15 singletons) and unresolved nominals with a single consumer (`research-methods`,
`github-facts`, `html-to-markdown`, `markdown-to-markup`, `plugin-install-facts`) stay exempt
by design — registering per-name tokens for a single consumer is the vocabulary dilution
ADR-0015 Alt E already rejected. `plan-` was the closest call (4 names) but 3 of its 4
residues would force compound ObjectVocab registrations whose only consumer is the name
itself; deferred, not rejected forever.

**The `intake` registration and the ADR-0016 non-goal it reverses:** ADR-0016 §14.5 D3
declined registering `intake` "solely to clear one exemption" (`lead-intake`), citing the same
Alt B/Alt E dilution concern. This amendment registers `intake` anyway — see D3 below for why
this is not a silent reversal but a different evidentiary bar being met.

**Scope arithmetic (verified against `naming.manifest.json` at the ratification tree,
2026-08-17):** the `make-` head plus B1–B10 (below) retires 10 skill exemptions
(`make-doc`, `make-hook`, `make-pack`, `make-plugin`, `make-script`, `make-skill` — residues
already registered — plus `make-reference`, `make-rubric`, `make-vision-memo`, `make-llms-txt`
via B7–B10); the `file-` head retires 3 (`file-bug`, `file-feature`, `file-task`;
`file-leftovers` stays exempt — `leftovers` fails the same single-consumer dilution bar).
`make-agent` stays exempt PERMANENTLY — see D2 — as does the quantifier trio
`check-all-agents`/`check-all-skills`/`check-everything` (ADR-0014's own ruling, unaffected).
`intake` (B6) retires `lead-intake` via the pre-existing `lead-` head (ADR-0016), and enables
the `intake-lead → intake-leader` rename (ADR-0017, issue #477) once combined with that ADR's
RoleLex growth.

**Owner boundary — same split as ADR-0011/0014/0015/0016/0017.** Docs-owned record amending a
docs-owned spec that governs an authorkit-owned validator and reference set. Ratification
provenance is the live AskUserQuestion named in `ratified:`; the follow-on implementation is
authorkit's, executed in the same PR under the same authorization.

## Decision

**The skill grammar (spec §3.2) gains two literal reserved verb-first heads, `make-` and
`file-`, exactly ADR-0014 §14.2's `check-` mechanics.** `ObjectVocab` gains 10 registrations.
The literal head set on the skill grammar closes at exactly `{check, lead, make, file}`.

### D1 — The production

```
skill := "make" "-" object-phrase     make-skill, make-doc, make-reference
skill := "file" "-" object-phrase     file-bug, file-feature, file-task
```

`make` and `file` are **literals**, exactly as `check` is under ADR-0014 D2 and `lead` is
under ADR-0016 D1 — not templates for other `VerbLex` members, even though both already sit in
`VerbLex` for the unrelated object-verb command production (§3.1) and the reverse-wrapper
skill production (§14.1). No conflict: the head check is a distinct literal-token branch,
consulted before either of those productions gets a chance to apply. Residue resolves against
`ObjectVocab` ONLY — never the `-rules` tail's three-way union pool (§14.2 D1) — because a
`make-<noun>`/`file-<noun>` name denotes a real object the forge or intake family produces,
the same object-denoting argument ADR-0014 D2 made for `check-<noun>`.

### D2 — Validator placement, and the tail-before-head invariant

`Grammar.parse`'s `kind == "skill"` branch gains the two head checks immediately after the
existing `lead-` head check and before the `ProcessLex`-terminal object-process check — the
same dead-code-hazard ordering ADR-0014 D2 and ADR-0016 D2 established (`make-pack`'s residue
`pack` and `file-task`'s residue `task` are plain `ObjectVocab` members that a later placement
would still, eventually, shadow for some future name landing in `ProcessLex`).

**This sits AFTER the `-agent` reserved-tail check that opens the skill branch** (spec §3, one
reserved head `-agent`, illegal on a skill). The tail check runs first, unconditionally,
regardless of the token-zero head literal — which is what keeps `make-agent` PERMANENTLY
failing even though `make` is now a valid reserved head: `make-agent`'s tokens end in `agent`,
the tail check fires and returns before any head-token branch is ever reached. This is not a
special case bolted onto the new heads; it falls out of the existing branch order for free,
and the selftest fixture (D2's own regression, below) proves it by direct assertion rather
than by argument.

### D3 — ObjectVocab registrations (10 entries), the anti-ambiguity gate, and the `intake` reversal

Per spec §5's per-entry anti-ambiguity gate (no prefix collision with an existing multi-token
entry; no existing name's parse made ambiguous) — all PASS:

| # | canonical | plural | gate note | needed by |
|---|---|---|---|---|
| 1 | `experiment` | null | no conflicts | `experiment-runner` (ADR-0017) |
| 2 | `decision` | `decisions` | no conflicts | `decision-watcher` (ADR-0017) |
| 3 | `fact` | null | plural `facts` would dual-register against ProcessLex `facts`; nulling avoids it (dual membership is legal per the `stage` precedent, ADR-0014, but not needed here) | `fact-finder` (ADR-0017) |
| 4 | `code` | null | no conflicts | `code-checker` (ADR-0017) |
| 5 | `wording` | null | dual with TopicLex `wording` — redundancy, not ambiguity (TopicLex has no disjointness requirement, ADR-0014 D3) | `wording-checker` (ADR-0017) |
| 6 | `intake` | null | **reverses ADR-0016 §14.5 D3's non-goal** — see below | `lead-intake` retires via the existing `lead-` head; enables `intake-leader` (ADR-0017) |
| 7 | `reference` | `references` | no conflicts | `make-reference` |
| 8 | `rubric` | `rubrics` | no conflicts | `make-rubric` |
| 9 | `vision-memo` | null | multi-token; no existing entry starts with `vision`; left-anchored greedy match unambiguous | `make-vision-memo` |
| 10 | `llms-txt` | null | multi-token; no conflicts | `make-llms-txt` |

**The `intake` reversal, stated honestly rather than left implicit.** ADR-0016 §14.5 D3
declined registering `intake` "solely to clear one exemption" — a bar against dilution on
single-consumer evidence. The evidence has changed: at ratification there is one LIVE
consumer (`docs:lead-intake`, which conforms via the pre-existing `lead-` head the instant
`intake` resolves) plus one consumer this SAME change deliberately creates
(`docs:intake-leader`, the `intake-lead → intake-leader` rename executed alongside this
amendment under ADR-0017, conforming via `{scope=intake}-{role=leader}`). This is the
second-consumer bar ADR-0016 asked for, met prospectively rather than retrospectively — a
distinction this ADR states explicitly so no future reader mistakes this for a bar quietly
lowered on thread-comment authority. ADR-0016 is not edited; this citation is the entire
mechanism of the reversal, exactly as ADR-0011's partial supersessions work.

**Not registered (out of ratified scope):** the optional `component`, `flow`, `layout`
entries #464's proposal offered alongside B1–B10 — Kim's ratification covers Proposals A/B/C
only. `component-checker`, `flow-checker`, `layout-checker` (screens) and `make-component`
stay exempt pending a future amendment.

### D4 — What deliberately does NOT change (the fence)

- **The literal head set stays closed at exactly `{check, lead, make, file}`** — ADR-0014
  Alt C (generalize to all of `VerbLex`) stays rejected, restated for these two heads
  specifically, not reopened.
- **`make-agent` stays exempt, permanently** — same permanent-exempt class as the
  `check-all-*`/`check-everything` quantifier trio (ADR-0014's own ruling): the `-agent`
  reserved tail strips first (D2), so `make-agent` never reaches the head production under any
  future ObjectVocab growth. No amount of future registration changes this.
- **`file-leftovers` stays exempt** — `leftovers` fails the same single-consumer dilution bar
  as the deferred verb-head families; not part of this registration wave.
- **`VerbLex`, the `-rules` tail (§14.2 D1), the `check-`/`lead-` heads and their selftest
  triads, agent grammar (§3.3, ADR-0015/0017), the wrapper production** — all unchanged.
- **Command-branch recognition, per ADR-0016 D2's precedent:** if a `make-*`/`file-*` surface
  ever ships under `commands/` (none does today — all live instances are command-species or
  plain skills), the validator recognizes the head there too, mirroring ADR-0016's dual-branch
  posture. No code change needed today; noted so a future implementer does not have to
  re-derive it.

### Alternatives considered

- **Alt A — register `pack`/`plugin`/`skill`/`doc`/`script`/`hook` residues as compound tokens
  instead of a reserved head.** Killed: those residues already resolve as plain `ObjectVocab`
  members (`make-doc` etc. conform TODAY via the nominal production once the head exists) —
  the actual gap is the literal `make`/`file` heads themselves, not missing residue tokens.
- **Alt B — generalize `check-`'s mechanism to all of VerbLex (ADR-0014 Alt C, revisited).**
  Killed again, on the same grounds ADR-0014 stated: dissolves §3.1's object-first ergonomic
  for every verb to serve a few families; a closed, enumerable set of literals is the narrowest
  cut that clears the evidenced need.
- **Alt C — leave `intake` unregistered and let `intake-lead`/`lead-intake` stay exempt
  forever.** Killed: `lead-intake` and the RoleLex-conforming `intake-leader` are both real,
  live, growing consumers at ratification time — the exact bar ADR-0016 named as the one that
  would flip its own ruling.

## Consequences

- **Ratification provenance:** Kim ratified live (2026-08-17, AskUserQuestion via
  plugins-team-lead), per #464's proposal comment (Proposals B, C) and #477's execution
  ticket. A change of mind is a superseding ADR (this file stays append-only); the
  implementation below reverts by ordinary PR.
- **The follow-on execution (authorkit-owned, same PR as this ADR, executed same-change under
  this authorization):**
  1. `validate.py` `Grammar.parse`: the D2 head checks on the skill branch, in the verified
     slot (after `lead-`, before the `ProcessLex` terminal check, after the `-agent` tail).
  2. `naming.manifest.json`: `object_vocab` gains the 10 B-entries (D3).
  3. Validator selftest fixtures (mirroring §14.2/§14.5's triad): positive — `make-doc`,
     `make-reference`, `make-rubric`, `make-vision-memo`, `make-llms-txt`, `file-bug`,
     `file-task` parse clean; negative — a non-reserved verb head (`sort-issues`) still fails,
     `make-{unregistered}` still fails; regression — `make-agent` keeps failing on the
     `-agent` tail (the tail-before-head fixture this ADR names explicitly, D2).
  4. `authorkit/skills/naming-conventions/references/GRAMMAR.md`: Productions block, the
     reserved heads/tails line (closed set restated), and the lexicon table.
  5. `.claude/docs/spec/spec-naming-convention.md`: §3.2 prose gains the two productions; a
     dated **§14.7** appended mirroring §14.2/§14.5/§14.6's pattern.
  6. **ADR-0014 and ADR-0016 are not edited, then or later** — both accepted and append-only;
     the `intake` reversal (D3) and the head-set extension (D1) live in this file's body and
     frontmatter alone.
  7. Re-run `authorkit:naming-audit --scope grammar` estate-wide; combined with ADR-0017 in the
     same PR (§14.7 carries the joint before/after arithmetic against the ratification tree's
     measured baseline, not the proposal's projection, per this ticket's own instruction not
     to force a number that live state has moved past).
- **`intent-refs: null` is deliberate** — same posture as ADRs 0001–0017; the T6 orphan-ADR
  WARN is accepted as-is.
- **Easier, once landed:** 13 skill exemptions retire immediately (10 `make-*` + 3 `file-*`);
  `lead-intake` retires via the pre-existing head; every future `make-*`/`file-*` mint with a
  registered residue conforms from day one.
- **Harder, once landed:** the estate now carries four reserved skill heads beyond `-agent`
  (`check-`, `lead-` on the skill branch, `make-`, `file-`) — each future literal-head proposal
  must still clear the recurring-and-still-being-minted bar individually; the accumulating
  list remains the signal ADR-0016 D4 already named ("three literals is a grammar; ten would
  be a lexicon wearing a disguise") — now at four.
- **Irreversible in the ratchet sense:** 13 exemption retirements (plus `lead-intake`, 14 with
  ADR-0017's dependent rename) — D8's ratchet forbids re-growing the array, so a reversal ADR
  could not re-admit these by exemption; it would have to keep some conforming production or
  force renames. The `intake` registration is also a one-way door in the ordinary
  ObjectVocab-growth sense (D8 governs exemptions, not lexicon membership, but no proposal here
  suggests de-registering a live-consumed token).
