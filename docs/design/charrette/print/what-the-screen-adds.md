# What the screen version would add — and the proof it adds nothing load-bearing

The premise's discipline: the printed artifact is complete. A screen version is the same sheets, alive. This note lists what interaction would add, and then demonstrates — distinction by distinction — that every truth the design must carry is already carried in ink, so each addition is convenience, not content.

## Additions

1. **Raw/pretty toggle.** On screen, each card gains a toggle to its exact serialized bytes (`.cesr`). On paper the equivalent is an appendix sheet of raw bytes, which these mocks omit for space; the toggle changes formatting only and may never change a state marker (the [affordances](../../../research/affordances.md) AF8 residue already constrains this). Not load-bearing: no matrix distinction lives in the raw view — Rule 9 explicitly *banishes* the one fact (explicit vs default `o`) that only raw bytes carry.
2. **Comparison and walk ceremonies for identifiers.** The printed identifier index guarantees only that repetitions are surfaced; comparing an identifier against outside ground truth is a seeded ceremony (P8: `EntvizCompare`/`EntvizWalk`-class) that a live host can run and paper cannot. Not load-bearing for rendering honesty: the ceremony is the *viewer's* verification act, which P7 says must stay human anyway; paper carries the full strings, which is the maximal honest input to any ceremony conducted elsewhere.
3. **Copy semantics.** Click-to-copy a SAID/AID with provenance intact (AF9). Paper's equivalent is retyping from the full printed string. Convenience only.
4. **Live re-checking, via the host.** On screen, an empty `☐` cell can carry an affordance asking the *host* to perform that check now — a protocol act on the host's intent boundary, never a render side effect (P14, Rule 17). Not load-bearing by construction: arcviz's rendering obligations are identical whether or not the host ever acts, and the printed record is the exact render of the every-channel-empty case that P16 requires to be fully honest.
5. **Reflow, pan, and zoom.** Viewport adaptation, and focus-plus-context piling (AF1) for larger graphs. This is the one addition with teeth: on paper the pile problem cannot even arise, so the screen version must *re-prove* the AF1/HP4 constraints (raised cards keep their edges; occluded budgeted markers survive somewhere). That is an added obligation, not an added truth.
6. **Freshness that moves.** A live view's "as of" recedes visibly; print's is frozen at production and says so. Same vocabulary, one more tick of the clock — Rule 4's markers are already in the printed record's footing.

## The proof, distinction by distinction

Every distinction the three cases must carry, and the ink that carries it with no interaction anywhere:

| Distinction (rule) | Printed carrier |
|---|---|
| H7 vs H8 vs H9 pairwise (Rule 1) | named dashed box vs terminus bar with no box vs manifest slot "none as issued — committed" — differences of kind, in shape and words |
| hole names its blocker; blocked checks unperformable (Rule 10) | blocking SAID printed inside the hole and repeated in the record's "blocked by" column |
| cause never invented (Rule 5) | "why it is not in hand: unknown — no cause was attested," verbatim, at every withheld unit |
| convergence unknowable (SC6 composition) | identical treatment for both fixtures; bracket labeled "one or two — unknowable from this material" |
| vector never scalar; per (check, subject) (Rule 2) | one printed row per (check, subject); two glyphs, defined at point of use; no ✓ exists unearned, no ✗ without host declaration |
| unperformed visible, wall not transient (P3, HP2) | the wall is given its full physical footprint; caption states it is the steady state; no space reserved for "filling in" |
| every positive scoped (Rules 3, 4) | ✓ is *defined* as carrying as-of + tool; revocation phrased horizon-bounded; "no freshness policy supplied" printed as a state |
| no chain roll-up unlabeled (Rule 11) | bona-fides row names ALL-EDGES as arcviz's own host-overridable rule, in the row itself |
| operator suppression / derivation (Rule 9) | identical edge annotations plus one shared footnote; no "(default)" badge anywhere |
| P before V, holder-facing shows nothing (Rule 18) | verifier-facing: the record is printed *inside* the presenter frame; holder-facing (SC3): no presenter ink exists |
| static output is a record, less authoritative (Rules 15, 16, P15) | the strip, the hand-fill print line, "as of production" phrasing, worksheet register; terms band with committed-absence statement and the sizing commitment |
| correlators surfaced, never manufactured (Rules 13, 14, P13) | identical strings print identically with identical marks; index enumerates; severed components stay severed; empty states scoped "in this material" |
| no network on render (Rule 17) | paper, by physics |
| greyscale/small survival (P9, P10) | there is no colour to lose and no hover to miss; every distinction above is shape + placement + words |

Nothing in the left column waits on a click. That is the premise's claim made checkable: take any interaction the screen adds, delete it, and the right column is untouched.

## What the screen must not add

The inversion cuts both ways. A screen version of these sheets may not: put any distinction on hover or behind a collapse without a persistent printed-equivalent signifier (P9/P10); animate the hole or terminus treatments into anything resembling loading; attach a fetch to expansion (Rule 17); or dress the live view's chrome so close to the print's that Rule 15's diff test fails from the other side. The print artifact is the conformance floor: if a screen build cannot produce these sheets from the same render model by flattening alone, the screen build is carrying state where it should not.
