#!/usr/bin/env python3
"""gate_guard — hash-record/hash-check/bounded-run for a gate-first mode gate script.

Usage:
  gate_guard.py record <gate.py>
  gate_guard.py run <gate.py> <clone-dir> [--timeout <seconds>]
  gate_guard.py selftest

Ruled by LLD-0026 (gh#939, gate-first mode): a `dispatch-ticket` Phase 4 validator authors one
executable gate script, `gate_<id>.py`, outside the build's scratch clone (Resolution 1). Because
the builder never sees that path, tampering with it is not something the sealed contract itself
prevents — `gate_guard.py` is the mechanical detector: `record` computes and stores the gate's
SHA-256 immediately after authoring (or after a `loop-rules` gate-repair), and `run` refuses to
execute the gate at all if its current hash no longer matches the recorded one, rather than
silently running a changed file.

  record  writes `<gate>.sha256` next to the gate file, holding its current SHA-256.
  run     re-hashes the gate, compares against `<gate>.sha256`; a mismatch is `gate-tampered`
          (exit 2) and the gate never executes. A match runs the gate as a subprocess against
          `<clone-dir>` (passed as the gate's sole argv[1]), bounded by --timeout (default 300s),
          and relays its exit code and stdout verbatim — the gate's own tri-state contract
          (0 green / 1 FAIL lines / 2 usage-or-tamper) passes straight through, this wrapper adds
          only the hash gate and the timeout bound.

Exit codes (this wrapper's own, distinct from the gate's own contract, which `run` relays as its
own process exit when the hash check passes): 0 clean run (whatever the gate itself returned,
relayed) — `record` also exits 0 on a successful write; 1 is never emitted by this wrapper
directly (a gate's own FAIL is exit 1 and is relayed, not re-coded); 2 on a usage error, a missing
gate/hash file, a hash mismatch (`gate-tampered`), or a timeout (`gate-timeout`).

`selftest` builds real temporary fixtures — a real gate script and a real tamper — proving
record/run/tamper-detection/timeout end to end. No network.
"""
import hashlib
import os
import subprocess
import sys
import tempfile


DEFAULT_TIMEOUT = 300


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_path_for(gate_path):
    return gate_path + ".sha256"


def record(gate_path):
    if not os.path.isfile(gate_path):
        raise RuntimeError(f"gate file not found: {gate_path}")
    digest = sha256_of(gate_path)
    with open(hash_path_for(gate_path), "w") as f:
        f.write(digest + "\n")
    return digest


