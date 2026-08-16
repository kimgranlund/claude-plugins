# The Product Lifecycle Bible
## How we build — the canonical reference

**v1.1.0 · 2026-08-13 (v1.1.0: gradual context-building named as a principle — Part 5, Kickoff, anti-patterns) · sourced from the internal doctrine corpus (v2.3.0); on any disagreement, the corpus wins. The companion one-pager ("How We Build") is this document's abstract.**

**How to read this:** Parts 1–3 are the read-through — the idea, the loops, the lifecycle. Parts 4–8 are the lookup — the alignment docs, the knowledge base, the rules, the metrics, the anti-patterns. Part 9 is the glossary. New joiners read the whole thing once (~15 minutes); after that, you consult it.

---

## TL;DR

- **The durable output of product work is the knowledge the software is built from.** Software is the snapshot; the knowledge base is the compounding asset. Every executor — engineer, contractor, AI agent, your own team in six months — starts cold and inherits only what was written down in a consumable form.
- **Three nested loops:** North star (thesis) → Foundation (architecture) → Releases (what ships). Outer loops hold assumptions and turn slowly; inner loops produce evidence and turn fast. Version numbers read off the loops: thesis 2 · architecture 2.3 · release 2.3.17.
- **One turn of the build loop:** Kickoff → Explore & prototype → Spec lock → Build → Verify → Ship → Retro, written down. Spec lock is the only hard gate.
- **Three alignment docs:** **IDR** (Intent Decision Records) · **ADR** (Architecture Decision Records) · **PRP** (Product Release Plans). Each loop keeps one living index and one locked record type. Releases lock; the roadmap breathes.
- **Context is grown, not authored:** born as homes on day 0, grown by harvest in the cheapest durable form, matured by pruning — robust means small, current, and load-bearing, earned over loop turns.
- **The habits:** explained twice → write it down · one home per fact · docs are searched, not read · rules become checks · a DRI can explain what shipped · every defect is called as bug or requirement gap.
- **The score:** relearn rate — how often we re-purchase a lesson we already captured. Target: never.

---

# Part 1 · The idea

Building software has become cheap. AI agents and AI-assisted engineers produce working systems quickly and keep getting faster. What has *not* become cheap: knowing what to build, why, and what is true about the domain.

Two mechanics drive everything in this document:

**Executors start cold.** A new engineer, a contractor, an AI agent, your own team in six months — each begins with an empty context and inherits only what crosses its boundary as a consumable artifact. Knowledge in heads and hallways does not transfer. For humans this was masked by charitable interpretation and hallway bandwidth; agents enforce it literally.

**The constraint moved upstream.** When execution was the expensive stage, we optimized engineer-hours and tolerated fuzzy intent — clarification could catch up. With execution abundant, the bottleneck is the supply of clear, testable intent and trustworthy context. A cheap executor fed poor context produces the wrong thing, sooner, at scale.

Therefore: **the highest-leverage, longest-lived asset a product team produces is its knowledge base** — captured intent, recorded decisions, domain truth with one home each. Good software can be rebuilt from good knowledge, to the contract that defines it. Good knowledge cannot be rebuilt from software, and never from memory.

# Part 2 · The three loops

Product work runs as three nested loops. Nesting is semantic: scope, cadence, and authority all follow from loop depth.

| Loop | Focus areas | Objective | Alignment doc | Turns · a turn means |
|---|---|---|---|---|
| **North star** (outer) | Intent capture · domain & market knowledge · core-loop and first-principles hypotheses · the proof of concept · the knowledge base itself | **Validate the product thesis:** prove the core loops, first principles, and first-class services with a running POC, and build the foundational context everything downstream mounts | **IDR** · index: the product brief | Slowest (yearly-ish) · a hypothesis superseded on evidence: a **pivot** |
| **Foundation** (inner) | Applied design · foundational systems and services · the test/CI/enforcement backbone · engineering patterns | **Turn validated hypotheses into production-grade architecture** — make quality structural, not supervisory | **ADR** · index: the architecture overview | Quarterly-ish · re-architecture within a standing thesis |
| **Releases** (innermost) | Deployment & operations · shipped releases · customer feedback intake · the roadmap | **Serve users and learn from production:** perform the product's intended duties, route feedback as evidence, compound the roadmap from what ships | **PRP** · index: the roadmap | Weekly/continuous · a release |

