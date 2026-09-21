# Credential types from `provenant/public-schema` and `~/code/tti/`

Extracted 2026-09-21. Read-only sweep; nothing under `/home/daniel/code/provenant/` or `/home/daniel/code/tti/` was modified.

Conventions used below. **Asserts** quotes or paraphrases the schema's own `description` (source 1) or the prose's own words (source 2); it is never my own characterization. **Key fields** are the verbatim property names of the attributes (`a`) block, including the ACDC housekeeping fields `d` (block SAID), `u` (salty nonce), `i` (issuee AID) and `dt` (issuance datetime), because the presence or absence of `i` is exactly what settles **Issuee?**. **Issuee?** is `yes` when the `a` block declares an `i` property and `no` when it does not — this is a structural reading of the schema, not a claim about how the credential is used in practice. Paths in **Cite** are absolute.

## Source 1 — `/home/daniel/code/provenant/public-schema`

The repo holds **29 credential schema files**: the 28 enumerated in `/home/daniel/code/provenant/public-schema/registry.json`, plus `dossier-base/dossier-base.json`, which exists on disk but is **not** listed in `registry.json` (verified by reading the whole registry file; it has 28 entries). `ai-user-coca/coc1.json` is a code-of-conduct document referenced by the `coc` field, not a credential schema, and is excluded. `*/rules.json` and `*/example*.json` files are likewise excluded.

`also-in-bakobo` was determined by comparing directory names against `ls /home/daniel/code/bakobo/schema`, which holds `ai-coder`, `ai-user-coca`, `attestation`, `award`, `bindkey`, `citation`, `dossier-base`, `faa`, `face-to-face`, `gcd`, `org-vet`, `proof-of-control`, `sedi-age`, `sedi-guardian`, `sedi-id`, `sedi-present-age-portrait`. Note that the brief's expected-overlap list named the four `sedi-*` schemas, but **none of them exist in public-schema** — the overlap is 12 directories, not 15. I did not compare file contents, so `also-in-bakobo: yes` means "a directory of that name exists in both repos", not "the two schemas are identical".

### A2P Campaign Credential

- **Name**: `A2P Campaign Credential` (title); `credentialType: "a2p-campaign-credential"`
- **Asserts**: "A credential issued to a brand for A2P 10DLC messaging campaigns"
- **Key fields**: `d`, `u`, `i`, `dt`, `brandId`, `campaignId`, `campaignType`, `startDate`, `endDate`, `telephoneNumbers`, `authorizedServiceProvider`, `campaignAttributes`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/a2p-campaign/a2p-campaign.schema.json:7` (credentialType), fields at `:45`
- **Status**: stated — title, description, credentialType and the `a`-block properties are all literal in the schema.
- **also-in-bakobo**: no

### Aegis Standard Vetting Result Credential

- **Name**: `Aegis Standard Vetting Result Credential` (title); `credentialType: "AegisStdVetCredential"`
- **Asserts**: "Report results of Aegis's standard vetting of an org."
- **Key fields**: `d`, `dt`, `id` ("Vetting request ID"), `score` ("The Vetting Score, 0-100, with 100 being the most robust reputation."), `iat` ("Vetting token issued date-time"), `exp` ("Vetting token expiration date-time"), `irp` ("from identityRulesPassed"), `cat` ("short strings that describe ways that the key will be used")
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/aegis-std-vetting/aegis-std-vetting.schema.json:7` (credentialType), fields at `:30`
- **Status**: stated — all field names and their quoted descriptions are literal. Worth flagging that the `cat` description ("ways that the key will be used") appears copied from another schema and does not match a vetting-result field; I record it verbatim without resolving the discrepancy.
- **also-in-bakobo**: no

### AI coder license

