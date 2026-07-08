#!/usr/bin/env python3
"""safety-check.py — the safety-verifier destructive-action linter. Self-contained (stdlib only).

A "destructive-action card" is the small declarative artifact safety-verifier emits for each
high-consequence action *before* a UI affordance is attached to it (and re-derives when auditing
one that exists). This linter routes the MECHANIZABLE invariants of the skill to code — the
judgment-heavy reviews (is the named consequence honest? is the recovery path real? is the
audit event actually surfaced?) stay in SKILL.md. It checks one or more cards (JSON) and reports
FAILs (gate violations) and WARNs (policy advisories / friction smells).

This is a LOSSY PRE-FILTER, not an oracle: a card clearing the gate is necessary, not sufficient —
it proves the *declared* friction matches the declared (blast × reversibility) coordinate, NOT that
the action is safe. Confirm the dangerous case (high-blast / irreversible) adversarially.

Destructive-action card shape (all keys optional except `name`):
  {
    "name": "delete account",            # the action label
    "verb": "delete",                    # create/update/delete/send/publish/invite/revoke
    "blast_radius": "high",              # low | medium | high | critical  (a COUNT, not an adjective — see SKILL.md)
    "reversibility": "irreversible",     # instant | session | minutes | days | irreversible  (a DURATION, not a boolean)
    "has_confirm": false,                # any confirmation step at all
    "confirm_type": "type-to-confirm",   # type-to-confirm | reauth | confirm | click | none
    "has_undo": false,                   # an undo affordance (toast / recall) exists
    "ops_reversible": false,             # reversal is an ops/support process (refunds, payments) —
                                         # review-then-commit is the domain norm, so NO_UNDO
                                         # downgrades to an advisory note (matrix.json species)
    "has_audit_event": false,            # emits a user-visible audit event
    "bulk": true,                        # affects > 1 entity
    "has_preview": false,                # bulk: shows count + sampled preview before executing
    "default_focus": "cancel"            # initial focus of the confirm dialog: cancel | destructive
  }

  python3 scripts/safety-check.py selftest
  python3 scripts/safety-check.py <card.json | dir>
  python3 scripts/safety-check.py --json <card.json | dir>     # machine-readable report

Card files in a dir are discovered by the *.action.json suffix. Python 3.8+.
"""
import json
import os
import sys

# --- the SKILL.md vocabulary (NOT a reversible boolean — reversibility is a duration) ----------
BLAST = ["low", "medium", "high", "critical"]            # ordered; index = severity
REVERSIBILITY = ["instant", "session", "minutes", "days", "irreversible"]
CONFIRM_TYPES = {"type-to-confirm", "reauth", "confirm", "click", "none"}

# A confirm_type is "strong" if it forces deliberate friction (type the name / re-authenticate).
# A plain "confirm" dialog or a single "click" is weak for a high-blast action.
STRONG_CONFIRM = {"type-to-confirm", "reauth"}
WEAK_CONFIRM = {"confirm", "click"}


def _has_any_confirm(card):
    """True if the card declares any confirmation step (flag or non-'none' confirm_type)."""
    ct = card.get("confirm_type")
    return bool(card.get("has_confirm")) or (ct is not None and ct != "none")


