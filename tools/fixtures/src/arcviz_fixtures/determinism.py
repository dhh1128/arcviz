"""Deterministic entropy for fixture generation.

Every SAID in this corpus is a digest, so any run-to-run change in a `u`
(UUID/nonce) value, an AID placeholder, or a timestamp would change every SAID
above it in a chain and make the corpus non-reproducible. Nothing here calls
`os.urandom` or any other real entropy source. All "random-looking" values are
blake3 digests of a fixed seed string plus a caller-supplied label, so the same
label always produces the same bytes.

This module intentionally does not model a real KERI keystore. AIDs produced
by `aid()` are blake3 digests formatted as CESR self-addressing identifiers
(the same shape a real delegated/multisig AID has), but they are not anchored
in any inception event -- there is no KEL behind them. That is a deliberate
scope decision, not an oversight: see tools/fixtures/README.md "What this
does not model."
"""

import blake3

from keri.core.coring import Diger, Noncer

# Bump this if the derivation scheme ever changes in a way that should
# invalidate previously-generated fixtures (i.e. force everyone to regenerate
# rather than silently comparing old and new SAIDs).
SEED_EPOCH = "arcviz-fixtures-v1"


def _digest(label: str) -> bytes:
    """32-byte blake3 digest of the epoch-scoped label. Deterministic."""
    return blake3.blake3(f"{SEED_EPOCH}:{label}".encode("utf-8")).digest()


def aid(label: str) -> str:
    """A deterministic, blake3-digest-shaped AID placeholder for `label`.

    Structurally indistinguishable from a real self-addressing (delegated or
    multisig) AID -- same derivation code, same length -- but not backed by
    any inception event. Two calls with the same label always return the same
    AID, which is what lets an issuer AID on one fixture equal an issuee AID
    on another (the alternating-issuer/subject shape the vLEI chain needs).
    """
    return Diger(raw=_digest(f"aid:{label}")).qb64


def nonce(label: str) -> str:
    """A deterministic 128-bit UUID/salt (`u` field value) for `label`."""
    return Noncer(raw=_digest(f"nonce:{label}")[:16]).qb64


def stamp(label: str) -> str:
    """A deterministic ISO-8601 datetime stamp for `label`.

    Fixed calendar dates derived from the label so every fixture that needs a
    `dt` gets a stable, distinct-looking value without touching the wall
    clock (`keri.help.nowIso8601()` is real-time and would break
    reproducibility).
    """
    # Spread deterministically over a small fixed range of dates so distinct
    # labels get visually distinct (but still fixed) timestamps.
    n = int.from_bytes(_digest(f"stamp:{label}")[:2], "big")
    day = 1 + (n % 27)
    return f"2026-01-{day:02d}T12:00:00.000000+00:00"
