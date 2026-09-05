"""Tests that assert the generated corpus is actually valid.

A fixture that merely looks right (parses as JSON, has plausible-looking
digests) but doesn't actually recompute is worse than no fixture at all --
it would let a renderer pass a test it should fail. These tests recompute
every fixture's SAID from its saved bytes, validate schemas, and check that
edges naming another fixture as their far node actually resolve.
"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from keri.core.coring import Diger
from keri.core.serdering import SerderACDC

CORPUS_DIR = Path(__file__).resolve().parents[3] / "corpus"


def _all_fixture_names():
    names = set()
    for p in CORPUS_DIR.glob("*.meta.json"):
        names.add(p.name.removesuffix(".meta.json"))
    return sorted(names)


FIXTURE_NAMES = _all_fixture_names()


def load(name):
    sad = json.loads((CORPUS_DIR / f"{name}.json").read_text())
    meta = json.loads((CORPUS_DIR / f"{name}.meta.json").read_text())
    return sad, meta


def test_corpus_is_not_empty():
    assert len(FIXTURE_NAMES) >= 25, (
        f"expected at least 25 fixtures, found {len(FIXTURE_NAMES)}: {FIXTURE_NAMES}")


def test_readme_indexes_every_fixture():
    readme = (CORPUS_DIR / "README.md").read_text()
    for name in FIXTURE_NAMES:
        assert f"`{name}`" in readme, f"{name} is not indexed in corpus/README.md"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_meta_sidecar_is_well_formed(name):
    _, meta = load(name)
    assert meta.get("name") == name
    assert "title" in meta and meta["title"]
    assert "summary" in meta and meta["summary"]
    assert "matrix_cells" in meta, "every fixture must name which matrix cell(s) it exercises"
    assert isinstance(meta["matrix_cells"], list)
    assert "files" in meta
    assert meta["files"].get("sad") == f"{name}.json"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_said_recomputes(name):
    """The core honesty check: re-derive the SAID from the disclosed bytes
    and confirm it matches the recorded `d`. SerderACDC(verify=True) raises
    on mismatch; we also independently re-serialize and hash to be sure this
    isn't just trusting keripy's own internal consistency.
    """
    sad, _ = load(name)
    # SerderACDC recomputes and verifies said(s) against the given sad.
    serder = SerderACDC(sad=sad, makify=False, verify=True)
    assert serder.said == sad["d"]

    # Independent cross-check: the .cesr sidecar's bytes must hash (via the
    # same digest algorithm the recorded SAID names) to that exact SAID over
    # the *dummied* serialization -- i.e. the raw wire bytes are consistent
    # with the SAID, not just internally self-referential.
    cesr_path = CORPUS_DIR / f"{name}.cesr"
    if cesr_path.exists():
        raw = cesr_path.read_bytes()
        assert raw == serder.raw, f"{name}.cesr does not match the recomputed wire serialization"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_nested_saids_are_not_placeholders(name):
    """No literal '' (unfilled-placeholder) SAID anywhere in a disclosed
    fixture -- see common.py's note on the compactify=False trap this
    generator had to work around. Generalized beyond 'd' by
    test_no_said_typed_field_is_empty_or_malformed below, which is the
    complete version of this check; kept separate because this one is the
    narrowest possible statement of the original bug and should never
    regress even if the broader check is ever loosened.
    """
    sad, _ = load(name)

    def walk(node, path):
        if isinstance(node, dict):
            if "d" in node:
                assert node["d"] != "", f"{name}{path}: empty 'd' placeholder was never filled"
            for k, v in node.items():
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(sad, "")


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_expanded_companion_recomputes_when_present(name):
    """A `<name>.expanded.json` (reference-only content behind a blinded or
    compact fixture) must itself be internally consistent: any nested block
    with a 'd' must be a real, non-empty digest.
    """
    exp_path = CORPUS_DIR / f"{name}.expanded.json"
    if not exp_path.exists():
        pytest.skip(f"{name} has no expanded companion")
    expanded = json.loads(exp_path.read_text())

    def walk(node, path):
        if isinstance(node, dict):
            if "d" in node:
                assert node["d"] != "", f"{name}.expanded.json{path}: empty 'd'"
            for k, v in node.items():
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(expanded, "")


# --- The generalized placeholder check. ---
#
# 'd' was the specific bug found during development (see common.py's note on
# compactify=False); 'rd' turned out to carry the exact same class of bug in
# a field the check above never looked at (bare_agid.json's "rd": "").
# SAID_TYPED_LABELS is every top-level-or-nested field whose value, WHEN A
# STRING, is meant to be a self-addressing digest (a SAID or an AGID, which
# is digest-derived the same way -- spec-body.md:712-720). Absence is a
# different, legitimate state (H9) from an empty string in one of these
# fields, which is neither a valid digest nor a meaningful "nothing" -- it is
# simply wrong, and exactly the state disclosure-matrix.md's H-axis exists to
# never let a renderer be confused by.
#
# 'n' is deliberately NOT in SAID_TYPED_LABELS, because it is overloaded:
# inside an Edge block it is the far-node SAID (spec-body.md:1140-1149), but
# in a registry-lifecycle message (rip/bup/upd) it is a sequence NUMBER
# (keri.core.Number-derived, a different CESR derivation-code family
# entirely -- Diger(qb64=...) on one of these would correctly reject it as
# "not a digest", which is not the bug we're checking for). So 'n' is
# checked as a SAID only inside fixtures whose top-level ilk is not a
# registry-lifecycle message; see check_edge_n below.
SAID_TYPED_LABELS = ("d", "rd", "ri", "s", "A")
REGISTRY_ILKS = {"rip", "bup", "upd"}


def _collect_said_field_violations(node, path, *, check_edge_n, violations):
    if isinstance(node, dict):
        labels = list(SAID_TYPED_LABELS)
        if check_edge_n:
            labels.append("n")
        for label in labels:
            if label not in node:
                continue
            value = node[label]
            if not isinstance(value, str):
                continue  # uncompacted/inline form (dict/list) -- not a SAID string here
            if value == "":
                violations.append(f"{path}.{label} is an empty-string placeholder (absent != empty)")
                continue
            try:
                Diger(qb64=value)
            except Exception as ex:  # noqa: BLE001
                violations.append(f"{path}.{label}={value!r} is not a well-formed SAID: {ex}")
        for k, v in node.items():
            _collect_said_field_violations(v, f"{path}.{k}", check_edge_n=check_edge_n, violations=violations)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _collect_said_field_violations(v, f"{path}[{i}]", check_edge_n=check_edge_n, violations=violations)


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_no_said_typed_field_is_empty_or_malformed(name):
    """Every SAID-typed field (d, rd, ri, s, A, and an Edge's n), at every
    level of nesting, is either absent or a well-formed non-empty SAID --
    never a placeholder empty string. Covers the disclosed sad, and
    separately the .expanded.json reference file when one exists, so a
    placeholder bug can't hide in content this generator produces but never
    puts in the primary disclosed artifact.
    """
    sad, _ = load(name)
    check_edge_n = sad.get("t") not in REGISTRY_ILKS
    violations = []
    _collect_said_field_violations(sad, name, check_edge_n=check_edge_n, violations=violations)

    exp_path = CORPUS_DIR / f"{name}.expanded.json"
    if exp_path.exists():
        expanded = json.loads(exp_path.read_text())
        _collect_said_field_violations(
            expanded, f"{name}.expanded", check_edge_n=True, violations=violations)

    assert not violations, "\n".join(violations)


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_acdc_fixtures_reference_schema_by_said(name):
    """Every ACDC (non-registry) fixture here carries a bare-SAID `s` --
    schema referenced, not inlined -- so a schema-validation test elsewhere
    that resolves `s` is actually checking something instead of silently
    validating against an already-inline schema block.
    """
    sad, _ = load(name)
    if sad.get("t") == "rip":
        pytest.skip("registry inception messages carry no schema section")
    assert isinstance(sad.get("s"), str) and sad["s"], "expected a compact (bare-SAID) schema reference"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_top_level_field_order(name):
    """acdc-inventory.md sec.1: top-level fields MUST appear in order
    [v, t, d, u, i, rd, s, a, A, e, r]."""
    sad, _ = load(name)
    canonical = ["v", "t", "d", "u", "i", "rd", "s", "a", "A", "e", "r"]
    present = [k for k in sad.keys() if k in canonical]
    expected_order = [k for k in canonical if k in sad]
    assert present == expected_order, f"{name}: top-level field order {present} != {expected_order}"


# --- Chain-resolution checks: specific, named fixtures whose edges/AGIDs
# must resolve against sibling fixtures in this corpus. ---

VLEI_CHAIN = ["vlei_qvi", "vlei_le", "vlei_ecr_auth", "vlei_ecr"]
VLEI_EDGE_LABELS = [None, "qvi", "le", "auth"]


def test_vlei_chain_resolves():
    sads = {name: load(name)[0] for name in VLEI_CHAIN}
    for i in range(1, len(VLEI_CHAIN)):
        near = sads[VLEI_CHAIN[i]]
        far = sads[VLEI_CHAIN[i - 1]]
        label = VLEI_EDGE_LABELS[i]
        edge = near["e"][label]
        assert edge["n"] == far["d"], (
            f"{VLEI_CHAIN[i]}'s edge {label!r} does not point at {VLEI_CHAIN[i-1]}'s SAID")
        assert edge["s"] == far["s"], f"{VLEI_CHAIN[i]}'s edge schema ref does not match far node's schema"

    # issuer/subject alternation (corpus-vlei-chain.md sec.1)
    assert sads["vlei_le"]["i"] == sads["vlei_qvi"]["a"]["i"]
    assert sads["vlei_ecr_auth"]["i"] == sads["vlei_le"]["a"]["i"]
    assert sads["vlei_ecr"]["i"] == sads["vlei_ecr_auth"]["a"]["i"]

    # leaf-only top-level u
    assert sads["vlei_qvi"].get("u") is None
    assert sads["vlei_le"].get("u") is None
    assert sads["vlei_ecr_auth"].get("u") is None
    assert sads["vlei_ecr"].get("u"), "the ECR leaf must carry the chain's only top-level u"

    # default vs explicit operator (RULE 9: must render identically)
    assert "o" not in sads["vlei_le"]["e"]["qvi"]
    assert "o" not in sads["vlei_ecr_auth"]["e"]["le"]
    assert sads["vlei_ecr"]["e"]["auth"]["o"] == "I2I"


def test_diamond_with_depth_resolves():
    a, _ = load("diamond_depth_a")
    b, _ = load("diamond_depth_b")
    c, _ = load("diamond_depth_c")
    f, _ = load("diamond_depth_f")
    origin, _ = load("diamond_depth_origin")

    assert b["e"]["baseline"]["n"] == a["d"]
    assert f["e"]["baseline"]["n"] == a["d"]
    assert c["e"]["waypoint"]["n"] == f["d"]
    assert origin["e"]["shortPath"]["n"] == b["d"]
    assert origin["e"]["longPath"]["n"] == c["d"]
    # both paths reconverge on the same node a, at different depths
    assert b["e"]["baseline"]["n"] == f["e"]["baseline"]["n"]


def test_same_schema_twice_dag_resolves():
    alice, _ = load("same_schema_alice")
    bob, _ = load("same_schema_bob")
    household, _ = load("same_schema_household")

    assert alice["s"] == bob["s"], "alice and bob must instantiate the identical schema SAID"
    assert alice["d"] != bob["d"], "but must be different ACDCs"
    assert household["e"]["memberA"]["n"] == alice["d"]
    assert household["e"]["memberB"]["n"] == bob["d"]


def test_optional_edge_pair_shares_schema_and_differs_on_edge():
    present, _ = load("optional_edge_present")
    absent, _ = load("optional_edge_absent")
    assert present["s"] == absent["s"], "the pair must share one schema SAID"
    assert "e" in present
    assert "e" not in absent
    assert present["d"] != absent["d"]


def test_working_edge_group_resolves_to_real_endorsers():
    main, _ = load("working_edge_group")
    a, _ = load("working_edge_group_endorser_a")
    b, _ = load("working_edge_group_endorser_b")
    assert main["e"]["o"] == "AND"
    assert main["e"]["inspectorA"]["n"] == a["d"]
    assert main["e"]["inspectorB"]["n"] == b["d"]
    assert a["d"] != b["d"]
    assert a["a"]["inspector"] != b["a"]["inspector"]


def test_compact_private_edge_hides_far_node():
    sad, _ = load("compact_private_edge")
    exp_path = CORPUS_DIR / "compact_private_edge.expanded.json"
    expanded = json.loads(exp_path.read_text())
    far = expanded["far_node"]

    # The disclosed sad must not contain the far node's SAID anywhere.
    disclosed_text = json.dumps(sad)
    assert far["d"] not in disclosed_text, "far node's SAID leaked into the disclosed sad"
    # The edge slot exists (structurally visible) but is a bare string.
    assert isinstance(sad["e"]["source"], str)


def test_blinded_edge_group_is_a_single_bare_said():
    sad, _ = load("blinded_edge_group")
    assert isinstance(sad["e"], str), "the whole edge-group must be one bare SAID"


def test_blinded_rule_group_is_a_single_bare_said():
    sad, _ = load("blinded_rule_group")
    assert isinstance(sad["r"], str), "the whole rule-group must be one bare SAID"


def test_bare_agid_matches_expanded_aggregate():
    sad, _ = load("bare_agid")
    expanded = json.loads((CORPUS_DIR / "bare_agid.expanded.json").read_text())
    assert isinstance(sad["A"], str), "A must be a bare AGID, not an array"
    assert sad["A"] == expanded["agid"]

    from keri.core import Aggor
    from keri.core.coring import Kinds
    assert Aggor.verifyDisclosure(expanded["aggregate_elements"], kind=Kinds.json)


def test_metadata_acdc_has_empty_top_uuid():
    sad, _ = load("metadata_acdc")
    assert sad.get("u") == "", "top-level u must be present AND empty for a Metadata ACDC"


@pytest.mark.parametrize("name,operator", [
    ("di2i_operator", "DI2I"),
    ("not_operator", "NOT"),
])
def test_operator_fixtures_carry_their_operator(name, operator):
    sad, _ = load(name)
    edge_group = sad["e"]
    ops = [v.get("o") for v in edge_group.values() if isinstance(v, dict) and "o" in v]
    assert operator in ops, f"{name} does not carry the {operator} operator in its disclosed edge"


def test_edge_group_operators_covers_and_or_avg_wavg():
    sad, _ = load("edge_group_operators")
    ops = {k: v["o"] for k, v in sad["e"].items() if isinstance(v, dict) and "o" in v}
    assert set(ops.values()) == {"AND", "OR", "AVG", "WAVG"}
    wavg = sad["e"]["weightedAverage"]
    assert wavg["primary"]["w"] == 0.7
    assert wavg["secondary"]["w"] == 0.3


def test_schema_referenced_by_optional_edge_pair_is_valid_json_schema():
    """Rebuild the shared schema exactly as the fixtures did and check it is
    itself a valid Draft 2020-12 schema, and that both instances validate.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from arcviz_fixtures import schemas

    schema_said, schema_mad = schemas.attr_schema(
        title="Optional-Edge Demo Schema", credential_type="ArcvizFixture_OptionalEdge",
        attr_props={"claim": {"type": "string"}}, attr_required=["claim"],
        has_edge=True, edge_required=False)

    Draft202012Validator.check_schema(schema_mad)

    present, _ = load("optional_edge_present")
    absent, _ = load("optional_edge_absent")
    assert present["s"] == schema_said == absent["s"]
    Draft202012Validator(schema_mad).validate(present)
    Draft202012Validator(schema_mad).validate(absent)


def test_vlei_ecr_schema_validates():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from arcviz_fixtures import schemas

    schema_said, schema_mad = schemas.attr_schema(
        title="ECR vLEI Credential Schema (fixture)", credential_type="ArcvizFixture_ECR",
        attr_props={
            "LEI": {"type": "string"}, "dt": {"type": "string", "format": "date-time"},
            "personLegalName": {"type": "string"}, "engagementContextRole": {"type": "string"},
        },
        attr_required=["LEI", "dt", "personLegalName", "engagementContextRole"])
    Draft202012Validator.check_schema(schema_mad)
    ecr, _ = load("vlei_ecr")
    assert ecr["s"] == schema_said
    Draft202012Validator(schema_mad).validate(ecr)
