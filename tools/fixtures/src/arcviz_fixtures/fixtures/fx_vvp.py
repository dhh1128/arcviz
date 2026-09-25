"""A synthetic VVP dossier, shaped like the live one, plus a brand.

Built 2026-09-25 at Daniel's request: "Make it very much like the live dossier, but add an
extra credential that is of type brand." The live dossier (eu-west.provenant.net, root
EB2jhY5laLc4rcWCEWLzT69mxEIfXJZ3kNzWfKx2vHpP) is Provenant production data and is never
committed here. What is copied from it is SHAPE: which credentials, which schemas, which edges
with which operators, who issues to whom, the rules sections, and the rhythm of the dates.
Every party, LEI, phone number and brand is invented.

THE CHAIN, as in the live dossier:

    vetter V  --vetting-->  legal entity L        (org-vet, 2025-12-19)
    L         --alloc-->    allocator A           (GCD role 'TN Allocator', same day)
    carrier C --tnalloc-->  A                     (TN allocation, 2026-03-11)
    A         --delsig-->   signer S              (GCD role 'Delegated Voice Call Signer';
                                                   its `issuer` edge points at the alloc)
    A issues the dossier itself, which has no issuee, only `dt`, and four edges.

PLUS THE BRAND (not in the live dossier):

    brand vetter B --bownr--> L                   (Brand Owner; its `issuer` edge must point
                                                   at a credential proving who B is, I2I)
    V         --vetting-->  B                     (a second org-vet, so that edge resolves)

Daniel chose the second vetting over leaving the brand's `issuer` edge pointing at a credential
the presentation does not carry (Q-CH23), because arcviz has not designed how to draw a missing
referent, and simply omitting one would hide an absence.

SCHEMAS. The dossier, GCD, TN-allocation and Brand Owner schemas are Provenant's public ones
(provenant-dev/public-schema). The live vetting credential uses a Provenant-internal "Bronze"
org-identity schema that is not public; bakobo/schema's Org Vet (EJ5HgojIGN2_...) has the same
attributes (loa, lids) and is public, so it stands in (Daniel, Q-C1JG). Org Vet's `e` section
is optional, so both vettings end the chain cleanly, as the live one does.

THE LOGO is committed by digest in the Brand Owner's vCard `LOGO;HASH=...` line, as that schema
asks, and the bytes are served from corpus/attachments/brand_logo.svg (Daniel's, recoloured
blue at his request; see MANIFEST.json).
"""

import json
from pathlib import Path

from .. import determinism as det
from .. import images
from ..common import credential, make_registry, simple_edge
from ..registry import fixture

DOSSIER_SCHEMA = "EH1jN4U4LMYHmPVI4FYdZ10bIPR7YWKp8TDdZ9Y9Al-P"   # Verifiable Voice Dossier
GCD_SCHEMA = "EL7irIKYJL9Io0hhKSGWI4OznhwC7qgJG5Qf4aEs6j0o"       # Generalized Cooperative Delegation
TNALLOC_SCHEMA = "EFvnoHDY7I-kaBBeKlbDbkjG4BaI0nKLGadxBdjMGgSQ"   # TN Allocation
BRAND_SCHEMA = "EBpGNZSWwj-btOJMJSMLCVoXbtKdJTcggO-zMevr4vH_"     # Brand Owner
ORGVET_SCHEMA = "EJ5HgojIGN2_R9TzhCgnYe9NhNHxfWY0MkENZcs1CRZa"    # bakobo Org Vet
ORGVET_RULES = "EPFGDcKNXJFuW41EVIac87paJs4FwkMzIMFxHyEBmh_w"     # bakobo org-vet/rules.json

RULES = json.loads((Path(__file__).parent / "vvp_rules.json").read_text())

VETTER = det.aid("vvp:vetter")
LEGAL_ENTITY = det.aid("vvp:legal_entity")
ALLOCATOR = det.aid("vvp:allocator")
CARRIER = det.aid("vvp:carrier")
SIGNER = det.aid("vvp:signer")
BRAND_VETTER = det.aid("vvp:brand_vetter")

