# ACDC field and section inventory

Phase 2A. Every claim below is quoted from the vendored specification, with a locator. See "Sources read" for exactly which commit of which repository each quote comes from, and "Open questions and spec ambiguities" at the end for everything flagged rather than resolved by inference. Source keys (`[acdc-spec]`, `[dossier-spec]`, `[cesr-spec]`, etc.) are defined in [`../../refs/sources.acdc-spec.yaml`](../../refs/sources.acdc-spec.yaml).

## Sources read

- **ACDC**: vendored at `~/code/me/kswg-acdc-specification`, `spec/spec-body.md`. The checked-out branch is `fix-worked-examples-schema-1520` at commit `651df33e14396d5a79e1b1abf419111a97a97f42` (2026-07-21). I diffed this file against the live `trustoverip/kswg-acdc-specification@main` (`f0bd097de318fbbe2d069a2b46cecd42550762e3`, fetched 2026-09-04) before relying on anything: every section this inventory cites — top-level field table, Attribute/Aggregate/Edge/Rule sections, disclosure-mechanism list, Registry/blinding fields — is byte-identical between the two. The vendored checkout is missing some newer worked-examples and lifecycle prose that main has added (see below), and is missing a proposed `E1E` edge operator that exists only on an unmerged local branch (`add-e1e-edge-operator`, commit `0b28b50`, 2026-07-28) — neither omission affects any claim below. All ACDC locators are line numbers in `spec/spec-body.md`.
- **CESR**: vendored at `~/code/me/kswg-cesr-specification`, `spec/spec-body.md`. Checked-out branch `pq` at commit `34c3978d5cd7531897dfdd26d954051937ff0640` (2026-08-25). Diffed against `trustoverip/kswg-cesr-specification@main` (`bad6edd84f928fe1e77a722edbdd829e0878377f`): the only differences are an unmerged post-quantum-signature-code addition (irrelevant to what's cited here — Version String field and SAID section are identical).
- **Dossier**: vendored at `~/code/me/kswg-dossier-specification`, `spec/dossier-spec-body.md`. The checked-out branch (`ci-pages-step-strict`, commit `7669358`) is **materially behind** `trustoverip/kswg-dossier-specification@main` (`b9227753cc1bbb92ed237970fc3b89bf1d0c904f`, fetched 2026-09-04): main replaced "signing" terminology with "anchoring" throughout, correcting the model of how a dossier is authenticated (see the Dossier section below). All dossier quotes in this document are taken from the **upstream `main` capture**, not the vendored checkout, because the checkout's "signed document" framing is superseded. Locators are line numbers in the upstream `main` version of `spec/dossier-spec-body.md` as fetched 2026-09-04; the vendored file's line numbers differ by a small, mostly-constant offset in the affected sections.

---

## 1. Top-level ACDC fields

Quoted directly from the spec's own table (`spec/spec-body.md:16-28`, "Top-Level Fields"):

| Label | Title | Type / value | Required? | Meaning (spec's own words) |
|---|---|---|---|---|
| `v` | Version String | fixed-format string | **Required** | "Regexable format: `ACDCMmmGggKKKKSSSS.` that provides protocol type, version, CESR genus version, serialization type, size, and terminator" (line 18) |
| `t` | Message Type | 3-char string | Optional (see below) | "Three-character Message type" (line 19) |
| `d` | Message Digest SAID | SAID | **Required** | "Self-referential fully qualified cryptographic digest of enclosing map" (line 20) |
| `u` | UUID | fully-qualified nonce | Optional | "Random Universally Unique Identifier as fully qualified high entropy pseudo-random string, a salty nonce" (line 21) |
| `i` | Issuer AID | AID | **Required** | "Autonomic Identifier whose control authority is established via KERI verifiable Key State" (line 22) |
| `rd` | Registry Digest SAID | SAID | Optional | "Issuance and/or revocation, transfer, or retraction registry for ACDC" (line 23) |
| `s` | Schema | SAID or block | **Required** | "Either the SAID of a JSON Schema block or the block itself" (line 24) |
| `a` | Attribute | SAID or block | Optional | "Either the SAID of a block of Attributes or the block itself" (line 25) |
| `A` | Attribute Aggregate | AGID or block | Optional | "Either the Aggregate of a selectively disclosable block of attributes or the block itself" (line 26) |
| `e` | Edge | SAID or block | Optional | "Either the SAID of a block of Edges or the block itself" (line 27) |
| `r` | Rule | SAID or block | Optional | "Either the SAID a block of Rules or the block itself [sic]" (line 28) |

**Field ordering** (`spec/spec-body.md:32`): "When present, the top-level fields MUST appear in the following order: `[v, t, d, u, i, rd, s, a, A, e, r]`."

**Required fields** (`spec/spec-body.md:36`): "The following fields are REQUIRED `[v, d, i, s]` i.e. they MUST appear in any ACDC (not to be confused with other message types in the ACDC protocol)." `t` is not in this list for the plain (implied-`acm`) case, but becomes conditionally required — see below.

**`a`/`A` mutual exclusion**: `a` field (line 106): "An ACDC MUST not have both an `a` field and an `A` field ... when it has either." Confirmed for `A` at line 110. Confirmed again for the fixed-field CESR-native message form (`spec/spec-body.md:2976`): "the value of either or both the `a` and `A` field MUST be empty. To clarify, both the `a` and `A` field values MUST not be non-empty, one or the other or both MUST be empty."

**Message-type conditionality of `t`** (`spec/spec-body.md:72`): "The presence of the message type field, labeled `t`, is optional for messages of type `acm` with non-CESR-native serialization kinds. It MUST be present in any `acm` message that uses a CESR serialization kind... It MUST be present in messages with any other message type, regardless of the kind of serialization. A message without a message type, `t`, field is assumed to be of type `acm`."

### Other reserved (non-top-level) fields

`spec/spec-body.md:38-54`, "Other Reserved Fields" — these MAY appear at other levels besides the top level:

| Label | Title | Meaning |
|---|---|---|
| `d` | Digest SAID | same semantics as top-level, self-referential to enclosing map |
| `u` | UUID | "Random ... salty nonce" |
| `i` | Identifier AID | "Context-dependent AID as determined by its enclosing map such as Issuee identifier" |
| `rd` | Registry Digest SAID | "Issuance and/or revocation, transfer, retraction, or usage registry for ACDC when not at top-level" |
| `dt` | Datetime | "Context-dependent ISO datetime string" |
| `n` | Node | "SAID of another ACDC as the terminating point (vertex) of a directed Edge" |
| `o` | Operator | "Either unary operator on Edge or m-ary operator on edge-group" |
| `w` | Weight | "Edge weight property ... for directed weighted edges and operators" |
| `l` | Legal Language | "Text of Ricardian contract clause" |

**Compact labels, rationale** (`spec/spec-body.md:58`): field labels are "meant to support resource-constrained applications such as supply chain or IoT," using at most two characters.

### The `u` (UUID) field, the blinding mechanism — F0

`spec/spec-body.md:89`: "Without the entropy provided by the UUID, `u`, field, an adversary may be able to reconstruct the block contents merely from the SAID of the block and the Schema of the block using a rainbow or dictionary attack on the set of field values allowed by the Schema."

`spec/spec-body.md:91` (general rule, applies at any nesting level): "A UUID, `u` field, MAY optionally appear in any block (field map) at any level of an ACDC. Whenever a block in an ACDC includes a UUID, `u`, field then, its associated SAID, `d`, field makes a blinded commitment to the contents of that block. The UUID, `u`, field is the blinding factor... With an embedded UUID field value that contains sufficient cryptographic entropy, the block contents can only be discovered if the included UUID field is explicitly disclosed."

**What an observer can and cannot infer from a blinded field:** given only the block's Schema and its SAID (no `u` disclosed), the adversary "is not able to discover the remaining contents of the ... block in a computationally feasible manner, such as a rainbow table attack" (recurring formula, e.g. `spec/spec-body.md:340`, `700`, `1093`, `1162`, `1275`). Concretely: an observer can know the *shape* (schema) of a blinded block and can verify set-membership / inclusion once given a candidate value plus the `u`, but cannot brute-force the value from `d` + schema alone when `u` has "approximately 128 bits of entropy" (recurring, e.g. line 1093). Presence vs. absence of `u` is itself the public/private distinction at any level: no top-level `u` ⇒ **Public ACDC** (`spec/spec-body.md:160`); present with sufficient entropy ⇒ **Private ACDC** (`spec/spec-body.md:164`); present but **empty** ⇒ **Metadata ACDC** (`spec/spec-body.md:166`, see §5 below). The same present/absent/empty three-way logic applies independently at the Attribute-block level (`spec/spec-body.md:306`, "Two other variants, namely private (public), are defined respectively by the presence (absence) of a UUID, `u`, field") and at the Edge-block level (`spec/spec-body.md:1164`: "The absence of the UUID, `u` field in an Edge block makes that edge a Public Edge. The presence of the UUID, `u` field ... makes that Edge a Private Edge.")

**Derivation in bulk/selective contexts**: `u` values may be independently random per block, or hierarchically-deterministically (HD) derived from a shared secret salt plus a path string, "so that the value of the UUID, `u`, fields" need not be transmitted individually (`spec/spec-body.md:2755` and the Bulk Issuance annex, `2765-2796`). Derivation-path collisions between the top-level `u`, per-attribute `u`, and (in bulk issuance) the separate blinding factor `v_k` are a live correctness concern the spec addresses explicitly on `main` but not in the vendored checkout — see Sources read.

---

## 2. `a` (Attribute) vs. `A` (Attribute Aggregate) — the heart of selective disclosure

These are **two different graduated-disclosure mechanisms with different names in the spec's own vocabulary**, not interchangeable synonyms. `spec/spec-body.md:661`: "A selectively disclosable blinded Aggregate section appears at the top level using the field label `A`. This is distinct from the field label `a` for a partially disclosable Attribute section. This makes clear (unambiguous) the semantics of each respective section's associated Schema."

| | `a` — Attribute section | `A` — Aggregate section |
|---|---|---|
| Disclosure mechanism named by the spec | **Partial Disclosure** | **Selective Disclosure** |
| Shape | a single nested field map (block), possibly nested further | an ordered **list/array** of independently blinded blocks, plus one aggregate value at index 0 |
| Compact form's value | the block's own SAID (`d`) | the **AGID** (Aggregate ID) — explicitly *not* a SAID: "the value of a compact variant of the selectively disclosable Aggregate section is an aggregate, AGID, (Aggregate ID) not a SAID" (line 661) |
| Granularity of disclosure | all fields in a given (sub)block disclose together: "All fields in a given block MUST be disclosed together as a set. When a blinded attribute block has more than one attribute field, then each field in the block is not independently selectively disclosable" (line 692) — nesting sub-blocks lets you partially disclose at finer grain, one sub-block at a time | each element of the array is independently, and unorderedly, discloseable: "Membership of any blinded commitment to a value in the list of aggregated blinded commitments may be proven without leaking (disclosing) the unblinded value belonging to any other blinded commitment in the list" (line 686) |
| What "Full Disclosure" means in context | exposes, at minimum, "the labels of other fields in its enclosing block" even before those fields' *values* are shown (line 1777, 1779) | exposes **nothing** about other still-undisclosed elements, "including their labels" (line 1777) — field labels live *inside* each blinded block, so undisclosed labels are also hidden (line 694: "because the field labels for a given block only appear within that blinded block, the field labels are also blinded") |
| Ordering leakage | n/a (single block) | explicitly defeated: "The order of appearance of elements in an `anyOf` subschema for the Aggregate array is not correlated to the actual order of appearance of the associated block or blocks in the blinded array itself. This prevents inference based on location in the blinded array" (line 694) |

**The precise Partial-vs-Selective distinction, in the spec's own summary** (`spec/spec-body.md:1777`): "A salient difference between Partial Disclosure and Selective Disclosure of a given block is the degree to which information about other fields is exposed in order to make Full Disclosure of its detailed field values. A partially disclosable block, when fully disclosed, exposes, at the very least, the labels of other fields in its enclosing block (a field map). Whereas a selectively disclosable block, when fully disclosed, does not expose any information about other yet-to-be-exposed fields, including their labels in its enclosing block (a field map array)."

**AGID computation** (`spec/spec-body.md:712-720`): the zeroth list element is a placeholder (dummied with `#` characters equal to the digest length), the remaining `N` elements are the blindable blocks' own SAIDs; AGID = digest of the ordered serialized list with the placeholder filled in: "AGID = H(C(a_i for all i in {0, ..., N}))". A worked JSON example with real values is at lines 904-956; a worked CESR-native example at 980-1024.

**Reserved fields inside Aggregate blocks** (`spec/spec-body.md:668-677`): `d`, `u`, `i`, `dt` — same semantics as elsewhere. Each blindable block additionally carries its one or more attribute-specific fields.

**Consistency rule**: `spec/spec-body.md:110` and `106` both state the ACDC "MUST not have both a non-empty `a` field value and a non-empty `A` field value ... when it has either" — i.e., an ACDC picks one graduated-disclosure mechanism for its payload, not both simultaneously.

---

## 3. Edge section (`e`), in full

### Block types

`spec/spec-body.md:1054-1058`: two block types nest inside `e` — **Edge-groups** and **Edges**. "An Edge MUST contain a node, `n` field. An Edge-group MUST NOT have a node, `n` field." The top-level `e` field is itself an Edge-group (line 1058).

### Edge-group reserved fields

`spec/spec-body.md:1076-1083`, order `[d, u, o, w]` when present:

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | "self-referential fully qualified cryptographic digest of enclosing Edge-group block" |
| `u` | Optional | blinding nonce, same semantics as elsewhere |
| `o` | Optional | "m-ary operator on the Edges in the Edge-group" |
| `w` | Optional | "property for nested Edges or Edge-groups for weighted average `WAVG` operator" |

"An Edge-group MUST NOT have a node, `n`, field" (line 1085). "The top-level Edge-group MUST NOT have a weight, `w` field, because it is not a member of another Edge-group" (line 1120).

**m-ary (Edge-group) operators**, `spec/spec-body.md:1101-1108`:

| Operator | Meaning | Default |
|---|---|---|
| `AND` | "Logical AND of the validity of the Edge-group members. Edge-group is valid only if all members are valid." | **Yes** |
| `OR` | "Logical OR ... valid if one of the members is valid." | No |
| `NAND` | "Logical NAND ... valid only if not all members are valid." | No |
| `NOR` | "Logical NOR ... valid only if all members are invalid." | No |
| `AVG` | "Arithmetic average of a given Edge-group member property. Averaged property is defined by the schema or EGF." | No |
| `WAVG` | "Weighted arithmetic average ... Weight is given by the `w` field." | No |

Missing/absent `o` on an Edge-group defaults to `AND` (line 1110).

### Edge reserved fields

`spec/spec-body.md:1140-1149`, order `[d, u, n, s, o, w]` when present:

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID of the Edge block |
| `u` | Optional | blinding nonce — presence makes it a **Private Edge**, absence a **Public Edge** (line 1164) |
| `n` | **Required** | "Required SAID of the far node ACDC as the terminating point of a directed edge that connects the Edge's encapsulating near node ACDC to the specified far node ACDC" |
| `s` | Optional | "Optional SAID of the JSON Schema block of the far node ACDC" |
| `o` | Optional | unary operator(s) on this Edge (list below) |
| `w` | Optional | "edge weight property that enables ... weighted average" |

**Unary (per-Edge) operators — the complete normative list**, `spec/spec-body.md:1190-1195`:

| Operator | Meaning (verbatim) | Default |
|---|---|---|
| `I2I` | "Issuer-To-Issuee, The Issuer AID of this ACDC MUST be the Issuee AID of the node this Edge points to." | **Yes**, when applicable (see default-injection rule below) |
| `NI2I` | "Not-Issuer-To-Issuee, The Issuer AID of this ACDC MAY or MAY not be the Issuee AID of the node that this Edge points to." | No |
| `DI2I` | "Delegated-Issuer-To-Issuee, The Issuer AID of this ACDC MUST be either the Issuee AID or a delegated AID of the Issuee AID of the node this Edge points to." | No |
| `NOT` | "Logical NOT. The validity of the node this Edge points to is inverted. If valid, then not valid. If invalid, then valid." | No |

**Default-injection rule** (`spec/spec-body.md:1197-1201`, load-bearing — arcviz must reproduce this to render edge validity correctly when `o` is absent): when `o` is missing/empty or contains none of `I2I`/`NI2I`/`DI2I`: "If the node pointed to by the Edge is a targeted ACDC, i.e., has an Issuee, then the `I2I` Operator MUST be appended... If the node pointed to by the Edge block is an Untargeted ACDC i.e., does not have an Issuee, then the `NI2I` Operator MUST be appended."

`o` may be a **list** of unary operators; on conflict, "the latest Operator among the conflicting Operators in the list takes precedence" (line 1186).

**A proposed but not-yet-normative fifth operator**, `E1E` ("IssueE-To-IssueE"), exists only on an unmerged local ACDC-repo branch (`add-e1e-edge-operator`, commit `0b28b50`, 2026-07-28) and is **not** part of the published spec (neither the vendored checkout nor `trustoverip/kswg-acdc-specification@main`). It would express "the Issuee AID of the current ACDC ... MUST be the Issuee AID of the node to which the Edge points" — an identity relation between two Issuees issued by different Issuers, distinct from the delegative `I2I`/`DI2I` relations. Flagged here because it changes the semantics arcviz would need if it ever ships; not implemented anywhere authoritative as of this reading. **Open question, not resolved by inference.**

### What an Edge does and does not transfer — F1 (governs what arcviz may imply about a parent from a child)

**Validity requirement, minimum** (`spec/spec-body.md:1174`): "In order for a given Edge to be valid, at the very least, a Validator MUST confirm that the SAID of the provided far node ACDC matches the node, `n` field value given in the near node ACDC Edge block and MUST confirm that the provided far node ACDC satisfies its own schema." If the Edge's own `s` field is present, the far node must *additionally* validate against that schema (line 1174, 1178).

**An Edge transfers, or constrains:**
- **Identity/authority linkage** between the near ACDC's Issuer and the far ACDC's Issuee, per the unary operator in force (`I2I`, `NI2I`, `DI2I`) — this is a constraint on *who may legitimately be the near-node Issuer*, not a transfer of the far node's attribute values.
- **A schema constraint** on the far node, via the optional `s` field (line 1176-1178) — "an additional constraint on the far node ACDC," used e.g. to force forward-compatibility across minor schema versions (line 1180-1182).
- **A weight** (`w`), for aggregation by an enclosing Edge-group's `WAVG`/`AVG` operator (line 1215-1217) — a property *of the edge*, not of either endpoint.
- **Validity propagation**, EGF-dependent, along a chain/tree: "When any node in a provenance chain is invalid, an Edge pointing to that node MAY also be invalid. If a node has an invalid Edge, then the node MAY also be invalid" (line 1114) — note the modal "MAY", not "MUST"; the spec explicitly defers the actual propagation logic to the ecosystem governance framework (line 1112: "the actual logic for interpreting the validity of a set of chained or treed ACDCs is EGF-dependent").

**An Edge does NOT transfer:**
- **Attribute values.** Nothing in the Edge block's reserved-field set (`d,u,n,s,o,w`) carries any of the far node's `a`/`A` payload. A near-node ACDC's Edge is a cryptographic pointer plus a validity/schema constraint; reading a far node's attributes requires fetching and independently validating that far node.
- **The far node's Issuee identity by default.** `NI2I` explicitly "removes or nullifies any requirement" that the near Issuer equal the far Issuee (line 1207) — so absent a stated `I2I`/`DI2I`, arcviz may **not** assume any identity relationship between the two ACDCs' principals.
- **Blinded/private detail, when the Edge or the far node is private.** A "Compact Private Edge... enables a presenter of that ACDC to make a verifiable commitment to the ACDC attached to the Edge without disclosing any details of that ACDC, including the ACDC's SAID" (line 1165) — so a rendered graph may have to show an edge whose far-node identity is itself undisclosed.
- **Node-vs-Edge-group distinction is structural, not optional**: "Each nested block in every Edge-group MUST have its own field with its own local (to the ACDC) label... each nested block MUST NOT include a type field. The type of each block is provided by that associated subschema" (line 1128-1130) — i.e., there is no ACDC-carried "edge type" string; the type comes from which labeled subschema slot the edge occupies, which arcviz must resolve against the (possibly-external) schema to know what an edge "means" semantically, beyond its structural operator.

**Compact and simple-compact Edge forms** (`spec/spec-body.md:1156-1225`): a Compact Edge replaces the whole block with its SAID (public if no `u`, private if `u` present, line 1158, 1165); a **Simple compact edge** applies only "When an Edge sub-block has only one field, that is, its node, `n` field" — then "the labeled Edge field value is the value of its node, `n`, field" directly (no SAID indirection) and "The Edge is, therefore, public" (line 1225).

### Property-graph framing

`spec/spec-body.md:1062`: "A set of ACDCs as nodes connected by edges forms a labeled property graph (LPG) or property graph (PG) for short... The properties of each node (ACDC) are provided essentially by its Attribute Section. The properties of each edge are provided by the combination of Edge blocks and Edge-group blocks." Edges form a DAG (line 1172: "The edges and nodes form a directed acyclic graph (DAG)").

---

## 4. Rule section (`r`) — how legal prose is carried

`spec/spec-body.md:1239`: "The purpose of the Rules section is to provide a set of rules or conditions as a Ricardian Contract. The important features of a Ricardian contract are that it is both human and machine-readable and referenceable by a cryptographic digest."

**Block types**: **Rule-groups** and **Rules**, same nesting discipline as Edge/Edge-group (`spec/spec-body.md:1245-1249`). A Rule-group is "indicated by the presence of one or more non-reserved labeled fields whose value represents a nested Rule or Rule-Groups" (line 1249).

**Rule-group reserved fields**, order `[d, u, l]` (`spec/spec-body.md:1257-1267`):

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID |
| `u` | Optional | blinding nonce (Rule-group may thereby be made private/confidential, line 1313) |
| `l` | Optional | "legal language for the Rule-group" |

**Rule (leaf) reserved fields**, order `[d, u, l]` (`spec/spec-body.md:1292-1300`):

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID |
| `u` | Optional | blinding nonce |
| `l` | **Required** | "The actual legal language for the clause." |

`spec/spec-body.md:1300`: "A Rule MUST have a Legal, `l`, field... A Rule MUST NOT have any other fields. In this sense, a Rule is a terminal node in a sub-graph of Rule-groups and Rules."

**Compact and Simple-compact Rule forms**: a Compact Rule replaces the block with its SAID, public or private depending on `u` presence (line 1307, same logic as Edges). A **Simple Compact Rule** applies "When a Rule block has only one field, that is, its legal, `l` field" — then "the block is represented as a single rule field and that labeled rule field value is what would have been the value of the block's legal, `l` field," and "The Rule block (rule) is, therefore, public" (line 1323).

**Discovery**: `spec/spec-body.md:1253` — Rule-section SAIDs can be resolved out-of-band via OOBI or attachment at issuance, "the essence of Percolated Discovery," same mechanism as for Edge-referenced ACDCs (line 1070).

---

## 5. Every disclosure variant, by the spec's own names

`spec/spec-body.md:1747-1774` gives the canonical enumeration under "Graduated Disclosure":

> "There are several graduated disclosure mechanisms as follows: Compact Disclosure, Metadata Disclosure, Partial Disclosure, Nested Partial Disclosure, Full Disclosure, Selective Disclosure, Bulk-issued Instance Disclosure. ... All the Graduated Disclosure mechanisms MAY be used in combination."

For each, exactly what's present / digest-only / absent, quoted:

| Variant | What's present | What's a digest only | What's absent | Spec quote / locator |
|---|---|---|---|---|
| **Compact Disclosure** | the section/block's SAID | the block's actual content (behind its SAID) | — (nothing is unrecoverable; it's an "undisclosed yet" state, not a redaction) | "relies on the inclusion in that block of a cryptographic digest of the content (SAID)... Disclosure of the SAID makes a verifiable commitment to its data that MAY be more fully disclosed later." (`spec/spec-body.md:1761`) |
| **Metadata Disclosure** | Issuer, Schema, provenanced Edges, Rules — via an ACDC with an **empty** top-level `u` field | the real ACDC's top-level `d` (unreachable from the metadata ACDC's `d`, since they're cryptographically distinct: "The top-level SAID, `d`, field, of the metadata ACDC, is cryptographically derived from an ACDC with an empty top-level UUID, `u`, field so its value will necessarily be different from that of an ACDC with a high entropy top-level UUID" — line 168) | the top-level Attribute (`a`) or Aggregate (`A`) field value, which "MAY be empty or missing so that its value is not correlatable across disclosures" (line 168); also, "only cryptographic commitments from the Discloser are attached, not commitments from the Issuer" (line 172) | "provide a mechanism for a Discloser to make cryptographic commitments to the metadata of a yet to be disclosed private ACDC without providing any point of correlation to the actual top-level SAID" (`spec/spec-body.md:166-168`); enumerated under Graduated Disclosure at line 1763 |
| **Partial Disclosure** | the block's SAID (`d`) plus its blinding nonce (`u`), once disclosed | before `u` is disclosed: the block's content is blinded behind `d` even though `d` is visible | field values not yet disclosed; but the **labels** of sibling fields in the enclosing map are exposed once any partial disclosure of that map happens (line 1779) | "relies upon a cryptographic digest (SAID) of the content and a salty nonce (UUID) embedded in that content... The content remains blinded in spite of disclosure of its SAID until and unless the salty nonce (UUID) is also disclosed." (`spec/spec-body.md:1765`) |
| **Nested Partial Disclosure** | same mechanism as Partial Disclosure, applied independently at each level of a nested block tree | any not-yet-expanded sub-block, behind its own `d`+`u` | deeper branches not yet expanded | "relies on each nested block embedding both its digest (SAID) and a salty nonce (UUID). This allows the Partial Disclosure of different branches of the tree at different levels of nesting." (`spec/spec-body.md:1767`); worked example at lines 503-657 |
| **Full Disclosure** | everything in the disclosed block/section, unhidden | nothing (within the scope being "fully disclosed") | nothing (within scope) | "Full Disclosure is disclosure without hiding a given block's content behind SAIDs or salted SAIDs." (`spec/spec-body.md:1769`). Note the spec's own caveat on scope-dependence of the term, line 1779: in a Partial-Disclosure context, "Full Disclosure" of a nested block still means "at least the disclosure of the labels of all the fields in the enclosing blocks of that branch" — it is not necessarily disclosure of the *entire ACDC*. |
| **Selective Disclosure** | the AGID (`A` compact) plus whichever Aggregate-array elements are chosen for disclosure, each with its own `d`,`u` | the other, undisclosed array elements — represented by their bare SAID strings in the list, contributing to the AGID digest but revealing nothing else, "including their labels" (line 1777) | field labels and values of undisclosed elements entirely | "relies on each element embedding its digest (said) and salty nonce (UUID) as partially disclosable elements. ... Membership in the set can be verified against a set of SAIDs" (`spec/spec-body.md:1771`) |
| **Bulk-issued Instance Disclosure** | one member (copy) of a bulk-issued set, with its own unique `d`/`u` | the linkage between this copy and any sibling copy (each sibling has different, uncorrelated SAID/UUID) | any other member's identity; optionally the shared `rd`, if nested inside `a`/`A` rather than top-level | "relies on issuing multiple instances of a given ACDC, each a copy but with unique instance identifiers so that the disclosure of one instance is not correlatable to another via the instance identifiers." (`spec/spec-body.md:1773`) |

### Also load-bearing for arcviz: the two *contractually-protected* wrappers around these mechanisms

`spec/spec-body.md:1781-1793`, "Contractually Protected Disclosure" is not itself a graduated-disclosure primitive but a **process** built on the above: "the potential Discloser first makes an offer using the least (Partial) Disclosure of some information about other information to be disclosed (Full Disclosure) contingent on the potential Disclosee first agreeing to the contractual terms."

- **Chain-Link Confidentiality Disclosure**: "imposes conditions and limitations on the further disclosure and/or use of the disclosed data ... applied to subsequent disclosures by the Disclosee that follow the data (hence chain-link)" (line 1790).
- **Contingent Disclosure**: "some contingency is specified in the Rules section that places an obligation by some party to make a disclosure when the contingency is satisfied" (line 1792) — e.g. escrow-triggered disclosure, enabling "latent accountability."

### The "compact vs. private/public vs. metadata" cross-cut (top level)

These three named ACDC **variants** are a separate axis from the graduated-disclosure list above, but interact with it directly and arcviz needs to represent both axes:

- **Compact ACDC** (`spec/spec-body.md:153-155`): every present top-level section field (`s,a,e,r`) is its SAID rather than its expanded block; `A`, when present, is compacted to its AGID instead (line 155, a special case: "the most compact form of the ACDC has the aggregate value as the value of the Aggregate section field... an Aggregate section uses its own algorithm for compact and un-compact (expanded) forms").
- **Public ACDC** (`spec/spec-body.md:160`): no top-level `u` — "the top-level, `d`, field is a cryptographic digest, [but] it may not securely blind the contents of the ACDC when knowledge of the Schema is available."
- **Private ACDC** (`spec/spec-body.md:164`): top-level `u` present with "sufficient cryptographic entropy" — "the top-level SAID, `d`, field of an ACDC could provide a secure cryptographic digest that blinds the contents."
- **Metadata ACDC** (`spec/spec-body.md:166`, see table row above): top-level `u` present but **empty**.

**IPEX cross-variant commitment note** (`spec/spec-body.md:1822`, load-bearing for how arcviz should treat "which variant did the Issuer actually sign"): "a signature on any variant MAY be used to verify the Issuer's commitment to any other variant either directly or indirectly, in whole or in part, on a top-level section-by-section basis. This cross-variant Issuer commitment verifiability is an essential property that supports Graduated Disclosure by the Disclosee of any or all variants, whether Full, Compact, Metadata, Partial, Selective, etc." I.e., there is exactly one Issuer commitment (via the composed Schema and the "most compact form" SAID algorithm, §130-151), and every disclosed variant is checked against that one commitment — arcviz does not need to track "which variant was signed" as a separate fact per disclosure.

---

## 6. Blinding and the `u` salt — summary (detail already threaded through §1–§5 above)

The mechanism is uniform across every level (top-level ACDC, Attribute block, nested Attribute sub-blocks, Aggregate-array elements, Edge blocks, Edge-groups, Rule blocks, Rule-groups, and TEL blinded-attribute blocks): a field map with a `d` (SAID) MAY also carry a `u` (UUID/salty nonce, "approximately 128 bits of entropy," recurring). Presence of `u` converts the SAID from a mere compactness/dedup mechanism into a genuine privacy-preserving blind: `spec/spec-body.md:89-91` (quoted above) is the canonical statement, restated near-verbatim at every level that reserves a `u` field.

**What an observer can infer, precisely:**
- The block's **shape** (its Schema/subschema), always — Schema is never itself hidden by `u`.
- **Set membership**: given a disclosed SAID and, separately, a full list of SAIDs (e.g. the Aggregate array, or a bulk-issuance/Merkle set), an observer can check whether a given digest is *in* that list, without learning the undisclosed members' content (`spec/spec-body.md:732`, `744-750`).
- **Nothing about content** from `d` + Schema alone, when `u` carries sufficient entropy — this is the rainbow-table-resistance property repeated at every level.
- **Once `u` (and the content) is disclosed**, full verifiability: recompute `d` from disclosed content+`u`, compare to the previously-committed compact-form value.

**Registry-level blinding is a distinct, related mechanism** (`spec/spec-body.md:2043-2143`, TEL Blinded Attribute Block): the transaction state itself (`ts`, `td`) can be hidden behind a BLID (a SAID-like digest over fixed-order concatenated fields, not a labeled field map digest — `spec/spec-body.md:2066`), unblindable only by whoever holds the same derivation salt and sequence-number path as the Issuer: "Only the Issuer and Discloser have a copy of the secret salt, so only they can independently derive the current blind from the sequence number" (`spec/spec-body.md:2133`). This is orthogonal to but composable with ACDC-level `u` blinding.

---

## 7. The dossier specification — joint issuance, threshold operators, revocation over ACDCs

Quoted from `trustoverip/kswg-dossier-specification@main` (`b9227753...`, fetched 2026-09-04) — see "Sources read" for why upstream `main` and not the vendored checkout.

### Anchoring, not signing — corrects a stale framing

**This overturns the vendored checkout's language** and is the single most important correction found in this audit stream: "A dossier is not a signed document. The issuer does not compute a signature over the dossier ACDC and attach that signature to it as proof of authenticity... Instead: 1. The assembled dossier ACDC is saidified... 2. The issuer constructs a seal containing that SAID. 3. The issuer anchors the seal in an append-only verifiable log... 4. The key event carrying the anchor is signed with the keys authoritative for the issuer's AID at that point in the log. The signature exists on the anchoring key event, not on the dossier." This matters for arcviz because a dossier's "is this authentic" affordance must point at an anchor/KEL-position, not at an attached signature on the artifact itself, in the general case. A narrow exception exists for single-interaction "Ephemeral Dossiers With Attached Signatures," explicitly NOT RECOMMENDED for anything published, cited, or cached.

### Dossier structure

- A dossier "MUST be a valid Authentic Chained Data Container (ACDC)."
- Its payload is a **graph of edges to external evidence**, not direct claims: "The primary payload of a dossier is not a set of direct claims, but rather a graph of references to external evidence... contained within an edges block (`e`)."
- The `a` section is reserved for **proximate metadata about the dossier act itself** (assembler, purpose, timestamps, jurisdiction, governance framework) and "MUST NOT be used to carry primary evidence."

### Joint issuance and threshold operators — the complete set

Placed in the `o` field of an edge group, per `MxN`/`RMxN`/`MxQ`/`RMxQ` conventions, all "satisfied when the weights (`w`) of its Endorsed slots sum to at least unity (1)":

| Operator | Kind | Mechanics |
|---|---|---|
| `MxN` | issuance | "The edge group contains exactly *N* slots, one per candidate endorser, each carrying a weight `w`... For the common equal-weight case, each slot is given `w` of `1/m`, so that any *m* of the *n* endorse to reach unity." Each counted endorsement carries `act`=`"issue"`, `disp`=`"endorse"`. |
| `RMxN` | revocation | "the same mechanics as `MxN`, applied to revocation... each counted endorsement MUST carry `act` `"revoke"`. The set of revocation slots MAY be identical to, overlap, or be disjoint from the issuance slots." |
| `MxQ` | issuance, open-ended endorser set | "the slot count is not fixed in advance; slots are added as qualified endorsers act... the operator declares a uniform member weight in its own `w` field... group is satisfied when those weights sum to unity (equivalently, when at least `1/w` qualified endorsers have endorsed)." Requires a qualification-proof edge `e.qp` validating against a schema named in the group's `qs` field. |
| `RMxQ` | revocation, open-ended | same mechanics as `MxQ`, `act`=`"revoke"`. |

**Slot dispositions** (three, mutually exclusive): **Pending** (references an unsigned/unanchored placeholder — "contributes nothing to the threshold sum"), **Endorsed** (`disp`="endorse", weight counted), **Declined** (`disp`="decline", a `declination` — "an authenticated refusal," weight not counted but the dissent is attributable). "Because only [an authenticated act] authenticates a candidate's decision, a pending slot and an absent slot are equivalent in trust terms... An active 'no' MUST therefore be expressed as [a signed/anchored] declination, never as a null or unsigned slot."

**Finalization**: an optional `fi` field in the dossier's `a` section names an AID whose KEL a `finalizer` anchors the threshold-satisfying proof set into, "so that the aggregate evidence is collected in one predictable place." Absent `fi`, "a verifier MUST instead gather the endorsements from the participants' individual KELs."

**Revocation is independently configurable from issuance**: "if no revocation operator is present, the threshold required to revoke a dossier is identical to the threshold required to issue it," but a dossier "MAY specify different operators, slot sets, or weights for issuance and revocation" (e.g., majority to issue, single admin AID to revoke).

### Annotation edges — mutable-looking state over immutable ACDCs

"Because ACDCs are immutable, an issuer cannot simply modify the metadata of an existing edge. To manage these state transitions, dossiers MUST use Annotation Edges. An annotation edge is an edge in a new version of the dossier that points to an artifact (or an edge) in a previous version... Verifiers MUST process the dossier by traversing the graph to resolve the 'effective state' of each piece of evidence, applying the latest annotations found in the chain." Directly relevant to arcviz's redacted/annotated/superseded-state rendering problem.

---

## 8. CESR — what a renderer receives on the wire

Quoted from `spec/spec-body.md` in `~/code/me/kswg-cesr-specification` (identical to upstream `main` for these sections — see Sources read).

- **Version String format** (`spec/spec-body.md:1174-1195`), 2.XX: `PPPPMmmGggKKKKBBBB.` — 19 characters, five parts: 4-char protocol (`ACDC`/`KERI`), 3-char major.minor protocol version (base64-numeric), 3-char CESR genus major.minor version, 4-char serialization kind (`JSON`/`CBOR`/`MGPK`/`CESR`), 4-char base64 total-length, `.` terminator. This is what a JSON/CBOR/MGPK-serialized ACDC's `v` field literally contains and what a renderer parses to determine size and kind before deserializing. A legacy 1.XX 17-character format (`PPPPvvKKKKllllll_`) MUST still be supported for old messages (line 1199-1217).
- **CESR-native messages carry no `v` string with size/kind** — that information is instead in the enclosing CESR count/group code (`-G##`/`--G#####`), and only a protocol+version placeholder is injected into any in-memory `v` field for reserialization bookkeeping (`spec/spec-body.md:1191`). A renderer consuming CESR-native input therefore gets sizing from the framing code, not from a regex-parsable `v` string.
- **SAID mechanics** (`spec/spec-body.md:1219-1233`): "SAIDs MUST be encoded as a CESR Primitive," i.e. a derivation-code-prefixed Base64 string, so a renderer sees the algorithm identifier baked into every SAID it displays (no separate "hash algorithm" field to look up).

**Presentation, display, or rendering — confirmed absent.** A full-text grep of `spec/spec-body.md` in all three vendored repos (ACDC, CESR; dossier not applicable — it discusses "human-readable" `l`/`purpose`/`ref` fields only in passing prose, not a rendering mechanism) for `presentation|display|render|visuali[sz]e|user interface|\bUI\b` turns up no rendering, display, or UI guidance of any kind in ACDC or CESR. The only hits are (a) prose uses of "presentation/present" in the credential-exchange sense (IPEX disclosure, not visual presentation), and (b) two incidental string matches: a URL fragment containing the substring "display" (a wiki link, ACDC bibliography) and the English word "render" used in its ordinary sense ("may render... an exercise in diminishing returns," ACDC Annex). **This is a confirmed nothing**, consistent with `docs/research/PLAN.md`'s framing that rendering authority is an open design question deferred to a later phase, not something the base specifications answer.

---

## Open questions and spec ambiguities

1. **`E1E` edge operator.** A fifth unary Edge operator, expressing Issuee-to-Issuee identity across differently-issued ACDCs, exists only on an unmerged branch in the vendored ACDC repo (`add-e1e-edge-operator`, commit `0b28b50`, 2026-07-28) and is not part of any published version of the spec I could reach (vendored checkout or `trustoverip/kswg-acdc-specification@main`). Not resolved: whether/when this lands, and whether arcviz should design for its eventual existence. Flagged, not inferred.
2. **Vendored ACDC checkout vs. published main — worked-examples/lifecycle gap.** The vendored branch is missing a "Registry-Dependent Issuance Lifecycle" worked example and some registry-aggregate reproducibility language that upstream `main` has added since. None of it changed any field/operator/disclosure-variant semantics I found (confirmed by diff), but I have not exhaustively read the added worked-example prose itself line-by-line against my inventory claims — if a later phase needs the TEL lifecycle walkthrough specifically, re-pull `main` rather than trusting the vendored copy.
3. **Vendored dossier checkout is stale on a substantive point** (anchoring vs. signing terminology) — already corrected above by citing `main` instead, but this means **whoever next updates the vendored `kswg-dossier-specification` checkout should be told it is behind `main` by a meaningful semantic revision**, not just a wording pass. This is a fact about repo state, not about the spec's content, but it's exactly the kind of thing EVIDENCE.md's rule 6 worked example warns about: I did not take the vendored copy on faith, but a future reader might.
4. **Provenance-chain validity propagation is EGF-dependent, not normatively fixed.** `spec/spec-body.md:1112-1116` repeatedly defers "the actual logic for interpreting the validity of a set of chained or treed ACDCs" to the ecosystem governance framework, using modal "MAY" language ("an Edge pointing to that node MAY also be invalid"). Arcviz cannot derive a universal "if child invalid then parent invalid" rule from the base ACDC spec alone — this is confirmed underspecified, not an oversight in this inventory. Any such rule arcviz encodes would be arcviz's own design choice (per `PLAN.md`'s "arcviz may make disclosure-side rules, flagged as new" principle), not inherited doctrine.
5. **`A` field's non-standard-digest compaction is explicitly non-uniform with the rest of the "most compact form" algorithm.** `spec/spec-body.md:155` calls this out directly ("an Aggregate section uses its own algorithm for compact and un-compact (expanded) forms") but does not fully spell out how an AGID composes when an ACDC containing `A` is itself referenced by an Edge's `n` field pointing at its "most compact form" SAID — i.e., I could not find, in the sections read, an explicit statement of whether the top-level `d` of an ACDC that uses `A` is computed with the AGID substituted in the same depth-first "most compact form" walk described for `s`/`a`/`e`/`r` (§130-151), or via some different rule. The prose that *would* resolve this (line 155) gestures at "its own algorithm" without giving the algorithm inline at that point. Flagged rather than inferred; a future phase reading the Aggregate section's composed-schema JSON (`spec/spec-body.md:759-902`) more mechanically, or checking a keripy reference implementation, should confirm this before arcviz's rendering logic depends on it.
6. **Rendering/display: confirmed absent, but only within these three specs.** I did not check the KERI base specification (`kswg-keri-specification`), which was outside this task's assigned scope (ACDC + dossier + CESR only). If a later phase needs to rule out KERI-level display guidance too, that is a separate, not-yet-done check.
