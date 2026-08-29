#!/usr/bin/env python3
"""doc_lint — structural validation for functional documents (the docs plugin's check tier).

Usage:
  doc_lint.py <file.md> [...]      lint documents (files without `doc-type:` frontmatter are skipped)
  doc_lint.py --hook               hook mode: read {"tool_input":{"file_path":...}} from stdin;
                                   silent pass for non-documents; emits a block decision on findings
  doc_lint.py --spine [docs-root]  sweep docs-root (default: this repo's `.claude/docs`) for
                                   duplicate adr/idr/lld/rdd `id:` values (T10); FAIL on collision
  doc_lint.py selftest             prove the counters bite

Rules ("no validator, no type" — Vol 3 §3.1):
  T1 [FAIL] frontmatter parses and carries doc-type, id, status
  T2 [FAIL] doc-type is one of the ten; status is in that type's enum
  T3 [FAIL] required sections for the type present as `## ` headings
  T4 [FAIL] ledger protection (hook mode): editing a file whose COMMITTED (HEAD) version is a
            locked ledger entry — an accepted ADR, a locked IDR, or a locked RDD — supersede,
            never edit. Refined 2026-07-15 (ADR): a new/untracked ADR, or one still `proposed` in
            HEAD, may be authored and ratified (the proposed->accepted flip is the ratification
            act, not a forgery); the append-only guarantee protects history. Generalized
            2026-08-16 (IDR, #316; RDD, #332) to a ledger-lock guard covering
            `doc-type: adr, status: accepted`, `doc-type: idr, status: locked`, and
            `doc-type: rdd, status: locked` — the same two-phase mechanic, reused verbatim per
            LEDGER_LOCK below. git absent / not a repo / any doubt -> conservative block, as before.
            Narrowly carved 2026-08-28 (ADR-0027, issue #978): a committed-accepted ADR may still
            receive exactly one edit — `intent-refs:` moving from empty/`null` to a non-empty
            citation, verified as the SOLE line-level delta against HEAD by `is_intent_refs_backfill()`
            — everything else (a second intent-refs edit, any other field, Context/Decision/
            Consequences) still FAILs. ADR-only; IDR/RDD carry no carve-out.
  T5 [WARN] plan steps without a done-when token; spec Requirements without REQ- IDs
  T6 [WARN] an ADR with no `intent-refs:` citation — an "orphan ADR" per the corpus's
            product-lifecycle-bible (Part 4): a HOW decision with no cited upstream IDR claim.
            Added 2026-08-16 (#316) alongside the `idr` type; existing ADRs 0001-0013 predate
            `intent-refs:` and are EXPECTED to warn here — the retrofit is its own deferred
            follow-up (PRD Implementation surface item 7), not required for this check to ship.
  T7 [FAIL] a `locked`-or-`superseded` RDD with an empty/missing `decision-refs:` OR an
            empty/missing `dri:` — a release commitment locked with no upward citation or no
            named accountable human. Added 2026-08-16 (#332, `prd-rdd-framework.md`) alongside
            the `rdd` type; `draft` RDDs are exempt on both fields (the harvest window — citations
            and DRI assignment may genuinely not be settled yet). Deliberately stricter than T6
            (FAIL, not WARN): RDD has zero existing instances, so there is no retrofit debt to
            excuse a soft landing. `decision-refs:` is a single-line comma/space-separated scalar
            (`parse_frontmatter` cannot read a YAML block list) — never a list.
  T8 [FAIL] an IDR with a missing/empty `provenance:` frontmatter key, or a value outside
            {derived-from-evidence, inferred, decided-by-human} — machine-readable provenance for
            every claim, one of the same three labels the `## Why` prose already states in prose
            for idr-0001..0006 (#431, ratification round). IDR-only for now (no retrofit debt on
            other types); FAIL, not WARN — IDR has a small, fully-authored instance set, so there
            is no soft-landing case to make.
  T9 [WARN] a SPEC with no `## Agent verification` section — the agent-testability doctrine
            (#542, `prd-agent-testability.md`): every SPEC states how a coding agent autonomously
            verifies the built system, not a human in the loop. Added 2026-08-17 as WARN, not
            FAIL, on the T6 orphan-ADR precedent — 3 live draft SPECs (spec-naming-convention,
            spec-linear-adapter, spec-ticketing-watch-triage) predate the section and are
            EXPECTED to warn here; the retrofit is its own deferred follow-up, not required for
            this check to ship. SPEC-only for now — PRD/LLD carry the same template section but
            check-doc's J7 judgment criterion covers them instead of a doc_lint presence rule
            (the PRD's own D3: SPEC gets the mechanical rule, PRD/LLD stay judgment-only).
  T11 [FAIL] an IDR whose `## Claim` names a feature/component/screen/endpoint grain — IDR is
            whole-app/product-thesis scope only (ruled #652, Kim's verbatim scope statement:
            "IDR = whole-app scope only; PRD = valid at app AND feature scope"); a feature- or
            component-grain hypothesis is PRD/SPEC territory, not an IDR. Heuristic, not a parser:
            a bare `\bfeature(s)?\b`/`component(s)?\b`/`screen(s)?\b`/`endpoint(s)?\b` word-boundary
            match inside the Claim section's PROSE (inline-code spans and fenced blocks are
            stripped first, so a skill-name mention like `` `file-feature` `` never false-positives
            — the #652 investigation's own idr-0008 near-miss). FAIL, not WARN: the existing corpus
            (idr-0001..0011) passes clean, so there is no retrofit debt to excuse a soft landing,
            same posture as T7/T8's own FAIL tier for a small, fully-authored IDR instance set.
  T12 [FAIL] `scope:` frontmatter grain, new-mints-only (#657, ratified 2026-08-18, decision 1):
            eight types (BRIEF/IDR/ROADMAP=app · PRD/RDD=app+feature · SPEC/LLD=feature/component ·
            ADR=decision-scoped, any grain) carry a fixed grain — a NEW mint (no committed HEAD
            version) with a missing/empty `scope:` FAILs; ANY document (new or grandfathered)
            whose present `scope:` value is out of vocabulary or out of its type's ratified grain
            also FAILs — grandfather waives presence, never correctness. TICKET/TASK/PLAN are
            deliberately not grain-governed (work-item/living-state trackers, not decision/
            knowledge documents) and carry no `scope:` requirement here.
  T13 [FAIL] `audience:` frontmatter, new-mints-only, ALL types (#657, ratified 2026-08-18,
            decision 4): a NEW mint with a missing/empty `audience:` FAILs — one-or-more of
            {human, product-seat, planner, builder, reviewer, any-agent}, comma/space-separated
            on one line (`parse_frontmatter` is a scalar parser, same convention as RDD's
            `decision-refs:`). No any-agent default: an absent value is never silently read as
            any-agent. Grandfather + ratchet (ADR-0011 D8 precedent): the existing corpus is
            exempt from PRESENCE on this field; a present value — new or grandfathered — is still
            validated against the vocabulary. `is_new_mint()` realizes both T12's and T13's
            new-mint test: the same git-HEAD-aware shape as T4's `head_is_locked_ledger()`,
            inverted (untracked/new -> enforce presence; already committed -> exempt).
  T10 [FAIL] `--spine` mode only: two adr/idr/lld/rdd documents under the doc spine claim the
            same (family, number) — the 2026-08-18 incident (#633): two parallel builds both
            minted `lld-0011` (one kept it, `lld-0011-recurrence-audit`; the other's draft was
            renumbered before merge, caught only by a coordinator's manual pre-merge read, not by
            any gate — nothing existed to catch it mechanically). Keyed on (family, number), not
            the full `id:` string — two colliding drafts plausibly differ only in their
            descriptive slug, so an exact-string dedup would let the real incident straight
            through. Reaches release_gate.py's G10 through `harness/scripts/docs_check.py`'s own
            self-contained R7 (a duplicate, not an import, per the hard plugin-boundary rule —
            see that script's own comment) rather than a new G-check; this CLI mode is the
            dev-time/standalone entry point, same relationship T1-T9 have to `check-doc`'s
            mechanical pass. The companion dispatch-rule half (re-read the spine's highest id off
            `origin/main` immediately before numbering) lives in `doc-writing-rules` and
            `teamwork:dispatch-ticket`, not here — this check only ever catches a miss after the
            fact.
"""
import json
import re
import sys
from pathlib import Path

