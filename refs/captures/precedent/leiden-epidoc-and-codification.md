# Who codifies Leiden today, and how it maps to a digital/machine-checkable form

Retrieved 2026-09-14.

## EpiDoc — the live, codified, machine-checkable descendant

- **What**: EpiDoc is a TEI-XML-based standard for encoding epigraphic and papyrological
  documents, maintained as an open community project (originally proposed 2000 by Tom Elliott,
  with Hugh Cayless and Amy Hawkins, at UNC Chapel Hill, in response to a call for open standards
  from the electronic-publication committee of the Association Internationale d'Épigraphie
  Grecque et Latine).
- **Current version at capture time**: EpiDoc Guidelines 9.8. Home: https://epidoc.stoa.org/
  Guidelines entry point: https://epidoc.stoa.org/gl/latest/ ; intro:
  https://epidoc.stoa.org/gl/latest/intro-intro.html
- **Explicit statement of the Leiden relationship** (quoted from the Guidelines' own intro
  section, via WebFetch of https://epidoc.stoa.org/gl/latest/intro-intro.html, retrieved
  2026-09-14): "The EpiDoc Guidelines are intended to complement the Leiden Conventions
  (hereafter 'Leiden'), which have been in use in epigraphy and papyrology for over 80 years and
  are understood in many philological and documentary fields." EpiDoc "does not mandate
  reproducing Leiden's specific typographical symbols in the XML itself... [it] base[s] their
  recommendations and examples upon these [Leiden] distinctions without requiring the specific
  typographical conventions and sigla recommended therein." The default EpiDoc Example
  Stylesheets *do* still render Leiden-style brackets/dots for human readers, i.e. Leiden notation
  is the display layer, EpiDoc/TEI is the semantic-encoding layer underneath it.
- **Machine-checkable structure — the `<gap>` element** (TEI element, used per EpiDoc's own
  guidance pages; retrieved via WebSearch/WebFetch of the EpiDoc guideline pages
  `trans-lostcharknown.html`, `trans-lostcharapprox.html`, `trans-lostcharunknown.html`,
  2026-09-14): a lacuna is marked with `<gap>`, carrying attributes:
  - `reason` — why the material is missing (commonly `"lost"` for a lacuna on the physical
    support, or `"illegible"`).
  - `quantity` + `unit` — used **when the number of missing units is known** (e.g.
    `<gap reason="lost" quantity="5" unit="character"/>`).
  - `extent="unknown"` — used **instead of `quantity`** precisely when the amount lost is *not*
    known: "in the case of an unknown number of characters being lost we use extent: extent with
    a value of 'unknown' denotes the fact that it is not possible to determine how many characters
    have been lost."
  - `atLeast` / `atMost` — for a bounded but imprecise range.
  This is the direct machine-readable analogue of Dow's `[- - -]` (unknown length) vs.
  `[- ca. 5 -]` (approximate length) vs. a bracket with a definite restored letter-count — i.e.
  the convention distinguishes, at the schema level, "we know exactly what's missing," "we know
  roughly how much is missing," and "we don't even know the extent," as three separate encodable
  states, not just three separate typographic habits.

## Leiden+ — the papyrological digital transcription syntax

- **What**: a "tag-lite" plain-text markup syntax, developed by the Integrating Digital Papyrology
  project, that lets a human type something that *looks like* Leiden notation directly into the
  Papyrological Editor at papyri.info, which is then mechanically translated (via an XSugar
  grammar) into full EpiDoc/TEI XML and back. Purpose, per secondary description found via
  WebSearch: to let non-specialists (of XML) produce valid EpiDoc encodings without hand-writing
  XML, while preserving Leiden's visual/semantic distinctions.
- **Status of primary source**: I could not retrieve the actual Leiden+ documentation page.
  `https://papyri.info/docs/leiden_plus` returned an anti-bot ("Anubis") interstitial refusing
  automated fetch. This is a **lead, not verified** — the description above is reconstructed from
  secondary pages (Digital Classicist wiki "Leiden-plus", ENCODE Guidelines' Leiden+ page) that
  themselves point at, but do not reproduce, the primary documentation. Do not cite Leiden+'s
  symbol table as verified; only its existence and general purpose are corroborated by more than
  one secondary source.
- Digital Classicist wiki: https://wiki.digitalclassicist.org/Leiden-plus (secondary, overview
  only, fetched 2026-09-14).
- ENCODE Guidelines: https://encode-guidelines.github.io/guidelines/leiden+/ (secondary, overview
  only, fetched 2026-09-14, points at the same inaccessible papyri.info page for the actual table).

## Who "owns" the standard today — summary

There is no single legal/formal standards body (no ISO-style committee). Codification today is
de facto distributed across three live projects, all citing Leiden as their common ancestor:
1. **EpiDoc** (community guidelines + TEI schema + reference stylesheets) — the closest thing to
   a maintained, versioned, machine-checkable spec. Governance appears to be an open community
   (per TEIWiki/Wikipedia secondary descriptions), not a formal standards organization.
2. **Duke Databank of Documentary Papyri / papyri.info** (Leiden+ syntax + Papyrological Editor)
   — the operational tool most working papyrologists actually type into.
3. Individual discipline style-sheets (e.g. *Supplementum Epigraphicum Graecum*'s own house
   conventions) that adapt Leiden with local variations — evidence the convention is not
   perfectly uniform even today (see the "documented internal ambiguity" note in
   `leiden-symbol-table.md`).
