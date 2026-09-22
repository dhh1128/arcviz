#!/usr/bin/env python3
"""Measure classify.py against the catalog, and be explicit about what 'ground truth' means here.

Ground truth is ONE PERSON'S READING -- the `Subject` column of README.md, which the catalog
already marks as derived rather than sourced, plus the override table below for the handful of
rows where the issuer/holder/subject configuration is what matters and the Subject column does not
capture it. It is not an authority. A disagreement between the classifier and this file is a
prompt to look at the row, not a verdict that the classifier is wrong.

What this script is actually for is the three numbers that decide whether a deterministic scheme
is viable at all:

  COVERAGE   how many rows carry enough machine-readable input to be classified even in principle
  AGREEMENT  of those, how many the rules get right
  FAILURES   which rows they get wrong, and whether the misses share a cause

Run: python3 evaluate.py        (expects rows.json beside it)
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import classify

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------------
# Truth, part 1: roll the catalog's derived Subject column up into the spine's vocabulary.
# --------------------------------------------------------------------------------------------

def subject_bucket(s: str) -> str:
    t = s.lower().replace("**", "")
    if any(k in t for k in ("another acdc", "another credential", "presentation", "a schema",
                            "credential statuses", "set of issuers", "collection", "the dossier",
                            "financial report", "external content", "certificate itself")):
        return "ASSEMBLY"
    if any(k in t for k in ("wallet", "keystore", "the verifier", "zero-attribute")) or t == "key":
        return "APPARATUS"
    if "ai agent" in t:
        return "ABOUT_AN_AGENT"
    if any(k in t for k in ("product", "device", "vehicle", "bicycle", "artifact", "data",
                            "stored value", "capability over a thing", "shipment")):
        return "ABOUT_A_THING"
    if any(k in t for k in ("transaction", "observation event", "event plus", "journey", "admission",
                            "booking", "permitted action", "disclosure act", "call /")) and "health" not in t:
        return "ABOUT_AN_OCCURRENCE"
    if any(k in t for k in ("entitlement", "offer", "redeemable", "permission", "bearer", "residual")):
        return "BEARER"
    if any(k in t for k in ("person", "legal entity", "two people", "issuer (self", "guardian",
                            "relationship between two people", "commercial relationship",
                            "delegation relationship", "authorization relationship",
                            "relation to a third party", "campaign", "varies")):
        return "ORDINARY"
    return "UNSORTED"


# Truth, part 2: rows where the configuration of issuer, holder and subject is the point, and the
# Subject column alone does not carry it. Each entry is a judgement, and each is stated so it can
# be argued with.
OVERRIDES = {
    10: "SELF",                 # ai-user-coca -- the issuer commits, about itself
    15: "SELF",                 # BindKeyAttestation -- the issuer's own key
    121: "SELF",                # self-issued driver's licence
    154: "SELF",                # food preference, issuer and holder one DID, no subject id
    4: "INVERTED",              # SEDI age-portrait presentation -- issuee is the verifier
    78: "INVERTED",             # relying-party registration certificate
    116: "ABOUT_ANOTHER_PARTY", # the recipient family's banking details
    127: "ABOUT_ANOTHER_PARTY", # child travel pass -- subject is the minor, holder is a parent
    108: "ABOUT_ANOTHER_PARTY", # status-check token issued by a person to his employer
    133: "BEARER",              # first-class upgrade coupon
    186: "BEARER",              # movie ticket, no identifying attribute of the bearer
    42: "BEARER",               # dossier-backed token
}

ROW_RE = re.compile(r"\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|")


def truth() -> dict[int, str]:
    out = {}
    for line in (HERE / "README.md").read_text().splitlines():
        m = ROW_RE.match(line)
        if m:
            out[int(m.group(1))] = subject_bucket(m.group(4).strip())
    out.update(OVERRIDES)
    return out


def main() -> int:
    rows = json.loads((HERE / "rows.json").read_text())
    want = truth()
    got = {r["id"]: classify.classify(r) for r in rows}

    known = [r for r in rows if r.get("fields_known")]
    print(f"catalog rows            {len(rows)}")
    print(f"rows with a field list  {len(known)}  ({len(known) * 100 // len(rows)}%)")
    print(f"rows without one        {len(rows) - len(known)}")
    by_eco = collections.Counter((r["ecosystem"], bool(r.get("fields_known"))) for r in rows)
    print("\nfield data by ecosystem")
    for eco in sorted({r["ecosystem"] for r in rows}):
        y, n = by_eco[(eco, True)], by_eco[(eco, False)]
        print(f"  {eco:12s} {y:3d} with fields, {n:3d} without")

    agree = dis = undecidable = 0
    misses = []
    for r in rows:
        g = got[r["id"]]["genus"]
        w = want.get(r["id"], "UNSORTED")
        if g == "UNDECIDABLE":
            undecidable += 1
        elif g == w:
            agree += 1
        else:
            dis += 1
            misses.append((r["id"], r["name"], w, g, got[r["id"]]["why"], r.get("fields_known")))

    decided = agree + dis
    print(f"\nGENUS\n  decided     {decided}\n  undecidable {undecidable}")
    if decided:
        print(f"  agreement   {agree}/{decided} = {agree * 100 // decided}%")

    print("\n  misses, grouped by what the truth says they are")
    for w in sorted({m[2] for m in misses}):
        group = [m for m in misses if m[2] == w]
        print(f"\n  want {w}  ({len(group)})")
        for i, n, _w, g, why, fk in group:
            flag = "" if fk else "  [no fields]"
            print(f"    {i:4d} {n[:44]:46s} got {g:20s} {why[:46]}{flag}")

    print("\nDOMAIN")
    dc = collections.Counter()
    nolabel = []
    for r in rows:
        ds = got[r["id"]]["domains"]
        if r.get("fields_known") and not ds:
            nolabel.append((r["id"], r["name"]))
        for d in ds:
            dc[d] += 1
    for k, v in dc.most_common():
        print(f"  {v:4d}  {k}")
    print(f"\n  rows with a field list but no domain label: {len(nolabel)}")
    for i, n in nolabel[:30]:
        print(f"    {i:4d} {n[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
