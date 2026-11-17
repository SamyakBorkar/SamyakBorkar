"""Generate the self-hosted SVG cards for the SamyakBorkar profile README.

Usage: python3 scripts/gen_cards.py assets
Edit the data lists below and re-run to refresh the cards.
"""
import sys
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)

BG, BORDER, TILE = "#1a1b27", "#2a2e42", "#232539"
TITLE, TEXT, MUTED = "#70a5fd", "#c0caf5", "#7a82a8"
TEAL, PURPLE, ORANGE, PINK = "#38bdae", "#bf91f3", "#e0af68", "#f7768e"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"

LANG_COLORS = {
    "Go": "#00ADD8", "C++": "#f34b7d", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Elixir": "#6e4a7e", "HTML": "#e34c26", "CSS": "#663399",
}


def svg(w, h, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<style>
  .t {{ font: 600 18px {FONT}; fill: {TITLE}; }}
  .h {{ font: 600 15px {FONT}; fill: {TEXT}; }}
  .s {{ font: 400 13px {FONT}; fill: {TEXT}; }}
  .m {{ font: 400 12px {FONT}; fill: {MUTED}; }}
  .b {{ font: 700 26px {FONT}; }}
  .chip {{ font: 600 11px {FONT}; }}
</style>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
{body}
</svg>
"""


def chip(x, y, text, color):
    w = 14 + 6.6 * len(text)
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="{color}" fill-opacity=".15" stroke="{color}" stroke-opacity=".5"/>'
            f'<text x="{x + w/2:.0f}" y="{y+14}" text-anchor="middle" class="chip" fill="{color}">{escape(text)}</text>'), w


def chips(x, y, items):
    out = []
    for label, color in items:
        c, w = chip(x, y, label, color)
        out.append(c)
        x += w + 6
    return "".join(out)


# ---------- Experience: vertical timeline ----------
COMPANY = ("Credibl", "Pune, India")
ROLES = [  # title, dates, bullet lines, current?
    ("Software Engineer", "Jul 2026 – Present", [
        "Own the core request generation engine (Elixir + PostgreSQL) for every resource",
        "type; replaced on-the-fly generation and resolved a production outage it caused.",
        "Built user management (roles, access, lifecycle) and reworked CSM onboarding tools.",
    ], True),
    ("Software Engineer Intern", "Jan 2026 – Jun 2026", [
        "Created a real-time Live Warehouse Manager with Phoenix LiveView dashboards,",
        "cutting manual inventory tracking effort by 30%; integrated 5+ REST APIs.",
        "Learned Elixir and shipped a production feature in 2 weeks → full-time offer.",
    ], False),
]
STACK = [("Elixir", PURPLE), ("Phoenix LiveView", "#FD4F00"), ("PostgreSQL", "#4f8fd6"), ("REST APIs", TEAL)]
W = 840
H = 96 + sum(30 + 19 * len(r[2]) + 18 for r in ROLES) + 6
b = [f'<text x="28" y="40" class="t">{escape(COMPANY[0])}</text>',
     f'<text x="28" y="60" class="m">{escape(COMPANY[1])}</text>']
cx = W - 28
for label, color in reversed(STACK):
    c, cw = chip(0, 0, label, color)
    cx -= cw
    b.append(f'<g transform="translate({cx:.0f},26)">{c}</g>')
    cx -= 6
y = 96
line_top = y + 4
for title, dates, lines, current in ROLES:
    dot = TEAL if current else TITLE
    b.append(f'<circle cx="36" cy="{y}" r="7" fill="{BG}" stroke="{dot}" stroke-width="3"/>')
    b.append(f'<text x="58" y="{y+5}" class="h">{escape(title)}</text>'
             f'<text x="{W-28}" y="{y+5}" text-anchor="end" class="m">{escape(dates)}</text>')
    if current:
        c, _ = chip(0, 0, "● current", TEAL)
        b.append(f'<g transform="translate({58 + 8.6*len(title) + 10:.0f},{y-10})">{c}</g>')
    for i, line in enumerate(lines):
        b.append(f'<text x="58" y="{y + 30 + 19*i}" class="s">{escape(line)}</text>')
    y += 30 + 19 * len(lines) + 18
b.insert(2, f'<line x1="36" y1="{line_top}" x2="36" y2="{y - 48 - 19*len(ROLES[-1][2])}" stroke="{BORDER}" stroke-width="2"/>')
(OUT / "experience.svg").write_text(svg(W, H, "\n".join(b), "Experience at Credibl"), encoding="utf-8")


# ---------- Achievements & leadership: stat tiles ----------
TILES = [  # big number, label line 1, label line 2, color
    ("1,500+", "participants hosted", "Rmageddon 2024–25", TEAL),
    ("100+", "students led across", "6+ committees", TITLE),
    ("500+", "DSA problems solved", "LeetCode · GFG · CF", ORANGE),
    ("SIH", "Smart India Hackathon", "cleared internal round", PURPLE),
]
W, H = 840, 150
b = [f'<text x="28" y="34" class="h">Coordinator, Rmageddon 2024–25 · SGGSIE&amp;T</text>',
     f'<text x="{W-28}" y="34" text-anchor="end" class="m">hosted Robowars, a first for the Marathwada region</text>']
tw = (W - 56 - 3 * 12) / 4
for i, (big, l1, l2, color) in enumerate(TILES):
    x = 28 + i * (tw + 12)
    b.append(f'<rect x="{x:.0f}" y="50" width="{tw:.0f}" height="78" rx="8" fill="{TILE}"/>'
             f'<rect x="{x:.0f}" y="50" width="4" height="78" rx="2" fill="{color}"/>'
             f'<text x="{x+18:.0f}" y="84" class="b" style="fill:{color}">{escape(big)}</text>'
             f'<text x="{x+18:.0f}" y="104" class="s">{escape(l1)}</text>'
             f'<text x="{x+18:.0f}" y="120" class="m">{escape(l2)}</text>')
(OUT / "achievements.svg").write_text(svg(W, H, "\n".join(b), "Achievements and leadership"), encoding="utf-8")


# ---------- Project cards ----------
PROJECTS = [  # slug, name, description lines, chips, language bytes, meta, badge
    ("eco-apt", "Eco-APT",
     ["Smarter Go CLI package manager for Debian-based Linux:", "better dependency resolution, P2P dependency sharing",
      "and pre-install storage checks (−25% download time)."],
     [("Go", "#00ADD8"), ("Linux", ORANGE), ("P2P", TEAL), ("CLI", PURPLE)],
     {"Go": 10729}, "", "in progress"),
    ("smarthr", "SmartHR Portal",
     ["MERN employee management system: JWT + RBAC,", "Dockerized services, and a RAG chatbot (LangChain",
      "+ Ollama) that answers HR policy questions."],
     [("React", "#61DAFB"), ("Node", "#8CC84B"), ("Docker", "#2496ED"), ("LangChain", TEAL)],
     {"JavaScript": 53280, "HTML": 359, "CSS": 22}, "★ 1", "live demo"),
    ("collab-todo", "Collaborative Todo · LiveView",
     ["Real-time multi-user task manager: updates sync", "instantly over WebSockets with Phoenix LiveView,",
      "persisted in PostgreSQL via Ecto."],
     [("Elixir", PURPLE), ("Phoenix", "#FD4F00"), ("PostgreSQL", "#4f8fd6")],
     {"Elixir": 80088, "HTML": 15239, "CSS": 4120, "JavaScript": 3145}, "", None),
    ("quadcopter", "QuadCopter",
     ["Custom-built drone with no off-the-shelf flight", "controller: ESP32 + MPU6050 IMU stabilization,",
      "BLDC motors, ESCs and a FlySky RF link."],
     [("ESP32", "#e7352c"), ("MPU6050", TEAL), ("Embedded", PURPLE)],
     {"C++": 23588}, "★ 2  ·  ⑂ 1", None),
]
CW, CH = 420, 190
for slug, name, lines, tags, langs, meta, badge in PROJECTS:
    b = [f'<text x="22" y="36" class="t">{escape(name)}</text>']
    if badge:
        c, cw = chip(0, 0, "● " + badge, TEAL)
        b.append(f'<g transform="translate({CW - 22 - cw:.0f},20)">{c}</g>')
    for i, line in enumerate(lines):
        b.append(f'<text x="22" y="{62 + i*19}" class="s">{escape(line)}</text>')
    b.append(chips(22, 126, tags))
    total = sum(langs.values())
    lx, barw = 22, CW - 44
    b.append(f'<clipPath id="r"><rect x="22" y="158" width="{barw}" height="6" rx="3"/></clipPath><g clip-path="url(#r)">')
    for lang, n in langs.items():
        w = barw * n / total
        b.append(f'<rect x="{lx:.1f}" y="158" width="{w:.1f}" height="6" fill="{LANG_COLORS.get(lang, MUTED)}"/>')
        lx += w
    b.append('</g>')
    top = max(langs, key=langs.get)
    b.append(f'<circle cx="27" cy="178" r="5" fill="{LANG_COLORS.get(top, MUTED)}"/>'
             f'<text x="38" y="182" class="m">{escape(top)} {100*langs[top]/total:.0f}%</text>')
    if meta:
        b.append(f'<text x="{CW-22}" y="182" text-anchor="end" class="m">{escape(meta)}</text>')
    (OUT / f"project-{slug}.svg").write_text(svg(CW, CH, "\n".join(b), name), encoding="utf-8")

print("\n".join(sorted(p.name for p in OUT.iterdir())))
