# Foundations — why these four tests, and only these

## The router routes on descriptions, so vocabulary is not a style choice

Skill selection is the model reading the description menu in its context and choosing — there is no
separate lexical matcher (amended on import, 2026-07-07: the source corpus stated this as a lexical
router; the verified mechanism is model-as-router, but the failure surface is the same). Overlap
between task phrasing and a description's trigger words is still what decides close calls, and
`/eval-run`'s stolen/leaked failure shapes measure it empirically. This is the load-bearing fact
the whole method rests on: **a split that gives two children overlapping trigger vocabulary does not create
two skills — it creates one skill with two unreliable coin-flips for an entry point.** Test 3
(vocabulary separability) is therefore not a nicety; it is the mechanism by which a bad split fails
silently, at query time, months after the refactor looked clean on paper.

## A knowledge pack's real unit of decomposition is the *question type*, not the file count

File count is a proxy, and a misleading one on its own. `color-contrast-facts` is defensible
at 8 files because APCA/WCAG/CVD is a genuinely distinct *question type* — a user asking "which
standard applies" is never simultaneously asking "how do I mix pigment." `color-theory-facts`'s four
"axes" are not distinct question types; they are four lenses on one question ("does this color
choice read as intended, and why"), and no amount of file-count padding turns four lenses into four
skills. When sizing a split, ask **"is this a different kind of question, or the same question asked
a different way?"** before counting files.

## Ask co-occurrence is the empirical version of the vocabulary test

Vocabulary separability can be argued from the description alone; ask co-occurrence proves it
against real queries. A corpus's own routing-corpus positives (or task-prompts, if the pack has an
`evals/` folder) are the cheapest available ground truth — they were written by whoever built the
pack to represent what users actually ask. Mapping each positive to the axis or axes it needs is
mechanical and reveals the same signal test 3 predicts, but empirically: if most real asks need two
axes, the pack's authors already discovered, by writing their own test corpus, that the axes don't
separate.

## The cost of a split is asymmetric with its benefit, and both must be named

A split's cost is concrete and front-loaded (N new descriptions, N routing corpora, a referrer
rewire across every sibling that ever cited the parent). Its benefit — cleaner retrieval, less
context loaded per query — is diffuse and only realized if the split actually reduces what an
average query loads. **State the benefit as a number, not an adjective**: how many fewer files does
a typical query load post-split versus pre-split? If the honest answer is "about the same, because
most queries needed most of the corpus anyway," the split has no benefit to net against its cost,
and the ledger is negative regardless of file count.

## Rejection discipline generalizes past whole-corpus verdicts

The color-science plan did not stop at "should the whole 159-file corpus split?" — it re-ran the
same tests on *candidate sub-splits within an already-justified split* (a 5th `palette` pack, a 5th
`naming` pack) and rejected both. The four tests are not a one-time gate at the top of a
decomposition; they apply recursively to every candidate boundary, including boundaries inside a
pack that is definitely splitting. A good decomposition names what it did *not* fragment as
carefully as what it did.

## A no-split verdict is not a failure of the exercise

`color-theory-facts`'s verdict — tested rigorously, documented, rejected — is exactly as valuable a
deliverable as `color-science`'s four-way split. The method's job is to find the truth of the
corpus's shape, not to manufacture a family because one was requested. A skill that always
recommends splitting (or always recommends against it) has stopped running the tests and started
performing a foregone conclusion.
