# Task Prompts

Slice of the original `color-science` (now `color-science-project-files`) eval set relevant to
`color-material-facts` — tasks 2, 3, and 4 of the original 8. See
`color-science-project-files/evals/task-prompts.md` for prior history / the full original set.

## What to look for

- Does the answer pick the right conceptual frame quickly?
- Does it distinguish standards, heuristics, and implementation reality?
- Does it recommend tools and references that fit the actual task?
- Does it stay concise unless the task really needs deeper theory?

## Prompts

### 2. Print versus screen mismatch

"My mockup looks bright and clean on my MacBook, but the printed brochure feels dull and slightly
warmer. Can you explain why this happens and what workflow would reduce the surprise next time?"

Good answer:

- explains gamut, viewing conditions, and print/screen differences cleanly
- mentions ICC, D50 or D65 context where useful
- does not oversimplify to 'printers use CMYK so colors are worse'

### 3. Paint mixing in software

"I'm making a digital painting tool and artists keep complaining that mixing yellow and blue looks
wrong. What model should I look at if I want mixing to feel more like paint than Photoshop
opacity?"

Good answer:

- rejects naive RGB interpolation for pigment mixing
- points toward Kubelka-Munk, Spectral.js, or Mixbox-style approaches
- explains why pigment mixing paths differ from light mixing

### 4. Naming and historical register

"Can you suggest names for 12 muted naturalist-style colors for a field guide interface? I want
something closer to Ridgway or ISCC-NBS than startup branding names."

Good answer:

- recognizes the naming-system question immediately
- mentions appropriate systems such as Ridgway, ISCC-NBS, or Munsell depending on the need
- avoids random poetic names unless the user asked for them
