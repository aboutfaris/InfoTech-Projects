#!/usr/bin/env python3
"""InfoTech Set 01 diagram: Azure Windows 10 VM web stack for osTicket.

Built from the repo-level assets/architecture_diagram.py: same helpers and layout
checks; only the EDIT blocks (canvas text, grid, groups, nodes, connections,
badges, legend steps) differ. Azure boundary, official Azure icons from the
`diagrams` package, stroke-only outline glyphs where no official icon fits.

Run:  .venv/bin/python architecture_diagram.py <path>/architecture
It writes architecture.svg and architecture.png (rendered at 2x) and must print
"layout problems: none".
"""
import base64
import os
import subprocess
import sys

import diagrams

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#8C4FFF")
ICON, HALF = 52, 26
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "Azure or app connection"),
    "external": (LINE, 1.6, "6 5", "ah", "Remote Desktop"),
    "business": (ACCENT, 2.2, None, "ahb", "Ticket lifecycle"),
}

# ---------------- canvas text ----------------
W, H = 1600, 760
TITLE = "InfoTech Set 01 | osTicket prerequisites and installation"
SUBTITLE = ("One Windows 10 VM in Azure runs IIS with CGI, PHP 7.3.8, and MySQL 5.5.62; "
            "a fresh osTicket install connects to its database.")
REGION = "resource group osTickets, East US"

out, icons, SEGS, BADGES, GRECTS = [], [], [], [], []
N, BOX, USED = {}, {}, set()


