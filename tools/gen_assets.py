#!/usr/bin/env python3
"""Generates the animated SVG assets for the YasenMakioui profile README."""
import random
from pathlib import Path
from xml.sax.saxutils import escape

random.seed(42)
OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

MONO = "font-family:'JetBrains Mono','Fira Code','SFMono-Regular',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
GREEN, CYAN, AMBER, BLUE, PINK, PURPLE = "#39d353", "#39c5cf", "#e3b341", "#58a6ff", "#ff7b72", "#bc8cff"
BG, PANEL, BORDER, MUTED, TEXT = "#0d1117", "#161b22", "#30363d", "#8b949e", "#e6edf3"

COMMON_STYLE = f"""
.mono{{{MONO}}}
.led{{animation:blink var(--d,1.2s) steps(2,start) infinite}}
@keyframes blink{{to{{opacity:.12}}}}
.cursor{{animation:blink 1s steps(2,start) infinite}}
"""

GLOW = """<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="2.5" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>"""


def led(cx, cy, color, r=3.2):
    d = random.choice([0.4, 0.7, 0.9, 1.3, 1.8, 2.6])
    delay = round(random.uniform(0, 2), 2)
    return (f'<circle class="led" style="--d:{d}s;animation-delay:{delay}s" '
            f'cx="{cx}" cy="{cy}" r="{r}" fill="{color}" filter="url(#glow)"/>')


def packet(path_id, color, dur, begin, reverse=False, r=3.5):
    kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if reverse else ""
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{begin}s"/>'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"{kp}>'
            f'<mpath href="#{path_id}"/></animateMotion></circle>')


