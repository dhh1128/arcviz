"""Fixtures for H5 (aggregate fully compact / bare AGID) and H6 (Metadata ACDC).

Both are on disclosure-matrix.md (e)'s "spec-only, no observed artifact
anywhere in the corpus" list.
"""

from keri.core import Aggor
from keri.core.coring import Kinds

from .. import determinism as det
from .. import schemas
from ..common import agg_credential, credential, simple_edge, simple_rule
from ..registry import fixture


@fixture("bare_agid")
def build_bare_agid(corpus_dir):
    """H5: the `A` field compacted to its AGID alone, nothing else recoverable.

    Exercises disclosure-matrix.md RULE 7 ("an AGID is never rendered as a
    SAID") and H5's naive-lie ("rendering the AGID as a SAID pill").
    """
    issuer = det.aid("bare_agid:issuer")
    issuee = det.aid("bare_agid:issuee")

    said, schema_mad = schemas.agg_schema(
        title="Bare-AGID Demo Schema",
        credential_type="ArcvizFixture_BareAGID",
        element_props={}, element_required=[],
    )

    # Aggregate element list: element 0 is the AGID placeholder, filled in by
    # Aggor; elements 1..3 are independently blindable attribute blocks, the
    # same shape as keripy's own aggregate selective-disclosure worked
    # example (tests/acdc/test_examples.py::test_selective_disclosure_aggregate_JSON).
    ael = [
        "",
        dict(d='', u=det.nonce("bare_agid:el1"), i=issuee),
        dict(d='', u=det.nonce("bare_agid:el2"), overAge=True),
        dict(d='', u=det.nonce("bare_agid:el3"), tier="gold"),
    ]
    aggor = Aggor(ael=ael, makify=True, kind=Kinds.json)
    agid = aggor.agid

    serder = agg_credential(
        "bare_agid", issuer=issuer, schema_said=said, aggregate=agid,
        top_uuid=det.nonce("bare_agid:u"),
    )

    return {
        "serder": serder,
        "expanded": {"aggregate_elements": aggor.ael, "agid": agid},
        "meta": {
            "title": "Bare AGID (Aggregate fully compact)",
            "summary": (
                "An 'A' (Attribute Aggregate) section reduced to only its "
                "AGID -- no element count, no labels, no values recoverable. "
                "corpus/bare_agid.expanded.json shows the 3-element aggregate "
                "that hashes to this AGID; a real disclosure of this fixture "
                "would never include that file. `rd` (Registry Digest) is "
                "OMITTED, not present-and-empty: this fixture is not "
                "registry-bound, and an empty-string `rd` would assert a "
                "distinct, real state (H2/H3-shaped: a registry commitment "
                "exists but is unguessable/blinded) that doesn't apply here. "
                "Omitting rather than emptying keeps it consistent with "
                "every other standalone (non-registry) fixture in this "
                "corpus; only the vLEI-chain fixtures, which narratively "
                "need a registry, carry a real `rd`."
            ),
            "matrix_cells": ["H5"],
            "rules_exercised": ["RULE 7"],
            "spec_refs": [
                "spec-body.md:661 (AGID is not a SAID)",
                "spec-body.md:712-720 (AGID computation)",
            ],
            "notes": (
                "AGID composition into the enclosing top-level SAID is an "
                "open spec question (acdc-inventory.md OQ5); this fixture "
                "uses keripy's Aggor + acdcmap (the flexible 'acm' map form, "
                "which omits an absent field rather than acdcagg's "
                "fixed-field empty-string sentinels) as the reference "
                "behavior."
            ),
        },
    }


@fixture("metadata_acdc")
def build_metadata_acdc(corpus_dir):
    """H6: top-level `u` present but EMPTY -- a Discloser's decoy commitment.

    Issuer, schema, edge, and rule are all disclosed; the attribute content
    is minimal/empty, and (the sharp part, per spec-body.md:172) the ISSUER
    has committed to none of it as presented -- only the Discloser has.
    """
    issuer = det.aid("metadata_acdc:issuer")
    far_placeholder = det.aid("metadata_acdc:would-be-far-node")
    far_schema_placeholder = det.aid("metadata_acdc:would-be-far-schema")

    said, schema_mad = schemas.attr_schema(
        title="Metadata ACDC Demo Schema",
        credential_type="ArcvizFixture_Metadata",
        attr_props={}, attr_required=[], require_issuee=False,
        edge_required=False, rule_required=False,
    )

    edge = {'d': '', 'evidence': simple_edge(
        "metadata_acdc", n=far_placeholder, s=far_schema_placeholder)}
    rule = {'d': '', 'terms': simple_rule(
        "This metadata commitment does not itself constitute an issued "
        "credential; the Issuer has made no commitment to the attribute "
        "content of the private ACDC this metadata describes.")}

    serder = credential(
        "metadata_acdc", issuer=issuer, schema_said=said,
        attrs={},  # present but empty: "MAY be empty ... not correlatable"
        edge=edge, rule=rule,
        top_uuid="",  # THE point of this fixture: present but empty
    )

    return {
        "serder": serder,
        "meta": {
            "title": "Metadata ACDC (top-level u present but empty)",
            "summary": (
                "A Discloser's pre-contractual commitment to the metadata "
                "(issuer, schema, edges, rules) of a not-yet-disclosed private "
                "ACDC. The attribute section is present but empty. The "
                "edge's far node (evidence) is a placeholder digest, not a "
                "resolvable fixture -- by design, nothing about the real "
                "ACDC's identity is discoverable from this artifact."
            ),
            "matrix_cells": ["H6"],
            "rules_exercised": ["RULE 12"],
            "spec_refs": [
                "spec-body.md:166-172 (Metadata Disclosure)",
                "spec-body.md:1763 (Metadata Disclosure, Graduated Disclosure enumeration)",
            ],
            "notes": (
                "The real ACDC this would be a decoy for does not exist in "
                "this corpus -- by construction, a Metadata ACDC's whole "
                "point is that its d cannot be correlated to any other ACDC's d."
            ),
        },
    }
