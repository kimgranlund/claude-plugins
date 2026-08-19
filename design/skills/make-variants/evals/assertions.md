# Behavioral assertions — make-variants

Checkable statements about the output of a with-skill run, compared against the documented
no-skill baseline (`evals/baseline.md`). All five hold for a compliant run.

1. **N cards, each labeled by its declared axes.** The published artifact renders N variant
   cards (N >= 2), and every card's DOM shows the axis/value pairs that produced it — never an
   unlabeled visual difference the user has to infer for themselves. The baseline (no skill)
   produces at most prose-described differences, no per-card axis labels.
2. **Every card carries a working three-state vote + note widget.** Each card's vote control
   supports up / down / unvoted (never a forced binary), and a free-text note field is present
   and editable. The baseline offers no structured per-variant feedback affordance at all — only
   a chat reply the next round can't parse.
3. **A live, schema-valid `variant-feedback/v1` JSON block is present and copyable.** The block
   updates as votes/notes change, its first top-level key is literally
   `"schema": "variant-feedback/v1"`, and a copy affordance is wired (`navigator.clipboard`, with
   a `select()` + `execCommand('copy')` fallback). The baseline emits no such block.
4. **Republishing preserves the URL.** Regenerating a round (fresh request or resume) writes to
   the SAME artifact file path as round 1 — the published URL does not change across rounds. A
   baseline run (no skill) has no round concept and no path-stability guarantee to compare
   against; this assertion is checked by inspecting two consecutive with-skill rounds' file paths.
5. **Resume mode respects the null-vs-down invariant.** Given a pasted `variant-feedback/v1` blob
   with a mix of `"up"`, `"down"`, and `null` votes, the regenerated round holds anchors (`up`)
   and unvoted (`null`) axis combinations unchanged while only `"down"`-voted combinations get a
   mutated axis value — an unvoted card is never silently treated as rejected.