# The live dossier's rhythm: background vetted months earlier, the rest assembled within a
# minute of each other on the day. The brand sits between.
ISSUED = {
    "brand_vetter_vetting": "2025-11-03T10:02:11.000000+00:00",
    "vetting": "2025-12-19T15:58:42.686258+00:00",
    "alloc": "2025-12-19T15:59:46.988000+00:00",
    "brand": "2026-01-08T09:14:05.000000+00:00",
    "tnalloc": "2026-03-11T14:25:31.040498+00:00",
    "delsig": "2026-03-11T14:25:58.648000+00:00",
    "dossier": "2026-03-11T14:26:28.521000+00:00",
}
GEOS = ["US-CA", "GB-ENG", "FR"]
# Ofcom reserves 07700 900000-900999 for drama, so this number can never ring anyone.
NUMBER = "+447700900123"


def _said(corpus_dir, name):
    return json.loads((corpus_dir / f"{name}.json").read_text())["d"]


def _logo_digest(corpus_dir):
    """Digest the committed logo. Unlike the accident photographs there is no placeholder to
    fall back on: the file is a vendored asset, and a missing one is a broken checkout."""
    return images.digest((corpus_dir / "attachments" / "brand_logo.svg").read_bytes())


def _meta(title, summary):
    return {"title": title, "summary": summary, "matrix_cells": ["H1"], "rules_exercised": []}


def _org_vet(label, *, issuee, lei, issued):
    return credential(
        label, issuer=VETTER, issuee=issuee, schema_said=ORGVET_SCHEMA,
        attrs={"dt": issued, "loa": 1, "lids": [lei]},
        rule=ORGVET_RULES,   # compact, as the live vetting's rules are: committed, not shown
        registry=make_registry(label, VETTER).said)


@fixture("vvp_vetting")
def build_vvp_vetting(corpus_dir):
    return {"serder": _org_vet("vvp_vetting", issuee=LEGAL_ENTITY,
                               lei="984500ARCV1Z0000FIX10", issued=ISSUED["vetting"]),
            "meta": _meta("VVP dossier: org vetting of the legal entity",
                          "The accountable party's identity, vetted at loa 1 with an LEI as its linked "
                          "identifier. Stands in for the live dossier's Provenant-internal 'Bronze' "
                          "vetting with bakobo's public Org Vet. Its rules section is compact, so the "
                          "rules are committed and not disclosed.")}


@fixture("vvp_brand_vetter_vetting")
def build_vvp_brand_vetter_vetting(corpus_dir):
    return {"serder": _org_vet("vvp_brand_vetter_vetting", issuee=BRAND_VETTER,
                               lei="984500ARCV1Z0000FIX11", issued=ISSUED["brand_vetter_vetting"]),
            "meta": _meta("VVP dossier: org vetting of the brand vetter",
                          "Proves who issued the brand credential, because the Brand Owner schema "
                          "requires an issuer edge (I2I) to such a proof. Shares schema and issuer "
                          "with vvp_vetting and differs in issuee.")}


def _gcd(label, *, issuer, issuee, role, goal, proto, issued, edge=None):
    attrs = {"dt": issued, "role": role, "c_goal": [goal], "c_pgeo": GEOS, "c_rgeo": GEOS,
             "c_proto": [proto], "c_human": "",
             "c_after": "2025-12-17T10:39:29.769000+00:00",
             "c_before": "2026-12-17T10:39:29.769000+00:00"}
    return credential(label, issuer=issuer, issuee=issuee, schema_said=GCD_SCHEMA, attrs=attrs,
                      edge=edge, rule=dict(RULES["gcd"]),
                      registry=make_registry(label, issuer).said)


@fixture("vvp_alloc")
def build_vvp_alloc(corpus_dir):
    return {"serder": _gcd("vvp_alloc", issuer=LEGAL_ENTITY, issuee=ALLOCATOR, role="TN Allocator",
                           goal="ops.it.telco.tnalloc", proto="ipex:issuer,issuee",
                           issued=ISSUED["alloc"]),
            "meta": _meta("VVP dossier: TN Allocator role",
                          "The legal entity delegates number allocation to a committee (a GCD role). "
                          "Shares its schema with vvp_delsig, and the two are separated only by the "
                          "issuer-supplied role string.")}


