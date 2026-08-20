#!/usr/bin/env python3
"""Build lib/sitemap.json for the corpus-reader from a directory of Markdown files.

Scans CORPUS_DIR for `.md` files, groups them by their top-level section folder,
extracts a title + one-line summary for each, and writes the sitemap the static
reader (index.html) loads. Works for any generated corpus, not just the bundled
example.

    python3 build-sitemap.py [CORPUS_DIR] [--out lib/sitemap.json] [--title TITLE]
    python3 build-sitemap.py --init <CORPUS_ROOT>   # scaffold <CORPUS_ROOT>/site/ + build
    python3 build-sitemap.py --bake <CORPUS_ROOT> [--out reader.html]   # ONE self-contained file

The `--init` form is the **common `<corpus>/site/` convention**: it copies this reader
(machinery only — never a bundled example corpus) into `<CORPUS_ROOT>/site/` and builds
the sitemap there. Every plugin that generates a corpus site calls it, so the layout is
identical everywhere: serve the corpus root, open `/site/`.

The `--bake` form emits **one self-contained `reader.html`** that works on `file://`
(double-click — no server): the sitemap, every page's raw markdown, the reader CSS (+
per-corpus theme), and the component modules are inlined (an inline `<script
type="module">` executes on file://; only *fetched* modules don't). The render libraries
stay CDN-pinned with Subresource Integrity — the tags are lifted verbatim from
index.html so the pins have one source; fully offline, prose degrades to escaped text
per the reader's existing marked/DOMPurify fallback. Re-run after the corpus changes
(the bake is a snapshot).

CORPUS_DIR defaults to the single sibling directory that contains `.md` files
(e.g. the bundled `brand-corpus`). Page paths are written relative to this
script's directory — where index.html lives — so the reader can fetch them
directly. Pass `..` to generate for a viewer that lives in a SUBFOLDER of the
corpus (the `<corpus>/site/` export layout): paths come out `../<section>/…`,
and this script's own directory is excluded from the scan. Re-run after the
corpus changes. An optional `<corpus>/reader.config.json` —
`{"title": "…", "sections": {"01-foo": "one-line description"}}` — adds a title
+ per-section card descriptions without touching the reader. Python 3.8+, stdlib only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# This generator was promoted out of the static corpus-reader web app (which lives at
# references/corpus-reader/ — index.html, lib/, its own build-sitemap.py) into a real bundled
# script at scripts/build_sitemap.py (MIGRATION.md, Gate A ruling). ROOT stays "where index.html
# lives" per this script's own contract above; that's no longer this file's own directory, so it
# is computed relative to the plugin's references/corpus-reader/ sibling instead.
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "references", "corpus-reader"))
SKIP_DIRS = {"lib", ".git", "node_modules"}


def find_corpus(root):
    """Sibling directories that contain at least one .md file."""
    found = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path) or name in SKIP_DIRS or name.startswith("."):
            continue
        for _dirpath, _dirnames, files in os.walk(path):
            if any(f.endswith(".md") for f in files):
                found.append(name)
                break
    return found


def split_frontmatter(text):
    """Return (meta_dict, body) splitting a leading `--- ... ---` YAML block.

    Only flat `key: value` pairs are read — enough for the meta bar; this is not
    a full YAML parser.
    """
    meta = {}
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.DOTALL)
    if not match:
        return meta, text
    for line in match.group(1).splitlines():
        pair = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if pair:
            meta[pair.group(1).strip()] = pair.group(2).strip().strip('"').strip("'")
    return meta, text[match.end():]


def first_heading(body):
    for line in body.splitlines():
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    return None


def first_paragraph(body):
    """The first real prose paragraph, flattened to a short plain-text summary."""
    buf = []
    in_fence = started = False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not started:
            if s == "" or s[:1] in ("#", ">", "|", "-", "*") or s.startswith("---"):
                continue
            started = True
            buf.append(s)
        elif s == "":
            break
        else:
            buf.append(s)
    text = " ".join(buf)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # [label](url) -> label
    text = re.sub(r"[*_`#>]", "", text).strip()
    return (text[:197].rstrip() + "…") if len(text) > 198 else text


def prettify(name):
    name = re.sub(r"\.md$", "", name)
    name = re.sub(r"^\d+[-_]+", "", name)
    name = name.replace("-", " ").replace("_", " ").strip()
    return (name[:1].upper() + name[1:]) if name else name


def section_order(folder):
    m = re.match(r"^(\d+)", folder)
    return int(m.group(1)) if m else 9999


PROV_RE = re.compile(r"\[(KNOWN|INFERRED|OPEN|SEEDED)\]")


def norm_status(s):
    """Normalize a frontmatter status to a maturity bucket (else "")."""
    s = (s or "").lower()
    if "need" in s:
        return "needed"
    if "active" in s:
        return "active"
    if "work" in s:
        return "working"
    if "draft" in s:
        return "draft"
    return ""


def is_readme(name):
    n = name.lower()
    return n.startswith("00-readme") or n in ("readme.md", "readme")


def build_tree(entries):
    """Nest a section's pages into a folder tree for the sidebar nav (additive — the flat `pages`
    list is kept for routing/home/search). `entries` is a list of (subparts, page), where subparts
    are the corpus-relative path parts BELOW the section folder, including the filename. Returns a
    list of nodes:
        group: {"type":"group", "title":…, "children":[…], optional "doc": <path>}
        doc:   {"type":"doc", "path":…, "title":…}
    A subfolder's 00-README/README is promoted to that group's label (its `doc` + `title`), so
    clicking the folder opens its readme; a folder without one falls back to a prettified name. A
    flat corpus yields only top-level `doc` nodes — the nav renders it exactly as before."""
    root = {"type": "group", "children": [], "_key": ""}
    for subparts, page in entries:
        node = root
        for i, folder in enumerate(subparts[:-1]):
            key = "/".join(subparts[: i + 1])
            child = next((c for c in node["children"]
                          if c.get("type") == "group" and c.get("_key") == key), None)
            if child is None:
                child = {"type": "group", "children": [], "_key": key, "_folder": folder}
                node["children"].append(child)
            node = child
        leaf = subparts[-1]
        if is_readme(leaf) and node is not root:        # promote a subfolder readme to its label
            node["doc"] = page["path"]
            node["title"] = page["title"]
        else:
            node["children"].append({"type": "doc", "path": page["path"], "title": page["title"]})

    def name_key(c):
        return (c.get("_folder") if c.get("type") == "group"
                else (c.get("path") or "").split("/")[-1]).lower()

    def finalize(n):
        if n.get("type") != "group":
            return
        if not n.get("title"):
            n["title"] = prettify(n.get("_folder", ""))
        n["children"].sort(key=name_key)
        for c in n["children"]:
            finalize(c)
        n.pop("_key", None)
        n.pop("_folder", None)

    finalize(root)
    return root["children"]


def collect_sitemap(corpus_label, corpus_abs, path_base, title_override=None):
    """Scan the corpus and assemble the sitemap dict. Page paths are written relative to
    `path_base` — the directory the reader loads from (ROOT for the served layouts; the
    corpus root for --bake, whose output sits beside the content). Returns
    (sitemap, theme_abs-or-None); the theme path inside the sitemap is path_base-relative."""
    # Optional per-corpus polish (never required): a title override + one-line section
    # descriptions, from <corpus>/reader.config.json — the reader is unchanged without it.
    cfg = {}
    cfg_path = os.path.join(corpus_abs, "reader.config.json")
    if os.path.isfile(cfg_path):
        try:
            with open(cfg_path, encoding="utf-8") as fh:
                cfg = json.load(fh)
        except (ValueError, OSError):
            cfg = {}
    cfg_sections = cfg.get("sections") or {}

    entries = []
    for dirpath, dirnames, filenames in os.walk(corpus_abs):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and os.path.join(dirpath, d) != ROOT]
        for fname in filenames:
            if not fname.endswith(".md") or fname.startswith("."):
                continue
            full = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(full, path_base).replace(os.sep, "/")
            rel_corpus = os.path.relpath(full, corpus_abs).replace(os.sep, "/")
            entries.append((rel_path, rel_corpus, full))

    if not entries:
        sys.exit("error: no .md files under %s" % corpus_label)

    sections = {}
    root_pages = []
    sec_status, sec_prov = {}, {}            # section folder -> {bucket: count}
    tot_status, tot_prov = {}, {}            # corpus-wide totals
    for rel_path, rel_corpus, full in sorted(entries, key=lambda t: t[1].lower()):
        with open(full, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        meta, body = split_frontmatter(text)
        page = {
            "path": rel_path,
            "title": meta.get("title") or first_heading(body) or prettify(os.path.basename(rel_corpus)),
        }
        summary = first_paragraph(body)
        if summary:
            page["summary"] = summary
        if meta.get("status"):
            page["status"] = meta["status"]
        # The full parsed frontmatter, so the reader can enrich search beyond title/path/summary
        # (tags, type, version, owner, …). Flat key:value only (split_frontmatter), kept verbatim.
        if meta:
            page["meta"] = meta

        parts = rel_corpus.split("/")
        folder = parts[0] if len(parts) > 1 else None
        if folder is None:
            root_pages.append(page)
        else:
            section = sections.setdefault(
                folder,
                {"id": folder, "title": prettify(folder), "order": section_order(folder),
                 "pages": [], "_entries": []},
            )
            section["pages"].append(page)
            section["_entries"].append((parts[1:], page))   # parts[1:] = path below the section folder

        # Maturity (frontmatter status) + provenance ([KNOWN]/[INFERRED]/[OPEN]/[SEEDED])
        # counts feed the home stats bar. Graceful: omitted entirely when a corpus has none.
        bucket = folder or "_root"
        ns = norm_status(meta.get("status"))
        if ns:
            d = sec_status.setdefault(bucket, {}); d[ns] = d.get(ns, 0) + 1
            tot_status[ns] = tot_status.get(ns, 0) + 1
        # Count tags in prose only — fenced blocks and inline code mentioning a tag
        # (e.g. a doc ABOUT the tag syntax) must not skew the stats bar.
        prose = re.sub(r"`[^`\n]*`", "", re.sub(r"(?ms)^```.*?^```\s*$", "", body))
        for m in PROV_RE.findall(prose):
            k = m.lower()
            d = sec_prov.setdefault(bucket, {}); d[k] = d.get(k, 0) + 1
            tot_prov[k] = tot_prov.get(k, 0) + 1

    section_list = sorted(sections.values(), key=lambda s: (s["order"], s["title"].lower()))
    for section in section_list:
        del section["order"]  # ordering is now positional
        section["tree"] = build_tree(section.pop("_entries"))  # nested nav structure (additive)
        desc = cfg_sections.get(section["id"])
        if desc:
            section["desc"] = desc

    title = title_override or cfg.get("title") or (root_pages[0]["title"] if root_pages else prettify(corpus_label))

    # Optional per-corpus theme (reader.config.json "theme"): a stylesheet inside the
    # corpus, emitted as a path_base-relative path the shell injects after corpus-reader.css.
    theme_rel = None
    theme_abs = None
    if cfg.get("theme"):
        corpus_norm = os.path.normpath(corpus_abs)  # corpus may be "..": normalize before containment
        cand = os.path.normpath(os.path.join(corpus_norm, cfg["theme"]))
        if os.path.isfile(cand) and cand.startswith(corpus_norm + os.sep):
            theme_abs = cand
            theme_rel = os.path.relpath(cand, path_base).replace(os.sep, "/")
        else:
            print("warning: reader.config.json theme not found in the corpus: %s" % cfg["theme"],
                  file=sys.stderr)

    mode = "provenance" if sum(tot_prov.values()) else ("status" if sum(tot_status.values()) else "none")
    stats = {"mode": mode, "status": tot_status, "provenance": tot_prov,
             "secStatus": sec_status, "secProvenance": sec_prov}

    sitemap = {"title": title, "base": corpus_label, "rootPages": root_pages,
               "sections": section_list, "stats": stats}
    if theme_rel:
        sitemap["theme"] = theme_rel
    return sitemap, theme_abs


def _script_safe_json(value):
    """JSON for embedding inside a <script> block — </script> and HTML-significant
    characters escaped so corpus content (which may contain raw script tags; the demo's
    sanitizer probe does) can never terminate or alter the surrounding document."""
    return (json.dumps(value, ensure_ascii=False)
            .replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e"))


# Bundle order: dependencies first (base, util), the shell last (it boots the app).
_BAKE_MODULES = [
    "components/base.js", "components/util.js",
    "components/cr-ui-diagram-viewer.js", "components/cr-ui-toc.js",
    "components/cr-ui-page.js", "components/cr-ui-nav.js",
    "components/cr-ui-header.js", "components/cr-ui-body.js",
    "components/cr-shell.js",
]


def bake(corpus_root, out_arg, title_override=None):
    """--bake: emit ONE self-contained reader.html that works on file:// (double-click).

    Inlined: the sitemap (as window.CORPUS), every page's raw markdown (window.CORPUS_FILES
    — rendering stays client-side: marked parses, DOMPurify sanitizes, same code path as
    the served reader), the reader CSS (+ the per-corpus theme, preserving the override
    order), and the component modules concatenated into one inline <script type="module">
    (inline modules execute on file://; only fetched modules don't). The render libraries
    stay CDN-pinned + SRI, lifted verbatim from index.html so the pins have one source.
    Relative images keep working when the output sits at the corpus root (the default)."""
    corpus_abs = os.path.abspath(corpus_root.rstrip("/"))
    if not os.path.isdir(corpus_abs):
        sys.exit("error: not a directory: %s" % corpus_root)
    out_path = (os.path.join(corpus_abs, "reader.html")
                if out_arg == os.path.join("lib", "sitemap.json") else os.path.abspath(out_arg))
    out_dir = os.path.dirname(out_path) or "."

    sitemap, theme_abs = collect_sitemap(os.path.basename(corpus_abs), corpus_abs,
                                         out_dir, title_override)

    files = {}
    pages = list(sitemap["rootPages"]) + [p for s in sitemap["sections"] for p in s["pages"]]
    for page in pages:
        full = os.path.normpath(os.path.join(out_dir, page["path"]))
        with open(full, encoding="utf-8", errors="replace") as fh:
            files[page["path"]] = fh.read()

    with open(os.path.join(ROOT, "lib", "corpus-reader.css"), encoding="utf-8") as fh:
        css = fh.read()
    if theme_abs:
        with open(theme_abs, encoding="utf-8") as fh:
            css += "\n\n/* ── per-corpus theme (reader.config.json) ── */\n" + fh.read()
    sitemap.pop("theme", None)  # baked: the theme is inlined, nothing to link

    # The CDN render-library tags, lifted verbatim from index.html — one source for the
    # version pins and their Subresource-Integrity hashes.
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        idx = fh.read()
    cdn_links = re.findall(r"<link[^>]*https://[^>]*>", idx)
    cdn_scripts = re.findall(r'<script src="https://[^>]*></script>', idx)

    parts = []
    for rel in _BAKE_MODULES:
        with open(os.path.join(ROOT, "lib", rel), encoding="utf-8") as fh:
            src = fh.read()
        src = re.sub(r"(?ms)^import\b.*?;[ \t]*$", "", src)            # imports: concatenated instead
        src = re.sub(r"(?m)^export (class|function|const)\b", r"\1", src)
        parts.append("// ── lib/%s ──\n%s" % (rel, src.strip()))
    bundle = "\n\n".join(parts)
    leftover = re.search(r"(?m)^\s*(import|export)\b", bundle)
    if leftover:
        sys.exit("error: bake bundler left an un-stripped module statement: %s" % leftover.group(0).strip())

    title_html = (sitemap["title"] or "Corpus").replace("&", "&amp;").replace("<", "&lt;")
    html = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\" />\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
        "<title>%s</title>\n"
        "<!-- Baked by build-sitemap.py --bake: self-contained, works on file://. Re-bake after corpus edits. -->\n"
        "<style>\n%s\n</style>\n"
        "%s\n"
        "</head>\n<body>\n<cr-shell></cr-shell>\n"
        "%s\n"
        "<script>\nwindow.CORPUS = %s;\nwindow.CORPUS_FILES = %s;\n</script>\n"
        "<script type=\"module\">\n%s\n</script>\n"
        "</body>\n</html>\n"
    ) % (title_html, css, "\n".join(cdn_links), "\n".join(cdn_scripts),
         _script_safe_json(sitemap), _script_safe_json(files), bundle)

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("baked %s — %d page(s), %d section(s), %d bytes; double-click to open (file:// works)"
          % (out_path, len(pages), len(sitemap["sections"]), len(html)))


def scaffold_site(corpus_root):
    """The common `<corpus>/site/` convention: copy this reader (machinery only — never a
    bundled example corpus) into `<corpus_root>/site/` and build its sitemap. Shared by
    every plugin's corpus-export command so the generated layout is identical everywhere."""
    corpus_root = os.path.abspath(corpus_root.rstrip("/"))
    if not os.path.isdir(corpus_root):
        sys.exit("error: not a directory: %s" % corpus_root)
    site = os.path.join(corpus_root, "site")
    os.makedirs(site, exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "index.html"), os.path.join(site, "index.html"))
    shutil.copy2(os.path.join(ROOT, "build-sitemap.py"), os.path.join(site, "build-sitemap.py"))
    lib_dst = os.path.join(site, "lib")
    if os.path.isdir(lib_dst):
        shutil.rmtree(lib_dst)
    shutil.copytree(os.path.join(ROOT, "lib"), lib_dst, ignore=shutil.ignore_patterns("sitemap.json"))
    subprocess.run([sys.executable, "build-sitemap.py", ".."], cwd=site, check=True)
    # Drop a redirect at the corpus root (only if nothing is there), so serving the root
    # and opening / lands in the reader instead of a 404 — never overwrites a user's file.
    root_index = os.path.join(corpus_root, "index.html")
    if not os.path.exists(root_index):
        try:
            with open(os.path.join(site, "lib", "sitemap.json"), encoding="utf-8") as fh:
                title = json.load(fh).get("title", "Corpus")
        except (OSError, ValueError):
            title = "Corpus"
        with open(root_index, "w", encoding="utf-8") as fh:
            fh.write('<!doctype html>\n<meta charset="utf-8">\n<title>%s</title>\n'
                     '<meta http-equiv="refresh" content="0; url=site/">\n'
                     '<script>location.replace("site/");</script>\n'
                     '<p>Redirecting to the <a href="site/">corpus reader</a>…</p>\n'
                     % title.replace("<", "&lt;"))
        print("wrote %s (redirect → site/)" % root_index)
    print("scaffolded %s/site/ — serve the corpus root and open /site/" % corpus_root)


