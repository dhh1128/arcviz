# Corpus note: a real vLEI ECR credential chain

The source analyzed here is a 383,574-byte CESR stream at `/home/daniel/xfer/credential.cesr`, outside this repository, containing a real vLEI Engagement Context Role (ECR) credential and its full dependency chain — real personal and organizational data about a real person and a real legal entity. It was read and parsed in place with a throwaway Python script (`json.loads` on each CESR-framed JSON message, located by scanning for `{"v":"..."}` version strings and using the declared size to slice exact frame boundaries); nothing from it was copied, and no excerpt or derivative of it exists anywhere else. Every SAID and AID quoted below is a content-addressed digest or an autonomic identifier, not personal data, and is needed to describe topology. No attribute value, name, LEI, role title, or timestamp value from the payload appears anywhere in this document — only field paths, types, and lengths. Where a claim rests on the vendored ACDC spec (`~/code/me/kswg-acdc-specification/spec/spec-body.md`), the line number is cited directly since this document does not touch `refs/sources.yaml`.

## 1. The credential DAG

Four ACDCs, in a strict linear chain (a path, not a branching DAG — every node has exactly one child and at most one parent within this payload):

| # | SAID | Schema SAID | Role (inferred) | Issuer AID | Subject (`a.i`) | Edge to parent |
|---|---|---|---|---|---|---|
| 0 | `EMatUqz_u9BizxwOc3JishC4MyXfiWzQadDpgCBA6X9n` | `EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao` | QVI | `EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS` | `ED88Jn6CnWpNbSYz6vp9DOSpJH2_Di5MSwWTf1l34JJm` | none (root) |
| 1 | `EB9yGbWXOn_MhTQsHltftAsNrlWAxgedMPIQl4rg6C1e` | `ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY` | LE (Legal Entity) | `ED88Jn6CnWpNbSYz6vp9DOSpJH2_Di5MSwWTf1l34JJm` | `EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL` | `qvi` → #0 |
| 2 | `EAwE2c_fLhqwUhtWgf-MT3cFjdpebyU-Yv1ZhNPbCo1T` | `EH6ekLjSr8V32WyFbGe1zXjTzFs9PkTYmupJ9H65O14g` | QVI ECR AUTH | `EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL` | `ED88Jn6CnWpNbSYz6vp9DOSpJH2_Di5MSwWTf1l34JJm` | `le` → #1 |
| 3 (leaf) | `ENLcB7zi4wYyQ2Q1aGSyGsOsKMxugyyb1IOgG4cSW44s` | `EEy9PkikFcANV1l7EHukCeXqrzT1hNZjGlUk7wuMO5jw` | ECR | `ED88Jn6CnWpNbSYz6vp9DOSpJH2_Di5MSwWTf1l34JJm` | `EBrBTKbvent0yq_rEHzaHNFx0CsNMEsuwOHNjSkAa-c2` | `auth` → #2 |

Depth 4, 3 edges — the "3 edge sections" from reconnaissance is confirmed exactly (one edge group per non-root credential, each containing a single edge). The role labels (QVI / LE / QVI ECR AUTH / ECR) are not recalled from training data — each is directly evidenced inside the payload itself: the edge names (`qvi`, `le`, `auth`) name what they point at, and the `r.privacyDisclaimer.l` boilerplate in credentials #2 and #3 literally names "QVI ECR AUTH vLEI Credentials" and "Holders as Issuees of an ECR vLEI Credential" respectively. This is a textbook vLEI issuance cascade: GLEIF's delegate issues the QVI credential to a Qualified vLEI Issuer; the QVI issues an LE credential to a legal entity; the LE issues an ECR-AUTH credential back to the QVI authorizing it to act on the LE's behalf; the QVI then uses that authorization to issue the leaf ECR credential to an individual person's own AID. Note the issuer/subject reversal in the middle: credential #1's subject and credential #2's issuer are the same AID (the LE), and credential #2's subject and credential #3's issuer are the same AID again (the QVI) — the chain alternates who is speaking.