def run(gate_path, clone_dir, timeout=DEFAULT_TIMEOUT):
    """Returns (exit_code, stdout_text). Raises RuntimeError on setup problems (missing gate,
    missing recorded hash) distinct from a gate's own FAIL — callers map RuntimeError to exit 2."""
    if not os.path.isfile(gate_path):
        raise RuntimeError(f"gate file not found: {gate_path}")
    hash_path = hash_path_for(gate_path)
    if not os.path.isfile(hash_path):
        raise RuntimeError(
            f"no recorded hash at {hash_path} — run `record` immediately after authoring "
            "(or after a gate-repair) before the first `run`"
        )
    with open(hash_path) as f:
        recorded = f.read().strip()
    current = sha256_of(gate_path)
    if current != recorded:
        raise TamperedError(
            f"gate-tampered: {gate_path} hash {current} does not match recorded {recorded} "
            f"({hash_path}) — refusing to execute a changed gate"
        )
    if not os.path.isdir(clone_dir):
        raise RuntimeError(f"clone dir not found: {clone_dir}")
    try:
        proc = subprocess.run(
            [sys.executable, gate_path, clone_dir],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise GateTimeoutError(f"gate-timeout: {gate_path} exceeded {timeout}s against {clone_dir}")
    return proc.returncode, proc.stdout + proc.stderr


class TamperedError(RuntimeError):
    pass


class GateTimeoutError(RuntimeError):
    pass


def parse_args(args):
    """Returns (mode, rest_dict). Raises ValueError on any unrecognized token or a flag missing
    its value — the #188-class silent-argument-swallowing defect this house style always rejects."""
    if not args:
        raise ValueError("a mode (record|run|selftest) is required")
    mode = args[0]
    if mode == "selftest":
        if len(args) != 1:
            raise ValueError("selftest takes no further arguments")
        return mode, {}
    if mode == "record":
        if len(args) != 2:
            raise ValueError("record requires exactly one argument: <gate.py>")
        return mode, {"gate_path": args[1]}
    if mode == "run":
        rest = args[1:]
        if len(rest) < 2:
            raise ValueError("run requires <gate.py> <clone-dir>")
        gate_path, clone_dir = rest[0], rest[1]
        timeout = DEFAULT_TIMEOUT
        i = 2
        while i < len(rest):
            if rest[i] == "--timeout":
                if i + 1 >= len(rest):
                    raise ValueError("--timeout requires a value")
                try:
                    timeout = int(rest[i + 1])
                except ValueError:
                    raise ValueError(f"--timeout value must be an integer, got {rest[i + 1]!r}")
                i += 2
            else:
                raise ValueError(f"unrecognized argument: {rest[i]}")
        return mode, {"gate_path": gate_path, "clone_dir": clone_dir, "timeout": timeout}
    raise ValueError(f"unrecognized mode: {mode}")


def selftest():
    fails = 0

    with tempfile.TemporaryDirectory() as tmp:
        gate_path = os.path.join(tmp, "gate_999.py")
        clone_dir = os.path.join(tmp, "clone")
        os.makedirs(clone_dir)

        # A gate that FAILs unless a marker file exists in the clone dir — proves both the
        # green and FAIL relay paths through one fixture.
        with open(gate_path, "w") as f:
            f.write(
                "import os, sys\n"
                "clone = sys.argv[1]\n"
                "marker = os.path.join(clone, 'ok.txt')\n"
                "if os.path.isfile(marker):\n"
                "    print('P1 [PASS] marker present')\n"
                "    sys.exit(0)\n"
                "print('P1 [FAIL] marker file ok.txt not found in clone — expected present, got absent')\n"
                "sys.exit(1)\n"
            )

        # run() before record() must raise (no recorded hash yet)
        try:
            run(gate_path, clone_dir)
            print("FAIL run/no-hash (expected RuntimeError with no recorded hash)")
            fails += 1
        except TamperedError:
            print("FAIL run/no-hash (raised TamperedError, expected plain RuntimeError)")
            fails += 1
        except RuntimeError:
            print("ok    run/no-hash (refuses to run with no recorded hash)")

        digest = record(gate_path)
        if not os.path.isfile(hash_path_for(gate_path)):
            print("FAIL record/writes-hash-file")
            fails += 1
        elif len(digest) != 64:
            print("FAIL record/digest-shape")
            fails += 1
        else:
            print("ok    record/writes-hash-file")

        # run() with the gate unmodified, marker absent -> gate FAILs, wrapper relays exit 1
        rc, out = run(gate_path, clone_dir)
        if rc != 1 or "FAIL" not in out:
            print(f"FAIL run/fail-relay (expected exit 1 with FAIL text, got {rc}: {out!r})")
            fails += 1
        else:
            print("ok    run/fail-relay (gate's own FAIL relayed verbatim)")

        # add the marker -> gate now passes, wrapper relays exit 0
        with open(os.path.join(clone_dir, "ok.txt"), "w") as f:
            f.write("present\n")
        rc, out = run(gate_path, clone_dir)
        if rc != 0 or "PASS" not in out:
            print(f"FAIL run/pass-relay (expected exit 0 with PASS text, got {rc}: {out!r})")
            fails += 1
        else:
            print("ok    run/pass-relay (gate's own green relayed verbatim)")

        # tamper: append a byte, hash no longer matches -> run() must raise TamperedError, gate
        # must never execute (proven by exit not being either of the gate's own codes)
        with open(gate_path, "a") as f:
            f.write("# tampered\n")
        try:
            run(gate_path, clone_dir)
            print("FAIL run/tamper-detection (expected TamperedError, gate ran instead)")
            fails += 1
        except TamperedError as e:
            if "gate-tampered" not in str(e):
                print("FAIL run/tamper-detection (raised, but message missing gate-tampered)")
                fails += 1
            else:
                print("ok    run/tamper-detection (refuses to execute a changed gate)")
        except RuntimeError:
            print("FAIL run/tamper-detection (raised wrong exception type)")
            fails += 1

        # re-record after the (simulated) gate-repair -> run() works again
        record(gate_path)
        rc, out = run(gate_path, clone_dir)
        if rc != 0:
            print(f"FAIL run/post-repair (expected exit 0 after re-record, got {rc})")
            fails += 1
        else:
            print("ok    run/post-repair (re-record after repair clears the tamper block)")

        # timeout: a gate that never returns
        slow_gate = os.path.join(tmp, "gate_slow.py")
        with open(slow_gate, "w") as f:
            f.write("import time, sys\ntime.sleep(5)\nsys.exit(0)\n")
        record(slow_gate)
        try:
            run(slow_gate, clone_dir, timeout=1)
            print("FAIL run/timeout (expected GateTimeoutError)")
            fails += 1
        except GateTimeoutError as e:
            if "gate-timeout" not in str(e):
                print("FAIL run/timeout (raised, but message missing gate-timeout)")
                fails += 1
            else:
                print("ok    run/timeout (bounded execution enforced)")
        except RuntimeError:
            print("FAIL run/timeout (raised wrong exception type)")
            fails += 1

    # parse_args — the #188-class negative controls
    mode, rest = parse_args(["run", "g.py", "c/", "--timeout", "10"])
    if (mode, rest) != ("run", {"gate_path": "g.py", "clone_dir": "c/", "timeout": 10}):
        print("FAIL parse_args/run-full")
        fails += 1
    else:
        print("ok    parse_args/run-full")
    mode, rest = parse_args(["record", "g.py"])
    if (mode, rest) != ("record", {"gate_path": "g.py"}):
        print("FAIL parse_args/record")
        fails += 1
    else:
        print("ok    parse_args/record")
    try:
        parse_args(["run", "g.py", "c/", "--bogus", "x"])
        print("FAIL parse_args/bogus (unrecognized flag must be rejected, not swallowed)")
        fails += 1
    except ValueError as e:
        if "--bogus" not in str(e):
            print("FAIL parse_args/bogus (error must name the bad flag)")
            fails += 1
        else:
            print("ok    parse_args/bogus")
    try:
        parse_args(["run", "g.py", "c/", "--timeout"])
        print("FAIL parse_args/missing-value (flag missing its value must be a clean error)")
        fails += 1
    except ValueError as e:
        if "--timeout" not in str(e):
            print("FAIL parse_args/missing-value (error must name the flag)")
            fails += 1
        else:
            print("ok    parse_args/missing-value")
    try:
        parse_args([])
        print("FAIL parse_args/empty (no mode at all must be a clean error)")
        fails += 1
    except ValueError:
        print("ok    parse_args/empty")
    try:
        parse_args(["bogus-mode"])
        print("FAIL parse_args/bogus-mode")
        fails += 1
    except ValueError:
        print("ok    parse_args/bogus-mode")

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        return 1
    print(
        "gate_guard selftest · PASS · record/hash-check, FAIL/PASS relay, tamper "
        "detection (real gate mutation, real refusal), post-repair re-record, timeout bound, "
        "and parse_args' #188-class controls all pass clean"
    )
    return 0


def main(argv):
    try:
        mode, rest = parse_args(argv)
    except ValueError as e:
        print(f"gate_guard: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2

    if mode == "selftest":
        return selftest()

    if mode == "record":
        try:
            digest = record(rest["gate_path"])
        except RuntimeError as e:
            print(f"gate_guard: {e}", file=sys.stderr)
            return 2
        print(f"recorded {rest['gate_path']} -> {digest}")
        return 0

    if mode == "run":
        try:
            rc, out = run(rest["gate_path"], rest["clone_dir"], timeout=rest["timeout"])
        except TamperedError as e:
            print(f"gate_guard: {e}", file=sys.stderr)
            return 2
        except GateTimeoutError as e:
            print(f"gate_guard: {e}", file=sys.stderr)
            return 2
        except RuntimeError as e:
            print(f"gate_guard: {e}", file=sys.stderr)
            return 2
        print(out, end="")
        return rc

    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
