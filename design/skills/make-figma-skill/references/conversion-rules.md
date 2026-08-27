# Conversion rules — estate skill / command / agent → Figma custom skill

The governing invariant: **resolution is never lost.** Every rule, threshold, contrast
pair, failure branch, and worked example in the source survives into the single file,
or is listed under `## Dropped` with a one-line reason. "Summarized" is a loss. Length is
not a cost the platform charges; fidelity is the deliverable.

## Transposition table

Each row: what the source carries → what the Figma file carries instead. The checker's F3
gate fails on any left-column form leaking through.

| Source construct | Figma-file construct | Notes |
|---|---|---|
| `references/x.md` citation | The file's content inlined as `## <x's title>` (whole, source order) | Inline every cited reference. A reference the SKILL.md never cites is still inlined when the body's rules depend on it (a rubric, a gates table); otherwise it goes to `## Dropped` with "uncited by source body". |
| `scripts/x.py` / `x.mjs` check | `## <check name> (transposed from scripts/x.py)` — a numbered checklist, one item per gate the script implements, each with its threshold verbatim and its pass condition stated as an observation the agent can make on the canvas | The script's docstring is the spec; read it, not the code, unless the docstring is thin. A check the agent genuinely cannot perform in Figma (a byte diff, an HTTP call) goes to `## Dropped` as "not performable in Figma; run `<script>` on the export instead". |
| `[[sibling]]` / `plugin:skill` handle | Either (a) the sibling's relevant slice inlined under its own heading, or (b) a plain-prose fence: "Out of this skill's scope: <topic>. Ask the user for <the artifact the sibling would produce>." | (a) when the source's rule cannot execute without the sibling's content (a token grammar, a voice table); (b) when the sibling is a separate job (a palette designer). Never a bare handle. |
| `${CLAUDE_PLUGIN_ROOT}` / absolute paths | Removed; the thing the path pointed at is inlined or Dropped | |
| `Read`/`Grep`/`Glob` the repo | "Inspect the file's local variables / styles / the linked library"; "read the selected frame's layer tree" | Figma-native equivalents; see the tool map below |
| `Bash` / running a command | Dropped, or transposed to a checklist (see scripts row) | |
| `Agent` dispatch / "dispatch the X-checker" | "Before finishing, re-read the output against `## <checker's rubric>` and report each dimension's score with cited evidence" — the checker's rubric inlined | Generator ≠ critic survives as a self-review pass with the rubric in hand, since no second agent exists in Figma |
| `AskUserQuestion` | "Ask the user in chat: <the question>, offering <the options>" | Same options, plain prose |
| `disable-model-invocation` / `user-invocable` / `model` / `context` / `paths` / `allowed-tools` (Claude Code keys) | Stripped. Model-invocable ⇒ description carries the active trigger; command-only ⇒ description says "Invoke with `/name`" and carries no auto-trigger phrasing | The species survives as description behavior, not as keys |
| `evals/evals.json` trigger cases | Carried into the description as verbatim phrasings (the `t*` prompts are the best trigger vocabulary you have); the `n*` cases become "Not for: …" sentences in the description | The checker's F8 (WARN) reports which `t*` prompts share no noun with the description |
| Output contract / failure branches / done-when | Verbatim, in the head | These are the contracts; they survive first. A source section that IS the contract (a receipt template inside a gates reference) is carried ONCE in the head; its source-order slot holds the one-line pointer `see ## Output contract` — that is a carry, not a Dropped entry |
| Path citations INSIDE an inlined reference (`references/x.md`, `scripts/y.py` mentioned by the reference's own prose or headings) | Rewritten to the pointer `## <that file's heading in this export>`; count them in `## Provenance` as `rewrites: N` | "Inline whole" governs content, not dead paths — a path the platform cannot open is rewritten, never left. F3 still scans inlined text, so this rewrite is mandatory |
| A transposed check's heading | `## <name> (transposed from scripts/x.py)` — the parenthetical is F3-exempt by design | Name the source script here and nowhere else in the running prose |
| Worked examples, good/bad pairs | Verbatim, in the tail, bad side still labeled | |

## Source shapes: skill, command, agent

`--source` resolves three shapes; each adds rows to the table above.

### Command-species skill (`disable-model-invocation: true`)

| Source construct | Figma-file construct |
|---|---|
| `$ARGUMENTS` / `argument-hint` | "the text after `/name` in chat"; the hint becomes the first sentence of the body ("Invoke as `/name <what to build>`") |
| Preconditions on repo/tree/credential state (`git status`, a token present) | The Figma-native precondition when one exists (a selection present, edit access to the file, a linked library reachable); otherwise `## Dropped` as `Claude Code runtime only` |
| `context: fork` / `agent:` / `background:` | Stripped — a Figma skill runs inline in the chat that invoked it |
| `allowed-tools` grants | Stripped (F2) |
| Side-effect confirmation points ("show the diff; proceed only on approval") | Kept verbatim as "show the change in chat; proceed only on the user's yes" — these are the command's safety contract |
| Description | "Invoke with `/name` …" — the human-timed contract survives as the trigger clause (F4 accepts it); no auto-trigger phrasings added |

### Agent definition (`agents/<name>.md`)

| Source construct | Figma-file construct |
|---|---|
| The role identity paragraph | The skill's identity line, verbatim |
| `tools:` wall (a checker's `Read, Grep, Glob`, with or without `Bash` for gate runs) | Figma has no tool wall; a no-edit wall becomes a `## Hard rules` line — "this skill reads and reports; it changes nothing on the canvas" — spending one of the ≤ 3 hard gates. The agent's other NEVER-class gates ride verbatim in their own sections; the head keeps at most three |
| `model:` / `effort:` / `color:` | Stripped (F2) |
| `skills: [a, b]` preloads | Each preloaded skill inlined WHOLE under `## <name> (preloaded)` — its SKILL.md body and its cited references — in list order. A cross-plugin preload (`docs:x`) resolves ONLY at `<workspace>/docs/skills/x/` (the checker never falls back to a same-named local skill); absent there it is an F6 FAIL to resolve, never a silent omission — inline it from that plugin's checkout, or Drop it as `sibling job, fenced` when the human rules the job out of scope |
| Sibling artifacts the agent reads AT DISPATCH TIME but does not preload (an owning sibling's `references/rubric.md`, a sibling's gate script) | Fenced, not inlined: "ask the user to paste <the rubric / the gate output>; else that dimension is UNMEASURED" — one `## Dropped` bullet per sibling, reason `sibling job, fenced`. Inlining would pull content the source deliberately refuses as a standing preload |
| A gate script the agent RUNS that is not bundled with the source (a sibling skill's `scripts/x.py`) | Not transposed (its docstring is outside the corpus); the run becomes "ask the user to paste the output, else UNMEASURED", Dropped as `not performable in Figma` |
| Priorities / numbered discipline list | Verbatim, in the head — it IS the contract |
| "deliver via `SendMessage`", `write-handoff` return block | "Reply in chat with this report shape:" + the handoff fields as a template |
| Dispatching sub-agents (`Agent` tool) | Self-review with the sub-agent's rubric inlined (the checker row above) |
| Description ("Use PROACTIVELY when …") | Reworded to "Use when …"; the NOT-clauses survive as "Not for: …" |

The F6 corpus for an agent = the agent body + every resolved preload's SKILL.md + those
skills' cited references. An agent with no preloads converts like a short skill.

## Tool map — Claude Code verb → Figma agent verb

| Claude Code | Figma agent / Make |
|---|---|
| Read a file | Read the selected layer / the page / the file's variables and styles |
| Grep the repo for a token | Search the file's variables (collections, modes) and text styles by name |
| Write/Edit a file | Create/modify layers, components, variables; in Make, generate or edit the code |
| Run a script | Perform the transposed checklist by inspection |
| Dispatch a checker agent | Self-review against the inlined rubric, scores + evidence in the reply |
| AskUserQuestion | Ask in chat with the options listed |
| Skill tool / slash another skill | "If the user needs <sibling job>, tell them to run `/<sibling figma skill>` if one exists, else ask for the artifact" |

## The three passes of a conversion

1. **Inventory.** List every `##`/`###` heading in the source SKILL.md, every cited
   `references/*.md` (and their headings), every bundled script (and its gates from the
   docstring), every `[[handle]]`/plugin mention, every numeric anchor. This list is the
   coverage manifest the checker's F6 gate enforces — write it into `## Provenance` as
   `inventory:` counts.
2. **Transpose.** Apply the table above row by row. Keep source order: SKILL.md sections
   first, then inlined references in the order the source SKILL.md first CITES them, then
   transposed checks. Keep thresholds verbatim (`4.5:1`, `≤ 700 chars`, `44px`) — the F6
   anchor gate compares strings.
3. **Reconcile.** Everything not carried lands in `## Dropped`, one bullet per item in the
   form `- <source heading or item> — <reason>`, the reason from this CLOSED set (the
   checker's F6 fails any bullet carrying none of them): `uncited by source body` · `not
   performable in Figma` · `Claude Code runtime only` · `superseded by inlined sibling
   slice` · `sibling job, fenced` · `user ruling: <quote>`. An empty `## Dropped` section is
   legal and means "everything carried".

## Head-first ordering (what the checker's F7 gate looks for)

```
---frontmatter---
# <name>
<identity line>
## Contents            ← routing table: "When you need … → see ##…"
## Hard rules          ← the source's ≤3 NEVER/MUST NOT gates, verbatim
## Output contract     ← what the agent hands back
## <source sections, in order>
## <inlined references, in order>
## <transposed checks>
## Examples
## Dropped
## Provenance
```

## Provenance fields

```
## Provenance
source: <path relative to the repo/plugin root> @ <plugin version>
date: <YYYY-MM-DD>
hash: <12 hex>      ← `python3 scripts/figma_skill_check.py --hash <source-dir | agents/x.md>`:
                      a skill dir → sha256 over sorted `<relpath> <sha256(bytes)>` lines,
                      excluding agents/ evals/ __pycache__/ dist/ and intent.md; an agent
                      file → its own bytes + each resolved preload dir's hash (a sibling
                      agent's edit does not move it; a preload edit does)
inventory: headings <n> · references <n> · scripts <n> · anchors <n> · rewrites <n> · dropped <n>
```

## Trigger description rules (Figma-specific)

- Lead with the job, then "Use when …" listing ≥ 3 of the source's `t*` phrasings verbatim,
  then "Not for: …" naming the `n*` FAMILIES (one clause per sibling/owner, not one per
  case — 15 cases is 3–5 clauses). Active voice throughout.
- Never "only when", "only if", "use only" — Figma documents these as misread.
- Name is specific: `<system>-<job>` (`nonoun-button-rules`), never a generic noun.
- ≤ 1024 chars; the whole description is the auto-trigger surface, so spend it on
  phrasings, not on restating the body.

## Contrast pair (normative)

```
Bad  (pointer survives, content lost — counter-example, do not imitate):
  For the token grammar see references/grammar.md; run scripts/check.py before shipping.

Good (content inlined, check transposed):
  ## Token grammar
  Tokens are `{prefix}-{family}-{slot}` … [grammar.md inlined whole]
  ## Pre-ship checks (transposed from scripts/check.py)
  1. Every fill/on pair ≥ 4.5:1 in both light and dark — inspect each pair's values.
  2. Every component leaf names `hover` with a literal value …
```
