"""Minimal, self-SAIDed JSON schemas for fixture ACDCs.

Scope decision, stated plainly: schemas here type the top-level ACDC shape and
the `a` (attribute) or `A` (aggregate) section's own properties precisely
(`additionalProperties: False`, explicit `required`), because those are the
fields these fixtures exist to exercise. The `e` (edge) and `r` (rule)
sections are typed loosely (`oneOf` [string, object], no nested property
schema) rather than reproduced with the ACDC spec's own worked-example
fidelity (see keripy tests/spec/acdc/test_acdc_examples.py for what a fully
elaborated nested edge/rule schema looks like). A loose schema still validates
correctly -- it just doesn't independently constrain edge/rule internals.
That's a deliberate corner cut to keep ~20 fixtures tractable; it does not
affect whether SAIDs are real or whether the targeted disclosure states are
faithfully represented.

Each builder returns (said, schema_dict) via keri.core.Mapper the same way
keripy's own acmSchemaDefault()/actSchemaDefault() do, so the schema itself is
a real SAIDed JSON Schema block, not just a plain dict.
"""

from keri.core import Mapper
from keri.core.coring import Kinds

_BASE_PROPS = {
    "v": {"description": "ACDC version string", "type": "string"},
    "t": {"description": "Message type", "type": "string"},
    "d": {"description": "Message SAID", "type": "string"},
    "u": {"description": "Message UUID", "type": "string"},
    "i": {"description": "Issuer AID", "type": "string"},
    "rd": {"description": "Registry SAID", "type": "string"},
    "s": {
        "description": "Schema Section",
        "oneOf": [
            {"description": "Schema Section SAID", "type": "string"},
            {"description": "Uncompacted Schema Section", "type": "object"},
        ],
    },
}

_LOOSE_EDGE = {
    "description": "Edge Section",
    "oneOf": [
        {"description": "Edge Section SAID", "type": "string"},
        {"description": "Uncompacted Edge Section", "type": "object"},
    ],
}

_LOOSE_RULE = {
    "description": "Rule Section",
    "oneOf": [
        {"description": "Rule Section SAID", "type": "string"},
        {"description": "Uncompacted Rule Section", "type": "object"},
    ],
}


def _mapper_said(mad, kind=Kinds.json):
    mapper = Mapper(mad=mad, makify=True, strict=False, saids={"$id": "E"},
                     saidive=True, kind=kind)
    return mapper.said, mapper.mad


def attr_schema(*, title, credential_type, attr_props, attr_required,
                 has_edge=True, has_rule=True, edge_required=False,
                 rule_required=False, require_issuee=False, reserve_u=True,
                 kind=Kinds.json):
    """Schema for an ACDC carrying an `a` (Attribute) section.

    attr_props/attr_required describe the fields of the *expanded* `a` block
    beyond the always-allowed `d`, `u`, `i` (issuee). additionalProperties is
    False on both the top level and the `a` object variant. `i` is always a
    legal property of the `a` object (present or not never violates
    additionalProperties); require_issuee only controls whether it is
    *mandatory*. Defaults to False -- most fixtures here are untargeted or
    only incidentally carry an issuee, and passing `i` in `attrs` when the
    schema doesn't require it is not a validation conflict either way.

    reserve_u controls the H2/H3 distinction (disclosure-matrix.md sec.
    "H2 ... unblinded commitment ... bare SAID in hand for a block whose
    schema reserves no `u`" vs H3's genuine blind):
      - True (the default, and every schema built before this parameter
        existed): `u` is a DECLARED-but-not-required property of the `a`
        object -- a compact instance under this schema MAY be genuinely
        blinded (H3) or may simply not have used the entropy (an
        undecidable case from schema+SAID alone -- pair 11, gap G7).
      - False: `u` is not a property of the `a` object AT ALL. A compact
        block under this schema can never carry entropy, so it is
        unconditionally H2 -- "guessable in principle... given the schema's
        value space" (spec-body.md:160) -- never merely undecided (gap G6).
    """
    a_object_props = {"d": {"description": "Attribute Section SAID", "type": "string"}}
    if reserve_u:
        a_object_props["u"] = {"description": "Attribute Section UUID", "type": "string"}
    a_object_props["i"] = {"description": "Issuee AID", "type": "string"}
    a_object_props.update(attr_props)
    a_required = ["d"] + (["i"] if require_issuee else []) + list(attr_required)

    props = dict(_BASE_PROPS)
    props["a"] = {
        "description": "Attribute Section",
        "oneOf": [
            {"description": "Attribute Section SAID", "type": "string"},
            {
                "description": "Uncompacted Attribute Section",
                "type": "object",
                "properties": a_object_props,
                "required": a_required,
                "additionalProperties": False,
            },
        ],
    }
    required = ["v", "d", "i", "s", "a"]
    if has_edge:
        props["e"] = _LOOSE_EDGE
        if edge_required:
            required.append("e")
    if has_rule:
        props["r"] = _LOOSE_RULE
        if rule_required:
            required.append("r")

    mad = {
        "$id": "",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "description": f"Schema for {title}.",
        "credentialType": credential_type,
        "version": "2.0.0",
        "type": "object",
        "required": required,
        "properties": props,
        "additionalProperties": False,
    }
    return _mapper_said(mad, kind=kind)


def agg_schema(*, title, credential_type, element_props, element_required,
               has_edge=True, has_rule=True, kind=Kinds.json):
    """Schema for an ACDC carrying an `A` (Aggregate) section.

    The `A` field is typed as oneOf [AGID string, array] -- the array's own
    element shape is intentionally left permissive (`items: {"type": "object"}`
    plus the string-form AGID-list elements for undisclosed members) since the
    whole point of an Aggregate section is that elements are independently
    typed by the issuer's own anyOf, not by one fixed schema per element.
    """
    props = dict(_BASE_PROPS)
    props["A"] = {
        "description": "Aggregate Section",
        "oneOf": [
            {"description": "Aggregate Section AGID", "type": "string"},
            {"description": "Uncompacted Aggregate Section", "type": "array"},
        ],
    }
    required = ["v", "d", "i", "s", "A"]
    if has_edge:
        props["e"] = _LOOSE_EDGE
    if has_rule:
        props["r"] = _LOOSE_RULE

    mad = {
        "$id": "",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "description": f"Schema for {title}.",
        "credentialType": credential_type,
        "version": "2.0.0",
        "type": "object",
        "required": required,
        "properties": props,
        "additionalProperties": False,
    }
    return _mapper_said(mad, kind=kind)
