#!/usr/bin/env python3
"""Compute everything the sample renders, from the corpus, and write it to public/data.json.

The sample is an instrument, not arcviz. Nothing here is the implementation: descriptors come
from `tools/describe` (whose durable spec is `vectors.json`), categories and the two structural
axes come from `docs/research/credential-types/classify.py` (synthesized, unratified rules), and
party names come from `host.json`, which stands in for the host application's alias lookup.
The React side renders what this file computes and computes nothing of its own, so a reader can
check every value on screen against one JSON file.

Three inputs are supplied by hand rather than derived, and each is flagged in the output so the
render can mark it:

  - type names and field roles for the accident schemas, which do not resolve (the test suite
    supplies the same ones, in `_accident_dag`);
  - the vLEI chain's schema entailments, BORROWED from the real vLEI schemas in
    `refs/schema-registry.json`, because the corpus chain was generated with stand-in schemas
    whose SAIDs are not the real ones;
  - the driving-licence subcategory glyph, which nothing selects yet (Daniel, Q-D4RX:
    hand-assign it and mark it as a placeholder).

Run from anywhere: `python3 samples/accident/build_data.py`. Standard library only.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORPUS = ROOT / "corpus"
PUBLIC = HERE / "public"

sys.path.insert(0, str(ROOT / "tools" / "describe"))
sys.path.insert(0, str(ROOT / "docs" / "research" / "credential-types"))

import classify  # noqa: E402
import coia_reader  # noqa: E402
import schemas  # noqa: E402
from describe import describe, load_corpus_dag  # noqa: E402

GLYPHS = ROOT / "docs" / "design" / "iconography" / "glyphs"


def category_meanings() -> dict:
    """Category -> its 'Means' text, read from the table in credential-categories.md so the
    hover text has one source. Markdown emphasis is stripped; `misc` comes from the sentence
    that defines it."""
    import re
    doc = (ROOT / "docs" / "design" / "credential-categories.md").read_text()
    out = {}
    for line in doc.splitlines():
        m = re.match(r"^\| `([a-z-]+)` \| (.+?) \|", line)
        if m:
            out[m.group(1)] = re.sub(r"[*`]", "", m.group(2)).strip()
        m = re.match(r"^`misc` is (.+)$", line)
        if m:
            tail = re.sub(r"[*`]", "", m.group(1)).rsplit(", and ", 1)[-1].strip()
            out["misc"] = "The residual. " + tail[0].upper() + tail[1:]
    return out


def sniff(b: bytes) -> str | None:
    """Media type from the bytes, never from a name. Only knowable when the bytes resolve."""
    if b.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if b.startswith(b"\xff\xd8\xff"):
        return "jpg"
    return None


def sad(name: str) -> dict:
    return json.loads((CORPUS / f"{name}.json").read_text())


def classify_node(s: dict, title: str | None = None) -> dict:
    """Run the synthesized classifier over the DISCLOSED attribute names.

    No schema document resolves for either frame, so the field list is what was disclosed, not
    what the schema declares. That is a weaker input than classify.py was measured on, and the
    render says so.
    """
    a = s.get("a") if isinstance(s.get("a"), dict) else {}
    row = {"id": s["d"], "name": s["d"], "title": title, "fields": list(a.keys()), "fields_known": True,
           "structure": {"has_issuee": "i" in a,
                         "names_other_credential": bool(s.get("e"))},
           # Disclosed values, so a bare `account` can be checked for money beside it.
           "values": a}
    subj, subj_why = classify.subject_axis(row)
    align, align_why = classify.alignment_axis(row)
    cats = classify.categories(row)
    why = classify.category_evidence(row)
    return {"categories": cats, "category_hits": why,
            "subject": subj, "subject_why": subj_why,
            "alignment": align, "alignment_why": align_why,
            "input": "disclosed attribute names; no schema resolved"}


def component_json(c) -> dict:
    v = c.value
    if isinstance(v, tuple):
        v = list(v)
    return {"kind": c.kind, "value": v, "gain": round(c.gain, 3),
            "role_bearing": c.role_bearing, "issuer_claim": c.issuer_claim,
            "negative": c.negative, "text_alternative": c.text_alternative}


def describe_json(dag) -> dict:
    out = {}
    for d in describe(dag):
        out[d.said] = {"components": [component_json(c) for c in d.components],
                       "annotations": d.annotations,
                       "distinguishing": d.distinguishing,
                       "distinguishing_as_text": d.distinguishing_as_text,
                       "indistinguishable_from": d.indistinguishable_from}
    return out


def parties(host: dict, aids: set) -> dict:
    lookup = host["aliases"]
    out = {}
    for aid in sorted(aids):
        # Verbatim, as the host's interface returned it (D-DCTS).
        alias = lookup.get(aid)
        out[aid] = coia_reader.party_view(aid, alias)
        out[aid]["pill"] = coia_reader.pill_props(aid, alias)
    return out


def edges_of(s: dict) -> list:
    e = s.get("e")
    out = []
    if isinstance(e, dict):
        for label, blk in e.items():
            if label in ("d", "u") or not isinstance(blk, dict):
                continue
            out.append({"label": label, "target": blk.get("n"), "schema": blk.get("s"),
                        "operator": blk.get("o")})
    return out


def node_json(name: str, s: dict, cls: dict, extra: dict | None = None) -> dict:
    a = s.get("a") if isinstance(s.get("a"), dict) else {}
    n = {"name": name, "said": s["d"], "schema": s["s"], "issuer": s["i"],
         "issuee": a.get("i"), "attrs": a, "edges": edges_of(s),
         "classified": cls, "fixture_summary": json.loads(
             (CORPUS / f"{name}.meta.json").read_text()).get("summary")}
    n.update(extra or {})
    return n


# --------------------------------------------------------------------------------------------
# Frame 1: the accident bundle


def accident(host: dict) -> dict:
    names = ["accident_bundle", "accident_licence_a", "accident_licence_b",
             "accident_photo_a", "accident_photo_b", "accident_photo_c", "accident_photo_d",
             "accident_statement_a", "accident_statement_b"]
    sads = {n: sad(n) for n in names}
    sc = {n: s["s"] for n, s in sads.items()}
    manifest = json.loads((CORPUS / "attachments" / "MANIFEST.json").read_text())

    image_field = {"accident_photo_a": "imageDigest", "accident_photo_b": "imageDigest",
                   "accident_photo_c": "imageDigest", "accident_photo_d": "imageDigest",
                   "accident_licence_a": "portraitDigest", "accident_licence_b": "portraitDigest"}
    stem = {"accident_photo_a": "photo_a", "accident_photo_b": "photo_b",
            "accident_photo_c": "photo_c", "accident_photo_d": "photo_d",
            "accident_licence_a": "licence_a_portrait", "accident_licence_b": "licence_b_portrait"}
    resolvable, images = set(), {}
    for cred, fld in image_field.items():
        png = CORPUS / "attachments" / f"{stem[cred]}.png"
        dig = sads[cred]["a"][fld]
        if png.exists() and stem[cred] in manifest:
            resolvable.add(dig)
            images[cred] = {"state": "resolved", "src": f"attachments/{png.name}",
                            "digest": dig, "manifest": manifest[stem[cred]],
                            "media_type": sniff(png.read_bytes())}
        else:
            images[cred] = {"state": "committed-not-resolved", "digest": dig}

    type_names = {sc["accident_licence_a"]: "driving licence",
                  sc["accident_photo_a"]: "scene photograph",
                  sc["accident_statement_a"]: "witness statement",
                  sc["accident_bundle"]: "claim file"}
    dag = load_corpus_dag(
        CORPUS, names, type_names=type_names,
        subject_fields={sc["accident_photo_a"]: "depicts"},
        image_fields={sc["accident_photo_a"]: "imageDigest",
                      sc["accident_licence_a"]: "portraitDigest"},
        resolvable_digests=resolvable)
    desc = describe_json(dag)

    nodes = []
    for n in names:
        s = sads[n]
        cls = classify_node(s, type_names.get(s["s"]))
        extra = {"image": images.get(n, {"state": "none"}),
                 "type": {"name": type_names.get(s["s"]), "source": "hand-supplied",
                          "schema_state": schemas.resolve(s["s"]).state}}
        if n.startswith("accident_licence"):
            extra["glyph_override"] = {"category": "qualification",
                                       "glyph": "qualification.driving",
                                       "why": "Q-D4RX: nothing selects a subcategory yet; "
                                              "hand-assigned for this sample"}
        if n.startswith("accident_photo") and not cls["categories"]:
            extra["photo_glyph"] = {"why": "photographs land in misc and show misc.file with the "
                                           "sniffed extension (Daniel, 2026-09-24)"}
        nodes.append(node_json(n, s, cls, extra))

    aids = {x for s in sads.values() for x in (s["i"], (s.get("a") or {}).get("i")) if x}
    return {"id": "accident", "title": "Accident claim file",
            "presented": sads["accident_bundle"]["d"],
            "nodes": nodes, "descriptors": {"host-aliases": desc},
            "descriptor_variants": ["host-aliases"],
            "parties": parties(host, aids),
            "supplied_by_hand": ["type names (schemas do not resolve)",
                                 "subject field 'depicts' for the photograph schema",
                                 "which attribute holds an image digest"]}


# --------------------------------------------------------------------------------------------
# Frame 2: the vLEI chain


# The corpus chain's schemas are stand-ins generated by tools/fixtures. Each is mapped to the
# real vLEI schema it imitates so the registry's verified entailments can be borrowed. This is
# the one place the sample reaches past the corpus, and the render marks it.
VLEI_REAL = {"vlei_qvi": "EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao",
             "vlei_le": "ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY",
             "vlei_ecr_auth": "EH6ekLjSr8V32WyFbGe1zXjTzFs9PkTYmupJ9H65O14g",
             "vlei_ecr": "EEy9PkikFcANV1l7EHukCeXqrzT1hNZjGlUk7wuMO5jw"}


def vlei(host: dict) -> dict:
    names = list(VLEI_REAL)
    sads = {n: sad(n) for n in names}
    entailed, pinned, type_names, borrowed = {}, {}, {}, {}
    for n, real in VLEI_REAL.items():
        info = schemas.resolve(real)
        s = sads[n]["s"]
        entailed[s], pinned[s], type_names[s] = info.entailed, info.pinned_edges, info.title
        borrowed[n] = {"real_schema": real, "state": info.state, "title": info.title,
                       "issuer_role": info.issuer_role, "issuee_role": info.issuee_role,
                       "entailed": list(info.entailed), "pinned_edges": list(info.pinned_edges)}

    aids = {x for s in sads.values() for x in (s["i"], (s.get("a") or {}).get("i")) if x}
    known = {a for a in aids if a in host["aliases"]}
    variants = {}
    for key, aliased in (("no-aliases", set()), ("host-aliases", known)):
        dag = load_corpus_dag(CORPUS, names, type_names=type_names, entailed=entailed,
                              pinned_edges=pinned, aliased=aliased)
        variants[key] = describe_json(dag)

    known = json.loads((ROOT / "refs" / "schema-registry.json").read_text())["known_schemas"]

    def classified(n):
        # A category declared for a verified schema type outranks the field-based classifier,
        # which cannot see it (the ECR Authorization credential carries the same fields as the
        # ECR credential it authorizes).
        c = classify_node(sads[n], type_names[sads[n]["s"]])
        rec = known.get(VLEI_REAL[n]) or {}
        if rec.get("categories"):
            c["categories"] = rec["categories"]
            c["category_hits"] = {cat: [f"its schema type, {rec['title']}, declared by hand"]
                                  for cat in rec["categories"]}
        return c

    nodes = [node_json(n, sads[n], classified(n),
                       {"image": {"state": "none"},
                        "type": {"name": type_names[sads[n]["s"]],
                                 "source": "borrowed from the real vLEI schema",
                                 "schema_state": schemas.resolve(sads[n]["s"]).state},
                        "borrowed_schema": borrowed[n]})
             for n in names]
    return {"id": "vlei", "title": "vLEI chain",
            "presented": sads["vlei_ecr"]["d"],
            "nodes": nodes, "descriptors": variants,
            "descriptor_variants": ["no-aliases", "host-aliases"],
            "parties": parties(host, aids),
            "supplied_by_hand": ["schema entailments borrowed from the real vLEI schemas; the "
                                 "corpus chain uses stand-in schema SAIDs"]}


def main() -> int:
    host = json.loads((HERE / "host.json").read_text())
    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / "glyphs").mkdir(exist_ok=True)
    for svg in GLYPHS.glob("*.svg"):
        shutil.copy2(svg, PUBLIC / "glyphs" / svg.name)
    (PUBLIC / "attachments").mkdir(exist_ok=True)
    for png in (CORPUS / "attachments").glob("*.png"):
        shutil.copy2(png, PUBLIC / "attachments" / png.name)
    data = {"generated_by": "samples/accident/build_data.py",
            "category_meanings": category_meanings(),
            "host_note": host["_note"],
            "frames": [accident(host), vlei(host)]}
    (PUBLIC / "data.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {PUBLIC / 'data.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
