# Root Brand Architecture

Tokens make output *consistent*; brand architecture makes it *recognizable*. A DESIGN.md with tokens but no architecture generates competent, anonymous UI — the single most common failure of generated design specs. This layer is what "enough captured for generation" means.

## The six slots

Fill every slot with **committed lines that carry a design consequence** — adjectives without consequences are padding.

### 1. Values (3–5)
What the brand believes, phrased so a design decision falls out of it.

- ✅ "Restraint over decoration: whitespace, hierarchy, one decisive action per view." *(consequence: agents cut elements, not add)*
- ❌ "We value simplicity and delight." *(no decision falls out)*

### 2. Voice
Person, casing, punctuation, emoji policy — each as a rule with an example.

- Person: who speaks to whom ("second person for instructions; the system refers to itself in third person").
- Casing: sentence case vs Title Case; where ALL-CAPS is legal (often: nowhere except a tracked kicker).
- Punctuation signatures: em-dash asides, backticked tokens, oxford comma stance.
- Emoji: a policy, not a vibe ("not part of the product voice; confined to receipts/checklists" — or wherever the brand actually stands).
- 2–3 **verbatim example phrasings** to pattern-match: "Reason over roles, never raw hexes."

### 3. Visual territories
What the brand's surfaces actually look like, stated as occupancy — which territories it holds and which it refuses:

- backgrounds (flat color? imagery? texture? gradients?)
- density (airy editorial vs dense instrument)
- color temperature and chroma posture (e.g. "cool neutrals, hue 225–248, color arrives as accent")
- depth model (flat / surface-step / shadow-driven)
- signature type moves (e.g. "mono kicker tracked +0.14em is the eyebrow")

### 4. Cultural references
The design lineage that anchors an agent's taste — 2–4 references with what to take from each. This is the highest-leverage line-per-word slot in the file: "Braun-era Rams instrument panels — controls as calm hardware" steers a thousand micro-decisions no token can reach. Name eras, schools, artifacts, not companies to clone.

### 5. Refusals
What the brand will never do, as a flat list. Refusals are generative: they prune the search space before generation. Reference example: "Deliberately refused: generic, low-contrast, decorative color with no semantic role." Typical entries: gradient washes, emoji as iconography, drop-shadow depth, rounded-corner-with-accent-border cards.

### 6. Signature details
The 2–3 recognizable moves that make output identifiably *this* brand — the things a designer would spot in a lineup. If the slot is empty after extraction, the interview isn't done: ask "what would make you recognize a screen as yours with the logo removed?"

## Extraction vs invention

- **Extraction runs** (corpus provided): quote the corpus; every architecture line should be traceable to evidence. Real product copy is the best voice evidence — collect 5–10 strings before writing the Voice slot.
- **Invention runs** (brief only): propose each slot explicitly AS a proposal and get confirmation before it hardens into the file. Invented architecture presented as fact poisons every downstream generation.
- Either way, the slot content lands in the DESIGN.md itself (Overview, Voice section, refusals in Do's/Don'ts, references where they fit) — architecture is not a side document.

## The sufficiency test

Before shipping, run the stranger test: *could a fresh agent, given only this file, generate a screen the brand's own designer would recognize as theirs?* Recognizable ≠ compliant — compliance comes from tokens; recognition comes from this layer. If the honest answer is "it would be consistent but anonymous," the architecture slots need another pass.
