# The audit methods themselves — how to run this kind of review

**The judgment call:** the six axes above are the FINDINGS species this pack teaches judgment
about; this axis is the METHOD that produces them. All three source corpora arrived at their
verdicts using variations on four concrete techniques, each reusable on a different codebase.
Running the techniques in this order — sync-point mapping, then bypass inventory, then coherence
mapping, then doctrine-vs-practice diffing — is what turns "there seems to be a mix of
implementations" into a ranked, citable finding list instead of a vibe.

## 1. Sync-point mapping [verified]

Build a table: every place a given fact is held (a mechanism inventory), each row naming its
`Home` (file:line), what it `Holds`, its `Propagation` mechanism, and a `Judgment` verdict
(signal-clean / manual-sync / manual-sync-by-convention / write-only-no-read-path). Then, as a
SEPARATE section, number the "sync-point map" — the specific places where two rows above disagree
about who owns a fact, each written as its own numbered finding with a file:line citation. This is
exactly agent-ui's `agent-admin-app-state-audit.md` method: the mechanism table surfaces every
CANDIDATE owner; the sync-point list is the CROSS-REFERENCE pass that finds where two candidates
collide. Running the table alone, without the explicit cross-reference pass, misses the bug class
this pack's `one-name-two-owners.md` and `two-facts-one-name.md` axes name — the table shows what
exists, the cross-reference is what shows what conflicts.

## 2. Bypass inventory [verified]

For each SANCTIONED layer (a ratified ADR, a "the one seam every consumer reaches for" contract),
build two lists side by side: real consumers (grep the actual import graph, not the ADR's stated
intent) and bypasses (every site-level module doing the same job outside the sanctioned seam,
with its own file:line). Then state the adoption verdict per layer explicitly —
built-but-unadopted, load-bearing-with-bypasses, or genuinely clean — rather than one estate-wide
"there's some drift" sentence. This is agent-ui's `data-persistence-layers.md` method; see
`adoption-verdict.md` for the judgment this technique feeds.

## 3. Coherence mapping [verified]

Build one table across the WHOLE codebase's layers (primitive/composite/shell/app/runtime, or
whatever tiers the specific stack has), one row per layer, with a `Model in practice` column and
a `Coherence` rating (HIGH/MEDIUM/LOW) plus a one-clause reason. Then rank the prose findings by
which layers scored LOW, not by which layer the original symptom was noticed in. This is gen-ui-
kit's `INDEX.md` method — see `doctrine-vs-practice.md` for the worked table and the judgment it
produces. The coherence map is what proves (or disproves) a "the mix is real but concentrated in
N places" verdict instead of asserting it.

## 4. Doctrine-vs-practice diffing [verified]

Run two independent passes and don't conflate them: (a) inventory the CODE's actual state
patterns (techniques 1–3), and (b) INDEPENDENTLY inventory the ratified DOCTRINE's own numbered
rules, sourced to their ADRs/specs, without reference to the code survey. Diff the two — code
patterns doctrine doesn't sanction, AND doctrine passages that contradict each other internally
(a live claim mismatch, a stale count, a frontmatter-vs-body inversion) are two DIFFERENT
findings classes; the second class exists even when the code perfectly follows one of the two
contradicting doctrine passages. This is gen-ui-kit's `04-doctrine-vs-practice.md` method (Part 1:
ratified rules with sources; Part 3: contradictions between doctrine documents, independent of
any code survey) cross-referenced against `INDEX.md`'s code-side layered map.

## Running the four together

The three corpora this pack draws from ran these techniques with different emphasis (agent-ui
leaned on 1+2 for one symptomatic app; gen-ui-kit leaned on 3+4 for a whole framework; adia-v2 ran
a six-axis version of 1+2 and named the meta-pattern directly in its own synthesis, see
`adoption-verdict.md`'s "fixed once never swept" corollary) — none of the three needed all four
run with equal weight to reach a citable, ranked verdict. Pick the technique(s) that match the
scope of the "mix of implementations" complaint: one symptomatic app → sync-point mapping first;
a whole framework/plugin family → coherence mapping + doctrine diffing first; a persistence or
cross-cutting-concern audit specifically → bypass inventory first.

## Sources

`/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/` (five of
the corpus's six files consulted for method — `follow-up-queue.md` is Kim's ticket-triage log, not
method content — technique demonstrated across `agent-admin-app-state-audit.md` +
`data-persistence-layers.md`);
`/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
+ `04-doctrine-vs-practice.md`; `/Users/kimba/Projects/adia/adia-v2/.claude/docs/reports/2026-08-20-reactivity-data-audit/00-index.md`.
