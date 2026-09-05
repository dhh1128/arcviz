"""A de-identified equivalent of the real vLEI ECR credential chain analyzed
in corpus-vlei-chain.md: linear depth 4 (QVI -> LE -> ECR-AUTH -> ECR), three
edges, four registries, entirely invented attribute values, freshly computed
SAIDs.

Deliberately reproduced: the chain shape and issuer/subject alternation
(credential N's issuer is credential N-1's issuee, sec.1); one edge writing
its operator explicitly (`auth`, o=I2I) next to two left at the default
(`qvi`, `le`), the one real inconsistency corpus-vlei-chain.md sec.2 flags as
worth carrying into arcviz; a leaf-only top-level `u` (sec.4: "u ... appears
only on credential #3"); and one registry per credential (four total).

Deliberately NOT reproduced -- a scope decision, not an oversight: any
KEL-level fact from corpus-vlei-chain.md sec.3 (weighted multisig, the one
asymmetric key rotation, the absent root delegator's KEL, witness thresholds,
the bloated/duplicated KEL). This generator computes ACDC and registry-
inception SAIDs; it does not simulate a KERI keystore, sign anything, or
construct icp/dip/drt/ixn events (see README.md "What this does not model").
Concretely, this means the real chain's H7 case (root delegator's KEL absent
from the payload) is NOT exercised here, because there is no KEL in this
fixture at all -- absent or otherwise. A future fixture that models KEL
events would be needed to close that gap.
"""

from .. import determinism as det
from .. import schemas
from ..common import credential, make_registry, simple_edge
from ..registry import fixture

_DT_PROP = {"dt": {"type": "string", "format": "date-time"}}
_LEI_PROP = {"LEI": {"type": "string"}}


@fixture("vlei_qvi")
def build_vlei_qvi(corpus_dir):
    issuer = det.aid("vlei:root_authority")          # stands in for EINmHd5g... (delegate of the absent root)
    issuee = det.aid("vlei:qvi_org")                  # stands in for ED88Jn6C... (the QVI's own AID)
    registry = make_registry("vlei_qvi", issuer)
    schema_said, _ = schemas.attr_schema(
        title="QVI vLEI Credential Schema (fixture)",
        credential_type="ArcvizFixture_QVI",
        attr_props={**_LEI_PROP, **_DT_PROP}, attr_required=["LEI", "dt"])
    serder = credential(
        "vlei_qvi", issuer=issuer, issuee=issuee, schema_said=schema_said,
        attrs={"LEI": "984500ARCV1Z0000FIX01", "dt": det.stamp("vlei:qvi")},
        registry=registry.said,
    )
    return {
        "serder": serder,
        "extra_writes": {"vlei_qvi.registry": registry},
        "meta": {
            "title": "vLEI-equivalent chain: QVI credential (root, depth 1 of 4)",
            "summary": "Root of the chain; no edges. Issuer stands in for the real chain's delegate-of-the-absent-root; issuee stands in for the QVI's own AID.",
            "matrix_cells": ["H1"],
            "rules_exercised": [],
            "notes": "See fx_vlei.py module docstring for what is and is not reproduced from corpus-vlei-chain.md.",
        },
    }


@fixture("vlei_le", depends_on=["vlei_qvi"])
def build_vlei_le(corpus_dir):
    import json
    qvi = json.loads((corpus_dir / "vlei_qvi.json").read_text())
    qvi_schema, _ = schemas.attr_schema(
        title="QVI vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_QVI",
        attr_props={**_LEI_PROP, **_DT_PROP}, attr_required=["LEI", "dt"])

    issuer = qvi["a"]["i"] if isinstance(qvi["a"], dict) else det.aid("vlei:qvi_org")
    issuee = det.aid("vlei:legal_entity")
    registry = make_registry("vlei_le", issuer)
    schema_said, _ = schemas.attr_schema(
        title="LE vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_LE",
        attr_props={**_LEI_PROP, **_DT_PROP}, attr_required=["LEI", "dt"])

    edge = {'d': '', 'qvi': simple_edge("vlei:le:qvi", n=qvi['d'], s=qvi_schema)}  # default operator (no 'o')
    serder = credential(
        "vlei_le", issuer=issuer, issuee=issuee, schema_said=schema_said,
        attrs={"LEI": "984500ARCV1Z0000FIX01", "dt": det.stamp("vlei:le")},
        registry=registry.said, edge=edge,
    )
    return {
        "serder": serder,
        "extra_writes": {"vlei_le.registry": registry},
        "meta": {
            "title": "vLEI-equivalent chain: LE credential (depth 2 of 4)",
            "summary": "Issuer is the QVI credential's issuee (issuer/subject alternation begins here). Edge 'qvi' left at the default I2I operator (no 'o' written).",
            "matrix_cells": ["H1"],
            "rules_exercised": ["RULE 9"],
            "depends_on": ["vlei_qvi"],
        },
    }


