---
doc-type: spec
id: spec-naming-convention
status: draft
version: 1.1.0
date: 2026-08-16
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
skill     := object "-" process                 skills-audit, ui-layout-planning
          |  nominal-phrase                     naming-conventions   (looser production)
agent     := skill-name "-" "agent"             skills-audit-agent   (primary)
          |  scope "-" role                     team-leader          (orchestrators — canonical, ADR-0015 D1)
          |  scope "-" role "-" "agent"         product-leader-agent (orchestrators — legacy spelling, ADR-0015 D1)
```

One reserved head: `-agent`. Mandatory on the primary agent production and on skills
(illegal there); optional on the orchestrator agent production only (§3.3, ADR-0015 D1).

#### 3.1 Commands — object-first

Commands are object-first (`skill-create`, not `create-skill`) so that slash autocomplete groups operations by object: `/skill-<tab>` surfaces `skill-create`, `skill-review`, `skill-lint` together. Discovery ergonomics outrank reading-as-English for a user-invoked surface.

The terminal token must be a member of `VerbLex`.

#### 3.2 Skills — nominal, process head preferred

The canonical skill production is `{object}-{process}` (`skills-audit`, `entry-file-authoring`). The terminal token should be a member of `ProcessLex`. Skills that are genuinely not object-process shaped — report generators, routers, and reference corpora — use the nominal-phrase production, but every token must still resolve in the lexicons (§4): the looseness is in the *shape*, never in the *vocabulary*.

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
    skills-audit/SKILL.md
    naming-conventions/SKILL.md      # reference-shaped: thin stub + references/
  agents/
    skills-audit-agent.md
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
```

Four top-level entries, nothing else. The partition axis is **how content participates when the skill runs**: `SKILL.md` is loaded into context; `references/` is selectively read into context; `scripts/` executes *outside* context — deterministic logic belongs in a script the skill calls, never in prose the model re-derives; `assets/` is neither read nor executed, only addressed by path. Every file answers one question — *context, computation, or payload?* — and the answer decides its folder.

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
| agent **performs** skill | the agent | `performs: skills-audit` | value == name minus `-agent`; skill exists |
| command **wraps** skill | the command | `wraps: naming-audit` | skill exists; skill is model-invocable |
| artifact **requires** skill | the consumer | `requires: [naming-conventions]` | each exists; compiled graph is acyclic |

`performs` is redundant with the string arithmetic by design — the redundancy is the check. A rename that touches one side and not the other fails loudly instead of drifting silently.

`requires` is the single dependency edge: "must exist and be available." Whether the dependent *invokes* the target's procedure or *consults* its references is visible in the dependent's body, where behavioral distinctions belong — a second edge type (`consults`) would encode in metadata what the body already states, and edge types that duplicate body content are the frontmatter equivalent of comments that restate code.

The **wrapper pattern** is how dual access works under the strict invoker partition: a model-invocable skill gains user access via a thin command (`/naming-audit` → `wraps: naming-audit`). Every artifact keeps exactly one invoker; dual access is composition, not a fourth kind.

Derived-graph audits (all mechanical): dangling endpoints (relation references a nonexistent artifact), orphaned agents (`performs` disagreement), and `requires` cycles.

---

### REQ-007 — 8. Frontmatter schema

Frontmatter is the **authoring surface** for everything the tooling reads. The rule that keeps it from rotting: **every field in this schema is validated; no field enters the schema unless something reads it.** Fields nothing validates are prohibited, not optional — ungoverned metadata is where frontmatter lies accumulate.

#### 8.1 Identity (required, all kinds)

```yaml
name: skills-audit          # canonical; == folder; parseable per §5
kind: skill                 # command | skill | agent
description: >              # the trigger contract — governed by
  Use when …                # skill-authoring-standards, not this spec
```

The validator asserts agreement, never trusts declaration: name parse + directory → **decided kind**; frontmatter must match. Disagreement is a lint failure. Frontmatter is an agreement check, never a tiebreaker — the specific defense against the rename-drift class (`entry-file-author` / `claude-md-author`) where a name silently stops meaning what the metadata claims.

