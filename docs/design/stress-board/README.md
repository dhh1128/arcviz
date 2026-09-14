# SC13 stress board — results

The artifact [synthesis.md](../charrette/synthesis.md) §6 said to build first: the composite design at 360 px, under multiplication, with the four budgeted prominence states co-present and all three absences drawn, built as two honest variants of the open ledger question [Q-KP7T]. This README states the falsifier results **as results**. Two of them wounded the composite; that is the board working.

## Files

- [board-per-card.html](board-per-card.html) — variant A: the full board, verification rendered per card.
- [board-central-ledger.html](board-central-ledger.html) — variant B: the identical board, verification rendered once as a per-(check, subject) matrix inside the gate.
- [focus-sequence.html](focus-sequence.html) — static frames of focus-in-place (rest; item 08 expanded with all ten other objects at the floor), plus the two gauges that measure the compact-chip floor and the hole/frontier distinction under compression.

All three files are standalone HTML+CSS: no build step, no JS, no external resources, no `:hover`, no animation. **Greyscale:** there is no separate greyscale variant because there is no colour variant — every file is authored hue-free (grep for non-grey colour values finds none), so each board is its own greyscale exhibit, per the charrette convention.

## The load

One presentation of eleven items. Inside the render each carries only an opaque host load label (`ITEM NN`); this manifest is the outside-the-render mapping:

| item | fixture | states it carries |
|---|---|---|
| 01 | `vlei_qvi` | H9 seal · stale (P30D) |
| 02 | `vlei_le` | stale (P30D) |
| 03 | `vlei_ecr` | edge into the H7 hole · stale (PT72H) · top-level `u` populated (contrast for item 10) |
| — | `vlei_ecr_auth` **withheld** per [`loads/h7_missing_credential`](../../../corpus/loads/h7_missing_credential.json) | the drawn hole `EM7gTDXqvy…`, severing the chain into two components |
| 04 | `diamond_depth_origin` | two edges · stale (PT12H) |
| 05 | `diamond_depth_b` | short path · byte-identical e-section with item 07 |
| 06 | `diamond_depth_c` | long path |
| 07 | `diamond_depth_f` | long path · byte-identical e-section with item 05 |
| 08 | `diamond_depth_a` | shared ancestor at longest-path rank · H9 seal · stale (PT12H) · the focus target |
| 09 | `two_blinded_edges_converge` | two H8 edges into the frontier |
| 10 | `metadata_acdc` | H6-possibly (empty top-level `u`, no corroboration) · its `evidence` edge yields the second H7 hole (`EDSm-SsfXZ…`) · committed `r` terms |
| 11 | `unblinded_commitment_h2` | H2-guessable `a` unit · H9 seal |

On item 09: the render never says which of the `two_blinded_edges_{converge,diverge}` pair it is, and by construction the diverge twin produces the same board with only the SAID strings differing — but this manifest names the fixture because the coyness would be theater: the item's own `d` pill identifies the fixture to anyone holding the corpus. That is itself the lesson the verification's T6 sweep taught — the ground truth leaks through any provenance channel adjacent to the render, which is why the host contract requires opaque load labels and why this table lives here and not in the files' commentary panels.

