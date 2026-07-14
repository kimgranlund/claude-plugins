#!/usr/bin/env python3
"""routing-eval.py — the routing-decomposer routing-LEGIBILITY AID. Self-contained (stdlib only).

THIS IS NOT THE PROOF. It is a cheap, transparent aid that lists phrase-level routing MISSES so you
know where to look — it does NOT certify a description. A green F1 here is *not* evidence of a good
description (a grammarless keyword list that echoes the corpus tokens scores F1 1.000), and a red F1
may be a proxy artifact, not a defect. The pass condition for a description is the `description-lint`
pass + a human read of the named misses/grabs — never an F1 number. (See `references/policy.md`.)

What it measures, and ONLY what it measures: LEXICAL TOKEN OVERLAP between a phrase and the
description. It therefore:
  • CANNOT grade B4 robustness (paraphrase / indirect / synonym routing). A genuine paraphrase
    positive that shares no surface words scores recall 0.000 here — that is a measurement limit of
    the proxy, NOT a description defect. Do not read a low recall on indirect phrasings as a bug.
  • parses the description into POSITIVE routing tokens (what the skill IS for) and FENCED tokens
    (the sibling vocabulary after a "NOT for …" clause — what it is NOT for). Overlap with the
    positive tokens RAISES a phrase's route-here score; overlap with the FENCED tokens REPELS it
    (lowers it). This is the central fix: a truthful sibling fence must HELP precision, not hurt it —
    so the fence's tokens act as a repellent, never a magnet.

Corpus (JSON):
  { "positives": ["decompose this skill's description", "grade the routing surface", ...],
    "negatives": ["author a whole new skill end to end", "score a UI layout", ...] }

  python3 bin/routing-eval.py selftest
  python3 bin/routing-eval.py <description.txt> <corpus.json> [--threshold 0.34] [--min-f1 0.7]

`--min-f1` (default 0.7) makes the aid exit nonzero on a low F1 so CI can SURFACE a routing regression
— it is a tripwire to prompt a human read, NOT a certification. Python 3.8+.
"""
import json
import re
import sys

# Tokens with no routing signal — they appear in nearly every description and request, so counting
# them as "overlap" would let a vague description match everything. Stripping them is what makes the
# overlap score track *concrete* trigger signal rather than filler.
STOP = {
    "a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "is", "it", "this", "that",
    "with", "as", "at", "by", "be", "are", "from", "into", "over", "your", "you", "i", "we",
    "do", "does", "not", "no", "use", "using", "used", "when", "what", "which", "how", "can",
    "should", "would", "will", "my", "our", "its", "their", "them", "these", "those", "any",
    "all", "some", "one", "two", "up", "out", "if", "so", "but", "than", "then", "also", "via",
    "per", "each", "etc", "eg", "ie", "vs", "across", "about", "more", "less", "new", "make",
}
# Light stemming so "routing" matches "route", "triggers" matches "trigger", etc. Order matters:
# longest suffix first.
_SUFFIXES = ("ization", "izations", "ingly", "ing", "ied", "ies", "ied", "ers", "er", "ed", "es", "s")


def _stem(tok):
    for suf in _SUFFIXES:
        if len(tok) > len(suf) + 2 and tok.endswith(suf):
            return tok[: -len(suf)]
    return tok


def tokenize(text):
    """Lowercase content tokens (stemmed, stopwords + sub-3-char noise removed)."""
    raw = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]*", text.lower())
    out = []
    for t in raw:
        t = t.strip("-_")
        if not t or t in STOP or len(t) < 3:
            continue
        out.append(_stem(t))
    return out


