#!/usr/bin/env python3
"""flow-check.py — the flow-decompose mechanism gate. Self-contained (stdlib only).

A "flow card" (*.flow.json) is the small declarative artifact the skill emits (or re-derives when
grading an existing app/spec) to describe ONE cross-screen user flow as a state machine: the
journey's states, the transitions (verbs) that move the user between them, the exits where the
task ends and what must be TRUE there, and the recovery/persistence overlay. This linter routes
the MECHANIZABLE facts of a journey to code — can every state be reached? does any non-exit state
strand the user? does every success exit assert something? does every fallible transition have a
declared recovery? — while the judgment-heavy review (is this the RIGHT journey? are the asserts
the RIGHT truths? do they hold against the rendered app?) stays in SKILL.md. An empty asserts[]
is mechanical; whether "balance reflects payment" actually holds is a probe or a human walk.

Flow card shape (all top-level keys optional; report — never silently pass — when absent):
  {
    "id": "one-time-pay",
    "task": "pay the amount owed now",
    "entry": ["statement"],                          # states the user can start from
    "states": [{"id": "statement", "screen": "statement"}, {"id": "pay-review"}],
    "transitions": [                                 # the declared verbs, incl. back/abandon
      {"from": "statement", "to": "pay-review", "verb": "pay"},
      {"from": "pay-review", "to": "receipt", "verb": "submit",
       "fallible": true, "destructive": true, "guard": "…optional note on a back verb…"}
    ],
    "exits": [                                       # where the task ends + what is TRUE there
      {"state": "receipt", "kind": "success", "asserts": ["balance reflects payment"]}
    ],
    "recovery": [                                    # how a fallible transition is survived
      {"from": "receipt", "to": "pay-review", "preserves_input": true}
    ],
    "persistence": {"resumable": true, "across": "session timeout / re-auth"}
  }

Checks (gate = a hard FAIL; advisory = a WARN that surfaces a risk for human review):
  UNREACHABLE_STATE (gate)     — a declared state no entry can reach (graph walk over transitions).
                                 A state that cannot be reached is either dead spec or a missing
                                 transition — both are machine defects.
  DEAD_END          (gate)     — a non-exit state with zero outgoing transitions. The journey
                                 strands the user there with no declared verb out (not even
                                 back/abandon).
  ORPHAN_EXIT       (gate)     — an exit naming a state that is undeclared or unreachable. The
                                 card claims the task can end somewhere the machine never goes.
  NO_EXIT_TRUTH     (gate)     — a SUCCESS exit with empty/missing asserts[]. Completion claimed,
                                 nothing asserted — the money-truth class of defect. The asserts'
                                 CONTENT is judgment/probe territory; their ABSENCE is mechanical.
  NO_RECOVERY       (gate)     — a transition marked fallible with no recovery entry whose `from`
                                 is that transition's source or target. Failure is declared
                                 possible but survival is not declared.
  UNGUARDED_BACK    (advisory) — a back/abandon/cancel verb out of a COMMITTED state (the target
                                 of a destructive transition) with no `guard` note on it. Going
                                 back over committed work needs a declared story (re-charge? no-op?).
  INPUT_LOSS        (advisory) — a recovery that does not declare preserves_input:true. Recovery
                                 that retypes the user's work is recovery in name only.
  UNKNOWN_SCREEN    (advisory) — with --inventory inventory.json (ui-audit's spine): a state whose
                                 `screen` is absent from the inventory's screens — the flow claims
                                 a surface the product doesn't list.

A check whose data is absent is SKIPPED and reported as a skip (no silent pass): no states[] ->
nothing state-level can run; no entry[] -> reachability can't run; no transitions[] -> the graph
checks can't run; no exits[] -> the exit checks can't run (and terminal states will read as
DEAD_END — declare your exits); no recovery[] -> INPUT_LOSS can't run (but a fallible transition
still gates NO_RECOVERY: the absence IS the defect); no persistence{} -> the resume story is
undeclared, reported for the B4 judgment pass. A malformed card (non-list sections, duplicate or
missing state ids, a transition/entry/recovery endpoint naming an undeclared state, non-list
asserts) yields a clear error, not a traceback.

  python3 scripts/flow-check.py selftest
  python3 scripts/flow-check.py <card.flow.json | dir> [--inventory inventory.json]

Exit 0 = every card clears the gates. Exit 1 = at least one gate FAIL (or malformed card).
Python 3.8+.
"""
import json
import os
import sys