def add(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est_w(s, size):
    return len(s) * size * 0.53


def text(x, y, s, size=13, weight=400, color=INK, anchor="middle", halo=False):
    h = (' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
         if halo else "")
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{h}>{esc(s)}</text>')


_cache = {}


def data(rel):
    if rel not in _cache:
        with open(os.path.join(R, rel), "rb") as fh:
            _cache[rel] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
    return _cache[rel]


# Stroke-only outline glyphs (52 px box, local coordinates) for software with no
# official icon. Generic shapes only, never a product logo.
GLYPHS = {
    "server": '<rect x="8" y="8" width="36" height="15" rx="2"/>'
              '<rect x="8" y="29" width="36" height="15" rx="2"/>'
              '<path d="M15,15.5 H17 M15,36.5 H17 M24,15.5 H37 M24,36.5 H37"/>',
    "code": '<rect x="4" y="8" width="44" height="36" rx="3"/><path d="M4,16 H48"/>'
            '<path d="M18,24 L12,30 L18,36 M34,24 L40,30 L34,36 M29,22 L23,38"/>',
    "webapp": '<rect x="4" y="8" width="44" height="36" rx="3"/><path d="M4,16 H48"/>'
              '<rect x="13" y="23" width="26" height="14" rx="1.5"/>'
              '<path d="M31,23 V37" stroke-dasharray="2 2"/>',
    "db": '<ellipse cx="26" cy="12" rx="18" ry="6"/>'
          '<path d="M8,12 V40 A18,6 0 0 0 44,40 V12 M8,26 A18,6 0 0 0 44,26"/>',
    "monitor": '<rect x="6" y="8" width="40" height="28" rx="2"/>'
               '<path d="M26,36 V44 M16,44 H36 M14,18 H30 M14,25 H24"/>',
    "shield": '<path d="M26,6 L44,12 V26 C44,36 36,43 26,47 C16,43 8,36 8,26 V12 Z"/>'
              '<path d="M18,26 L24,32 L34,20"/>',
    "people": '<circle cx="19" cy="18" r="6"/><path d="M7,43 C7,31 31,31 31,43"/>'
              '<circle cx="35" cy="15" r="5"/><path d="M29,29 C33,26 45,27 45,38"/>',
    "agent": '<circle cx="26" cy="17" r="8"/><path d="M10,46 C10,32 42,32 42,46"/>'
             '<path d="M15,19 V15 A11,11 0 0 1 37,15 V19"/>',
    "person": '<circle cx="26" cy="16" r="8"/><path d="M10,46 C10,32 42,32 42,46"/>',
    "clock": '<circle cx="26" cy="26" r="19"/><path d="M26,14 V26 L34,31"/>',
    "tag": '<path d="M6,10 H26 L46,30 L30,46 L6,22 Z"/><circle cx="15" cy="19" r="3"/>',
    "inbox": '<path d="M6,28 L12,10 H40 L46,28 V42 H6 Z"/>'
             '<path d="M6,28 H18 L21,33 H31 L34,28 H46"/>',
    "chat": '<path d="M6,10 H46 V34 H22 L12,43 V34 H6 Z"/><path d="M14,19 H38 M14,26 H30"/>',
    "notes": '<path d="M12,6 H34 L42,14 V46 H12 Z M34,6 V14 H42"/>'
             '<path d="M18,22 H36 M18,29 H36 M18,36 H30"/>',
    "check": '<circle cx="26" cy="26" r="19"/><path d="M17,26 L24,33 L36,19"/>',
    "laptop": '<rect x="10" y="10" width="32" height="23" rx="2"/>'
              '<path d="M5,37 H47 L44,42 H8 Z"/>',
}


def node(key, rel, cx, cy, l1, l2=None):
    """Register an icon (file path, or 'glyph:<name>') at slot (cx, cy)."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
        if rel.startswith("glyph:"):
            add(f'<g transform="translate({cx-HALF},{cy-HALF})" fill="none" stroke="{LINE}" '
                f'stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">'
                f'{GLYPHS[rel[6:]]}</g>')
        else:
            add(f'<image x="{cx-HALF}" y="{cy-HALF}" width="{ICON}" height="{ICON}" '
                f'xlink:href="{data(rel)}"/>')
        text(cx, cy + HALF + 17, l1, 13, 400, INK)
        if l2:
            text(cx, cy + HALF + 32, l2, 12, 400, TEXT2)


def port(key, side, gap=5):
    """Connection point: l, r, t (top edge of icon), b (below the label block)."""
    cx, cy, n = N[key]
    return {"l": (cx - HALF - gap, cy), "r": (cx + HALF + gap, cy),
            "t": (cx, cy - HALF - gap),
            "b": (cx, cy + HALF + (36 if n == 2 else 21) + gap)}[side]


def path(pts, a, b, kind="service"):
    color, width, dash, marker, _ = KINDS[kind]
    USED.add(kind)
    for p, q in zip(pts, pts[1:]):
        assert p[0] == q[0] or p[1] == q[1], ("diagonal segment", a, b, p, q)
        SEGS.append((p, q, a, b))
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
        f'marker-end="url(#{marker})"/>')


def link(a, sa, b, sb, kind="service", via=None):
    """Connect two nodes. via = elbow points; every segment must be horizontal or vertical."""
    path([port(a, sa)] + (via or []) + [port(b, sb)], a, b, kind)


def badge(cx, cy, n, record=True):
    if record:
        BADGES.append((cx, cy, n))
    add(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="{BADGE}"/>')
    text(cx, cy + 4.6, str(n), 13, 700, "#FFFFFF")


def group(x0, y0, x1, y1, title):
    GRECTS.append((x0, y0, x1, y1))
    add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" '
        f'stroke="{GROUP}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    text(x0 + 14, y0 + 25, title, 14.5, 700, INK, "start")


# ---------------- grid ----------------
AX0, AX1, AY0, AY1 = 190, 1570, 110, 500             # Azure boundary
COLS = [(220, 636), (672, 1088), (1124, 1540)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
ROWS = [(150, 470)]                                   # one group row
A1, B1 = 250, 380                                     # icon lanes (center y)
XL = 95                                               # external column
# ---------------- canvas and Azure boundary ----------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
    '<marker id="ahb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" '
    f'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
text(40, 56, TITLE, 26, 700, INK, "start")
text(40, 82, SUBTITLE, 14, 400, TEXT2, "start")
add(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" fill="none" '
    f'stroke="{INK}" stroke-width="1.6"/>')
add(f'<image x="{AX0+4}" y="{AY0+4}" width="26" height="26" '
    f'xlink:href="{data("azure/azure.png")}"/>')
add(f'<text x="{AX0+40}" y="{AY0+22}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">Microsoft Azure<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

GLYPHS.update({
    "org": '<rect x="18" y="6" width="16" height="11" rx="1.5"/>'
           '<rect x="4" y="35" width="16" height="11" rx="1.5"/>'
           '<rect x="32" y="35" width="16" height="11" rx="1.5"/>'
           '<path d="M26,17 V26 M12,26 H40 M12,26 V35 M40,26 V35"/>',
    "form": '<rect x="8" y="6" width="36" height="40" rx="2"/>'
            '<rect x="14" y="13" width="8" height="8" rx="1"/>'
            '<path d="M16,17 L18,19 L21,14 M27,17 H38 M14,29 H38 M14,36 H32"/>',
    "gear": '<circle cx="26" cy="26" r="9"/><circle cx="26" cy="26" r="3"/>'
            '<path d="M26,6 V15 M26,37 V46 M6,26 H15 M37,26 H46 '
            'M12,12 L18,18 M34,34 L40,40 M40,12 L34,18 M18,34 L12,40"/>',
    "browser": '<rect x="4" y="8" width="44" height="36" rx="3"/><path d="M4,17 H48"/>'
               '<circle cx="10" cy="12.5" r="1.5"/><circle cx="15.5" cy="12.5" r="1.5"/>'
               '<path d="M12,27 H40 M12,34 H30"/>',
})

# ---------------- groups ----------------
group(COLS[0][0], ROWS[0][0], COLS[0][1], ROWS[0][1], "Azure VM and networking")
group(COLS[1][0], ROWS[0][0], COLS[1][1], ROWS[0][1], "On the VM: IIS, PHP, osTicket")
group(COLS[2][0], ROWS[0][0], COLS[2][1], ROWS[0][1], "On the VM: MySQL database")

# ---------------- nodes ----------------
G = "glyph:"
node("comp", G + "laptop", XL, A1, "Your computer", "Remote Desktop")
# Azure VM and the resources Azure created with it
node("pip", "azure/network/public-ip-addresses.png", SL[0][0], A1, "Public IP", "RDP entry point")
node("vm", "azure/compute/vm-windows.png", SL[0][2], A1, "VM-osTicket", "Windows 10 Pro")
node("nsg", "azure/networking/network-security-groups.png", SL[0][0], B1,
     "Security group", "created with VM")
node("nic", "azure/network/network-interfaces.png", SL[0][1], B1,
     "Network interface", "created with VM")
node("vnet", "azure/network/virtual-networks.png", SL[0][2], B1,
     "Virtual network", "created with VM")
# IIS, PHP, osTicket
node("iis", G + "server", SL[1][0], A1, "IIS", "CGI enabled")
node("php", G + "code", SL[1][1], A1, "PHP 7.3.8", "php-cgi.exe")
node("ost", G + "webapp", SL[1][2], A1, "osTicket", "Default Web Site")
node("phpmgr", G + "gear", SL[1][1], B1, "PHP Manager", "imap, intl, opcache")
node("browser", G + "browser", SL[1][2], B1, "Browser on VM", "Browse *:80")
# MySQL database
node("mysql", G + "db", SL[2][1], A1, "MySQL 5.5.62", "database osTicket")
node("heidi", G + "monitor", SL[2][1], B1, "HeidiSQL", "root session")

# ---------------- connections ----------------
link("comp", "r", "pip", "l", "external")
link("pip", "r", "vm", "l")
link("vm", "r", "iis", "l")
link("iis", "r", "php", "l")
link("php", "r", "ost", "l")
link("phpmgr", "t", "php", "b")
link("browser", "t", "ost", "b")
link("heidi", "t", "mysql", "b")
link("ost", "r", "mysql", "l")

# ---------------- line labels (white halo keeps them readable over lines) ----------------
text((SL[1][0] + SL[1][1]) / 2, A1 - 8, "CGI", 11.5, 400, TEXT2, halo=True)
text(1215, A1 - 8, "database settings", 11.5, 400, TEXT2, halo=True)

draw_nodes()

# ---------------- step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(165, 222, 1), (654, 222, 2), (910, 333, 3), (1035, 333, 4),
                  (1362, 333, 5), (1106, 222, 6)]:
    badge(cx, cy, n)

# ---------------- legend steps, one short sentence each, same order as the badges ----------------
LY = 580
STEPS = [
    "Create VM-osTicket in East US; Remote Desktop reaches it through its public IP.",
    "On the VM, turn on IIS with CGI under Turn Windows features on or off.",
    "PHP Manager registers C:\\PHP\\php-cgi.exe in IIS and enables imap, intl, and opcache.",
    "Browse *:80 opens the osTicket installer; ost-sampleconfig.php becomes ost-config.php.",
    "HeidiSQL opens a root session to MySQL 5.5.62 and creates the osTicket database.",
    "The installer connects osTicket to that database as root; Install Now finishes setup.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 770, LY + 34 + row * 32
    badge(bx, by, i + 1, record=False)
    text(bx + 22, by + 4.6, s, 13.5, 400, INK, "start")

# line-style key, one entry per line kind actually used
KEY_Y = LY + 40 + per_col * 32
lx = 40
for k, (color, width, dash, marker, label) in KINDS.items():
    if k not in USED:
        continue
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="M {lx},{KEY_Y} L {lx+52},{KEY_Y}" stroke="{color}" stroke-width="{width}"'
        f'{da} marker-end="url(#{marker})"/>')
    text(lx + 62, KEY_Y + 4.5, label, 12.5, 400, TEXT2, "start")
    lx += 62 + est_w(label, 12.5) + 48
add("</svg>")
assert KEY_Y + 30 <= H, "canvas too short for the legend: raise H"


# ---------------- checks: keep all of them ----------------
def seg_hits_box(p, q, box, pad=2):
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if ay == by:
        lo, hi = sorted((ax, bx))
        return y0 - pad < ay < y1 + pad and lo < x1 + pad and hi > x0 - pad
    lo, hi = sorted((ay, by))
    return x0 - pad < ax < x1 + pad and lo < y1 + pad and hi > y0 - pad


def boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def crossings():
    hs = [s for s in SEGS if s[0][1] == s[1][1]]
    vs = [s for s in SEGS if s[0][0] == s[1][0]]
    found = []
    for hp, hq, ha, hb in hs:
        y = hp[1]
        x0, x1 = sorted((hp[0], hq[0]))
        for vp, vq, va, vb in vs:
            if (ha, hb) == (va, vb):
                continue
            x = vp[0]
            y0, y1 = sorted((vp[1], vq[1]))
            if x0 < x < x1 and y0 < y < y1:
                found.append(f"{ha}->{hb} x {va}->{vb}")
    return found


def shared_segments():
    found = []
    for i in range(len(SEGS)):
        for j in range(i + 1, len(SEGS)):
            (p, q, a, b), (r, s, c, d) = SEGS[i], SEGS[j]
            if (a, b) == (c, d):
                continue
            if p[1] == q[1] == r[1] == s[1]:
                lo1, hi1 = sorted((p[0], q[0]))
                lo2, hi2 = sorted((r[0], s[0]))
            elif p[0] == q[0] == r[0] == s[0]:
                lo1, hi1 = sorted((p[1], q[1]))
                lo2, hi2 = sorted((r[1], s[1]))
            else:
                continue
            if min(hi1, hi2) - max(lo1, lo2) > 0:
                found.append(f"{a}->{b} shares a segment with {c}->{d}")
    return found


problems = []
for p, q, a, b in SEGS:
    for k, box in BOX.items():
        if k not in (a, b) and seg_hits_box(p, q, box):
            problems.append(f"line {a}->{b} crosses {k}")
keys = list(BOX)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if boxes_overlap(BOX[keys[i]], BOX[keys[j]]):
            problems.append(f"label overlap {keys[i]} / {keys[j]}")
for cx, cy, n in BADGES:
    bb = (cx - 12, cy - 12, cx + 12, cy + 12)
    for p, q, a, b in SEGS:
        if seg_hits_box(p, q, bb, pad=1):
            problems.append(f"badge {n} sits on line {a}->{b}")
    for k, box in BOX.items():
        if boxes_overlap(bb, box):
            problems.append(f"badge {n} overlaps {k}")
for k, (x0, y0, x1, y1) in BOX.items():
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    for gx0, gy0, gx1, gy1 in GRECTS:
        if gx0 < mx < gx1 and gy0 < my < gy1 and (
                x0 < gx0 + 4 or x1 > gx1 - 4 or y0 < gy0 + 34 or y1 > gy1 - 4):
            problems.append(f"label of {k} touches its group border or title")
problems += shared_segments()
X = crossings()
if len(X) > 2:
    problems.append(f"{len(X)} line crossings (2 at most, only where unavoidable)")

svg = "\n".join(out)
assert "\u2014" not in svg and "\u2013" not in svg, "em or en dash found"
with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", "2", "-o", OUT_PNG, OUT_SVG], check=True)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
