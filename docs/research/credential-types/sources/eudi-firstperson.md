# EUDI reference issuer, EUDI ARF, and the First Person Project

Extraction compiled 2026-09-21. Everything below the three `##` sections was fetched live on that date; the retrieval command and HTTP status for each source is recorded in its section preamble. The final `## from-memory-UNVERIFIED` section is walled off from the fetched material.

## 1. issuer.eudiw.dev (EUDI Wallet reference "EUDIW Testing Issuer")

**Provenance.** `curl https://issuer.eudiw.dev/.well-known/openid-credential-issuer` returned HTTP 200, 91,319 bytes of JSON, containing `credential_configurations_supported` with exactly 27 entries. The landing page at `https://issuer.eudiw.dev/` (HTTP 200) renders as server-side HTML and describes itself in prose as "This is a EUDIW Testing Issuer supporting PID and mDL in mDoc and SD-JWT VC format at the following OID4VCI url: https://issuer.eudiw.dev/.well-known/openid-credential-issuer" — i.e. the landing page names only PID and mDL, and understates what the metadata actually advertises. The metadata is the authoritative enumeration and is what is recorded here. Issuer top-level `display[0].name` is `"Digital Credentials Issuer"`; `credential_issuer` is `https://issuer.eudiw.dev`.

**Blanket facts that hold for all 27 entries, so they are not repeated per entry.** Every configuration carries `cryptographic_binding_methods_supported: ["jwk","cose_key"]` and `proof_types_supported` with keys `attestation` and `jwt` — that is, all 27 are holder-key-bound and require a holder proof-of-possession at issuance, which is the basis for every `Issuee? yes` below. Display names, formats, doctypes, vcts and claim path names are verbatim from the metadata. Claim paths are given with the mdoc namespace prefix stripped where the metadata repeats the doctype as `path[0]`; the two ISO configurations (`mdl_mdoc`, `photoid`, `reservation_mdoc`) use a namespace distinct from their doctype so their prefix is shown as the metadata gives it. Nested SD-JWT claims are shown dotted (`address.locality`). Note that the SD-JWT format string used throughout is `dc+sd-jwt`, not `vc+sd-jwt`. Several entries carry `credential_metadata.credential_reuse_policy.id: "arf_annex_ii"`, an explicit back-reference from this issuer to the ARF. The `Asserts` clause in each entry is a one-line characterisation drawn from the entry's own display name and claim set — the metadata gives no separate prose definition of what any credential asserts — so `Asserts` is marked `inferred` in every `Status` line below while the name, format, doctype/vct and field names are `stated`.

### Certificate of Residence (MSO Mdoc)

- **Name**: `Certificate of Residence (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.cor_mdoc`)
- **Asserts**: that the named natural person resides at a stated address in a stated issuing country, from a stated arrival date.
- **Key fields**: `given_name`, `family_name`, `birth_date`, `residence_address`, `gender`, `birth_place`, `nationality`, `arrival_date`, `expiry_date`, `issuance_date`, `issuing_country`, `issuing_authority`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.cor_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.cor.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### Diploma (SD-JWT VC)

- **Name**: `Diploma (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.diploma_vc_sd_jwt`)
- **Asserts**: an educational affiliation and identity within a home organization, with an assurance level.
- **Key fields**: `identifier`, `scoped_affiliation`, `personal_unique_code`, `personal_unique_id`, `home_organization`, `family_name`, `first_name`, `display_name`, `date_of_birth`, `common_name`, `email`, `principal_name`, `primary_affiliation`, `affiliations`, `assurance`, `image`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.diploma_vc_sd_jwt"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:diploma:1:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred from the display name and claim set. Note the claim set is an eduPerson-style affiliation schema rather than an award/qualification schema, despite the name "Diploma".

### EHIC (MSO Mdoc)

