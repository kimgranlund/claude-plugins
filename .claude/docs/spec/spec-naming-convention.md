# Harness Artifact Naming Convention — Specification

**Status:** Draft v1.0 · **Applies to:** `.claude/` harness artifacts (agents, commands, skills) · **Enforced by:** `naming.manifest.json` + validator (CI gate, pre-mint gate in `/skill-create`)

---

## 1. Purpose

One canonical name per artifact, everywhere it appears. Kind, invoker, and composition relations are decidable from the name plus its location — mechanically, by string operations, with no registry lookup and no reliance on frontmatter honesty. Frontmatter must *agree* with the parse; it never decides.

Design principle: **syntax encodes invocation semantics**. The grammatical mood of a name mirrors how the artifact is invoked. Illegal names are unrepresentable under the grammar, not merely discouraged.

---

## 2. Taxonomy

Three kinds, partitioned by **invoker** — the one axis the platform actually enforces.

| Kind | Invoker | Surface | Grammatical form |
|---|---|---|---|
| **command** | User only (`/name`) | Slash autocomplete | Object-first verb phrase |
| **skill** | Model only (trigger-description match) | Description routing | Nominal / activity phrase |
| **agent** | Delegated (own context window) | Task delegation | Agentive nominal |

**Knowledge is a content pattern, not a kind, subtype, or suffix.** Some skills are mostly `references/` with a thin routing stub; the substrate matches descriptions identically either way, and relations target artifact names either way, so nothing in the tooling needs the distinction — the taxonomy does not invent one the validator would never read. Reference-shaped skills are named by the ordinary skill grammar (`naming-conventions`, `hcc-coding`), and their descriptions carry the consultation trigger.

**Dual access is composition, not a kind.** A capability that must be both user- and model-invocable is a skill plus a thin command wrapper. The wrapper relation is declared in the command's frontmatter (§7).

---

## 3. Grammar

```
command   := object "-" verb                    skill-create, work-start
skill     := object "-" process                 skills-audit, ui-layout-planning
          |  nominal-phrase                     naming-conventions   (looser production)
agent     := skill-name "-" "agent"             skills-audit-agent   (primary)
          |  scope "-" role "-" "agent"         team-leader-agent    (orchestrators only)
```

One reserved head: `-agent`.

### 3.1 Commands — object-first

Commands are object-first (`skill-create`, not `create-skill`) so that slash autocomplete groups operations by object: `/skill-<tab>` surfaces `skill-create`, `skill-review`, `skill-lint` together. Discovery ergonomics outrank reading-as-English for a user-invoked surface.

The terminal token must be a member of `VerbLex`.

### 3.2 Skills — nominal, process head preferred

The canonical skill production is `{object}-{process}` (`skills-audit`, `entry-file-authoring`). The terminal token should be a member of `ProcessLex`. Skills that are genuinely not object-process shaped — report generators, routers, and reference corpora — use the nominal-phrase production, but every token must still resolve in the lexicons (§4): the looseness is in the *shape*, never in the *vocabulary*.

Reading test (procedural): the name completes "this artifact teaches how to do ___."
Reading test (reference-shaped): the name completes "consult ___ for this."

### 3.3 Agents — derived from skills

The primary production is `{existing-skill-name}-agent`. An agent's capability must have an authored skill spec; the peer audit verifies this by stripping `-agent` and asserting the skill exists.

The single escape hatch is the orchestrator production `{scope}-{role}-agent` (`team-leader-agent`), for agents that coordinate rather than execute and therefore have no patient object. `RoleLex` starts at ≤4 entries and grows only by manifest PR.

Reading test: the name completes "hand this off to the ___."

---

## 4. Lexicons

Four lexicons live in `naming.manifest.json`. Three are closed (additions require a manifest PR — this is the governance gate); one grows by registration.

| Lexicon | Contents | Membership |
|---|---|---|
| `VerbLex` | Command terminal tokens: `create`, `review`, `lint`, `sweep`, `start`, `finish`, `run`, `mint`… | Closed |
| `ProcessLex` | Skill terminal tokens: `audit`, `planning`, `authoring`, `triage`, `review`ᵈ, `migration`… | Closed |
| `RoleLex` | Orchestrator roles: `leader`, `orchestrator`, `coordinator` | Closed, ≤4 to start |
| `ObjectVocab` | Domain objects: `skill`/`skills`, `issue`/`issues`, `pr`, `ui-layout`, `entry-file`, `harness`… | Registered |