# --------------------------------------------------------------------------- header
def header():
    W, H = 1000, 290
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f"<style>{COMMON_STYLE}</style>",
         "<defs>", GLOW,
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0a1f14"/></linearGradient>',
         '<pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#17271e" stroke-width="1"/></pattern>',
         '<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#e6edf3"/><stop offset="1" stop-color="#7ee787"/></linearGradient>',
         '<clipPath id="cardclip"><rect width="1000" height="290" rx="16"/></clipPath>',
         "</defs>",
         f'<g clip-path="url(#cardclip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         # scanning line
         f'<rect x="0" y="0" width="{W}" height="2" fill="{GREEN}" opacity=".18"><animate attributeName="y" values="0;{H};0" dur="9s" repeatCount="indefinite"/></rect></g>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{BORDER}"/>']

    # rack
    rx, ry, rw, rh = 44, 28, 190, 234
    p.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="6" fill="#0b0f14" stroke="{BORDER}" stroke-width="2"/>')
    p.append(f'<rect x="{rx+8}" y="{ry+8}" width="8" height="{rh-16}" fill="#11161d"/>')
    p.append(f'<rect x="{rx+rw-16}" y="{ry+8}" width="8" height="{rh-16}" fill="#11161d"/>')
    for i in range(0, rh - 20, 9):
        p.append(f'<circle cx="{rx+12}" cy="{ry+14+i}" r="1.2" fill="#2b333d"/><circle cx="{rx+rw-12}" cy="{ry+14+i}" r="1.2" fill="#2b333d"/>')
    uy = ry + 12
    kinds = ["server", "server", "switch", "server", "storage", "server", "ups"]
    for k in kinds:
        h = 26
        ux, uw = rx + 20, rw - 40
        p.append(f'<rect x="{ux}" y="{uy}" width="{uw}" height="{h}" rx="3" fill="{PANEL}" stroke="#262d36"/>')
        if k == "server":
            for j in range(5):
                p.append(f'<rect x="{ux+6+j*15}" y="{uy+6}" width="11" height="14" rx="1.5" fill="#0d1117" stroke="#2f3742"/>')
                p.append(led(ux + 11.5 + j * 15, uy + 16.5, random.choice([GREEN, GREEN, BLUE]), r=1.6))
            p.append(led(ux + uw - 22, uy + 13, GREEN))
            p.append(led(ux + uw - 12, uy + 13, random.choice([AMBER, GREEN, BLUE])))
        elif k == "switch":
            for j in range(12):
                p.append(f'<rect x="{ux+6+j*9.5}" y="{uy+8}" width="7" height="7" fill="#0d1117" stroke="#3a434e" stroke-width=".8"/>')
                p.append(led(ux + 9.5 + j * 9.5, uy + 20, random.choice([GREEN, AMBER, GREEN]), r=1.4))
            p.append(led(ux + uw - 12, uy + 13, CYAN))
        elif k == "storage":
            for j in range(8):
                p.append(f'<rect x="{ux+6+j*12}" y="{uy+5}" width="9" height="16" rx="1" fill="#0d1117" stroke="#2f3742"/>')
                p.append(led(ux + 10.5 + j * 12, uy + 9, random.choice([BLUE, PURPLE]), r=1.4))
            p.append(led(ux + uw - 12, uy + 13, PURPLE))
        else:  # ups
            p.append(f'<text x="{ux+8}" y="{uy+17}" class="mono" font-size="9" fill="{MUTED}">UPS</text>')
            p.append(f'<rect x="{ux+34}" y="{uy+9}" width="70" height="8" rx="2" fill="#0d1117" stroke="#2f3742"/>')
            p.append(f'<rect x="{ux+35}" y="{uy+10}" width="40" height="6" rx="1.5" fill="{GREEN}" opacity=".85"><animate attributeName="width" values="52;68;52" dur="4s" repeatCount="indefinite"/></rect>')
            p.append(led(ux + uw - 12, uy + 13, GREEN))
        uy += h + 4

    # title block
    tx = 285
    p.append(f'<text x="{tx}" y="62" class="mono" font-size="15" fill="{GREEN}">root@YasenMakioui:~#<tspan fill="{TEXT}"> ./boot --profile</tspan>'
             f'<tspan class="cursor" fill="{GREEN}"> █</tspan></text>')
    p.append(f'<text x="{tx-3}" y="128" class="mono" font-size="56" font-weight="800" fill="url(#title)" letter-spacing="-1">Yasen Makioui</text>')
    p.append(f'<text x="{tx}" y="162" class="mono" font-size="17" fill="{MUTED}">SRE · Platform Engineer · Packet Herder</text>')
    tags = [("linux", GREEN), ("kubernetes", BLUE), ("aws", AMBER), ("networking", CYAN), ("go", PURPLE)]
    x = tx
    for name, c in tags:
        w = 14 + len(name) * 8.6 + 14
        p.append(f'<rect x="{x}" y="178" width="{w}" height="24" rx="12" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".55"/>')
        p.append(f'<text x="{x+w/2}" y="194.5" text-anchor="middle" class="mono" font-size="12.5" fill="{c}">{name}</text>')
        x += w + 8

    # network strip
    y = 246
    p.append(f'<path id="net" d="M{rx+rw} 145 H258 V{y} H965" fill="none" stroke="#24442f" stroke-width="2"/>')
    p.append(f'<path d="M{rx+rw} 145 H258 V{y} H965" fill="none" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="3 9" opacity=".6">'
             f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur="1s" repeatCount="indefinite"/></path>')
    for i, (c, dur, rev) in enumerate([(GREEN, 4.5, False), (CYAN, 6, True), (AMBER, 5.2, False), (PINK, 7, True), (BLUE, 3.8, False)]):
        p.append(packet("net", c, dur, round(i * 0.9, 1), rev, r=3))
    nodes = [(380, "fw-01", PINK), (530, "core-sw", CYAN), (680, "lb", AMBER), (830, "eks", BLUE), (955, "s3", PURPLE)]
    for nx, label, c in nodes:
        p.append(f'<rect x="{nx-24}" y="{y-11}" width="48" height="22" rx="5" fill="{PANEL}" stroke="{c}" stroke-opacity=".8"/>')
        p.append(f'<text x="{nx}" y="{y+4}" text-anchor="middle" class="mono" font-size="10" fill="{c}">{label}</text>')
    p.append(f'<text x="{W-24}" y="36" text-anchor="end" class="mono" font-size="11" fill="{MUTED}">uptime: <tspan fill="{GREEN}">99.99%</tspan>  ·  load: <tspan fill="{AMBER}">0.42</tspan></text>')
    p.append("</svg>")
    (OUT / "header.svg").write_text("\n".join(p))


# --------------------------------------------------------------------------- terminal
ASCII = [
    " .------------------------------.",
    " | [=][=][=][=][=]   *  *  |||| |",
    " |------------------------------|",
    " | [=][=][=][=][=]   *  *  |||| |",
    " |------------------------------|",
    " | [::::::::::::::::]  *  *  >> |",
    " |------------------------------|",
    " | [=][=][=][=][=]   *  *  |||| |",
    " |------------------------------|",
    " | [##][##][##][##][##]   *  *  |",
    " |------------------------------|",
    " | UPS [||||||||||||||    ]  *  |",
    " '------------------------------'",
    "    ||                      ||",
]

INFO = [
    ("Role", "Site Reliability / Platform Engineer"),
    ("Uptime", "5+ yrs IT · before: electrical & electronics"),
    ("Kernel", "Linux. Always Linux."),
    ("Shell", "bash · go · python"),
    ("Clouds", "AWS · Hetzner · Proxmox (homelab)"),
    ("Orchestr", "Kubernetes (EKS) · ArgoCD · Karpenter"),
    ("IaC", "Terraform · SaltStack"),
    ("CI/CD", "GitLab CI"),
    ("Observ", "SigNoz · OpenTelemetry"),
    ("Network", "MikroTik RouterOS · VLANs · L2/L3"),
    ("Certs", "AWS · Terraform Assoc. · LPIC-1 · ITIL v4"),
    ("Locale", "es_ES · ca_ES · en_US"),
    ("On-call", "L2 escalation · mentoring juniors"),
]


def show(t):
    return f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'


def terminal():
    W = 1000
    lh = 22
    top = 112
    H = top + (len(INFO) + 3) * lh + 64
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f"<style>{COMMON_STYLE}</style>", "<defs>", GLOW, "</defs>",
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>',
         f'<path d="M1 13 a12 12 0 0 1 12 -12 H{W-13} a12 12 0 0 1 12 12 V38 H1 Z" fill="{PANEL}"/>',
         f'<line x1="1" y1="38" x2="{W-1}" y2="38" stroke="{BORDER}"/>',
         '<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>',
         f'<text x="{W/2}" y="24.5" text-anchor="middle" class="mono" font-size="12.5" fill="{MUTED}">yasen@homelab: ~ — ssh — 120×34</text>']

    # typed command
    cmd = "neofetch --off-the-rack"
    cw = 9.0  # approx char width at 15px
    p.append(f'<clipPath id="type"><rect x="182" y="56" width="0" height="26">'
             f'<animate attributeName="width" from="0" to="{len(cmd)*cw+4}" begin="0.4s" dur="{len(cmd)*0.05:.2f}s" fill="freeze" calcMode="discrete" '
             f'values="{";".join(str(round(i*cw,1)) for i in range(len(cmd)+1))}"/></rect></clipPath>')
    p.append(f'<text x="24" y="74" class="mono" font-size="15" fill="{GREEN}">yasen@homelab<tspan fill="{TEXT}">:</tspan><tspan fill="{BLUE}">~</tspan><tspan fill="{TEXT}">$</tspan></text>')
    p.append(f'<text x="182" y="74" class="mono" font-size="15" fill="{TEXT}" clip-path="url(#type)">{cmd}</text>')

    t0 = 0.4 + len(cmd) * 0.05 + 0.35
    # ascii rack
    for i, line in enumerate(ASCII):
        y = top + i * 20
        segs = []
        for ch in escape(line).replace(" ", " "):
            segs.append(ch)
        s = "".join(segs)
        # colour LEDs
        out = ""
        for ch in s:
            if ch == "*":
                c = random.choice([GREEN, GREEN, AMBER, BLUE])
                d = random.choice([0.5, 0.8, 1.1, 1.7])
                out += f'<tspan class="led" style="--d:{d}s" fill="{c}">●</tspan>'
            else:
                out += ch
        p.append(f'<text x="28" y="{y}" class="mono" font-size="14" fill="#3fb950" opacity="0">{out}{show(t0 + i*0.04)}</text>')

    ix, vx = 400, 510
    y = top
    p.append(f'<text x="{ix}" y="{y}" class="mono" font-size="15" font-weight="700" opacity="0" fill="{GREEN}">yasen<tspan fill="{TEXT}">@</tspan>YasenMakioui{show(t0)}</text>')
    y += lh
    p.append(f'<text x="{ix}" y="{y}" class="mono" font-size="15" opacity="0" fill="{MUTED}">{"-"*24}{show(t0+0.1)}</text>')
    for i, (k, v) in enumerate(INFO):
        y += lh
        t = t0 + 0.2 + i * 0.13
        p.append(f'<g opacity="0">{show(t)}<text x="{ix}" y="{y}" class="mono" font-size="15" font-weight="700" fill="{CYAN}">{escape(k)}</text>'
                 f'<text x="{vx}" y="{y}" class="mono" font-size="15" fill="{TEXT}">{escape(v)}</text></g>')
    y += lh + 6
    t = t0 + 0.2 + len(INFO) * 0.13
    colors = ["#484f58", PINK, GREEN, AMBER, BLUE, PURPLE, CYAN, TEXT]
    g = f'<g opacity="0">{show(t)}'
    for i, c in enumerate(colors):
        g += f'<rect x="{ix + i*30}" y="{y-12}" width="30" height="18" fill="{c}"/>'
    p.append(g + "</g>")

    y = H - 26
    p.append(f'<text x="24" y="{y}" class="mono" font-size="15" opacity="0" fill="{GREEN}">{show(t+0.3)}yasen@homelab<tspan fill="{TEXT}">:</tspan><tspan fill="{BLUE}">~</tspan><tspan fill="{TEXT}">$ </tspan>'
             f'<tspan fill="{MUTED}"># it\'s always DNS </tspan><tspan class="cursor" fill="{GREEN}">█</tspan></text>')
    p.append("</svg>")
    (OUT / "terminal.svg").write_text("\n".join(p))