BACK_VERBS = {"back", "abandon", "cancel"}
EXIT_KINDS = {"success", "abandon", "error"}


def _require_state(name, id_set, sid, where):
    if not isinstance(sid, str) or not sid:
        raise ValueError("%s: %s names a non-string state id: %r" % (name, where, sid))
    if sid not in id_set:
        raise ValueError("%s: %s references undeclared state '%s'" % (name, where, sid))


def _reachable(entry, transitions):
    """BFS over the declared transitions from the entry states."""
    edges = {}
    for t in transitions:
        edges.setdefault(t["from"], set()).add(t["to"])
    seen, queue = set(entry), list(entry)
    while queue:
        cur = queue.pop(0)
        for nxt in edges.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def check_card(card, screens=None):
    """Return (fails, warns, skips) for one flow card. `screens` is an optional set of known
    screen ids (from --inventory) enabling the UNKNOWN_SCREEN advisory.

    Raises ValueError on a structurally malformed card (caller turns it into a clean error)."""
    if not isinstance(card, dict):
        raise ValueError("card must be a JSON object")
    fails, warns, skips = [], [], []
    name = card.get("id") or card.get("task") or "<card>"

    # --- validity pass: malformed shapes are errors, not silent skips ---------------------------
    states = card.get("states")
    if states is not None and not isinstance(states, list):
        raise ValueError("%s: 'states' must be a list" % name)
    id_set, state_list = set(), []
    if isinstance(states, list):
        for i, s in enumerate(states):
            if not isinstance(s, dict):
                raise ValueError("%s: states[%d] must be an object" % (name, i))
            sid = s.get("id")
            if not isinstance(sid, str) or not sid:
                raise ValueError("%s: states[%d] has no string 'id'" % (name, i))
            if sid in id_set:
                raise ValueError("%s: duplicate state id '%s'" % (name, sid))
            id_set.add(sid)
            state_list.append(s)

    transitions = card.get("transitions")
    if transitions is not None and not isinstance(transitions, list):
        raise ValueError("%s: 'transitions' must be a list" % name)
    if isinstance(transitions, list):
        for i, t in enumerate(transitions):
            if not isinstance(t, dict):
                raise ValueError("%s: transitions[%d] must be an object" % (name, i))
            _require_state(name, id_set, t.get("from"), "transitions[%d].from" % i)
            _require_state(name, id_set, t.get("to"), "transitions[%d].to" % i)

    entry = card.get("entry")
    if entry is not None and not isinstance(entry, list):
        raise ValueError("%s: 'entry' must be a list of state ids" % name)
    if isinstance(entry, list):
        for i, e in enumerate(entry):
            _require_state(name, id_set, e, "entry[%d]" % i)

    exits = card.get("exits")
    if exits is not None and not isinstance(exits, list):
        raise ValueError("%s: 'exits' must be a list" % name)
    if isinstance(exits, list):
        for i, x in enumerate(exits):
            if not isinstance(x, dict):
                raise ValueError("%s: exits[%d] must be an object" % (name, i))
            kind = x.get("kind")
            if kind not in EXIT_KINDS:
                raise ValueError("%s: exits[%d].kind %r not one of %s"
                                 % (name, i, kind, sorted(EXIT_KINDS)))
            if x.get("asserts") is not None and not isinstance(x.get("asserts"), list):
                raise ValueError("%s: exits[%d].asserts must be a list" % (name, i))
            # NOTE: exits[].state validity is ORPHAN_EXIT's gate, not a malformed-card error.

    recovery = card.get("recovery")
    if recovery is not None and not isinstance(recovery, list):
        raise ValueError("%s: 'recovery' must be a list" % name)
    if isinstance(recovery, list):
        for i, r in enumerate(recovery):
            if not isinstance(r, dict):
                raise ValueError("%s: recovery[%d] must be an object" % (name, i))
            _require_state(name, id_set, r.get("from"), "recovery[%d].from" % i)
            _require_state(name, id_set, r.get("to"), "recovery[%d].to" % i)

    persistence = card.get("persistence")
    if persistence is not None and not isinstance(persistence, dict):
        raise ValueError("%s: 'persistence' must be an object" % name)

    # --- exit-state set (used by DEAD_END; empty when exits[] absent) ---------------------------
    exit_states = set()
    if isinstance(exits, list):
        exit_states = {x.get("state") for x in exits if isinstance(x.get("state"), str)}

    # --- UNREACHABLE_STATE (gate): graph walk from entry[] --------------------------------------
    reachable = None
    if not state_list:
        skips.append("%s: no states[] — every state-level check skipped" % name)
    elif transitions is None:
        skips.append("%s: no transitions[] — UNREACHABLE_STATE / DEAD_END checks skipped" % name)
    elif not entry:
        skips.append("%s: no entry[] — UNREACHABLE_STATE (and exit reachability) skipped" % name)
    else:
        reachable = _reachable(entry, transitions)
        for sid in (s["id"] for s in state_list):
            if sid not in reachable:
                fails.append("%s: UNREACHABLE_STATE — state '%s' is not reachable from any entry "
                             "%s; dead spec or a missing transition" % (name, sid, entry))

    # --- DEAD_END (gate): non-exit state with zero outgoing verbs -------------------------------
    if state_list and isinstance(transitions, list):
        outgoing = {t["from"] for t in transitions}
        if exits is None:
            skips.append("%s: no exits[] — terminal states cannot be excused as exits "
                         "(declare them)" % name)
        for sid in (s["id"] for s in state_list):
            if sid not in outgoing and sid not in exit_states:
                fails.append("%s: DEAD_END — non-exit state '%s' has zero outgoing transitions; "
                             "the journey strands the user there (declare the verbs out — even "
                             "back/abandon — or declare it an exit)" % (name, sid))

    # --- ORPHAN_EXIT (gate) + NO_EXIT_TRUTH (gate) -----------------------------------------------
    if exits is None:
        skips.append("%s: no exits[] — ORPHAN_EXIT / NO_EXIT_TRUTH checks skipped" % name)
    elif not exits:
        skips.append("%s: exits[] is empty — ORPHAN_EXIT / NO_EXIT_TRUTH checks skipped" % name)
    else:
        for i, x in enumerate(exits):
            st = x.get("state")
            label = st if isinstance(st, str) else "exits[%d]" % i
            if not isinstance(st, str) or st not in id_set:
                fails.append("%s: ORPHAN_EXIT — exit '%s' (%s) names an undeclared state"
                             % (name, label, x.get("kind")))
            elif reachable is not None and st not in reachable:
                fails.append("%s: ORPHAN_EXIT — exit '%s' (%s) names an unreachable state — the "
                             "card claims the task can end where the machine never goes"
                             % (name, label, x.get("kind")))
            if x.get("kind") == "success":
                asserts = x.get("asserts")
                if not asserts or not any(isinstance(a, str) and a.strip() for a in asserts):
                    fails.append("%s: NO_EXIT_TRUTH — success exit '%s' with empty/missing "
                                 "asserts[] — completion claimed, nothing asserted; declare what "
                                 "must be TRUE at it (e.g. \"balance reflects payment\")"
                                 % (name, label))

    # --- NO_RECOVERY (gate): every fallible transition needs a declared survival ----------------
    if isinstance(transitions, list):
        fallible = [t for t in transitions if t.get("fallible")]
        if not fallible:
            skips.append("%s: no fallible transitions — NO_RECOVERY not applicable" % name)
        else:
            rec_froms = {r["from"] for r in recovery} if isinstance(recovery, list) else set()
            for t in fallible:
                if not ({t["from"], t["to"]} & rec_froms):
                    fails.append("%s: NO_RECOVERY — fallible transition '%s' (%s→%s) has no "
                                 "recovery entry from its source or target; failure is declared "
                                 "possible but survival is not declared"
                                 % (name, t.get("verb", "?"), t["from"], t["to"]))

    # --- UNGUARDED_BACK (advisory): back-verbs out of committed states need a guard note --------
    if isinstance(transitions, list) and transitions:
        committed = {t["to"] for t in transitions if t.get("destructive")}
        for t in transitions:
            verb = t.get("verb", "")
            if (isinstance(verb, str) and verb.strip().lower() in BACK_VERBS
                    and t["from"] in committed
                    and not str(t.get("guard") or "").strip()):
                warns.append("%s: UNGUARDED_BACK — '%s' out of committed state '%s' (a "
                             "destructive transition lands there) with no guard note — what does "
                             "going back over committed work do? (review)"
                             % (name, verb, t["from"]))

    # --- INPUT_LOSS (advisory): recovery must preserve the user's work --------------------------
    if recovery is None:
        skips.append("%s: no recovery[] — INPUT_LOSS check skipped" % name)
    else:
        for r in recovery:
            if r.get("preserves_input") is not True:
                warns.append("%s: INPUT_LOSS — recovery %s→%s with preserves_input:%r — recovery "
                             "that retypes the user's work is recovery in name only (review)"
                             % (name, r["from"], r["to"], r.get("preserves_input")))

    # --- persistence: presence is reported; its adequacy is the B4 judgment ---------------------
    if persistence is None:
        skips.append("%s: no persistence{} — resume-across-interruption story undeclared "
                     "(B4 judgment has nothing to anchor on)" % name)

    # --- UNKNOWN_SCREEN (advisory): only with --inventory ---------------------------------------
    if screens is not None:
        if not state_list:
            pass  # the no-states skip above already covers it
        else:
            for s in state_list:
                sc = s.get("screen")
                if isinstance(sc, str) and sc and sc not in screens:
                    warns.append("%s: UNKNOWN_SCREEN — state '%s' renders on screen '%s' which is "
                                 "absent from the inventory — the flow claims a surface the "
                                 "product doesn't list (review)" % (name, s["id"], sc))

    return fails, warns, skips


