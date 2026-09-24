"""Consume COIA aliases. arcviz DISPLAYS them; it never mints, parses or interprets one.

NAMED `coia_reader` AND NOT `coia`, because the spec ships its own `coia.py` -- the normative
oracle at ~/code/me/coia -- and a file of ours with that basename would imply a conformance
claim. arcviz claims none of COIA's three classes (Normalizer, Generator, Matcher).

WHAT COIA IS, read from the spec rather than recalled. A convention for the label field that
wallets and key managers already have -- *who*, *role*, *scope* -- plus a comma-delimited flag
suffix. §1: "an alias improves UX for the person who creates it. It is not a commitment to
meaning for anyone else." So arcviz never mines an alias for meaning, and the COIA `role` is not
the `role` channel in `describe.py`.

THE ALIAS IS SHOWN EXACTLY AS THE LOOKUP RETURNS IT, FLAGS AND ALL. Daniel, 2026-09-24
(D-DCTS), after this module had split flags off into a separate warning chip: "It is the job of
a COIA alias to eliminate or communicate MITM risk, so if you're trying to say that the name
'Jae Park witness' still has MITM risk, we're doing it wrong. This is the job of the interface
that you should be calling to resolve AIDs to aliases." And: "Maybe arcviz should surface some
flags, but not ones on aliases. It is *already* surfacing those flags if it displays coia
aliases by calling the interface that looks them up."

So the host's lookup interface owns the alias and the risk it carries. Whatever it returns --
`jae-park-witness`, or `bob-payee-bitcoin,9` -- is what the pill's label shows, verbatim. An
earlier version of this module parsed the §6.1/§6.2 flag groups, stripped them from the label
and returned them as a separate channel; that is gone, along with its tests, because it put
arcviz in the business of re-adjudicating a risk the interface had already communicated.

What is left is small, and every piece of it is about not collapsing states: no alias versus an
alias, a name withheld here versus none known, and a host that said nothing about a credential
versus a host that said no.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AliasLookup:
    """The argument arcviz takes: the host's interface from identifier to alias.

    Returns the alias string exactly as the host resolved it, or None when the host has none.
    Cached because a render asks about the same AID many times.
    """
    lookup: callable
    _cache: dict = field(default_factory=dict)

    def __call__(self, identifier: str) -> str | None:
        if identifier not in self._cache:
            raw = self.lookup(identifier)
            self._cache[identifier] = raw if raw else None
        return self._cache[identifier]


def pill_props(identifier: str, alias: str | None) -> dict:
    """What to hand `<EntvizPill>` for one AID. Read from entviz-js, not assumed.

    The host-settable slot is `label` (EntvizPill.ts:62), filled by precedence
    (EntvizPill.ts:499-505):

        explicit `label`  >  the gated mnemonic  >  the type text ("cesr key")

    Passing nothing lets entviz's own fallback run, so the pill is never empty. That is what
    "no alias known" must mean, and it is why arcviz passes None and never "" -- an empty
    string is still a label, wins the precedence with nothing in it, and blanks the pill.

    The mnemonic rung is gated on entviz's `corpus` trust posture, which is per value: an AID
    is in the corpus exactly when the host's lookup knows it (D-VTKV; docs/integration/entviz.md).
    """
    return {"value": identifier, "label": alias if alias else None}


# ---------------------------------------------------------------------------------------
# What the host says about a party on a node, kept apart.
#
# THE NAME SLOT CARRIES IDENTITY ONLY. Daniel, 2026-09-24: "naming an issuer isn't supposed to
# be a reputation signal at all... Knowing that a witness testified to fact X in court, and
# knowing that witness X is trustworthy, are radically different questions." So nothing below
# is ever folded into the label.
#
# ONE host judgement remains beside the alias. Daniel, 2026-09-24 (Q-JX0D): "the first and
# second things are the same question. The host is always the creator. Any alias not created by
# a host cannot be returned by the lookup interface." So the alias creator's flags and the host's
# confidence in an alias are one thing, and it is expressed by what the lookup returns. What stays
# separate is the host's stance on a CREDENTIAL, which is about the evidence, not the name.


@dataclass(frozen=True)
class Stance:
    """The host's view of whether to credit one ACDC as evidence. Per ACDC, never per corpus.

    A holder does not trust a presentation uniformly: Provenant trusts GLEIF and itself, and
    does not thereby trust a stranger citing GLEIF's AID. So this hangs off a node's SAID.
    """
    credited: bool | None = None
    reason: str | None = None


def party_view(identifier: str, alias: str | None, *,
               stance: Stance | None = None,
               apply_alias: bool | None = None) -> dict:
    """Everything known about one party as it appears on one node, with nothing merged.

    `apply_alias` is the host's per-(identifier, node) call about whether to USE a known alias
    here. It defaults to showing it, because identification is a precondition for evaluation
    and withholding a name is the more damaging choice.
    """
    known = bool(alias)
    show = True if apply_alias is None else apply_alias
    return {
        "identifier": identifier,
        # Identity only, and verbatim: whatever the host's interface returned, flags included.
        "label": alias if (known and show) else None,
        # Three states, not two: a name withheld here is not the same as a party we cannot
        # name at all, and a viewer should be able to tell them apart.
        "aliasState": ("shown" if known and show
                       else "withheld-here" if known
                       else "none"),
        "credited": stance.credited if stance else None,
        "creditedReason": stance.reason if stance else None,
    }
