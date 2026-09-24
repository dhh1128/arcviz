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
             "accident_photo_a", "accident_photo_b",
             "accident_statement_a", "accident_statement_b"]
    sads = {n: json.loads((CORPUS / f"{n}.json").read_text()) for n in names}
    sc = {n: s["s"] for n, s in sads.items()}
    resolvable = {sads["accident_photo_a"]["a"]["imageDigest"],
                  sads["accident_photo_b"]["a"]["imageDigest"],
                  sads["accident_licence_a"]["a"]["portraitDigest"]}
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
    assert "issuer" in got["accident_statement_a"], got["accident_statement_a"]
    assert "issuer" in got["accident_statement_b"], got["accident_statement_b"]
    # Driver B's portrait does not resolve, so it cannot be the discriminator and the label
    # must fall through to the issuee -- see the unresolved_image vector for why.
    assert "issuee" in got["accident_licence_b"], got["accident_licence_b"]


def test_the_withheld_portrait_is_annotated_on_the_node_that_withheld_it():
    dag, _, by_said = _accident_dag(with_subject=True)
    ann = {by_said[d.said]: [a["kind"] for a in d.annotations] for d in describe(dag)}
    assert ann["accident_licence_b"] == ["image_committed_not_resolved"], ann
    assert ann["accident_licence_a"] == [], ann


def test_the_root_is_described_by_its_type_alone():
    """A presented root is the claim rather than a part of it: nothing else shares its schema,
    so the head is the whole description and no discriminator is appended for its own sake."""
    dag, _, by_said = _accident_dag(with_subject=True)
    root = next(d for d in describe(dag) if by_said[d.said] == "accident_bundle")
    assert [c.kind for c in root.components] == ["type"], root.components


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
    assert [a["kind"] for a in out["accident_photo_a"].annotations] == []
    assert "subject_undetermined" in [a["kind"] for a in out["accident_statement_a"].annotations]


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
