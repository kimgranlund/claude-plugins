#!/usr/bin/env python3
"""docs_check — mechanical freshness of a plugin's human-facing docs.

Usage:
  docs_check.py <plugin-root>     validate README.md / MANUAL.md / CLAUDE.md coverage
  docs_check.py selftest          prove the counters bite

Rules (the checkable slice; description *accuracy* stays with /ship-plugin and /check-everything):
  R1 [FAIL] every skills/<name> appears in README.md — OR (ticket #249) in the marketplace root
            README's own generated inventory block (the `<!-- inventory:begin` fence), when this
            plugin sits under one and that root README carries it
  R2 [FAIL] every skills/<name> appears in MANUAL.md (skipped if no MANUAL.md)
  R3 [FAIL] README footer's version equals .claude-plugin/plugin.json version — OR (ticket #249)
            the newest GitHub Release / git tag when the README carries no ledger line at all
  R4 [WARN] CLAUDE.md's stated skill count matches the tree (skipped if no CLAUDE.md — it
            doesn't ship in the artifact)
  R5 [WARN] every scripts/*.py is mentioned in README.md — same root-README fallback as R1
  R6 [WARN] footer ledger entries stay one physical line each (plugin-writing-rules' cap,
            issue #203: no more than one `vX.Y.Z · date ·` marker per line, no line past
            600 chars — the unbounded-paragraph-append shape caught once at 157 KB)
  R7 [FAIL] two adr/idr/lld/rdd documents under this repo's `.claude/docs` doc spine claim the
            same (family, number) — the 2026-08-18 incident (#633): two parallel builds both
            minted `lld-0011`, caught only by a coordinator's manual pre-merge read, nothing
            mechanical. Runs once per plugin-gate invocation (this check already runs for every
            plugin via G10), so every plugin's gate inherits the same protection with no new
            G-check. The sweep/parse logic here is a deliberate, self-contained DUPLICATE of
            `docs/scripts/doc_lint.py`'s own T10 (same rule, same incident) — not an import: this
            script is harness's plugin-agnostic gate machinery, and a script-path reach into the
            docs plugin's `scripts/` would violate the hard plugin-boundary rule
            (`.claude/rules/plugin-authoring.md`). `doc_lint.py --spine` stays the canonical,
            dev-time-invocable copy; this one exists only so G10 enforces it universally.
            Skipped (no findings) when no `.claude/docs` directory is found walking up from the
            plugin root — a repo that hasn't adopted the doc spine yet is not a failure.

Exit 0 clean/warnings, 1 on any FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

# R7's scope: the four ledger families the doc spine numbers, and the (family, number) pattern
# their `id:` frontmatter values carry (`lld-0011-recurrence-audit` -> ("lld", "0011")). Mirrors
# docs/scripts/doc_lint.py's own SPINE_FAMILIES/SPINE_ID_RE verbatim (kept in sync by hand — see
# R7's docstring above for why this is a duplicate, not a shared import).
_SPINE_FAMILIES = {"adr", "idr", "lld", "rdd"}
_SPINE_ID_RE = re.compile(r"^(adr|idr|lld|rdd)-(\d+)\b")


_TAG_VERSION_RE = re.compile(r"(?:^|[-_/])v?(\d+\.\d+\.\d+)$")


def _extract_version(tag):
    """Pure. Extracts an `X.Y.Z` version from a tag that may carry a plugin-name prefix (this
    repo's own real shape is `adia-sdlc-v0.6.76`, not a bare `v0.6.76`) — matches a trailing
    `-`/`_`/`/`-delimited (or bare, unprefixed) `vX.Y.Z`/`X.Y.Z` at the END of the string. Returns
    None on no match, never a raise or a garbage partial string. Same regex/shape as
    `version_monotonic_check.py`'s own `_extract_version` — see `_newest_release_or_tag`'s own
    docstring for why this is a deliberate duplicate, not a shared import."""
    m = _TAG_VERSION_RE.search(tag)
    return m.group(1) if m else None


def _newest_release_or_tag(root: Path, run_fn=None):
    """Ticket #249 (adiahealth/adia-harness). A deliberate, self-contained DUPLICATE of
    `version_monotonic_check.py`'s own `resolve_release_ledger_fallback` — same reasoning as R7's
    own duplication above (this is harness's plugin-agnostic gate machinery; a cross-script
    import would be a needless coupling for six lines of subprocess plumbing). Tries the newest
    GitHub Release first, falls back to the newest local git tag on ANY failure OR an unparseable
    tag name. `run_fn` is test-injectable (a callable taking `(*args)`, returning stdout or
    raising) so `selftest` never touches the network or `gh`. Returns
    `(source: str|None, version: str|None)`."""
    if run_fn is not None:
        try:
            out = run_fn("gh", "release", "list", "--limit", "1", "--json", "tagName")
            data = json.loads(out)
            if data:
                v = _extract_version(data[0]["tagName"])
                if v is not None:
                    return "GitHub Releases", v
        except Exception:  # noqa: BLE001
            pass
        try:
            out = run_fn("git", "describe", "--tags", "--abbrev=0")
            tag = out.strip()
            v = _extract_version(tag) if tag else None
            return ("newest git tag", v) if v is not None else (None, None)
        except Exception:  # noqa: BLE001
            return None, None

    gh = subprocess.run(["gh", "release", "list", "--limit", "1", "--json", "tagName"],
                         capture_output=True, text=True, cwd=root)
    if gh.returncode == 0 and gh.stdout.strip():
        try:
            data = json.loads(gh.stdout)
            if data:
                v = _extract_version(data[0]["tagName"])
                if v is not None:
                    return "GitHub Releases", v
        except ValueError:
            pass
    tag = subprocess.run(["git", "describe", "--tags", "--abbrev=0"],
                          capture_output=True, text=True, cwd=root)
    if tag.returncode == 0 and tag.stdout.strip():
        v = _extract_version(tag.stdout.strip())
        if v is not None:
            return "newest git tag", v
    return None, None


def _repo_docs_root(root: Path):
    """Walk upward from a plugin root looking for `.claude/docs` — this workspace's shared
    functional-doc spine (CLAUDE.md's docs-root override). No git dependency: plugin roots sit
    directly under the repo root in every observed layout, but walking up (rather than assuming
    exactly one level) tolerates a nested plugin root too. Returns None within 6 levels — a repo
    that hasn't adopted the doc spine yet, not a failure."""
    cur = root.resolve()
    for _ in range(6):
        candidate = cur / ".claude" / "docs"
        if candidate.is_dir():
            return candidate
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def _spine_frontmatter(text):
    """Minimal doc-type/id frontmatter read — see R7's docstring for why this duplicates
    doc_lint.py's `parse_frontmatter` instead of importing it."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].splitlines():
        m = re.match(r"^([\w-]+):\s*(.*?)(\s+#.*)?$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def _spine_duplicate_ids(root: Path):
    """R7: sweep `.claude/docs/**` for two adr/idr/lld/rdd documents claiming the same
    (family, number). Keyed on (family, number), never the full `id:` string — two colliding
    drafts plausibly differ only in their descriptive slug, so an exact-string dedup would let
    the real #633 incident straight through."""
    docs_root = _repo_docs_root(root)
    if docs_root is None:
        return []
    seen = {}
    findings = []
    for p in sorted(docs_root.rglob("*.md")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = _spine_frontmatter(text)
        if fm.get("doc-type") not in _SPINE_FAMILIES:
            continue
        doc_id = fm.get("id", "")
        m = _SPINE_ID_RE.match(doc_id)
        if not m:
            continue  # doc_lint's own T1/T2 own a missing/malformed id; not this rule's job
        key = (m.group(1), m.group(2))
        if key in seen:
            prev_path, prev_id = seen[key]
            findings.append(("FAIL", "R7",
                              f"id collision: {p} (`{doc_id}`) and {prev_path} (`{prev_id}`) both "
                              f"claim {key[0]}-{key[1]} -> re-read the spine's highest id off "
                              f"origin/main before numbering (dispatch-ticket's own discipline)"))
        else:
            seen[key] = (p, doc_id)
    return findings


_INVENTORY_FENCE = "<!-- inventory:begin"


def _marketplace_root_readme_text(root: Path):
    """Ticket #249 (adiahealth/adia-harness). A plugin living under a marketplace repo
    (`<workspace>/plugins/<name>`, this repo's own layout, ADR-0007) may carry NO per-skill/
    per-script prose of its own — its root README's own generated inventory block (the
    `<!-- inventory:begin` fence `make_inventory.py`-shaped scripts write) already names every
    skill and script mechanically, kept fresh by that generator's own freshness gate. Walks up
    from `root` (mirrors `_repo_docs_root`'s own upward walk, six levels) looking for the
    nearest ancestor README.md carrying that fence; returns its text, or None when no such
    ancestor exists (an isolated plugin checkout, or a marketplace whose root README hasn't
    adopted the generated-inventory convention) — R1/R5 fall back to FAILing/WARNing on the
    plugin's own README alone in that case, unchanged pre-#249 behavior."""
    cur = root.resolve()
    for _ in range(6):
        if cur.parent == cur:
            break
        cur = cur.parent
        candidate = cur / "README.md"
        if candidate.is_file():
            try:
                text = candidate.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if _INVENTORY_FENCE in text:
                return text
    return None


def check(root: Path, release_run_fn=None):
    """`release_run_fn` is test-injectable (R3's Release/tag fallback, ticket #249) — None in
    every pre-#249 call site, unchanged behavior (real `gh`/`git` subprocess calls)."""
    findings = []
    skills = sorted(p.parent.name for p in root.glob("skills/*/SKILL.md"))
    readme = root / "README.md"
    if not readme.is_file():
        return [("FAIL", "R1", "no README.md at plugin root -> the version ledger is mandatory")]
    rd = readme.read_text(encoding="utf-8", errors="replace")

    # Ticket #249: R1 (skills) and R5 (scripts) below both accept a mention in the marketplace
    # ROOT README's own generated inventory block as satisfying "mentioned in README.md" — a
    # plugin whose own README carries no per-member prose (having moved that duty to the root
    # README's mechanically-generated inventory, adia-sdlc's own shape post-#95/#245) is not
    # penalized for it. `rd` itself (this plugin's own README) is unioned with `root_readme_text`
    # so a plugin still naming members in its OWN README (the pre-#249 norm) is unaffected.
    root_readme_text = _marketplace_root_readme_text(root)
    mention_text = rd if root_readme_text is None else (rd + "\n" + root_readme_text)

    for s in skills:
        if s not in mention_text:
            findings.append(("FAIL", "R1", f"skills/{s} has no mention in README.md (or the "
                                            "marketplace root README's inventory block) -> add its map row"))

    manual = root / "MANUAL.md"
    if manual.is_file():
        md = manual.read_text(encoding="utf-8", errors="replace")
        for s in skills:
            if s not in md:
                findings.append(("FAIL", "R2", f"skills/{s} is undocumented in MANUAL.md -> users can't discover it"))

    try:
        version = json.loads((root / ".claude-plugin" / "plugin.json").read_text()).get("version", "")
    except (OSError, ValueError):
        version = ""
    m = re.search(r"^v(\d+\.\d+\.\d+)\b", rd, re.M)
    if not m:
        # Ticket #249 (adiahealth/adia-harness): a README with NO ledger line at all falls back
        # to the newest GitHub Release or git tag before FAILing outright — a WARN naming the
        # fallback on a match, never a silent PASS. A README that DOES carry a line but it's
        # wrong (the `elif` branch below) is unaffected — still a straight FAIL.
        source, fallback_version = _newest_release_or_tag(root, run_fn=release_run_fn)
        if fallback_version is not None and version and fallback_version == version:
            findings.append(("WARN", "R3", f"README carries no ledger line; verified via fallback "
                                            f"({source}): {fallback_version} matches plugin.json's {version}"))
        elif fallback_version is not None:
            findings.append(("FAIL", "R3", f"README carries no ledger line; fallback ({source}) "
                                            f"newest is {fallback_version}, plugin.json says {version} -> mismatch"))
        else:
            findings.append(("FAIL", "R3", "README carries no `vX.Y.Z` footer ledger line, and no "
                                            "GitHub Release or git tag resolves as a fallback either"))
    elif version and m.group(1) != version:
        findings.append(("FAIL", "R3", f"README footer says v{m.group(1)} but plugin.json says {version} "
                                       "-> the ledger lies about the current release"))

    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        cm = claude_md.read_text(encoding="utf-8", errors="replace")
        c = re.search(r"\((\d+),", cm)
        if c and int(c.group(1)) != len(skills):
            findings.append(("WARN", "R4", f"CLAUDE.md states {c.group(1)} skills; tree has {len(skills)} -> stale count"))

    for sc in sorted(root.glob("scripts/*.py")):
        if sc.name not in mention_text:
            findings.append(("WARN", "R5", f"scripts/{sc.name} is not mentioned in README.md "
                                            "(or the marketplace root README's inventory block)"))

    ledger_marker = re.compile(r"v\d+\.\d+\.\d+ · \d{4}-\d{2}-\d{2} · ")
    for line in rd.splitlines():
        hits = len(ledger_marker.findall(line))
        if hits >= 2:
            findings.append(("WARN", "R6",
                              f"{hits} ledger entries blobbed onto one line -> split to one entry per line "
                              f"({line[:60]}...)"))
        elif hits == 1 and len(line) > 600:
            findings.append(("WARN", "R6",
                              f"ledger entry line is {len(line)} chars -> compress to one-line-per-version "
                              f"(plugin-writing-rules' cap, issue #203) ({line[:60]}...)"))
    findings.extend(_spine_duplicate_ids(root))
    return findings


def run(root: Path):
    fs = check(root)
    verdict = "FAIL" if any(f[0] == "FAIL" for f in fs) else ("warn" if fs else "clean")
    print(f"docs_check · {verdict} · {root}")
    for sev, code, msg in fs:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if verdict == "FAIL" else 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / ".claude-plugin").mkdir()
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "demo", "version": "1.2.0"}')
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text("x")
        (r / "scripts").mkdir()
        (r / "scripts" / "demo_check.py").write_text("x")
        (r / "README.md").write_text("map: demo-review · demo_check.py\n\nv1.2.0 · ledger\n")
        (r / "MANUAL.md").write_text("use demo-review\n")
        (r / "CLAUDE.md").write_text("skills (1, each)\n")
        assert not check(r), f"clean fixture must pass, got {check(r)}"
        (r / "skills" / "demo-forge").mkdir()
        (r / "skills" / "demo-forge" / "SKILL.md").write_text("x")
        codes = {f[1] for f in check(r)}
        assert {"R1", "R2", "R4"} <= codes, f"undocumented skill + stale count must fire, got {codes}"
        (r / "README.md").write_text("map: demo-review demo-forge demo_check.py\n\nv1.1.0 · ledger\n")
        (r / "MANUAL.md").write_text("demo-review demo-forge\n")
        assert any(f[1] == "R3" for f in check(r)), "version mismatch must fail R3"

        # R6: one-line-per-version ledger cap (issue #203) — negative control first.
        good_line = "v1.2.0 · 2026-08-13 · a compact one-line summary of the bump\n"
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + good_line
        )
        (r / "MANUAL.md").write_text("demo-review demo-forge\n")
        assert not any(f[1] == "R6" for f in check(r)), "a clean one-liner must not fire R6"
        blobbed = (
            "v1.2.0 · 2026-08-13 · first entry · v1.1.0 · 2026-08-12 · second entry blobbed onto the same line\n"
        )
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + blobbed
        )
        assert any(f[1] == "R6" for f in check(r)), "two markers on one line must fire R6"
        overlong = "v1.2.0 · 2026-08-13 · " + ("padding " * 90) + "\n"
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + overlong
        )
        assert any(f[1] == "R6" for f in check(r)), "a >600-char single entry must fire R6"

    # R7 spine id-collision FAIL (#633): reproduces the 2026-08-18 incident — two lld-0011 files
    # (different slugs, same family+number) under `<workspace>/.claude/docs/lld/`, with `root`
    # standing in for a plugin dir sitting directly under that same workspace root.
    with tempfile.TemporaryDirectory() as td:
        workspace = Path(td)
        plugin_root = workspace / "demo-plugin"
        plugin_root.mkdir()
        spine = workspace / ".claude" / "docs" / "lld"
        spine.mkdir(parents=True)
        lld_tpl = ("---\ndoc-type: lld\nid: {id}\nstatus: draft\ndate: 2026-08-18\nowner: k\n"
                   "ticket: n/a\nsupersedes: null\n---\n# L\n"
                   "## Components\nc\n## Interfaces\ni\n## Data\nd\n## Risks\nr\n")
        (spine / "lld-0011-a.md").write_text(lld_tpl.format(id="lld-0011-recurrence-audit"))
        (spine / "lld-0011-b.md").write_text(lld_tpl.format(id="lld-0011-fleet-state-rollup"))
        assert any(f[1] == "R7" for f in _spine_duplicate_ids(plugin_root)), \
            "two lld-0011 files (any slug) must FAIL R7 — the #633 incident"
        # negative control: renumber the second file's id -> clean spine, no R7
        (spine / "lld-0011-b.md").write_text(lld_tpl.format(id="lld-0012-fleet-state-rollup"))
        assert not any(f[1] == "R7" for f in _spine_duplicate_ids(plugin_root)), \
            "distinct numbers must NOT FAIL R7"
    # negative control: an isolated tree with no reachable .claude/docs at all -> no findings
    with tempfile.TemporaryDirectory() as td2:
        lonely = Path(td2) / "elsewhere" / "plugin"
        lonely.mkdir(parents=True)
        assert _repo_docs_root(lonely) is None, "an isolated tempdir must have no reachable .claude/docs"
        assert _spine_duplicate_ids(lonely) == [], \
            "a plugin root with no reachable .claude/docs must return no R7 findings"
    # ---- Ticket #249 (adiahealth/adia-harness): R3's Release/tag fallback when a README has NO
    # ledger line at all ----
    with tempfile.TemporaryDirectory() as td3:
        r3 = Path(td3)
        (r3 / ".claude-plugin").mkdir()
        (r3 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo3", "version": "2.5.0"}')
        (r3 / "README.md").write_text("this plugin README carries no ledger line at all\n")

        def _fallback_match(*args):
            if args[:2] == ("gh", "release"):
                return '[{"tagName": "v2.5.0"}]'
            raise AssertionError(f"unexpected call: {args}")

        findings_match = check(r3, release_run_fn=_fallback_match)
        assert not any(f[0] == "FAIL" and f[1] == "R3" for f in findings_match), \
            f"positive control: a matching GitHub Release fallback must WARN, never FAIL R3: {findings_match}"
        assert any(f[0] == "WARN" and f[1] == "R3" for f in findings_match), \
            f"positive control: a matching fallback must WARN by name (never a silent PASS): {findings_match}"

        def _fallback_mismatch(*args):
            if args[:2] == ("gh", "release"):
                return '[{"tagName": "v2.4.0"}]'
            raise AssertionError(f"unexpected call: {args}")

        findings_mismatch = check(r3, release_run_fn=_fallback_mismatch)
        assert any(f[0] == "FAIL" and f[1] == "R3" and "mismatch" in f[2] for f in findings_mismatch), \
            f"negative control: a non-matching fallback must still FAIL R3: {findings_mismatch}"

        def _fallback_nothing(*args):
            raise RuntimeError("nothing resolves")

        findings_none = check(r3, release_run_fn=_fallback_nothing)
        assert any(f[0] == "FAIL" and f[1] == "R3" for f in findings_none), \
            f"reverse control: no ledger line AND no fallback resolving must still FAIL R3, never silently pass: {findings_none}"

        # Live fixture control (adiahealth/adia-harness#249 review): this repo's own real tag
        # shape is plugin-prefixed (`adia-sdlc-v2.5.0`), not a bare `v2.5.0`.
        assert _extract_version("adia-sdlc-v2.5.0") == "2.5.0", \
            f"positive control: a plugin-prefixed tag must extract its trailing version: {_extract_version('adia-sdlc-v2.5.0')!r}"
        assert _extract_version("not-a-version") is None, \
            "a tag with no trailing X.Y.Z must extract to None, never a garbage partial match"

        def _fallback_prefixed_match(*args):
            if args[:2] == ("gh", "release"):
                return '[{"tagName": "demo3-v2.5.0"}]'
            raise AssertionError(f"unexpected call: {args}")

        findings_prefixed = check(r3, release_run_fn=_fallback_prefixed_match)
        assert any(f[0] == "WARN" and f[1] == "R3" for f in findings_prefixed), \
            f"positive control (live fixture shape): a plugin-prefixed GitHub Release tag must satisfy the R3 fallback: {findings_prefixed}"

    print("docs_check selftest (ticket #249) · PASS · R3 Release/tag fallback WARNs on a match, "
          "FAILs on a mismatch, FAILs when nothing resolves — never a silent PASS")

    # ---- Ticket #249 (adiahealth/adia-harness): R1/R5's marketplace-root-README fallback ----
    with tempfile.TemporaryDirectory() as td4:
        workspace4 = Path(td4)
        plugin4 = workspace4 / "plugins" / "demo4"
        plugin4.mkdir(parents=True)
        (plugin4 / ".claude-plugin").mkdir()
        (plugin4 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo4", "version": "1.0.0"}')
        (plugin4 / "skills" / "alpha-skill").mkdir(parents=True)
        (plugin4 / "skills" / "alpha-skill" / "SKILL.md").write_text("x")
        (plugin4 / "scripts").mkdir()
        (plugin4 / "scripts" / "alpha_check.py").write_text("x")
        # The plugin's OWN README carries only the ledger line — no skill/script prose at all
        # (the shape #245/#249 moved to: identity + Compendium + Releases pointer).
        (plugin4 / "README.md").write_text("v1.0.0 · 2026-09-02 · initial\n")

        # No root README at all -> R1 FAILs and R5 WARNs, unchanged pre-#249 behavior.
        findings_no_root = check(plugin4)
        assert any(f[0] == "FAIL" and f[1] == "R1" for f in findings_no_root), \
            f"reverse control: no marketplace root README at all must still FAIL R1 on the plugin's own README alone: {findings_no_root}"
        assert any(f[1] == "R5" for f in findings_no_root), \
            f"reverse control: no marketplace root README at all must still WARN R5: {findings_no_root}"

        # A root README two levels up carrying the inventory fence AND naming the skill/script
        # -> R1/R5 both clear, no padding needed in the plugin's own README.
        (workspace4 / "README.md").write_text(
            "# workspace\n\n<!-- inventory:begin generated by scripts/make_inventory.py -->\n"
            "- alpha-skill — does a thing\n- alpha_check.py — checks a thing\n"
            "<!-- inventory:end -->\n"
        )
        findings_with_root = check(plugin4)
        assert not any(f[1] == "R1" for f in findings_with_root), \
            f"positive control: a matching root-README inventory fence must satisfy R1 without any plugin-README padding: {findings_with_root}"
        assert not any(f[1] == "R5" for f in findings_with_root), \
            f"positive control: a matching root-README inventory fence must satisfy R5 too: {findings_with_root}"

        # Negative control: a root README exists but does NOT carry the fence (a plain repo
        # README with no generated inventory) -> R1/R5 fall back to FAILing/WARNing exactly as
        # if no root README existed at all — the fence itself is the trust boundary, not mere
        # ancestor-README presence.
        (workspace4 / "README.md").write_text("# workspace\n\njust a plain README, no fence\n")
        findings_no_fence = check(plugin4)
        assert any(f[0] == "FAIL" and f[1] == "R1" for f in findings_no_fence), \
            f"negative control: a root README with no inventory fence must NOT satisfy R1: {findings_no_fence}"

    print("docs_check selftest (ticket #249) · PASS · R1/R5 accept the marketplace root README's "
          "generated inventory block as an alternate mention source (fence-gated, never mere "
          "ancestor-README presence), no plugin-README padding required")

    print("docs_check selftest · PASS · coverage both docs, version ledger, stale count, script mentions, "
          "ledger one-liner cap, spine id-collision FAIL bites (#633)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(args[0]).resolve()))