**Loop mechanics.**
- *Containment:* inner loops work inside the outer loops' standing decisions and never edit them directly — they emit evidence outward.
- *Escalation:* evidence that stays in scope iterates the current loop. Evidence that breaks an assumption held one loop out climbs to that loop as a new record version, reason attached. A release finding that breaks a design assumption triggers a Foundation turn; foundation experience that falsifies a product hypothesis climbs to the North star as a recorded pivot.
- *Version triple:* outer turn ≈ major, inner ≈ minor, innermost ≈ patch. "Thesis 2, architecture 2.3, release 2.3.17" is a complete status report.
- *Concurrency:* loops differ in emphasis, never exclusivity — all three run at once when the product is live. An outer loop that never turns is dogma; one that turns monthly is churn.

**The POC boundary.** The North star's first turn ends with a fairly complete proof of concept that functionally proves the core hypotheses. The POC's *code is evidence, not product.* The Foundation loop inherits the **validated hypotheses plus the knowledge base — never the POC codebase** — and rebuilds to the contract at production grade. Keep the knowledge; regenerate the artifact. This ends the throw-away-the-prototype debate by making it a non-question.

**Deliverables by loop.** North star: product brief, IDRs with proof references, the POC, the domain & market layer (glossary, indexed walkthrough videos, failure ledger, annotated prototype), the knowledge base stood up at kickoff. Foundation: design docs and ADRs, foundational services and platform code (the first loop where code *is* the product), the test/CI/enforcement backbone, promoted engineering patterns. Releases: PRPs with acceptance criteria, specs that point at the source of truth, shipped releases and changelogs, the living roadmap, feedback routed as evidence, the ops layer (dashboards, runbooks). Each loop's headline deliverable is the next loop's starting context — you never hand an inner loop your *work*, you hand it your *record*.

# Part 3 · The build loop, stage by stage

One turn, seven stages. Spec lock is the only hard gate; everything else overlaps by design.

**1 · Kickoff.** The brief is written *from* the knowledge base — prior decisions and domain terms referenced, not rediscovered — and the project's knowledge base stands up the same day: a home for every kind of fact before real work starts. Draft IDRs open here. *Done when:* every kind of fact has a home — **homes, not content.** Day 0 builds the shelves, not the library: context is never backfilled and never big-banged; it accumulates in place from the first conversation.

**2 · Explore & prototype.** Requirements, prototype, and design evolve together; the prototype is intent made runnable, and it transmits more intent per unit of attention than prose — to humans and doubly to machines. Corrections arrive hourly here: this is the harvest window. *Done when:* anything explained twice is written down, and every draft hypothesis has a draft test.

**3 · Spec lock.** Acceptance criteria lock — each testable, each backed by a demo or test. The lock exists because Verify needs a frozen reference point: bug-vs-requirement-gap is only decidable against a locked spec. *From here:* changes are new versions with reasons, never silent edits.

**4 · Build.** Team plus AI tools build from the knowledge base. Specs *point* at the source of truth instead of paraphrasing it — every re-summary hop loses fidelity, so the executor at the end of the chain reads the original. Checks run inside the build, not after it.

**5 · Verify.** Human judgment on top of continuous checks. Every defect is called: **bug** (fix in place) **or requirement gap** (update the requirement, on the record, as a new IDR version). *Done when:* a **DRI signs off who can explain what shipped** — work a reviewer cannot explain back is a defect here, not a style issue.

