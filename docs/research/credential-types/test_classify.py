#!/usr/bin/env python3
"""Test vectors for classify.py, plus a regression guard over the real catalog.

**What these tests can and cannot do, stated up front because the distinction matters.** They
cannot prove the classifier categorizes *correctly*, because there is no external authority that
says what the right category for a credential is -- the scheme is ours, the catalog's labels are
one person's reading, and a test written by the same hand that wrote the rule cannot adjudicate
between them. What they DO is pin behaviour and record decisions: every vector carries a `why`
naming the choice it defends, so that changing the answer means arguing with a written reason
rather than silently shifting a boundary. 6 of them are marked REGRESSION and each corresponds
to a defect the 2026-09-22 evaluation actually found, including the unsafe default that rendered
a wallet attestation as evidence about the person presenting it.

The catalog guard is the complement: it fails if aggregate agreement against the hand reading
drops, so a vocabulary edit that fixes one vector and breaks nine real rows cannot pass quietly.

Run:  python3 test_classify.py          (no pytest required)
      python3 -m pytest test_classify.py -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import classify  # noqa: E402
import evaluate  # noqa: E402

HERE = Path(__file__).resolve().parent

# Floors, not targets. They are the measurements from 2026-09-22 minus nothing: the point is to
# catch a regression, so they are set AT the current value rather than below it. Raising them when
# the classifier improves is deliberate work, not bookkeeping.
FLOOR_SUBJECT_AGREEMENT = 0.93
FLOOR_ALIGNMENT_AGREEMENT = 0.91
FLOOR_CATEGORY_RECALL = 0.94

SUBJECT_FROM_SINGLE = {
    "ASSEMBLY": "evidence", "APPARATUS": "apparatus", "ABOUT_A_THING": "thing",
    "ABOUT_AN_OCCURRENCE": "occurrence", "BEARER": "none", "ABOUT_AN_AGENT": "agent",
    "SELF": "party", "INVERTED": "party", "ABOUT_ANOTHER_PARTY": "party", "ORDINARY": "party",
}
ALIGNMENT_FROM_SINGLE = {
    "SELF": "self-attested", "INVERTED": "inverted",
    "ABOUT_ANOTHER_PARTY": "other-party", "ORDINARY": "ordinary",
}

# Categories the hand labels use that the collapse folded away, mapped forward so the 2026-09-21
# label set can still score the 2026-09-23 one.
COLLAPSE = {
    "IDENTITY": "identity", "AGE": "identity", "RESIDENCE": "identity", "TRAVEL": "identity",
    "ORG-IDENTITY": "org-identity", "ACADEMIC": "qualification", "LICENCE": "qualification",
    "AWARD": "qualification", "FINANCIAL": "financial", "EMPLOYMENT": "affiliation",
    "MEMBERSHIP": "affiliation", "RELATIONSHIP": "affiliation", "AUTHORITY": "authority",
    "TELECOM": "authority", "BRAND": "authority", "CONTROL": "authority", "HEALTH": "health",
    "CIVIL-STATUS": "civil-status", "HUMANNESS": "humanness", "MISC": "misc",
}


def _vectors() -> list[dict]:
    return json.loads((HERE / "test_vectors.json").read_text())["vectors"]


def test_vectors() -> list[str]:
    """Every hand-built vector, checked on all three outputs. Returns a list of failure strings."""
    failures = []
    for v in _vectors():
        row, want = v["row"], v["expect"]
        got_subject, subj_why = classify.subject_axis(row)
        got_align, align_why = classify.alignment_axis(row)
        got_cats = classify.categories(row)
        for label, got, expected, why in (
            ("subject", got_subject, want["subject"], subj_why),
            ("alignment", got_align, want["alignment"], align_why),
            ("categories", got_cats, want["categories"], ""),
        ):
            if got != expected:
                failures.append(
                    f"{v['name']}\n      {label}: wanted {expected!r}, got {got!r}"
                    + (f"\n      rule that fired: {why}" if why else "")
                    + f"\n      this vector defends: {v['why']}"
                )
    return failures


def test_category_values_are_declared() -> list[str]:
    """No vector may expect a category that is not in the declared set. Catches a typo becoming a category."""
    known = set(classify.CATEGORIES) | {classify.RESIDUAL}
    failures = []
    for v in _vectors():
        for c in v["expect"]["categories"]:
            if c not in known:
                failures.append(f"{v['name']}: expects undeclared category {c!r}")
    return failures


def test_lower_kebab() -> list[str]:
    """Every category and axis value is lower-kebab. Daniel asked for it; this keeps it true."""
    failures = []
    for name, values in (
        ("CATEGORIES", classify.CATEGORIES + [classify.RESIDUAL]),
        ("SUBJECT_VALUES", classify.SUBJECT_VALUES),
        ("ALIGNMENT_VALUES", classify.ALIGNMENT_VALUES),
    ):
        for v in values:
            if v != v.lower() or "_" in v or " " in v:
                failures.append(f"{name}: {v!r} is not lower-kebab")
    return failures


def test_catalog_regression() -> list[str]:
    """Aggregate agreement over the 195 real rows must not drop. Guards against a local fix that breaks the whole."""
    rows = json.loads((HERE / "rows.json").read_text())
    single = evaluate.truth()
    dom = {int(k): v for k, v in json.loads((HERE / "domain_truth.json").read_text()).items()}
    failures = []

    for axis_name, fn, mapping, floor in (
        ("subject", classify.subject_axis, SUBJECT_FROM_SINGLE, FLOOR_SUBJECT_AGREEMENT),
        ("alignment", classify.alignment_axis, ALIGNMENT_FROM_SINGLE, FLOOR_ALIGNMENT_AGREEMENT),
    ):
        agree = decided = 0
        for r in rows:
            want = mapping.get(single.get(r["id"]))
            if want is None:
                continue
            got, _ = fn(r)
            if got == "unknown":
                continue
            decided += 1
            agree += got == want
        rate = agree / decided if decided else 0.0
        if rate < floor:
            failures.append(f"{axis_name} agreement {agree}/{decided} = {rate:.2f}, below floor {floor}")

    tp = fn_ = 0
    for r in rows:
        want_raw = dom.get(r["id"])
        if want_raw is None or not r.get("fields_known"):
            continue
        want = {COLLAPSE[x] for x in want_raw} - {"misc"}
        got = set(classify.categories(r))
        tp += len(got & want)
        fn_ += len(want - got)
    recall = tp / (tp + fn_) if (tp + fn_) else 0.0
    if recall < FLOOR_CATEGORY_RECALL:
        failures.append(f"category recall {recall:.2f} below floor {FLOOR_CATEGORY_RECALL}")
    return failures


def main() -> int:
    suites = [
        ("hand-built vectors", test_vectors),
        ("declared category values", test_category_values_are_declared),
        ("lower-kebab naming", test_lower_kebab),
        ("catalog regression floors", test_catalog_regression),
    ]
    total = 0
    for name, fn in suites:
        failures = fn()
        total += len(failures)
        mark = "ok  " if not failures else "FAIL"
        print(f"{mark} {name}" + (f"  ({len(failures)} failures)" if failures else ""))
        for f in failures:
            print(f"    - {f}")
    n = len(_vectors())
    print(f"\n{n} vectors, {total} failures")
    return 1 if total else 0


# pytest entry points -- each asserts on the same functions, so either runner works.
def test_all_vectors_pass():
    assert test_vectors() == []


def test_all_categories_declared():
    assert test_category_values_are_declared() == []


def test_naming_is_lower_kebab():
    assert test_lower_kebab() == []


def test_no_catalog_regression():
    assert test_catalog_regression() == []


if __name__ == "__main__":
    raise SystemExit(main())