def main():
    ap = argparse.ArgumentParser(description="Generate lib/sitemap.json for the corpus-reader.")
    ap.add_argument("corpus", nargs="?", default=None, help="corpus directory (default: auto-detect)")
    ap.add_argument("--out", default=os.path.join("lib", "sitemap.json"), help="output path (default: lib/sitemap.json)")
    ap.add_argument("--title", default=None, help="corpus title (default: root README H1, else dir name)")
    ap.add_argument("--init", metavar="CORPUS_ROOT", default=None,
                    help="scaffold CORPUS_ROOT/site/ with this reader (machinery only) + build its sitemap — the common <corpus>/site/ layout")
    ap.add_argument("--bake", metavar="CORPUS_ROOT", default=None,
                    help="emit ONE self-contained reader.html beside the corpus (works on file:// — double-click); --out overrides the output path")
    args = ap.parse_args()

    if args.init is not None:
        scaffold_site(args.init)
        return
    if args.bake is not None:
        bake(args.bake, args.out, args.title)
        return

    corpus = args.corpus
    if not corpus:
        candidates = find_corpus(ROOT)
        if len(candidates) == 1:
            corpus = candidates[0]
        elif not candidates:
            sys.exit("error: no corpus directory with .md files found — pass one explicitly")
        else:
            sys.exit("error: multiple corpus dirs found (%s) — pass one explicitly" % ", ".join(candidates))

    corpus = corpus.rstrip("/")
    corpus_abs = os.path.join(ROOT, corpus)
    if not os.path.isdir(corpus_abs):
        sys.exit("error: not a directory: %s" % corpus)

    sitemap, _theme_abs = collect_sitemap(corpus, corpus_abs, ROOT, args.title)
    root_pages, section_list, title = sitemap["rootPages"], sitemap["sections"], sitemap["title"]

    out_path = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(sitemap, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    pages = len(root_pages) + sum(len(s["pages"]) for s in section_list)
    print("wrote %s — %d page(s), %d section(s), title=%r" % (args.out, pages, len(section_list), title))


def selftest():
    """Exercise the mechanized substrate (frontmatter/heading/summary/prettify/tree-nesting),
    collect_sitemap end-to-end on a small fixture corpus, --bake against the REAL bundled
    references/corpus-reader/ assets (the exact ROOT this script now resolves to post-move),
    --init's site/ scaffold, and negative controls: an empty corpus and a non-directory target
    must fail loudly (SystemExit), never silently succeed. Exit 0 = pass, 1 = fail."""
    import shutil
    import tempfile
    fails = []

    def expect(cond, msg):
        if not cond:
            fails.append(msg)

    # --- unit-level: the parsing/formatting substrate ---------------------------------------
    meta, body = split_frontmatter('---\ntitle: Hello\nstatus: active\n---\n# Hi\nbody text\n')
    expect(meta == {"title": "Hello", "status": "active"}, f"split_frontmatter mis-parsed: {meta}")
    expect(body.strip() == "# Hi\nbody text", f"split_frontmatter left the wrong body: {body!r}")
    no_meta, no_body = split_frontmatter("# Just a doc\nno frontmatter here\n")
    expect(no_meta == {}, "split_frontmatter invented metadata with no leading --- block")
    expect(no_body == "# Just a doc\nno frontmatter here\n", "split_frontmatter mangled a doc with no frontmatter")

    expect(first_heading("intro\n# Real Title\nmore\n") == "Real Title", "first_heading missed the H1")
    expect(first_heading("no headings here\n") is None, "first_heading invented a heading")

    summary = first_paragraph("# Title\n\nThis is the real summary paragraph, plain and simple.\n\nSecond para ignored.\n")
    expect(summary == "This is the real summary paragraph, plain and simple.",
           f"first_paragraph picked the wrong text: {summary!r}")
    fenced = first_paragraph("# T\n\n```\ncode, not prose\n```\n\nActual prose paragraph here.\n")
    expect(fenced == "Actual prose paragraph here.", f"first_paragraph did not skip a fenced code block: {fenced!r}")

    expect(prettify("03-roadmap") == "Roadmap", f"prettify did not strip the numeric prefix: {prettify('03-roadmap')!r}")
    expect(prettify("the-position.md") == "The position", f"prettify mishandled a filename: {prettify('the-position.md')!r}")
    expect(section_order("01-foundation") == 1 and section_order("no-number") == 9999,
           "section_order did not rank numbered-first, unnumbered-last")
    expect(norm_status("Needs work") == "needed" and norm_status("Active") == "active" and norm_status(None) == "",
           "norm_status bucketing is wrong")
    expect(is_readme("00-README.md") and is_readme("readme.md") and not is_readme("guide.md"),
           "is_readme did not recognize the README aliases")

    # build_tree: a subfolder README is promoted to the group's label; a flat entry stays a leaf
    entries = [
        (["intro.md"], {"path": "01-foundation/intro.md", "title": "Intro"}),
        (["sub", "00-README.md"], {"path": "01-foundation/sub/00-README.md", "title": "Sub"}),
        (["sub", "detail.md"], {"path": "01-foundation/sub/detail.md", "title": "Detail"}),
    ]
    tree = build_tree(entries)
    kinds = {c["type"] for c in tree}
    expect(kinds == {"doc", "group"}, f"build_tree did not produce one doc + one group at top level: {tree}")
    group = next(c for c in tree if c["type"] == "group")
    expect(group.get("doc") == "01-foundation/sub/00-README.md", "build_tree did not promote the subfolder README to the group's doc")
    expect(any(c["type"] == "doc" and c["path"].endswith("detail.md") for c in group["children"]),
           "build_tree lost the non-README leaf inside the promoted group")

    # --- collect_sitemap end-to-end on a small fixture corpus -------------------------------
    d = tempfile.mkdtemp(prefix="build-sitemap-selftest-")
    try:
        os.makedirs(os.path.join(d, "01-foundation"))
        os.makedirs(os.path.join(d, "02-voice"))
        open(os.path.join(d, "01-foundation", "position.md"), "w", encoding="utf-8").write(
            "---\ntitle: The Position\nstatus: active\n---\n# The Position\n\nQuiet confidence, made ownable. [KNOWN]\n")
        open(os.path.join(d, "02-voice", "tone.md"), "w", encoding="utf-8").write(
            "# Tone\n\nDirect, warm, a little dry.\n")
        sitemap, theme_abs = collect_sitemap("corpus", d, d)
        expect(theme_abs is None, "collect_sitemap invented a theme with no reader.config.json")
        secs = {s["id"]: s for s in sitemap["sections"]}
        expect(set(secs) == {"01-foundation", "02-voice"}, f"collect_sitemap missed a section: {set(secs)}")
        expect(secs["01-foundation"]["pages"][0]["title"] == "The Position", "collect_sitemap lost the frontmatter title")
        expect(secs["01-foundation"]["pages"][0].get("status") == "active", "collect_sitemap lost the frontmatter status")
        expect(sitemap["stats"]["mode"] == "provenance", f"collect_sitemap did not detect provenance markers: {sitemap['stats']}")
        expect(sitemap["stats"]["provenance"].get("known") == 1, "collect_sitemap miscounted the [KNOWN] marker")
        # negative control: an empty corpus dir must fail loudly, not return an empty-but-clean sitemap
        empty = os.path.join(d, "empty")
        os.makedirs(empty)
        try:
            collect_sitemap("empty", empty, empty)
            expect(False, "collect_sitemap on an empty corpus did not raise (silent success on no content)")
        except SystemExit as e:
            expect("no .md files" in str(e), f"empty-corpus SystemExit had the wrong message: {e}")

        # --- --bake against the REAL bundled corpus-reader assets (this script's actual ROOT) ---
        out_html = os.path.join(d, "reader.html")
        bake(d, out_html)
        expect(os.path.isfile(out_html), "--bake did not write reader.html")
        html = open(out_html, encoding="utf-8").read()
        expect("window.CORPUS" in html and "window.CORPUS_FILES" in html, "baked reader.html is missing the inlined sitemap/files")
        expect("Quiet confidence" in html, "baked reader.html did not inline the page content")
        expect("<script type=\"module\">" in html, "baked reader.html is missing the inlined module bundle")
        # bake() itself sys.exits on a leftover top-of-line import/export in the concatenated
        # bundle (its own internal invariant) — reaching this line at all is that check passing.
        # negative control: baking a non-directory must fail loudly
        try:
            bake(os.path.join(d, "does-not-exist"), out_html)
            expect(False, "bake on a non-directory did not raise")
        except SystemExit:
            pass

        # --- --init: scaffold <corpus>/site/ from the real reader assets -------------------
        scaffold_site(d)
        site = os.path.join(d, "site")
        expect(os.path.isfile(os.path.join(site, "index.html")), "--init did not copy index.html into site/")
        expect(os.path.isfile(os.path.join(site, "lib", "sitemap.json")), "--init did not build site/lib/sitemap.json")
        expect(os.path.isfile(os.path.join(d, "index.html")), "--init did not drop a corpus-root redirect index.html")
        redirect = open(os.path.join(d, "index.html"), encoding="utf-8").read()
        expect("site/" in redirect, "--init's corpus-root redirect does not point at site/")
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # --- XSS-safety: _script_safe_json must neutralize a raw </script> in corpus content -----
    escaped = _script_safe_json({"x": "</script><img onerror=alert(1)>"})
    expect("</script>" not in escaped and "\\u003c" in escaped, "_script_safe_json did not neutralize a raw </script>")

    if fails:
        sys.stderr.write("build-sitemap selftest: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("build-sitemap selftest: OK (frontmatter/heading/summary/prettify/tree-nesting correct; "
          "collect_sitemap builds sections + stats from a fixture corpus and refuses an empty one; "
          "--bake inlines real content from the bundled references/corpus-reader/ assets with no leftover "
          "module statements; --init scaffolds site/ + a root redirect; a non-directory --bake target raises; "
          "_script_safe_json neutralizes a raw </script>)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
