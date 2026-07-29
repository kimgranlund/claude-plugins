#!/usr/bin/env python3
"""doc_state.py — read-only doc-layer collector for the check-state skill.

Usage:
  doc_state.py [<repo-root>]     print the JSON snapshot
  doc_state.py selftest          prove the parsers on inline fixtures

No args defaults the root to `.` — a deliberate, disclosed deviation from the
no-args-prints-usage anatomy: the default target is meaningful for a collector.

Collects:
  items          ROADMAP / PLAN / BACKLOG / TICKET-typed markdown (matched by filename,
                 case-insensitive) under docs/ trees and the repo root: frontmatter
                 status/id/type (doc-writing-rules' fields), checkbox progress, and
                 every TKT-#### / ADR-#### the body references (the ID spine)
  release_drift  per plugin dir carrying .claude-plugin/plugin.json: manifest version
                 vs README ledger mention vs dist/<name>-<version>.plugin presence

Parsing is filename+frontmatter only — doc VALIDITY stays with docs' doc_lint;
this script only inventories what exists and what it points at.

Exit: 0 snapshot printed · 1 unexpected failure · 2 usage.
Selftest: 0 proven · 1 a control failed.
"""
import json
import re
import sys
from pathlib import Path

# Letter-bounded, not \b: "my-plan"/"plan_v2" hit, "explanation"/"implants" do not
# (audit 2026-07-29 M3: substring matching inventoried non-docs as phantom items)
DOC_NAME = re.compile(r"(?<![a-z])(roadmap|plan|backlog|ticket|tkt-\d+)(?![a-z])",
                      re.IGNORECASE)
SPINE_ID = re.compile(r"\b(TKT-\d{3,5}|ADR-\d{3,5})\b")
FM_FIELD = re.compile(r"^(status|id|type)\s*:\s*(.+?)\s*$", re.MULTILINE)


def parse_doc(text, path):
    item = {"path": path, "id": None, "type": None, "status": None,
            "open_boxes": 0, "done_boxes": 0, "spine_refs": []}
    if text.startswith("---"):
        fm = text.split("---", 2)[1] if text.count("---") >= 2 else ""
        for m in FM_FIELD.finditer(fm):
            item[m.group(1)] = m.group(2).strip("\"' ")
    item["open_boxes"] = len(re.findall(r"^\s*[-*] \[ \]", text, re.MULTILINE))
    item["done_boxes"] = len(re.findall(r"^\s*[-*] \[[xX]\]", text, re.MULTILINE))
    item["spine_refs"] = sorted(set(SPINE_ID.findall(text)))
    return item


def find_docs(root):
    root = Path(root)
    seen, hits = set(), []
    candidates = list(root.glob("*.md")) + list(root.glob("*/*.md")) \
        + list(root.glob("docs/**/*.md")) + list(root.glob("*/docs/**/*.md"))
    skip_parts = {".refactor-attic", "node_modules", "templates", "adr"}
    for p in candidates:
        # templates are forms, not work items; ADRs are decision-watcher's territory
        if p in seen or skip_parts & set(p.parts):
            continue
        seen.add(p)
        if DOC_NAME.search(p.stem):
            hits.append(p)
    return sorted(hits)


def release_drift(plugins):
    """plugins: [{name, version, readme_text, dist_names}] -> drift entries only.
    dist_names is None when no dist/ dir exists — dist/ is gitignored gate output,
    so its absence in a fresh clone is not drift (2026-07-29 smoke-test incident)."""
    drift = []
    for p in plugins:
        ledger_ok = p["version"] in p["readme_text"]
        dist_ok = (p["dist_names"] is None
                   or f"{p['name']}-{p['version']}.plugin" in p["dist_names"])
        if not (ledger_ok and dist_ok):
            drift.append({"plugin": p["name"], "version": p["version"],
                          "ledger_has_version": ledger_ok, "dist_has_version": dist_ok})
    return drift