TYPES = {
    "adr":     {"status": {"proposed", "accepted", "superseded"}, "sections": ["Context", "Decision", "Consequences"]},
    "prd":     {"status": {"draft", "approved", "superseded"},    "sections": ["Problem", "Users", "Outcomes", "Non-goals"]},
    "spec":    {"status": {"draft", "approved", "superseded"},    "sections": ["Requirements", "Non-goals", "Examples", "Acceptance"]},
    "lld":     {"status": {"draft", "approved", "superseded"},    "sections": ["Components", "Interfaces", "Data", "Risks"]},
    "plan":    {"status": {"active", "complete", "abandoned"},    "sections": ["Steps", "Validation", "Rollback"]},
    "roadmap": {"status": {"active", "retired"},                  "sections": ["Now", "Next", "Later"]},
    "brief":   {"status": {"active", "retired"},                  "sections": ["Thesis", "Confirmed", "Open Questions"]},
    "ticket":  {"status": {"open", "doing", "done", "wontfix"},   "sections": ["Summary", "Acceptance", "Links"]},
    "task":    {"status": {"todo", "doing", "done"},              "sections": ["Goal", "Done-when"]},
    "idr":     {"status": {"draft", "locked", "superseded"},      "sections": ["Claim", "Why", "Proof"]},
    "rdd":     {"status": {"draft", "locked", "superseded"},      "sections": ["Scope", "Acceptance", "Sequencing", "Completion"]},
}

# T4's ledger-lock scope, keyed by doc-type -> the status value that means "committed and locked".
# ADR's `accepted` and IDR's `locked` are the same mechanic (ADR-0013's proven two-phase
# proposed/draft -> ratified flip); adding a doc-type here is the whole extension, no new code path.
# RDD's `locked` reuses the identical mechanic verbatim (#332) — the primary Mutability design
# from `prd-rdd-framework.md`: `shipped-and-archived` tracks on the `roadmap`'s own living index,
# never a fourth status enum value here, so no new guard logic is owed.
LEDGER_LOCK = {
    "adr": "accepted",
    "idr": "locked",
    "rdd": "locked",
}

# T7's scope: RDD statuses at or beyond `locked` that must carry both a citation and a DRI.
RDD_CITED_STATUSES = {"locked", "superseded"}

# T8's scope: the vocabulary a `provenance:` key on an IDR must take.
PROVENANCE_VALUES = {"derived-from-evidence", "inferred", "decided-by-human"}

# T10's scope: the four ledger families the doc spine numbers, and the (family, number) pattern
# their `id:` frontmatter values carry (`lld-0011-recurrence-audit` -> ("lld", "0011")).
SPINE_FAMILIES = {"adr", "idr", "lld", "rdd"}
SPINE_ID_RE = re.compile(r"^(adr|idr|lld|rdd)-(\d+)\b")

# T11's scope: the feature/component/screen/endpoint grain nouns an IDR's `## Claim` must never
# name (#652) — IDR is whole-app/product-thesis scope only.
IDR_SCOPE_GRAIN_RE = re.compile(r"\b(feature|features|component|components|screen|screens|endpoint|endpoints)\b", re.I)

# T12's scope: which types carry a `scope:` frontmatter field validated against a fixed grain, and
# what grain(s) each permits (#657, ratified 2026-08-18, grain table decision 1). TICKET/TASK/PLAN
# are deliberately absent — the ratified grain table names only the decision/knowledge-bearing
# eight; a work-item/living-state tracker's own `scope:` isn't grain-validated by this check.
SCOPE_GRAIN = {
    "brief":    {"app"},
    "idr":      {"app"},
    "roadmap":  {"app"},
    "prd":      {"app", "feature"},
    "rdd":      {"app", "feature"},
    "spec":     {"feature", "component"},
    "lld":      {"feature", "component"},
    "adr":      {"app", "feature", "component"},  # decision-scoped: any grain
}
SCOPE_VALUES = {"app", "feature", "component"}