Host stubs, declared (SC13's gap G3, partially instantiated): per-credential freshness policies P30D (items 01, 02), PT72H (03), PT12H (04, 08), none for the rest — three distinct policies so Rule 4's two-policy test runs at scale, and six no-policy cards so the no-policy state stays exhibited; one host as-of scope (2026-06-14T00:00Z) and a host render moment (2026-09-14T12:00Z); a SAID-verified schema document for item 11 only (fields `{d, i, overThreshold}`, no `u` reserved — the Rule 8 "guessable" classification rides this declared input, since no other schema document exists in the corpus); the root-delegator load context from [`loads/h7_missing_delegator_kel`](../../../corpus/loads/h7_missing_delegator_kel.json). No verification vectors, cause attestations, watchers, or presentation evidence — the honest defaults everywhere else.

**Deviation from the brief, owned:** the brief said eight or nine cards. Eleven are rendered, because the four budgeted states plus all three absences cannot be carried by nine real-fixture cards — the metadata-decoy and guessable states have exactly one fixture carrier each, and the diamond cannot lose a node. Eleven cards at 360 px is strictly more stress than nine, so every falsifier below ran under a harder load than specified, never a lighter one.

## Where each element came from

Gate-as-enclosure: structure's geometry, print's wording, with one addition forced by mobile — the gate's side rails are the only part of the render-level state that survives scroll (see falsifier 2). Frontier as first-class region with open-arrowhead terminals and fixed-size entry marks: graph, with precedent's anti-leak constraint; its continuation down the left margin as a gutter (so blinded edges and hole fringes enter it locally, keeping structure's sublinearity at mobile aspect ratio) is this board's own extension, not a charrette element. Hole with double border, shared hatch, SAID pill, four fixed statements, egress fringe: graph and structure per synthesis §2.1, fringe honors shared with precedent. Seal plus committed-fact sentence: graph/structure §2.3. Always-on section manifest on every card, all four slots, no exceptions: print (its own F-PR2 fixed). Point-of-use captions, no legend: print. No empty-box glyph anywhere: print's finding, enforced. Word/glyph ledger cells with declared outcome space: structure's words, graph's ○/⊘. Operator discipline — five `NI2I — derived` on the diamond, `I2I — derived` byte-identical wording on the chain edge, `I2I · declared` on the edge into the hole, `operator UNDETERMINED` on both H8 edges and the o-less edge to the second hole: Rule 9 as rewritten, checked against every fixture (no `a.i` anywhere in the diamond family; the chain's far nodes targeted). Card-level deformations — stale breaks the frame, H6-possibly withdraws the frame to its corners, H2-guessable spends a transparent region: structure's sketched tier, mocked here for the first time; the corner-withdrawal form for the *possibly* state is this board's coinage and needs review. Correlator dock and ×N chips: graph. Delegation reach wording ("reach 0 tiers, blocked at issuer KEL"): print's correct version of what F-S3 got wrong. Centralized matrix: print's aggregated wall, extended honestly to full per-(check, subject) arity. The floor form: graph's asserted floor, given a concrete shape and measured.

## Falsifier results, in the synthesis's order of cheapness

### 1. The compact-chip floor — HOLDS, but it is thinner than the composite claimed

There is a legible floor form: 76×44 px (gauge A in [focus-sequence.html](focus-sequence.html)) — an 8 px ten-character SAID pill, a 6.5 px item tag, glyph-only ports or a seal bar, and the stale frame-break. Ten such objects plus one fully expanded card plus gate, band, and gutter fit in 716 px of height — just over one phone viewport: frame 2 shows the whole eleven-object presentation focused on item 08 with both parents attached and nothing removed — the pile's impossible condition, met at SC13 scale. Focus-in-place therefore keeps its load-bearing property, with two hard qualifications:

- **The floor holds states, not parameters.** The stale *kind* survives (the break); the policy value, horizon, and every cause/cardinality sentence die. Rule 4's two-policy distinction is invisible between two floor chips — it recovers only on expansion. Convergence 4 (prose dies first) is confirmed under multiplication, at the exact point the composite leaned on prose.
- **Only one of the three card-level deformations survives the floor structurally.** The frame-break is a perimeter event and reads at 76 px; the corner-withdrawn frame and the transparent a-region are area signatures and do not — at the floor, items 10 and 11 keep their budgeted states as six-point words, which is precisely the P9 failure mode. Either the floor for deformed cards is higher than 76×44, or H6/H2 need perimeter-class floor glyphs that have not been designed. This is a real wound: "budgeted markers held above the floor" is currently true of stale only.
- The gauge's other finding: uniform scaling exhausts legibility by ≈ 0.85×, so "compression substitutes for occlusion" must mean *reflow to the floor form*, never scaling. Any implementation that animates a uniform shrink passes through illegible states.

### 2. Level competition — the levels do not compete; the scroll does

With everything co-present — gate, two holes, a KEL-tier hole, the frontier, five stale breaks under three policies, the corner-withdrawn frame, the transparent unit, 101 quiet cells — no two levels contend for one channel anywhere on either board. Enclosure, geometry, card form, and symbol stay disjoint at 360 px; a reader scanning either variant meets terrain, not competing alarms. HP3's specific fear did not materialize, and the frontier's sublinearity held (two blinded edges, two fringes, one region). Geometry cost of the graph-level tier: the hole/foundation/band stack is ≈ 530 px, about 8 % of variant A's column height, plus the 16 px gutter (≈ 5 % of the width) running its full length — structure's "space is commitment" is affordable at this density.

**But the board surfaced the real competitor, which the charrette's desktop mocks could not see: at 360 px, co-presence dissolves into sequence.** Variant A's render measures 6,884 px — over ten phone screens — so at any scroll position, almost every budgeted marker is off-viewport with **no surviving trace**, which is SC13's own fails-if observable ("occluded by pile/scroll/collapse behavior with no surviving trace"), hit by both variants. The one element that survives scroll is the gate, and only because it is an enclosure: its double rails run the full height. Nothing analogous exists for stale, the holes, or the wall. The prominence spine survives multiplication; **it does not survive the viewport**, and no mitigation is designed anywhere in the composite. This is the board's largest adverse finding and it is a design gap, not a mock defect.

### 3. Hole versus frontier — DISTINGUISHABLE, but the hatch is not what distinguishes them

Gauge B, corrected by the rendered evidence: the hatch does not die uniformly — it dies *asymmetrically*, because texture legibility depends on area. By 0.55× a chip-sized hole's interior reads as flat grey while the larger frontier region still reads visibly striped, so the "one texture, one concept" link between hole interior and frontier breaks at chip scale even before the texture itself vanishes; a viewer comparing a small hole against the region has no texture match left to find. Below that point the distinction is carried entirely by *double-bordered-and-pilled* versus *unbordered region*, plus position. The pill inside the hole stays legible down to the floor form (8 px); the double border survives everything. Result: the slab fallback is **not triggered** — but the design's stated mechanism ("one texture for unmapped, border-plus-pill for a named window onto it") should be restated, because at chip scale the texture contributes nothing and the border-pill pair does all the work. The hatch's honest job description is large-scale texture.

### 4. Loading and counting misreads — cannot be closed from the armchair; the board sharpened both

P9 forbids certifying these without users, so the board records geometry choices and one negative result. Loading: no shimmer, no spinner geometry, no retry affordance, static declarative text in every hole and the band — the choices are made, and the small-n probe (five untrained readers, three questions) named in synthesis §6 remains the only way to close it. Counting: at full scale the bracket-plus-cardinality mitigation renders beside item 09; **at the floor it does not exist** — frame 2 reduces two blinded edges to two open arrowheads and a six-point "1–2 dest." tag, so the count-the-terminals residual is *unmitigated* exactly where the presentation is densest. The structure seat called this residual unfixable without lying in the other direction; the board adds that the fix the composite does have is confined to expanded scale.

## The ledger recommendation [Q-KP7T]: per-card, with the matrix retained as a flattening

Measured on the pair: variant B's graph column is 4,110 px against A's 6,710 (the eleven per-card ledgers cost ≈ 2,490 px, about 37 % of A's column, and the whole render drops from 6,884 px to 4,858 px — 29 % shorter), and its 573 px matrix holds all 101 cells in under one phone screen without collapsing arity. That is the whole case for centralization, and it is real but it is a *scroll* saving, not an honesty gain. What it costs, observed in the build: every Rule 10 blocking identifier moves out of its cell into footnotes a–f — "why is this ⊘" becomes a three-hop read (card → column → footnote) — the two drawn holes can no longer name their blocked checks inline and point at ledger notes instead, and once the matrix scrolls off, **no V state of any kind is co-visible with any card**; the manifest's `V: ledger col NN` mark is a pointer, not a state, and the distance channel is exactly the one the synthesis predicted a habituated reader stops crossing. Meanwhile falsifier 1 showed chips never carry ledgers anyway, so per-card cost is only paid at expanded scale, where it is affordable — and per-card keeps the blocker at the point of the state, which is the property Rule 10 exists for.

**Recommendation: per-card.** The centralized matrix earned a different job than the one at issue: it is the correct *print flattening* of the wall (SC14) and a candidate gate-adjacent summary *in addition to* per-card state — it demonstrated that at the all-unperformed default the wall's uniformity is one fact that can be shown once. It should not be the primary residence of V state on screen.

## What the board could not test

- **Interaction.** The AF1 observables (focus transitions, nothing occluded *during* reflow) are drawn at two moments, not operated; the mid-transition states, and whether uniform-scale animation sneaks in illegible frames, need the interactive build.
- **The untrained read** — loading misread, error misread, terminal counting, and whether "possibly a metadata ACDC" or "recoverable/guessable" mean anything to anyone. Needs the small-n probe; the armchair is disqualified (P9).
- **Scroll-occlusion mitigation** (falsifier 2's wound): nothing here tests a fix, because none exists to test. Candidates — a persistent edge-of-viewport residue strip, or rail deformations per budgeted state — are undesigned and unvalidated.
- **Habituation (HP2)**: the board renders the wall honestly 11 times over ≈ 2,490 px in variant A; whether anyone still sees it on the hundredth render is untestable in a static artifact and unclaimed.
- **Real host vectors** — every ledger is at the honest store-fed default; a board with mixed pass/fail cells under a fail-capable host is a different stress (SC9's territory) and would exercise the matrix much harder than uniformity does.
- **The `r`-band layout commitment** (gap G12): item 10's terms row is one sentence, not a rules band; Rule 16's real test still cannot run.
- **First-contact legibility.** Opaque load labels plus pill-first identity solved the P12/leak problem completely and made the board unreadable as "what does this credential say" — the board is tuned to the far end of the [Q-8Y3M] dial by inheritance, and it quantifies what that costs but cannot adjudicate the dial.

## Coinages requiring review (this board's own, not the charrette's)

The frontier gutter (the region continued down the left margin); the corner-withdrawn frame for H6-possibly; the `·` no-such-subject glyph in the matrix; the 76×44 floor form and its shedding order. Each was forced by 360 px and none has a charrette pedigree — treat them as proposals with exactly one exhibit behind them.
