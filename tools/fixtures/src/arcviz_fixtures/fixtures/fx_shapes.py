"""DAG shapes named as missing from the corpus in corpus-keripy-examples.md
"Shapes still missing": same-schema-twice DAG, an optional/absent edge
leaving a visible gap, and a diamond that also has depth. (The
depth-3-or-more chain from the same list is satisfied by the vLEI-equivalent
fixture in fx_vlei.py -- 4 nodes, depth 4 -- rather than duplicated here; see
corpus/README.md.)
"""

from .. import determinism as det
from .. import schemas
from ..common import credential, simple_edge
from ..registry import fixture

_PERSON_PROPS = {"name": {"type": "string"}, "birthYear": {"type": "integer"}}
_PERSON_REQUIRED = ["name", "birthYear"]


def _person_schema():
    return schemas.attr_schema(
        title="Person Identity Schema", credential_type="ArcvizFixture_PersonIdentity",
        attr_props=_PERSON_PROPS, attr_required=_PERSON_REQUIRED)


@fixture("same_schema_alice")
def build_same_schema_alice(corpus_dir):
    schema_said, _ = _person_schema()
    issuer = det.aid("same_schema:registrar")
    issuee = det.aid("same_schema:alice")
    serder = credential("same_schema_alice", issuer=issuer, issuee=issuee,
                         schema_said=schema_said,
                         attrs={"name": "Alice Householder", "birthYear": 1988})
    return {
        "serder": serder,
        "meta": {
            "title": "Same-schema-twice DAG: Alice's identity credential",
            "summary": "Instantiates the shared Person Identity schema; referenced by 'same_schema_household'.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("same_schema_bob")
def build_same_schema_bob(corpus_dir):
    schema_said, _ = _person_schema()
    issuer = det.aid("same_schema:registrar")
    issuee = det.aid("same_schema:bob")
    serder = credential("same_schema_bob", issuer=issuer, issuee=issuee,
                         schema_said=schema_said,
                         attrs={"name": "Bob Householder", "birthYear": 1990})
    return {
        "serder": serder,
        "meta": {
            "title": "Same-schema-twice DAG: Bob's identity credential",
            "summary": "Instantiates the SAME schema SAID as 'same_schema_alice', different content and SAID; referenced by 'same_schema_household'.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("same_schema_household", depends_on=["same_schema_alice", "same_schema_bob"])
def build_same_schema_household(corpus_dir):
    """The DAG cp_disclosure's docstring names but never builds (corpus-keripy-examples.md
    sec.(b)3): one presentation edging to two nodes that instantiate the same
    schema. A renderer must not conflate the two same-shaped nodes as the same
    node.
    """
    import json
    alice = json.loads((corpus_dir / "same_schema_alice.json").read_text())
    bob = json.loads((corpus_dir / "same_schema_bob.json").read_text())
    schema_said, _ = _person_schema()

    issuer = det.aid("same_schema:household_presenter")
    household_schema, _ = schemas.attr_schema(
        title="Household Presentation Schema", credential_type="ArcvizFixture_HouseholdPresentation",
        attr_props={"householdId": {"type": "string"}}, attr_required=["householdId"])

    edge = {
        'd': '',
        'memberA': simple_edge("same_schema:a", n=alice['d'], s=schema_said, o="NI2I"),
        'memberB': simple_edge("same_schema:b", n=bob['d'], s=schema_said, o="NI2I"),
    }
    serder = credential("same_schema_household", issuer=issuer, schema_said=household_schema,
                         attrs={"householdId": "HH-0042"}, edge=edge)

    return {
        "serder": serder,
        "meta": {
            "title": "Same-schema-twice DAG (household presentation)",
            "summary": (
                "One presentation with two edges, both pointing at ACDCs "
                "that instantiate the identical Person Identity schema SAID "
                "-- 'same_schema_alice' and 'same_schema_bob' -- with "
                "different content, issuees, and SAIDs. Corpus gap named but "
                "never built in test_cp_disclosure.py's docstring."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "depends_on": ["same_schema_alice", "same_schema_bob"],
        },
    }


@fixture("optional_edge_present")
def build_optional_edge_present(corpus_dir):
    far_schema, _ = schemas.attr_schema(
        title="Endorsement Reference Schema", credential_type="ArcvizFixture_EndorsementRef",
        attr_props={"note": {"type": "string"}}, attr_required=["note"])
    far_issuer = det.aid("optional_edge:far_issuer")
    far = credential("optional_edge_far", issuer=far_issuer, schema_said=far_schema,
                      attrs={"note": "an endorsement the issuer chose to attach"})

    schema_said, _ = schemas.attr_schema(
        title="Optional-Edge Demo Schema", credential_type="ArcvizFixture_OptionalEdge",
        attr_props={"claim": {"type": "string"}}, attr_required=["claim"],
        has_edge=True, edge_required=False)
    issuer = det.aid("optional_edge:issuer")
    edge = {'d': '', 'endorsement': simple_edge("optional_edge", n=far.said, s=far_schema)}
    serder = credential("optional_edge_present", issuer=issuer, schema_said=schema_said,
                         attrs={"claim": "a claim with an attached endorsement"}, edge=edge)
    return {
        "serder": serder,
        "expanded": {"far_node": far.sad},
        "meta": {
            "title": "Optional edge section, present",
            "summary": (
                "Instantiates a schema whose 'e' field is optional "
                "(edge_required=false), WITH an edge populated. Pair with "
                "'optional_edge_absent', which shares the identical schema "
                "SAID but omits 'e' entirely."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("optional_edge_absent")
def build_optional_edge_absent(corpus_dir):
    schema_said, _ = schemas.attr_schema(
        title="Optional-Edge Demo Schema", credential_type="ArcvizFixture_OptionalEdge",
        attr_props={"claim": {"type": "string"}}, attr_required=["claim"],
        has_edge=True, edge_required=False)
    issuer = det.aid("optional_edge:issuer_unendorsed")
    serder = credential("optional_edge_absent", issuer=issuer, schema_said=schema_said,
                         attrs={"claim": "a claim issued with no endorsement attached"})
    return {
        "serder": serder,
        "meta": {
            "title": "Optional edge section, absent (the visible gap)",
            "summary": (
                "Same schema SAID as 'optional_edge_present' -- 'e' is legal "
                "to omit under that schema, and this instance omits it. H9 "
                "at section granularity: issuance-time absence, committed by "
                "the top-level SAID, not a rendering error."
            ),
            "matrix_cells": ["H9"],
            "rules_exercised": ["RULE 1", "RULE 13"],
            "notes": "corpus-keripy-examples.md 'Shapes still missing': every schema there makes edges required; this pair does not.",
        },
    }


@fixture("diamond_depth_a")
def build_diamond_depth_a(corpus_dir):
    schema_said, _ = schemas.attr_schema(
        title="Shared Ancestor Schema", credential_type="ArcvizFixture_DiamondAncestor",
        attr_props={"standard": {"type": "string"}}, attr_required=["standard"])
    issuer = det.aid("diamond:root_authority")
    serder = credential("diamond_depth_a", issuer=issuer, schema_said=schema_said,
                         attrs={"standard": "ISO-9001-ish Baseline"})
    return {
        "serder": serder,
        "meta": {
            "title": "Diamond-with-depth: shared ancestor (leaf)",
            "summary": "The reconvergence point both DAG paths reach.",
            "matrix_cells": ["H1"], "rules_exercised": [],
        },
    }


@fixture("diamond_depth_b", depends_on=["diamond_depth_a"])
def build_diamond_depth_b(corpus_dir):
    import json
    a = json.loads((corpus_dir / "diamond_depth_a.json").read_text())
    a_schema, _ = schemas.attr_schema(
        title="Shared Ancestor Schema", credential_type="ArcvizFixture_DiamondAncestor",
        attr_props={"standard": {"type": "string"}}, attr_required=["standard"])
    schema_said, _ = schemas.attr_schema(
        title="Diamond Short-Path Schema", credential_type="ArcvizFixture_DiamondShortPath",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    issuer = det.aid("diamond:short_path_issuer")
    edge = {'d': '', 'baseline': simple_edge("diamond:b", n=a['d'], s=a_schema)}
    serder = credential("diamond_depth_b", issuer=issuer, schema_said=schema_said,
                         attrs={"scope": "short path, one hop from the ancestor"}, edge=edge)
    return {
        "serder": serder,
        "meta": {
            "title": "Diamond-with-depth: short-path node B (depth 1 from origin)",
            "summary": "One hop from the shared ancestor A.",
            "matrix_cells": ["H1"], "rules_exercised": [],
            "depends_on": ["diamond_depth_a"],
        },
    }


@fixture("diamond_depth_f", depends_on=["diamond_depth_a"])
def build_diamond_depth_f(corpus_dir):
    import json
    a = json.loads((corpus_dir / "diamond_depth_a.json").read_text())
    a_schema, _ = schemas.attr_schema(
        title="Shared Ancestor Schema", credential_type="ArcvizFixture_DiamondAncestor",
        attr_props={"standard": {"type": "string"}}, attr_required=["standard"])
    schema_said, _ = schemas.attr_schema(
        title="Diamond Long-Path Waypoint Schema", credential_type="ArcvizFixture_DiamondWaypoint",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    issuer = det.aid("diamond:long_path_waypoint_issuer")
    edge = {'d': '', 'baseline': simple_edge("diamond:f", n=a['d'], s=a_schema)}
    serder = credential("diamond_depth_f", issuer=issuer, schema_said=schema_said,
                         attrs={"scope": "long path, one hop from the ancestor"}, edge=edge)
    return {
        "serder": serder,
        "meta": {
            "title": "Diamond-with-depth: long-path waypoint F (depth 1 from A, depth 2 from origin)",
            "summary": "Intermediate node on the longer of the two reconverging paths.",
            "matrix_cells": ["H1"], "rules_exercised": [],
            "depends_on": ["diamond_depth_a"],
        },
    }


@fixture("diamond_depth_c", depends_on=["diamond_depth_f"])
def build_diamond_depth_c(corpus_dir):
    import json
    f = json.loads((corpus_dir / "diamond_depth_f.json").read_text())
    f_schema, _ = schemas.attr_schema(
        title="Diamond Long-Path Waypoint Schema", credential_type="ArcvizFixture_DiamondWaypoint",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    schema_said, _ = schemas.attr_schema(
        title="Diamond Long-Path Entry Schema", credential_type="ArcvizFixture_DiamondLongPath",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    issuer = det.aid("diamond:long_path_issuer")
    edge = {'d': '', 'waypoint': simple_edge("diamond:c", n=f['d'], s=f_schema)}
    serder = credential("diamond_depth_c", issuer=issuer, schema_said=schema_said,
                         attrs={"scope": "long path, two hops from the ancestor"}, edge=edge)
    return {
        "serder": serder,
        "meta": {
            "title": "Diamond-with-depth: long-path node C (depth 1 from origin, depth 2 from ancestor)",
            "summary": "Origin's long-path neighbor; reaches the shared ancestor via F.",
            "matrix_cells": ["H1"], "rules_exercised": [],
            "depends_on": ["diamond_depth_f"],
        },
    }


@fixture("diamond_depth_origin", depends_on=["diamond_depth_b", "diamond_depth_c"])
def build_diamond_depth_origin(corpus_dir):
    """The origin/presented node: a diamond (two paths reconverging at
    diamond_depth_a) where one path has depth 2 (origin->B->A) and the other
    has depth 3 (origin->C->F->A) -- production has depth without branching,
    keripy's guardian-presentation DAG has branching without depth beyond 2;
    nothing in the corpus has both (corpus-keripy-examples.md 'Shapes still
    missing').
    """
    import json
    b = json.loads((corpus_dir / "diamond_depth_b.json").read_text())
    c = json.loads((corpus_dir / "diamond_depth_c.json").read_text())
    b_schema, _ = schemas.attr_schema(
        title="Diamond Short-Path Schema", credential_type="ArcvizFixture_DiamondShortPath",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    c_schema, _ = schemas.attr_schema(
        title="Diamond Long-Path Entry Schema", credential_type="ArcvizFixture_DiamondLongPath",
        attr_props={"scope": {"type": "string"}}, attr_required=["scope"])
    schema_said, _ = schemas.attr_schema(
        title="Diamond Origin Schema", credential_type="ArcvizFixture_DiamondOrigin",
        attr_props={"claim": {"type": "string"}}, attr_required=["claim"])
    issuer = det.aid("diamond:origin_issuer")
    edge = {
        'd': '',
        'shortPath': simple_edge("diamond:origin:short", n=b['d'], s=b_schema),
        'longPath': simple_edge("diamond:origin:long", n=c['d'], s=c_schema),
    }
    serder = credential("diamond_depth_origin", issuer=issuer, schema_said=schema_said,
                         attrs={"claim": "reachable via two paths of unequal length"}, edge=edge)
    return {
        "serder": serder,
        "meta": {
            "title": "Diamond-with-depth: origin (presented node)",
            "summary": (
                "origin -> B -> A (depth 2) and origin -> C -> F -> A (depth "
                "3) reconverge at the shared ancestor A. Diamond convergence "
                "plus depth greater than keripy's existing (depth-2) diamond, "
                "neither of which the production vLEI chain (pure depth, no "
                "branching) exercises."
            ),
            "matrix_cells": ["H1"], "rules_exercised": [],
            "depends_on": ["diamond_depth_b", "diamond_depth_c"],
        },
    }