# --- selftest fixtures ---------------------------------------------------------------------------
# must-NOT-flag: a reachable clean flow — every state reachable, no dead end, success exit with
# asserts, the fallible transition covered by an input-preserving recovery from its target,
# persistence declared. The back verb leaves a NON-committed state, so no advisory.
GOOD = {
    "id": "clean-flow", "task": "do the thing",
    "entry": ["start"],
    "states": [{"id": "start", "screen": "home"}, {"id": "review"}, {"id": "done"}],
    "transitions": [
        {"from": "start", "to": "review", "verb": "begin"},
        {"from": "review", "to": "start", "verb": "back"},
        {"from": "review", "to": "done", "verb": "submit", "fallible": True, "destructive": True},
    ],
    "exits": [
        {"state": "done", "kind": "success", "asserts": ["the record reflects the submission"]},
        {"state": "start", "kind": "abandon", "asserts": ["nothing was committed"]},
    ],
    "recovery": [{"from": "done", "to": "review", "preserves_input": True}],
    "persistence": {"resumable": True, "across": "reload"},
}
# must-FLAG DEAD_END: 'stuck' has zero outgoing transitions and is not an exit.
DEAD = {
    "id": "dead-end-flow", "entry": ["a"],
    "states": [{"id": "a"}, {"id": "b"}, {"id": "stuck"}],
    "transitions": [{"from": "a", "to": "b", "verb": "go"},
                    {"from": "b", "to": "stuck", "verb": "continue"}],
    "exits": [{"state": "b", "kind": "success", "asserts": ["b holds"]}],
}
# must-FLAG NO_EXIT_TRUTH twice (empty asserts + missing asserts) but NOT on the abandon exit.
NO_TRUTH = {
    "id": "truthless-flow", "entry": ["a"],
    "states": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
    "transitions": [{"from": "a", "to": "b", "verb": "go"},
                    {"from": "a", "to": "c", "verb": "skip"}],
    "exits": [{"state": "b", "kind": "success", "asserts": []},
              {"state": "c", "kind": "success"},
              {"state": "a", "kind": "abandon"}],
}
# must-FLAG NO_RECOVERY: a fallible transition with no recovery[] at all.
NO_RECOV = {
    "id": "unrecoverable-flow", "entry": ["a"],
    "states": [{"id": "a"}, {"id": "b"}],
    "transitions": [{"from": "a", "to": "b", "verb": "submit", "fallible": True}],
    "exits": [{"state": "b", "kind": "success", "asserts": ["b holds"]}],
}
# must-FLAG UNREACHABLE_STATE ('island') + ORPHAN_EXIT twice (undeclared 'ghost', unreachable 'island').
ISLAND = {
    "id": "island-flow", "entry": ["a"],
    "states": [{"id": "a"}, {"id": "b"}, {"id": "island"}],
    "transitions": [{"from": "a", "to": "b", "verb": "go"},
                    {"from": "island", "to": "b", "verb": "swim"}],
    "exits": [{"state": "b", "kind": "success", "asserts": ["b holds"]},
              {"state": "ghost", "kind": "error"},
              {"state": "island", "kind": "error"}],
}
# must-WARN UNGUARDED_BACK (back out of committed 'paid', no guard) + INPUT_LOSS
# (preserves_input:false); the guarded twin ('receipt' -> guard note) must stay quiet.
BACKLOSS = {
    "id": "backloss-flow", "entry": ["a"],
    "states": [{"id": "a"}, {"id": "paid"}, {"id": "receipt"}],
    "transitions": [
        {"from": "a", "to": "paid", "verb": "submit", "fallible": True, "destructive": True},
        {"from": "paid", "to": "receipt", "verb": "continue", "destructive": True},
        {"from": "paid", "to": "a", "verb": "back"},
        {"from": "receipt", "to": "a", "verb": "back", "guard": "receipt is read-only; no re-charge"},
    ],
    "exits": [{"state": "receipt", "kind": "success", "asserts": ["receipt shows the charge"]}],
    "recovery": [{"from": "paid", "to": "a", "preserves_input": False}],
}
# sparse card: states only — every absent section reports a SKIP, no fail, no warn.
SPARSE = {"id": "sparse-flow", "states": [{"id": "a"}]}
# inventory fixture: state 'start' renders on screen 'home'; an inventory without 'home' must warn.
INVENTORIED = GOOD
# malformed cards: each must raise a clean ValueError, never crash or silently pass.
MALFORMED_STATES = {"id": "m1", "states": "nope"}
MALFORMED_DUP = {"id": "m2", "states": [{"id": "a"}, {"id": "a"}]}
MALFORMED_EDGE = {"id": "m3", "states": [{"id": "a"}],
                  "transitions": [{"from": "a", "to": "ghost", "verb": "go"}]}
