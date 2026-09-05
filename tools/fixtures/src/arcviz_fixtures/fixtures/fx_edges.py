"""Fixtures for edge/rule blinding, the DI2I/NOT operators, edge weights and
edge-group operators (AND/OR/AVG/WAVG), and a working (non-defect) edge-group
scenario. All targets named in disclosure-matrix.md (e) and
corpus-keripy-examples.md "Shapes still missing".
"""

from keri.core.coring import Kinds
from keri.core.mapping import Compactor

from .. import determinism as det
from .. import schemas
from ..common import credential, simple_edge, simple_rule
from ..registry import fixture


def _tiny_attr_schema(title, ctype):
    return schemas.attr_schema(
        title=title, credential_type=ctype,
        attr_props={"label": {"type": "string"}},
        attr_required=["label"],
    )


@fixture("compact_private_edge")
def build_compact_private_edge(corpus_dir):
    """H8: a single Edge collapsed to its SAID, with `u` inside -- the far
    node's identity is withheld, not merely its content.
    """
    far_issuer = det.aid("compact_private_edge:far_issuer")
    far_issuee = det.aid("compact_private_edge:far_issuee")
    far_said_schema, _ = _tiny_attr_schema(
        "Compact Private Edge -- Far Node Schema", "ArcvizFixture_CPE_Far")
    far = credential(
        "compact_private_edge_far", issuer=far_issuer, issuee=far_issuee,
        schema_said=far_said_schema, attrs={"label": "the withheld far node"},
    )

    near_issuer = det.aid("compact_private_edge:near_issuer")
    near_schema, _ = _tiny_attr_schema(
        "Compact Private Edge -- Near Node Schema", "ArcvizFixture_CPE_Near")

    # The edge itself carries u -> its SAID is a genuine blind, not merely a
    # compaction. A separate Compactor pass over just this group collapses
    # the "source" member down to that bare SAID (compactify=True, applied
    # HERE, only to this sub-tree -- see common.py's note on why the outer
    # credential() call below must NOT also set compactify=True). The group
    # itself keeps its own d/u visible: a renderer can see *that* a "source"
    # edge exists, but nothing about where it points.
    raw_edge_group = {
        'd': '',
        'source': simple_edge(
            "compact_private_edge", n=far.said, s=far_said_schema,
            u=det.nonce("compact_private_edge:edge_u")),
    }
    edge_compactor = Compactor(mad=raw_edge_group, makify=True,
                                compactify=True, kind=Kinds.json)
    edge_group = edge_compactor.mad  # {'d': <group_said>, 'source': <bare edge SAID>}

    near = credential(
        "compact_private_edge_near", issuer=near_issuer,
        schema_said=near_schema, attrs={"label": "the presenting node"},
        edge=edge_group,
    )

    return {
        "serder": near,
        "expanded": {
            "far_node": far.sad,
            "note": ("far_node is included for test verification only -- a "
                      "real presenter using this mechanism never discloses it."),
        },
        "meta": {
            "title": "Compact Private Edge",
            "summary": (
                "The near node's 'source' edge is a bare SAID computed over "
                "an edge block that itself carries a `u`. Unlike a plain "
                "compact edge (H2-shaped, guessable if the far-node universe "
                "is small), this SAID is a genuine blind: the far node's own "
                "SAID never appears."
            ),
            "matrix_cells": ["H8"],
            "rules_exercised": ["RULE 1"],
            "spec_refs": ["spec-body.md:1165", "spec-body.md:1164"],
        },
    }


