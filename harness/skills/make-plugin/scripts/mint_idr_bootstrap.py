#!/usr/bin/env python3
"""Mint the OUT-02 bootstrap skeleton for a project newly adopting the IDR pattern.

Usage:
    python3 mint_idr_bootstrap.py <git-root-of-the-target-repo> [--docs-dir <relpath, default .claude/docs>]
    python3 mint_idr_bootstrap.py selftest

<git-root-of-the-target-repo> is the root of the repo being adopted/scaffolded — the directory
whose (shared, workspace-level) `.claude/docs/` will hold the IDR ledger. In a multi-plugin
workspace this is the WORKSPACE root, never one plugin's own subdirectory — a plugin owns no
docs tree of its own.

Realizes prd-idr-framework.md's OUT-02: "A newly bootstrapped project/plugin using this
pattern has exactly one idr-0001 in draft status ... verifiable by
`find .claude/docs/idr -name 'idr-0001*'`" — plus the product-brief living-index stub named
in issue #316's deferral note (the aggregator TYPE itself stays deferred per the PRD's
Non-goals; this is a plain placeholder file, not a new doc-type).

Idempotent BY CONSTRUCTION: if <docs-dir>/idr/idr-0001*.md already exists, this is not the
project's first bootstrap moment (make-plugin may run many times against one already-adopted
repo) — the mint is skipped silently, never duplicated, never overwritten. This is what keeps
OUT-02's "exactly one" true regardless of how many times the calling command re-invokes this
script against the same target.

Exit 0 = minted, or already bootstrapped (both are success — the postcondition holds either
way); exit 1 = a write failed (target unwritable, product-brief path is a directory, etc.);
exit 2 = usage error (no target-repo-root given).
"""

import datetime
import glob
import os
import sys

IDR_TEMPLATE = """\
---
doc-type: idr
id: idr-0001
status: draft            # draft | locked | superseded
date: {date}
owner:
proof-ref:                # path/URL to the test, demo, or prototype state — fill before locking
supersedes: null
---
# IDR-0001 — <the testable hypothesis or outcome claim, stated so it could fail>

## Claim
<!-- One testable hypothesis or outcome claim — the founding belief this project is built on.
     Admission test before minting a second one: "would two reasonable builds differ on it?" -->

## Why
<!-- The reasoning and evidence behind the claim — context, not proof. -->

## Proof
<!-- A REFERENCE only — a test, demo, or prototype path/URL that would confirm or falsify the
     claim. Fill this and `proof-ref` before flipping to `locked`. -->
"""

PRODUCT_BRIEF_STUB = """\
# Product brief — living index (stub)

A placeholder living index over this project's IDR ledger (`idr/idr-0*`). The "product brief"
aggregator is a deferred doc type (product-lifecycle-bible.md Part 4; prd-idr-framework.md's
Non-goals and Delta sections) — until it exists as a first-class type, query `idr-0*` files
directly, or list them here by hand as the ledger grows.

## Current IDRs

- `idr-0001` — <one-line summary, fill in>
"""


def mint(target_root: str, docs_dir_rel: str = ".claude/docs") -> int:
    docs_dir = os.path.join(target_root, docs_dir_rel)
    idr_dir = os.path.join(docs_dir, "idr")

    existing = glob.glob(os.path.join(idr_dir, "idr-0001*.md"))
    if existing:
        print(f"mint_idr_bootstrap: already bootstrapped — {existing[0]} exists, no-op (exit 0)")
        return 0

    try:
        os.makedirs(idr_dir, exist_ok=True)
        idr_path = os.path.join(idr_dir, "idr-0001-founding-hypothesis.md")
        with open(idr_path, "w", encoding="utf-8") as f:
            f.write(IDR_TEMPLATE.format(date=datetime.date.today().isoformat()))

        brief_path = os.path.join(docs_dir, "product-brief.md")
        if os.path.isdir(brief_path):
            print(f"mint_idr_bootstrap: FAIL — {brief_path} is a directory, cannot write stub")
            return 1
        if not os.path.exists(brief_path):
            with open(brief_path, "w", encoding="utf-8") as f:
                f.write(PRODUCT_BRIEF_STUB)
    except OSError as e:
        print(f"mint_idr_bootstrap: FAIL — {e}")
        return 1

    print(f"mint_idr_bootstrap: minted {idr_path} and {brief_path} (exit 0)")
    return 0


