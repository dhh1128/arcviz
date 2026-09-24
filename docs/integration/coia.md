# Consuming COIA aliases

Written 2026-09-24 from the specification at `~/code/me/coia`, after a whole session of citing it secondhand from `credential-identity.md` without opening it. Section numbers refer to that spec's `README.md`.

## arcviz is a consumer, and only a consumer

COIA is a convention for the label field wallets and key managers already have — three components in a fixed order, **who**, **role**, **scope** — plus a comma-delimited flag suffix. It is explicitly *"not an identifier, not a namespace, and not a protocol"*.

Generating an alias needs who/role/scope answered by a human about their own context. arcviz has none of that and must not invent it: **the application supplies a lookup and arcviz renders what comes back.**

**§1 forbids the tempting move.** *"An alias improves UX for the person who creates it. It is not a commitment to meaning for anyone else,"* and parsing someone else's alias for meaning is *"a dangerous antipattern"*. So the body is displayed verbatim and never mined — and COIA's `role` component is **not** the same thing as the `role` channel in `tools/describe/describe.py`, which is an edge label. Do not conflate them.

## The flags are the reason this needs code

§6.3 registers ten digits, ordered by seriousness:

```
0 unverified   1 pairwise   2,3 reserved   4 unfit      5 second-hand
6 test         7 do-not-use 8 retired      9 compromised
```

They qualify **the whole alias assertion** — that the identifier is controlled by the party the creator calls `who`, that this party acts in the capacity `role`, within the context `scope` — not merely the subject. Dropping one silently would put a reassuring human name on an identifier its own creator marked as controlled by the wrong party.

**An unrecognized digit MUST be surfaced, not ignored** — it is a warning from a later version of the registry, and its *position* is a severity hint even when its meaning is unknown.

## §6.3 states this project's own thesis, in someone else's spec

> *"**Absence is never a guarantee.** For every flag, absence means only that the flag was not set; it never asserts the negation. An application MUST NOT render an absent flag as a positive assurance."*

So an unflagged alias is **not** a verified one, and a lookup must return three states — no alias, an alias with flags, an alias without — so a render cannot collapse the last two into "fine". This is `AGENTS.md`'s first rule arriving from outside.

## Order of operations is load-bearing

**§6.2: split the flag groups off *before* normalizing the body.** *"The reverse order destroys the delimiter."* §5 normalization discards all punctuation, so normalizing first eats the comma and folds a `,9` compromised flag into the name. `tools/describe/test_describe.py` has a test that spies on the normalizer to prove the order.

Also from §6.2, for a reader: accept `U+3001`, `U+060C` and `U+FF0C` as delimiters besides `U+002C`, and accept any Unicode decimal digit. §6.1: duplicates collapse and groups sort **descending**, so the most serious flag is first; COIA 1.x sorted ascending, and a reader accepts ascending input and canonicalises.

## Conformance, claimed honestly

§3 defines three classes — **Normalizer**, **Generator**, **Matcher**. arcviz claims **none of them**. `tools/describe/coia_reader.py` implements the §6.1/§6.2 flag split, which is the safety-critical half, and all eleven normative parse vectors pass on their flag groups. One vector's *body* is knowingly unchecked because it needs the §5 normalizer, and the test asserts that count is exactly one so the disclaimer cannot go stale.

§5 normalization is 69 further golden vectors and real work. The reference `coia.py` in that repo is the oracle for it; an application that already has a conforming normalizer can pass one in. **Do not name an arcviz file `coia.py`** — that basename belongs to the spec's oracle and implies a conformance claim we disclaim. Ours is `coia_reader.py` for exactly that reason.

The machine-readable vectors are `~/code/me/coia/vectors.json`, keyed by section (`normalize`, `generate`, `reject`, `parse`, `match`, `search`). They are **normative**, and authored from the prose rather than captured from an implementation — where prose and vectors disagree, that is a spec defect to report.

## Three channels, never merged

The alias creator's flags are one speaker. The host's confidence in the **identifier-to-alias binding** is a second. The host's **evidentiary stance** on a credential is a third. They are assertions by different parties about different objects and they can disagree — a host may have vetted an alias its creator flagged `,0`, and may be certain an AID belongs to a diploma mill while crediting nothing it issues.

The name slot carries **identity only**; every assessment rides elsewhere. See `credential-descriptors.md` §1 for the decisions behind that, and [entviz.md](entviz.md) for why flags in particular must stay out of the pill's `label`.

## Where the pieces are

`tools/describe/coia_reader.py` — the reader, `AliasLookup`, `Binding`, `Stance`, `party_view()`, `pill_props()`. `tools/describe/vectors.json` §`channels` — the nine vectors pinning the three-channel separation. Both are prototype and executable specification, not arcviz's implementation; the vectors are the durable artifact.