**6 · Ship.** Boring, because deployment was rehearsed continuously.

**7 · Retro — written down.** Not a meeting that evaporates: lessons, corrections, and why-we-changed-our-minds land in the knowledge base, where the next kickoff reads them. *The test:* the next kickoff starts smarter than this one did.

# Part 4 · The alignment docs: IDR · ADR · PRP

Each loop keeps **one living index + one locked record type.** The records are how decisions stay traceable and assumptions stay contestable.

| | **IDR** — Intent Decision Record | **ADR** — Architecture Decision Record | **PRP** — Product Release Plan |
|---|---|---|---|
| Loop | North star | Foundation | Releases |
| Unit | One testable hypothesis or outcome claim | One system decision, rejected alternatives included | One release: scope, acceptance criteria, sequencing |
| Admission test | Would two reasonable builds differ on it? | A choice someone will later ask "why" about | Could two reasonable teams ship different releases from this roadmap line? |
| Contains | Claim · why · proof reference (test, demo, prototype state) | Decision · context · alternatives rejected and why · IDR citations | Scope · acceptance criteria (IDR-grammar, feature grain) · sequencing · citations · DRI · completion clause |
| States | Draft → locked at Spec lock → superseded-with-reason | Proposed → accepted → superseded-with-reason | Draft → locked at release commitment → shipped-and-archived, or superseded-with-reason |
| Cites upward | — | ≥1 IDR | ≥1 ADR and/or IDR |
| Living index | Product brief | Architecture overview | **Roadmap — releases lock, the roadmap breathes** |

**Rules that make the records real.** Locked records are never edited in place — a change is a new version citing its predecessor and the evidence that forced it; the "why we changed our minds" chain is the most valuable intent material the org owns. An ADR with no IDR citation is an orphan (a decision serving no recorded intent). An IDR with no downstream citations after Build is unimplemented intent. A shipped PRP left "active" is a false fact a future reader will absorb as true.

**Escalation rides the citations.** A PRP repeatedly failing against the same ADR is evidence for an ADR revision. An ADR falsified by build reality climbs to an IDR revision. Which record does this evidence contradict? Fix at that grain.

# Part 5 · The knowledge base

**Robust context is grown, not authored.** The knowledge base follows a maturation arc, and every stage of it is event-driven rather than scheduled:

1. **Born as homes** (Kickoff) — structure before content: a place for every kind of fact, nearly empty.
2. **Grows by harvest** — captured at the moment a truth surfaces, in the *cheapest durable form* (a rough note, an ugly screen recording); refinement is earned by recurrence, never done speculatively. Growth follows evidence — a fact enters because someone needed it, not because a template had a slot.
3. **Evolves under amendment** — wrong claims get dated corrections; decisions get superseded; nothing silently rewritten.
4. **Matures by pruning** — lines that stop changing behavior get deleted. **Robust means small, current, and load-bearing — a state you earn over turns of the loop, not a deliverable you write.** A growth curve that never bends is rot, not health.

The compounding is the point: each loop turn deposits, amends, and prunes, so the knowledge base a project has at thesis 2 is one no team could have authored at day 0 — it is the residue of every correction, defect adjudication, and pivot, kept current. That is what makes it trustworthy enough for executors to build from.

**The source of truth, actually enforced.** Every fact has exactly one home; everything else references it. A restated fact is a copy with no synchronization protocol — divergence isn't a risk, it's the steady state.

**Searched, not read.** The knowledge base is an index executors pull from just-in-time, never a payload loaded wholesale — for AI agents this is a hard technical requirement (large loaded contexts degrade output), not a preference. Author dense; consume sparse.

**The grounding doc.** Every repo carries one (in practice, `CLAUDE.md`/`AGENTS.md`): one screen that takes an executor from cold to oriented. Five sections in priority order — identity, the never-do invariants, the trigger→home routing map, how to work here, what done means. It *points* at the knowledge base; it never *is* the knowledge base. A grounding doc that grows per incident has a routing problem, not a documentation problem.

