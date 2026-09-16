# Captures of the responsive arm B

Renders of [../arm-b-responsive.html](../arm-b-responsive.html), clipped to the component itself — no page chrome, no gauge rail, no phone frame — except the two `desktop-*` files, which are whole pages because what they show is a page-level fault. The number in each filename is the viewport width in CSS pixels; each file is that width and no other, because the component has no authoring width. Captured at device pixel ratio 2 in headless Chrome 153. Measurements are in [../RESPONSIVE.md](../RESPONSIVE.md).

The component caps at 480 px by default and turns surplus width into margin, so there is no capture above 480 apart from the desktop pair: every wider viewport renders identically to `rest-480.png`.

| file | what it shows |
|---|---|
| `rest-320.png` | The rest register at the conformance floor. Three chips across. The `qvi` edge from ITEM 02 to ITEM 01 is drawn **ascending** — the DD-1 violation of RESPONSIVE.md's F1 — and ITEM 04 shows `⋯2 edges` where its two labels do not fit. |
| `rest-360.png` | The same load at the width every earlier artifact was authored at. Four across, and the objects land on the authored mock's own column positions. |
| `rest-480.png` | Five across — the component's default maximum width, so this is what every viewport of 480 px or wider shows. |
| `desktop-uncapped-1440.png` | **Whole page**, with the maximum width removed. All thirteen objects in one row, 102 px tall: the diamond, the shared ancestor and both descending edges are gone. This is the layout converging on the horizontal axis DD-7 refused, and it is what the first version of this file did at every ordinary desktop width. RESPONSIVE.md §10. |
| `desktop-capped-1440.png` | **Whole page**, same viewport, with the 480 px maximum in force. The pair is the argument for having a ceiling at all. |
| `focus08-320.png` | ITEM 08 expanded in place at 320. Both parents stay attached; the full stale banner holds one line in the 288 px card. |
| `focus08-360.png`, `focus08-480.png` | The same focus at wider viewports; the card gets shorter as it gets wider. |
| `twofloor-320.png` | DD-5's second floor at 320. No row holds two mid forms, which is the threshold at work. ITEM 04 carries **both** edge labels here — the tier at which DD-3 becomes satisfiable. |
| `twofloor-360.png`, `twofloor-480.png` | The second floor above the two-mid threshold. |
| `bands-320.png`, `bands-360.png` | Band packing, which forces a row break at each authored band boundary. Compare against `rest-*` at the same width: +30.5% of column at 320. |
| `words-320.png` | The words-only floor the perimeter glyphs replace, for the small-n probe to compare against `rest-320.png`. Items 10 and 11 carry their states as six-point words. |
| `banner-el251-768.png` | Component pinned to 283 px inside a 768 px viewport: card 251 px, full stale banner on one line. |
| `banner-el248-768.png` | Pinned to 280 px: card 248 px — the retest's number — with the short banner on one line. |
| `banner-el176-768.png` | Pinned to 208 px: card 176 px, short banner wrapping. Nothing clips. |

Every capture is a render at the stated width, not a reconstruction or a scaled specimen.
