#!/usr/bin/env python3
"""authorkit validator — enforces the harness artifact naming convention.

Deterministic checks only: name grammar, folder layout, frontmatter schema,
relation graph, policy/capability coherence, provenance. Judgment (severity
interpretation, report narrative) belongs to the naming-audit skill, not here.

Usage:
  validate.py --target PATH [--manifest PATH] [--json] [--hook] [--scope full|grammar]
  validate.py hook                            PostToolUse entry point: reads the hook
                                               event off stdin and derives --target/
                                               --manifest itself from tool_input.file_path
                                               (issue #276) — never call with --target by
                                               hand; see resolve_hook_target below
  validate.py selftest                        prove the counters bite

Exit codes: 0 clean (warnings allowed), 1 errors found, 2 no manifest or no
args (--hook mode exits 0 on missing manifest: governance is opt-in per estate).
`hook` mode's own contract differs: exit 2 = grammar FINDINGS on the written
file's plugin (the PostToolUse blocking convention); everything unexpected —
malformed/wrong-shape event, no derivable root, unreadable manifest — exits 0
silently (fail open, hook-writing-rules).

Manifest resolution for a plugin-scoped `--target` (issue #842, 2026-08-21): probes
`<target>/naming.manifest.json`, then `<target>/.claude/naming.manifest.json`, then
falls back once to `<git toplevel of target>/naming.manifest.json` via
`find_repo_root` — so a workspace-root manifest governing a plugin one or more
levels below it is found without a directory walk (that walk was tried and
rejected for a different case; see `find_repo_root`'s docstring). `--manifest`
always overrides all three probes.

`hook` mode (issue #276, 2026-08-15): a write-time PostToolUse hook that hardcodes
`--target "$CLAUDE_PROJECT_DIR/$plugin"` for a fixed plugin roster is blind to
EnterWorktree sessions — `$CLAUDE_PROJECT_DIR` names the PRIMARY checkout for the whole
session's lifetime, never the worktree a campaign is required to write into (ADR-0002), so
the hook validated the wrong tree's (already-clean) files while the campaign's real writes
went unchecked until `release_gate.py` G12 caught them a whole tier later. `hook` mode fixes
this at the root: it derives its target from the tool payload actually written
(`tool_input.file_path`, on the hook's own stdin per the platform's documented event
contract) via `resolve_hook_target`/`find_repo_root` — ask git for `--show-toplevel` of the
checkout containing the written file; that IS the repo root the write landed in, primary
checkout or worktree alike, because every EnterWorktree checkout is its own git worktree
with its own top-level. (A directory walk for a `naming.manifest.json` marker file was
tried first and rejected: `authorkit` carries its own nested manifest copy for
self-dogfooding, which makes a walk-up-to-nearest-manifest stop at the wrong ancestor for
any write inside authorkit, worktree or not — see `find_repo_root`'s own docstring.) No env
var, no worktree-marker string match, no hardcoded plugin list — which also naturally
narrows validation to the ONE plugin the triggering write actually touched, instead of
unconditionally re-checking all N plugins on every write.

--scope (2026-08-14, issue #197 wiring): this validator checks two genuinely different
things under one name — naming GRAMMAR (name production, lexicon disjointness, the
reserved -agent head; what ADR-0011 D8's grandfather+ratchet exemptions actually cover)
and a broader STRUCTURAL schema (author/created/last_updated provenance, kind-declared
policy grants, reference-index completeness). Measured empirically wiring this into
nonoun-plugins (2026-08-14): running --scope full (the default, authorkit's own
dogfooding contract) against an estate that never adopted the structural schema fails on
hundreds of structural findings that have nothing to do with naming — a false blocking
gate for anyone ADR-0011 never asked to backfill author/created/last_updated across an
existing estate. --scope grammar restricts the exit-code/gating decision to
`grammar_errors` only; structural findings still print (and appear in `--json` output
under `structural_errors`) so nothing goes silently unmeasured, they just do not fail
the run. Every finding is tagged in `--json` output; `grammar_errors`/`structural_errors`
partition `errors` exhaustively.

schema_scope (2026-08-14, issue #226, executing #224's ruling b): the four provenance
fields (kind/author/created/last_updated) are authorkit-internal convention, not estate
law — nothing outside authorkit reads them, so counting them as findings across an estate
that never adopted the schema is unmade-adoption noise (2,115 findings estate-wide, all
outside authorkit). Rather than every caller passing --scope by hand, the ESTATE's own
naming.manifest.json now carries an optional `schema_scope: "grammar" | "full"` field —
the manifest declares its own tier, in ONE file, never a hardcoded per-caller plugin list
(the stale-list defect class that recurred 3x: gate.yml, marketplace.json, the hook loop).
Precedence: an explicit --scope flag always wins (the PostToolUse hook's own case, and
release_gate's G12, both keep calling it exactly as before); with no --scope, the
manifest's schema_scope picks the default (absent field -> "full", so an existing
manifest/consumer with no opinion behaves unchanged). Independent of scope: when the
effective scope is "grammar", the structural channel is computed only for artifacts
INSIDE this validator's own plugin tree (authorkit dogfoods "full" on itself regardless
of the estate's declared tier — its own ~13 structural findings stay visible); artifacts
OUTSIDE that tree have their structural findings dropped entirely, not merely
non-gated — this is what actually collapses the estate-wide count, not just the gate
decision --scope already made non-blocking.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(text):
    """Minimal YAML-subset parser: scalars, inline lists, block lists,
    folded scalars. No external dependency by design."""
    if not text.startswith("---"):
        return {}, "missing frontmatter block"
    lines = text.split("\n")
    end = None
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip() == "---":
            end = i
            break
    if end is None:
        return {}, "unterminated frontmatter block"
    fm, key = {}, None
    i = 1
    while i < end:
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if raw.startswith((" ", "\t")):
            if key is None:
                return {}, f"indented line without key: {stripped!r}"
            if stripped.startswith("- "):
                if not isinstance(fm[key], list):
                    fm[key] = []
                fm[key].append(_scalar(stripped[2:]))
            else:  # folded/continued scalar
                fm[key] = (str(fm[key]) + " " + stripped).strip()
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
        if not m:
            return {}, f"unparseable frontmatter line: {stripped!r}"
        key, val = m.group(1), m.group(2).strip()
        if val in (">", ">-", "|", "|-"):
            fm[key] = ""
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            fm[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        elif val == "":
            fm[key] = []  # block list or empty; block items fill it
        else:
            fm[key] = _scalar(val)
        i += 1
    return fm, None


def _scalar(v):
    v = v.strip().strip("'\"").split("  #")[0].strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v

# -------------------------------------------------------------------- grammar

# Every top-level field MANIFEST-TEMPLATE.json declares as a list — swept from that
# template's own schema (issue #296) rather than hand-picked, so a field the template adds
# tomorrow is caught by re-reading the template, not by remembering to update this set by
# hand. `schema_scope` is the one top-level field that is NOT list-shaped (a string) and
# already carries its own back-compat fallback in main(); it is deliberately excluded here.
TOP_LEVEL_LIST_FIELDS = (
    "verb_lex", "process_lex", "role_lex", "object_vocab", "brand_tokens",
    "author_registry", "mutating_no_confirm_allowlist", "exemptions", "topic_lex",
)


def _typed_list(manifest, field, errors):
    """Return manifest[field] if present and list-shaped; otherwise record a named,
    actionable manifest_errors finding and return [] — never let a wrong-type top-level
    field crash downstream (`set(...)`/`for entry in ...`) with a raw, uncaught TypeError
    (issue #296, generalizing #252's author_registry-only shape guard to every top-level
    list field). A field missing entirely is not an error — every field here is optional
    per MANIFEST-TEMPLATE.json and defaults to empty."""
    if field not in manifest:
        return []
    val = manifest[field]
    if not isinstance(val, list):
        errors.append(
            f"manifest field {field!r} must be a list, got "
            f"{type(val).__name__}: {val!r} (see MANIFEST-TEMPLATE.json)"
        )
        return []
    return val


# ADR-0020 D3 (2026-08-17, issue #520): `bind-`/`fork-`/`sub-` replace the general-purpose
# `lead-` production as the estate's reserved, mechanism-revealing command/skill heads —
# `bind-` (seat adoption, no spawn), `fork-` (context: fork), `sub-` (Agent dispatch). `lead-`
# is retired as an OPEN production (no new `lead-{scope}` mint conforms). Wave 5 (#523) renamed
# every live `/lead-*` surface to `bind-{scope}` (the six: `lead-team`, `lead-build`,
# `lead-planning`, `lead-product`, `lead-review`, `lead-intake`), so the `LEAD_HEAD_GRANDFATHER`
# closed set this comment used to describe — and the `lead` branches that consulted it — are
# deleted outright, not merely emptied (removed 2026-08-17, #523): nothing needs grandfathering
# anymore, and re-adding a `lead-{scope}` mint should fail grammar like any other retired head.
#
# The three ADR-0020 D3 heads — residue resolves against the same orchestrator-scope pool
# `lead-` always used (ADR-0015 D2: ObjectVocab ∪ ProcessLex), since each names a different
# platform mechanic for adopting the identical seat-scope vocabulary.
RESERVED_BIND_FORK_SUB_HEADS = ("bind", "fork", "sub")


class Grammar:
    def __init__(self, manifest):
        self.manifest_errors = []
        self.verb_lex = set(_typed_list(manifest, "verb_lex", self.manifest_errors))
        self.process_lex = set(_typed_list(manifest, "process_lex", self.manifest_errors))
        self.role_lex = set(_typed_list(manifest, "role_lex", self.manifest_errors))
        # TopicLex (spec-naming-convention.md §14.2, ADR-0014 D3): closed lexicon of
        # `-rules` reference-doc topic words (`icon`, `motion`, …), structurally identical
        # to RoleLex — consulted ONLY inside D1's union-pool resolution below, never
        # disjointness-checked against ObjectVocab/ProcessLex (D3: no ambiguity possible in
        # that context, only harmless redundancy).
        self.topic_lex = set(_typed_list(manifest, "topic_lex", self.manifest_errors))
        self.exemptions = set(_typed_list(manifest, "exemptions", self.manifest_errors))
        # author_registry must be a flat list of plain strings (MANIFEST-TEMPLATE.json's
        # own contract). A structured entry (e.g. {"name": ..., "emails": [...]}) is not
        # hashable and used to raise a raw, uncaught `TypeError: unhashable type: 'dict'`
        # straight out of this constructor (issue #252) — found live by overhaul-execute's
        # first real dogfood run, traced to manifest-authoring's own seeding step never
        # stating the expected shape. Fail clean instead: skip the malformed entry (it
        # cannot match any artifact's `author` field either way) and surface a named,
        # actionable manifest_errors finding instead of a stack trace. Silently coercing a
        # dict to some extracted key was considered and rejected — a structured entry
        # (name + emails) has no single field that is obviously "the" author string, and
        # guessing one would mask the real fix (correcting the manifest) behind output that
        # looks like it worked.
        self.authors = set()
        for entry in _typed_list(manifest, "author_registry", self.manifest_errors):
            if isinstance(entry, str):
                self.authors.add(entry)
            else:
                self.manifest_errors.append(
                    f"author_registry entry must be a plain string, got "
                    f"{type(entry).__name__}: {entry!r} — expected a flat list of "
                    f"strings, e.g. [\"kim\", \"jane\"] (see MANIFEST-TEMPLATE.json)"
                )
        self.brand_tokens = set(_typed_list(manifest, "brand_tokens", self.manifest_errors))
        self.mutation_allowlist = set(
            _typed_list(manifest, "mutating_no_confirm_allowlist", self.manifest_errors)
        )
        self.objects = {}       # any acceptable surface form -> canonical
        self.banned = {}        # banned alias -> canonical
        seen_canonicals = set()
        for entry in _typed_list(manifest, "object_vocab", self.manifest_errors):
            # Mirror of #252's author_registry guard, in the OTHER direction: object_vocab
            # expects a STRUCTURED {"canonical": ...} entry per MANIFEST-TEMPLATE.json; a
            # plain STRING entry (e.g. mistakenly mimicking author_registry's own flat-list
            # shape) used to raise a raw, uncaught `TypeError: string indices must be
            # integers` out of `entry["canonical"]` below (issue #296).
            if not isinstance(entry, dict):
                self.manifest_errors.append(
                    f"object_vocab entry must be a structured object with a 'canonical' "
                    f"key, got {type(entry).__name__}: {entry!r} — expected "
                    f"{{\"canonical\": ..., \"plural\": ..., \"banned_aliases\": [...]}} "
                    f"(see MANIFEST-TEMPLATE.json)"
                )
                continue
            # Required key missing — used to raise a raw, uncaught `KeyError: 'canonical'`
            # out of the same line (issue #296).
            if "canonical" not in entry:
                self.manifest_errors.append(
                    f"object_vocab entry missing required key 'canonical': {entry!r} "
                    f"(see MANIFEST-TEMPLATE.json)"
                )
                continue
            canon = entry["canonical"]
            # Duplicate registration — pinned semantics (issue #296): the LAST entry for a
            # given `canonical` wins (its plural/banned_aliases silently override the
            # earlier entry's), matching this dict's own natural last-write-wins
            # assignment below. That resolution is never left UNSIGNALED, though — a
            # duplicate always surfaces as a named manifest_errors finding so the manifest
            # is not considered clean until the redundant entry is resolved by hand.
            if canon in seen_canonicals:
                self.manifest_errors.append(
                    f"duplicate object_vocab registration: canonical={canon!r} registered "
                    f"more than once — the LAST registration wins, silently overriding the "
                    f"earlier entry's plural/banned_aliases (pinned semantics, issue #296); "
                    f"de-duplicate in the manifest to clear this finding"
                )
            seen_canonicals.add(canon)
            self.objects[canon] = canon
            if entry.get("plural"):
                self.objects[entry["plural"]] = canon
            for alias in entry.get("banned_aliases", []):
                self.banned[alias] = canon
        # D1's union pool (ADR-0014): ObjectVocab ∪ single-token ProcessLex members ∪
        # TopicLex — built once here, never re-derived per parse. ProcessLex/TopicLex
        # entries are added only where absent so an ObjectVocab canonical form (which may
        # carry its own plural mapping) is never shadowed by a same-spelled Process/Topic
        # entry (issue matters only in a name clash, which registration hygiene should
        # flag, never something this merge should silently prefer one way).
        self.objects_union = dict(self.objects)
        for tok in self.process_lex:
            self.objects_union.setdefault(tok, tok)
        for tok in self.topic_lex:
            self.objects_union.setdefault(tok, tok)
        overlap = self.verb_lex & self.process_lex
        self.lexicon_errors = (
            [f"VerbLex/ProcessLex disjointness violated: {sorted(overlap)}"]
            if overlap else []
        )
        # ADR-0015 D2's orchestrator scope pool: ObjectVocab (every canonical + plural
        # key of self.objects) union ProcessLex — deliberately NOT ADR-0014 D1's
        # three-way union (self.objects_union also folds in TopicLex): a seat
        # coordinates a thing or a process, never a reference-doc topic word, so
        # TopicLex stays out of this pool (ADR-0015 D2, distinguishing itself from the
        # `-rules` production's pool on purpose).
        self.orchestrator_scope_pool = dict(self.objects)
        for tok in self.process_lex:
            self.orchestrator_scope_pool.setdefault(tok, tok)
        # ADR-0015 D3: RoleLex must be disjoint from ObjectVocab ∪ ProcessLex — once a
        # bare {scope}-{role} name is a legal agent shape, a role word double-booked as
        # an object/process would let the same string parse as a skill AND an agent.
        role_overlap = self.role_lex & (set(self.objects) | self.process_lex)
        if role_overlap:
            self.lexicon_errors.append(
                f"RoleLex/ObjectVocab∪ProcessLex disjointness violated: {sorted(role_overlap)}"
            )

    def _resolve(self, tokens, pool):
        """Greedy left-anchored longest-match of hyphen tokens against `pool`.
        Returns (ok, unresolved_token_or_None). Shared by resolve_objects (ObjectVocab
        alone) and resolve_objects_union (D1's union pool) — same algorithm, different
        lexicon set, per ADR-0014 D1's own framing ("no change to the matching algorithm
        itself, only to which lexicon set it's built from")."""
        i = 0
        while i < len(tokens):
            matched = False
            for j in range(len(tokens), i, -1):  # longest first
                cand = "-".join(tokens[i:j])
                if cand in self.banned:
                    return False, f"banned alias {cand!r} (use {self.banned[cand]!r})"
                if cand in pool:
                    i, matched = j, True
                    break
            if not matched:
                return False, f"token {tokens[i]!r} resolves in no lexicon or vocab"
        return True, None

    def resolve_objects(self, tokens):
        """Greedy left-anchored longest-match of hyphen tokens against
        ObjectVocab. Returns (ok, unresolved_token_or_None)."""
        return self._resolve(tokens, self.objects)

    def resolve_objects_union(self, tokens):
        """Same algorithm as resolve_objects, resolved against D1's union pool
        (ObjectVocab ∪ ProcessLex ∪ TopicLex) — the `-rules` reserved-tail production's
        own resolution pool (ADR-0014 D1)."""
        return self._resolve(tokens, self.objects_union)

    def resolve_orchestrator_scope(self, tokens):
        """Same algorithm, resolved against ADR-0015 D2's pool (ObjectVocab ∪
        ProcessLex, no TopicLex) — the orchestrator agent production's own scope
        resolution, shared by both the bare and legacy `-agent`-tailed spellings."""
        return self._resolve(tokens, self.orchestrator_scope_pool)

    def check_brand(self, tokens):
        hits = [t for t in tokens if t in self.brand_tokens]
        return f"brand token(s) in local name: {hits}" if hits else None

    def parse(self, kind, name, skills, wraps_target=None, commands=None, user_invocable=False):
        """Returns list of grammar errors for this name."""
        errs = []
        tokens = name.split("-")
        brand = self.check_brand(tokens)
        if brand:
            errs.append(brand)

        if kind == "agent":
            # ADR-0015 D1: the orchestrator production no longer requires the -agent
            # tail. `-agent` remains the estate's one reserved head for the PRIMARY
            # production (skill-name + "-agent"), and remains a legal — legacy —
            # spelling on the orchestrator production; both spellings are tried below.
            legacy = name.endswith("-agent")
            residue = name[: -len("-agent")] if legacy else name
            if legacy and residue in skills:
                return errs  # primary production: agent-of-skill (unchanged)
            # vocab-stem production (2026-08-31, adiahealth/adia-harness): the residue may
            # instead resolve wholly against ObjectVocab — a domain-scoped generalist agent
            # (`sdlc-agent`, `build-agent`) whose stem names a registered domain token rather
            # than one skill. Resolved against ObjectVocab ONLY (not ProcessLex/TopicLex), so
            # a process word like `review` still needs the skill-stem or scope-role form —
            # keeping the production narrow enough that an unregistered coinage still fails.
            if legacy and self._resolve(residue.split("-"), self.objects)[0]:
                return errs
            rtoks = residue.split("-")
            if len(rtoks) >= 2 and rtoks[-1] in self.role_lex:
                ok, why = self.resolve_orchestrator_scope(rtoks[:-1])
                return errs if ok else errs + [f"orchestrator scope: {why}"]
            if legacy:
                return errs + [
                    f"strip -agent -> {residue!r} is no extant skill, no ObjectVocab "
                    f"term(s), and no scope-role production (RoleLex: {sorted(self.role_lex)})"
                ]
            return errs + [
                f"agent name {name!r} is no bare scope-role orchestrator name "
                f"(RoleLex: {sorted(self.role_lex)}) and does not end in -agent"
            ]

        if kind == "command":
            # wrapper production: command name identical to its wrapped skill
            if wraps_target and name == wraps_target and name in skills:
                return errs
            # ADR-0020 D3 (2026-08-17, #520) — `bind-`/`fork-`/`sub-` reserved verb-first
            # heads replace `lead-`: `{head}-{scope}` conforms when the scope resolves
            # against the orchestrator scope pool (ADR-0015 D2's ObjectVocab ∪ ProcessLex —
            # the command makes the session adopt the orchestrator seat whose scope that
            # is; the head names which platform mechanic does the adopting). Each head is
            # a literal, exactly like ADR-0014's `check-`: not a VerbLex member, never a
            # template for other verbs.
            if tokens[0] in RESERVED_BIND_FORK_SUB_HEADS and len(tokens) >= 2:
                ok, why = self.resolve_orchestrator_scope(tokens[1:])
                return errs if ok else errs + [f"command scope ({tokens[0]}- head): {why}"]
            if len(tokens) < 2:
                return errs + ["command needs object-verb shape (>= 2 tokens)"]
            verb = tokens[-1]
            if verb not in self.verb_lex:
                return errs + [
                    f"command terminal {verb!r} not in VerbLex "
                    f"{sorted(self.verb_lex)} (and name is not a wrapper "
                    f"identical to its wrapped skill)"
                ]
            ok, why = self.resolve_objects(tokens[:-1])
            return errs if ok else errs + [f"command object: {why}"]

        if kind == "skill":
            # ADR-0020 D3/D4 (2026-08-17, #520/#523) — `bind-`/`fork-`/`sub-` reserved
            # heads MUST run before the unconditional `-agent` reserved-tail check just
            # below: D4 mandates `/fork-agent {agent-name}` and `/sub-agent {agent-name}`
            # by name, and their residue is the literal word `agent` (which resolves
            # cleanly in ObjectVocab) — a genuinely new instance of the dead-code hazard
            # `make-agent` intentionally hits (that one stays correctly rejected; this one
            # must not, since ADR-0020 names these two exact surfaces as the mint). Placed
            # here, ahead of every other skill-branch check, for the same reason.
            if tokens[0] in RESERVED_BIND_FORK_SUB_HEADS and len(tokens) >= 2:
                ok, why = self.resolve_orchestrator_scope(tokens[1:])
                return errs if ok else errs + [f"skill scope ({tokens[0]}- head): {why}"]
            if tokens[-1] == "agent":
                return errs + ["reserved head -agent on a skill"]
            # D1 — `-rules` reserved TAIL (spec §14.2, ADR-0014): must sit BEFORE the
            # object-process check below, since `rules` already sits in ProcessLex and
            # that check hard-returns on any match — a branch placed after it would be
            # unreachable dead code for this entire class (ADR-0014 Context, "Root cause").
            if tokens[-1] == "rules" and len(tokens) >= 2:
                ok, why = self.resolve_objects_union(tokens[:-1])
                return errs if ok else errs + [f"skill topic (rules tail): {why}"]
            # D2 — `check-` reserved HEAD (spec §14.2, ADR-0014): same dead-code hazard as
            # D1 — must also sit before the object-process check (critical for
            # `check-stage`, whose terminal token `stage` sits in ProcessLex).
            if tokens[0] == "check" and len(tokens) >= 2:
                ok, why = self.resolve_objects(tokens[1:])
                return errs if ok else errs + [f"skill object (check- head): {why}"]
            # (bind-/fork-/sub- checked at the very top of this kind branch, ahead of the
            # -agent tail check — see the comment there for why.)
            # ADR-0018 D1 — `make-` and `file-` reserved HEADS (spec §14.7, mechanism per §14.2, same
            # mechanism as ADR-0014's check- head): literal head token, residue
            # resolves against ObjectVocab ONLY (never the process/union pools) —
            # the estate's canonical forge (`make-`) and intake (`file-`) verb
            # families. Must sit BEFORE the object-process check below for the same
            # dead-code-hazard reason as check-/lead-: `make-doc`'s residue `doc`
            # and `file-task`'s residue `task` are plain ObjectVocab members, but a
            # branch placed after the process check could still shadow a future
            # residue landing in ProcessLex. The literal head set stays closed at
            # {check, make, file} — not a template for other VerbLex members
            # (ADR-0014 Alt C stays rejected). Runs AFTER the -agent tail check
            # above (line ~391), which is what keeps `make-agent` permanently
            # failing: the tail strips first, unconditionally, before any head
            # branch is reached.
            if tokens[0] in ("make", "file") and len(tokens) >= 2:
                ok, why = self.resolve_objects(tokens[1:])
                return errs if ok else errs + [f"skill object ({tokens[0]}- head): {why}"]
            if len(tokens) >= 2 and tokens[-1] in self.process_lex:
                ok, why = self.resolve_objects(tokens[:-1])
                return errs if ok else errs + [f"skill object: {why}"]
            # Reverse-wrapper amendment (spec-naming-convention.md §14.1, issue #241,
            # extended §14.9, issue #525): an object-verb skill name is legal IFF EITHER an
            # identically-named command exists in the same plugin root (the command wraps
            # it — §14.1's original realization) OR the skill itself carries
            # `user-invocable: true` with no sibling command at all (§14.9's skill-as-command
            # realization, ratified 2026-08-17: the successor dual-access shape retires the
            # wrapper command, so its ABSENCE is no longer evidence against the object-verb
            # name it used to license — the skill's own `user-invocable: true` is the same
            # "one procedure, two surfaces" fact, just carried on one file instead of two).
            # Never on the skill's say-so alone either way — object resolution below still
            # applies in both branches.
            if len(tokens) >= 2 and tokens[-1] in self.verb_lex and (
                name in (commands or ()) or user_invocable
            ):
                ok, why = self.resolve_objects(tokens[:-1])
                return errs if ok else errs + [f"skill object (reverse-wrapper): {why}"]
            ok, why = self.resolve_objects(tokens)  # nominal production
            if ok:
                return errs
            return errs + [
                f"neither object-process (terminal not in ProcessLex "
                f"{sorted(self.process_lex)}) nor nominal ({why})"
            ]
        return errs + [f"unknown kind {kind!r}"]

# ------------------------------------------------------------ schema & policy

COMMON_REQUIRED = ["name", "kind", "description", "author", "created", "last_updated"]
COMMON_OPTIONAL = ["review_after"]
FIELDS = {
    "skill":   {"required": COMMON_REQUIRED,
                "optional": COMMON_OPTIONAL + ["requires", "allowed-tools",
                                                "disable-model-invocation", "user-invocable"]},
    "command": {"required": COMMON_REQUIRED,
                "optional": COMMON_OPTIONAL + ["requires", "wraps", "mutates",
                                                "confirm", "allowed-tools",
                                                "argument-hint"]},
    "agent":   {"required": COMMON_REQUIRED + ["performs", "autonomous_write",
                                                "context", "tools"],
                "optional": COMMON_OPTIONAL + ["requires", "model"]},
}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}