def main(argv) -> int:
    if argv and argv[0] == "selftest":
        return selftest()
    if not argv:
        print(__doc__)
        return 2

    docs_dir_rel = ".claude/docs"
    if "--docs-dir" in argv:
        i = argv.index("--docs-dir")
        if i + 1 >= len(argv):
            print(__doc__)
            return 2
        docs_dir_rel = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]

    if not argv:
        print(__doc__)
        return 2

    return mint(argv[0], docs_dir_rel)


# --- selftest ----------------------------------------------------------------------------------
# Fixture-locked proof: a fresh temp dir mints idr-0001 + the stub (positive control); re-running
# against the SAME dir is a no-op that must not duplicate or overwrite (negative control — the
# thing OUT-02's "exactly one" depends on); a dir pre-seeded with a DIFFERENTLY-slugged idr-0001
# is still detected via the glob, proving detection isn't tied to this script's own filename
# choice (reverse control); no target arg is a usage error.

def selftest() -> int:
    import contextlib
    import io
    import shutil
    import tempfile

    errs = []
    tmp = tempfile.mkdtemp(prefix="mint_idr_bootstrap_selftest_")
    try:
        # 1. Fresh bootstrap mints both files.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = mint(tmp)
        idr_path = os.path.join(tmp, ".claude/docs/idr/idr-0001-founding-hypothesis.md")
        brief_path = os.path.join(tmp, ".claude/docs/product-brief.md")
        if code != 0:
            errs.append(f"fresh bootstrap did not exit 0 (got {code}); output:\n{buf.getvalue()}")
        if not os.path.isfile(idr_path):
            errs.append("fresh bootstrap did not create idr-0001*.md")
        else:
            content = open(idr_path, encoding="utf-8").read()
            for needle in ("doc-type: idr", "id: idr-0001", "status: draft", "## Claim", "## Why", "## Proof"):
                if needle not in content:
                    errs.append(f"minted idr-0001 missing required marker: {needle!r}")
        if not os.path.isfile(brief_path):
            errs.append("fresh bootstrap did not create product-brief.md")

        # 2. Idempotency: re-run must be a silent no-op, not a duplicate.
        if os.path.isfile(idr_path):
            os.utime(idr_path, (0, 0))  # sentinel mtime to prove it's untouched by re-run
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            code2 = mint(tmp)
        if code2 != 0:
            errs.append(f"idempotent re-run did not exit 0 (got {code2})")
        matches = glob.glob(os.path.join(tmp, ".claude/docs/idr/idr-0001*.md"))
        if len(matches) != 1:
            errs.append(f"idempotent re-run produced {len(matches)} idr-0001 files, expected exactly 1")
        if os.path.isfile(idr_path) and os.stat(idr_path).st_mtime != 0:
            errs.append("idempotent re-run overwrote the existing idr-0001 file (mtime changed)")

        # 3. Reverse control: detection isn't tied to this script's own chosen filename/slug.
        tmp2 = tempfile.mkdtemp(prefix="mint_idr_bootstrap_selftest_preexisting_")
        try:
            preexisting_dir = os.path.join(tmp2, ".claude/docs/idr")
            os.makedirs(preexisting_dir, exist_ok=True)
            with open(os.path.join(preexisting_dir, "idr-0001-some-other-slug.md"), "w", encoding="utf-8") as f:
                f.write("---\ndoc-type: idr\nid: idr-0001\nstatus: locked\n---\n")
            buf3 = io.StringIO()
            with contextlib.redirect_stdout(buf3):
                code3 = mint(tmp2)
            if code3 != 0:
                errs.append(f"pre-seeded repo (differently-slugged idr-0001) did not exit 0 (got {code3})")
            if os.path.isfile(os.path.join(tmp2, ".claude/docs/product-brief.md")):
                errs.append("pre-seeded repo: no-op path should not have written product-brief.md either")
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)

        # 4. Usage error: no target given.
        buf4 = io.StringIO()
        with contextlib.redirect_stdout(buf4):
            code4 = main([])
        if code4 != 2:
            errs.append(f"no-args invocation did not exit 2 (got {code4})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if errs:
        print("mint_idr_bootstrap selftest: FAIL (%d)" % len(errs))
        for e in errs:
            print("  - %s" % e)
        return 1
    print(
        "mint_idr_bootstrap selftest: OK — fresh bootstrap mints idr-0001 + product-brief.md; "
        "re-run is an untouched no-op (exactly 1 idr-0001 file, unchanged); a differently-slugged "
        "pre-existing idr-0001 is still detected; no-args exits 2"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
