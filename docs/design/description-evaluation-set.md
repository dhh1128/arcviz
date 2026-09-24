# The evaluation set for credential descriptions

**Status.** The goal in §1 and the scope principle in §2 are Daniel Hardman's, settled 2026-09-23, and are quoted rather than paraphrased. Everything else — the choice of bundles, the claim that each stresses a different discriminator, and every assessment of a channel — is synthesized. It is recorded so a later session does not re-derive it, not so a later session can cite it as decided.

## 1 · What a description is for

*Let the viewer say what part this credential plays in the argument the DAG is making.*

Not what kind of thing it is in the abstract: the nine categories of [credential-categories.md](credential-categories.md) answer that, and are to be carried by colour and a watermark. Not which one it is: the credential's SAID answers that, as a reference handle. What work it does **here**. The test is whether removing the node would let a viewer say what the argument lost.

This follows point 5 of [posture.md](posture.md), whose second half — *"how are these pieces of evidence related?"* — has been read as a question about edges when it is equally a question about what each node contributes.

A competing goal was considered and rejected: that the description exists to let the viewer decide whether to **trust** the credential, which would make it evidentiary rather than narrative. Posture point 4 says arcviz is about helping users understand more than proving something, and the 2026-09-19 amendment makes orientation primary, so evaluation is second-order by Daniel's own ordering.

## 2 · Why the evaluation unit is a bundle, not a credential

In his words: *"I can't just look at one acdc and say, what should be its description? I have to look at that acdc as part of a larger corpus of evidence and say, what is it about this credential, in a larger corpus, that would help a person make sense of its intended role in the corpus at first glance?"*

Three consequences, all synthesized.

The description is a function of (credential, DAG), so it cannot be precomputed, cached, or stored on the credential. It is a render-time computation over the whole presentation, and the same credential legitimately reads differently in two bundles. The operation is therefore **contrastive** — show what distinguishes this node from its neighbours in *this* corpus — which promotes discrimination from an occasional bonus to the mechanism. And a rule already written down changes: `credential-categories.md` says that when a rendering can show only one category, `identity` yields, being the substrate of nearly everything. Under DAG scope that is a special case of *show what varies, suppress what is constant*, and in a bundle where the licences are the only `identity` credentials among photographs and statements, `identity` is the most informative thing present and must not yield. A hardcoded precedence becomes a computed one. That doc lists the substrate rule as synthesized, so this does not disturb the nine settled categories.

The cost, which is real: a contrastive description is unstable across renders. That argues for the stable channels — category colour, watermark, the SAID handle — carrying the anchor while only the description text moves.

## 3 · Why an evaluation set is needed at all

Measured 2026-09-23. The 29 ACDCs then in `corpus/` formed 18 connected components, of which only four had more than one node: `diamond_depth` (5), the vLEI chain (4), the household (3) and `working_edge_group` (3). Fourteen were isolated singles. None was a heterogeneous bundle of evidence.

That was not a corpus defect. `corpus/README.md` records that each fixture names the disclosure-matrix cell it exercises; the corpus was built for mechanisms H1–H9 and the blinding rules, and it does that job. But it means any claim about descriptions was being tested against four DAGs, none of which resembled the case that motivated the question.

## 4 · The eight bundles

Chosen because each stresses a **different discriminator**, not a different domain. Six come from the use-case section of the dossier specification (`~/code/me/kswg-dossier-specification/spec/dossier-spec-body.md`, "Use Cases and Architectural Patterns"); two do not.

| # | Bundle | Pattern | The discriminator it forces | Status |
|---|---|---|---|---|
| 1 | Insurance accident report | — | Heterogeneous **subject kinds** in one bundle | **Built** — `corpus/accident_*` |
| 2 | Verifiable Voice Protocol | Compositional | **Issuer** — trust derives from which independent authority vouched | **Real data** — see §5 |
| 3 | Law enforcement / adjudication | Procedural | **State** — Marked, Offered, Admitted, Stricken | Not built |
| 4 | Investigative journalism | Redacted | **Nothing, by design** — a blinded precursor edge | Not built |
| 5 | Mortgage qualification | Snapshot | **Time** plus observer | Not built |
| 6 | Clinical trials | Predicate | **What was proven**, the evidence revealing nothing | Not built |
| 7 | Petition | Open-endorsement | **Endorser**, across N otherwise identical nodes | Not built |
| 8 | Same-schema household | — | **Issuee** — the minimal case | Already in corpus |

### 1 · The accident report — heterogeneous subjects