def tool_list(fm):
    raw = fm.get("allowed-tools", fm.get("tools", []))
    if isinstance(raw, str):
        raw = [t.strip() for t in raw.split(",")]
    return [t for t in raw if t]


def grant_tool_name(t):
    """Strip a grant's parenthesized scope to its bare tool name — e.g.
    'Edit(**/naming.manifest.json)' -> 'Edit'. A bare grant ('Edit') passes
    through unchanged. Without this, a SCOPED write grant reads as
    write-less to the policy/grant-coherence check below (#237, found
    during #235/PR #236): WRITE_TOOLS intersected the raw grant strings
    exactly, so 'Edit(...)' never matched 'Edit'."""
    m = re.match(r"^([A-Za-z][A-Za-z0-9_]*)\(", t)
    return m.group(1) if m else t


def policy_checks(kind, fm, name):
    errs, warns = [], []
    tools = tool_list(fm)
    granted = {grant_tool_name(t) for t in tools}
    unscoped_bash = any(t == "Bash" for t in tools)
    writey = bool(WRITE_TOOLS & granted) or unscoped_bash
    for t in tools:
        if t == "Bash":
            errs.append("unscoped Bash grant — scope it: Bash(pattern)")
    if kind == "agent":
        aw = fm.get("autonomous_write", False)  # fail closed
        if not isinstance(aw, bool):
            errs.append("autonomous_write must be boolean")
            aw = False
        if not aw and writey:
            errs.append("autonomous_write: false but write-capable tools granted")
        if fm.get("context") not in ("isolated", "inherited"):
            errs.append("context must be isolated|inherited")
    if kind == "command":
        mutates = fm.get("mutates", False)
        confirm = fm.get("confirm", "none")
        if mutates and confirm != "required" and name not in _grammar.mutation_allowlist:
            errs.append("mutates: true requires confirm: required (or allowlist entry)")
        if mutates and not writey:
            errs.append("mutates: true but no write-capable tool granted")
        if not mutates and writey:
            errs.append("mutates: false but write-capable tools granted")
    return errs, warns