MALFORMED_ENTRY = {"id": "m4", "states": [{"id": "a"}], "entry": ["ghost"]}
MALFORMED_KIND = {"id": "m5", "states": [{"id": "a"}],
                  "exits": [{"state": "a", "kind": "victory"}]}
MALFORMED_ASSERTS = {"id": "m6", "states": [{"id": "a"}],
                     "exits": [{"state": "a", "kind": "success", "asserts": "yes"}]}
MALFORMED_RECOV = {"id": "m7", "states": [{"id": "a"}],
                   "recovery": [{"from": "a", "to": "ghost"}]}


def selftest():
    errs = []

    gf, gw, gs = check_card(GOOD)
    if gf:
        errs.append("clean flow produced fails: %s" % gf)
    if gw:
        errs.append("clean flow produced warns: %s" % gw)
    bad_skips = [s for s in gs if "not applicable" not in s]
    if bad_skips:
        errs.append("fully-populated clean flow silently skipped a present section: %s" % bad_skips)

    df, _, _ = check_card(DEAD)
    if sum("DEAD_END" in f for f in df) != 1 or not any("'stuck'" in f for f in df):
        errs.append("dead-end 'stuck' not the exactly-one DEAD_END: %s" % df)
    if any("'b'" in f and "DEAD_END" in f for f in df):
        errs.append("exit state 'b' wrongly flagged DEAD_END")

    tf, _, _ = check_card(NO_TRUTH)
    if sum("NO_EXIT_TRUTH" in f for f in tf) != 2:
        errs.append("empty + missing asserts[] not exactly-two NO_EXIT_TRUTH: %s" % tf)
    if any("NO_EXIT_TRUTH" in f and "'a'" in f for f in tf):
        errs.append("abandon exit without asserts wrongly gated NO_EXIT_TRUTH (success-only rule)")

    rf, _, rs = check_card(NO_RECOV)
    if not any("NO_RECOVERY" in f for f in rf):
        errs.append("fallible transition without recovery not gated NO_RECOVERY")
    if not any("INPUT_LOSS check skipped" in s for s in rs):
        errs.append("absent recovery[] did not report the INPUT_LOSS skip")

    isf, _, _ = check_card(ISLAND)
    if not any("UNREACHABLE_STATE" in f and "'island'" in f for f in isf):
        errs.append("unreachable 'island' not gated UNREACHABLE_STATE")
    if sum("ORPHAN_EXIT" in f for f in isf) != 2:
        errs.append("undeclared 'ghost' + unreachable 'island' exits not exactly-two ORPHAN_EXIT: %s" % isf)

    bf, bw, _ = check_card(BACKLOSS)
    if bf:
        errs.append("backloss fixture produced unexpected fails: %s" % bf)
    if sum("UNGUARDED_BACK" in w for w in bw) != 1 or not any(
            "UNGUARDED_BACK" in w and "'paid'" in w for w in bw):
        errs.append("unguarded back out of 'paid' not the exactly-one UNGUARDED_BACK: %s" % bw)
    if any("UNGUARDED_BACK" in w and "'receipt'" in w for w in bw):
        errs.append("guarded back out of 'receipt' wrongly warned (guard note not honored)")
    if not any("INPUT_LOSS" in w for w in bw):
        errs.append("recovery with preserves_input:false not warned INPUT_LOSS")

    sf, sw, ss = check_card(SPARSE)
    if sf or sw:
        errs.append("sparse card produced fails/warns: %s / %s" % (sf, sw))
    for token in ("no transitions[]", "no exits[]", "no recovery[]", "no persistence{}"):
        if not any(token in s for s in ss):
            errs.append("sparse card did not report the '%s' skip (silent pass?)" % token)

    _, iw, _ = check_card(INVENTORIED, screens={"statement", "receipt"})
    if not any("UNKNOWN_SCREEN" in w and "'home'" in w for w in iw):
        errs.append("state on screen 'home' absent from inventory not warned UNKNOWN_SCREEN")
    _, okw, _ = check_card(INVENTORIED, screens={"home"})
    if any("UNKNOWN_SCREEN" in w for w in okw):
        errs.append("inventoried screen 'home' wrongly warned UNKNOWN_SCREEN")

    for label, bad in (("states-not-a-list", MALFORMED_STATES), ("duplicate state id", MALFORMED_DUP),
                       ("transition to undeclared state", MALFORMED_EDGE),
                       ("entry names undeclared state", MALFORMED_ENTRY),
                       ("unknown exit kind", MALFORMED_KIND), ("asserts not a list", MALFORMED_ASSERTS),
                       ("recovery to undeclared state", MALFORMED_RECOV)):
        try:
            check_card(bad)
            errs.append("malformed card (%s) did not raise" % label)
        except ValueError:
            pass

    return errs