Daniel's own worked example: an adjuster's claim file over photographs of the vehicles, driving licences of the drivers, and witness statements. Built as three matched pairs, each colliding on schema — and therefore on category, colour and badge — and each separated by a different channel, so that a proposal resting on any single channel fails at least one pair visibly.

The licences differ only in **issuee**. The statements share an issuee, both being addressed to the insurer, and differ only in **issuer**. The photographs are identical on schema, issuer *and* issuee, the last because neither has one, so **nothing structural separates them**: the only discriminator is an issuer-chosen attribute that nothing in the credential marks as the subject rather than as an incidental field. That third pair is the hardest case the set contains, and it is not contrived — two photographs of one accident attested by one adjuster is what an adjuster's file holds.

It also carries all three image states (§6) and an issuance date on every node (§7).

### 3 · Procedural — state as the discriminator

The spec's law-enforcement pattern manages evidence from field collection through adjudication, where an artifact may be `Marked`, `Offered`, `Admitted` or `Stricken`, applied by annotation edges from a later dossier version rather than by altering the original.

`Stricken` is the absent-versus-fine problem in its purest available form, and it is why this bundle is the most valuable one not yet built. A struck exhibit is *present*, *preserved for appeal*, and *excluded from the effective body of facts* — three states that a naive render collapses into one, and the collapse is in the direction that misleads. [AGENTS.md](../../AGENTS.md) states the project's thesis as never letting *absent*, *undisclosed*, *redacted* and *unverified* be mistaken for one another or for *fine*; this pattern adds *excluded but retained* to that list.

### 4 · Redacted — designed indiscriminability

A public artifact linked to a private precursor by a blinded edge. The node is *meant* to offer nothing about its source. The handoff note that opened this question listed as an open problem that "a node reached across a blinded edge may offer nothing discriminating at all"; this pattern is that case with an intended answer, so the description must say *derived from something withheld* rather than fail silently.

### 5 · Snapshot — time as the discriminator

Observation attestations: an oracle signs "I observed account X at balance Y at time Z". Two snapshots of one account differ in nothing but the timestamp, and the whole point of the pattern is that the timestamp is the content.

### 6 · Predicate — the evidence reveals nothing

A zero-knowledge predicate edge: the dossier asserts `inclusion_criteria_met: true` and the evidence behind it discloses no underlying data. The discriminator can only be *what was proven*, which is a property of the predicate rather than of any party or subject. This is the one bundle in the set where no channel in §7 applies at all.

### 7 · Petition — scale

N endorsements of identical schema, identical category and identical role, differing only in endorser: `same_schema_alice`/`same_schema_bob` at scale. **At N = 500, per-node description is the wrong answer entirely**, and the honest rendering describes a population rather than its members. Nothing in the design so far can express that, and it is a consequence of the DAG-scope principle that the accident bundle would never have surfaced.

## 5 · The one bundle that is real

The live VVP dossier at `https://eu-west.provenant.net/v1/agent/public/EB2jhY5laLc4rcWCEWLzT69mxEIfXJZ3kNzWfKx2vHpP/dossier.cesr` is 167 KB, 175 KERI messages, five distinct ACDCs, and the only non-synthetic presentation this project has examined. It is worth more than its size suggests, because it independently confirmed three things that had been inferred from synthetic fixtures and corrected a fourth.

Confirmed: the root is untargeted, carries no attribute but a timestamp, and its entire content is four edge labels (`vetting`, `alloc`, `tnalloc`, `delsig`) — a presented root is the claim rather than a part of it. Two of its children share one schema and are separated only by an issuer-supplied `a.role` string reading "TN Allocator" against "Delegated Voice Call Signer" — schema, and therefore category, does not discriminate. Its parties form a delegation ladder in which one AID is issuee twice and issuer twice, and none of it is drawn today.

Corrected: its `tnalloc` credential has an issuee **and** a subject that is a thing. `a.numbers` is a telephone-number range; the issuee is the party *granted* that range. So the subject and the issuee are independent — they coincide for identity- and qualification-shaped credentials and diverge for authority-shaped ones — and describing that node as "about EIgFVo" would be actively misleading. `credential-categories.md`'s `alignment` axis is the existing machinery for that switch.

## 6 · Channels, graded

No single channel survives all eight bundles. Grades are by **provenance**, which matters because [principles.md](../research/principles.md) P12 requires the proved-versus-guessed distinction to be visible in the UI rather than merely present in the data.