# A "NOT for …" clause names the FENCED territory — the sibling vocabulary the skill explicitly is
# *not* for. Those tokens are negative routing signal: a phrase that overlaps them should be
# REPELLED, not matched. We split the description at the first fence marker so the fence's tokens
# never leak into the positive routing set (the bug this fix removes).
#
# HARDENED 2026-07-04: only the DELIBERATE house forms parse as fence markers. Bare "does not" was
# removed from the set — it matched ordinary prose anywhere in a description ("it grades, it does
# not build"; "ANSWERS…, it does not generate") and silently truncated the positive zone at that
# point, fencing every trigger that followed. Proven live: component-reviewer's F1 measured 0.375
# solely because its own role sentence tripped the marker; two more instances found corpus-wide
# (ui-genres, ui-patterns). A fence is a deliberate act in the house grammar, never a side effect
# of natural prose.
_FENCE_MARKERS = re.compile(
    r"(?i)\b(?:not\s+for|not\s+when|do(?:es)?\s*n['’]?ot\s+trigger|don['’]?t\s+trigger|never\s+for)\b"
)


def split_fence(description):
    """Return (positive_text, fenced_text). Everything from the first fence marker onward is fenced
    (the NOT-for territory); everything before it is the positive claim + triggers."""
    m = _FENCE_MARKERS.search(description)
    if not m:
        return description, ""
    return description[: m.start()], description[m.start():]


def description_tokens(description):
    """The set of POSITIVE content tokens the description offers as routing signal — i.e. with any
    NOT-for fenced vocabulary stripped OUT, so the fence can never act as a match magnet."""
    pos_text, _ = split_fence(description)
    return set(tokenize(pos_text))


def fenced_tokens(description):
    """The set of FENCED content tokens — the sibling vocabulary after a NOT-for clause — that should
    REPEL a phrase (lower its route-here score), minus anything also in the positive set."""
    pos_text, fenced_text = split_fence(description)
    fenced = set(tokenize(fenced_text))
    return fenced - set(tokenize(pos_text))


def routes_here(phrase, desc_tokens, threshold, fence_tokens=frozenset()):
    """Deterministic LEXICAL-OVERLAP proxy for 'would the model route this phrase to this skill?'.

    Base score = fraction of the PHRASE's content tokens that the description's POSITIVE set carries.
    Then the fence REPELS: each phrase token that overlaps the fenced (NOT-for) vocabulary subtracts
    from the score, so a truthful sibling fence pushes a sibling phrase BELOW threshold instead of
    pulling it above. A phrase routes here iff the net score clears the threshold. Returns
    (bool, score). Measures lexical overlap only — blind to paraphrase/synonyms (cannot grade B4)."""
    pset = set(tokenize(phrase))
    if not pset:
        return (False, 0.0)
    n = len(pset)
    hits = sum(1 for t in pset if t in desc_tokens)
    repelled = sum(1 for t in pset if t in fence_tokens and t not in desc_tokens)
    score = (hits - repelled) / n
    return (score >= threshold, score)


def evaluate(description, corpus, threshold=0.34):
    """Run the lexical-overlap routing proxy over the corpus; return a metrics + diagnostics dict.
    This is a legibility AID (lists phrase-level misses), NOT a certification — see module docstring."""
    dt = description_tokens(description)
    ft = fenced_tokens(description)
    pos = corpus.get("positives", []) or []
    neg = corpus.get("negatives", []) or []
    tp, fn, missed = 0, 0, []
    for p in pos:
        ok, sc = routes_here(p, dt, threshold, ft)
        if ok:
            tp += 1
        else:
            fn += 1
            missed.append((p, round(sc, 2)))
    fp, tn, grabbed = 0, 0, []
    for neg_phrase in neg:
        ok, sc = routes_here(neg_phrase, dt, threshold, ft)
        if ok:
            fp += 1
            grabbed.append((neg_phrase, round(sc, 2)))
        else:
            tn += 1
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    # Legibility caveat: a "green" F1 is gameable — a grammarless keyword list echoing the corpus
    # tokens scores F1 1.000. So we record the SHAPE of the description (does it quote triggers? does
    # it carry a fence?) as a hint that a high F1 here is or isn't backed by a real routing surface.
    _, fenced_text = split_fence(description)
    has_fence = bool(fenced_text.strip())
    has_quoted_triggers = bool(re.search(r'"[^"]{3,}"', description))
    return {
        "n_pos": len(pos), "n_neg": len(neg),
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3),
        "has_fence": has_fence,                      # description carries a NOT-for clause
        "has_quoted_triggers": has_quoted_triggers,  # description quotes concrete trigger phrases
        "fenced_token_count": len(ft),
        "missed_positives": missed,      # recall holes — under-trigger
        "grabbed_negatives": grabbed,    # precision holes — over-trigger
        "threshold": threshold,
        "desc_token_count": len(dt),
    }


