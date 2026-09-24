#!/usr/bin/env python3
"""A deterministic credential classifier, run against the 195-row catalog.

The point of this file is to be TESTABLE, not to be right. It encodes one candidate scheme as
ordered, explicit predicates over inputs a real implementation would actually have -- the field
names a SAID-verified schema declares, and a few structural facts about the payload -- and then
`evaluate.py` measures where it succeeds, where it falls through, and where it cannot see enough
to answer at all. Every rule here is a synthesized proposal. None of it is ratified.

Two stages, and the separation is the whole design:

  GENUS   a structural spine of three forks, producing exactly one value per credential. Its job
          is not to name the kind; it is to say whether the viewer's default assumption -- that
          this is evidence about the person presenting it -- holds.

  DOMAIN  a flat pass that returns zero, one or several familiar labels. Bundling lives here on
          purpose, because a driver's licence is an identity document AND a licence and no
          precedence rule makes that untrue.

Inputs come from rows.json, which was extracted from the sources without reference to any
category, so that this file is tested rather than confirmed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------------
# Field vocabularies. Each is a set of regexes matched against a field name, lowercased. They are
# deliberately written against names that actually occur in the catalog's sources rather than
# against names a classifier might wish for.
# --------------------------------------------------------------------------------------------

def _rx(*pats: str) -> list[re.Pattern]:
    return [re.compile(p) for p in pats]


V = {
    "identity": _rx(
        r"^(family|given|first|last)_?name", r"^name_?(given|family)", r"^namegiven$", r"^namefamily$",
        r"^registered_(family|given)_name", r"birth_?date$", r"^dob$", r"^birthdate$", r"^date_of_birth$",
        r"^portrait", r"^picture$", r"^image$", r"^facetemplate$", r"^photo$", r"^resident_image$",
        r"^place_of_birth$", r"^birth_?place", r"^nationalit", r"^sex$", r"^gender$",
        r"^document_number$", r"^personal_administrative_number$", r"^credential_holder",
        r"^family_name_(unicode|latin1)", r"^given_name_(unicode|latin1)", r"^resident_name$",
    ),
    "age": _rx(r"^age_?over", r"^ageover", r"^age_?above", r"^overage$", r"^age_in_years$", r"^age_birth_year$"),
    "financial": _rx(
        r"^iban$", r"^currency$", r"^bank", r"^national_bank_code$", r"^business_identifier_code$",
        r"^payment", r"^card", r"^masked_account_reference$", r"^tax_?number$", r"^taxpayer_type$",
        r"^church_tax_id$", r"^monetarylimit$", r"^c_upto$", r"^balance$", r"^last four digits$",
        r"^credential id$", r"^card network$", r"^payment_instrument_id$",
    ),
    "academic": _rx(
        r"degree", r"transcript", r"^achievement", r"^learning", r"^course", r"grade", r"^alumniof$",
        r"diploma", r"^scoped_affiliation$", r"^home_organization$", r"^primary_affiliation$",
        r"^affiliations$", r"^expected_study_time$", r"^level_of_learning_experience$",
        r"^prerequisites_to_enroll$", r"^criteria", r"^assessment",
    ),
    "licence": _rx(
        r"licen[cs]e", r"^driving_privileges$", r"^domestic_driving_privileges$", r"^capacities$",
        r"^stcw_code$", r"^certification", r"^board", r"^privileges$", r"^loa$", r"^score$",
        r"^vettingscore$", r"^effective_dt$", r"^expire_dt$", r"^authorisation number$",
        r"^licensed roles$",
    ),
    "health": _rx(
        r"^health", r"^patient", r"vaccinat", r"^social_security_pin$", r"^competent_institution$",
        r"^1d47_vaccinated$", r"^ra01", r"prescription", r"^micov",
    ),
    "employment": _rx(
        r"^employe", r"^employment", r"^officialrole$", r"^engagementcontextrole$", r"^role$",
        r"^places_of_work$", r"^legislation$", r"^issuer_name$", r"^employer",
    ),
    "telecom": _rx(r"^phone", r"^msisdn$", r"^numbers$", r"^telephone", r"^mobile_operator$", r"^contract_owner$",
                   r"^end_user$", r"^rangestart$", r"^rangeend$", r"^donotoriginate$", r"^channel$"),
    "residence": _rx(r"^resident_", r"^residence", r"^address", r"^arrival_date$", r"^postal", r"^locality$"),
    "membership": _rx(r"^membership", r"^loyalty", r"^client_id$", r"^tier$", r"^company$", r"^merchant"),
    "civil_status": _rx(r"^parent", r"^spouse$", r"^maidenname$", r"^naturalization", r"^citizenship$",
                        r"^marital", r"^lprcategory$", r"^lprnumber$", r"^residentsince$", r"^ward$"),
    "authority": _rx(
        r"^c_goal", r"^c_proto", r"^constraints$", r"^goals$", r"^facet$", r"^gfw$", r"^powers$",
        r"^full_powers$", r"^eservice$", r"^legal_person_identifier$", r"^terminatingevents$",
        r"^disclosables$", r"^fiduciary$", r"^recognition$", r"^delegat", r"^licensevalue$",
        r"^extendscredential$", r"^authorizedserviceprovider$",
    ),
    # `^biometric` was here and is narrowed: an mDL carries `biometric_template_xx` as an identity
    # element, which is not a claim that the holder is a human being. `ongoing` and `minutes` are
    # dropped as too generic to carry the claim on their own.
    "humanness": _rx(r"^biometrichashes$", r"^biometricprotocol$", r"^knownas$", r"^firstmet$",
                     r"^lastinteraction$", r"^modalities$", r"^personhood"),
    "brand": _rx(r"^brand", r"^logo", r"^vcard$", r"^wordmark$"),
    # `issuing_organization` was here and is removed: it names the ISSUER, not an organization the
    # credential is about, and it appears in the EU IBAN and MSISDN attestations about individuals.
    "org_identity": _rx(r"^lei$", r"^legalcompany", r"^lids$", r"^legal_name$", r"^taxid$", r"^partygln$",
                        r"^organizationname$", r"^graceperiod$"),
    # Non-party vocabularies.
    # `typ`, `siz` and `loc` were in this list and are removed: they are generic enough to match a
    # citation, whose subject is external content rather than a thing the credential is about.
    "thing": _rx(r"^vin$", r"^registration_", r"^basic_vehicle_info$", r"^gtin", r"^res$",
                 r"^art_digest$", r"^content_", r"^digest$", r"^filename$",
                 r"^provenance$", r"^uses$", r"^des$", r"^lbl$", r"^sdt$"),
    "bearer": _rx(r"ticket", r"coupon", r"^offer", r"voucher", r"^redemption", r"^seat", r"^barcode",
                  r"^admission", r"^movie$", r"^cinema$", r"^theater_id$", r"^parking_option$",
                  r"^poster$", r"^smarttapredemptionvalue$", r"^rotatingbarcode$"),
    "occurrence": _rx(r"^occurredat$", r"^venue$", r"^check_in_date$", r"^check_out_date$", r"^guests$",
                      r"^show_date_time$", r"^seat", r"^flight", r"^departure", r"^reservation_",
                      r"^booking_", r"^assembly_dt$", r"^evt_dt$", r"^evt_loc$", r"^transitType$",
                      r"^num_of_rooms$", r"^car_rental$"),
    # `be` was in this list and is removed: it is proof-of-control's "bits of entropy in the
    # challenge", and matching it classified a credential about a person as machinery. `pubkey`
    # moved here from "thing", because a key-binding attestation is about a key.
    "apparatus": _rx(r"^wallet", r"^keystore$", r"^wscd$", r"^attested_keys$", r"^pseudonym$",
                     r"^registered_attributes$", r"^pubkey$"),
    "evidence_ref": _rx(r"^said$", r"^disp$", r"^act$", r"^qp$", r"^ref$", r"^statuslist", r"^encodedlist$",
                        r"^recognizedto$", r"^recognizedin$", r"^disputedclaim$", r"^currentstatus$",
                        r"^evd$", r"^assertion$", r"^credentialschema$", r"^targetdigest$", r"^target$"),
}


def hits(fields: list[str], key: str) -> list[str]:
    """Every field name matching vocabulary `key`. Returned rather than counted so a failure can be read."""
    out = []
    for f in fields:
        low = f.lower().strip("`")
        if any(rx.search(low) for rx in V[key]):
            out.append(f)
    return out


def has(fields: list[str], key: str) -> bool:
    return bool(hits(fields, key))


# --------------------------------------------------------------------------------------------
# Stage 1 -- the structural spine. Ordered; first match wins; exactly one value is always returned.
# --------------------------------------------------------------------------------------------

GENUS_VALUES = [
    "ASSEMBLY",       # the payload points at other evidence rather than at the world
    "APPARATUS",      # the subject is the machinery that makes other evidence usable
    "ABOUT_A_THING",
    "ABOUT_AN_OCCURRENCE",
    "BEARER",         # possession is the whole binding; there is no subject
    "SELF",           # issuer and subject are the same party
    "INVERTED",       # the subject is the verifier
    "ABOUT_ANOTHER_PARTY",
    "ORDINARY",       # evidence about the party presenting it -- the unmarked default
    "UNDECIDABLE",    # the inputs do not contain enough to answer
]


# Housekeeping field names carry no claim of their own: an ACDC block SAID, its salty nonce, the
# issuee AID, the issuance timestamp. A payload consisting only of these plus assembly metadata is
# a payload that asserts nothing about the world -- which is what a dossier looks like.
HOUSEKEEPING = {"d", "u", "i", "dt", "ri", "rd", "s", "v", "e", "a", "r"}
ASSEMBLY_META = _rx(
    r"^assembl", r"^assemble_dt$", r"^purpose$", r"^gov", r"^evt_", r"^jur$", r"^cls$", r"^class$",
    r"^phase$", r"^fi$", r"^ref$", r"^name$", r"^said$", r"^act$", r"^disp$", r"^reason$",
)


def _substantive(fields: list[str]) -> list[str]:
    """Field names that make a claim about the world, as opposed to housekeeping or assembly metadata."""
    out = []
    for f in fields:
        low = f.lower().strip("`")
        if low in HOUSEKEEPING:
            continue
        if any(rx.search(low) for rx in ASSEMBLY_META):
            continue
        out.append(f)
    return out


def genus(row: dict, *, safe_default: bool = True, narrow_assembly: bool = True) -> tuple[str, str]:
    """Return (value, why). `why` names the rule that fired, so a wrong answer is traceable.

    The two keyword arguments are the variants the evaluation reports side by side.

    `safe_default` decides what to do when a credential declares an issuee and publishes no field
    list. Answering ORDINARY is the tempting choice and it is the unsafe one: it renders a wallet
    attestation, a device credential or a relying party's own registration certificate as though it
    were evidence about the person presenting it, silently and in the one direction that matters.
    With `safe_default` on, the classifier declines instead.

    `narrow_assembly` decides what counts as evidence-about-evidence. Referencing another credential
    is not enough -- nearly every ACDC has edges, and a guardianship credential names its ward by
    edge while being ordinary evidence about the guardian. Narrowed, ASSEMBLY requires that the
    payload make no substantive claim of its OWN.
    """
    f = row.get("fields") or []
    st = row.get("structure") or {}
    known = row.get("fields_known", False)
    refs_other = st.get("names_other_credential") is True
    own_claim = bool(_substantive(f)) if known else None

    # Fork 1 -- does the payload point at other evidence INSTEAD OF at the world?
    if refs_other:
        if not narrow_assembly:
            return "ASSEMBLY", "names_other_credential"
        if own_claim is False:
            return "ASSEMBLY", "references other evidence and makes no substantive claim of its own"
        if own_claim is None:
            return "UNDECIDABLE", "references other evidence, but no field list to say whether it also claims something itself"
    if known and has(f, "evidence_ref") and not _substantive_beyond(f, "evidence_ref"):
        return "ASSEMBLY", f"payload is only evidence references {hits(f, 'evidence_ref')}"

    # Fork 2 -- is the subject the machinery itself?
    if known and has(f, "apparatus"):
        return "APPARATUS", f"apparatus fields {hits(f, 'apparatus')}"

    # Fork 3 -- is there a subject party, and how do issuer, holder and subject line up?
    issuee = st.get("has_issuee")

    if issuee is False:
        if not known:
            return "UNDECIDABLE", "no issuee, and no field list to say what it is about"
        # A credential with no issuee may still be about its issuer -- a self-attestation.
        if has(f, "humanness") or has(f, "org_identity") or has(f, "identity"):
            return "SELF", f"no issuee but party attributes present {hits(f, 'identity') + hits(f, 'org_identity')}"
        if has(f, "thing"):
            return "ABOUT_A_THING", f"thing fields {hits(f, 'thing')}"
        if has(f, "occurrence"):
            return "ABOUT_AN_OCCURRENCE", f"occurrence fields {hits(f, 'occurrence')}"
        return "BEARER", "no issuee and no subject vocabulary matched"

    if issuee is True:
        if not known:
            if safe_default:
                return "UNDECIDABLE", "issuee declared but no field list; declining rather than assuming ordinary"
            return "ORDINARY", "issuee declared; no fields, so the default applies"
        if has(f, "thing") and not has(f, "identity"):
            return "ABOUT_A_THING", f"issuee declared but the payload is about a thing {hits(f, 'thing')}"
        return "ORDINARY", "issuee declared and the payload is about a party"

    return "UNDECIDABLE", "the source does not say whether there is an issuee"


def _substantive_beyond(fields: list[str], key: str) -> bool:
    """True when the payload carries a substantive claim that is NOT matched by vocabulary `key`."""
    refs = set(hits(fields, key))
    return any(x not in refs for x in _substantive(fields))


# --------------------------------------------------------------------------------------------
# Stage 1b -- the same structural question, split into the TWO axes the single spine was
# conflating. The evaluation showed the conflation directly: a key-binding attestation is a
# self-attestation AND its subject is a key, and a single-valued spine has to discard one of those
# facts. `BindKeyAttestation`, `ai-user-coca` and `orgVet` all failed for that reason and not
# because any rule was wrong about them.
#
#   SUBJECT    what the credential is about. One value, always.
#   ALIGNMENT  how issuer, holder and subject line up. One value, always; NOT_A_PARTY when the
#              subject is not a party at all, which is a real answer rather than a gap.
#
# Each is MECE on its own. Neither is MECE jointly with the other, which is the point.
# --------------------------------------------------------------------------------------------

SUBJECT_VALUES = ["party", "thing", "occurrence", "evidence", "apparatus", "agent", "none", "unknown"]
ALIGNMENT_VALUES = ["ordinary", "self-attested", "other-party", "inverted", "not-a-party", "unknown"]


def subject_axis(row: dict) -> tuple[str, str]:
    f = row.get("fields") or []
    st = row.get("structure") or {}
    known = row.get("fields_known", False)
    own_claim = bool(_substantive(f)) if known else None

    if st.get("names_other_credential") is True and own_claim is False:
        return "evidence", "references other evidence and claims nothing itself"
    if known and has(f, "evidence_ref") and not _substantive_beyond(f, "evidence_ref"):
        return "evidence", f"payload is only evidence references {hits(f, 'evidence_ref')}"
    if not known:
        if st.get("names_other_credential") is True:
            return "unknown", "references other evidence, but no field list to say whether it also claims something itself"
        return "unknown", "no field list"
    if has(f, "apparatus"):
        return "apparatus", f"apparatus fields {hits(f, 'apparatus')}"
    if has(f, "identity") or has(f, "org_identity") or has(f, "humanness"):
        return "party", f"party attributes {(hits(f, 'identity') + hits(f, 'org_identity') + hits(f, 'humanness'))[:4]}"
    # A declared issuee outranks object vocabulary. A proof-of-control credential names a resource
    # and is about the PARTY who controls it; a telephone-allocation credential names a number range
    # and is about the party holding the right. The object is what the claim is made WITH, not what
    # the claim is ABOUT. Only a credential with no issuee at all is about the object itself.
    if st.get("has_issuee") is True:
        return "party", "an issuee is declared, so the payload's objects are what is claimed about them"
    if has(f, "thing"):
        return "thing", f"thing fields {hits(f, 'thing')}"
    if has(f, "bearer"):
        return "none", f"bearer fields {hits(f, 'bearer')}"
    if has(f, "occurrence"):
        return "occurrence", f"occurrence fields {hits(f, 'occurrence')}"
    return "unknown", "no subject vocabulary matched and no issuee declared"


def alignment_axis(row: dict) -> tuple[str, str]:
    st = row.get("structure") or {}
    subj, _ = subject_axis(row)
    if subj == "unknown":
        # Answering "ordinary" here is the unsafe default in a second disguise: it would assert that
        # the credential is about the party presenting it, on no evidence beyond an issuee existing.
        return "unknown", "the subject is unknown, so how it aligns with the holder is unknown too"
    if subj in ("thing", "occurrence", "evidence", "apparatus", "none"):
        return "not-a-party", f"subject is {subj}"
    issuee = st.get("has_issuee")
    if issuee is False and subj == "party":
        # No issuee, yet the payload carries party attributes: the party is the issuer.
        return "self-attested", "party attributes present with no issuee declared"
    if issuee is True:
        return "ordinary", "an issuee is declared"
    return "unknown", "the source does not say whether there is an issuee"


# --------------------------------------------------------------------------------------------
# Stage 2 -- the domain pass. Zero, one or several labels. Never exclusive.
# --------------------------------------------------------------------------------------------

# The nine categories, lower-kebab, as settled on 2026-09-23. Each maps to one or more of the
# field vocabularies above; the merges are recorded in docs/design/credential-categories.md and
# each one has a reason from the corpus rather than from tidiness.
CATEGORIES = [
    "org-identity",   # who an organization is
    "identity",       # who a natural person is -- absorbs age, residence and travel
    "humanness",      # that a party is a real person, without saying which person
    "financial",
    "qualification",  # absorbs academic, licence and award
    "health",
    "affiliation",    # absorbs employment, membership and relationship
    "authority",      # absorbs telecom rights, brand rights and proof of control
    "civil-status",
]

CATEGORY_VOCAB = {
    "org-identity": ["org_identity"],
    "identity": ["identity", "age", "residence"],
    "humanness": ["humanness"],
    "financial": ["financial"],
    "qualification": ["academic", "licence"],
    "health": ["health"],
    "affiliation": ["employment", "membership"],
    "authority": ["authority", "telecom", "brand"],
    "civil-status": ["civil_status"],
}

RESIDUAL = "misc"


# A bare `account` is money only when the credential also carries money. Daniel, 2026-09-24,
# after a witness statement's `account` (of what happened) was classified financial: "our
# classifier should only match that field name to money if it can find a field of type floating
# point and/or a field with an ISO currency code or a common currency symbol in it. Otherwise
# this is just as likely to be a user account." Anchored names that are unambiguously financial
# (`masked_account_reference`, `iban`, ...) stay in the vocabulary above and need no support.
ACCOUNT = re.compile(r"account")

# A SUBSET of ISO 4217, the codes in common use; extend it rather than trusting it as complete.
ISO_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "CNY", "CHF", "CAD", "AUD", "NZD", "HKD", "SGD", "SEK", "NOK",
    "DKK", "PLN", "CZK", "HUF", "RON", "BGN", "TRY", "RUB", "UAH", "INR", "PKR", "BDT", "KRW",
    "IDR", "MYR", "THB", "VND", "PHP", "ILS", "AED", "SAR", "QAR", "EGP", "NGN", "KES", "ZAR",
    "BRL", "MXN", "ARS", "CLP", "COP", "PEN",
}
CURRENCY_SYMBOLS = "$€£¥₹₩₽₺₪฿₫₴₦₱"


def money_evidence(row: dict) -> list[str]:
    """Fields that show the credential carries money, from the only two inputs that can say so:
    a declared JSON Schema type (`field_types`: name -> type) and disclosed values (`values`:
    name -> value). Either may be absent, and the catalog rows carry neither, so a bare
    `account` there never counts as financial."""
    out = []
    for name, typ in (row.get("field_types") or {}).items():
        if typ == "number" or (isinstance(typ, list) and "number" in typ):
            out.append(name)
    for name, val in (row.get("values") or {}).items():
        if isinstance(val, float):
            out.append(name)
        elif isinstance(val, str):
            v = val.strip()
            if v.upper() in ISO_CURRENCIES and v.isupper() or any(ch in CURRENCY_SYMBOLS for ch in v):
                out.append(name)
    return sorted(set(out))


def category_evidence(row: dict) -> dict[str, list[str]]:
    """Category -> the field names that put it there. The reasons, so a render can show them."""
    f = row.get("fields") or []
    if not row.get("fields_known", False):
        return {}
    out = {c: sorted({h for v in CATEGORY_VOCAB[c] for h in hits(f, v)}) for c in CATEGORIES}
    accounts = [x for x in f if ACCOUNT.search(x.lower().strip("`"))]
    money = money_evidence(row) if accounts else []
    if money:
        out["financial"] = sorted(set(out["financial"]) | set(accounts) | set(money))
    return {c: v for c, v in out.items() if v}


def categories(row: dict) -> list[str]:
    """Zero, one or several categories. Never exclusive -- a driving licence is two of them.

    Ordering is meaningful rather than alphabetical: the first element is the one a single-glyph
    rendering should use. `identity` is demoted whenever it co-occurs, because identity attributes
    are the substrate nearly every credential is built on and are therefore the least informative
    label a credential can carry (F-HZ5X, and the precision measurement in CLASSIFIER.md).
    """
    ev = category_evidence(row)
    out = [c for c in CATEGORIES if c in ev]
    if "identity" in out and len(out) > 1:
        out = [c for c in out if c != "identity"] + ["identity"]
    return out


def domains(row: dict) -> list[str]:
    """Deprecated alias kept so the older evaluation scripts still run."""
    return categories(row)


def classify(row: dict) -> dict:
    g, why = genus(row)
    return {"id": row["id"], "name": row["name"], "genus": g, "why": why, "domains": domains(row)}


def main() -> int:
    rows = json.loads((HERE / "rows.json").read_text())
    out = [classify(r) for r in rows]
    json.dump(out, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
