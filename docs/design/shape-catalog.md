# The shape catalog

The first document of the design phase, and the instrument every later design proposal is tested against. It itemizes the layout problems a design must survive — derived from the corpus and the disclosure-state matrix, not invented — so that "this design works" becomes a claim with a test behind it. **Nothing here is a design.** No visual treatment is proposed; where a sentence below seems to describe how something should look, it is describing what a reviewer must be able to *distinguish or verify* in a mock, which is a constraint on the design space, not a point in it.

**Citation discipline.** As in [affordances.md](../research/affordances.md) and [principles.md](../research/principles.md): matrix holdings states are cited as "H*n*", combination rows as "R*n*", indistinguishable pairs as "pair *n*", rendering rules as "Rule *n*", and sections as "§x", all into [disclosure-matrix.md](../research/disclosure-matrix.md); principles as "P*n*" and tensions as "T*n*" into [principles.md](../research/principles.md); affordances as "AF*n*" into [affordances.md](../research/affordances.md); corpus facts cite [corpus-vlei-chain.md](../research/corpus-vlei-chain.md) and [corpus-keripy-examples.md](../research/corpus-keripy-examples.md) by section; fixtures cite [corpus/README.md](../../corpus/README.md) by fixture name. No new spec claim is made here; every spec-grounded statement rides on a locator already verified in the matrix. The dimensional analysis in §(a) and the covering argument in §(f) are this document's own reasoning and are marked **Inference (ours)** where they go beyond the cited sources.

---

## (a) The four dimensions, and which of them actually interact

A case is a point in four dimensions: **topology** (the node-edge structure of the credential DAG), **state occupancy** (which matrix coordinates appear, and on which units), **scale** (one credential, a handful, the pathological capture), and **medium** (mobile, desktop, print/static). The full cross-product is enormous and mostly redundant. The covering set below is small because of five structural claims about where the dimensions do and do not interact. Each claim is falsifiable; refuting one enlarges the set, and a reviewer should attack these before attacking the cases.