# --- selftest fixtures -------------------------------------------------------------------------
# A well-built description: names its capability (grade/decompose a skill's description/routing),
# its scope (precision/recall, the eval corpus), and concrete triggers — and is fenced against the
# sibling (whole-skill authoring).
GOOD_DESC = (
    "Grade and decompose the routing surface of a skill — its frontmatter description — measuring "
    "whether it fires on the right requests and holds against the wrong ones. Run a routing eval "
    "over a labeled corpus of trigger phrases to score precision, recall, and F1, then fix the "
    "wording that mis-routes (under-trigger or over-trigger). Triggers on: grade this description, "
    "is this description routing correctly, why does my skill not fire, why does it over-trigger, "
    "score the routing, build a routing corpus. NOT for authoring a whole skill end to end "
    "(skills-studio)."
)
GOOD_CORPUS = {
    "positives": [
        "grade this skill's description",
        "is my description routing correctly",
        "why does my skill never fire on real requests",
        "this skill over-triggers and grabs the wrong requests",
        "score the precision and recall of this routing surface",
        "build a routing corpus for my skill",
        "measure whether this description fires on the right phrases",
        "fix the wording that mis-routes",
    ],
    "negatives": [
        "author a whole new skill from scratch end to end",
        "run the adversarial critic panel on my plugin",
        "decompose this UI layout into regions",
        "grade a unit of code against its contract",
        "convert design tokens between formats",
        "write the CSS for this component",
    ],
}
# A description that READS well but MIS-ROUTES: it describes the capability in abstract,
# capability-honest prose but names none of the concrete trigger words the requests use, so it
# under-triggers (low recall). This is the "reads well, mis-routes" quadrant — the eval must catch it.
MISROUTING_DESC = (
    "An instrument for the qualitative appraisal of textual metadata pertaining to the "
    "discoverability of capabilities within an agentic context, emphasizing rhetorical clarity and "
    "the felicitous selection of lexical signifiers."
)
# A description so broad it grabs the sibling negatives too — over-trigger (low precision).
OVERBROAD_DESC = (
    "Grade, score, decompose, review, audit, evaluate, check, measure, analyze, and improve any "
    "skill, description, layout, component, code, token, corpus, plugin, routing, UI, and contract "
    "for quality, correctness, fit, and coherence across every axis and dimension."
)

# --- B1 regression fixture: the fence must REPEL, not MAGNETIZE ---------------------------------
# The skill's central doctrine is "add a truthful NOT-for fence naming the sibling". The OLD proxy
# inverted this: the fence's sibling tokens ("layout", "code") overlapped negatives drawn from those
# siblings, so adding the fence GREW precision holes. These paired fixtures pin the fix: the SAME
# description WITH a truthful sibling fence must score precision/F1 >= the same description WITHOUT it.
FENCE_BASE_DESC = (
    "Grade the routing surface of a skill — its frontmatter description. Run a routing eval over a "
    "labeled corpus to score precision and recall. Triggers on: grade this description, score the "
    "routing precision and recall, build a routing corpus, why does my skill not fire."
)
FENCE_WITH_DESC = (
    FENCE_BASE_DESC
    + " NOT for grading a UI layout into regions (layout-decomposer); NOT for grading a unit of code "
      "against its contract (code-decomposer)."
)
# Negatives drawn from the very siblings the fence names — the adversarial case the old proxy failed.
FENCE_CORPUS = {
    "positives": [
        "grade this skill description",
        "score the routing precision and recall",
        "build a routing corpus",
        "why does my skill not fire",
    ],
    "negatives": [
        "grade this UI layout into regions",
        "decompose this layout into regions",
        "grade a unit of code against its contract",
        "review this code function for bugs",
    ],
}

