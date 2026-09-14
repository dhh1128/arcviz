"""Gap G1 (docs/design/shape-catalog.md (d)): a documented "withhold this
dependency" load mode, so H7 (missing referent) is producible on demand
rather than by accident of corpus incompleteness.

This is deliberately a LOADER feature, not a new credential (per the gap
table: "loader/harness feature, not a new artifact"). Every fixture this
module touches already exists in corpus/, fully generated with correct
SAIDs; what's added here is a small, inspectable "load recipe" -- a plain
JSON manifest under corpus/loads/ naming which of an existing chain's
members to actually serve, and which one to withhold, while recording the
withheld member's real SAID so a test (or a renderer-under-test) can confirm
the reference resolves to *nothing present*, not to garbage and not to
nothing-named.

Two flavours, matching shape-catalog.md SC6's framing that H7 is "the same
state reached two ways":

  - "credential": an edge's `n` names a real ACDC's SAID, and that ACDC's
    own file is excluded from the served set. This is directly testable:
    load only `served`, confirm none of those files has `d` equal to the
    withheld SAID.
  - "delegator_kel": an AID is asserted (out of band, exactly as a real
    verifier receives delegation facts -- from its own KEL walk, never from
    an ACDC field, since ACDCs carry no delegation info at all) to be a
    credential's issuer's own delegator, and no KEL artifact for that AID
    exists anywhere in this corpus -- nor could it, since this generator
    does not model KELs at all (tools/fixtures/README.md "What this does
    not model"). This flavour doesn't subset anything (there was never a
    KEL fixture to remove); what it adds is NAMING the hole in a discoverable
    manifest, rather than leaving it as an unstated consequence of scope.
"""

import json
from pathlib import Path

from . import determinism as det

CREDENTIAL_RECIPES = [
    {
        "name": "h7_missing_credential",
        "chain": ["vlei_qvi", "vlei_le", "vlei_ecr_auth", "vlei_ecr"],
        "withhold_fixture": "vlei_ecr_auth",
        "referencing": [{"fixture": "vlei_ecr", "path": "e.auth.n"}],
        "description": (
            "The vLEI-equivalent chain served with its ECR-AUTH credential "
            "withheld. vlei_ecr's edge 'auth' still names ECR-AUTH's real "
            "SAID -- a renderer given only the 'served' files must draw an "
            "explicit hole at that SAID (Rule 10), not a trimmed edge and "
            "not a guessed/manufactured far node (H8's naive lie, applied "
            "here to H7)."
        ),
    },
]

DELEGATOR_RECIPES = [
    {
        "name": "h7_missing_delegator_kel",
        "chain": ["vlei_qvi", "vlei_le", "vlei_ecr_auth", "vlei_ecr"],
        "withheld_aid_label": "vlei:absent_root_delegator",
        "referenced_by": {
            "fixture": "vlei_qvi",
            "field": "i",
            "role": (
                "vlei_qvi's issuer AID stands in for the real chain's "
                "first-tier delegate (corpus-vlei-chain.md sec.1's "
                "EINmHd5g7iV...). That AID's own inception is, in the real "
                "chain, itself delegated (a dip event naming a root "
                "delegator, corpus-vlei-chain.md sec.3's EDP1vHcw_wc4M...); "
                "this corpus does not model KEL events at all, so that "
                "delegation fact cannot live inside vlei_qvi.json (no ACDC "
                "field carries it -- delegation is a KEL-level fact a real "
                "verifier gets from walking the issuer's own KEL, never from "
                "the credential). It is recorded HERE, in this load recipe, "
                "which is the closest honest analogue to how a renderer "
                "actually receives it: as context from a KEL-resolution "
                "component that is not the ACDC itself."
            ),
        },
        "description": (
            "The vLEI-equivalent chain, served in full (nothing is removed, "
            "because no KEL fixture for this AID has ever existed -- see "
            "'referenced_by'). Names the second way shape-catalog.md SC6 "
            "reaches H7: an absent root DELEGATOR's KEL, not an absent "
            "credential. Rule 10's 'name the blocking SAID/AID' requirement "
            "applies identically to this flavour; the blocking identifier "
            "here is an AID, not a credential SAID."
        ),
    },
]