- **Name**: `EHIC (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.ehic_mdoc`)
- **Asserts**: entitlement to healthcare under a competent institution for a stated period (European Health Insurance Card).
- **Key fields**: `credential_holder`, `subject`, `social_security_pin`, `starting_date`, `ending_date`, `document_id`, `competent_institution`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.ehic_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.ehic.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`; also `credential_metadata.credential_reuse_policy.id` = `arf_annex_ii`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name, the acronym EHIC, and the claim set. The expansion "European Health Insurance Card" is not written out in the metadata.

### EHIC (SD-JWT VC)

- **Name**: `EHIC (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.ehic_sd_jwt_vc`)
- **Asserts**: as above, in SD-JWT VC form, with the issuing authority and authentic source each modelled as an id/name pair.
- **Key fields**: `personal_administrative_number`, `issuing_authority`, `issuing_authority.id`, `issuing_authority.name`, `issuing_country`, `date_of_expiry`, `date_of_issuance`, `authentic_source`, `authentic_source.id`, `authentic_source.name`, `starting_date`, `ending_date`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.ehic_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eudi:ehic:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred. Note the vct namespace here is `urn:eudi:` while most other SD-JWT entries use `urn:eu.europa.ec.eudi:`.

### Employee ID (MSO Mdoc)

- **Name**: `Employee ID (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.employee_mdoc`)
- **Asserts**: that the named person is an employee of a named employer under a stated employment type, from a stated start date.
- **Key fields**: `given_name`, `family_name`, `birth_date`, `employee_id`, `employer_name`, `employment_start_date`, `employment_type`, `country_code`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.employee_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.employee.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### Health ID (MSO Mdoc)

- **Name**: `Health ID (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.hiid_mdoc`)
- **Asserts**: a health insurance and patient identifier for the holder, plus a block of "matching" identity attributes for record linkage against a health system.
- **Key fields**: `health_insurance_id`, `patient_id`, `tax_number`, `one_time_token`, `affiliation_country`, `issuance_date`, `expiry_date`, `matching_institution-id`, `matching_registered_family_name`, `matching_registered_given_name`, `matching_resident_address`, `matching_birth_place`, `matching_birth_date`, `issuing_authority`, `document_number`, `administrative_number`, `issuing_country`, `issuing_jurisdiction`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.hiid_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.hiid.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set. The `matching_*` prefix and the `one_time_token` claim are stated field names; the record-linkage purpose read into them is inference.

### Health ID (SD-JWT VC)

- **Name**: `Health ID (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.hiid_sd_jwt_vc`)
- **Asserts**: as the mdoc Health ID above; the claim set is identical.
- **Key fields**: `health_insurance_id`, `patient_id`, `tax_number`, `one_time_token`, `affiliation_country`, `issuance_date`, `expiry_date`, `matching_institution-id`, `matching_registered_family_name`, `matching_registered_given_name`, `matching_resident_address`, `matching_birth_place`, `matching_birth_date`, `issuing_authority`, `document_number`, `administrative_number`, `issuing_country`, `issuing_jurisdiction`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.hiid_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:hiid:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### IBAN (MSO Mdoc)

- **Name**: `IBAN (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.iban_mdoc`)
- **Asserts**: that a named bank account (IBAN) at a named institution is held by the named person in a stated role (owner, co-owner or disponent), with its product type, currency and status.
- **Key fields**: `iban`, `national_account_number`, `account_product`, `account_name`, `account_type`, `currency`, `bank_account_status`, `payment_possibility`, `registered_family_name`, `registered_given_name`, `date_of_birth`, `account_holder_owner`, `coowner`, `disponent`, `issuing_organization`, `national_bank_code`, `issuance_date`, `expiry_date`, `credential_type`, `business_identifier_code`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.iban_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.iban.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### IBAN (SD-JWT VC)

- **Name**: `IBAN (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.iban_sd_jwt_vc`)
- **Asserts**: as the mdoc IBAN above; the claim set is identical.
- **Key fields**: `iban`, `national_account_number`, `account_product`, `account_name`, `account_type`, `currency`, `bank_account_status`, `payment_possibility`, `registered_family_name`, `registered_given_name`, `date_of_birth`, `account_holder_owner`, `coowner`, `disponent`, `issuing_organization`, `national_bank_code`, `issuance_date`, `expiry_date`, `credential_type`, `business_identifier_code`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.iban_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:iban:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### Learning Credential (SD-JWT VC)

- **Name**: `Learning Credential (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.learning_credential_vc_sd_jwt`)
- **Asserts**: that the named learner achieved a titled learning achievement, with its outcomes, grade, level, study time, prerequisites and quality assurance.
- **Key fields**: `family_name`, `given_name`, `achievement_title`, `achievement_description`, `learning_outcomes`, `assessment_grade`, `language_of_classes`, `learner_identification`, `expected_study_time`, `level_of_learning_experience`, `types_of_quality_assurance`, `prerequisites_to_enroll`, `integration_stackability_options`, `issuing_authority`, `issuing_country`, `date_of_issuance`, `date_of_expiry`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.learning_credential_vc_sd_jwt"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:learning:credential:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred from the display name and claim set

### Loyalty (MSO Mdoc)

- **Name**: `Loyalty (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.loyalty_mdoc`)
- **Asserts**: that the named person is a client of a named company under a client identifier.
- **Key fields**: `given_name`, `family_name`, `company`, `client_id`, `issuance_date`, `expiry_date`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.loyalty_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.loyalty.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### mDL (MSO Mdoc)

- **Name**: `mDL (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.mdl_mdoc`)
- **Asserts**: driving privileges held by the named person, in the ISO/IEC 18013-5 mobile driving licence doctype.
- **Key fields** (all under namespace `org.iso.18013.5.1`): `family_name`, `given_name`, `birth_date`, `issue_date`, `expiry_date`, `issuing_country`, `issuing_authority`, `document_number`, `portrait`, `driving_privileges`, `un_distinguishing_sign`, `administrative_number`, `sex`, `height`, `weight`, `eye_colour`, `hair_colour`, `birth_place`, `resident_address`, `portrait_capture_date`, `age_in_years`, `age_birth_year`, `age_over_18`, `issuing_jurisdiction`, `nationality`, `resident_city`, `resident_state`, `resident_postal_code`, `resident_country`, `family_name_national_character`, `given_name_national_character`, `signature_usual_mark`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.mdl_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`org.iso.18013.5.1.mDL`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the doctype and claim set. `age_over_18` is a stated claim name, so this credential carries a derived age-threshold attribute alongside full birth date.

### MSISDN (MSO Mdoc)

- **Name**: `MSISDN (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.msisdn_mdoc`)
- **Asserts**: that a named mobile phone number is contracted to and in use by the named person with a named mobile operator.
- **Key fields**: `phone_number`, `registered_family_name`, `registered_given_name`, `contract_owner`, `end_user`, `mobile_operator`, `issuance_date`, `expiry_date`, `credential_type`, `issuing_organization`, `phone_number_in_use`, `document_number`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.msisdn_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.msisdn.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### MSISDN (SD-JWT VC)

- **Name**: `MSISDN (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.msisdn_sd_jwt_vc`)
- **Asserts**: as the mdoc MSISDN above; the claim set is identical.
- **Key fields**: `phone_number`, `registered_family_name`, `registered_given_name`, `contract_owner`, `end_user`, `mobile_operator`, `issuance_date`, `expiry_date`, `credential_type`, `issuing_organization`, `phone_number_in_use`, `document_number`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.msisdn_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:msisdn:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### PDA1 (MSO Mdoc)

- **Name**: `PDA1 (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.pda1_mdoc`)
- **Asserts**: which member state's social security legislation applies to the holder's employment, confirmed by a competent institution (the Portable Document A1).
- **Key fields**: `credential_holder`, `social_security_pin`, `employment_details`, `places_of_work`, `legislation`, `status_confirmation`, `document_id`, `competent_institution`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.pda1_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.pda1.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the claim names `legislation` and `status_confirmation`. The expansion "Portable Document A1" is not written out in the metadata.

### PDA1 (SD-JWT VC)

- **Name**: `PDA1 (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.pda1_sd_jwt_vc`)
- **Asserts**: as the mdoc PDA1 above, but with the nested structure fully expanded into 41 claim paths.
- **Key fields**: `credential_holder`, `credential_holder.family_name`, `credential_holder.given_name`, `credential_holder.birth_date`, `social_security_pin`, `employment_details`, `employment_details.employment_type`, `employment_details.name`, `employment_details.employer_id`, `employment_details.id_type`, `employment_details.street`, `employment_details.town`, `employment_details.postal_code`, `employment_details.country_code`, `places_of_work`, `places_of_work.place_of_work`, `places_of_work.no_fixed_place`, `places_of_work.place_of_work.company`, `places_of_work.place_of_work.flag_base_home_state`, `places_of_work.place_of_work.company_id`, `places_of_work.place_of_work.id_type`, `places_of_work.place_of_work.street`, `places_of_work.place_of_work.town`, `places_of_work.place_of_work.postal_code`, `places_of_work.place_of_work.country_code`, `places_of_work.no_fixed_place.country_code`, `legislation`, `legislation.member_state`, `legislation.transitional_rules`, `legislation.starting_date`, `legislation.ending_date`, `status_confirmation`, `document_id`, `competent_institution`, `competent_institution.institution_id`, `competent_institution.institution_name`, `competent_institution.country_code`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.pda1_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:pda1:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### Photo ID (MSO Mdoc)

- **Name**: `Photo ID (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.photoid`)
- **Asserts**: a photographic identity document in the ISO/IEC 23220-2 photo ID doctype, carrying a portrait plus civil identity attributes in both Unicode and Latin-1 transcriptions.
- **Key fields** (all under namespace `org.iso.23220.photoid.1`): `portrait`, `portrait_capture_date`, `family_name_unicode`, `given_name_unicode`, `family_name_latin1`, `given_name_latin1`, `birth_date`, `age_over_18`, `age_in_years`, `age_birth_year`, `birthplace`, `name_at_birth`, `resident_address_unicode`, `resident_city_unicode`, `resident_postal_code`, `resident_country`, `resident_city_latin1`, `sex`, `nationality`, `document_number`, `issuing_subdivision`, `issuance_date`, `expiry_date`, `issuing_authority_unicode`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.photoid"]`, keys `format` (`mso_mdoc`), `doctype` (`org.iso.23220.2.photoid.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred. Note a stated discrepancy in the metadata itself: the `doctype` is `org.iso.23220.2.photoid.1` while the claim paths use the namespace `org.iso.23220.photoid.1` (no `.2`).

### PID (MSO Mdoc)

- **Name**: `PID (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.pid_mdoc`)
- **Asserts**: Person Identification Data — the core civil identity of a natural person, in the EUDI PID doctype.
- **Key fields**: `family_name`, `given_name`, `birth_date`, `family_name_birth`, `given_name_birth`, `place_of_birth`, `resident_address`, `resident_country`, `resident_state`, `resident_city`, `resident_postal_code`, `resident_street`, `resident_house_number`, `personal_administrative_number`, `sex`, `email_address`, `mobile_phone_number`, `nationality`, `issuance_date`, `expiry_date`, `issuing_authority`, `document_number`, `trust_anchor`, `issuing_country`, `portrait`, `issuing_jurisdiction`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.pid_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.pid.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); the expansion "Person Identification Data" is stated in the ARF (see §2) rather than in this metadata, so the Asserts clause is inferred here

### PID (MSO Mdoc Deferred)

- **Name**: `PID (MSO Mdoc Deferred)` (configuration id `eu.europa.ec.eudi.pid_mdoc_deferred`)
- **Asserts**: the same thing as `PID (MSO Mdoc)` — same doctype, same 26 claims — issued through the deferred-issuance flow rather than immediately.
- **Key fields**: identical to `PID (MSO Mdoc)` above
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.pid_mdoc_deferred"]`, `doctype` (`eu.europa.ec.eudi.pid.1`, identical to the non-deferred entry), and top-level `deferred_credential_endpoint` (`https://backend.issuer.eudiw.dev/deferred_credential`)
- **Status**: stated (it is a distinct configuration id with its own display name); the reading that it is an issuance-flow variant rather than a distinct credential kind is inferred from the identical doctype and claim set

### PID (SD-JWT VC)

- **Name**: `PID (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.pid_vc_sd_jwt`)
- **Asserts**: Person Identification Data in SD-JWT VC form, using OIDC-style claim naming (`birthdate`, `picture`, `address.*`) rather than the mdoc names.
- **Key fields**: `family_name`, `given_name`, `birthdate`, `place_of_birth`, `nationalities`, `address`, `address.street_address`, `address.locality`, `address.region`, `address.postal_code`, `address.country`, `address.formatted`, `address.house_number`, `personal_administrative_number`, `picture`, `birth_family_name`, `birth_given_name`, `sex`, `email`, `phone_number`, `date_of_issuance`, `date_of_expiry`, `issuing_authority`, `document_number`, `trust_anchor`, `issuing_country`, `issuing_jurisdiction`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.pid_vc_sd_jwt"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eudi:pid:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred. The divergence in claim naming between the mdoc and SD-JWT PID is stated — both claim lists are verbatim.

### Power Of Representation (MSO Mdoc)

- **Name**: `Power Of Representation (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.por_mdoc`)
- **Asserts**: that the holder may represent a named legal person, with full powers or a scoped eService, for a stated effective period.
- **Key fields**: `legal_person_identifier`, `legal_name`, `full_powers`, `eService`, `effective_from_date`, `effective_until_date`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_jurisdiction`, `issuing_country`
- **Issuee?**: yes — and note this is the one entry in this issuer whose subject matter is a relation between the holder and a *third party* (the represented legal person), rather than an attribute of the holder alone
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.por_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.por.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts and the third-party observation inferred from the claim names `legal_person_identifier`, `legal_name` and `full_powers`

### Power Of Representation (SD-JWT VC)

- **Name**: `Power Of Representation (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.por_sd_jwt_vc`)
- **Asserts**: as the mdoc Power Of Representation above; the claim set is identical.
- **Key fields**: `legal_person_identifier`, `legal_name`, `full_powers`, `eService`, `effective_from_date`, `effective_until_date`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_jurisdiction`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.por_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:por:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### Seafarer (MSO Mdoc)

- **Name**: `Seafarer (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.seafarer_mdoc`)
- **Asserts**: a maritime professional qualification — the capacities the named seafarer may serve in, under an STCW code, countersigned by a named issuing officer.
- **Key fields**: `family_name`, `given_name`, `birth_date`, `issue_date`, `issue_place`, `expiry_date`, `issuing_country`, `issuing_authority`, `issuing_authority_logo`, `document_name`, `document_number`, `portrait`, `capacities`, `family_name_issuing_officer`, `given_name_issuing_officer`, `signature_usual_mark_issuing_officer`, `title_issuing_officer`, `stcw_code`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.seafarer_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.seafarer.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the claim names `capacities` and `stcw_code`. The four `*_issuing_officer` claims are stated and are unusual — this is the only entry in this issuer that names a *human signatory* of the issuing authority as claims within the credential.

### Tax Number (MSO Mdoc)

- **Name**: `Tax Number (MSO Mdoc)` (configuration id `eu.europa.ec.eudi.tax_mdoc`)
- **Asserts**: the holder's tax number in an affiliation country, optionally with a church tax ID and a linked IBAN.
- **Key fields**: `tax_number`, `affiliation_country`, `registered_given_name`, `registered_family_name`, `resident_address`, `birth_date`, `church_tax_ID`, `iban`, `credential_type`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_jurisdiction`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.tax_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`eu.europa.ec.eudi.tax.1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set

### Tax Residency (SD-JWT VC)

- **Name**: `Tax Residency (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.tax_residency_vc_sd_jwt`)
- **Asserts**: that a taxpayer (of a stated taxpayer type) was tax-resident for a requested period under a stated legal framework, per a source-country competent authority.
- **Key fields**: `taxpayer_type`, `name`, `date_of_birth`, `address`, `identification_number`, `legal_framework`, `source_country_competent_authority`, `start_date_of_residency_requested_period`, `end_date_of_residency_requested_period`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.tax_residency_vc_sd_jwt"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:tax:1:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred. Distinct from Tax Number despite sharing the `tax` vct stem — the vct is `urn:eu.europa.ec.eudi:tax:1:1` versus `urn:eu.europa.ec.eudi:tax:1`, and the claim sets do not overlap except on identity. The `taxpayer_type` claim is stated, implying the subject may be other than a natural person.

### Tax Number (SD-JWT VC)

- **Name**: `Tax Number (SD-JWT VC)` (configuration id `eu.europa.ec.eudi.tax_sd_jwt_vc`)
- **Asserts**: as the mdoc Tax Number above; the claim set is identical.
- **Key fields**: `tax_number`, `affiliation_country`, `registered_given_name`, `registered_family_name`, `resident_address`, `birth_date`, `church_tax_ID`, `iban`, `credential_type`, `issuance_date`, `expiry_date`, `issuing_authority`, `issuing_jurisdiction`, `issuing_country`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["eu.europa.ec.eudi.tax_sd_jwt_vc"]`, keys `format` (`dc+sd-jwt`), `vct` (`urn:eu.europa.ec.eudi:tax:1`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, vct, field names); Asserts inferred

### Reservation

- **Name**: `Reservation` (configuration id `org.iso.18013.5.1.reservation_mdoc`)
- **Asserts**: a booking held by the named person with a named service provider — dates, location, guest count, rooms, car rental.
- **Key fields** (all under namespace `org.iso.18013.5.reservation.1`): `booking_service_name`, `reservation_id`, `reservation_date`, `service_provider_name`, `location`, `check_in_date`, `check_out_date`, `guests`, `car_rental`, `num_of_rooms`, `family_name`, `given_name`, `birth_date`
- **Issuee?**: yes
- **Cite**: https://issuer.eudiw.dev/.well-known/openid-credential-issuer — `credential_configurations_supported["org.iso.18013.5.1.reservation_mdoc"]`, keys `format` (`mso_mdoc`), `doctype` (`org.iso.18013.5.1.reservation`), `credential_metadata.display[0].name`, `credential_metadata.claims[*].path`
- **Status**: stated (name, format, doctype, field names); Asserts inferred from the display name and claim set. This is the only entry whose display name carries no format suffix, and the only one whose configuration id is not in the `eu.europa.ec.eudi.*` namespace.

### Observations about this issuer's enumeration as a whole

Fourteen of the 27 configurations are format pairs of the same underlying subject matter (EHIC, Health ID, IBAN, MSISDN, PDA1, Power of Representation, Tax Number) plus the PID trio (mdoc, mdoc-deferred, SD-JWT VC). Counting distinct subject matters rather than configurations gives roughly 18: Certificate of Residence, Diploma, EHIC, Employee ID, Health ID, IBAN, Learning Credential, Loyalty, mDL, MSISDN, PDA1, Photo ID, PID, Power of Representation, Reservation, Seafarer, Tax Number, Tax Residency. That collapse is my count, not the source's — the metadata states 27 configurations and no grouping. Per the task instruction, nothing here is deduped against other sources in the corpus.

## 2. EUDI ARF attestation catalogue

**Provenance and the headline negative finding.** The ARF's published attestation catalogue is much thinner than the issuer above. The ARF repository tree (`https://api.github.com/repos/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/git/trees/main?recursive=1`, HTTP 200) contains exactly two attestation rulebooks under `docs/annexes/annex-3/`: `annex-3.01-pid-rulebook.md` and `annex-3.02-mDL-rulebook.md`. The separate catalogue repository `eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog` (described in the org listing as "Collection of EUDI Wallet rulebooks") likewise contains only `rulebooks/pid/` and `rulebooks/mdl/`, plus `template/attestation-rulebook-template.md` (tree API, HTTP 200). A speculative path `docs/annexes/annex-3/annex-3-attestation-rulebooks.md` returned HTTP 404 and `annex-3.00-attestation-rulebooks.md` returned HTTP 404 — there is no index-of-rulebooks file. **So: as fetched on 2026-09-21, the ARF names PID and mDL as its only concrete attestation types with rulebooks. Everything else is a registration mechanism for rulebooks not yet written.** The entries below are therefore drawn from the two rulebooks, from the ARF's legal-category taxonomy in main chapter 5, and from the defined terms in Annex 1.

### Person Identification Data (PID)

- **Name**: `Person Identification Data (PID)`
- **Asserts**: verbatim — "a set of data that is issued in accordance with Union or national law and that enables the establishment of the identity of a natural or legal person, or of a natural person representing another natural person or a legal person"
- **Key fields**: not stated in the fetched chapter (the attribute list lives in Annex 3.01, the PID Rulebook, which exists at `docs/annexes/annex-3/annex-3.01-pid-rulebook.md` but whose attribute table was not itself fetched). The reference issuer's PID claim list is recorded in §1 above and is a separate artifact.
- **Issuee?**: yes — the ARF states "the subject of all PIDs in the Wallet Unit will be the same person, namely the User of the Wallet Unit", and that "the presence or absence of a valid PID determines whether a Wallet Unit is in the Operational or the Valid state"
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/main/05-data-model-and-data-exchange-protocols.md — §5.2.2 "Person Identification Data (PID)"; rulebook at https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/annexes/annex-3/annex-3.01-pid-rulebook.md
- **Status**: stated (definition quoted verbatim); the absence of a field list here is a fact about what was fetched, not about the rulebook

### Mobile Driving Licence (mDL)

- **Name**: `mDL` — the ARF's Annex 3.02 is titled "mDL Rulebook"
- **Asserts**: not stated as a definition in the fetched chapter; §5.2.1 uses the mDL as its worked example of the legal categories — "an mDL may be issued as a PuB-EAA, a QEAA, or a non-qualified EAA, depending on the legal status of the party issuing mobile driving licences in each Member State"
- **Key fields**: not stated in the fetched material (Annex 3.02 exists but its attribute table was not fetched; the issuer's ISO 18013-5 claim list is in §1 above)
- **Issuee?**: yes (inferred — it is a Wallet Unit attestation about the User)
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/main/05-data-model-and-data-exchange-protocols.md — §5.2.1 Overview; rulebook at https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/annexes/annex-3/annex-3.02-mDL-rulebook.md
- **Status**: stated (that the rulebook exists, and the quoted sentence); Asserts and Issuee inferred

### The four legal categories of attestation

- **Name**: `Person Identification Data (PID)`, `Qualified Electronic Attestation of Attributes (QEAA)`, `Electronic attestation of attributes issued by or on behalf of a public sector body responsible for an authentic source (PuB-EAA)`, `Non-Qualified Electronic Attestation of Attributes (EAA)` — all four verbatim
- **Asserts**: these are not subject-matter types but legal statuses. Verbatim: "the differences between them are purely legal. For example, a diploma may be a QEAA or a non-qualified EAA, depending on whether it is issued by a qualified trust service provider (QTSP) or by an unqualified one." A QEAA is "an electronic attestation of attributes which is issued by a qualified trust service provider (QTSP) and meets the requirements laid down in Annex V"; a PuB-EAA is one "issued by a public sector body that is responsible for an authentic source or by a public sector body that is designated by the Member State to issue such attestations of attributes on behalf of the public sector bodies responsible for authentic sources"; a non-qualified EAA is "an EAA which is not a QEAA or a PuB-EAA".
- **Key fields**: not stated — "From a technical point of view, all PIDs, QEAAs, PuB-EAAs, and EAAs comply with one of the attestation formats listed in Section 5.4"
- **Issuee?**: yes, for all four
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/main/05-data-model-and-data-exchange-protocols.md — §5.2.1 through §5.2.5
- **Status**: stated. Recorded here because it is the axis along which the ARF itself partitions attestations, and it is orthogonal to subject matter — the same credential (a diploma, an mDL) sits in different categories depending on who issued it.

### Wallet Unit Attestation (WUA)

- **Name**: `Wallet Unit Attestation (WUA)`
- **Asserts**: verbatim — "A data object that describes the components of the Wallet Unit or allows authentication and validation of those components." The same entry notes: "The ARF defines two concrete subtypes: the Wallet Instance Attestation (WIA) and the Key Attestation (KA)."
- **Key fields**: not stated in Annex 1
- **Issuee?**: yes, but the subject is a Wallet Unit — software and hardware — not a person. This is the one type in this section whose subject is not a natural or legal person.
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/annexes/annex-1/annex-1-definitions.md — definitions table, "Wallet Unit Attestation (WUA)"
- **Status**: stated (definition quoted verbatim); the observation that its subject is not a person is inferred from that definition

### Wallet Instance Attestation (WIA)

- **Name**: `Wallet Instance Attestation (WIA)`
- **Asserts**: verbatim — "A type of Wallet Unit Attestation that attests the integrity and authenticity of a Wallet Instance, and that carries a revocation reference for the Wallet Instance, as well as information about the Wallet Solution, including its name, version, and certification."
- **Key fields**: stated only in prose — a revocation reference for the Wallet Instance; the Wallet Solution's name, version and certification. No claim identifiers given.
- **Issuee?**: yes — the Wallet Instance
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/annexes/annex-1/annex-1-definitions.md — definitions table, "Wallet Instance Attestation (WIA)"
- **Status**: stated

### Key Attestation (KA)

- **Name**: `Key Attestation (KA)`
- **Asserts**: verbatim — "A type of Wallet Unit Attestation that attests the certification and properties of a WSCA/WSCD or keystore available to the Wallet Unit, and that contains one or more public keys whose corresponding private keys are generated by and stored in that WSCA/WSCD or keystore, as well as a revocation reference for the WSCD or keystore."
- **Key fields**: stated only in prose — one or more public keys; a revocation reference for the WSCD or keystore. No claim identifiers given.
- **Issuee?**: yes — the subject is a secure cryptographic device or keystore
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/annexes/annex-1/annex-1-definitions.md — definitions table, "Key Attestation (KA)"
- **Status**: stated

### Pseudonym

- **Name**: `Pseudonym`
- **Asserts**: verbatim — "Data uniquely representing a User which in itself does not allow to infer the User's attributes or person identification data, without the use of additional information that is kept separately by the issuer of the data uniquely representing the user."
- **Key fields**: not stated
- **Issuee?**: yes — it uniquely represents a User
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/annexes/annex-1/annex-1-definitions.md — definitions table, "Pseudonym"
- **Status**: stated. Recorded because it is a zero-attribute holder artifact — the limiting case of a credential that asserts identity continuity and nothing else.

### Wallet-relying party registration certificate

- **Name**: `(Wallet-relying party) registration certificate`
- **Asserts**: verbatim — "A data object that indicates the attributes the wallet-relying party has registered to intend to request from Users"
- **Key fields**: not stated
- **Issuee?**: yes — the issuee is a *verifier*, not a wallet holder. The accompanying definition names the issuer: "Provider of (wallet-relying party) registration certificates | A natural or legal person mandated by a Member State to issue wallet-relying party registration certificates to wallet-relying parties registered in that Member State".
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/annexes/annex-1/annex-1-definitions.md — definitions table, "(Wallet-relying party) registration certificate" and "Provider of (wallet-relying party) registration certificates"
- **Status**: stated. Recorded because it inverts the usual direction — a credential held by the party doing the asking, constraining what it may ask for.

### Catalogue of attributes / catalogue of schemes for the attestation of attributes

- **Name**: `catalogue of attributes` and `catalogue of schemes for the attestation of attributes` — these are registries, not credential types, and are recorded here only to document why the ARF's attestation catalogue is currently near-empty
- **Asserts**: verbatim from the ARF discussion paper — "**Scheme for the attestation of attributes** is a machine-readable attestation definition" and "**Attestation Rulebook** is a human-readable specification of the scheme for the attestation of attributes". The paper further states: "the catalogue of attributes is limited to attributes that rely on authentic sources within the public sector, with its primary objective being the discovery of verification points [...] In contrast, the catalogue of schemes for the attestation of attributes has a broader scope, as it allows any scheme owner to register their attestation scheme."
- **Key fields**: the paper states the minimum parameters of a registration request, including "a namespace for the identifier of the attributes", "an identifier of the attribute, unique within the namespace, and the version of the attribute", "semantic description of the attribute", "the data type of the attribute", and for a scheme "the format or formats of electronic attestation of attributes within the scope of the scheme"
- **Issuee?**: not applicable
- **Cite**: https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/discussion-topics/o-catalogues-for-attestations.md — "Topic O - Catalogues for Attestations", version 1.0 updated 29 Sep 2025, §2 and §2.1; GitHub discussion linked from the document at https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/discussions/557
- **Status**: stated. The paper also states that the existing ARF requirements for these catalogues "are considered outdated and will be updated", and lists CAT_01 through CAT_10 for removal — so the catalogue design was in flux as of that document's date.

## 3. The First Person Project (Medium article, and the project's own white-paper page)

**Provenance, including a partial fetch failure.** The Medium article at `https://medium.com/@glinznews/the-first-person-project-redefining-digital-identity-in-an-ai-dominated-world-28e35afe73c9` returned **HTTP 403 Forbidden** to direct `curl` (both with a browser user-agent and with a Googlebot user-agent) and to WebFetch. The full article text was retrieved instead through the public reader proxy `https://r.jina.ai/<url>` (HTTP 200, 11,472 bytes), which returns the article body as markdown with the title, canonical URL, and a published time of 2025-07-03T10:48:09Z. **Everything quoted in §3a below is from that proxied retrieval, not from medium.com directly** — the content is consistent and coherent but I did not see it rendered by Medium itself, and a reader should know that. §3b is separately sourced from the project's own site, fetched directly.

### 3a. Credential types named in the Medium article

#### First Person Credentials

- **Name**: `First Person Credentials`
- **Asserts**: verbatim — they are "built on **Decentralized Identifiers (DIDs)** and **Verifiable Relationship Credentials (VRCs)** — providing cryptographic proof of genuine personal trust relationships", and the technologies together "enable individuals to prove their humanity and establish trust without relying on centralized authorities or surrendering personal data"
- **Key fields**: not stated
- **Issuee?**: yes — an individual. Verbatim: "First Person Credentials operate through a sophisticated system of personal attestations, where individuals vouch for their relationships with others, creating a decentralized network of trust."
- **Cite**: https://medium.com/@glinznews/the-first-person-project-redefining-digital-identity-in-an-ai-dominated-world-28e35afe73c9 (retrieved via https://r.jina.ai/) — paragraphs 3 ("In the context of first-person identity…") and the "Technical Architecture and Implementation" section
- **Status**: stated

#### Verifiable Relationship Credentials (VRCs)

- **Name**: `Verifiable Relationship Credentials (VRCs)`
- **Asserts**: verbatim — "Verifiable Relationship Credentials (VRCs) create cryptographic proofs of authentic human connections"
- **Key fields**: not stated
- **Issuee?**: yes, and the issuer is a peer rather than an institution — "individuals vouch for their relationships with others"
- **Cite**: https://medium.com/@glinznews/the-first-person-project-redefining-digital-identity-in-an-ai-dominated-world-28e35afe73c9 (retrieved via https://r.jina.ai/) — "Technical Architecture and Implementation" section, and paragraph 3
- **Status**: stated

#### Proof of personhood (the capability the above are for)

- **Name**: `proof-of-personhood` (the article's own hyphenation; it also writes "proof-of-personhood solution" and "proof-of-personhood systems")
- **Asserts**: the article frames this as the problem, not a credential — "the **First Person Project**, which offers a groundbreaking approach to solving the 'proof-of-personhood' challenge in our increasingly AI-dominated digital landscape", and "the ability to distinguish between real people and bots presents critical threats to digital democracy and authentic human discourse"
- **Key fields**: not fields, but stated *criteria*, verbatim: "Any effective proof-of-personhood solution must satisfy several essential criteria: it must be **tangible** (grounded in real-world interactions that are difficult to fabricate), **usable** (with an intuitive interface design that doesn't burden users), **useful** (addressing genuine problems that people actually face), **portable** (functioning across various platforms and services), **contextual** (providing appropriate verification levels for different use cases), and **actionable** (enabling concrete decisions and protective measures)."
- **Issuee?**: not applicable — this is a property to be proved, not a named credential in the article
- **Cite**: https://medium.com/@glinznews/the-first-person-project-redefining-digital-identity-in-an-ai-dominated-world-28e35afe73c9 (retrieved via https://r.jina.ai/) — paragraph 2, "The Escalating Crisis of Digital Trust", and the criteria list in "Technical Architecture and Implementation"
- **Status**: stated. The contextual criterion — "providing appropriate verification levels for different use cases" — is the article's only gesture at personhood assurance being graded rather than binary.

#### Comparator identity systems named in passing

- **Name**: `World (formerly Worldcoin)`, `Switzerland's e-ID / SWIYU`, `The European Union's Digital Identity Wallet framework`, `government-issued digital IDs`, `knowledge-based authentication`, `hardware security keys`
- **Asserts**: World is described as one of the "centralized biometric systems [...] which rely on iris scanning and global databases"; SWIYU as a "self-sovereign identity (SSI) model" reached after "voters rejected a 2021 proposal involving private companies over privacy concerns"; the EU wallet as taking "a different approach, emphasizing user control and interoperability while maintaining regulatory oversight"; and the last three appear only in the list "Other alternatives, such as government-issued digital IDs, knowledge-based authentication, and hardware security keys, each offer different trade-offs between security, privacy, usability, and scalability."
- **Key fields**: not stated for any of them
- **Issuee?**: unknown — the article says nothing about the structure of any of them
- **Cite**: https://medium.com/@glinznews/the-first-person-project-redefining-digital-identity-in-an-ai-dominated-world-28e35afe73c9 (retrieved via https://r.jina.ai/) — paragraph 3, "Global Policy Implications and Regulatory Landscape", and "Comparative Analysis with Existing Solutions". The article links https://www.eid.admin.ch/en/swiyu-e for SWIYU and https://vitalik.eth.limo/general/2023/07/24/biometric.html for Buterin's "pluralistic identity" argument.
- **Status**: stated that the article names these; they are named as comparators, not defined as credential types, so treat them as pointers rather than entries

**Not a credential, recorded to prevent a miscategorisation**: the article names `Decentralized Identifiers (DIDs)` repeatedly, but as infrastructure — "Decentralized Identifiers (DIDs) provide the technical infrastructure for self-sovereign identity management". An identifier is not an attestation.

### 3b. Credential types named on the First Person Network's own white-paper page

**Provenance.** The article's closing paragraph links "website placeholder" to `https://www.firstperson.network/`. That landing page fetched HTTP 200 but renders entirely from JavaScript — stripping tags yields zero text — so it carries nothing. Its `/white-paper` page fetched HTTP 200 and *does* render server-side; the executive summary below is from that page's own text. This is a different source from the Medium article and is cited as such. The full 80-page white paper itself (linked from that page as a Google Doc and a ~12 MB PDF) was **not** fetched, so nothing below comes from the paper's body.

#### Personhood credentials (PHCs)

- **Name**: `Personhood credentials`, abbreviated `PHCs` on the same page
- **Asserts**: verbatim — "Personhood credentials are issued by any ecosystem (any qualified entity such as a company, university, nonprofit community, government, etc.) who can attest to the credential holder being a real unique person within that ecosystem."
- **Key fields**: not stated
- **Issuee?**: yes — a natural person, called "the credential holder". The issuer is explicitly open-ended: "any qualified entity such as a company, university, nonprofit community, government, etc."
- **Cite**: https://www.firstperson.network/white-paper — Executive Summary, "What is the First Person Project?"; the abbreviation PHC appears in the "Proof of Personhood" overview panel on the same page
- **Status**: stated. Note the scoping clause "within that ecosystem" — the assertion is uniqueness relative to an issuing community, not globally.

#### Verifiable relationship credentials (VRCs)

- **Name**: `Verifiable relationship credentials`, abbreviated `VRCs` on the same page
- **Asserts**: verbatim — "Verifiable relationship credentials are issued peer-to-peer between holders of personhood credentials in order to attest to verifiable first-person trust relationships."
- **Key fields**: not stated
- **Issuee?**: yes — another natural person. This entry states a *precondition on both parties*: both issuer and issuee must already hold personhood credentials.
- **Cite**: https://www.firstperson.network/white-paper — Executive Summary, "What is the First Person Project?"
- **Status**: stated

#### First Person credentials (the umbrella term)

- **Name**: `First Person credentials`
- **Asserts**: verbatim — "These First Person credentials can be stored in any compatible digital wallet and presented to any party who needs proof that the credential holder is a real unique human." Stated properties: "Decentralized, i.e., there is no centralized database of First Person credential holders (or their biometrics). First Person credentials are stored only in the digital wallets of the individuals to whom they are issued (and any biometrics are local to those devices)." And: "Privacy-preserving, i.e., First Person credentials can provide strong zero-knowledge proof verification that you are a real person without requiring you to share any personal data or be tracked in any type of global biometric database."
- **Key fields**: not stated
- **Issuee?**: yes — a natural person
- **Cite**: https://www.firstperson.network/white-paper — Executive Summary
- **Status**: stated. The term is the union of PHCs and VRCs, per "two new types of verifiable digital credentials" introduced immediately before it.

#### First Person Certified AI agents

- **Name**: `First Person Certified AI agents`
- **Asserts**: the page poses the question and names this as the answer, verbatim — "The biggest leverage point is the fundamental trust issue with personal AI agents: who do they work for? The compelling answer to that question: First Person Certified AI agents." Elsewhere: the network provides "not just privacy-preserving proof of personhood, but also the tools needed for individuals to safely delegate to personal AI agents".
- **Key fields**: not stated
- **Issuee?**: yes — an AI agent, with a natural person as the delegating principal. This is the inverse of proof of personhood: a credential whose subject is explicitly *not* human and which binds that non-human to a human.
- **Cite**: https://www.firstperson.network/white-paper — "First Person AI Agents" overview panel, and the Executive Summary's reference to Part Eight
- **Status**: stated that the term is used and what question it answers; it is not given a structural definition on this page, and the characterisation as a delegation credential is inferred from the two quoted sentences. The detail is said to live in Part Eight of the full paper, which was not fetched.

#### Stated deployment context, which bears on what a personhood credential is for

- The page gives a named worked case, verbatim: "He showed an example of how the combination of personhood credentials (issued by the Linux Foundation or a relevant employer) and verifiable relationship credentials (issued by project contributors to each other as they meet each other in person) would have prevented 'Jia Tan' from ever obtaining maintainer rights to XZ utils." This states the issuer for PHCs in that case (a foundation or an employer) and the issuance event for VRCs (meeting in person).
- Also stated: the project is "a collaboration between Linux Foundation Decentralized Trust (LFDT), Ayra Association, Trust Over IP (ToIP), Decentralized Identity Foundation (DIF), and OpenWallet Foundation (OWF)", that standardisation is by the "Decentralized Trust Graph Working Group", and that the intended governing body is the "First Person Cooperative (FPC)". The collection of all issuers and holders is called a "decentralized trust graph".
- **Cite**: https://www.firstperson.network/white-paper — "Why is the Linux Foundation 'customer #1' for FPP?" and the Executive Summary
- **Status**: stated

## from-memory-UNVERIFIED

Nothing in this section was fetched. It is recorded separately because it is training-memory recall that may be stale or wrong, and it must not be mixed with the material above.

- I have a recollection that the EUDI ARF ecosystem includes or has discussed additional attestation types not found in the fetches above — among them a **Wallet Trust Evidence (WTE)** artifact and an **age-verification attestation / proof-of-age** credential. The ARF Annex 1 definitions I actually fetched contain WUA, WIA and KA but **no** WTE entry, so either the term was renamed (WUA/WIA/KA look like a successor naming) or my recollection is wrong. Treat as unverified. Separately, I observed during the fetch that the `eu-digital-identity-wallet` GitHub org contains a repository `av-doc-technical-specification`, described in the org listing as "European Age Verification solution documentation" — that description **is** a fetched fact (https://api.github.com/orgs/eu-digital-identity-wallet/repos), but I did not open the repository, so nothing about what credential type it defines is verified here. It is the obvious next fetch for anyone extending this file.
- I believe the ISO/IEC 18013-5 mDL specification defines age-attestation claims of the form `age_over_NN` for arbitrary NN, of which `age_over_18` is one instance. The issuer metadata above states only `age_over_18`, `age_in_years` and `age_birth_year`. The generalisation is unverified.
- I believe OpenID4VCI's earlier drafts used the format identifier `vc+sd-jwt` and that this was renamed to `dc+sd-jwt` in later drafts. The issuer metadata fetched above uses `dc+sd-jwt` exclusively, which is a fetched fact; the history behind the rename is memory and unverified.