@fixture("vlei_ecr_auth", depends_on=["vlei_le"])
def build_vlei_ecr_auth(corpus_dir):
    import json
    le = json.loads((corpus_dir / "vlei_le.json").read_text())
    le_schema, _ = schemas.attr_schema(
        title="LE vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_LE",
        attr_props={**_LEI_PROP, **_DT_PROP}, attr_required=["LEI", "dt"])

    issuer = le["a"]["i"] if isinstance(le["a"], dict) else det.aid("vlei:legal_entity")
    issuee = det.aid("vlei:qvi_org")  # alternation: subject flips back to the QVI org AID
    registry = make_registry("vlei_ecr_auth", issuer)
    schema_said, _ = schemas.attr_schema(
        title="ECR-AUTH vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_ECR_AUTH",
        attr_props={
            **_LEI_PROP, **_DT_PROP,
            "AID": {"type": "string"},
            "personLegalName": {"type": "string"},
            "engagementContextRole": {"type": "string"},
        },
        attr_required=["LEI", "dt", "AID", "personLegalName", "engagementContextRole"])

    edge = {'d': '', 'le': simple_edge("vlei:auth:le", n=le['d'], s=le_schema)}  # default operator
    person_aid = det.aid("vlei:person")
    serder = credential(
        "vlei_ecr_auth", issuer=issuer, issuee=issuee, schema_said=schema_said,
        attrs={
            "LEI": "984500ARCV1Z0000FIX01", "dt": det.stamp("vlei:ecr_auth"),
            "AID": person_aid, "personLegalName": "Jordan Q. Fixture",
            "engagementContextRole": "Compliance Analyst",
        },
        registry=registry.said, edge=edge,
    )
    return {
        "serder": serder,
        "extra_writes": {"vlei_ecr_auth.registry": registry},
        "meta": {
            "title": "vLEI-equivalent chain: ECR-AUTH credential (depth 3 of 4)",
            "summary": "Issuer is the LE credential's issuee; issuee flips back to the QVI org AID -- the 'chain alternates who is speaking' (corpus-vlei-chain.md sec.1). Edge 'le' at the default operator.",
            "matrix_cells": ["H1"],
            "rules_exercised": ["RULE 9"],
            "depends_on": ["vlei_le"],
        },
    }


@fixture("vlei_ecr", depends_on=["vlei_ecr_auth"])
def build_vlei_ecr(corpus_dir):
    import json
    auth = json.loads((corpus_dir / "vlei_ecr_auth.json").read_text())
    auth_schema, _ = schemas.attr_schema(
        title="ECR-AUTH vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_ECR_AUTH",
        attr_props={
            **_LEI_PROP, **_DT_PROP, "AID": {"type": "string"},
            "personLegalName": {"type": "string"}, "engagementContextRole": {"type": "string"},
        },
        attr_required=["LEI", "dt", "AID", "personLegalName", "engagementContextRole"])

    issuer = auth["a"]["i"] if isinstance(auth["a"], dict) else det.aid("vlei:qvi_org")
    issuee = det.aid("vlei:person")  # the individual holder's own AID
    registry = make_registry("vlei_ecr", issuer)
    schema_said, _ = schemas.attr_schema(
        title="ECR vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_ECR",
        attr_props={
            **_LEI_PROP, **_DT_PROP,
            "personLegalName": {"type": "string"},
            "engagementContextRole": {"type": "string"},
        },
        attr_required=["LEI", "dt", "personLegalName", "engagementContextRole"])

    # EXPLICIT o=I2I here, vs. the default left implicit on 'qvi' and 'le' --
    # the one real inconsistency corpus-vlei-chain.md sec.2 flags.
    edge = {'d': '', 'auth': simple_edge("vlei:ecr:auth", n=auth['d'], s=auth_schema, o="I2I")}

    serder = credential(
        "vlei_ecr", issuer=issuer, issuee=issuee, schema_said=schema_said,
        attrs={
            "LEI": "984500ARCV1Z0000FIX01", "dt": det.stamp("vlei:ecr"),
            "personLegalName": "Jordan Q. Fixture", "engagementContextRole": "Compliance Analyst",
        },
        registry=registry.said, edge=edge,
        top_uuid=det.nonce("vlei:ecr:top_u"),  # leaf-ONLY top-level u, per sec.4
    )
    return {
        "serder": serder,
        "extra_writes": {"vlei_ecr.registry": registry},
        "meta": {
            "title": "vLEI-equivalent chain: ECR credential (leaf, depth 4 of 4)",
            "summary": (
                "The individual holder's own credential. Carries the chain's "
                "ONLY top-level `u` (anti-correlation salt on a small, "
                "guessable attribute space -- LEI + role), matching "
                "corpus-vlei-chain.md sec.4 exactly. Edge 'auth' writes "
                "o=I2I EXPLICITLY, unlike 'qvi' and 'le' upstream, which "
                "leave it at the default -- render these identically "
                "(RULE 9)."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": ["RULE 9"],
            "depends_on": ["vlei_ecr_auth"],
            "notes": (
                "Also satisfies corpus-keripy-examples.md's 'depth-3-or-more "
                "chain' missing-shape (this chain is depth 4) -- no separate "
                "generic deep-chain fixture is built to avoid duplicating it."
            ),
        },
    }
