// The shape of public/data.json, written by build_data.py. The React side renders these values
// and computes nothing of its own beyond layout and the line budget.

export interface Component {
  kind: string;
  value: any;
  gain: number;
  role_bearing: boolean;
  issuer_claim: boolean;
  negative: boolean;
  text_alternative: boolean;
}

export interface Descriptor {
  components: Component[];
  annotations: { kind: string; digest?: string }[];
  distinguishing: boolean;
  distinguishing_as_text: boolean;
  indistinguishable_from: string[];
}

export interface Classified {
  categories: string[];
  category_hits: Record<string, string[]>;
  subject: string;
  subject_why: string;
  alignment: string;
  alignment_why: string;
  input: string;
}

export interface Edge {
  label: string;
  target: string;
  schema: string;
  operator?: string | null;
}

export interface Img {
  state: "resolved" | "committed-not-resolved" | "none";
  src?: string;
  digest?: string;
  manifest?: Record<string, any>;
  media_type?: string | null;
}

export interface CNode {
  name: string;
  said: string;
  schema: string;
  issuer: string;
  issuee?: string | null;
  attrs: Record<string, any>;
  sections: Partial<Record<"a" | "A" | "e" | "r", any>>;
  edges: Edge[];
  classified: Classified;
  fixture_summary?: string;
  image: Img;
  type: { name: string | null; source: string; schema_state: string };
  glyph_override?: { category: string; glyph: string; why: string };
  photo_glyph?: { why: string };
  borrowed_schema?: Record<string, any>;
}

export interface Party {
  identifier: string;
  label: string | null;
  aliasState: "shown" | "withheld-here" | "none";
}

export interface Frame {
  id: string;
  title: string;
  presented: string;
  nodes: CNode[];
  descriptors: Record<string, Record<string, Descriptor>>;
  descriptor_variants: string[];
  parties: Record<string, Party>;
  supplied_by_hand: string[];
}

export interface Data {
  generated_by: string;
  abbreviations: Record<string, { medium: string; short: string }>;
  category_meanings: Record<string, string>;
  host_note: string;
  frames: Frame[];
}

// DD-1: the presented node on top, references descending, rank by LONGEST path so a node
// reachable at two depths sits at its deepest.
export function ranks(frame: Frame): string[][] {
  const bySaid = new Map(frame.nodes.map((n) => [n.said, n]));
  const depth = new Map<string, number>();
  const visit = (said: string, d: number, seen: Set<string>) => {
    if (seen.has(said)) return;
    if ((depth.get(said) ?? -1) >= d) return;
    depth.set(said, d);
    const n = bySaid.get(said);
    if (!n) return;
    const next = new Set(seen).add(said);
    for (const e of n.edges) visit(e.target, d + 1, next);
  };
  visit(frame.presented, 0, new Set());
  const rows: string[][] = [];
  for (const n of frame.nodes) {
    const d = depth.get(n.said) ?? Number.MAX_SAFE_INTEGER;
    const idx = d === Number.MAX_SAFE_INTEGER ? -1 : d;
    if (idx < 0) continue;
    (rows[idx] ??= []).push(n.said);
  }
  const orphans = frame.nodes.filter((n) => !depth.has(n.said)).map((n) => n.said);
  if (orphans.length) rows.push(orphans);
  return rows.filter(Boolean);
}

// "Ranked by surprisal, with the weakest dropped rather than the last truncated." The type is
// the head and is always shown, so the budget applies to everything after it. Kept components
// are displayed in the algorithm's own order; only the choice of WHICH to keep uses the gain.
export function budgeted(d: Descriptor, lines: number): { kept: Component[]; dropped: Component[] } {
  // Not budgeted: the type is the head, the role rides on the labelled arrow, and the image is
  // the thumbnail. None of them is a line of text on the card.
  const body = d.components.filter((c) => !["type", "role", "image"].includes(c.kind));
  if (lines >= body.length) return { kept: body, dropped: [] };
  const order = body
    .map((c, i) => ({ c, i }))
    .sort((a, b) => b.c.gain - a.c.gain || a.i - b.i);
  const keep = new Set(order.slice(0, lines).map((x) => x.i));
  return {
    kept: body.filter((_, i) => keep.has(i)),
    dropped: body.filter((_, i) => !keep.has(i)),
  };
}

// refs/abbreviations.json: "A render uses the longest form that fits. `short` exists for the
// floor form, not as a default."
//
// ONE TERM AT A TIME. Daniel, turn 36: the first version "went from zero abbreviated words to 2
// abbreviated words without testing whether one abbreviated word would make it fit". So this
// yields candidates in order of increasing abbreviation: each step shortens ONE more occurrence,
// the one that saves the most characters, first to its medium form and only then, again one at a
// time, to its short form. The render takes the first candidate that fits.
//
// Capitals are kept: a replacement for a capitalised word is capitalised, and a medium form that
// differs from the term only in case ("legal entity") is no change at all.
export type Tier = "full" | "medium" | "short";

interface Occ { start: number; end: number; term: string; tier: 0 | 1 | 2 }

function withCase(original: string, repl: string): string {
  if (repl !== repl.toLowerCase()) return repl;            // already carries its own capitals (ECR, LE)
  return /^[A-Z]/.test(original) ? repl[0].toUpperCase() + repl.slice(1) : repl;
}

export function abbreviations(text: string, lex: Record<string, { medium: string; short: string }>): string[] {
  const occ: Occ[] = [];
  const taken = new Array(text.length).fill(false);
  for (const term of Object.keys(lex).sort((a, b) => b.length - a.length)) {
    const esc = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    for (const m of text.matchAll(new RegExp(`\\b${esc}\\b`, "gi"))) {
      const s0 = m.index!, e0 = s0 + m[0].length;
      if (taken.slice(s0, e0).some(Boolean)) continue;
      taken.fill(true, s0, e0);
      occ.push({ start: s0, end: e0, term, tier: 0 });
    }
  }
  const render = () => {
    let out = "", at = 0;
    for (const o of [...occ].sort((a, b) => a.start - b.start)) {
      const orig = text.slice(o.start, o.end);
      const form = o.tier === 0 ? orig : withCase(orig, o.tier === 1 ? lex[o.term].medium : lex[o.term].short);
      out += text.slice(at, o.start) + form;
      at = o.end;
    }
    return out + text.slice(at);
  };
  const out = [text];
  for (const tier of [1, 2] as const) {
    for (;;) {
      const current = render();
      let best: Occ | null = null, bestLen = current.length;
      for (const o of occ) {
        if (o.tier >= tier) continue;   // a term whose medium form saves nothing can still go to short
        const was = o.tier; o.tier = tier;
        const len = render().length;
        o.tier = was;
        if (len < bestLen) { best = o; bestLen = len; }
      }
      if (!best) break;
      best.tier = tier;
      out.push(render());
    }
  }
  return out;
}
