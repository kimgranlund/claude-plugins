# Choosing a concrete font per family slot

Designing which typeface fills each of the five `--font-*` roles (`display · heading · body · ui
· mono`) from a brand concept or creative brief is `typography-system-design`'s job — it interprets
the brief into a specific point in design space, makes the distinctive-vs-neutral call per voice
with a stated rationale, sets the pairing/contrast drama, and verifies metric compatibility before
handing the decision here for realization as bound CSS custom properties. Route there for the full
treatment: territory interpretation, the deepened per-voice judgment, the verified metrics table,
the categorized font register, and the `typeface-check.py` craft-correctness checker.

This file gives only a **fallback heuristic** for the (rarer) case where no brief, brand system, or
prior art-direction decision exists at all — a placeholder call to unblock a build, not a substitute
for a designed decision.

## The fallback: distinctiveness by slot, absent any other signal

| Slot | Default absent a brief |
|---|---|
| `--font-display` | distinctive if the surface is brand-forward/marketing/editorial; neutral if the "hero" is itself dense information |
| `--font-heading` | distinctive in editorial/content-brand products; neutral in enterprise SaaS with heavy i18n |
| `--font-body` | neutral by default — long-form editorial reading is the exception, not the rule |
| `--font-ui` | neutral almost always — chrome legibility outweighs personality |
| `--font-mono` | neutral almost always; distinctive only for a code-aesthetic brand (dev tools, terminal-flavored products) |

The pattern: **display, headline, kicker, and code are where a distinctive face earns its keep**;
**body, label, and tiny default to neutral** — legibility-at-small-sizes and broad script
coverage usually outweigh personality on those voices. A project's own brand system or an existing
type spec always overrides this fallback; when it does, the obligation is to state the reason
(a brand mandate, an existing type system, a platform constraint), not to silently default to
whatever's familiar.

## Boundary

This file is the no-brief fallback only. For a real brand concept, creative brief, or
visual-territory description — the actual per-voice design decision, its rationale, the pairing
drama, and the verified metric-compatibility check — use `typography-system-design`, then return
here to bind its decision to `--font-*`.