def provenance_checks(fm, grammar):
    errs, warns = [], []
    if fm.get("author") not in grammar.authors:
        errs.append(f"author {fm.get('author')!r} not in AuthorRegistry")
    d = {}
    for f in ("created", "last_updated"):
        try:
            d[f] = date.fromisoformat(str(fm.get(f, "")))
        except ValueError:
            errs.append(f"{f} is not an ISO date: {fm.get(f)!r}")
    if len(d) == 2 and d["last_updated"] < d["created"]:
        errs.append("last_updated predates created")
    if "last_updated" in d:
        window = int(str(fm.get("review_after", "180d")).rstrip("d") or 180)
        if (date.today() - d["last_updated"]).days > window:
            warns.append(f"stale: last_updated exceeds {window}d review window")
    return errs, warns

# ----------------------------------------------------------- layout & indexes

ALLOWED_SKILL_ENTRIES = {"SKILL.md", "references", "scripts", "assets", "evals", "intent.md"}


def layout_checks(skill_dir):
    errs = []
    entries = [p.name for p in skill_dir.iterdir()]
    if "SKILL.md" not in entries:
        errs.append("SKILL.md missing")
    for e in entries:
        if e not in ALLOWED_SKILL_ENTRIES:
            errs.append(f"top-level entry outside closed set: {e!r}")
    for sub in skill_dir.rglob("SKILL.md"):
        if sub.parent != skill_dir:
            errs.append(f"nested skill at {sub.relative_to(skill_dir)}")
    return errs


def index_checks(skill_dir, body):
    """Every references/ file appears in the SKILL.md reference index; every
    index row points at an extant file."""
    errs = []
    refdir = skill_dir / "references"
    files = {p.name for p in refdir.iterdir() if p.is_file()} if refdir.is_dir() else set()
    rows = set()
    in_refs = False
    for ln in body.split("\n"):
        if re.match(r"^##\s+References\b", ln):
            in_refs = True
            continue
        if in_refs and ln.startswith("## "):
            in_refs = False
        if in_refs:
            m = re.match(r"^\|\s*`?([^|`]+?)`?\s*\|", ln)
            if m and m.group(1).strip().lower() not in ("file", "---", ":---"):
                cell = m.group(1).strip()
                if not set(cell) <= {"-", ":", " "}:
                    rows.add(cell)
    if files and not rows:
        errs.append("references/ populated but SKILL.md has no '## References' index")
    for f in files - rows:
        errs.append(f"references/{f} missing from reference index")
    for r in rows - files:
        errs.append(f"index row {r!r} points at no file in references/")
    return errs

# --------------------------------------------------------------------- runner

_grammar = None

# This validator's own plugin root (.../authorkit), derived from its own file
# location — never a hardcoded plugin-name string, so it never joins the
# stale-list defect class a maintained roster would. Used only to decide
# whether an artifact is "authorkit's own tree" for schema_scope's own-tree
# carve-out (module docstring, schema_scope section). run() accepts an
# own_root override so selftest can simulate the carve-out without depending
# on this real checkout's own content.
_OWN_PLUGIN_ROOT = Path(__file__).resolve().parents[3]


def discover(target: Path):
    """Yield (kind, name, path, is_dir_artifact). Supports a plugin root or a
    repo with .claude/."""
    root = target / ".claude" if (target / ".claude").is_dir() else target
    for kind, sub in (("command", "commands"), ("agent", "agents")):
        d = root / sub
        if d.is_dir():
            for p in sorted(d.glob("*.md")):
                yield kind, p.stem, p, False
    sd = root / "skills"
    if sd.is_dir():
        for p in sorted(sd.iterdir()):
            if p.is_dir():
                yield "skill", p.name, p, True


def run(target: Path, manifest: dict, scope: str = "full", own_root: Path = None) -> dict:
    """Core check logic over an already-resolved target and already-loaded
    manifest dict. Pure of argv/exit-code concerns so it is directly callable
    from both main() and selftest().

    scope: "full" counts every finding; "grammar" additionally drops (not
    merely non-gates) structural findings for artifacts outside own_root —
    the schema_scope carve-out (module docstring). own_root defaults to this
    validator's own plugin root; selftest overrides it to simulate the
    carve-out on a tempdir fixture."""
    global _grammar
    _grammar = g = Grammar(manifest)
    if own_root is None:
        own_root = _OWN_PLUGIN_ROOT

    def _is_own(path: Path) -> bool:
        try:
            path.resolve().relative_to(own_root.resolve())
            return True
        except ValueError:
            return False

    artifacts = list(discover(target))
    skills = {n for k, n, _, _ in artifacts if k == "skill"}
    commands = {n for k, n, _, _ in artifacts if k == "command"}
    findings = []          # (name, level, message, category) — category ∈ {grammar, structural}
    fms = {}               # name -> (kind, fm)
    paths = {}             # name -> Path, for the relation/acyclicity passes below

    for msg in g.lexicon_errors:
        findings.append(("manifest", "error", msg, "grammar"))
    for msg in g.manifest_errors:
        findings.append(("manifest", "error", msg, "structural"))

    for kind, name, path, is_dir in artifacts:
        paths[name] = path
        skip_structural = scope == "grammar" and not _is_own(path)
        md = path / "SKILL.md" if is_dir else path
        text = md.read_text() if md.is_file() else ""
        fm, fmerr = parse_frontmatter(text)
        body = text.split("---", 2)[2] if text.count("---") >= 2 else ""
        fms[name] = (kind, fm)
        exempt = name in g.exemptions

        def E(m, cat="structural"):
            if cat == "structural" and skip_structural:
                return
            findings.append((name, "error", m, cat))
        def W(m, cat="structural"):
            if cat == "structural" and skip_structural:
                return
            findings.append((name, "warn", m, cat))
        def X(m, cat="structural"): findings.append((name, "exempt-note", m, cat))

        # 1–2: grammar (exemptions skip; recorded for burn-down)
        errs = g.parse(kind, name, skills, wraps_target=fm.get("wraps"), commands=commands,
                        user_invocable=bool(fm.get("user-invocable", False)))
        for e in errs:
            (X if exempt else E)(e, "grammar")

        # 3: folder/file == name; layout; index (structural — redundant with skill_lint
        # F9/A6, which police this at write time; kept here as a second stack per D9)
        declared = fm.get("name")
        if declared != name:
            E(f"frontmatter name {declared!r} != {'folder' if is_dir else 'file'} name")
        if is_dir:
            for e in layout_checks(path):
                E(e)
            for e in index_checks(path, body):
                E(e)

        # 4: frontmatter schema (structural — provenance/schema, not naming grammar)
        if fmerr:
            E(fmerr)
            continue
        spec = FIELDS[kind]
        for f in spec["required"]:
            if f not in fm:
                E(f"required field missing: {f}")
        allowed = set(spec["required"]) | set(spec["optional"])
        for f in fm:
            if f not in allowed:
                E(f"field outside schema for kind={kind}: {f}")
        if fm.get("kind") != kind:
            E(f"declared kind {fm.get('kind')!r} != decided kind {kind!r} (directory)")

        # 6: policy & grants (structural)
        pe, pw = policy_checks(kind, fm, name)
        for e in pe:
            E(e)
        for w in pw:
            W(w)

        # 7: provenance (structural)
        ve, vw = provenance_checks(fm, g)
        for e in ve:
            E(e)
        for w in vw:
            W(w)

    # 5: relation graph (structural — a real relation check, but a different concern than
    # the name-production grammar above; not what D8's exemptions grandfather)
    names = set(fms)
    for name, (kind, fm) in fms.items():
        skip_structural = scope == "grammar" and not _is_own(paths[name])
        def E(m):
            if skip_structural:
                return
            findings.append((name, "error", m, "structural"))
        if kind == "agent":
            perf = fm.get("performs")
            if perf and name.endswith("-agent") and perf != name[:-6]:
                E(f"performs {perf!r} != name minus -agent")
            if perf and perf not in skills:
                E(f"performs target {perf!r} is no extant skill")
        if kind == "command":
            w = fm.get("wraps")
            if w and w not in skills:
                E(f"wraps target {w!r} is no extant skill")
        reqs = fm.get("requires", [])
        if isinstance(reqs, str):
            reqs = [reqs]
        for r in reqs:
            if r not in names:
                E(f"requires target {r!r} does not exist")
    # acyclicity over requires
    edges = {}
    for name, (_, fm) in fms.items():
        reqs = fm.get("requires", [])
        edges[name] = [reqs] if isinstance(reqs, str) else list(reqs)
    state = {}
    def dfs(n, trail):
        state[n] = 1
        for m in edges.get(n, []):
            if state.get(m) == 1:
                if not (scope == "grammar" and n in paths and not _is_own(paths[n])):
                    findings.append((n, "error", f"requires cycle: {' -> '.join(trail + [m])}", "structural"))
            elif state.get(m, 0) == 0 and m in edges:
                dfs(m, trail + [m])
        state[n] = 2
    for n in edges:
        if state.get(n, 0) == 0:
            dfs(n, [n])

    errors = [f for f in findings if f[1] == "error"]
    warns = [f for f in findings if f[1] == "warn"]
    exemption_notes = [f for f in findings if f[1] == "exempt-note"]
    grammar_errors = [f for f in errors if f[3] == "grammar"]
    structural_errors = [f for f in errors if f[3] == "structural"]

    return {
        "artifacts": len(artifacts), "findings": findings,
        "errors": errors, "warnings": warns,
        "grammar_errors": grammar_errors, "structural_errors": structural_errors,
        "exemption_burndown": {"count": len(g.exemptions), "notes": exemption_notes},
    }


