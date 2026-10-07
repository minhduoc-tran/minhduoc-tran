"""Generate the light/dark SVG cards used in README.md.

Run `python3 scripts/build_assets.py` after editing the content below.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 854
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#09090b", panel="#111114", border="#27272a", fg="#fafafa", muted="#a1a1aa",
                 subtle="#71717a", grid="#27272a", accent="#60a5fa", green="#4ade80",
                 kw="#c084fc", str="#86efac", prop="#93c5fd", chip="#18181b", glow="#1d4ed8"),
    "light": dict(bg="#ffffff", panel="#fafafa", border="#e4e4e7", fg="#09090b", muted="#52525b",
                  subtle="#a1a1aa", grid="#e4e4e7", accent="#2563eb", green="#16a34a",
                  kw="#9333ea", str="#15803d", prop="#1d4ed8", chip="#f4f4f5", glow="#93c5fd"),
}

BASE_CSS = """
.in { animation: in .7s cubic-bezier(.2,.7,.2,1) both; }
@keyframes in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.blink { animation: blink 1.1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
.pulse { animation: pulse 2s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes pulse { from { opacity: .6; transform: scale(1); } to { opacity: 0; transform: scale(3); } }
"""


def text_width(s, size, mono=False):
    """Rough advance width; good enough to size chips for these fonts."""
    if mono:
        return len(s) * size * 0.6
    narrow, wide = set("il.,:;'|!·() "), set("MWmw")
    return sum(size * (0.3 if c in narrow else 0.82 if c in wide else 0.62 if c.isupper() else 0.54) for c in s)


def svg(h, t, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{escape(label)}">
<style>{BASE_CSS}
.sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
</style>
<defs>
  <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t['grid']}"/></pattern>
  <radialGradient id="fade" cx=".3" cy=".3" r=".8"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="m"><rect width="{W}" height="{h}" fill="url(#fade)"/></mask>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t['glow']}" stop-opacity=".18"/><stop offset="1" stop-color="{t['glow']}" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{h}" fill="{t['bg']}"/>
  <rect width="{W}" height="{h}" fill="url(#dots)" mask="url(#m)"/>
{body}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="14" fill="none" stroke="{t['border']}"/>
</svg>
"""


def chip(x, y, label, t, size=12, mono=False, color=None):
    w = text_width(label, size, mono) + 20
    cls = "mono" if mono else "sans"
    return w, (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{t["chip"]}" stroke="{t["border"]}"/>'
               f'<text x="{x + w / 2:.0f}" y="{y + 16}" text-anchor="middle" class="{cls}" font-size="{size}" '
               f'fill="{color or t["muted"]}">{escape(label)}</text>')


def chips(x, y, labels, t, gap=8, **kw):
    out = []
    for label in labels:
        w, s = chip(x, y, label, t, **kw)
        out.append(s)
        x += w + gap
    return "\n".join(out)


def hero(t):
    code = [  # (indent, [(text, colour key)])
        (0, [("export const ", "kw"), ("duoc", "fg"), (" = {", "subtle")]),
        (1, [("role", "prop"), (": ", "subtle"), ('"Web Developer"', "str"), (",", "subtle")]),
        (1, [("location", "prop"), (": ", "subtle"), ('"Cần Thơ, VN"', "str"), (",", "subtle")]),
        (1, [("stack", "prop"), (": [", "subtle"), ('"React"', "str"), (", ", "subtle"), ('"Next.js"', "str"), (", ", "subtle"), ('"TS"', "str"), ("],", "subtle")]),
        (1, [("building", "prop"), (": ", "subtle"), ('"tablecn"', "str"), (",", "subtle")]),
        (0, [("};", "subtle")]),
    ]
    px, py, pw, ph = 474, 36, 344, 208
    lines = []
    for i, (indent, parts) in enumerate(code):
        y = py + 66 + i * 23
        spans = "".join(f'<tspan fill="{t[k]}">{escape(s)}</tspan>' for s, k in parts)
        lines.append(f'<g class="in" style="animation-delay:{.35 + i * .12:.2f}s">'
                     f'<text x="{px + 16}" y="{y}" class="mono" font-size="11.5" fill="{t["subtle"]}" opacity=".6">{i + 1}</text>'
                     f'<text x="{px + 38 + indent * 14}" y="{y}" class="mono" font-size="12.5">{spans}</text></g>')
    cursor_y = py + 66 + (len(code) - 1) * 23
    body = f"""
  <ellipse cx="640" cy="140" rx="300" ry="160" fill="url(#glow)"/>
  <g class="in">
    <text x="44" y="78" class="mono" font-size="13" fill="{t['subtle']}">~/minhduoc-tran</text>
    <text x="42" y="126" class="sans" font-size="42" font-weight="700" fill="{t['fg']}" letter-spacing="-1">Tran Minh Duoc</text>
  </g>
  <g class="in" style="animation-delay:.15s">
    <text x="44" y="162" class="sans" font-size="16" fill="{t['muted']}">Web developer building data-heavy interfaces</text>
    <text x="44" y="185" class="sans" font-size="16" fill="{t['muted']}">with React, Next.js and TypeScript.</text>
  </g>
  <g class="in" style="animation-delay:.3s">
    <circle class="pulse" cx="52" cy="226" r="4" fill="{t['green']}"/>
    <circle cx="52" cy="226" r="4" fill="{t['green']}"/>
    <text x="64" y="230" class="sans" font-size="13" fill="{t['muted']}">Building <tspan fill="{t['fg']}" font-weight="600">tablecn</tspan>  ·  Cần Thơ, Việt Nam</text>
  </g>
  <g class="in" style="animation-delay:.2s">
    <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{t['panel']}" stroke="{t['border']}"/>
    <line x1="{px}" y1="{py + 34}" x2="{px + pw}" y2="{py + 34}" stroke="{t['border']}"/>
    <circle cx="{px + 18}" cy="{py + 17}" r="4.5" fill="{t['border']}"/>
    <circle cx="{px + 33}" cy="{py + 17}" r="4.5" fill="{t['border']}"/>
    <circle cx="{px + 48}" cy="{py + 17}" r="4.5" fill="{t['border']}"/>
    <text x="{px + pw / 2}" y="{py + 21}" text-anchor="middle" class="mono" font-size="11.5" fill="{t['subtle']}">about.ts</text>
  </g>
  {"".join(lines)}
  <rect class="blink" x="{px + 58}" y="{cursor_y - 11}" width="7" height="14" fill="{t['accent']}"/>"""
    return svg(280, t, body, "Tran Minh Duoc, web developer from Cần Thơ, Việt Nam")


def project(t):
    rows = [("Nguyễn Văn An", "Paid", "42.00"), ("Trần Thị Bình", "Paid", "38.50"),
            ("Lê Hoàng Nam", "Paid", "27.90"), ("Phạm Minh Thư", "Paid", "15.00")]
    mx, my, mw = 474, 32, 344
    table = []
    for i, (name, status, amount) in enumerate(rows):
        y = my + 128 + i * 30
        table.append(f'<g class="in" style="animation-delay:{.5 + i * .1:.1f}s">'
                     f'<line x1="{mx}" y1="{y - 19}" x2="{mx + mw}" y2="{y - 19}" stroke="{t["border"]}"/>'
                     f'<text x="{mx + 16}" y="{y}" class="sans" font-size="12.5" fill="{t["fg"]}">{name}</text>'
                     f'<rect x="{mx + 180}" y="{y - 13}" width="44" height="18" rx="9" fill="{t["green"]}" fill-opacity=".14"/>'
                     f'<text x="{mx + 202}" y="{y}" text-anchor="middle" class="sans" font-size="11" fill="{t["green"]}">{status}</text>'
                     f'<text x="{mx + mw - 16}" y="{y}" text-anchor="end" class="mono" font-size="12" fill="{t["muted"]}">{amount}</text></g>')
    _, f1 = chip(mx + 12, my + 46, "Status is Paid", t, size=11.5, color=t["fg"])
    _, f2 = chip(mx + 124, my + 46, "Amount 10 – 50", t, size=11.5, color=t["fg"])
    body = f"""
  <ellipse cx="646" cy="130" rx="260" ry="150" fill="url(#glow)"/>
  <g class="in">
    <text x="44" y="68" class="mono" font-size="11.5" fill="{t['accent']}" letter-spacing="1.5">FEATURED PROJECT</text>
    <text x="42" y="108" class="sans" font-size="32" font-weight="700" fill="{t['fg']}" letter-spacing="-.8">tablecn</text>
    <text x="44" y="140" class="sans" font-size="15" fill="{t['muted']}">Open-source data table blocks for shadcn/ui.</text>
    <text x="44" y="162" class="sans" font-size="15" fill="{t['muted']}">Filter, search, sort and page, all in the URL.</text>
  </g>
  <g class="in" style="animation-delay:.15s">
{chips(44, 188, ["TanStack Table", "shadcn registry", "Radix · Base UI · React Aria"], t)}
  </g>
  <g class="in" style="animation-delay:.3s">
    <text x="44" y="252" class="sans" font-size="13" fill="{t['subtle']}"><tspan fill="{t['fg']}" font-weight="600">4</tspan> npm packages   ·   <tspan fill="{t['fg']}" font-weight="600">15</tspan> filter operators   ·   <tspan fill="{t['fg']}" font-weight="600">EN / VI</tspan></text>
  </g>
  <g class="in" style="animation-delay:.2s">
    <rect x="{mx}" y="{my}" width="{mw}" height="236" rx="10" fill="{t['panel']}" stroke="{t['border']}"/>
    <text x="{mx + 14}" y="{my + 22}" class="mono" font-size="11" fill="{t['subtle']}">?status__eq=paid&amp;sort=-amount</text>
    <line x1="{mx}" y1="{my + 34}" x2="{mx + mw}" y2="{my + 34}" stroke="{t['border']}"/>
    {f1}{f2}
    <text x="{mx + 16}" y="{my + 100}" class="sans" font-size="11" font-weight="600" fill="{t['subtle']}">NAME</text>
    <text x="{mx + 180}" y="{my + 100}" class="sans" font-size="11" font-weight="600" fill="{t['subtle']}">STATUS</text>
    <text x="{mx + mw - 16}" y="{my + 100}" text-anchor="end" class="sans" font-size="11" font-weight="600" fill="{t['subtle']}">AMOUNT ↓</text>
  </g>
  {"".join(table)}"""
    return svg(300, t, body, "tablecn: open-source data table blocks for shadcn/ui")


def stack(t):
    groups = [
        ("FRONTEND", ["React", "Next.js", "Tailwind CSS", "TanStack", "Vue", "Angular", "Redux"]),
        ("BACKEND", [".NET", "Spring Boot", "FastAPI", "Node.js"]),
        ("DATA", ["PostgreSQL", "SQL Server", "MySQL", "MongoDB"]),
        ("LANGUAGES", ["TypeScript", "JavaScript", "C#", "Java", "Python"]),
    ]
    rows = []
    for i, (label, items) in enumerate(groups):
        y = 64 + i * 42
        rows.append(f'<g class="in" style="animation-delay:{i * .1:.1f}s">'
                    f'<text x="44" y="{y + 16}" class="mono" font-size="11.5" fill="{t["subtle"]}" letter-spacing="1.5">{label}</text>'
                    f'{chips(160, y, items, t, size=12.5, color=t["fg"])}</g>')
    body = f"""
  <text x="44" y="40" class="mono" font-size="11.5" fill="{t['accent']}" letter-spacing="1.5">TOOLBOX</text>
  {"".join(rows)}"""
    return svg(236, t, body, "Tech stack")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in {"hero": hero, "project-tablecn": project, "stack": stack}.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print("built", sorted(p.name for p in OUT.glob("*.svg")))
