# Credential categories

**Status: the nine categories below are Daniel Hardman's, settled 2026-09-23. Everything else in this document is synthesized — a session's reasoning, offered as the record of how the nine were arrived at, not as anything he has ratified.** Where a claim is his, it says so.

This is the design-side companion to [the catalog](../research/credential-types/README.md), which holds the evidence — 195 credential types compiled from eleven sources across five ecosystems — and to [CLASSIFIER.md](../research/credential-types/CLASSIFIER.md), which holds the measurements.

## The question this answers

From [posture.md](posture.md), point 5, in his words: *"At first glance, the most important question about an ACDC DAG is: what kinds of evidence are there? (I am looking at a driver's license, a proof of age, and a credit card)."* arcviz had no answer to that. These categories are the answer's first half. The second half — how a category is conveyed to a viewer — is a separate piece of work and is deliberately not decided here.

## The nine categories

Referred to in lower-kebab, always.

| Category | Means | The test | Bundles with |
|---|---|---|---|
| `identity` | Who a natural person is. The civil-identity attribute set — name, birth date, portrait, place of birth, nationality — plus the things derived from it: an address, an age predicate, a travel document's holder page. | Identity attributes are the payload's point, not merely present in it. | Almost everything. This is the substrate, not a genus. |
| `org-identity` | Who an organization is. A legal identifier (LEI, registration number), a legal name, a vetting result, a level of assurance. | Attributes identifying a legal person. | `authority`, `financial`, `qualification`. |
| `humanness` | That the holder is a real person — and, in the personhood variants, a *unique* one within some community. Deliberately does not say **which** person. | A human-verification basis: a face-to-face meeting, a biometric hash bound to an interaction, a personhood attestation. | Rarely; it is usually the whole claim. |
| `financial` | An account, a payment instrument, a tax relationship, an insurance policy. Anything whose misuse costs money directly. | An account identifier, a card, an IBAN, a tax number, a currency. | `identity` (constantly — see the EU IBAN attestation), `org-identity`. |
| `qualification` | That a party has been assessed against a standard and met it. Degrees, transcripts, professional licences, statutory certifications, awards, driving privileges. | A conferred competence or permission to practise, issued after assessment. | `identity` (a licence is also an identity document), `affiliation`. |
| `health` | Health cover, patient identity, vaccination and test records, prescriptions. Kept separate from `financial` despite health insurance being a policy, because the disclosure stakes are different in kind. | Health-domain claims about a person. | `identity`, `financial`. |
| `affiliation` | That a party is associated with another party. Employment, organizational role, membership, enrolment, loyalty, alumni status, peer relationships. | An association with a named counterparty, without a conferred competence. | `identity`, `qualification`. |
| `authority` | A granted or demonstrated right: to act for another party, or over a controlled resource or identifier. Delegation, guardianship, power of representation, a telephone-number range, a brand, a GS1 prefix, proof of control of a domain. | A right whose scope is stated and whose exercise binds someone else. | `org-identity`, `identity`. |
| `civil-status` | State-recorded facts about a person's status rather than their identity: birth, marriage, death, naturalization, residency status, legally recognized disability. | A registrar's record of a status transition or a standing legal status. | `identity`. |

`misc` is the residual. It exists, it is named honestly, and a credential landing there is a prompt to look rather than a classification.

**Categories are never exclusive.** Roughly a quarter of the catalog carries more than one, and no precedence rule makes that untrue: a driving licence is `identity` and `qualification`; the EU IBAN attestation is `identity` and `financial`; a seafarer certificate is both, plus the issuing officer's own identity inside it. This is a property of the artifacts, not of the scheme.

**When a rendering can show only one, `identity` yields.** It is the substrate of nearly every credential and therefore the least informative thing any credential can say. A driving licence should show the car, not the person. This is implemented as an ordering rule, not a discard.

## What was learned, and what it cost to learn it

### Daniel's genera were on an axis that cannot partition

His 2026-09-19 examples — identity, financial instrument, academic, certification — describe a credential's *domain*, and domain is inherently multi-valued because real credentials bundle. This was the first thing the corpus settled, and it is why the design has two layers instead of one.

### Identity is a substrate, not a bucket

**22 of the 24 EU reference-issuer configurations that publish a claim list carry the holder's name and/or birth date alongside their domain payload** — the loyalty card, the reservation, the tax number, the seafarer certificate. The lone clear exception names a legal person instead. The mirror image holds in KERI: ACDCs bind to a holder by AID, so only about three of the nineteen `bakobo/schema` schemas carry a personal name at all. A rule that fires on "identity attributes are present" therefore matches nearly everything in one ecosystem and nearly nothing in the other.

### A category scheme alone is not enough — there is a second, structural axis

