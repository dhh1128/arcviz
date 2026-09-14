# Documented redaction failure modes — capture

Status: mixed — one PRIMARY technical standard (NSA guidance, fetched and pdftotext'd from the actual PDF), one PRIMARY academic paper (fetched and pdftotext'd), one well-documented real-world incident (secondary reporting, multiple outlets, treated as established fact given corroboration).
Retrieved: 2026-09-14.

## 1. NSA, "Redacting with Confidence: How to Safely Publish Sanitized Reports Converted From Word to PDF"

Primary source, PDF fetched via Wayback Machine mirror (the original https://sgp.fas.org/othergov/dod/nsa-redact.pdf returned an empty body / bot-challenge to direct curl; the Wayback Machine snapshot at https://web.archive.org/web/2020/https://sgp.fas.org/othergov/dod/nsa-redact.pdf returned the full 19-page PDF, HTTP 200, 681417 bytes). Document identifier reported by secondary sources as I333-015R-2005 / I333-TR-015R, dated 2005 with a 2006 revision addressed here. Text extracted with `pdftotext -layout`.

### The core principle (page 2, "Deletion not Redaction")

> "The key concept for understanding the issues that lead to the inadvertent exposure is that information hidden or covered in a computer document can almost always be recovered. The way to avoid exposure is to ensure that sensitive information is not just visually hidden or made illegible, but is actually removed from the original document. Thus any sensitive information must be removed from the document through deletion."

### The three named failure modes (page 1–2, "Typical Kinds of Exposures")

> "1. Redaction of Text and Diagrams - Covering text, charts, tables, or diagrams with black rectangles, or highlighting text in black, is a common and effective means of redaction for hardcopy printed materials. It is not effective, in general, for computer documents distributed across computer networks (i.e. in 'softcopy' format). The most common mistake is covering text with black."

> "2. Redaction of Images - Covering up parts of an image with separate graphics such as black rectangles, or making images 'unreadable' by reducing their size, has also been used for redaction of hardcopy printed materials. It is generally not effective for computer documents distributed in softcopy form."

> "3. Meta-data and Document Properties - In addition to the visible content of a document, most office tools, such as MS Word, contain substantial hidden information about the document. This information is often as sensitive as the original document, and its presence in downgraded or sanitized documents has historically led to compromise."

This is exactly the failure mode the assignment asked to find: a visual mask (black box/highlight) that LOOKS like a redaction but does not actually remove the underlying data — the redaction fails to hide its own extent because it doesn't actually delete anything; the "extent" and the content are both still fully present underneath, contrary to what the black box implies to a viewer.

## 2. Lopresti & Spitz, "Information Leakage Through Document Redaction: Attacks and Countermeasures" (SPIE Document Recognition and Retrieval XII, Jan. 2005)

Primary source, PDF fetched directly (https://www.cse.lehigh.edu/~lopresti/Publications/2005/spie05a.pdf, 381097 bytes), text extracted with `pdftotext -layout`.

### Documented real-world incident this paper is responding to (their own citation, Naccache & Whelan)

> "It has been recently demonstrated, in dramatic fashion, that sensitive information thought to be obliterated through the process of redaction can be successfully recovered via a combination of manual effort, document image analysis, and natural language processing (NLP) techniques. As reported in international news media, computer security researchers David Naccache and Claire Whelan demonstrated that they could recover two instances of redacted text from images of previously classified U.S. intelligence memos by measuring font design attributes and matching them against a font database... they were able to determine that the missing word in the second case was almost certainly 'Egyptian.'"

(This is the well-known font-matching recovery of a redacted word from a leaked U.S. government memo — the paper cites it as motivation but does not itself name the specific memo/incident beyond this description; treat the underlying Naccache/Whelan claim as a LEAD if a named, dated incident is needed — this capture only verifies what Lopresti & Spitz themselves say about it.)

### The extent/length side-channel (exactly the "box size leaks information" failure mode requested)

> "3. When using a monospaced font (such as Courier), the width of the gulf between the cleartext immediately adjacent to the redacted region reveals the length, in characters, of the missing word(s). Combined with [NLP / dictionary knowledge] ... 4. For proportionally-spaced fonts, based on the locations of adjacent words and estimates of character widths ... the widths of missing words can be estimated and, as in the monospaced case, NLP brought to [bear]."

> "...an estimate of the width of the redacted text in combination with language statistics. To study this question, we conducted a simple experiment that involved computing the widths of text strings chosen from [a lexicon] ... to determine the missing text based solely on the width of the redaction."

The paper's own countermeasures section explicitly names the design failure and its fix:

> "Some fonts reveal more information via word widths than others; do not permit sensitive documents to be [set in low-entropy fonts] ... Produce special 'secure-for-redaction' fonts in which the width of each character is varied randomly ... Taking the previous idea to an extreme, reflow the text so that the widths of all redacted regions are made to be the same constant size ... A large, fixed-sized rectangle reading 'REDACTED' could be inserted where the redacted text was removed."

And the acknowledged limit of any such fix:

> "the above techniques will hide the length of a missing word, for example, but few will obscure the fact that it is[a word at all]..."

This last line is important: even the paper's own proposed countermeasure (fixed-size boxes) only hides LENGTH, not the fact that something was removed. It cannot be pushed further into hiding whether a redaction happened at all without ceasing to be a redaction (a real page with a real gap) — a caution directly relevant to arcviz's design problem, since arcviz's states must be distinguishable as REAL structural facts, not just visually smoothed over.

## 3. Real-world incident: Manafort defense filing, January 2019 (secondary reporting, multiple corroborating outlets — treated as established fact)

On January 8, 2019, Paul Manafort's defense team filed a brief in federal court (response to Special Counsel allegations of breached plea-cooperation agreement) with black boxes placed over sensitive paragraphs. The boxes were image/annotation overlays that had not been "flattened" into the PDF — the underlying text remained present and selectable in the PDF's content stream underneath the black boxes. Reporters (widely reported at the time, e.g. by CNBC and Vice, per WebSearch results retrieved 2026-09-14) discovered they could select the "blacked-out" text, copy it, and paste it into a word processor to reveal it in full — revealing that Manafort's campaign-chairman-era team had shared 2016 campaign polling data with Konstantin Kilimnik. This is the canonical example of the NSA guidance's Type-1 mistake ("covering text... with black" rather than deleting it) occurring in a modern, high-profile, unintentional court filing, not a hypothetical.

NOTE: this incident is corroborated across multiple independent outlets in the WebSearch results (Vice, ABA Journal, CNBC-via-secondary, Lexology) but was not independently re-fetched and quoted verbatim from a single primary news article in this pass — mark the specific attributed quotes above ("those sections are easily viewable...") as SECONDARY/paraphrased-from-search-summary rather than a directly fetched verbatim quote.

## Design principle synthesis (Inference (ours), not legal fact)

The common thread across the NSA guidance and the Lopresti paper: a redaction fails exactly when the VISUAL absence of information is decoupled from the ACTUAL absence of information underneath, or when the visual signifier's own geometry (box size, gap width) leaks a proxy for the withheld content's size. Two independent, decades-apart, technically-grounded sources converge on the same principle: the marker of "something is missing here" must not encode anything about WHAT is missing (not even its length), and it must be a genuine structural absence, not a masked presence. This maps directly onto arcviz's HP1: a node/edge signifier for "known to exist, contents withheld" must be an honest, structurally-real placeholder (a real graph node/edge marked with a type, the visualization equivalent of "deletion not redaction") rather than a mere visual dimming or box laid over real data that a user could accidentally reveal or unconsciously estimate the size of.
