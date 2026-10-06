"""A teen's guardian-authorized presentation under Utah SEDI, disclosed as little as possible.

Built 2026-10-06 at Daniel's request. The graph is keripy's own worked example,
tests/acdc/test_ward_authz_presentation.py on branch feat-indep-registry-bulk-issuance:
seventeen-year-old Cara Carver presents to a social platform (here "SocialWeb") an
authorization her custodial parent Bob Carver issued her. The four durable credentials are
built by CALLING that module's builders, so their schemas, AIDs, values, nonces and SAIDs are
keripy's, not a re-typing of them. Two things are ours, both approved by Daniel:

  1. AN AGE CREDENTIAL FOR CARA. keripy's ward graph has none, although the platform must
     identify her as a minor. The schema is the Age Threshold Credential of the sibling module
     tests/acdc/test_bulk_issuance_precreated_registry.py (flags for 13, 16, 18, 21, 55, 65 as
     an aggregate), issued by the State to Cara, with that schema's E1E `identity` edge to her
     Ward Citizen credential.
  2. THE PRESENTATION. keripy's Ward Presentation schema allows one edge, `authz`, and a rules
     section that is a bare SAID. Ours adds an `age` edge (I2I: Cara issues the presentation and
     is the age credential's issuee), and carries the bespoke-ACDC rules of
     tests/acdc/test_cp_disclosure.py -- Purpose, Assimilation and SafeHarbor -- with the
     Assimilation and SafeHarbor text verbatim and the Purpose clause rewritten for this
     exchange. The schema is keripy's with those two changes, re-SAIDed.

THE DISCLOSURE. Every credential is written in the form SocialWeb receives, chosen to reveal as
little as possible about Cara or Bob while still letting the platform run the checks keripy's
_verify_authz_chain runs. Each fixture's .expanded.json is the full credential.

  presentation     whole: it is the envelope, and its rules are terms SocialWeb must read.
  AuthZ Social     whole: the routes, capabilities and window are what is being exercised.
  age              the issuee and the over-18 flag only. Over-18 false entails over-21, -55 and
                   -65 false; it says nothing about 13 or 16, whose labels stay hidden.
  Ward Citizen     the issuee only; name, dob and residence are withheld as block SAIDs.
  Digital Guardian whole, because its attribute section is flat and cannot be split. This is
                   the residual leak keripy itself records: `expiryDate` 2027-04-10 is Cara's
                   18th birthday, so it gives away her birth month and day.
  Bob's Citizen    the issuee only.
"""

import importlib
import json
import sys
from pathlib import Path

from keri.acdc.messaging import acdcmap
from keri.core import Aggor, Diger
from keri.core.coring import Kinds

from .. import determinism as det
from ..common import fully_expand, make_registry
from ..registry import fixture

KERIPY = Path.home() / "code" / "wot" / "keripy"
KIND = Kinds.json


def _keripy(module):
    if str(KERIPY) not in sys.path:
        sys.path.insert(0, str(KERIPY))
    return importlib.import_module(f"tests.acdc.{module}")


def _ward():
    return _keripy("test_ward_authz_presentation")


def _precreated():
    return _keripy("test_bulk_issuance_precreated_registry")


def _cp():
    return _keripy("test_cp_disclosure")


def _graph():
    """keripy's four durable credentials, built by keripy (see the module docstring)."""
    return _ward()._credential_graph(KIND)


def _rebuild(acdc, attribute):
    """acdc, re-issued in the form that carries `attribute`. keripy's own _disclose leaves every
    nested `d` as an empty placeholder (see common.py's note on compactify); here each section is
    run through fully_expand, so every nested SAID is real. The ACDC's SAID is computed over its
    most compact form, so it is unchanged by which form is disclosed, and that is asserted."""
    sad = json.loads(json.dumps(acdc.sad))
    schema = sad['s']['$id'] if isinstance(sad['s'], dict) else sad['s']
    out = acdcmap(israid=sad['i'], uuid=sad.get('u'), regid=sad.get('rd'), schema=schema,
                  attribute=fully_expand(json.loads(json.dumps(attribute))),
                  edge=fully_expand(sad['e']) if isinstance(sad.get('e'), dict) else sad.get('e'),
                  rule=fully_expand(sad['r']) if isinstance(sad.get('r'), dict) else sad.get('r'),
                  kind=KIND)
    assert out.said == acdc.said, f"disclosure changed the SAID of {acdc.said}"
    return out


