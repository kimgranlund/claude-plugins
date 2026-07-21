#!/usr/bin/env python3
"""inventory-scan.py — the check-whole-ui Step-1 inventory mechanizer. Self-contained (stdlib only).

The audit's spine is the inventory: screens/routes, flows, shared modules. Hand-building it is
slow and samples; this scan makes it MECHANIZED where the source tree is available. It is static,
deterministic, and ASSISTED — heuristics over source text, not a parse of the running app — so the
output is a draft the auditor confirms, never gospel. Confirm module identities before grading.

  python3 inventory-scan.py <src-root> [--manifest manifest.json] [--out inventory.json]
  python3 inventory-scan.py selftest

What it extracts (heuristics, each honest about its reach):

  Screens/routes — three detectors:
    - hash routes: any '#/x' string literal (hash-router registrations AND hash hrefs both name
      a screen; a hash target nobody renders is a finding for the audit, not for this scan).
    - path-literal route registrations/navigations: route('/x', h) · addRoute · registerRoute ·
      navigate('/x') · go/push/redirect('/x') · <Route path="/x">.
    - file-per-view conventions: files under **/views|pages|routes|screens/ (js/jsx/ts/tsx/vue/
      svelte/html) — one screen per file, id from the stem, no route claimed.
    Each screen: {id, route?, file, verbs, source}.

  Modules (the shared-cluster detection; threshold: used in >= 2 distinct screen FILES):
    - custom-element tags (<x-chip>)                       -> kind "element"
    - imported UI components (import ... from a path containing /components/ or /ui/)
                                                           -> kind "component"
    - repeated structural classname families (class="card-*": tokens grouped by their first-dash
      prefix; a family needs >= 2 distinct member classes)  -> kind "classname"
    Each module: {id, kind, usedBy: [screen ids], source}.

  Verbs — per screen file, event bindings counted by type:
    addEventListener('type') (any type) · on<event>= HTML attrs · on<Event>= JSX · @click / v-on:
    Vue (attr/JSX/Vue forms filtered to a known-event allowlist so 'online=' noise stays out).
    Each screen gains verbs: [{type, count}].

  Manifest merge (--manifest): the auditor declares what heuristics can't see —
    {"screens": [...], "flows": [...], "modules": [...]}. Flows are DECLARED-ONLY, never guessed.
    Every entry carries source: "scanned" | "declared" | "scanned+declared" (declared keys fill
    gaps on a scanned match; scanned facts win).

  Honesty metadata — meta: {scanned_files, unmatched_route_hints[], collisions[]}: path hrefs
    (href="/x") whose target matches no known screen route — links into rooms nobody built. A scan
    that found nothing emits an honest empty inventory, not an invented one.

  Collision guard: a route detector and the file-per-view detector can independently produce the
    SAME slug for the SAME logical screen (e.g. hash route '#/statement' and file views/statement.ts
    both slug to 'statement') — but the route detector's "file" attribution is just "wherever the
    route string literal lives" (often a router/app file, NOT the real view). Confirmed real-world:
    this silently discarded the real view file for 7 of 12 screens in one app, with no warning, and
    compounded into wrong verb counts + understated module-reuse spread (verbs/modules are computed
    against the "file" field). Fix: when the file-per-view detector reaches an id already claimed by
    a route detector, it CORRECTS the file attribution to the real view file (never silently
    no-ops) and records the correction in meta.collisions[]. When two DISTINCT view files slug to
    the same id (a genuine ambiguity, not a same-screen correction), the second is disambiguated —
    suffixed with its parent-directory slug (`settings` + `src/views/admin/` -> `settings-admin`) —
    so neither is silently dropped; also recorded in meta.collisions[]. Never a silent overwrite.

Output (inventory.json — the shape ui-probe.mjs consumes via --inventory):
  {"screens": [...], "flows": [...], "modules": [...],
   "meta": {"src_root", "scanned_files", "unmatched_route_hints", "mode": "assisted-static"}}

Python 3.8+.
"""
import json
import os
import re
import sys
import tempfile

