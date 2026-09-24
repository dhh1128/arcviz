"""Presentation-SHAPE fixtures, as opposed to disclosure-mechanism fixtures.

Every other module here targets a cell of `docs/research/disclosure-matrix.md` -- a
blinding, a compaction, an operator. This one targets nothing in that matrix. It exists
because the corpus was measured on 2026-09-23 and found to contain, across 29 ACDCs, only
four presentations of more than one node: the synthetic `diamond_depth` chain, the vLEI
delegation chain, the three-node household, and `working_edge_group`. None is a
heterogeneous bundle of evidence. That was not a defect -- the corpus was built to exercise
mechanisms, and it does -- but Daniel settled on 2026-09-23 that **the DAG, not the
credential, is the scope of evaluation** when deciding what description of a credential
would help a viewer, and an instrument holding four DAGs cannot evaluate a claim about DAGs.

His worked example is the one built here: an insurance adjuster's accident report, holding
photographs of the vehicles, driving licences of the drivers, and witness statements. It was
chosen over the dossier specification's other patterns because it is the case where the
*subject kinds differ inside one bundle* -- a licence is about a person, a photograph is
about a car, a statement is about an event -- which is the distinction that the single-axis
question "what identifies a credential" kept collapsing.

WHAT IT IS BUILT TO TEST, and the reason for its shape. Three matched pairs, each of which
collides on everything the render can currently show and is separated by a DIFFERENT thing:

  - the two driving licences share a schema and an issuer, and differ only in their ISSUEE;
  - the two photographs share a schema and an issuer, carry no issuee at all, and differ
    only in an issuer-chosen attribute naming the THING depicted;
  - the two witness statements share a schema and an ISSUEE -- both are given to the
    insurer -- and differ only in their ISSUER, the witness.

So a proposal that identifies credentials by any single channel fails at least one pair
here, visibly, in a bundle a human can reason about. That is the whole point: the corpus's
existing `same_schema_alice` / `same_schema_bob` pair already proves that schema and issuer
can collide, but it proves it once, in the abstract, with the answer (the issuee) available.

TWO PROPERTIES OF THE FIXTURE ARE THEMSELVES FINDINGS rather than design choices.

First, the root carries no issuee. That is not an omission: the live VVP dossier at
`eu-west.provenant.net/.../EB2jhY5laLc4rcWCEWLzT69mxEIfXJZ3kNzWfKx2vHpP` is shaped the same
way -- untargeted, no attribute but a timestamp, its entire content the labels of its four
edges. A presented root is the claim rather than a part of it, so it has no incoming edge to
be named by and nothing to be "about".

Second, the edge labels degenerate. `licenceA` and `licenceB` name the ROLE the exhibit
plays and then fall back to a bare letter to separate the two instances -- which is
`ITEM 03` reappearing one level up, in the channel that was supposed to have replaced it.
That is realistic (the VVP dossier's own labels are `vetting`, `alloc`, `tnalloc`, `delsig`,
role names that would collide the moment there were two allocations) and it is left in
deliberately. An edge label carries role and not instance, and this fixture should show
that rather than be tuned to hide it.

NOTHING HERE IS A CLAIM ABOUT HOW ANY OF IT SHOULD RENDER. The categories in the summaries
below are named from `docs/design/credential-categories.md`, whose nine categories are
settled; the `subject` and `alignment` values are from that document's second axis, which it
marks as synthesized and not ratified, and they are repeated here in the same spirit.
"""

import json

from .. import determinism as det
from .. import schemas
from ..common import credential, simple_edge
from ..registry import fixture

# One occurrence, and every exhibit in the bundle bears on it. Held as a literal rather than
# as a credential because a collision is not a credential; the licences, photographs and
# statements are the evidence, and the event is what they are evidence about.
OCCURRENCE = "2026-03-02T08:41:00+00:00"
CLAIM_REF = "CLM-2026-0041"

# Issuance dates (`a.dt`). Every ACDC in the live VVP dossier carries one and only 4 of
# the 36 corpus fixtures did, so the instrument could not test a channel that production
# credentials use universally. The values are chosen to carry ARGUMENT STRUCTURE rather
# than merely to differ: the licences predate the collision by years and are background
# the claim did not create, while the photographs, statements and the claim file itself
# are minutes apart because they were assembled as one act, for this claim. That is the
# same shape the real dossier shows -- two credentials from December, then three within
# 57 seconds of each other in March.
ISSUED = {
    "licence_a": "2021-06-30T09:12:00+00:00",
    "licence_b": "2019-11-14T11:48:00+00:00",
    "photo_a": "2026-03-02T10:15:40+00:00",
    "photo_b": "2026-03-02T10:16:05+00:00",
    "statement_a": "2026-03-04T14:02:00+00:00",
    "statement_b": "2026-03-05T09:30:00+00:00",
    "bundle": "2026-03-06T08:00:00+00:00",
}