A large minority of the catalog is not about a party at all: another credential, a presentation, a schema, a status list, a set of issuers, a product, a device, an event, a transaction, a wallet, a key, and in one case the verifier. Two further rows invert issuance entirely. None of the nine categories has anything to say about these, and they are not rare. They are handled by a separate structural pair, documented in [CLASSIFIER.md](../research/credential-types/CLASSIFIER.md):

- **subject** — what the credential is about: `party`, `thing`, `occurrence`, `evidence`, `apparatus`, `agent`, `none`, `unknown`.
- **alignment** — how issuer, holder and subject line up: `ordinary`, `self-attested`, `other-party`, `inverted`, `not-a-party`, `unknown`.

Each is single-valued. Splitting them apart from each other, and from the categories, raised measured agreement from 71% to 93% and 91% respectively — with no new evidence and no cleverer rules. The gain came entirely from no longer forcing one answer where an artifact has two. A key-binding attestation is a self-attestation *whose subject is a key*; a single-valued scheme has to throw one of those away.

### The structural axis's job is not to name the kind

`ordinary` — evidence about the party presenting it — is roughly half the corpus. As a set of learnable values that is a poor partition, which inverts what the axis is for. It does not announce which of eight kinds this is; it announces that a credential is **not** the ordinary case. Ordinary becomes the unmarked default and every other value is a deviation the viewer should notice.

### Field presence tells you what a credential carries, not what it is for

Measured: per-label recall 0.94 against precision 0.77. The classifier almost never misses a category that is genuinely present, and reliably adds ones that are present but not the point. Nothing in a JSON Schema expresses **dominance** — which fields are the payload's purpose — so precision is capped until something does.

### The defaults are where the danger is

The single worst defect found was one rule: *an issuee is declared and no fields are published, therefore ordinary.* It accounted for 19 of 42 errors and rendered a Wallet Unit Attestation, a device credential and a relying party's own registration certificate as evidence about the person presenting them — silently, confidently, and in the one direction that matters. It is now a refusal. **`unknown` is a legitimate answer and must render as one**; it must not look like `ordinary`.

### More than half the corpus is invisible to any field-based rule

Only 85 of 195 types publish a field list at all: keri 40 of 56, eudi 25 of 33, but w3c 18 of 65 and wallet 2 of 34. Pass styles are presentation templates with issuer-defined text and no semantics; use-case narratives are not schemas. This is not a defect of the catalog, it is a fact about the ecosystems, and any shipped scheme has to say what it does when handed one.

## What is decided, and what is open

**Decided (his).** The nine categories, and that a structural bucket left undivided is not useful — the categories are load-bearing rather than an optional second stage.

**Synthesized, not ratified.** The two structural axes and their values; the substrate rule that demotes `identity`; the claim that the scarce exclusive channel should carry structure while a plural channel carries categories; every field vocabulary in `classify.py`.

**Open.**

- **How a category is conveyed.** Daniel has said kind should be signalled two ways — a colour or background pattern, and a visual watermark — because redundancy is not a bad thing and colour alone fails colour-blind viewers. Which channel carries which axis is proposed but unsettled, and the icon work is a separate commission.
- **What `unknown` looks like**, and how it differs from `ordinary` at a glance. Nothing specifies this and it is the highest-stakes rendering question the scheme raises.
- **Dominance.** Whether required-versus-optional fields, or field order, proxies well enough to lift precision. Untested, and the cheapest next experiment.
- **Non-schema fallback.** What to classify from when there is no schema — a type identifier, an issuer identity, a registry. Noting that the catalog found type identifiers to be unstable: three spellings of one photo-ID doctype, one EU credential with two identifiers chosen by serialization format, and two distinct schemas sharing one `credentialType` string.
- **`agent`.** A credential whose subject is an AI agent has no category and an under-specified subject value. Two rows today, and rising.

## Where the machinery is

| Path | Holds |
|---|---|
| [`docs/research/credential-types/README.md`](../research/credential-types/README.md) | The 195-row catalog and its sources |
| [`docs/research/credential-types/classify.py`](../research/credential-types/classify.py) | The rules, as ordered predicates over schema field names |
| [`docs/research/credential-types/test_vectors.json`](../research/credential-types/test_vectors.json) | 30 hand-built vectors, each carrying the decision it defends |
| [`docs/research/credential-types/test_classify.py`](../research/credential-types/test_classify.py) | The suite, plus regression floors over the real catalog |
| [`docs/research/credential-types/CLASSIFIER.md`](../research/credential-types/CLASSIFIER.md) | The measurements and the failure analysis |

Run `python3 docs/research/credential-types/test_classify.py` from the repository root's `docs/research/credential-types` directory. No pytest required, though it works under pytest too.