CODE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".html", ".htm"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "out", "vendor", "coverage",
             ".next", ".cache", ".svelte-kit", "__pycache__"}
VIEW_DIRS = {"views", "pages", "routes", "screens"}

HASH_ROUTE_RE = re.compile(r"""["'`](#/[A-Za-z0-9_\-/:.]*)["'`]""")
PATH_CALL_RE = re.compile(
    r"""\b(?:route|addRoute|registerRoute|navigate|go|push|redirect)\s*\(\s*["'`](/[A-Za-z0-9_\-/:.]*)["'`]""")
JSX_ROUTE_RE = re.compile(r"""<Route\b[^>]*\bpath\s*=\s*\{?["'](/[^"'}]*)["']""")
HREF_RE = re.compile(r"""\bhref\s*=\s*["'](/[A-Za-z0-9_\-/:.]*)["']""")
CUSTOM_EL_RE = re.compile(r"<([a-z][a-z0-9]*(?:-[a-z0-9]+)+)[\s/>]")
IMPORT_RE = re.compile(
    r"""import\s+(?:\{([^}]*)\}|([A-Za-z_$][\w$]*))\s+from\s+["']([^"']+)["']""")
CLASS_RE = re.compile(r"""\bclass(?:Name)?\s*=\s*["']([^"']+)["']""")

# addEventListener accepts any type (it is explicit); the attribute/JSX/Vue forms are filtered to
# a known-event allowlist so prose like 'online=' or 'onion=' never becomes a verb.
LISTENER_RE = re.compile(r"""addEventListener\(\s*["']([a-z]+)["']""")
ATTR_EVENT_RE = re.compile(r"""(?<![\w.$])on([a-z]{3,})\s*=""")
JSX_EVENT_RE = re.compile(r"""(?<![\w.$])on([A-Z][A-Za-z]+)\s*=""")
VUE_EVENT_RES = (re.compile(r"""@([a-z]+)\s*="""), re.compile(r"""v-on:([a-z]+)"""))
KNOWN_EVENTS = {
    "click", "dblclick", "contextmenu", "input", "change", "submit", "reset", "invalid",
    "keydown", "keyup", "keypress", "focus", "blur", "focusin", "focusout",
    "pointerdown", "pointerup", "pointermove", "pointerenter", "pointerleave", "pointercancel",
    "mousedown", "mouseup", "mousemove", "mouseover", "mouseout", "mouseenter", "mouseleave",
    "touchstart", "touchend", "touchmove", "touchcancel", "wheel", "scroll", "select",
    "dragstart", "dragend", "dragover", "dragenter", "dragleave", "drop",
    "load", "error", "toggle", "close", "open", "paste", "copy", "cut",
}


def _slug(route):
    """'#/x/y' -> 'x-y'; '/' -> 'root'."""
    s = route.lstrip("#").strip("/")
    s = re.sub(r"[/:.]+", "-", s).strip("-")
    return s or "root"


def _walk_files(src_root):
    files = []
    for dp, dns, fns in os.walk(src_root):
        dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(fns):
            if os.path.splitext(fn)[1].lower() in CODE_EXTS:
                files.append(os.path.join(dp, fn))
    return files