**Issuer AID.** Present on all 29 corpus ACDCs and all five in the real dossier, and where man-in-the-middle risk lives. Universal, and blind at exactly the collision that started this question — the only two corpus fixtures sharing an issuer are `same_schema_alice` and `same_schema_bob`.

**Issuee AID.** Structural, machine-identifiable, no interpretation required. Present on 9 of 29 corpus ACDCs — which is not a coverage gap but a measurement of how often the subject is not a party.

**Issuance date (`a.dt`).** Present on 5 of 5 ACDCs in the real dossier and originally 4 of 36 fixtures, a gap this document's bundle closed. Bound into the SAID, so unalterable after issuance without detection. It does more than discriminate: in the real dossier two credentials are dated 2025-12-19 and three are dated 2026-03-11 within 57 seconds of each other, which separates pre-existing background from material assembled *for* this claim and exposes the assembly order. Under §1's goal that is the question answered directly rather than a proxy for it. **The strongest text channel in the set.**

**Thumbnail.** A credential commits to an image by digest, so the render can prove *this credential commits to exactly these bytes* and cannot prove the bytes depict what they purport to. Stronger than the text claim it replaces, because the binding is cryptographic where a text claim's is nothing; weaker than it *looks*, because a photograph reads as self-evident. Korir's finding that users read an identifier's form as itself the security mechanism is the same failure at higher gain. A thumbnail is not a description — it is evidence rendered directly, so it does not compete for the label slot but changes what the label must say: **the image carries the subject, the text is freed to carry the provenance.** Three states must render distinctly (§7), it must be governed by what was *disclosed* rather than by what is resolvable — a presentation proving age without identity is defeated by a renderer that helpfully resolves the portrait — and fetching the bytes is a network act and therefore a correlation vector.

**Suggested filename.** `expenses.xls` against `application.pdf`. Uniquely valuable because it is the only field in the whole stack authored by a human, in prose, for another human to read; every other channel was written for machines and is being repurposed. Weakest evidentially: pure issuer claim, and it carries an implicit type assertion in its extension that need not match the bytes. Render as untrusted input — extension from sniffed content rather than from the string, and bidirectional control characters stripped, since `report‮fdp.exe` displays as `report exe.pdf`.

**Attachment size.** Discriminates without informing, which is the SAID's defect in a worse form since it is neither unique nor meaningful, and it moves under recompression. A last-resort tiebreaker only, rendered as a human magnitude rather than a byte count, because precision implies a meaning it does not have.

**Referring edge label.** Present for 11 of 29 corpus ACDCs, and structurally impossible for the presented root of any DAG. It is the one naming channel not supplied by the named credential's own issuer — it is the referrer's claim. It carries **role and not instance**: the accident bundle's labels degenerate to `licenceA`/`licenceB`, and the real dossier's `vetting`/`alloc`/`tnalloc`/`delsig` would collide the moment there were two allocations. Supplementary, never primary.

**Credential SAID.** A poor name and an ideal handle. It discriminates perfectly and therefore informs nothing, which is the wrong property for a description and exactly the right one for a reference token — globally stable across renders, sessions and people. Daniel settled 2026-09-23 that this is what `ITEM 03` was doing, so the number is deleted rather than demoted. One distinction travels with that: displaying an identifier as a reference token is not the same act as wrapping it in a recognition-and-comparison ceremony. The SAID keeps the display and loses the ceremony; the AIDs get the ceremony.

## 7 · The states that must not collapse

Wherever a channel can be absent, the reason for its absence is itself information, and this project's thesis is that the reasons must not be interchangeable.

For an image: **no image committed**, **committed and resolved**, and **committed and not resolved**. The third must never look like the first. All three are now testable — `accident_photo_a`, `accident_photo_b` and `accident_licence_a` commit to digests computed over bytes in `corpus/attachments/`; `accident_licence_b` commits to a portrait whose bytes are generated and deliberately discarded, so two licences side by side show one face and one grey box; the statements and the claim file commit to no image at all.

For a party: **untargeted by design** (the dossier root, the scene photographs) against **targeted but undisclosed**. For a category: **`unknown`** against **`ordinary`**, which `credential-categories.md` names as the highest-stakes rendering question the scheme raises. For an exhibit in a procedural bundle: **struck** against **never offered**.

## 8 · What is not decided here

Whether the eight are the right eight. How a description is composed once its channels are chosen. What a population summary looks like for the petition case. Whether the `identity`-yields correction in §2 is accepted. And the open problem behind all of it: an issuer AID may resolve to no alias, and Korir argues against showing the raw high-entropy string, so a party-anchored description has no fallback when the alias is missing.
