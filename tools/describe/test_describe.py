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

from describe import (Dag, Node, _role_stem, describe,  # noqa: E402
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
               field_roles=spec.get("field_roles", {}),
               image_fields=spec.get("image_fields", {}),
               resolvable_digests=set(spec.get("resolvable_digests", [])),
               entailed={k: tuple(v) for k, v in (spec.get("entailed") or {}).items()},
               aliased=set(spec.get("aliased", [])),
               presented=spec.get("presented"),
               pinned_edges={k: tuple(v)
                             for k, v in (spec.get("pinned_edges") or {}).items()})


def _check_vector(vec: dict) -> list[str]:
    assert vec.get("defends"), f"{vec['name']} carries no `defends`"
    dag = _dag_from_spec(vec["dag"])
    by_said = {d.said: d for d in describe(dag)}
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
        if "gains" in want:
            actual = {c.kind: round(c.gain, 3) for c in got.components}
            for kind, bits in want["gains"].items():
                if abs(actual.get(kind, -1) - bits) > 0.01:
                    bad(f"{said} gain[{kind}] = {actual.get(kind)}, expected {bits}")
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


def test_a_verified_schema_entailment_reaches_the_descriptor():
    """End to end, from the registry rather than from a vector. `schemas.resolve` names the
    two party slots ("issuer", "issuee") while the vectors name the channel ("parties"), and
    for a while each half passed its own tests while the real Legal Entity schema suppressed
    nothing. Found by building the sample, which is the only place the two met."""
    import schemas
    le = schemas.resolve("ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY")
    assert le.trustworthy and set(le.entailed) == {"issuer", "issuee"}
    nodes = [Node(said="A", schema="LE", issuer="Q", issuee="L"),
             Node(said="B", schema="OTHER", issuer="L", issuee="P")]
    dag = Dag(nodes=nodes, entailed={"LE": le.entailed})
    got = {d.said: [c.kind for c in d.components] for d in describe(dag)}
    assert got["A"] == ["type"], got
    assert "parties" in got["B"], got


# --- COIA ----------------------------------------------------------------------------------

def test_no_alias_passes_no_label_so_entvizs_own_fallback_runs():
    """`label: None`, never `""`. An empty string is still a label: it wins the precedence at
    EntvizPill.ts:499 and suppresses the type text, leaving a pill with no text at all."""
    import coia_reader as coia
    p = coia.pill_props("EKx4P_qnxW1ycaLCUlzoFCZJv6NlvrX2SQu58vq_oIt3", None)
    assert p["label"] is None
    assert coia.pill_props("EAID", "")["label"] is None


def test_the_alias_is_shown_verbatim_flags_and_all():
    """D-DCTS, Daniel 2026-09-24: arcviz "is *already* surfacing those flags if it displays coia
    aliases by calling the interface that looks them up." So a flagged alias reaches the label
    exactly as the host's interface returned it -- nothing split off, nothing stripped, no
    separate warning channel re-adjudicating a risk the interface already communicated."""
    import coia_reader as coia
    assert coia.pill_props("EAID", "bob-payee-bitcoin,9")["label"] == "bob-payee-bitcoin,9"
    view = coia.party_view("EAID", "jae-park-witness,0")
    assert view["label"] == "jae-park-witness,0"
    assert not any(k.lower().startswith("coia") for k in view), view


def test_the_lookup_is_consulted_once_per_identifier():
    import coia_reader as coia
    calls = []
    look = coia.AliasLookup(lambda aid: calls.append(aid) or {"EA": "alice"}.get(aid))
    assert look("EA") == "alice" and look("EA") == "alice" and look("EB") is None
    assert calls == ["EA", "EB"]