**Disjointness invariant:** `VerbLex ∩ ProcessLex = ∅`. A token lives in exactly one. Where a word plausibly belongs to both (e.g. `audit`), it is assigned to one lexicon and the other kind uses an alternative (`audit` ∈ ProcessLex; a command triggering an audit uses `run` or wraps the skill per §7). This disjointness is what keeps command/skill classification decidable from the name alone as a lint check, even though directory location is the authoritative discriminator (§6).

**ObjectVocab registration** records, per entry:

- `canonical` — the one true form (`pr`)
- `plural` — inflected form for imperative objects where applicable (`issues`)
- `banned_aliases` — rejected synonyms (`pull-request`, `pull-requests`)
- Registration is **rejected** if the new token creates parse ambiguity with any existing multi-token entry (§5).

Brand tokens (`adia`) are banned from ObjectVocab. Plugin namespacing is the marketplace prefix's job (`plugin-name:artifact-name`); embedding brand in the local name double-prefixes and forces renames on plugin moves.

**Plurality rule:** objects of imperatives pluralize where natural (`sweep-issues`); attributive objects do not (`issue-triage`, per "issue tracker" not "issues tracker"). Both inflections resolve to the same ObjectVocab entry.

---

## 5. Parse algorithm

Deterministic; specified here so no two tools hand-roll it differently.

1. **Strip the reserved head:** `-agent`, if present. What was stripped fixes kind candidacy.
2. **Longest-match resolve** the remaining token sequence against ObjectVocab (multi-token entries like `ui-layout` match greedily, left-anchored).
3. **Classify the terminal token** of the residue against `VerbLex` / `ProcessLex` / `RoleLex`.
4. **Every token must resolve.** Any token that is in no lexicon and no ObjectVocab entry fails the parse.

Ambiguity is prevented at write time, not resolved at read time: the ObjectVocab registration gate (§4) rejects entries that would make step 2 ambiguous. Example: with skill `ui-layout-planning` extant, `ui-layout-planning-agent` parses uniquely as agent-of-skill because `-agent` strips first and the residue matches an existing skill name before any decomposition is attempted.

---

## 6. Directory & file layout

Invoker is decided by **location**; the grammar corroborates it.

```
.claude/
  commands/
    skill-create.md
  skills/
    skills-audit/SKILL.md
    naming-conventions/SKILL.md      # reference-shaped: thin stub + references/
  agents/
    skills-audit-agent.md
```

**Folder equals canonical name, no decoration.** One canonical string everywhere — no folder-level transforms to validate, no discovery-compatibility risk. Reference-shaped skills are visually indistinct from procedural ones in a listing; if that view is ever needed operationally, it is a derived report (`naming-audit` lists skills with no ProcessLex head), never a naming rule.

Validator rule: `folder == name` for every artifact.

### 6.1 Skill folder layout — closed set

```
skills/{name}/
  SKILL.md          # required — routing stub + procedure (thin stub for reference-shaped skills)
  references/       # passive matter: read into context, never executed
  scripts/          # executable matter: code the procedure invokes
  assets/           # inert payload: images, fixtures, binary/static files
```

Four top-level entries, nothing else. The partition axis is **how content participates when the skill runs**: `SKILL.md` is loaded into context; `references/` is selectively read into context; `scripts/` executes *outside* context — deterministic logic belongs in a script the skill calls, never in prose the model re-derives; `assets/` is neither read nor executed, only addressed by path. Every file answers one question — *context, computation, or payload?* — and the answer decides its folder.

Boundary validation (the validator checks these and nothing deeper):

1. `SKILL.md` exists.
2. No top-level entries outside the closed set — a stray `docs/`, `notes.md`, or `old/` at the skill root fails lint. Unclassified top-level matter is how skill folders become junk drawers.
3. Nothing under `scripts/` is referenced from outside the skill — encapsulation holds in both directions.
4. **No nested skills.** A skill containing sub-capabilities that want their own triggers is decomposed into sibling artifacts with `requires` edges, never a hierarchy — hierarchical skills would make the router's matching ambiguous (parent or child?) and break the flat namespace the parse depends on.

