"""Generate a proposed descriptive label for each ACDC in a DAG.

THE PROBLEM THIS IS, WHICH IS THE ONLY REASON IT IS AN ALGORITHM AND NOT A HEURISTIC SOUP.
`docs/design/description-evaluation-set.md` settles that the description says what part a
credential plays in the argument, and that the DAG rather than the credential is the scope of
evaluation -- so the label is whatever distinguishes this node from the others *in this
bundle*. That is a minimal distinguishing description: given a set of objects and a target,
emit the smallest set of property-value pairs that picks the target out of the set.

LEAD, NOT A SOURCE, and flagged as such because `docs/research/EVIDENCE.md` is binding on
anything claiming to be evidence. This shape is, to my recollection, the Incremental Algorithm
from the natural-language-generation literature on referring expression generation (Dale and
Reiter, early 1990s): walk a fixed PREFERENCE ORDER of properties, add a property to the
description only if it rules out at least one remaining distractor, stop when no distractors
remain, and always include a head noun even when it rules nothing out. I have not read that
paper in preparing this and it is not cited anywhere in `docs/research/`. Treat the attribution
as a lead worth checking before anyone repeats it; the algorithm below stands on its own
whether or not the attribution is right.

WHY THAT SHAPE FITS RATHER THAN MERELY RESEMBLING. Three of this project's own conclusions
fall out of it instead of having to be bolted on. "Show what varies, suppress what is
constant" is exactly the rule that a property which rules out nothing is never added. The
head noun is the category, which we want present for orientation even when every node in the
bundle shares it. And the failure mode is the honest one: when the preference order is
exhausted and distractors remain, the answer is *these are indistinguishable*, which is what
the petition case (five hundred identical endorsements) needs, rather than a label that looks
like an answer.

WHAT IT REFUSES TO PRETEND. Two inputs it genuinely does not have, both reported rather than
guessed:

  - WHICH ATTRIBUTE IS THE SUBJECT. `credential-categories.md` measured that field presence
    tells you what a credential carries, not what it is for, and that nothing in a JSON Schema
    expresses dominance. So the subject field is an input (`subject_fields`), supplied per
    schema by whoever knows; absent it, the component comes back `undetermined` and the
    algorithm falls through to other channels. The unsolved problem stays visible in the
    output instead of being papered over by a field-name guess.
  - WHAT THE TYPE IS CALLED. Zero schemas resolve in this corpus, so the schema SAID is an
    opaque key: it can say "these two are the same type" and cannot say what type. The type
    component therefore carries `name: None` when unresolved, and a renderer that prints
    "Unknown type" is telling the truth where one that omits the component is not.

The output is STRUCTURE, not a finished string. Which components a given render has room for,
and how it renders an unresolvable type or a withheld portrait, is a rendering decision this
does not make. `render_plain` exists to make the tests readable, not to be the answer.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------------------
# Input model


@dataclass(frozen=True)
class Node:
    """One disclosed ACDC, as a renderer would receive it."""
    said: str
    schema: str | None = None
    issuer: str | None = None
    issuee: str | None = None
    attrs: dict = field(default_factory=dict)
    out_edges: dict = field(default_factory=dict)   # label -> target SAID

    @classmethod
    def from_sad(cls, sad: dict) -> "Node":
        a = sad.get("a")
        attrs = a if isinstance(a, dict) else {}
        e = sad.get("e")
        out = {}
        if isinstance(e, dict):
            for label, blk in e.items():
                if label in ("d", "u", "o") or not isinstance(blk, dict):
                    continue
                if blk.get("n"):
                    out[label] = blk["n"]
        return cls(said=sad.get("d"), schema=sad.get("s"), issuer=sad.get("i"),
                   issuee=attrs.get("i"), attrs=attrs, out_edges=out)


@dataclass
class Dag:
    nodes: list[Node]
    # schema SAID -> human type name, where one is known. Empty in arcviz today, because no
    # schema document in the corpus resolves.
    type_names: dict = field(default_factory=dict)
    # schema SAID -> the attribute that names what the credential is ABOUT. See the module
    # docstring: this is an input because nothing in the data determines it.
    subject_fields: dict = field(default_factory=dict)
    # schema SAID -> attribute holding a digest of an attached image, and the set of digests
    # that actually resolve to bytes. A digest that does not resolve is a THIRD state and is
    # reported as such rather than folded into "no image".
    image_fields: dict = field(default_factory=dict)
    resolvable_digests: set = field(default_factory=set)

    def incoming(self, said: str) -> list[str]:
        return sorted(label for n in self.nodes
                      for label, tgt in n.out_edges.items() if tgt == said)


# ---------------------------------------------------------------------------------------
# Channels
#
# A channel maps a node to a hashable value, or to None when the channel does not apply. The
# ORDER is the preference order, and it is the one place the project's grading of evidence
# becomes executable: see description-evaluation-set.md section 6. Role-bearing and
# high-provenance channels come first; channels that discriminate without informing come last.


@dataclass(frozen=True)
class Component:
    kind: str
    value: object
    # True when this component says what the node IS rather than which one it is. Kept so a
    # render can always show the role even if it drops discriminators for space.
    role_bearing: bool = False
    # True when the component's content is the issuer's word rather than anything the
    # machinery binds. P12 requires this distinction to be visible, so it travels with the
    # component rather than being recovered later.
    issuer_claim: bool = False
    # True when this component discriminates by an ABSENCE ("the one with no issuee").
    negative: bool = False
    # True when this component is carried NOT because it discriminates but because the
    # component it accompanies cannot be rendered as text. See `describe_node`.
    text_alternative: bool = False


def _role_stem(label: str) -> str:
    """`licenceA` -> `licence`, `photo2` -> `photo`, `vetting` -> `vetting`.

    Only a trailing index is removed -- a run of digits, or a single trailing capital in an
    otherwise lowercase-started name. `tnalloc` keeps its `c`; `TN` is left alone because
    stripping from an all-caps token would eat meaning rather than an index.
    """
    s = label.rstrip("0123456789")
    if s != label:
        return s or label
    if len(label) > 1 and label[-1].isupper() and not label[:-1].isupper():
        return label[:-1]
    return label


def _relative_date_band(dag: Dag, gap_days: int = 30) -> dict:
    """Cluster issuance dates and name each node's cluster by position, not by value.

    A bare timestamp discriminates but says little. What carried meaning in the live VVP
    dossier is that two credentials sat months before the rest and three sat within 57 seconds
    of each other -- pre-existing background against material assembled for this claim. So the
    channel is the CLUSTER, ordered, and the last cluster is the assembly.
    """
    stamped = []
    for n in dag.nodes:
        raw = n.attrs.get("dt")
        if not isinstance(raw, str):
            continue
        try:
            stamped.append((datetime.datetime.fromisoformat(raw), n.said))
        except ValueError:
            continue
    if len(stamped) < 2:
        return {}
    stamped.sort()
    bands, current = [], [stamped[0]]
    for prev, cur in zip(stamped, stamped[1:]):
        if (cur[0] - prev[0]).days >= gap_days:
            bands.append(current)
            current = []
        current.append(cur)
    bands.append(current)
    if len(bands) < 2:
        return {}
    out = {}
    for i, band in enumerate(bands):
        name = "assembled-for-this-claim" if i == len(bands) - 1 else f"pre-existing-{i + 1}"
        for _, said in band:
            out[said] = name
    return out


def _channels(dag: Dag):
    bands = _relative_date_band(dag)

    def role(n):
        """The referring edge's label, with any instance index stripped.

        THE STRIPPING IS THE POINT, and it was found by running this algorithm rather than by
        reasoning. An edge label names the ROLE an exhibit plays and then, when the referrer
        has two of them, falls back to a bare index: `licenceA` and `licenceB`, `photoA` and
        `photoB`. Left whole, those labels are unique, so the role channel alone distinguishes
        every node and the algorithm stops before it ever consults the issuee, the subject or
        the image -- and emits "as licenceA", which is `ITEM 03` with a longer name, in the
        channel that was supposed to have replaced it. Two exhibits playing the same role are
        not told apart by the referrer having numbered them; they are told apart by what they
        are about. So labels sharing a stem are one role, and the channel correctly declines
        to discriminate between them.
        """
        inc = dag.incoming(n.said)
        if not inc:
            return None
        return _role_stem(inc[0])

    def subject(n):
        fld = dag.subject_fields.get(n.schema)
        if fld is None:
            return None
        v = n.attrs.get(fld)
        return v if isinstance(v, (str, int, float)) else None

    def image(n):
        """The digest, but ONLY when it resolves to bytes.

        A committed image that does not resolve is deliberately not a discriminator. It would
        be an effective one -- "the licence whose photo is missing" picks out exactly one node
        in the accident bundle -- and that is the trap. Whether a portrait was disclosed is an
        accident of this presentation, not a fact about whose licence it is, so describing Bob
        by what the bundle failed to carry would make the label hostage to the disclosure. It
        surfaces instead as an ANNOTATION, which always shows and never discriminates: see
        `_annotations`.
        """
        fld = dag.image_fields.get(n.schema)
        if fld is None:
            return None
        dig = n.attrs.get(fld)
        if not isinstance(dig, str):
            return None
        return dig if dig in dag.resolvable_digests else None

    return [
        # kind,        getter,                     role_bearing, issuer_claim
        ("role",       role,                       True,  True),
        # Image before subject, on both of this project's own criteria. Provenance: the
        # credential commits to the image by digest, so the binding is cryptographic, while
        # the subject field is an unmarked issuer claim that nothing in the credential even
        # identifies as the subject. And directness: two thumbnails of two damaged cars are
        # separated by perception rather than by reading, which is why the pair that nothing
        # structural could separate is separable at all.
        ("image",      image,                      True,  False),
        ("subject",    subject,                    True,  True),
        ("issuee",     lambda n: n.issuee,         False, False),
        ("issuer",     lambda n: n.issuer,         False, False),
        ("when",       lambda n: bands.get(n.said), True, False),
        ("filename",   lambda n: n.attrs.get("filename"),   False, True),
        ("size",       lambda n: n.attrs.get("byteCount"),  False, True),
    ]


# ---------------------------------------------------------------------------------------
# The algorithm


def _annotations(dag: Dag, n: Node) -> list:
    """Facts a viewer needs regardless of whether they help pick this node out.

    The separation matters. A component is there to DISTINGUISH; an annotation is there to
    WARN, and conflating them lets a warning be optimised away the moment it stops being
    discriminating -- which is precisely when there are two withheld portraits instead of one.
    `AGENTS.md` says never let absent, undisclosed, redacted and unverified be mistaken for
    one another or for fine, and a caveat that only appears when it happens to be unique is
    not that.
    """
    out = []
    fld = dag.image_fields.get(n.schema)
    if fld is not None:
        dig = n.attrs.get(fld)
        if isinstance(dig, str) and dig not in dag.resolvable_digests:
            out.append({"kind": "image_committed_not_resolved", "digest": dig})
    return out


def _subject_is_unsaid(dag: Dag, n: Node, components: list) -> bool:
    """True when the finished label says nothing about what this credential is ABOUT.

    Narrower than "no subject field was supplied", which fires on almost everything and is
    therefore noise. For a party-subject credential the issuee IS the subject, and a resolved
    thumbnail shows the subject directly, so neither case has a gap to announce. The gap is
    real only when the label separated this node by something that says nothing about its
    content -- an issuer, a date, a bare absence -- while a sibling of the same type stood
    beside it. Then "I cannot tell you what this one is about" is the honest report, and it is
    the dominance problem surfacing at exactly the node it damages.
    """
    if dag.subject_fields.get(n.schema) is not None:
        return False
    if not any(m.schema == n.schema for m in dag.nodes if m.said != n.said):
        return False
    return not any(c.kind in ("subject", "issuee") and not c.negative
                   for c in components)


@dataclass
class Description:
    said: str
    components: list
    distinguishing: bool
    # Whether the label still picks this node out when the images CANNOT be shown -- a
    # text-only export, a screen reader, a tier too small for a thumbnail. Reported separately
    # because `distinguishing` alone was quietly asserting a modality the label cannot assume:
    # five nodes in the accident bundle came back "shown by its picture", each correct in the
    # data model and each useless to a reader who cannot see the picture.
    distinguishing_as_text: bool = True
    annotations: list = field(default_factory=list)
    # The distractors still standing when the channels ran out. Non-empty means the render
    # must not pretend: these nodes are not separable by anything available.
    indistinguishable_from: list = field(default_factory=list)

    def to_dict(self):
        return {
            "said": self.said,
            "distinguishing": self.distinguishing,
            "indistinguishable_from": self.indistinguishable_from,
            "distinguishing_as_text": self.distinguishing_as_text,
            "annotations": self.annotations,
            "components": [{"kind": c.kind, "value": c.value,
                            "role_bearing": c.role_bearing,
                            "issuer_claim": c.issuer_claim,
                            "negative": c.negative} for c in self.components],
        }


def _select(dag: Dag, target: Node, skip: tuple = ()) -> tuple:
    """Run the incremental selection, optionally with some channels unavailable.

    `skip` is what makes the text-only question answerable: run the same algorithm with the
    image channel removed and see whether the distractor set still empties. That is a real
    second answer rather than a guess about one, and it costs one extra pass.
    """
    distractors = [n for n in dag.nodes if n.said != target.said]

    # The head. Always present, even when every node shares it, because the viewer's first
    # question is what KIND of evidence this is and a description that omits it to save space
    # has optimised away the orientation it exists to give. `name` is None when no schema
    # document resolves, which is every schema in this corpus today.
    components = [Component(kind="type",
                            value={"schema": target.schema,
                                   "name": dag.type_names.get(target.schema)},
                            role_bearing=True)]
    # The head is also the first discriminator: anything of another type is already ruled out.
    distractors = [d for d in distractors if d.schema == target.schema]

    deferred_negatives = []
    for kind, get, role_bearing, issuer_claim in _channels(dag):
        if kind in skip:
            continue
        if not distractors:
            break
        mine = get(target)
        if mine is None:
            # An absence can discriminate -- "the one with no issuee" -- but it names nothing,
            # so it is held back and only spent if the positive channels run out.
            if any(get(d) is not None for d in distractors):
                deferred_negatives.append((kind, get, role_bearing, issuer_claim))
            continue
        remaining = [d for d in distractors if get(d) == mine]
        if len(remaining) == len(distractors) and not role_bearing:
            # Rules nothing out: the suppress-constants rule. It applies only to channels that
            # say WHICH one this is. A role-bearing channel says what part the node plays, and
            # that is the locked goal rather than a discriminator -- "one of the two licences"
            # is exactly what a viewer needs even though, being one of two, it separates
            # nothing. Generalising the head-noun rule rather than special-casing the head.
            continue
        components.append(Component(kind=kind, value=mine, role_bearing=role_bearing,
                                    issuer_claim=issuer_claim))
        distractors = remaining

    for kind, get, role_bearing, issuer_claim in deferred_negatives:
        if not distractors:
            break
        remaining = [d for d in distractors if get(d) is None]
        if len(remaining) == len(distractors):
            continue
        components.append(Component(kind=kind, value=None, role_bearing=role_bearing,
                                    issuer_claim=issuer_claim, negative=True))
        distractors = remaining

    annotations = _annotations(dag, target)
    if _subject_is_unsaid(dag, target, components):
        annotations.append({"kind": "subject_undetermined"})
    return components, distractors


def describe_node(dag: Dag, target: Node) -> Description:
    components, distractors = _select(dag, target)

    # THE LABEL IS THE UNION OF WHAT EACH MODALITY NEEDS, which is the general form of a
    # narrower fix that did not survive its own test. The first attempt appended the subject
    # whenever an image discriminated, and then reported text-only separability from a SECOND,
    # unrelated selection -- so the flag described a label the render would never see. Running
    # the selection again with the image channel unavailable, and carrying whatever it needed
    # that the first pass did not, makes the emitted label the one both flags are about.
    text_components, text_only_left = _select(dag, target, skip=("image",))
    have = {(c.kind, str(c.value)) for c in components}
    for c in text_components:
        if (c.kind, str(c.value)) not in have:
            components.append(Component(kind=c.kind, value=c.value,
                                        role_bearing=c.role_bearing,
                                        issuer_claim=c.issuer_claim, negative=c.negative,
                                        text_alternative=True))

    annotations = _annotations(dag, target)
    if _subject_is_unsaid(dag, target, components):
        annotations.append({"kind": "subject_undetermined"})
    return Description(said=target.said, components=components,
                       annotations=annotations,
                       distinguishing=not distractors,
                       distinguishing_as_text=not text_only_left,
                       indistinguishable_from=sorted(d.said for d in distractors))


def describe(dag: Dag) -> list:
    return [describe_node(dag, n) for n in dag.nodes]


# ---------------------------------------------------------------------------------------
# Rendering, for tests and for reading output by eye. NOT the answer to how this should look.


def render_plain(d: Description, names: dict | None = None) -> str:
    names = names or {}

    def short(v):
        s = str(v)
        return names.get(s, s[:10] + "…" if len(s) > 12 else s)

    parts = []
    for c in d.components:
        if c.kind == "type":
            parts.append(c.value.get("name") or f"type {short(c.value.get('schema'))}")
        elif c.negative:
            parts.append(f"with no {c.kind}")
        elif c.kind == "image":
            parts.append("shown by its picture")
        elif c.kind == "when":
            parts.append(c.value)
        elif c.kind == "role":
            parts.append(f"as {c.value}")
        else:
            parts.append(f"{c.kind} {short(c.value)}")
    out = ", ".join(parts)
    if not d.distinguishing_as_text:
        out += "  [NOT UNIQUE WITHOUT THE PICTURES]"
    for a in d.annotations:
        out += ("  [picture withheld]" if a["kind"] == "image_committed_not_resolved"
                else "  [subject undetermined]")
    if not d.distinguishing:
        out += f"  [NOT UNIQUE: {len(d.indistinguishable_from)} other(s) identical]"
    return out


def load_corpus_dag(corpus_dir, names, **kw) -> Dag:
    """Build a Dag from arcviz corpus fixture files."""
    from pathlib import Path
    corpus_dir = Path(corpus_dir)
    nodes = [Node.from_sad(json.loads((corpus_dir / f"{n}.json").read_text())) for n in names]
    return Dag(nodes=nodes, **kw)
