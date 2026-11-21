#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page: THE WORLD, 1024x1024 PNG.

Drawn programmatically with PIL. Deterministic: same fonts, same text, same
bytes every run. No network, no randomness.

Layout is measured, not guessed: every block is drawn from a running y
cursor and each text is wrapped to its column before it is placed, so no
story can run into the one below it.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)   # cream newsprint
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 90, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def fit(draw, text, path, start, max_w):
    """Largest font size (<= start) at which text fits max_w."""
    size = start
    while size > 10 and text_w(draw, text, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(y, text, f, fill=INK, x0=0, x1=W):
    w = text_w(d, text, f)
    d.text(((x0 + x1 - w) / 2, y), text, font=f, fill=fill)


def rule(y, x0=32, x1=W - 32, width=3, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_burst(cx, cy, r, fill):
    pts = []
    for i in range(32):
        ang = math.pi * i / 16
        rr = r if i % 2 == 0 else r * 0.55
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def draw_missile(x, y, s):
    """Small horizontal missile silhouette, nose pointing right."""
    body = [(x, y - 7 * s), (x + 62 * s, y - 7 * s), (x + 78 * s, y),
            (x + 62 * s, y + 7 * s), (x, y + 7 * s)]
    d.polygon(body, fill=(60, 60, 60))
    d.polygon([(x + 8 * s, y - 7 * s), (x + 22 * s, y - 20 * s),
               (x + 30 * s, y - 7 * s)], fill=(60, 60, 60))
    d.polygon([(x + 8 * s, y + 7 * s), (x + 22 * s, y + 20 * s),
               (x + 30 * s, y + 7 * s)], fill=(60, 60, 60))
    d.polygon([(x - 2 * s, y - 5 * s), (x - 20 * s, y - 14 * s), (x - 20 * s, y),
               (x - 20 * s, y + 14 * s), (x - 2 * s, y + 5 * s)],
              fill=(230, 120, 20))


def draw_chart(x, y, w, h):
    """Falling market line on axes with a red down arrow."""
    d.line([(x, y + h), (x + w, y + h)], fill=INK, width=3)
    d.line([(x, y), (x, y + h)], fill=INK, width=3)
    pts = [(x + 8, y + 12), (x + w * 0.35, y + h * 0.35),
           (x + w * 0.6, y + h * 0.55), (x + w - 14, y + h - 10)]
    d.line(pts, fill=RED, width=6)
    ex, ey = pts[-1]
    d.polygon([(ex + 2, ey - 16), (ex + 16, ey - 2), (ex - 12, ey - 2)],
              fill=RED)


def draw_sun_globe(x, y, s):
    cx, cy, r = x + 34 * s, y + 26 * s, 20 * s
    for k in range(8):
        ang = math.pi * k / 4
        d.line([(cx + (r + 4) * math.cos(ang), cy + (r + 4) * math.sin(ang)),
                (cx + (r + 12) * math.cos(ang), cy + (r + 12) * math.sin(ang))],
               fill=(230, 140, 20), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 180, 40))
    gx, gy, gr = x + 62 * s, y + 46 * s, 17 * s
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 200))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255),
              width=2)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=(255, 255, 255), width=2)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340,
          fill=(255, 255, 255), width=2)


def draw_factory(x, y, s):
    d.rectangle([x, y + 18 * s, x + 66 * s, y + 56 * s], fill=(90, 90, 90))
    d.polygon([(x, y + 18 * s), (x + 22 * s, y + 4 * s), (x + 44 * s, y + 18 * s)],
              fill=(90, 90, 90))
    d.polygon([(x + 44 * s, y + 18 * s), (x + 66 * s, y + 4 * s),
               (x + 66 * s, y + 18 * s)], fill=(90, 90, 90))
    d.rectangle([x + 50 * s, y - 8 * s, x + 58 * s, y + 10 * s], fill=(70, 70, 70))
    f = font(SANS_B, int(30 * s))
    d.text((x + 24 * s, y + 20 * s), "$", font=f, fill=(255, 255, 255))


def draw_cross(x, y, s):
    d.rounded_rectangle([x, y, x + 56 * s, y + 56 * s], radius=8 * s,
                        fill=(178, 34, 34))
    d.rectangle([x + 24 * s, y + 10 * s, x + 32 * s, y + 46 * s],
                fill=(255, 255, 255))
    d.rectangle([x + 10 * s, y + 24 * s, x + 46 * s, y + 32 * s],
                fill=(255, 255, 255))


def draw_flame(x, y, s):
    pts = [(x + 28 * s, y), (x + 52 * s, y + 26 * s), (x + 50 * s, y + 44 * s),
           (x + 34 * s, y + 56 * s), (x + 18 * s, y + 56 * s),
           (x + 6 * s, y + 44 * s), (x + 8 * s, y + 24 * s)]
    d.polygon(pts, fill=(230, 90, 20))
    d.polygon([(x + 28 * s, y + 20 * s), (x + 40 * s, y + 36 * s),
               (x + 36 * s, y + 48 * s), (x + 22 * s, y + 48 * s),
               (x + 16 * s, y + 34 * s)], fill=(245, 180, 40))


