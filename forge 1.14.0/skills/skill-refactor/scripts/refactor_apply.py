#!/usr/bin/env python3
"""refactor_apply — execute a validated skill-decompose or skill-synthesize manifest.

Usage:
  refactor_apply.py <manifest.json> [--root DIR] [--apply]
  refactor_apply.py selftest

Modes:
  plan (default)  print every operation the manifest implies; touch nothing
  --apply         execute: move files, retire old entry surfaces to the attic,
                  rewrite referrers, then prove the sweep

Contract:
  * Input is a DESIGN-validated manifest (manifest_check.py / consolidation_check.py clean).
    This script re-validates against DISK: every source file exists, no target collisions,
    every repair-map `old` string is actually present in its file.
  * Nothing is ever deleted. Superseded files and retired entry surfaces (the old pack's
    SKILL.md, evals/, scripts/) move to `.refactor-attic/<timestamp>/` — merges are not
    git-reversible, so the attic is the undo.
  * Sweep proof: after apply, the retired handle(s) must appear NOWHERE in live files
    (skills/, agents/, CLAUDE.md, settings*.json), CHANGELOGs and the attic excluded.
    A dirty sweep exits 1 — the refactor is not done until the sweep is clean.

Exit 0 = plan printed / apply completed with a clean sweep. Exit 1 = preflight or sweep failure.
"""
import json
import shutil
import sys
import time
from pathlib import Path

SWEEP_SKIP_DIRS = {".refactor-attic", "dist", ".git"}


def load_ops(manifest, root: Path):
    """Normalize either manifest type into (moves, attic_dirs, retired_handles, repairs).
    moves: list[(src_abs, dst_abs)]; attic_dirs: list[Path]; retired_handles: list[str]."""
    fails, moves, attic_dirs, retired = [], [], [], []

    if manifest.get("verdict") in ("split", "partial"):
        src_dir = root / manifest["source_corpus"]["path"]
        if not src_dir.is_dir():
            return [f"source corpus dir missing: {src_dir}"], [], [], [], []
        for pack in manifest.get("packs", []):
            dst_dir = root / "skills" / pack["name"]
            for f in pack.get("files", []):
                s, d = src_dir / f, dst_dir / f
                if not s.is_file():
                    fails.append(f"manifest is stale vs disk: {s} does not exist")
                elif d.exists():
                    fails.append(f"target collision: {d} already exists")
                else:
                    moves.append((s, d))
        attic_dirs.append(src_dir)          # the parent's entry surface retires whole
        retired.append(src_dir.name)
    elif manifest.get("verdict") == "consolidate":
        tgt = manifest["target_pack"]
        dst_dir = root / "skills" / tgt["name"]
        cand_paths = {c["name"]: root / c.get("path", f"skills/{c['name']}") for c in manifest["source_candidates"]}
        for name, p in cand_paths.items():
            if not p.is_dir():
                fails.append(f"candidate dir missing: {p}")
        for entry in tgt.get("file_map", []):
            src_base = cand_paths.get(entry.get("from"))
            if src_base is None:
                fails.append(f"file_map entry {entry.get('file')!r} names unknown candidate {entry.get('from')!r}")
                continue
            s = src_base / entry["file"]
            if not s.is_file():
                fails.append(f"manifest is stale vs disk: {s} does not exist")
                continue
            if "superseded_by" in entry:
                continue                     # rides to the attic with its candidate dir
            d = dst_dir / entry["file"]
            if d.exists():
                fails.append(f"target collision: {d} already exists")
            else:
                moves.append((s, d))
        attic_dirs.extend(cand_paths.values())
        retired.extend(cand_paths.keys())
    else:
        fails.append(f"verdict {manifest.get('verdict')!r} is not executable "
                     "(no-split / keep-separate verdicts have nothing to apply)")

    repairs = manifest.get("referrer_repair_map", [])
    for r in repairs:
        f = root / r["file"]
        if not f.is_file():
            fails.append(f"repair map names missing file: {f}")
        elif r["old"] not in f.read_text(encoding="utf-8", errors="replace"):
            fails.append(f"repair map is stale: {r['old']!r} not present in {r['file']}")
    return fails, moves, attic_dirs, retired, repairs


def sweep(root: Path, handles, exclude=()):
    hits = []
    for p in root.rglob("*"):
        if p.is_dir() or any(part in SWEEP_SKIP_DIRS for part in p.parts) or "CHANGELOG" in p.name:
            continue
        if p.resolve() in exclude:
            continue  # the manifest being applied legitimately names the retired handle
        if p.suffix not in (".md", ".json", ".py"):
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for h in handles:
                if h in line:
                    hits.append(f"{p.relative_to(root)}:{i}: {h}")
    return hits


