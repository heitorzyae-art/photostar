#!/usr/bin/env python3
"""Draws the PhotoStar app icon: an engraving-style camera on the blue tile.

Same spec as the previous icon: 512-unit full-bleed tile (rx=112), exactly three colours
(ink, paper, PhotoStar blue), figure filling the tile, line work in the engraving style
(hatching, knurling, stipple). Original artwork, no third-party material.

    python3 make_icon.py out.svg
"""
import math
import sys

INK, PAPER, BLUE = "#0b0b0c", "#efe9dc", "#2f7bf5"
CX, CY = 256, 298          # lens centre


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def line(x1, y1, x2, y2, w, color=INK, cap="round"):
    return f'<path d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" stroke="{color}" stroke-width="{f(w)}" stroke-linecap="{cap}" fill="none"/>'


def polar(r, deg, cx=CX, cy=CY):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def radial_ticks(r1, r2, n, w, color, start=0.0, cx=CX, cy=CY, skip=lambda i: False):
    out = []
    for i in range(n):
        if skip(i):
            continue
        d = start + 360.0 * i / n
        x1, y1 = polar(r1, d, cx, cy)
        x2, y2 = polar(r2, d, cx, cy)
        out.append(line(x1, y1, x2, y2, w, color, "butt"))
    return "".join(out)


def strap(x0, y0, dx, dy, width, length):
    """Neck-strap band from a lug, running off the tile edge: outline, paper fill, stitching."""
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    hw = width / 2
    a = (x0 + px * hw, y0 + py * hw)
    b = (x0 - px * hw, y0 - py * hw)
    c = (b[0] + ux * length, b[1] + uy * length)
    d = (a[0] + ux * length, a[1] + uy * length)
    pts = " ".join(f"{f(x)} {f(y)}" for x, y in (a, b, c, d))
    out = [f'<path d="M{pts}Z" fill="{PAPER}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>']
    # edge stitching (dashed) inset from both sides
    for s in (-1, 1):
        o = hw - 9
        p1 = (x0 + px * o * s, y0 + py * o * s)
        p2 = (p1[0] + ux * length, p1[1] + uy * length)
        out.append(f'<path d="M{f(p1[0])} {f(p1[1])}L{f(p2[0])} {f(p2[1])}" stroke="{INK}" stroke-width="2.6" stroke-dasharray="9 7" fill="none"/>')
    # engraved cross-hatch near the lug end (shadow where the strap meets the camera)
    for k in range(7):
        t = 6 + k * 7
        q1 = (x0 + ux * t + px * (hw - 3), y0 + uy * t + py * (hw - 3))
        q2 = (x0 + ux * t - px * (hw - 3), y0 + uy * t - py * (hw - 3))
        out.append(line(q1[0], q1[1], q2[0], q2[1], 3.4 - k * 0.4, INK, "butt"))
    return "".join(out)


