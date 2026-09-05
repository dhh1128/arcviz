"""Fixture registration.

A fixture is a zero-argument builder function that either writes its files to
corpus/ and returns a short summary dict, or raises FixtureBlocked with an
honest explanation of why it could not be generated. generate.py collects
both outcomes and reports them -- a documented failure is a valid result, not
an error to hide.
"""

from dataclasses import dataclass, field


class FixtureBlocked(Exception):
    """Raised by a fixture builder that cannot honestly produce its target.

    The message is the blocker, written for a human reading the generation
    report -- e.g. "keripy's Reger.sources cannot traverse edge-groups
    (test_edge_groups_standalone.py), so no verifier-executable working
    edge-group scenario exists; this fixture is syntax/SAID-only."
    """


@dataclass
class Fixture:
    name: str
    fn: callable
    depends_on: list[str] = field(default_factory=list)


_REGISTRY: list[Fixture] = []


def fixture(name: str, depends_on: list[str] | None = None):
    def deco(fn):
        _REGISTRY.append(Fixture(name=name, fn=fn, depends_on=depends_on or []))
        return fn
    return deco


def all_fixtures() -> list[Fixture]:
    return list(_REGISTRY)
