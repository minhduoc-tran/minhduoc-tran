"""Generate the animated light/dark header used at the top of README.md.

Run `python3 scripts/build_header.py` after editing the content below.
The background is transparent and fades out at its edges, so the header
blends into GitHub's page instead of sitting in a box.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W, H = 854, 300
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

NAME = "Tran Minh Duoc"
TYPED = "building data-heavy UIs with React & Next.js"
STATUS = "Web developer  ·  Cần Thơ, Việt Nam"

THEMES = {
    "dark": dict(fg="#fafafa", muted="#a1a1aa", subtle="#52525b", accent="#60a5fa", green="#4ade80",
                 name_to="#93c5fd", blob=.34, bar="#27272a", bar_hi="#3f3f46", chip="#60a5fa"),
    "light": dict(fg="#09090b", muted="#52525b", subtle="#a1a1aa", accent="#2563eb", green="#16a34a",
                  name_to="#2563eb", blob=.32, bar="#e4e4e7", bar_hi="#d4d4d8", chip="#2563eb"),
}

TYPE_SECONDS = 2.6
CSS = f"""
.sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}
.in {{ animation: in .8s cubic-bezier(.2,.7,.2,1) both; }}
@keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
.drift-a {{ animation: drift-a 14s ease-in-out infinite alternate; }}
.drift-b {{ animation: drift-b 18s ease-in-out infinite alternate; }}
.drift-c {{ animation: drift-c 16s ease-in-out infinite alternate; }}
@keyframes drift-a {{ to {{ transform: translate(70px, 30px) scale(1.15); }} }}
@keyframes drift-b {{ to {{ transform: translate(-80px, -20px) scale(.9); }} }}
@keyframes drift-c {{ to {{ transform: translate(40px, -35px) scale(1.1); }} }}
.type {{ animation: type {TYPE_SECONDS}s steps({len(TYPED)}) .9s both; }}
@keyframes type {{ from {{ width: 0; }} }}
.caret {{ animation: follow {TYPE_SECONDS}s steps({len(TYPED)}) .9s both, blink 1s steps(1) {TYPE_SECONDS + .9}s infinite; }}
@keyframes follow {{ from {{ transform: translateX(-{len(TYPED) * 8.4:.1f}px); }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.pulse {{ animation: pulse 2s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
@keyframes pulse {{ from {{ opacity: .7; transform: scale(1); }} to {{ opacity: 0; transform: scale(3); }} }}
.sweep {{ animation: sweep 4.5s cubic-bezier(.6,0,.4,1) 1.2s infinite; }}
@keyframes sweep {{ 0%, 12% {{ transform: translateY(0); }} 30%, 42% {{ transform: translateY(34px); }}
  60%, 72% {{ transform: translateY(102px); }} 90%, 100% {{ transform: translateY(0); }} }}
.float-a {{ animation: float 5s ease-in-out infinite alternate; }}
.float-b {{ animation: float 6s ease-in-out 1s infinite alternate-reverse; }}
@keyframes float {{ to {{ transform: translateY(-7px); }} }}
"""


def table(t):
    """A frameless, stylised data table: header, rows of bars, a moving highlight."""
    x, y = 520, 92
    widths = [(118, 54, 40), (92, 54, 46), (130, 54, 34), (104, 54, 42), (84, 54, 38)]
    rows = [f'<rect x="{x}" y="{y - 20}" width="{w}" height="6" rx="3" fill="{t["subtle"]}" opacity=".5"/>'
            for x, w in ((x + 12, 46), (x + 168, 38), (x + 268, 30))]
    for i, (a, b, c) in enumerate(widths):
        ry = y + 14 + i * 34
        rows.append(
            f'<g class="in" style="animation-delay:{.4 + i * .1:.1f}s">'
            f'<line x1="{x}" y1="{ry - 17}" x2="{x + 300}" y2="{ry - 17}" stroke="{t["bar"]}"/>'
            f'<rect x="{x + 12}" y="{ry - 4}" width="{a}" height="8" rx="4" fill="{t["bar_hi"]}"/>'
            f'<rect x="{x + 168}" y="{ry - 7}" width="{b}" height="14" rx="7" fill="{t["green"]}" fill-opacity=".18"/>'
            f'<rect x="{x + 300 - 12 - c}" y="{ry - 4}" width="{c}" height="8" rx="4" fill="{t["bar"]}"/></g>')
    chip = lambda cx, cy, label, cls: (  # noqa: E731
        f'<g class="{cls}"><rect x="{cx}" y="{cy}" width="{len(label) * 7 + 22}" height="24" rx="12" '
        f'fill="{t["chip"]}" fill-opacity=".12"/><text x="{cx + 11}" y="{cy + 16}" class="mono" '
        f'font-size="11.5" fill="{t["chip"]}">{escape(label)}</text></g>')
    return f"""
  <g mask="url(#table-fade)">
    {"".join(rows)}
    <rect class="sweep" x="{x - 6}" y="{y - 3}" width="312" height="34" rx="8" fill="{t['accent']}" fill-opacity=".09"/>
  </g>
  {chip(x + 136, y - 64, "status = paid", "float-a")}
  {chip(x + 22, y + 186, "sort: -amount", "float-b")}"""


def header(t):
    caret_x = 44 + len(TYPED) * 8.4 + 4
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(NAME)}, web developer {escape(TYPED)}">
<style>{CSS}</style>
<defs>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
  <radialGradient id="edge" cx=".5" cy=".5" r=".5"><stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="edge-fade"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
  <linearGradient id="row-fade" x1="0" x2="0" y1="0" y2="1"><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="table-fade"><rect width="{W}" height="{H}" fill="url(#row-fade)"/></mask>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{t['fg']}"/><stop offset=".55" stop-color="{t['fg']}"/><stop offset="1" stop-color="{t['name_to']}"/></linearGradient>
  <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t['subtle']}" opacity=".35"/></pattern>
  <clipPath id="typed"><rect class="type" x="44" y="{H / 2 + 8}" width="{len(TYPED) * 8.4 + 2:.0f}" height="24"/></clipPath>
</defs>
<g mask="url(#edge-fade)">
  <g filter="url(#blur)" opacity="{t['blob']}">
    <ellipse class="drift-a" cx="560" cy="110" rx="170" ry="110" fill="#3b82f6"/>
    <ellipse class="drift-b" cx="720" cy="190" rx="150" ry="100" fill="#8b5cf6"/>
    <ellipse class="drift-c" cx="260" cy="200" rx="160" ry="90" fill="#14b8a6"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
</g>
<g class="in">
  <text x="44" y="{H / 2 - 62}" class="mono" font-size="13" fill="{t['accent']}">~/minhduoc-tran</text>
  <text x="41" y="{H / 2 - 12}" class="sans" font-size="46" font-weight="750" letter-spacing="-1.4" fill="url(#name)">{escape(NAME)}</text>
</g>
<text x="44" y="{H / 2 + 26}" class="mono" font-size="14" fill="{t['muted']}" clip-path="url(#typed)" textLength="{len(TYPED) * 8.4:.0f}" lengthAdjust="spacingAndGlyphs">{escape(TYPED)}</text>
<rect class="caret" x="{caret_x:.0f}" y="{H / 2 + 12}" width="8" height="17" fill="{t['accent']}"/>
<g class="in" style="animation-delay:.3s">
  <circle class="pulse" cx="52" cy="{H / 2 + 64}" r="4" fill="{t['green']}"/>
  <circle cx="52" cy="{H / 2 + 64}" r="4" fill="{t['green']}"/>
  <text x="66" y="{H / 2 + 69}" class="sans" font-size="14" fill="{t['muted']}">{escape(STATUS)}</text>
</g>
{table(t)}
</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (OUT / f"header-{theme}.svg").write_text(header(t), encoding="utf-8")
    print("built", sorted(p.name for p in OUT.glob("header-*.svg")))
