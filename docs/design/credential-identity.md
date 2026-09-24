# How a credential is identified — the open question, and what is already known

Opened 2026-09-18, by Daniel Hardman, after looking at the responsive arm B rebuild: the entviz pill is on the wrong identifiers, and labelling credentials `ITEM 03` is useless. This file is the brief for the session studying it. It records what is measured, what the research already decided, and what is genuinely open — so that session starts from evidence rather than re-deriving.

## 1 · What the artifacts actually show, measured

Every mock in this repository, including the rebuilt responsive one, renders **thirteen SAID pills and one AID**. The AID appears only inside the expanded card, only for the focused item — one of thirteen objects, and only on demand.

| identifier class | present in the corpus | rendered |
|---|---|---|
| `d` — the credential's SAID | all 13 objects | **all 13, at every tier** |
| `i` — the issuer AID | **every fixture** | 1, inside the focused card only |
| `a.i` — the issuee AID | all three vLEI fixtures | **none** |
| the presenting party's AID | named by the gate header | **none** |
| `ri` — registry identifier | where present | none |

The gate's own header reads "no evidence binds the presenting party to any holder AID below" — it names the presenter AID as the thing at stake and then shows no AID at all.

The issuer AIDs also carry the chain's party structure, and it is invisible. In the vLEI fixtures `vlei_le`'s issuer is `vlei_qvi`'s *issuee* — the delegation step — so "who issued this, and is that the same party who issued that one" is answerable from the corpus and unanswerable from the render. The render draws which credential references which, and hides who stands behind any of it.

## 2 · Why the pill belongs on AIDs — the reasoning, not the likelihood

Daniel's framing was that AIDs carry MITM risk and SAIDs are "far less likely to be attacked." The conclusion holds, and the reason is stronger than likelihood: **it is about what a human comparison can settle.**

- A **SAID is content-derived.** Hold the content and the machine recomputes and compares it exactly; a human glance adds nothing to a bit-exact computation. Don't hold the content — an edge's `n`, a compact block — and a human glance cannot settle it either, because there is nothing to compare against; its integrity rides on the containing credential's signature chain instead. Either way, no question a human eye answers.
- An **AID is not derived from anything you hold.** "Is this the party I think it is?" is not computable. It is anchored out-of-band, in a KEL obtained through some channel, and that channel is where a man in the middle stands. That is precisely the question a comparison ceremony exists to answer.

So entviz's whole apparatus — recognition, then expand, then a formal comparison — is answering a question that only AIDs ask. Putting it on SAIDs spends the ceremony where no ceremony is needed, and leaves it absent where it is the only defence.

**Two qualifications, so the rule is not over-applied.**

- The **schema SAID** is the one SAID whose substitution has real teeth: Rule 8 derives its gravest distinction from the schema, and a substituted schema that reserves a `u` makes arcviz assert H3's protection on an H2 unit. But the defence is SAID-verified resolution (stock keripy's `CacheResolver.add` refuses a mismatched SAID), which is computational. Still not a human-comparison job.
- There is a **recognition** case for SAID pills — "have I seen this exact credential before?" — but that is entviz's *corpus* posture, for a closed single-origin body of values the user already trusts. arcviz is wild by its own gate header. It does not apply here.

Neither qualification changes the conclusion; both bound it.

## 3 · The research already decided this, and the mocks never implemented it

This is the uncomfortable part, and it is the answer to "how could we get the affordances so wrong when the research is supposed to include UX work."

**The research is right.** [affordances.md](../research/affordances.md) §5 already states the treatment: *"Ugly fields render as entviz pills, **labelled with a COIA alias where one resolves**"* — verdict *sound with constraints*. The same entry already draws the class distinction Daniel is raising: *"An AGID never gets a SAID pill (Rule 7 — it is a different commitment object)."* And [principles.md](../research/principles.md) P12 governs the label: an alias is a private nickname, not evidence; the proved-versus-guessed distinction is visible in the UI, not merely present in the data; flags are never dropped; an unflagged alias is never treated as verified. P12 also carries the Korir finding that participants read a DID's random-string *form* as itself the security mechanism — which is an argument against showing raw identifier strings to users at all.

So the specified design is: **a pill, labelled with a resolved alias, carrying its provenance flags visibly.** Not a number. *(Revised 2026-09-24, D-DCTS: the flags are made visible by showing the alias verbatim as the host's interface returns it, not by arcviz parsing them into a separate channel. See [credential-descriptors.md](credential-descriptors.md) §1.)*

**`ITEM 03` is exhibit hygiene that escaped into the design.** It exists for a legitimate reason: the annotation discipline forbids naming a fixture inside a render, so ground truth cannot leak into an exhibit that is supposed to be read blind. The stress board kept it as a small corner tag and was honest about what it was. On 2026-09-17 it was promoted into the entviz pill's **label slot** — the single most human-facing position in the design, and the slot the research had reserved for the alias. A test-harness placeholder ended up occupying the identity affordance.

**The structural hazard worth naming.** The annotation discipline creates a vacuum exactly where the credential's human identity belongs, and nothing marks the vacuum as a vacuum. Every mock therefore looks complete while omitting the thing a real viewer most needs — and it has looked complete to reviewers for the whole life of the project. Any future exhibit convention that suppresses real content should have to render a visible placeholder that says what is being suppressed and why.

## 4 · What is genuinely open

1. **What identifies a credential to a human.** The alias is specified for *parties*; a credential is not obviously the same problem. Candidates in the material already: the schema title (issuer content, P11-untrusted), the issuer's alias plus a type, the `a` section's own content. None has been worked.
2. **Which identifier classes get a pill, and which get something else.** Rule 7 already says an AGID does not get a SAID pill. The full mapping — issuer AID, issuee AID, presenter AID, credential SAID, schema SAID, registry `ri` — has never been written down.
3. **Where the issuer AID goes at the floor.** It is the identifier that matters most and there is no room for it at 76×44 beside anything else; this collides directly with the floor-form work in [layout-comparison/RESPONSIVE.md](layout-comparison/RESPONSIVE.md) §11.
4. **Whether showing raw high-entropy strings to users is ever right**, given Korir. The pill's answer is "no, show a type and a name, keep the value one gesture away" — which arcviz has not adopted anywhere outside the pill itself.
5. **The presenter AID.** The gate names it and shows nothing; this also touches the open holder-facing presenter-indicator question in [decisions.md](decisions.md).

## 5 · What not to redo

The responsive rebuild's packing, connector routing, conformance and glyph work is independent of this question and stands. What is void is every mock's *identity* treatment, at every tier. Do not treat the `ITEM NN` labels as a convention to preserve — they are a test harness, and this file exists partly because they were mistaken for a design once already.
