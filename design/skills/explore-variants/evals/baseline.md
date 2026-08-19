# Baseline — explore-variants (documented-delta form)

Per the accepted-with-note pattern the ticket's source intent record already used: this baseline
is recorded as a description of current no-skill behavior rather than live fresh-session
captures. The behavior delta is structural — a feedback CONTRACT (declared axes, per-card
three-state vote + note widgets, a versioned resumable JSON schema, a stable republish URL) that
cannot exist without the skill — so a no-skill baseline trivially lacks every element of it; there
is no ambiguous middle case a live capture would need to adjudicate.

## What Claude produces today, without this skill, on the trigger prompts

- **"explore variants of this component" / "give me 5 takes on this layout":** one design, or
  several ad-hoc takes rendered as separate messages or an unlabeled artifact — no declared axes,
  no stable per-variant id, no vote/note widget, nothing serialized for the next round to consume.
- **User reactions ("I like the second one but make it more compact"):** arrive as prose in the
  next chat turn. The next generation has to re-parse free text to figure out which variant and
  which axis changed — lossy, and nothing is ever explicit about which axes were even varied.
- **Resuming a prior exploration:** no mechanism exists; each new request starts over, and a new
  artifact typically gets a new URL — no "same URL, next round" contract.

This is the gap `evals/assertions.md`'s five assertions check against — each assertion states a
concrete artifact-level fact the baseline behavior above has no equivalent for.
