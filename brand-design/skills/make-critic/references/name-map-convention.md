# The `.name-map.md` attribution discipline — canonical home

**This file is the canonical documentation of the convention** — every existing persona file's
"_Lens distilled from a real, widely recognized ... practitioner. The attribution, bio, and sources
live in the git-ignored `.name-map.md`_" disclaimer implements what's stated here; before this
ticket, the convention existed only as that repeated disclaimer line with no single owning
document. `make-critic` step 4 points here; nothing else restates this.

## Why the map exists at all

Every persona is deliberately **distilled from** a real, identifiable practitioner's public body of
work and point of view — that's what gives a lens genuine authority instead of a generic invented
opinion. But the tracked, committed persona file (`critic-<handle>.md`) never names that real
person, carries their bio, or cites their sources directly. Two reasons, both load-bearing:

1. **Consent and attribution risk.** A committed, publicly-readable file that puts adversarial,
   sometimes harsh critique in a specific named real person's mouth — without that person's
   knowledge or consent — is a live reputational and potentially legal exposure the moment the
   persona is used to critique someone else's real work. The persona is a LENS inspired by a real
   point of view, not a puppet of a named individual, and the file must never blur that line.
2. **The lens survives independent of the mapping.** Handles (`luke-s`, `paula-s`) let a dispatcher,
   a roster table, and every downstream reference stay stable and namable without that stability
   depending on a sensitive fact staying secret by convention alone — it's structurally kept out of
   the tracked tree instead.

## The mechanism

- **`.name-map.md` lives at the council's own skill root** (e.g.
  `check-brand-council/.name-map.md`), is listed in `.gitignore`, and is **never committed** —
  verify it is actually ignored (`git check-ignore` or equivalent) before the first write, not
  assumed from the filename alone.
- **One entry per handle**, plain and undecorated — handle, the real practitioner's name, a short
  bio, and the sourcing that grounded the distilled lens (interviews, published work, a body of
  writing). No fixed schema is mandated beyond "enough for a future maintainer to trace the lens
  back to its real root" — this is private working material, not a publishable record.
- **The tracked persona file never references the map's contents**, only its existence — the
  standing disclaimer line ("The attribution, bio, and sources live in the git-ignored
  `.name-map.md`") is the ONLY place the map is mentioned in tracked material.
- **A new council instance (`make-council`) gets its own `.name-map.md`**, gitignored the same way,
  from its first critic — this is not a brand-design-specific convention, it is the general
  discipline every council instance inherits the moment it mints its first `make-critic`-drafted
  persona.

## Failure branches

- `.gitignore` doesn't yet cover `.name-map.md` for a brand-new council skill directory → add the
  rule in the same change that creates the file (`.claude/rules/gitignore-repair.md`'s own
  discipline, applied at mint time rather than retirement time — the same duty, opposite
  direction: a NEW gitignored path gets its rule the moment it's created, not retrofitted later).
- A real name or sourcing detail is found already leaked into a tracked persona file (a pre-
  existing file, or a draft not yet committed) → strip it immediately, move the material into
  `.name-map.md`, and treat the leak as a finding worth naming in the build's own report — never a
  silent fix with no record.