**The domain layer — what a prototype can't carry.** Short indexed walkthrough videos (3–8 minutes, one topic, recorded while fresh) · annotated prototypes (notes pinned to screens, each marked *hard rule* or *just an example*) · decision records with the rejected alternatives · a living glossary (one home per term) · a failure ledger (what we tried, why it died, one line each). **The indexing rule:** every media artifact gets a one-paragraph text index in the knowledge base, or it's a large file, not knowledge.

# Part 6 · The habits

1. **Explained it twice? Write it down.** The third telling should already be an edit — a pattern, a record, or an automated check.
2. **One home per fact.** Reference, never restate.
3. **Rules that matter become checks.** A convention living only in prose is a promise with a half-life of one reorg; machine-checkable rules run automatically and never soften their findings to keep a meeting pleasant.
4. **Fix with a date; never erase.** Wrong claims get dated amendments. Decisions get superseded, never rewritten — an edited decision is forged institutional memory.
5. **A DRI can explain it.** Checks verify; a named human answers.
6. **Plans die into the archive.** On completion, learnings promote out and the plan archives. Nothing stays "active" that isn't.
7. **Prune.** Every line in the knowledge base must change what an executor does — remove it and someone's work gets worse — or it gets deleted. A healthy knowledge base is small.

# Part 7 · What we measure

- **Relearn rate** — how often the org re-purchases a lesson it already captured. Target: trending to zero. *(Being instrumented before we make external claims on it.)*
- **Turn rates per loop** — healthy products release constantly, re-architect occasionally, pivot rarely-but-not-never.
- **Comprehension** — can the people who shipped it explain it? Measured at Verify via explain-back; a failing answer is logged as a defect.

# Part 8 · Anti-patterns, named

| Anti-pattern | Why it fails |
|---|---|
| **Roadmap as contract** | The roadmap is the living index over PRPs; committing the index freezes learning. Releases lock instead |
| **Renegotiating a locked PRP without a version** | Silent renegotiation destroys the record's meaning |
| **Backfilled documentation** | Context written after the fact is reconstruction from whoever still remembers; capture happens during Explore |
| **POC ossification** | Shipping the prototype codebase into production skips the rebuild-to-the-contract step; inherit the knowledge, not the code |
| **The growing grounding doc** | Per-incident growth means lessons aren't routing to skills and checks |
| **Restated facts** | Every copy is a future contradiction |
| **Docs for docs' sake** | Fails the pruning habit; documentation is judged by behavior change, not coverage |
| **The big-bang knowledge base** | Authoring "robust context" upfront produces speculation, not knowledge — robustness is grown through the harvest/amend/prune arc, and a day-0 library is a day-0 drift farm |

# Part 9 · Glossary

**IDR** — Intent Decision Record: one testable hypothesis with a changelog. **ADR** — Architecture Decision Record. **PRP** — Product Release Plan (a launch plan). **DRI** — Directly Responsible Individual: the named human who can explain what shipped. **Acceptance criteria** — the testable conditions locked at Spec lock; collectively, the rubric. **Pivot** — a North-star turn: a hypothesis superseded on evidence, on the record. **Knowledge base / source of truth** — the project's captured context: skills, records, glossary, domain layer. **Grounding doc** — the one-screen entry point that orients a cold executor. **Harvest** — returning lessons to the knowledge base as a scheduled step, not a hope. **Relearn rate** — the score: how often we re-learn what we already knew.

---

**What this is not:** not waterfall — the loops run concurrently, stages overlap, and Spec lock is the only hard gate. Not documentation for its own sake — the pruning habit cuts anything that doesn't change behavior. And not AI replacing judgment — machines took the typing, so human time concentrates where it was always scarce: deciding what's worth building, and standing behind what shipped.