# --------------------------------------------------------------------------- topology
def topology():
    W, H = 1000, 420
    cx, cy = 500, 215
    nodes = [
        # x, y, iface, label, color
        (150, 95, "eth0 · cloud", "AWS · Hetzner", AMBER),
        (500, 62, "eth1 · orchestration", "Kubernetes · ArgoCD", BLUE),
        (850, 95, "eth2 · iac / config", "Terraform · SaltStack", PURPLE),
        (150, 335, "eth3 · lang", "Go · Python · Bash", CYAN),
        (500, 370, "eth4 · net / metal", "MikroTik · Proxmox", GREEN),
        (850, 335, "eth5 · observability", "SigNoz · OpenTelemetry", PINK),
    ]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f"<style>{COMMON_STYLE}.flow{{animation:flow 1.2s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-24}}}}</style>",
         "<defs>", GLOW,
         '<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1f2730"/></pattern>',
         '<radialGradient id="halo"><stop offset="0" stop-color="#39d353" stop-opacity=".25"/><stop offset="1" stop-color="#39d353" stop-opacity="0"/></radialGradient>',
         "</defs>",
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#dots)"/>',
         f'<text x="24" y="30" class="mono" font-size="13" fill="{GREEN}">$ <tspan fill="{TEXT}">traceroute --stack yasen</tspan></text>',
         f'<text x="{W-24}" y="30" text-anchor="end" class="mono" font-size="11" fill="{MUTED}">6 hops · 0% packet loss</text>']

    # links
    for i, (x, y, _, _, c) in enumerate(nodes):
        # endpoints: node edge facing core
        nx = x + (105 if x < cx else -105 if x > cx else 0)
        ny = y + (0 if x != cx else (29 if y < cy else -29))
        sx = cx + (-80 if x < cx else 80 if x > cx else 0)
        sy = cy + (0 if x != cx else (-32 if y < cy else 32))
        if x == cx:
            d = f"M{sx} {sy} L{nx} {ny}"
        else:
            mx = (sx + nx) / 2
            d = f"M{sx} {sy} C{mx} {sy} {mx} {ny} {nx} {ny}"
        p.append(f'<path id="l{i}" d="{d}" fill="none" stroke="#252c35" stroke-width="3"/>')
        p.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="4 8" class="flow"/>')
        p.append(packet(f"l{i}", c, round(random.uniform(2.2, 3.4), 1), round(random.uniform(0, 1.5), 1), reverse=False))
        p.append(packet(f"l{i}", c, round(random.uniform(2.6, 3.8), 1), round(random.uniform(0.5, 2.0), 1), reverse=True, r=2.5))

    # core
    p.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="url(#halo)"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="{GREEN}" stroke-opacity=".5">'
             '<animate attributeName="r" values="60;105" dur="2.4s" repeatCount="indefinite"/>'
             '<animate attributeName="stroke-opacity" values=".5;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    p.append(f'<rect x="{cx-80}" y="{cy-32}" width="160" height="64" rx="10" fill="{PANEL}" stroke="{GREEN}" stroke-width="1.5"/>')
    for j in range(6):
        p.append(led(cx - 55 + j * 22, cy + 18, random.choice([GREEN, GREEN, AMBER, CYAN]), r=2.4))
    p.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="mono" font-size="17" font-weight="800" fill="{TEXT}">core-sw-01</text>')

    for x, y, iface, label, c in nodes:
        p.append(f'<rect x="{x-105}" y="{y-29}" width="210" height="58" rx="9" fill="{PANEL}" stroke="{c}" stroke-opacity=".75" stroke-width="1.3"/>')
        p.append(f'<text x="{x-92}" y="{y-8}" class="mono" font-size="10.5" fill="{c}">{iface}</text>')
        p.append(f'<text x="{x-92}" y="{y+15}" class="mono" font-size="14" font-weight="700" fill="{TEXT}">{label}</text>')
        p.append(led(x + 92, y - 12, c, r=3))
    p.append("</svg>")
    (OUT / "topology.svg").write_text("\n".join(p))


# --------------------------------------------------------------------------- divider
def divider():
    W, H = 1000, 26
    d = f"M10 13 H{W-10}"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         "<defs>", GLOW, "</defs>",
         f'<path id="d" d="{d}" stroke="#30363d" stroke-width="1.5" stroke-dasharray="2 6"/>',
         f'<circle cx="10" cy="13" r="4" fill="none" stroke="{GREEN}"/><circle cx="{W-10}" cy="13" r="4" fill="none" stroke="{GREEN}"/>']
    for i, (c, dur, rev) in enumerate([(GREEN, 6, False), (CYAN, 8, True), (AMBER, 7, False)]):
        p.append(packet("d", c, dur, i * 1.3, rev, r=3))
    p.append("</svg>")
    (OUT / "divider.svg").write_text("\n".join(p))


if __name__ == "__main__":
    header(); terminal(); topology(); divider()
    print("ok", sorted(f.name for f in OUT.iterdir()))
