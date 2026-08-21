# Domain intake — the full worked checklist

Run this before drafting anything. Every question below has a wrong-answer failure mode worth
naming, because guessing here costs a rebuilt roster later, not a cheap edit.

## 1. What artifact type is under review?

Name it concretely — "a pull request diff", "a marketing landing page brief", "a product spec" —
never "whatever gets sent in." The artifact type decides what the new convening skill's own
"artifact under critique" argument means throughout its body, exactly as `check-brand-council`
fixes "brand work" as its own artifact type.

**Wrong-answer failure mode:** an artifact type stated too broadly ("any document") produces a
roster with no coherent shared ground — a critic panel needs to agree on what KIND of thing it is
adversarially reading, even while disagreeing about everything else.

## 2. Which role families does the roster need?

Ask: what are the genuinely distinct, real-practitioner points of view a panel for this artifact
type would assemble? Brand's answer was strategy / design / voice — three genuinely different
professional lenses that each catch what the other two structurally miss (`council-rules`'
`references/roster-and-personas.md`, "the blind-spot handle"). A new domain's answer might be
completely different in count and shape:

- **Code review** might split into correctness/security · architecture/maintainability ·
  performance — three lenses a real senior engineering panel would bring.
- **Marketing copy** might split into brand-voice fidelity · persuasion/conversion craft ·
  legal/claims accuracy.

**Wrong-answer failure mode:** inventing role families that are really the SAME lens phrased twice
(the overlap `make-critic` step 2 checks at persona granularity, checked here at family
granularity first) — verify each proposed family would catch a defect the others would miss before
finalizing the split.

## 3. Minimum viable roster size

`council-rules` fixes no number, by design (it is domain configuration). As a floor:

- Each sub-council needs at least 2 members to run at all, and ideally 3 to make a same-sub-council
  2-of-3 contested-finding vote possible without borrowing a third critic from outside the lens
  (`council-rules`' `references/severity-and-voting.md`).
- A sub-council with exactly 2 members needs a documented fallback for a contested finding (borrow
  a third opinion from an adjacent sub-council, or log `hung` more often — state which, don't leave
  it implicit).
- `full` (the union of every sub-council) needs no separate minimum — it inherits whatever the sum
  of the sub-councils already is.

## 4. Is a sub-council split earned at all?

A domain with genuinely one coherent lens (a narrow artifact type reviewed by one kind of
practitioner) does not need sub-councils invented to look more like the brand instance. State this
explicitly in the new skill's own body — "this instance runs `full` only, no sub-council split,
because <reason>" — rather than manufacturing a second family with one member each just to have a
table with more than one row.

## Output of this step

A short intake summary (artifact type, role families with one-sentence justification each, roster
size per family, sub-council-or-not decision) that step 2 of the main procedure (minting the new
convening skill) drafts directly from — never re-derived from memory later in the build.