The leaf's own AID, `EBrBTKbvent0yq_rEHzaHNFx0CsNMEsuwOHNjSkAa-c2`, is the only AID in the whole payload with a plain (non-delegated) `icp` and a single (not weighted, not multi-sig) signing key — consistent with this being the individual credential holder's personal keystore, distinct from every organizational AID in the chain, all of which are delegated and multi-sig.

## 2. Every edge, in detail

All three edges use the same shape: a one-member edge-group (`{"d": <edge-group SAID>, "<name>": {"n":..., "s":..., ["o":...]}}`). No edge group carries an `o` (m-ary operator, e.g. `AND`/`OR`) because each group has only one member — the m-ary default of `AND` over one member is trivial and unobservable. No edge or edge-group carries `w` (weight) or `u` (UUID) at any level; the `WAVG` weighted-average operator (`kswg-acdc-specification/spec/spec-body.md:1081,1108`) never appears.

- **Edge `qvi`** (in #1, LE → QVI): fields `n` (far SAID) and `s` (far schema SAID) present, no `o`. Far node is targeted (has an issuee), so per spec the effective operator defaults to `I2I` even though it's not written (`spec-body.md:1197-1205`): #1's issuer must equal #0's issuee. Verified directly: #1's issuer AID equals #0's `a.i`.
- **Edge `le`** (in #2, ECR-AUTH → LE): same shape, no `o`, same implicit default-`I2I` relationship, and it holds: #2's issuer equals #1's `a.i`.
- **Edge `auth`** (in #3, ECR → ECR-AUTH): same shape but with `o: "I2I"` **explicit** this time, even though the far node is equally targeted and the default would be identical. This is the one real inconsistency worth carrying into arcviz: two schemas in the same family write the default operator, one doesn't, and a renderer showing "operator" as a badge must treat an absent `o` and an explicit `I2I` on a targeted edge as the same fact, not as "unspecified" vs "specified."

Every edge's `s` (far schema SAID) is present and matches the far node's actual top-level `s` — schema referencing is used consistently, never omitted, across all three edges. No edge is expressed in the compacted bare-SAID form the spec allows for an edge block (`spec-body.md:27`); all three are always full inline objects. No edge or edge-group is itself blinded or SAID-only.

## 3. The KEL context

Verified counts match reconnaissance exactly: 1 `icp`, 7 `dip`, 4 `drt`, 341 `ixn`, plus 4 `vcp` (registry inceptions) and 4 `iss` (TEL issuances) — 365 KERI/ACDC frames total.

Delegation structure (three organizational AIDs, all delegated from one root AID that is referenced but never itself present in this payload):

```
EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2  (root delegator — referenced by "di" only, its own icp/dip is NOT in this payload)
 ├─ dip → EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS   (issuer of #0, the QVI credential)
 │        └─ dip, then drt at sn 18 → ED88Jn6CnWpNbSYz6vp9DOSpJH2_Di5MSwWTf1l34JJm  (issuer of #1 and #3; subject of #0 and #2 — this is the QVI's own AID)
 └─ dip → EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL   (issuer of #2; subject of #1 — the LE's AID)
```

The QVI's own AID (`ED88Jn6Cn...`) rotates once, at sequence 18, from a 4-key weighted scheme (each key weight `1/2`, i.e. any 2 of 4 suffice) to an 8-entry key list where the 4 prior keys are retained at weight `0` (present but inert) alongside 4 new keys again at weight `1/2` — while the next-key commitment (`nt`/`n`) only pre-commits to 4 digests, not 8. Current-key-count and next-digest-count diverge across a rotation; a renderer that assumes they line up will misrender the rotation. All organizational AIDs use fractional weighted multi-sig (`kt`/`nt` arrays of `"1/2"` strings, satisfied when the weighted sum reaches 1) with 5 witnesses and a witness threshold (`bt`) of 4; the person's own `icp` is a plain single-key, single-witness-threshold-of-5 AID.

Every one of the four registries is configured with `"c": ["NB"]` (No Backers), `"bt": "0"`, `"b": []` — the simplest TEL variant, no backer receipts. No `rev`/`brv`/`bis` event of any kind appears: as captured in this payload, none of the four credentials has been revoked.

The 341 `ixn` events are overwhelmingly **not** about this chain. Only 20 anchor seals (across the whole payload) reference one of this chain's 4 `vcp`/`iss` TEL-event SAIDs — the other ~94% of interaction events belong to unrelated activity by the same three prolific issuer AIDs (95 distinct registry/credential AIDs show up as seal targets in total). The busiest AID, the QVI's `ED88Jn6Cn...`, carries 272 `ixn` events but only a handful relate to this chain. **A renderer that wants "who signed this" must expect to receive, and filter, the issuer's entire operational KEL — not a KEL scoped to the credential.**

The payload also duplicates shared ancestor events wholesale: of the 341 `ixn` frames only 107 are distinct by SAID (most repeat 2× or 4×), the 7 `dip` frames cover only 3 distinct SAIDs, and the 4 `drt` frames are 4 copies of one event. This is consistent with each credential's full chain-of-custody (KEL+TEL+ACDC) having been assembled independently and then concatenated, so ancestor material common to two credentials appears once per credential that needed it. **A parser must deduplicate by SAID before counting or rendering, or it will double- or quadruple-count shared history.**

Delegation approval is only partially checkable from this payload: `EINmHd5g7iV...`'s own `ixn` events do anchor `ED88Jn6Cn...`'s `dip` and `drt` (seal digests matching those event SAIDs were found), but the root `EDP1vHcw...`'s KEL — which would need to anchor `EINmHd5g7iV...`'s and `EFcrtYzHx11T...`'s own `dip` events — is absent entirely. **The chain's delegation claims cannot be fully verified from this payload alone; the root's KEL has to be fetched separately.**

## 4. Field inventory as actually used

Against the top-level ACDC field table (`spec-body.md:18-28`) and the Edge-group/Edge tables (`spec-body.md:1078-1147`):

Used, every instance: `v`, `d`, `i`, `s` (always a bare schema SAID, never an inline schema block), `a` (always an inline object, never a bare SAID), `r` (always inline). Edge: `n`, `s` on every edge.

Used, sometimes: `u` (top-level UUID salt) appears only on credential #3 (the leaf ECR), not on #0/#1/#2; `o` (edge operator) appears only on the one `auth` edge. `a.u` (an attribute-block-level salt) likewise appears only inside #3's attribute block.

Never observed anywhere in this chain: `A` (Attribute Aggregate / selectively-disclosable block, `spec-body.md:26`), `w` (edge weight) and the `WAVG` operator, `u` at the edge or edge-group level, inline (non-SAID) schema blocks, a bare-SAID (compacted) `a` or `e` block, and any BLID/blinding mechanism (`spec-body.md:2053-2201`) or TEL `b` (blinded-attribute-block SAID, `spec-body.md:1979`). None of the `NI2I` or `DI2I` edge operators appear either — every edge in this real chain is a plain (default or explicit) `I2I`.

Rules (`r`) always carry 2–3 named clauses (`usageDisclaimer`, `issuanceDisclaimer`, and — only on #2 and #3 — `privacyDisclaimer`), each a single `l` (Legal Language) field holding a long fixed disclaimer string; `r.u` never appears.

**Hint for arcviz:** compact/SAID-only sections, blinding, and edge weights are all real spec features this real-world chain never exercises. They can be deferred behind a "not yet observed in production" flag rather than built to the same fidelity as the always-used fields on day one.

## 5. Disclosure state of this payload

Everything here is fully disclosed. Every `a`, `e`, and `r` section on every credential is the full inline object, never a bare SAID standing in for withheld content. The one `u` (salt) on credential #3 is present precisely so that #3's SAID (and its attribute block's SAID) are not brute-forceable from the small, guessable attribute space (an LEI plus a role) — its presence is evidence that selective disclosure / anti-correlation *machinery* was engineered into this schema, but its actual exercise (something withheld and later revealed) is not observable from a fully-disclosed payload like this one. **This corpus item cannot exercise arcviz's redacted/blinded rendering states** — a second, deliberately partial fixture is needed for that (see PLAN.md 2C's "chain where an intermediate node is undisclosed").

## 6. What makes this hard to render

- **Byte-size skew toward attachments, not content.** Only 33.1% of the file (127,106 of 383,574 bytes) is the JSON payload (KEL/TEL events + ACDCs); 66.9% is CESR attachment groups (signatures, receipts) that a structural/content renderer has no reason to display but must still skip correctly.
- **Massive KEL duplication and irrelevant volume.** 341 `ixn` frames collapse to 107 distinct events, and of those only a handful relate to the 4 credentials being rendered; the rest is the issuer's unrelated operational history. A "who issued this" view needs active filtering and dedup, not a straight walk of what's present.
- **Asymmetric rotation arrays.** The one key rotation goes from 4 current keys to 8 (4 real, 4 zero-weight placeholders) while only pre-committing to 4 next-key digests — current-key-count and next-digest-count are not the same number across a rotation, which breaks any layout that assumes they pair up.
- **Deep, non-uniform delegation with a hole at the top.** Two of the three organizational AIDs delegate from a root whose own inception is not in the payload at all — a renderer showing "issued by AID X" has to represent a delegator that is named but not resolvable from local data.
- **A single long fixed-text field dwarfs everything else in the credential.** The `r` section's `l` (Legal Language) strings run 341–480 characters versus 12–44 characters for every actual data field — a card layout sized for attribute values will be blown out by the rules section alone.

## 7. The PII map, by field path

Every field path below carries personal or organization-identifying data in at least one credential in this chain. No values are reproduced.

| Credential | Field path | Nature |
|---|---|---|
| #0 (QVI) | `a.LEI` | organization identifier |
| #0 (QVI) | `a.dt` | issuance timestamp |
| #1 (LE) | `a.LEI` | organization identifier |
| #1 (LE) | `a.dt` | issuance timestamp |
| #2 (ECR AUTH) | `a.LEI` | organization identifier |
| #2 (ECR AUTH) | `a.dt` | issuance timestamp |
| #2 (ECR AUTH) | `a.AID` | a person's control identifier, held as an attribute value (not the credential's own `i`/subject fields) |
| #2 (ECR AUTH) | `a.personLegalName` | person's legal name |
| #2 (ECR AUTH) | `a.engagementContextRole` | role title tied to a named person |
| #3 (ECR) | `a.LEI` | organization identifier |
| #3 (ECR) | `a.dt` | issuance timestamp |
| #3 (ECR) | `a.personLegalName` | person's legal name |
| #3 (ECR) | `a.engagementContextRole` | role title tied to a named person |
| #3 (ECR) | `a.u` | a privacy salt whose value is specific to this person's credential instance |
| #3 (ECR) | `a.i` (subject) | the person's own control AID — pseudonymous but linkable across every system that sees this credential |

`a.i` (subject) on #0, #1, and #2, and every credential's own `i` (issuer), are organizational AIDs, not personal, and are not listed. `ri` (registry AID) and all schema SAIDs are structural, not PII, and are already quoted throughout this document.

## What a synthetic equivalent must reproduce

A regenerated, de-identified fixture is a faithful stand-in only if it keeps: the 4-node linear chain (QVI → LE → ECR-AUTH → ECR) with the issuer/subject alternation described in §1; exactly one edge per non-root node, each referencing the far schema SAID, with at least one edge showing an explicit `o` and at least one showing the same relationship left to the default; a leaf credential with a top-level `u` salt that its ancestors lack, so arcviz's field-inventory tests see both states; weighted multi-sig KEL events (fractional `kt`/`nt`) for every organizational AID and a plain single-key `icp` for the individual; the one asymmetric rotation (current-key-count ≠ next-digest-count, with zero-weight retained keys); at least one delegator whose own inception is absent from the fixture, to exercise the "can't verify to the root" case; a deliberately bloated, mostly-irrelevant KEL around the real chain (duplicated ancestor events plus dozens of unrelated anchors) so dedup/filtering logic has something to fail against; registries configured `NB`/`bt:0`; long fixed-text `r.l` disclaimer strings sized like the real ones (300–500 characters) so layout is tested against the actual outlier field; and, as a second fixture entirely (not this one), a partially-disclosed/blinded variant, since this real payload is 100% disclosed and cannot exercise that rendering path.
