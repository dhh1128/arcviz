"""SC7 (docs/design/shape-catalog.md) gaps G6 and G7: two of Rule 8's four
compact-block treatments the corpus previously had none of (the H3 leg
already existed via blinded_rule_group and every H3-shaped edge/rule
fixture; H2 and the permissive-schema-undecidable case did not).

Gap G8 (schema-unresolved: "a schema we do not have") is deliberately NOT
attempted here -- see the module-level note at the bottom of this file for
why it needs generator surgery rather than a new fixture definition.
"""

from .. import determinism as det
from .. import schemas
from ..common import compact_block, credential_with_compact_attribute
from ..registry import fixture


@fixture("unblinded_commitment_h2")
def build_unblinded_commitment_h2(corpus_dir):
    """H2: a compact block whose SAID-verified schema reserves NO `u` at
    all -- gap G6. Unlike every H3 fixture in this corpus, there is no
    entropy behind this SAID even in principle: the schema's value space
    (one boolean) is small enough that, per spec-body.md:160, the content
    "may be discoverable now by rainbow/dictionary attack" -- an unblinded
    commitment SHOULD be treated as public, never given the lock/private
    treatment reserved for H3 (Rule 8's gravest lie).
    """
    issuer = det.aid("unblinded_h2:issuer")
    issuee = det.aid("unblinded_h2:issuee")

    schema_said, schema_mad = schemas.attr_schema(
        title="Unblinded Commitment (H2) Demo Schema",
        credential_type="ArcvizFixture_UnblindedH2",
        attr_props={"overThreshold": {"type": "boolean"}},
        attr_required=["overThreshold"],
        require_issuee=True,
        reserve_u=False,  # the schema affirmatively reserves no u -- unconditionally H2
    )

    bare_said, full_block = compact_block({"overThreshold": True}, issuee=issuee)
    serder = credential_with_compact_attribute(
        "unblinded_commitment_h2", issuer=issuer, schema_said=schema_said,
        bare_attribute_said=bare_said,
    )

    return {
        "serder": serder,
        "expanded": {
            "attribute_block": full_block,
            "note": (
                "Shown for test verification only. In a real presentation "
                "this content is never disclosed as a block -- but unlike "
                "H3, it doesn't need to be: with the schema resolved (one "
                "boolean field, no `u`), the value space is {True, False} "
                "and a verifier holding just the schema and this SAID can "
                "brute-force which one it is."
            ),
        },
        "meta": {
            "title": "Unblinded commitment (H2): schema reserves no u",
            "summary": (
                "The `a` field is a bare SAID computed over a block whose "
                "resolved schema declares only {d, i, overThreshold} -- no "
                "`u` property at all. This is unconditionally H2: the "
                "commitment is guessable in principle from schema + SAID "
                "alone, not merely undecided (contrast "
                "'permissive_schema_undecidable', gap G7, whose schema "
                "allows but does not mandate `u`)."
            ),
            "matrix_cells": ["H2"],
            "rules_exercised": ["RULE 8"],
            "spec_refs": ["spec-body.md:160"],
            "notes": (
                "docs/design/shape-catalog.md gap G6. Pairs with "
                "'permissive_schema_undecidable' (G7) to give Rule 8's test "
                "two of its remaining three named treatments; G8 "
                "(schema-unresolved) is not attempted -- see this module's "
                "docstring."
            ),
        },
    }


@fixture("permissive_schema_undecidable")
def build_permissive_schema_undecidable(corpus_dir):
    """Pair 11 / gap G7: a compact block whose schema makes `u` OPTIONAL
    (declared, not required -- the shape every other attr_schema() call in
    this corpus already has by default). From the resolved schema plus the
    bare SAID alone, a viewer cannot tell whether THIS PARTICULAR instance
    used the entropy or not -- undecidable between H2 and H3, not merely
    "hidden". This fixture's actual ground truth (documented only in
    .expanded.json, never disclosed) is that it DID use `u`; the point is
    that nothing in the disclosed artifact lets a viewer confirm that.
    """
    issuer = det.aid("permissive_undecidable:issuer")
    issuee = det.aid("permissive_undecidable:issuee")

    schema_said, schema_mad = schemas.attr_schema(
        title="Permissive-Schema Undecidable Demo Schema",
        credential_type="ArcvizFixture_PermissiveUndecidable",
        attr_props={"overThreshold": {"type": "boolean"}},
        attr_required=["overThreshold"],
        require_issuee=True,
        reserve_u=True,  # the default: u is declared but NOT required
    )

    bare_said, full_block = compact_block(
        {"overThreshold": True}, issuee=issuee,
        u=det.nonce("permissive_undecidable:u"))  # ground truth: u WAS used
    serder = credential_with_compact_attribute(
        "permissive_schema_undecidable", issuer=issuer, schema_said=schema_said,
        bare_attribute_said=bare_said,
    )

    return {
        "serder": serder,
        "expanded": {
            "attribute_block": full_block,
            "ground_truth_u_was_used": True,
            "note": (
                "This instance actually included `u` (genuine entropy), but "
                "a schema-only reader cannot tell: the same schema equally "
                "permits an instance that omitted it (compare "
                "'unblinded_commitment_h2', which uses a DIFFERENT schema "
                "that forbids u outright and is thus unconditionally H2)."
            ),
        },
        "meta": {
            "title": "Permissive-schema undecidable (H2 vs H3, pair 11)",
            "summary": (
                "The `a` field is a bare SAID computed over a block whose "
                "resolved schema declares `u` as legal but not required. A "
                "viewer resolving the schema learns this instance MIGHT be "
                "genuinely blinded (H3) or might just be an unused-entropy "
                "compaction (H2) -- and cannot resolve that from the "
                "disclosed sad, the schema, or both together. The honest "
                "render is 'hidden; protection unknown', distinct from both "
                "H2's and H3's own treatments (Rule 8's third state)."
            ),
            "matrix_cells": ["H2", "H3"],
            "rules_exercised": ["RULE 8"],
            "spec_refs": [
                "spec-body.md:160", "spec-body.md:164",
            ],
            "notes": (
                "docs/design/shape-catalog.md gap G7, disclosure-matrix.md "
                "(c) pair 5 (\"Blinded vs unblinded commitment (H3 vs H2) "
                "when the schema is not in hand\") generalized to the case "
                "where the schema IS in hand but is itself permissive."
            ),
        },
    }


# G8 (schema-unresolved: "a schema we do not have") is not attempted here.
# Every fixture in this corpus references its schema purely by SAID -- no
# fixture module, including this one, ever writes a schema out as its own
# corpus/*.json artifact. Nothing today distinguishes "the schema exists
# somewhere resolvable" from "the schema is gone": there is no schemas/
# directory, no registry of which schema SAIDs the corpus can resolve, and
# no test that resolves a fixture's schema from disk rather than by
# recomputing it from the same Python call that built it. Manufacturing a
# schema-unresolved fixture without first building that resolution concept
# would not produce a meaningfully different artifact from every other
# fixture here -- it would just be a fixture, indistinguishable from the
# rest by any test this generator could write. That is generator surgery
# (a new schemas/ corpus concept and a resolution convention), not a new
# fixture definition, so it is left as a named, open gap rather than faked.