def _get_path(sad, path):
    node = sad
    for part in path.split("."):
        node = node[part]
    return node


def _load_sad(corpus_dir: Path, fixture_name: str) -> dict:
    return json.loads((corpus_dir / f"{fixture_name}.json").read_text())


def build_credential_recipe(corpus_dir: Path, recipe: dict) -> dict:
    chain_sads = {name: _load_sad(corpus_dir, name) for name in recipe["chain"]}
    withheld_name = recipe["withhold_fixture"]
    withheld_said = chain_sads[withheld_name]["d"]
    served = [n for n in recipe["chain"] if n != withheld_name]

    referencing = []
    for ref in recipe["referencing"]:
        said = _get_path(chain_sads[ref["fixture"]], ref["path"])
        if said != withheld_said:
            raise ValueError(
                f"recipe {recipe['name']!r}: {ref['fixture']}.{ref['path']} "
                f"= {said!r} does not match withheld SAID {withheld_said!r}")
        referencing.append({"fixture": ref["fixture"], "path": ref["path"], "said": said})

    return {
        "name": recipe["name"],
        "kind": "credential",
        "description": recipe["description"],
        "chain": recipe["chain"],
        "served": served,
        "withheld": {"fixture": withheld_name, "said": withheld_said},
        "referencing": referencing,
    }


def build_delegator_recipe(corpus_dir: Path, recipe: dict) -> dict:
    withheld_aid = det.aid(recipe["withheld_aid_label"])

    # Confirm this AID really does not correspond to any artifact anywhere
    # in the generated corpus -- i.e. that naming it here doesn't
    # accidentally collide with something that DOES exist (which would
    # silently turn this into a credential-flavour recipe wearing the wrong
    # label). Scans every *.json in corpus_dir (not just the chain) since
    # the claim being made is "nowhere in this corpus", not "not in the
    # chain".
    for path in sorted(corpus_dir.glob("*.json")):
        if path.name.endswith((".meta.json",)):
            continue
        try:
            sad = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(sad, dict):
            continue
        if sad.get("d") == withheld_aid or sad.get("i") == withheld_aid:
            raise ValueError(
                f"recipe {recipe['name']!r}: withheld AID {withheld_aid!r} "
                f"unexpectedly matches {path.name} -- label collision")

    return {
        "name": recipe["name"],
        "kind": "delegator_kel",
        "description": recipe["description"],
        "chain": recipe["chain"],
        "served": list(recipe["chain"]),
        "withheld": {
            "aid": withheld_aid,
            "referenced_by": recipe["referenced_by"],
        },
    }


def write_load_recipes(corpus_dir: Path) -> list[str]:
    """Build and write every load recipe to corpus/loads/. Must run AFTER
    the main fixture-generation pass, since recipes read real SAIDs back
    from already-written fixture files.
    """
    loads_dir = corpus_dir / "loads"
    loads_dir.mkdir(parents=True, exist_ok=True)
    written = []

    for recipe in CREDENTIAL_RECIPES:
        manifest = build_credential_recipe(corpus_dir, recipe)
        _write_recipe(loads_dir, manifest)
        written.append(manifest["name"])

    for recipe in DELEGATOR_RECIPES:
        manifest = build_delegator_recipe(corpus_dir, recipe)
        _write_recipe(loads_dir, manifest)
        written.append(manifest["name"])

    return written


def _write_recipe(loads_dir: Path, manifest: dict):
    (loads_dir / f"{manifest['name']}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    meta = {
        "name": manifest["name"],
        "title": (
            "Load recipe: missing referent via withheld credential"
            if manifest["kind"] == "credential"
            else "Load recipe: missing referent via absent delegator KEL"
        ),
        "summary": manifest["description"],
        "matrix_cells": ["H7"],
        "rules_exercised": ["RULE 10", "RULE 9"],
        "kind": manifest["kind"],
        "files": {"sad": f"{manifest['name']}.json"},
    }
    (loads_dir / f"{manifest['name']}.meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
