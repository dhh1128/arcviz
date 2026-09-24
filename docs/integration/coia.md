# Consuming COIA aliases

Written 2026-09-24 from the specification at `~/code/me/coia`, and revised the same day after Daniel ruled on flags (D-DCTS). Section numbers refer to that spec's `README.md`.

## arcviz displays aliases, and does nothing else with them

COIA is a convention for the label field wallets and key managers already have — three components in a fixed order, **who**, **role**, **scope** — plus a comma-delimited flag suffix. It is explicitly *"not an identifier, not a namespace, and not a protocol"*.

Generating an alias needs who/role/scope answered by a human about their own context. arcviz has none of that and must not invent it: **the host supplies a lookup interface from AID to alias, and arcviz shows what comes back.**

**§1 forbids reading meaning out of an alias.** *"An alias improves UX for the person who creates it. It is not a commitment to meaning for anyone else,"* and parsing someone else's alias for meaning is *"a dangerous antipattern"*. COIA's `role` component is also not the `role` channel in `tools/describe/describe.py`, which is an edge label.

## The alias is shown verbatim, flags included

§6.3 registers ten flag digits (`0` unverified through `9` compromised). An earlier version of this note, and of `coia_reader.py`, split those flags off the alias, kept them out of the pill's label, and rendered them as a separate warning. Daniel reversed that on 2026-09-24, after the sample showed `Jae Park witness` with an "unverified" chip beside it:

> It is the job of a COIA alias to eliminate or communicate MITM risk, so if you're trying to say that the name "Jae Park witness" still has MITM risk, we're doing it wrong. This is the job of the interface that you should be calling to resolve AIDs to aliases.

> Maybe arcviz should surface some flags, but not ones on aliases. It is *already* surfacing those flags if it displays coia aliases by calling the interface that looks them up.

So the lookup interface owns the alias and the risk it carries. Whatever it returns, whether `jae-park-witness` or `bob-payee-bitcoin,9`, is what the pill's `label` shows, character for character. arcviz does not split, strip, normalise, or re-render the flags.

## What arcviz still has to get right

**No alias is its own state.** The lookup returns an alias or nothing, and "nothing" must reach entviz as `undefined`, never `""`, so the pill's own fallback runs. See [entviz.md](entviz.md).

**A name withheld on one node is not the same as no name.** The host may decline to apply an alias it knows on a particular node, and `party_view` keeps `withheld-here` distinct from `none`.

**The host is the alias's creator, always.** Daniel, 2026-09-24 (Q-JX0D): *"The host is always the creator. Any alias not created by a host cannot be returned by the lookup interface."* So the creator's flags and the host's confidence in an alias are the same thing, carried by what the lookup returns. arcviz has no separate field for either.

**The name slot carries identity only.** The host's evidentiary stance on a credential is the one judgement that stays separate, and it is never folded into the label; see `credential-descriptors.md` §1.

## Conformance

§3 defines three classes, Normalizer, Generator and Matcher. arcviz claims none of them. **Do not name an arcviz file `coia.py`**: that basename belongs to the spec's oracle and would imply a conformance claim.

## Where the pieces are

`tools/describe/coia_reader.py` holds `AliasLookup`, `pill_props()`, `Stance` and `party_view()`. `tools/describe/vectors.json` §`channels` holds the vectors pinning the separation that remains. Both are a prototype and an executable specification, not arcviz's implementation.