@fixture("blinded_edge_group")
def build_blinded_edge_group(corpus_dir):
    """A blinded Edge-GROUP: the group itself (not one member) carries `u`
    and is collapsed to its bare SAID. No `u` at edge/edge-group level
    appears anywhere in the real vLEI chain or the keripy corpus
    (corpus-vlei-chain.md sec.2; disclosure-matrix.md (e)).
    """
    issuer = det.aid("blinded_edge_group:issuer")
    schema_said, _ = _tiny_attr_schema(
        "Blinded Edge-Group Demo Schema", "ArcvizFixture_BlindedEdgeGroup")

    peer_a = det.aid("blinded_edge_group:peer_a")
    peer_b = det.aid("blinded_edge_group:peer_b")
    peer_a_schema, _ = _tiny_attr_schema("Peer A Schema", "ArcvizFixture_PeerA")
    peer_b_schema, _ = _tiny_attr_schema("Peer B Schema", "ArcvizFixture_PeerB")

    # This whole group -- both slots plus their shared 'o' -- is blinded
    # behind one SAID. Passing it as the ACDC's edge= value directly (a bare
    # string) means the top-level 'e' field in the disclosed sad is that
    # single SAID, full stop.
    inner_group = {
        'd': '',
        'u': det.nonce("blinded_edge_group:group_u"),
        'o': 'OR',
        'first': simple_edge("blinded_edge_group:first", n=peer_a, s=peer_a_schema),
        'second': simple_edge("blinded_edge_group:second", n=peer_b, s=peer_b_schema),
    }
    from keri.core.mapping import Compactor
    from keri.core.coring import Kinds
    compactor = Compactor(mad=inner_group, makify=True, compactify=True, kind=Kinds.json)
    group_said = compactor.said

    serder = credential(
        "blinded_edge_group", issuer=issuer, schema_said=schema_said,
        attrs={"label": "presenting node with a wholly hidden edge-group"},
        edge=group_said,
    )

    return {
        "serder": serder,
        "expanded": {"edge_group": compactor.mad},
        "meta": {
            "title": "Blinded Edge-Group",
            "summary": (
                "The presenting node's entire 'e' section is one bare SAID, "
                "computed over an edge-group carrying its own `u`. A viewer "
                "cannot tell there are two edges, an OR operator, or "
                "anything else -- only that *some* edge-group is committed to."
            ),
            "matrix_cells": ["H8"],
            "rules_exercised": ["RULE 1"],
            "notes": "Blinding at the edge-GROUP level, distinct from compact_private_edge (a single Edge).",
        },
    }


@fixture("blinded_rule_group")
def build_blinded_rule_group(corpus_dir):
    """A blinded Rule (leaf) nested inside a blinded Rule-group, both
    carrying `u`. No `u` at rule level appears anywhere in the corpus
    (corpus-vlei-chain.md sec.4: "r.u never appears").
    """
    issuer = det.aid("blinded_rule_group:issuer")
    schema_said, _ = _tiny_attr_schema(
        "Blinded Rule-Group Demo Schema", "ArcvizFixture_BlindedRuleGroup")

    from keri.core.mapping import Compactor
    from keri.core.coring import Kinds

    confidential_rule = simple_rule(
        "This clause's legal language is confidential and disclosed only to "
        "a Disclosee who has separately agreed to its terms.",
        u=det.nonce("blinded_rule_group:leaf_u"))

    rule_group = {
        'd': '',
        'u': det.nonce("blinded_rule_group:group_u"),
        'confidentialTerm': confidential_rule,
    }
    compactor = Compactor(mad=rule_group, makify=True, compactify=True, kind=Kinds.json)

    serder = credential(
        "blinded_rule_group", issuer=issuer, schema_said=schema_said,
        attrs={"label": "presenting node with wholly hidden rules"},
        rule=compactor.said,
    )

    return {
        "serder": serder,
        "expanded": {"rule_group": compactor.mad},
        "meta": {
            "title": "Blinded Rule-Group (and nested blinded Rule)",
            "summary": (
                "The 'r' section is one bare SAID over a Rule-group that "
                "itself carries `u`, whose one member ('confidentialTerm') "
                "is a leaf Rule that ALSO carries its own `u`. Two blinding "
                "levels in one fixture."
            ),
            "matrix_cells": ["H3", "H8"],
            "rules_exercised": ["RULE 1"],
            "notes": "Rule-group and Rule blinding use the same u-in-a-SAIDed-map mechanism as Edge blinding (spec-body.md:1313).",
        },
    }


