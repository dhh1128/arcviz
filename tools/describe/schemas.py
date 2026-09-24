"""Resolve a schema SAID to what the type already implies. Four states, none of them silent.

WHY THIS EXISTS. The describe algorithm needs to know what a TYPE entails, because a datum the
type already implies carries no information. The vLEI chain is the proof: across all four
credentials the party relation is fixed by the schema -- a Legal Entity vLEI Credential is
"issued by a Qualified vLEI issuer to a Legal Entity", and its schema says so in the
descriptions of its own `i` and `a.i` properties -- so a descriptor reading "from the QVI to
the legal entity" restates the type in longer words. Without the schema the algorithm cannot
know that and emits the redundancy. With it, it can.

THE REGISTRY IS A HINT, NOT A TRUST ANCHOR, and that is what makes fetching from a stranger
acceptable. A schema is content-addressed, so a fetched document can be checked against the
SAID that was asked for. A hostile source cannot substitute a different schema; the worst it
can do is decline to answer, or learn that somebody asked.

THAT SECOND ONE IS A REAL COST. Asking a host for schema X tells it somebody is looking at a
credential of that type, which is a correlation vector. So resolution is OFF unless a caller
passes a fetcher, and answers are cached forever -- a content-addressed document cannot change,
which is a rare case where "cache forever" is correct rather than lazy.

ON VERIFICATION, AND WHAT IS NOT IMPLEMENTED HERE. Real verification recomputes the SAID:
dummy out the `$id`, serialise exactly as the issuer did, digest, compare. That needs blake3
and a byte-exact serialiser, and this module is deliberately dependency-free because it is
renderer-side. So a document whose self-declared `$id` matches is recorded as UNVERIFIED, not
as verified, and callers are told the difference. An unverified schema may lend a display name
-- marked as unverified provenance per P12 -- and may NOT be relied on for entailments, because
a schema that understates what a type implies would make the algorithm say too much. Supplying
`digest=` switches on real verification.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

VERIFIED = "verified"
UNVERIFIED = "unverified"
UNAVAILABLE = "unavailable"
MISMATCH = "mismatch"

REGISTRY = Path(__file__).resolve().parents[2] / "refs" / "schema-registry.json"


@dataclass
class SchemaInfo:
    """What is known about one type, and how well it is known."""
    said: str
    state: str = UNAVAILABLE
    title: str | None = None
    short: str | None = None
    issuer_role: str | None = None
    issuee_role: str | None = None
    # Channels the TYPE already fixes, so naming them per-node says nothing. This is the input
    # the surprisal criterion was missing.
    entailed: tuple = ()
    source: str | None = None

    @property
    def trustworthy(self) -> bool:
        """Whether entailments may be acted on. A title is cosmetic; an entailment is not.

        Acting on an entailment SUPPRESSES a component, so a wrong one makes the label say
        less than it should -- an omission, which is the direction this project treats as
        dangerous. A wrong title is visible and merely wrong.
        """
        return self.state == VERIFIED


def load_registry(path: Path | None = None) -> dict:
    return json.loads((path or REGISTRY).read_text())


def resolve(said: str, *, registry: dict | None = None, fetch=None, digest=None,
            cache: dict | None = None) -> SchemaInfo:
    """Resolve one schema SAID.

    `fetch(said, source)` returns the document text or None; omit it and nothing is requested
    from the network, which is the default because asking is itself a disclosure. `digest(doc)`
    returns the SAID of a document; omit it and a matching self-declared `$id` yields
    UNVERIFIED rather than VERIFIED.
    """
    registry = registry if registry is not None else load_registry()
    if cache is not None and said in cache:
        return cache[said]

    known = (registry.get("known_schemas") or {}).get(said)
    if known:
        info = SchemaInfo(
            said=said, state=VERIFIED, title=known.get("title"), short=known.get("short"),
            issuer_role=known.get("issuer_role"), issuee_role=known.get("issuee_role"),
            entailed=tuple(known.get("entailed") or ()), source="registry:known_schemas")
        if cache is not None:
            cache[said] = info
        return info

    info = SchemaInfo(said=said)
    if fetch is not None:
        for src in registry.get("sources") or []:
            doc = fetch(said, src)
            if not doc:
                continue
            try:
                parsed = json.loads(doc)
            except Exception:
                continue
            if digest is not None:
                computed = digest(doc)
                if computed != said:
                    # Never cached, never fallen back from. A document that does not digest to
                    # the SAID asked for is an answer about a DIFFERENT schema at best.
                    return SchemaInfo(said=said, state=MISMATCH, source=src.get("id"))
                state = VERIFIED
            else:
                if parsed.get("$id") != said:
                    continue
                state = UNVERIFIED
            info = SchemaInfo(
                said=said, state=state, title=parsed.get("title"),
                short=None, source=src.get("id"),
                issuer_role=_role_of(parsed, "i"), issuee_role=_role_of(parsed, "a.i"),
                entailed=("issuer", "issuee") if state == VERIFIED and
                _role_of(parsed, "i") and _role_of(parsed, "a.i") else ())
            break

    if cache is not None and info.state != MISMATCH:
        cache[said] = info
    return info


def _role_of(schema: dict, path: str):
    """The role a schema assigns to a party slot, read from its own property description.

    The real vLEI schemas describe `i` as 'QVI Issuer AID' and `a.i` as 'LE Issuer AID', which
    is where the entailment lives. It is prose rather than structure, so this is a reading and
    not a parse -- and `credential-categories.md` already measured that schema metadata is not
    reliably self-consistent (that same schema describes its `LEI` attribute as 'LE Issuer AID'
    too, which is plainly a copy-paste slip). Treated as a hint accordingly.
    """
    props = schema.get("properties") or {}
    if path == "i":
        node = props.get("i") or {}
    else:
        a = props.get("a") or {}
        variants = a.get("oneOf") or [a]
        node = {}
        for v in variants:
            inner = (v or {}).get("properties") or {}
            if "i" in inner:
                node = inner["i"]
                break
    d = (node.get("description") or node.get("title") or "").strip()
    return d or None
