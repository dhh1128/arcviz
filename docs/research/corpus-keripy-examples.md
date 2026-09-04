# Corpus audit: keripy worked examples (`tests/acdc/`)

Phase 2C-b. Source repo: `~/code/wot/keripy` (working tree on branch `feat-indep-registry-bulk-issuance`; several files audited here are not checked out on that branch and were read via `git show <commit>:<path>`, cited that way below). Nothing in the keripy tree was modified to produce this audit.

## (a) Triage table

Every file currently in `tests/acdc/` (on-disk, branch `feat-indep-registry-bulk-issuance`), plus the two PR-only files Daniel named.

| File | What it demonstrates | Corpus value |
|---|---|---|
| `9120fac25:tests/acdc/test_ward_authz_presentation.py` (PR #1577, not checked out) | Ward-presents guardianship: a 14-year-old holds and presents her own guardian-issued delegated-authorization ACDC. 4-node DAG, 4 edge operators (I2I, E1E×2, NI2I), attenuation check, gated IPEX. | High |
| `a02757671:tests/acdc/test_guardianship_presentation.py` (PR #1530, not checked out) | Guardian-presents guardianship: a parent presents on behalf of a 7-year-old who cannot act. 5-node DAG mixing attributive and aggregative credentials, represented presentation (holder != subject), blindable-registry revocation. | High |
| `test_cp_disclosure.py` | Chain-Link Confidentiality as a credential: a holder-issued bespoke presentation ACDC edging into two source credentials, with a negotiated Rules section (Purpose/Assimilation/SafeHarbor) gating disclosure. Also a second, simpler job-application variant at the bottom of the file. | High |
| `test_bulk_issuance_shared_registry.py` | Bulk-issued private ACDCs, basic form: M index-aligned copies of a 2-node identity+age DAG sharing one registry and one blinded aggregate `B`, spent one-per-verifier for cross-verifier unlinkability. | High |
| `test_bulk_issuance_cocreated_registry.py` | Same scenario, independent-registry variant: each copy gets its own registry, incepted with the set (registry SAID re-derivable from the shared salt). Explicitly "not the SEDI path" — kept as a contrast case. | High |
| `test_bulk_issuance_precreated_registry.py` | Same scenario again, independent-registry variant Utah actually intends to deploy: registries pre-created in bulk, unassigned, with vacuous-update herd anchoring so assignment is unobservable. | High |
| `test_edge_groups_standalone.py` | Edge-GROUP syntax (nested, no `n`, group-level `o` e.g. `"ME"`) and a *defect reproduction*: stock keripy's `Reger.sources` cannot traverse an edge-group, only flat edges. Not a working credential graph. | Medium (syntax reference + a real limitation the renderer should know about) |
| `test_forked_dag_v2_edge_groups.py` | Same edge-group defect, reproduced against `Verifier.processCredential` instead of `Reger.sources`. No real multi-credential scenario. | Medium (same reason) |
| `test_examples.py` | Foundational single-node ACDC mechanics: registry issuance lifecycle, aggregate selective disclosure, attributive partial-disclosure compaction, blindable-registry correlation minimization. No multi-credential chaining. | Medium (baseline disclosure mechanics, no DAG) |
| `test_forked_dag_v2_multiendorse.py` | Wire-protocol probe: does a V2 IPEX grant accept a signature group from a non-sender AID ("Multiply Endorsed Presentation", disc #1555)? One trivial single-claim ACDC, no real shape. | None |
| `test_ipexing.py` | IPEX v2 message-builder/parser/dispatch unit tests (apply/offer/agree/grant/admit/spurn plumbing, nested-artifact validation). Protocol mechanics, not credential shapes. | None |
| `test_messaging.py` | Unit tests for the low-level message builders (`regcept`, `blindate`, `acdcatt`/`acdcagg`/`acdcmap`, section builders). No scenario. | None |
| `test_regbasing.py` | LMDB registry-database store contract (six-store schema). Pure infra test. | None |
| `test_webregbasing.py` | Same store contract for the browser/IndexedDB-backed registry store. Pure infra test. | None |

## (b) High-value examples in depth

### 1. Ward-presents guardianship (PR #1577)

`9120fac25:tests/acdc/test_ward_authz_presentation.py:5-138` (module docstring), scenario at `:13-33`.

Bob (custodial parent, state-recognized guardian) issues Cara (his 14-year-old) a delegated-authorization ACDC; Cara — not Bob — presents it herself to a social-media platform. Four credentials, all v2, all registry-bound:

```
(1) Guardian-as-Citizen         (2) Guardian-as-Guardian
    State -> Bob                    State -> Bob, attr carries CARA's AID
    no edges                        |
        ^                           | E1E (citizen, same subject Bob)
        |__________________________ 
                                     ^
                                     | I2I (authority: Bob held it)
                                     |
                        (4) Ward AuthZ Social
                        Bob -> Cara, in BOB's OWN registry
                            |
                            | E1E (subject, same subject Cara, diff issuer)
                            v
                        (3) Ward-as-Citizen-Ward
                        State -> Cara
                            |
                            | NI2I (encumbrance: points at (2))
                            v
                          (2) [same node as above]
```

ASCII DAG (chain with a fork at the bottom — node 4 is the presented origin, reachable to every other node in one hop or two):

```
        (1) Guardian-Citizen
               ^
               | E1E "citizen"
        (2) Guardian-as-Guardian ---NI2I "guardian"---> (3) Ward-Citizen
               ^                                              ^
               | I2I "authority"                              | E1E "subject"
               +----------------- (4) Ward AuthZ Social -------+
                                   [PRESENTED / origin node]
```

Depth: 2 (from presented node (4) to leaf (1)). Fan-out: node (4) has out-degree 2 (to (2) and (3)); node (2) is pointed to by both (3) and (4) — a genuine reconvergence, not a tree.

**Edges.** Four edges, four distinct operators, each pinned by a JSON-Schema `const` on the edge's `o` field (`test_ward_authz_presentation.py:246-265,978-987`) so a mislabeled operator fails wire validation rather than verifier discretion:
- `authority` I2I: (4)→(2), same-holder (issuer(4)=Bob=issuee(2)) — proves Bob held what he delegated.
- `subject` E1E: (4)→(3), same subject (Cara), different issuers (Bob vs State) — the case I2I would falsely reject.
- `citizen` E1E: (2)→(1), same subject (Bob), same issuer (State) — still E1E because the relation is "one subject," not "one issuer."
- `guardian` NI2I: (3)→(2), different subjects (Cara vs Bob) — untargeted reference, the encumbrance marker.

No edge groups, no weights. E1E is explicitly not yet in the ACDC spec's closed operator set {I2I, NI2I, DI2I, NOT} (`:77-82`) — a pre-#1527 verifier coerces an unknown operator, wrongly rejecting both E1E edges here.

**Disclosure.** Gated IPEX (apply→offer→agree→grant→admit), `:1268-1450`. The `dp` (disclosure-paths) field of the query section is an *ordered list* of `(schemaSAID, [paths])` pairs, ACDC-relative, breadth-first from the origin (`:1290-1350`). The platform asks: from (4) itself, `i`, `a/i`, `a/authz`; from (2), `a/i`, `a/ward`, `a/powers`; from (3), only `a/i`. Node (1) (Guardian-as-Citizen) gets **zero** disclosure paths — it's a DAG node the platform never asks about. The grant discloses (4) expanded, (2) whole (it's a non-selectively-disclosable "disclosed whole" credential), and (3) compacted to the issuee alone (every attribute block reduced to a bare SAID). An honest residual is asserted, not hidden: because (2) is disclosed whole, its `expiryDate` (Cara's 18th birthday) crosses the wire and leaks her birth month/day even though her own citizen credential (3) withholds DOB (`:1429-1434`).

### 2. Guardian-presents guardianship (PR #1530)

`a02757671:tests/acdc/test_guardianship_presentation.py:5-127` (docstring), scenario at `:30-43`.

Bob presents *about* Cara (7-year-old, cannot act) rather than Cara presenting herself — the inverse of #1. Five nodes:

```
       sedi-id (attributive, State->Cara)
           ^
           | E1E "identity"
       sedi-age (aggregative, boolean flags, Endorser->Cara)
                                        birth-certificate (State->Cara, evidences parental right)
                                              ^
                                              | NI2I "authorization"
       sedi-guardian (State->Bob, ward named by attribute+edge) ---NI2I "subject"---> sedi-id [above]
           ^                     ^
           | I2I "authority"     | NI2I "wardAge"
           |                     |
      guardian-presentation (Bob->service) ----NI2I "wardId"----> sedi-id
```

ASCII, cleaner form (star/fan-in at the presentation node, plus a separate identity chain):

```
  sedi-id <--E1E-- sedi-age                 birth-cert
     ^                 ^                        ^
     |(NI2I "subject") |                        |(NI2I "authorization")
     |                 |                        |
     +----- sedi-guardian (Bob, ward=Cara) ------+
     ^  ^         ^
     |  |         | (I2I "authority")
     |  +---------+---- presentation (Bob -> service)
     | (NI2I "wardId")       |
     +------------------------ (NI2I "wardAge" points at sedi-age)
```

Depth 2, fan-in of 3 at `sedi-guardian`, fan-out of 3 at `presentation` — the richest topology in the corpus (a converging DAG, not a simple chain or tree).

**Edge mix — the one place aggregative *and* attributive credentials chain together.** `sedi-id` is attributive (fixed labeled fields, each independently disclosable); `sedi-age` is aggregative (`acg`, an array of 6 boolean age-threshold flags at positions 2..7, issuee at `A[1].i`), chained to `sedi-id` by an E1E identity edge — same subject, different issuers, the second independent use case for E1E in the corpus. Three operators total: I2I (authority), NI2I×2 (ward data — deliberately *not* I2I, since presenter != subject would make I2I impersonation-shaped), E1E (identity, age→core-id).

**Disclosure — aggregate selective disclosure is the star here.** `_age_disclosure` (`:747-756`) reveals only the issuee block and the over-13 flag from a 6-element boolean array; the other five thresholds (16/18/21/55/65) stay as bare SAIDs, so the verifier learns "over 13: true" and nothing about which other thresholds hold — the aggregate form exists precisely so *which* flags are asserted stays hidden (`:71-76`), unlike a labeled attribute set where a revealed field advertises its own name. `sedi-id` is minimally disclosed to issuee-only (binds the ward, nothing else). The module explicitly disclaims identifier-level unlinkability: the ward's stable AID and source-credential SAIDs still travel, so two colluding verifiers could still join on them (`:76-79`) — that gap is what the bulk-issuance examples close.

### 3. Contractually-protected disclosure (`test_cp_disclosure.py`)

`test_cp_disclosure.py:1-65` (docstring), schemas at `:141-380`.

```
   sedi-id (attributive) ---I2I "identity"---> [bespoke presentation]
       ^                                              ^
       | E1E                                          |
   sedi-age (aggregative) ------I2I "age"--------------+
                                        (Alice -> Club, one-time, not registry-bound)
```

A star: one presentation node with two I2I edges down to independent source credentials (age chains to identity via its own E1E, so the full graph is a 3-node diamond-ish shape — presentation at top, age and identity as siblings, plus age→identity beneath). Depth 2.

**Rules section as the load-bearing content.** Three named clauses (`:391-411`): `Purpose` (one-time over-21 + photo-match verification, adapted from the ACDC spec's "Bespoke Issued ACDC" GoodFood example), `Assimilation` (anti-correlation: verifier may not aggregate/correlate/sell the disclosed data), `SafeHarbor` (references a governance-framework SAID for statutory liability safe harbor under Utah 63A-20-701). This is the only example in the corpus that puts negotiated legal terms, rather than only edges, in the trust boundary.

**Disclosure mechanics — the richest `dp` (disclosure-path) documentation in the corpus.** `:990-1043` spells out the full grammar: `dp` is an ordered list of `(schemaSAID, pathPrefix, [paths])` **triples** (not pairs, unlike the guardianship examples) — the middle element is a DAG-absolute path prefix, empty string for the ACDC-relative form used here, or a `/`-delimited absolute route using the virtual `_` path component to cross an edge (`/e/identity/_/a/photo`). A trailing `/` on a path means "the whole node" (used for the origin's Rules section, since the club must read the terms before agreeing); every other path is a scalpel-cut leaf. The example also demonstrates a second, simpler variant at the bottom (`test_job_application_entitlement_presentation_JSON`, `:1632+`): identity + entitlement (a food-handler permit) combined into one holder-issued presentation, same I2I/E1E shape, no CLC Rules section — useful as the "plain combined disclosure, no legal terms" contrast case.

### 4. Bulk issuance (three sibling modules): multi-party structure via replication, not chaining

`test_bulk_issuance_shared_registry.py:1-100`, `test_bulk_issuance_cocreated_registry.py:1-45`, `test_bulk_issuance_precreated_registry.py:1-45`.

Same logical DAG as guardian-presentation's identity pair, replicated M=5 times:

```
verifier 0 (Alcove)      sedi-id_0  <--E1E-- sedi-age_0     (spent once, discarded)
verifier 1 (Dispensary)  sedi-id_1  <--E1E-- sedi-age_1
verifier 2 (Sportsbook)  sedi-id_2  <--E1E-- sedi-age_2
verifier 3               sedi-id_3  <--E1E-- sedi-age_3     (unspent)
verifier 4               sedi-id_4  <--E1E-- sedi-age_4     (unspent)
```

Alice spends copy *k* at verifier *k*; each copy has a unique SAID generated on demand from one shared salt, so two verifiers hold disjoint SAID/edge sets and cannot join on a standing identifier — closing the correlation gap the guardianship example (#2 above) explicitly leaves open. The three modules are the SAME scenario under three registry-topology choices, not three different credential shapes:

- **Shared registry** (`test_bulk_issuance_shared_registry.py`): all M copies share one registry; a single blinded aggregate `B = H(C(b_k for k))` commits the whole set in one issuance event. Simplest, but the shared registry SAID and `B` itself are still cross-context join keys (an honest residual the module names and asserts, `test_partition_across_verifiers_JSON`).
- **Independent, co-created registries** (`test_bulk_issuance_cocreated_registry.py`): each copy gets its own registry, incepted *with* the set, its `rip` entropy derived from the same shared salt — cheap to store (just salt + template) but recognizable as one set to any third party watching the issuer's KEL, because all M registries share one issuance-time datetime stamp.
- **Independent, pre-created registries** (`test_bulk_issuance_precreated_registry.py`): the Utah/SEDI deployment target. Registries are incepted in bulk, unassigned, ahead of any ACDC ("the State just creates say 12M registries... and anchors them all at once with a merkle tree anchor" — Sam Smith, quoted at `:19-23`), then assigned during bulk-update rounds that are mostly vacuous no-op updates mixing many citizens together, so assignment itself is unobservable (herd privacy).

**Edge/disclosure axes are unchanged from #2** — this trio's contribution to the corpus is entirely about *registry and identifier topology for the same 2-node identity/age shape*, not about new edge operators or new disclosure paths. Worth treating as one entry in a design matrix ("how many identifiers/registries does replayed disclosure need to not correlate") rather than three distinct credential shapes.

### 5. Edge groups (`test_edge_groups_standalone.py`, `test_forked_dag_v2_edge_groups.py`) — syntax only, and a real gap

Neither file builds a working multi-credential scenario. Both demonstrate the *shape* the ACDC spec defines for an Edge-group (spec-body.md, "Block Types": an Edge-group MUST NOT carry an `n` field and MAY nest to arbitrary depth) and then show that stock keripy's edge-walking code (`Reger.sources`, `Verifier.processCredential`) assumes every non-reserved label under `e` is a flat edge with an `n` field, so a nested group throws `KeyError: 'n'`:

```json
{"d": "...", "o": "ME",
 "work": {"n": "<farSAID1>"},
 "citizenship": {"n": "<farSAID2>"}}
```

`"o": "ME"` is Sam Smith's proposed "Multiply Endorsed" M-ary edge-group operator (discussion #1555); groups can nest (`test_edge_groups_standalone.py:107-110` builds a two-deep nesting). **This is directly relevant to arcviz**: if a real ACDC ever uses edge-groups (multiple endorsers, M-ary operators), today's keripy reference implementation cannot even walk the structure to gather disclosure artifacts — a renderer built only against examples #1-#4 would never encounter this shape, but the spec permits it and it is a known, currently-broken path.

## (c) Shapes the corpus now covers

- Simple chain with fork (ward-authz: one presented node reaching two others, one of which reconverges).
- Converging DAG / diamond with fan-in 3 (guardian-presentation: multiple nodes point at one guardianship credential, which itself points to two more).
- Star / two-sibling fan-out (cp_disclosure: one presentation edging to two independent source credentials).
- Attributive selective disclosure (individually-blinded nested attribute blocks, reveal-or-withhold per field).
- Aggregative selective disclosure (boolean-flag array, reveal one flag without revealing which others exist or their values) — a materially different disclosure shape from attributive, present in guardianship, cp_disclosure, and all three bulk-issuance modules.
- Compact vs. expanded ACDC (same SAID, edges section collapsed to a bare SAID string vs. inline object) — present in every high-value example.
- Registry-bound vs. not-registry-bound credentials (authority/identity credentials are `rd`-bound for dynamic revocation checks; one-time presentations often are not).
- Blindable/blinded registries for status-check correlation minimization (guardian-presentation Phase 4, bulk-issuance).
- Gated IPEX disclosure exchange (apply→offer→agree→grant→admit) with disclosure paths (`dp`) as an ordered, breadth-first list — including the DAG-absolute-path grammar with the virtual `_` edge-crossing component and the trailing-`/`-means-whole-node convention.
- Negative/attenuation cases: a guardian delegating more than he holds (schema-valid, binding-refused); a mislabeled edge operator (schema-rejected); a guardianship over the wrong ward (well-formed, binding-refused).
- Bulk-issued replicated credentials for cross-verifier identifier partitioning, at three registry-topology tiers.
- Rules-section negotiated terms (Purpose/Assimilation/SafeHarbor) as part of the trust object, not just edges.
- Edge-group *syntax* (nested groups, group-level `o`, no `n`) — though no working multi-credential example exercises it.

## Shapes still missing (to synthesize)

- **A working edge-group / M-ary-operator credential graph.** The two files that touch this are defect reproductions on synthetic literals, not scenarios — no schema-real, disclosure-real example of "credential X requires simultaneous endorsement from Y and Z" exists yet. A renderer needs to decide how to draw a group boundary distinct from a single edge, and nothing in this corpus shows what real attribute/disclosure content sits inside one.
- **A tree with branching depth greater than 2**, or a genuinely long chain (depth 3+). Every example here bottoms out at depth 2 from its presented/origin node. Nothing stresses a renderer's handling of a long provenance chain (e.g., credential A attests B attests C attests D).
- **Weighted or thresholded multi-signature edges** (e.g., an "N of M" edge group, or a weight on individual edges within a group) — the `ME` operator gestures at multi-endorsement but the corpus never shows weights or a threshold count.
- **Redaction after disclosure** (a credential disclosed once, then a field redacted/retracted in a later state) — the corpus shows withholding-at-issue-time and selective disclosure-at-presentation-time, but nothing about revoking a previously-granted disclosure.
- **Cross-schema DAGs with the same schema appearing twice at different positions** — the cp_disclosure docstring explicitly names this case (presenting one's own identity alongside a spouse's, both under the same SEDI schema) as the reason `dp` is a list rather than a dict, but no example actually builds that DAG. A renderer needs to handle two same-shaped nodes that are NOT the same node.
- **A credential with a legitimately empty/optional edge section next to one that's populated** — every schema in the corpus makes its edges `required`; the `dp` path-prefix machinery is explicitly designed to handle optional edges leaving gaps in the breadth-first order (`test_cp_disclosure.py:1023-1027`), but no example exercises that gap.
- **DI2I / NOT operators.** The corpus exercises I2I, NI2I, and the not-yet-ratified E1E extensively, but never DI2I or NOT, both of which are in the ACDC spec's closed operator set.
- **A verified/failed revocation state actually rendered mid-presentation** — blindable registries appear, but the worked examples check status programmatically (`assert`), not as a disclosed visual/data state a renderer would need to distinguish from "issued" or "absent."
- **Multi-hop guardianship (guardian-of-a-guardian) or co-guardianship (two guardians, one ward)** — Sam Smith's own #1550 diagram (referenced in the ward-authz docstring) implies richer guardianship topologies than either PR models; both examples here are single-guardian, single-ward.

## (d) Licensing finding

**keripy is Apache License 2.0** — confirmed by reading `LICENSE` at the repo root (`git show HEAD:LICENSE`; full Apache-2.0 text, boilerplate copyright-notice appendix, no NOTICE file present in the tree). This is a primary-source check, not an inference from the README.

Apache-2.0 permits reproduction, modification, and redistribution, including for a derivative/fixture use, provided: (1) a copy of the license accompanies the redistribution, (2) modified files carry a notice stating they were changed, and (3) any `NOTICE` file content is preserved (keripy has none to preserve). This means test-derived fixture JSON (the credential SADs these examples construct) is very likely reusable in arcviz's `corpus/` with attribution to keripy and a note of what was extracted/modified — but this is a license-compatibility read, not legal advice, and no fixture has been copied as part of this audit per the task's instruction not to copy anything yet. Recommend before actually copying: (a) decide whether arcviz's own license is compatible with carrying Apache-2.0-licensed fixture content forward (arcviz's own license was not checked here), and (b) capture the attribution (repo URL + commit SHA the fixture was derived from, per source) alongside each fixture file, consistent with `EVIDENCE.md` rule 3 (capture locally) applied to code-derived artifacts.