def star(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        x, y = polar(r, rot + i * 36, cx, cy)
        pts.append(f"{f(x)} {f(y)}")
    return "M" + "L".join(pts) + "Z"


def build():
    g = []
    # --- clip shapes -------------------------------------------------------------------------
    defs = (
        '<defs>'
        '<clipPath id="t"><rect width="512" height="512" rx="112"/></clipPath>'
        '<clipPath id="b"><rect x="44" y="176" width="424" height="232" rx="34"/></clipPath>'
        f'<clipPath id="l"><circle cx="{CX}" cy="{CY}" r="123"/></clipPath>'
        '</defs>'
    )
    g.append(f'<rect width="512" height="512" fill="{BLUE}"/>')

    # --- engraved field: sparse sunburst behind the camera -----------------------------------
    g.append(radial_ticks(232, 420, 72, 2.4, INK, start=2.5, cx=CX, cy=CY - 10))

    # --- straps (behind the body, running off the tile) --------------------------------------
    g.append(strap(92, 182, -0.62, -1.0, 40, 250))
    g.append(strap(420, 182, 0.62, -1.0, 40, 250))

    # --- top: prism housing, dial, shutter button --------------------------------------------
    g.append(f'<path d="M184 182L204 128Q208 116 222 116L290 116Q304 116 308 128L328 182Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    g.append(f'<path d="{star(256, 152, 17, 7.5)}" fill="{INK}"/>')                       # the "Star"
    for k in range(5):                                                                    # prism shading
        y = 134 + k * 8
        g.append(line(206 + k * 2, y, 226 + k * 1, y, 2.6, INK, "butt"))
        g.append(line(292, y, 306 - k * 2, y, 2.6, INK, "butt"))
    # mode dial (left): cylinder with knurling
    g.append(f'<rect x="84" y="142" width="70" height="40" rx="9" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>')
    for k in range(9):
        g.append(line(95 + k * 7.2, 147, 95 + k * 7.2, 177, 3.0, INK, "butt"))
    # shutter button (right): collar + button
    g.append(f'<rect x="362" y="146" width="62" height="36" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>')
    g.append(f'<ellipse cx="393" cy="146" rx="22" ry="9" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>')
    g.append(f'<ellipse cx="393" cy="144" rx="10" ry="3.6" fill="{INK}"/>')

    # --- body ---------------------------------------------------------------------------------
    g.append(f'<rect x="44" y="176" width="424" height="232" rx="34" fill="{PAPER}" stroke="{INK}" stroke-width="9"/>')
    body = []
    # leatherette stipple on both grips
    for row in range(14):
        y = 226 + row * 12
        for col in range(5):
            xl = 66 + col * 13 + (6 if row % 2 else 0)
            xr = 372 + col * 13 + (6 if row % 2 else 0)
            for x in (xl, xr):
                if 60 < x < 140 or 372 < x < 450:
                    body.append(f'<circle cx="{f(x)}" cy="{y}" r="2.3" fill="{INK}"/>')
    # engraved shading along the bottom edge: diagonal hatch, thickening downward
    for k in range(-14, 60):
        x = 30 + k * 9.2
        body.append(line(x, 408, x + 34, 366, 2.2 + 1.0 * ((k % 4) == 0), INK, "butt"))
    for k in range(6):                                                                    # bottom rule
        body.append(line(44, 396 + k * 3, 468, 396 + k * 3, 1.6 + k * 0.5, INK, "butt"))
    g.append(f'<g clip-path="url(#b)">{"".join(body)}</g>')
    # rangefinder window (left) and meter window (right)
    g.append(f'<rect x="70" y="190" width="74" height="30" rx="8" fill="{INK}"/>')
    g.append(f'<rect x="78" y="196" width="26" height="9" rx="3" fill="{BLUE}"/>')
    g.append(f'<circle cx="408" cy="205" r="15" fill="{INK}"/><circle cx="403" cy="200" r="5" fill="{PAPER}"/>')
    # body outline again on top so hatching never covers it
    g.append(f'<rect x="44" y="176" width="424" height="232" rx="34" fill="none" stroke="{INK}" stroke-width="9"/>')

    # --- lens -----------------------------------------------------------------------------------
    g.append(f'<circle cx="{CX}" cy="{CY}" r="124" fill="{PAPER}" stroke="{INK}" stroke-width="9"/>')
    # bottom-right engraved shadow on the mount
    sh = []
    for k in range(26):
        d = 20 + k * 3.0
        x1, y1 = polar(106 + 0, d)
        x2, y2 = polar(124, d)
        sh.append(line(x1, y1, x2, y2, 3.2, INK, "butt"))
    g.append(f'<g clip-path="url(#l)">{"".join(sh)}</g>')
    g.append(f'<circle cx="{CX}" cy="{CY}" r="110" fill="{INK}"/>')                      # grip ring
    g.append(radial_ticks(94, 106, 72, 4.2, PAPER, start=0))                              # knurling
    g.append(f'<circle cx="{CX}" cy="{CY}" r="90" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>')   # barrel
    # distance-scale ticks on the barrel
    g.append(radial_ticks(76, 86, 36, 2.6, INK, start=5))
    g.append(f'<circle cx="{CX}" cy="{CY}" r="70" fill="{INK}"/>')                        # lens cell
    g.append(f'<circle cx="{CX}" cy="{CY}" r="58" fill="{BLUE}"/>')                       # front glass
    for r, w in ((50, 2.6), (41, 2.6), (32, 2.6)):                                        # coating rings
        g.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}"/>')
    g.append(f'<circle cx="{CX}" cy="{CY}" r="22" fill="{INK}"/>')                        # iris
    # glass reflections
    x1, y1 = polar(46, 215)
    x2, y2 = polar(46, 262)
    g.append(f'<path d="M{f(x1)} {f(y1)}A46 46 0 0 1 {f(x2)} {f(y2)}" stroke="{PAPER}" stroke-width="7" stroke-linecap="round" fill="none"/>')
    g.append(f'<circle cx="{f(CX + 14)}" cy="{f(CY - 15)}" r="5" fill="{PAPER}"/>')
    g.append(f'<circle cx="{f(CX - 11)}" cy="{f(CY + 12)}" r="3" fill="{PAPER}"/>')

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">' + defs +
        '<g clip-path="url(#t)">' + "".join(g) + '</g></svg>\n'
    )


if __name__ == "__main__":
    open(sys.argv[1], "w", encoding="utf-8").write(build())