@fixture("vvp_tnalloc")
def build_vvp_tnalloc(corpus_dir):
    serder = credential(
        "vvp_tnalloc", issuer=CARRIER, issuee=ALLOCATOR, schema_said=TNALLOC_SCHEMA,
        attrs={"dt": ISSUED["tnalloc"],
               "numbers": {"rangeStart": NUMBER, "rangeEnd": NUMBER},
               "channel": "voice", "doNotOriginate": False,
               "startDate": "2026-03-01T00:00:00+00:00", "endDate": "2027-03-01T00:00:00+00:00"},
        rule=dict(RULES["tnalloc"]),
        registry=make_registry("vvp_tnalloc", CARRIER).said)
    return {"serder": serder,
            "meta": _meta("VVP dossier: TN allocation",
                          "A carrier allocates one number (a range whose start and end are equal) to "
                          "the allocator. The number is in Ofcom's drama range.")}


@fixture("vvp_delsig", depends_on=["vvp_alloc"])
def build_vvp_delsig(corpus_dir):
    edge = {"d": "", "issuer": simple_edge("vvp_delsig:issuer", n=_said(corpus_dir, "vvp_alloc"),
                                           s=GCD_SCHEMA, o="I2I")}
    return {"serder": _gcd("vvp_delsig", issuer=ALLOCATOR, issuee=SIGNER,
                           role="Delegated Voice Call Signer", goal="ops.it.telco.send.sign",
                           proto="vvp:op", issued=ISSUED["delsig"], edge=edge),
            "meta": _meta("VVP dossier: Delegated Voice Call Signer role",
                          "The allocator delegates call signing. Its issuer edge points at the alloc "
                          "role, which is how the allocator proves it may delegate.")}


@fixture("vvp_brand", depends_on=["vvp_brand_vetter_vetting"])
def build_vvp_brand(corpus_dir):
    logo = _logo_digest(corpus_dir)
    vcard = ["ORG:Fixture Freight Ltd",
             f"LOGO;HASH={logo};VALUE=URI:https://example.com/brand/logo.svg",
             "URL:https://example.com",
             f"TEL;TYPE=support:{NUMBER}"]
    edge = {"d": "", "issuer": simple_edge("vvp_brand:issuer",
                                           n=_said(corpus_dir, "vvp_brand_vetter_vetting"),
                                           s=ORGVET_SCHEMA, o="I2I")}
    serder = credential(
        "vvp_brand", issuer=BRAND_VETTER, issuee=LEGAL_ENTITY, schema_said=BRAND_SCHEMA,
        attrs={"dt": ISSUED["brand"], "vcard": vcard, "goals": ["ops.it.telco.send"]},
        edge=edge, rule=dict(RULES["brand"]),
        registry=make_registry("vvp_brand", BRAND_VETTER).said)
    return {"serder": serder,
            "meta": _meta("VVP dossier: brand owner",
                          "The legal entity's right to present a brand, with its logo committed by "
                          "digest in a vCard LOGO line. The URI is example.com and serves nothing; "
                          "the bytes are in corpus/attachments/brand_logo.svg.")}


@fixture("vvp_dossier", depends_on=["vvp_vetting", "vvp_alloc", "vvp_tnalloc", "vvp_delsig",
                                    "vvp_brand"])
def build_vvp_dossier(corpus_dir):
    s = lambda n: _said(corpus_dir, n)   # noqa: E731
    edge = {
        "d": "",
        "vetting": simple_edge("vvp_dossier:vetting", n=s("vvp_vetting"), s=ORGVET_SCHEMA, o="NI2I"),
        "alloc": simple_edge("vvp_dossier:alloc", n=s("vvp_alloc"), s=GCD_SCHEMA, o="I2I"),
        "tnalloc": simple_edge("vvp_dossier:tnalloc", n=s("vvp_tnalloc"), s=TNALLOC_SCHEMA, o="I2I"),
        "delsig": simple_edge("vvp_dossier:delsig", n=s("vvp_delsig"), s=GCD_SCHEMA, o="NI2I"),
        "bownr": simple_edge("vvp_dossier:bownr", n=s("vvp_brand"), s=BRAND_SCHEMA, o="NI2I"),
    }
    serder = credential("vvp_dossier", issuer=ALLOCATOR, schema_said=DOSSIER_SCHEMA,
                        attrs={"dt": ISSUED["dossier"]}, edge=edge,
                        registry=make_registry("vvp_dossier", ALLOCATOR).said)
    return {"serder": serder,
            "meta": _meta("VVP dossier (synthetic, shaped like the live one, plus a brand)",
                          "Seven credentials. The root is untargeted, carries only dt, and is made of "
                          "its edges: vetting, alloc, tnalloc, delsig as in the live dossier, plus "
                          "bownr to a Brand Owner credential.")}