def scan(src_root):
    """Scan a source tree. Returns the inventory dict (screens/flows/modules/meta)."""
    files = _walk_files(src_root)
    texts = {}
    for fp in files:
        try:
            with open(fp, encoding="utf-8", errors="ignore") as fh:
                texts[fp] = fh.read()
        except OSError:
            texts[fp] = ""

    screens = {}  # id -> screen dict
    href_hints = set()
    collisions = []  # honesty metadata: every id collision the scan had to resolve, never silent

    def add_screen(sid, route, fp):
        rel = os.path.relpath(fp, src_root)
        if sid in screens:
            if route and not screens[sid].get("route"):
                screens[sid]["route"] = route
            return
        entry = {"id": sid, "file": rel, "source": "scanned", "_file_kind": "route"}
        if route:
            entry["route"] = route
        screens[sid] = entry

    # --- screens: hash routes + path-literal registrations/navigations + <Route path> -----------
    for fp, text in texts.items():
        for m in HASH_ROUTE_RE.finditer(text):
            add_screen(_slug(m.group(1)), m.group(1), fp)
        for m in PATH_CALL_RE.finditer(text):
            add_screen(_slug(m.group(1)), m.group(1), fp)
        for m in JSX_ROUTE_RE.finditer(text):
            add_screen(_slug(m.group(1)), m.group(1), fp)
        for m in HREF_RE.finditer(text):
            href_hints.add(m.group(1))

    # --- screens: file-per-view convention -------------------------------------------------------
    def _disambiguate(base_sid, rel):
        parent = os.path.basename(os.path.dirname(rel)) or "root"
        candidate = "%s-%s" % (base_sid, _slug(parent))
        n = 2
        while candidate in screens:
            candidate = "%s-%s-%d" % (base_sid, _slug(parent), n)
            n += 1
        return candidate

    for fp in files:
        rel = os.path.relpath(fp, src_root)
        parts = rel.split(os.sep)
        if len(parts) >= 2 and any(p in VIEW_DIRS for p in parts[:-1]):
            stem = os.path.splitext(parts[-1])[0]
            if stem == "index":
                stem = parts[-2] if parts[-2] not in VIEW_DIRS else "index"
            sid = _slug(stem)
            if sid in screens and screens[sid].get("file") != rel:
                existing = screens[sid]
                if existing.get("_file_kind") == "route":
                    # A route detector's "file" is just "wherever the route string literal
                    # lives" (often a router/app file) — NOT authoritative over a real view
                    # file. Correct the attribution rather than silently keeping the wrong one
                    # (the confirmed real-world bug: this used to no-op via setdefault()).
                    collisions.append({
                        "id": sid, "kept_file": rel, "dropped_file": existing["file"],
                        "reason": "route-detector file attribution corrected to the conventional view file",
                    })
                    existing["file"] = rel
                    existing["_file_kind"] = "view"
                else:
                    # Two DISTINCT view files slug to the same id — a genuine collision between
                    # two different screens. Disambiguate so neither is silently dropped.
                    new_sid = _disambiguate(sid, rel)
                    collisions.append({
                        "id": sid, "kept_file": existing["file"], "disambiguated_as": new_sid,
                        "disambiguated_file": rel,
                        "reason": "two distinct view files slug to the same id",
                    })
                    screens[new_sid] = {"id": new_sid, "file": rel, "source": "scanned", "_file_kind": "view"}
            elif sid not in screens:
                screens[sid] = {"id": sid, "file": rel, "source": "scanned", "_file_kind": "view"}

    # --- verbs: per screen file ------------------------------------------------------------------
    verbs_by_file = {}
    screen_files = {s["file"] for s in screens.values() if s.get("file")}
    for rel in screen_files:
        text = texts.get(os.path.join(src_root, rel), "")
        counts = {}
        for m in LISTENER_RE.finditer(text):
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
        for regex, lower in ((ATTR_EVENT_RE, True), (JSX_EVENT_RE, True)):
            for m in regex.finditer(text):
                t = m.group(1).lower() if lower else m.group(1)
                if t in KNOWN_EVENTS:
                    counts[t] = counts.get(t, 0) + 1
        for regex in VUE_EVENT_RES:
            for m in regex.finditer(text):
                if m.group(1) in KNOWN_EVENTS:
                    counts[m.group(1)] = counts.get(m.group(1), 0) + 1
        verbs_by_file[rel] = [{"type": t, "count": c}
                              for t, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    for s in screens.values():
        s["verbs"] = verbs_by_file.get(s.get("file"), [])

    # --- modules: clusters used in >= 2 distinct screen files ------------------------------------
    screens_by_file = {}
    for s in screens.values():
        screens_by_file.setdefault(s.get("file"), []).append(s["id"])

    el_files, comp_files, cls_files, cls_members = {}, {}, {}, {}
    for rel in screen_files:
        text = texts.get(os.path.join(src_root, rel), "")
        for m in CUSTOM_EL_RE.finditer(text):
            el_files.setdefault(m.group(1), set()).add(rel)
        for m in IMPORT_RE.finditer(text):
            named, default, path_ = m.group(1), m.group(2), m.group(3)
            if not ("/components/" in path_ or "/ui/" in path_
                    or path_.startswith(("components/", "ui/"))):
                continue
            names = ([n.strip().split(" as ")[-1].strip() for n in named.split(",") if n.strip()]
                     if named else [default])
            for name in names:
                if name:
                    comp_files.setdefault(name, set()).add(rel)
        for m in CLASS_RE.finditer(text):
            for token in m.group(1).split():
                if "-" not in token or token.startswith("-"):
                    continue
                fam = token.split("-", 1)[0] + "-*"
                cls_files.setdefault(fam, set()).add(rel)
                cls_members.setdefault(fam, set()).add(token)

    modules = []

    def used_by(file_set):
        ids = set()
        for rel in file_set:
            ids.update(screens_by_file.get(rel, []))
        return sorted(ids)

    for tag, fset in sorted(el_files.items()):
        if len(fset) >= 2:
            modules.append({"id": tag, "kind": "element", "usedBy": used_by(fset),
                            "source": "scanned"})
    for name, fset in sorted(comp_files.items()):
        if len(fset) >= 2:
            modules.append({"id": name, "kind": "component", "usedBy": used_by(fset),
                            "source": "scanned"})
    for fam, fset in sorted(cls_files.items()):
        if len(fset) >= 2 and len(cls_members.get(fam, ())) >= 2:
            modules.append({"id": fam, "kind": "classname", "usedBy": used_by(fset),
                            "source": "scanned"})

    # --- honesty metadata -------------------------------------------------------------------------
    known_routes = {s.get("route") for s in screens.values() if s.get("route")}
    unmatched = sorted(h for h in href_hints if h not in known_routes)

    for s in screens.values():
        s.pop("_file_kind", None)  # internal bookkeeping only — never leaks into the output

    return {
        "screens": sorted(screens.values(), key=lambda s: s["id"]),
        "flows": [],  # declared-only: flows come from --manifest, never from a guess
        "modules": modules,
        "meta": {"src_root": os.path.abspath(src_root), "scanned_files": len(files),
                 "unmatched_route_hints": unmatched, "collisions": collisions,
                 "mode": "assisted-static", "tool": "inventory-scan.py"},
    }


def merge_manifest(inv, manifest):
    """Merge auditor-declared screens/flows/modules into a scanned inventory.

    Declared-only entries get source "declared"; a declared entry matching a scanned one (by id,
    or by route for screens) fills the scanned entry's missing keys and marks it
    "scanned+declared" — scanned facts always win over declared ones."""
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object with screens/flows/modules lists")

    def merge_list(inv_list, decl_list, match_keys):
        for decl in decl_list or []:
            if not isinstance(decl, dict):
                raise ValueError("manifest entries must be objects, got %r" % (decl,))
            hit = None
            for entry in inv_list:
                if any(decl.get(k) is not None and decl.get(k) == entry.get(k)
                       for k in match_keys):
                    hit = entry
                    break
            if hit is not None:
                for k, v in decl.items():
                    hit.setdefault(k, v)
                hit["source"] = "scanned+declared"
            else:
                entry = dict(decl)
                entry["source"] = "declared"
                inv_list.append(entry)

    merge_list(inv["screens"], manifest.get("screens"), ("id", "route"))
    merge_list(inv["modules"], manifest.get("modules"), ("id",))
    for flow in manifest.get("flows") or []:
        if not isinstance(flow, dict):
            raise ValueError("manifest flows must be objects, got %r" % (flow,))
        entry = dict(flow)
        entry["source"] = "declared"
        inv["flows"].append(entry)
    return inv


# --- selftest fixtures ---------------------------------------------------------------------------
# A hash-router app: two hash routes + one path registration, event listeners, one dead path href.
FIXTURE_HASH = {
    "app.js": """
const routes = {
  '#/home': renderHome,
  '#/settings': renderSettings,
};
route('/about', renderAbout);
function bind() {
  document.getElementById('save').addEventListener('click', onSave);
  window.addEventListener('keydown', onKey);
}
const nav = `<a href="/about">about</a><a href="/ghost">ghost</a>`;
""",
}
# Component reuse across two view files: a custom element, an imported component, a classname
# family — each in >= 2 screen files. lone.js's <x-once> appears in ONE file: not a module.
FIXTURE_VIEWS = {
    os.path.join("src", "views", "dashboard.js"): """
import { DataTable } from '../components/table.js';
import Chart from '../ui/chart.js';
export function render() {
  return `<section class="card-header card-body"><x-chip label="a"></x-chip></section>`;
}
root.addEventListener('click', open);
""",
    os.path.join("src", "views", "reports.js"): """
import { DataTable } from '../components/table.js';
export const view = `<div class="card-footer"><x-chip label="b"></x-chip>
  <button onclick="save()">save</button></div>`;
form.addEventListener('submit', save);
""",
    os.path.join("src", "views", "lone.js"): """
export const v = `<x-once></x-once>`;
""",
    os.path.join("src", "components", "table.js"): """
export class DataTable {}
""",
}
# A manifest declaring a flow (declared-only), a new screen, and a re-declaration of a scanned one.
FIXTURE_MANIFEST = {
    "screens": [{"id": "admin", "route": "#/admin"}, {"id": "home", "note": "landing"}],
    "flows": [{"id": "onboarding", "steps": ["home", "settings"]}],
}
# A tree with no routes at all: the honest result is EMPTY, never invented.
FIXTURE_EMPTY = {
    "util.js": "export const clamp = (v, a, b) => Math.min(b, Math.max(a, v));\n",
}
# Route-file-vs-view-file collision (the confirmed real-world bug): a hash route '#/dashboard' in
# a router file slugs to 'dashboard', and views/dashboard.js ALSO slugs to 'dashboard' — the SAME
# logical screen. The route detector runs first and claims "file": app.js (wherever the route
# string lives, not the real view); the file-per-view detector must CORRECT that attribution, not
# silently no-op (the old setdefault() bug), and record the correction in meta.collisions[].
FIXTURE_COLLISION = {
    "app.js": "const routes = { '#/dashboard': renderDashboard };\n",
    os.path.join("src", "views", "dashboard.js"): """
export function render() { return `<h1>Dashboard</h1>`; }
document.addEventListener('click', onClick);
""",
}
# Two DISTINCT view files slug to the same id ('settings') — a genuine ambiguity between two
# different screens, not a same-screen correction. Both must survive (disambiguated), never a
# silent drop of the second.
FIXTURE_DISTINCT_COLLISION = {
    os.path.join("src", "views", "admin", "settings.js"): "export const a = 1;\n",
    os.path.join("src", "views", "user", "settings.js"): "export const b = 2;\n",
}


def _write_tree(root, tree):
    for rel, content in tree.items():
        fp = os.path.join(root, rel)
        os.makedirs(os.path.dirname(fp) or root, exist_ok=True)
        with open(fp, "w", encoding="utf-8") as fh:
            fh.write(content)


def selftest():
    errs = []

    def screen(inv, sid):
        return next((s for s in inv["screens"] if s["id"] == sid), None)

    def module(inv, mid):
        return next((m for m in inv["modules"] if m["id"] == mid), None)

    # --- 1. hash-router app: routes, verbs, unmatched href hints ------------------------------
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_HASH)
        inv = scan(td)
        ids = {s["id"] for s in inv["screens"]}
        if ids != {"home", "settings", "about"}:
            errs.append("hash fixture screens wrong: %s (expected home/settings/about)" % sorted(ids))
        h = screen(inv, "home")
        if not h or h.get("route") != "#/home" or h.get("source") != "scanned":
            errs.append("hash fixture: '#/home' screen wrong: %r" % (h,))
        if not screen(inv, "about") or screen(inv, "about").get("route") != "/about":
            errs.append("hash fixture: route('/about') registration not extracted")
        verbs = {v["type"]: v["count"] for v in (h or {}).get("verbs", [])}
        if verbs.get("click") != 1 or verbs.get("keydown") != 1:
            errs.append("hash fixture verbs wrong: %r (expected click:1 keydown:1)" % verbs)
        if inv["meta"]["unmatched_route_hints"] != ["/ghost"]:
            errs.append("unmatched href '/ghost' not reported: %r"
                        % inv["meta"]["unmatched_route_hints"])
        if inv["meta"]["scanned_files"] != 1:
            errs.append("hash fixture scanned_files != 1: %r" % inv["meta"]["scanned_files"])
        if inv["flows"]:
            errs.append("flows must never be guessed from a scan: %r" % inv["flows"])

    # --- 2. component reuse: element/component/classname modules at the >=2-files threshold ----
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_VIEWS)
        inv = scan(td)
        ids = {s["id"] for s in inv["screens"]}
        if not {"dashboard", "reports", "lone"} <= ids:
            errs.append("view-file screens missing: %s" % sorted(ids))
        el = module(inv, "x-chip")
        if not el or el["kind"] != "element" or el["usedBy"] != ["dashboard", "reports"]:
            errs.append("x-chip element module wrong: %r" % (el,))
        comp = module(inv, "DataTable")
        if not comp or comp["kind"] != "component" or comp["usedBy"] != ["dashboard", "reports"]:
            errs.append("DataTable component module wrong: %r" % (comp,))
        fam = module(inv, "card-*")
        if not fam or fam["kind"] != "classname" or fam["usedBy"] != ["dashboard", "reports"]:
            errs.append("card-* classname family wrong: %r" % (fam,))
        if module(inv, "x-once"):
            errs.append("x-once (one file) must not clear the >=2-screen-files threshold")
        if module(inv, "Chart"):
            errs.append("Chart (imported in one file) must not clear the threshold")
        d_verbs = {v["type"]: v["count"] for v in screen(inv, "dashboard")["verbs"]}
        r_verbs = {v["type"]: v["count"] for v in screen(inv, "reports")["verbs"]}
        if d_verbs.get("click") != 1:
            errs.append("dashboard verbs wrong: %r" % d_verbs)
        if r_verbs.get("submit") != 1 or r_verbs.get("click") != 1:
            errs.append("reports verbs wrong (expected submit:1 + onclick attr click:1): %r" % r_verbs)

    # --- 3. manifest merge: declared flows/screens, scanned+declared on collision --------------
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_HASH)
        inv = merge_manifest(scan(td), FIXTURE_MANIFEST)
        adm = screen(inv, "admin")
        if not adm or adm.get("source") != "declared" or adm.get("route") != "#/admin":
            errs.append("declared screen 'admin' wrong: %r" % (adm,))
        h = screen(inv, "home")
        if not h or h.get("source") != "scanned+declared" or h.get("note") != "landing":
            errs.append("scanned+declared merge on 'home' wrong: %r" % (h,))
        if h and h.get("route") != "#/home":
            errs.append("declared keys must not overwrite scanned facts: %r" % (h,))
        if len(inv["flows"]) != 1 or inv["flows"][0].get("source") != "declared" \
                or inv["flows"][0].get("id") != "onboarding":
            errs.append("declared flow wrong: %r" % (inv["flows"],))

    # --- 4. no-routes tree: an honest empty inventory, not an invented one ---------------------
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_EMPTY)
        inv = scan(td)
        if inv["screens"] or inv["modules"] or inv["flows"]:
            errs.append("no-routes tree must yield empty screens/modules/flows: %d/%d/%d"
                        % (len(inv["screens"]), len(inv["modules"]), len(inv["flows"])))
        if inv["meta"]["scanned_files"] != 1 or inv["meta"]["unmatched_route_hints"]:
            errs.append("no-routes tree meta wrong: %r" % (inv["meta"],))
        if inv["meta"].get("collisions") != []:
            errs.append("a collision-free scan must report an empty collisions[], not omit it: %r"
                        % (inv["meta"].get("collisions"),))

    # --- 5. route-file-vs-view-file collision: the real view file must survive, not be dropped -
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_COLLISION)
        inv = scan(td)
        d = screen(inv, "dashboard")
        want_file = os.path.join("src", "views", "dashboard.js")
        if not d or d.get("file") != want_file:
            errs.append("route-file-vs-view-file collision: the real view file was NOT preserved "
                        "(the confirmed real-world silent-drop bug): %r" % (d,))
        if not d or d.get("route") != "#/dashboard":
            errs.append("collision correction must not drop the route: %r" % (d,))
        if "_file_kind" in (d or {}):
            errs.append("internal _file_kind bookkeeping must never leak into the output: %r" % (d,))
        if not inv["meta"].get("collisions"):
            errs.append("a route/view collision must be reported in meta.collisions[], never silent")
        verbs = {v["type"]: v["count"] for v in (d or {}).get("verbs", [])}
        if verbs.get("click") != 1:
            errs.append("collision-corrected screen must compute verbs against the REAL view "
                        "file, not the router file: %r" % (verbs,))

    # --- 6. two distinct view files colliding on the same slug: BOTH must survive ---------------
    with tempfile.TemporaryDirectory() as td:
        _write_tree(td, FIXTURE_DISTINCT_COLLISION)
        inv = scan(td)
        settings_screens = [s for s in inv["screens"]
                            if s["id"] == "settings" or s["id"].startswith("settings-")]
        if len(settings_screens) != 2:
            errs.append("two distinct view files colliding on 'settings' must BOTH survive "
                        "(disambiguated), never one silently dropped: %r" % (settings_screens,))
        files_seen = {s["file"] for s in settings_screens}
        want_files = {os.path.join("src", "views", "admin", "settings.js"),
                      os.path.join("src", "views", "user", "settings.js")}
        if files_seen != want_files:
            errs.append("distinct-file collision disambiguation lost a real file: %r (wanted %r)"
                        % (files_seen, want_files))
        if not inv["meta"].get("collisions"):
            errs.append("a distinct-file collision must be reported in meta.collisions[], never silent")

    # --- 7. malformed manifest -> clean error, not a crash -------------------------------------
    try:
        merge_manifest({"screens": [], "flows": [], "modules": [], "meta": {}}, ["not", "a", "dict"])
        errs.append("malformed manifest (a list) did not raise ValueError")
    except ValueError:
        pass

    return errs


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("inventory-scan: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("inventory-scan: OK — hash/path/view-file screens + module clustering + verbs + "
              "manifest merge + honest-empty + collision guard (route-vs-view correction, "
              "distinct-file disambiguation) verified over embedded fixtures")
        return 0

    src_root, manifest_path, out_path = None, None, "inventory.json"
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--manifest":
            if not args:
                sys.stderr.write("--manifest needs a path\n")
                return 2
            manifest_path = args.pop(0)
        elif a == "--out":
            if not args:
                sys.stderr.write("--out needs a path\n")
                return 2
            out_path = args.pop(0)
        elif src_root is None:
            src_root = a
        else:
            sys.stderr.write("unexpected argument %r\n" % a)
            return 2
    if not src_root:
        sys.stderr.write("usage: inventory-scan.py <src-root> [--manifest manifest.json] "
                         "[--out inventory.json] | selftest\n")
        return 2
    if not os.path.isdir(src_root):
        sys.stderr.write("inventory-scan: %r is not a directory\n" % src_root)
        return 2

    inv = scan(src_root)
    if manifest_path:
        try:
            with open(manifest_path, encoding="utf-8") as fh:
                manifest = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            sys.stderr.write("inventory-scan: manifest unreadable (%s)\n" % e)
            return 2
        try:
            inv = merge_manifest(inv, manifest)
        except ValueError as e:
            sys.stderr.write("inventory-scan: %s\n" % e)
            return 2

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(inv, fh, indent=2)
        fh.write("\n")
    print("inventory-scan: %d screen(s), %d module(s), %d flow(s) -> %s  "
          "(assisted-static: confirm before grading; %d file(s) scanned, %d unmatched route hint(s))"
          % (len(inv["screens"]), len(inv["modules"]), len(inv["flows"]), out_path,
             inv["meta"]["scanned_files"], len(inv["meta"]["unmatched_route_hints"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