def _licence_schema():
    return schemas.attr_schema(
        title="Driving Licence Schema",
        credential_type="ArcvizFixture_DrivingLicence",
        attr_props={
            "dt": {"type": "string"},
            "licenceNumber": {"type": "string"},
            "holderName": {"type": "string"},
            "classes": {"type": "array", "items": {"type": "string"}},
            "expires": {"type": "string"},
        },
        attr_required=["dt", "licenceNumber", "holderName", "classes", "expires"],
        require_issuee=True,
    )


def _photograph_schema():
    return schemas.attr_schema(
        title="Scene Photograph Attestation Schema",
        credential_type="ArcvizFixture_ScenePhotograph",
        attr_props={
            "dt": {"type": "string"},
            "depicts": {"type": "string"},
            "vehicleVin": {"type": "string"},
            "imageDigest": {"type": "string"},
            "capturedAt": {"type": "string"},
        },
        attr_required=["dt", "depicts", "vehicleVin", "imageDigest", "capturedAt"],
    )


def _statement_schema():
    return schemas.attr_schema(
        title="Witness Statement Schema",
        credential_type="ArcvizFixture_WitnessStatement",
        attr_props={
            "dt": {"type": "string"},
            "observedAt": {"type": "string"},
            "account": {"type": "string"},
            "vantagePoint": {"type": "string"},
        },
        attr_required=["dt", "observedAt", "account", "vantagePoint"],
        require_issuee=True,
    )


# The parties. One licensing authority issues both licences, one adjuster attests both
# photographs, and both witnesses address their statements to the same insurer -- each
# sameness is load-bearing, because it is what forces the discriminator onto a different
# channel in each pair.
LICENSING_AUTHORITY = det.aid("accident_bundle:licensing_authority")
ADJUSTER = det.aid("accident_bundle:adjuster")
INSURER = det.aid("accident_bundle:insurer")
DRIVER_A = det.aid("accident_bundle:driver_a")
DRIVER_B = det.aid("accident_bundle:driver_b")
WITNESS_A = det.aid("accident_bundle:witness_a")
WITNESS_B = det.aid("accident_bundle:witness_b")


def _licence(label, *, issuee, number, name, expires, issued):
    schema_said, _ = _licence_schema()
    return credential(
        label, issuer=LICENSING_AUTHORITY, issuee=issuee, schema_said=schema_said,
        attrs={"dt": issued, "licenceNumber": number, "holderName": name,
               "classes": ["B"], "expires": expires},
    ), schema_said


def _photograph(label, *, depicts, vin, digest_seed, issued):
    schema_said, _ = _photograph_schema()
    return credential(
        label, issuer=ADJUSTER, schema_said=schema_said,
        attrs={"dt": issued, "depicts": depicts, "vehicleVin": vin,
               "imageDigest": det.aid(f"accident_bundle:image:{digest_seed}"),
               "capturedAt": "2026-03-02T10:15:00+00:00"},
    ), schema_said


def _statement(label, *, issuer, account, vantage, issued):
    schema_said, _ = _statement_schema()
    return credential(
        label, issuer=issuer, issuee=INSURER, schema_said=schema_said,
        attrs={"dt": issued, "observedAt": OCCURRENCE, "account": account, "vantagePoint": vantage},
    ), schema_said


