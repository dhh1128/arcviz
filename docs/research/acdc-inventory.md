# ACDC field and section inventory

Phase 2A, rebased 2026-09-11. Every claim below is quoted from the specification, with a locator. See "Sources read" for exactly which commit of which repository each quote comes from, and "Open questions and spec ambiguities" at the end for everything flagged rather than resolved by inference. See "Corrections from the 2026-09-05 revision" below for what this rebase changed and why. Source keys (`[acdc-spec]`, `[dossier-spec]`, `[cesr-spec]`, etc.) are defined in [`../../refs/sources.acdc-spec.yaml`](../../refs/sources.acdc-spec.yaml).

## Sources read

- **ACDC**: `trustoverip/kswg-acdc-specification` is two diverged branches, `main` and `v1.1`, both declaring "Specification Status: v1.1" and describing ACDC protocol 2.x — not two versions of the spec, but one editorially unreconciled repository (see AGENTS.md rule 5 and [reviews/2026-09-06-operator-semantics-adjudication.md](../../reviews/2026-09-06-operator-semantics-adjudication.md), especially its 2026-09-10 correction). **`v1.1` is ahead on content and is the source of truth for this document.** Read via the `toip` remote in `~/code/me/kswg-acdc-specification` (`git fetch toip`, then `git show toip/v1.1:spec/spec-body.md`) at commit `910c74afce07e29c308015dabad9a576cc542f4d` (2026-08-27). All ACDC locators below are line numbers in that file, cited as `toip/v1.1:spec/spec-body.md:NNN`, unless a passage is explicitly noted as `main`-only. I diffed `v1.1` against `toip/main` (`f0bd097de318fbbe2d069a2b46cecd42550762e3`, 2026-08-28; 92 hunks, 338 insertions/386 deletions on `spec/spec-body.md`) and against the previously-vendored checkout this inventory was built from (`fix-worked-examples-schema-1520`, commit `651df33e14396d5a79e1b1abf419111a97a97f42`, 2026-07-21, still checked out at `HEAD` in the vendored repo — left untouched, per instructions, not repointed). The vendored repo's checked-out branch was **not** changed by this work. Every hunk in both diffs is accounted for in "Corrections from the 2026-09-05 revision" below. The local vendored checkout is stale relative to `v1.1` on exactly the same points the old inventory was; it is no longer used as a source.
- **CESR**: vendored at `~/code/me/kswg-cesr-specification`, `spec/spec-body.md`. Checked-out branch `pq`, still at commit `34c3978d5cd7531897dfdd26d954051937ff0640` (re-verified 2026-09-11, unchanged since the prior revision). Re-diffed against `trustoverip/kswg-cesr-specification@main` (`bad6edd84f928fe1e77a722edbdd829e0878377f`, 2026-08-28): the only differences remain the unmerged post-quantum-signature-code addition (Annex A code table plus one Annex prose section), confined to content not cited here — Version String field and SAID section are untouched and identical. No CESR claim in this document changes.
- **Dossier**: vendored at `~/code/me/kswg-dossier-specification`, `spec/dossier-spec-body.md`. Checked-out branch `ci-pages-step-strict`, now at commit `7669358f3cfd754c2544d451aca48e2045603909` (2026-09-03) — still **materially behind** `trustoverip/kswg-dossier-specification@main` (`b9227753cc1bbb92ed237970fc3b89bf1d0c904f`, 2026-08-25, re-fetched and re-verified 2026-09-11, unchanged since the prior revision): main still replaces "signing" terminology with "anchoring" throughout. All dossier quotes in this document are taken from the **upstream `main` capture**, not the vendored checkout, for the same reason as before. No dossier claim in this document changes.

---

## Corrections from the 2026-09-05 revision

The prior revision of this document was built from the vendored ACDC checkout at commit `651df33` (2026-07-21), cross-checked only against `trustoverip/kswg-acdc-specification@main`. Per AGENTS.md rule 5, that was checking the wrong branch for content: `v1.1` carries the substantive changes below, all present at `toip/v1.1:910c74a` and absent from `main`. Every item is a **correction to a specific prior claim**, not new material invented independently of it.

1. **`E1E` — was "not part of the published spec," is now normative.** The prior revision's Edge-operator section stated: *"A proposed but not-yet-normative fifth operator, `E1E`... exists only on an unmerged local ACDC-repo branch... and is not part of the published spec"* and listed it as **Open question 1**, unresolved. This was wrong for `v1.1`: `E1E` is in the normative unary operator table (`toip/v1.1:spec/spec-body.md:1206`), with full semantics (`:1223`) and an amended default-injection clause that names it (`:1209`). See §3 above. The prior revision's own cross-check only reached `main`, which genuinely lacks it — the error was in trusting that check as sufficient for a two-branch repository, exactly the failure mode [reviews/2026-09-06-operator-semantics-adjudication.md](../../reviews/2026-09-06-operator-semantics-adjudication.md) documents.
2. **`dp` (Disclosure Paths) — was absent from this document entirely; a related finding (SPC-F4) called a `dp`-dependent design "an unresolvable reference... an unmerged construct from a keripy discussion."** That characterization, made by a review panel reading `main`, is retracted by the 2026-09-10 correction cited above. `dp` is a full normative section on `v1.1` (16 occurrences, 4 section headings, `toip/v1.1:spec/spec-body.md:1809-1994`), merged as PR #203. See new §9 above.
3. **Field-label restrictions (`-` forbidden, bare `_` reserved) — entirely new content, not present in the prior revision in any form.** Added to §1 above, `toip/v1.1:spec/spec-body.md:61-69`.
4. **The `_` DAG-hop virtual label — entirely new content.** Added to §1 above; flagged there as a rendering hazard per the task brief (`toip/v1.1:spec/spec-body.md:55`, `65-67`).
5. **The `u` field's title — was "UUID" throughout this document; is now "UE" (unique entropy).** Every quoted passage, table cell, and prose reference to "UUID" in the prior revision is updated to "unique entropy" / "UE" where quoting `v1.1`, with the old term retained only where explicitly discussing the rename (§1) or quoting `main` for contrast. This is a renaming, not a semantics change — flagged so a reader comparing this document against the live spec is not confused by an apparent mismatch.
6. **Primary ACDC source repointed.** The prior revision's primary source was the vendored local checkout (branch `fix-worked-examples-schema-1520`, commit `651df33`), cross-checked against `main`. This revision's primary source is `toip/v1.1` at commit `910c74a`, read directly via the `toip` remote; the vendored checkout is no longer cited as a source for ACDC content (see "Sources read" above). This corrects the vendoring problem identified in the review's "process failures" section — checking one branch of a two-branch repository was never a sufficient cross-check.
7. **A derivation-path-collision claim is retracted.** The prior revision stated bulk-issuance derivation-path collisions between the top-level `u`, per-attribute `u`, and the separate blinding factor `v_k` were "a live correctness concern the spec addresses explicitly on `main`." Re-checked directly: **neither `main` nor `v1.1` contains this language.** It exists only on unmerged feature branches in the local ACDC repo. See the "Derivation in bulk/selective contexts" note in §1 above.
8. **Two incidental findings, neither in the prior revision, neither relied upon by any claim in this document:** a leftover "UUID" (not renamed to "UE") appears three times within the new Disclosure Paths section on `v1.1` (`:1869`, `:1871`, `:1923`), evidently merged separately from the rename sweep; and a pre-existing "UUDI" typo at `:2956` was likewise untouched by the rename. Recorded because a future reader diffing quotes against a re-fetched `v1.1` might otherwise take these as transcription errors in this document rather than in the spec itself.
9. **Every locator in this document that predates this revision has been re-verified against `toip/v1.1:910c74a` and updated where the underlying line moved** (the two branches diverge by 92 hunks / 338 insertions / 386 deletions on `spec/spec-body.md`, most of it the UUID→UE rename). Locators for §7 (dossier) and §8 (CESR) are unchanged — neither source spec changed.
10. **All hunks in both diffs accounted for.** Diffing `toip/main` against `toip/v1.1` (92 hunks) and diffing the old vendored checkout against `toip/v1.1` (93 hunks, effectively the same substantive set) turned up exactly the changes enumerated above as corrections 1–5 and 7, plus the `main`-only worked-examples block addressed in "Open questions" item 2 below, plus one cosmetic rename ("Annex" → "Annex C") and one heading correction ("Universally Unique Identifier (UUID) Fields" → "Unique Entropy (UE) Fields", part of correction 5). No other substantive hunk exists in either diff.