def collect(root):
    rootp = Path(root)
    items = [parse_doc(p.read_text(errors="replace"), str(p.relative_to(rootp)))
             for p in find_docs(root)]
    plugins = []
    for manifest in sorted(rootp.glob("*/.claude-plugin/plugin.json")):
        pdir = manifest.parent.parent
        try:
            meta = json.loads(manifest.read_text())
        except json.JSONDecodeError:
            continue
        readme = pdir / "README.md"
        plugins.append({
            "name": meta.get("name", pdir.name),
            "version": meta.get("version", "?"),
            "readme_text": readme.read_text(errors="replace") if readme.exists() else "",
            "dist_names": [d.name for d in (pdir / "dist").glob("*.plugin")]
            if (pdir / "dist").is_dir() else None})
    return {"items": items, "release_drift": release_drift(plugins),
            "plugins_seen": [p["name"] for p in plugins]}


def selftest():
    fails = []
    doc = ("---\nid: TKT-0042\ntype: TICKET\nstatus: in-progress\n---\n"
           "# Fix the thing\nSee ADR-0002.\n- [x] repro\n- [ ] fix\n- [ ] gate\n")
    item = parse_doc(doc, "docs/tickets/tkt-0042.md")
    if not (item["id"] == "TKT-0042" and item["status"] == "in-progress"
            and item["open_boxes"] == 2 and item["done_boxes"] == 1):
        fails.append("negative control: frontmatter/checkbox parse missed fields")
    if item["spine_refs"] != ["ADR-0002", "TKT-0042"]:
        fails.append("ID-spine extraction wrong")
    plain = parse_doc("# just notes\nno spine here\n", "notes.md")
    if plain["id"] or plain["status"] or plain["spine_refs"]:
        fails.append("reverse control: plain doc grew phantom fields")
    drift = release_drift([
        {"name": "aged", "version": "2.0.0", "readme_text": "ledger: v1.9.0 only",
         "dist_names": ["aged-1.9.0.plugin"]},
        {"name": "clean", "version": "1.0.0", "readme_text": "v1.0.0 shipped",
         "dist_names": ["clean-1.0.0.plugin"]},
        {"name": "fresh-clone", "version": "1.0.0", "readme_text": "v1.0.0 shipped",
         "dist_names": None}])
    if len(drift) != 1 or drift[0]["plugin"] != "aged" or drift[0]["ledger_has_version"]:
        fails.append("negative control: version drift not caught")
    if any(d["plugin"] == "clean" for d in drift):
        fails.append("reverse control: clean plugin flagged as drifted")
    if any(d["plugin"] == "fresh-clone" for d in drift):
        fails.append("reverse control (2026-07-29 incident): absent dist/ (gitignored "
                     "gate output) flagged as drift")
    if not DOC_NAME.search("ROADMAP") or DOC_NAME.search("readme"):
        fails.append("doc-name matcher wrong (ROADMAP must hit, readme must not)")
    # M3 fixtures (audit 2026-07-29): substring hits were phantom docs
    for phantom in ("explanation", "airplane", "implants"):
        if DOC_NAME.search(phantom):
            fails.append(f"reverse control: '{phantom}' matched as a doc name")
    for real in ("my-plan", "plan_v2", "tkt-0042"):
        if not DOC_NAME.search(real):
            fails.append(f"negative control: '{real}' missed as a doc name")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        from pathlib import Path as P
        for rel in ("docs/plan.md", "docs/templates/plan.md", "docs/adr/0005-ticket-x.md"):
            f = P(td) / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_text("x")
        found = [str(p.relative_to(td)) for p in find_docs(td)]
        if found != ["docs/plan.md"]:
            fails.append(f"reverse control (2026-07-29): templates/ADR paths not "
                         f"excluded from inventory (got {found})")
    if fails:
        print(f"doc_state · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]; sys.exit(1)
    print("doc_state · selftest ok · 0 fail / 0 warn"); sys.exit(0)


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    root = argv[1] if len(argv) > 1 else "."
    if root.startswith("-"):
        print(__doc__); sys.exit(2)
    try:
        print(json.dumps(collect(root), indent=2))
    except OSError as e:
        print(f"doc_state · FAIL · {e}"); sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
