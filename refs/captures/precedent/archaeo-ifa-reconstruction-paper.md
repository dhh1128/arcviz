# IFA Paper No. 5 — "Archaeological reconstruction: illustrating the past" (Hodgson, 2001)

**Title**: Archaeological reconstruction: illustrating the past
**Author**: John Hodgson
**Body**: Institute of Field Archaeologists (IFA — predecessor body to the current Chartered Institute for Archaeologists, CIfA), jointly with the Association of Archaeological Illustrators & Surveyors (AAI&S)
**Series**: IFA Paper No. 5, ISBN 0 948393 17 3, edited by Andrew Dutton
**URL**: https://www.archaeologists.net/sites/default/files/2024-11/CIfA-Archaeological-Reconstruction-Illustrating-the-past_2001.pdf
**Retrieved**: 2026-09-14
**Status**: PRIMARY — full text read directly from the CIfA-hosted PDF via the Read tool's PDF parser (WebFetch's own summarizer choked on the binary/JBIG2 stream and could not extract text; the Read tool succeeded where WebFetch failed).

This is a professional-body technical paper (not a binding "Standard," but a citable IFA/CIfA-published guidance document co-authored with the illustrators' own professional association) specifically about how to visually communicate the boundary between attested fact and conjecture in reconstruction drawing. It is the closest primary source found to arcviz's HP1 problem — and it is notable that, as of 2001, the profession explicitly says this problem is UNSOLVED for them too.

## Key verbatim passages

### On buildings whose only firm evidence is invisible (foundations)
> If the building still stands, the chances of making a valid reconstruction of its original appearance (or of one of its phases) are fairly high. In other cases, these subjects demonstrate a major difficulty of reconstruction: the only firm surviving evidence is the foundations, which were invisible anyway; all the rest of the structure is conjectural. Buildings of this kind are a major argument for producing a number of alternative, equally valid, hypotheses.
(p.9, "Buildings")

### On the temptation to hide the boundary of what's known — THE closest direct hit on HP1
> One factor that may still be a problem is the temptation to show everything, whether the evidence is there or not. A conventional illustration, by its nature, has some areas that are hidden from the viewer because other objects interpose; the artist can arrange for these to coincide with those areas that are doubtful or missing. This can no longer apply if the audience is, in effect, going to be swarming all over the scene. It would be possible for these areas to be rendered grey, or even insubstantial, but it seems that artists usually render every surface as if full information were available. **This may well give a false impression of the extent of the data.**
(p.16, "Monochrome (black and white) artwork" section)

This is a named failure mode with the same shape as arcviz's problem: an illustrator can cheat by hiding uncertainty behind occlusion (something else in the way), but that trick only works in a fixed 2D view — the moment the audience/user can move around or interact (arcviz: pan/zoom/expand a graph), the cheat is exposed and the missing-vs-known distinction has to be rendered honestly. The paper floats "grey" or "insubstantial" rendering for doubtful/missing areas as the fix, but reports that in practice illustrators don't do it and default to full solidity — i.e., **industry practice as of 2001 fails this problem by defaulting to "everything is fine."**

### On there being no standard for grading certainty — explicit "not yet solved"
> If an archaeologist is making a written conjecture about the possible meaning and significance of a site, the article will bristle with references, parallels and closely reasoned argument. If an artist makes a pictorial conjecture from the same data, it is apparently sufficient to put 'Artist's impression' as a footnote. This may explain why reconstruction is not always regarded as a very scientific exercise by the archaeological profession; information sources are of widely varying quality, quantity and objectivity, and are never cited anyway. While both considerations of space and publisher's wishes may preclude a full citation under a reconstruction, some effort to include at least the major sources might help the credibility of the practice. **In the long run, a recognised system of quantifying the reconstruction's level of probability – if this can be achieved – would give the audience a much better indication of its value.**
(p.17, "Citation of sources")

The conditional "if this can be achieved" is the tell: as of this 2001 professional-body paper, a standardized, graduated certainty/probability notation for reconstruction drawing did **not exist** and was aspirational. This corroborates arcviz's own "no prior art found" framing for the general problem — it's not that arcviz failed to find an existing solution, it's that the archaeological-illustration profession itself hadn't produced one either by 2001 (a search for a post-2001 resolution was outside this pass's scope; flagged as a LEAD to check if wanted).

### On alternative, equally-valid reconstructions from identical data (a different mitigation than certainty-grading)
> Simon James: Cowdery's Down. This is now a classic example of alternative reconstructions, an approach which is still underused. These 'alternative realities', based on identical data sets, have very different characters and apparent status. The spectrum of possible interpretation can, for most sites, be very broad.
(p.10, Figure 9 caption)

### On the future-facing aspiration toward showing possibilities rather than one certainty
> There is now the opportunity to present a far more fluid picture which is much more representative of the real situation – showing possibilities, rather than pretending to certainties.
(p.18, "Future developments")

## Assessment against arcviz's HP1

- The paper confirms, from inside the discipline, that (a) the failure mode arcviz worries about ("everything is fine" / hiding the unknown behind implicit occlusion) is a REAL, NAMED, and as-of-2001 UNSOLVED problem in archaeological illustration; and (b) the two mitigations floated by the field are (i) graduated certainty/probability notation (aspirational, not built) and (ii) presenting multiple alternative reconstructions side by side rather than one authoritative image — a different strategy from arcviz's "distinguish three states within one graph" ask, closer to "don't claim a single answer at all."
- **Inference (ours):** arcviz's three-state requirement (withheld-contents / missing-referent / blinded-edge) is a harder and more structured version of this problem than the reconstruction-drawing literature has attempted — that literature is fighting a binary (attested vs. conjectural), not a three-way distinction with a topology-unknown case. No evidence was found that the reconstruction-illustration field has gone further than the binary.
