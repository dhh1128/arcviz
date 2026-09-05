"""Shared helpers for building fixture ACDCs on top of keri.acdc.messaging.

None of this models a real KERI keystore or KEL: see determinism.py's
module docstring and tools/fixtures/README.md "What this does not model."
Every issuer/issuee AID here is a deterministic blake3-digest placeholder,
not an AID anchored in any inception event.
"""

from keri.acdc.messaging import acdcmap, regcept
from keri.core.coring import Kinds
from keri.core.mapping import Compactor

from . import determinism as det

# A note on `compactify`, because its exact semantics are easy to get wrong
# and getting it wrong silently changes what a fixture discloses:
#
#   compactify=False (the default here, matching keripy's own acdcmap
#   default): whatever shape you hand in for attribute/aggregate/edge/rule is
#   preserved -- every nested `d: ''` placeholder is filled with its real
#   computed digest, but nothing is collapsed into a bare SAID string that
#   you didn't ask for. This is what every fixture below wants UNLESS its
#   whole point is to hide something.
#
#   compactify=True collapses every DIRECT CHILD of the ACDC's own root
#   (i.e. the whole `a`, `e`, and `r` fields themselves, not just their
#   descendants) into bare SAID strings -- this is the spec's "most compact
#   ACDC" (acdc-inventory.md sec.5: "every present top-level section field
#   is its SAID rather than its expanded block"). It is NOT a scalpel for
#   collapsing one specific nested edge while leaving its siblings visible.
#
# To hide exactly one nested block while leaving its enclosing group (and
# everything else) visible -- what H8's Compact Private Edge needs -- run a
# separate keri.core.mapping.Compactor pass over just that sub-tree first
# (compactify=True there collapses every descendant of THAT sub-tree, while
# the sub-tree's own root stays a dict), then hand the resulting mad/string
# in as edge=/rule=/attribute= here with this function's own compactify left
# at its default False. See fx_edges.py::build_compact_private_edge.
#
# A second, sharper trap sits underneath the first one: with compactify=False,
# keripy's SerderACDC._compute() ONLY fills in the top-level ACDC's own `d`.
# It does NOT recurse into a/e/r to fill any nested `d: ''` placeholder --
# those are left as LITERAL EMPTY STRINGS in the returned .sad unless you
# compute them yourself first. (Confirmed by reading serdering.py's
# SerderACDC._compute(): the fully-recursive digest walk only ever populates
# a *deepcopy* used to derive the outer SAID; the returned sad is that
# deepcopy only when compactify=True, i.e. only in the fully-collapsed case.)
# fully_expand() below is the fix: it runs the same Compactor.compact()+
# expand() machinery keripy's own tests use to get a fully-expanded partial
# (tests/spec/acdc/test_acdc_examples.py's `compactor.partials[path]`
# pattern) but automatically picks the most-expanded partial rather than
# requiring the caller to name every leaf path by hand. credential() and
# agg_credential() apply it to every dict-shaped attribute/edge/rule they are
# given, so ordinary callers never need to think about it.


def fully_expand(mad, kind=Kinds.json):
    """Return `mad` with every nested block's real digest filled in, at every
    level, WITHOUT collapsing anything to a bare SAID string that wasn't
    already one. Safe to call on a mad that has no nesting at all (returns it
    with just its own `d` computed) and safe to call on a mad that already
    contains pre-collapsed bare-string children (nothing to expand there, so
    they pass through unchanged).
    """
    compactor = Compactor(mad=mad, makify=True, compactify=True, kind=kind)
    candidates = [k for k in compactor.partials.keys() if k != ('',)]
    if not candidates:
        return compactor.mad  # nothing nested; the compact form IS the expanded form
    fullest = max(candidates, key=len)
    return compactor.partials[fullest].mad


def make_registry(label, issuer):
    """A registry inception ('rip') message. Its .said is the `rd` value."""
    return regcept(issuer, uuid=det.nonce(f"reg:{label}"),
                    stamp=det.stamp(f"reg:{label}"))


def credential(label, *, issuer, schema_said, attrs, issuee=None,
               edge=None, rule=None, top_uuid=None, registry=None,
               compactify=False):
    """An 'acm' ACDC with an Attribute ('a') section.

    attrs is the expanded attribute block content (without d/u/i, which are
    filled in deterministically here unless already present in attrs).
    """
    # Reserved fields first (d, u, i), matching the ordering every keripy
    # worked example uses for attribute blocks, then the caller's own fields.
    attribute = {'d': '', 'u': det.nonce(f"{label}:a")}
    if issuee is not None:
        attribute['i'] = issuee
    attribute.update(attrs)
    attribute = fully_expand(attribute)
    kwargs = dict(israid=issuer, schema=schema_said, attribute=attribute,
                  kind=Kinds.json, compactify=compactify)
    if edge is not None:
        kwargs['edge'] = fully_expand(edge) if isinstance(edge, dict) else edge
    if rule is not None:
        kwargs['rule'] = fully_expand(rule) if isinstance(rule, dict) else rule
    if top_uuid is not None:
        kwargs['uuid'] = top_uuid
    if registry is not None:
        kwargs['regid'] = registry
    return acdcmap(**kwargs)


def agg_credential(label, *, issuer, schema_said, aggregate, issuee=None,
                    edge=None, rule=None, top_uuid=None, registry=None,
                    compactify=False):
    """An ACDC with an Aggregate ('A') section, via the flexible 'acm' map
    form (acdcmap), NOT the fixed-field 'acg' form (acdcagg).

    acdcagg is a fixed-field message type: it unconditionally sets `rd`, `e`,
    and `r` to empty-string/empty-dict sentinels even when the caller never
    asked for a registry, edge, or rule section at all -- `rd: ""` for a
    credential with no registry is a real, distinct H-state (present but
    empty) from H9 (absent), and stamping every aggregate fixture with it
    regardless of whether a registry narrative applies would silently assert
    that state. acdcmap, by contrast, only includes a field when given a
    value for it, matching every other standalone (non-registry-bound)
    fixture in this corpus. Use make_registry()+registry= when a fixture's
    narrative genuinely needs a bound registry.
    """
    kwargs = dict(israid=issuer, schema=schema_said, aggregate=aggregate,
                  kind=Kinds.json, compactify=compactify)
    if edge is not None:
        kwargs['edge'] = fully_expand(edge) if isinstance(edge, dict) else edge
    if rule is not None:
        kwargs['rule'] = fully_expand(rule) if isinstance(rule, dict) else rule
    if top_uuid is not None:
        kwargs['uuid'] = top_uuid
    if registry is not None:
        kwargs['regid'] = registry
    return acdcmap(**kwargs)


def simple_edge(label, *, n, s, o=None, u=None, w=None):
    """A single (non-group) Edge block, order [d, u, n, s, o, w]."""
    e = {'d': ''}
    if u is not None:
        e['u'] = u
    e['n'] = n
    e['s'] = s
    if o is not None:
        e['o'] = o
    if w is not None:
        e['w'] = w
    return e


def simple_rule(l_text, *, u=None):
    """A single (leaf) Rule block, order [d, u, l]."""
    r = {'d': ''}
    if u is not None:
        r['u'] = u
    r['l'] = l_text
    return r