- **Name**: `AI coder license` (title); `credentialType: "ai-coder-license"`
- **Asserts**: "Certify that a software developer is committed to and capable of using AI coding tools with appropriate guard rails, according to the governance in the rules section."
- **Key fields**: `d`, `u`, `i`, `dt`, `effective_dt`, `expire_dt`, `issuer_name`, `issuee_name`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/ai-coder/ai-coder.schema.json:7` (credentialType), fields at `:42`
- **Status**: stated.
- **also-in-bakobo**: yes

### AI user code of conduct attestation

- **Name**: `AI user code of conduct attestation` (title); `credentialType: "ai-user-coca"`
- **Asserts**: "Attest that the issuer is committed to follow a particular code of conduct with respect to their personal use of AI."
- **Key fields**: `d`, `i`, `dt`, `effective_dt`, `coc` ("The code of conduct to which the issuer commits. SHOULD hold the SAID of a document published elsewhere, OR HTML encoded as a data URL.")
- **Issuee?**: yes (an `i` property is declared, described as "AID of issuee (award recipient)")
- **Cite**: `/home/daniel/code/provenant/public-schema/ai-user-coca/ai-user-coca.schema.json:7` (credentialType), fields at `:38`
- **Status**: stated, with a caveat I am not resolving — the description says the *issuer* commits, while the `a` block carries an `i` whose own description is copy-pasted from the award schema ("award recipient"). Both readings are literally present in the file.
- **also-in-bakobo**: yes

### Data Attestation

- **Name**: `Data Attestation` (title); `credentialType: "DataAttestation"`
- **Asserts**: "Data attestation enables verifiable attestation of the data(cryptographic digest) by the Issuer"
- **Key fields**: `d`, `dt`, `digest`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/attestation/attestation.schema.json:7` (credentialType), fields at `:38`
- **Status**: stated.
- **also-in-bakobo**: yes

### Award Credential

- **Name**: `Award Credential` (title); `credentialType: "AwardCredential"`
- **Asserts**: "Confer an award on a staff member or other associated person or group."
- **Key fields**: `d`, `u`, `i`, `dt`, `effective_dt`, `issuer_name`, `award_name`, `category`, `timeframe`, `details`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/award/award.schema.json:7` (credentialType), fields at `:42`
- **Status**: stated.
- **also-in-bakobo**: yes

### Bind Key

- **Name**: `Bind Key` (title); `credentialType: "BindKeyAttestation"`
- **Asserts**: "Declare that issuer uses a cryptographic key that's not directly managed by the KEL (e.g., to conform to an external standard). Issuing this ACDC makes key binding provable and revokable."
- **Key fields**: `d`, `dt`, `pubkey`, `startDate`, `stopDate`, `uses`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/bindkey/bindkey.schema.json:8` (credentialType), fields at `:39`
- **Status**: stated.
- **also-in-bakobo**: yes

### Brand Owner Credential

- **Name**: `Brand Owner Credential` (title); `credentialType: "BrandOwnerCredential"`
- **Asserts**: "Issued to a legal entity that has the right to use a brand because it is the direct owner or a licensee of that brand."
- **Key fields**: `d`, `i`, `dt`, `vcard`, `goals`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/brand-owner/brand-owner.schema.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### Citation

