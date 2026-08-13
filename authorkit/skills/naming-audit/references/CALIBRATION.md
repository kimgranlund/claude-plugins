# Calibration — findings from authorkit's own first audit (2026-08-13)

The validator's first target was this plugin. Findings and the calibration
they set:

1. **Wrapper commands initially failed the object-verb production.** The
   command `naming-audit` (wrapping the skill) has terminal `audit` ∈
   ProcessLex, not VerbLex. Resolution: the wrapper production — a command
   name identical to its wraps target passes by wrapper identity. Calibration:
   a command failing object-verb is checked for a wraps declaration BEFORE
   being reported as a violation.
2. **The reference index check caught its own scaffolding.** Files created in
   references/ before their index rows were written failed
   'missing from reference index'. Calibration: index findings during active
   authoring are ordinary red-green, not estate rot; in an audit report they
   are real errors.
3. **Coherence checks caught a draft where rename-execute declared
   mutates: true before its Edit grant was added.** Calibration: policy/grant
   incoherence is a high-signal finding — in every observed case it meant the
   frontmatter and the body were written at different times, which is exactly
   the drift the check exists for.
4. **Steady state:** authorkit validates clean with an empty exemptions
   array. Any future authorkit release that requires a self-exemption is a
   spec bug, not a name bug.