# T13's scope: the audience seat-class vocabulary every NEW document mint must declare (#657,
# ratified 2026-08-18, decision 4) — one-or-more, comma/space-separated (parse_frontmatter is a
# scalar parser, no YAML block lists — same convention as RDD's `decision-refs:`).
AUDIENCE_VALUES = {"human", "product-seat", "planner", "builder", "reviewer", "any-agent"}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = {}
    for line in parts[1].splitlines():
        m = re.match(r"^([\w-]+):\s*(.*?)(\s+#.*)?$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def strip_code_spans(text):
    """T11's own noise filter: drop fenced code blocks and inline `code spans` before a keyword
    match, so a skill/command mention (`` `file-feature` ``) inside a Claim's prose never trips
    the scope heuristic — the #652 investigation's own idr-0008 near-miss."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def extract_section(text, name):
    """The `## <name>` section's body text, up to the next `## ` heading or EOF; "" if absent."""
    m = re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    m2 = re.search(r"^##\s+", rest, re.M)
    return rest[:m2.start()] if m2 else rest


def lint_text(text, new_mint=True):
    """`new_mint` (default True — safe for a text-only caller with no git context, e.g. selftest's
    synthetic fixtures) gates T12/T13's PRESENCE requirement only; a present scope:/audience:
    value is validated against its vocabulary/grain regardless of new_mint. A real file caller
    (hook_mode, the CLI file path) computes new_mint via `is_new_mint(path)` instead of trusting
    the default."""
    fm = parse_frontmatter(text)
    if fm is None or "doc-type" not in fm:
        return None  # not a functional document; not ours to judge
    findings = []
    dtype = fm.get("doc-type", "")
    spec = TYPES.get(dtype)
    if spec is None:
        return [("FAIL", "T2", f"doc-type `{dtype}` is not one of {sorted(TYPES)}")]
    for field in ("id", "status"):
        if not fm.get(field):
            findings.append(("FAIL", "T1", f"frontmatter missing `{field}` -> code cannot read this document's state"))
    status = fm.get("status", "")
    if status and status not in spec["status"]:
        findings.append(("FAIL", "T2", f"status `{status}` -> {dtype} takes {sorted(spec['status'])}"))
    heads = set(re.findall(r"^##\s+(.+?)\s*$", text, re.M))
    for sec in spec["sections"]:
        if sec not in heads:
            findings.append(("FAIL", "T3", f"required section `## {sec}` missing -> the template is the contract"))
    if dtype == "plan" and "Steps" in heads and "done-when" not in text.lower():
        findings.append(("WARN", "T5", "no `done-when` found in the plan -> steps without one are guesses"))
    if dtype == "spec" and "Requirements" in heads and not re.search(r"\bREQ-([A-Z]+-)?\d+", text):
        findings.append(("WARN", "T5", "no REQ- IDs in the spec -> the ID spine starts here"))
    if dtype == "spec" and "Agent verification" not in heads:
        findings.append(("WARN", "T9", "no `## Agent verification` section -> the spec doesn't say "
                                        "how a coding agent autonomously verifies the built system"))
    if dtype == "adr":
        intent_refs = fm.get("intent-refs", "").strip().lower()
        if intent_refs in ("", "null", "none", "[]"):
            findings.append(("WARN", "T6", "no `intent-refs:` citation -> an ADR with no upstream "
                                            "IDR is an orphan (bible: 'an ADR with no IDR citation is an orphan')"))
    if dtype == "rdd" and status in RDD_CITED_STATUSES:
        decision_refs = fm.get("decision-refs", "").strip().lower()
        if decision_refs in ("", "null", "none", "[]"):
            findings.append(("FAIL", "T7", "no `decision-refs:` citation -> a locked-or-beyond RDD "
                                            "with no upward ADR/IDR citation is a release commitment "
                                            "with zero traceability"))
        dri = fm.get("dri", "").strip().lower()
        if dri in ("", "null", "none", "[]"):
            findings.append(("FAIL", "T7", "no `dri:` -> a locked-or-beyond RDD needs a named "
                                            "accountable human, mechanically, not just a Problem-statement claim"))
    if dtype == "idr":
        provenance = fm.get("provenance", "").strip()
        if provenance not in PROVENANCE_VALUES:
            findings.append(("FAIL", "T8", f"`provenance:` missing or not one of {sorted(PROVENANCE_VALUES)} "
                                            "-> every IDR claim needs a machine-readable source label, "
                                            "not just prose in `## Why`"))
        claim_prose = strip_code_spans(extract_section(text, "Claim"))
        grain = IDR_SCOPE_GRAIN_RE.search(claim_prose)
        if grain:
            findings.append(("FAIL", "T11", f"Claim names a `{grain.group(1)}`-grain hypothesis -> "
                                             "IDR is whole-app/product-thesis scope only; a feature- "
                                             "or component-grain claim is PRD/SPEC territory (#652)"))
    if dtype in SCOPE_GRAIN:
        scope = fm.get("scope", "").strip().lower()
        if not scope:
            if new_mint:
                findings.append(("FAIL", "T12", f"`scope:` missing -> every new {dtype} mint must "
                                                  f"declare its grain, one of {sorted(SCOPE_GRAIN[dtype])} "
                                                  "(#657, ratified grain table)"))
        elif scope not in SCOPE_VALUES:
            findings.append(("FAIL", "T12", f"`scope: {scope}` is not one of {sorted(SCOPE_VALUES)}"))
        elif scope not in SCOPE_GRAIN[dtype]:
            findings.append(("FAIL", "T12", f"`scope: {scope}` is out of {dtype}'s ratified grain "
                                              f"{sorted(SCOPE_GRAIN[dtype])} (#657 grain table)"))
    audience_tokens = [t.strip().lower() for t in re.split(r"[,\s]+", fm.get("audience", "")) if t.strip()]
    if not audience_tokens:
        if new_mint:
            findings.append(("FAIL", "T13", "`audience:` missing -> every new mint must declare an "
                                              f"explicit seat-class audience, one-or-more of "
                                              f"{sorted(AUDIENCE_VALUES)} (#657 — no any-agent default)"))
    else:
        bad_audience = [t for t in audience_tokens if t not in AUDIENCE_VALUES]
        if bad_audience:
            findings.append(("FAIL", "T13", f"`audience:` token(s) {bad_audience} not in {sorted(AUDIENCE_VALUES)}"))
    return findings


def check_spine(docs_root: Path):
    """T10: sweep docs_root for two adr/idr/lld/rdd documents claiming the same (family, number).
    Keyed on the (family, number) pair, never the full `id:` string (see module docstring, T10).
    Returns [] when docs_root doesn't exist -- a repo that hasn't adopted the `.claude/docs`
    spine yet is not a failure, same posture as T5's/T9's own conditional triggers."""
    if not docs_root.is_dir():
        return []
    seen = {}
    findings = []
    for p in sorted(docs_root.rglob("*.md")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if not fm or fm.get("doc-type") not in SPINE_FAMILIES:
            continue
        doc_id = fm.get("id", "")
        m = SPINE_ID_RE.match(doc_id)
        if not m:
            continue  # T1/T2 already own a missing/malformed id on the file itself
        key = (m.group(1), m.group(2))
        if key in seen:
            prev_path, prev_id = seen[key]
            findings.append(("FAIL", "T10",
                              f"id collision: {p} (`{doc_id}`) and {prev_path} (`{prev_id}`) both "
                              f"claim {key[0]}-{key[1]} -> re-read the spine's highest id off "
                              f"origin/main before numbering (dispatch-ticket's own discipline)"))
        else:
            seen[key] = (p, doc_id)
    return findings


def render(path, findings):
    if findings is None:
        print(f"doc_lint · not a functional document · {path}")
        return 0
    verdict = "FAIL" if any(f[0] == "FAIL" for f in findings) else ("warn" if findings else "clean")
    print(f"doc_lint · {verdict} · {path}")
    for sev, code, msg in findings:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if verdict == "FAIL" else 0


def is_new_mint(p: Path) -> bool:
    """T12/T13's own grandfather+ratchet test (#657, ADR-0011 D8 precedent): True (a NEW mint,
    enforce scope:/audience: presence) when this path has no committed HEAD version; False
    (already part of the committed corpus — grandfathered, presence not enforced) when it does.
    Same git-HEAD-aware shape as `head_is_locked_ledger` above, inverted: there, untracked/new is
    the ALLOWED case; here, untracked/new is the ENFORCED case. git absent / not a repo / any
    doubt -> conservative True (still enforce) — mirrors that function's own posture of erring
    toward the stricter branch on ambiguity, not silently exempting it."""
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, cwd=p.parent, timeout=10)
        if r.returncode != 0:
            return True
        top = Path(r.stdout.strip())
        rel = p.resolve().relative_to(top.resolve())
        r = subprocess.run(["git", "show", f"HEAD:{rel.as_posix()}"], capture_output=True,
                           text=True, cwd=top, timeout=10)
        return r.returncode != 0  # no HEAD version -> new mint
    except Exception:
        return True


def head_is_locked_ledger(p: Path) -> bool:
    """T4's scope test (refined 2026-07-15 for ADR; generalized 2026-08-16, #316, for IDR; #332,
    for RDD): the ledger protection guards COMMITTED history. True (block) when the file's HEAD
    version is a locked ledger entry per LEDGER_LOCK (an accepted ADR, a locked IDR, or a locked
    RDD); False (allow) when the file is new/untracked or still pre-lock (`proposed`/`draft`) in
    HEAD — authoring and the lock-flip ratification are legal acts on an uncommitted ledger entry.
    git absent, not a repo, or any failure -> True (conservative block, unchanged from the
    ADR-only version)."""
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, cwd=p.parent, timeout=10)
        if r.returncode != 0:
            return True
        top = Path(r.stdout.strip())
        rel = p.resolve().relative_to(top.resolve())
        r = subprocess.run(["git", "show", f"HEAD:{rel.as_posix()}"], capture_output=True,
                           text=True, cwd=top, timeout=10)
        if r.returncode != 0:
            return False  # not in HEAD: a new ledger entry, not history
        head_fm = parse_frontmatter(r.stdout)
        if not head_fm:
            return False
        locked_status = LEDGER_LOCK.get(head_fm.get("doc-type"))
        return bool(locked_status and head_fm.get("status") == locked_status)
    except Exception:
        return True


