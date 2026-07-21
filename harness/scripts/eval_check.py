#!/usr/bin/env python3
"""eval_check — mechanical validation of trigger-eval suites (evals/evals.json).

Usage:
  eval_check.py <path/to/evals.json> [...]   validate suite files
  eval_check.py --coverage <plugin-root>     every model-invocable skill carries a suite
  eval_check.py selftest                     prove the counters bite

Rules:
  E1 valid JSON object with `skill` and non-empty `cases`
  E2 every case: unique id, non-empty prompt, expect in {trigger, no-trigger}
  E3 `skill` matches the suite's parent skill directory (a copied suite lies about its owner)
  E4 duplicate prompts across cases (WARN — one behavior, one case)
  E5 case-mix floor: >=5 trigger and >=3 no-trigger (WARN — thin suites tune nothing)
  Coverage (--coverage): model-invocable skill without evals/evals.json -> WARN, listed

Exit 0 clean (warnings allowed), 1 on any FAIL.
"""
import json
import re
import sys
from pathlib import Path

EXPECT = {"trigger", "no-trigger"}


def check_suite_text(text, skill_dir_name):
    findings = []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError) as e:
        return [("FAIL", "E1", f"invalid JSON ({e})")]
    if not isinstance(data, dict) or not data.get("skill") or not isinstance(data.get("cases"), list) or not data["cases"]:
        return [("FAIL", "E1", "must be an object with `skill` and a non-empty `cases` list")]
    ids, prompts = set(), {}
    n_trig = n_no = 0
    for i, c in enumerate(data["cases"]):
        tag = c.get("id", f"#{i}")
        if not isinstance(c, dict) or not c.get("prompt", "").strip() or c.get("expect") not in EXPECT:
            findings.append(("FAIL", "E2", f"case {tag}: needs non-empty prompt and expect in {sorted(EXPECT)}"))
            continue
        if c.get("id") in ids:
            findings.append(("FAIL", "E2", f"case id `{c['id']}` duplicated -> ids are the regression keys"))
        ids.add(c.get("id"))
        key = re.sub(r"\W+", " ", c["prompt"].lower()).strip()
        if key in prompts:
            findings.append(("WARN", "E4", f"case {tag} duplicates prompt of {prompts[key]}"))
        prompts[key] = tag
        n_trig += c["expect"] == "trigger"
        n_no += c["expect"] == "no-trigger"
    if skill_dir_name and data["skill"] != skill_dir_name:
        findings.append(("FAIL", "E3", f"suite says `{data['skill']}` but lives under `{skill_dir_name}` -> a copied suite lies about its owner"))
    if n_trig < 5 or n_no < 3:
        findings.append(("WARN", "E5", f"{n_trig} trigger / {n_no} no-trigger -> floors are 5/3; thin suites tune nothing"))
    return findings


def check_coverage(root: Path):
    findings = []
    for sk in sorted(root.glob("skills/*/SKILL.md")):
        fm = sk.read_text(encoding="utf-8", errors="replace").split("---")[1] if "---" in sk.read_text(encoding="utf-8", errors="replace") else ""
        m = re.search(r"disable-model-invocation:\s*(\w+)", fm)
        if m and m.group(1) == "true":
            continue  # user-only: description never enters model context; nothing to tune
        if not (sk.parent / "evals" / "evals.json").is_file():
            findings.append(("WARN", "E6", f"{sk.parent.name}: model-invocable, no evals/evals.json -> its description is untuned and unregressed"))
    return findings


def run(paths):
    worst = 0
    for path in paths:
        p = Path(path)
        fs = check_suite_text(p.read_text(encoding="utf-8", errors="replace"),
                              p.parent.parent.name if p.parent.name == "evals" else None)
        verdict = "FAIL" if any(f[0] == "FAIL" for f in fs) else ("warn" if fs else "clean")
        print(f"eval_check · {verdict} · {path}")
        for sev, code, msg in fs:
            print(f"  {sev:5} {code}  {msg}")
        worst = max(worst, 1 if verdict == "FAIL" else 0)
    return worst


def selftest():
    good = json.dumps({"skill": "demo-review", "cases": (
        [{"id": f"t{i}", "prompt": f"trigger prompt {i}", "expect": "trigger"} for i in range(5)]
      + [{"id": f"n{i}", "prompt": f"miss prompt {i}", "expect": "no-trigger"} for i in range(3)])})
    assert not check_suite_text(good, "demo-review"), "clean suite must pass"
    assert any(f[1] == "E1" for f in check_suite_text("{not json", None))
    assert any(f[1] == "E3" for f in check_suite_text(good, "other-skill")), "owner mismatch must fail"
    bad = json.loads(good); bad["cases"][1]["id"] = "t0"; bad["cases"][2]["expect"] = "maybe"
    fs = check_suite_text(json.dumps(bad), "demo-review")
    assert any(f[1] == "E2" for f in fs), "dup id / bad expect must fail E2"
    thin = json.dumps({"skill": "demo-review", "cases": [{"id": "t0", "prompt": "x", "expect": "trigger"}]})
    assert any(f[1] == "E5" for f in check_suite_text(thin, "demo-review")), "thin suite must warn E5"
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td); (r / "skills" / "a").mkdir(parents=True)
        (r / "skills" / "a" / "SKILL.md").write_text("---\nname: a\ndescription: x\ndisable-model-invocation: false\nuser-invocable: true\n---\nbody")
        assert any(f[1] == "E6" for f in check_coverage(r)), "uncovered model-invocable skill must warn E6"
        (r / "skills" / "a" / "evals").mkdir(); (r / "skills" / "a" / "evals" / "evals.json").write_text(good.replace("demo-review", "a"))
        assert not check_coverage(r), "covered skill must be clean"
    print("eval_check selftest · PASS · schema, identity, mix, and coverage counters bite")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "--coverage":
        fs = check_coverage(Path(args[1]).resolve())
        print(f"eval_check coverage · {'warn' if fs else 'clean'} · {args[1]}")
        for sev, code, msg in fs:
            print(f"  {sev:5} {code}  {msg}")
        sys.exit(0)
    sys.exit(run(args))