- **Name**: `Citation` (title); `credentialType: "citation"`
- **Asserts**: "Formally reference non-ACDC content."
- **Key fields**: `d`, `dt`, `sdt`, `des`, `typ`, `lbl`, `content`, `siz`, `loc`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/citation/citation.schema.json:7` (credentialType), fields at `:39`
- **Status**: stated.
- **also-in-bakobo**: yes

### Dossier (Base)

- **Name**: `Dossier (Base)` (title); no `credentialType` property anywhere in the file
- **Asserts**: "Base schema for verifiable dossiers — issuer-curated, ACDC-native collections of evidence with no issuee. Any schema that derives from this one (via an allOf $ref to this schema's SAID) is considered a dossier schema."
- **Key fields**: `d`, `dt`, `assemble_dt`, `assembler`, `purpose`, `ref`, `gov`, `evt_dt`, `evt_loc`, `jur`, `class`, `phase`, `gov_rules`
- **Issuee?**: no — the `a` block's own description says it "SHOULD NOT include an `i` (issuee) field"
- **Cite**: `/home/daniel/code/provenant/public-schema/dossier-base/dossier-base.json:5` (description), fields at `:41`
- **Status**: stated. Two structural notes, both literal: the file is absent from `registry.json`, and its top-level properties are `v, d, u, i, rd, s, a, e, r` — `rd` rather than the `ri` every other schema here uses.
- **also-in-bakobo**: yes

### Foreign Artifact Affidavit

- **Name**: `Foreign Artifact Affidavit` (title); `credentialType: "foreign-artifact-affidavit"`
- **Asserts**: "An ACDC wrapper that gives arbitrary binary data a tamper-evident, cryptographic identity, and that documents key attributes. This allows it to be cited as evidence in a verifiable data graph."
- **Key fields**: `d`, `u`, `dt`, `content_identifier`, `art_posture`, `rev_latency`, `content_type`, `content_size`, `content_location`, `filename`, `description`, `provenance`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/faa/faa.schema.json:7` (credentialType), fields at `:44`
- **Status**: stated.
- **also-in-bakobo**: yes

### Face-to-Face credential

- **Name**: `Face-to-Face credential` (title); `credentialType: "FaceToFaceCredential"`
- **Asserts**: "Assert that an issuer knows the issuee to be a human being, based one or more face-to-face interactions."
- **Key fields**: `d`, `u`, `i`, `dt`, `assertDate`, `minutes`, `biometricHashes`, `basis`, `caveats`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/face-to-face/face-to-face.schema.json:8` (credentialType), fields at `:44`
- **Status**: stated.
- **also-in-bakobo**: yes

### Generalized Cooperative Delegation Credential

- **Name**: `Generalized Cooperative Delegation Credential` (title); `credentialType: "gcd-credential"`
- **Asserts**: "Define the authorizations, duties, and constraints of a person who receives delegated authority."
- **Key fields** (committed version, `git show HEAD:gcd/gcd.schema.json`, which parses cleanly): `d`, `u`, `i`, `dt`, `gfw`, `role`, `c_goal`, `c_pgeo`, `c_rgeo`, `c_jur`, `c_ical`, `c_proto`, `c_prove`, `c_human`, `c_after`, `c_before`. The working tree additionally carries `c_upto` ("Constrains the financial stakes of the delegated action; the delegate can act only in contexts where a financial value less than this value is at stake.", examples `"25 CHF"`, `"0.3 BTC"`, `"4 OZ-XAU"`), which is **not committed** — see Status.
- **Issuee?**: yes (`i` described as "AID of delegate, as it appears in delegator's interaction event")
- **Cite**: `/home/daniel/code/provenant/public-schema/gcd/gcd.schema.json:8` (credentialType), fields at `:58`; the `c_upto` addition at `:169` of the working tree and at `/home/daniel/code/provenant/public-schema/gcd/index.md:39`
- **Status**: stated for title, description, credentialType and the 16 committed field names. Two things a consumer needs to know about this file, both verified and neither caused by this sweep. First, **the working-tree copy is not valid JSON** — `python3 json.loads` and `jq empty` both fail with "Expecting ',' delimiter / Objects must consist of key:value pairs at line 223, column 9". Second, that breakage comes from an **uncommitted local edit**: `git status` reports `gcd/gcd.schema.json` and `gcd/index.md` as modified, both with an mtime of 2026-06-10, and the diff adds the `c_upto` block with one unbalanced brace. `git show HEAD:gcd/gcd.schema.json` parses without error, so the published schema is fine and `c_upto` is a work-in-progress field that has never shipped. I left both files exactly as found. The last commit to touch the schema is `4ac7b37` "In gcd schema, made attribute section nonce field optional (#16)".
- **also-in-bakobo**: yes

### Org Vet

- **Name**: `Org Vet` (title); `credentialType: "orgVet"`
- **Asserts**: "Authenticate an org with an explicit level of assurance."
- **Key fields**: `d`, `dt`, `loa` ("Level of assurance."), `lids` ("Array of linked identifiers (LIDs) that vetter claims were able to act as references for this legal entity when the org was vetted.")
- **Issuee?**: no — the `a` block declares no `i`, so the org being vetted is identified through `lids` rather than as an issuee
- **Cite**: `/home/daniel/code/provenant/public-schema/org-vet/org-vet.schema.json:7` (credentialType), fields at `:39`
- **Status**: stated.
- **also-in-bakobo**: yes

### OVC Brand Owner Credential

- **Name**: `OVC Brand Owner Credential` (title); `credentialType: "BrandOwnerCredential"` — the same credentialType string as `brand-owner`, under a different title and a different schema SAID
- **Asserts**: "Issued to a legal entity that has the right to use a brand because it is the direct owner or a licensee of that brand." (byte-identical to `brand-owner`'s description)
- **Key fields**: `d`, `i`, `dt`, `vcard`, `goals`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/ovc-brand-owner/ovc-brand-owner.schema.json:7` (credentialType), fields at `:34`
- **Status**: stated. Recorded as a separate entry because it is a separate registry entry with its own SAID (`EAoRVmgPyacjhUxaV0nPwiuUuHMjKDpNZrj7ClofZ-3Z`); I am not asserting whether it is a variant, a fork or a stale copy.
- **also-in-bakobo**: no

