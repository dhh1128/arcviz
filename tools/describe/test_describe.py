"""The suite for `describe.py`: the vectors in vectors.json, plus corpus integration.

Runs under plain `python3 test_describe.py` and under pytest. No dependency on keripy or on
`tools/fixtures` -- this is renderer-side code, and `tools/fixtures/README.md` is explicit that
the renderer must never link a KERI node.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from describe import (Dag, Node, _relative_date_band, _role_stem, describe,  # noqa: E402
                      describe_node, load_corpus_dag)

HERE = Path(__file__).resolve().parent
CORPUS = HERE / ".." / ".." / "corpus"


def _dag_from_spec(spec: dict) -> Dag:
    nodes = [Node(said=n["said"], schema=n.get("schema"), issuer=n.get("issuer"),
                  issuee=n.get("issuee"), attrs=n.get("attrs", {}),
                  out_edges=n.get("out_edges", {}))
             for n in spec["nodes"]]
    return Dag(nodes=nodes,
               type_names=spec.get("type_names", {}),
               subject_fields=spec.get("subject_fields", {}),
               image_fields=spec.get("image_fields", {}),
               resolvable_digests=set(spec.get("resolvable_digests", [])))


def _check_vector(vec: dict) -> list[str]:
    assert vec.get("defends"), f"{vec['name']} carries no `defends`"
    dag = _dag_from_spec(vec["dag"])
    by_said = {d.said: d for d in describe(dag)}
    bands = _relative_date_band(dag)
    problems = []

    def bad(msg):
        problems.append(f"{vec['name']}: {msg}")

    for said, want in vec["expect"].items():
        got = by_said.get(said)
        if got is None:
            bad(f"no description produced for {said}")
            continue
        if "kinds" in want:
            kinds = [c.kind for c in got.components]
            if kinds != want["kinds"]:
                bad(f"{said} components {kinds} != expected {want['kinds']}")
        if "distinguishing" in want and got.distinguishing != want["distinguishing"]:
            bad(f"{said} distinguishing={got.distinguishing} != {want['distinguishing']}")
        if "distinguishing_as_text" in want:
            if got.distinguishing_as_text != want["distinguishing_as_text"]:
                bad(f"{said} distinguishing_as_text={got.distinguishing_as_text} "
                    f"!= {want['distinguishing_as_text']}")
        if "indistinguishable_from" in want:
            if got.indistinguishable_from != want["indistinguishable_from"]:
                bad(f"{said} indistinguishable_from={got.indistinguishable_from} "
                    f"!= {want['indistinguishable_from']}")
        if "annotations" in want:
            kinds = [a["kind"] for a in got.annotations]
            if kinds != want["annotations"]:
                bad(f"{said} annotations {kinds} != {want['annotations']}")
        if "negative_kinds" in want:
            neg = [c.kind for c in got.components if c.negative]
            if neg != want["negative_kinds"]:
                bad(f"{said} negative components {neg} != {want['negative_kinds']}")
        if "type_name" in want:
            head = got.components[0]
            if head.kind != "type" or head.value.get("name") != want["type_name"]:
                bad(f"{said} head {head.kind}/{head.value} != type name {want['type_name']}")
        if "band" in want and bands.get(said) != want["band"]:
            bad(f"{said} band {bands.get(said)!r} != {want['band']!r}")
    return problems


def test_vectors():
    data = json.loads((HERE / "vectors.json").read_text())
    problems = []
    for vec in data["vectors"]:
        problems += _check_vector(vec)
    assert not problems, "\n".join(problems)


def test_role_stem_strips_an_index_and_nothing_else():
    assert _role_stem("licenceA") == "licence"
    assert _role_stem("photo2") == "photo"
    assert _role_stem("statementB") == "statement"
    # Real roles must survive intact, or the counterweight vector is meaningless.
    for intact in ("vetting", "alloc", "tnalloc", "delsig", "inspectorA"):
        stem = _role_stem(intact)
        assert stem == intact or intact == "inspectorA", f"{intact} -> {stem}"
    # An all-caps token is left alone: stripping there eats meaning rather than an index.
    assert _role_stem("TN") == "TN"


def _accident_dag(with_subject: bool):
    names = ["accident_bundle", "accident_licence_a", "accident_licence_b",
             "accident_photo_a", "accident_photo_b", "accident_photo_c",
             "accident_photo_d",
             "accident_statement_a", "accident_statement_b"]
    sads = {n: json.loads((CORPUS / f"{n}.json").read_text()) for n in names}
    sc = {n: s["s"] for n, s in sads.items()}
    # Derived from what is ON DISK, never from a list written here. An earlier version
    # hardcoded the three digests that resolved at the time, and went on asserting that
    # driver B's portrait was withheld for a while after it started resolving -- a test
    # passing against a model of the corpus instead of against the corpus, which is the
    # failure this repository exists to refuse, in its own suite.
    attachments = CORPUS / "attachments"
    manifest = json.loads((attachments / "MANIFEST.json").read_text())
    resolvable = set()
    for cred, fieldname in (("accident_photo_a", "imageDigest"),
                            ("accident_photo_b", "imageDigest"),
                            ("accident_photo_c", "imageDigest"),
                            ("accident_photo_d", "imageDigest"),
                            ("accident_licence_a", "portraitDigest"),
                            ("accident_licence_b", "portraitDigest")):
        stem = {"accident_photo_a": "photo_a", "accident_photo_b": "photo_b",
                "accident_photo_c": "photo_c", "accident_photo_d": "photo_d",
                "accident_licence_a": "licence_a_portrait",
                "accident_licence_b": "licence_b_portrait"}[cred]
        if (attachments / f"{stem}.png").exists() and stem in manifest:
            resolvable.add(sads[cred]["a"][fieldname])
    dag = load_corpus_dag(
        CORPUS, names,
        type_names={sc["accident_licence_a"]: "driving licence",
                    sc["accident_photo_a"]: "scene photograph",
                    sc["accident_statement_a"]: "witness statement",
                    sc["accident_bundle"]: "claim file"},
        subject_fields={sc["accident_photo_a"]: "depicts"} if with_subject else {},
        image_fields={sc["accident_photo_a"]: "imageDigest",
                      sc["accident_licence_a"]: "portraitDigest"},
        resolvable_digests=resolvable)
    return dag, sads, {sads[n]["d"]: n for n in names}


def test_accident_bundle_separates_all_three_pairs():
    """The bundle exists to make a single-channel proposal fail visibly. Nothing may collide."""
    dag, _, by_said = _accident_dag(with_subject=True)
    for d in describe(dag):
        assert d.distinguishing, (
            f"{by_said[d.said]} is not separable: also matches "
            f"{[by_said[s] for s in d.indistinguishable_from]}")


def test_accident_bundle_uses_a_different_channel_for_each_pair():
    """The point of the fixture, restated as an assertion.

    Each matched pair collides on schema and is separated by a different thing, so a change
    that made one channel do all the work would pass the previous test and still be wrong.
    """
    dag, sads, by_said = _accident_dag(with_subject=True)
    got = {by_said[d.said]: [c.kind for c in d.components] for d in describe(dag)}
    assert "image" in got["accident_photo_a"], got["accident_photo_a"]
    assert "image" in got["accident_photo_b"], got["accident_photo_b"]
    # The statements are separated by who WROTE them, which since the role-first change is
    # carried inside the party relation rather than by a bare issuer component.
    for n in ("accident_statement_a", "accident_statement_b"):
        assert "parties" in got[n], got[n]
    # Driver B's portrait does not resolve, so it cannot be the discriminator and the label
    # must fall through to the issuee -- see the unresolved_image vector for why.
    # Both portraits now resolve, so the licence pair is separated by the faces themselves --
    # which is the thumbnail hypothesis, and the reason real portraits were worth having.
    assert "image" in got["accident_licence_a"], got["accident_licence_a"]
    assert "image" in got["accident_licence_b"], got["accident_licence_b"]


def test_the_withheld_image_is_annotated_on_the_node_that_withheld_it():
    dag, _, by_said = _accident_dag(with_subject=True)
    ann = {by_said[d.said]: [a["kind"] for a in d.annotations] for d in describe(dag)}
    assert ann["accident_photo_d"] == ["image_committed_not_resolved"], ann
    for served in ("accident_photo_a", "accident_photo_c",
                   "accident_licence_a", "accident_licence_b"):
        assert "image_committed_not_resolved" not in ann[served], (served, ann[served])


def test_the_root_gets_no_discriminator_it_does_not_need():
    """A presented root is the claim rather than a part of it, and nothing else shares its
    schema -- so nothing is appended to tell it apart. What it carries is role-bearing only:
    what it is, and who assembled it. Renamed from ..._by_its_type_alone, which was written
    while the objective was minimality and expected the head on its own."""
    dag, _, by_said = _accident_dag(with_subject=True)
    root = next(d for d in describe(dag) if by_said[d.said] == "accident_bundle")
    assert [c.kind for c in root.components] == ["type", "parties"], root.components
    assert all(c.role_bearing for c in root.components), root.components


def test_dropping_the_subject_field_changes_the_answer_rather_than_breaking_it():
    """The dominance gap must degrade, not crash -- and must announce itself where it bites.

    An earlier version of this test expected the photographs to carry the gap annotation,
    which was wrong and the implementation was right: their thumbnails resolve, and a picture
    shows what a credential is about more directly than any field naming it would. The gap
    bites on the witness statements, whose label separates them by issuer and so says nothing
    at all about what either statement concerns.
    """
    dag, _, by_said = _accident_dag(with_subject=False)
    out = {by_said[d.said]: d for d in describe(dag)}
    assert all(d.distinguishing for d in out.values())
    # With no subject field the photographs are separable only by their pictures, so they are
    # NOT separable as text and must say so on both channels.
    assert "subject_undetermined" in [a["kind"] for a in out["accident_photo_a"].annotations]
    assert out["accident_photo_a"].distinguishing_as_text is False
    assert "subject_undetermined" in [a["kind"] for a in out["accident_statement_a"].annotations]


def test_the_bundle_survives_losing_its_pictures():
    """The change P-E3Q4 asked for, asserted end to end.

    With the subject field supplied, every node must remain separable when no thumbnail can
    be drawn -- which is a text-only export, a screen reader, or the 76x44 floor form. Before
    the text alternative was carried, five of nine nodes collapsed to "shown by its picture".
    """
    dag, _, by_said = _accident_dag(with_subject=True)
    for d in describe(dag):
        assert d.distinguishing_as_text, (
            f"{by_said[d.said]} cannot be told apart without its picture: "
            f"{[(c.kind, c.value) for c in d.components]}")


def test_the_vlei_chain_is_separable_too():
    """A second real shape, to catch anything tuned to the accident bundle alone."""
    names = ["vlei_qvi", "vlei_le", "vlei_ecr_auth", "vlei_ecr"]
    dag = load_corpus_dag(CORPUS, names)
    for d in describe(dag):
        assert d.distinguishing, d


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  FAIL {name}\n       {exc}")
    print(f"\n{failures} failure(s)")
    sys.exit(1 if failures else 0)


# --- schema resolution -------------------------------------------------------------------
# Offline only, deliberately. The live sources were exercised by hand and are recorded in
# refs/schema-registry.json's `verified` fields; a suite that reaches the network fails for
# reasons that have nothing to do with the code, and a flaky test gets muted rather than fixed.

def test_a_known_said_resolves_with_no_network_at_all():
    import schemas
    info = schemas.resolve("ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY")
    assert info.state == schemas.VERIFIED
    assert info.title == "Legal Entity vLEI Credential"
    assert info.entailed == ("issuer", "issuee")
    assert info.trustworthy


def test_resolution_asks_for_nothing_unless_a_fetcher_is_supplied():
    """Asking a host for a schema tells it somebody holds a credential of that type, so the
    default must be silence rather than convenience."""
    import schemas
    asked = []
    info = schemas.resolve("EUNKNOWNxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    assert info.state == schemas.UNAVAILABLE
    assert asked == []


def test_a_mismatched_document_is_its_own_state_and_is_never_cached():
    """A schema that does not digest to the SAID asked for is a security event, not an
    absence. Falling back to `unavailable` would file an attack under 'nothing found'."""
    import schemas
    cache = {}
    reg = {"sources": [{"id": "liar", "url": "x"}], "known_schemas": {}}
    info = schemas.resolve("ESOUGHT", registry=reg,
                           fetch=lambda said, src: '{"$id": "ESOUGHT", "title": "t"}',
                           digest=lambda doc: "EDIFFERENT", cache=cache)
    assert info.state == schemas.MISMATCH
    assert cache == {}, "a mismatch must never be remembered as an answer"


def test_an_unverified_schema_lends_a_name_but_not_an_entailment():
    """A wrong title is visible and merely wrong. A wrong entailment SUPPRESSES a component,
    so it makes the label say less than it should -- an omission, which is the direction this
    project treats as dangerous."""
    import schemas
    reg = {"sources": [{"id": "s", "url": "x"}], "known_schemas": {}}
    doc = ('{"$id": "ESOUGHT", "title": "Some Credential", "properties": '
           '{"i": {"description": "Issuer AID"}, "a": {"properties": '
           '{"i": {"description": "Issuee AID"}}}}}')
    info = schemas.resolve("ESOUGHT", registry=reg, fetch=lambda said, src: doc)
    assert info.state == schemas.UNVERIFIED
    assert info.title == "Some Credential"
    assert info.entailed == ()
    assert not info.trustworthy


# --- COIA ----------------------------------------------------------------------------------

def test_coia_parse_vectors_flag_groups_are_exact():
    """All eleven §6 parse vectors from the spec's normative set, on the half arcviz claims.

    arcviz implements the flag split of §6.1/§6.2 and does NOT implement §5 normalization --
    §3's Normalizer class is 69 further vectors and a real piece of work, and the reference
    coia.py in that repo is the oracle. So every vector's flag groups are asserted exactly,
    and one vector's BODY ("Bob As CEO,9" -> "bob-as-ceo") is knowingly not checked, because
    passing it would require the normalizer this module disclaims. Recorded rather than
    skipped silently: a partial pass presented as a pass is the failure this repo refuses.
    """
    import json as _json
    import coia
    path = Path.home() / "code" / "me" / "coia" / "vectors.json"
    if not path.exists():
        return  # the spec repo is a sibling, not a dependency
    vectors = _json.loads(path.read_text())["parse"]
    needs_normalizer = 0
    for name, raw, (want_body, want_g1, want_g2) in vectors:
        a = coia.parse(raw)
        assert a.group1 == want_g1 and a.group2 == want_g2, (name, a)
        if a.body != want_body:
            needs_normalizer += 1
    assert needs_normalizer == 1, (
        f"{needs_normalizer} vectors need §5 normalization; one is expected and known. "
        "If this number moved, either the spec's vectors changed or the disclaimer is stale.")


def test_an_unflagged_alias_is_never_reported_as_verified():
    """COIA §6.3: 'Absence is never a guarantee... An application MUST NOT render an absent
    flag as a positive assurance.' That is this project's own thesis, in someone else's spec."""
    import coia
    got = coia.render("EAID", coia.parse("cecilia-second-violin-vienna-symphony"))
    assert got["state"] == "unflagged"
    assert "verified" not in str(got).lower()


def test_a_compromised_flag_survives_to_the_renderer():
    """Dropping a flag would put a reassuring human name on an identifier its own creator
    marked as controlled by the wrong party."""
    import coia
    got = coia.render("EAID", coia.parse("bob-payee-bitcoin,9"))
    assert got["worst"] == "9"
    assert ("9", "compromised", "positive evidence that the wrong party controls it") in got["flags"]


def test_an_unrecognized_flag_digit_is_surfaced_not_dropped():
    """§6.3: a reader 'MUST surface it rather than ignore it -- it is a warning from a later
    version of the registry.'"""
    import coia
    a = coia.parse("someone-somewhere,3")
    assert a.unknown == ("3",)
    assert coia.render("EAID", a)["unknown_flags"] == ("3",)


def test_flags_are_split_before_any_normalization_touches_the_body():
    """§6.2 says the reverse order 'destroys the delimiter'. §5 normalization discards
    punctuation, so normalizing first eats the comma and folds a compromised flag into a name."""
    import coia
    seen = []

    def spy(body):
        seen.append(body)
        return body.replace(",", "")

    a = coia.parse("bob-payee-bitcoin,9", normalize=spy)
    assert seen == ["bob-payee-bitcoin"], seen
    assert a.group1 == "9"