def check_card(card):
    """Return (fails, warns, skips) for one destructive-action card."""
    fails, warns, skips = [], [], []
    name = card.get("name", "<card>")

    # --- vocabulary gates: an out-of-set value is a malformed coordinate, not a safe one ---
    blast = card.get("blast_radius")
    rev = card.get("reversibility")
    if blast is not None and blast not in BLAST:
        fails.append("%s: blast_radius %r not in %s" % (name, blast, BLAST))
        blast = None
    if rev is not None and rev not in REVERSIBILITY:
        fails.append("%s: reversibility %r not in %s" % (name, rev, REVERSIBILITY))
        rev = None
    ct = card.get("confirm_type")
    if ct is not None and ct not in CONFIRM_TYPES:
        warns.append("%s: confirm_type %r not in %s" % (name, ct, CONFIRM_TYPES))
        ct = None

    # An action with NEITHER coordinate declared can't be placed on the plane — skip, don't pass.
    # (Unclassified actions are refused; absent data is reported, never a silent PASS.)
    if blast is None and rev is None:
        skips.append("%s: no blast_radius or reversibility declared — cannot place on the "
                     "blast/reversibility plane (classify the action first)" % name)
        return fails, warns, skips

    irreversible = rev == "irreversible"
    high_blast = blast in ("high", "critical")
    has_confirm = _has_any_confirm(card)
    has_undo = bool(card.get("has_undo"))
    strong = ct in STRONG_CONFIRM

    # --- GATE: UNGUARDED_DESTRUCTIVE — high-blast OR irreversible with no confirmation at all ---
    # (the silent irreversible delete; the matrix never allows a bare action here)
    if (high_blast or irreversible) and not has_confirm and not has_undo:
        fails.append("UNGUARDED_DESTRUCTIVE %s: %s action has neither confirmation nor undo — "
                     "the matrix requires friction here (silent irreversible/high-blast delete refused)"
                     % (name, "/".join(x for x in (blast if high_blast else None, rev if irreversible else None) if x)))

    # --- GATE: NO_UNDO — an irreversible action with neither undo nor confirm ---
    #     (a *reversible* action lacking undo is only advisory)
    #     Reversibility species (matrix.json): ops_reversible:true declares reversal lives in an
    #     ops/support process (refunds, payments) — review-then-commit is the domain norm there,
    #     so NO_UNDO downgrades to an advisory note; the undo>confirm rule is for the
    #     user-reversible-in-app species only.
    ops_rev = bool(card.get("ops_reversible"))
    if irreversible and not has_undo and not has_confirm:
        if ops_rev:
            warns.append("NO_UNDO %s (note): ops-reversible action has no in-app undo — expected "
                         "(review-then-commit is the domain norm) — but the review step is missing "
                         "too; add the confirm that commits it" % name)
        else:
            fails.append("NO_UNDO %s: irreversible action has no undo AND no confirm — "
                         "irreversible actions must escalate friction (type-to-confirm), not run silently" % name)
    elif rev in ("instant", "session", "minutes", "days") and not has_undo and rev is not None:
        if ops_rev:
            # in-app undo is not expected for this species — note it, don't prescribe undo.
            warns.append("NO_UNDO %s (note): ops-reversible (%s) — no in-app undo is the domain "
                         "norm (review-then-commit), not a defect; verify the ops recovery path "
                         "is real" % (name, rev))
        else:
            # undo is the *preferred* treatment for reversible actions (undo > confirm) — advisory.
            warns.append("NO_UNDO %s: reversible (%s) action declares no undo — prefer undo over confirm "
                         "for reversible actions (undo toast >= 6s)" % (name, rev))

    # --- GATE: WEAK_CONFIRM — high-blast action guarded only by a single click / plain confirm ---
    #     SKILL.md's stance: high/critical irreversible demands type-to-confirm. A bare click is a gate fail.
    if high_blast and has_confirm and not strong and not has_undo:
        weak_kind = ct if ct in WEAK_CONFIRM else ("single click" if card.get("has_confirm") else "confirm")
        msg = ("WEAK_CONFIRM %s: %s-blast action guarded only by '%s' (no type-to-confirm / re-auth, no undo) — "
               "friction must match blast radius" % (name, blast, weak_kind))
        # high/critical + irreversible: the matrix mandates type-to-confirm → gate. Otherwise advisory.
        (fails if irreversible else warns).append(msg)

    # --- ADVISORY: missing audit event for high-blast OR irreversible ---
    if (high_blast or irreversible) and card.get("has_audit_event") is False:
        warns.append("NO_AUDIT %s: high-blast/irreversible action emits no user-visible audit event "
                     "(who/what/when/before/after)" % name)
    elif (high_blast or irreversible) and "has_audit_event" not in card:
        skips.append("%s: has_audit_event not declared — can't verify the audit-event invariant" % name)

    # --- ADVISORY: OVER_CONFIRM — a LOW-blast action gated by heavy friction (confirmation fatigue) ---
    #     SKILL.md espouses undo-over-confirm; a type-to-confirm/re-auth on a low-blast action is a friction smell.
    if blast == "low" and rev in ("instant", "session", "minutes", "days") and ct in STRONG_CONFIRM:
        warns.append("OVER_CONFIRM %s: low-blast reversible action gated by '%s' — heavy friction on a "
                     "reversible low-stakes action is confirmation fatigue; prefer undo" % (name, ct))
    # the universal-confirm smell: a plain confirm on a low-blast reversible action
    if blast == "low" and rev in ("instant", "session") and ct == "confirm":
        warns.append("OVER_CONFIRM %s: low-blast instant/session action gated by a confirm dialog — "
                     "ship an undo toast instead (undo > confirm)" % name)

    # --- GATE: destructive default-focus posture ---
    df = card.get("default_focus")
    if df == "destructive":
        fails.append("DEFAULT_DESTRUCTIVE %s: confirm dialog default-focuses the destructive CTA — "
                     "default focus MUST be Cancel (destructive defaults are refused)" % name)

    # --- ADVISORY: bulk action without preview ---
    if card.get("bulk"):
        if card.get("has_preview") is False:
            warns.append("NO_PREVIEW %s: bulk action shows no count + sampled preview before executing "
                         "(preview before bulk)" % name)
        elif "has_preview" not in card:
            skips.append("%s: bulk action but has_preview not declared — can't verify preview-before-bulk" % name)

    return fails, warns, skips