def _iter_cards(path):
    if os.path.isdir(path):
        for dp, _, fns in os.walk(path):
            for fn in sorted(fns):
                if fn.endswith(".flow.json"):
                    yield os.path.join(dp, fn)
    else:
        yield path


def _load_screens(inventory_path):
    """The inventory's screen ids (ui-audit's inventory-scan.py shape, or a bare list)."""
    inv = json.load(open(inventory_path, encoding="utf-8"))
    raw = inv.get("screens", []) if isinstance(inv, dict) else inv
    screens = set()
    for s in raw or []:
        if isinstance(s, dict) and isinstance(s.get("id"), str):
            screens.add(s["id"])
        elif isinstance(s, str):
            screens.add(s)
    return screens


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("flow-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("flow-check: OK — gate + advisory checks verified over good/bad/sparse/malformed fixtures")
        return 0
    screens = None
    args = list(argv)
    if "--inventory" in args:
        i = args.index("--inventory")
        try:
            screens = _load_screens(args[i + 1])
        except (IndexError, OSError, json.JSONDecodeError, AttributeError) as e:
            sys.stderr.write("flow-check: cannot read --inventory (%s)\n" % e)
            return 1
        del args[i:i + 2]
    if not args:
        sys.stderr.write("usage: flow-check.py <card.flow.json | dir> [--inventory inventory.json] | selftest\n")
        return 2
    fails, warns, skips, n = [], [], [], 0
    for fp in _iter_cards(args[0]):
        try:
            doc = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fails.append("%s: unreadable (%s)" % (fp, e))
            continue
        for card in (doc if isinstance(doc, list) else [doc]):
            n += 1
            try:
                f, w, s = check_card(card, screens=screens)
            except ValueError as e:
                fails.append("%s: malformed card (%s)" % (fp, e))
                continue
            fails += f
            warns += w
            skips += s
    for s in skips:
        print("  - (skip) %s" % s)
    for w in warns:
        print("  ! %s" % w)
    if fails:
        sys.stderr.write("flow-check: FAIL (%d)\n" % len(fails))
        for f in fails:
            sys.stderr.write("  - %s\n" % f)
        return 1
    print("flow-check: OK — %d card(s) clear the flow gates" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