def find_repo_root(path: Path):
    """git's own top-level for the checkout containing `path` — correct for a worktree
    BY CONSTRUCTION (every EnterWorktree checkout is its own git worktree with its own
    top-level; asking git is unambiguous, never a heuristic).

    A directory walk for a `naming.manifest.json` marker file was tried first and
    REJECTED: this very estate's `authorkit` plugin carries its own nested copy of
    `naming.manifest.json` for self-dogfooding (its own README: "validates clean against
    its own validator"), so a walk-up-to-nearest-manifest stops at `authorkit/` instead
    of the true workspace root for ANY write inside authorkit — in the primary checkout,
    not just a worktree — silently narrowing `target` to a non-plugin subdirectory
    (`authorkit/skills`) that `discover()` finds nothing under, so authorkit's own
    grammar violations would never be caught by the hook at all. `git rev-parse
    --show-toplevel` has no such false-positive: it asks git which checkout the file
    physically lives in, and a nested manifest file is irrelevant to that answer.

    Returns None (fail open) on any git failure — no `.git`, git missing, timeout."""
    cwd = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return Path(out.stdout.strip())


def resolve_hook_target(file_path: str):
    """Given the absolute path of a file a PostToolUse write just landed on
    (`tool_input.file_path`), return (target_dir, manifest_path) for `run()` — or
    (None, None) if no owning root can be derived, meaning the hook should no-op.

    Resolves the write's own checkout root via `find_repo_root` (git's top-level, worktree-
    correct by construction — issue #276), requires a `naming.manifest.json` directly AT
    that root (governance is opt-in — no manifest there, no-op, same as the prior `--hook`
    contract), and takes the first path segment under that root as the touched plugin — so
    only that ONE plugin is validated, never a fixed all-N-plugins loop."""
    if not file_path:
        return None, None
    p = Path(file_path)
    if not p.is_absolute():
        return None, None
    repo_root = find_repo_root(p)
    if repo_root is None:
        return None, None
    manifest_path = repo_root / "naming.manifest.json"
    if not manifest_path.is_file():
        return None, None
    try:
        rel = p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None, None
    if not rel.parts:
        return None, None
    target = repo_root / rel.parts[0]
    if not target.is_dir():
        return None, None
    return target, manifest_path


def main_hook_stdin():
    """PostToolUse entry point (`validate.py hook`, issue #276). Reads the hook event
    off stdin, derives target+manifest via `resolve_hook_target`, and gates on grammar
    findings only — the same `--scope grammar` the prior fixed-loop hook always passed.
    Fails open (exit 0, silent) on anything unexpected: a malformed event, no derivable
    root, an unreadable/wrong-shape manifest, or any other unhandled exception inside
    `run()` — a flaky governance hook is worse than none (hook-writing-rules)."""
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    # Shape guards (code-checker finding, 2026-08-15): valid JSON is not necessarily a
    # dict-shaped event — `[1,2]`, `{"tool_input":"oops"}`, and a non-str file_path all
    # crashed here with traceback + exit 1, violating this function's own fail-open
    # contract. Guard every shape before use.
    if not isinstance(event, dict):
        return 0
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    file_path = tool_input.get("file_path", "")
    if not isinstance(file_path, str) or not file_path:
        return 0
    target, manifest_path = resolve_hook_target(file_path)
    if target is None:
        return 0  # nothing governed under this write — no manifest ancestor found
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError):
        return 0  # unreadable/malformed manifest — fail open, never block the write
    if not isinstance(manifest, dict):
        return 0  # valid JSON, wrong shape (e.g. a bare list) — fail open, not a crash
    try:
        result = run(target, manifest, scope="grammar")
    except Exception:
        # run()/Grammar() can still raise on a manifest that's dict-shaped but malformed
        # in some OTHER way this validator doesn't defensively check for everywhere
        # (found live, issue #276 review: hook-checker probed a wrong-shape-but-valid-JSON
        # manifest and got an uncaught crash here). A crashing governance hook is worse
        # than a skipped check — fail open on ANY unexpected exception, never let an
        # internal bug surface as exit 1 + traceback on every subsequent write.
        return 0
    if result["grammar_errors"]:
        for name, _lvl, msg, _cat in result["grammar_errors"]:
            print(f"authorkit naming-grammar: {name}: {msg}", file=sys.stderr)
        return 2
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--manifest")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hook", action="store_true",
                    help="no-op cleanly when target has no manifest")
    ap.add_argument("--scope", choices=["full", "grammar"], default=None,
                    help="full: gate on every finding, authorkit's own dogfooding "
                         "contract. grammar: gate only on naming-grammar findings, "
                         "and drop (not just non-gate) structural findings outside "
                         "authorkit's own tree. Explicit --scope always wins over the "
                         "manifest. Omitted: the default comes from the manifest's own "
                         "schema_scope field (absent -> full, back-compat) — see "
                         "module docstring")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    mpath = Path(args.manifest) if args.manifest else None
    if mpath is None:
        for cand in (target / "naming.manifest.json",
                     target / ".claude" / "naming.manifest.json"):
            if cand.is_file():
                mpath = cand
                break
    if mpath is None:
        # Neither direct probe found a manifest AT `target` itself. Issue #842: a
        # plugin-scoped `--target <plugin-dir>` under a workspace-governed estate (the
        # manifest sitting one or more levels ABOVE the plugin, e.g. at the git
        # toplevel) was invisible here, so every such run fell through to "ungoverned"
        # and recommended seeding a plugin-local manifest — forking the estate lexicon.
        #
        # This is deliberately NOT the directory-walk-to-nearest-manifest that
        # `find_repo_root`'s own docstring rejects: that rejection is scoped to HOOK
        # target derivation (`resolve_hook_target`), where authorkit's own nested
        # self-dogfood manifest copy makes a walk stop at the wrong ancestor for a
        # write inside authorkit itself. Here we reuse `find_repo_root`'s single
        # `git rev-parse --show-toplevel` call (no walk, no marker-file search) and
        # probe the git toplevel exactly once — the outermost governing manifest, never
        # authorkit's own nested copy, because that copy is never AT the toplevel.
        repo_root = find_repo_root(target)
        if repo_root is not None and repo_root != target:
            cand = repo_root / "naming.manifest.json"
            if cand.is_file():
                mpath = cand
    if mpath is None or not mpath.is_file():
        msg = ("no naming.manifest.json found at <target>/, <target>/.claude/, or the "
               "git toplevel — estate is ungoverned")
        if args.hook:
            print(f"authorkit: {msg}; skipping (governance is opt-in)")
            sys.exit(0)
        print(f"authorkit: {msg}. Seed one via manifest-authoring.")
        sys.exit(2)

    manifest = json.loads(mpath.read_text())
    if args.scope is not None:
        scope = args.scope
    else:
        scope = manifest.get("schema_scope", "full")
        if scope not in ("full", "grammar"):
            scope = "full"  # unrecognized value -> back-compat default, never crash
    result = run(target, manifest, scope=scope)
    gating_errors = result["errors"] if scope == "full" else result["grammar_errors"]

    if args.json:
        print(json.dumps({
            "target": str(target), "manifest": str(mpath), "scope": scope,
            "artifacts": result["artifacts"], "errors": result["errors"],
            "warnings": result["warnings"],
            "grammar_errors": result["grammar_errors"],
            "structural_errors": result["structural_errors"],
            "exemption_burndown": result["exemption_burndown"],
        }, indent=2))
    else:
        print(f"authorkit validate — {result['artifacts']} artifacts @ {target} (scope={scope})")
        for name, lvl, msg, cat in result["findings"]:
            tag = {"error": "ERROR", "warn": "WARN ", "exempt-note": "EXMPT"}[lvl]
            demoted = " [structural, non-blocking in --scope grammar]" if (
                scope == "grammar" and lvl == "error" and cat == "structural") else ""
            print(f"  [{tag}] {name}: {msg}{demoted}")
        print(f"  errors={len(result['errors'])} "
              f"(grammar={len(result['grammar_errors'])} structural={len(result['structural_errors'])}) "
              f"warnings={len(result['warnings'])} exemptions={result['exemption_burndown']['count']}")
    sys.exit(1 if gating_errors else 0)


