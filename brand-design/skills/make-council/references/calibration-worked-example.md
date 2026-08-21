# Calibration worked example — step 6

A worked, disclosed walkthrough of standing up a minimal two-critic demo council end to end — the
PATTERN `make-council` step 6 asks for, not a shipped, permanently-registered new plugin skill (the
live end-to-end integration proof across the whole council-as-platform campaign is a later, separate
step's job, not this ticket's — see the SKILL.md's own "What this procedure does NOT do").

## Worked example — a tiny "release-notes" demo council

**Domain intake (per `references/domain-intake.md`):** artifact type = "a drafted release-notes
entry"; role families = `clarity` (does a reader understand what changed without reading the diff)
and `honesty` (does the entry overstate or understate the actual change) — two families, genuinely
distinct lenses, each catches what the other misses (a release note can be perfectly honest and
still unreadable, or perfectly clear and still spin a bug fix as a "performance improvement").
Roster size: one critic per family (below the 2-3 floor `domain-intake.md` recommends — disclosed
explicitly as a MINIMAL demo, not a production-ready roster; a real instance would want at least 2
per family).

**Critic shell:** a demo `release-notes-judge` agent, patterned off `brand-judge` per
`references/roster-and-chair-wiring.md`'s checklist — same input contract shape, same four-tier
severity labels.

**Chair:** `council-chair-agent`, reused unchanged, per the default.

**Calibration fixture (unpromoted, markdown-only):**

```markdown
Release note under review: "Improved performance and reliability across the app."

(Actual underlying change, for the critic's context: a null-pointer crash on the settings screen
was fixed; no performance work was done in this release.)
```

**Expected catch:** the `honesty` critic should flag "improved performance" as unsupported by the
actual change (a crash fix is not a performance improvement) — characteristic vocabulary: an
objection naming the mismatch between the claimed category (performance) and the actual change
(a crash fix), not a generic "be more specific" note. The `clarity` critic, reviewing the same
one-line note, has nothing to add here (single-defect fixture, one lens's ground) — a clean pass
from `clarity` on THIS fixture is expected, not a sign the panel is failing to be adversarial
(`council-rules`' own "a strategy council will not catch a typographic failure" framing, applied to
this domain's two lenses instead of brand's three).

## What this demo does not prove

It does not prove a `--deliberate` phase-2 round for this domain (a `council-chair-agent` dispatch was
never actually made here — this is a disclosed dry-run walkthrough, not a live run); it does not
register `release-notes-judge` or its critics anywhere durable in the estate. A live run through
this exact demo, and a decision on whether it's worth actually shipping as a real convening skill,
is explicitly out of this worked example's own scope.
