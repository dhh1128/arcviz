# Urtext / critical-edition bracket conventions for editorial additions

Status: general convention well-corroborated across multiple secondary/scholarly sources; one
primary-ish source (a published early-music edition project's own editorial-principles page,
fetched via search snippet only — direct WebFetch of that URL timed out twice). Retrieved
2026-09-14.

## The convention

Across text-critical and musical scholarly editing alike, square brackets `[ ]` are the
near-universal marker for "not in the source, supplied by the editor." Distinct from parentheses
`( )`, which composers themselves use inside their own text, so brackets are reserved for the
editor's voice to avoid ambiguity.

Henle Verlag's own explanation of Urtext principle (fetched directly, https://www.henle.de/us/navigation/4bce7ec22c714fe58b0d2c0ed21757ab):
> "The most important observations and editorial decisions are elucidated in the preface, in the
> critical commentary, in footnotes, or by being marked as such in the musical text."

This is Henle's general statement of the principle (mark editorial decisions as editorial); the
page does not spell out the specific bracket glyph convention (that lives in each edition's own
preface/"Bemerkungen," which I did not have access to for a specific work in this pass — flagged
as a gap, not fabricated).

A concrete, citable specific-edition example of the bracket convention in practice, from a
published early-music scholarly edition project (Lost and Found, hosted by FCSH/NOVA University
Lisbon), editorial-principles page (https://lostandfound.fcsh.unl.pt/editorial-principles —
content below captured via WebSearch snippet; direct WebFetch of the page timed out twice and
could not be independently re-verified in this pass):

> "If voices are not named in the source, suitable names in square brackets are provided by the
> editor." / "Missing portions of music and other notational elements editorially reconstructed
> are placed in square brackets." / "Editorial, implied, and cautionary accidentals are placed
> above the notes concerned."

James Grier, "Editing," *Grove Music Online* / Oxford Music Online (2001, updated 2014),
DOI 10.1093/gmo/9781561592630.article.08550 — a standard reference musicology article on
editorial method — states the parallel ethical hazard to Brandi's "creative conservation" ban,
regarding conjectural emendation of a corrupt/ambiguous reading:

> "the opposite extreme, the temptation to improve on the composer, holds equal danger. An
> editor should not be open to the charge of printing the piece the composer would have written
> had he or she known as much as the editor."

This is the musicological mirror of Brandi's principle 1 ("the unacceptability of creative
conservation... a conservator must never attempt to substitute the artist" — see
`conservation-brandi-principles.md`): both fields independently arrived at "the completer's
knowledge must not silently pass as the original creator's."

## Gap flagged

I was not able to pull a specific Bärenreiter or Henle *edition preface* (as opposed to their
general marketing/FAQ pages) showing the exact bracket/dashed-slur legend for one named work.
The general convention (square brackets = editorial addition) is extremely well corroborated
across independent sources including music-notation software documentation (MuseScore forum:
"the standard method of indicating editorial additions and changes in a score is to enclose them
within square brackets") but a specific publisher's exact typographic legend for a specific
edition remains a lead, not a verified quote, in this capture.

## Source records

- key: henle-what-is-urtext
  title: "What is Urtext"
  author/body: G. Henle Verlag
  url: https://www.henle.de/us/navigation/4bce7ec22c714fe58b0d2c0ed21757ab
  retrieved: 2026-09-14
  status: primary (publisher's own statement of editorial principle)
  quote: "The most important observations and editorial decisions are elucidated in the preface, in the critical commentary, in footnotes, or by being marked as such in the musical text."
  locator: page body, "What is Urtext" section

- key: lostandfound-editorial-principles
  title: "Editorial Principles"
  author/body: Lost and Found (early-music edition project), FCSH/NOVA University Lisbon
  url: https://lostandfound.fcsh.unl.pt/editorial-principles
  retrieved: 2026-09-14
  status: lead (content only seen via WebSearch snippet; direct WebFetch timed out twice, not independently re-verified against the live page in this session)
  quote: "Missing portions of music and other notational elements editorially reconstructed are placed in square brackets."

- key: grier-editing-grove
  title: "Editing"
  author: James Grier
  venue: Grove Music Online / Oxford Music Online, published 2001-01-20, updated 2014-01-31
  url: https://doi.org/10.1093/gmo/9781561592630.article.08550 (fetched via mirror PDF at https://openeclass.uom.gr/modules/document/file.php/UNI339/Grier-Editing%20OMO%202014.pdf)
  retrieved: 2026-09-14
  status: primary (standard reference musicology encyclopedia article, full text pdftotext-extracted and grepped directly)
  quote: "the opposite extreme, the temptation to improve on the composer, holds equal danger. An editor should not be open to the charge of printing the piece the composer would have written had he or she known as much as the editor."
  locator: pdftotext extraction, line ~547-549 (article body, section on establishing readings/emendation)
