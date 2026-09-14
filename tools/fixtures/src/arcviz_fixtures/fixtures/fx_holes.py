"""SC6 (docs/design/shape-catalog.md) gap G2: two Compact Private Edges (H8)
from one node, such that a viewer cannot tell whether they converge on the
same far node or point at two different ones.

The mechanism that makes this true is worth being explicit about, because it
is not "the fixture author picked SAIDs that happen to collide or not": each
edge's outer SAID is a digest over (d, u, n, s[, o]), and the two edges use
DIFFERENT `u` nonces even when their `n` is identical. So the two disclosed
bare-SAID strings are *always* different from each other, regardless of
whether the far nodes converge -- the disclosed bytes carry no information
about convergence either way. That is the point being tested: two fixtures
built with opposite ground truths (documented, dev-only, in each one's
.expanded.json) must be indistinguishable from their disclosed sad alone.
"""

from keri.core.coring import Kinds
from keri.core.mapping import Compactor

from .. import determinism as det
from ..common import credential, simple_edge
from ..registry import fixture


def _tiny_attr_schema(title, ctype):
    from .. import schemas
    return schemas.attr_schema(
        title=title, credential_type=ctype,
        attr_props={"label": {"type": "string"}}, attr_required=["label"])


def _build_two_blinded_edges(label, *, far_a_said, far_a_schema,
                              far_b_said, far_b_schema):
    """Shared builder: a near node with two independently-blinded edge
    slots, sourceA and sourceB, each collapsed to its own bare SAID with its
    own `u`. Structurally identical regardless of whether far_a_said equals
    far_b_said -- that identity is the only thing that varies between the
    converge/diverge fixtures below.
    """
    near_issuer = det.aid(f"{label}:near_issuer")
    near_schema, _ = _tiny_attr_schema(
        f"Two Blinded Edges ({label}) -- Near Node Schema",
        "ArcvizFixture_TwoBlindedEdges_Near")

    raw_group = {
        'd': '',
        'sourceA': simple_edge(f"{label}:a", n=far_a_said, s=far_a_schema,
                                u=det.nonce(f"{label}:edgeA_u")),
        'sourceB': simple_edge(f"{label}:b", n=far_b_said, s=far_b_schema,
                                u=det.nonce(f"{label}:edgeB_u")),
    }
    compactor = Compactor(mad=raw_group, makify=True, compactify=True, kind=Kinds.json)
    edge_group = compactor.mad  # {'d': <group_said>, 'sourceA': <bare>, 'sourceB': <bare>}

    near = credential(
        f"{label}_near", issuer=near_issuer, schema_said=near_schema,
        attrs={"label": "presenting node with two independently blinded edges"},
        edge=edge_group,
    )
    return near


@fixture("two_blinded_edges_converge")
def build_two_blinded_edges_converge(corpus_dir):
    """Ground truth (dev-only, see .expanded.json): sourceA and sourceB
    point at the SAME far node. Nothing in the disclosed sad says so.
    """
    far_issuer = det.aid("two_blinded_edges:converge:far_issuer")
    far_schema, _ = _tiny_attr_schema(
        "Two Blinded Edges (converge) -- Far Node Schema",
        "ArcvizFixture_TwoBlindedEdges_Far")
    far = credential("two_blinded_edges_converge_far", issuer=far_issuer,
                      schema_said=far_schema,
                      attrs={"label": "the one far node both edges point at"})

    near = _build_two_blinded_edges(
        "two_blinded_edges_converge",
        far_a_said=far.said, far_a_schema=far_schema,
        far_b_said=far.said, far_b_schema=far_schema,
    )

    return {
        "serder": near,
        "expanded": {
            "ground_truth": "converge",
            "far_node": far.sad,
            "note": (
                "Both sourceA and sourceB actually point at this SAME far "
                "node. This file is dev-only verification content -- a real "
                "presenter using this mechanism discloses none of it, and a "
                "renderer must not treat the two disclosed SAID strings "
                "(which differ from each other, since each edge has its own "
                "u) as any kind of signal either way."
            ),
        },
        "meta": {
            "title": "Two blinded edges, one node -- convergence unknowable (ground truth: converge)",
            "summary": (
                "A near node with two Compact Private Edges, sourceA and "
                "sourceB, each an independent bare SAID computed with its "
                "own `u`. A viewer KNOWS: two committed edges exist, in "
                "named slots, each hiding its destination. A viewer CANNOT "
                "KNOW: whether sourceA and sourceB point at the same far "
                "node or two different ones -- the two disclosed SAID "
                "strings differ from each other regardless, because each "
                "edge's own `u` differs, so string comparison carries no "
                "signal. This fixture's actual ground truth (documented "
                "only in two_blinded_edges_converge.expanded.json, never "
                "disclosed) is that they converge; the sibling fixture "
                "two_blinded_edges_diverge has the opposite ground truth "
                "and is byte-for-byte the same SHAPE -- a renderer that "
                "treats the two fixtures differently is inferring "
                "information the format does not carry."
            ),
            "matrix_cells": ["H8"],
            "rules_exercised": ["RULE 1"],
            "spec_refs": ["spec-body.md:1165", "spec-body.md:1164"],
            "notes": (
                "Instantiates disclosure-matrix.md (b) I2's inference: "
                "'two H8 edges in one graph may or may not share a far "
                "node... the layout must be able to draw uncertain "
                "convergence' -- see docs/design/shape-catalog.md SC6 and "
                "gap G2."
            ),
        },
    }