@fixture("accident_licence_a")
def build_accident_licence_a(corpus_dir):
    serder, _ = _licence("accident_licence_a", issuee=DRIVER_A,
                         number="D-4471-9920", name="Alice Moreau",
                         expires="2031-06-30", issued=ISSUED["licence_a"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: driver A's driving licence",
            "summary": (
                "Category identity and qualification; subject is a PARTY and alignment is "
                "ordinary -- the issuee is who the credential is about. Shares its schema "
                "AND its issuer with accident_licence_b, so within the bundle the pair is "
                "separable only by issuee."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_licence_b")
def build_accident_licence_b(corpus_dir):
    serder, _ = _licence("accident_licence_b", issuee=DRIVER_B,
                         number="D-8813-2077", name="Bob Ferreira",
                         expires="2029-11-14", issued=ISSUED["licence_b"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: driver B's driving licence",
            "summary": (
                "The matched half of accident_licence_a. Same schema, same issuing "
                "authority, different issuee. Whatever channel carries category will show "
                "these two identically."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_photo_a")
def build_accident_photo_a(corpus_dir):
    serder, _ = _photograph("accident_photo_a",
                            depicts="front nearside damage, vehicle A",
                            vin="WVWZZZ1KZAW084471", digest_seed="a", issued=ISSUED["photo_a"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: photograph of vehicle A",
            "summary": (
                "Subject is a THING and there is no issuee at all -- the adjuster attests "
                "what the image depicts, and no party is the credential's subject. This is "
                "the case where 'which party is this about' has no answer, and the only "
                "discriminator against accident_photo_b is an issuer-chosen attribute "
                "(depicts / vehicleVin) that nothing in the credential marks as the subject."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_photo_b")
def build_accident_photo_b(corpus_dir):
    serder, _ = _photograph("accident_photo_b",
                            depicts="offside rear damage, vehicle B",
                            vin="JTDKN3DU0A1075512", digest_seed="b", issued=ISSUED["photo_b"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: photograph of vehicle B",
            "summary": (
                "The matched half of accident_photo_a. Same schema, same attesting "
                "adjuster, no issuee on either -- so the issuee channel that separates the "
                "two licences is not merely unhelpful here, it is absent."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_statement_a")
def build_accident_statement_a(corpus_dir):
    serder, _ = _statement("accident_statement_a", issuer=WITNESS_A,
                           account="The northbound car entered the junction on amber.",
                           vantage="northeast corner, on foot", issued=ISSUED["statement_a"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: first witness statement",
            "summary": (
                "Subject is an OCCURRENCE, and the issuee is the insurer receiving the "
                "statement rather than what the statement is about -- the same divergence "
                "the live VVP dossier's tnalloc credential shows, where an issuee is "
                "present and is not the subject. Shares its schema and its issuee with "
                "accident_statement_b; the pair is separable only by ISSUER."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_statement_b")
def build_accident_statement_b(corpus_dir):
    serder, _ = _statement("accident_statement_b", issuer=WITNESS_B,
                           account="The northbound car was already in the junction.",
                           vantage="southbound queue, second vehicle", issued=ISSUED["statement_b"])
    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle: second witness statement",
            "summary": (
                "The matched half of accident_statement_a, and the two accounts disagree "
                "about the same fact on purpose. A bundle may hold evidence that conflicts, "
                "and nothing in the credentials says so -- both are valid, correctly issued "
                "and mutually inconsistent."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }


@fixture("accident_bundle", depends_on=["accident_licence_a", "accident_licence_b",
                                        "accident_photo_a", "accident_photo_b",
                                        "accident_statement_a", "accident_statement_b"])
def build_accident_bundle(corpus_dir):
    """The adjuster's claim file: one untargeted root over six heterogeneous exhibits."""
    licence_schema, _ = _licence_schema()
    photo_schema, _ = _photograph_schema()
    statement_schema, _ = _statement_schema()

    def said_of(name):
        return json.loads((corpus_dir / f"{name}.json").read_text())["d"]

    # Labels name the ROLE and then fall back to a letter for the instance. Left as-is
    # deliberately -- see this module's docstring.
    edge = {
        'd': '',
        'licenceA': simple_edge("accident_bundle:licenceA",
                                n=said_of("accident_licence_a"), s=licence_schema),
        'licenceB': simple_edge("accident_bundle:licenceB",
                                n=said_of("accident_licence_b"), s=licence_schema),
        'photoA': simple_edge("accident_bundle:photoA",
                              n=said_of("accident_photo_a"), s=photo_schema),
        'photoB': simple_edge("accident_bundle:photoB",
                              n=said_of("accident_photo_b"), s=photo_schema),
        'statementA': simple_edge("accident_bundle:statementA",
                                  n=said_of("accident_statement_a"), s=statement_schema),
        'statementB': simple_edge("accident_bundle:statementB",
                                  n=said_of("accident_statement_b"), s=statement_schema),
    }

    schema_said, _ = schemas.attr_schema(
        title="Accident Claim File Schema",
        credential_type="ArcvizFixture_AccidentClaimFile",
        attr_props={"dt": {"type": "string"},
            "claimReference": {"type": "string"},
                    "occurredAt": {"type": "string"}},
        attr_required=["dt", "claimReference", "occurredAt"],
    )

    serder = credential(
        "accident_bundle", issuer=ADJUSTER, schema_said=schema_said,
        attrs={"dt": ISSUED["bundle"], "claimReference": CLAIM_REF, "occurredAt": OCCURRENCE},
        edge=edge,
    )

    return {
        "serder": serder,
        "meta": {
            "title": "Accident bundle (heterogeneous evidence over one occurrence)",
            "summary": (
                "Seven nodes: an untargeted root over two driving licences, two scene "
                "photographs and two witness statements. Three matched pairs, each "
                "colliding on schema and therefore on category, and each separated by a "
                "different channel -- issuee for the licences, an issuer-chosen attribute "
                "for the photographs, issuer for the statements. The root carries no "
                "issuee, matching the live VVP dossier's shape: a presented root is the "
                "claim rather than a part of it."
            ),
            "matrix_cells": ["H1"],
            "rules_exercised": [],
        },
    }
