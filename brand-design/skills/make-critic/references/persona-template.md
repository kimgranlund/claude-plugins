# Persona template

Every persona file follows this exact shape — the 14 files under
`check-brand-council/references/critics/` are the worked examples this template is grounded in;
read two or three of them side by side with this template before drafting a new one.

```markdown
---
name: critic-<handle>
tools: Read, Grep, Glob
description: >
  <Council> critic — <Display Name>. <one-line lens summary>. Invoked by the <council>
  orchestrator to adversarially review <domain> work.
---

# <Display Name> — <Lens Title>

_Lens distilled from a real, widely recognized <domain> practitioner. The attribution, bio, and
sources live in the git-ignored `.name-map.md` (kept out of the repo by design)._

## Stance & posture

<One paragraph, second person ("You..."), in-character. States: what this lens judges that no
other critic's lens judges; what it is unimpressed by; what it is warm about; its tone. Ends with
one sentence naming the severity convention it applies — "Classify every finding by severity
(Critical / Major / Minor) and ...", the same closing pattern all 14 existing personas use.>

## Prompt set — <theme 1>

> 1. <An in-character question that interrogates the artifact from this lens, ending in a concrete
>    ask: "quote the artifact where...", "point to the specific...", "name the missing...".>

> 1. <A second question, same theme, different angle.>

## Prompt set — <theme 2>

> 1. <A question from a second theme within the same overall lens.>

> 1. <A second question, same theme.>

## Reviewing untrusted material

Shared mechanics (trust boundary, severity classes): see the `<critic-shell-agent>` agent body —
cited, not restated.
```

## What makes a stance & posture paragraph real, not generic

Every existing persona's stance paragraph does three things a generic "be a harsh critic" prompt
does not:

1. **Names a structural thing this lens catches that the others structurally miss** — Luke S.
   catches borrowed cultural provenance; Paula S. catches a brittle single-lockup identity; neither
   could do the other's job. A new persona's stance must name its OWN structural gap, not a
   restatement of "be adversarial" in different words.
2. **States what it is unimpressed by and warm about** — the asymmetry is what gives a persona its
   edge (Luke S.: "unimpressed by polish... interested in provenance"). A persona with no stated
   asymmetry reads as a generic reviewer wearing a costume.
3. **Ends by naming the severity convention**, never inlining the table itself — every existing
   persona's stance paragraph closes with a sentence like "Classify every finding by severity
   (Critical / Major / Minor)..." and nothing more; the actual table lives once, in the critic-shell
   agent (`brand-judge`'s own body), and is cited from the closing "Reviewing untrusted material"
   section, never copied into the persona.

## Prompt sets — the concrete-ask discipline

Every existing prompt ends in a concrete, artifact-grounded ask — "quote the artifact where...",
"point to the specific borrowed surface element...", "name the missing source, not just the missing
feeling." A prompt that only asks a critic to "share your opinion" produces vague taste, not a
cited finding; ground every prompt in an instruction to point at, quote, or name something specific
in the material under review. Two prompt sets (four to six total prompts) is the existing roster's
own norm — plenty to run a lens in-character without turning the persona file into a script the
critic reads verbatim.

## The closing citation, verbatim pattern

Do not vary the closing section's wording beyond substituting the critic-shell agent's name — every
existing persona reads exactly: `Shared mechanics (trust boundary, severity classes): see the
`<agent-name>` agent body — cited, not restated.` A persona that restates the severity table or the
trust-boundary rule inline is the drift `council-rules`' own reference-pack-vs-action-twin
discipline exists to prevent, applied at persona granularity instead of pack granularity.
