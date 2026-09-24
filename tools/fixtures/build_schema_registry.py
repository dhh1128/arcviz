"""Populate refs/schema-registry.json from the three known publishers, every entry verified.

READ FROM COMMITTED STATE, NOT WORKING TREES. A working copy is somebody's edit in progress --
Provenant's gcd.schema.json was syntactically broken on disk while its committed version is
fine -- and a registry of what a publisher PUBLISHES should not depend on who happens to be
mid-keystroke.

EVERY SAID IS RECOMPUTED rather than copied. That is the line arcviz draws anyway: it may
compute and must not adjudicate. A digest matches or it does not, so no trust in bakobo,
Provenant or GLEIF is required for the answer, and an entry that fails is dropped rather than
recorded.

A registry maps SAIDs for two KINDS of object. A schema SAIDs on `$id`; an ACDC rules block
SAIDs on `d`. Only schemas can appear in a credential's `s` field, so only schemas are useful
to arcviz -- but the rules blocks are counted, because sixteen of them briefly looked like
sixteen broken schemas and the distinction is worth not rediscovering.
"""
import json
import pathlib
import subprocess
import sys
import urllib.request

from keri.core import coring

OUT = pathlib.Path(sys.argv[1])


def git_show(repo, path):
    r = subprocess.run(["git", "-C", str(repo), "show", f"HEAD:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def role_of(schema, which):
    props = schema.get("properties") or {}
    if which == "i":
        node = props.get("i") or {}
    else:
        a = props.get("a") or {}
        node = {}
        for v in (a.get("oneOf") or [a]):
            inner = (v or {}).get("properties") or {}
            if "i" in inner:
                node = inner["i"]
                break
    return ((node.get("description") or node.get("title") or "").strip()) or None


def pinned_edges(schema):
    e = (schema.get("properties") or {}).get("e") or {}
    out = []
    for variant in (e.get("oneOf") or [e]):
        if not isinstance(variant, dict):
            continue
        required = set(variant.get("required") or ())
        for label, blk in (variant.get("properties") or {}).items():
            if label in ("d", "u") or label not in required or not isinstance(blk, dict):
                continue
            if ((blk.get("properties") or {}).get("s") or {}).get("const"):
                out.append(label)
    return sorted(set(out))


def entry_for(doc, origin, ref, url=None):
    e = {"title": doc.get("title"), "origin": origin, "ref": ref,
         "verified": "2026-09-24, SAID recomputed with keripy Saider.saidify(label='$id')"}
    if doc.get("credentialType"):
        e["credential_type"] = doc["credentialType"]
    if url:
        e["url"] = url
    ir, ee = role_of(doc, "i"), role_of(doc, "a.i")
    if ir:
        e["issuer_role"] = ir
    if ee:
        e["issuee_role"] = ee
    if ir and ee:
        e["entailed"] = ["issuer", "issuee"]
    pe = pinned_edges(doc)
    if pe:
        e["pinned_edges"] = pe
    return e


known, stats = {}, {}

for origin, repo, base in (
        ("bakobo", pathlib.Path.home() / "code/bakobo/schema", "https://schema.bakobo.com/"),
        ("provenant", pathlib.Path.home() / "code/provenant/public-schema", None)):
    reg = json.loads(git_show(repo, "registry.json"))
    c = {"in_registry": len(reg), "schemas": 0, "rules_blocks": 0, "dropped": 0}
    for said, rel in sorted(reg.items()):
        raw = git_show(repo, rel)
        if raw is None:
            c["dropped"] += 1
            continue
        try:
            doc = json.loads(raw)
        except Exception:
            c["dropped"] += 1
            continue
        label = "$id" if "$id" in doc else ("d" if "d" in doc else None)
        if label is None:
            c["dropped"] += 1
            continue
        try:
            saider, _ = coring.Saider.saidify(sad=json.loads(raw), label=label)
        except Exception:
            c["dropped"] += 1
            continue
        if saider.qb64 != said:
            c["dropped"] += 1
            continue
        if label == "d":
            c["rules_blocks"] += 1      # a rules block, not a credential type
            continue
        new = entry_for(doc, origin, rel, (base + rel) if base else None)
        if said in known:
            # Two publishers serving one content-addressed document is REDUNDANCY, not a
            # conflict: the SAID proves the bytes are identical whatever the paths say. Seven
            # of these exist between bakobo and Provenant, and recording both means a
            # resolution failure at one host is answerable at the other.
            known[said].setdefault("also_published_by", []).append(
                {"origin": origin, "ref": rel,
                 "url": (base + rel) if base else None})
        else:
            known[said] = new
        c["schemas"] += 1
    stats[origin] = c

# vLEI / GLEIF. These repos name files by credential type rather than by SAID, so the set has
# to be enumerated rather than looked up -- which is exactly why naming them here is worth
# doing: it turns a non-addressable source into an addressable one for the common cases.
VLEI_BASE = "https://raw.githubusercontent.com/WebOfTrust/vLEI/dev/schema/acdc/"
VLEI_FILES = [
    "qualified-vLEI-issuer-vLEI-credential.json",
    "legal-entity-vLEI-credential.json",
    "legal-entity-official-organizational-role-vLEI-credential.json",
    "legal-entity-engagement-context-role-vLEI-credential.json",
    "oor-authorization-vlei-credential.json",
    "ecr-authorization-vlei-credential.json",
]
c = {"tried": len(VLEI_FILES), "schemas": 0, "dropped": 0}
for fn in VLEI_FILES:
    try:
        with urllib.request.urlopen(VLEI_BASE + fn, timeout=25) as r:
            raw = r.read().decode()
    except Exception:
        c["dropped"] += 1
        continue
    try:
        doc = json.loads(raw)
        saider, _ = coring.Saider.saidify(sad=json.loads(raw), label="$id")
    except Exception:
        c["dropped"] += 1
        continue
    if saider.qb64 != doc.get("$id"):
        c["dropped"] += 1
        continue
    known[saider.qb64] = entry_for(doc, "weboftrust-vlei", fn, VLEI_BASE + fn)
    c["schemas"] += 1
stats["weboftrust-vlei"] = c

existing = json.loads(OUT.read_text())
known["_comment"] = existing["known_schemas"]["_comment"]
existing["known_schemas"] = known
existing["updated"] = "2026-09-24"
existing["verification"] = {
    "method": "Every entry's SAID was recomputed from the document with keripy's "
              "Saider.saidify and compared to the key it is filed under. Entries that did not "
              "match were DROPPED, not recorded. Local sources were read from committed state "
              "(git show HEAD:) rather than from working trees, because a working copy is "
              "somebody's edit in progress.",
    "why": "A schema is content-addressed, so this is computation and not trust. Copying a "
           "publisher's asserted SAID would make this a record of claims; recomputing makes it "
           "a record of facts, and needs no relationship with any publisher.",
    "two_kinds": "A publisher's registry maps SAIDs for schemas AND for ACDC rules blocks. A "
                 "schema SAIDs on `$id`, a rules block on `d`. Only schemas can appear in a "
                 "credential's `s` field, so only schemas are recorded here -- but rules blocks "
                 "are counted, because sixteen of bakobo's briefly looked like sixteen broken "
                 "schemas before the distinction was noticed.",
    "counts": stats,
}
OUT.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(stats, indent=2))
print("known_schemas:", len([k for k in known if not k.startswith("_")]))
