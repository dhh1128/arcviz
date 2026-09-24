"""Consume COIA aliases. arcviz READS them; it never mints one.

NAMED `coia_reader` AND NOT `coia`, because the first name was a mistake worth not repeating.
The COIA specification ships its own `coia.py` -- the normative oracle at ~/code/me/coia --
and a file of mine with that basename implies this is an implementation OF the spec, which is
a conformance claim the paragraph below explicitly disclaims. It is a CONSUMER. Nothing here
changes COIA, proposes a change to COIA, or implements its generator, normalizer or matcher.

WHAT COIA IS, read from the spec at ~/code/me/coia rather than recalled. It is a convention
for the label field that wallets and key managers already have -- three components in a fixed
order, *who*, *role*, *scope* -- plus a comma-delimited flag suffix. It is explicitly "not an
identifier, not a namespace, and not a protocol", and §1 is blunt that "an alias improves UX
for the person who creates it. It is not a commitment to meaning for anyone else."

SO ARCVIZ IS A CONSUMER AND ONLY A CONSUMER, and two consequences follow that are easy to get
wrong. Generating an alias needs who/role/scope answered by a human about their own context,
which arcviz does not have and must not invent; the application supplies a lookup and arcviz
renders what comes back. And §1 forbids the tempting move of reading meaning out of somebody
else's alias -- parsing `cecilia-second-violin-vienna-symphony` for a role would be "a
dangerous antipattern" in the spec's words -- so the body is displayed verbatim and never
mined. The `role` in a COIA alias and the `role` channel in `describe.py` are different
things and must not be conflated.

THE FLAGS ARE WHY THIS MODULE EXISTS RATHER THAN A ONE-LINE DICTIONARY LOOKUP. §6.3 registers
ten digits -- 0 unverified, 1 pairwise, 4 unfit, 5 second-hand, 6 test, 7 do-not-use, 8
retired, 9 compromised -- ordered by seriousness, and they qualify the whole alias assertion
rather than only its subject. They are safety-relevant, and dropping one silently would put a
reassuring human name on an identifier the creator has marked as controlled by the wrong
party. `principles.md` P12 already requires the proved-versus-guessed distinction to be
visible; COIA's flags are that distinction, already standardised, already in the data.

AND THE SPEC STATES THIS PROJECT'S OWN THESIS, IN §6.3: "*Absence is never a guarantee.* For
every flag, absence means only that the flag was not set; it never asserts the negation. An
application MUST NOT render an absent flag as a positive assurance." An unflagged alias is
therefore not a verified one, and `AliasLookup` returns three states -- no alias, an alias
with flags, an alias without -- so a render cannot collapse the last two into "fine".

CONFORMANCE, STATED HONESTLY. §3 defines three classes: Normalizer, Generator, Matcher.
arcviz claims NONE of them. It implements the flag split of §6.1/§6.2, which is the
safety-critical half, and it does NOT implement §5 normalization -- that is 69 of the spec's
golden vectors and a real piece of work, and the reference `coia.py` in that repo is the
oracle for it. An application that already has a conforming normalizer may pass one in. The
test suite runs all eleven §6 parse vectors and records which assertions it can make without
a normalizer, rather than claiming a pass it has not earned.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# §6.2: "a reader MUST accept U+3001, U+060C and U+FF0C as group delimiters in addition to
# U+002C, so a user retyping an alias on a CJK or Arabic keyboard is understood."
DELIMITERS = ",、،，"

# §6.3, quoted. Ordered by seriousness ascending, and that ordering "carries meaning: a reader
# encountering an unrecognized digit MAY use its position as a severity hint."
REGISTRY = {
    "0": ("unverified", "doubt about the alias assertion is unresolved"),
    "1": ("pairwise", "for one relationship only; do not share"),
    "4": ("unfit", "technical posture weak for high-stakes use, and not yet accepted"),
    "5": ("second-hand", "imported, restored, synced, or accepted from another party"),
    "6": ("test", "throwaway, test, demo; no real-world consequence"),
    "7": ("do-not-use", "the creator has decided not to transact"),
    "8": ("retired", "no longer in service; historical references still resolve"),
    "9": ("compromised", "positive evidence that the wrong party controls it"),
}
RESERVED = {"2", "3"}


@dataclass(frozen=True)
class Alias:
    """One alias as read. `body` is for display only -- never for parsing (§1)."""
    raw: str
    body: str
    group1: str = ""          # registry digits, §6.3
    group2: str = ""          # private use, §6.1
    # Digits in group1 that this build of the registry does not know. §6.3: "A reader
    # encountering an unrecognized digit in group1 MUST surface it rather than ignore it --
    # it is a warning from a later version of the registry."
    unknown: tuple = ()

    @property
    def flags(self) -> tuple:
        return tuple((d, *REGISTRY[d]) for d in self.group1 if d in REGISTRY)

    @property
    def worst(self) -> str | None:
        """The most serious registry digit, or None. group1 is sorted descending, so it is
        first -- but an unknown digit may outrank everything known and is included by
        position, which is what §6.3 says its position is for."""
        candidates = self.group1
        return candidates[0] if candidates else None

    @property
    def is_flagged(self) -> bool:
        return bool(self.group1 or self.group2)


def _fold_digits(s: str) -> str:
    """§6.2: "a reader MUST accept any Unicode decimal digit." Folds to ASCII."""
    out = []
    for ch in s:
        if ch.isdigit():
            v = unicodedata.digit(ch, None)
            out.append(str(v) if v is not None else ch)
        else:
            out.append(ch)
    return "".join(out)


def parse(raw: str, *, normalize=None) -> Alias:
    """Split an alias into body and flag groups, per §6.1 and §6.2.

    §6.2 is explicit about the order and about why: "A matcher or reader MUST split flag
    groups off *before* normalizing the body. The reverse order destroys the delimiter." §5
    normalization discards punctuation, so normalizing first would eat the comma and silently
    fold a `,9` compromised flag into the name.
    """
    if raw is None:
        raise ValueError("no alias")
    text = _fold_digits(raw)
    parts = re.split(f"[{re.escape(DELIMITERS)}]", text)
    body = parts[0]
    g1 = parts[1] if len(parts) > 1 else ""
    g2 = parts[2] if len(parts) > 2 else ""

    def canon(group: str) -> str:
        digits = {c for c in group if c.isdigit()}
        # §6.1: duplicates collapsed, sorted DESCENDING "so that the most serious flag appears
        # first". A reader accepts ascending input and canonicalises it.
        return "".join(sorted(digits, reverse=True))

    g1, g2 = canon(g1), canon(g2)
    unknown = tuple(d for d in g1 if d not in REGISTRY)
    if normalize is not None:
        body = normalize(body)
    return Alias(raw=raw, body=body, group1=g1, group2=g2, unknown=unknown)


@dataclass
class AliasLookup:
    """The argument arcviz takes: a map from identifier to alias, supplied by the application.

    A plain callable would have done, but the three-state result is the point and a callable
    returning None invites a caller to write `alias or aid` and lose the distinction between
    "this party has no alias" and "this party has an alias the creator flagged as
    compromised". `describe` needs those to render differently.
    """
    lookup: callable
    normalize: callable | None = None
    _cache: dict = field(default_factory=dict)

    def __call__(self, identifier: str) -> Alias | None:
        if identifier in self._cache:
            return self._cache[identifier]
        raw = self.lookup(identifier)
        alias = parse(raw, normalize=self.normalize) if raw else None
        self._cache[identifier] = alias
        return alias


def render(identifier: str, alias: Alias | None, *, elide: int = 10) -> dict:
    """What a renderer needs to draw one party, with nothing collapsed.

    Deliberately NOT a string. `credential-identity.md` records Korir's finding that
    participants read a DID's random-string form as itself the security mechanism, so how much
    raw identifier to show, and whether to show it at all, is a rendering decision this does
    not make.
    """
    if alias is None:
        return {"identifier": identifier, "alias": None, "state": "no-alias",
                "elided": identifier[:elide] + "…" if len(identifier) > elide else identifier}
    return {
        "identifier": identifier,
        "alias": alias.body,
        # Never "verified". §6.3: absence of a flag "never asserts the negation".
        "state": "flagged" if alias.is_flagged else "unflagged",
        "flags": alias.flags,
        "unknown_flags": alias.unknown,
        "private_flags": alias.group2,
        "worst": alias.worst,
        "elided": identifier[:elide] + "…" if len(identifier) > elide else identifier,
    }


def pill_props(identifier: str, alias: Alias | None) -> dict:
    """What to hand `<EntvizPill>` for one AID. Read from entviz-js, not assumed.

    THE SLOT IS `label`, and Daniel's instinct about it was right where mine was wrong. I had
    described the CHARACTERIZATION STRIP (`CESR, Blake3-256`) from entviz's integration guide,
    which belongs to the entviz drawing rather than to the pill chrome. The pill's own
    host-settable slot is `label?: string`, documented as "First-party custom text shown after
    the type (host-set, trusted — unlike the note)", and it does take precedence, in this
    order (EntvizPill.ts:499-505):

        explicit `label`  >  the gated mnemonic  >  the type text ("cesr key")

    so passing nothing lets entviz's own fallback chain run and the pill is never empty. That
    is exactly what "blank when no alias is known" should mean, and it is why arcviz must pass
    `undefined` rather than `""` — an empty string is still a label, and would win the
    precedence with nothing in it.

    WHAT THE MIDDLE RUNG ACTUALLY IS, corrected after getting it wrong. I claimed the
    fallback was the type text and that "a compressed version of the value with ellipses" was
    the hover tooltip. Both halves were wrong. The mnemonic (describe.ts:428) is built from the
    entviz's OWN displayed cells and returns `first…middle…last` for a >=256-bit value -- cell
    texts are chunks of the value itself, so a CESR AID renders as something like
    `EKx4…vq_o…It3`. That IS the raw value with ellipses. bakobo/cesrview is the worked
    example: its StreamPill passes no label and declares `STREAM_TRUST = {posture: 'corpus',
    mnemonic: true, ...}`, and its own test comment reads "The entviz pill never draws the raw
    value; the value lives on cesrview's own wrapper" -- what a reader sees as the value is the
    mnemonic, which is made of the value.

    AND THAT IS THE CONSEQUENCE ARCVIZ HAS TO FACE. The mnemonic rung is gated on the `corpus`
    trust posture, and `credential-identity.md` section 2 records arcviz as WILD by its own
    gate header. So cesrview's pills fall back to a scannable value fragment and arcviz's fall
    all the way to the type text -- "cesr key" -- which is materially worse, and it is a
    consequence of a posture decision rather than of anything about labels. cesrview made the
    opposite call deliberately, with a decision id (e5vk7n), on the ground that a pasted CESR
    stream is a single-origin body of values. Whether a single presented dossier is the same
    kind of thing is Daniel's call and is not made here.

    FLAGS DO NOT GO IN THE LABEL, and this is the part that is security-relevant rather than
    cosmetic. `label` is documented as TRUSTED first-party text, and entviz keeps a separate
    `note` slot for self-declared content precisely so the two cannot be confused -- the source
    comment at EntvizPill.ts:522 says the label is "never the note (self-declared) on the
    pill". A COIA flag is a warning ABOUT the value, not part of anybody's name for it, so
    concatenating `,9` into the label would launder a compromise warning into trusted chrome
    and, worse, make it look like part of the party's name. The flags come back separately here
    for the host to render as its own chrome.
    """
    if alias is None:
        # Not "" -- an empty string is still a label and would win the precedence with nothing
        # in it, suppressing the type text and leaving a pill with no text at all.
        return {"value": identifier, "label": None, "coiaState": "no-alias", "flags": ()}
    return {
        "value": identifier,
        "label": alias.body,
        # Never "verified": COIA §6.3 says absence of a flag "never asserts the negation".
        "coiaState": "flagged" if alias.is_flagged else "unflagged",
        "flags": alias.flags,
        "unknownFlags": alias.unknown,
        "privateFlags": alias.group2,
        "worst": alias.worst,
    }


# ---------------------------------------------------------------------------------------
# The three channels, kept apart.
#
# THREE SPEAKERS, NEVER MERGED. A COIA flag is the ALIAS CREATOR's warning about an
# identifier. A binding judgement is the HOST's view of whether that alias names the party
# controlling the identifier. An evidentiary stance is the HOST's view of whether a credential
# deserves to be credited. They are different assertions by different parties about different
# objects, and collapsing any two of them loses which party is speaking -- which is exactly
# what makes the interesting cases interesting. A host may vet an alias its creator flagged
# unverified. A host may be certain an AID belongs to a diploma mill and credit nothing it
# issues.
#
# AND THE NAME SLOT CARRIES IDENTITY ONLY. Daniel, 2026-09-24: "naming an issuer isn't supposed
# to be a reputation signal at all... Knowing that a witness testified to fact X in court, and
# knowing that witness X is trustworthy, are radically different questions." Identification is
# a precondition for evaluation, not a form of it, so no assessment from any of the three
# channels is ever folded into the label.


@dataclass(frozen=True)
class Binding:
    """The host's view of whether an alias names the controller of an identifier.

    `confident` is a tri-state and the third state is load-bearing: None means the host did not
    say, which is NOT "no". COIA §6.3 makes the same point about its own flags -- "absence means
    only that the flag was not set; it never asserts the negation" -- and the rule generalises
    to every judgement arcviz receives rather than computes.
    """
    confident: bool | None = None
    source: str | None = None       # host-defined; rendered as attribution, never interpreted


@dataclass(frozen=True)
class Stance:
    """The host's view of whether to credit one ACDC as evidence. Per ACDC, never per corpus.

    A holder does not trust a presentation uniformly: Provenant trusts GLEIF and itself, and
    does not thereby trust a stranger citing GLEIF's AID. So this hangs off a node's SAID.
    """
    credited: bool | None = None
    reason: str | None = None


def party_view(identifier: str, alias: Alias | None, *,
               binding: Binding | None = None, stance: Stance | None = None,
               apply_alias: bool | None = None) -> dict:
    """Everything known about one party as it appears on one node, with nothing merged.

    `apply_alias` is the host's per-(identifier, node) call about whether to USE a known alias
    here. It defaults to showing it, because identification is a precondition for evaluation
    and withholding a name is the more damaging choice -- a viewer who knows something about
    that party can no longer apply it. A host may still decline, for reasons that are its own:
    not wanting to reveal which parties it recognises, or holding an alias that is simply wrong
    in this context.
    """
    known = alias is not None
    show = True if apply_alias is None else apply_alias
    return {
        "identifier": identifier,
        # Identity only. No flag digits, no trust marks, no reputation.
        "label": alias.body if (known and show) else None,
        # Three states, not two: a name withheld here is not the same as a party we cannot
        # name at all, and a viewer should be able to tell them apart.
        "aliasState": ("shown" if known and show
                       else "withheld-here" if known
                       else "none"),
        # Channel 1 -- the alias creator speaking about the identifier.
        "coiaFlags": alias.flags if known else (),
        "coiaUnknownFlags": alias.unknown if known else (),
        "coiaWorst": alias.worst if known else None,
        # Channel 2 -- the host speaking about the binding.
        "bindingConfident": binding.confident if binding else None,
        "bindingSource": binding.source if binding else None,
        # Channel 3 -- the host speaking about the credential.
        "credited": stance.credited if stance else None,
        "creditedReason": stance.reason if stance else None,
    }