def _issuee_only(acdc):
    return _rebuild(acdc, _ward()._issuee_only_attributes(acdc, KIND))


def _whole(acdc):
    return _rebuild(acdc, acdc.sad['a'])


_expanded = _whole


def _meta(title, summary):
    return {"title": title, "summary": summary, "matrix_cells": [], "rules_exercised": []}


@fixture("sedi_bob_citizen")
def build_sedi_bob_citizen(corpus_dir):
    citizen, _, _, _ = _graph()
    return {"serder": _issuee_only(citizen), "expanded": _expanded(citizen).sad,
            "meta": _meta("SEDI: Bob Carver's Citizen credential (issuee only)",
                          "State -> Bob, keripy's 'SEDI Citizen Credential'. Disclosed with only "
                          "its issuee; name, dob and residence travel as block SAIDs.")}


@fixture("sedi_guardian")
def build_sedi_guardian(corpus_dir):
    _, guardian, _, _ = _graph()
    return {"serder": _whole(guardian),
            "meta": _meta("SEDI: Digital Guardian (Bob for Cara), disclosed whole",
                          "State -> Bob, keripy's 'SEDI Digital Guardian'. Flat, so disclosed "
                          "whole: ward, basis, scope, powers, fiduciary, effective and expiry "
                          "dates. The expiry is Cara's 18th birthday, keripy's recorded "
                          "residual leak. E1E edge to Bob's Citizen credential.")}


@fixture("sedi_cara_citizen")
def build_sedi_cara_citizen(corpus_dir):
    _, _, ward, _ = _graph()
    return {"serder": _issuee_only(ward), "expanded": _expanded(ward).sad,
            "meta": _meta("SEDI: Cara Carver's Ward Citizen credential (issuee only)",
                          "State -> Cara, keripy's 'SEDI Ward Citizen Credential', encumbered by "
                          "its NI2I edge to the guardianship. Disclosed with only its issuee.")}


@fixture("sedi_authz")
def build_sedi_authz(corpus_dir):
    _, _, _, authz = _graph()
    return {"serder": _whole(authz),
            "meta": _meta("SEDI: Ward AuthZ Social (Bob -> Cara), disclosed whole",
                          "keripy's 'Ward AuthZ Social', in Bob's own registry: social_feed read, "
                          "social_posts read+post, social_dm read+message, 16:00-20:00 "
                          "America/Denver from 2026-08-01 to 2026-11-30. I2I authority edge to "
                          "the guardianship, E1E subject edge to Cara's Ward Citizen credential.")}


# The age credential: ours (see the module docstring), in keripy's precreated module's schema.
CARA_AGE = 17   # keripy's own CARA_AGE; dob 2009-04-10 at the 2026-08-03 presentation


def _age_ael(issuee):
    p = _precreated()
    ael = ["", dict(d='', u=det.nonce("sedi_age:issuee"), i=issuee)]
    for n in p.AGE_THRESHOLDS:
        ael.append(dict(d='', u=det.nonce(f"sedi_age:over{n}"), **{f"over{n}": CARA_AGE >= n}))
    return ael


