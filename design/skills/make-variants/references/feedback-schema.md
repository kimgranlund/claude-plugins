# feedback-schema — variant-feedback/v1

The versioned JSON contract `make-variants` serializes into every published artifact and
consumes on resume. This file is the contract's canonical source; the artifact's inline script
carries a generated copy, never a hand-diverged one.

## Shape

```json
{
  "schema": "variant-feedback/v1",
  "round": 1,
  "target": "pricing card component",
  "verdicts": [
    {
      "id": "compact-sharp-quiet",
      "axes": { "density": "compact", "corners": "sharp", "tone": "quiet" },
      "vote": "up",
      "note": "the sharp corners read as more premium"
    },
    {
      "id": "compact-round-loud",
      "axes": { "density": "compact", "corners": "round", "tone": "loud" },
      "vote": null,
      "note": ""
    }
  ],
  "overall": "",
  "grounding": {
    "sources": ["DESIGN.md", "src/tokens.css"],
    "resolved_version": "1.3.2",
    "hash": "sha256:9f2a…"
  }
}
```

`round` is a 1-based integer. `target` names what's being varied (a component name or a one-line
design brief) and stays constant across rounds. `verdicts` is one entry per rendered card, every
round — no card is ever omitted from the list, voted or not. `overall` is optional free text; a
"pick" (the terminating verdict) may be written there or in the accompanying chat message.

## Invariants

- **Stable IDs are axis-derived, not positional.** An id joins each declared axis's chosen value
  in the axes' declared order (axes `{density: compact, corners: sharp, tone: quiet}` -> id
  `compact-sharp-quiet`). The SAME axis combination gets the SAME id across rounds even if its
  card's screen position moves — resume mode keys anchors and mutations off this id, never off
  array index or DOM order.
- **`vote: null` is UNVOTED, never a downvote.** A card the user never touched serializes
  `vote: null`; every read site treats null and `"down"` as distinct. This bites hardest at
  resume: an unvoted axis combination HOLDS into the next round exactly like an anchor, while a
  downvoted one gets mutated — coercing null to a boolean collapses that distinction and silently
  discards untouched variants the user simply hadn't gotten to yet.
- **`verdicts` is exhaustive per round.** Resume mode cannot infer a dropped card's axes from a
  partial list — every card rendered that round has exactly one entry.
- **`grounding` is a pointer, never a payload** (optional, additive 2026-08-21 — the schema
  stays `/v1`; a blob without it is a legal ungrounded exploration). `sources` lists the
  substrate paths the round-1 Ground step resolved, `resolved_version` any version those
  sources declare, `hash` a content hash over them. The token VALUES live inlined in the
  artifact page itself — never in this blob, which travels through chat. Constant across
  rounds unless the user chooses to re-ground on a surfaced drift.
- **One schema key names one contract.** A pasted blob is resume-mode input only when its first
  top-level key is literally `"schema": "variant-feedback/v1"`. A differently-shaped or
  differently-versioned blob is not this skill's input — never guess-parse it into this contract.

## Resume-mode read

1. Parse `round`, `target`, `verdicts` (and `grounding`, when present) from the pasted blob.
   With `grounding`: re-hash its `sources` — match → reuse the pinned snapshot; mismatch → ask
   (re-ground or hold the pin) before rendering anything; missing sources → same question.
2. Partition verdicts by vote: `"up"` -> **anchor**, axes held fixed next round. `"down"` ->
   **reject**, axes mutated next round (pick a new value along at least one losing axis; never
   re-render the identical rejected combination). `null` -> **unvoted**, axes held fixed exactly
   like an anchor, but never cited as evidence FOR that direction — it's silence, not a signal.
3. Regenerate round `round + 1` republished to the SAME artifact file path (SKILL.md's
   one-artifact rule) — anchors' and unvoted combinations reappear as cards with their ids
   repeating by construction; rejects are replaced by new combinations along the mutated axis.
4. Terminate on a "pick" (a single winning id named in `overall` or the accompanying message) or
   an all-up round (every verdict `"up"`) — hand the winning axis combination as a spec to the
   requested build skill and stop.