**I1 — Card-local occupancy is independent of topology.** The matrix's addressable-unit definition (§a) splits occupancy into states that attach to units *inside* one card — compact/blinded sections and elements (H2, H3, H4, H5), the whole-artifact decoy state (H6), the V vector's per-(check, subject) cells, T's as-of scopes and staleness, X's instance identity, and the content of the P banner — and states that change what the *graph* is. The card-local group does not alter node-edge structure: a card whose `a` section is at H3 occupies exactly the same layout slot as one at H1. A design that renders these states correctly on one card renders them correctly on a card in any graph position, because nothing about the treatment consumes or reads graph context. **Inference (ours)** — the consequence: card-local occupancy is enumerated once each, on the cheapest topology (SC7–SC11), and never multiplied against topologies. One caveat feeds I3: card-local states that spend the prominence budget (T2's four: stale, P-unknown verifier-facing, the conditioned metadata marker, H2-guessable) re-enter the layout problem when many cards carry them at once, because the budget is per-render, not per-card.

**I2 — Graph-structural occupancy interacts with topology, and the interaction is the project's hard core.** H7 (referent named, artifact absent), H8 (edge present, destination hidden), H9 at edge-section granularity (committed no-edge), and H6 occupying a node position each change the graph the layout must draw: a hole is a node (Rule 10), a blinded edge is an edge whose far end is not a place (H8's naive lie — dropping it redraws the topology), and committed absence is *not* a hole and must not read as one (Rule 1's H7-vs-H9 test). Worse, occupancy can make the topology itself unknowable: two H8 edges in one graph may or may not share a far node — whether they converge is exactly what H8's "cannot know" column withholds — so the layout must be able to draw *uncertain convergence*, a state no drawn-graph convention has. **Inference (ours)**, derived from H8's cannot-know cell; no source states the two-edge composition, which is why SC6 carries it explicitly. These states therefore get enumerated in the graph positions that stress them — terminus of a chain (SC2), mid-graph (SC6) — but not against every topology: a hole's layout demand is local to its incident edges, so a design that handles a hole as chain-terminus and as interior node composes node-wise to diamonds and fans (**Inference (ours)**; if a design's hole treatment turns out to consume non-local context, this claim fails and the set must grow).

**I3 — Scale interacts with occupancy through the prominence budget and the honest default; it does not interact with topology beyond what the topology entries already carry.** Deep (depth 4) and wide (fan-in 3 / fan-out 3, per [corpus-keripy-examples.md](../research/corpus-keripy-examples.md) §(b)2) are topology entries, present as SC2 and SC4. What scale adds beyond them is: (1) the budget under multiplication — four budgeted states, finite per render (T2), co-occurring on many cards (SC13); (2) the all-unperformed wall — P3 makes nearly-all-unperformed the honest default V vector of every store-fed credential, so at any scale above one the dominant visual fact of an honest render is a wall of unperformed cells ([affordances.md](../research/affordances.md) §(f)6; SC9, SC13); and (3) filtering — the production capture's bulk is 66.9% signature attachments and ~94%-irrelevant interaction events ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md) §6), so pathological scale is a relevance problem *before* it is a layout problem, and the relevance decision itself makes rendering claims (SC12). The "handful" scale point needs no dedicated case: SC2–SC5 are all 3–5 node graphs.

**I4 — Medium is independent of topology and scale, conditional on a design invariant; it interacts with occupancy at exactly V, T, and P.** P9/P10 already forbid any distinction carried by color alone or available only on hover, in every medium — that is an invariant checkable on any single case, not a per-case axis. Given it, a layout that works at desktop works in print *as a layout* (**Inference (ours)** — conditional on the invariant holding; SC14's greyscale test is where the condition is checked). What medium genuinely changes is epistemics, and only for the live-state axes: static output must re-render every V and P indicator as historical record and carry the terms (Rule 15, Rule 16, P15) — one dedicated case, SC14. The one topology/scale-relevant medium fact is viewport: the binding pair is smallest medium × largest render, so mobile is folded into SC13 rather than multiplied across the set.

**I5 — P is per-render and multiplies with nothing.** Axis P applies once, to the whole render (§a of the matrix), so its three states do not multiply the set; the two viewer-role renders of one artifact (SC10) cover it, plus its static form in SC14 and its budget interaction in SC13.

The consequence of I1–I5: the only dimension pairs needing explicit joint enumeration are (graph-structural occupancy × topology) → SC1, SC2, SC3, SC6; (scale × occupancy) → SC13; (medium × V/T/P occupancy) → SC14; (scale × medium) → SC13. Everything else composes.

---

## (b) The covering set

Fourteen cases. Format per case: the problem in one line; the topology where one applies; the state occupancy in the matrix's vocabulary; the interaction that earns it a place (per §a); the instantiating fixture, or the explicit absence of one; and the design-failure observables — what a reviewer looks for in a mock to fail a design against this case.

### SC1 — Solitary card, committed absence

**Problem:** one credential, no graph — and an absence that is a committed issuance-time fact, not a hole and not an empty state.

**Topology:** a single node. No ASCII needed.

**Occupancy:** all sections H1; the `e` section at H9 (committed absence — the enclosing block is at H1, so absence is warranted); its control twin with `e` present.

**Why in the set:** the scale-1 endpoint, and the negative control for I2 — a design must not require graph chrome to exist before a card is honest, and H9 is the state most likely to be misrendered when there is no graph to have a hole in.

**Fixture:** `optional_edge_absent` (H9, Rule 1, Rule 13) with `optional_edge_present` as control ([corpus/README.md](../../corpus/README.md)).

**Fails if:** the absent-edge render is visually confusable with any hole/loading/error treatment (Rule 1's H7-vs-H9 distinctness); the absence renders as a corpus-level negative — "no linked credentials" phrased as a fact about the world rather than the committed fact "this credential, as issued, has no edge section" (Rule 13); or the two twins are indistinguishable at a glance despite differing in a committed structural fact.

### SC2 — The production chain: deep, fully disclosed, and still incomplete

**Problem:** the *normal* real-world artifact — a linear chain of maximal available disclosure that still cannot be fully verified from what was presented — must render as normal, with its incompleteness legible.

**Topology:**

```
qvi (root) <-- le <-- ecr_auth <-- ecr (presented leaf)     depth 4, no branching
  ^
  (delegation root's KEL: referenced, absent)
```

**Occupancy:** every ACDC section H1 throughout; the delegation root's KEL at H7 (R1 — corpus-attested, [corpus-vlei-chain.md](../research/corpus-vlei-chain.md) §3); V at its honest store-fed default — nearly all cells unperformed, delegation unperformable past the deepest KEL in hand (R0, P3); T with no supplied freshness policy ("no policy supplied" is its own state, Rule 4); P = unknown; identical AIDs recurring across cards (the issuer/subject alternation of §1, the shared `a.i` correlators of §7).

**Why in the set:** the anchor case for I2's terminus position and the baseline every other case perturbs. R1's own warning is the reason it leads: "R1 is the *normal* case, and a design that treats it as exceptional will misrender production traffic."

**Fixture:** `vlei_qvi` → `vlei_le` → `vlei_ecr_auth` → `vlei_ecr` plus the four registry fixtures. The H7 root hole has no fixture of its own — it is produced by the chain's `di` reference having no KEL anywhere in the corpus (structural fixtures carry no KELs at all, [corpus/README.md](../../corpus/README.md) Known limitations), which happens to reproduce the production hole but is not a controllable withholding mechanism; see gap G1.

**Fails if:** the render shows fewer than four tiers, or any delegation affordance without a reach annotation, or the root delegator omitted (Rule 10 — the fixture "must show the root delegator"); anything reads as a positive check outcome without a host-supplied vector (R0's lie, Rule 2's bare-store test); the default-vs-explicit `I2I` difference between the `le` and `auth` edges is visible anywhere outside a raw view (Rule 9(a), pair 2); identical AIDs across cards render non-identically (P13.1, Rule 14); or the overall render carries any "exceptional/degraded" framing — this is what every credential looks like.

### SC3 — Diamond with depth: one ancestor, two path lengths

**Problem:** a shared ancestor reached by paths of unequal length breaks every tree layout, and the two available tree escapes (duplicate the node, drop an edge) are both epistemic lies.

**Topology:**

```
        origin (presented)
        /            \
       B              C
       |              |
       |              F
        \            /
         A  (shared ancestor: depth 2 via B, depth 3 via C-F)
```

**Occupancy:** all H1 — deliberately, so the case isolates topology (production supplied depth without branching, keripy branching without depth; this fixture family exists because neither supplies both, [corpus/README.md](../../corpus/README.md)).

**Why in the set:** the pure-topology stress in I2's composition argument, and the recorded refutation of the commissioning sketch's "tree of cards" ([affordances.md](../research/affordances.md) §(b)1): duplicating A draws one committed artifact as two nodes, misstating what the SAIDs commit to; dropping an edge is H8's naive lie applied to a disclosed edge.

**Fixture:** `diamond_depth_origin`, `diamond_depth_b`, `diamond_depth_c`, `diamond_depth_f`, `diamond_depth_a`.

**Fails if:** A appears twice; any of the five edges is absent; the two occurrences of A's SAID (as edge `n` values in B and F) render non-identically (Rule 14, P13.1); or a focus interaction (AF1's pile) detaches the raised card from either parent or occludes a sibling's marker — the proposal-2 constraints, testable on this fixture set as one pile ([affordances.md](../research/affordances.md) AF1's fixture column names exactly this).

### SC4 — Edge-group fan: operators, weights, and a boundary that is not an edge

**Problem:** an edge-group is a bounded set of edges with its own operator and weights — a layout object with no analogue in plain node-link drawing — and its operator vocabulary must render without becoming a scoreboard.

**Topology:**

```
            +--AND--[ endorser_a ]
  origin ---|
            +--AND--[ endorser_b ]      (working_edge_group: fan-out 2 under one group)

  edge_group_operators: one node, groups carrying AND / OR / AVG / WAVG with per-edge weights
```

**Occupancy:** all H1; the group structure, group-level operators, edge weights, and the unary operators `DI2I` and `NOT` (H1 rows of `di2i_operator`, `not_operator`).

**Why in the set:** the wide/fan topology entry of I3, and the one place the edge vocabulary is exercised at full width. The reference implementation cannot even walk edge-groups (`Reger.sources`/`Verifier.processCredential` throw — [corpus-keripy-examples.md](../research/corpus-keripy-examples.md) §(b)5), so no shipped rendering precedent exists at all for the group boundary.

**Fixture:** `working_edge_group` + `working_edge_group_endorser_a`/`_b`; `edge_group_operators`; `di2i_operator`; `not_operator`. Caveat carried from the corpus: a stock-keripy-fed host never delivers `DI2I`/`NOT` from its store (§e of the matrix), so those two test direct-feed hosts only. `E1E` has no fixture (gap G10).

**Fails if:** a group boundary is indistinguishable from a single edge, or from a visual grouping that carries no commitment (the group has its own SAID — it is structure, not decoration); any operator or weight distinction rides on stroke color alone (P9, P10); an aggregate verdict appears over the group without naming the EGF rule it aggregates under (Rule 11); a `NOT` edge — a *negative* constraint — renders with the same directional affordance as a provenance edge (T4 permits rendering determinate negatives; conflating them with positive provenance is the failure); or weights render as a quality ranking of the far nodes rather than as aggregation inputs (P2's no-scalar rule leaking in through `WAVG`).

### SC5 — Same schema twice: two nodes that must not merge

**Problem:** two structurally near-identical nodes instantiating the identical schema SAID are different committed artifacts, and any layout economy that keys on shape or schema will conflate them.

**Topology:**

```
  household (presented) ---> alice   (schema S)
                 \---------> bob     (schema S, same schema SAID, different d, i, a.i)
```

**Occupancy:** all H1; X singular for each; the discriminating facts are exactly the SAIDs and AIDs.

**Why in the set:** the anti-conflation dual of SC3. SC3 requires two references to *merge* into one node (same SAID); SC5 requires two similar nodes to *stay apart* (different SAIDs, same schema). A design passes both only if node identity is keyed on the SAID and nothing else. The case was a named corpus gap ("A renderer needs to handle two same-shaped nodes that are NOT the same node," [corpus-keripy-examples.md](../research/corpus-keripy-examples.md) Shapes still missing) before the fixture closed it.

**Fixture:** `same_schema_household`, `same_schema_alice`, `same_schema_bob`.

**Fails if:** the two leaves are rendered from one template instance such that any identity-bearing element (SAID pill, `a.i`) is shared or elided "because the cards look the same"; a schema-title label carries the visual weight of node identity (P12 — a schema title is issuer content and a claim, not an identity); or the near-identical pills invite the implied-comparison lie (AF10 — nothing may suggest the two pills were compared and differ, only that they *are* two values).

### SC6 — The hole triptych: three absences that must not share a face

**Problem:** missing referent (H7), hidden destination (H8), and committed no-edge (H9) are pairwise different epistemic states presenting near-identically as "nothing there," and the layout must make each read as itself — including the case where hidden destinations make convergence itself unknowable.

**Topology:**

```
  near ---n:SAID---> [ X ]        H7: referent named, artifact absent — a hole WITH an identity
  near ---(blinded)--> ?          H8: edge committed, destination withheld — an edge to no place
  near                            H9: no edge, committed by the enclosing SAID — NOT a hole

  and the composition:   near ---(blinded)--> ?   near ---(blinded)--> ?
                         (whether the two ?s are one node is unknowable)
```

**Occupancy:** H7 (with the blocking SAID known); H8 (`compact_private_edge`; group form `blinded_edge_group`); H9 (`optional_edge_absent`); C unknowable throughout (pair 1, pair 4 — cause renders unknown, Rule 5); an `o`-less edge whose far node is at H7, making the effective operator undetermined (Rule 9(b)).

**Why in the set:** the sharpest point of I2, and the instantiation of the project's founding hard problem (HP1 below). This is where topology and occupancy stop being separable: the occupancy states *are* topology facts here.

**Fixture:** `compact_private_edge` and `blinded_edge_group` (H8); `optional_edge_absent` (H9); **H7 has no fixture** — it can only be produced by withholding a dependency at load time (load `vlei_ecr` without `vlei_ecr_auth`), and no documented withholding mechanism exists (gap G1). The two-blinded-edges composition has no fixture either (gap G2).

**Fails if:** any two of the three treatments are visually confusable (Rule 1's pairwise test for H7/H8/H9); the H7 hole fails to name its blocking SAID, or any check it blocks reports something other than unperformable (Rule 10); the H8 edge is dropped from the graph, or drawn with a manufactured far node (H8's naive lie both ways); any hole resembles a loading state, spinner, or error (H3's naive-lie family; AF7's constraint that absence-as-signifier must not read as loading); a cause word — "redacted," "withheld," "deleted" — appears with the cause channel empty (Rule 5); two H8 edges are drawn as definitely converging or as definitely separate (**Inference (ours)** per I2 — the honest render must carry "unknown whether these meet"); the `o`-less H7-far edge shows "I2I (default)" (Rule 9's test); or opening any hole triggers network activity (Rule 17).

### SC7 — The card-internal disclosure suite

**Problem:** within a single card, nine-ish distinguishable holdings treatments — the H2/H3/H4/H5 family, Rule 8's four compact-block treatments, the `a`/`A` leakage asymmetry, and the AGID — must coexist in one card layout without collapsing into a generic "hidden."

**Topology:** none — one card; per I1 this suite is enumerated here once and inherited by every other case.

**Occupancy:** H5 (`A` fully compact — an AGID, not a SAID); H3 (blinded commitments, including nested rule-groups); H4 (hidden aggregate elements: count known, labels unknowable); R2 mid-use (one `A` element H1, siblings H4); R3 mid-use (one `a` sub-block H1, siblings label-known-value-hidden — the forced `a.i`/`a.dt` transition included); H2 and the permissive-schema and schema-unresolved treatments (pairs 5 and 11, Rule 8's four); Rule 19's parse-level states.

**Why in the set:** I1's single enumeration point for topology-independent unit states — the dimension the brief warns is most likely to be under-weighted lives largely here and in SC9.

**Fixture:** `bare_agid` (H5, Rule 7); `blinded_rule_group` (H3 nested, Rule 1); `compact_private_edge` doubles from SC6. **No fixture** for: R2 mid-use (gap G4), R3 mid-use (gap G5), H2/permissive-schema/schema-unresolved — Rule 8's test names four fixtures and the corpus has only the H3 leg (gaps G6–G8), Rule 19 negatives (gap G11).

**Fails if:** one "hidden" icon spans any two of H2/H3/H4/H5/H8 (Rule 1; P1's forbid list); a lock or privacy treatment appears on an H2 or protection-undecidable unit (Rule 8's gravest lie); hidden `A` elements carry candidate labels from the schema's `anyOf`, or are positioned in schema order (Rule 6, R2's two lies); R3's leaked sibling labels are hidden — understating what the verifier already learned (Rule 6's other half); the AGID wears a SAID pill or any content-address affordance (Rule 7); or an expansion cue appears on a unit whose content is not in hand — the signifier-without-affordance mismatch (AF2, AF3).

### SC8 — The metadata ambiguity: a card that must wear uncertainty

**Problem:** an empty top-level `u` is simultaneously the spec's metadata-decoy discriminator and keripy's unset default on ordinary issued credentials, so the layout needs a stable *named-ambiguity* state between "issued credential" and "issuer-uncommitted sketch" — and both resolved states besides.

**Topology:** one card (per I1), but note the node-position consequence: an H6 artifact carries edges "as described by the discloser," so an H6 node inside a graph is a node whose *edges* have no issuer commitment either.

**Occupancy:** H6; R5 (metadata offer, pre-agreement); the confusable control — an ordinary issued credential with `u=''` (§B1's H6 note, SKP-F2).

**Why in the set:** the only whole-artifact occupancy state, one of T2's four budgeted states when its conditioned trigger fires, and the case where P5's mirror obligation bites: the anti-lie marker over-fired is itself a lie (Rule 12's amended text).

**Fixture:** `metadata_acdc` (H6, Rule 12). **No fixture** for the control — a keripy-built, fully-issued credential with `u=''` and issuer commitments attached (gap G9).

**Fails if:** the H6 card is chrome-indistinguishable from an issued credential (Rule 12's first test — "the card looks issued," R5); the full non-dismissable marker fires on the empty-`u` control (Rule 12's second test); no distinct "possibly a metadata ACDC" state exists between the two (P5); or the marker is dismissable or corner-badge-sized (P9 — this is a budgeted state precisely because its naive lie reads as fine).

### SC9 — The verification vector, time, and the all-unperformed wall

**Problem:** verification is a per-(check, subject) vector whose honest default is nearly all unperformed, whose "fail" is opt-in, whose every pass carries an as-of scope, and whose staleness must surface without user action — a card-internal layout problem that dwarfs the attribute fields it sits beside.

**Topology:** per I1, card-local — with one deliberate exception: the vector's subject arity requires a two-edge artifact with one far node in hand and one at H7, because that artifact has no honest single value for the edge-constraint check (Rule 2's own further test).

**Occupancy:** V at {pass, unperformed, unperformable} default with per-cell T scopes (P3, P4); host-declared fail on some cells and a declared degraded {pass, not-pass} space on others (pair 10); T stale on one credential under one policy, "no freshness policy supplied" on another (Rule 4's two-policy test); check 7 rendered as the labeled roll-up of check 6 it is (Rule 11 as amended).

**Why in the set:** I1's second enumeration point, and the honest-default half of I3 — a design tested only against cheerful vectors has been tested against a state the substrate cannot produce ([keripy-verification.md](../research/keripy-verification.md) §(d) via P3).

**Fixture:** **none.** No corpus fixture exercises any V or T cell — the KEL/TEL tier is the corpus's stated out-of-scope (§e of the matrix; AF11's fixture column says the same). Needs host-vector and freshness-policy stubs (gap G3).

**Fails if:** any single element summarizes more than one (check, subject) cell, or a two-edge fixture shows one check-6 indicator (Rule 2); a fail glyph appears without a host fail-declaration (Rule 2(c)); unperformed is invisible — absence of a positive reading as fine (the COIA rule via P3); any pass lacks a reachable as-of, or revocation is phrased "not revoked" (Rule 3, P4); an aged fixture's render is pixel-identical to the fresh one, or one global staleness window spans credentials (Rule 4's tests); or the design visibly presumes the all-unperformed wall is transient — e.g., layout space reserved as if cells will fill in (HP2; the wall is the steady state).

### SC10 — One artifact, two renders: the presenter split

**Problem:** the same credential renders verifier-facing (P = unknown: the presenter question must be answered-as-unanswered before the V vector is reachable) and holder-facing (P = self: no presenter indicator may exist at all), and the layout must make these two renders differ structurally, not by a swapped badge.

**Topology:** any; use SC2's chain unchanged — per I5 this case multiplies with nothing.

**Occupancy:** R9 (verifier-facing, P = unknown, all artifact-side states as in SC2); the same rows with P = self; P = attested with Rule 3's full scoping as the third pole.

**Why in the set:** I5's single P case, and one of T2's budgeted states. Pair 12 is the ground: a replayed credential's bytes pass every artifact-side check identically, so the *placement* of the P state relative to the V vector is a layout obligation, not a styling choice (Rule 18: before, and at least as prominently).

**Fixture:** `vlei_ecr` rendered in both modes — the mode is a host declaration, not fixture content (AF17's fixture column).

**Fails if:** in the verifier-facing render, any route reaches the V vector without passing the P state (Rule 18's test); the holder-facing render carries any presenter glyph, positive or negative (Rule 18 — the foreclosed question must not look answered or askable); "presenter verified" appears backed by store presence (pair 12); or the two renders differ only by an element small enough to miss — the difference is budgeted and must be structural (P9, P6).

### SC11 — Text extremes: the rules section dwarfs the data

**Problem:** legal prose 300–500 characters long sits in the same card as data fields of 12–44 characters, must render as prose, must never be truncated into invisibility — because its presence encumbers the reader — and the same slot must survive non-Latin scripts.

**Topology:** card-local (I1); every `vlei_*` card carries it, so SC2 inherits this at scale.

**Occupancy:** `r` at H1 with multi-clause prose ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md) §6: 341–480-character `l` strings against 12–44-character data fields — "a card layout sized for attribute values will be blown out by the rules section alone"); the terms-attach indication of Rule 16; contrast case `blinded_rule_group` (rules present but at H3 — terms whose *content* is withheld while their existence is committed).

**Why in the set:** the corpus's one purely typographic layout pathology, and it is load-bearing rather than cosmetic: the reader of a render is a Disclosee, and a layout that hides the rules to save space is where chain-link confidentiality silently breaks (Rule 16's ground).

**Fixture:** `vlei_ecr` et al. (long disclaimers, Rule 9 fixtures double here); `blinded_rule_group` for the H3 contrast. **No fixture** carries real chain-link-confidentiality clauses — the corpus's own §e names this (gap G12); no non-Latin-script fixture exists (gap G13).

**Fails if:** the rules prose is truncated, summarized, or collapsed with no persistent indication that terms attach (Rule 16 — encumbered data rendering as unencumbered); the card's data fields become unreadable because prose sizing won (the inverse failure — the disclaimer is boilerplate in every production credential and must not drown the 12–44-character facts that vary); the `r` SAID is unreachable from the terms indication (Rule 16); or a blinded rules section reads as "no terms" rather than "terms committed, content withheld" (H3 vs H9 at the section level — Rule 1 again).

### SC12 — Pathological scale: filtering before layout

**Problem:** the real payload is two-thirds signature attachments, its 341 interaction events deduplicate to 107 of which a handful concern the chain, and shared ancestor material arrives duplicated 2–4× — so the design's first act at production scale is a relevance decision, and that decision itself makes claims the render must keep honest.

**Topology:** SC2's four-node chain — buried in a 383,574-byte stream where the chain-relevant fraction is a few percent ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md) §6).

**Occupancy:** as SC2; the occupancy point is what is *not* rendered — omitted attachments and unrelated anchors are corpus-level absences (Rule 13 territory), not committed ones.

**Why in the set:** I3's filtering clause. Scale here is not "more cards"; it is a signal-extraction problem the brief names as prior to layout, and no fixture-sized test would ever surface it.

**Fixture:** **none, and none can be public.** The instantiating artifact is the private capture analyzed in place ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md), preamble — never copied, PII); the corpus fixtures carry no KEL/TEL bulk at all. The synthetic-equivalent spec ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md) "What a synthetic equivalent must reproduce": deliberately bloated mostly-irrelevant KEL, duplicated ancestor events, dozens of unrelated anchors) exists but was never built (gap G14).