# --- selftest fixtures (locked: must-FLAG + must-NOT-flag, per the SKILL.md's invariants) -------
# must-NOT-flag: high-blast irreversible, properly escalated (type-to-confirm + undo + audit)
GOOD_HIGH = {
    "name": "delete organization", "verb": "delete", "blast_radius": "high", "reversibility": "irreversible",
    "has_confirm": True, "confirm_type": "type-to-confirm", "has_undo": True, "has_audit_event": True,
    "default_focus": "cancel",
}
# must-NOT-flag: low-blast reversible, no confirm — correctly fine (undo is enough; here it has undo)
GOOD_LOW = {
    "name": "delete draft", "verb": "delete", "blast_radius": "low", "reversibility": "instant",
    "has_confirm": False, "confirm_type": "none", "has_undo": True,
}
# must-FLAG: high-blast irreversible with NO confirmation → UNGUARDED_DESTRUCTIVE (+ NO_UNDO)
BAD_UNGUARDED = {
    "name": "wipe account", "verb": "delete", "blast_radius": "high", "reversibility": "irreversible",
    "has_confirm": False, "confirm_type": "none", "has_undo": False, "has_audit_event": True,
}
# must-FLAG: high-blast irreversible guarded only by a single click → WEAK_CONFIRM (gate, because irreversible)
BAD_WEAK = {
    "name": "delete all backups", "verb": "delete", "blast_radius": "high", "reversibility": "irreversible",
    "has_confirm": True, "confirm_type": "click", "has_undo": False, "has_audit_event": True,
}
# must-FLAG: confirm dialog default-focuses the destructive CTA → DEFAULT_DESTRUCTIVE
BAD_DEFAULT = {
    "name": "delete project", "verb": "delete", "blast_radius": "high", "reversibility": "days",
    "has_confirm": True, "confirm_type": "confirm", "has_undo": True, "has_audit_event": True,
    "default_focus": "destructive",
}
# must-WARN: low-blast reversible gated by type-to-confirm → OVER_CONFIRM (friction smell)
WARN_OVER = {
    "name": "rename my note", "verb": "update", "blast_radius": "low", "reversibility": "instant",
    "has_confirm": True, "confirm_type": "type-to-confirm", "has_undo": True,
}
# must-WARN (not fail): high-blast DAYS-reversible guarded by a single click + no undo → WEAK_CONFIRM advisory
WARN_WEAK_REVERSIBLE = {
    "name": "archive workspace", "verb": "update", "blast_radius": "high", "reversibility": "days",
    "has_confirm": True, "confirm_type": "click", "has_undo": False, "has_audit_event": True,
}
# must-NOT-flag: an ops-reversible payment on the review-then-commit norm — confirm present,
# no in-app undo, and that is the domain norm, not a defect (no NO_UNDO at all).
GOOD_PAYMENT = {
    "name": "submit payment", "verb": "send", "blast_radius": "medium", "reversibility": "irreversible",
    "has_confirm": True, "confirm_type": "confirm", "has_undo": False, "has_audit_event": True,
    "ops_reversible": True,
}
# must-WARN as a NOTE (not "prefer undo"): ops-reversible refund, reversible-in-days via ops —
# NO_UNDO downgrades to the species note instead of prescribing an undo toast.
OPS_REFUND = {
    "name": "refund charge", "verb": "update", "blast_radius": "medium", "reversibility": "days",
    "has_confirm": True, "confirm_type": "confirm", "has_undo": False, "has_audit_event": True,
    "ops_reversible": True,
}
# ops-reversible but SILENT (no confirm, no undo): NO_UNDO stays a note, but the
# UNGUARDED_DESTRUCTIVE gate still fires — even review-then-commit needs the review.
OPS_SILENT = {
    "name": "auto-charge card", "verb": "send", "blast_radius": "low", "reversibility": "irreversible",
    "has_confirm": False, "confirm_type": "none", "has_undo": False, "has_audit_event": True,
    "ops_reversible": True,
}
# must-SKIP: no coordinate declared → can't place on the plane
SKIP_NO_COORD = {"name": "mystery action", "has_confirm": True}
# malformed-but-not-crash: a bad blast value → clean FAIL, no exception
BAD_VOCAB = {"name": "bogus", "blast_radius": "apocalyptic", "reversibility": "irreversible",
             "has_confirm": True, "confirm_type": "type-to-confirm", "has_undo": True, "has_audit_event": True}