Below the boundary, the validator is deliberately blind: internal file names, nesting, and formats are the author's domain. Validation pressure inside a skill's internals is the §9 signal that content wants to be an artifact — never a reason to grow the validator.

### 6.2 Content organization within the layout

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

## 7. Composition relations — declared in frontmatter, graph derived

Composability comes from the **shared ObjectVocab**, not from shared name shapes. Relations are **declared in the frontmatter of the depending artifact** — never in a central registry. One authority per fact: a relation lives with the artifact that holds it; the manifest holds only lexicons and exemptions; the estate-wide relation graph is *compiled* from frontmatter by the validator, never hand-maintained. A central `relations` registry would force two files to agree about one fact, which is the drift shape this spec exists to kill.

| Relation | Declared by | Field | Validator check |
|---|---|---|---|
| agent **performs** skill | the agent | `performs: skills-audit` | value == name minus `-agent`; skill exists |
| command **wraps** skill | the command | `wraps: naming-audit` | skill exists; skill is model-invocable |
| artifact **requires** skill | the consumer | `requires: [naming-conventions]` | each exists; compiled graph is acyclic |

`performs` is redundant with the string arithmetic by design — the redundancy is the check. A rename that touches one side and not the other fails loudly instead of drifting silently.

`requires` is the single dependency edge: "must exist and be available." Whether the dependent *invokes* the target's procedure or *consults* its references is visible in the dependent's body, where behavioral distinctions belong — a second edge type (`consults`) would encode in metadata what the body already states, and edge types that duplicate body content are the frontmatter equivalent of comments that restate code.

The **wrapper pattern** is how dual access works under the strict invoker partition: a model-invocable skill gains user access via a thin command (`/naming-audit` → `wraps: naming-audit`). Every artifact keeps exactly one invoker; dual access is composition, not a fourth kind.

Derived-graph audits (all mechanical): dangling endpoints (relation references a nonexistent artifact), orphaned agents (`performs` disagreement), and `requires` cycles.

---

## 8. Frontmatter schema

Frontmatter is the **authoring surface** for everything the tooling reads. The rule that keeps it from rotting: **every field in this schema is validated; no field enters the schema unless something reads it.** Fields nothing validates are prohibited, not optional — ungoverned metadata is where frontmatter lies accumulate.

### 8.1 Identity (required, all kinds)

```yaml
name: skills-audit          # canonical; == folder; parseable per §5
kind: skill                 # command | skill | agent
description: >              # the trigger contract — governed by
  Use when …                # skill-authoring-standards, not this spec
```

The validator asserts agreement, never trusts declaration: name parse + directory → **decided kind**; frontmatter must match. Disagreement is a lint failure. Frontmatter is an agreement check, never a tiebreaker — the specific defense against the rename-drift class (`entry-file-author` / `claude-md-author`) where a name silently stops meaning what the metadata claims.

### 8.2 Relations (per §7, on the depending artifact)

```yaml
performs: skills-audit             # agents
wraps: naming-audit                # commands (dual-access)
requires: [naming-conventions]     # any kind — deps that must exist and be available
```

### 8.3 Invocation policy and tool grants (required for agents and mutating commands)

```yaml
# agents
autonomous_write: false     # agent may not mutate the estate; report-only
context: isolated           # isolated | inherited
tools: Read, Glob, Grep, Bash(python */scripts/validate.py *)

# commands
mutates: true               # touches files beyond its own output
confirm: required           # required | none — human gate before mutation
allowed-tools:
  - Read
  - Edit
  - Bash(git mv *)
```

Policy fields are **enforced contracts, not documentation**: the validator asserts `mutates: true ⇒ confirm: required` unless the command is in a reviewed allowlist, and any agent lacking `autonomous_write` fails closed (treated as `false`). This transposes the product-side hard invariant into the harness: no artifact acquires write authority by omission.

**Tool grants are where policy materializes** — and declaring them also removes runtime permission interruptions, so least-privilege and ergonomics are the same move. Rules:

- Every artifact declares the minimum tool set its body actually uses. `Bash` grants are always **scoped patterns** (`Bash(git mv *)`), never blanket — enumerate the legal set, reject by default, same as the lexicons.
- **Policy/capability coherence is validated:** `autonomous_write: false` ⇒ no `Edit`, `Write`, or unscoped `Bash` in the agent's tools. `mutates: true` ⇒ the command declares a write-capable tool; `mutates: false` ⇒ it declares none. Divergence between the policy fields and the grants is a lint failure — policy asserts, grants enforce, and neither may drift from the other.
- The estate's mutation topology becomes grep-decidable: which artifacts can write is answered from frontmatter alone, never from reading procedure bodies.