def is_intent_refs_backfill(p: Path, new_text: str) -> bool:
    """ADR-0027's narrow T4 carve-out (2026-08-28): an already-committed, `status: accepted` ADR
    may receive exactly one class of edit — `intent-refs:` moving from empty/`null`/absent to a
    non-empty citation — verified structurally, not by trust. The BODY (everything after the
    frontmatter's closing `---`, i.e. Context/Decision/Consequences and beyond) must be
    byte-identical to HEAD. Within the frontmatter block, exactly one of two shapes is allowed:
    (a) an existing `intent-refs:` line's value moves from empty/`null` to non-empty at the same
    position (adr-0014..adr-0025's bucket: the field existed, shipped null); or (b) a brand-new
    `intent-refs: <value>` line is inserted with every other frontmatter line unchanged and in
    the same relative order (adr-0001..adr-0013's bucket: they predate the field's existence —
    T6 already treats a missing key identically to an empty one via `fm.get("intent-refs", "")`,
    so a first-time insertion is the same backfill, not a new class of edit). Any other delta —
    a second edit to an already-populated `intent-refs:`, a body change, a reordered or altered
    frontmatter line elsewhere — returns False (T4 still FAILs, exactly as before this carve-out
    existed). ADR-scoped only: IDR/RDD ledger-lock entries don't carry `intent-refs:` and get no
    carve-out here."""
    import re
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, cwd=p.parent, timeout=10)
        if r.returncode != 0:
            return False
        top = Path(r.stdout.strip())
        rel = p.resolve().relative_to(top.resolve())
        r = subprocess.run(["git", "show", f"HEAD:{rel.as_posix()}"], capture_output=True,
                           text=True, cwd=top, timeout=10)
        if r.returncode != 0:
            return False
        head_text = r.stdout
    except Exception:
        return False
    head_fm = parse_frontmatter(head_text)
    if not head_fm or head_fm.get("doc-type") != "adr":
        return False
    head_parts = head_text.split("---", 2)
    new_parts = new_text.split("---", 2)
    if len(head_parts) < 3 or len(new_parts) < 3:
        return False
    if head_parts[0] != new_parts[0] or head_parts[2] != new_parts[2]:
        return False  # anything outside the frontmatter block changed -> not this carve-out
    head_fm_lines = head_parts[1].splitlines()
    new_fm_lines = new_parts[1].splitlines()
    key_re = re.compile(r"^intent-refs\s*:\s*(.*)$")

    def strip_val(raw):
        return raw.split("#", 1)[0].strip().strip('"\'')

    if len(head_fm_lines) == len(new_fm_lines):
        diffs = [i for i in range(len(head_fm_lines)) if head_fm_lines[i] != new_fm_lines[i]]
        if len(diffs) != 1:
            return False
        old_m = key_re.match(head_fm_lines[diffs[0]])
        if not old_m:
            return False
        old_val = strip_val(old_m.group(1)).lower()
        new_line = new_fm_lines[diffs[0]]
    elif len(new_fm_lines) == len(head_fm_lines) + 1:
        n = len(head_fm_lines)
        pre = 0
        while pre < n and head_fm_lines[pre] == new_fm_lines[pre]:
            pre += 1
        suf = 0
        while suf < n - pre and head_fm_lines[n - 1 - suf] == new_fm_lines[len(new_fm_lines) - 1 - suf]:
            suf += 1
        if pre + suf != n:
            return False  # more than a single-line insertion happened
        old_val = ""  # the key was absent in HEAD -> T6 already treats this as empty
        new_line = new_fm_lines[pre]
    else:
        return False
    new_m = key_re.match(new_line)
    if not new_m:
        return False
    new_val = strip_val(new_m.group(1))
    if old_val not in ("", "null", "none"):
        return False
    return bool(new_val) and new_val.lower() not in ("null", "none")