# --- M2 gameability fixture: a green F1 is NOT a good-description certificate --------------------
# The eval is trivially gamed: a grammarless keyword list that ECHOES the corpus positives' own
# tokens (and nothing else) scores F1 ~1.000 — no capability claim, no fence, no quoted triggers, no
# grammar. Building it from the corpus is the point: an adversary optimizing for the number harvests
# exactly these words. The selftest asserts the eval STILL scores it green (we don't pretend the
# proxy catches this) AND flags it fence-less / quote-less — the signal the framing uses to say
# "F1 alone is not the proof; the pass condition is description-lint + a human read".
def _gamed_keyword_list(corpus):
    toks = []
    for p in corpus.get("positives", []):
        toks.extend(tokenize(p))
    # de-dup preserving order; pure tokens, no punctuation, no grammar, no fence
    seen, out = set(), []
    for t in toks:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return " ".join(out)


def selftest():
    errs = []
    # 1. tokenize strips stopwords / short noise / stems
    toks = set(tokenize("Grade the ROUTING of a skill's descriptions"))
    if "the" in toks or "of" in toks:
        errs.append("tokenize did not strip stopwords: %s" % sorted(toks))
    if "rout" not in toks and "route" not in toks and "routing" not in toks:
        errs.append("tokenize lost the 'routing' signal: %s" % sorted(toks))
    if "description" not in toks and "descript" not in toks:
        errs.append("tokenize/stem dropped 'descriptions': %s" % sorted(toks))

    # 2. the GOOD description scores well — high F1, fires on its positives, holds its negatives
    g = evaluate(GOOD_DESC, GOOD_CORPUS)
    if g["f1"] < 0.7:
        errs.append("GOOD description scored F1=%.2f (< 0.7); missed=%s grabbed=%s"
                    % (g["f1"], g["missed_positives"], g["grabbed_negatives"]))
    if g["recall"] < 0.7:
        errs.append("GOOD description recall too low: %.2f (missed %s)" % (g["recall"], g["missed_positives"]))
    if g["precision"] < 0.7:
        errs.append("GOOD description precision too low: %.2f (grabbed %s)" % (g["precision"], g["grabbed_negatives"]))

    # 3. the MIS-ROUTING (reads-well-but-vague) description under-triggers: it must MISS positives
    m = evaluate(MISROUTING_DESC, GOOD_CORPUS)
    if not m["missed_positives"]:
        errs.append("mis-routing description wrongly fired on every positive (recall=%.2f)" % m["recall"])
    if m["recall"] >= g["recall"]:
        errs.append("mis-routing description should have LOWER recall than GOOD (%.2f vs %.2f)"
                    % (m["recall"], g["recall"]))

    # 4. the OVER-BROAD description over-triggers: it must GRAB negatives (precision hole)
    o = evaluate(OVERBROAD_DESC, GOOD_CORPUS)
    if not o["grabbed_negatives"]:
        errs.append("over-broad description wrongly held all negatives (precision=%.2f)" % o["precision"])
    if o["precision"] >= g["precision"]:
        errs.append("over-broad description should have LOWER precision than GOOD (%.2f vs %.2f)"
                    % (o["precision"], g["precision"]))

    # 5. routes_here is monotone in overlap and empty-safe
    dt = description_tokens(GOOD_DESC)
    if routes_here("", dt, 0.34)[0]:
        errs.append("empty phrase wrongly routed")
    on, son = routes_here("grade this skill's description routing", dt, 0.34)
    off, soff = routes_here("xyzzy plugh quux frobnitz", dt, 0.34)
    if not on or off:
        errs.append("routes_here on/off-target wrong: on=%s(%.2f) off=%s(%.2f)" % (on, son, off, soff))

    # 6. B1 REGRESSION — the truthful sibling fence must REPEL, not MAGNETIZE.
    #    The SAME description WITH a fence naming the siblings must score precision/F1 >= WITHOUT it.
    #    (Before the fix this was reversed: the fence's tokens grabbed the sibling negatives.)
    nf = evaluate(FENCE_BASE_DESC, FENCE_CORPUS)
    wf = evaluate(FENCE_WITH_DESC, FENCE_CORPUS)
    if wf["precision"] < nf["precision"]:
        errs.append("B1 INVERSION: fenced precision %.3f < unfenced %.3f — the fence is acting as a "
                    "magnet, not a repellent" % (wf["precision"], nf["precision"]))
    if wf["f1"] < nf["f1"]:
        errs.append("B1 INVERSION: fenced F1 %.3f < unfenced %.3f — adding the doctrine's NOT-for "
                    "fence made routing WORSE" % (wf["f1"], nf["f1"]))
    if wf["grabbed_negatives"]:
        errs.append("B1: fenced description still grabs sibling negatives it explicitly fences: %s"
                    % wf["grabbed_negatives"])
    if wf["recall"] < nf["recall"]:
        errs.append("B1: the fence dropped a real positive (recall %.3f < %.3f) — fence should only "
                    "touch the NOT-for vocabulary" % (wf["recall"], nf["recall"]))
    if not wf["has_fence"]:
        errs.append("B1: fenced fixture not detected as carrying a fence")

    # 7. FENCE-MARKER HARDENING (2026-07-04) — ordinary "does not" prose must NOT truncate the
    #    positive zone (the component-reviewer regression: F1 0.375 from its own role sentence).
    prose_desc = (
        "Grade the routing surface of a skill; it grades, it does not build. Triggers on: "
        "grade this description, score the routing precision and recall, build a routing corpus. "
        "NOT for authoring a whole skill end to end (skills-studio)."
    )
    pos_text, fenced_text = split_fence(prose_desc)
    if "build a routing corpus" not in pos_text:
        errs.append("FENCE HARDENING regression: ordinary 'does not' prose truncated the positive "
                    "zone — triggers after it were fenced out")
    if "skills-studio" not in fenced_text:
        errs.append("FENCE HARDENING: the deliberate NOT-for fence must still parse (fenced zone "
                    "lost skills-studio)")
    on_trigger, _ = routes_here("build a routing corpus", description_tokens(prose_desc), 0.34,
                                fenced_tokens(prose_desc))
    if not on_trigger:
        errs.append("FENCE HARDENING: a trigger placed after ordinary 'does not' prose must route")
    # the explicit trigger-forms stay parseable as deliberate fences
    m = _FENCE_MARKERS.search("routes X. Does not trigger on Y (owner).")
    if not m:
        errs.append("FENCE HARDENING: 'does not trigger' must still parse as a deliberate fence marker")

    # 8. M2 GAMEABILITY — a grammarless keyword list echoing the corpus scores green F1 but is NOT a
    #    good description. The eval must still score it green (we don't pretend the proxy catches it)
    #    AND must flag it as fence-less / quote-less so the framing can say "F1 alone is not the proof".
    gamed_list = _gamed_keyword_list(GOOD_CORPUS)
    gamed = evaluate(gamed_list, GOOD_CORPUS)
    if gamed["f1"] < 0.99:
        errs.append("M2: keyword-list fixture unexpectedly did NOT game the eval (F1=%.3f) — echoing "
                    "the corpus tokens should score ~1.0, demonstrating the gameability the framing warns about"
                    % gamed["f1"])
    if gamed["has_fence"] or gamed["has_quoted_triggers"]:
        errs.append("M2: keyword list wrongly reported as having a fence/quoted triggers: fence=%s quoted=%s"
                    % (gamed["has_fence"], gamed["has_quoted_triggers"]))
    return errs