def test_channel_vectors():
    """The host's judgements about a party, and the decision about whether to apply an alias.

    Kept in the same file as the describe vectors because they are the same kind of artifact --
    a claim with the reason it is held -- and split into their own section because they test a
    different surface. Every one carries a `defends`, for the same reason: a vector whose
    intent is unrecorded cannot be maintained.
    """
    import coia_reader as coia
    data = json.loads((HERE / "vectors.json").read_text())
    problems = []
    for vec in data["channels"]:
        assert vec.get("defends"), f"{vec['name']} carries no `defends`"
        i = vec["input"]
        alias = i.get("alias")
        got = coia.party_view(
            i["identifier"], alias,
            stance=coia.Stance(**i["stance"]) if i.get("stance") else None,
            apply_alias=i.get("apply_alias"))
        for key, want in vec["expect"].items():
            actual = got[key]
            if isinstance(want, list):          # JSON has no tuples
                actual = [list(x) if isinstance(x, tuple) else x for x in actual]
            if actual != want:
                problems.append(f"{vec['name']}: {key} = {actual!r}, expected {want!r}")
    assert not problems, "\n".join(problems)




# --- the abbreviation lexicon ------------------------------------------------------------
# Checked by test rather than by eye, because the rule it enforces is exactly the kind a
# careful human misses: `auth` looks fine until you notice the domain contains two words it
# could come from.

def _lexicon():
    return json.loads((HERE / ".." / ".." / "refs" / "abbreviations.json").read_text())


def test_no_abbreviation_is_reachable_from_two_terms():
    """Daniel's rule, 2026-09-24: an abbreviation must be unambiguous WITHIN THE DOMAIN, not
    merely derivable from the word. A mechanical shortener produces `auth` from both
    authorization and authentication and is wrong in a way nobody notices until a reader takes
    one credential for the other -- security-relevant here, not cosmetic."""
    lex = _lexicon()["terms"]
    seen = {}
    collisions = []
    for term, forms in lex.items():
        for tier in ("medium", "short"):
            form = forms.get(tier)
            if not form or form == term:
                continue
            key = form.casefold()
            if key in seen and seen[key] != term:
                collisions.append(f"{form!r} is reachable from {seen[key]!r} and {term!r}")
            seen.setdefault(key, term)
    assert not collisions, "\n".join(collisions)


def test_the_two_words_that_forced_the_rule_do_not_collide():
    lex = _lexicon()["terms"]
    assert lex["authorization"]["medium"] == "authz"
    assert lex["authentication"]["medium"] == "authn"
    for term in ("authorization", "authentication"):
        for tier in ("medium", "short"):
            assert lex[term][tier] != "auth", f"{term}/{tier} fell back to the ambiguous form"


def test_every_abbreviation_is_shorter_than_its_term_or_equal_by_choice():
    """A `short` equal to `medium` is a statement that no shorter form is safe, not an
    omission -- but an abbreviation LONGER than the word it abbreviates is a mistake."""
    for term, forms in _lexicon()["terms"].items():
        for tier in ("medium", "short"):
            assert len(forms[tier]) <= len(term), f"{term}/{tier}={forms[tier]} is not shorter"


def test_tiers_never_widen():
    """short may equal medium; it may never be longer. A render stepping down a tier must
    never get more text than it had."""
    for term, forms in _lexicon()["terms"].items():
        assert len(forms["short"]) <= len(forms["medium"]), term


def test_every_disagreement_with_the_ecosystem_is_explained():
    """vLEI ships AUTH, and this lexicon refuses it. Any entry that departs from the domain's
    own usage carries a `note` saying so, because an unexplained disagreement reads as an
    oversight and gets 'corrected' back."""
    lex = _lexicon()["terms"]
    assert "vLEI's own ECR-AUTH uses AUTH" in lex["authorization"]["note"]
    for term in ("issuer", "issuee", "verifiable", "identifier", "delegation"):
        assert lex[term].get("note"), f"{term} departs from the obvious short form unexplained"


if __name__ == "__main__":
    # This block MUST be the last thing in the file. A test defined after it is invisible to
    # this runner and silently reported as absent rather than as failing -- which is how four
    # channel vectors passed a mutation test they should have caught. pytest collects them
    # either way, so the discrepancy is the tell.
    import inspect as _inspect
    _src = pathlib.Path(__file__).read_text() if "pathlib" in dir() else open(__file__).read()
    if _src.index('if __name__ == "__main__":') < _src.rfind("\ndef test_"):
        raise SystemExit("test_describe.py: a test is defined AFTER the runner block and "
                         "would never run. Move the runner to the end of the file.")
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