def hook_mode():
    try:
        payload = json.load(sys.stdin)
        fpath = payload.get("tool_input", {}).get("file_path", "")
    except (ValueError, AttributeError):
        return 0
    p = Path(fpath)
    if p.suffix != ".md" or not p.is_file():
        return 0
    text = p.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    if fm is None or "doc-type" not in fm:
        return 0
    findings = lint_text(text, new_mint=is_new_mint(p)) or []
    dtype = fm.get("doc-type")
    locked_status = LEDGER_LOCK.get(dtype)
    if (locked_status and fm.get("status") == locked_status and head_is_locked_ledger(p)
            and not is_intent_refs_backfill(p, text)):
        findings.append(("FAIL", "T4", f"this {dtype.upper()} is {locked_status} in committed history — the ledger is append-only; "
                                       f"revert this edit and write a new {dtype.upper()} with `supersedes: " + fm.get("id", f"{dtype}-????") + "`"))
    fails = [f for f in findings if f[0] == "FAIL"]
    if fails:
        print(json.dumps({"decision": "block",
                          "reason": "doc_lint: " + " | ".join(f"{c} {m}" for _, c, m in fails)}))
    return 0


def selftest():
    tpl_dir = Path(__file__).resolve().parent.parent / "skills" / "doc-writing-rules" / "references" / "templates"
    for tpl in sorted(tpl_dir.glob("*.md")):
        text = tpl.read_text().replace("YYYY-MM-DD", "2026-07-07")
        fs = [f for f in (lint_text(text) or []) if f[0] == "FAIL"]
        assert not fs, f"template {tpl.name} must lint clean against its own contract, got {fs}"
    assert lint_text("# just a readme\nprose\n") is None, "non-documents are not ours to judge"
    bad = "---\ndoc-type: spec\nid: spec-x\nstatus: shipped\n---\n# S\n\n## Requirements\ntext\n"
    codes = {f[1] for f in lint_text(bad)}
    assert {"T2", "T3"} <= codes, f"bad status + missing sections must fail, got {codes}"
    # T6 orphan-ADR WARN (#316): no intent-refs -> warn; cited intent-refs -> silent
    orphan_adr = ("---\ndoc-type: adr\nid: adr-0099\nstatus: proposed\ndate: 2026-08-16\n"
                  "intent-refs: null\n---\n# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
    assert any(f[1] == "T6" for f in lint_text(orphan_adr)), "ADR with no intent-refs must WARN T6 (orphan)"
    cited_adr = orphan_adr.replace("intent-refs: null", "intent-refs: idr-0001")
    assert not any(f[1] == "T6" for f in lint_text(cited_adr)), "ADR citing an IDR must NOT warn T6"
    assert any(f[1] == "T5" for f in lint_text(bad.replace("status: shipped", "status: draft"))), "REQ-less spec must warn T5"
    # T5 REQ-<INFIX>- prefixed IDs (#634, operator-ruled 2026-08-18, gen-ui-kit#1625/#1627):
    # per-doc pools distinguished by an uppercase infix (REQ-P-001, REQ-R-001) must NOT warn;
    # a lowercase infix is a negative control and must still warn.
    spec_req_infix = ("---\ndoc-type: spec\nid: spec-x\nstatus: draft\n---\n# S\n"
                       "## Requirements\nREQ-P-001: x\n## Non-goals\nn\n## Examples\ne\n## Acceptance\na\n"
                       "## Agent verification\nv\n")
    assert not any(f[1] == "T5" for f in lint_text(spec_req_infix)), "REQ-<INFIX>- (uppercase) must NOT warn T5"
    spec_req_lowercase_infix = spec_req_infix.replace("REQ-P-001", "REQ-p-001")
    assert any(f[1] == "T5" for f in lint_text(spec_req_lowercase_infix)), "REQ- with a lowercase infix must still warn T5 (negative control)"
    # T9 SPEC agent-verification WARN (#542): no `## Agent verification` -> warn; section present -> silent.
    spec_no_av = ("---\ndoc-type: spec\nid: spec-x\nstatus: draft\n---\n# S\n"
                  "## Requirements\nREQ-1: x\n## Non-goals\nn\n## Examples\ne\n## Acceptance\na\n")
    assert any(f[1] == "T9" for f in lint_text(spec_no_av)), "SPEC with no Agent verification section must WARN T9"
    spec_with_av = spec_no_av + "## Agent verification\nv\n"
    assert not any(f[1] == "T9" for f in lint_text(spec_with_av)), "SPEC with Agent verification section must NOT warn T9"
    # T7 RDD citation+DRI-presence FAIL (#332): locked-or-beyond with empty refs/dri FAILs;
    # draft is exempt on both; locked with both present is clean.
    rdd_base = ("---\ndoc-type: rdd\nid: rdd-0099\nstatus: {s}\ndate: 2026-08-16\nowner: k\n"
                "dri: {dri}\ndecision-refs: {refs}\nsupersedes: null\n---\n# R\n"
                "## Scope\ns\n## Acceptance\na\n## Sequencing\nq\n## Completion\nc\n")
    locked_empty_refs = rdd_base.format(s="locked", dri="kim", refs="")
    assert any(f[1] == "T7" for f in lint_text(locked_empty_refs)), "locked RDD with empty decision-refs must FAIL T7"
    locked_empty_dri = rdd_base.format(s="locked", dri="", refs="adr-0002")
    assert any(f[1] == "T7" for f in lint_text(locked_empty_dri)), "locked RDD with empty dri must FAIL T7"
    locked_clean = rdd_base.format(s="locked", dri="kim", refs="adr-0002, idr-0001")
    assert not any(f[1] == "T7" for f in lint_text(locked_clean)), "locked RDD with refs+dri must NOT FAIL T7"
    draft_empty = rdd_base.format(s="draft", dri="", refs="")
    assert not any(f[1] == "T7" for f in lint_text(draft_empty)), "draft RDD is exempt from T7 on both fields"
    # T8 IDR provenance FAIL (#431): missing/empty/bad-value provenance FAILs; a valid value is clean.
    idr_prov_base = ("---\ndoc-type: idr\nid: idr-0099\nstatus: draft\ndate: 2026-08-16\n"
                      "owner: k\nproof-ref: n/a\n{prov}supersedes: null\n---\n"
                      "# I\n## Claim\nc\n## Why\nw\n## Proof\np\n")
    missing_prov = idr_prov_base.format(prov="")
    assert any(f[1] == "T8" for f in lint_text(missing_prov)), "IDR with no provenance must FAIL T8"
    bad_prov = idr_prov_base.format(prov="provenance: made-up\n")
    assert any(f[1] == "T8" for f in lint_text(bad_prov)), "IDR with an out-of-vocab provenance must FAIL T8"
    good_prov = idr_prov_base.format(prov="provenance: decided-by-human\n")
    assert not any(f[1] == "T8" for f in lint_text(good_prov)), "IDR with a valid provenance must NOT FAIL T8"
    nofm = lint_text("---\ndoc-type: adr\n---\n# A\n## Context\n## Decision\n## Consequences\n")
    assert any(f[1] == "T1" for f in nofm), "missing id/status must fail T1"
    # T4 git-aware scope (2026-07-15, ADR; generalized 2026-08-16, #316, IDR): committed-locked
    # blocks; new/ratifying doesn't. Same temp repo, two independent ledger files -> proves the
    # generalized guard still handles ADR (regression) and now also handles IDR (new).
    import shutil
    if shutil.which("git"):
        import subprocess
        import tempfile
        adr = ("---\ndoc-type: adr\nid: adr-0001\nstatus: {s}\ndate: 2026-07-15\n---\n"
               "# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
        idr = ("---\ndoc-type: idr\nid: idr-0001\nstatus: {s}\ndate: 2026-08-16\nproof-ref: n/a\n"
               "provenance: decided-by-human\nsupersedes: null\n---\n# I\n## Claim\nc\n## Why\nw\n## Proof\np\n")
        rdd = ("---\ndoc-type: rdd\nid: rdd-0001\nstatus: {s}\ndate: 2026-08-16\nowner: k\n"
               "dri: k\ndecision-refs: adr-0002\nsupersedes: null\n---\n# R\n"
               "## Scope\ns\n## Acceptance\na\n## Sequencing\nq\n## Completion\nc\n")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            env_git = lambda *a: subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True,
                                                env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                                     "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                                                     "PATH": __import__("os").environ["PATH"], "HOME": td})
            env_git("init", "-q")
            # --- ADR regression: the pre-existing fixture pair, unaffected by the generalization ---
            f = repo / "0001-x.md"
            f.write_text(adr.format(s="accepted"))
            assert not head_is_locked_ledger(f), "untracked new accepted ADR must be ALLOWED (authoring, not forgery)"
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "adr proposed")
            assert head_is_locked_ledger(f), "committed-accepted ADR must BLOCK edits (the ledger) — regression"
            f.write_text(adr.format(s="proposed"))
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "as proposed")
            assert not head_is_locked_ledger(f), "HEAD-proposed ADR must allow the ratification flip — regression"
            # --- ADR-0027 carve-out (#978): intent-refs backfill positive + negative controls ---
            adr_ir = ("---\ndoc-type: adr\nid: adr-0002\nstatus: accepted\ndate: 2026-07-15\n"
                      "intent-refs: null\n---\n# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
            h = repo / "0002-x.md"
            h.write_text(adr_ir)
            env_git("add", "0002-x.md"); env_git("commit", "-qm", "adr with null intent-refs, accepted")
            backfilled = adr_ir.replace("intent-refs: null", "intent-refs: idr-0002")
            assert is_intent_refs_backfill(h, backfilled), \
                "intent-refs null->cited, sole delta, must be ALLOWED past T4 (ADR-0027)"
            other_field_touched = backfilled.replace("## Context\nc\n", "## Context\nc changed\n")
            assert not is_intent_refs_backfill(h, other_field_touched), \
                "intent-refs backfill PLUS any other line delta must still FAIL T4 (not byte-identical elsewhere)"
            assert not is_intent_refs_backfill(h, adr_ir), \
                "no delta at all is not a backfill -> False (nothing to carve an exception for)"
            # commit the backfill (simulates the carve-out already exercised once) -> a SECOND
            # edit to the now-populated intent-refs must still FAIL: the carve-out is one-time.
            h.write_text(backfilled)
            env_git("add", "0002-x.md"); env_git("commit", "-qm", "intent-refs backfilled")
            second_edit = backfilled.replace("intent-refs: idr-0002", "intent-refs: idr-0003")
            assert not is_intent_refs_backfill(h, second_edit), \
                "editing an ALREADY-populated intent-refs is a second edit, not the one-time backfill -> still FAIL"
            # --- ADR-0027 carve-out, bucket-A shape (#978): adr-0001..0013 predate the field
            # entirely -> the backfill INSERTS a new intent-refs line rather than editing one.
            adr_no_field = ("---\ndoc-type: adr\nid: adr-0001\nstatus: accepted\ndate: 2026-07-09\n"
                            "---\n# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
            k = repo / "0001-nofield.md"
            k.write_text(adr_no_field)
            env_git("add", "0001-nofield.md"); env_git("commit", "-qm", "adr, no intent-refs field at all")
            inserted = adr_no_field.replace("date: 2026-07-09\n---",
                                            "date: 2026-07-09\nintent-refs: idr-0003\n---")
            assert is_intent_refs_backfill(k, inserted), \
                "first-time intent-refs insertion (bucket-A ADRs, field never existed) must be ALLOWED"
            inserted_plus_body_edit = inserted.replace("## Context\nc\n", "## Context\nc, and more\n")
            assert not is_intent_refs_backfill(k, inserted_plus_body_edit), \
                "an insertion PLUS a body change must still FAIL T4 (body must stay byte-identical)"
            reordered = adr_no_field.replace(
                "id: adr-0001\nstatus: accepted\n",
                "status: accepted\nid: adr-0001\n") .replace("date: 2026-07-09\n---",
                                                              "date: 2026-07-09\nintent-refs: idr-0003\n---")
            assert not is_intent_refs_backfill(k, reordered), \
                "an insertion alongside a REORDERED frontmatter line must still FAIL (not a clean single insertion)"
            # --- IDR positive: committed-locked IDR blocks edit ---
            g = repo / "idr-0001-x.md"
            g.write_text(idr.format(s="locked"))
            env_git("add", "idr-0001-x.md"); env_git("commit", "-qm", "idr locked")
            assert head_is_locked_ledger(g), "committed-locked IDR must BLOCK edits (the ledger) — positive"
            # --- IDR negative: a draft IDR (even committed) stays freely editable ---
            g.write_text(idr.format(s="draft"))
            env_git("add", "idr-0001-x.md"); env_git("commit", "-qm", "idr amended to draft")
            assert not head_is_locked_ledger(g), "committed-draft IDR must be ALLOWED to edit — negative"
            # --- RDD positive: committed-locked RDD blocks edit ---
            h = repo / "rdd-0001-x.md"
            h.write_text(rdd.format(s="locked"))
            env_git("add", "rdd-0001-x.md"); env_git("commit", "-qm", "rdd locked")
            assert head_is_locked_ledger(h), "committed-locked RDD must BLOCK edits (the ledger) — positive"
            # --- RDD negative: a draft RDD (even committed) stays freely editable ---
            h.write_text(rdd.format(s="draft"))
            env_git("add", "rdd-0001-x.md"); env_git("commit", "-qm", "rdd amended to draft")
            assert not head_is_locked_ledger(h), "committed-draft RDD must be ALLOWED to edit — negative"
    # T10 spine id-collision FAIL (#633): reproduces the 2026-08-18 incident — two lld-0011
    # files (different slugs, same family+number) must FAIL; a clean spine, and an id-less/
    # malformed-id doc (T1/T2's own territory, not this check's), must not.
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        spine = Path(td) / ".claude" / "docs" / "lld"
        spine.mkdir(parents=True)
        lld_tpl = ("---\ndoc-type: lld\nid: {id}\nstatus: draft\ndate: 2026-08-18\nowner: k\n"
                   "ticket: n/a\nsupersedes: null\n---\n# L\n"
                   "## Components\nc\n## Interfaces\ni\n## Data\nd\n## Risks\nr\n")
        (spine / "lld-0011-recurrence-audit.md").write_text(lld_tpl.format(id="lld-0011-recurrence-audit"))
        (spine / "lld-0011-fleet-state-rollup-draft.md").write_text(lld_tpl.format(id="lld-0011-fleet-state-rollup"))
        collision = check_spine(spine.parent)
        assert any(f[1] == "T10" for f in collision), "two lld-0011 files (any slug) must FAIL T10 — the #633 incident"
        # negative control: renumber the second file's id -> clean spine, no T10
        (spine / "lld-0011-fleet-state-rollup-draft.md").write_text(lld_tpl.format(id="lld-0012-fleet-state-rollup"))
        assert not any(f[1] == "T10" for f in check_spine(spine.parent)), "distinct numbers must NOT FAIL T10"
        # negative control: a docs_root that doesn't exist is not a failure (repo hasn't adopted the spine)
        assert check_spine(Path(td) / "nope") == [], "a missing docs_root must return no findings, not fail"
    # T11 IDR scope FAIL (#652): a Claim naming a feature/component/screen/endpoint grain FAILs;
    # a whole-app/product-thesis Claim doesn't; a code-span skill-name mention (`file-feature`)
    # must not false-positive; this repo's own locked IDRs (idr-0001..0011) MUST pass clean.
    idr_scope_base = ("---\ndoc-type: idr\nid: idr-0099\nstatus: draft\ndate: 2026-08-18\nowner: k\n"
                       "proof-ref: n/a\nprovenance: decided-by-human\nsupersedes: null\n---\n"
                       "# I\n## Claim\n{claim}\n## Why\nw\n## Proof\np\n")
    idr_feature_grain = idr_scope_base.format(claim="The checkout feature should validate coupon codes before submit.")
    assert any(f[1] == "T11" for f in lint_text(idr_feature_grain)), "feature-grain IDR Claim must FAIL T11"
    idr_component_grain = idr_scope_base.format(claim="The nav bar component should collapse under 600px.")
    assert any(f[1] == "T11" for f in lint_text(idr_component_grain)), "component-grain IDR Claim must FAIL T11"
    idr_app_level = idr_scope_base.format(claim="This estate's self-hosted toolchain converts every "
                                                 "incident class into a lint rule, gate check, or selftest "
                                                 "fixture before the fix ships.")
    assert not any(f[1] == "T11" for f in lint_text(idr_app_level)), "app-level IDR Claim must NOT FAIL T11"
    idr_code_mention = idr_scope_base.format(claim="User signal enters through the existing intake spine "
                                                    "(`file-bug`/`file-feature`/issue-sorter), not a new door.")
    assert not any(f[1] == "T11" for f in lint_text(idr_code_mention)), \
        "a code-span skill name containing 'feature' must NOT FAIL T11 (idr-0008 near-miss)"
    real_idr_dir = Path(__file__).resolve().parent.parent.parent / ".claude" / "docs" / "idr"
    if real_idr_dir.is_dir():
        for p in sorted(real_idr_dir.glob("*.md")):
            fs = [f for f in (lint_text(p.read_text(encoding="utf-8", errors="replace")) or []) if f[1] == "T11"]
            assert not fs, f"locked IDR {p.name} must pass T11 clean (#652 acceptance), got {fs}"
    # T12/T13 scope+audience FAIL, new-mints-only (#657, ratified 2026-08-18): a SPEC fixture
    # (grain-governed: feature|component) parameterized on scope/audience/new_mint.
    spec_scope_base = ("---\ndoc-type: spec\nid: spec-x\nstatus: draft\n{scope}{audience}---\n"
                        "# S\n## Requirements\nREQ-1: x\n## Non-goals\nn\n## Examples\ne\n"
                        "## Acceptance\na\n## Agent verification\nv\n")
    missing_scope = spec_scope_base.format(scope="", audience="audience: builder\n")
    assert any(f[1] == "T12" for f in lint_text(missing_scope, new_mint=True)), \
        "new-mint SPEC with no scope: must FAIL T12"
    assert not any(f[1] == "T12" for f in lint_text(missing_scope, new_mint=False)), \
        "grandfathered (new_mint=False) SPEC with no scope: must NOT FAIL T12"
    bad_scope_value = spec_scope_base.format(scope="scope: whole-app\n", audience="audience: builder\n")
    assert any(f[1] == "T12" for f in lint_text(bad_scope_value, new_mint=False)), \
        "an out-of-vocabulary scope: value must FAIL T12 even when grandfathered"
    out_of_grain = spec_scope_base.format(scope="scope: app\n", audience="audience: builder\n")
    assert any(f[1] == "T12" for f in lint_text(out_of_grain, new_mint=False)), \
        "scope: app on a SPEC (feature|component grain) must FAIL T12 even when grandfathered"
    valid_scope = spec_scope_base.format(scope="scope: feature\n", audience="audience: builder\n")
    assert not any(f[1] == "T12" for f in lint_text(valid_scope, new_mint=True)), \
        "scope: feature on a SPEC must NOT FAIL T12"
    adr_any_grain = ("---\ndoc-type: adr\nid: adr-0099\nstatus: proposed\ndate: 2026-08-18\n"
                      "intent-refs: idr-0001\nscope: {scope}\naudience: reviewer\n---\n"
                      "# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
    for g in ("app", "feature", "component"):
        assert not any(f[1] == "T12" for f in lint_text(adr_any_grain.format(scope=g), new_mint=True)), \
            f"ADR is decision-scoped (any grain) — scope: {g} must NOT FAIL T12"
    ticket_no_scope_requirement = ("---\ndoc-type: ticket\nid: tkt-0099\nstatus: open\ndate: 2026-08-18\n"
                                    "audience: builder\n---\n# T\n## Summary\ns\n## Acceptance\na\n## Links\nl\n")
    assert not any(f[1] == "T12" for f in lint_text(ticket_no_scope_requirement, new_mint=True)), \
        "TICKET is not grain-governed — no scope: must NOT FAIL T12"
    # T13 audience: FAIL, new-mints-only, ALL types (#657) — reuse the SPEC fixture, vary audience.
    missing_audience = spec_scope_base.format(scope="scope: feature\n", audience="")
    assert any(f[1] == "T13" for f in lint_text(missing_audience, new_mint=True)), \
        "new-mint SPEC with no audience: must FAIL T13"
    assert not any(f[1] == "T13" for f in lint_text(missing_audience, new_mint=False)), \
        "grandfathered (new_mint=False) SPEC with no audience: must NOT FAIL T13"
    bad_audience_value = spec_scope_base.format(scope="scope: feature\n", audience="audience: nobody\n")
    assert any(f[1] == "T13" for f in lint_text(bad_audience_value, new_mint=False)), \
        "an out-of-vocabulary audience: token must FAIL T13 even when grandfathered"
    multi_audience = spec_scope_base.format(scope="scope: feature\n", audience="audience: builder, reviewer\n")
    assert not any(f[1] == "T13" for f in lint_text(multi_audience, new_mint=True)), \
        "a valid comma-separated multi-token audience: must NOT FAIL T13"
    # is_new_mint() itself, git-aware, same shape as T4's head_is_locked_ledger fixture: an
    # untracked file is a new mint; once committed, it's grandfathered.
    if shutil.which("git"):
        with tempfile.TemporaryDirectory() as td2:
            repo2 = Path(td2)
            env_git2 = lambda *a: subprocess.run(["git", *a], cwd=repo2, capture_output=True, text=True,
                                                 env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                                      "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                                                      "PATH": __import__("os").environ["PATH"], "HOME": td2})
            env_git2("init", "-q")
            mint_file = repo2 / "spec-x.md"
            mint_file.write_text(valid_scope)
            assert is_new_mint(mint_file), "an untracked file must be a new mint -> enforce presence"
            env_git2("add", "spec-x.md"); env_git2("commit", "-qm", "mint")
            assert not is_new_mint(mint_file), "a committed (HEAD) file must be grandfathered -> presence not enforced"
    # Corpus-clean proof (#657 acceptance): every real, already-committed doc under this repo's
    # own `.claude/docs` spine must pass T12/T13 clean under its ACTUAL is_new_mint() status — the
    # grandfather ratchet in practice, not just in a synthetic fixture.
    real_docs_root = Path(__file__).resolve().parent.parent.parent / ".claude" / "docs"
    if real_docs_root.is_dir():
        for p in sorted(real_docs_root.rglob("*.md")):
            rtext = p.read_text(encoding="utf-8", errors="replace")
            rfm = parse_frontmatter(rtext)
            if not rfm or "doc-type" not in rfm or rfm.get("doc-type") not in TYPES:
                continue
            fs = [f for f in (lint_text(rtext, new_mint=is_new_mint(p)) or []) if f[1] in ("T12", "T13")]
            assert not fs, f"existing corpus doc {p.name} must pass T12/T13 clean (grandfather, #657), got {fs}"
    print("doc_lint selftest · PASS · all 11 templates self-consistent; type/status/sections/spine counters bite; "
          "T4 ledger-lock guards committed ADR(accepted)/IDR(locked)/RDD(locked) history only; "
          "T4's ADR-0027 intent-refs backfill carve-out bites, second-edit and other-field negative controls hold (#978); "
          "T6 orphan-ADR warn bites; T7 RDD citation+DRI-presence FAIL bites; T8 IDR provenance FAIL bites; "
          "T9 SPEC agent-verification WARN bites; T10 spine id-collision FAIL bites (#633); "
          "T11 IDR scope FAIL bites, code-span mentions don't false-positive, this repo's own IDRs pass clean (#652); "
          "T5 REQ-<INFIX>- prefixed ids (uppercase) pass, lowercase infix still warns (#634); "
          "T12 scope: grain FAIL bites new-mints-only, grandfather waives presence never correctness (#657); "
          "T13 audience: FAIL bites new-mints-only, no any-agent default (#657); is_new_mint() git-aware "
          "bites; the full existing .claude/docs corpus passes T12/T13 clean (grandfather proven in practice)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "--hook":
        sys.exit(hook_mode())
    if args[0] == "--spine":
        docs_root = Path(args[1]) if len(args) > 1 else Path(__file__).resolve().parent.parent.parent / ".claude" / "docs"
        findings = check_spine(docs_root)
        if findings:
            print(f"doc_lint --spine · FAIL · {docs_root}")
            for sev, code, msg in findings:
                print(f"  {sev:5} {code}  {msg}")
            sys.exit(1)
        print(f"doc_lint --spine · clean · {docs_root}")
        sys.exit(0)
    sys.exit(max(render(a, lint_text(Path(a).read_text(encoding="utf-8", errors="replace"),
                                     new_mint=is_new_mint(Path(a)))) for a in args))
