#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Tuesday, 24 November 2026.

Every story on the page was first reported on 24 November 2026
(Reuters, AP, BBC, France 24). The picture is drawn entirely with
Pillow primitives and DejaVu fonts: no photographs, no borrowed art.
Output: entry.png, 1024 x 1024, well under 1 MiB.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
STEEL = (70, 96, 122)
GOLD = (196, 148, 32)
SEA = (38, 84, 138)
SKY = (214, 228, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y just below it."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fill=RED):
    draw.text((x, y), text.upper(), font=SANS_B(17), fill=fill)
    return y + 24


def headline(draw, x, y, text, size, width, fill=INK):
    fnt = SERIF_B(size)
    y2 = para(draw, x, y, text, fnt, width, fill=fill,
              leading=int(size * 1.12))
    return y2


def draw_ship_scene(draw, x, y, w, h):
    """A Libyan harbour at dusk: sea, a grey warship, an explosion burst
    and small naval drones overhead. All Pillow primitives."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun low on the horizon
    draw.ellipse([x + w - 110, y + 26, x + w - 46, y + 90], fill=(232, 178, 84))
    # distant harbour cranes and rooftops
    draw.rectangle([x + 20, y + h - 150, x + 150, y + h - 118], fill=(120, 128, 138))
    for cx in (x + 40, x + 90, x + 130):
        draw.line([(cx, y + h - 150), (cx, y + h - 118)], fill=(90, 98, 110), width=4)
        draw.line([(cx, y + h - 150), (cx + 26, y + h - 150)], fill=(90, 98, 110), width=4)
    # sea
    draw.rectangle([x, y + h - 118, x + w, y + h], fill=SEA)
    for wy in range(y + h - 104, y + h - 8, 18):
        draw.line([(x + 14, wy), (x + w - 14, wy)], fill=(90, 140, 190), width=2)
    # warship hull and superstructure, listing slightly
    hx, hy = x + 150, y + h - 118
    draw.polygon([(hx, hy), (hx + 300, hy), (hx + 330, hy - 34),
                  (hx + 330, hy - 58), (hx + 30, hy - 58), (hx, hy)],
                 fill=(96, 104, 112))
    draw.rectangle([hx + 90, hy - 92, hx + 210, hy - 58], fill=(80, 88, 98))
    draw.rectangle([hx + 118, hy - 118, hx + 182, hy - 92], fill=(70, 78, 88))
    draw.line([(hx + 150, hy - 92), (hx + 150, hy - 108)], fill=(80, 88, 98), width=6)
    # funnel smoke
    for i, r in enumerate((14, 11, 8)):
        draw.ellipse([hx + 220 + i * 22, hy - 96 - i * 6,
                      hx + 220 + i * 22 + r * 2, hy - 96 - i * 6 + r * 2],
                     fill=(150, 150, 148))
    # explosion burst over the stern
    bx, by = hx + 300, hy - 52
    for r, col in ((44, (255, 176, 32)), (30, (255, 120, 24)), (16, (255, 214, 96))):
        pts = []
        for k in range(12):
            ang = k * 3.14159 / 6
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((bx + rr * math.cos(ang),
                        by + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)
    # two naval drones skimming the water
    for dx, dy in ((x + 60, y + h - 70), (x + 420, y + h - 46)):
        draw.ellipse([dx, dy, dx + 34, dy + 12], fill=(40, 44, 50))
        draw.line([(dx + 6, dy + 6), (dx - 14, dy + 2)], fill=(40, 44, 50), width=3)
        draw.line([(dx + 28, dy + 6), (dx + 48, dy + 2)], fill=(40, 44, 50), width=3)
    # caption strip
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(22, 22, 22))
    draw.text((x + 12, y + h - 22),
              "A Russian corvette burns in a Libyan port after a Ukrainian drone strike.",
              font=SANS(15), fill=(240, 240, 240))


def draw_chip(draw, cx, cy, s):
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(30, 30, 34))
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                   fill=(196, 148, 32))
    for i in range(3):
        off = (i - 1) * s // 4
        draw.line([(cx + off, cy - s // 2 - 10), (cx + off, cy - s // 2)], fill=INK, width=3)
        draw.line([(cx + off, cy + s // 2), (cx + off, cy + s // 2 + 10)], fill=INK, width=3)
        draw.line([(cx - s // 2 - 10, cy + off), (cx - s // 2, cy + off)], fill=INK, width=3)
        draw.line([(cx + s // 2, cy + off), (cx + s // 2 + 10, cy + off)], fill=INK, width=3)


def draw_globe(draw, cx, cy, s):
    r = s // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 84, 138))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(22, 22, 22), width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(120, 200, 120), width=10)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 110, fill=(120, 200, 120), width=10)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(120, 200, 120), width=8)
    # crack through the middle: talks break down
    draw.line([(cx - 6, cy - r), (cx + 8, cy - r // 3), (cx - 8, cy + r // 3),
               (cx + 6, cy + r)], fill=(255, 214, 96), width=5)


def draw_ballot(draw, cx, cy, s):
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   outline=INK, width=4, fill=(255, 255, 255))
    draw.rectangle([cx - s // 4, cy - 4, cx + s // 4, cy + 4], fill=INK)
    draw.line([(cx - s // 2 - 6, cy - s // 2 - 8), (cx - 4, cy - s // 2 + 6),
               (cx + s // 2 + 6, cy - s // 2 - 14)], fill=RED, width=7)


def draw_ban(draw, cx, cy, s):
    """A prohibition sign: red ring with a diagonal bar (sanctions)."""
    r = s // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=6)
    draw.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)],
              fill=RED, width=6)


def draw_warning(draw, cx, cy, s):
    """A warning triangle with an exclamation mark."""
    draw.polygon([(cx, cy - s), (cx + s * 0.7, cy + s * 0.6),
                  (cx - s * 0.7, cy + s * 0.6)],
                 fill=GOLD, outline=INK)
    draw.text((cx, cy - s * 0.1), "!", font=SANS_B(30), fill=INK, anchor="ma")


def draw_flame(draw, cx, cy, s):
    pts = [(cx, cy - s), (cx + s * 0.55, cy - s * 0.25), (cx + s * 0.7, cy + s * 0.3),
           (cx + s * 0.3, cy + s * 0.75), (cx - s * 0.3, cy + s * 0.75),
           (cx - s * 0.7, cy + s * 0.3), (cx - s * 0.55, cy - s * 0.25)]
    draw.polygon(pts, fill=(230, 90, 20))
    draw.polygon([(cx, cy - s * 0.45), (cx + s * 0.3, cy + s * 0.1),
                  (cx, cy + s * 0.55), (cx - s * 0.3, cy + s * 0.1)],
                 fill=(255, 200, 60))


def draw_flag(draw, cx, cy, s):
    draw.line([(cx - s // 2, cy - s // 2), (cx - s // 2, cy + s // 2)],
              fill=INK, width=4)
    draw.polygon([(cx - s // 2, cy - s // 2), (cx + s // 2, cy - s // 2 + 12),
                  (cx - s // 2, cy - s // 2 + 26)], fill=BLUE)
    draw.polygon([(cx - s // 2, cy - s // 2 + 26), (cx + s // 2, cy - s // 2 + 38),
                  (cx - s // 2, cy - s // 2 + 52)], fill=(255, 255, 255))
    draw.polygon([(cx - s // 2, cy - s // 2 + 52), (cx + s // 2, cy - s // 2 + 64),
                  (cx - s // 2, cy - s // 2 + 78)], fill=RED)


def story_block(draw, x, y, w, icon, kick, head, body, hsize=30):
    """A small story: icon on the left, kicker, headline, standfirst."""
    y = kicker(draw, x + 96, y, kick)
    icon(draw, x + 44, y + 8, 64)
    y = headline(draw, x + 96, y, head, hsize, w - 96)
    y = para(draw, x + 96, y + 4, body, SANS(18), w - 96)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    d.text((W // 2, 18), "THE WORLD", font=SERIF_B(96), fill=INK, anchor="ma")
    rule(d, M, 128, W - M, 4)
    d.text((W // 2, 140), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(30),
           fill=RED, anchor="ma")
    d.text((W // 2, 178), "One day's world news, in one picture  •  Price: one careful look",
           font=SANS(18), fill=(90, 90, 90), anchor="ma")
    rule(d, M, 210, W - M, 2)

    # ---- Lead story: Ukraine drones sink Russian warship ----
    ly = 228
    draw_ship_scene(d, M, ly, 600, 220)
    y = ly + 236
    y = kicker(d, M, y, "Lead story — Ukraine war")
    y = headline(d, M, y, "UKRAINE'S DRONES SINK RUSSIAN WARSHIP IN LIBYA", 40, 600)
    y = para(d, M, y + 6,
             "President Volodymyr Zelenskyy said Ukrainian naval drones sank a "
             "Russian corvette in a Libyan port, a day after a drone hit a "
             "Russian-linked ship in the Gulf of Finland. (Reuters, BBC)",
             SANS(20), 600)
    rule(d, M, y + 14, M + 600, 2)

    # ---- Right column: Megaspeed blacklist + EU sanctions ----
    rx, rw = M + 624, 328
    y = ly
    y = story_block(d, rx, y, rw, draw_chip, "Business — Tech",
                    "US BLACKLISTS MEGASPEED",
                    "Washington blacklisted Singapore chip firm Megaspeed over "
                    "the Nvidia chip scandal. (Reuters)", 28)
    rule(d, rx, y + 12, rx + rw, 2)
    y = story_block(d, rx, y + 28, rw, draw_ban, "Europe — Sanctions",
                    "EU UNVEILS NEW RUSSIA SANCTIONS",
                    "Brussels unveiled a new package hitting banks, the shadow "
                    "fleet and athletes. (Reuters)", 28)
    rule(d, rx, y + 12, rx + rw, 2)

    # ---- Bottom row: three stories ----
    by = 740
    rule(d, M, by - 14, W - M, 2)
    col_w = (W - 2 * M - 48) // 3
    xs = [M, M + col_w + 24, M + 2 * (col_w + 24)]
    stories = [
        (draw_warning, "Ukraine war",
         "ZELENSKY WARNS OF NEW STRIKES",
         "Zelenskyy said intelligence shows Russia is preparing new strikes "
         "on Ukraine. (Reuters)"),
        (draw_flame, "Asia — Indonesia",
         "24 DEAD IN FACTORY FIRE",
         "At least 24 people died in a blaze at a factory in Indonesia; "
         "dozens are still missing. (Reuters)"),
        (draw_flag, "Europe — Baltic",
         "MOSCOW WARNS ESTONIA",
         "Russia accused Estonia of hostile acts on the 'verge of triggering "
         "open war'. (Reuters)"),
    ]
    for x, (icon, kick, head, body) in zip(xs, stories):
        y = by
        y = kicker(d, x, y, kick)
        icon(d, x + 30, y + 44, 44)
        y = headline(d, x + 84, y, head, 26, col_w - 84)
        y = para(d, x, y + 6, body, SANS(18), col_w)

    # ---- Footer ----
    rule(d, M, 952, W - M, 2)
    d.text((W // 2, 962),
           "Sources: Reuters • Associated Press • BBC • France 24  —  All stories first reported 24 November 2026",
           font=SANS(16), fill=(90, 90, 90), anchor="ma")

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), optimize=True)
    print("wrote", os.path.join(out, "entry.png"), img.size)


if __name__ == "__main__":
    main()
