# Lacuna / missing-measure conventions in text and score editing

Status: general convention for text criticism is well-established and directly sourced; the
music-specific "missing measures" convention is thinner in what I could independently verify —
flagged explicitly below. Retrieved 2026-09-14.

## Text-critical convention (classical/medieval philology — the ancestor of the musical practice)

Standard scholarly practice (per a University of Toronto Centre for Medieval Studies guide to
text editions, and corroborated by general Leiden-convention literature already captured
elsewhere in this repo, `leiden-symbol-table.md`):
- A lacuna caused by physical damage is marked with asterisks `***`.
- A *conjectural* lacuna (inferred from a deficiency of grammar/sense, not visible physical
  damage) is marked the same way but inside angle brackets: `<***>`.
- Smaller lacunae (a few missing characters) are sometimes marked with a count (a number, or a
  string of zeros) indicating the estimated number of missing characters, rather than an
  unbounded ellipsis.

This is directly analogous to arcviz's problem: text criticism already distinguishes "we know
something is missing and roughly how much" (asterisks with a count) from "we are inferring that
something must be missing" (the same marker in angle brackets) — i.e., a confidence/provenance
distinction on the *fact of the gap itself*, not just on its filled content.

## Music-specific convention — thinner evidence

I could not find a single well-documented, widely-cited convention specifically for "N measures
of the manuscript are physically missing/illegible" analogous to the text-critical asterisk
convention. What the search surfaced instead:
- Ossia staves (a small alternate staff printed above the main one) are a real, well-documented
  convention, but they are for presenting a genuine *alternative reading* the editor believes is
  equally valid (an easier version, a variant the composer left open, a proposed cadenza) — not
  specifically a marker for "this passage is reconstructed because the source is damaged/lost."
  Wikipedia's "Ossia" article and MuseScore/Finale documentation describe the mechanism, but
  none of the sources I found used it explicitly as a lacuna-marking device (that would be an
  inference, not sourced).
- Early-music scholarly editions do have an explicit lacuna convention at the level of
  individual notes/passages: "Missing portions of music and other notational elements
  editorially reconstructed are placed in square brackets" (Lost and Found project, see
  `notation-urtext-brackets.md` — status: lead, not independently re-verified this session).
- I did not find a citable source describing a standard convention for marking an entire missing
  *measure* (as opposed to a note, accidental, or short passage) distinctly from a reconstructed
  one — e.g., blank measures, "[N mm. missing]" text insertions, or dedicated engraving symbols.
  This appears to be handled ad hoc, per edition, via prose in the critical commentary/preface
  rather than a codified graphical convention — this is my own read of the evidence gap, not a
  sourced claim that no such convention exists anywhere.

**This is a genuine finding, not a search failure to hide**: unlike the AIC ethics clause or the
Leiden text conventions, there does not appear to be a single, citable, codified graphical
symbol for "measure(s) physically missing from a musical manuscript" the way there is for
textual lacunae. Scholarly music editions handle it through prose (critical commentary/preface)
on a case-by-case basis. If arcviz needs a codified symbol precedent for "topology entirely
unknown," the text-critical `<***>` convention is the closer and better-sourced analogy than
anything found specifically in music engraving practice.

## Source records

- key: toronto-medieval-text-editions-guide
  title: "Guide to Text Editions" (course guide)
  author/body: Centre for Medieval Studies, University of Toronto
  url: https://www.medieval.utoronto.ca/sites/medieval.utoronto.ca/files/Guide%20to%20Text%20Editions.pdf
  retrieved: 2026-09-14
  status: secondary (pedagogical guide summarizing standard classical/medieval editorial convention), not independently pdftotext-verified this session — sourced via WebSearch synthesis
  quote: "indicate a lacuna by three asterisks *** if the text is damaged; if the lacuna is conjectural ... place the asterisks in pointed brackets <***>"
  locator: guide body (page/section not confirmed — flagged as lead-grade sourcing for exact wording, though the convention itself is standard and cross-corroborated in classics/papyrology generally)

- key: ossia-wikipedia
  title: "Ossia"
  url: https://en.wikipedia.org/wiki/Ossia
  retrieved: 2026-09-14
  status: secondary (general encyclopedia), used only for the mechanism description — NOT claimed as a lacuna-marking convention (that would be our own inference, not sourced)

- key: music-lacuna-gap (negative finding)
  status: gap/lead only — no citable source found in this pass for a codified graphical convention marking an entire missing measure/passage as physically lost (as distinct from editorially reconstructed at the note level). Treat "music engraving has no single codified missing-measure symbol" as an honest evidence gap, not a confirmed universal negative.