### 8.4 Provenance (required, all kinds)

```yaml
author: kim                 # ∈ AuthorRegistry in the manifest
created: 2026-08-13
last_updated: 2026-08-13    # staleness input, not trivia
review_after: 180d          # optional per-artifact override of the default
```

`last_updated` is load-bearing: `harness_check` flags any artifact whose `last_updated` exceeds its review window as **stale** — a warning tier alongside the exemption burn-down, because stale files are drift's incubation stage. The field is validated against git history (declared date may not postdate the last commit touching the artifact), so it cannot be cosmetically bumped without an actual change.

### 8.5 What stays out

`version` (git is the version authority), `tags` (the grammar + description are the routing surface; a parallel folksonomy forks it), free-form `notes` (body content, not metadata). If a future field earns validation, it enters by manifest PR like a lexicon entry.

---

## 9. Two-level taxonomy — artifacts vs intra-skill resources

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

## 10. Migration posture — grandfathering

The live estate conforms at roughly 30%. The grammar is a target; without an explicit migration mechanism it is dead paper. Posture: **enforce for new names; grandfather existing ones.**

- `naming.manifest.json` carries an `exemptions` array listing every current non-conforming name verbatim.
- The validator passes any name in `exemptions` and enforces the full grammar on everything else.
- **The array may shrink and may never grow.** CI diffs the array; any addition fails the build.
- `harness_check` reports exemption count as a burn-down metric. Renames retire exemptions opportunistically (when an artifact is otherwise being touched), never as a big-bang campaign — renames are a known drift source because invocation strings live in prompts, hooks, and workflow configs.

Known exemption seeds (non-exhaustive): `handoff-to-human`, `handoff-to-agent`, `find-unused`, `team-weekly`, `team-daily`, `pylon-triage-weekly`, `linguistic-techniques`, `start-work`, `finish-work`, and all `adia-*`-prefixed local names.

---

## 11. Validator

String ops plus YAML reads, no NLP. Runs in CI and as a pre-mint gate in `/skill-create`.

Checks, in order:

1. Name ∈ `exemptions` → grammar checks skip (record for burn-down); frontmatter checks (4–7) still apply.
2. Parse per §5; all tokens resolve; no banned aliases; no brand tokens.
3. `folder == name` (§6); skill folder layout closed set, `SKILL.md` present, no nested skills (§6.1); reference index complete and dangling-free (§6.2).
4. Frontmatter schema (§8): required fields present; no fields outside the schema; decided kind (parse + directory) matches declared kind.
5. Relations (§7): every endpoint exists; `performs` equals name minus `-agent`; `wraps` targets a model-invocable skill; compiled `requires` graph is acyclic.
6. Invocation policy (§8.3): `mutates: true ⇒ confirm: required` (allowlist excepted); agents fail closed to `autonomous_write: false`; policy/capability coherence — tool grants match declared policy, `Bash` grants are scoped patterns.
7. Provenance (§8.4): `author` ∈ AuthorRegistry; `last_updated` does not postdate last git touch; staleness beyond review window → warning tier.
8. ObjectVocab registration gate (on manifest change): new entries create no parse ambiguity; disjointness of VerbLex/ProcessLex holds.

Grammar and relation failures block the mint/merge; staleness warns.

---

## 12. Worked examples

| Name | Location | Parse | Verdict |
|---|---|---|---|
| `skill-create` | `commands/` | object=`skill`, verb=`create` | ✓ command |
| `skills-audit` | `skills/` | object=`skills`, process=`audit` | ✓ skill |
| `naming-conventions` | `skills/` | nominal production; reference-shaped body | ✓ skill |
| `hcc-coding` | `skills/` | nominal production (tokens resolve) | ✓ skill |
| `skills-audit-agent` | `agents/` | strips `-agent` → extant skill `skills-audit` | ✓ agent (performs) |
| `team-leader-agent` | `agents/` | scope=`team`, role=`leader` ∈ RoleLex | ✓ agent (orchestrator) |
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
