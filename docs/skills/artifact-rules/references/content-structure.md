# Content structure — classifying a content source before it gets a shell

The question this file answers: **given a content source, is it a report/retro, a handbook, or
does it span both — the classification `make-artifact`'s Phase 3 runs before choosing a shell?**
This is the CLASSIFICATION task only. What each answer should visually LOOK like (narrative
single-scroll, tabbed chapters, mechanism-first cards, hero-as-thesis) lives in
`design:artifact-styling-rules`' `shells-and-genres.md` — cited here, never restated (soft
cross-plugin mention, degrades gracefully where `design` isn't installed).

## The three-way test

- **Report/retro** — content answering "what happened / what did we decide," read start to
  finish, once, in order.
- **Handbook** — content answering "how do I look this up," multi-section, consulted
  non-linearly, referenced repeatedly rather than read straight through.
- **Spanning both** — a content source that is genuinely both (a handbook chapter that is itself a
  retro). Named explicitly in the build's Done report, never silently defaulted to one shell.

## Where this feeds forward

This classification is exactly the structural routing decision `#649`'s (not-yet-built) content
model composition phase will drive at scale — mapping Intent/User-Story/Concept/System record
layers to a chapter/section pattern is itself a repeated application of this same three-way test,
once per section rather than once per page. This file states the test; #649 (when built) is what
runs it programmatically across many sections.

## Choosing the shell

Once classified, route to `design:artifact-styling-rules`' `shells-and-genres.md` for the visual
doctrine each class gets. This file's job ends at the classification; it never states what a
narrative shell or a tabbed handbook should look like.

Extension: governed by [[make-pack]].
