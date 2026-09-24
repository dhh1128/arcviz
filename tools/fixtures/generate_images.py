#!/usr/bin/env python3
"""Generate the corpus's photorealistic attachments. RUN BY HAND, NEVER BY THE GENERATOR.

WHY THIS IS A SEPARATE SCRIPT, WHICH IS THE WHOLE POINT. `tools/fixtures/README.md` promises
that `uv run arcviz-fixtures` is deterministic -- the same code always produces byte-identical
output -- and every SAID in the corpus depends on it, because an ACDC commits to its
attachment by digest and that digest is folded into the credential's SAID and into every SAID
above it. A generative model is the exact opposite of deterministic: the same prompt returns
different bytes every call. Wiring image generation into the fixture generator would therefore
change `imageDigest`, and so every SAID in the accident bundle, on every run, and the
corpus's central guarantee would be gone -- silently, because the fixtures would still all be
internally valid.

So the images are a VENDORED ASSET. They are generated once by this script, committed, and
from then on read off disk by `fx_bundles.py`, which digests what it finds. Regenerating the
corpus does not regenerate the images. Re-running this script is a deliberate act that
produces a visible diff in `corpus/attachments/` and changes the bundle's SAIDs, which is
correct: new bytes ARE new content.

PROVENANCE IS THE PRICE OF NON-REPRODUCIBILITY. A photorealistic image sitting unlabelled in
a fixture corpus is a claim nobody can check later, and this repository's evidence discipline
exists to prevent exactly that. Because these cannot be regenerated identically, the record of
where they came from is the only provenance there will ever be -- so MANIFEST.json carries the
model, the full prompt, the time and the SHA-256 of each file, in the same spirit as the
`keripy_commit` stamp every fixture already carries.

ON GENERATING FACES, since the corpus contains two driving licences. There is nothing wrong
with a synthetic face here, and an earlier draft of this corpus argued otherwise on reflex
rather than on reasoning: the fixture already ships a fabricated name, licence number, VIN and
AID, and a fabricated face is the same class of artifact. The test the thumbnail channel needs
-- does a portrait separate two licences at forty pixels -- cannot be run against coloured
rectangles. The prompts below ask for plainly synthetic, neutral studio portraits and attach
no allegation to either driver; the bundle's disagreeing witness statements are about the
collision, not about a face.

Usage:

    OPENROUTER_API_KEY=... uv run --with pillow --with httpx python generate_images.py
    uv run --with pillow --with httpx python generate_images.py --dry-run   # prompts only

The key is read from the environment or from ~/.config/io.datasette.llm/keys.json, which is
where `llm` already keeps it. Cost at the time of writing was roughly $0.004 per image.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import io
import json
import os
import pathlib
import sys

MODEL = "google/gemini-2.5-flash-image"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
# Downscaled from the model's 1024px output. A thumbnail is the use case, and a public repo
# should not carry five megabytes of PNG to prove that two cars look different.
EDGE = 512

CORPUS = pathlib.Path(__file__).resolve().parents[2] / "corpus"
OUT = CORPUS / "attachments"

# Only images that are actually SERVED are generated. `accident_licence_b`'s portrait is
# deliberately never written -- it is the committed-but-unresolvable state -- so there is
# nothing to generate for it and no reason to pay for bytes that get discarded.
IMAGES = {
    "photo_a": (
        "An insurance adjuster's evidence photograph of collision damage to the front "
        "nearside corner of a silver compact hatchback. Daylight, overcast, an ordinary "
        "urban street. The crumpled wing, broken indicator lens and scuffed bumper fill the "
        "frame. Flat documentary style, no people, no visible number plate, no text."
    ),
    "photo_b": (
        "An insurance adjuster's evidence photograph of collision damage to the offside rear "
        "quarter of a dark blue saloon car. Daylight, overcast, an ordinary urban street. A "
        "deep crease along the rear door and wing, cracked tail light. Flat documentary "
        "style, no people, no visible number plate, no text."
    ),
    "licence_a_portrait": (
        "A plain head-and-shoulders identity document portrait of an adult woman against a "
        "flat light grey background, evenly lit, neutral expression, facing the camera. "
        "Passport-photo framing. No text, no border, no document furniture."
    ),
}


def _key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k
    cfg = pathlib.Path.home() / ".config/io.datasette.llm/keys.json"
    if cfg.exists():
        k = json.loads(cfg.read_text()).get("openrouter")
        if k:
            return k
    sys.exit("no OpenRouter key: set OPENROUTER_API_KEY or configure `llm keys set openrouter`")


def _generate(client, prompt: str) -> bytes:
    r = client.post(ENDPOINT, json={
        "model": MODEL,
        "modalities": ["image", "text"],
        "messages": [{"role": "user", "content": prompt}],
    }, timeout=240.0)
    r.raise_for_status()
    body = r.json()
    if "error" in body:
        raise RuntimeError(body["error"])
    images = body["choices"][0]["message"].get("images") or []
    if not images:
        # A model that answers in prose instead of pixels exits 200 with no image. Failing
        # loudly here is the difference between "no image" and "an image nobody noticed was
        # missing", which is the distinction this whole corpus is about.
        raise RuntimeError(f"no image in response; text was "
                           f"{body['choices'][0]['message'].get('content')!r}")
    return base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print the prompts and stop")
    args = ap.parse_args()

    if args.dry_run:
        for name, prompt in IMAGES.items():
            print(f"\n=== {name} ===\n{prompt}")
        return 0

    import httpx
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    client = httpx.Client(headers={"Authorization": f"Bearer {_key()}"})

    for name, prompt in IMAGES.items():
        print(f"[{name}] generating...", flush=True)
        raw = _generate(client, prompt)
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.thumbnail((EDGE, EDGE), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        payload = buf.getvalue()
        (OUT / f"{name}.png").write_bytes(payload)
        manifest[name] = {
            "model": MODEL,
            "prompt": prompt,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(
                timespec="seconds"),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
            "pixels": list(img.size),
            "note": ("Synthetic. Generated by the model named above from the prompt named "
                     "above. Depicts nothing real: no real person, vehicle, or incident."),
        }
        print(f"[{name}] wrote {len(payload)}B at {img.size[0]}x{img.size[1]}")

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {manifest_path}")
    print("Now re-run `uv run arcviz-fixtures`: the bundle's SAIDs will change, because the "
          "credentials commit to these bytes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
