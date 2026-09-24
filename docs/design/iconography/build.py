"""Build arcviz's category glyphs from the vendored sources beside this file.

Every glyph is one flattened path on a 24-unit grid, filled with currentColor. Vendored glyphs are
copied unmodified into sources/, and every change made to them happens here, in code, so the
modification each licence asks us to disclose is exactly what this file does.

Run from this directory (needs rsvg-convert on PATH for the sheets):

    uv run --with picosvg --with skia-pathops --with pillow python build.py
"""
import io
import pathlib
import re
import subprocess

from picosvg import svg_pathops as ops
from picosvg.svg import SVG
from picosvg.svg_transform import Affine2D
from picosvg.svg_types import SVGCircle, SVGEllipse, SVGPath, SVGPolygon, SVGRect
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).parent
SRC = HERE / "sources"
GRID = 24  # viewBox is 0 0 24 24
LIVE = 22  # the larger dimension of a square-ish glyph; one unit of clear space on every side
LIVE_MAX = 23.5  # wide glyphs may grow toward the edge, never touch it


# --- geometry -----------------------------------------------------------------
def cmds(shape):
    return list(shape.as_cmd_seq())


def union(*seqs):
    return list(ops.union(list(seqs), ["nonzero"] * len(seqs)))


def diff(a, *bs):
    return list(ops.difference([a, *bs], ["nonzero"] * (1 + len(bs))))


def dilate(seq, w):
    return union(seq, list(ops.stroke(seq, "round", "round", 2 * w, 4, 0.05)))


def circle(cx, cy, r):
    return cmds(SVGCircle(cx=cx, cy=cy, r=r))


def rect(x, y, w, h, r=0):
    return cmds(SVGRect(x=x, y=y, width=w, height=h, rx=r, ry=r))


def poly(*pts):
    return cmds(SVGPolygon(points=" ".join(f"{x},{y}" for x, y in pts)))


def ring(cx, cy, r_out, r_in):
    return diff(circle(cx, cy, r_out), circle(cx, cy, r_in))


def transform(seq, a):
    return cmds(SVGPath.from_commands(seq).apply_transform(a))


def move(seq, dx, dy, s=1.0):
    return transform(seq, Affine2D.identity().translate(dx, dy).scale(s))


def bbox(seq):
    return SVGPath.from_commands(seq).bounding_box()


def load(path):
    """Every painted shape in a source SVG, unioned into one command sequence."""
    txt = pathlib.Path(path).read_text()
    txt = re.sub(r"<clipPath.*?</clipPath>", "", txt)
    txt = re.sub(r' clip-path="[^"]*"', "", txt)
    txt = re.sub(r'<path[^>]*fill-opacity="0.0"[^>]*/>', "", txt)
    return union(*[cmds(s) for s in SVG.fromstring(txt).topicosvg().shapes()])


def subpaths(seq):
    out = []
    for c in cmds(SVGPath.from_commands(seq).absolute()):
        if c[0] == "M":
            out.append([])
        out[-1].append(c)
    return out


def raw(path):
    """The single path of a one-path source, unflattened, so its subpaths can be edited."""
    return cmds(SVGPath(d=re.search(r' d="([^"]+)"', pathlib.Path(path).read_text()).group(1)))


def fit(seq):
    """Centre on the grid. The larger dimension is LIVE, grown slightly for wide glyphs, which
    otherwise look small beside square ones at equal width (a mild optical correction)."""
    b = bbox(seq)
    aspect = max(b.w, b.h) / min(b.w, b.h)
    live = min(LIVE_MAX, LIVE * aspect**0.2)
    s = live / max(b.w, b.h)
    a = Affine2D.identity().translate(GRID / 2, GRID / 2).scale(s).translate(-(b.x + b.w / 2), -(b.y + b.h / 2))
    return transform(seq, a)


# --- modified vendored glyphs --------------------------------------------------
def person():
    """Phosphor person, head lowered 10/256 so it no longer floats off the body."""
    head, body = subpaths(raw(SRC / "phosphor/person-fill.svg"))
    return union(move(head, 0, 10), body)


def affiliation():
    """Phosphor users-three with both back figures rebuilt from the front bust. The right one is
    smaller (0.7) and higher, to break the symmetry; busts rather than full figures, because an
    affiliation can be with something that is not a person."""
    left, right, centre = subpaths(raw(SRC / "phosphor/users-three-fill.svg"))
    c = bbox(centre)

    def bust(s, cx, top):
        return transform(centre, Affine2D.identity().translate(cx, top).scale(s).translate(-(c.x + c.w / 2), -c.y))

    lb, rb = bbox(left), bbox(right)
    gap = dilate(centre, 8)
    return union(diff(bust(0.8, lb.x + lb.w / 2 - 4, lb.y), gap), diff(bust(0.7, rb.x + rb.w / 2 + 4, rb.y - 12), gap), centre)