#### 8.2 Relations (per §7, on the depending artifact)

```yaml
performs: skills-audit             # agents
wraps: naming-audit                # commands (dual-access)
requires: [naming-conventions]     # any kind — deps that must exist and be available
```

#### 8.3 Invocation policy and tool grants (required for agents and mutating commands)

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

#### 8.4 Provenance (required, all kinds)

```yaml
author: kim                 # ∈ AuthorRegistry in the manifest
created: 2026-08-13
last_updated: 2026-08-13    # staleness input, not trivia
review_after: 180d          # optional per-artifact override of the default
```

`last_updated` is load-bearing: `harness_check` flags any artifact whose `last_updated` exceeds its review window as **stale** — a warning tier alongside the exemption burn-down, because stale files are drift's incubation stage. The field is validated against git history (declared date may not postdate the last commit touching the artifact), so it cannot be cosmetically bumped without an actual change.

#### 8.5 What stays out

`version` (git is the version authority), `tags` (the grammar + description are the routing surface; a parallel folksonomy forks it), free-form `notes` (body content, not metadata). If a future field earns validation, it enters by manifest PR like a lexicon entry.

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

Known exemption seeds (non-exhaustive): `handoff-to-human`, `handoff-to-agent`, `find-unused`, `team-weekly`, `team-daily`, `pylon-triage-weekly`, `linguistic-techniques`, `start-work`, `finish-work`, and all `adia-*`-prefixed local names.

---

## Acceptance

### 11. Validator

String ops plus YAML reads, no NLP. Runs in CI and as a pre-mint gate in `/skill-create`.

Checks, in order:

1. **AC-001** (REQ-001) Name ∈ `exemptions` → grammar checks skip (record for burn-down); frontmatter checks (4–7) still apply.
2. **AC-002** (REQ-004) Parse per §5; all tokens resolve; no banned aliases; no brand tokens.
3. **AC-003** (REQ-005) `folder == name` (§6); skill folder layout closed set, `SKILL.md` present, no nested skills (§6.1); reference index complete and dangling-free (§6.2).
4. **AC-004** (REQ-007) Frontmatter schema (§8): required fields present; no fields outside the schema; decided kind (parse + directory) matches declared kind.
5. **AC-005** (REQ-006) Relations (§7): every endpoint exists; `performs` equals name minus `-agent`; `wraps` targets a model-invocable skill; compiled `requires` graph is acyclic.
6. **AC-006** (REQ-007) Invocation policy (§8.3): `mutates: true ⇒ confirm: required` (allowlist excepted); agents fail closed to `autonomous_write: false`; policy/capability coherence — tool grants match declared policy, `Bash` grants are scoped patterns.
7. **AC-007** (REQ-007) Provenance (§8.4): `author` ∈ AuthorRegistry; `last_updated` does not postdate last git touch; staleness beyond review window → warning tier.
8. **AC-008** (REQ-003) ObjectVocab registration gate (on manifest change): new entries create no parse ambiguity; disjointness of VerbLex/ProcessLex holds; disjointness of RoleLex against ObjectVocab ∪ ProcessLex holds (ADR-0015 D3).

Grammar and relation failures block the mint/merge; staleness warns.

---

## Examples

### 12. Worked examples

| Name | Location | Parse | Verdict |
|---|---|---|---|
| `skill-create` | `commands/` | object=`skill`, verb=`create` | ✓ command |
| `skills-audit` | `skills/` | object=`skills`, process=`audit` | ✓ skill |
| `naming-conventions` | `skills/` | nominal production; reference-shaped body | ✓ skill |
| `hcc-coding` | `skills/` | nominal production (tokens resolve) | ✓ skill |
| `skills-audit-agent` | `agents/` | strips `-agent` → extant skill `skills-audit` | ✓ agent (performs) |
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
