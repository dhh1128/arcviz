"""Deterministic synthetic images, and their real digests.

WHY THIS EXISTS. A credential commits to an image by DIGEST, not by value, so a renderer
that wants to show a thumbnail has to resolve the digest to bytes from somewhere. That
resolution is a separate act which can fail, which means there are three states a render must
tell apart -- no image committed, an image committed and resolved, and an image committed
that does NOT resolve -- and the third must never look like the first. That is this
project's whole thesis arriving in the most visually persuasive element on a card. Before
this module the corpus could not exercise any of it: `accident_photo_a` carried an
`imageDigest` that was a placeholder AID, committing to bytes that had never existed, so
"resolves" and "does not resolve" were indistinguishable because nothing ever resolved.

WHAT THESE IMAGES ARE, AND ARE NOT. They are flat geometric placeholders -- a background
field, a band, a block -- rendered from a fixed palette. They are deliberately NOT
photorealistic, and that is a correctness property rather than an apology for effort. A
fixture corpus that shipped convincing fake photographs of damaged cars and of people's faces
would put images into a public repository that a later reader, or a screenshot, could mistake
for real evidence about real people. A placeholder that is obviously a placeholder cannot be
misread, and it still does the one job the thumbnail question needs: two of them are
distinguishable at 40 pixels, which is the claim being tested.

DETERMINISM. `tools/fixtures/README.md` promises byte-identical output across runs, and an
image encoder is an easy place to break that. Nothing here touches the clock or real entropy:
the pixels come from `determinism._digest` of a label, and the PNG is written with a fixed
zlib level and no ancillary chunks, so there is no embedded timestamp, no gamma chunk and no
encoder version string. The bytes are the same on every machine, and the test suite checks it.

NO NEW DEPENDENCY. This writes PNG with `zlib` and `struct` from the standard library rather
than adding Pillow. PNG's baseline is small enough that a correct encoder is thirty lines,
and `tools/fixtures` already carries keripy's native-extension weight; adding an imaging
stack to draw four rectangles would be a poor trade. The output is verified by decoding it
back with `zlib` in the tests rather than by trusting this code.
"""

import struct
import zlib

from keri.core.coring import Diger

from . import determinism as det

# Flat, high-contrast, and distinguishable from each other when scaled to a thumbnail. The
# point of the palette is separability at small size, not realism.
_PALETTE = {
    "slate": (0x3A, 0x45, 0x52),
    "rust": (0x9C, 0x4A, 0x2F),
    "moss": (0x4A, 0x6B, 0x3D),
    "ochre": (0xB5, 0x8A, 0x2B),
    "plum": (0x5E, 0x3A, 0x5E),
    "bone": (0xE8, 0xE2, 0xD5),
}

WIDTH = HEIGHT = 96


def _chunk(tag: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + tag + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))


def _png(rows: list[list[tuple[int, int, int]]]) -> bytes:
    """Encode 8-bit truecolour PNG. Filter type 0 on every scanline, level 9, no extras."""
    raw = b"".join(b"\x00" + b"".join(bytes(px) for px in row) for row in rows)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw, 9))
            + _chunk(b"IEND", b""))


def synthetic(label: str, *, ground: str, mark: str) -> bytes:
    """A placeholder image for `label`: a ground colour, a band, and a digest-placed block.

    The block's position comes from the label's digest, so two images that share a palette
    still differ visibly -- which matters, because the pair this corpus needs to separate is
    two photographs taken by one adjuster at one scene, where a caller might reasonably pick
    the same colours for both.
    """
    g, m = _PALETTE[ground], _PALETTE[mark]
    d = det._digest(f"image:{label}")
    bx, by = 12 + (d[0] % 36), 12 + (d[1] % 36)
    band_top, band_height = 20 + (d[2] % 24), 10 + (d[3] % 8)
    rows = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if band_top <= y < band_top + band_height:
                row.append(m)
            elif bx <= x < bx + 32 and by <= y < by + 32:
                row.append(m)
            else:
                row.append(g)
        rows.append(row)
    return _png(rows)


def digest(payload: bytes) -> str:
    """The CESR self-addressing digest OF THE ACTUAL BYTES.

    This is the part that makes the resolve/does-not-resolve distinction real rather than
    asserted. `Diger` over the image content means a consumer can recompute the digest from
    the file on disk and get the value the credential committed to -- so a fixture whose bytes
    are deliberately absent is genuinely unresolvable, and one whose bytes are present is
    genuinely verifiable, instead of both being placeholder strings that differ from the file
    in the same way.
    """
    return Diger(ser=payload).qb64