def age():
    """Three life stages, built from the modified humanness figure, overlapping with a cut gap."""
    fig = person()
    out = []
    for s, x in ((0.55, 0), (0.75, 85), (0.97, 185)):
        g = transform(fig, Affine2D.identity().translate(x, 240 * (1 - s)).scale(s))
        out = union(diff(out, dilate(g, 9)), g) if out else g
    return out


# --- originals -------------------------------------------------------------------
def temple():
    """After Daniel's sketch (sources/daniel/org-icon.svg): pediment, entablature, four columns,
    stepped base. Five columns fall below the minimum gap at 32 px; three read as a gate."""
    parts = [poly((12, 2.5), (22.5, 7), (1.5, 7)), rect(2.5, 8.2, 19, 1.8), rect(1.5, 19.3, 21, 1.6), rect(0.5, 21, 23, 1.6)]
    cols, span, w = 4, 17, 2.4
    gap = (span - cols * w) / (cols - 1)
    parts += [rect(3.5 + i * (w + gap), 11.2, w, 7) for i in range(cols)]
    return union(*parts)


def marriage():
    """A solitaire: thick band, unfaceted stone, a small setting joining them."""
    band = ring(12, 14.5, 7.5, 4.8)
    stone = poly((9, 4.6), (15, 4.6), (16.8, 6.6), (12, 11), (7.2, 6.6))
    setting = poly((10.3, 8.5), (13.7, 8.5), (12.9, 7.2), (11.1, 7.2))
    return union(diff(band, dilate(stone, 0.9)), stone, setting)


# --- the set ---------------------------------------------------------------------
def file_blank():
    """`misc` with its two text lines removed, so a renderer can print a file extension on the
    page instead. Daniel, 2026-09-24, choosing it over a picture pictograph for photographs:
    "We already show the actual photo, so having an icon for a photo isn't important." The
    extension is text laid over the glyph by the renderer, never part of the path, so the glyph
    stays one silhouette in currentColor."""
    keep = [s for s in subpaths(raw(SRC / "material-symbols/description-fill.svg"))
            if abs(s[0][1][0] - 349) > 0.5]   # the two lines both start at x=349
    return union(*keep)


# name -> (builder, <title>, credit). The credit is written into the glyph as a comment, because
# Apache-2.0 asks modified files to say they were changed and CC BY asks for it at point of use.
# None means an arcviz original.
GLYPHS = {
    "identity": (lambda: load(SRC / "phosphor/identification-badge-fill.svg"), "identity", "Phosphor Icons 'identification-badge' (fill), MIT; rescaled and centred on a 24-unit grid"),
    "identity.travel": (lambda: load(SRC / "material-symbols/flight-fill.svg"), "identity: travel", "Material Symbols 'flight' (rounded, fill), Apache-2.0; rescaled and centred on a 24-unit grid"),
    "identity.age": (age, "identity: age", "built from Phosphor Icons 'person' (fill), MIT; head lowered, three scaled copies overlapped"),
    "identity.address": (lambda: load(SRC / "phosphor/house-fill.svg"), "identity: address", "Phosphor Icons 'house' (fill), MIT; rescaled and centred on a 24-unit grid"),
    "org-identity": (temple, "org-identity", None),
    "humanness": (person, "humanness", "Phosphor Icons 'person' (fill), MIT; head lowered 10/256, rescaled to a 24-unit grid"),
    "financial": (lambda: load(SRC / "font-awesome/money-bill-wave.svg"), "financial", "Font Awesome Free 'money-bill-wave' (solid), CC BY 4.0; rescaled and centred on a 24-unit grid"),
    "financial.tax": (lambda: load(SRC / "phosphor/receipt-fill.svg"), "financial: tax", "Phosphor Icons 'receipt' (fill), MIT; rescaled and centred on a 24-unit grid"),
    "financial.insurance": (lambda: load(SRC / "fluent/umbrella_24_filled.svg"), "financial: insurance", "Fluent UI System Icons 'umbrella', MIT; rescaled and centred on a 24-unit grid"),
    "qualification": (lambda: load(SRC / "phosphor/medal-fill.svg"), "qualification", "Phosphor Icons 'medal' (fill), MIT; rescaled and centred on a 24-unit grid"),
    "qualification.academic": (lambda: load(SRC / "font-awesome/graduation-cap.svg"), "qualification: academic", "Font Awesome Free 'graduation-cap' (solid), CC BY 4.0; rescaled and centred on a 24-unit grid"),
    "qualification.driving": (lambda: load(SRC / "material-symbols/directions_car-fill.svg"), "qualification: driving", "Material Symbols 'directions_car' (rounded, fill), Apache-2.0; rescaled and centred on a 24-unit grid"),
    "health": (lambda: load(SRC / "material-symbols/ecg_heart-fill.svg"), "health", "Material Symbols 'ecg_heart' (rounded, fill), Apache-2.0; rescaled and centred on a 24-unit grid"),
    "affiliation": (affiliation, "affiliation", "Phosphor Icons 'users-three' (fill), MIT; back figures rebuilt from the front bust, right one smaller and higher, rescaled to a 24-unit grid"),
    "authority.delegation": (lambda: load(SRC / "font-awesome/sitemap.svg"), "authority: delegation", "Font Awesome Free 'sitemap' (solid), CC BY 4.0; rescaled and centred on a 24-unit grid"),
    "authority.control": (lambda: load(SRC / "font-awesome/key.svg"), "authority: control", "Font Awesome Free 'key' (solid), CC BY 4.0; rescaled and centred on a 24-unit grid"),
    "civil-status.birth": (lambda: load(SRC / "phosphor/baby-fill.svg"), "civil-status: birth", "Phosphor Icons 'baby' (fill), MIT; rescaled and centred on a 24-unit grid"),
    "civil-status.marriage": (marriage, "civil-status: marriage", None),
    "misc": (lambda: load(SRC / "material-symbols/description-fill.svg"), "misc", "Material Symbols 'description' (rounded, fill), Apache-2.0; rescaled and centred on a 24-unit grid"),
    "misc.file": (file_blank, "misc: file", "Material Symbols 'description' (rounded, fill), Apache-2.0; its two text lines removed, rescaled and centred on a 24-unit grid"),
}


