# Leiden Conventions — symbol table (verified against primary/authoritative sources)

Retrieved 2026-09-14.

## Status of sources

- **Primary-adjacent, verified in full**: Sterling Dow, *Conventions in Editing: A Suggested
  Reformulation of the Leiden System*, Greek Roman and Byzantine Scholarly Aids no. 2 (Duke
  University, 1969). This is not the 1931/32 Leiden proceedings themselves (those are apparently
  out of print / not found online — see "Unverified" below) but the standard English-language
  critical restatement of them, written by a Harvard epigrapher, published by Duke, and cited as
  authoritative by later sources (EpiDoc, TEI). Fetched as PDF from
  `https://grbs.library.duke.edu/public/journals/11/grbs-supplemental-files/Conventions.pdf`,
  OCR'd with `pdftotext`, full text saved to
  `leiden-dow-conventions-in-editing-full-ocr.txt` in this directory. Section/page numbers below
  refer to that document's own pagination (printed page numbers appear in the OCR near each
  section).
- **Secondary, corroborating**: TEI "Epigraphy" guidance page (Mahoney), EpiDoc Guidelines 9.8,
  Wikipedia "Leiden Conventions".
- **Unverified / lead only**: the actual 1931/32 proceedings (U. Wilcken, "Das Leydener
  Klammersystem," *Archiv für Papyrusforschung* 10 (1932) 211–212; B.A. van Groningen, "Projet
  d'unification des systèmes de signes critiques," *Chronique d'Égypte* 7 (1932) 262–269; the
  Union Académique Internationale's official 1932/1938 booklet). These are cited by Dow's own
  bibliography (p.14 of his text) but I could not reach digitized copies — French/German journals
  from the 1930s, not online in the search results. Treat any claim about the *exact* original 1931
  wording as resting on Dow's 1969 restatement, one step removed.

## The symbol table (from Dow, 1969)

Quotes below are verbatim from the OCR (OCR has some scanning noise, e.g. Greek letters garbled
and stray characters; brackets/angle-bracket glyphs are reproduced as best the OCR captured them —
cross-check the PDF for anything load-bearing).

| Notation | Name (Dow's heading) | Meaning | Quote / locator |
|---|---|---|---|
| `[ ]` square brackets | Restorations | "Square brackets enclose areas once inscribed, whether the stone is: (a) preserved but with the surface too worn or eroded to retain actual strokes of letters... or (b) preserved behind the original front surface, itself now missing... or (c) entirely broken away." Rule: "In any formal text... every square bracket should be answered by another square bracket." Rule: "No detectable stroke of a letter should be enclosed within square brackets." | §"The Use of Editorial Signs — Restorations: Square Brackets `[ ]`", full-ocr lines 394–415 |
| `[- - -]` or `[- ca.5 -]` dashes inside brackets | Lacunae of uncertain/estimated length | "A dash or dashes should be used solely to indicate a lacuna of uncertain length. The lacuna should be marked also by square brackets... `[- - -]` can mean a few; or many; or an indefinite number[ ] of letters missing." An estimate can be given: "if an estimate, though inexact, would be useful, print `[- ca. 5 -]`." | §"Lacunae: Dashes, Dots", lines 417–426 |
| superscript `vac.` or `vacat`, with a number | Intentional blank left by the letterer | Distinguishes space **deliberately** left blank by the mason from a lacuna (space where letters were once present and are now lost/illegible). "If a small number of spaces are left blank, print one for each blank space... If the blank space is lengthy: `vacat. 20` where the space can be accurately measured... `vacat.` where the space cannot be measured; or is indefinitely large." Restorable: "`[vac.]` one space is considered by the editor to have been left blank, but the surface is not preserved sufficiently so that the matter can be determined by the stone itself." | §"Spaces Left Blank by the Letterer", lines 446–484 |
| subscript dot (underdot) under a letter | Doubtful reading | "A subscript dot should be placed under any letter which as a whole is so dim that, in isolation, neither the letter as a whole, nor any stroke of it, could be positively read. A subscript dot should be placed under any letter of which a stroke or strokes are clear, but do not suffice to determine what the letter would be in isolation." Explicit rule against conflating with restoration: "No letter between brackets, except doubtful letters in erasures... should be dotted" — a dotted letter *inside* brackets would wrongly read as "restoration doubtful" rather than "reading doubtful." | §"Doubtful Readings: Subscript Dots", lines 488–528 |
| shading (typographic) | Attrition, letter-shape ambiguity | "Where the surface is in a condition such that it appears to have been inscribed, but attrition has made the existence of inscribed letters doubtful, shading will convey a correct notion." Used e.g. where a letter's rounded middle could be Θ or Ο. | §"Attrition: Shading", lines 511–534 |
| `⟦ ⟧` double square brackets, letters shown | Ancient erasure, still legible | "indicate a rasura... Indicating an area containing the letters shown within the brackets, which were the only letters ever inscribed in the area, and which were evidently intended to be erased, but can still be positively read." | §"Rasurae: Double Square Brackets", lines 540–585 |
| `⟦- - -⟧` double brackets around dashes | Ancient erasure, illegible, editor restores nothing | "Indicating erased areas of lengths — as shown, where no letter can be read and where the editor restores nothing." | lines 540–553 |
| `⟦[...]⟧` double brackets nested with square brackets | Ancient erasure, editor conjectures the erased content | "Indicating that the editor restores an erasure and the letters conjectured to have been erased." Flagged by Dow as rare/cumbersome but a real, distinct category. | lines 630–632 |
| plain (non-italic) capital letters | Reading certain, sense/interpretation unknown | "Whole capital letters are used... to designate letters which individually are legible (or partially legible and if so dotted) but which collectively do not appear to the editor to make sense." | §"Reading Clear, Interpretation Unknown: Capital Letters", lines 646–671 |
| broken/partial capital letters | Stroke visible, letter identity unknown | "Partial, or broken, capital letters are used... where... the context does not decide the identity of the (imperfectly preserved) letter." | §"Strokes Clear, Letters Unknown: Broken Capitals", lines 685–702 |
| underlining | Letters read by an earlier editor, now lost from the object | "the use of underlining — to indicate letters read with certainty in earlier editions but now missing (usually because of the breaking-away of parts of the stone at the edges)." A second-hand attestation state: was directly observed once, is not directly observable now. | §"Parts Read Earlier, Now Missing: Underlining", lines 703–719 |
| `⟨ ⟩` angle/pointed brackets | (a) Editor's addition for scribal omission | "Letters... inserted by the editor to supply letters... considered by him to have been intended to be inscribed, but which were omitted by error." | §"Additions by the Editor: Pointed Brackets", lines 673–683 |
| `⟨ ⟩` angle/pointed brackets | (b) Editor's substitution for an erroneous letter | "Enclosing letters... substituted by the editor for letters... actually inscribed, but considered by him to have been inscribed by error, instead of the (correct) letters given within the pointed brackets." | §"Substitutions by the Editor: Pointed Brackets", lines 721–729 |
| `⟨ ⟩` angle/pointed brackets | (c) Letter mechanically left incomplete by the mason | "parts of letters were sometimes never cut... strictly `⟨A⟩` should be printed" when intent is clear but the stroke is physically incomplete (as opposed to a doubtful reading, which takes a dot). | §"Letters Left Incomplete by the Letterer", lines 733–741 |
| `{ }` braces | Editorial deletion/suppression | "Enclosing letters... considered by the editor not to have been intended to be inscribed, but inscribed by error." | §"Suppressions by the Editor: Braces", lines 742–751 |
| `( )` parentheses | Resolution of abbreviation/ligature | "Indicating letters added by the editor to fill out an abbreviation to the full form of the word... also to give the full form of an abbreviation inscribed as a ligature." | §"Resolutions of Abbreviations and Ligatures: Parentheses", lines 757–777 |

## Documented internal ambiguity (a real, sourced weakness — not my inference)

Dow flags that the single sign `⟨ ⟩` was retasked mid-history and never fully stabilized:
"The legislators of Leiden... chose to alter the meaning of `⟨ ⟩` in Greek epigraphy so that,
although in nearly all the past century of publications `⟨ ⟩` regularly meant *dele* [delete], in
works after ca. 1932 `⟨ ⟩` usually mean[s] *adde* [add]... Clarity was not obtained by the change."
(lines 250–254) And: "The signs `⟨ ⟩` are ambiguous, and the Leiden convention... proposes `⌐ ⌐`
for corrections, but these look too much like `[ ]`, and broken type or poor printing might easily
change `[` to `⌐`. Hence in epigraphy this recommendation has not been accepted." (lines 787–793)
So the same bracket shape is documented as doing at least three different jobs (add-omitted,
substitute-erroneous, mark-incomplete) depending on sub-discipline and date, disambiguated only by
the editor's prose commentary — Dow's own stated view is this is a defect, not a feature: "in all
of the above instances except restorations and abbreviations, the critical apparatus ought to
state the facts clearly. There is no other way to insure clarity of understanding." (lines 790–792)

## Sources

- Sterling Dow, *Conventions in Editing: A Suggested Reformulation of the Leiden System* (Duke,
  1969). PDF: https://grbs.library.duke.edu/public/journals/11/grbs-supplemental-files/Conventions.pdf
  — capture: `leiden-dow-conventions-in-editing-full-ocr.txt` (this directory). Status: primary-adjacent
  (standard critical restatement, not the 1931 minutes themselves).
- TEI "Epigraphy" (Mahoney): https://tei-c.org/Vault/ETE/Preview/mahoney.html — secondary,
  corroborates angle-bracket/underdot/double-bracket meanings and flags the system as "neither
  universal nor flawless."
