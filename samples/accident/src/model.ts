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
// floor form, not as a default." Whole words only, longest term first so "legal entity" wins
// over any shorter term inside it.
export type Tier = "full" | "medium" | "short";
export function abbreviate(text: string, lex: Data["abbreviations"], tier: Tier): string {
  if (tier === "full") return text;
  let out = text;
  for (const term of Object.keys(lex).sort((a, b) => b.length - a.length)) {
    const esc = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    out = out.replace(new RegExp(`\\b${esc}\\b`, "gi"), lex[term][tier]);
  }
  return out;
}