def selftest():
    """Prove run()'s counters bite: a clean mini-estate passes; a deliberately
    broken one is caught (name/folder mismatch, schema-outside field, banned
    alias, lexicon-disjointness violation); the two invocation dials this
    ticket adds to the schema are accepted, not flagged as outside-schema."""
    import tempfile

    manifest = {
        "verb_lex": ["audit"], "process_lex": ["review"], "role_lex": [],
        "object_vocab": [{"canonical": "demo", "plural": None, "banned_aliases": ["sample"]}],
        "brand_tokens": [], "author_registry": ["kim"],
        "mutating_no_confirm_allowlist": [], "exemptions": [],
    }

    def skill_md(name, extra_fm=""):
        return (f"---\nname: {name}\nkind: skill\ndescription: demo\n"
                f"author: kim\ncreated: 2026-08-13\nlast_updated: 2026-08-13\n"
                f"disable-model-invocation: false\nuser-invocable: false\n{extra_fm}---\nbody\n")

    # Reverse control: a clean estate must validate with zero errors, and the
    # two dials this ticket adds to the schema must not fire "outside schema".
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not result["errors"], f"clean estate must validate error-free: {result['errors']}"
        assert not any("disable-model-invocation" in e[2] or "user-invocable" in e[2]
                       for e in result["errors"]), "invocation dials must be schema-accepted"

    # Inversion fixture 1: frontmatter name != folder name must be CAUGHT.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("wrong-name"))
        result = run(r, manifest)
        assert any("!= folder" in e[2] for e in result["errors"]), \
            "name/folder mismatch must be caught"

    # Inversion fixture 2: a field outside the kind's schema must be CAUGHT.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(
            skill_md("demo-review", extra_fm="bogus_field: x\n"))
        result = run(r, manifest)
        assert any("outside schema" in e[2] for e in result["errors"]), \
            "unschema'd field must be caught"

    # Inversion fixture 3: VerbLex/ProcessLex disjointness violation must be CAUGHT.
    bad_manifest = dict(manifest, verb_lex=["review"], process_lex=["review"])
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, bad_manifest)
        assert any("disjointness" in e[2] for e in result["errors"]), \
            "lexicon disjointness violation must be caught"

    # --scope fixture (issue #197 wiring): a name-clean skill missing provenance fields
    # is STRUCTURAL only — grammar_errors must stay empty even though errors does not.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        no_author = "---\nname: demo-review\nkind: skill\ndescription: demo\n" \
                    "disable-model-invocation: false\nuser-invocable: false\n---\nbody\n"
        (r / "skills" / "demo-review" / "SKILL.md").write_text(no_author)
        result = run(r, manifest)
        assert result["errors"] and not result["grammar_errors"], \
            "missing-provenance fixture must be structural-only, not grammar"
        assert result["structural_errors"], "missing-provenance fixture must land in structural_errors"
        # partition is exhaustive: every error is exactly one of the two buckets
        assert len(result["grammar_errors"]) + len(result["structural_errors"]) == len(result["errors"]), \
            "grammar_errors + structural_errors must exhaustively partition errors"

    # Inverse: a genuine grammar violation (unresolvable object-process name) must land
    # in grammar_errors even when every provenance field is present and clean.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-nonsense").mkdir(parents=True)
        (r / "skills" / "demo-nonsense" / "SKILL.md").write_text(skill_md("demo-nonsense"))
        result = run(r, manifest)
        assert result["grammar_errors"], "unresolvable name must land in grammar_errors"

    # Skill-lint's retired W4 successor (issue #197): a skill name ending in the reserved
    # -agent head is a grammar violation, not a structural one — the cross-type-ambiguity
    # concern W4 used to police, under this grammar's own terms.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-agent").mkdir(parents=True)
        (r / "skills" / "demo-agent" / "SKILL.md").write_text(skill_md("demo-agent"))
        result = run(r, manifest)
        assert any("reserved head -agent on a skill" in e[2] for e in result["grammar_errors"]), \
            "a skill named *-agent must be a grammar_errors hit (W4's successor concern)"

    # ADR-0015 D1/D2/D3 — orchestrator agents parse as {scope}-{role}, -agent optional
    # on that production only; scope resolves against ObjectVocab ∪ ProcessLex; RoleLex
    # stays disjoint from that pool. `manifest` above ships role_lex=[]; a dedicated
    # variant registers `leader` plus the scopes these fixtures exercise.
    def agent_md(name, performs="demo-review"):
        return (f"---\nname: {name}\nkind: agent\ndescription: demo\n"
                f"author: kim\ncreated: 2026-08-13\nlast_updated: 2026-08-13\n"
                f"performs: {performs}\nautonomous_write: false\ncontext: isolated\n"
                f"tools: Read\n---\nbody\n")

    orch_manifest = dict(
        manifest,
        role_lex=["leader"],
        object_vocab=manifest["object_vocab"] + [
            {"canonical": "team", "plural": None, "banned_aliases": []},
            {"canonical": "product", "plural": None, "banned_aliases": []},
        ],
    )

    # Positive: bare {scope}-{role} — scope resolved against ObjectVocab (`team`).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "team-leader.md").write_text(agent_md("team-leader"))
        result = run(r, orch_manifest)
        assert not result["grammar_errors"], \
            f"bare {{scope}}-{{role}} orchestrator name must parse clean: {result['grammar_errors']}"

    # Positive: bare {scope}-{role} — scope resolved against ProcessLex (`review`,
    # ADR-0015 D2's union pool, not ObjectVocab alone).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "review-leader.md").write_text(agent_md("review-leader"))
        result = run(r, orch_manifest)
        assert not result["grammar_errors"], \
            f"ProcessLex-scoped orchestrator name must parse clean: {result['grammar_errors']}"

    # Positive: vocab-stem production (2026-08-31, adiahealth/adia-harness) — a
    # {ObjectVocab-token}-agent name parses clean (a domain-scoped generalist agent).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "team-agent.md").write_text(agent_md("team-agent"))
        result = run(r, orch_manifest)
        assert not result["grammar_errors"], \
            f"ObjectVocab-stem -agent name must parse clean: {result['grammar_errors']}"

    # Negative: the vocab-stem production resolves against ObjectVocab ONLY — a
    # ProcessLex word as the stem (`review-agent`) must still fail (skill-stem or
    # scope-role remain the only doors for process words).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "review-agent.md").write_text(agent_md("review-agent"))
        result = run(r, orch_manifest)
        assert result["grammar_errors"], \
            "a ProcessLex-stem -agent name must NOT parse via the vocab-stem production"

    # Regression: the legacy {scope}-{role}-agent spelling still parses (D1 keeps it
    # conformant by grammar, not by exemption).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "product-leader-agent.md").write_text(agent_md("product-leader-agent"))
        result = run(r, orch_manifest)
        assert not result["grammar_errors"], \
            f"legacy scope-role-agent spelling must still parse clean: {result['grammar_errors']}"

    # Negative: a bare non-role name in agents/ (no RoleLex terminal, no -agent tail)
    # must still fail.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "estate-audit.md").write_text(agent_md("estate-audit"))
        result = run(r, orch_manifest)
        assert result["grammar_errors"], \
            "a bare non-role agent name must still fail grammar"

    # Negative: the same {scope}-{role} string in skills/ must still fail — `leader`
    # is no ObjectVocab/ProcessLex member, so nominal resolution rejects it.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "team-leader").mkdir(parents=True)
        (r / "skills" / "team-leader" / "SKILL.md").write_text(skill_md("team-leader"))
        result = run(r, orch_manifest)
        assert result["grammar_errors"], \
            "a scope-role string minted as a SKILL must still fail grammar"

    # Negative: a RoleLex word that also lives in ObjectVocab must raise the D3
    # manifest disjointness error.
    collision_manifest = dict(
        manifest,
        role_lex=["leader"],
        object_vocab=manifest["object_vocab"] + [
            {"canonical": "leader", "plural": None, "banned_aliases": []},
        ],
    )
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, collision_manifest)
        assert any("RoleLex" in e[2] and "disjointness" in e[2] for e in result["errors"]), \
            f"RoleLex/ObjectVocab collision must raise the D3 manifest error: {result['errors']}"

    # ADR-0020 D3 (2026-08-17, #520) — `bind-`/`fork-`/`sub-` reserved verb-first heads
    # on both the command and skill parse branches, replacing the general-purpose
    # `lead-` production (ADR-0016 D1/D2). Scope pool = the orchestrator scope pool
    # (ADR-0015 D2), unchanged. Positive: each of the three heads on both branches;
    # negative: a non-reserved verb-first command/skill, and an unregistered scope on
    # each head; regression: object-first commands and object-process skills unaffected.
    lead_manifest = dict(
        manifest,
        process_lex=["review", "planning"],
        object_vocab=manifest["object_vocab"] + [
            {"canonical": "team", "plural": None, "banned_aliases": []},
            {"canonical": "product", "plural": "products", "banned_aliases": []},
            {"canonical": "build", "plural": "builds", "banned_aliases": []},
            {"canonical": "agent", "plural": "agents", "banned_aliases": []},
        ],
    )

    def lead_command_md(name):
        return (f"---\nname: {name}\nkind: command\ndescription: demo\n"
                f"author: kim\ncreated: 2026-08-16\nlast_updated: 2026-08-16\n---\nbody\n")

    # Positive: each of bind-/fork-/sub- parses clean as a SKILL, across an
    # ObjectVocab scope (team/build) and a ProcessLex scope (planning/review). Scope
    # deliberately avoids "agent" here — a residue of "agent" collides with the
    # unconditional -agent reserved-TAIL check on the skill branch (same dead-code
    # hazard make-agent proves below), which is a real, correct rejection, not a bug in
    # this head; "agent" is exercised on the COMMAND branch instead, just below.
    for reserved_name in ("bind-team", "bind-planning", "fork-build", "sub-review"):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "skills" / reserved_name).mkdir(parents=True)
            (r / "skills" / reserved_name / "SKILL.md").write_text(skill_md(reserved_name))
            result = run(r, lead_manifest)
            assert not result["grammar_errors"], \
                f"{reserved_name} must parse clean under ADR-0020's reserved heads: {result['grammar_errors']}"

    # Positive: the same three heads on the COMMAND branch (a commands/ file each).
    for reserved_name in ("bind-team", "fork-agent", "sub-agent"):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "commands").mkdir(parents=True)
            (r / "commands" / f"{reserved_name}.md").write_text(lead_command_md(reserved_name))
            result = run(r, lead_manifest)
            assert not result["grammar_errors"], \
                f"{reserved_name} as a command must parse clean: {result['grammar_errors']}"

    # Negative: a verb-first command that is NOT one of the reserved heads still fails —
    # each head is one literal, never a VerbLex-wide verb-first production.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "commands").mkdir(parents=True)
        (r / "commands" / "audit-team.md").write_text(lead_command_md("audit-team"))
        result = run(r, lead_manifest)
        assert result["grammar_errors"], \
            "a non-reserved-head verb-first command must still fail grammar"

    # Negative: {head}-{unregistered scope} fails on BOTH branches, for each reserved head.
    for head in ("bind", "fork", "sub"):
        name = f"{head}-bogus"
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "skills" / name).mkdir(parents=True)
            (r / "skills" / name / "SKILL.md").write_text(skill_md(name))
            (r / "commands").mkdir(parents=True)
            (r / "commands" / f"{name}.md").write_text(lead_command_md(name))
            result = run(r, lead_manifest)
            hit_names = {n for n, _, _, _ in result["grammar_errors"]}
            assert name in hit_names and len(result["grammar_errors"]) >= 2, \
                f"{head}-<unregistered> must fail on both branches: {result['grammar_errors']}"

    # Regression: object-first commands and object-process skills are unaffected.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        (r / "commands").mkdir(parents=True)
        (r / "commands" / "demo-audit.md").write_text(lead_command_md("demo-audit"))
        result = run(r, lead_manifest)
        assert not result["grammar_errors"], \
            f"object-first names must be unaffected by the new reserved heads: {result['grammar_errors']}"

    # ADR-0020 D3 — `lead-` is RETIRED as an open production, with no grandfather set left
    # (the closed `LEAD_HEAD_GRANDFATHER` set and its two branches were deleted outright at
    # wave 5, #523, once all six live surfaces renamed to `bind-{scope}`): ANY `lead-*` mint —
    # brand new, or one of the six former surface names — must be REJECTED now, exactly like
    # any other unregistered head. It falls through to the plain object-verb command/skill
    # productions and fails there (`lead` is not a VerbLex/ProcessLex/ObjectVocab member), not
    # via a dedicated "lead- head retired" message — there is no lead- branch left to raise one.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "lead-widget").mkdir(parents=True)
        (r / "skills" / "lead-widget" / "SKILL.md").write_text(
            skill_md("lead-widget"))
        widget_manifest = dict(
            lead_manifest,
            object_vocab=lead_manifest["object_vocab"] + [
                {"canonical": "widget", "plural": "widgets", "banned_aliases": []},
            ],
        )
        result = run(r, widget_manifest)
        assert result["grammar_errors"], \
            "a lead-* mint must be rejected — lead- is retired with no grandfather set left"

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "commands").mkdir(parents=True)
        (r / "commands" / "lead-widget.md").write_text(lead_command_md("lead-widget"))
        widget_manifest = dict(
            lead_manifest,
            object_vocab=lead_manifest["object_vocab"] + [
                {"canonical": "widget", "plural": "widgets", "banned_aliases": []},
            ],
        )
        result = run(r, widget_manifest)
        assert result["grammar_errors"], \
            "a lead-* command mint must be rejected on the command branch too"

    # Regression — the six FORMER `/lead-*` surfaces, renamed to `/bind-*` at wave 5 (#523),
    # parse clean under their new names with no grandfather set involved — the general
    # RESERVED_BIND_FORK_SUB_HEADS branch alone, same as any other bind-/fork-/sub- mint.
    # `intake` isn't in lead_manifest's scope pool above, so extend it locally — exactly
    # the original lead-intake fixture's own pattern for the same reason.
    bind_regression_manifest = dict(
        lead_manifest,
        object_vocab=lead_manifest["object_vocab"] + [
            {"canonical": "intake", "plural": None, "banned_aliases": []},
        ],
    )
    for bind_name in ("bind-team", "bind-product", "bind-build", "bind-planning", "bind-review", "bind-intake"):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "commands").mkdir(parents=True)
            (r / "commands" / f"{bind_name}.md").write_text(lead_command_md(bind_name))
            result = run(r, bind_regression_manifest)
            assert not result["grammar_errors"], \
                f"{bind_name} must parse clean as a command via the general bind- head: {result['grammar_errors']}"

    # ADR-0017 — RoleLex +10 execution-seat suffixes (checker/runner/planner/watcher/
    # finder/sorter/cleaner/judge/builder/writer): the {scope}-{role} production now
    # covers execution seats, not only coordinators. Positive: a scope token (either
    # ObjectVocab or ProcessLex, per ADR-0015 D2's pool) with each new role suffix.
    s8_role_manifest = dict(
        manifest,
        role_lex=["leader", "checker", "runner", "planner", "watcher", "finder",
                  "sorter", "cleaner", "judge", "builder", "writer"],
        process_lex=["review"],
        object_vocab=manifest["object_vocab"] + [
            {"canonical": "code", "plural": None, "banned_aliases": []},
            {"canonical": "experiment", "plural": None, "banned_aliases": []},
            {"canonical": "decision", "plural": "decisions", "banned_aliases": []},
        ],
    )
    for agent_name in ("code-checker", "experiment-runner", "decision-watcher",
                       "review-planner"):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "agents").mkdir(parents=True)
            (r / "agents" / f"{agent_name}.md").write_text(agent_md(agent_name))
            result = run(r, s8_role_manifest)
            assert not result["grammar_errors"], \
                f"{agent_name} must parse clean under RoleLex+10: {result['grammar_errors']}"

    # Negative: a bare RoleLex terminal with no scope token still fails (ADR-0017
    # explicitly does NOT make bare role words like `builder`/`planner` conformant —
    # the {scope}-{role} production requires >= 2 tokens with a resolvable scope).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir(parents=True)
        (r / "agents" / "builder.md").write_text(agent_md("builder"))
        result = run(r, s8_role_manifest)
        assert result["grammar_errors"], \
            "a bare RoleLex word with no scope token must still fail grammar"

    # ADR-0018 D1 — `make-` and `file-` reserved skill heads. Positive: registered
    # ObjectVocab residues under each head.
    s8_head_manifest = dict(
        manifest,
        object_vocab=manifest["object_vocab"] + [
            {"canonical": "doc", "plural": "docs", "banned_aliases": []},
            {"canonical": "reference", "plural": "references", "banned_aliases": []},
            {"canonical": "rubric", "plural": "rubrics", "banned_aliases": []},
            {"canonical": "vision-memo", "plural": None, "banned_aliases": []},
            {"canonical": "llms-txt", "plural": None, "banned_aliases": []},
            {"canonical": "bug", "plural": "bugs", "banned_aliases": []},
            {"canonical": "task", "plural": "tasks", "banned_aliases": []},
        ],
    )
    for head_name in ("make-doc", "make-reference", "make-rubric", "make-vision-memo",
                      "make-llms-txt", "file-bug", "file-task"):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "skills" / head_name).mkdir(parents=True)
            (r / "skills" / head_name / "SKILL.md").write_text(skill_md(head_name))
            result = run(r, s8_head_manifest)
            assert not result["grammar_errors"], \
                f"{head_name} must parse clean under the make-/file- heads: {result['grammar_errors']}"

    # Negative: a non-reserved verb head is not granted the same treatment — the
    # literal head set stays closed at {check, make, file}, never a template
    # for VerbLex at large (ADR-0014 Alt C stays rejected).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "sort-issues").mkdir(parents=True)
        (r / "skills" / "sort-issues" / "SKILL.md").write_text(skill_md("sort-issues"))
        result = run(r, s8_head_manifest)
        assert result["grammar_errors"], \
            "a non-reserved verb head (sort-) must still fail grammar"

    # Negative: make-{unregistered scope} still fails.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "make-widget").mkdir(parents=True)
        (r / "skills" / "make-widget" / "SKILL.md").write_text(skill_md("make-widget"))
        result = run(r, s8_head_manifest)
        assert result["grammar_errors"], \
            "make-<unregistered scope> must still fail grammar"

    # CRITICAL regression — tail-before-head: `make-agent` must keep failing even
    # though `make` is now a valid reserved head, because the -agent reserved TAIL
    # check (line ~391) runs unconditionally before any head-token branch is reached.
    # This is the one fixture ADR-0018 names explicitly as the dead-code-hazard proof.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "make-agent").mkdir(parents=True)
        (r / "skills" / "make-agent" / "SKILL.md").write_text(skill_md("make-agent"))
        result = run(r, s8_head_manifest)
        assert any("reserved head -agent on a skill" in e[2] for e in result["grammar_errors"]), \
            f"make-agent must keep failing on the -agent tail, tail-before-head: {result['grammar_errors']}"

    # Scoped write-grant detection (issue #237, found during #235/PR #236): the
    # policy/grant-coherence check must recognize a SCOPED write grant (tool name
    # + parenthesized scope, e.g. 'Edit(**/naming.manifest.json)') as that write
    # tool, not read as write-less. Exercised directly against policy_checks —
    # the grant-parsing unit under test — rather than through a full skill/agent
    # fixture, since none of these three controls touch Grammar/_grammar state.

    # Positive control: a scoped Edit grant must still be caught as write-capable.
    scoped_fm = {"autonomous_write": False, "context": "isolated",
                 "tools": ["Edit(**/naming.manifest.json)"]}
    scoped_errs, _ = policy_checks("agent", scoped_fm, "demo-agent")
    assert any("autonomous_write: false but write-capable tools granted" in e for e in scoped_errs), \
        "a scoped Edit(...) grant must still read as write-carrying (#237)"

    # Bare-name control (no regression): the un-scoped form that already worked
    # before this fix must keep working exactly as before.
    bare_fm = {"autonomous_write": False, "context": "isolated", "tools": ["Edit"]}
    bare_errs, _ = policy_checks("agent", bare_fm, "demo-agent")
    assert any("autonomous_write: false but write-capable tools granted" in e for e in bare_errs), \
        "a bare Edit grant must read as write-carrying (regression control)"

    # Negative control: a read-only grant, scoped or bare, must never read as write.
    readonly_fm = {"autonomous_write": False, "context": "isolated",
                    "tools": ["Read(**/*.md)", "Grep"]}
    readonly_errs, _ = policy_checks("agent", readonly_fm, "demo-agent")
    assert not any("write-capable tools granted" in e for e in readonly_errs), \
        "a read-only grant (scoped or bare) must never read as write-carrying"

    # CLI wiring: --scope grammar must exit 0 on a structural-only fixture that --scope
    # full (default) fails; a genuine grammar violation must still exit 1 under either.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(no_author)
        mf = r / "naming.manifest.json"
        mf.write_text(json.dumps(manifest))
        full = subprocess.run([sys.executable, __file__, "--target", str(r), "--manifest", str(mf)])
        assert full.returncode == 1, "--scope full (default) must fail the structural-only fixture"
        grammar = subprocess.run([sys.executable, __file__, "--target", str(r), "--manifest", str(mf),
                                   "--scope", "grammar"])
        assert grammar.returncode == 0, "--scope grammar must pass a structural-only fixture"

    # schema_scope (issue #226, #224 ruling b): the manifest's own field picks the
    # default scope when --scope is omitted; an explicit --scope still overrides it.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(no_author)

        # Negative control: schema_scope ABSENT -> defaults to full (back-compat) —
        # a manifest with no opinion behaves exactly as it did before this field existed.
        mf_absent = r / "naming.manifest.json"
        mf_absent.write_text(json.dumps(manifest))
        absent = subprocess.run([sys.executable, __file__, "--target", str(r),
                                  "--manifest", str(mf_absent)])
        assert absent.returncode == 1, \
            "schema_scope absent must default to full (back-compat negative control)"

        # schema_scope: "grammar" in the manifest, no --scope flag -> the manifest's
        # own tier picks the default; a structural-only fixture must now pass.
        mf_grammar = dict(manifest, schema_scope="grammar")
        mf_grammar_path = r / "naming.manifest.grammar.json"
        mf_grammar_path.write_text(json.dumps(mf_grammar))
        grammar_default = subprocess.run([sys.executable, __file__, "--target", str(r),
                                           "--manifest", str(mf_grammar_path)])
        assert grammar_default.returncode == 0, \
            "schema_scope: grammar in the manifest must default the run to grammar scope"

        # Explicit --scope still overrides the manifest's own schema_scope.
        override = subprocess.run([sys.executable, __file__, "--target", str(r),
                                    "--manifest", str(mf_grammar_path), "--scope", "full"])
        assert override.returncode == 1, \
            "explicit --scope full must override a manifest schema_scope: grammar"

    # schema_scope own-tree carve-out (issue #226): under scope=grammar, structural
    # findings for artifacts OUTSIDE own_root are dropped entirely (not just
    # non-gated); artifacts INSIDE own_root still count — authorkit dogfoods full
    # on itself regardless of the estate's declared tier.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(no_author)
        own = r / "own-plugin"
        (own / "skills" / "demo-review").mkdir(parents=True)
        (own / "skills" / "demo-review" / "SKILL.md").write_text(no_author)

        foreign_result = run(r, manifest, scope="grammar", own_root=own)
        assert not foreign_result["structural_errors"], \
            "grammar scope must drop structural findings for artifacts outside own_root"

        own_result = run(own, manifest, scope="grammar", own_root=own)
        assert own_result["structural_errors"], \
            "grammar scope must still count structural findings for own_root's own artifacts"

        full_result = run(r, manifest, scope="full", own_root=own)
        assert full_result["structural_errors"], \
            "full scope must count structural findings regardless of own_root"

    # Reverse-wrapper grammar amendment (spec-naming-convention.md §14.1, issue #241): a
    # skill's object-verb name (terminal token in VerbLex, not ProcessLex) is legal IFF an
    # identically-named command exists in the same plugin root. Three fixtures: positive
    # (WITH the wrapper passes), negative (the SAME name WITHOUT one still fails — the
    # amendment must not open the door to unwrapped verb-terminal skill names), and
    # regression (existing nominal names are unaffected).
    reverse_manifest = dict(manifest, verb_lex=["audit", "execute"])

    def command_md(name, wraps=None):
        extra = f"wraps: {wraps}\n" if wraps else ""
        return (f"---\nname: {name}\nkind: command\ndescription: demo\n"
                f"author: kim\ncreated: 2026-08-13\nlast_updated: 2026-08-13\n{extra}---\nbody\n")

    # Positive control: verb-terminal skill name WITH an identically-named command wrapper
    # passes grammar.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-execute").mkdir(parents=True)
        (r / "skills" / "demo-execute" / "SKILL.md").write_text(skill_md("demo-execute"))
        (r / "commands").mkdir(parents=True)
        (r / "commands" / "demo-execute.md").write_text(command_md("demo-execute", wraps="demo-execute"))
        result = run(r, reverse_manifest)
        assert not result["grammar_errors"], \
            f"verb-terminal skill WITH identical command wrapper must pass grammar: {result['grammar_errors']}"

    # Negative control: the SAME verb-terminal skill name WITHOUT the wrapper still fails —
    # the amendment must not open the door to an unwrapped verb-terminal skill name.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-execute").mkdir(parents=True)
        (r / "skills" / "demo-execute" / "SKILL.md").write_text(skill_md("demo-execute"))
        result = run(r, reverse_manifest)
        assert result["grammar_errors"], \
            "verb-terminal skill WITHOUT an identical command wrapper must still fail grammar"
        assert any(n == "demo-execute" for n, _, _, _ in result["grammar_errors"]), \
            "the failing grammar finding must name the unwrapped skill"

    # Regression control: an existing nominal (object-process) skill name is unaffected by
    # the amendment, even under a manifest whose VerbLex now carries the new verb token.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, reverse_manifest)
        assert not result["grammar_errors"], \
            f"existing nominal skill names must be unaffected by the reverse-wrapper amendment: {result['grammar_errors']}"

    # Reverse-wrapper amendment, extended (spec-naming-convention.md §14.9, issue #525): a
    # verb-terminal skill name is ALSO legal with `user-invocable: true` and NO sibling
    # command at all — the skill-as-command dual-access shape that supersedes the
    # command-wrapper realization §14.1 originally licensed. Same triad: positive (the
    # skill alone, `user-invocable: true`, no commands/ dir whatsoever, passes), negative
    # (the identical skill with `user-invocable: false` and still no wrapper still fails —
    # the extension must not make the dial irrelevant), regression (the §14.1 command-wrapper
    # path above still passes unchanged now that this second path exists too).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-execute").mkdir(parents=True)
        (r / "skills" / "demo-execute" / "SKILL.md").write_text(
            skill_md("demo-execute", extra_fm="user-invocable: true\n"))
        result = run(r, reverse_manifest)
        assert not result["grammar_errors"], \
            f"verb-terminal skill with user-invocable:true and no wrapper must pass grammar: {result['grammar_errors']}"

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-execute").mkdir(parents=True)
        (r / "skills" / "demo-execute" / "SKILL.md").write_text(skill_md("demo-execute"))
        result = run(r, reverse_manifest)
        assert result["grammar_errors"], \
            "verb-terminal skill with user-invocable:false and no wrapper must still fail grammar"

    # D1 — `-rules` reserved-tail production (spec-naming-convention.md §14.2, ADR-0014):
    # positive (topic-phrase resolves via the union pool: an ObjectVocab noun + a
    # ProcessLex word, mirroring the estate's real `{noun}-writing-rules` pattern),
    # negative (an unregistered topic word still fails — the amendment must not open the
    # door to an arbitrary `-rules` name), regression (a plain object-process name is
    # unaffected even once TopicLex is populated).
    topic_manifest = dict(manifest, topic_lex=["icon"])

    # Positive control: `demo-review-rules` — "demo" ∈ ObjectVocab, "review" ∈ ProcessLex —
    # resolves via D1's union pool even though neither token is in TopicLex.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review-rules").mkdir(parents=True)
        (r / "skills" / "demo-review-rules" / "SKILL.md").write_text(skill_md("demo-review-rules"))
        result = run(r, topic_manifest)
        assert not result["grammar_errors"], \
            f"a -rules tail whose topic-phrase resolves via the union pool must pass: {result['grammar_errors']}"

    # Positive control 2: `icon-rules` — "icon" resolves via TopicLex alone (no ObjectVocab
    # or ProcessLex membership needed) — the pure D3 topic-word case.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "icon-rules").mkdir(parents=True)
        (r / "skills" / "icon-rules" / "SKILL.md").write_text(skill_md("icon-rules"))
        result = run(r, topic_manifest)
        assert not result["grammar_errors"], \
            f"a -rules tail resolving purely via TopicLex must pass: {result['grammar_errors']}"

    # Negative control: `bogus-rules` — "bogus" resolves in no lexicon at all — must still
    # fail; the union pool is not a blanket pass for any `-rules` name.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "bogus-rules").mkdir(parents=True)
        (r / "skills" / "bogus-rules" / "SKILL.md").write_text(skill_md("bogus-rules"))
        result = run(r, topic_manifest)
        assert result["grammar_errors"], \
            "a -rules tail with an unregistered topic word must still fail grammar"
        assert any("rules tail" in e[2] for e in result["grammar_errors"]), \
            "the failing finding must name the rules-tail production"

    # Regression control: an ordinary object-process skill name (no -rules tail) is
    # unaffected even once TopicLex carries entries.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, topic_manifest)
        assert not result["grammar_errors"], \
            f"a non--rules name must be unaffected by a populated TopicLex: {result['grammar_errors']}"

    # D2 — `check-` reserved-head production (spec-naming-convention.md §14.2, ADR-0014):
    # positive (`check-demo`, residue resolves via ObjectVocab), negative (`check-bogus`,
    # unregistered residue still fails), regression (a quantifier-shaped name —
    # `check-all-demos`-style — stays failing exactly as the 4 named non-goals require,
    # since "all" is never registered anywhere).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "check-demo").mkdir(parents=True)
        (r / "skills" / "check-demo" / "SKILL.md").write_text(skill_md("check-demo"))
        result = run(r, manifest)
        assert not result["grammar_errors"], \
            f"check-<noun> whose residue resolves via ObjectVocab must pass: {result['grammar_errors']}"

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "check-bogus").mkdir(parents=True)
        (r / "skills" / "check-bogus" / "SKILL.md").write_text(skill_md("check-bogus"))
        result = run(r, manifest)
        assert result["grammar_errors"], \
            "check- with an unregistered residue noun must still fail grammar"
        assert any("check- head" in e[2] for e in result["grammar_errors"]), \
            "the failing finding must name the check-head production"

    # Regression control: the 4 quantifier-shaped non-goals (ADR-0014 "What does NOT
    # change") stay exempt-only — "all" is never registered in any lexicon, so a
    # check-all-<noun> shape still fails grammar even when <noun> itself resolves.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "check-all-demo").mkdir(parents=True)
        (r / "skills" / "check-all-demo" / "SKILL.md").write_text(skill_md("check-all-demo"))
        result = run(r, manifest)
        assert result["grammar_errors"], \
            "a quantifier-shaped check-all-<noun> name must still fail grammar (named non-goal)"

    # Dual-membership control (ADR-0014 D4): a token registered in BOTH ObjectVocab and
    # ProcessLex (like the production manifest's own `stage`) must still resolve under D2's
    # ObjectVocab-only residue check — proves D2 does not accidentally exclude a dual-member
    # token just because it also sits in ProcessLex.
    dual_manifest = dict(
        manifest,
        process_lex=list(manifest["process_lex"]) + ["stage"],
        object_vocab=list(manifest["object_vocab"]) + [
            {"canonical": "stage", "plural": None, "banned_aliases": []}
        ],
    )
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "check-stage").mkdir(parents=True)
        (r / "skills" / "check-stage" / "SKILL.md").write_text(skill_md("check-stage"))
        result = run(r, dual_manifest)
        assert not result["grammar_errors"], \
            f"check-stage must pass via D2 even with stage dual-registered in ProcessLex: {result['grammar_errors']}"

    # author_registry shape validation (issue #252): a structured entry (dict, not a plain
    # string) used to raise a raw uncaught `TypeError: unhashable type: 'dict'` straight out
    # of Grammar.__init__'s set(...) call. Three fixtures: the exact crash reproduced via a
    # direct run() call (must not raise, must surface a clean, actionable manifest_errors
    # finding instead), the same fixture through the CLI's own exit-code contract (must
    # exit 1, never a traceback), and a normal plain string-list manifest as the regression
    # control (must validate completely unaffected by the shape check).
    structured_registry_manifest = dict(manifest, author_registry=[
        {"name": "kim", "emails": ["kim@example.com"]}
    ])
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        # direct run() call: must not raise, must report the shape problem cleanly.
        result = run(r, structured_registry_manifest)
        assert any(
            "author_registry entry must be a plain string" in e[2] for e in result["errors"]
        ), "a structured author_registry entry must surface a named, actionable finding, not crash"
        assert not any(
            "unhashable" in e[2] for e in result["errors"]
        ), "the raw TypeError text must never leak into a finding message"

        # CLI's own exit-code contract: same fixture, through main() via subprocess — must
        # exit 1 (a clean gating error), never a Python traceback (which would exit via an
        # unhandled exception, not this process's own sys.exit(1) contract).
        mf = r / "naming.manifest.json"
        mf.write_text(json.dumps(structured_registry_manifest))
        cli = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--manifest", str(mf)],
            capture_output=True, text=True,
        )
        assert cli.returncode == 1, \
            f"a structured author_registry entry must exit 1 cleanly, not crash: {cli.returncode}"
        assert "Traceback" not in cli.stderr, \
            f"a structured author_registry entry must never raise a raw traceback: {cli.stderr}"

    # Regression control: a normal plain string-list author_registry (the shape every fixture
    # in this selftest already uses) must validate completely unaffected by the shape check.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not any("author_registry entry must be a plain string" in e[2] for e in result["errors"]), \
            "a normal plain string-list author_registry must never trip the shape check"

    # ------------------------------------------------------------------------------
    # Malformed-manifest robustness sweep (issue #296, pre-adia-estates-campaign): every
    # remaining malformed-`naming.manifest.json` class besides #252's own author_registry
    # shape guard, swept from MANIFEST-TEMPLATE.json's own schema rather than hand-picked.
    # Each class follows #252's worked triplet: a direct run() call (must not raise, must
    # surface a named manifest_errors finding), the CLI's own exit-code contract via
    # subprocess (must exit 1, never a raw traceback), and a regression control (a clean
    # fixture must never trip the new check).
    # ------------------------------------------------------------------------------

    # --- Class 1: wrong type per top-level field — swept from MANIFEST-TEMPLATE.json's own
    # list-typed fields (TOP_LEVEL_LIST_FIELDS), not hand-picked. Every field gets the SAME
    # wrong-type value (a bare int — non-iterable, so it used to raise `TypeError: 'int'
    # object is not iterable` uncaught out of every one of these fields' pre-guard
    # set()/for-loop call sites) and must surface a named finding instead, never crash.
    for field in TOP_LEVEL_LIST_FIELDS:
        bad_manifest = dict(manifest, **{field: 5})
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / "skills" / "demo-review").mkdir(parents=True)
            (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
            result = run(r, bad_manifest)
            assert any(field in e[2] and "must be a list" in e[2] for e in result["errors"]), \
                f"wrong-type {field!r} must surface a named manifest_errors finding: {result['errors']}"
            assert not any("not iterable" in e[2] for e in result["errors"]), \
                f"the raw TypeError text must never leak into a {field!r} finding message"

            mf = r / "naming.manifest.json"
            mf.write_text(json.dumps(bad_manifest))
            cli = subprocess.run(
                [sys.executable, __file__, "--target", str(r), "--manifest", str(mf)],
                capture_output=True, text=True,
            )
            assert cli.returncode == 1, f"wrong-type {field!r} must exit 1 cleanly, not crash: {cli.returncode}"
            assert "Traceback" not in cli.stderr, \
                f"wrong-type {field!r} must never raise a raw traceback: {cli.stderr}"

    # Regression control: the baseline manifest (every TOP_LEVEL_LIST_FIELDS entry
    # correctly list-shaped) must never trip the top-level type sweep.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not any("must be a list" in e[2] for e in result["errors"]), \
            "a correctly-typed manifest must never trip the top-level shape sweep"

    # --- Class 2: missing keys — an object_vocab entry omitting the required 'canonical'
    # key used to raise a raw, uncaught `KeyError: 'canonical'` out of `entry["canonical"]`;
    # must instead surface a named finding and skip the malformed entry, never crash.
    missing_key_manifest = dict(manifest, object_vocab=[{"plural": "skills"}])
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, missing_key_manifest)
        assert any(
            "object_vocab entry missing required key 'canonical'" in e[2] for e in result["errors"]
        ), f"an object_vocab entry missing 'canonical' must surface a named finding: {result['errors']}"
        assert not any("KeyError" in e[2] for e in result["errors"]), \
            "the raw KeyError text must never leak into a finding message"

        mf = r / "naming.manifest.json"
        mf.write_text(json.dumps(missing_key_manifest))
        cli = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--manifest", str(mf)],
            capture_output=True, text=True,
        )
        assert cli.returncode == 1, f"a missing 'canonical' key must exit 1 cleanly, not crash: {cli.returncode}"
        assert "Traceback" not in cli.stderr, \
            f"a missing 'canonical' key must never raise a raw traceback: {cli.stderr}"

    # Regression control: a complete object_vocab entry (every fixture in this selftest
    # already uses one) must never trip the missing-key check.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not any("missing required key 'canonical'" in e[2] for e in result["errors"]), \
            "a complete object_vocab entry must never trip the missing-key check"

    # --- Class 3: duplicate registrations — two object_vocab entries registering the SAME
    # canonical name today silently overwrite each other with no signal at all. Ruling
    # (pinned here, never silently coerced): duplicate registration is an ERROR — the LAST
    # entry still wins (matching this dict's own natural last-write-wins assignment), but
    # that resolution is always surfaced as a named finding, so an unresolved duplicate
    # still gates exit 1 rather than validating clean by accident.
    dup_manifest = dict(manifest, object_vocab=[
        {"canonical": "demo", "plural": None, "banned_aliases": ["sample"]},
        {"canonical": "demo", "plural": "demos", "banned_aliases": []},
    ])
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, dup_manifest)
        assert any(
            "duplicate object_vocab registration" in e[2] and "demo" in e[2] for e in result["errors"]
        ), f"a duplicate canonical registration must surface a named finding: {result['errors']}"
        assert any("last" in e[2].lower() and "wins" in e[2].lower() for e in result["errors"]), \
            "the duplicate finding must name the pinned last-wins resolution, not stay silent about it"

        mf = r / "naming.manifest.json"
        mf.write_text(json.dumps(dup_manifest))
        cli = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--manifest", str(mf)],
            capture_output=True, text=True,
        )
        assert cli.returncode == 1, f"a duplicate registration must exit 1 cleanly, not crash: {cli.returncode}"
        assert "Traceback" not in cli.stderr, \
            f"a duplicate registration must never raise a raw traceback: {cli.stderr}"

    # Regression control: no duplicate canonicals (every other fixture in this selftest)
    # must never trip the duplicate-registration check.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not any("duplicate object_vocab registration" in e[2] for e in result["errors"]), \
            "a manifest with no duplicate canonicals must never trip the duplicate-registration check"

    # --- Class 4: structured-vs-string entries — the MIRROR of #252's author_registry fix:
    # there, a STRUCTURED entry was given where author_registry expects a plain string.
    # Here, object_vocab expects a STRUCTURED {"canonical": ...} entry per
    # MANIFEST-TEMPLATE.json — a plain STRING entry (e.g. mistakenly mimicking
    # author_registry's own flat-list shape) used to raise a raw, uncaught `TypeError:
    # string indices must be integers` out of `entry["canonical"]`. Must surface a named
    # finding instead, never crash.
    string_entry_manifest = dict(manifest, object_vocab=["demo"])
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, string_entry_manifest)
        assert any(
            "object_vocab entry must be a structured object" in e[2] for e in result["errors"]
        ), f"a plain-string object_vocab entry must surface a named finding: {result['errors']}"
        assert not any("string indices" in e[2] for e in result["errors"]), \
            "the raw TypeError text must never leak into a finding message"

        mf = r / "naming.manifest.json"
        mf.write_text(json.dumps(string_entry_manifest))
        cli = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--manifest", str(mf)],
            capture_output=True, text=True,
        )
        assert cli.returncode == 1, \
            f"a plain-string object_vocab entry must exit 1 cleanly, not crash: {cli.returncode}"
        assert "Traceback" not in cli.stderr, \
            f"a plain-string object_vocab entry must never raise a raw traceback: {cli.stderr}"

    # Regression control: normal structured object_vocab entries (every fixture above)
    # must never trip the structured-vs-string check.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        result = run(r, manifest)
        assert not any(
            "object_vocab entry must be a structured object" in e[2] for e in result["errors"]
        ), "normal structured object_vocab entries must never trip the shape check"

    # `hook` mode target derivation (issue #276) — a REAL git repo + a REAL `git worktree
    # add`, not a simulated directory tree, because the fix's own correctness claim is
    # "git's own top-level is worktree-correct by construction"; a fixture that never
    # asks git would not actually exercise that claim.
    def _git(cwd, *args):
        subprocess.run(
            ["git", "-c", "user.email=demo@example.com", "-c", "user.name=demo", *args],
            cwd=str(cwd), check=True, capture_output=True, text=True,
        )

    with tempfile.TemporaryDirectory() as td:
        # .resolve() up front: macOS's /var -> /private/var symlink means an unresolved
        # tempdir path and git's (always-physical) --show-toplevel answer compare unequal
        # for the identical directory otherwise — a path-normalization artifact, not a
        # real target mismatch.
        r = Path(td).resolve()
        _git(r, "init", "-q")
        (r / "naming.manifest.json").write_text(json.dumps(manifest))
        # authorkit's own nested naming.manifest.json (self-dogfooding, per its README) is
        # the exact fixture that falsified the manifest-walk approach: a write inside it,
        # in the PRIMARY checkout, with NO worktree involved at all, must still resolve to
        # authorkit/ as the plugin root — never authorkit/skills — proving find_repo_root's
        # git-based answer is immune to the nested-manifest false stop.
        (r / "authorkit").mkdir()
        (r / "authorkit" / "naming.manifest.json").write_text(json.dumps(manifest))
        (r / "authorkit" / "skills" / "demo-agent3").mkdir(parents=True)
        (r / "authorkit" / "skills" / "demo-agent3" / "SKILL.md").write_text(skill_md("demo-agent3"))
        _git(r, "add", "-A")
        _git(r, "commit", "-q", "-m", "seed")

        nested_write = r / "authorkit" / "skills" / "demo-agent3" / "SKILL.md"
        nested_target, nested_manifest = resolve_hook_target(str(nested_write))
        assert nested_target == r / "authorkit", (
            "a write inside authorkit's OWN nested-manifest tree must still resolve to "
            f"authorkit/ (not authorkit/skills) in the PRIMARY checkout: {nested_target}"
        )
        nested_hook = subprocess.run(
            [sys.executable, __file__, "hook"],
            input=json.dumps({"tool_input": {"file_path": str(nested_write)}}),
            capture_output=True, text=True,
        )
        assert nested_hook.returncode == 2, (
            "the nested-manifest false-stop must not silently swallow a real grammar "
            f"violation inside authorkit itself: {nested_hook.returncode} {nested_hook.stderr}"
        )

        # Now the worktree half of the fixture: a REAL `git worktree add`, whose own
        # top-level `git rev-parse --show-toplevel` reports is the WORKTREE path, never
        # the primary's — the exact mechanism this fix relies on. Branched off the commit
        # ABOVE (which carries no harness/ at all yet), so nothing under harness/ is shared
        # checked-out history between the two — the primary's own post-branch edit below is
        # genuinely invisible to the worktree, not just uncommitted-but-still-shared.
        wt = r / ".claude" / "worktrees" / "demo-wt"
        _git(r, "worktree", "add", "-q", "-b", "demo-wt-branch", str(wt))

        # A grammar violation added to the PRIMARY checkout's own working tree AFTER the
        # worktree branched off — present on disk at r/harness, never committed, and
        # invisible to the worktree's own working directory by construction (worktrees
        # share git history, never uncommitted files). If target resolution ever bled
        # into the primary root, this is what a worktree-write validation would wrongly
        # catch.
        (r / "harness" / "skills" / "demo-agent").mkdir(parents=True)
        (r / "harness" / "skills" / "demo-agent" / "SKILL.md").write_text(skill_md("demo-agent"))

        (wt / "harness" / "skills" / "demo-review").mkdir(parents=True)
        (wt / "harness" / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))

        clean_write = wt / "harness" / "skills" / "demo-review" / "SKILL.md"
        target, mpath = resolve_hook_target(str(clean_write))
        assert target == wt / "harness", \
            f"a write inside a worktree must resolve to THAT worktree's own plugin root, got {target}"
        assert mpath == wt / "naming.manifest.json", \
            f"a write inside a worktree must resolve to THAT worktree's own manifest, got {mpath}"

        clean_hook = subprocess.run(
            [sys.executable, __file__, "hook"],
            input=json.dumps({"tool_input": {"file_path": str(clean_write)}}),
            capture_output=True, text=True,
        )
        assert clean_hook.returncode == 0, (
            "a clean write inside a worktree must exit 0 even though the PRIMARY "
            f"checkout's own harness/ is grammar-broken (proves no primary bleed): "
            f"{clean_hook.returncode} {clean_hook.stderr}"
        )

        (wt / "harness" / "skills" / "demo-agent2").mkdir(parents=True)
        (wt / "harness" / "skills" / "demo-agent2" / "SKILL.md").write_text(skill_md("demo-agent2"))
        bad_write = wt / "harness" / "skills" / "demo-agent2" / "SKILL.md"
        bad_hook = subprocess.run(
            [sys.executable, __file__, "hook"],
            input=json.dumps({"tool_input": {"file_path": str(bad_write)}}),
            capture_output=True, text=True,
        )
        assert bad_hook.returncode == 2, \
            f"a genuinely bad write inside the SAME worktree must still be caught: {bad_hook.returncode}"
        assert "demo-agent2" in bad_hook.stderr, \
            f"the caught finding must name the offending artifact: {bad_hook.stderr}"

        _git(r, "worktree", "remove", "-f", str(wt))

    # CLI `--target` ancestor-manifest fallback (issue #842, 2026-08-21): a plugin two
    # directories below the git toplevel, with NO manifest of its own and NO --manifest
    # flag passed, must resolve GOVERNED via the toplevel manifest — not exit 2
    # "ungoverned". A real git repo (not a simulated tree), same rationale as the hook
    # fixture above: the fix's own claim is "git's toplevel is the resolution root".
    with tempfile.TemporaryDirectory() as td:
        r = Path(td).resolve()
        _git(r, "init", "-q")
        (r / "naming.manifest.json").write_text(json.dumps(manifest))
        # Two directories up from the target: r -> estate -> plugin-dir.
        plugin_dir = r / "estate" / "plugin-dir"
        (plugin_dir / "skills" / "demo-review").mkdir(parents=True)
        (plugin_dir / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        _git(r, "add", "-A")
        _git(r, "commit", "-q", "-m", "seed")

        governed = subprocess.run(
            [sys.executable, __file__, "--target", str(plugin_dir)],
            capture_output=True, text=True,
        )
        assert governed.returncode == 0, (
            "a plugin two dirs below a governed git toplevel, no --manifest flag, must "
            f"resolve GOVERNED (not ungoverned): {governed.returncode} {governed.stdout} "
            f"{governed.stderr}"
        )
        assert "ungoverned" not in governed.stdout, \
            f"a governed toplevel manifest must never read back as ungoverned: {governed.stdout}"

        # Regression control: an explicit --manifest flag still overrides every probe,
        # ancestor fallback included.
        explicit = subprocess.run(
            [sys.executable, __file__, "--target", str(plugin_dir),
             "--manifest", str(r / "naming.manifest.json")],
            capture_output=True, text=True,
        )
        assert explicit.returncode == 0, \
            f"--manifest must still override cleanly: {explicit.returncode} {explicit.stderr}"

    # Negative control: no manifest ANYWHERE (not at target, not at the git toplevel) —
    # the ancestor fallback must never manufacture governance that doesn't exist; still
    # exits 2 ungoverned, and the refusal names all three probes it tried.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td).resolve()
        _git(r, "init", "-q")
        plugin_dir = r / "estate" / "plugin-dir"
        (plugin_dir / "skills" / "demo-review").mkdir(parents=True)
        (plugin_dir / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        _git(r, "add", "-A")
        _git(r, "commit", "-q", "-m", "seed")

        ungoverned_cli = subprocess.run(
            [sys.executable, __file__, "--target", str(plugin_dir)],
            capture_output=True, text=True,
        )
        assert ungoverned_cli.returncode == 2, (
            "no manifest at target, target/.claude, or the git toplevel must still exit "
            f"2 ungoverned: {ungoverned_cli.returncode} {ungoverned_cli.stdout}"
        )
        assert "git toplevel" in ungoverned_cli.stdout, \
            f"the refusal must name the toplevel probe it tried: {ungoverned_cli.stdout}"

    # Fail-open controls: malformed event, a write with no naming.manifest.json at its
    # repo's own top-level, and a write outside any git repo at all — all three must
    # exit 0 silently, never raise (hook-writing-rules: a flaky governance hook is worse
    # than none).
    malformed = subprocess.run(
        [sys.executable, __file__, "hook"], input="not json", capture_output=True, text=True,
    )
    assert malformed.returncode == 0, f"a malformed hook event must fail open: {malformed.returncode}"

    # Valid-JSON-but-wrong-shape events (code-checker finding, 2026-08-15): each of these
    # three shapes crashed pre-guard with traceback + exit 1 — the exact fail-open breach
    # the guards close. All must exit 0 with EMPTY stderr (a traceback would still print).
    for shape_name, payload in (
        ("bare-list event", "[1, 2]"),
        ("non-dict tool_input", json.dumps({"tool_input": "oops"})),
        ("non-str file_path", json.dumps({"tool_input": {"file_path": 3}})),
    ):
        wrong_shape = subprocess.run(
            [sys.executable, __file__, "hook"], input=payload, capture_output=True, text=True,
        )
        assert wrong_shape.returncode == 0, \
            f"{shape_name} must fail open, got exit {wrong_shape.returncode}"
        assert "Traceback" not in wrong_shape.stderr, \
            f"{shape_name} must not print a traceback: {wrong_shape.stderr}"

    with tempfile.TemporaryDirectory() as td:
        orphan = Path(td) / "somewhere" / "file.md"
        orphan.parent.mkdir(parents=True)
        orphan.write_text("x")
        ungoverned = subprocess.run(
            [sys.executable, __file__, "hook"],
            input=json.dumps({"tool_input": {"file_path": str(orphan)}}),
            capture_output=True, text=True,
        )
        assert ungoverned.returncode == 0, \
            f"a write outside any git repo must fail open: {ungoverned.returncode}"

    # Wrong-SHAPE manifest, still valid JSON (issue #276 review, hook-checker): a bare
    # list at naming.manifest.json's top level parses clean but crashed uncaught deep
    # inside Grammar.__init__/run() before the isinstance(manifest, dict) guard + broad
    # except in main_hook_stdin were added — must now fail open, never exit 1 + traceback.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        _git(r, "init", "-q")
        (r / "naming.manifest.json").write_text(json.dumps(["not", "a", "dict"]))
        (r / "harness" / "skills" / "demo-review").mkdir(parents=True)
        (r / "harness" / "skills" / "demo-review" / "SKILL.md").write_text(skill_md("demo-review"))
        _git(r, "add", "-A")
        _git(r, "commit", "-q", "-m", "seed")
        wrong_shape_write = r / "harness" / "skills" / "demo-review" / "SKILL.md"
        wrong_shape_hook = subprocess.run(
            [sys.executable, __file__, "hook"],
            input=json.dumps({"tool_input": {"file_path": str(wrong_shape_write)}}),
            capture_output=True, text=True,
        )
        assert wrong_shape_hook.returncode == 0, (
            "a wrong-shape (but valid-JSON) manifest must fail open, never crash: "
            f"{wrong_shape_hook.returncode} {wrong_shape_hook.stderr}"
        )
        assert "Traceback" not in wrong_shape_hook.stderr, \
            f"a wrong-shape manifest must never surface a raw traceback: {wrong_shape_hook.stderr}"

    print("naming-audit validate selftest · PASS · schema/grammar/lexicon counters bite, "
          "--scope grammar/full partition proven, schema_scope manifest default + "
          "own-tree carve-out proven, reverse-wrapper skill-name amendment "
          "(positive/negative/regression) proven, ADR-0014 D1 -rules reserved-tail + D2 "
          "check- reserved-head productions (positive/negative/regression, plus a "
          "quantifier-non-goal and a dual-membership control) proven, author_registry "
          "shape validation "
          "(issue #252: structured entry fails clean, never a raw TypeError) proven, "
          "`hook` mode worktree-scoped target derivation (issue #276: resolves to the "
          "writing worktree's own root+plugin, not the primary checkout; catches a bad "
          "write there; fails open on malformed events, ungoverned trees, and a "
          "wrong-shape-but-valid-JSON manifest) proven, malformed-manifest robustness "
          "sweep (issue #296: wrong type per top-level field swept from "
          "MANIFEST-TEMPLATE.json's own schema, missing object_vocab key, duplicate "
          "object_vocab registration pinned last-wins-but-named, structured-vs-string "
          "object_vocab entries — each a named manifest_errors finding + clean exit-1, "
          "never a raw traceback, each with a regression control) proven, ADR-0015 D1/D2/D3 "
          "orchestrator agent production (bare {scope}-{role} against ObjectVocab and "
          "ProcessLex scopes, legacy {scope}-{role}-agent regression, a bare non-role "
          "agent-dir negative, a scope-role string minted as a skill negative, a "
          "RoleLex/ObjectVocab D3 disjointness manifest error) proven, ADR-0020 D3 "
          "bind-/fork-/sub- reserved verb-first heads (each head on skill + command "
          "branches, unregistered-scope negative per head, object-first regression, "
          "a lead-* mint rejected on both branches with no grandfather set left "
          "(#523: the six former lead-* surfaces renamed to bind-*, LEAD_HEAD_GRANDFATHER "
          "deleted outright), the six renamed bind-* surfaces parsing clean via the "
          "general reserved-head branch alone) "
          "proven")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    if sys.argv[1] == "hook":
        sys.exit(main_hook_stdin())
    main()
