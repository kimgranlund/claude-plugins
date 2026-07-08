# mini-bundle — teaching fixture + gate fixture (receipt)

The smallest end-to-end Claude Design export bundle this skill considers well-shaped:
8 roles x 2 schemes, all four artifacts, every gate green. **A fixture, not a
production bundle** — it sits deliberately below the 15–25 role band (rubric B4)
to keep the shape readable; copy the shape, not the size. `scripts/bundle_gates.py
--selftest` gates this bundle green and a mutated copy red on every run.

Naming standard: Ultimate Tokens grammar `--{prefix}-{family}-{slot}`, prefix `c`,
families `neutral` / `primary`. Encoding standard: OKLCH in DESIGN.md frontmatter,
hex in tokens.json, `color-scheme` + `light-dark()` in the preview.

## Gate results (regenerate with any edit: `python3 ../../scripts/bundle_gates.py .`)

- G1 contrast: 12 pairs >= 4.5:1 both schemes (worst: light 6.25:1
  neutral-on-surface-variant / neutral-surface; dark 6.97:1 primary-on-primary / primary)
- G2 parity: 8 roles x 2 schemes, both carriers
- G3 carrier equality: OKLCH frontmatter == hex tokens.json within +-1/255
- G4 previews: 1 card, @dsCard line 1, self-contained, color-scheme + light-dark
- G5 references: all {group.token} references resolve
- G6 sections: 10 canonical sections in order; Responsive Behavior + Agent Prompt Guide present
- G7 required roles: primary present; every family base has its on-partner
- Divergences: neutral-outline-variant constant across schemes by design (translucent
  hairline — alpha rides in the value; not an on-color, so no DIVERGENCE line)
