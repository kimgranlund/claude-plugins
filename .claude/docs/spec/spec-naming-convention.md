---
doc-type: spec
id: spec-naming-convention
status: draft
version: 1.2.0
date: 2026-08-17
owner: kim.granlund
prd: null   # no PRD — descends from ADR-0011 (accepted 2026-08-13), amended by ADR-0014 (2026-08-16)
---
# Harness Artifact Naming Convention — Specification

**Status:** Draft v1.0 · **Applies to:** `.claude/` harness artifacts (agents, commands, skills) · **Enforced by:** `naming.manifest.json` + validator (CI gate, pre-mint gate in `/skill-create`)

---

## 1. Purpose

One canonical name per artifact, everywhere it appears. Kind, invoker, and composition relations are decidable from the name plus its location — mechanically, by string operations, with no registry lookup and no reliance on frontmatter honesty. Frontmatter must *agree* with the parse; it never decides.

Design principle: **syntax encodes invocation semantics**. The grammatical mood of a name mirrors how the artifact is invoked. Illegal names are unrepresentable under the grammar, not merely discouraged.

---

## Requirements

REQ-numbered clusters below state this spec's binding rules. Each retains its original
section number (`2.`–`9.`) as a stable citation anchor — ADR-0011, ADR-0014, `validate.py`, and
sibling docs cite this spec by those numbers (see §14 Amendments); the numbers are unchanged by
this restructure, only regrouped under the SPEC-type contract's required headings.

### REQ-001 — 2. Taxonomy

Three kinds, partitioned by **invoker** — the one axis the platform actually enforces.

| Kind | Invoker | Surface | Grammatical form |
|---|---|---|---|
| **command** | User only (`/name`) | Slash autocomplete | Object-first verb phrase |
| **skill** | Model only (trigger-description match) | Description routing | Nominal / activity phrase |
| **agent** | Delegated (own context window) | Task delegation | Agentive nominal |

**Knowledge is a content pattern, not a kind, subtype, or suffix.** Some skills are mostly `references/` with a thin routing stub; the substrate matches descriptions identically either way, and relations target artifact names either way, so nothing in the tooling needs the distinction — the taxonomy does not invent one the validator would never read. Reference-shaped skills are named by the ordinary skill grammar (`naming-conventions`, `hcc-coding`), and their descriptions carry the consultation trigger.

**Dual access is composition, not a kind.** A capability that must be both user- and model-invocable is a skill plus a thin command wrapper. The wrapper relation is declared in the command's frontmatter (§7).

---

### REQ-002 — 3. Grammar

```
command   := object "-" verb                    skill-create, work-start
          |  ("bind"|"fork"|"sub") "-" scope    bind-team, fork-agent, sub-agent
                                                 (reserved heads, §14.5, ADR-0020 D3)
          |  "lead" "-" scope                   lead-team            (RETIRED open production,
                                                 ADR-0020 D3; six-name closed grandfather
                                                 only, §14.8)
skill     := object "-" process                 estate-audit, ui-layout-planning
          |  nominal-phrase                     naming-conventions   (looser production)
agent     := skill-name "-" "agent"             estate-audit-agent   (primary)
          |  scope "-" role                     team-leader          (orchestrators — canonical, ADR-0015 D1)
          |  scope "-" role "-" "agent"         product-leader-agent (orchestrators — legacy spelling, ADR-0015 D1)
```

One reserved head: `-agent`. Mandatory on the primary agent production and on skills
(illegal there); optional on the orchestrator agent production only (§3.3, ADR-0015 D1).

#### 3.1 Commands — object-first

Commands are object-first (`skill-create`, not `create-skill`) so that slash autocomplete groups operations by object: `/skill-<tab>` surfaces `skill-create`, `skill-review`, `skill-lint` together. Discovery ergonomics outrank reading-as-English for a user-invoked surface. <!-- fix-old-names: keep --> (illustrative `/skill-`-prefixed trio; `skill-create`/`skill-lint` never existed as real artifacts and `skill-review` since renamed to `check-skill` — rewriting it here would break the shared-prefix point the sentence makes, since `check-skill` no longer groups under `/skill-<tab>`.)

The terminal token must be a member of `VerbLex`.

