"""Writing fixtures (and their sidecar metadata) to corpus/."""

import datetime
import json
import subprocess
from pathlib import Path

KERIPY_PATH = Path("/home/daniel/code/wot/keripy")


def keripy_commit() -> str:
    """The keripy commit this generation run read from, for provenance.

    Best-effort: returns 'unknown' rather than failing generation if git isn't
    available or the tree is in some unreadable state.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(KERIPY_PATH), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        )
        sha = out.stdout.strip()
        branch = subprocess.run(
            ["git", "-C", str(KERIPY_PATH), "branch", "--show-current"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(KERIPY_PATH), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
        suffix = "-dirty" if dirty else ""
        return f"{sha}{suffix} (branch {branch})"
    except Exception:
        return "unknown"


def write_fixture(corpus_dir: Path, name: str, *, sad: dict, meta: dict,
                   raw: bytes | None = None, expanded: dict | None = None):
    """Write <name>.json (+ .cesr, + .expanded.json) and <name>.meta.json.

    Parameters:
        sad: the primary, disclosed field map for this fixture -- what a
            renderer would actually receive.
        raw: the exact wire-serialized bytes (SerderACDC.raw) for the same
            sad, when meaningful to carry alongside the pretty JSON.
        expanded: an optional fully-expanded reference form (e.g. the
            un-compacted edge/rule/aggregate content behind a fixture's
            blinded or compact SAIDs), for tests to recompute nested SAIDs
            against. Not itself "the fixture" -- a renderer would never
            legitimately receive this for a disclosure-state fixture whose
            whole point is that the content is withheld.
    """
    corpus_dir.mkdir(parents=True, exist_ok=True)
    files = {}

    json_path = corpus_dir / f"{name}.json"
    json_path.write_text(json.dumps(sad, indent=2, ensure_ascii=False) + "\n")
    files["sad"] = json_path.name

    if raw is not None:
        cesr_path = corpus_dir / f"{name}.cesr"
        cesr_path.write_bytes(raw)
        files["cesr"] = cesr_path.name

    if expanded is not None:
        exp_path = corpus_dir / f"{name}.expanded.json"
        exp_path.write_text(json.dumps(expanded, indent=2, ensure_ascii=False) + "\n")
        files["expanded"] = exp_path.name

    meta = dict(meta)
    meta["files"] = files
    meta.setdefault("generated_at", datetime.datetime.now(datetime.UTC).isoformat())
    meta.setdefault("keripy_commit", keripy_commit())
    meta_path = corpus_dir / f"{name}.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    return files