**Fails if:** render cost or visual density scales with payload size rather than chain size (the design drew what was present instead of what was relevant); duplicated ancestor events are double- or quadruple-counted anywhere a count or history is shown (§6's dedup warning); the filtered-out volume is invisible in a way that lets "what was presented" read as "all that exists" (Rule 13 — the filter must leave an honest residue, scoped in-this-material); or a "who signed this" view presents the issuer's entire operational KEL as though scoped to the credential (§3's warning).

### SC13 — The budget under multiplication, at mobile width

**Problem:** the prominence budget is per-render and structural; when many cards each carry budgeted states at once, on the smallest viewport, the design must keep the budgeted states loud, distinct, and un-occluded — or admit the budget does not scale.

**Topology:** SC2's chain plus SC3's diamond loaded as one presentation (8–9 cards), at mobile width.

**Occupancy:** every card T-stale under differing per-credential policies (R8); P = unknown verifier-facing (R9); one H6-possibly card (SC8's ambiguity state); one H2-guessable unit (Rule 8); V at the all-unperformed default throughout — i.e., all four of T2's budgeted states co-present, times N cards.

**Why in the set:** the scale × occupancy interaction of I3 and the scale × medium binding pair of I4, in one case. T2 resolves the budget for one card; nothing in the research resolves it for N cards, which is exactly why the case must be in the catalog rather than discovered in a mock review (HP3).

**Fixture:** the fixtures exist (`vlei_*`, `diamond_depth_*`, `metadata_acdc`); the *states* need host stubs — staleness policies and aged as-ofs (gap G3 again). Partially instantiable today.

**Fails if:** any budgeted marker is occluded by pile/scroll/collapse behavior with no surviving trace (AF1's Schechter-grounded constraint — a removed indicator goes unnoticed); the four budgeted states become mutually indistinguishable when co-present (each is budgeted *because* its naive lie is "fine"; a merged "problems exist" treatment is a scalar — P2); staleness markers under different policies render as one uniform state with the policy difference lost (Rule 4's two-policy test at scale); or the design at mobile width demotes any budgeted state to a hover, overflow menu, or off-viewport position with no persistent signifier (P9, P10).

### SC14 — Static output: the same truths with no interaction and less authority

**Problem:** print and export must carry every distinction the live render carries — with no hover, no progressive disclosure, possibly no color — while re-rendering every V and P claim as historical record, carrying the terms, and looking *less* authoritative than the live view.

**Topology:** SC2's chain and SC4's operator card, printed; any card exported.

**Occupancy:** as the source cases, plus the medium shift: every V cell and any P claim as "checked ⟨scope⟩ by ⟨tool⟩" (Rule 15); Rule 16's terms accompaniment; the nine H-state treatments and the edge/operator vocabulary surviving greyscale (P10).

**Why in the set:** I4's one genuine medium × occupancy interaction. No audited ecosystem designed for this moment at all (P15's evidence — a confirmed gap in every prior art stream), so no design will inherit a correct instinct here; the catalog must force the test.

**Fixture:** `edge_group_operators` printed greyscale (AF16's own test fixture); any `vlei_*` card for the live-vs-print diff. The terms half is blocked on the real-CLC gap (G12).

**Fails if:** live and print verification chrome are identical under diff (Rule 15's test); any distinction present live is absent or collapsed in print — including every Rule 1 pairwise distinction and Rule 8's four treatments, in greyscale (P10's ship condition); a live-styled P badge or any live-implying element survives into the export (Rule 15); attribute values export from a non-empty-`r` credential with no terms reference (Rule 16's test); or the static render's overall authority is indistinguishable from the live view's (P15 — the "flash pass" failure).

---

## (c) The named hard problems

Stated now, so no design review discovers them as surprises. Each is a problem the covering set *contains* but does not solve; a design proposal that does not address them head-on is incomplete regardless of how many SC cases it passes.

**HP1 — Laying out a partially-disclosed DAG so the holes read as holes.** The central problem, and it has no prior art: the literature survey found nothing in graph-visualization research addressing a graph whose node *existence* is certain but whose node *content* is not — the nearest analogue is uncertainty visualization of point symbols on maps, explicitly an analogy and explicitly not about graph layout ([prior-art/literature.md](../research/prior-art/literature.md) cluster 3's recorded gap; [maceachren2012semiotics] cited there as analogy only). MacEachren's own finding sharpens the difficulty: different uncertainty categories want different sign-vehicles, and arcviz has at least four categorically distinct not-knowns, so a single greyed-out treatment fails on readability grounds before it fails on honesty grounds (P10's citation of the same). SC6 is the test bench; the H8-convergence sub-problem (topology itself unknowable) is its hardest corner.

**HP2 — The all-unperformed wall.** The honest default render of every store-fed credential is a verification vector that is almost entirely unperformed, everywhere, always (P3) — and the indicator literature says passive indicators habituate away while offering no mechanism that produces comprehension ([affordances.md](../research/affordances.md) §(f)6: "no research answer exists"). The layout question the catalog can state but not answer: how much surface does the steady-state wall occupy, such that it stays true without training dismissal? SC9 and SC13 carry the observables.

**HP3 — The prominence budget does not obviously scale.** T2 allocates structural prominence to four states for a render; SC13 shows all four co-present across many cards on a phone. Either the budget concept survives multiplication (and the design must show how) or prominence at scale needs a different mechanism than prominence at card-count one. The research resolves the single-card budget and is silent on this (**Inference (ours)** that the silence is a gap and not an answer).

**HP4 — The pile and the DAG.** Focus-plus-context (bring a card forward) and topology honesty (a raised card keeps its diamond edges; occluded cards keep their budgeted markers visible somewhere) pull directly against each other, already logged as a design-phase problem ([affordances.md](../research/affordances.md) §(f)4). SC3 plus SC13 jointly instantiate it.

**HP5 — Filtering is a rendering claim.** At production scale the design must omit most of the payload (SC12), and Rule 13 governs what omission may imply: filtered-out material is a corpus-level absence and must not read as nonexistence. "What did the design decide not to draw, and what does that absence say?" is a question every scale-bearing proposal must answer explicitly.

**HP6 — Static honesty with no prior art.** Rule 15/16's re-rendering obligations have no shipped precedent in any audited ecosystem (P15), so SC14 tests designs against rules with no reference implementation anywhere — the highest-variance case in the catalog for that reason.

---

## (d) Fixture gaps — the work-list for `tools/fixtures/`

Every case above that lacks an instantiating fixture, consolidated. G1–G3 were already known ([affordances.md](../research/affordances.md) §(f)7); the rest surface from this catalog's coverage check.

| # | Gap | Serves | Nature |
|---|---|---|---|
| G1 | A documented "withhold this dependency" load mode, so H7 is producible on demand rather than by accident of corpus incompleteness | SC2, SC6 | loader/harness feature, not a new artifact |
| G2 | A fixture with two blinded edges from one node (the convergence-unknowable composition) | SC6 | new fixture; trivial variant of `blinded_edge_group` |
| G3 | Host-input stubs: verification vectors (per-(check, subject), with declared outcome spaces), per-credential freshness policies, aged as-of scopes, P-attestation evidence | SC9, SC10, SC13 | stub schema + sample payloads, not ACDCs — the corpus's KEL/TEL out-of-scope stands |
| G4 | R2 mid-use: an `A` array with one element at H1 and siblings at H4 | SC7 | new fixture (worked-example-attested only, §e of the matrix) |
| G5 | R3 mid-use: an `a` block with one sub-block at H1 and siblings label-known-value-hidden | SC7 | new fixture |
| G6 | H2: a compact block whose SAID-verified schema reserves no `u` | SC7 | new fixture + schema |
| G7 | Permissive-schema undecidable: compact block, schema makes `u` optional (pair 11) | SC7 | new fixture + schema |
| G8 | Schema-unresolved: a fixture whose schema is deliberately not in the corpus ("a schema we do not have," [PLAN.md](../research/PLAN.md) §2C) | SC7 | withholding convention, like G1 |
| G9 | The Rule 12 control: an ordinary issued credential with `u=''` and issuer commitments attached | SC8 | new fixture (keripy emits this shape natively) |
| G10 | An `E1E`-operator fixture (normative on `v1.1`, exercised by both guardianship worked examples, no corpus fixture — §e of the matrix) | SC4 | new fixture |
| G11 | Rule 19 negatives: a field label containing `-`; an expanded-DAG path using `_` | SC7 | requires an invalid-artifact mode the generator currently has no reason to support; low priority, flagged rather than assumed cheap |
| G12 | A rules section carrying real chain-link-confidentiality clauses (the matrix's §e names this; `test_cp_disclosure.py`'s Purpose/Assimilation/SafeHarbor trio is the model) | SC11, SC14 | new fixture |
| G13 | A non-Latin-script fixture ([PLAN.md](../research/PLAN.md) §2C, never built) | SC11 | new fixture |
| G14 | The bloated synthetic equivalent: duplicated ancestor events, dozens of unrelated anchors, attachment-dominated bulk ([corpus-vlei-chain.md](../research/corpus-vlei-chain.md) "What a synthetic equivalent must reproduce") | SC12 | large; requires KEL/TEL simulation the fixture tools deliberately do not do — the one gap that needs a scope decision, not just work |

---

## (e) What the catalog deliberately excludes, and why

Stated loudly, per the brief: a covering set that quietly drops a hard case is worse than a longer one. Each exclusion names its ground; if the ground moves, the case comes back.

**Cross-presentation composition.** No case loads two presentations, joins them, or renders a bulk-instance sibling set side by side. Ground: Daniel Hardman's 2026-09-11 scope ruling — arcviz renders one loaded presentation at a time, correlation within it only ([PLAN.md](../research/PLAN.md) decisions 2026-09-11; AF14 retired). This is an exclusion by decided scope, not by oversight.

**Bulk-instance rendering (X = bulk-instance, R7) as a layout case.** Within one presentation, a bulk instance is one card whose X annotation changes what words are honest ("unlinkable" scoped, never absolute — §B5), not where anything sits; its sibling set never co-renders under the scope ruling above. The state remains a rendering obligation (P13, §B5) — it is excluded from the *layout* catalog because it makes no layout demand distinguishable from SC1's card. **Inference (ours)**; if a design's X treatment turns out to need structural space, this returns as a case.

**KEL/TEL event-structure layout.** The asymmetric rotation arrays, witness configurations, and delegation event sequences of [corpus-vlei-chain.md](../research/corpus-vlei-chain.md) §3/§6 are real rendering pathologies — for a KEL visualizer. arcviz renders the ACDC DAG; KEL facts reach it as V-check outcomes with scopes (SC9) and as the H7 delegator hole (SC2). A future decision to render event history in-card would reopen this.

**The erased-vs-withheld pair as a separate case.** Pair 1's whole content is that the two states share one observable; a dedicated case would demand a distinction the artifact cannot carry, which is precisely what Rule 5 forbids. SC6 renders the shared observable with cause unknown; the attested-cause channel (P16) is exercised there when a host supplies it.

**IPEX exchange-state rendering.** Pair 3's separator (negotiation position, `dp` paths) is an undecided host-interface question (matrix §f question 6; AF-level gap 5 in [affordances.md](../research/affordances.md) §(f)). Until the interface exists, no layout case can be stated falsifiably. The compact-pending vs withheld-final ambiguity itself is covered — as ambiguity — by SC6/SC7's Rule 5 observables.

**Interaction ceremonies and affordance mechanics.** The comparison walk (AF10), copy semantics (AF9), raw/pretty toggle mechanics (AF8) are affordance obligations already specified in [affordances.md](../research/affordances.md); they are design-surface requirements, not DAG-shape cases, and duplicating them here would blur what this catalog tests. Their layout *residue* — e.g., the toggle changing formatting but never state markers — appears inside SC7/SC14 observables where it constrains layout.

**Depth beyond four and width beyond a handful, as separate cases.** [PLAN.md](../research/PLAN.md) §2C named an eight-deep chain; the corpus decided depth 4 discharges the depth-3+ gap ([corpus/README.md](../../corpus/README.md) Known limitations). The catalog follows: hole-plus-chain handling composes along a path (I2), so added depth stresses only viewport and budget, which SC13 owns. If a design's chain treatment turns out to be depth-bounded (e.g., a fixed-tier layout), that is an SC2 failure observable in spirit and the reviewer should treat it as one.

---

## (f) The covering argument, closed

The claim to attack: **a design that survives SC1–SC14 survives every combination the matrix and corpus attest, by construction.** The mechanism is §(a)'s interaction analysis — card-local occupancy composes onto any topology (I1), hole treatments compose node-wise (I2), the budget and viewport own scale (I3), media inherit layouts given the P9/P10 invariant (I4), P touches nothing else (I5). The residue that cannot compose is exactly the fourteen cases.

Coverage of the matrix's own inventory, so omissions are findable:

| Matrix object | Case(s) |
|---|---|
| H1 | everywhere; SC2, SC3, SC5 pure |
| H2, H3, H4, H5 | SC7 |
| H6 | SC8 |
| H7 | SC2 (terminus), SC6 (interior) |
| H8 | SC6 |
| H9 | SC1 (solo), SC6 (against its confusables) |
| R0, R1 | SC2 |
| R2, R3, R4 | SC7 |
| R5 | SC8 |
| R6 | SC6 |
| R7 | excluded — §(e), bulk-instance ground |
| R8 | SC9, SC13 |
| R9 | SC10 |
| Rules 1, 5 | SC1, SC6, SC7, SC8 |
| Rules 2, 3, 4, 11 | SC9 (Rule 11 also SC4) |
| Rules 6, 7, 8, 19 | SC7 |
| Rule 9 | SC2 (determined), SC6 (undetermined) |
| Rule 10 | SC2, SC6 |
| Rules 12 | SC8 |
| Rule 13 | SC1, SC12 |
| Rule 14 | SC2, SC3, SC5 |
| Rules 15, 16 | SC14 (Rule 16 also SC11) |
| Rule 17 | SC2, SC6 |
| Rule 18 | SC10, SC13, SC14 |
| pairs 1, 3, 4 | SC6 (as rendered ambiguity) |
| pairs 5, 11 | SC7 |
| pair 2 | SC2 (suppression side), SC6 (undetermined side) |
| pairs 6, 7, 10 | SC9 (scoped claims, degraded outcome spaces) |
| pair 8 | SC1 (the H9 "cannot know" column at whole-credential level) |
| pair 9 | SC7 (AGID treatment) |
| pair 12 | SC10 |

Every rule and row lands in at least one case, or in a named exclusion with its ground. A reviewer who finds a matrix state, corpus shape, or affordance constraint that maps to no row of this table has falsified the covering claim, and the correct response is a new case, not a footnote.