---

## 1. Top-level ACDC fields

Quoted directly from the spec's own table (`toip/v1.1:spec/spec-body.md:16-28`, "Top-Level Fields"):

| Label | Title | Type / value | Required? | Meaning (spec's own words) |
|---|---|---|---|---|
| `v` | Version String | fixed-format string | **Required** | "Regexable format: `ACDCMmmGggKKKKSSSS.` that provides protocol type, version, CESR genus version, serialization type, size, and terminator" (line 18) |
| `t` | Message Type | 3-char string | Optional (see below) | "Three-character Message type" (line 19) |
| `d` | Message Digest SAID | SAID | **Required** | "Self-referential fully qualified cryptographic digest of enclosing map" (line 20) |
| `u` | UE (Unique Entropy) | fully-qualified nonce | Optional | "Random unique entropy as fully qualified high entropy pseudo-random string, a salty nonce" (line 21) — **renamed from "UUID"**, see the UE terminology note under §1 below |
| `i` | Issuer AID | AID | **Required** | "Autonomic Identifier whose control authority is established via KERI verifiable Key State" (line 22) |
| `rd` | Registry Digest SAID | SAID | Optional | "Issuance and/or revocation, transfer, or retraction registry for ACDC" (line 23) |
| `s` | Schema | SAID or block | **Required** | "Either the SAID of a JSON Schema block or the block itself" (line 24) |
| `a` | Attribute | SAID or block | Optional | "Either the SAID of a block of Attributes or the block itself" (line 25) |
| `A` | Attribute Aggregate | AGID or block | Optional | "Either the Aggregate of a selectively disclosable block of attributes or the block itself" (line 26) |
| `e` | Edge | SAID or block | Optional | "Either the SAID of a block of Edges or the block itself" (line 27) |
| `r` | Rule | SAID or block | Optional | "Either the SAID a block of Rules or the block itself [sic]" (line 28) |

**Field ordering** (`toip/v1.1:spec/spec-body.md:32`): "When present, the top-level fields MUST appear in the following order: `[v, t, d, u, i, rd, s, a, A, e, r]`."

**Required fields** (`toip/v1.1:spec/spec-body.md:36`): "The following fields are REQUIRED `[v, d, i, s]` i.e. they MUST appear in any ACDC (not to be confused with other message types in the ACDC protocol)." `t` is not in this list for the plain (implied-`acm`) case, but becomes conditionally required — see below.

**`a`/`A` mutual exclusion**: `a` field (line 117): "An ACDC MUST not have both an `a` field and an `A` field ... when it has either." Confirmed for `A` at line 121. Confirmed again for the fixed-field CESR-native message form (`toip/v1.1:spec/spec-body.md:3179`): "the value of either or both the `a` and `A` field MUST be empty. To clarify, both the `a` and `A` field values MUST not be non-empty, one or the other or both MUST be empty."

**Message-type conditionality of `t`** (`toip/v1.1:spec/spec-body.md:83`): "The presence of the message type field, labeled `t`, is optional for messages of type `acm` with non-CESR-native serialization kinds. It MUST be present in any `acm` message that uses a CESR serialization kind... It MUST be present in messages with any other message type, regardless of the kind of serialization. A message without a message type, `t`, field is assumed to be of type `acm`."

### Other reserved (non-top-level) fields

`toip/v1.1:spec/spec-body.md:38-55`, "Other Reserved Fields" — these MAY appear at other levels besides the top level. **This table gained a tenth row on `v1.1`, the `_` DAG-hop virtual label** (see "The `_` DAG-hop virtual label" below):

| Label | Title | Meaning |
|---|---|---|
| `d` | Digest SAID | same semantics as top-level, self-referential to enclosing map |
| `u` | UE | "Random unique entropy ... a salty nonce" — **renamed from "UUID"** |
| `i` | Identifier AID | "Context-dependent AID as determined by its enclosing map such as Issuee identifier" |
| `rd` | Registry Digest SAID | "Issuance and/or revocation, transfer, retraction, or usage registry for ACDC when not at top-level" |
| `dt` | Datetime | "Context-dependent ISO datetime string" |
| `n` | Node | "SAID of another ACDC as the terminating point (vertex) of a directed Edge" |
| `o` | Operator | "Either unary operator on Edge or m-ary operator on edge-group" |
| `w` | Weight | "Edge weight property ... for directed weighted edges and operators" |
| `l` | Legal Language | "Text of Ricardian contract clause" |
| `_` | DAG Hop | **New, normative, `v1.1` only.** "Virtual label that denotes the traversal (hop) from an Edge in the near-side ACDC to the top level of the far-side ACDC referenced by that Edge's Node, `n`, field. It appears only in an expansion of a DAG of chained ACDCs and MUST NOT appear as a field label in an ACDC" (`toip/v1.1:spec/spec-body.md:55`) — see "The `_` DAG-hop virtual label" below |

**Compact labels, rationale** (`toip/v1.1:spec/spec-body.md:58`): field labels are "meant to support resource-constrained applications such as supply chain or IoT," using at most two characters.

### Field label restrictions — new, normative, `v1.1` only

`v1.1` adds a new subsection, "Field Label Restrictions" (`toip/v1.1:spec/spec-body.md:61-69`), immediately after Compact Labels and before Version String Field. Two characters are now reserved out of field labels, for the benefit of the new [Disclosure Paths](#9-disclosure-paths-dp--new-normative-construct-v11-only) path syntax below:

- **`-` is forbidden in any ACDC field label.** "When a path is serialized compactly as a CESR primitive, the path delimiter, `/`, is replaced by `-`, so that the result is pure Base64 and no character has to be expanded into a Base64 equivalent. A field label in an ACDC MUST NOT, therefore, contain the character `-`" (`toip/v1.1:spec/spec-body.md:63`). This is directly a rendering concern: a renderer that encounters a `-` in what it takes to be a field label has either mis-parsed a compact path or is looking at something that is not a valid ACDC.
- **A bare `_` is reserved as the virtual DAG-hop label and MUST NOT be used as a real field label.** "With `-` reserved as the compact path delimiter, the only Base64 character left to denote a hop across an Edge is `_`. The label `_` MUST therefore be reserved as a virtual path component denoting that hop... A field in an ACDC MUST NOT be labeled with a single `_`. Only that label is forbidden; `_` MAY appear within a longer label, such as `first_name`" (`toip/v1.1:spec/spec-body.md:65`). See "The `_` DAG-hop virtual label" immediately below.
- **Scope**: both restrictions govern "the labels of its top-level fields and of the fields within its Attribute, Aggregate, Edge, and Rule sections," but not the Schema Section, whose labels are JSON Schema vocabulary, not Issuer-chosen (`toip/v1.1:spec/spec-body.md:69`).

### The `_` DAG-hop virtual label — new, normative, `v1.1` only

`_` is not a field an Issuer ever writes into an ACDC. It is a synthetic label that appears only when a DAG of chained ACDCs is *expanded* into a single field map for path-addressing purposes: "In such an expansion, each Edge block gains a field labeled `_` whose value is the subgraph contributed by the far-side ACDC named by that Edge's Node, `n`, field. Because every hop supplies such a field, a path across the DAG needs no delimiter but `/`" (`toip/v1.1:spec/spec-body.md:67`). This is directly a rendering concern flagged in the task brief: **a renderer that walks an expanded DAG and displays every field label verbatim would show `_` as if it were real data.** It is not — it marks a hop across an Edge to the far-side ACDC's top level, and MUST NOT appear as a label an Issuer chose. Any arcviz code that lists an ACDC's (or an expanded DAG's) field labels for display must special-case `_` as synthetic/structural, not data.

### The `u` field, the blinding mechanism — F0 — renamed "UUID" → "unique entropy (UE)" on `v1.1`

**Terminology change, not a semantics change.** On `v1.1`, every occurrence of "UUID" describing the `u` field is renamed to "unique entropy" / "UE" (merged as PR #191/194, per the 2026-09-10 correction in [reviews/2026-09-06-operator-semantics-adjudication.md](../../reviews/2026-09-06-operator-semantics-adjudication.md)). The mechanism, requirements (approximately 128 bits of entropy), and every present/absent/empty rule below are byte-for-byte the same; only the name changed, e.g. the field's title cell in the top-level table read "UUID" and now reads "UE" (`toip/v1.1:spec/spec-body.md:21`), and the section heading changed from "Universally Unique Identifier (UUID) Fields" to "Unique Entropy (UE) Fields" (`toip/v1.1:spec/spec-body.md:98`). **The previous revision of this inventory used "UUID" throughout; that is now the stale term** — see "Corrections from the 2026-09-05 revision" below. This document now uses "unique entropy" / "UE" when describing the current spec, and calls out "UUID" only when quoting or contrasting the old term.

`toip/v1.1:spec/spec-body.md:100`: "Without the entropy provided by the unique-entropy, `u`, field, an adversary may be able to reconstruct the block contents merely from the SAID of the block and the Schema of the block using a rainbow or dictionary attack on the set of field values allowed by the Schema."

`toip/v1.1:spec/spec-body.md:102` (general rule, applies at any nesting level): "A unique-entropy, `u` field, MAY optionally appear in any block (field map) at any level of an ACDC. Whenever a block in an ACDC includes a unique-entropy, `u`, field then, its associated SAID, `d`, field makes a blinded commitment to the contents of that block. The unique-entropy, `u`, field is the blinding factor... With an embedded unique-entropy field value that contains sufficient cryptographic entropy, the block contents can only be discovered if the included unique-entropy field is explicitly disclosed."

**What an observer can and cannot infer from a blinded field:** given only the block's Schema and its SAID (no `u` disclosed), the adversary "is not able to discover the remaining contents of the ... block in a computationally feasible manner, such as a rainbow table attack" (recurring formula, e.g. `toip/v1.1:spec/spec-body.md:351`, `711`, `1104`, `1173`, `1289`). Concretely: an observer can know the *shape* (schema) of a blinded block and can verify set-membership / inclusion once given a candidate value plus the `u`, but cannot brute-force the value from `d` + schema alone when `u` has "approximately 128 bits of entropy" (recurring, e.g. line 1104). Presence vs. absence of `u` is itself the public/private distinction at any level: no top-level `u` ⇒ **Public ACDC** (`toip/v1.1:spec/spec-body.md:171`); present with sufficient entropy ⇒ **Private ACDC** (`toip/v1.1:spec/spec-body.md:175`); present but **empty** ⇒ **Metadata ACDC** (`toip/v1.1:spec/spec-body.md:177`, see §5 below). The same present/absent/empty three-way logic applies independently at the Attribute-block level (`toip/v1.1:spec/spec-body.md:317`, "Two other variants, namely private (public), are defined respectively by the presence (absence) of a unique-entropy, `u`, field") and at the Edge-block level (`toip/v1.1:spec/spec-body.md:1175`: "The absence of the unique-entropy, `u` field in an Edge block makes that edge a Public Edge. The presence of the unique-entropy, `u` field ... makes that Edge a Private Edge.")

**Derivation in bulk/selective contexts**: `u` values may be independently random per block, or hierarchically-deterministically (HD) derived from a shared secret salt plus a path string (`toip/v1.1:spec/spec-body.md:2954`, "Hierarchical derivation at issuance of selectively disclosable attribute ACDCs," and the parallel Bulk Issuance annex section at `toip/v1.1:spec/spec-body.md:2990`). **Correction from the prior revision**: that revision asserted derivation-path collisions between the top-level `u`, per-attribute `u`, and the bulk blinding factor `v_k` were "addressed explicitly on `main`." Re-checked directly against both `toip/main` and `toip/v1.1`: **neither branch contains any such language** — no hits for "collision," "v_k," or "derivation-path radix" tied to this topic in either file. That content exists only on unmerged feature branches in the local ACDC repo (`fix-bulk-issuance-derivation`, `pin-derivation-path-radix`, `indep-registry-bulk-issuance`), none merged into either `main` or `v1.1` as of this reading. The prior claim is retracted; this remains an open, unresolved concern on neither published line. **Incidental finding, not previously flagged**: `toip/v1.1:spec/spec-body.md:2956` still reads "UUDI" (a pre-existing typo for UUID) and was *not* touched by the UE rename sweep, even though the parallel sentence at `toip/v1.1:spec/spec-body.md:2990` was correctly updated to "unique-entropy" — a leftover of the rename, not a claim this document relies on.

---

## 2. `a` (Attribute) vs. `A` (Attribute Aggregate) — the heart of selective disclosure

These are **two different graduated-disclosure mechanisms with different names in the spec's own vocabulary**, not interchangeable synonyms. `toip/v1.1:spec/spec-body.md:672`: "A selectively disclosable blinded Aggregate section appears at the top level using the field label `A`. This is distinct from the field label `a` for a partially disclosable Attribute section. This makes clear (unambiguous) the semantics of each respective section's associated Schema."

| | `a` — Attribute section | `A` — Aggregate section |
|---|---|---|
| Disclosure mechanism named by the spec | **Partial Disclosure** | **Selective Disclosure** |
| Shape | a single nested field map (block), possibly nested further | an ordered **list/array** of independently blinded blocks, plus one aggregate value at index 0 |
| Compact form's value | the block's own SAID (`d`) | the **AGID** (Aggregate ID) — explicitly *not* a SAID: "the value of a compact variant of the selectively disclosable Aggregate section is an aggregate, AGID, (Aggregate ID) not a SAID" (line 672) |
| Granularity of disclosure | all fields in a given (sub)block disclose together: "All fields in a given block MUST be disclosed together as a set. When a blinded attribute block has more than one attribute field, then each field in the block is not independently selectively disclosable" (line 703) — nesting sub-blocks lets you partially disclose at finer grain, one sub-block at a time | each element of the array is independently, and unorderedly, discloseable: "Membership of any blinded commitment to a value in the list of aggregated blinded commitments may be proven without leaking (disclosing) the unblinded value belonging to any other blinded commitment in the list" (line 697) |
| What "Full Disclosure" means in context | exposes, at minimum, "the labels of other fields in its enclosing block" even before those fields' *values* are shown (line 1791, 1793) | exposes **nothing** about other still-undisclosed elements, "including their labels" (line 1791) — field labels live *inside* each blinded block, so undisclosed labels are also hidden (line 705: "because the field labels for a given block only appear within that blinded block, the field labels are also blinded") |
| Ordering leakage | n/a (single block) | explicitly defeated: "The order of appearance of elements in an `anyOf` subschema for the Aggregate array is not correlated to the actual order of appearance of the associated block or blocks in the blinded array itself. This prevents inference based on location in the blinded array" (line 705) |

**The precise Partial-vs-Selective distinction, in the spec's own summary** (`toip/v1.1:spec/spec-body.md:1791`): "A salient difference between Partial Disclosure and Selective Disclosure of a given block is the degree to which information about other fields is exposed in order to make Full Disclosure of its detailed field values. A partially disclosable block, when fully disclosed, exposes, at the very least, the labels of other fields in its enclosing block (a field map). Whereas a selectively disclosable block, when fully disclosed, does not expose any information about other yet-to-be-exposed fields, including their labels in its enclosing block (a field map array)."

**AGID computation** (`toip/v1.1:spec/spec-body.md:723-731`): the zeroth list element is a placeholder (dummied with `#` characters equal to the digest length), the remaining `N` elements are the blindable blocks' own SAIDs; AGID = digest of the ordered serialized list with the placeholder filled in: "AGID = H(C(a_i for all i in {0, ..., N}))". A worked JSON example with real values is at lines 915-967; a worked CESR-native example at 991-1035.

**Reserved fields inside Aggregate blocks** (`toip/v1.1:spec/spec-body.md:679-688`): `d`, `u`, `i`, `dt` — same semantics as elsewhere (`u` renamed to unique entropy). Each blindable block additionally carries its one or more attribute-specific fields.

**New in this section on `v1.1`: Aggregate Section pathing.** A blinded attribute block MAY now be addressed in a Disclosure Paths, `dp`, entry by its uniquely-labeled attribute field instead of its array offset — see "Aggregate Section Pathing" in §9 below. This is new normative machinery, not a restatement of anything in the prior revision.

**Consistency rule**: `toip/v1.1:spec/spec-body.md:121` and `117` both state the ACDC "MUST not have both a non-empty `a` field value and a non-empty `A` field value ... when it has either" — i.e., an ACDC picks one graduated-disclosure mechanism for its payload, not both simultaneously.

---

## 3. Edge section (`e`), in full

### Block types

`toip/v1.1:spec/spec-body.md:1065-1069`: two block types nest inside `e` — **Edge-groups** and **Edges**. "An Edge MUST contain a node, `n` field. An Edge-group MUST NOT have a node, `n` field." The top-level `e` field is itself an Edge-group (line 1069).

### Edge-group reserved fields

`toip/v1.1:spec/spec-body.md:1087-1094`, order `[d, u, o, w]` when present:

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | "self-referential fully qualified cryptographic digest of enclosing Edge-group block" |
| `u` | Optional | blinding nonce (unique entropy), same semantics as elsewhere |
| `o` | Optional | "m-ary operator on the Edges in the Edge-group" |
| `w` | Optional | "property for nested Edges or Edge-groups for weighted average `WAVG` operator" |

"An Edge-group MUST NOT have a node, `n`, field" (line 1096). "The top-level Edge-group MUST NOT have a weight, `w` field, because it is not a member of another Edge-group" (line 1131).

**m-ary (Edge-group) operators**, `toip/v1.1:spec/spec-body.md:1112-1119`:

| Operator | Meaning | Default |
|---|---|---|
| `AND` | "Logical AND of the validity of the Edge-group members. Edge-group is valid only if all members are valid." | **Yes** |
| `OR` | "Logical OR ... valid if one of the members is valid." | No |
| `NAND` | "Logical NAND ... valid only if not all members are valid." | No |
| `NOR` | "Logical NOR ... valid only if all members are invalid." | No |
| `AVG` | "Arithmetic average of a given Edge-group member property. Averaged property is defined by the schema or EGF." | No |
| `WAVG` | "Weighted arithmetic average ... Weight is given by the `w` field." | No |

Missing/absent `o` on an Edge-group defaults to `AND` (line 1121). **This m-ary table is unchanged between `main` and `v1.1`.** The dossier specification's `MxN`/`RMxN`/`MxQ`/`RMxQ` threshold operators (§7 below) are a distinct, sibling-spec extension of this same `o` field on an edge-group — not part of this table on either branch.

### Edge reserved fields

`toip/v1.1:spec/spec-body.md:1151-1160`, order `[d, u, n, s, o, w]` when present:

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID of the Edge block |
| `u` | Optional | blinding nonce (unique entropy) — presence makes it a **Private Edge**, absence a **Public Edge** (line 1175) |
| `n` | **Required** | "Required SAID of the far node ACDC as the terminating point of a directed edge that connects the Edge's encapsulating near node ACDC to the specified far node ACDC" |
| `s` | Optional | "Optional SAID of the JSON Schema block of the far node ACDC" |
| `o` | Optional | unary operator(s) on this Edge (list below) |
| `w` | Optional | "edge weight property that enables ... weighted average" |

**Unary (per-Edge) operators — the complete normative list, now five operators on `v1.1`** (`toip/v1.1:spec/spec-body.md:1203-1207`):

| Operator | Meaning (verbatim) | Default |
|---|---|---|
| `I2I` | "Issuer-To-Issuee, The Issuer AID of this ACDC MUST be the Issuee AID of the node this Edge points to." | **Yes**, when applicable (see default-injection rule below) |
| `NI2I` | "Not-Issuer-To-Issuee, The Issuer AID of this ACDC MAY or MAY not be the Issuee AID of the node that this Edge points to." | No |
| `DI2I` | "Delegated-Issuer-To-Issuee, The Issuer AID of this ACDC MUST be either the Issuee AID or a delegated AID of the Issuee AID of the node this Edge points to." | No |
| `E1E` | **New on `v1.1`.** "IssueE-To-IssueE, The Issuee AID of this ACDC MUST be the Issuee AID of the node this Edge points to. This is an identity relation on the two ACDCs' Issuees and places no constraint on either ACDC's Issuer." | No, and **also exempted from default-injection** (see below) |
| `NOT` | "Logical NOT. The validity of the node this Edge points to is inverted. If valid, then not valid. If invalid, then valid." | No |

**`E1E` full semantics** (`toip/v1.1:spec/spec-body.md:1223`): "The `E1E` unary Operator, when present, means that the Issuee AID of the current ACDC in which the Edge resides MUST be the Issuee AID of the node to which the Edge points. Unlike `I2I` and `DI2I`, which are delegative Operators that constrain the Issuer AID of the current ACDC relative to the Issuee AID of the node the Edge points to, `E1E` is an identity relation between the two ACDCs' Issuee AIDs and places no constraint on either ACDC's Issuer AID. Therefore, to be valid, both the ACDC in which the Edge resides and the node to which the Edge points MUST be Targeted ACDCs (each MUST have an Issuee), and the Edge is valid when, and only when, those two Issuee AIDs are equal. This supports use cases in which two ACDCs describe the same subject (share an Issuee) but are issued by different Issuers, so the Issuer of neither ACDC is the Issuee of the other. An example is a core identity credential and a separate entitlement credential issued to the same Issuee by different Issuers: `E1E` binds them as being about the same subject, a relationship the delegative `I2I` Operator cannot express because `I2I` would instead require the entitlement ACDC's Issuer to be the core credential's Issuee."

**Default-injection rule, amended for `E1E`** (`toip/v1.1:spec/spec-body.md:1209`, load-bearing — arcviz must reproduce this to render edge validity correctly when `o` is absent): when `o` is missing/empty or contains none of `I2I`/`NI2I`/`DI2I`/**`E1E`**: "If the node pointed to by the Edge is a targeted ACDC, i.e., has an Issuee, then the `I2I` Operator MUST be appended... If the node pointed to by the Edge block is an Untargeted ACDC i.e., does not have an Issuee, then the `NI2I` Operator MUST be appended." **This is the amendment the task brief calls for**: on `main` the injection clause names only `I2I`/`NI2I`/`DI2I` (`toip/main:spec/spec-body.md:1197`), so `main`-only knowledge would wrongly inject `I2I` onto an edge that actually carries `E1E`. On `v1.1`, `E1E` suppresses injection exactly like the other three named operators.

`o` may be a **list** of unary operators; on conflict, "the latest Operator among the conflicting Operators in the list takes precedence" (line 1197).

### What an Edge does and does not transfer — F1 (governs what arcviz may imply about a parent from a child)

**Validity requirement, minimum** (`toip/v1.1:spec/spec-body.md:1185`): "In order for a given Edge to be valid, at the very least, a Validator MUST confirm that the SAID of the provided far node ACDC matches the node, `n` field value given in the near node ACDC Edge block and MUST confirm that the provided far node ACDC satisfies its own schema." If the Edge's own `s` field is present, the far node must *additionally* validate against that schema (line 1185, 1189).

**An Edge transfers, or constrains:**
- **Identity/authority linkage** between the near ACDC's Issuer and the far ACDC's Issuee, per the unary operator in force (`I2I`, `NI2I`, `DI2I`, or, on `v1.1`, `E1E`) — this is a constraint on *who may legitimately be the near-node Issuer* (or, for `E1E`, a constraint that both share an Issuee), not a transfer of the far node's attribute values.
- **A schema constraint** on the far node, via the optional `s` field (line 1187-1189) — "an additional constraint on the far node ACDC," used e.g. to force forward-compatibility across minor schema versions (line 1191-1193).
- **A weight** (`w`), for aggregation by an enclosing Edge-group's `WAVG`/`AVG` operator (line 1229-1231) — a property *of the edge*, not of either endpoint.
- **Validity propagation**, EGF-dependent, along a chain/tree: "When any node in a provenance chain is invalid, an Edge pointing to that node MAY also be invalid. If a node has an invalid Edge, then the node MAY also be invalid" (line 1125) — note the modal "MAY", not "MUST"; the spec explicitly defers the actual propagation logic to the ecosystem governance framework (line 1123: "the actual logic for interpreting the validity of a set of chained or treed ACDCs is EGF-dependent").

**An Edge does NOT transfer:**
- **Attribute values.** Nothing in the Edge block's reserved-field set (`d,u,n,s,o,w`) carries any of the far node's `a`/`A` payload. A near-node ACDC's Edge is a cryptographic pointer plus a validity/schema constraint; reading a far node's attributes requires fetching and independently validating that far node.
- **The far node's Issuee identity by default.** `NI2I` explicitly "removes or nullifies any requirement" that the near Issuer equal the far Issuee (line 1219) — so absent a stated `I2I`/`DI2I`/`E1E`, arcviz may **not** assume any identity relationship between the two ACDCs' principals.
- **Blinded/private detail, when the Edge or the far node is private.** A "Compact Private Edge... enables a presenter of that ACDC to make a verifiable commitment to the ACDC attached to the Edge without disclosing any details of that ACDC, including the ACDC's SAID" (line 1176) — so a rendered graph may have to show an edge whose far-node identity is itself undisclosed.
- **Node-vs-Edge-group distinction is structural, not optional**: "Each nested block in every Edge-group MUST have its own field with its own local (to the ACDC) label... each nested block MUST NOT include a type field. The type of each block is provided by that associated subschema" (line 1139-1141) — i.e., there is no ACDC-carried "edge type" string; the type comes from which labeled subschema slot the edge occupies, which arcviz must resolve against the (possibly-external) schema to know what an edge "means" semantically, beyond its structural operator.

**Compact and simple-compact Edge forms** (`toip/v1.1:spec/spec-body.md:1167-1239`): a Compact Edge replaces the whole block with its SAID (public if no `u`, private if `u` present, line 1169, 1176); a **Simple compact edge** applies only "When an Edge sub-block has only one field, that is, its node, `n` field" — then "the labeled Edge field value is the value of its node, `n`, field" directly (no SAID indirection) and "The Edge is, therefore, public" (line 1239).

### Property-graph framing

`toip/v1.1:spec/spec-body.md:1073`: "A set of ACDCs as nodes connected by edges forms a labeled property graph (LPG) or property graph (PG) for short... The properties of each node (ACDC) are provided essentially by its Attribute Section. The properties of each edge are provided by the combination of Edge blocks and Edge-group blocks." Edges form a DAG (line 1183: "The edges and nodes form a directed acyclic graph (DAG)").

---

## 4. Rule section (`r`) — how legal prose is carried

`toip/v1.1:spec/spec-body.md:1253`: "The purpose of the Rules section is to provide a set of rules or conditions as a Ricardian Contract. The important features of a Ricardian contract are that it is both human and machine-readable and referenceable by a cryptographic digest."

**Block types**: **Rule-groups** and **Rules**, same nesting discipline as Edge/Edge-group (`toip/v1.1:spec/spec-body.md:1259-1263`). A Rule-group is "indicated by the presence of one or more non-reserved labeled fields whose value represents a nested Rule or Rule-Groups" (line 1263).

**Rule-group reserved fields**, order `[d, u, l]` (`toip/v1.1:spec/spec-body.md:1271-1281`):

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID |
| `u` | Optional | blinding nonce, unique entropy (Rule-group may thereby be made private/confidential, line 1327) |
| `l` | Optional | "legal language for the Rule-group" |

**Rule (leaf) reserved fields**, order `[d, u, l]` (`toip/v1.1:spec/spec-body.md:1306-1314`):

| Field | Required? | Meaning |
|---|---|---|
| `d` | Optional | self-referential SAID |
| `u` | Optional | blinding nonce (unique entropy) |
| `l` | **Required** | "The actual legal language for the clause." |

`toip/v1.1:spec/spec-body.md:1314`: "A Rule MUST have a Legal, `l`, field... A Rule MUST NOT have any other fields. In this sense, a Rule is a terminal node in a sub-graph of Rule-groups and Rules."

**Compact and Simple-compact Rule forms**: a Compact Rule replaces the block with its SAID, public or private depending on `u` presence (line 1321, same logic as Edges). A **Simple Compact Rule** applies "When a Rule block has only one field, that is, its legal, `l` field" — then "the block is represented as a single rule field and that labeled rule field value is what would have been the value of the block's legal, `l` field," and "The Rule block (rule) is, therefore, public" (line 1337).

**Discovery**: `toip/v1.1:spec/spec-body.md:1267` — Rule-section SAIDs can be resolved out-of-band via OOBI or attachment at issuance, "the essence of Percolated Discovery," same mechanism as for Edge-referenced ACDCs (line 1081).

---

## 5. Every disclosure variant, by the spec's own names

`toip/v1.1:spec/spec-body.md:1761-1788` gives the canonical enumeration under "Graduated Disclosure":

> "There are several graduated disclosure mechanisms as follows: Compact Disclosure, Metadata Disclosure, Partial Disclosure, Nested Partial Disclosure, Full Disclosure, Selective Disclosure, Bulk-issued Instance Disclosure. ... All the Graduated Disclosure mechanisms MAY be used in combination."

For each, exactly what's present / digest-only / absent, quoted:

| Variant | What's present | What's a digest only | What's absent | Spec quote / locator |
|---|---|---|---|---|
| **Compact Disclosure** | the section/block's SAID | the block's actual content (behind its SAID) | — (nothing is unrecoverable; it's an "undisclosed yet" state, not a redaction) | "relies on the inclusion in that block of a cryptographic digest of the content (SAID)... Disclosure of the SAID makes a verifiable commitment to its data that MAY be more fully disclosed later." (`toip/v1.1:spec/spec-body.md:1775`) |
| **Metadata Disclosure** | Issuer, Schema, provenanced Edges, Rules — via an ACDC with an **empty** top-level `u` field | the real ACDC's top-level `d` (unreachable from the metadata ACDC's `d`, since they're cryptographically distinct: "The top-level SAID, `d`, field, of the metadata ACDC, is cryptographically derived from an ACDC with an empty top-level unique-entropy, `u`, field so its value will necessarily be different from that of an ACDC with a high entropy top-level unique-entropy" — line 179) | the top-level Attribute (`a`) or Aggregate (`A`) field value, which "MAY be empty or missing so that its value is not correlatable across disclosures" (line 179); also, "only cryptographic commitments from the Discloser are attached, not commitments from the Issuer" (line 183) | "provide a mechanism for a Discloser to make cryptographic commitments to the metadata of a yet to be disclosed private ACDC without providing any point of correlation to the actual top-level SAID" (`toip/v1.1:spec/spec-body.md:177-179`); enumerated under Graduated Disclosure at line 1777 |
| **Partial Disclosure** | the block's SAID (`d`) plus its blinding nonce (`u`), once disclosed | before `u` is disclosed: the block's content is blinded behind `d` even though `d` is visible | field values not yet disclosed; but the **labels** of sibling fields in the enclosing map are exposed once any partial disclosure of that map happens (line 1793) | "relies upon a cryptographic digest (SAID) of the content and a salty nonce (UE) embedded in that content... The content remains blinded in spite of disclosure of its SAID until and unless the salty nonce (UE) is also disclosed." (`toip/v1.1:spec/spec-body.md:1779`) |
| **Nested Partial Disclosure** | same mechanism as Partial Disclosure, applied independently at each level of a nested block tree | any not-yet-expanded sub-block, behind its own `d`+`u` | deeper branches not yet expanded | "relies on each nested block embedding both its digest (SAID) and a salty nonce (UE). This allows the Partial Disclosure of different branches of the tree at different levels of nesting." (`toip/v1.1:spec/spec-body.md:1781`); worked example at lines 514-668 |
| **Full Disclosure** | everything in the disclosed block/section, unhidden | nothing (within the scope being "fully disclosed") | nothing (within scope) | "Full Disclosure is disclosure without hiding a given block's content behind SAIDs or salted SAIDs." (`toip/v1.1:spec/spec-body.md:1783`). Note the spec's own caveat on scope-dependence of the term, line 1793: in a Partial-Disclosure context, "Full Disclosure" of a nested block still means "at least the disclosure of the labels of all the fields in the enclosing blocks of that branch" — it is not necessarily disclosure of the *entire ACDC*. |
| **Selective Disclosure** | the AGID (`A` compact) plus whichever Aggregate-array elements are chosen for disclosure, each with its own `d`,`u` | the other, undisclosed array elements — represented by their bare SAID strings in the list, contributing to the AGID digest but revealing nothing else, "including their labels" (line 1791) | field labels and values of undisclosed elements entirely | "relies on each element embedding its digest (said) and salty nonce (UE) as partially disclosable elements. ... Membership in the set can be verified against a set of SAIDs" (`toip/v1.1:spec/spec-body.md:1785`) |
| **Bulk-issued Instance Disclosure** | one member (copy) of a bulk-issued set, with its own unique `d`/`u` | the linkage between this copy and any sibling copy (each sibling has different, uncorrelated SAID/UE) | any other member's identity; optionally the shared `rd`, if nested inside `a`/`A` rather than top-level | "relies on issuing multiple instances of a given ACDC, each a copy but with unique instance identifiers so that the disclosure of one instance is not correlatable to another via the instance identifiers." (`toip/v1.1:spec/spec-body.md:1787`) |

**New in this section on `v1.1`, addressable via §9 below**: the Disclosure Paths, `dp`, construct gives every one of these variants a normative path syntax for specifying exactly which sections/blocks/elements a disclosure covers, replacing the `apply`/`offer` messages' informal "Attribute field label list, Aggregate element label list" (see §9).

### Also load-bearing for arcviz: the two *contractually-protected* wrappers around these mechanisms

`toip/v1.1:spec/spec-body.md:1795-1807`, "Contractually Protected Disclosure" is not itself a graduated-disclosure primitive but a **process** built on the above: "the potential Discloser first makes an offer using the least (Partial) Disclosure of some information about other information to be disclosed (Full Disclosure) contingent on the potential Disclosee first agreeing to the contractual terms."

- **Chain-Link Confidentiality Disclosure**: "imposes conditions and limitations on the further disclosure and/or use of the disclosed data ... applied to subsequent disclosures by the Disclosee that follow the data (hence chain-link)" (line 1804).
- **Contingent Disclosure**: "some contingency is specified in the Rules section that places an obligation by some party to make a disclosure when the contingency is satisfied" (line 1806) — e.g. escrow-triggered disclosure, enabling "latent accountability."

### The "compact vs. private/public vs. metadata" cross-cut (top level)

These three named ACDC **variants** are a separate axis from the graduated-disclosure list above, but interact with it directly and arcviz needs to represent both axes:

- **Compact ACDC** (`toip/v1.1:spec/spec-body.md:164-166`): every present top-level section field (`s,a,e,r`) is its SAID rather than its expanded block; `A`, when present, is compacted to its AGID instead (line 166, a special case: "the most compact form of the ACDC has the aggregate value as the value of the Aggregate section field... an Aggregate section uses its own algorithm for compact and un-compact (expanded) forms").
- **Public ACDC** (`toip/v1.1:spec/spec-body.md:171`): no top-level `u` — "the top-level, `d`, field is a cryptographic digest, [but] it may not securely blind the contents of the ACDC when knowledge of the Schema is available."
- **Private ACDC** (`toip/v1.1:spec/spec-body.md:175`): top-level `u` present with "sufficient cryptographic entropy" — "the top-level SAID, `d`, field of an ACDC could provide a secure cryptographic digest that blinds the contents."
- **Metadata ACDC** (`toip/v1.1:spec/spec-body.md:177`, see table row above): top-level `u` present but **empty**.

**IPEX cross-variant commitment note** (`toip/v1.1:spec/spec-body.md:2023`, load-bearing for how arcviz should treat "which variant did the Issuer actually sign"): "a signature on any variant MAY be used to verify the Issuer's commitment to any other variant either directly or indirectly, in whole or in part, on a top-level section-by-section basis. This cross-variant Issuer commitment verifiability is an essential property that supports Graduated Disclosure by the Disclosee of any or all variants, whether Full, Compact, Metadata, Partial, Selective, etc." I.e., there is exactly one Issuer commitment (via the composed Schema and the "most compact form" SAID algorithm, §130-151), and every disclosed variant is checked against that one commitment — arcviz does not need to track "which variant was signed" as a separate fact per disclosure.

---

## 6. Blinding and the `u` salt — summary (detail already threaded through §1–§5 above)

The mechanism is uniform across every level (top-level ACDC, Attribute block, nested Attribute sub-blocks, Aggregate-array elements, Edge blocks, Edge-groups, Rule blocks, Rule-groups, and TEL blinded-attribute blocks): a field map with a `d` (SAID) MAY also carry a `u` (unique entropy/salty nonce, "approximately 128 bits of entropy," recurring; **renamed from "UUID" on `v1.1`** — see §1 above). Presence of `u` converts the SAID from a mere compactness/dedup mechanism into a genuine privacy-preserving blind: `toip/v1.1:spec/spec-body.md:100-102` (quoted above) is the canonical statement, restated near-verbatim at every level that reserves a `u` field.

**What an observer can infer, precisely:**
- The block's **shape** (its Schema/subschema), always — Schema is never itself hidden by `u`.
- **Set membership**: given a disclosed SAID and, separately, a full list of SAIDs (e.g. the Aggregate array, or a bulk-issuance/Merkle set), an observer can check whether a given digest is *in* that list, without learning the undisclosed members' content (`toip/v1.1:spec/spec-body.md:743`, `755-761`).
- **Nothing about content** from `d` + Schema alone, when `u` carries sufficient entropy — this is the rainbow-table-resistance property repeated at every level.
- **Once `u` (and the content) is disclosed**, full verifiability: recompute `d` from disclosed content+`u`, compare to the previously-committed compact-form value.

**Registry-level blinding is a distinct, related mechanism** (`toip/v1.1:spec/spec-body.md:2244-2344`, TEL Blinded Attribute Block): the transaction state itself (`ts`, `td`) can be hidden behind a BLID (a SAID-like digest over fixed-order concatenated fields, not a labeled field map digest — `toip/v1.1:spec/spec-body.md:2267`), unblindable only by whoever holds the same derivation salt and sequence-number path as the Issuer: "Only the Issuer and Discloser have a copy of the secret salt, so only they can independently derive the current blind from the sequence number" (`toip/v1.1:spec/spec-body.md:2334`). This is orthogonal to but composable with ACDC-level `u` blinding.

**New in this section on `v1.1`: field-label restrictions apply here too.** A path into a blinded block, per §9 below, closes over "the simple fields of a block [that] share one SAID and one UUID" (`toip/v1.1:spec/spec-body.md:1869`) — i.e. the Disclosure Paths construct's closure rules formalize, for the first time, exactly which fields a given `u`-bearing block's blinding covers when a path names it. See §9. **Incidental finding**: that quote's "UUID" is verbatim from the spec — the Disclosure Paths section (`toip/v1.1:spec/spec-body.md:1869`, `1871`, `1923`) is the only place in `v1.1` where "UUID" still appears; it was merged separately from the UE rename sweep and was never reconciled with it. Three leftover "UUID"s, not a claim this document relies on.

---

## 7. The dossier specification — joint issuance, threshold operators, revocation over ACDCs

Quoted from `trustoverip/kswg-dossier-specification@main` (`b9227753...`, re-verified unchanged 2026-09-11) — see "Sources read" for why upstream `main` and not the vendored checkout. No claim in this section changed in this rebase.

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

Quoted from `spec/spec-body.md` in `~/code/me/kswg-cesr-specification` (identical to upstream `main` for these sections — see Sources read). Locators below are unchanged from the prior revision — the CESR spec did not change on either branch. No claim in this section changed in this rebase.

- **Version String format** (`spec/spec-body.md:1174-1195`), 2.XX: `PPPPMmmGggKKKKBBBB.` — 19 characters, five parts: 4-char protocol (`ACDC`/`KERI`), 3-char major.minor protocol version (base64-numeric), 3-char CESR genus major.minor version, 4-char serialization kind (`JSON`/`CBOR`/`MGPK`/`CESR`), 4-char base64 total-length, `.` terminator. This is what a JSON/CBOR/MGPK-serialized ACDC's `v` field literally contains and what a renderer parses to determine size and kind before deserializing. A legacy 1.XX 17-character format (`PPPPvvKKKKllllll_`) MUST still be supported for old messages (line 1199-1217).
- **CESR-native messages carry no `v` string with size/kind** — that information is instead in the enclosing CESR count/group code (`-G##`/`--G#####`), and only a protocol+version placeholder is injected into any in-memory `v` field for reserialization bookkeeping (`spec/spec-body.md:1191`). A renderer consuming CESR-native input therefore gets sizing from the framing code, not from a regex-parsable `v` string.
- **SAID mechanics** (`spec/spec-body.md:1219-1233`): "SAIDs MUST be encoded as a CESR Primitive," i.e. a derivation-code-prefixed Base64 string, so a renderer sees the algorithm identifier baked into every SAID it displays (no separate "hash algorithm" field to look up).

**Presentation, display, or rendering — confirmed absent.** A full-text grep of `spec/spec-body.md` in all three vendored repos (ACDC, CESR; dossier not applicable — it discusses "human-readable" `l`/`purpose`/`ref` fields only in passing prose, not a rendering mechanism) for `presentation|display|render|visuali[sz]e|user interface|\bUI\b` turns up no rendering, display, or UI guidance of any kind in ACDC or CESR. The only hits are (a) prose uses of "presentation/present" in the credential-exchange sense (IPEX disclosure, not visual presentation), and (b) two incidental string matches: a URL fragment containing the substring "display" (a wiki link, ACDC bibliography) and the English word "render" used in its ordinary sense ("may render... an exercise in diminishing returns," ACDC Annex). **This is a confirmed nothing**, consistent with `docs/research/PLAN.md`'s framing that rendering authority is an open design question deferred to a later phase, not something the base specifications answer.

---

## 9. Disclosure Paths (`dp`) — new, normative construct, `v1.1` only

**Absent from `main` entirely** (0 occurrences of `dp` on `toip/main`); on `v1.1` it is a full normative section of 185 new lines, merged as PR #203 (2026-08-12 per the branch name `dp-disclosure-paths-1549`), with 16 occurrences of `` `dp` `` and four section headings containing "Disclosure Paths": `toip/v1.1:spec/spec-body.md:1809` (`## Disclosure Paths`), `:1879` (`### Disclosure Paths, `dp`, Field`), `:1941` (`### Disclosure Paths Example`), `:2013` (`#### Disclosure Paths in `apply` and `offer``). This closes the gap the task brief calls out and corrects the prior revision's SPC-F4-adjacent framing (see [reviews/2026-09-06-operator-semantics-adjudication.md](../../reviews/2026-09-06-operator-semantics-adjudication.md), 2026-09-10 correction): `dp` is not an unmerged keripy-discussion proposal, it is specified.

**What it is, in one sentence**: `dp` is a field in the *messages that negotiate a disclosure* (not in the ACDC itself — `toip/v1.1:spec/spec-body.md:1811`, "The `dp` field is not an ACDC field... It is therefore not reserved as an ACDC field label"), carrying a list of tuples that together specify exactly which parts of a DAG of chained ACDCs are to be disclosed.

### The DAG the paths address

An issuance or presentation exchange discloses a single DAG with exactly one source node, the **origin node** — the ACDC being disclosed, or, when several unchained ACDCs must travel together, a purpose-built **bespoke ACDC** whose Edges chain to all of them (`toip/v1.1:spec/spec-body.md:1817-1821`). The DAG is walked in **breadth-first order** from the origin, chosen (over depth-first) because in dossier joint issuance the jointly-issued ACDCs "fall together in breadth-first order and scatter in depth-first" (`toip/v1.1:spec/spec-body.md:1833`).

### Path syntax

A path is a tuple of components — field labels, or (for arrays) zero-based integer offsets — joined by the path delimiter `/`, or by `-` in the CESR-compact form (this is exactly the `-` that Field Label Restrictions, §1 above, reserves out of field labels: `toip/v1.1:spec/spec-body.md:1837`). A path beginning with `/` is **DAG-absolute**, rooted at the origin ACDC's top level; one that does not is **ACDC-relative**, rooted at its own ACDC's top level (`toip/v1.1:spec/spec-body.md:1839-1841`).

**Traversing an Edge** requires DAG-absolute form and the virtual `_` hop component (§1 above): a path such as `/e/reports/project/_/a/author` descends the origin's Edge Section to Edge-group `reports`, its Edge `project`, hops (`_`) to the far-side ACDC, then descends that ACDC's Attribute Section to `author` (`toip/v1.1:spec/spec-body.md:1845-1849`).

**Node paths vs. leaf paths** (`toip/v1.1:spec/spec-body.md:1855-1861`): a path ending in the delimiter (or an empty final component) is a **node path**, designating a whole field map/array and everything beneath it — "the node form is a hammer." A path ending in a real label or index is a **leaf path**, designating one value plus only what's needed to validate the SAIDs on its branch — "the leaf form a scalpel." A top-level `d/` is a node path for the entire ACDC.

**Closures** (`toip/v1.1:spec/spec-body.md:1865-1877`): what a path discloses. In a **partially disclosable** section (Attribute, Edge, or Rule), a leaf path closes over every simple field sharing that block's one SAID+UE (nested sub-blocks stay compacted). In the **selectively disclosable** Aggregate Section, a leaf path to one blinded block closes over that block alone — no sibling. The Schema Section is always disclosed, so no path ever needs to name it.

### The `dp` field itself

`toip/v1.1:spec/spec-body.md:1881`: "The value of the Disclosure Paths, `dp`, field is a list of tuples... of the form `(ACDCSchemaSAID, PathPrefix, [paths])`." Serialized as a three-element JSON array where JSON has no distinct tuple type. A Schema SAID MAY repeat across tuples — two ACDCs of the same type (same Schema) can both appear in one DAG, which a field-map-keyed-by-SAID design could not distinguish (`toip/v1.1:spec/spec-body.md:1883`).

**Path Prefix** (`toip/v1.1:spec/spec-body.md:1885-1897`): the DAG-absolute route shared by every path in that tuple's list, so the individual paths need not repeat it. Empty for the origin (whose paths are then ACDC-relative); for any other ACDC, ends in the `_` hop (e.g. `/e/accreditation/_/`). Concatenation of prefix + entry is always well-formed because a prefix is either empty or delimiter-terminated and an entry never begins with the delimiter. Where the prefix is non-empty, an empty entry `""` designates the whole ACDC (the prefix, ending in `/`, is itself the node path); where the prefix is empty, an empty entry designates nothing, and the shortest whole-ACDC path is `d/`.

**Identifying each tuple's ACDC** (`toip/v1.1:spec/spec-body.md:1901-1913`): elements MUST appear in breadth-first order; the **zeroth element MUST be the origin node**, identified by its Schema SAID. Where every prefix is non-empty, the list MAY omit ACDCs with nothing requested. Where a Schema makes an Edge (or an Edge-group) optional, position alone can't disambiguate a possibly-absent node, so **every element after the zeroth MUST carry a non-empty prefix** in that case.

**Solicited Response** (`toip/v1.1:spec/spec-body.md:1917`): an empty `dp` list, `[]`, answering a prior message that also carried one, means "the same disclosure as before." An unsolicited message, or one proposing a different disclosure, MUST NOT send an empty list.

### Special cases

- **Aggregate Section Pathing** (`toip/v1.1:spec/spec-body.md:1921-1931`): a blinded attribute block MAY be named by its uniquely-labeled field instead of its array offset, e.g. `A/over21` for the block at offset 1 is shorthand for `A/1/over21` (unambiguous since a field label MUST NOT begin with a numeral). The shorthand cannot reach nested sub-blocks inside that element — a path like `A/over21/issued` MUST be rejected; use the explicit offset (`A/1/over21/issued`) instead. The AGID at array offset 0 is addressable directly as `A/0`.
- **Simple Compact Edge** (`toip/v1.1:spec/spec-body.md:1933-1935`): pathed the same as any other Edge (label then `_`), even though its value is the far-node SAID directly rather than an Edge-block SAID.
- **Private Edge** (`toip/v1.1:spec/spec-body.md:1937-1939`): may require two-step negotiation, since the Edge (or its enclosing Edge-group) Schema SAID needed to build the path may itself be blinded until an earlier exchange step discloses it.

### Worked example (from the spec, `toip/v1.1:spec/spec-body.md:1941-1994`)

A four-ACDC DAG (transcript → accreditation, and → a `reports` Edge-group with `research` and `project` Edges) requesting the Issuer, Issuee/author, and full Rule Section from each ACDC. ACDC-relative form (empty prefixes):

```json
[
  ["EMm9Gn9Qq9gkRQduJx9Vjtj3b3l1cVpe4Sv18EdAVRtb", "", ["i", "a/i", "r/"]],
  ["EOlgQaGgXI6Zqikg4I0KWaQeL9sRUGu7PUj78GekKnSf", "", ["i", "a/i", "r/"]],
  ["EOumGkAf8Y28g9xBWmVJAisgkolBPaJ64nPlf8McWgvg", "", ["i", "a/author", "r/"]],
  ["EOumGkAf8Y28g9xBWmVJAisgkolBPaJ64nPlf8McWgvg", "", ["i", "a/author", "r/"]]
]
```

The last two elements share a Schema SAID (research report and project report ACDCs) — "the case that a field map keyed by Schema SAID could not express." The DAG-absolute equivalent factors the route into each tuple's prefix instead:

```json
[
  ["EMm9Gn9Qq9gkRQduJx9Vjtj3b3l1cVpe4Sv18EdAVRtb", "/", ["i", "a/i", "r/"]],
  ["EOlgQaGgXI6Zqikg4I0KWaQeL9sRUGu7PUj78GekKnSf", "/e/accreditation/_/", ["i", "a/i", "r/"]],
  ["EOumGkAf8Y28g9xBWmVJAisgkolBPaJ64nPlf8McWgvg", "/e/reports/research/_/", ["i", "a/author", "r/"]],
  ["EOumGkAf8Y28g9xBWmVJAisgkolBPaJ64nPlf8McWgvg", "/e/reports/project/_/", ["i", "a/author", "r/"]]
]
```

### Binding into IPEX

`toip/v1.1:spec/spec-body.md:2004,2006`, the `apply`/`offer` message-content table: `dp` **replaces** the old informal "Attribute field label list, Aggregate element label list" columns entirely (present in both `apply` and `offer` rows on `main`, absent on `v1.1`). `toip/v1.1:spec/spec-body.md:2013-2019`: `dp` MUST appear in the query section, `q`, not the attribute section, `a`, of an `apply`/`offer` exn message, since "a request to disclose... is a query." Solicited-response emptiness (above) applies directly to an `offer` answering an `apply`.

**Direct relevance to arcviz**: `dp` is the first normative machinery for saying, machine-readably, exactly which parts of a partially-disclosed DAG a given exchange covers — precisely the boundary arcviz's rendering must track between *disclosed*, *undisclosed*, and *structurally absent*. A later rendering phase should treat a `dp` value (or its resulting closure) as the authoritative source for which nodes/fields a given view is entitled to show as disclosed versus blinded, rather than inferring it from which fields happen to be present in a partially-expanded ACDC.

---

## Open questions and spec ambiguities

1. **`E1E` and `dp` are now resolved as normative on `v1.1` — removed as open questions.** The prior revision's items 1 (E1E as an unmerged proposal) and the SPC-F4-adjacent framing of `dp` as unresolved are superseded; see §3 and §9 above and "Corrections from the 2026-09-05 revision" below. This is not a new open question, it is the closure of two old ones — listed here only so a reader diffing this section against the prior revision can see why they're gone.
2. **`main` carries worked-examples content that neither the old vendored checkout nor `v1.1` has — this is now confirmed as a genuine, unrelated branch divergence, not a staleness gap.** `main` has a "Registry-Dependent Issuance Lifecycle" walkthrough and additional "Graduated Disclosure" worked examples (`toip/main:spec/spec-body.md:4849-5103`, ~255 lines) that `v1.1` lacks entirely — confirmed by diffing `toip/main` against `toip/v1.1` directly (not against the vendored checkout, which also lacks this content, matching `v1.1` on this point). Per AGENTS.md rule 5, `v1.1` is authoritative for content, so this document does not draw on that worked-example prose. None of it changed any field/operator/disclosure-variant semantics found elsewhere in this inventory. If a later phase needs the TEL lifecycle walkthrough specifically, it exists only on `main`, and using it should be flagged as drawing from the tooling-only branch rather than the content-authoritative one.
3. **Vendored dossier checkout is stale on a substantive point** (anchoring vs. signing terminology) — already corrected above by citing `main` instead, but this means **whoever next updates the vendored `kswg-dossier-specification` checkout should be told it is behind `main` by a meaningful semantic revision**, not just a wording pass. This is a fact about repo state, not about the spec's content, but it's exactly the kind of thing EVIDENCE.md's rule 6 worked example warns about: I did not take the vendored copy on faith, but a future reader might. Re-verified 2026-09-11: still true, unchanged since the prior revision.
4. **Provenance-chain validity propagation is EGF-dependent, not normatively fixed.** `toip/v1.1:spec/spec-body.md:1123-1127` repeatedly defers "the actual logic for interpreting the validity of a set of chained or treed ACDCs" to the ecosystem governance framework, using modal "MAY" language ("an Edge pointing to that node MAY also be invalid"). Arcviz cannot derive a universal "if child invalid then parent invalid" rule from the base ACDC spec alone — this is confirmed underspecified, not an oversight in this inventory. Any such rule arcviz encodes would be arcviz's own design choice (per `PLAN.md`'s "arcviz may make disclosure-side rules, flagged as new" principle), not inherited doctrine. Unaffected by the `v1.1` rebase.
5. **`A` field's non-standard-digest compaction is explicitly non-uniform with the rest of the "most compact form" algorithm.** `toip/v1.1:spec/spec-body.md:166` calls this out directly ("an Aggregate section uses its own algorithm for compact and un-compact (expanded) forms") but does not fully spell out how an AGID composes when an ACDC containing `A` is itself referenced by an Edge's `n` field pointing at its "most compact form" SAID — i.e., I could not find, in the sections read, an explicit statement of whether the top-level `d` of an ACDC that uses `A` is computed with the AGID substituted in the same depth-first "most compact form" walk described for `s`/`a`/`e`/`r`, or via some different rule. The prose that *would* resolve this (line 166) gestures at "its own algorithm" without giving the algorithm inline at that point. Flagged rather than inferred; a future phase reading the Aggregate section's composed-schema JSON (`toip/v1.1:spec/spec-body.md:770-913`) more mechanically, or checking a keripy reference implementation, should confirm this before arcviz's rendering logic depends on it. Unaffected by the `v1.1` rebase.
6. **Rendering/display: confirmed absent, but only within these three specs.** I did not check the KERI base specification (`kswg-keri-specification`), which was outside this task's assigned scope (ACDC + dossier + CESR only). If a later phase needs to rule out KERI-level display guidance too, that is a separate, not-yet-done check. Unaffected by the `v1.1` rebase.
7. **New from this rebase: the `dp` field's interaction with operator-based validity is not spelled out.** §9's closure rules state what a path *discloses*; they say nothing about how a Disclosee should treat an edge whose operator (§3) governs a node that a `dp` value's closure excludes from disclosure — e.g. an `E1E`-governed edge to an undisclosed far node. Nothing in `v1.1` addresses this combination directly; it is a genuine gap at the intersection of two `v1.1`-only constructs, not resolved by inference here.
8. **New from this rebase: two leftover terminology inconsistencies on `v1.1` itself**, both incidental and neither relied upon by any claim above — see the notes under "The `u` field" (§1) and "Blinding and the `u` salt" (§6): the Disclosure Paths section still says "UUID" in three places (`toip/v1.1:spec/spec-body.md:1869`, `1871`, `1923`), and `toip/v1.1:spec/spec-body.md:2956` still has the pre-existing "UUDI" typo, both missed by the UE rename sweep because they were introduced or left untouched by different, unreconciled merges.
