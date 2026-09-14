# How famous completions mark "composer's hand" vs. "completer's reconstruction"

Status: mixed — historical anecdote (Stadler/Mozart) is well-attested across sources but I could
not independently verify it in a fetched primary text this session (Wikipedia's Requiem article,
directly fetched, does NOT contain it — see note). Mahler 10/Cooke material is secondary but
consistent across multiple sources. Elgar/Payne is well-sourced on the "elaboration not
completion" naming distinction specifically. Retrieved 2026-09-14.

## Overall honest assessment

This turns out to be **looser and less codified than the paintings/AIC or urtext-bracket cases**.
None of the three famous completions below uses a single, standardized in-score typographic
device (a special notehead, an ink/print color, a running margin mark) to flag "composer's
actual notation" vs. "completer's reconstruction" note-by-note, the way tratteggio or a
bracketed pitch does. Instead, each relies on one or more of: (a) the completer's own prose
disclaimers, (b) prefaces/critical apparatus in the score, (c) third-party tabulation
(after-the-fact, in program notes/reference works, not in the engraved score itself), or (d) —
in one historical case — literal handwritten circling by a contemporary on the actual autograph
manuscript (not something a modern printed edition preserves as a signal). This is a genuine and
somewhat surprising finding: the domain with the most famous completions (Requiem, Mahler 10)
does NOT have the codified per-note graphical marking that urtext editing has for smaller
editorial additions.

## Mozart Requiem (Süssmayr, and later Levin/Maunder/Druce completions)

- Historical: Wikipedia's account (as reported via WebSearch synthesis — the article's current
  text, when I fetched it directly, did **not** contain this passage, so treat this specific claim
  as a lead pending re-verification) states that Abbé Maximilian Stadler "carefully marked Count
  Walsegg's score to indicate which handwriting was Mozart's and which was Süssmayr's" — i.e. a
  physical, contemporary hand-marking directly on the manuscript, not a print convention.
  **Caveat**: my direct WebFetch of https://en.wikipedia.org/wiki/Requiem_(Mozart) found no
  mention of Stadler at all; it did contain an image caption "Everything not circled with pencil
  is in Mozart's hand up to page 32" describing a facsimile of the autograph — which independently
  corroborates that pencil-circling on the actual manuscript is the historically attested marking
  device, even though the Stadler attribution specifically did not appear in the fetched text.
- Modern editions (Bärenreiter/Nowak-Wolff, Peters/Black, Carus): per publisher descriptions
  found via search, these editions document the Mozart/Süssmayr(/Eybler) boundary through
  **prefaces and a detailed critical report/apparatus**, not through altered engraving (different
  notehead shape, italic type, etc.) within the printed score itself. I did not find a source
  confirming any of these editions use in-score typographic differentiation.
- Third-party (not the score itself): a fan/reference wiki table format uses italics to mark
  which sections of the Requiem's structure are "Süssmayr's additions" versus Mozart's — useful
  for orientation, but this is a describing-document convention, not something printed in the
  performing score, and the source is a fan wiki (low authority) — status: lead only.

## Mahler Symphony No. 10 (Deryck Cooke performing version, 1960-1976; revised with Colin &
David Matthews)

Cooke's own stated posture, per multiple secondary sources (Mahler Foundation, LA Phil program
notes, Wise Music/Universal Edition):
> "Mahler's actual music, even in its unperfected and unelaborated state, has such significance,
> strength, and beauty, that it dwarfs into insignificance the momentary uncertainties about
> notation and the occasional subsidiary pastiche-composing... After all, the thematic line
> throughout, and something like 90% of the counterpoint and harmony, are pure Mahler, and
> vintage Mahler at that."

Cooke was explicit his goal was **not** "completing" or "reconstructing" Mahler's thoughts but
producing "a practical performing version" — deliberately declining the stronger authorial claim
a "completion" would imply. Per one secondary description: "The publication of the score of
Deryck Cooke's version shows what is Mahler's and what has been added" — but I could not verify
the specific mechanism (footnotes vs. typography vs. accompanying critical notes) from a primary
source (a Universal Edition score preface) in this pass; this is a lead, not a confirmed
graphical-convention finding.

## Elgar Symphony No. 3 ("the sketches for Symphony No 3 elaborated by Anthony Payne")

This case is the best-sourced on the *naming/framing* distinction, though again not on in-score
typography:
- The work's official title is deliberately "elaborated by," not "completed by" — Payne and
  Elgar's estate insisted on this framing, per multiple sources including Payne's own book
  *Elgar's Third Symphony: The Story of the Reconstruction*.
- Payne's own account (per secondary sources on his book/interviews): the task was "not a
  'completion'... only Elgar could have done that," but a way of "presenting Elgar's ideas in
  full orchestral dress" while candidly adding "developmental and transitional passages that were
  missing from the sketches."
- Payne published the source sketches themselves (in facsimile, in his book) alongside his
  elaboration, letting readers compare directly — analogous in spirit to a critical apparatus,
  though delivered as an accompanying scholarly book rather than as in-score marks.
- Historical counter-example, sourced: an earlier BBC attempt (Roger Fiske orchestrating some of
  the sketches, with Carice Elgar's approval and Adrian Boult set to conduct) was abandoned when
  producer Maurice Johnstone judged it amounted to "tinkering" with Elgar's expressed wish ("No
  one must tinker with it") — i.e. a case where the profession's answer to "how much
  reconstruction is legitimate" was to not publish/perform at all, the direct musical analogue of
  Brandi's "the path chosen is not to complete anything" (see `conservation-brandi-principles.md`).

## Source records

- key: mozart-requiem-wikipedia-direct
  title: "Requiem (Mozart)"
  url: https://en.wikipedia.org/wiki/Requiem_(Mozart)
  retrieved: 2026-09-14
  status: primary (directly fetched), but does NOT corroborate the Stadler claim — used here as a negative-control / caveat, and for the "Everything not circled with pencil is in Mozart's hand up to page 32" image-caption quote
  quote: "Everything not circled with pencil is in Mozart's hand up to page 32."
  locator: image caption in the article body, on the autograph-manuscript facsimile image

- key: mozart-requiem-stadler-claim
  status: lead only — Stadler hand-marking claim surfaced via WebSearch synthesis, NOT confirmed in the directly-fetched Wikipedia article; needs a dedicated primary source (e.g. a Mozart Requiem scholarly monograph) to upgrade past "lead"

- key: mahler10-cooke-quote
  title: program notes / foundation pages on Mahler Symphony No. 10 (Cooke performing version)
  urls:
    - https://mahlerfoundation.org/mahler/compositions/symphony-no-10/symphony-no-10-history/
    - https://www.laphil.com/musicdb/pieces/3913/symphony-no-10-ed-deryck-cooke
    - https://www.wisemusicclassical.com/work/30391/Symphony-No-10-Cooke-completion--Gustav-Mahler/
  retrieved: 2026-09-14
  status: secondary (program-note/publisher tertiary sources quoting Cooke)
  quote: "Mahler's actual music, even in its unperfected and unelaborated state, has such significance, strength, and beauty, that it dwarfs into insignificance the momentary uncertainties about notation..."

- key: elgar-payne-symphony3-title
  title: "Symphony No. 3 (Elgar/Payne)"
  url: https://en.wikipedia.org/wiki/Symphony_No._3_(Elgar/Payne)
  retrieved: 2026-09-14
  status: secondary (directly fetched)
  quote: official work title uses "elaborated by Anthony Payne," and Payne "was obliged to contribute a quantity of original music" for the finale, having written its "entire development section and the coda"
  locator: article body