def selftest():
    errs = []

    def fails_of(c):
        return check_card(c)[0]

    def warns_of(c):
        return check_card(c)[1]

    def skips_of(c):
        return check_card(c)[2]

    # must-NOT-flag
    if fails_of(GOOD_HIGH):
        errs.append("GOOD_HIGH (escalated high-blast irreversible) produced fails: %s" % fails_of(GOOD_HIGH))
    if fails_of(GOOD_LOW):
        errs.append("GOOD_LOW (low-blast reversible w/ undo) produced fails: %s" % fails_of(GOOD_LOW))
    if any("OVER_CONFIRM" in w for w in warns_of(GOOD_LOW)):
        errs.append("GOOD_LOW wrongly flagged OVER_CONFIRM")

    # must-FLAG
    if not any("UNGUARDED_DESTRUCTIVE" in f for f in fails_of(BAD_UNGUARDED)):
        errs.append("UNGUARDED_DESTRUCTIVE not caught on silent high-blast irreversible action")
    if not any("WEAK_CONFIRM" in f for f in fails_of(BAD_WEAK)):
        errs.append("WEAK_CONFIRM not gated on click-only high-blast IRREVERSIBLE action")
    if not any("DEFAULT_DESTRUCTIVE" in f for f in fails_of(BAD_DEFAULT)):
        errs.append("DEFAULT_DESTRUCTIVE not caught (destructive default focus)")

    # must-WARN (advisory, not gate)
    if not any("OVER_CONFIRM" in w for w in warns_of(WARN_OVER)):
        errs.append("OVER_CONFIRM not warned on heavy friction over low-blast reversible action")
    if fails_of(WARN_WEAK_REVERSIBLE):
        errs.append("WEAK_CONFIRM wrongly GATED on a reversible (days) action: %s" % fails_of(WARN_WEAK_REVERSIBLE))
    if not any("WEAK_CONFIRM" in w for w in warns_of(WARN_WEAK_REVERSIBLE)):
        errs.append("WEAK_CONFIRM not warned on click-only high-blast reversible action")

    # reversibility species: ops_reversible downgrades NO_UNDO to an advisory note
    if fails_of(GOOD_PAYMENT):
        errs.append("GOOD_PAYMENT (ops-reversible, review-then-commit) produced fails: %s"
                    % fails_of(GOOD_PAYMENT))
    if any("NO_UNDO" in w for w in warns_of(GOOD_PAYMENT)):
        errs.append("GOOD_PAYMENT (confirm present) wrongly noted NO_UNDO")
    if fails_of(OPS_REFUND):
        errs.append("OPS_REFUND wrongly FAILED: %s" % fails_of(OPS_REFUND))
    if not any("NO_UNDO" in w and "review-then-commit" in w for w in warns_of(OPS_REFUND)):
        errs.append("OPS_REFUND: NO_UNDO not downgraded to the ops-reversible note")
    if any("prefer undo over confirm" in w for w in warns_of(OPS_REFUND)):
        errs.append("OPS_REFUND: undo>confirm advisory fired on an ops-reversible action")
    osf, osw = fails_of(OPS_SILENT), warns_of(OPS_SILENT)
    if any("NO_UNDO" in f for f in osf):
        errs.append("OPS_SILENT: NO_UNDO not downgraded from gate despite ops_reversible")
    if not any("NO_UNDO" in w for w in osw):
        errs.append("OPS_SILENT: downgraded NO_UNDO note missing")
    if not any("UNGUARDED_DESTRUCTIVE" in f for f in osf):
        errs.append("OPS_SILENT: UNGUARDED_DESTRUCTIVE must still gate a zero-friction action")

    # must-SKIP (never a silent pass on absent data)
    if not skips_of(SKIP_NO_COORD):
        errs.append("uncoordinated action not reported as a SKIP")
    if fails_of(SKIP_NO_COORD):
        errs.append("uncoordinated action wrongly FAILED instead of skipped")

    # malformed → clean FAIL, no crash
    try:
        bvf = fails_of(BAD_VOCAB)
    except Exception as e:  # noqa: BLE001 — the point is to prove it does NOT raise
        errs.append("malformed card crashed instead of clean FAIL: %r" % e)
        bvf = []
    if not any("not in" in f for f in bvf):
        errs.append("malformed blast_radius value not reported as a clean FAIL")

    return errs