def _age(disclosed: bool):
    w, p = _ward(), _precreated()
    _, _, ward, _ = _graph()
    schema_said, _ = p._saidify_schema(dict(p.AGE_SCHEMA_MAD), kind=KIND)
    aggor = Aggor(ael=_age_ael(w.CARA), makify=True, kind=KIND)
    if disclosed:
        over18 = 2 + p.AGE_THRESHOLDS.index(18)
        aggregate, _ = aggor.disclose(indices=[1, over18])
    else:
        aggregate = aggor.ael
    edge = fully_expand(dict(d='', u=det.nonce("sedi_age:e"),
                             identity=dict(d='', u=det.nonce("sedi_age:e:identity"),
                                           n=ward.said, s=ward.sad['s']['$id'], o='E1E')))
    return acdcmap(israid=w.STATE, uuid=det.nonce("sedi_age:u"),
                   regid=make_registry("sedi_age", w.STATE).said, schema=schema_said,
                   aggregate=aggregate, edge=edge, kind=KIND), aggor


@fixture("sedi_age")
def build_sedi_age(corpus_dir):
    serder, aggor = _age(disclosed=True)
    return {"serder": serder,
            "expanded": {"aggregate_elements": aggor.ael, "agid": aggor.agid},
            "meta": _meta("SEDI: Cara's Age Threshold credential (over-18 only)",
                          "Not in keripy's ward graph; added at Daniel's request. Schema is the "
                          "precreated-registry module's Age Threshold Credential, issued by the "
                          "State to Cara, E1E identity edge to her Ward Citizen credential. "
                          "Discloses the issuee and over18=false only.")}


PURPOSE_TEXT = ("One-time verification by the Verifier that the Discloser is a minor acting "
                "under the guardian authorization referenced by the edge section, for the sole "
                "purpose of applying the account changes that authorization permits.")


def _presentation_schema():
    w = _ward()
    mad = json.loads(json.dumps(w.PRESENTATION_SCHEMA_MAD))
    mad["description"] += (" arcviz variant: adds an I2I `age` edge to the ward's age "
                           "credential, and a rules section of Purpose, Assimilation and "
                           "SafeHarbor clauses after tests/acdc/test_cp_disclosure.py.")
    edges = mad["properties"]["e"]["oneOf"][1]
    edges["required"] = ["d", "authz", "age"]
    edges["properties"]["age"] = w._edge_schema("I2I", "the ward is the subject of this age "
                                                       "credential")
    mad["properties"]["r"] = {"description": "Bespoke rules: Purpose, Assimilation, SafeHarbor",
                              "oneOf": [{"type": "string"}, {"type": "object"}]}
    return w._saidify_schema(mad, kind=KIND)[0]


@fixture("sedi_presentation", depends_on=["sedi_age"])
def build_sedi_presentation(corpus_dir):
    w, cp = _ward(), _cp()
    _, _, _, authz = _graph()
    age, _ = _age(disclosed=False)
    edge = dict(d='', u=det.nonce("sedi_presentation:e"),
                authz=dict(d='', u=det.nonce("sedi_presentation:e:authz"), n=authz.said,
                           s=authz.sad['s']['$id'], o='I2I'),
                age=dict(d='', u=det.nonce("sedi_presentation:e:age"), n=age.said,
                         s=age.sad['s'], o='I2I'))
    rule = dict(d='', Purpose=dict(d='', l=PURPOSE_TEXT),
                Assimilation=dict(d='', l=cp.ASSIMILATION_TEXT),
                SafeHarbor=dict(d='', l=cp.SAFE_HARBOR_TEXT))
    attr = w._presentation_attr()
    attr = {"d": attr.pop("d"), "u": attr.pop("u"), "i": w.SOCIAL, **attr}
    serder = acdcmap(israid=w.CARA, uuid=det.nonce("sedi_presentation:u"),
                     schema=_presentation_schema(), attribute=fully_expand(attr),
                     edge=fully_expand(edge), rule=fully_expand(rule), kind=KIND)
    return {"serder": serder,
            "meta": _meta("SEDI: Cara's presentation to SocialWeb",
                          "The DAG's origin, issued by Cara to SocialWeb, one-time and not "
                          "registry-bound. keripy's Ward Presentation plus an I2I age edge and "
                          "the Purpose / Assimilation / SafeHarbor rules of test_cp_disclosure.py "
                          "(SafeHarbor cites Utah Code 63A-20-701 and -801).")}