@fixture("di2i_operator")
def build_di2i_operator(corpus_dir):
    """DI2I: near issuer must be the far issuee OR a delegate of it.

    Not exercised anywhere in the keripy or vLEI corpus
    (corpus-keripy-examples.md "Shapes still missing").
    """
    far_issuer = det.aid("di2i:far_issuer")
    far_issuee = det.aid("di2i:far_issuee")
    far_schema, _ = _tiny_attr_schema("DI2I Far Node Schema", "ArcvizFixture_DI2I_Far")
    far = credential("di2i_far", issuer=far_issuer, issuee=far_issuee,
                      schema_said=far_schema, attrs={"label": "the delegator's credential"})

    # near.i is a placeholder "delegated AID of far_issuee" -- there is no
    # real KEL/dip event behind this claim; see determinism.py docstring.
    near_issuer = det.aid("di2i:near_issuer_delegate_of_far_issuee")
    near_schema, _ = _tiny_attr_schema("DI2I Near Node Schema", "ArcvizFixture_DI2I_Near")
    edge = {'d': '', 'delegatedAuthority': simple_edge(
        "di2i", n=far.said, s=far_schema, o="DI2I")}
    near = credential("di2i_near", issuer=near_issuer, schema_said=near_schema,
                       attrs={"label": "the delegate's credential"}, edge=edge)

    return {
        "serder": near,
        "expanded": {"far_node": far.sad},
        "meta": {
            "title": "DI2I edge operator",
            "summary": (
                "Near issuer claims to be a delegate of the far node's "
                "issuee. No KEL is modeled -- this fixture exercises the "
                "field-level shape of the claim, not delegation proof."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "spec_refs": ["spec-body.md:1190-1195 (unary operators)"],
        },
    }


@fixture("not_operator")
def build_not_operator(corpus_dir):
    """NOT: validity of the pointed-to node is logically inverted."""
    far_issuer = det.aid("not_op:far_issuer")
    far_issuee = det.aid("not_op:far_issuee")
    far_schema, _ = _tiny_attr_schema("NOT Far Node Schema", "ArcvizFixture_NOT_Far")
    far = credential("not_operator_far", issuer=far_issuer, issuee=far_issuee,
                      schema_said=far_schema,
                      attrs={"label": "a disqualifying-condition credential"})

    near_issuer = det.aid("not_op:near_issuer")
    near_schema, _ = _tiny_attr_schema("NOT Near Node Schema", "ArcvizFixture_NOT_Near")
    edge = {'d': '', 'exclusion': simple_edge("not_op", n=far.said, s=far_schema, o="NOT")}
    near = credential("not_operator_near", issuer=near_issuer, schema_said=near_schema,
                       attrs={"label": "valid unless the exclusion node is valid"},
                       edge=edge)

    return {
        "serder": near,
        "expanded": {"far_node": far.sad},
        "meta": {
            "title": "NOT edge operator",
            "summary": "The near node is valid iff the far ('exclusion') node is NOT valid.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "spec_refs": ["spec-body.md:1190-1195 (unary operators)"],
        },
    }


@fixture("edge_group_operators")
def build_edge_group_operators(corpus_dir):
    """One ACDC, four sibling edge-groups: AND (explicit), OR, AVG, WAVG.

    AVG/WAVG/explicit-AND/weighted edges are on disclosure-matrix.md (e)'s
    spec-only list. Far nodes here are placeholder AIDs, not resolvable
    fixtures -- the point of this fixture is operator/weight syntax, not a
    real multi-party scenario (see the "working_edge_group" fixture for that).
    """
    issuer = det.aid("edge_group_operators:issuer")
    schema_said, _ = _tiny_attr_schema(
        "Edge-Group Operators Demo Schema", "ArcvizFixture_EdgeGroupOperators")

    def far(label):
        return det.aid(f"edge_group_operators:{label}"), det.aid(f"edge_group_operators:{label}:schema")

    a_n, a_s = far("and.peerA")
    b_n, b_s = far("and.peerB")
    o1_n, o1_s = far("or.peerA")
    o2_n, o2_s = far("or.peerB")
    v1_n, v1_s = far("avg.sensor1")
    v2_n, v2_s = far("avg.sensor2")
    w1_n, w1_s = far("wavg.primary")
    w2_n, w2_s = far("wavg.secondary")

    edge = {
        'd': '',
        'unanimous': {
            'd': '', 'o': 'AND',  # explicit; default with no 'o' would mean the same thing
            'peerA': simple_edge("egop:and:a", n=a_n, s=a_s),
            'peerB': simple_edge("egop:and:b", n=b_n, s=b_s),
        },
        'anyOne': {
            'd': '', 'o': 'OR',
            'peerA': simple_edge("egop:or:a", n=o1_n, s=o1_s),
            'peerB': simple_edge("egop:or:b", n=o2_n, s=o2_s),
        },
        'average': {
            'd': '', 'o': 'AVG',
            'sensor1': simple_edge("egop:avg:1", n=v1_n, s=v1_s),
            'sensor2': simple_edge("egop:avg:2", n=v2_n, s=v2_s),
        },
        'weightedAverage': {
            'd': '', 'o': 'WAVG',
            'primary': simple_edge("egop:wavg:1", n=w1_n, s=w1_s, w=0.7),
            'secondary': simple_edge("egop:wavg:2", n=w2_n, s=w2_s, w=0.3),
        },
    }

    serder = credential(
        "edge_group_operators", issuer=issuer, schema_said=schema_said,
        attrs={"label": "one node, four differently-gated edge-groups"},
        edge=edge,  # credential() fully-expands this: real digests at every level, nothing collapsed
    )

    return {
        "serder": serder,
        "meta": {
            "title": "Edge-group operators: AND / OR / AVG / WAVG, plus edge weights",
            "summary": (
                "Four sibling edge-groups on one ACDC, one per m-ary "
                "operator. The WAVG group's two edges carry `w` (0.7/0.3). "
                "Far nodes are placeholder AIDs (no resolvable fixture "
                "behind them) -- see 'working_edge_group' for a scenario "
                "with real, resolvable co-endorser credentials."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "spec_refs": ["spec-body.md:1101-1108 (m-ary operators)",
                          "spec-body.md:1215-1217 (edge weight)"],
        },
    }


@fixture("working_edge_group_endorser_a")
def build_endorser_a(corpus_dir):
    issuer = det.aid("working_edge_group:endorser_a:issuer")
    issuee = det.aid("working_edge_group:facility")
    schema_said, _ = schemas.attr_schema(
        title="Inspector Endorsement Schema", credential_type="ArcvizFixture_InspectorEndorsement",
        attr_props={"inspector": {"type": "string"}, "findingsClean": {"type": "boolean"}},
        attr_required=["inspector", "findingsClean"])
    serder = credential(
        "working_edge_group_endorser_a", issuer=issuer, issuee=issuee,
        schema_said=schema_said,
        attrs={"inspector": "Northgate Safety Consultants", "findingsClean": True})
    return {
        "serder": serder,
        "meta": {
            "title": "Working edge-group: endorser A's independent inspection credential",
            "summary": "One of two real, independently-issued inspection credentials endorsing the same facility, referenced by 'working_edge_group'.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("working_edge_group_endorser_b")
def build_endorser_b(corpus_dir):
    issuer = det.aid("working_edge_group:endorser_b:issuer")
    issuee = det.aid("working_edge_group:facility")
    schema_said, _ = schemas.attr_schema(
        title="Inspector Endorsement Schema", credential_type="ArcvizFixture_InspectorEndorsement",
        attr_props={"inspector": {"type": "string"}, "findingsClean": {"type": "boolean"}},
        attr_required=["inspector", "findingsClean"])
    serder = credential(
        "working_edge_group_endorser_b", issuer=issuer, issuee=issuee,
        schema_said=schema_said,
        attrs={"inspector": "Meridian Compliance Group", "findingsClean": True})
    return {
        "serder": serder,
        "meta": {
            "title": "Working edge-group: endorser B's independent inspection credential",
            "summary": "The other of two real, independently-issued inspection credentials endorsing the same facility, referenced by 'working_edge_group'.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("working_edge_group",
         depends_on=["working_edge_group_endorser_a", "working_edge_group_endorser_b"])
def build_working_edge_group(corpus_dir):
    """A genuine multi-endorser scenario: a Joint Facility Certification is
    valid only if BOTH independent inspectors' credentials are present
    (edge-group `o: AND`), each pointing at a real, separately-issued,
    schema-real credential -- unlike test_edge_groups_standalone.py and
    test_forked_dag_v2_edge_groups.py, whose edges point at synthetic
    literal SAID strings with nothing real behind them.

    Note on scope: this fixture is generated directly via
    keri.acdc.messaging.acdcmap + Compactor, the same low-level machinery
    every other fixture here uses -- it does NOT go through keripy's
    Reger.sources / Verifier.processCredential, which is the code path
    documented (corpus-keripy-examples.md sec.(b)5) as unable to traverse
    edge-groups (KeyError: 'n'). So this fixture is "working" in the sense
    that it is a real, resolvable, self-consistent multi-credential DAG with
    correct SAIDs -- not in the sense of having been round-tripped through
    keripy's own verifier, which is a documented gap upstream, not something
    this generator works around.
    """
    import json
    endorser_a_json = (corpus_dir / "working_edge_group_endorser_a.json")
    endorser_b_json = (corpus_dir / "working_edge_group_endorser_b.json")
    a_sad = json.loads(endorser_a_json.read_text())
    b_sad = json.loads(endorser_b_json.read_text())

    a_schema, _ = schemas.attr_schema(
        title="Inspector Endorsement Schema", credential_type="ArcvizFixture_InspectorEndorsement",
        attr_props={"inspector": {"type": "string"}, "findingsClean": {"type": "boolean"}},
        attr_required=["inspector", "findingsClean"])

    issuer = det.aid("working_edge_group:certifier")
    issuee = det.aid("working_edge_group:facility")
    schema_said, _ = schemas.attr_schema(
        title="Joint Facility Certification Schema",
        credential_type="ArcvizFixture_JointCertification",
        attr_props={"facilityName": {"type": "string"}},
        attr_required=["facilityName"])

    edge = {
        'd': '', 'o': 'AND',
        'inspectorA': simple_edge("working_edge_group:a", n=a_sad['d'], s=a_schema),
        'inspectorB': simple_edge("working_edge_group:b", n=b_sad['d'], s=a_schema),
    }

    serder = credential(
        "working_edge_group", issuer=issuer, issuee=issuee, schema_said=schema_said,
        attrs={"facilityName": "Rangeview Cold Storage Facility 3"}, edge=edge,
    )

    return {
        "serder": serder,
        "meta": {
            "title": "Working edge-group (AND, two real co-endorsers)",
            "summary": (
                "A joint certification valid only when both inspectorA and "
                "inspectorB's edges resolve -- both are real, separately "
                "issued, resolvable ACDCs in this corpus (see depends_on), "
                "not synthetic literal SAID strings."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "depends_on": ["working_edge_group_endorser_a", "working_edge_group_endorser_b"],
            "notes": (
                "Generated via keri.acdc.messaging.acdcmap + Compactor "
                "directly; not round-tripped through keripy's "
                "Reger.sources/Verifier.processCredential, which cannot "
                "traverse edge-groups (documented keripy gap, see summary docstring)."
            ),
        },
    }