def svg_text(seq, title, credit=None):
    d = SVGPath.from_commands(seq).round_floats(2).d
    note = f"<!-- Derived from {credit}. See ../ATTRIBUTION.md. -->" if credit else "<!-- arcviz original. -->"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRID} {GRID}" fill="currentColor">{note}<title>{title}</title><path d="{d}"/></svg>\n'


def raster(svg, px):
    png = subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px)], input=svg.replace("currentColor", "#000").encode(), capture_output=True, check=True).stdout
    a = Image.open(io.BytesIO(png)).convert("RGBA").getchannel("A")
    im = Image.new("RGB", a.size, "white")
    im.paste((20, 20, 20), (0, 0), a)
    return im


# Real label sets from the catalog, ordered as classify.categories() orders them (identity last).
COMPOSITIONS = [
    ("driving licence", ["qualification.driving", "identity"]),
    ("EU IBAN attestation", ["financial", "identity"]),
    ("PDA1", ["health", "affiliation", "identity"]),
    ("GCD", ["financial", "affiliation", "authority.delegation"]),
    ("four (never observed)", ["health", "financial", "affiliation", "identity"]),
]
# Categories whose own glyph is one of their subcategories' pictures (his ruling, 2026-09-24).
# Written as separate files, with their own <title>, so a renderer looks glyphs up by category name.
ALIASES = {"authority": "authority.control", "civil-status": "civil-status.marriage"}

GAP = 4  # px between adjacent 32 px glyphs: one eighth of the glyph


def main():
    out = HERE / "glyphs"
    out.mkdir(exist_ok=True)
    svgs = {}
    for name, (build, title, credit) in GLYPHS.items():
        svgs[name] = svg_text(fit(build()), title, credit)
        (out / f"{name}.svg").write_text(svgs[name])
    for alias, target in ALIASES.items():
        build, title, credit = GLYPHS[target]
        (out / f"{alias}.svg").write_text(svg_text(fit(build()), alias, credit))

    font = ImageFont.load_default(size=13)
    names = list(GLYPHS)

    # contact sheet: every glyph at 32 px, actual size, nothing else
    contact = Image.new("RGB", (len(names) * (32 + 8) + 8, 48), "white")
    for i, n in enumerate(names):
        contact.paste(raster(svgs[n], 32), (8 + i * 40, 8))
    contact.save(HERE / "contact-32.png")

    # ladder: 32 / 64 / 128 per glyph, labelled
    cols = 4
    cw, rh = 250, 160
    ladder = Image.new("RGB", (cols * cw, ((len(names) + cols - 1) // cols) * rh), "white")
    dr = ImageDraw.Draw(ladder)
    for i, n in enumerate(names):
        x, y = (i % cols) * cw + 8, (i // cols) * rh + 8
        ladder.paste(raster(svgs[n], 32), (x, y + 96))
        ladder.paste(raster(svgs[n], 64), (x + 40, y + 64))
        ladder.paste(raster(svgs[n], 128), (x + 112, y))
        dr.text((x, y + 134), n, fill="black", font=font)
    ladder.save(HERE / "ladder.png")

    # composition: real multi-category label sets at 32 px
    comp = Image.new("RGB", (400, len(COMPOSITIONS) * 48 + 8), "white")
    dr = ImageDraw.Draw(comp)
    for j, (label, row) in enumerate(COMPOSITIONS):
        y = 8 + j * 48
        for i, n in enumerate(row):
            comp.paste(raster(svgs[n], 32), (8 + i * (32 + GAP), y))
        dr.text((8 + 4 * (32 + GAP) + 12, y + 10), label, fill="black", font=font)
    comp.save(HERE / "composition-32.png")


if __name__ == "__main__":
    main()
