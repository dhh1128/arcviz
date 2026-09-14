# Design principle and known limits of the Leiden Conventions

Retrieved 2026-09-14.

## The design principle, in the sources' own words

Sterling Dow states the objective directly (Dow 1969, "General Definition of Objectives",
`leiden-dow-conventions-in-editing-full-ocr.txt` lines 280–284): "The aim of good editing is to
set forth in print, by use of regular, understood, agreed-upon conventions, which shall be as
simple and clear as possible... a clear and correct representation of the original text." The
whole apparatus exists so a reader can tell, mark by mark, which category of confidence a given
letter belongs to — never so an editor's best guess can be typographically indistinguishable from
what the stone/papyrus actually preserves. This is explicit in several of the individual rules
already captured in `leiden-symbol-table.md`:
- Restorations must be bracket-delimited and never contain a letter that is actually visible:
  "No detectable stroke of a letter should be enclosed within square brackets" (line 412) — i.e.
  the boundary between "attested" and "conjectured" is drawn at the level of the individual
  letter, not the line or the document.
- The subscript dot must never appear inside a restoration bracket, because that would collapse
  two different kinds of doubt into one mark: "No letter between brackets... should be dotted...
  A dotted letter within square brackets would naturally be taken to mean not 'reading doubtful'
  but 'restoration doubtful'" (lines 498–502) — the convention actively defends against exactly
  the failure mode arcviz is worried about: one notation being misread as covering two different
  epistemic situations.
- Deliberate blank space (vacat) is kept typographically distinct from a lacuna, so "nothing was
  ever written here" cannot be mistaken for "something was written here and is now lost" — see
  the vacat vs. lacuna entries in `leiden-symbol-table.md`.

EpiDoc's own framing (quoted in `leiden-epidoc-and-codification.md`) makes the same point at the
encoding level: it exists to record "textual interventions [such] as an editor's supplement for
characters wholly lost to damage" as a distinct, taggable category from the transcribed text
itself, so that downstream renderers/readers cannot silently flatten "editor's guess" into "what
the document says."

## Known critiques / documented failure modes

All of the following are sourced, not inferred:

1. **Requires a trained reader.** TEI's own guidance (Mahoney, https://tei-c.org/Vault/ETE/Preview/mahoney.html,
   fetched 2026-09-14) states plainly: "the Leiden convention is neither universal nor flawless...
   any given book may or may not include a key to its particular markup system, so readers must
   become aware of different publishers' preferred styles." A reader unfamiliar with a given
   journal's house variant cannot decode the marks from the marks alone.
2. **Simplification for non-specialists strips the distinctions that matter.** Same source:
   "because a fully-marked text can be cumbersome to read, some publications omit the more
   complicated markings — especially in texts intended for beginners and students." This is a
   direct precedent for "a UI that hides the hard states to stay readable" as a known, documented
   failure mode, not a hypothetical one.
3. **A single glyph has carried conflicting meanings across time/sub-discipline.** Documented in
   Dow (see `leiden-symbol-table.md`, "documented internal ambiguity" section): angle brackets
   flipped meaning (delete → add) around 1932 and still do at least three distinct jobs depending
   on convention/date, disambiguated only by the editor's prose commentary, not by the mark
   itself. Dow's own verdict: "in all of the above instances except restorations and
   abbreviations, the critical apparatus ought to state the facts clearly. There is no other way
   to insure clarity of understanding" (lines 790–792) — i.e. even the system's own primary
   codifier concedes the notation alone is sometimes not self-sufficient and needs an out-of-band
   explanation.
4. **Editorial judgment is presented with the same typographic weight regardless of how contested
   it is.** Dow, discussing restoration inside square brackets generally (lines 262–270): in
   Classical epigraphy there is "increasing pressure of conviction that restorations should no
   longer be freely inserted in texts to express the editor's subjective... conjectures; but
   rather that restorations should be rigidly controlled by specifiable evidence" — i.e.
   practitioners themselves have flagged that a bracket doesn't distinguish a rigorously
   evidenced restoration from a speculative one; Dow proposes (but the field never fully adopted)
   a "small interrogation point" for restorations that are merely probable rather than certain
   (line 415, "For a proposal to designate restorations that are probable but not certain by a
   small interrogation point, see Chapter IV").
5. **Digital rendering is not solved by the print convention as-is.** This is why EpiDoc/Leiden+
   exist at all — encoding secondary sources describe the print convention as not directly
   machine-checkable or uniformly renderable across fonts/systems, which is what motivated moving
   the semantic distinctions into TEI XML attributes (`reason`, `quantity`, `extent`) rather than
   relying on bracket glyphs alone (see `leiden-epidoc-and-codification.md`).

## Sources
- TEI "Epigraphy" (Mahoney): https://tei-c.org/Vault/ETE/Preview/mahoney.html — secondary,
  fetched 2026-09-14.
- Sterling Dow, *Conventions in Editing* (Duke, 1969) — see `leiden-symbol-table.md` for full
  citation; capture: `leiden-dow-conventions-in-editing-full-ocr.txt`.
- EpiDoc Guidelines 9.8, intro: https://epidoc.stoa.org/gl/latest/intro-intro.html — fetched
  2026-09-14.