def _fmt_metrics(m):
    print("routing-eval (lexical-overlap AID — NOT a certification) — %d positive(s), %d negative(s), "
          "threshold %.2f, %d positive token(s), %d fenced token(s)"
          % (m["n_pos"], m["n_neg"], m["threshold"], m["desc_token_count"], m["fenced_token_count"]))
    print("  precision %.3f   recall %.3f   F1 %.3f   (tp=%d fp=%d fn=%d tn=%d)"
          % (m["precision"], m["recall"], m["f1"], m["tp"], m["fp"], m["fn"], m["tn"]))
    if m["missed_positives"]:
        print("  recall holes — positives that do NOT route here (lexical miss; may be a PARAPHRASE "
              "the proxy can't see, NOT a defect — read each):")
        for p, sc in m["missed_positives"]:
            print("    ✗ %.2f  %s" % (sc, p))
    if m["grabbed_negatives"]:
        print("  precision holes — negatives this WRONGLY grabs (over-trigger):")
        for n, sc in m["grabbed_negatives"]:
            print("    ✗ %.2f  %s" % (sc, n))
    if not m["missed_positives"] and not m["grabbed_negatives"]:
        print("  · every corpus positive cleared threshold and every negative held — but this is "
              "lexical overlap only; confirm with description-lint + a human read")
    if not m["has_quoted_triggers"]:
        print("  ⚠ description quotes NO concrete trigger phrases — a green F1 here can be a keyword "
              "list gaming the overlap; the pass condition is the read, not this number")
    if not m["has_fence"]:
        print("  ⚠ description carries NO NOT-for fence — precision against real siblings is untested")


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("routing-eval: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("routing-eval: OK — tokenizer + overlap proxy + fence-repels-not-magnetizes (B1) + "
              "fence-marker hardening (ordinary 'does not' prose never truncates; deliberate forms "
              "still parse) + gameability/paraphrase-blindness caveats verified")
        return 0
    if len(argv) < 2:
        sys.stderr.write("usage: routing-eval.py <description.txt> <corpus.json> [--threshold T] [--min-f1 F]\n")
        return 2
    desc_path, corpus_path = argv[0], argv[1]
    threshold = float(argv[argv.index("--threshold") + 1]) if "--threshold" in argv else 0.34
    min_f1 = float(argv[argv.index("--min-f1") + 1]) if "--min-f1" in argv else 0.7
    try:
        description = open(desc_path, encoding="utf-8").read()
        corpus = json.load(open(corpus_path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write("routing-eval: bad input — %s\n" % e)
        return 2
    if not isinstance(corpus, dict) or not (corpus.get("positives") or corpus.get("negatives")):
        sys.stderr.write("routing-eval: corpus must be {\"positives\":[...], \"negatives\":[...]}\n")
        return 2
    m = evaluate(description, corpus, threshold)
    _fmt_metrics(m)
    if m["f1"] < min_f1:
        sys.stderr.write("routing-eval: TRIPPED — F1 %.3f below --min-f1 %.2f. This SURFACES a "
                         "routing concern for a human read; it is not a verdict. Read each named miss: "
                         "a lexical miss on a direct phrasing → add the trigger word the request uses; "
                         "a grab → tighten scope / add a NOT-for fence. A miss on a PARAPHRASE may be "
                         "a proxy artifact (this tool grades lexical overlap only, not B4 robustness).\n"
                         % (m["f1"], min_f1))
        return 1
    print("routing-eval: clear — F1 %.3f >= %.2f (a legibility check, not a pass; the description "
          "passes only on description-lint + a human read of the misses/grabs)" % (m["f1"], min_f1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