def _iter_cards(path):
    if os.path.isdir(path):
        for dp, _, fns in os.walk(path):
            for fn in sorted(fns):
                if fn.endswith(".action.json"):
                    yield os.path.join(dp, fn)
    else:
        yield path


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("safety-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("safety-check: OK — gate + advisory + skip checks verified over good/bad/malformed fixtures")
        return 0

    as_json = False
    args = list(argv)
    if args and args[0] == "--json":
        as_json = True
        args = args[1:]
    if not args:
        sys.stderr.write("safety-check: no path given\n")
        return 2

    fails, warns, skips, n = [], [], [], 0
    for fp in _iter_cards(args[0]):
        try:
            doc = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fails.append("%s: unreadable (%s)" % (fp, e))
            continue
        cards = doc.get("actions") if isinstance(doc, dict) and "actions" in doc else doc
        for card in (cards if isinstance(cards, list) else [cards]):
            if not isinstance(card, dict):
                fails.append("%s: card is not an object (%r)" % (fp, type(card).__name__))
                continue
            n += 1
            f, w, s = check_card(card)
            fails += f
            warns += w
            skips += s

    if as_json:
        print(json.dumps({"cards": n, "fails": fails, "warns": warns, "skips": skips,
                          "ok": not fails}, indent=2))
        return 1 if fails else 0

    for s in skips:
        print("  ~ SKIP %s" % s)
    for w in warns:
        print("  ⚠ %s" % w)
    if fails:
        sys.stderr.write("safety-check: FAIL (%d)\n" % len(fails))
        for f in fails:
            sys.stderr.write("  - %s\n" % f)
        return 1
    print("safety-check: OK — %d card(s) clear the gates (%d skipped checks, %d advisories)"
          % (n, len(skips), len(warns)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