Three reserved verb-first heads: `bind-`/`fork-`/`sub-` (§14.5/§14.8, ADR-0020 D3),
superseding `lead-` (ADR-0016, retired). `{head}-{scope}` conforms when `{scope}` resolves
against the orchestrator scope pool (`ObjectVocab ∪ ProcessLex`, ADR-0015 D2's pool) — the
command makes the host session adopt the orchestrator seat whose scope that is; the head
names which platform mechanic does the adopting (`bind-`: the host itself; `fork-`: `context:
fork`; `sub-`: an `Agent` dispatch). Each head is a literal (like §14.2's `check-`), not a
`VerbLex` member. `lead-` still parses, but ONLY for a closed, never-grown six-name
grandfather set (§14.8) — a new `lead-*` mint fails even when its scope resolves. Because the
live `/bind-*`/`/fork-*`/`/sub-*` surfaces ship as a mix of true commands and command-species
skills and §6 decides kind by directory, the validator recognizes every head (including the
grandfathered `lead-`) on both the command and skill parse branches (§14.5/§14.8).

#### 3.2 Skills — nominal, process head preferred

The canonical skill production is `{object}-{process}` (`estate-audit`, `entry-file-authoring`). The terminal token should be a member of `ProcessLex`. Skills that are genuinely not object-process shaped — report generators, routers, and reference corpora — use the nominal-phrase production, but every token must still resolve in the lexicons (§4): the looseness is in the *shape*, never in the *vocabulary*.

Six literal reserved verb-first heads live on the skill grammar, closed at exactly this set — not a template for any other `VerbLex` member: `check-` (§14.2, ADR-0014), `bind-`/`fork-`/`sub-` (§14.5/§14.8, ADR-0020 D3, superseding `lead-`), the now-closed-grandfather `lead-` itself (six live names only, §14.8), and `make-`/`file-` (§14.7, ADR-0018). Each resolves its residue against `ObjectVocab` alone (`check-`/`make-`/`file-`) or the orchestrator scope pool (`bind-`/`fork-`/`sub-`/`lead-`), and each sits before the `ProcessLex` terminal check to avoid the dead-code hazard §14.2 names.

Reading test (procedural): the name completes "this artifact teaches how to do ___."
Reading test (reference-shaped): the name completes "consult ___ for this."

#### 3.3 Agents — derived from skills

The primary production is `{existing-skill-name}-agent`. An agent's capability must have an authored skill spec; the peer audit verifies this by stripping `-agent` and asserting the skill exists.

The orchestrator production, for agents that coordinate rather than execute and therefore have no patient object: `{scope}-{role}` (`team-leader`) is canonical (ADR-0015 D1 — the role noun is already the agent marker, so the `-agent` tail is redundant on this production only); `{scope}-{role}-agent` (`product-leader-agent`) remains a legal legacy spelling, never rejected, not chosen for new mints. `scope` resolves against `ObjectVocab ∪ ProcessLex` (ADR-0015 D2 — a coordinating seat's scope is either a thing or a process). `RoleLex` starts at ≤4 entries, grows only by manifest PR, and stays disjoint from `ObjectVocab ∪ ProcessLex` (ADR-0015 D3, §4 AC-008).

Reading test: the name completes "hand this off to the ___."

---

### REQ-003 — 4. Lexicons

Four lexicons live in `naming.manifest.json`. Three are closed (additions require a manifest PR — this is the governance gate); one grows by registration.

| Lexicon | Contents | Membership |
|---|---|---|
| `VerbLex` | Command terminal tokens: `create`, `review`, `lint`, `sweep`, `start`, `finish`, `run`, `mint`… | Closed |
| `ProcessLex` | Skill terminal tokens: `audit`, `planning`, `authoring`, `triage`, `review`ᵈ, `migration`… | Closed |
| `RoleLex` | Orchestrator roles: `leader`, `orchestrator`, `coordinator` | Closed, ≤4 to start; disjoint from `ObjectVocab ∪ ProcessLex` (ADR-0015 D3) |
| `ObjectVocab` | Domain objects: `skill`/`skills`, `issue`/`issues`, `pr`, `ui-layout`, `entry-file`, `harness`… | Registered |

**Disjointness invariant:** `VerbLex ∩ ProcessLex = ∅`. A token lives in exactly one. Where a word plausibly belongs to both (e.g. `audit`), it is assigned to one lexicon and the other kind uses an alternative (`audit` ∈ ProcessLex; a command triggering an audit uses `run` or wraps the skill per §7). This disjointness is what keeps command/skill classification decidable from the name alone as a lint check, even though directory location is the authoritative discriminator (§6). A second, independent disjointness holds once the orchestrator agent production admits a bare `{scope}-{role}` name (ADR-0015 D1): `RoleLex ∩ (ObjectVocab ∪ ProcessLex) = ∅` (AC-008) — otherwise a role word could double as a skill's object or process token, letting one string parse as a skill and as an agent.

**ObjectVocab registration** records, per entry:

- `canonical` — the one true form (`pr`)
- `plural` — inflected form for imperative objects where applicable (`issues`)
- `banned_aliases` — rejected synonyms (`pull-request`, `pull-requests`)
- Registration is **rejected** if the new token creates parse ambiguity with any existing multi-token entry (§5).

Brand tokens (`adia`) are banned from ObjectVocab. Plugin namespacing is the marketplace prefix's job (`plugin-name:artifact-name`); embedding brand in the local name double-prefixes and forces renames on plugin moves.

**Plurality rule:** objects of imperatives pluralize where natural (`sweep-issues`); attributive objects do not (`issue-triage`, per "issue tracker" not "issues tracker"). Both inflections resolve to the same ObjectVocab entry.

---

### REQ-004 — 5. Parse algorithm

Deterministic; specified here so no two tools hand-roll it differently.

1. **Strip the reserved head:** `-agent`, if present. For the primary agent production
   (and a skill's own reserved-head rejection) what was stripped still fixes kind
   candidacy. For a bare orchestrator name (ADR-0015 D1) there is nothing to strip —
   kind candidacy then comes from the directory (`agents/`) plus a `RoleLex` terminal
   token, tried alongside the stripped form rather than instead of it.
2. **Longest-match resolve** the remaining token sequence against ObjectVocab (commands,
   skills, the primary agent production; multi-token entries like `ui-layout` match
   greedily, left-anchored) — or, for the orchestrator agent production's scope phrase
   specifically, against `ObjectVocab ∪ ProcessLex` (ADR-0015 D2), same algorithm, wider pool.
3. **Classify the terminal token** of the residue against `VerbLex` / `ProcessLex` / `RoleLex`.
4. **Every token must resolve.** Any token that is in no lexicon and no ObjectVocab entry fails the parse.

Ambiguity is prevented at write time, not resolved at read time: the ObjectVocab registration gate (§4) rejects entries that would make step 2 ambiguous. Example: with skill `ui-layout-planning` extant, `ui-layout-planning-agent` parses uniquely as agent-of-skill because `-agent` strips first and the residue matches an existing skill name before any decomposition is attempted.

---

### REQ-005 — 6. Directory & file layout

Invoker is decided by **location**; the grammar corroborates it.

```
.claude/
  commands/
    skill-create.md
  skills/
    estate-audit/SKILL.md
    naming-conventions/SKILL.md      # reference-shaped: thin stub + references/
  agents/
    estate-audit-agent.md
```

**Folder equals canonical name, no decoration.** One canonical string everywhere — no folder-level transforms to validate, no discovery-compatibility risk. Reference-shaped skills are visually indistinct from procedural ones in a listing; if that view is ever needed operationally, it is a derived report (`naming-audit` lists skills with no ProcessLex head), never a naming rule.

Validator rule: `folder == name` for every artifact.

#### 6.1 Skill folder layout — closed set

```
skills/{name}/
  SKILL.md          # required — routing stub + procedure (thin stub for reference-shaped skills)
  references/       # passive matter: read into context, never executed
  scripts/          # executable matter: code the procedure invokes
  assets/           # inert payload: images, fixtures, binary/static files
  evals/            # routing-surface proof: trigger evals, behavioral assertions, baselines (§14.10, ADR-0024)
  intent.md         # make-skill's own living build ledger, a bare top-level file like SKILL.md (§14.10, ADR-0024)
```

Six top-level entries, nothing else. The partition axis is **how content participates when the skill runs**: `SKILL.md` is loaded into context; `references/` is selectively read into context; `scripts/` executes *outside* context — deterministic logic belongs in a script the skill calls, never in prose the model re-derives; `assets/` is neither read nor executed, only addressed by path; `evals/` is proof the routing surface holds, evaluated against by a script or a judge, never itself loaded as procedure; `intent.md` is the forge's own actively-written build ledger, never passive reference matter. Every file answers one question — *context, computation, payload, routing proof, or build ledger?* — and the answer decides its folder.

Boundary validation (the validator checks these and nothing deeper):

1. `SKILL.md` exists.
2. No top-level entries outside the closed set — a stray `docs/`, `notes.md`, or `old/` at the skill root fails lint. Unclassified top-level matter is how skill folders become junk drawers.
3. Nothing under `scripts/` is referenced from outside the skill — encapsulation holds in both directions.
4. **No nested skills.** A skill containing sub-capabilities that want their own triggers is decomposed into sibling artifacts with `requires` edges, never a hierarchy — hierarchical skills would make the router's matching ambiguous (parent or child?) and break the flat namespace the parse depends on.

Below the boundary, the validator is deliberately blind: internal file names, nesting, and formats are the author's domain. Validation pressure inside a skill's internals is the §9 signal that content wants to be an artifact — never a reason to grow the validator.

#### 6.2 Content organization within the layout

**Knowledge corpora — discoverable by two hops, loaded on demand.** Discovery is always: *description → SKILL.md → reference index → file.* The router matches the skill's `description` (hop one); the SKILL.md body must then contain a **reference index** — a table listing every file under `references/` with a one-line *when-to-read* trigger (hop two):

```markdown
## References
| File | Read when |
|---|---|
| HIERARCHY.md | resolving V28 hierarchy conflicts between HCC codes |
| edge-cases.md | a mapping falls outside the standard crosswalk |
```

The index is the corpus's contract with context: without it, an agent session either loads the whole corpus (context waste) or greps blind (missed knowledge). With it, disclosure is progressive — stub loads at trigger time, individual files load only when their *read-when* condition fires. Agent sessions inherit discovery through the same two hops via `performs`/`requires`; no separate agent-facing mechanism exists or is needed. Validator: every file under `references/` appears in the index; every index row points at an extant file. (This is the one intra-folder check, and it's justified because the index *is* the boundary — it's how the folder's contents become reachable at all.)

**Templates and schemas — passive contracts, so `references/`.** A template is matter the model reads and instantiates; a schema is matter that constrains an output. Both are context, not computation, so both live in `references/` — UPPERCASE per the contract convention (`REPORT-TEMPLATE.md`, `OUTPUT.schema.json`) — and both get *read-when* rows in the index. No `templates/` or `schemas/` folder: the moment schemas earned structural treatment, every author would face the undecidable "template vs schema vs example vs fixture" sort. Two special rules: a schema that a script *enforces* still lives in `references/` and the script addresses it by relative path — single copy, both consumers point at it. A template or schema needed by a **second skill** follows the §9 extraction rule verbatim: it becomes an ordinary skill (`project-schemas`, `report-templates`, nominal production), consumers declare `requires`, and its SKILL.md's reference index is what makes the shared contracts individually addressable.

**Procedures and workflows — the SKILL.md body is the procedure's single authority.** One skill, one procedure; the procedure is not a document *inside* the skill, it *is* the skill. Long procedures split by phase into `references/` files (`PHASE-2-RECONCILE.md`) loaded when the phase runs — same progressive-disclosure mechanics as corpora, indexed the same way. A **workflow spanning multiple skills is composition, not a document**: it's expressed as an orchestrating artifact — a command chaining steps behind its confirm gate, or an orchestrator agent — whose own body states the sequence and whose `requires` edges declare the participants. The anti-pattern this bans: a `WORKFLOW.md` sitting in one skill's `references/` describing steps that other artifacts perform. That's an authority claim over artifacts that don't declare the dependency — the relation graph can't see it, the peer audit can't verify it, and it drifts the day any participant changes. If a workflow deserves documentation, it deserves to be an artifact; then the graph carries it.

---

### REQ-006 — 7. Composition relations — declared in frontmatter, graph derived

Composability comes from the **shared ObjectVocab**, not from shared name shapes. Relations are **declared in the frontmatter of the depending artifact** — never in a central registry. One authority per fact: a relation lives with the artifact that holds it; the manifest holds only lexicons and exemptions; the estate-wide relation graph is *compiled* from frontmatter by the validator, never hand-maintained. A central `relations` registry would force two files to agree about one fact, which is the drift shape this spec exists to kill.

| Relation | Declared by | Field | Validator check |
|---|---|---|---|
| agent **performs** skill | the agent | `performs: estate-audit` | value == name minus `-agent`; skill exists |
| command **wraps** skill | the command | `wraps: naming-audit` | skill exists; skill is model-invocable |
| artifact **requires** skill | the consumer | `requires: [naming-conventions]` | each exists; compiled graph is acyclic |

`performs` is redundant with the string arithmetic by design — the redundancy is the check. A rename that touches one side and not the other fails loudly instead of drifting silently.

`requires` is the single dependency edge: "must exist and be available." Whether the dependent *invokes* the target's procedure or *consults* its references is visible in the dependent's body, where behavioral distinctions belong — a second edge type (`consults`) would encode in metadata what the body already states, and edge types that duplicate body content are the frontmatter equivalent of comments that restate code.

The **wrapper pattern** is how dual access works under the strict invoker partition: a model-invocable skill gains user access via a thin command (`/naming-audit` → `wraps: naming-audit`). Every artifact keeps exactly one invoker; dual access is composition, not a fourth kind.

Derived-graph audits (all mechanical): dangling endpoints (relation references a nonexistent artifact), orphaned agents (`performs` disagreement), and `requires` cycles.

---

### REQ-007 — 8. Frontmatter schema

Frontmatter is the **authoring surface** for everything the tooling reads. The rule that keeps it from rotting: **every field in this schema is validated; no field enters the schema unless something reads it.** Fields nothing validates are prohibited, not optional — ungoverned metadata is where frontmatter lies accumulate.

**Agent schema, amended to the measured convention (ADR-0025, §14.11):** the field list below for commands and skills is unchanged; the agent schema in 8.1–8.4 reflects what every agent in this estate actually carries (measured 2026-08-21, 40 files), not the earlier aspirational draft — `kind`, `performs`, `autonomous_write`, `context`, and the provenance block (`author`/`created`/`last_updated`/`review_after`) are dropped from the agent schema; nothing here changes command/skill frontmatter.

#### 8.1 Identity (required, all kinds)

```yaml
name: estate-audit          # canonical; == folder; parseable per §5
description: >              # the trigger contract — governed by
  Use when …                # skill-writing-rules, not this spec
```

Commands and skills also declare `kind: command | skill` per their own frontmatter contract
(`skill-writing-rules`); an agent's kind is decided by directory + name-parse (§5/§6) and is
never itself a declared frontmatter field — no agent in the estate declares one, and nothing
reads it if it did. The validator asserts agreement, never trusts declaration, for the kinds
that do declare it: name parse + directory → **decided kind**; frontmatter must match.
Disagreement is a lint failure. Frontmatter is an agreement check, never a tiebreaker — the
specific defense against the rename-drift class (`entry-file-author` / `claude-md-author`) where
a name silently stops meaning what the metadata claims.

**Agent identity, measured (ADR-0025):** `name` and `description` are the only fields every
agent carries. `model` and `tools` are carried by every agent sampled too — common convention,
not a schema-enforced requirement — with `effort` (paired with `model`, `harness:
agent-writing-rules`' tiering ladder), `skills` (preloaded skill dependencies — the real
analogue of §7's `requires` edge, under the name agents actually use), `color` (cosmetic
grouping), and `disallowedTools` (a negative tool grant) as measured optional fields.

#### 8.2 Relations (per §7, on the depending artifact)

```yaml
wraps: naming-audit                # commands (dual-access)
requires: [naming-conventions]     # any kind — deps that must exist and be available
skills: [naming-conventions]       # agents — the same edge, under the field name agents use
```

**`performs` is dropped from the agent schema (ADR-0025 D2).** §7 still documents the
agent-performs-skill relation and its structural check (name minus `-agent` equals an extant
skill) — that check runs against the name itself via §5's parse algorithm, with no frontmatter
field needed, and zero agents duplicate it in frontmatter. §7's relation table is unamended;
this section only corrects the earlier claim that agents *declare* `performs` in frontmatter.

#### 8.3 Invocation policy and tool grants

```yaml
# agents
model: sonnet
tools: Read, Glob, Grep, Bash(python */scripts/validate.py *)

# commands
mutates: true               # touches files beyond its own output
confirm: required           # required | none — human gate before mutation
allowed-tools:
  - Read
  - Edit
  - Bash(git mv *)
```

**`autonomous_write` and `context` (`isolated`/`inherited`) are dropped from the agent schema
(ADR-0025 D2).** No agent declares either — the platform's own dispatch mechanics (an agent's
tool grant; whether it runs via a fresh context or a fork) already carry the distinction these
fields would have restated. The command policy fields (`mutates`/`confirm`/`allowed-tools`) are
unamended: the validator asserts `mutates: true ⇒ confirm: required` unless the command is in a
reviewed allowlist.

**Tool grants are where agent policy actually materializes** — and declaring them also removes
runtime permission interruptions, so least-privilege and ergonomics are the same move. Rules:

- Every artifact declares the minimum tool set its body actually uses. `Bash` grants are always **scoped patterns** (`Bash(git mv *)`), never blanket — enumerate the legal set, reject by default, same as the lexicons.
- The estate's mutation topology is answered from an agent's `tools` grant directly (no `Edit`/`Write`/unscoped `Bash` ⇒ report-only in practice), never from reading procedure bodies — the same grep-decidability goal the earlier `autonomous_write` field aimed at, achieved by the grant itself rather than a second field asserting what the grant already shows.

#### 8.4 Provenance

**Dropped from the agent schema only (ADR-0025 D3); commands and skills are out of this
amendment's scope.** For agents, `author`/`created`/`last_updated`/`review_after` had zero
adoption outside one plugin's own internal dogfooding copy (`authorkit`'s `schema_scope:
"full"` self-check, issue #226/#224 ruling b) — restating them as estate-wide agent schema when
no estate-wide gate ever enforced them was aspiration standing in for reality. `authorkit`'s own
internal convention is untouched by this drop; a plugin may still track its own provenance
fields on its own agents as an internal choice. Whether commands and skills carry this block at
a rate that still earns it as documented schema is a separate, unmeasured question this ADR does
not rule on — ADR-0025's own evidence (§14.11) is agents-only; the block below stands unamended
for those two kinds pending that separate measurement.

#### 8.5 What stays out

`version` (git is the version authority), `tags` (the grammar + description are the routing surface; a parallel folksonomy forks it), free-form `notes` (body content, not metadata), and — for agents specifically, per ADR-0025 — `kind`, `performs`, `autonomous_write`, `context`, `author`, `created`, `last_updated`, `review_after`: none read by anything outside one plugin's own internal self-check. If a future field earns estate-wide validation, it enters by manifest PR like a lexicon entry, the same door ADR-0025 leaves open to re-admit any of these should a real consumer materialize.

---

### REQ-008 — 9. Two-level taxonomy — artifacts vs intra-skill resources

The estate has exactly two levels, and only the top one is governed by this grammar:

1. **Artifacts** — named per §3, validated per §10, participate in relations. The unit of routing: things the user, model, or another artifact can reach for.
2. **Intra-skill resources** — files under a skill's `references/` folder. Not routable, not named by the grammar, loaded only when their owning skill runs.

**Placement is decided by one question: does it need to be independently triggered or depended upon?**

- Yes → artifact, full grammar, full frontmatter.
- No (consumed only within one skill's execution) → `references/`. Promoting it would pollute the router's description-matching pool with entries competing for triggers they should never win.

Checklists, rubrics, templates, calibration corpora (`CALIBRATION.md`), blast-radius procedures, reference material — these are `references/` residents by default. **No name suffixes for content patterns.** A `-knowledge-base`, `-procedure`, or `-playbook` suffix would annotate at the name level a property the tooling never reads: relations target artifact names (so encapsulation is structural, not nominal), descriptions carry triggers (consultation or execution alike), and the loose nominal production already admits skills without procedures. One reserved head (`-agent`) is the complete set. The bar for a second: the validator or router must treat it differently. Nothing proposed clears it.

**Extraction rule:** knowledge lives in `references/` of the skill that uses it — most knowledge has a natural procedural owner, and co-location beats extraction. When a **second consumer** materializes, extract the content into a skill of its own (nominal production: `naming-conventions`, `hcc-coding`) and each consumer declares `requires`. This is the same judgment as extracting a shared function — don't duplicate an authority — and needs no machinery beyond it. The tell that a resource wants extraction: you feel the urge to validate it. Validation pressure inside `references/` is the signal the content has become a contract, and contracts are artifacts.

**Resource-level convention (readability only; validator ignores it):** UPPERCASE filenames for contracts the skill's own text points at (`CALIBRATION.md`, `RUBRIC.md`); lowercase for supporting matter.

---

## Non-goals

See also §8.5 ("What stays out") for the artifact-frontmatter fields this spec deliberately
excludes from validation (`version`, `tags`, free-form `notes`).

### 10. Migration posture — grandfathering

The live estate conforms at roughly 30%. The grammar is a target; without an explicit migration mechanism it is dead paper. Posture: **enforce for new names; grandfather existing ones.**

- `naming.manifest.json` carries an `exemptions` array listing every current non-conforming name verbatim.
- The validator passes any name in `exemptions` and enforces the full grammar on everything else.
- **The array may shrink and may never grow.** CI diffs the array; any addition fails the build.
- `harness_check` reports exemption count as a burn-down metric. Renames retire exemptions opportunistically (when an artifact is otherwise being touched), never as a big-bang campaign — renames are a known drift source because invocation strings live in prompts, hooks, and workflow configs.

Known exemption seeds (non-exhaustive): `handoff-to-human`, `handoff-to-agent`, `find-unused`, `team-weekly`, `team-daily`, `pylon-triage-weekly`, `prompt-wording-rules`, `start-work`, `finish-work`, and all `adia-*`-prefixed local names.

---

## Acceptance

### 11. Validator

String ops plus YAML reads, no NLP. Runs in CI and as a pre-mint gate in `/skill-create`.

Checks, in order:

1. **AC-001** (REQ-001) Name ∈ `exemptions` → grammar checks skip (record for burn-down); frontmatter checks (4–7) still apply.
2. **AC-002** (REQ-004) Parse per §5; all tokens resolve; no banned aliases; no brand tokens.
3. **AC-003** (REQ-005) `folder == name` (§6); skill folder layout closed set, `SKILL.md` present, no nested skills (§6.1); reference index complete and dangling-free (§6.2).
4. **AC-004** (REQ-007) Frontmatter schema (§8): required fields present per kind (agents:
   `name`/`description`; commands/skills also declare `kind`, checked against decided kind);
   no fields outside the schema (ADR-0025: the agent schema no longer lists `kind`/`performs`/
   `autonomous_write`/`context`/`author`/`created`/`last_updated`/`review_after`, so none of
   those count as "outside the schema" on an agent — they simply aren't read).
5. **AC-005** (REQ-006) Relations (§7): every endpoint exists; `performs` equals name minus `-agent`
   (checked structurally off the name itself, §5 — never off a frontmatter field, ADR-0025 D2);
   `wraps` targets a model-invocable skill; compiled `requires`/`skills` graph is acyclic.
6. **AC-006** (REQ-007) Invocation policy (§8.3): `mutates: true ⇒ confirm: required` (allowlist
   excepted, commands); agent policy is read from its `tools` grant directly — no
   `autonomous_write` field to fail closed on (ADR-0025 D2); `Bash` grants are scoped patterns.
7. **AC-007** (REQ-007) Provenance (§8.4): applies to commands and skills as before; dropped for
   agents (ADR-0025 D3) — `author`/`created`/`last_updated`/`review_after` are not checked
   against an agent's frontmatter.
8. **AC-008** (REQ-003) ObjectVocab registration gate (on manifest change): new entries create no parse ambiguity; disjointness of VerbLex/ProcessLex holds; disjointness of RoleLex against ObjectVocab ∪ ProcessLex holds (ADR-0015 D3).

Grammar and relation failures block the mint/merge; staleness warns.

---

## Examples

### 12. Worked examples

| Name | Location | Parse | Verdict |
|---|---|---|---|
| `skill-create` | `commands/` | object=`skill`, verb=`create` | ✓ command |
| `estate-audit` | `skills/` | object=`estate`, process=`audit` | ✓ skill |
| `naming-conventions` | `skills/` | nominal production; reference-shaped body | ✓ skill |
| `hcc-coding` | `skills/` | nominal production (tokens resolve) | ✓ skill |
| `estate-audit-agent` | `agents/` | strips `-agent` → extant skill `estate-audit` | ✓ agent (performs) |
| `team-leader` | `agents/` | scope=`team` ∈ ObjectVocab, role=`leader` ∈ RoleLex | ✓ agent (orchestrator, canonical, ADR-0015 D1) |
| `team-leader-agent` | `agents/` | scope=`team`, role=`leader` ∈ RoleLex | ✓ agent (orchestrator, legacy spelling) |
| `create-skill` | `commands/` | verb-initial — violates object-first | ✗ reject |
| `hcc-coding-knowledge-base` | `skills/` | `knowledge-base` ∉ any lexicon — no reserved head exists for content patterns | ✗ reject |
| `coding-agent` | `agents/` | strip `-agent` → `coding` is no extant skill, no role | ✗ reject |
| `entry-file-author` | `skills/` | agentive head on a skill | ✗ → rename `entry-file-authoring` or exempt |

---

## 13. Open items to v1.0-final

1. Seed the four lexicons, the initial ObjectVocab, and the AuthorRegistry; ratify via manifest PR.
2. Enumerate the full `exemptions` array from the live inventory.
3. Backfill frontmatter (relations, invocation policy, provenance) across the existing estate — exempt names still carry full frontmatter (§11 check 1).
4. Set the default staleness review window and the mutating-command allowlist.

---

## 14. Amendments

### 14.1 Reverse-wrapper skill names (2026-08-14, issue #241, Sign-off ratified on #241)

**Ruling:** a skill MAY carry an object-verb name (terminal token drawn from `VerbLex`, not
`ProcessLex`) **IFF** an identically-named command exists in the same plugin root and wraps it
(§7's wrapper relation, read in reverse — a command normally wraps a skill for user access; this
production licenses the skill's own name shape off that same sibling's existence). Absent that
wrapper, an object-verb skill name is illegal exactly as §3.2/§5 already specify — this amendment
adds one narrow production, it does not relax the `VerbLex ∩ ProcessLex = ∅` disjointness
invariant (§4) or license a verb-terminal skill name standing alone.

**Why:** issue #238's design phase established the `overhaul-planning` → `overhaul-execute`
naming symmetry the estate wants, mirroring the existing `rename-planning` → `rename-execute`
precedent pair. `rename-execute` ships command-only today (no skill counterpart) because, before
this amendment, no legal skill-grammar production existed for a verb-terminal name at all —
confirmed empirically during #238's build: `rename-execute`/`exemption-retire` are command-only
files with zero skill siblings, not "grandfathered exemptions" as an earlier, incorrect claim on
that issue's thread asserted. `overhaul-execute` needs to be **both** model-invocable (so an
orchestrating skill or command can dispatch it without a human typing the slash command) **and**
user-invocable (the existing host-run command, unchanged in its confirm-gated mutation posture).
One procedure, two surfaces, is exactly the wrapper pattern (§7) — just applied to a name shape
§3.2 didn't previously admit. Kim's Sign-off on #241 is this ruling's authority; no future seat
needs to trust a mid-build comment for it.

**Validator change:** `naming-audit/scripts/validate.py`'s skill-grammar production gains one new
branch: if the terminal token resolves in `VerbLex` (not `ProcessLex`) AND a command file of the
identical name exists in the same plugin root, the object prefix must still resolve against
`ObjectVocab` exactly as the object-process production already requires — the wrapper's existence
is the license, not a bypass of object resolution. A verb-terminal skill name with no
identically-named command sibling still fails exactly as before this amendment (the negative
control the validator's own selftest fixtures alongside the positive and regression controls).

**Non-goal:** this amendment does not touch command grammar (§3.1), agent grammar (§3.3), or the
`VerbLex`/`ProcessLex` disjointness invariant (§4) — a token still lives in exactly one lexicon;
this amendment only adds a second *skill* production that may legally consume a `VerbLex` token
under the stated precondition.

### 14.2 `-rules` reserved tail and `check-` reserved head (2026-08-16, issue #353, ADR-0014 ratified 2026-08-16)

**Ruling:** two new, independently-scoped skill-grammar productions, plus one new closed lexicon,
register two recurring name shapes the estate kept re-exempting by hand instead of parsing:

```
skill := topic-phrase "-" "rules"          # D1 — rules becomes a reserved TAIL
skill := "check" "-" object-phrase         # D2 — check becomes a reserved HEAD
```

`rules` is the literal terminal token (D1). `topic-phrase` (every token but the trailing `rules`)
resolves against a **union pool** — `ObjectVocab ∪ ProcessLex ∪ TopicLex` — via the same greedy
longest-match algorithm §5 already specifies, just fed a broader lexicon set. `check` is the
literal token `tokens[0]` (D2), not a `VerbLex`-head production generalized to every verb; the
remaining `object-phrase` resolves against **`ObjectVocab` only**, deliberately narrower than
D1's pool — a `check-<noun>` name denotes a real, checkable system object, the same contract
`ObjectVocab` already carries. Kim's ratification of ADR-0014 (2026-08-16) is this ruling's
authority.

**Why:** ADR-0011 D8's grandfather-and-ratchet migration posture is correct for one-off legacy
debt; it is the wrong tool for a *recurring, predictable* shape a human keeps re-minting. Measured
against the pre-amendment `naming.manifest.json`: 22 exempted names ended in `-rules` (a closed
reference-doc-standards pattern — `agent-writing-rules`, `doc-writing-rules`, …) and 14 matched
`check-<noun>`, of which 3 (`check-doc`, `check-skill`, `check-stage`) already parsed clean only
*by accident* — leaning on `check` sitting in `ObjectVocab` as if it were an ordinary noun, which
only worked for the lucky subset of tails whose other token happened to be independently
registered. Declining to register either pattern means every future `-rules` standards skill or
`check-<noun>` report generator re-earns a hand exemption forever — the exact toil ADR-0011 D8's
ratchet exists to retire opportunistically, never eliminate structurally. Full design record,
decision rationale, and the rejected alternatives (an unconstrained `-rules` prefix; folding topic
words into `ObjectVocab`; generalizing `check-` to every `VerbLex` verb): ADR-0014.

**Validator change:** `naming-audit/scripts/validate.py`'s `Grammar.parse` skill branch gains two
new branches, both inserted **before** the existing object-process check (`tokens[-1] in
self.process_lex`) — that check hard-returns on any match, and `rules` already sits in
`ProcessLex` (registered for the ordinary `{object}-writing` shape), so a branch placed after it
would be unreachable dead code for the entire `-rules` class. Same hazard for D2: `check-stage`'s
terminal token `stage` sits in `ProcessLex`, so D2 must also precede that check or it would never
see `check-stage` at all. A new `resolve_objects_union` method (a `_resolve` helper shared with
`resolve_objects`, differing only in which lexicon dict it searches) implements D1's union-pool
resolution; `Grammar.__init__` builds the union pool once — `ObjectVocab` entries plus every
single-token `ProcessLex` member (`ProcessLex` is single-token by construction — every entry is a
skill terminal) plus every `TopicLex` member, multi-token compounds included (`font-token`,
`ops-write-sandbox`, …), `ObjectVocab` never shadowed. `ObjectVocab` gained 12
entries (`entry-file`, `routing`, `state`, `focus`, `safety`, `speed`, `translation`/`translations`,
`color`/`colors`, `isolation`, `a2a`, `ui-change`, and `stage` — the last a deliberate dual
membership with `ProcessLex`, keeping `check-stage` resolving once `check` is no longer in
`ObjectVocab`); `check` itself was **removed** from `ObjectVocab` — D2's reserved head supersedes
the reason it was registered, and leaving it in would let a stray nominal phrase abuse `check` as
an ordinary noun.

**New lexicon `TopicLex` (D3):** structurally identical to `RoleLex` — a flat list, closed,
`naming.manifest.json` top level, grown only by manifest PR. Seeded with 15 entries covering 14 of
the 22 `-rules` names (`icon`, `loop`, `motion`, `checking`, `font-token`, `design-md`,
`ops-write-sandbox`, `parallel-work`, `size-and-shape`, `team-or-solo`, `thinking-depth`,
`blocked-by`, `big-change-git`, `prompt`, `wording`); the remaining 8 need no new `TopicLex` entry
at all — 7 are the `{noun}-writing-rules` pattern (the noun is already `ObjectVocab`, `writing` is
already `ProcessLex`) and the 8th (`entry-file-rules`) resolves through the `entry-file`
`ObjectVocab` addition instead. `TopicLex` carries **no disjointness requirement** against
`ObjectVocab`/`ProcessLex` — it is consulted only inside D1's already-fixed union-pool context,
where a token sitting in more than one pool creates redundancy, never ambiguity.

**Non-goals (named explicitly, never grandfathered back in per §10's shrink-only rule):**

- This amendment does not touch command grammar (§3.1), agent grammar (§3.3), the `-agent`
  reserved head, the §14.1 reverse-wrapper amendment, or the plain nominal-phrase fallback for
  every skill name that is neither `-rules`-tailed nor `check-`-headed.
- It does not extend the `VerbLex ∩ ProcessLex = ∅` disjointness invariant (§4) to `TopicLex` —
  no such requirement exists, by design (D3 above).
- **4 exemptions this amendment deliberately does not retire:** `check-all-agents`,
  `check-all-skills`, `check-everything`, `check-whole-ui`. Their non-tail tokens (`all`,
  `everything`, `whole`) are quantifiers, not domain objects — minting a `QuantifierLex` for 3
  idiomatic superlative names is disproportionate to the recurring-pattern problem this amendment
  exists to fix. They stay exempt; the validator's own selftest carries a control proving they
  still fail grammar (never silently start passing).
- `check-` is one literal reserved head, closed — not a `VerbLex`-wide production. Generalizing it
  to every `VerbLex` verb was considered and rejected (ADR-0014 Alt C): it would open a second,
  broader avenue for verb-shaped skill names undermining §14.1's own narrowness rationale, making
  "is this a skill or could it be read as command-shaped" no longer decidable from the lexicon
  alone.

**Exemption burn-down:** on landing, exactly 32 of the estate's then-156 exemptions retired via
`naming.manifest.json`'s shrink-only `exemptions` array (156 → 124) — the 22 `-rules` names in
full, plus 10 of the 14 exempted `check-<noun>` names (the 4 quantifier non-goals above stay
exempt). `check-doc`, `check-skill`, `check-stage`, `naming-rules`, and `product-lifecycle-rules`
were never in `exemptions` (they already parsed clean); their passing reason changes from
accidental to designed under this amendment, not counted in the 32.

### 14.3 SPEC-type frontmatter and section restructure (2026-08-16, issue #372, Kim's ruling)

**Ruling:** this spec gained `docs/skills/doc-writing-rules` SPEC-type frontmatter
(`doc-type: spec`) and was reorganized under that type's four required `## ` headings —
Requirements, Non-goals, Examples, Acceptance — so `docs/scripts/doc_lint.py` covers it as a
functional document. **Form only, no substance change:** every normative sentence in §§1–13 is
unchanged verbatim; sections `2.`–`12.` keep their original numbers (now written as
`REQ-00N — N. Title` or `N. Title` headings, one level deeper) so every existing citation into
this spec by number — from ADR-0011, ADR-0014, `validate.py`, `overhaul-execute/SKILL.md`,
`authorkit/README.md`, and this file's own §14.1/§14.2 — still resolves without edits.

Sections `2.`–`9.` (Taxonomy, Grammar, Lexicons, Parse algorithm, Directory & file layout,
Composition relations, Frontmatter schema, Two-level taxonomy) became REQ-001 through REQ-008
under `## Requirements`; §10 (Migration posture) moved under `## Non-goals` (its own
scope-limiting content — "enforce for new names; grandfather existing" — was already the closest
existing fit, alongside a new pointer to §8.5 "What stays out"); §12 (Worked examples) moved
under `## Examples`; §11 (Validator) moved under `## Acceptance`, its 8 checks labeled
AC-001–AC-008 against their nearest REQ. §1, §13, and §14 kept their original numbering and
position unchanged.

**Why:** docs-checker flagged this spec (PR #368 review, 2026-08-16) as "not a functional
document — no doc-type frontmatter" despite being ADR-0011's own ratified naming canon.
Frontmatter-only was investigated first and found infeasible without content change — `doc_lint`
hard-requires the four headings with no exemption path (findings posted to #372:
`https://github.com/kimgranlund/claude-plugins/issues/372#issuecomment-5307727282`). Kim ruled
to restructure rather than carve a doc_lint exemption or leave the spec permanently out of the
type contract (the other two options raised in that finding).

**Rejected alternatives** (from the original #372 finding, superseded by this ruling): (1) add a
`doc_lint` exemption/grandfather mechanism for legacy specs predating the section contract —
rejected because T3 is FAIL-tier by design, not WARN, and a bespoke carve-out for one file
undermines the "template is the contract" invariant the check exists to enforce; (2) leave
`spec-naming-convention.md` permanently out of `doc_lint`'s scope — rejected because ADR-0011's
own canon spec being invisible to the docs type contract it was written to satisfy for every
*other* artifact was the actual gap #372 exists to close.

**Non-goal:** this amendment does not touch any normative rule in §§2–12, the `-agent` reserved
head, the §14.1 reverse-wrapper amendment, the §14.2 `-rules`/`check-` amendment, or
`naming-audit/scripts/validate.py`'s parsing logic — it is a docs-plugin frontmatter/structure
fix, not a naming-grammar change.

### 14.4 Orchestrator `-agent` tail becomes optional; scope resolves against ObjectVocab ∪ ProcessLex (2026-08-16, issue #433, ADR-0015 ratified 2026-08-16)

**Ruling authority:** ADR-0015 (`.claude/docs/adr/0015-orchestrator-agents-drop-agent-suffix.md`),
ratified by Kim 2026-08-16, superseding three clauses of ADR-0011 D7 only (the orchestrator
agent production's hardcoded `-agent` tail; the orchestrator scope-resolution pool; the
lexicon disjointness set the AC-008 gate checks). ADR-0011 itself is not edited — accepted
ADRs are append-only (T4); the supersession is recorded by ADR-0015's `supersedes:` field.

**Validator change:** three changes to `naming-audit/scripts/validate.py`'s `Grammar.parse`,
`kind == "agent"` branch, mirroring §14.1/§14.2's positive/negative/regression pattern:

1. **D1 — the orchestrator production accepts a bare `{scope}-{role}` name.** A
   `-agent`-tailed name still strips the tail and tries primary (residue ∈ skills) then
   orchestrator (residue's terminal ∈ RoleLex); a bare name tries orchestrator only
   (terminal ∈ RoleLex); a name that is neither fails with a diagnostic naming both roads.
   The primary production and the skill-side reserved-head rejection are unchanged.
2. **D2 — the orchestrator scope phrase resolves against `ObjectVocab ∪ ProcessLex`,
   for both spellings.** One more resolution pool built once at `Grammar.__init__`,
   deliberately narrower than §14.2 D1's three-way union (no `TopicLex` — a seat
   coordinates a thing or a process, never a reference-doc topic word). `build`
   registers in `ObjectVocab` (needed for `build-leader`; `planning`/`review` already
   sit in `ProcessLex`).
3. **D3 — `RoleLex` gains a disjointness check against `ObjectVocab ∪ ProcessLex`,**
   one more `lexicon_errors` intersection alongside the existing `VerbLex ∩ ProcessLex`
   check (AC-008).

**Selftest fixtures** (mirroring §14.1/§14.2's triad): positive `team-leader` (ObjectVocab
scope) and `review-leader` (ProcessLex scope) parse; legacy `product-leader-agent` still
parses (regression); negative `estate-audit` bare in `agents/` fails (no RoleLex terminal,
no `-agent` tail); negative `team-leader` minted as a skill fails (`leader` resolves in no
lexicon or vocab); a manifest fixture with a RoleLex word also registered in ObjectVocab
raises the D3 manifest error.

**Non-goal:** this amendment does not touch command grammar (§3.1), skill grammar (§3.2,
incl. §14.1/§14.2), the primary agent production, `performs` arithmetic (AC-005), the
`-agent` reserved head on skills, ADR-0011 D8's shrink-only exemption ratchet, or any
existing exemption (124 → 124, none retired or admitted by this change).

**Exemption count:** unchanged (124 → 124) — this amendment admits `{scope}-{role}` names
by grammar conformance, never by exemption; D8's ratchet is untouched.

### 14.5 `lead-` reserved verb-first head on the command grammar (2026-08-17, issue #433, ADR-0016)

**Ruling authority:** ADR-0016 (`.claude/docs/adr/0016-lead-reserved-head-for-commands.md`),
ratified 2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead, confirming the
overnight standing-directive authorization), superseding one clause of
ADR-0011 D7 only (the command production's verb-terminal requirement as §3.1 adopted it).
ADR-0011 and ADR-0015 are not edited — accepted ADRs are append-only (T4).

**Grammar change (D1):** the command grammar gains one reserved verb-first head:

```
command := "lead" "-" scope        lead-team, lead-review
```

`lead` is a literal (like §14.2's `check-`), not a `VerbLex` member. `scope` resolves via
the same greedy longest-match algorithm against the orchestrator scope pool `ObjectVocab ∪
ProcessLex` (ADR-0015 D2's pool, shared deliberately: a `/lead-{scope}` command makes the
host session adopt the orchestrator seat whose scope that is — one vocabulary for what a
seat coordinates, whether the seat is a dispatched agent or the host itself). No `TopicLex`.

**Validator change (D2):** `naming-audit/scripts/validate.py`'s `Grammar.parse` recognizes
the head on BOTH the `kind == "command"` and `kind == "skill"` branches, reusing
`resolve_orchestrator_scope` — the live `/lead-*` surfaces are command-species skills
(`user-invocable: true`, `disable-model-invocation: true`, no `commands/` dir), and §6
decides kind by directory, exactly the placement logic that put ADR-0014's `check-` head on
the skill branch. On the skill branch the check sits BEFORE the object-process check
(`lead-review`/`lead-planning` have `ProcessLex` terminals — the §14.2 dead-code hazard).

**Selftest fixtures** (mirroring §14.1/§14.2/§14.4's triad): positive — `lead-team`,
`lead-product`, `lead-build` (ObjectVocab scopes) and `lead-planning`, `lead-review`
(ProcessLex scopes) parse clean as skills, and `lead-team` parses clean as a command;
negative — a non-`lead` verb-first command (`audit-team`) still fails; negative —
`lead-{unregistered}` (`lead-intake`'s class) fails on both branches; regression —
object-first commands and object-process skills unaffected.

**Exemption count:** 124 → 120. Four exemptions retire (`lead-build`, `lead-planning`,
`lead-review`, `lead-team` — they conform by grammar from ADR-0016 on); `lead-intake` stays
exempt (`intake` resolves in no lexicon or vocab, and registering a word solely to clear one
exemption is the dilution ADR-0014 Alt B / ADR-0015 Alt E rejected); `lead-product` mints as
a new conforming name (unblocking issue #433's product-seat command leg). D8's shrink-only
ratchet is honored in its burn-down direction and untouched in its rule.

**Non-goal:** this amendment does not touch `VerbLex` (no verb-first production generalizes
from this literal), skill grammar otherwise (§3.2, §14.1, §14.2), agent grammar (§3.3,
§14.4), the `-agent` reserved head, or the wrapper production. `lead-*` names in `agents/`
still fail; the agent seats (`team-lead`, `build-lead`, `intake-lead`) stay exempt exactly
as ADR-0015 D4 left them. [Amended 2026-08-17, issue #477: `team-lead`/`build-lead` renamed
`team-leader.md`/`build-leader.md` and now conform by grammar (§3.3 orchestrator production);
`intake-lead` renamed `intake-leader` and conforms once `intake` enters `ObjectVocab` (§14.7
D2) — the `intake` registration this amendment declined is exactly what S8/ADR-0018 later
registers, on new second-consumer evidence. This line's exemption list is historical as of
that rename; see §14.7 for the current state.]

### 14.6 `RoleLex` gains the execution-seat suffixes (2026-08-17, issue #477, ADR-0017)

**Ruling authority:** ADR-0017 (`.claude/docs/adr/0017-rolelex-execution-seats.md`), ratified
2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead), superseding ADR-0011 D7's
"≤4 entries to start" sizing clause as this spec's §4 adopted it, and ADR-0015 D1's
coordinator-only framing of the `{scope}-{role}` production. ADR-0011 and ADR-0015 are not
edited — accepted ADRs are append-only (T4); ADR-0015 D2 (scope pool), D3 (disjointness), and
D4 (exemption posture) stand unchanged.

**Lexicon change (D1):** `RoleLex` grows from `{leader, orchestrator, coordinator}` by 10
members: `checker, runner, planner, watcher, finder, sorter, cleaner, judge, builder,
writer`. No grammar production changes — §3.3's `{scope}-{role}` shape already covers any
`RoleLex` terminal; this amendment only widens which words qualify, so the estate's dominant
execution-seat naming pattern (`code-checker`, `experiment-runner`, `decision-watcher`, …)
parses as the same production coordinators already use, instead of needing a fresh exemption
per new reviewer/standing seat.

**Anti-ambiguity gate (D2, ADR-0015 D3):** each of the 10 candidates checked against the live
manifest — none collides with `ObjectVocab` or `ProcessLex` (exact-token disjointness; near
misses `builder`/`build`, `planner`/`planning`, `writer`/`writing`, `checker`/`checking` are
harmless because disjointness is exact-token and `TopicLex` carries no disjointness
requirement, ADR-0014 D3). Gate: PASS × 10.

**Cost (ADR-0015's own caveat, carried forward):** each of the 10 is now permanently barred
from future `ObjectVocab`/`ProcessLex` registration by D3's disjointness — a one-way door,
cheap here because all 10 are agentive nouns with no plausible object/process reading.

**Deliberately not widened:** bare `RoleLex` terminals with no scope token (`builder`,
`planner`) stay exempt — the `{scope}-{role}` production requires a resolvable scope phrase;
conforming them is a rename question (e.g. `feature-builder`), out of this amendment's scope.
`lead` is deliberately not added to `RoleLex` — it is ADR-0016's reserved *command* head, and
`leader` already covers the role; `intake-lead` follows the `team-lead → team-leader`
precedent (§14.4/§14.5 history) via direct rename instead (done same-change, issue #477).

**Selftest fixtures** (mirroring §14.4's triad): positive — `code-checker`,
`experiment-runner`, `decision-watcher` (`ObjectVocab` scopes) and `review-planner`
(`ProcessLex` scope) parse clean as agents under the grown `RoleLex`; negative — a bare
`RoleLex` terminal with no scope token (`builder`) still fails.

**Exemption count:** measured baseline 118 (D8's ratchet had already dropped 2 of the
proposal's projected 120 by this tree — `team-lead`/`build-lead` conformed via an earlier
rename, ahead of this amendment). This amendment plus §14.7 together retire 33 (118 → 85);
see §14.7 for the combined burn-down since the two amendments landed as one PR.

### 14.7 `make-`/`file-` reserved skill heads + ObjectVocab registrations (2026-08-17, issue #477, ADR-0018)

**Ruling authority:** ADR-0018 (`.claude/docs/adr/0018-make-file-reserved-heads.md`), ratified
2026-08-17 by Kim (live AskUserQuestion via plugins-team-lead). Amends §3.2 by the §14.2
mechanism (ADR-0014). ADR-0014 and ADR-0016 are not edited — accepted ADRs are append-only
(T4); the `check-`/`lead-` heads and their selftest triads are unchanged.

**Grammar change (D1):** two literal verb-first heads join `check`/`lead` on the skill
grammar:

```
skill := "make" "-" object-phrase     make-skill, make-doc, make-reference
skill := "file" "-" object-phrase     file-bug, file-feature, file-task
```

Residue resolves against `ObjectVocab` ONLY (never the `-rules` tail's union pool) — same
mechanism as `check-`, same reasoning: `make-`/`file-` names denote a real object the forge or
intake family produces, not a process. The literal head set is now closed at exactly
`{check, lead, make, file}` — ADR-0014 Alt C (generalizing to all of `VerbLex`) stays
rejected; `make`/`file` already sit in `VerbLex` for the unrelated object-verb command
production (§3.1) and command-terminal skill wrapper — no conflict, the head check is a
distinct literal-token branch on the skill grammar only.

**Validator change (D2):** `Grammar.parse`'s `kind == "skill"` branch gains the two head
checks immediately after the `lead-` head and before the `ProcessLex` terminal check — same
dead-code-hazard placement as `check-`/`lead-` (`make-pack`'s residue `pack` and `file-task`'s
residue `task` are plain `ObjectVocab` members that a later placement would never reach for
some names). Critically, this sits AFTER the `-agent` reserved-tail check that opens the
branch (§3, one reserved head `-agent`): the tail strips first, unconditionally, which is
what keeps `make-agent` permanently failing even though `make` is now a valid head —
tail-before-head, not a special case.

**ObjectVocab registrations (D3, 10 entries):** `experiment` (null plural), `decision`
(`decisions`), `fact` (null — deliberately, to avoid a collision with `ProcessLex`'s `facts`),
`code` (null), `wording` (null — dual membership with `TopicLex`'s `wording` is redundancy,
not ambiguity; `TopicLex` carries no disjointness requirement, ADR-0014 D3), `intake` (null),
`reference` (`references`), `rubric` (`rubrics`), `vision-memo` (null, multi-token, no
existing entry starts with `vision`), `llms-txt` (null, multi-token). All 10 gated per §5's
per-entry anti-ambiguity check (no prefix collision with an existing multi-token entry, no
existing name's parse made ambiguous) — PASS × 10.

**The `intake` reversal, named explicitly:** ADR-0016 §14.5 declined registering `intake`
"solely to clear one exemption" (Alt B / Alt E dilution concern). This amendment registers it
anyway, on different evidence than ADR-0016 had: one live consumer (`docs:lead-intake`, which
retires from this registration alone via the existing `lead-` head) plus one deliberate
consumer this same change creates (`docs:intake-leader`, the `intake-lead → intake-leader`
rename executed alongside this amendment, conforming via `{scope=intake}-{role=leader}`).
The second-consumer bar ADR-0016 asked for is met prospectively, not retrospectively — recorded
here so no future reader mistakes this for a silent reversal on thread-comment authority alone.

**Selftest fixtures** (mirroring §14.2/§14.5's triad): positive — `make-doc`,
`make-reference`, `make-rubric`, `make-vision-memo`, `make-llms-txt`, `file-bug`, `file-task`
parse clean under the new heads; negative — a non-reserved verb head (`sort-issues`) still
fails, `make-{unregistered scope}` still fails; regression — `make-agent` keeps failing on the
`-agent` tail (the tail-before-head fixture named in D2).

**Exemption count (combined with §14.6, one PR):** measured baseline 118 (2 below the
proposal's projected 120 — `team-lead`/`build-lead` had already conformed via rename ahead of
this tree). Re-running the estate audit at `--scope grammar` with exemptions emptied measures
86 genuine grammar failures under the new grammar (19 fewer skill exemptions from the
`make-`/`file-` heads and B-registrations, 12 fewer agent exemptions from §14.6's RoleLex
growth, plus `lead-intake` retiring via B6's `intake` registration) — 118 → 86 by grammar
conformance alone. One further entry, `intake-lead`, was a dead exemption after this same
change's `intake-lead → intake-leader` rename: no artifact named `intake-lead` remains to
exempt, so it is removed as housekeeping rather than retired by conformance — final count
118 → 85, one below the proposal's 86 projection. No exemption outside the proposal's own
enumeration was retired; every retirement (conformance-based or dead-entry housekeeping) was
verified against a live re-run, never forced to match the projection (per this ticket's own
instruction).

**Non-goal:** the optional B11–B13 registrations (`component`, `flow`, `layout`) proposed
alongside B1–B10 are NOT included — out of this amendment's ratified scope; the three
screens checkers they would have retired (`component-checker`, `flow-checker`,
`layout-checker`) and `make-component` stay exempt pending a future amendment.

### 14.8 `bind-`/`fork-`/`sub-` reserved heads supersede `lead-` (2026-08-17, issue #520, ADR-0020 D3)

**Ruling authority:** ADR-0020 (`.claude/docs/adr/0020-fleet-vocabulary-and-binding-heads.md`),
accepted 2026-08-17 by Kim (rejected 16:03, ratified 16:04, tie-break "ratify stands" 16:21,
FINAL RULING "ACCEPTED" 16:31 — all live, via plugins-team-lead; see gh#518's full thread).
Supersedes ADR-0016 D1/D2 in full (the `lead-` reserved head and its scope-resolution
clause). ADR-0016 is not edited — accepted ADRs are append-only (T4); §14.5 above stays as
written, historical as of this section.

**Grammar change (D1):** the command grammar's one reserved verb-first head becomes three:

```
command := ("bind"|"fork"|"sub") "-" scope     bind-team, fork-agent, sub-agent
```

Each of `bind`, `fork`, `sub` is a literal (like §14.2's `check-`), not a `VerbLex` member.
`scope` resolves via the same greedy longest-match algorithm against the orchestrator scope
pool `ObjectVocab ∪ ProcessLex` (ADR-0015 D2's pool, unchanged) — the head names which
platform mechanic adopts the seat (`bind-`: the host session itself, no spawn; `fork-`:
`context: fork`; `sub-`: an `Agent` dispatch), the scope names which seat.

**`lead-` retirement, not deletion (D3, this ticket's own sequencing finding):** ADR-0020's
own wave order (#519→#524) sequences the six live `/lead-*` surfaces' rename to wave 5
(#523), which is NOT atomic with this grammar change (#520) — both are only `Blocked-by`
#520, not by each other. Retiring `lead-` as an open production immediately, with no interim,
would force those six into `exemptions` — but D8's ratchet is shrink-only (ADR-0011), so six
new entries could never be shed and this ticket's own acceptance criterion ("the exemptions
array has not grown") would be unmeetable by construction. Resolution (conservative reading,
posted as Findings on gh#520 rather than assumed): `lead-` becomes a CLOSED grandfather
production — `LEAD_HEAD_GRANDFATHER` in `validate.py`, exactly `{lead-team, lead-build,
lead-planning, lead-product, lead-review, lead-intake}`, never grown — instead of the open
`lead-{any resolvable scope}` production ADR-0016 D1 defined. A name on the list still
resolves its scope against the same orchestrator pool as before; any `lead-*` name NOT on the
list (a brand-new mint) now fails grammar outright, even if its scope would resolve fine.
Deprecated 2026-08-17; wave 5 (#523) deletes the grandfather set and both `lead-` code
branches outright when it renames those six to `bind-{scope}` — this is scaffolding for one
sequencing gap, never a permanent fourth head.

**Validator change (D2):** `Grammar.parse`'s `kind == "command"` and `kind == "skill"`
branches each gain the `bind-`/`fork-`/`sub-` head check (same placement logic as `lead-`
always used — before the object-process/verb-terminal fallback, since a scope residue can
land a `ProcessLex` terminal), followed by the now-closed `lead-` check consulting
`LEAD_HEAD_GRANDFATHER`.

**Selftest fixtures** (mirroring §14.5's triad, extended): positive — each of `bind-`/`fork-`/
`sub-` parses clean on both the skill and command branches (ObjectVocab and ProcessLex
scopes; the skill-branch fixtures deliberately avoid an `agent` scope, which collides with
the unconditional `-agent` reserved-tail check — the same dead-code hazard `make-agent`
proves in §14.7, not a defect in this head); negative — a non-reserved verb-first name still
fails, and `{head}-{unregistered scope}` fails on both branches, for each of the three heads;
negative — a brand-new `lead-*` mint (`lead-widget`, scope resolvable) is REJECTED on both
branches, naming the retirement explicitly; regression — all six grandfathered `lead-*`
names still parse clean; regression — object-first commands and object-process skills
unaffected.

**Exemption count:** unchanged, 85 → 85. This wave conforms zero new names and retires zero
exemptions by design — the six live `/lead-*` surfaces were never in `exemptions` (they
conformed by grammar under ADR-0016), and they stay conforming by grammar under the new
closed grandfather production; nothing here touches D8's ratchet in either direction.

**Non-goal:** this section does not rename any of the six live `/lead-*` surfaces (wave 5,
#523) or `team-leader`/`leading-teams`/`team-or-solo-rules` (waves 3/4/6, #521/#522/#524);
it does not register `marshal`/`orchestration` (wave 1, #519, already landed); it does not
touch `VerbLex`, skill grammar otherwise (§3.2, §14.1, §14.2, §14.7), agent grammar (§3.3,
§14.4, §14.6), or the `-agent`/wrapper productions.

### 14.9 Reverse-wrapper extended to skill-as-command, no sibling command required (2026-08-17, issue #525)

**Ruling authority:** issue #525's live ruling (Kim, 2026-08-17): "Successor shape:
skill-as-command (`user-invocable: true` on the SKILL.md itself). Migration posture: CONVERT
ALL — all 15 command wrappers (teamwork ×5, authorkit ×10) convert in a one-shot campaign, no
grandfathering." This section amends §14.1 to make that ruling's authorkit slice
grammar-legal — §14.1 is not edited (draft-amendment convention, this file's own §14.1–§14.8
precedent: append, never rewrite a landed section).

**The conflict this closes:** §14.1's reverse-wrapper production requires "an identically-named
command exists in the same plugin root and wraps it" as the precondition licensing a
verb-terminal skill name (`overhaul-execute`, and — newly minted as skills this same ticket —
`rename-execute`/`exemption-retire`, previously command-only per §14.1's own "Why" section).
Issue #525's ruling retires the sibling command entirely in favor of one file carrying both
surfaces. Read literally, §14.1's precondition becomes permanently unsatisfiable for the exact
names it was written to license the moment their wrapper commands are deleted — a direct
collision between two rulings this section resolves in the newer ruling's favor, naming the
supersession explicitly rather than leaving it to be rediscovered.

**Ruling:** a skill's verb-terminal name (terminal ∈ VerbLex, not ProcessLex) is ALSO legal —
in addition to, never instead of, §14.1's original command-sibling path — when the skill itself
carries `user-invocable: true` and has NO sibling command at all. Object-prefix resolution
against `ObjectVocab` still applies in both branches; the license is the dual-access fact (one
procedure, two surfaces — §14.1's own framing), never the skill's say-so alone. `VerbLex ∩
ProcessLex = ∅` (§4) is untouched — this is a second precondition on the same production, not a
new lexicon or a relaxed disjointness rule.

**Why this and not a §14.1 rewrite:** §14.1's own ratified authority (Kim's Sign-off on #241) was
narrowly "a command wraps this skill" — rewriting it in place to also cover the no-command case
would blur which ruling licenses which shape as the estate's history is read back later. Amending
forward, the same convention every prior 14.x section in this file already uses, keeps both facts
recoverable: §14.1 explains why the wrapper-sibling path exists at all (the `overhaul-planning` →
`overhaul-execute` symmetry, `rename-planning` → `rename-execute`'s original command-only gap);
§14.9 explains why that path stopped being the ONLY one.

**Validator change:** `naming-audit/scripts/validate.py`'s `Grammar.parse` skill branch's
existing reverse-wrapper condition (`name in commands`) becomes `name in commands OR
user_invocable` — `Grammar.parse` gains a `user_invocable` parameter, threaded from the
artifact's own `user-invocable` frontmatter field at the single call site in `run()`. A
verb-terminal skill name with NEITHER a command sibling NOR `user-invocable: true` still fails
exactly as before this amendment (the negative control alongside a positive fixture for each of
the two now-independent paths and a regression fixture proving the original §14.1 command-sibling
path is unaffected).

**Non-goal:** this section does not touch command grammar (§3.1), agent grammar (§3.3), the
`VerbLex`/`ProcessLex` disjointness invariant (§4), or the plain object-process/nominal skill
productions for a terminal that already resolves via `ProcessLex` or `ObjectVocab` alone (`audit`,
`planning`, `authoring` — the process-terminal skills this same campaign also converted needed no
grammar change at all, since their legality never depended on a sibling command in the first
place). It does not retire or deprecate §14.1's command-sibling path — a future plugin may still
ship a verb-terminal skill behind a real wrapper command if that shape ever earns a reason to
exist again; this section only stops the wrapper's absence from being read as evidence against a
name §14.1 already earned the right to carry.

**Landed same-change:** `authorkit`'s 10 command wrappers (issue #525's authorkit slice) —
`overhaul-execute` converts in place; `rename-execute` and `exemption-retire` mint as skills for
the first time (previously command-only, zero skill siblings, per §14.1's own "Why" section); the
remaining 7 needed no grammar change (process-terminal names, always legal independent of any
wrapper). Exemption count unchanged (85 → 85) — this section conforms names that were already
either grammar-clean or licensed via §14.1, not previously-exempted debt.

### 14.10 `evals/` and `intent.md` join the §6.1 skill-folder closed set (2026-08-21, issue #861, ADR-0024)

**Ruling authority:** issue #861, tracing `plan-2026-08-brand-design-bloat-overhaul` seed S4 —
ruled 2026-08-21 (close-session leftovers round): "amend the spec, not the practice." `evals/`
was that ruling's direct subject; `intent.md`'s fate was the ticket's own deferred
sub-decision (Acceptance item 4), ruled inside the same ADR rather than reopened as a second
round.

**The gap this closes:** §6.1's closed set has read `SKILL.md` / `references/` / `scripts/` /
`assets/` since ADR-0011 landed the spec. `plugin-authoring.md`'s routing-surface invariant has
since mandated `evals/evals.json` estate-wide, and `make-skill`'s own forge has always produced
`intent.md` as its living build ledger — both top-level entries the closed set never named,
20/20 and 4/20 respectively in the brand-design sample that surfaced the staleness (27/estate
for `intent.md` at ratification). `authorkit`'s own `naming-audit` validator (`validate.py`'s
`ALLOWED_SKILL_ENTRIES`) already allow-lists both — this amendment brings the spec's prose in
line with code already shipped, never the reverse; no exemption or remediation debt is created,
since nothing that conformed to the validator yesterday stops conforming today.

**Ruling:** §6.1's closed skill-folder set grows from four entries to six: `SKILL.md` /
`references/` / `scripts/` / `assets/` / `evals/` / `intent.md`. `evals/` is proof the routing
surface holds — evaluated against by a script or judge, never itself loaded as procedure.
`intent.md` is a bare top-level *file* (like `SKILL.md`), never routed into `references/`: it
fails §6.2's passive-matter test for that folder on both axes (actively written to during a
skill's own forge; never a two-hop-discoverable reference a routed session reads at trigger
time) — full rationale, including why remediation-into-`references/` was considered and
rejected, lives in ADR-0024 D2.

**Non-goal:** this section does not touch the partition axis's other four answers, the
no-nested-skills rule, or the validator's blind-below-the-boundary posture (§6.1's own closing
paragraph) — all stand unamended. It does not touch §6.2's reference-index contract; `intent.md`
staying outside `references/` means it never needs an index row, by design.

**Validator change:** none owed — `ALLOWED_SKILL_ENTRIES` already reads the six-entry set this
section ratifies (verified against `authorkit/skills/naming-audit/scripts/validate.py` at the
ratification tree, 2026-08-21). Re-running `naming-audit --scope grammar` estate-wide is a
confirmation step, not a migration: zero new violations open, zero close.

### 14.11 §8's agent frontmatter schema amended to the measured convention (2026-08-21, issue #863, ADR-0025)

**Ruling authority:** ADR-0025 (`.claude/docs/adr/0025-agent-frontmatter-schema-matches-reality.md`),
ratified 2026-08-21 by Kim (close-session leftovers round, `plan-2026-08-brand-design-bloat-overhaul`
seed S5, Gate A approved 2026-08-21 — "amend the spec, don't backfill"). Supersedes ADR-0011's
§8 agent frontmatter schema only — identity fields `name`/`description`, the grammar/directory
rules (§§2–6), the composition-relations mechanism (§7), and the migration posture (§10) all
stand unamended. ADR-0011 is not edited — accepted ADRs are append-only (T4); §8 above is
edited in place per this file's own §3.1/§3.2/§6.1/§14.10 convention (prose amended inline,
never only logged here).

**Measured (2026-08-21, 40 agent files, `*/agents/*.md`):** 39/40 carry none of `kind`/
`author`/`created`/`last_updated`/`performs`/`autonomous_write`/`context` — the one exception,
`authorkit/agents/estate-audit-agent.md`, carries the full documented schema as a deliberate
self-dogfood (`authorkit`'s own `schema_scope: "full"` convention, issue #226/#224 ruling b,
already predates and is consistent with this amendment). Every one of the 40 carries `name`,
`description`, `model`, `tools`; 37/40 carry `effort`; 24/40 carry `skills`; 12/40 carry
`color`; 1/40 carries `disallowedTools`. A cross-plugin sample issue #863 named directly —
harness's `skill-checker`, teamwork's `builder`, docs' `doc-checker` — carries none of the
dropped fields either.

**Ruling:** §8's agent schema drops `kind` (an agent's kind is decided by directory + name-parse,
§5/§6 — never a declared field), `performs` (checked structurally off the name itself, §5 — §7's
relation table and its structural check are unamended, only the frontmatter-declaration claim is
dropped), `autonomous_write` and `context` (no agent declares either; the platform's own
dispatch mechanics and the `tools` grant already carry the distinction), and the provenance
block `author`/`created`/`last_updated`/`review_after` (zero adoption outside authorkit's own
internal self-check). `name`/`description` stay required; `model`/`tools`/`effort`/`skills`/
`color`/`disallowedTools` are documented as the measured, non-enforced convention. Commands and
skills are untouched by this amendment — their own frontmatter schema (§8.1's `kind` field,
§8.4's provenance block) stands exactly as written.

**Non-goal:** this section does not touch §7's relation table or the structural `performs`
check, command/skill frontmatter (§8.1/§8.3/§8.4 as they apply to those two kinds), the
grammar/directory rules (§§2–6), `authorkit`'s own internal `schema_scope: "full"` convention on
its own agents, or the migration posture (§10) — no exemption is created or retired by this
amendment.

**Validator change:** none owed — `naming.manifest.json`'s `schema_scope: "grammar"` already
routes estate-wide agents around the dropped fields' enforcement (issue #226/#224, predating
this ticket); this amendment ratifies the spec text to match validator behavior already
shipped, not the reverse. Re-running `authorkit:naming-audit` against brand-design's 4 agents is
a confirmation step, not a migration: zero frontmatter findings before and after this change.