def fit_all(draw, lines, path, start, max_w):
    """One font size (<= start) at which every line fits max_w."""
    size = start
    while size > 10 and any(
            text_w(draw, line, font(path, size)) > max_w for line in lines):
        size -= 1
    return font(path, size)


def story(x, y, col_w, kicker, lines, deck, head_start, deck_size,
          deck_leading):
    """Draw one story block; return the y just below it."""
    d.text((x, y), kicker, font=font(SANS_B, 26), fill=RED)
    y += 32
    hf = fit_all(d, lines, SERIF_B, head_start, col_w)
    for line in lines:
        d.text((x, y), line, font=hf, fill=INK)
        y += hf.size + 2
    y += 4
    df = font(SERIF, deck_size)
    for line in wrap(d, deck, df, col_w):
        d.text((x, y), line, font=df, fill=INK)
        y += deck_leading
    return y


# ---- Masthead ----
center(8, "THE WORLD", font(SERIF_B, 104))
rule(128, width=4)
rule(136, width=2)

# ---- Dateline ----
center(146, "FRIDAY, 20 NOVEMBER 2026", font(SANS_B, 40), fill=RED)
center(192, "THE DAY'S WORLD NEWS  —  IN ONE PAGE", font(SANS, 20), fill=GREY)
rule(224, width=3)

# ---- Main story: Poland (text col 32..652, icon col 700..992) ----
MX, MW = 32, 620
y = story(MX, 240, MW,
          "POLAND  —  MISSILES CROSS NATO BORDER",
          ["RUSSIAN MISSILES", "HIT POLAND"],
          "Two missiles and a drone crash in south-east Poland. "
          "Warsaw calls it a deliberate provocation; NATO jets scramble.",
          62, 26, 32)
assert y <= 492, y
draw_burst(830, 316, 52, (220, 60, 40))
draw_burst(830, 316, 30, (245, 180, 40))
draw_missile(700, 408, 1.0)
d.text((700, 440), "MISSILES DOWN", font=font(SANS_B, 20), fill=RED)
rule(492, width=3)

# ---- Second story: markets ----
y = story(MX, 508, MW,
          "MARKETS  —  AI SELL-OFF",
          ["STOCKS PLUNGE AS", "AI RALLY CRACKS"],
          "S&P 500 falls 3.7% into correction; Nikkei drops 5.1%. "
          "Nvidia faces SEC probe.",
          54, 26, 32)
assert y <= 724, y
draw_chart(700, 556, 260, 100)
d.text((700, 668), "S&P −3.7%  ·  NIKKEI −5.1%", font=font(SANS_B, 20), fill=RED)
rule(724, width=3)

# ---- Bottom row: four short items ----
COLS = [
    ("COP31", ["CLIMATE TALKS", "IN OVERTIME"],
     "Nearly 200 nations deadlocked in Antalya over a fossil-fuel deal.",
     draw_sun_globe),
    ("WASHINGTON", ["TRUMP THREATENS", "TECH TAX"],
     "A \u201ctremendous tax\u201d on US tech building AI data centers abroad.",
     draw_factory),
    ("HEALTH", ["MEASLES STATUS", "LOST"],
     "PAHO ends the status America held since 2000.",
     draw_cross),
    ("LOS ANGELES", ["PALISADES FIRE", "VERDICT"],
     "Jury convicts Rinderknecht over the 2025 fire that killed 12.",
     draw_flame),
]
col_w = (W - 64 - 3 * 24) / 4
x = 32
for kicker, head_lines, body, icon in COLS:
    d.text((x, 740), kicker, font=font(SANS_B, 22), fill=RED)
    icon(x + 8, 768, 0.85)
    hy = 820
    hf = fit_all(d, head_lines, SANS_B, 23, col_w)
    for line in head_lines:
        d.text((x, hy), line, font=hf, fill=INK)
        hy += hf.size + 3
    by = hy + 4
    bf = font(SERIF, 18)
    for line in wrap(d, body, bf, col_w):
        d.text((x, by), line, font=bf, fill=INK)
        by += 23
    assert by <= 952, (kicker, by)
    x += col_w + 24

# ---- Also strip + footer ----
center(958, "ALSO: Anthropic up 17% on IPO debut  ·  EU–UK food and carbon "
            "deals  ·  6.7 quake in Peru",
       font(SANS, 19), fill=GREY)
rule(988, width=2)
center(994, "THE WORLD  ·  FRIDAY 20 NOVEMBER 2026", font(SANS, 18), fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20nov/entry.png",
         format="PNG", optimize=True)
print("saved entry.png")