### OVC Identity Credential

- **Name**: `OVC Identity Credential` (title); `credentialType: "orgVet"` — the same credentialType string as `org-vet`, under a different title and a different schema SAID
- **Asserts**: "Authenticate an org with an explicit level of assurance." (byte-identical to `org-vet`'s description)
- **Key fields**: `d`, `dt`, `loa`, `lids`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/ovc-org-vet/ovc-org-vet.schema.json:7` (credentialType), fields at `:39`
- **Status**: stated. Same note as OVC Brand Owner — separate registry entry, own SAID (`EHFdm3U_4nML6lo-q_xDTO8183hC9HlWif2l4ycNo8TW`).
- **also-in-bakobo**: no

### Proof-of-Control Credential

- **Name**: `Proof-of-Control Credential` (title); `credentialType: "ProofOfControlCredential"`
- **Asserts**: "Assert the issuee has demonstrated to the issuer the ability to control a digital resource like a web site, social media handle, or email address."
- **Key fields**: `d`, `u`, `i`, `dt`, `res`, `be`, `assertDate`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/proof-of-control/proof-of-control.schema.json:7` (credentialType), fields at `:42`
- **Status**: stated.
- **also-in-bakobo**: yes

### TCR Vetting Credential

- **Name**: `TCR Vetting Credential` (title); `credentialType: "TCRVettingCredential"`
- **Asserts**: "The Campaign Registry(TCR) Vetting Credential issued to a Brand for A2P 10DLC messaging campaigns"
- **Key fields**: `d`, `i`, `dt`, `legalCompanyName`, `legalCompanyAddress`, `taxId`, `vettingScore`, `LEI`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/tcr-vetting/tcr-vetting.schema.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### TN Allocation Credential

- **Name**: `TN Allocation Credential` (title); `credentialType: "TNAllocationCredential"`
- **Asserts**: "TN Allocation credential proves an enterpise has the right to use(RTU) specific telephone numbers, either directly from a regulator or through a telephone number provider."
- **Key fields**: `d`, `u`, `i`, `dt`, `numbers`, `channel`, `doNotOriginate`, `startDate`, `endDate`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/tn-alloc/tn-alloc.schema.json:7` (credentialType), fields at `:44`
- **Status**: stated (the typo "enterpise" is the source's).
- **also-in-bakobo**: no

### Telephone Number Credential

- **Name**: `Telephone Number Credential` (title); `credentialType: "TelephoneNumberCredential"`
- **Asserts**: "Telephone Number Credential issued to a Brand for A2P 10DLC messaging campaigns"
- **Key fields**: `d`, `u`, `i`, `dt`, `numbers`, `channel`, `doNotOriginate`, `startDate`, `endDate` (the same field set as TN Allocation)
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/tn/tn.schema.json:7` (credentialType), fields at `:45`
- **Status**: stated.
- **also-in-bakobo**: no

### ECR Authorization vLEI Credential

- **Name**: `ECR Authorization vLEI Credential` (title); `credentialType: "ECRAuthorizationvLEICredential"`
- **Asserts**: "A vLEI Authorization Credential issued by a Legal Entity to a QVI for the authorization of ECR credentials"
- **Key fields**: `d`, `i`, `dt`, `AID`, `LEI`, `personLegalName`, `engagementContextRole`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/ecr-authorization-vlei-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### Legal Entity Engagement Context Role vLEI Credential

- **Name**: `Legal Entity Engagement Context Role vLEI Credential` (title); `credentialType: "LegalEntityEngagementContextRolevLEICredential"`
- **Asserts**: "A vLEI Role Credential issued to representatives of a Legal Entity in other than official roles but in functional or other context of engagement"
- **Key fields**: `d`, `u`, `i`, `dt`, `LEI`, `personLegalName`, `engagementContextRole`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/legal-entity-engagement-context-role-vLEI-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### Legal Entity Official Organizational Role vLEI Credential

- **Name**: `Legal Entity Official Organizational Role vLEI Credential` (title); `credentialType: "LegalEntityOfficialOrganizationalRolevLEICredential"`
- **Asserts**: "A vLEI Role Credential issued by a Qualified vLEI issuer to official representatives of a Legal Entity"
- **Key fields**: `d`, `i`, `dt`, `LEI`, `personLegalName`, `officialRole`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/legal-entity-official-organizational-role-vLEI-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### Legal Entity vLEI Credential

- **Name**: `Legal Entity vLEI Credential` (title); `credentialType: "LegalEntityvLEICredential"`
- **Asserts**: "A vLEI Credential issued by a Qualified vLEI issuer to a Legal Entity"
- **Key fields**: `d`, `i`, `dt`, `LEI`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/legal-entity-vLEI-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### OOR Authorization vLEI Credential

- **Name**: `OOR Authorization vLEI Credential` (title); `credentialType: "OORAuthorizationvLEICredential"`
- **Asserts**: "A vLEI Authorization Credential issued by a Legal Entity to a QVI for the authorization of OOR credentials"
- **Key fields**: `d`, `i`, `dt`, `AID`, `LEI`, `personLegalName`, `officialRole`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/oor-authorization-vlei-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### Qualified vLEI Issuer Credential

- **Name**: `Qualified vLEI Issuer Credential` (title); `credentialType: "QualifiedvLEIIssuervLEICredential"`
- **Asserts**: "A vLEI Credential issued by GLEIF to Qualified vLEI Issuers which allows the Qualified vLEI Issuers to issue, verify and revoke Legal Entity vLEI Credentials and Legal Entity Official Organizational Role vLEI Credentials"
- **Key fields**: `d`, `i`, `dt`, `LEI`, `gracePeriod`
- **Issuee?**: yes
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/qualified-vLEI-issuer-vLEI-credential.json:7` (credentialType), fields at `:34`
- **Status**: stated.
- **also-in-bakobo**: no

### iXBRL Data Value Attestation

- **Name**: `iXBRL Data Value Attestation` (title); `credentialType: "iXBRLDataAttestation"`
- **Asserts**: "A data attestation against an iXBRL report, linked to either a vLEI OOR or vLEI ECR credential"
- **Key fields**: `d`, `dt`, `rd`, `f`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/verifiable-ixbrl-report-attestation.json:6` (credentialType), fields at `:25`
- **Status**: stated.
- **also-in-bakobo**: no

### iXBRL Data Value D6 Attestation

- **Name**: `iXBRL Data Value D6 Attestation` (title); `credentialType: "iXBRLDataD6Attestation"`
- **Asserts**: "A data attestation against an iXBRL report, linked to either a vLEI OOR or vLEI ECR credential using Digital Signatures in XBRL(D6) specification"
- **Key fields**: `d`, `dt`, `rd`, `target`, `targetDigest`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/vLEI/acdc/verifiable-ixbrl-report-d6-attestation.json:6` (credentialType), fields at `:25`
- **Status**: stated.
- **also-in-bakobo**: no

### Verifiable Voice Dossier Credential

- **Name**: `Verifiable Voice Dossier Credential` (title); `credentialType: "VvpDossierCredential"`
- **Asserts**: "Attestation credential, issued by the accountable party, that assembles all of the evidence required as per the Verifiable Voice Protocol"
- **Key fields**: `d`, `dt`, `name`
- **Issuee?**: no
- **Cite**: `/home/daniel/code/provenant/public-schema/vvp-dossier/vvp-dossier.schema.json:7` (credentialType), fields at `:39`
- **Status**: stated. The payload is carried in the edges (`e`) block rather than in `a`, which is why the attributes block has only three fields.
- **also-in-bakobo**: no

## Source 2 — verifiable IBAN (REDACTED: the underlying material is private)

**This section is deliberately thin, and the reason is publication hygiene rather than a thin sweep.** The verifiable-IBAN material lives in `~/code/tti/`, which is private client work in private repositories, and this repository is public. Per [EVIDENCE.md](../../EVIDENCE.md) rule 4, non-republishable material is cited by description and by public URL only, and the local detail stays in `.ignored/private-refs/`. What follows records that the work exists and what is publicly checkable about it; the internal analysis, its file paths and its quotations are not reproduced here.

**What the sweep established, publishable.** The one entry backed by an actual artifact rather than prose is a live **EU IBAN attestation**, obtained on 2026-08-28 from the European Commission's own reference issuer. It is an SD-JWT VC, not an ACDC. Its `vct` is `urn:eu.europa.ec.eudi:iban:1`, its credential configuration id is `eu.europa.ec.eudi.iban_sd_jwt_vc`, and its twenty claims are `iban`, `currency`, `bank_account_status`, `payment_possibility`, `registered_family_name`, `registered_given_name`, `date_of_birth`, `account_holder_owner`, `coowner`, `issuing_organization`, `business_identifier_code`, `national_account_number`, `account_product`, `account_name`, `account_type`, `disponent`, `national_bank_code`, `issuance_date`, `expiry_date`, `credential_type`. Every one of those is independently verifiable at the public endpoint `https://issuer.eudiw.dev/.well-known/openid-credential-issuer`, which is where this catalog cites them — see [`eudi-firstperson.md`](eudi-firstperson.md) §1, where the same configuration was enumerated independently. **It binds an IBAN to a natural person and carries no legal-person claim at all** — no LEI, no registration number, nothing that could carry a corporate identity. Four properties of the live artifact bear on how such a credential would render: every claim including the IBAN itself is selectively disclosable, with nothing in the clear but `iss`, `iat`, `exp`, `vct`, `status` and `cnf`; the attribute values were typed into a web form and verified by nobody; the signing certificate is a PID document signer with no indication that the issuer is a bank or is supervised; and four claims declared as booleans in the issuer metadata are carried as the strings `"true"`/`"false"` in the credential.

**Recorded as existing, not reproduced.** The private material also discusses a conventional *name-to-IBAN credential* asserting that an IBAN belongs to a legal person, which the internal analysis argues against; a multi-link *chain of authority* construction it prefers; the EU wallet pilots' own IBAN attestation rulebook, summarised at second hand; and PSD2 qualified certificates under ETSI TS 119 495, raised as a production analogue of a credential outliving the fact it asserts. These appear in the catalog as rows without detail. Anyone continuing this line of work should read the rulebook and the ETSI specification directly rather than relying on a summary — which is the same rule this repository applies to every second-hand citation.

**One terminological trap, because both spellings appear in the literature.** `vIBAN` in European Banking Authority material means **virtual IBAN**, a regulatory and anti-money-laundering concept about IBANs that map to a master account. That is not "verifiable IBAN" and the two must not be merged.