def run(manifest_path: Path, root: Path, apply: bool):
    manifest = json.loads(manifest_path.read_text())
    fails, moves, attic_dirs, retired, repairs = load_ops(manifest, root)
    if fails:
        print(f"refactor_apply · PREFLIGHT FAIL · {len(fails)} finding(s)")
        for f in fails:
            print(f"  FAIL  {f}")
        print("  -> fix the manifest (or re-run its design checker) and retry; nothing was touched")
        return 1

    mode = "APPLY" if apply else "PLAN"
    print(f"refactor_apply · {mode} · {manifest_path.name} · {len(moves)} moves, "
          f"{len(repairs)} referrer edits, {len(attic_dirs)} dir(s) to attic, retiring: {', '.join(retired)}")
    for s, d in moves:
        print(f"  move   {s.relative_to(root)} -> {d.relative_to(root)}")
    for a in attic_dirs:
        print(f"  attic  {a.relative_to(root)} (entry surface retired; nothing is deleted)")
    for r in repairs:
        print(f"  edit   {r['file']}: {r['old']} -> {r['new']}")
    if not apply:
        print("  -> plan only; re-run with --apply to execute")
        return 0

    for s, d in moves:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))
    attic = root / ".refactor-attic" / time.strftime("%Y%m%d-%H%M%S")
    attic.mkdir(parents=True, exist_ok=True)
    for a in attic_dirs:
        if a.is_dir():
            shutil.move(str(a), str(attic / a.name))
    for r in repairs:
        f = root / r["file"]
        t = f.read_text(encoding="utf-8", errors="replace")
        n = t.count(r["old"])
        f.write_text(t.replace(r["old"], r["new"]))
        print(f"  edited {r['file']} ({n} occurrence(s))")

    hits = sweep(root, retired, exclude={manifest_path.resolve()})
    if hits:
        print(f"refactor_apply · SWEEP DIRTY · {len(hits)} live reference(s) to a retired handle:")
        for h in hits[:20]:
            print(f"  FAIL  {h}")
        print("  -> these referrers were not in the repair map; fix them, then re-run the sweep")
        return 1
    print(f"refactor_apply · DONE · sweep clean; retired surfaces preserved in {attic.relative_to(root)}")
    return 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        big = root / "skills" / "big-pack"; (big / "references").mkdir(parents=True)
        (big / "SKILL.md").write_text("---\nname: big-pack\n---\nbody")
        (big / "references" / "a.md").write_text("alpha")
        (big / "references" / "b.md").write_text("beta")
        other = root / "skills" / "other"; other.mkdir()
        (other / "SKILL.md").write_text("consult big-pack for alpha things")
        split = {"verdict": "split", "source_corpus": {"path": "skills/big-pack", "total_files": 2},
                 "packs": [{"name": "pack-alpha", "files": ["references/a.md"]},
                           {"name": "pack-beta", "files": ["references/b.md"]}],
                 "referrer_repair_map": [{"file": "skills/other/SKILL.md", "old": "big-pack", "new": "pack-alpha"}]}
        mf = root / "m.json"; mf.write_text(json.dumps(split))
        assert run(mf, root, apply=False) == 0, "plan on a clean manifest must succeed"
        assert (big / "references" / "a.md").is_file(), "plan mode must not move anything"
        assert run(mf, root, apply=True) == 0, "apply must complete with a clean sweep"
        assert (root / "skills" / "pack-alpha" / "references" / "a.md").is_file(), "file must move"
        assert not big.exists(), "parent surface must retire to the attic"
        assert list((root / ".refactor-attic").rglob("SKILL.md")), "retired SKILL.md preserved in attic"
        assert "pack-alpha" in (other / "SKILL.md").read_text(), "referrer must be rewritten"
        # stale manifest → preflight refuses
        assert run(mf, root, apply=True) == 1, "re-applying a consumed manifest must fail preflight"
        # merge with a missed referrer → sweep must catch it
        for n in ("thin-a", "thin-b"):
            d = root / "skills" / n; d.mkdir()
            (d / "SKILL.md").write_text(f"---\nname: {n}\n---\nbody")
            (d / "r.md").write_text(n)
        (root / "skills" / "other" / "SKILL.md").write_text("see thin-a and pack-alpha")
        merge = {"verdict": "consolidate",
                 "source_candidates": [{"name": "thin-a", "files": ["r.md"]}, {"name": "thin-b", "files": ["r.md"]}],
                 "target_pack": {"name": "merged-pack", "file_map": [
                     {"file": "r.md", "from": "thin-a"},
                     {"file": "r.md", "from": "thin-b", "superseded_by": "r.md", "reason": "duplicate"}]},
                 "referrer_repair_map": []}
        mf.write_text(json.dumps(merge))
        assert run(mf, root, apply=True) == 1, "a live referrer outside the repair map must dirty the sweep"
        assert (root / "skills" / "merged-pack" / "r.md").is_file(), "moved file lands despite dirty sweep"
    print("refactor_apply selftest · PASS · plan is inert, apply moves+retires+rewrites, "
          "stale manifests refused, dirty sweep caught")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    root = Path(args[args.index("--root") + 1]).resolve() if "--root" in args else Path.cwd()
    sys.exit(run(Path(args[0]), root, apply="--apply" in args))