@fixture("two_blinded_edges_diverge")
def build_two_blinded_edges_diverge(corpus_dir):
    """Ground truth (dev-only, see .expanded.json): sourceA and sourceB
    point at two DIFFERENT far nodes. Nothing in the disclosed sad says so
    either -- compare against two_blinded_edges_converge, which is
    structurally identical with the opposite ground truth.
    """
    far_a_issuer = det.aid("two_blinded_edges:diverge:far_a_issuer")
    far_b_issuer = det.aid("two_blinded_edges:diverge:far_b_issuer")
    far_a_schema, _ = _tiny_attr_schema(
        "Two Blinded Edges (diverge) -- Far Node A Schema",
        "ArcvizFixture_TwoBlindedEdges_FarA")
    far_b_schema, _ = _tiny_attr_schema(
        "Two Blinded Edges (diverge) -- Far Node B Schema",
        "ArcvizFixture_TwoBlindedEdges_FarB")
    far_a = credential("two_blinded_edges_diverge_far_a", issuer=far_a_issuer,
                        schema_said=far_a_schema, attrs={"label": "far node A"})
    far_b = credential("two_blinded_edges_diverge_far_b", issuer=far_b_issuer,
                        schema_said=far_b_schema, attrs={"label": "far node B"})

    near = _build_two_blinded_edges(
        "two_blinded_edges_diverge",
        far_a_said=far_a.said, far_a_schema=far_a_schema,
        far_b_said=far_b.said, far_b_schema=far_b_schema,
    )

    return {
        "serder": near,
        "expanded": {
            "ground_truth": "diverge",
            "far_node_a": far_a.sad,
            "far_node_b": far_b.sad,
            "note": (
                "sourceA and sourceB point at two DIFFERENT far nodes. "
                "Dev-only verification content -- see the sibling fixture's "
                "note for why this must render identically to the "
                "converging case."
            ),
        },
        "meta": {
            "title": "Two blinded edges, one node -- convergence unknowable (ground truth: diverge)",
            "summary": (
                "Structurally identical to two_blinded_edges_converge -- "
                "same shape, same two named H8 edge slots -- but this "
                "fixture's actual ground truth (documented only in the "
                ".expanded.json, never disclosed) is that sourceA and "
                "sourceB point at two DIFFERENT far nodes. A viewer cannot "
                "tell this fixture apart from its converging sibling from "
                "the disclosed sad alone, which is exactly the property "
                "under test: the render must be the same for both."
            ),
            "matrix_cells": ["H8"],
            "rules_exercised": ["RULE 1"],
            "spec_refs": ["spec-body.md:1165", "spec-body.md:1164"],
            "notes": "Pair with two_blinded_edges_converge; see that fixture's notes.",
        },
    }
